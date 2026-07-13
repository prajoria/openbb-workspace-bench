"""Task metadata and baseline validation."""

from __future__ import annotations

from typing import Any

from workspace_bench.core.models import Task
from workspace_bench.core.runner import TaskRunner, tasks_workspace_baseline
from workspace_bench.core.suite_checks import release_checks_for_suite


def validate_tasks(
    tasks: list[Task], min_tasks: int = 1, release_profile: str | None = None
) -> dict[str, Any]:
    """Validate task loadability, metadata, oracle pass, and noop failure."""

    if tasks and all(task.code_task is not None for task in tasks):
        from workspace_bench.code_tasks import validate_code_tasks

        result = validate_code_tasks(tasks, min_tasks=min_tasks)
        result["workspace_baseline"] = tasks_workspace_baseline(tasks)
        return result
    if any(task.code_task is not None for task in tasks):
        raise ValueError("cannot mix real-code and simulated Workspace tasks in one validation")
    runner = TaskRunner()
    oracle_results = [runner.run(task, "oracle") for task in tasks]
    noop_results = [runner.run(task, "noop") for task in tasks]
    issues: list[dict[str, str]] = []
    seen_ids: set[tuple[str, str]] = set()
    duplicate_ids: set[tuple[str, str]] = set()
    for task in tasks:
        identity = (task.family, task.id)
        if identity in seen_ids:
            duplicate_ids.add(identity)
        seen_ids.add(identity)
    for family, task_id in sorted(duplicate_ids):
        issues.append(
            {"task_id": f"{family}/{task_id}", "message": "task id must be unique within its family"}
        )
    if len(tasks) < min_tasks:
        issues.append(
            {
                "task_id": "benchmark",
                "message": f"expected at least {min_tasks} task(s), found {len(tasks)}",
            }
        )
    release_checks = release_checks_for_suite(release_profile, tasks, oracle_results)
    for check_name, passed in release_checks.items():
        if not passed:
            issues.append(
                {"task_id": "benchmark", "message": f"release check failed: {check_name}"}
            )
    for task, oracle_result, noop_result in zip(tasks, oracle_results, noop_results):
        for message in task_metadata_issues(task):
            issues.append({"task_id": task.id, "message": message})
        if not oracle_result.grade.passed:
            issues.append(
                {"task_id": task.id, "message": "oracle trace does not pass task grader"}
            )
        if noop_result.grade.passed:
            issues.append(
                {"task_id": task.id, "message": "noop baseline passed; task is too weak"}
            )
    return {
        "passed": not issues,
        "workspace_baseline": tasks_workspace_baseline(tasks),
        "task_count": len(tasks),
        "oracle_passed": sum(result.grade.passed for result in oracle_results),
        "noop_failed": sum(not result.grade.passed for result in noop_results),
        "release_checks": release_checks,
        "issues": issues,
    }


def task_metadata_issues(task: Task) -> list[str]:
    issues = []
    if not task.family:
        issues.append("family must be non-empty")
    if task.difficulty not in {"easy", "medium", "hard"}:
        issues.append("difficulty must be one of easy, medium, hard")
    if not task.oracle_tool_calls and task.code_task is None:
        issues.append("oracle_tool_calls must be non-empty")
    if not task.allowed_tools:
        issues.append("allowed_tools must be non-empty")
    return issues
