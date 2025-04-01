# ruff: noqa: F821

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# For managing and launching Ray Cluster

import base64
import getpass
import json
import logging
import platform
import re
import sys
import tempfile
import time
from collections import Counter
from typing import Any

import attrs
import kubernetes
import kubernetes.client.exceptions
import pyarrow as pa
import ray

# do global config init
from kubernetes import config as kube_config
from kubernetes.client.api import core_v1_api

import geneva
from geneva.config import ConfigBase
from geneva.packager.autodetect import upload_local_env

kube_config.load_config()

_LOG = logging.getLogger(__name__)

GENEVA_RAY_HEAD_NODE = "geneva.lancedb.com/ray-head"
GENEVA_RAY_CPU_NODE = "geneva.lancedb.com/ray-worker-cpu"
GENEVA_RAY_GPU_NODE = "geneva.lancedb.com/ray-worker-gpu"


@attrs.define
class _RayClusterConfig(ConfigBase):
    user: str = attrs.field(
        converter=attrs.converters.default_if_none(default=getpass.getuser())
    )

    namespace: str = attrs.field(
        converter=attrs.converters.default_if_none(default="geneva")
    )

    @classmethod
    def name(cls) -> str:
        return "raycluster"

    def cluster_name(self) -> str:
        if self.user:
            return self.user
        _LOG.info("Using the current OS user name as the cluster name")
        return getpass.getuser()


def _size_converter(value: int | str) -> int:
    if isinstance(value, int):
        return value
    suffixes = {
        "K": 1000,
        "M": 1000**2,
        "G": 1000**3,
        "T": 1000**4,
        "Ki": 1024,
        "Mi": 1024**2,
        "Gi": 1024**3,
        "Ti": 1024**4,
    }
    match = re.match(r"(?P<value>\d+)(?P<unit>[KMGT]i?)", value)
    value = int(match.group("value"))
    unit = suffixes[match.group("unit")]

    return value * unit


@attrs.define(kw_only=True, slots=False)
class _ResrouceMixin:
    num_cpus: int = attrs.field(default=1, validator=attrs.validators.gt(0))
    memory: int = attrs.field(
        converter=_size_converter,
        default=2 * (1024**3),
        validator=attrs.validators.gt(0),
    )
    num_gpus: int = attrs.field(default=0, validator=attrs.validators.ge(0))

    arm: bool = attrs.field(default=platform.processor() == "aarch64")

    @property
    def _resources(self) -> dict:
        resource = {
            "requests": {
                "cpu": self.num_cpus,
                "memory": self.memory,
            },
            "limits": {
                "cpu": self.num_cpus,
                "memory": self.memory,
            },
        }

        if self.num_gpus:
            resource["requests"]["nvidia.com/gpu"] = self.num_gpus
            resource["limits"]["nvidia.com/gpu"] = self.num_gpus

        return resource


@attrs.define(kw_only=True, slots=False)
class _RayVersionMixin:
    ray_version: str = attrs.field(init=False)
    """
    The version of Ray to use for the cluster. Auto detected from the Ray
    package version in the current environment.
    """

    @ray_version.default
    def _default_ray_version(self) -> str:
        return ray.__version__


@attrs.define(kw_only=True, slots=False)
class _PythonVersionMixin:
    python_version: str = attrs.field(init=False)
    """
    The major.minor version of Python to use for the cluster.
    Auto detected from the python version in the current environment.
    """

    @python_version.default
    def _default_python_version(self) -> str:
        return f"{sys.version_info.major}.{sys.version_info.minor}"


def get_ray_image(
    version: str, python_version: str, *, gpu: bool = False, arm: bool = False
) -> str:
    py_version = python_version.replace(".", "")
    image = f"rayproject/ray:{version}-py{py_version}"
    if gpu:
        image += "-gpu"
    if arm:
        image += "-aarch64"
    return image


@attrs.define(kw_only=True, slots=False)
class _ImageMixin(_RayVersionMixin, _PythonVersionMixin, _ResrouceMixin):
    # set a dummpy default so the generated __init__
    # gets the correct signature
    image: str = attrs.field(default="_DEFUALT_IMAGE")

    def __attrs_post_init__(self) -> None:
        if self.image == "_DEFUALT_IMAGE":
            self.image = get_ray_image(
                self.ray_version,
                self.python_version,
                gpu=self.num_gpus > 0,
                arm=self.arm,
            )


