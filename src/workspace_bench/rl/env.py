"""Gym-style environment adapter for Workspace Bench."""

from __future__ import annotations

import random
from dataclasses import asdict
from typing import Any

from workspace_bench.agent_command import build_task_envelope
from workspace_bench.episode import WorkspaceEpisode
from workspace_bench.models import JsonDict, Scenario, ToolCall
from workspace_bench.runner import load_builtin_scenarios


DONE_TOOLS = {"done", "__done__", "finish", "final"}


class WorkspaceGymEnv:
    """Small Gymnasium-style wrapper around ``WorkspaceEpisode``.

    The class intentionally does not require Gymnasium at import time. It uses
    the same return shape as Gymnasium: ``observation, reward, terminated,
    truncated, info``.
    """

    def __init__(
        self,
        scenarios: list[Scenario] | None = None,
        *,
        scenario: Scenario | None = None,
        process_rewards: bool = False,
        valid_tool_reward: float = 0.0,
        invalid_tool_penalty: float = 0.0,
        schema_before_create_reward: float = 0.0,
        repeated_snapshot_penalty: float = 0.0,
    ):
        if scenario is not None and scenarios is not None:
            raise ValueError("Pass either scenario or scenarios, not both.")
        if scenario is not None:
            scenarios = [scenario]
        self.scenarios = list(scenarios or load_builtin_scenarios())
        if not self.scenarios:
            raise ValueError("WorkspaceGymEnv requires at least one scenario.")
        self.process_rewards = process_rewards
        self.valid_tool_reward = valid_tool_reward
        self.invalid_tool_penalty = invalid_tool_penalty
        self.schema_before_create_reward = schema_before_create_reward
        self.repeated_snapshot_penalty = repeated_snapshot_penalty
        self._rng = random.Random()
        self._scenario: Scenario | None = None
        self._episode: WorkspaceEpisode | None = None
        self._turn_index = 0
        self._last_tool_result: JsonDict | None = None
        self._done = False

    def reset(
        self,
        seed: int | None = None,
        options: JsonDict | None = None,
    ) -> tuple[JsonDict, JsonDict]:
        if seed is not None:
            self._rng.seed(seed)
        self._scenario = self._select_scenario(options or {})
        self._episode = WorkspaceEpisode(self._scenario)
        self._turn_index = 0
        self._last_tool_result = None
        self._done = False
        return self._observation(), {"scenario_id": self._scenario.id}

    def step(self, action: JsonDict) -> tuple[JsonDict, float, bool, bool, JsonDict]:
        if self._episode is None or self._scenario is None:
            raise RuntimeError("Call reset() before step().")
        if self._done:
            raise RuntimeError("Episode is done. Call reset() before stepping again.")

        if _is_done_action(action):
            grade = self._episode.grade()
            self._done = True
            return (
                self._observation(),
                grade.score,
                True,
                False,
                {"grade": asdict(grade), "done_reason": "agent_done"},
            )

        call = _action_to_tool_call(action)
        tool_result = self._episode.step(call)
        self._last_tool_result = tool_result
        self._turn_index += 1
        grade = self._episode.grade()
        terminated = grade.passed
        truncated = not terminated and self._turn_index >= self._max_turns()
        self._done = terminated or truncated
        reward = grade.score if self._done else 0.0
        process_reward = 0.0
        if self.process_rewards:
            process_reward = self._process_reward(call, tool_result)
            reward += process_reward
        return (
            self._observation(),
            reward,
            terminated,
            truncated,
            {
                "grade": asdict(grade),
                "tool_result": tool_result,
                "process_reward": process_reward,
                "done_reason": _done_reason(terminated, truncated),
            },
        )

    def render(self) -> JsonDict:
        if self._episode is None:
            return {}
        return self._episode.snapshot()

    def close(self) -> None:
        self._episode = None
        self._scenario = None
        self._last_tool_result = None
        self._done = True

    def _select_scenario(self, options: JsonDict) -> Scenario:
        scenario_id = options.get("scenario_id")
        if scenario_id:
            for scenario in self.scenarios:
                if scenario.id == scenario_id:
                    return scenario
            raise KeyError(f"Unknown scenario {scenario_id!r}")
        return self._rng.choice(self.scenarios)

    def _observation(self) -> JsonDict:
        assert self._episode is not None
        assert self._scenario is not None
        task = build_task_envelope(self._scenario)["scenario"]
        return {
            "task": task,
            "allowed_tools": list(self._scenario.allowed_tools),
            "last_tool_result": self._last_tool_result,
            "snapshot": self._episode.snapshot(),
            "turn_index": self._turn_index,
            "remaining_turns": max(0, self._max_turns() - self._turn_index),
        }

    def _max_turns(self) -> int:
        assert self._scenario is not None
        return int(self._scenario.limits.get("max_turns", 12))

    def _process_reward(self, call: ToolCall, tool_result: JsonDict) -> float:
        assert self._episode is not None
        assert self._scenario is not None
        if tool_result.get("ok"):
            reward = self.valid_tool_reward
        else:
            reward = self.invalid_tool_penalty

        if self._schema_before_create_satisfied(call):
            reward += self.schema_before_create_reward
        if self._is_repeated_snapshot(call):
            reward += self.repeated_snapshot_penalty
        return reward

    def _schema_before_create_satisfied(self, call: ToolCall) -> bool:
        assert self._episode is not None
        if call.name != "create_widget":
            return False
        args = call.args
        origin = str(args.get("origin") or args.get("backend_name"))
        widget_id = str(args.get("widget_id"))
        prior_events = self._episode.trace[:-1]
        return any(
            event.ok
            and event.call.name == "get_widget_schema"
            and str(event.call.args.get("origin")) == origin
            and str(event.call.args.get("widget_id")) == widget_id
            for event in prior_events
        )

    def _is_repeated_snapshot(self, call: ToolCall) -> bool:
        assert self._episode is not None
        if call.name != "get_workspace_snapshot" or len(self._episode.trace) < 2:
            return False
        return self._episode.trace[-2].call.name == "get_workspace_snapshot"


def _is_done_action(action: JsonDict) -> bool:
    if not isinstance(action, dict):
        return False
    if action.get("done") is True:
        return True
    tool = action.get("tool") or action.get("name")
    return isinstance(tool, str) and tool in DONE_TOOLS


def _action_to_tool_call(action: JsonDict) -> ToolCall:
    if not isinstance(action, dict):
        return ToolCall("invalid_action", {"message": "action must be an object"})
    tool = action.get("tool") or action.get("name")
    args: Any = action.get("args", {})
    if not isinstance(tool, str) or not tool:
        return ToolCall("invalid_action", {"message": "missing tool/name"})
    if not isinstance(args, dict):
        return ToolCall("invalid_action", {"message": "args must be an object"})
    return ToolCall(tool, args)


def _done_reason(terminated: bool, truncated: bool) -> str | None:
    if terminated:
        return "scenario_passed"
    if truncated:
        return "max_turns"
    return None
