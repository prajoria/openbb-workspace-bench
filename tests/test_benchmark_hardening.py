from __future__ import annotations

import copy
import json

import pytest

from workspace_bench.agents.agent_command import build_task_envelope
from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.models import Task, TaskSuiteManifest
from workspace_bench.core.mutation_checks import grader_mutation_failures
from workspace_bench.core.runner import TaskRunner, find_task, load_builtin_tasks
from workspace_bench.workspace.live_mcp import compare_tool_schemas


def test_current_task_schema_is_strict() -> None:
    source = find_task("morning_briefing_level0", suite="workspace-tasks")
    assert source.source_path is not None
    payload = json.loads(source.source_path.read_text(encoding="utf-8"))
    payload.setdefault("family", source.family)
    payload.setdefault("category", source.category)

    obsolete_level = dict(payload)
    obsolete_level["level"] = "t2"
    with pytest.raises(ValueError, match="unknown fields: level"):
        Task.from_dict(obsolete_level)

    retired_metadata = dict(payload)
    retired_metadata["title"] = "Retired Title"
    retired_metadata["novelty"] = "retired rationale"
    with pytest.raises(ValueError, match="unknown fields: novelty, title"):
        Task.from_dict(retired_metadata)

    unknown_field = dict(payload)
    unknown_field["famliy"] = "typo"
    with pytest.raises(ValueError, match="unknown fields: famliy"):
        Task.from_dict(unknown_field)

    nested_typo = copy.deepcopy(payload)
    nested_typo["eval"]["trace_cheks"] = {}
    with pytest.raises(ValueError, match="eval contains unknown fields"):
        Task.from_dict(nested_typo)

    mixed_schemas = copy.deepcopy(payload)
    mixed_schemas["success"] = {"required_tabs": ["overview"]}
    with pytest.raises(ValueError, match="mixes the eval block"):
        Task.from_dict(mixed_schemas)

    trace_contract = copy.deepcopy(payload)
    trace_contract["eval"]["trace_checks"] = {"max_invalid_tool_calls": 0}
    parsed = Task.from_dict(trace_contract)
    assert parsed.success.trace.max_invalid_tool_calls == 0


def test_active_identity_is_suite_family_task_without_generation_labels() -> None:
    tasks = load_builtin_tasks("workspace-tasks")

    assert len(tasks) == 120
    assert all(not task.id.startswith(("auth_", "gen_")) for task in tasks)
    assert all(task.qualified_id == f"{task.suite.suite_id}/{task.family}/{task.id}" for task in tasks if task.suite)

    assert (
        find_task("workspace-tasks/portfolio_manager/morning_briefing_level0").family
        == "portfolio_manager"
    )


def test_suite_manifests_reject_manual_release_versioning() -> None:
    with pytest.raises(ValueError, match="unknown fields: release_id, version"):
        TaskSuiteManifest.from_dict(
            {
                "suite_id": "private",
                "release_id": "private-v1",
                "version": "1.0.0",
            }
        )


def test_task_envelope_uses_suite_provenance() -> None:
    task = find_task("morning_briefing_level0", suite="workspace-tasks")
    envelope = build_task_envelope(task)

    assert envelope["schema_version"] == "workspace-bench-envelope"
    assert envelope["benchmark"]["suite_id"] == "workspace-tasks"
    assert len(envelope["benchmark"]["content_sha256"]) == 64
    assert "release_id" not in envelope["benchmark"]
    assert (
        envelope["task"]["qualified_id"]
        == "workspace-tasks/portfolio_manager/morning_briefing_level0"
    )


def test_state_and_trace_requirements_are_reported_independently() -> None:
    task = find_task("allocation_read_level0", suite="workspace-tasks")
    episode = WorkspaceEpisode(task)
    for call in task.oracle_tool_calls:
        if call.name != "get_widget_data":
            episode.step(call)

    grade = episode.grade()

    assert grade.state_passed is True
    assert grade.trace_passed is False
    assert grade.passed is False
    assert any(issue.code == "missing_tool_call" for issue in grade.issues)


def test_oracle_is_sensitive_to_independent_mutations() -> None:
    task = find_task("morning_briefing_level0", suite="workspace-tasks")
    oracle = TaskRunner().run(task, "oracle")

    assert oracle.grade.passed
    assert grader_mutation_failures(task, oracle) == []


def test_hosted_schema_audit_allows_additions_but_rejects_breaking_drift() -> None:
    expected = {
        "create_widget": {
            "properties": {
                "origin": {"type": "string", "description": "display origin"},
                "widget_id": {"type": "string"},
            },
            "required": ["origin"],
        }
    }
    additive = copy.deepcopy(expected)
    additive["create_widget"]["properties"]["tab_id"] = {"type": "string"}
    assert compare_tool_schemas(expected, additive) == []

    removed = copy.deepcopy(expected)
    removed["create_widget"]["properties"].pop("widget_id")
    assert "accepted argument was removed" in compare_tool_schemas(expected, removed)[0]

    newly_required = copy.deepcopy(expected)
    newly_required["create_widget"]["required"].append("widget_id")
    assert "became required" in compare_tool_schemas(expected, newly_required)[0]

    nullable_widening = copy.deepcopy(expected)
    nullable_widening["create_widget"]["properties"]["widget_id"] = {
        "anyOf": [{"type": "string"}, {"type": "null"}],
        "default": None,
    }
    assert compare_tool_schemas(expected, nullable_widening) == []