@attrs.define(kw_only=True, slots=False)
class _MountsMixin:
    volumes: dict[str, dict] = attrs.field(default={})
    """
    Volumes to attach to the worker Pod.

    The key is the name of the volume and the value is the volume specification.
    """

    mounts: list[tuple[str, str]] = attrs.field(default=[])
    """
    The list of mounts to attach to the worker containers.
    """

    @mounts.validator
    def _validate_mounts(self, attribute: str, value: list[tuple[str, str]]) -> None:
        paths = set()
        for name, path in value:
            if name not in self.volumes:
                raise ValueError(f"Volume {name} not found in volumes")
            paths.add(path)

        if len(paths) != len(value):
            dups = [
                item
                for item, count in Counter(path for _, path in value).items()
                if count > 1
            ]
            raise ValueError(f"Duplicate mount paths: {dups}")

    @property
    def mounts_definition(self) -> list[dict[str, str]]:
        return [{"name": volume, "mountPath": path} for volume, path in self.mounts]

    @property
    def volume_definition(self) -> list[dict[str, str]]:
        return [{"name": volume, **config} for volume, config in self.volumes.items()]


@attrs.define(kw_only=True)
class _HeadGroupSpec(_ImageMixin, _ResrouceMixin, _MountsMixin):
    node_selector: dict[str, str] = attrs.field(default={"_PLACEHOLDER": "true"})

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        if self.node_selector == {"_PLACEHOLDER": "true"}:
            self.node_selector = {GENEVA_RAY_HEAD_NODE: ""}

    @property
    def _ports(self) -> list[dict]:
        return [
            {
                "containerPort": 10001,
                "name": "client",
                "protocol": "TCP",
            },
            {
                "containerPort": 8265,
                "name": "dashboard",
                "protocol": "TCP",
            },
            {
                "containerPort": 6379,
                "name": "gsc-server",
                "protocol": "TCP",
            },
        ]

    @property
    def definition(self) -> dict:
        definition = {
            "rayStartParams": {
                # do not schedule tasks onto the head node this prevents cluster
                # crashes due to other tasks killing the head node
                "num-cpus": "0"
            },
            "template": {
                "spec": {
                    "containers": [
                        {
                            "name": "ray-head",
                            "image": self.image,
                            "imagePullPolicy": "IfNotPresent",
                            "resources": self._resources,
                            "ports": self._ports,
                            "volumeMounts": self.mounts_definition,
                        }
                    ],
                    "volumes": self.volume_definition,
                    "nodeSelector": self.node_selector,
                }
            },
        }

        return definition


@attrs.define(kw_only=True)
class _WorkerGroupSpec(_ImageMixin, _ResrouceMixin, _MountsMixin):
    """
    A worker group specification for a Ray cluster.
    """

    name: str = "worker"

    node_selector: dict[str, str] = attrs.field(default={"_PLACEHOLDER": "true"})

    min_replicas: int = attrs.field(
        default=0,
        validator=attrs.validators.ge(0),
    )
    max_replicas: int = attrs.field(
        default=100,
    )

    @max_replicas.validator
    def _validate_max_replicas(self, attribute: str, value: int) -> None:
        if value == 0:
            raise ValueError("max_replicas must be greater than 0")

        if value < self.min_replicas:
            raise ValueError(
                f"max_replicas ({value}) must be greater than or",
                f" equal to min_replicas ({self.min_replicas})",
            )

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        if self.node_selector == {"_PLACEHOLDER": "true"}:
            if self.num_gpus > 0:
                self.node_selector = {GENEVA_RAY_GPU_NODE: ""}
            else:
                self.node_selector = {GENEVA_RAY_CPU_NODE: ""}

    @property
    def definition(self) -> dict:
        return {
            "groupName": self.name,
            "minReplicas": self.min_replicas,
            "maxReplicas": self.max_replicas,
            "rayStartParams": {
                "num-cpus": str(self.num_cpus),
            },
            "template": {
                "spec": {
                    "containers": [
                        {
                            "name": "ray-worker",
                            "image": self.image,
                            "imagePullPolicy": "IfNotPresent",
                            "resources": self._resources,
                            "volumeMounts": self.mounts_definition,
                        }
                    ],
                    "volumes": self.volume_definition,
                    "nodeSelector": self.node_selector,
                }
            },
        }


