"""Gym-style environment adapter for Workspace Bench."""

from __future__ import annotations

import random
from dataclasses import asdict

from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.models import JsonDict, Task, ToolCall
from workspace_bench.core.runner import load_builtin_tasks
from workspace_bench.rl.actions import action_to_tool_call, is_done_action
from workspace_bench.rl.observations import build_observation
from workspace_bench.rl.rewards import process_reward


class WorkspaceGymEnv:
    """Small Gymnasium-style wrapper around ``WorkspaceEpisode``.

    The class intentionally does not require Gymnasium at import time. It uses
    the same return shape as Gymnasium: ``observation, reward, terminated,
    truncated, info``.
    """

    def __init__(
        self,
        tasks: list[Task] | None = None,
        *,
        task: Task | None = None,
        process_rewards: bool = False,
        valid_tool_reward: float = 0.0,
        invalid_tool_penalty: float = 0.0,
        schema_before_create_reward: float = 0.0,
        repeated_snapshot_penalty: float = 0.0,
    ):
        if task is not None and tasks is not None:
            raise ValueError("Pass either task or tasks, not both.")
        if task is not None:
            tasks = [task]
        self.tasks = list(tasks or load_builtin_tasks())
        if not self.tasks:
            raise ValueError("WorkspaceGymEnv requires at least one task.")
        self.process_rewards = process_rewards
        self.valid_tool_reward = valid_tool_reward
        self.invalid_tool_penalty = invalid_tool_penalty
        self.schema_before_create_reward = schema_before_create_reward
        self.repeated_snapshot_penalty = repeated_snapshot_penalty
        self._rng = random.Random()
        self._task: Task | None = None
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
        self._task = self._select_task(options or {})
        self._episode = WorkspaceEpisode(self._task)
        self._turn_index = 0
        self._last_tool_result = None
        self._done = False
        return self._observation(), {"task_id": self._task.id}

    def step(self, action: JsonDict) -> tuple[JsonDict, float, bool, bool, JsonDict]:
        if self._episode is None or self._task is None:
            raise RuntimeError("Call reset() before step().")
        if self._done:
            raise RuntimeError("Episode is done. Call reset() before stepping again.")

        if is_done_action(action):
            grade = self._episode.grade()
            self._done = True
            return (
                self._observation(),
                grade.score,
                True,
                False,
                {"grade": asdict(grade), "done_reason": "agent_done"},
            )

        call = action_to_tool_call(action)
        tool_result = self._episode.step(call)
        self._last_tool_result = tool_result
        self._turn_index += 1
        grade = self._episode.grade()
        terminated = grade.passed
        truncated = not terminated and self._turn_index >= self._max_turns()
        self._done = terminated or truncated
        reward = grade.score if self._done else 0.0
        process_reward_value = 0.0
        if self.process_rewards:
            process_reward_value = self._process_reward(call, tool_result)
            reward += process_reward_value
        return (
            self._observation(),
            reward,
            terminated,
            truncated,
            {
                "grade": asdict(grade),
                "tool_result": tool_result,
                "process_reward": process_reward_value,
                "done_reason": _done_reason(terminated, truncated),
            },
        )

    def render(self) -> JsonDict:
        if self._episode is None:
            return {}
        return self._episode.snapshot()

    def close(self) -> None:
        self._episode = None
        self._task = None
        self._last_tool_result = None
        self._done = True

    def _select_task(self, options: JsonDict) -> Task:
        task_id = options.get("task_id")
        if task_id:
            for task in self.tasks:
                if task.id == task_id:
                    return task
            raise KeyError(f"Unknown task {task_id!r}")
        return self._rng.choice(self.tasks)

    def _observation(self) -> JsonDict:
        assert self._episode is not None
        assert self._task is not None
        return build_observation(
            task=self._task,
            episode=self._episode,
            last_tool_result=self._last_tool_result,
            turn_index=self._turn_index,
            max_turns=self._max_turns(),
        )

    def _max_turns(self) -> int:
        assert self._task is not None
        return int(self._task.limits.get("max_turns", 12))

    def _process_reward(self, call: ToolCall, tool_result: JsonDict) -> float:
        assert self._episode is not None
        assert self._task is not None
        return process_reward(
            episode=self._episode,
            call=call,
            tool_result=tool_result,
            valid_tool_reward=self.valid_tool_reward,
            invalid_tool_penalty=self.invalid_tool_penalty,
            schema_before_create_reward=self.schema_before_create_reward,
            repeated_snapshot_penalty=self.repeated_snapshot_penalty,
        )


def _done_reason(terminated: bool, truncated: bool) -> str | None:
    if terminated:
        return "task_passed"
    if truncated:
        return "max_turns"
    return None
