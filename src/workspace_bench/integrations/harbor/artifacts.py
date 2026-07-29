"""Trusted Harbor episode artifact helpers."""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import Any

from workspace_bench.core.models import JsonDict, ToolCall, ToolTraceEvent


EPISODE_SCHEMA_VERSION = "workspace-bench-harbor-episode/v1"


def trace_event_payload(event: ToolTraceEvent) -> JsonDict:
    """Serialize one canonical benchmark trace event."""

    return {
        "index": event.index,
        "call": {"name": event.call.name, "args": event.call.args},
        "ok": event.ok,
        "result": event.result,
    }


def trace_event_from_payload(payload: JsonDict) -> ToolTraceEvent:
    """Deserialize one trusted trace event, rejecting malformed shapes."""

    call = payload.get("call")
    result = payload.get("result")
    if not isinstance(call, dict) or not isinstance(result, dict):
        raise ValueError("trace event requires call and result objects")
    event = ToolTraceEvent(
        index=int(payload["index"]),
        call=ToolCall.from_dict(call),
        ok=bool(payload.get("ok")),
        result=result,
    )
    if event.index <= 0:
        raise ValueError("trace event index must be positive")
    return event


def atomic_write_json(path: Path, payload: object) -> None:
    """Durably replace a JSON file without exposing a partial artifact."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def full_grade_payload(grade: Any) -> JsonDict:
    """Serialize every GradeResult field, including judge dimensions."""

    return asdict(grade)

