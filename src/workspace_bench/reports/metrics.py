"""Shared benchmark metric helpers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence


def compute_reliability_metrics(
    outcomes_by_task: Mapping[str, Sequence[bool]],
) -> dict[str, float | int]:
    """Compute repeat-run reliability metrics over task outcomes.

    pass@k counts a task as passed when at least one attempt passed.
    pass^k counts a task as passed only when every attempt passed.
    """

    task_count = len(outcomes_by_task)
    pass_at_k_count = 0
    pass_power_k_count = 0
    attempts = [len(outcomes) for outcomes in outcomes_by_task.values()]
    for outcomes in outcomes_by_task.values():
        passed = [bool(outcome) for outcome in outcomes]
        if passed and any(passed):
            pass_at_k_count += 1
        if passed and all(passed):
            pass_power_k_count += 1
    return {
        "reliability_task_count": task_count,
        "reliability_min_k": min(attempts) if attempts else 0,
        "reliability_max_k": max(attempts) if attempts else 0,
        "pass_at_k_count": pass_at_k_count,
        "pass_power_k_count": pass_power_k_count,
        "pass_at_k": pass_at_k_count / task_count if task_count else 0.0,
        "pass_power_k": (
            pass_power_k_count / task_count if task_count else 0.0
        ),
    }
