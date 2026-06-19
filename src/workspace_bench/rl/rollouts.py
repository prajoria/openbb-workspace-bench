"""Small rollout helpers for policy evaluation loops."""

from __future__ import annotations

from typing import Iterable

from workspace_bench.models import JsonDict


def collect_rollout(
    env,
    actions: Iterable[JsonDict],
    *,
    seed: int | None = None,
    options: JsonDict | None = None,
) -> list[JsonDict]:
    """Reset an environment and collect transitions for a fixed action sequence."""

    observation, reset_info = env.reset(seed=seed, options=options)
    transitions = []
    for action in actions:
        next_observation, reward, terminated, truncated, info = env.step(action)
        transitions.append(
            {
                "observation": observation,
                "action": action,
                "reward": reward,
                "next_observation": next_observation,
                "terminated": terminated,
                "truncated": truncated,
                "info": info,
                "reset_info": reset_info,
            }
        )
        observation = next_observation
        if terminated or truncated:
            break
    return transitions

