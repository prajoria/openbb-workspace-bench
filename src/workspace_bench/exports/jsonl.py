"""Shared JSONL writer utilities for export commands."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from workspace_bench.models import JsonDict


def write_jsonl(rows: Iterable[JsonDict], output_path: Path) -> int:
    """Write JSONL rows and return the number written."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
            count += 1
    return count

