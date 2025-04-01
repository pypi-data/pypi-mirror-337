# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# a zip packager for local workspace

import hashlib
import logging
import re
import site
import sys
import tempfile
import zipfile
from pathlib import Path

import attrs
import emoji

from geneva.config import ConfigBase
from geneva.tqdm import tqdm

_LOG = logging.getLogger(__name__)


@attrs.define
class _ZipperConfig(ConfigBase):
    output_path: Path | None = attrs.field(
        validator=attrs.validators.instance_of(Path),
        converter=attrs.converters.optional(Path),
    )

    @classmethod
    def name(cls) -> str:
        return "zipper"


_DEFAULT_IGNORES = [
    r"\.pyc",
    r".*__pycache__.*",
    r"\.venv",
    r"\.git",
    r"\.ruff_cache",
    r"\.vscode",
    r"\.github",
]


@attrs.define
class WorkspaceZipper:
    path: Path = attrs.field(
        converter=attrs.converters.pipe(
            Path,
            Path.resolve,
            Path.absolute,
        )
    )

    @path.validator
    def _path_validator(self, attribute, value: Path) -> None:
        if not value.is_dir():
            raise ValueError("path must be a directory")

        # make sure the path is the current working directory, or
        # is part of sys.path
        if value == Path.cwd().resolve().absolute():
            return

        sys_paths = {Path(x).resolve().absolute() for x in sys.path}

        if value not in sys_paths:
            raise ValueError("path must be cwd or part of sys.path")

    output_dir: Path = attrs.field(converter=Path)

    @output_dir.default
    def _output_dir_default(self) -> Path:
        config = _ZipperConfig.get()
        if config.output_path is not None:
            return config.output_path
        return self.path / ".geneva"

    ignore_regexs: list[re.Pattern] = attrs.field(
        factory=lambda: [re.compile(r) for r in _DEFAULT_IGNORES],
        converter=lambda x: [re.compile(r) for r in x],
    )
    """
    a list of regex patterns to ignore when zipping the workspace

    only ignores based on the relative path of the file
    """

    file_name: str = attrs.field(default="workspace.zip")

    def zip(self) -> tuple[Path, str]:
        """
        create a zip file for the workspace

        return the path of the zip file and the sha256 hash of the zip file
        """
        zip_path = self.output_dir / self.file_name
        # compression is too costly, so we don't compress
        # TODO: we can shard the zip file to multiple files and compress them
        # in parallel
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_STORED) as z:
            pbar = tqdm(self.path.rglob("*"))
            total_size = 0
            pbar.set_description(
                emoji.emojize(
                    f":magnifying_glass_tilted_left: scanning workspace: {self.path}"
                )
            )

            for child in pbar:
                arcname = child.relative_to(self.path)
                if any(r.match(arcname.as_posix()) for r in self.ignore_regexs):
                    continue
                total_size += child.stat().st_size

            pbar.close()

            with tqdm(
                total=total_size, unit="B", unit_scale=True, unit_divisor=1024
            ) as pbar:
                pbar.set_description(
                    emoji.emojize(f":card_file_box: zipping workspace: {self.path}")
                )
                for child in self.path.rglob("*"):
                    arcname = child.relative_to(self.path)
                    if any(r.match(arcname.as_posix()) for r in self.ignore_regexs):
                        continue
                    total_size += child.stat().st_size
                    z.write(child, arcname.as_posix())
                    pbar.update(child.stat().st_size)
        # IMPORTANT: make the zip file world readable
        # TODO: move these to a "ZipUploader/Downloader" interface
        zip_path.chmod(0o777)
        zip_path.parent.chmod(0o777)
        return zip_path, hashlib.sha256(zip_path.read_bytes()).hexdigest()


@attrs.define
class _UnzipperConfig(ConfigBase):
    output_dir: Path | None = attrs.field(
        converter=attrs.converters.optional(Path),
        default=None,
    )

    @classmethod
    def name(cls) -> str:
        return "unzipper"


# Kept separate from the zipper to avoid config mess
@attrs.define
class WorkspaceUnzipper:
    output_dir: Path = attrs.field(
        converter=attrs.converters.pipe(
            attrs.converters.default_if_none(
                _UnzipperConfig.get().output_dir,
            ),
            attrs.converters.default_if_none(
                factory=tempfile.mkdtemp,
            ),
            Path,
            Path.resolve,
            Path.absolute,
        ),
        default=None,
    )

    def unzip(self, zip_path: Path, *, checksum: str) -> None:
        """
        extract the zip file to the workspace
        """
        if hashlib.sha256(zip_path.read_bytes()).hexdigest() != checksum:
            raise ValueError("workspace zip checksum mismatch")

        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(self.output_dir)
        _LOG.info("extracted workspace to %s", self.output_dir)

        site.addsitedir(self.output_dir.as_posix())
        _LOG.info("added %s to sys.path", self.output_dir)
