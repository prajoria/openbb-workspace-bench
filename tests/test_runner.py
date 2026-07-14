from __future__ import annotations

import json

import pytest

from workspace_bench.cli import main
from workspace_bench.core.models import CANARY_GUID, Task
from workspace_bench.core.runner import (
    TaskRunner,
    load_builtin_tasks,
    load_task_directory,
    load_task_file,
)


def test_oracle_passes_all_builtin_tasks() -> None:
    runner = TaskRunner()
    results = [runner.run(task, "oracle") for task in load_builtin_tasks()]

    assert results
    assert all(result.grade.passed for result in results)


def test_noop_agent_fails_builtin_tasks() -> None:
    runner = TaskRunner()
    results = [runner.run(task, "noop") for task in load_builtin_tasks()]

    assert results
    assert all(not result.grade.passed for result in results)


def test_cli_can_write_trace_artifacts(tmp_path) -> None:
    exit_code = main(
        [
            "run",
            "--task",
            "price_performance_aapl",
            "--agent",
            "oracle",
            "--trace-dir",
            str(tmp_path),
            "--json",
        ]
    )

    artifact = tmp_path / "price_performance_aapl.json"
    payload = json.loads(artifact.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert payload["grade"]["passed"] is True
    assert payload["task"]["family"] == "create"
    assert payload["task"]["difficulty"] == "easy"
    assert payload["trace"][0]["tool"] == "get_workspace_snapshot"


def test_builtin_tasks_have_terminal_bench_style_metadata() -> None:
    tasks = load_builtin_tasks()

    assert all(task.family for task in tasks)
    assert all(
        task.specification_level
        in {"explicit", "partially-specified", "open-brief"}
        for task in tasks
    )
    assert all(task.difficulty in {"easy", "medium", "hard"} for task in tasks)
    assert all(task.source_path and task.source_path.parent.name == task.family for task in tasks)


def test_task_directory_derives_missing_family_from_its_directory(tmp_path) -> None:
    source = next(
        task for task in load_builtin_tasks() if task.id == "price_performance_aapl"
    )
    assert source.source_path is not None
    family_dir = tmp_path / source.family
    family_dir.mkdir()
    payload = json.loads(source.source_path.read_text(encoding="utf-8"))
    payload.pop("family")
    (family_dir / source.source_path.name).write_text(
        json.dumps(payload),
        encoding="utf-8",
    )

    loaded = load_task_directory(tmp_path)
    assert [task.family for task in loaded] == [source.family]

    # Without a source path there is nothing to derive the family from.
    with pytest.raises(ValueError, match="requires family"):
        Task.from_dict(payload)


def test_cli_validate_passes_for_builtin_tasks() -> None:
    assert main(["validate", "--min-tasks", "300"]) == 0


def test_cli_validate_passes_for_build_suite(capsys) -> None:
    exit_code = main(["validate", "--suite", "build-openbb-apps", "--min-tasks", "236", "--json"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["release_checks"], "build suite must carry release quotas"
    assert payload["release_checks"]["per_specification_level_graded_check_caps"] is True
    assert payload["release_checks"]["prompt_specification_lint_236"] is True
    assert payload["release_checks"]["ownership_aggrid_widget_types"] is True
    assert all(payload["release_checks"].values())


def test_cli_validate_skips_bundled_quotas_for_filtered_slices(capsys) -> None:
    exit_code = main(["validate", "--difficulty", "easy", "--json"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["release_checks"] == {}


def test_cli_filters_by_first_class_family(capsys) -> None:
    exit_code = main(["list", "--family", "create", "--json"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert len(payload) == 20
    assert {task["family"] for task in payload} == {"create"}


def test_find_task_searches_all_bundled_suites() -> None:
    from workspace_bench.core.runner import find_task

    assert find_task("price_performance_aapl").id == (
        "price_performance_aapl"
    )
    assert find_task("revision_grid").id == ("revision_grid")
    assert (
        find_task("revision_grid", suite="build-openbb-apps").id
        == "revision_grid"
    )
    try:
        find_task("revision_grid", suite="enterprise-apps-usage")
    except KeyError:
        pass
    else:
        raise AssertionError("build task must not resolve from the core suite")


def test_cli_smoke_workspace_mcp_wires_task_and_suite(monkeypatch) -> None:
    from workspace_bench.workspace import live_mcp

    async def stub(**kwargs):
        raise RuntimeError("stubbed live bridge")

    monkeypatch.setattr(live_mcp, "run_workspace_mcp_smoke", stub)

    exit_code = main(
        [
            "smoke-workspace-mcp",
            "--task",
            "price_performance_aapl",
            "--suite",
            "enterprise-apps-usage",
        ]
    )

    assert exit_code == 2


def test_cli_manifest_resolves_core_suite(capsys) -> None:
    exit_code = main(["manifest", "--suite", "enterprise-apps-usage", "--json"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["task_count"] == 300
    assert "create" in payload["families"]
    assert payload["task_suite"]["suite_id"] == "enterprise-apps-usage"
    assert len(payload["task_suite"]["content_sha256"]) == 64
    assert "read" in payload["categories"]


def test_cli_validate_fails_when_min_task_gate_is_not_met(capsys) -> None:
    exit_code = main(["validate", "--category", "repair", "--min-tasks", "300"])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "expected at least 300" in output


def test_cli_filters_by_difficulty(capsys) -> None:
    exit_code = main(["list", "--difficulty", "medium", "--family", "params"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "options_constrained_pair_for_price_performance" in output
    assert "price_performance_aapl" not in output


def test_cli_canary_command(capsys) -> None:
    exit_code = main(["canary"])

    output = capsys.readouterr().out.strip()
    assert exit_code == 0
    assert output == CANARY_GUID


def test_cli_manifest_json_includes_dataset_summary(capsys) -> None:
    exit_code = main(["manifest", "--json"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["name"] == "openbb-workspace-bench"
    assert payload["task_suite"]["suite_id"] == "enterprise-apps-usage"
    assert "release_id" not in payload
    assert payload["task_count"] == len(load_builtin_tasks())
    assert payload["canary_guid"] == CANARY_GUID
    assert "dashboard" in payload["categories"]


def test_cli_report_json_includes_release_checks(capsys) -> None:
    exit_code = main(["report", "--json"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["manifest"]["task_count"] >= 300
    assert payload["release_checks"]["oracle_all_pass"] is True
    assert payload["release_checks"]["noop_all_fail"] is True


def test_cli_report_can_write_markdown(tmp_path) -> None:
    output = tmp_path / "nested" / "report.md"

    exit_code = main(["report", "--output", str(output)])

    text = output.read_text(encoding="utf-8")
    assert exit_code == 0
    assert "# OpenBB Workspace Bench Report" in text
    assert "task_count_at_least_300" in text


def test_cli_run_json_includes_aggregate_summary(capsys) -> None:
    exit_code = main(
        [
            "run",
            "--task",
            "price_performance_aapl",
            "--agent",
            "oracle",
            "--json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["summary"]["passed"] == 1
    assert payload["results"][0]["category"] == "single-widget"
    assert payload["results"][0]["difficulty"] == "easy"


def test_cli_run_resolves_build_suite_task_without_suite_flag(capsys) -> None:
    exit_code = main(
        [
            "run",
            "--task",
            "revision_grid",
            "--agent",
            "oracle",
            "--json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["summary"]["passed"] == 1
    assert payload["results"][0]["id"] == "revision_grid"


def test_cli_runtime_result_row_includes_deployment_receipt(capsys) -> None:
    exit_code = main(
        [
            "run",
            "--task",
            "build-openbb-apps/e2e/case_triage",
            "--agent",
            "oracle",
            "--json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    receipt = payload["results"][0]["deployment_receipt"]
    assert exit_code == 0
    assert receipt["backend_names"] == ["Surveillance Data"]
    assert receipt["app_ids"] == ["case-triage"]
    assert receipt["instantiated_dashboard_ids"] == ["dash_002"]
    assert receipt["counts"]["widget_probes"] == 2
    assert all(probe["outcome"] == "passed" for probe in receipt["widget_probes"])


def test_cli_can_run_private_task_directory(tmp_path, capsys) -> None:
    task = next(
        item for item in load_builtin_tasks() if item.id == "price_performance_aapl"
    )
    (tmp_path / "create").mkdir()
    task_path = tmp_path / "create" / "price_performance_aapl.json"
    task_path.write_text(
        task.source_path.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    validate_exit = main(["validate", "--task-dir", str(tmp_path), "--min-tasks", "1"])
    capsys.readouterr()
    run_exit = main(
        [
            "run",
            "--task-dir",
            str(tmp_path),
            "--agent",
            "oracle",
            "--json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert validate_exit == 0
    assert run_exit == 0
    assert payload["summary"]["total"] == 1
    assert payload["summary"]["passed"] == 1


def test_runner_round_trips_workspace_resource_and_prompt_task(tmp_path) -> None:
    task_path = tmp_path / "resource_prompt_round_trip.json"
    task_path.write_text(
        json.dumps(
            {
                "id": "resource_prompt_round_trip",
                "category": "read",
                "family": "resources",
                "difficulty": "easy",
                "prompt": "Read the app index and tool usage prompt.",
                    "fixtures": {"backends": [{"name": "getting-started"}]},
                "initial_state": {},
                "allowed_tools": [
                    "read_workspace_resource",
                    "get_workspace_prompt",
                ],
                "success": {
                    "required_resource_reads": [
                        {
                            "uri": "openbb://workspace/app-builder/index",
                                "data_contains": ["Onboarding App for Devs"],
                        }
                    ],
                    "required_tool_calls": [
                        {
                            "tool": "get_workspace_prompt",
                            "args_contains": {"name": "workspace_tool_usage"},
                        }
                    ],
                    "required_tool_results": [
                        {
                            "tool": "get_workspace_prompt",
                            "data_contains": ["schema-before-create workspace tool discipline"],
                        }
                    ],
                },
                "oracle_tool_calls": [
                    {
                        "tool": "read_workspace_resource",
                        "args": {"uri": "openbb://workspace/app-builder/index"},
                    },
                    {
                        "tool": "get_workspace_prompt",
                        "args": {"name": "workspace_tool_usage"},
                    },
                ],
                "limits": {"max_turns": 2},
            }
        ),
        encoding="utf-8",
    )
    task = load_task_file(task_path)

    result = TaskRunner().run(task, "oracle")

    assert result.grade.passed is True
    assert [event.call.name for event in result.trace] == [
        "read_workspace_resource",
        "get_workspace_prompt",
    ]


def test_cli_private_task_suite_manifest_applies(tmp_path, capsys) -> None:
    task = next(
        item for item in load_builtin_tasks() if item.id == "price_performance_aapl"
    )
    (tmp_path / "task_suite.json").write_text(
        json.dumps(
            {
                "suite_id": "private-pack",
                "visibility": "private",
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "price_performance_aapl.json").write_text(
        task.source_path.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    manifest_exit = main(["manifest", "--task-dir", str(tmp_path), "--json"])

    payload = json.loads(capsys.readouterr().out)
    assert manifest_exit == 0
    assert payload["task_suite"]["suite_id"] == "private-pack"
    assert payload["task_suite"]["visibility"] == "private"


def test_cli_hidden_task_suite_redacts_trace_prompts(tmp_path, capsys) -> None:
    task = next(
        item for item in load_builtin_tasks() if item.id == "price_performance_aapl"
    )
    task_dir = tmp_path / "hidden_pack"
    trace_dir = tmp_path / "traces"
    task_dir.mkdir()
    (task_dir / "task_suite.json").write_text(
        json.dumps({"visibility": "hidden"}),
        encoding="utf-8",
    )
    (task_dir / "create").mkdir()
    (task_dir / "create" / "price_performance_aapl.json").write_text(
        task.source_path.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    manifest_exit = main(["manifest", "--task-dir", str(task_dir), "--json"])
    manifest = json.loads(capsys.readouterr().out)
    run_exit = main(
        [
            "run",
            "--task-dir",
            str(task_dir),
            "--agent",
            "oracle",
            "--trace-dir",
            str(trace_dir),
            "--json",
        ]
    )

    payload = json.loads((trace_dir / "price_performance_aapl.json").read_text())
    assert manifest_exit == 0
    assert run_exit == 0
    assert manifest["redacted"] is True
    assert "prompt" not in payload["task"]
    assert payload["task"]["prompt_redacted"] is True


def test_cli_export_task_writes_public_agent_envelope(tmp_path) -> None:
    output = tmp_path / "task.json"

    exit_code = main(
        [
            "export-task",
            "--task",
            "price_performance_aapl",
            "--output",
            str(output),
        ]
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert payload["schema_version"] == "workspace-bench-envelope"
    assert payload["benchmark"]["suite_id"] == "enterprise-apps-usage"
    assert payload["task"]["qualified_id"] == "enterprise-apps-usage/create/price_performance_aapl"
    assert payload["task"]["id"] == "price_performance_aapl"
    assert payload["task"]["family"] == "create"
    assert payload["task"]["business_terms"] == []
    assert "oracle_tool_calls" not in payload["task"]
    assert "success" not in payload["task"]


def test_cli_run_agent_command_uses_jsonl_contract(tmp_path, capsys) -> None:
    exit_code = main(
        [
            "run-agent-command",
            "--task",
            "price_performance_aapl",
            "--agent-command",
            "python -m workspace_bench.agents.rule_agent",
            "--run-dir",
            str(tmp_path / "runs"),
            "--json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert "git_commit" in payload["benchmark"]
    assert payload["summary"]["passed"] == 1
    assert payload["results"][0]["passed"] is True
    assert payload["results"][0]["agent_exit_code"] == 0


def test_cli_run_agent_command_does_not_reuse_stale_output(tmp_path, capsys) -> None:
    run_dir = tmp_path / "runs"
    first_exit = main(
        [
            "run-agent-command",
            "--task",
            "price_performance_aapl",
            "--agent-command",
            "python -m workspace_bench.agents.rule_agent",
            "--run-dir",
            str(run_dir),
            "--json",
        ]
    )
    capsys.readouterr()

    second_exit = main(
        [
            "run-agent-command",
            "--task",
            "price_performance_aapl",
            "--agent-command",
            'python -c "raise SystemExit(2)"',
            "--run-dir",
            str(run_dir),
            "--json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert first_exit == 0
    assert second_exit == 1
    assert payload["summary"]["passed"] == 0
    assert payload["summary"]["process_failures"] == 1


def test_task_loader_rejects_legacy_split_field(tmp_path) -> None:
    task = next(
        item for item in load_builtin_tasks() if item.id == "price_performance_aapl"
    )
    payload = json.loads(task.source_path.read_text(encoding="utf-8"))
    payload["split"] = "train"
    task_path = tmp_path / "legacy_split.json"
    task_path.write_text(json.dumps(payload), encoding="utf-8")

    try:
        load_task_file(task_path)
    except ValueError as error:
        assert "unknown fields" in str(error)
    else:
        raise AssertionError("legacy split field should be rejected")


def test_task_loader_rejects_malformed_allowed_tools(tmp_path) -> None:
    task = next(
        item for item in load_builtin_tasks() if item.id == "price_performance_aapl"
    )
    payload = json.loads(task.source_path.read_text(encoding="utf-8"))
    payload["setup"]["allowed_tools"] = "create_widget"
    task_path = tmp_path / "bad_allowed_tools.json"
    task_path.write_text(json.dumps(payload), encoding="utf-8")

    try:
        load_task_file(task_path)
    except ValueError as error:
        assert "allowed_tools must be a list" in str(error)
    else:
        raise AssertionError("malformed allowed_tools should fail")


def test_validate_reports_duplicate_task_ids(tmp_path, capsys) -> None:
    task = next(
        item for item in load_builtin_tasks() if item.id == "price_performance_aapl"
    )
    source = task.source_path.read_text(encoding="utf-8")
    (tmp_path / "create").mkdir()
    (tmp_path / "create" / "one.json").write_text(source, encoding="utf-8")
    (tmp_path / "create" / "two.json").write_text(source, encoding="utf-8")

    exit_code = main(["validate", "--task-dir", str(tmp_path), "--min-tasks", "1"])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "task id must be unique" in output
