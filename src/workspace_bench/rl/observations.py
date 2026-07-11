"""Observation construction for RL adapters."""

from __future__ import annotations

from workspace_bench.agents.agent_command import build_task_envelope
from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.models import JsonDict, Task


def build_observation(
    *,
    task: Task,
    episode: WorkspaceEpisode,
    last_tool_result: JsonDict | None,
    turn_index: int,
    max_turns: int,
) -> JsonDict:
    envelope_task = build_task_envelope(task)["task"]
    return {
        "task": envelope_task,
        "allowed_tools": list(task.allowed_tools),
        "last_tool_result": last_tool_result,
        "snapshot": episode.snapshot(),
        "turn_index": turn_index,
        "remaining_turns": max(0, max_turns - turn_index),
    }

