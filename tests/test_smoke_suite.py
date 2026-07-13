"""Focused coverage for the generated Workspace MCP smoke suite."""

from __future__ import annotations

import pytest

from workspace_bench.core.models import Task
from workspace_bench.core.runner import TaskRunner, load_builtin_tasks
from workspace_bench.workspace.live_parity import (
    DEFAULT_ORIGIN_MAP,
    LiveParityIneligible,
    check_eligibility,
)
from workspace_bench.workspace.tool_surface import WORKSPACE_TOOL_NAMES


def _tasks_by_family() -> dict[str, Task]:
    return {task.family: task for task in load_builtin_tasks("smoke")}


def test_smoke_suite_loads_one_task_per_workspace_tool() -> None:
    tasks = load_builtin_tasks("smoke")

    assert len(tasks) == len(WORKSPACE_TOOL_NAMES) == 20
    assert {task.family for task in tasks} == set(WORKSPACE_TOOL_NAMES)
    assert all(task.id == f"smoke_{task.family}" for task in tasks)
    assert all(task.suite is not None for task in tasks)
    assert all(task.suite.workspace_baseline == "default-v1" for task in tasks if task.suite)


@pytest.mark.parametrize(
    "family",
    ["get_widget_data", "update_widget_layout", "manage_apps"],
)
def test_sampled_smoke_oracles_certify(family: str) -> None:
    result = TaskRunner().run(_tasks_by_family()[family], "oracle")

    assert result.grade.passed
    assert result.grade.checks_total <= 4


@pytest.mark.parametrize(
    ("family", "eligible"),
    [
        ("create_widget", True),
        ("get_skill_content", True),
        ("manage_apps", False),
    ],
)
def test_sampled_smoke_live_eligibility(family: str, eligible: bool) -> None:
    task = _tasks_by_family()[family]

    if eligible:
        check_eligibility(task, DEFAULT_ORIGIN_MAP)
    else:
        with pytest.raises(LiveParityIneligible):
            check_eligibility(task, DEFAULT_ORIGIN_MAP)
