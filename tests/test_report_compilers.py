"""Focused tests for package-owned report compiler logic."""

from __future__ import annotations

from pathlib import Path

from workspace_bench.core.runner import TaskRunner, find_task
from workspace_bench.reports.model_compare import ComparisonRun, agent_run_summary
from workspace_bench.reports.oracle_report import result_summary
from workspace_bench.reports.serialization import grade_summary
from workspace_bench.reports.suites import summarize


def test_cli_and_model_comparison_share_grade_serialization(tmp_path: Path) -> None:
    result = TaskRunner().run(find_task("decision_briefing_level0"), "oracle")
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


def test_suite_summary_reuses_shared_metrics_with_metadata_slices() -> None:
    rows = [
        {
            "id": "a",
            "qualified_id": "demo/forms/a",
            "family": "stale",
            "difficulty": "stale",
            "repeat": 1,
            "passed": True,
            "state_passed": True,
            "score": 0.8,
            "runtime_checks_total": 1,
            "runtime_passed": True,
            "runtime_score": 0.5,
        },
        {
            "id": "b",
            "qualified_id": "demo/debug/b",
            "repeat": 2,
            "passed": False,
            "state_passed": False,
            "score": 0.2,
            "runtime_checks_total": 0,
            "issues": [{"code": "missing_widget"}],
        },
    ]
    metadata = {
        "demo/forms/a": ("forms", "easy"),
        "demo/debug/b": ("debug", "hard"),
    }

    summary = summarize(rows, metadata)

    assert summary == {
        "passed": 1,
        "total": 2,
        "unique_tasks": 2,
        "repeats": [1, 2],
        "strict_pass_rate": 0.5,
        "mean_score": 0.5,
        "runtime_task_count": 1,
        "runtime_passed": 1,
        "runtime_pass_rate": 1.0,
        "mean_runtime_score": 0.5,
        "by_difficulty": {
            "easy": {"passed": 1, "total": 1, "rate": 1.0},
            "hard": {"passed": 0, "total": 1, "rate": 0.0},
        },
        "by_family": {
            "debug": {"passed": 0, "total": 1, "rate": 0.0},
            "forms": {"passed": 1, "total": 1, "rate": 1.0},
        },
        "issue_codes": {"missing_widget": 1},
    }
