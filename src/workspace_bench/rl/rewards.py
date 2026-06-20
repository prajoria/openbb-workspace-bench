"""Reward helpers for Gym-style Workspace episodes."""

from __future__ import annotations

from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.models import JsonDict, ToolCall


def process_reward(
    *,
    episode: WorkspaceEpisode,
    call: ToolCall,
    tool_result: JsonDict,
    valid_tool_reward: float,
    invalid_tool_penalty: float,
    schema_before_create_reward: float,
    repeated_snapshot_penalty: float,
) -> float:
    """Compute optional process reward for one intermediate tool call."""

    reward = valid_tool_reward if tool_result.get("ok") else invalid_tool_penalty
    if schema_before_create_satisfied(episode, call):
        reward += schema_before_create_reward
    if is_repeated_snapshot(episode, call):
        reward += repeated_snapshot_penalty
    return reward


def schema_before_create_satisfied(
    episode: WorkspaceEpisode,
    call: ToolCall,
) -> bool:
    if call.name != "create_widget":
        return False
    args = call.args
    origin = str(args.get("origin") or args.get("backend_name"))
    widget_id = str(args.get("widget_id"))
    prior_events = episode.trace[:-1]
    return any(
        event.ok
        and event.call.name == "get_widget_schema"
        and str(event.call.args.get("origin")) == origin
        and str(event.call.args.get("widget_id")) == widget_id
        for event in prior_events
    )


def is_repeated_snapshot(episode: WorkspaceEpisode, call: ToolCall) -> bool:
    if call.name != "get_workspace_snapshot" or len(episode.trace) < 2:
        return False
    return episode.trace[-2].call.name == "get_workspace_snapshot"
