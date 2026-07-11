"""Shared JSONL writer utilities for export commands."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from workspace_bench.core.models import JsonDict


def write_jsonl(rows: Iterable[JsonDict], output_path: Path) -> int:
    """Write JSONL rows and return the number written.

    Keys are sorted for stable diffs. Consumers must treat JSON object key
    order as insignificant; the harness's own replay files
    (tool_calls.jsonl) preserve insertion order instead, because tool-call
    arg order is semantic to the simulator there.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
            count += 1
    return count

