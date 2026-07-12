from __future__ import annotations

import copy
import json
from dataclasses import replace

import pytest

from workspace_bench.agents.agent_command import build_task_envelope
from workspace_bench.cli import main as cli_main
from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.graders import grade_task
from workspace_bench.core.models import Task, TaskSuiteManifest, WorkspaceChecks
from workspace_bench.core.mutation_checks import grader_mutation_failures
from workspace_bench.core.runner import TaskRunner, find_task, load_builtin_tasks
from workspace_bench.workspace.tool_surface import WORKSPACE_TOOL_NAMES
from workspace_bench.workspace.surface_audit import compare_tool_schemas


def test_current_task_schema_is_strict_and_legacy_migration_is_explicit() -> None:
    source = find_task("price_performance_aapl", suite="core")
    assert source.source_path is not None
    payload = json.loads(source.source_path.read_text(encoding="utf-8"))

    missing_version = dict(payload)
    missing_version.pop("schema_version")
    with pytest.raises(ValueError, match="missing schema_version"):
        Task.from_dict(missing_version)

    obsolete_level = dict(payload)
    obsolete_level["level"] = "t2"
    with pytest.raises(ValueError, match="unknown fields: level"):
        Task.from_dict(obsolete_level)

    unknown_field = dict(payload)
    unknown_field["famliy"] = "typo"
    with pytest.raises(ValueError, match="unknown fields: famliy"):
        Task.from_dict(unknown_field)

    nested_typo = copy.deepcopy(payload)
    nested_typo["success"]["trace_cheks"] = {}
    with pytest.raises(ValueError, match="success contains unknown fields"):
        Task.from_dict(nested_typo)

    legacy = dict(missing_version)
    legacy["level"] = "L1"
    migrated = Task.migrate_legacy_payload(legacy)
    assert migrated["schema_version"] == "workspace-bench-task"
    assert "level" not in migrated
    assert Task.from_dict(migrated).id == "price_performance_aapl"


def test_active_identity_is_suite_family_task_without_generation_labels() -> None:
    tasks = [
        *load_builtin_tasks("core"),
        *load_builtin_tasks("build-openbb-apps"),
    ]

    assert len(tasks) == 536

    debug_tasks = [task for task in tasks if task.family == "debug"]
    assert len(debug_tasks) == 24
    assert {len(task.oracle_tool_calls) for task in debug_tasks} == {16, 17}
    assert {task.difficulty for task in debug_tasks} == {"easy", "medium", "hard"}
    assert {task.specification_level for task in debug_tasks} == {
        "partially-specified",
        "open-brief",
    }
    assert all(not task.id.startswith(("auth_", "gen_")) for task in tasks)
    assert all(not any(tag.startswith(("level-", "tier-")) for tag in task.tags) for task in tasks)
    assert all(task.qualified_id == f"{task.suite.suite_id}/{task.family}/{task.id}" for task in tasks if task.suite)

    with pytest.raises(KeyError, match="Ambiguous task"):
        find_task("chain_flows", suite="build-openbb-apps")
    assert find_task("build-openbb-apps/e2e/chain_flows").family == "e2e"


def test_suite_manifests_reject_manual_release_versioning() -> None:
    with pytest.raises(ValueError, match="unknown fields: release_id, version"):
        TaskSuiteManifest.from_dict(
            {
                "suite_id": "private",
                "release_id": "private-v1",
                "version": "1.0.0",
            }
        )


def test_cli_migrates_a_legacy_task_file(tmp_path) -> None:
    task = find_task("price_performance_aapl", suite="core")
    assert task.source_path is not None
    legacy = json.loads(task.source_path.read_text(encoding="utf-8"))
    legacy.pop("schema_version")
    legacy.pop("category")
    legacy.pop("family")
    legacy["level"] = "L1"
    source = tmp_path / "legacy.json"
    output = tmp_path / "current.json"
    source.write_text(json.dumps(legacy), encoding="utf-8")

    assert cli_main(["migrate-task", "--input", str(source), "--output", str(output)]) == 0
    migrated = json.loads(output.read_text(encoding="utf-8"))
    assert migrated["schema_version"] == "workspace-bench-task"
    assert Task.from_dict(migrated).family == "create"


