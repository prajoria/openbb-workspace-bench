"""SFT dataset conversion helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from workspace_bench.exports.jsonl import write_jsonl
from workspace_bench.exports.schema import RolloutRecord, SFTFormat
from workspace_bench.models import JsonDict


def write_sft_jsonl(
    records: Iterable[RolloutRecord],
    output_path: Path,
    *,
    fmt: SFTFormat,
    include_failures: bool = False,
) -> int:
    """Write SFT-ready JSONL in one of the supported message formats."""

    rows = []
    for record in records:
        if not include_failures and not record.metadata.get("passed"):
            continue
        rows.append(format_sft_record(record, fmt=fmt))
    return write_jsonl(rows, output_path)


def format_sft_record(record: RolloutRecord, *, fmt: SFTFormat) -> JsonDict:
    if fmt == "openai_messages":
        return {"messages": record.messages, "metadata": record.metadata}
    if fmt == "sharegpt":
        role_map = {"system": "system", "user": "human", "assistant": "gpt"}
        return {
            "conversations": [
                {
                    "from": role_map.get(str(message.get("role")), message.get("role")),
                    "value": message.get("content", ""),
                }
                for message in record.messages
            ],
            "metadata": record.metadata,
        }
    if fmt == "tool_call_jsonl":
        return {
            "task": record.task,
            "tool_calls": record.tool_calls,
            "metadata": record.metadata,
        }
    raise ValueError(f"Unknown SFT format {fmt!r}")

