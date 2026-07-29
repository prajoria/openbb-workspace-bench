"""Focused tests for package-owned report compiler logic."""

from __future__ import annotations

from pathlib import Path

from workspace_bench.core.runner import TaskRunner, find_task
from workspace_bench.reports.model_compare import ComparisonRun, agent_run_summary
from workspace_bench.reports.oracle_report import result_summary
from workspace_bench.reports.serialization import grade_summary


def test_cli_and_model_comparison_share_grade_serialization(tmp_path: Path) -> None:
    result = TaskRunner().run(find_task("morning_briefing_level0"), "oracle")
    comparison = ComparisonRun(
        run_result=result,
        command="test-agent",
        exit_code=0,
        timed_out=False,
        stdout="",
        stderr="",
        run_dir=tmp_path,
        task_path=tmp_path / "task.json",
        output_path=tmp_path / "output.jsonl",
        runner="batch",
    )

    canonical = grade_summary(result.grade)
    cli_row = result_summary(result)
    comparison_row = agent_run_summary(comparison)

    assert {key: cli_row[key] for key in canonical} == canonical
    assert comparison_row["passed"] is canonical["passed"]
    assert cli_row["workspace_baseline"] == "stark-workspace-a"
    assert comparison_row["workspace_baseline"] == "stark-workspace-a"
    assert {
        key: comparison_row[key] for key in canonical if key != "passed"
    } == {key: value for key, value in canonical.items() if key != "passed"}
