"""Canonical export record schemas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from workspace_bench.core.models import JsonDict


ROLLOUT_SCHEMA_VERSION = "workspace-bench-rollout-v1"
PREFERENCE_SCHEMA_VERSION = "workspace-bench-preference-v1"
SFTFormat = Literal["sharegpt", "openai_messages", "tool_call_jsonl"]


@dataclass(frozen=True)
class RolloutRecord:
    """Canonical portable record for one Workspace Bench attempt."""

    task: JsonDict
    messages: list[JsonDict]
    tool_calls: list[JsonDict]
    tool_results: list[JsonDict]
    final_snapshot: JsonDict
    grade: JsonDict
    metadata: JsonDict

    def to_dict(self) -> JsonDict:
        return {
            "schema_version": ROLLOUT_SCHEMA_VERSION,
            "task": self.task,
            "messages": self.messages,
            "tool_calls": self.tool_calls,
            "tool_results": self.tool_results,
            "final_snapshot": self.final_snapshot,
            "grade": self.grade,
            "metadata": self.metadata,
        }

