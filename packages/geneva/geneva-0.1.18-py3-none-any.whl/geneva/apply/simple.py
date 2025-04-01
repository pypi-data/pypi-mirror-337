# ruff: noqa: PERF203

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# super simple applier

import attrs
import pyarrow as pa

from geneva.apply.applier import BatchApplier
from geneva.apply.task import ReadTask
from geneva.debug.logger import ErrorLogger
from geneva.transformer import UDF


@attrs.define
class SimpleApplier(BatchApplier):
    """
    A simple applier that applies a function to each element in the batch.
    """

    def run(
        self,
        task: ReadTask,
        fn: UDF,
        error_logger: ErrorLogger,
    ) -> pa.RecordBatch:
        arrs = []
        row_addrs = []
        # TODO: add caching for the input data
        for seq, batch in enumerate(
            # TODO: allow configuring the global batch size via config
            task.to_batches(batch_size=fn.batch_size or 32)
        ):
            try:
                arrs.append(fn(batch))
                row_addrs.append(batch["_rowaddr"])
            except Exception as e:
                error_logger.log_error(e, task, fn, seq)
                raise e

        arr = pa.concat_arrays(arrs)
        row_addr_arr = pa.concat_arrays(row_addrs)

        return pa.RecordBatch.from_pydict(
            {
                "_rowaddr": row_addr_arr,
                "data": arr,
            },
            schema=pa.schema(
                [
                    pa.field("_rowaddr", pa.uint64()),
                    pa.field("data", fn.data_type),
                ]
            ),
        )
