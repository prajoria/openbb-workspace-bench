"""Focused coverage for the generated Workspace MCP smoke ladder."""

from __future__ import annotations

import json

import pytest

from workspace_bench.core.models import Task
from workspace_bench.core.runner import TaskRunner, load_builtin_tasks
from workspace_bench.core.suite_checks import (
    SMOKE_LEVELS,
    SMOKE_TASK_FIELDS,
    smoke_release_checks,
)
from workspace_bench.workspace.live_parity import (
    DEFAULT_ORIGIN_MAP,
    LiveParityIneligible,
    check_eligibility,
)
from workspace_bench.workspace.tool_surface import WORKSPACE_TOOL_NAMES


def _tasks_by_id() -> dict[str, Task]:
    return {task.id: task for task in load_builtin_tasks("smoke")}


def test_smoke_suite_is_a_four_level_ladder_per_tool() -> None:
    tasks = load_builtin_tasks("smoke")

    assert len(tasks) == len(WORKSPACE_TOOL_NAMES) * len(SMOKE_LEVELS) == 80
    assert {task.family for task in tasks} == set(WORKSPACE_TOOL_NAMES)
    assert {(task.family, task.difficulty) for task in tasks} == {
        (family, level) for family in WORKSPACE_TOOL_NAMES for level in SMOKE_LEVELS
    }
    assert all(
        task.id == f"smoke_{task.family}_{task.difficulty}" for task in tasks
    )


def test_smoke_tasks_declare_their_workspace_axes() -> None:
    for task in load_builtin_tasks("smoke"):
        assert task.workspace_backends is not None
        assert "stark-enterprise-x" in task.workspace_backends
        assert task.workspace_skills is not None
        assert all(slug.startswith("daloopa-") for slug in task.workspace_skills)
        if task.difficulty in ("level0", "level1"):
            # "" is the explicit bare-workspace declaration.
            assert task.workspace_baseline == ""
        else:
            assert task.workspace_baseline == "stark-onboard-a"
        if task.difficulty == "level0":
            assert task.allowed_tools == (task.family,)
        else:
            assert set(task.allowed_tools) == set(WORKSPACE_TOOL_NAMES)


def test_smoke_second_origin_family_connects_getting_started() -> None:
    task = _tasks_by_id()["smoke_list_available_widgets_level0"]

    assert task.workspace_backends == ("stark-enterprise-x", "getting-started")


def test_smoke_category_is_derived_not_written() -> None:
    tasks = load_builtin_tasks("smoke")

    assert all(smoke_release_checks(tasks).values())
    categories = {task.family: task.category for task in tasks}
    assert categories["get_widget_schema"] == "read"
    assert categories["create_widget"] == "single-widget"
    assert categories["manage_apps"] == "dashboard"
    assert categories["assign_tasks_to_agents"] == "platform"
    for task in tasks:
        assert task.source_path is not None
        payload = json.loads(task.source_path.read_text(encoding="utf-8"))
        assert set(payload) <= SMOKE_TASK_FIELDS
        assert "category" not in payload
        assert all(value not in ({}, []) for value in payload.values())


def test_smoke_release_checks_reject_a_broken_ladder(tmp_path) -> None:
    from dataclasses import replace

    tasks = load_builtin_tasks("smoke")
    source = tasks[0].source_path
    assert source is not None
    payload = json.loads(source.read_text(encoding="utf-8"))
    payload["category"] = "read"
    fat_path = tmp_path / "fat_task.json"
    fat_path.write_text(json.dumps(payload), encoding="utf-8")

    fat_tasks = [replace(tasks[0], source_path=fat_path), *tasks[1:]]
    assert not smoke_release_checks(fat_tasks)["task_fields_within_smoke_profile"]

    unleveled = [replace(tasks[0], difficulty="easy"), *tasks[1:]]
    checks = smoke_release_checks(unleveled)
    assert not checks["difficulty_is_level_ladder"]


@pytest.mark.parametrize(
    "task_id",
    [
        "smoke_get_widget_data_level0",
        "smoke_update_widget_layout_level2",
        "smoke_manage_apps_level1",
        "smoke_delete_widget_level3",
    ],
)
def test_sampled_smoke_oracles_certify(task_id: str) -> None:
    result = TaskRunner().run(_tasks_by_id()[task_id], "oracle")

    assert result.grade.passed
    assert result.grade.checks_total <= 6


@pytest.mark.parametrize(
    ("task_id", "eligible"),
    [
        ("smoke_create_widget_level0", True),
        ("smoke_get_skill_content_level0", True),
        ("smoke_manage_apps_level0", False),
    ],
)
def test_sampled_smoke_live_eligibility(task_id: str, eligible: bool) -> None:
    task = _tasks_by_id()[task_id]

    if eligible:
        check_eligibility(task, DEFAULT_ORIGIN_MAP)
    else:
        with pytest.raises(LiveParityIneligible):
            check_eligibility(task, DEFAULT_ORIGIN_MAP)