def test_build_task_envelope_uses_build_suite_provenance() -> None:
    task = find_task("vol_commentary", suite="build-openbb-apps")
    envelope = build_task_envelope(task)

    assert envelope["schema_version"] == "workspace-bench-envelope"
    assert envelope["benchmark"]["suite_id"] == "build-openbb-apps"
    assert len(envelope["benchmark"]["content_sha256"]) == 64
    assert "release_id" not in envelope["benchmark"]
    assert envelope["task"]["qualified_id"] == "build-openbb-apps/types/vol_commentary"


def test_build_tasks_offer_full_surface_and_grade_working_outcomes() -> None:
    tasks = load_builtin_tasks("build-openbb-apps")

    assert tasks
    assert all(task.allowed_tools == WORKSPACE_TOOL_NAMES for task in tasks)
    assert all(len(task.prompt.split()) <= 180 for task in tasks)
    assert all(
        task.success.required_widgets or task.success.required_capabilities
        for task in tasks
    )
    assert all(
        task.success.required_dashboard_name_contains
        for task in tasks
        if task.success.required_app_defs
    )
    assert all(
        required.data_equals is None
        for task in tasks
        for required in task.success.required_generated_widgets
    )


def test_build_completion_notes_require_semantic_deployment_facts() -> None:
    task = find_task("build-openbb-apps/e2e/case_triage")
    oracle = TaskRunner().run(task, "oracle")
    required = task.success.required_generated_widgets[0]

    assert required.data_equals is None
    assert "Case Triage" in required.data_contains
    assert "Surveillance Data" in required.data_contains
    assert "C-1048" in required.data_contains

    paraphrased = copy.deepcopy(oracle.final_snapshot)
    note = next(
        widget
        for widget in paraphrased["dashboard_composition"]["widgets"]
        if widget.get("generated")
    )
    note["generated_data"] = (
        "Surveillance Data deployed the Case Triage workflow for case triage; "
        "the case_id selection is C-1048."
    )
    assert grade_task(task, paraphrased, oracle.trace).passed

    missing_backend = copy.deepcopy(paraphrased)
    note = next(
        widget
        for widget in missing_backend["dashboard_composition"]["widgets"]
        if widget.get("generated")
    )
    note["generated_data"] = note["generated_data"].replace(
        "Surveillance Data", "Wrong Backend"
    )
    grade = grade_task(task, missing_backend, oracle.trace)
    assert not grade.passed
    assert any(issue.code == "missing_generated_widget" for issue in grade.issues)

    missing_app = copy.deepcopy(paraphrased)
    note = next(
        widget
        for widget in missing_app["dashboard_composition"]["widgets"]
        if widget.get("generated")
    )
    note["generated_data"] = note["generated_data"].replace(
        "Case Triage", "Different App"
    ).replace("case triage", "different workflow")
    note["name"] = "Different App"
    assert not grade_task(task, missing_app, oracle.trace).passed


def test_state_and_trace_policy_are_reported_independently() -> None:
    task = find_task("price_performance_msft", suite="core")
    episode = WorkspaceEpisode(task)
    for call in task.oracle_tool_calls:
        if call.name != "list_available_widgets":
            episode.step(call)

    grade = episode.grade()

    assert grade.state_passed is True
    assert grade.state_score == 1.0
    assert grade.trace_passed is False
    assert grade.passed is False
    assert any(issue.code == "widget_list_not_called_before_use" for issue in grade.issues)


def test_whole_workspace_preservation_catches_collateral_dashboard_change() -> None:
    task = find_task("limits", suite="core")
    task = replace(
        task,
        success=replace(
            task.success,
            workspace=WorkspaceChecks(preserve_other_dashboards=True),
        ),
    )
    initial = {
        "workspace_state": {"current_dashboard_uuid": "active"},
        "dashboard_compositions": {
            "active": {"dashboard_id": "active", "name": "Active"},
            "other": {"dashboard_id": "other", "name": "Other", "widgets": []},
        },
    }
    final = copy.deepcopy(initial)
    final["dashboard_compositions"]["other"]["name"] = "Mutated"
    final["dashboard_composition"] = {"name": "Active", "tabs": [], "widgets": []}
    final["custom_backends"] = {}

    grade = grade_task(task, final, (), initial_snapshot=initial)

    assert not grade.state_passed
    assert any(issue.code == "collateral_dashboard_change" for issue in grade.issues)


def test_oracle_is_sensitive_to_independent_mutations() -> None:
    task = find_task("vendor_review_form", suite="build-openbb-apps")
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
