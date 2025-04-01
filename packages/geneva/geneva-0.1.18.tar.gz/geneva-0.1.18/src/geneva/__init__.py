# ruff: noqa: E402
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# lance dataset distributed transform job checkpointing + UDF utils

import base64
import fcntl
import json
import logging
import os
import site
import tempfile
import zipfile
from pathlib import Path

import pyarrow.fs as fs

_LOG = logging.getLogger(__name__)

# MAGIC: if GENEVA_ZIPS is set, we will extract the zips and add them as site-packages
# this is how we acheive "import geneva" == importing workspace from client
#
# NOTE: think of this like booting up a computer. At this point we do not have any
# dependencies installed, so this logic needs to have minimal dependency surface.
# We avoid importing anything from geneva and do everything in the stdlib
if "GENEVA_ZIPS" in os.environ:
    import fcntl

    with open("/tmp/.geneva_zip_setup", "w") as file:  # noqa: S108
        # use fcntl to lock the file so we don't have multiple processes
        # trying to extract at the same time and blow up the disk space
        fcntl.lockf(file, fcntl.LOCK_EX)

        payload = json.loads(base64.b64decode(os.environ["GENEVA_ZIPS"]))
        zips = payload.get("zips", [])

        for z in zips:
            _LOG.info("Setting up geneva workspace from zip %s", z)
            # pyarrow stubs are not correct
            handle, path = fs.FileSystem.from_uri(z)
            handle: fs.FileSystem = handle
            path: str = path

            file_name = path.split("/")[-1]

            output_dir = Path(tempfile.gettempdir()) / file_name.replace(".zip", "")  # noqa: S108
            if output_dir.exists():
                _LOG.info("workspace already extracted to %s", output_dir)
            else:
                zip_download_path = Path(tempfile.gettempdir()) / file_name
                with (
                    handle.open_input_file(path) as f,
                    open(zip_download_path, "wb") as out,
                ):
                    chunk_size = 1024 * 1024 * 8  # 8MiB chunks
                    while data := f.read(chunk_size):
                        out.write(data)

                with zipfile.ZipFile(zip_download_path) as z:
                    z.extractall(output_dir)
                _LOG.info("extracted workspace to %s", output_dir)

            site.addsitedir(output_dir.as_posix())
            _LOG.info("added %s to sys.path", output_dir)

        fcntl.lockf(file, fcntl.LOCK_UN)


from geneva.apply import LanceRecordBatchUDFApplier, ReadTask
from geneva.checkpoint import (
    ArrowFsCheckpointStore,
    CheckpointStore,
    InMemoryCheckpointStore,
    LanceCheckpointStore,
)
from geneva.db import connect
from geneva.docker import DockerWorkspacePackager
from geneva.transformer import udf

__all__ = [
    "ArrowFsCheckpointStore",
    "CheckpointStore",
    "connect",
    "InMemoryCheckpointStore",
    "LanceRecordBatchUDFApplier",
    "LanceCheckpointStore",
    "ReadTask",
    "udf",
    "DockerWorkspacePackager",
]

version = "0.1.18"

__version__ = version
