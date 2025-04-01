# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# definition of the read task, which is portion of a fragment

import hashlib
from collections.abc import Iterator

import attrs
import pyarrow as pa

from geneva.db import connect


@attrs.define(order=True)
class ReadTask:
    uri: str
    columns: list[str]
    frag_id: int
    offset: int
    limit: int

    version: int | None = None
    filter: str | None = None

    with_row_address: bool = False

    def to_batches(self, *, batch_size=32) -> Iterator[pa.RecordBatch]:
        uri_parts = self.uri.split("/")
        name = ".".join(uri_parts[-1].split(".")[:-1])
        db = "/".join(uri_parts[:-1])

        tbl = connect(db).open_table(name, version=self.version)
        query = tbl.search().enable_internal_api()

        if self.with_row_address:
            query = query.with_row_address()

        query = (
            query.with_fragments(self.frag_id)
            .select(self.columns)
            .offset(self.offset)
            .limit(self.limit)
        )
        if self.filter is not None:
            query = query.where(self.filter)

        # Currently lancedb reports the wrong type for the return value
        # of the to_batches method.  Remove pyright ignore when fixed.
        batches: pa.RecordBatchReader = query.to_batches(batch_size)  # pyright: ignore[reportAssignmentType]

        yield from batches

    def checkpoint_key(self) -> str:
        hasher = hashlib.md5()
        hasher.update(
            f"{self.uri}:{self.version}:{self.columns}:{self.frag_id}:{self.offset}:{self.limit}:{self.filter}".encode(),
        )
        return hasher.hexdigest()
