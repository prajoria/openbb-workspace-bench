from __future__ import annotations

import json
from pathlib import Path

from workspace_bench.cli import main
from workspace_bench.models import CANARY_GUID
from workspace_bench.runner import ScenarioRunner, load_builtin_scenarios, load_scenario_file


def test_oracle_passes_all_builtin_scenarios() -> None:
    runner = ScenarioRunner()
    results = [runner.run(scenario, "oracle") for scenario in load_builtin_scenarios()]

    assert results
    assert all(result.grade.passed for result in results)


def test_noop_agent_fails_builtin_scenarios() -> None:
    runner = ScenarioRunner()
    results = [runner.run(scenario, "noop") for scenario in load_builtin_scenarios()]

    assert results
    assert all(not result.grade.passed for result in results)


def test_cli_can_write_trace_artifacts(tmp_path) -> None:
    exit_code = main(
        [
            "run",
            "--scenario",
            "l1_add_price_widget",
            "--agent",
            "oracle",
            "--trace-dir",
            str(tmp_path),
            "--json",
        ]
    )

    artifact = tmp_path / "l1_add_price_widget.json"
    payload = json.loads(artifact.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert payload["grade"]["passed"] is True
    assert payload["scenario"]["difficulty"] == "easy"
    assert payload["trace"][0]["tool"] == "get_workspace_snapshot"


def test_builtin_scenarios_have_terminal_bench_style_metadata() -> None:
    scenarios = load_builtin_scenarios()

    assert all(scenario.category for scenario in scenarios)
    assert all(scenario.difficulty in {"easy", "medium", "hard"} for scenario in scenarios)
    assert all(scenario.tags for scenario in scenarios)


def test_cli_validate_passes_for_builtin_scenarios() -> None:
    assert main(["validate", "--min-scenarios", "25"]) == 0


def test_cli_validate_fails_when_min_scenario_gate_is_not_met(capsys) -> None:
    exit_code = main(["validate", "--level", "L4", "--min-scenarios", "25"])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "expected at least 25" in output


def test_cli_filters_by_level_and_tag(capsys) -> None:
    exit_code = main(["list", "--level", "L2", "--tag", "multi-widget"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "l2_earnings_dashboard" in output
    assert "l1_add_price_widget" not in output


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
    assert payload["release_id"] == "workspace-core-v0"
    assert payload["scenario_count"] == len(load_builtin_scenarios())
    assert payload["canary_guid"] == CANARY_GUID
    assert "dashboard-construction" in payload["categories"]
    assert payload["splits"] == ["dev"]


def test_cli_report_json_includes_release_checks(capsys) -> None:
    exit_code = main(["report", "--json"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["manifest"]["scenario_count"] >= 25
    assert payload["release_checks"]["oracle_all_pass"] is True
    assert payload["release_checks"]["noop_all_fail"] is True


def test_cli_report_can_write_markdown(tmp_path) -> None:
    output = tmp_path / "report.md"

    exit_code = main(["report", "--output", str(output)])

    text = output.read_text(encoding="utf-8")
    assert exit_code == 0
    assert "# OpenBB Workspace Bench Report" in text
    assert "scenario_count_at_least_25" in text


def test_cli_run_json_includes_aggregate_summary(capsys) -> None:
    exit_code = main(
        [
            "run",
            "--scenario",
            "l1_add_price_widget",
            "--agent",
            "oracle",
            "--json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["summary"]["passed"] == 1
    assert payload["results"][0]["difficulty"] == "easy"
    assert payload["results"][0]["split"] == "dev"


def test_cli_can_run_private_scenario_directory(tmp_path, capsys) -> None:
    scenario = next(
        item for item in load_builtin_scenarios() if item.id == "l1_add_price_widget"
    )
    scenario_path = tmp_path / "l1_add_price_widget.json"
    scenario_path.write_text(
        scenario.source_path.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    validate_exit = main(
        ["validate", "--scenario-dir", str(tmp_path), "--min-scenarios", "1"]
    )
    capsys.readouterr()
    run_exit = main(
        [
            "run",
            "--scenario-dir",
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


def test_cli_private_task_pack_manifest_sets_default_split(tmp_path, capsys) -> None:
    scenario = next(
        item for item in load_builtin_scenarios() if item.id == "l1_add_price_widget"
    )
    (tmp_path / "task_pack.json").write_text(
        json.dumps(
            {
                "pack_id": "private-pack",
                "release_id": "private-pack-v1",
                "version": "1.0.0",
                "visibility": "private",
                "default_split": "validation",
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "l1_add_price_widget.json").write_text(
        scenario.source_path.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    manifest_exit = main(["manifest", "--scenario-dir", str(tmp_path), "--json"])

    payload = json.loads(capsys.readouterr().out)
    assert manifest_exit == 0
    assert payload["splits"] == ["validation"]
    assert payload["task_pack"]["pack_id"] == "private-pack"
    assert payload["scenarios"][0]["split"] == "validation"


def test_cli_hidden_task_pack_redacts_trace_prompts(tmp_path, capsys) -> None:
    scenario = next(
        item for item in load_builtin_scenarios() if item.id == "l1_add_price_widget"
    )
    scenario_dir = tmp_path / "hidden_pack"
    trace_dir = tmp_path / "traces"
    scenario_dir.mkdir()
    (scenario_dir / "task_pack.json").write_text(
        json.dumps({"visibility": "hidden"}),
        encoding="utf-8",
    )
    (scenario_dir / "l1_add_price_widget.json").write_text(
        scenario.source_path.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    manifest_exit = main(["manifest", "--scenario-dir", str(scenario_dir), "--json"])
    manifest = json.loads(capsys.readouterr().out)
    run_exit = main(
        [
            "run",
            "--scenario-dir",
            str(scenario_dir),
            "--agent",
            "oracle",
            "--trace-dir",
            str(trace_dir),
            "--json",
        ]
    )

    payload = json.loads((trace_dir / "l1_add_price_widget.json").read_text())
    assert manifest_exit == 0
    assert run_exit == 0
    assert manifest["redacted"] is True
    assert "prompt" not in payload["scenario"]
    assert payload["scenario"]["prompt_redacted"] is True


def test_cli_filters_by_split_for_private_task_pack(tmp_path, capsys) -> None:
    scenario = next(
        item for item in load_builtin_scenarios() if item.id == "l1_add_price_widget"
    )
    (tmp_path / "task_pack.json").write_text(
        json.dumps({"default_split": "validation"}),
        encoding="utf-8",
    )
    (tmp_path / "l1_add_price_widget.json").write_text(
        scenario.source_path.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    exit_code = main(
        [
            "list",
            "--scenario-dir",
            str(tmp_path),
            "--split",
            "test",
            "--json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload == []


def test_cli_export_task_writes_public_agent_envelope(tmp_path) -> None:
    output = tmp_path / "task.json"

    exit_code = main(
        [
            "export-task",
            "--scenario",
            "l1_add_price_widget",
            "--output",
            str(output),
        ]
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert payload["schema_version"] == "workspace-bench-task-v1"
    assert payload["benchmark"]["release_id"] == "workspace-core-v0"
    assert payload["scenario"]["id"] == "l1_add_price_widget"
    assert payload["scenario"]["split"] == "dev"
    assert "oracle_tool_calls" not in payload["scenario"]
    assert "success" not in payload["scenario"]


def test_cli_export_rollouts_writes_oracle_record(tmp_path) -> None:
    output = tmp_path / "rollouts.jsonl"

    exit_code = main(
        [
            "export-rollouts",
            "--oracle",
            "--scenario",
            "l1_add_price_widget",
            "--output",
            str(output),
        ]
    )

    records = [
        json.loads(line)
        for line in output.read_text(encoding="utf-8").splitlines()
    ]
    assert exit_code == 0
    assert len(records) == 1
    assert records[0]["schema_version"] == "workspace-bench-rollout-v1"
    assert records[0]["metadata"]["benchmark_release_id"] == "workspace-core-v0"
    assert records[0]["metadata"]["export_schema_version"] == "workspace-bench-rollout-v1"
    assert records[0]["metadata"]["exported_at"].endswith("Z")
    assert records[0]["metadata"]["passed"] is True
    assert records[0]["tool_calls"][0]["tool"] == "get_workspace_snapshot"
    assert records[0]["tool_results"][0]["ok"] is True


def test_cli_export_sft_defaults_to_passing_oracle_attempts(tmp_path) -> None:
    output = tmp_path / "sft.jsonl"

    exit_code = main(
        [
            "export-sft",
            "--oracle",
            "--scenario",
            "l1_add_price_widget",
            "--format",
            "openai_messages",
            "--output",
            str(output),
        ]
    )

    records = [
        json.loads(line)
        for line in output.read_text(encoding="utf-8").splitlines()
    ]
    assert exit_code == 0
    assert len(records) == 1
    assert records[0]["metadata"]["passed"] is True
    assert records[0]["messages"][0]["role"] == "user"


def test_cli_run_agent_command_uses_jsonl_contract(tmp_path, capsys) -> None:
    exit_code = main(
        [
            "run-agent-command",
            "--scenario",
            "l1_add_price_widget",
            "--agent-command",
            "python -m workspace_bench.examples.jsonl_rule_agent",
            "--run-dir",
            str(tmp_path / "runs"),
            "--json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["benchmark"]["release_id"] == "workspace-core-v0"
    assert payload["summary"]["passed"] == 1
    assert payload["results"][0]["passed"] is True
    assert payload["results"][0]["agent_exit_code"] == 0


def test_cli_run_agent_command_does_not_reuse_stale_output(tmp_path, capsys) -> None:
    run_dir = tmp_path / "runs"
    first_exit = main(
        [
            "run-agent-command",
            "--scenario",
            "l1_add_price_widget",
            "--agent-command",
            "python -m workspace_bench.examples.jsonl_rule_agent",
            "--run-dir",
            str(run_dir),
            "--json",
        ]
    )
    capsys.readouterr()

    second_exit = main(
        [
            "run-agent-command",
            "--scenario",
            "l1_add_price_widget",
            "--agent-command",
            "python -c \"raise SystemExit(2)\"",
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


def test_scenario_loader_rejects_invalid_split(tmp_path) -> None:
    scenario = next(
        item for item in load_builtin_scenarios() if item.id == "l1_add_price_widget"
    )
    payload = json.loads(scenario.source_path.read_text(encoding="utf-8"))
    payload["split"] = "prod"
    scenario_path = tmp_path / "bad_split.json"
    scenario_path.write_text(json.dumps(payload), encoding="utf-8")

    try:
        load_scenario_file(scenario_path)
    except ValueError as error:
        assert "split must be one of" in str(error)
    else:
        raise AssertionError("invalid scenario split should fail")


def test_scenario_loader_rejects_malformed_allowed_tools(tmp_path) -> None:
    scenario = next(
        item for item in load_builtin_scenarios() if item.id == "l1_add_price_widget"
    )
    payload = json.loads(scenario.source_path.read_text(encoding="utf-8"))
    payload["allowed_tools"] = "create_widget"
    scenario_path = tmp_path / "bad_allowed_tools.json"
    scenario_path.write_text(json.dumps(payload), encoding="utf-8")

    try:
        load_scenario_file(scenario_path)
    except ValueError as error:
        assert "allowed_tools must be a list" in str(error)
    else:
        raise AssertionError("malformed allowed_tools should fail")


def test_validate_reports_duplicate_scenario_ids(tmp_path, capsys) -> None:
    scenario = next(
        item for item in load_builtin_scenarios() if item.id == "l1_add_price_widget"
    )
    source = scenario.source_path.read_text(encoding="utf-8")
    (tmp_path / "one.json").write_text(source, encoding="utf-8")
    (tmp_path / "two.json").write_text(source, encoding="utf-8")

    exit_code = main(
        ["validate", "--scenario-dir", str(tmp_path), "--min-scenarios", "1"]
    )

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "scenario id must be unique" in output
