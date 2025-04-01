# ruff: noqa: S108

import importlib

import pytest

try:
    import ray

    from geneva.runners.ray.raycluster import (
        RayCluster,
        _HeadGroupSpec,
        _WorkerGroupSpec,
    )
except ImportError:
    import pytest

    pytest.skip("failed to import geneva.runners.ray", allow_module_level=True)


@pytest.mark.skip
@pytest.mark.serial
def test_raycluster_can_import_deps() -> None:
    with RayCluster(
        name="test",
        namespace="geneva",
        head_group=_HeadGroupSpec(
            mounts=[
                ("host-tmp", "/tmp"),
            ],
            volumes={
                "host-tmp": {
                    "hostPath": {"path": "/host_tmp"},
                },
            },
        ),
        worker_groups=[
            _WorkerGroupSpec(
                mounts=[
                    ("host-tmp", "/tmp"),
                ],
                volumes={
                    "host-tmp": {
                        "hostPath": {"path": "/host_tmp"},
                    },
                },
            )
        ],
        use_host_ip=True,
    ):
        ray.get(
            ray.remote(num_cpus=0.1)(lambda: importlib.import_module("geneva")).remote()
        )
