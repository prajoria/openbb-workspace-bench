"""Focused tests for package-owned report compiler logic."""

from __future__ import annotations

import json
from pathlib import Path

from workspace_bench.core.runner import TaskRunner, find_task
from workspace_bench.reports.model_compare import ComparisonRun, agent_run_summary
from workspace_bench.reports.oracle_report import result_summary
from workspace_bench.reports.serialization import grade_summary
from workspace_bench.reports.significance import main as significance_main
from workspace_bench.reports.suites import summarize


def test_cli_and_model_comparison_share_grade_serialization(tmp_path: Path) -> None:
    result = TaskRunner().run(find_task("price_performance_aapl"), "oracle")
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
    assert cli_row["workspace_baseline"] == "minimal"
    assert comparison_row["workspace_baseline"] == "minimal"
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


def _write_task(suite_dir: Path, family: str, task_id: str) -> None:
    path = suite_dir / family / f"{task_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "id": task_id,
                "family": family,
                "difficulty": "easy" if task_id == "a" else "hard",
            }
        ),
        encoding="utf-8",
    )


def _write_run(path: Path, outcomes: dict[str, tuple[bool, bool]]) -> None:
    rows = [
        {
            "qualified_id": task_ref,
            "repeat": repeat,
            "passed": passed,
        }
        for task_ref, repeated in outcomes.items()
        for repeat, passed in enumerate(repeated, 1)
    ]
    path.write_text(
        json.dumps({"benchmark": {"git_commit": "abc123"}, "results": rows}),
        encoding="utf-8",
    )


def test_significance_compiler_accepts_explicit_runs_and_counts(tmp_path: Path) -> None:
    suite_dir = tmp_path / "build_openbb_apps"
    suite_dir.mkdir()
    (suite_dir / "task_suite.json").write_text(
        json.dumps({"content_sha256": "f" * 64}), encoding="utf-8"
    )
    _write_task(suite_dir, "alpha", "a")
    _write_task(suite_dir, "beta", "b")
    run_dir = tmp_path / "runs"
    run_dir.mkdir()
    a_ref = "build-openbb-apps/alpha/a"
    b_ref = "build-openbb-apps/beta/b"
    _write_run(run_dir / "model-a.json", {a_ref: (True, True), b_ref: (True, False)})
    _write_run(run_dir / "model-b.json", {a_ref: (True, False), b_ref: (False, False)})
    output = tmp_path / "significance.json"

    exit_code = significance_main(
        [
            "--build-run-dir",
            str(run_dir),
            "--build-run",
            "model-a.json",
            "--build-run",
            "model-b.json",
            "--attempts-per-model",
            "4",
            "--tasks-per-model",
            "2",
            "--output",
            str(output),
        ],
        suite_dirs={"build-openbb-apps": suite_dir},
        repo=tmp_path,
    )

    report = json.loads(output.read_text(encoding="utf-8"))
    suite = report["suites"]["build-openbb-apps"]
    assert exit_code == 0
    assert suite["attempts_per_model"] == 4
    assert suite["tasks_per_model"] == 2
    assert suite["models"]["model-a"]["all"]["passed"] == 3
    assert suite["models"]["model-b"]["all"]["passed"] == 1
    assert suite["pairs"] == [
        {
            "a": "model-a",
            "b": "model-b",
            "a_pass_b_fail": 2,
            "a_fail_b_pass": 0,
            "mcnemar_p": 0.5,
            "task_iid_test": "McNemar (descriptive; sibling tasks are clustered)",
            "cluster_bootstrap_difference_95": [0.5, 0.5],
        }
    ]
