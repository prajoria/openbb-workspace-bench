"""Shared benchmark metric helpers."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from statistics import median
from typing import Any


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


def pairwise_flip_rate(outcomes: Sequence[bool]) -> float:
    """Return the share of repeat pairs with different strict outcomes."""

    passed = sum(bool(outcome) for outcome in outcomes)
    failed = len(outcomes) - passed
    pairs = len(outcomes) * (len(outcomes) - 1) // 2
    return passed * failed / pairs if pairs else 0.0


def summarize_result_rows(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Compute calibration metrics from serialized per-episode rows."""

    total = len(rows)
    strict_passed = sum(bool(row.get("passed")) for row in rows)
    state_passed = sum(bool(row.get("state_passed")) for row in rows)
    runtime_rows = [row for row in rows if int(row.get("runtime_checks_total") or 0) > 0]
    runtime_passed = sum(bool(row.get("runtime_passed")) for row in runtime_rows)
    tool_calls = sum(int(row.get("tool_call_count") or 0) for row in rows)
    failed_calls = sum(int(row.get("failed_tool_call_count") or 0) for row in rows)
    recovery_candidates = [
        row for row in rows if int(row.get("failed_tool_call_count") or 0) > 0
    ]
    recovered = sum(bool(row.get("passed")) for row in recovery_candidates)
    browser_rows = [row for row in rows if row.get("browser_verdict") in {"pass", "fail"}]
    browser_passed = sum(row.get("browser_verdict") == "pass" for row in browser_rows)
    outcomes_by_task: dict[str, list[bool]] = defaultdict(list)
    for row in rows:
        task_ref = str(row.get("qualified_id") or row.get("id"))
        outcomes_by_task[task_ref].append(bool(row.get("passed")))
    reliability = compute_reliability_metrics(outcomes_by_task)
    flip_rates = [pairwise_flip_rate(outcomes) for outcomes in outcomes_by_task.values()]
    costs = [
        float(row["cost_usd"])
        for row in rows
        if isinstance(row.get("cost_usd"), (int, float))
    ]
    return {
        "total": total,
        "strict_passed": strict_passed,
        "strict_pass_rate": strict_passed / total if total else 0.0,
        "state_passed": state_passed,
        "state_pass_rate": state_passed / total if total else 0.0,
        "runtime_task_count": len(runtime_rows),
        "runtime_passed": runtime_passed,
        "runtime_pass_rate": runtime_passed / len(runtime_rows) if runtime_rows else None,
        "browser_status": "observed" if browser_rows else "pending",
        "browser_task_count": len(browser_rows),
        "browser_passed": browser_passed,
        "browser_pass_rate": browser_passed / len(browser_rows) if browser_rows else None,
        "tool_call_count": tool_calls,
        "failed_tool_call_count": failed_calls,
        "invalid_tool_call_rate": failed_calls / tool_calls if tool_calls else 0.0,
        "median_turns": median(
            [int(row.get("tool_call_count") or 0) for row in rows]
        )
        if rows
        else 0.0,
        "recovery_candidate_count": len(recovery_candidates),
        "recovered_after_failure": recovered,
        "recovery_after_failure_rate": (
            recovered / len(recovery_candidates) if recovery_candidates else None
        ),
        "flip_rate": sum(flip_rates) / len(flip_rates) if flip_rates else 0.0,
        "flipped_task_count": sum(rate > 0 for rate in flip_rates),
        "input_tokens": sum(int(row.get("input_tokens") or 0) for row in rows),
        "cached_tokens": sum(int(row.get("cached_tokens") or 0) for row in rows),
        "output_tokens": sum(int(row.get("output_tokens") or 0) for row in rows),
        "total_tokens": sum(int(row.get("total_tokens") or 0) for row in rows),
        "wall_time_seconds": round(
            sum(float(row.get("wall_time_seconds") or 0.0) for row in rows), 6
        ),
        "cost_usd": round(sum(costs), 10) if len(costs) == total and total else None,
        "costed_episode_count": len(costs),
        **reliability,
    }


def task_reliability_matrix(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Build per-task outcomes and repeat variance for calibration review."""

    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("qualified_id") or row.get("id"))].append(row)
    matrix = []
    for task_ref, task_rows in sorted(grouped.items()):
        ordered = sorted(task_rows, key=lambda row: int(row.get("repeat") or 1))
        outcomes = [bool(row.get("passed")) for row in ordered]
        metrics = summarize_result_rows(ordered)
        matrix.append(
            {
                "task_ref": task_ref,
                "family": ordered[0].get("family"),
                "difficulty": ordered[0].get("difficulty"),
                "outcomes": outcomes,
                "strict_pass_rate": metrics["strict_pass_rate"],
                "state_pass_rate": metrics["state_pass_rate"],
                "runtime_pass_rate": metrics["runtime_pass_rate"],
                "browser_status": metrics["browser_status"],
                "browser_pass_rate": metrics["browser_pass_rate"],
                "invalid_tool_call_rate": metrics["invalid_tool_call_rate"],
                "median_turns": metrics["median_turns"],
                "recovery_after_failure_rate": metrics["recovery_after_failure_rate"],
                "flip_rate": pairwise_flip_rate(outcomes),
                "pass_at_k": any(outcomes),
                "pass_power_k": all(outcomes) if outcomes else False,
            }
        )
    return matrix
