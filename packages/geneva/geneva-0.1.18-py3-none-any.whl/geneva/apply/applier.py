# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import abc

import pyarrow as pa

from geneva.apply.task import ReadTask
from geneva.debug.logger import ErrorLogger
from geneva.transformer import UDF


class BatchApplier(abc.ABC):
    """Interface class for all appliers"""

    @abc.abstractmethod
    def run(
        self,
        task: ReadTask,
        fn: UDF,
        error_logger: ErrorLogger,
    ) -> pa.RecordBatch:
        """Run the applier on the task and return the result

        return a record batch, which contains the result of the function
        the batch should include two columns:
        - _rowaddr: the row address of the input batch
        - data: the result of the function
        """