@attrs.define(kw_only=True)
class RayCluster(_RayVersionMixin):
    """
    A Ray cluster specification.

    This is also a context manager for managing a Ray cluster.
    This context manager will apply the Ray cluster definition to the
    Kubernetes cluster when entering the context and delete the Ray
    cluster from the Kubernetes cluster when exiting the context.

    When entering the context, ray.init will be called with the address of the
    Ray cluster head node. When exiting the context, ray.shutdown will be
    called to shutdown the Ray cluster.

    Example:
        >>> from geneva.runners.ray.raycluster import RayCluster, cluster
        >>> head_group = _HeadGroupSpec(image="rayproject/ray:latest")
        >>> worker_group = _WorkerGroupSpec(name="worker", image="rayproject/ray")
        >>> with RayCluster(
        ...     name="test-cluster",
        ...     head_group=head_group,
        ...     worker_groups=[worker_group],
        ... ):
        ...     print("Ray cluster is running")
        Ray cluster is running
    """

    name: str = attrs.field()
    """
    The name of the Ray cluster. This name is used for deduplication of Ray
    clusters in the Kubernetes cluster. When a Ray cluster with the same name
    already exists, we will not create a new one.

    TODO: add a recreate=True option to force the recreation of the cluster.
    """

    @name.default
    def _default_name(self) -> str:
        config = _RayClusterConfig.get()
        return f"geneva-{config.user}"

    namespace: str = attrs.field()
    """
    The namespace of the Ray cluster. This is the namespace in which the Ray
    cluster will be created in the Kubernetes cluster.

    By default, we use `geneva` as the namespace.
    """

    @namespace.default
    def _default_namespace(self) -> str:
        config = _RayClusterConfig.get()
        return config.namespace

    head_group: _HeadGroupSpec = attrs.field(factory=_HeadGroupSpec)
    """
    The head group specification for the Ray cluster.
    """

    worker_groups: list[_WorkerGroupSpec] = attrs.field(
        factory=lambda: [_WorkerGroupSpec()]
    )
    """
    The worker group specifications for the Ray cluster.
    """

    use_host_ip: bool = attrs.field(default=False)
    """
    Whether to use the host IP address for the head node of the Ray cluster.
    """

    zip_output_dir: str = attrs.field(default=tempfile.mkdtemp())
    """
    The directory to store the zipped environment files.
    """

    @property
    def _autoscaler_options(self) -> dict:
        """
        The autoscaler options for the Ray cluster.
        """
        # TODO: allow customization of the autoscaler options
        return {
            "env": [],
            "envFrom": [],
            "idleTimeoutSeconds": 60,
            "imagePullPolicy": "IfNotPresent",
            "resources": {
                "requests": {
                    "cpu": "1",
                    "memory": "1Gi",
                },
                "limits": {
                    "cpu": "1",
                    "memory": "1Gi",
                },
            },
            "upscalingMode": "Default",
        }

    @property
    def spec(self) -> dict:
        """
        The Ray cluster specification.

        This can be used as part of RayJob for configuring the Ray cluster.
        """
        return {
            "enableInTreeAutoscaling": True,
            "autoscalerOptions": self._autoscaler_options,
            "rayVersion": self.ray_version,
            "headGroupSpec": self.head_group.definition,
            "workerGroupSpecs": [worker.definition for worker in self.worker_groups],
        }

    @property
    def definition(self) -> dict:
        """
        The Ray cluster definition.

        This is the full definition of the Ray cluster, including the name and
        autoscaler options. This can be used to create the Ray cluster in the
        Kubernetes cluster via a CRD.
        """
        return {
            "apiVersion": "ray.io/v1",
            "kind": "RayCluster",
            "metadata": {
                "name": self.name,
                "namespace": self.namespace,
            },
            "spec": self.spec,
        }

    def _has_existing_cluster(self, api: kubernetes.client.CustomObjectsApi) -> bool:
        try:
            api.get_namespaced_custom_object(
                group="ray.io",
                version="v1",
                namespace=self.namespace,
                plural="rayclusters",
                name=self.name,
            )
        except kubernetes.client.exceptions.ApiException as e:
            if e.status == 404:
                return False
            raise e
        return True

    def _wait_for_cluster(self, api: kubernetes.client.CustomObjectsApi) -> Any:
        while True:
            # TODO: add wait for the Ray cluster to be ready
            result = api.get_namespaced_custom_object(
                group="ray.io",
                version="v1",
                namespace=self.namespace,
                plural="rayclusters",
                name=self.name,
            )
            assert isinstance(result, dict)

            if "status" not in result:
                _LOG.info("Waiting for the Ray cluster to be ready")
                time.sleep(1)
                continue

            status = result["status"]
            assert isinstance(status, dict)

            if "head" not in status:
                _LOG.info("Waiting for the head node to be ready")
                time.sleep(1)
                continue

            head = status["head"]
            assert isinstance(head, dict)

            if "podIP" not in head:
                _LOG.info("Waiting for the head node IP address")
                time.sleep(1)
                continue

            _LOG.info("Ray cluster is ready")
            return result

    def _wait_for_head_node(self, api: core_v1_api.CoreV1Api, pod_name: str) -> Any:
        while True:
            pod = api.read_namespaced_pod(name=pod_name, namespace=self.namespace)
            if pod.status.phase != "Running":
                _LOG.info("Waiting for the head node to be running")
                time.sleep(1)
                continue

            _LOG.info("Head node is running")
            return pod

    def _expose_node_port(self, api: core_v1_api.CoreV1Api) -> None:
        _LOG.info("Exposing head node on a node port")
        # create a service to expose the head node
        api.create_namespaced_service(
            namespace=self.namespace,
            body={
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {
                    "name": f"{self.name}-head",
                    "namespace": self.namespace,
                },
                "spec": {
                    "ports": [
                        {
                            "name": "client",
                            "port": 10001,
                            "nodePort": 30001,
                        },
                    ],
                    "selector": {
                        "ray.io/identifier": f"{self.name}-head",
                    },
                    "type": "NodePort",
                },
            },
        )

    def apply(self) -> str:
        """
        Apply the Ray cluster definition to the Kubernetes cluster.

        returns the ip address of the head node
        """
        api = kubernetes.client.CustomObjectsApi()

        if self._has_existing_cluster(api):
            _LOG.info(
                "Ray cluster already exists, patching instead of creating a new one."
                " This means existing nodes will not update until they are recreated."
                " Use recreate=True to force recreation."
            )
            api.patch_namespaced_custom_object(
                group="ray.io",
                version="v1",
                namespace=self.namespace,
                plural="rayclusters",
                name=self.name,
                body=self.definition,
            )
        else:
            api.create_namespaced_custom_object(
                group="ray.io",
                version="v1",
                namespace=self.namespace,
                plural="rayclusters",
                body=self.definition,
            )

        cluster_status = self._wait_for_cluster(api)

        pod_name = cluster_status["status"]["head"]["podName"]
        core_api = core_v1_api.CoreV1Api()

        pod = self._wait_for_head_node(core_api, pod_name)

        if self.use_host_ip:
            _LOG.info("Using host ip for head node")
            self._expose_node_port(core_api)
            return pod.status.host_ip

        return pod.status.pod_ip

    def delete(self) -> None:
        """
        Delete the Ray cluster from the Kubernetes cluster.
        """
        try:
            api = kubernetes.client.CustomObjectsApi()
            api.delete_namespaced_custom_object(
                group="ray.io",
                version="v1",
                namespace=self.namespace,
                plural="rayclusters",
                name=self.name,
            )
        except Exception:
            _LOG.exception("Failed to delete Ray cluster")

        if self.use_host_ip:
            try:
                core_api = core_v1_api.CoreV1Api()
                core_api.delete_namespaced_service(
                    name=f"{self.name}-head",
                    namespace=self.namespace,
                )
            except Exception:
                _LOG.exception("Failed to delete head service")

    def __enter__(self) -> "RayCluster":
        if ray.is_initialized():
            raise RuntimeError(
                "Ray is already initialized, we cannot start a new cluster"
            )

        _LOG.info("Starting Ray cluster")
        ip = self.apply()
        addr = f"ray://{ip}:30001" if self.use_host_ip else f"ray://{ip}:10001"

        _LOG.info("Packaging local environment")
        zips = upload_local_env(zip_output_dir=self.zip_output_dir)
        geneva_zip_payload = base64.b64encode(
            json.dumps({"zips": zips}).encode("utf-8")
        ).decode("utf-8")

        _LOG.info("Connecting to Ray cluster")
        try:
            import multiprocess

            ray.init(
                addr,
                runtime_env={
                    # need these two for loading the workspace deps
                    "py_modules": [geneva, pa, multiprocess],
                    "env_vars": {
                        "GENEVA_ZIPS": geneva_zip_payload,
                    },
                },
            )
        except Exception as e:
            _LOG.exception("Failed to connect to Ray cluster, cleaning up")
            self.delete()
            raise e

        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        ray.shutdown()
        self.delete()
