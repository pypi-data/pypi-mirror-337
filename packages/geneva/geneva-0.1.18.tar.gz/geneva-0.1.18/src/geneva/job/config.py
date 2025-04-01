# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import attrs

from geneva.checkpoint import CheckpointConfig, CheckpointStore
from geneva.config import ConfigBase


@attrs.define
class JobConfig(ConfigBase):
    """Geneva Job Configurations."""

    checkpoint: CheckpointConfig = attrs.field(default=CheckpointConfig("tempfile"))

    batch_size: int = attrs.field(default=10240, converter=int)

    task_shuffle_diversity: int = attrs.field(default=8, converter=int)

    # How many fragments to be committed in one single transaction.
    commit_granularity: int = attrs.field(default=64, converter=int)

    @classmethod
    def name(cls) -> str:
        return "job"

    def make_checkpoint_store(self) -> CheckpointStore:
        return (self.checkpoint or CheckpointConfig("tempfile")).make()
