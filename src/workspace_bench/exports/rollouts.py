"""Canonical rollout JSONL writer."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from workspace_bench.exports.jsonl import write_jsonl
from workspace_bench.exports.schema import RolloutRecord


def write_rollouts_jsonl(records: Iterable[RolloutRecord], output_path: Path) -> int:
    """Write canonical rollout JSONL and return record count."""

    return write_jsonl((record.to_dict() for record in records), output_path)

