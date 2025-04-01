# ruff: noqa: PERF203
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# multi-process applier

import attrs
import multiprocess
import pyarrow as pa

from geneva.apply.applier import BatchApplier
from geneva.apply.task import ReadTask
from geneva.debug.logger import ErrorLogger
from geneva.transformer import UDF


@attrs.define
class MultiProcessBatchApplier(BatchApplier):
    """
    A multi-process applier that applies a function to each element in the batch.
    """

    num_processes: int = attrs.field(validator=attrs.validators.ge(1))

    def run(
        self,
        task: ReadTask,
        fn: UDF,
        error_logger: ErrorLogger,
    ) -> pa.RecordBatch:
        with multiprocess.context.SpawnContext().Pool(self.num_processes) as pool:
            # don't pull new batches until the previous ones are done
            # this way we reduce the number of batches in memory
            def _run_with_backpressure():  # noqa: ANN202
                futs = []
                row_addr_arr = []
                seqs = []

                for seq, batch in enumerate(
                    task.to_batches(batch_size=fn.batch_size or 32)
                ):
                    # TODO: allow configuring the global batch size via config
                    row_addr_arr.append(batch["_rowaddr"])
                    seqs.append(seq)
                    futs.append(pool.apply_async(fn, args=(batch,)))
                    # don't start waiting till we have primed the queue
                    if len(futs) >= self.num_processes + 1:
                        seq = seqs.pop(0)
                        fut = futs.pop(0)
                        row_addr = row_addr_arr.pop(0)
                        try:
                            yield row_addr, fut.get()
                        except Exception as e:
                            error_logger.log_error(e, task, fn, seq)
                            raise e

                while futs:
                    seq = seqs.pop(0)
                    fut = futs.pop(0)
                    row_addr = row_addr_arr.pop(0)
                    try:
                        yield row_addr, fut.get()
                    except Exception as e:
                        error_logger.log_error(e, task, fn, seq)
                        raise e

            results = list(_run_with_backpressure())
            arrs = [arr for _, arr in results]
            row_addrs = [row_addr for row_addr, _ in results]

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
