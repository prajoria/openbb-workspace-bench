"""Action normalization for the Gym-style Workspace environment."""

from __future__ import annotations

from typing import Any

from workspace_bench.core.models import JsonDict, ToolCall


DONE_TOOLS = {"done", "__done__", "finish", "final"}


def is_done_action(action: JsonDict) -> bool:
    if not isinstance(action, dict):
        return False
    if action.get("done") is True:
        return True
    tool = action.get("tool") or action.get("name")
    return isinstance(tool, str) and tool in DONE_TOOLS


def action_to_tool_call(action: JsonDict) -> ToolCall:
    if not isinstance(action, dict):
        return ToolCall("invalid_action", {"message": "action must be an object"})
    tool = action.get("tool") or action.get("name")
    args: Any = action.get("args", {})
    if not isinstance(tool, str) or not tool:
        return ToolCall("invalid_action", {"message": "missing tool/name"})
    if not isinstance(args, dict):
        return ToolCall("invalid_action", {"message": "args must be an object"})
    return ToolCall(tool, args)

