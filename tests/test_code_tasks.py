from __future__ import annotations

import os
import shlex
import sys
from pathlib import Path

import pytest

from workspace_bench.code_tasks import (
    apply_oracle_overlay,
    evaluate_code_repository,
    instantiate_code_task,
    run_code_task,
    validate_code_tasks,
)
from workspace_bench.core.runner import find_task, load_builtin_tasks


def test_code_suite_has_twelve_typed_fixture_backed_tasks() -> None:
    tasks = load_builtin_tasks("build-openbb-backends")

    assert len(tasks) == 12
    assert {task.difficulty for task in tasks} == {"easy", "medium", "hard"}
    assert all(task.code_task is not None for task in tasks)
    assert all(task.source_path and task.source_path.exists() for task in tasks)
    for task in tasks:
        assert task.code_task is not None
        root = task.source_path.parent
        assert (root / task.code_task.starter_path / "pyproject.toml").is_file()
        assert (root / task.code_task.starter_path / "tests" / "test_backend.py").is_file()
        assert (root / task.code_task.oracle_path / "app.py").is_file()


def test_code_suite_release_driver_passes_every_release_check() -> None:
    result = validate_code_tasks(
        load_builtin_tasks("build-openbb-backends"),
        min_tasks=12,
    )

    assert result["passed"] is True
    assert result["task_count"] == 12
    assert result["oracle_passed"] == 12
    assert result["noop_failed"] == 12
    assert result["issues"] == []
    assert set(result["release_checks"]) == {
        "task_count_is_12",
        "all_tasks_are_code_tasks",
        "difficulty_spread_3_6_3",
        "oracle_all_pass",
        "starter_all_fail",
        "oracle_http_probes_all_pass",
        "oracle_test_suites_non_empty",
        "oracle_process_cleanup",
        "starter_process_cleanup",
        "mutation_removed_endpoint_rejected",
        "mutation_placeholder_payload_rejected",
    }
    assert all(result["release_checks"].values())


def test_oracle_runs_real_server_tests_and_leaves_no_process(tmp_path: Path) -> None:
    task = find_task("market_movers_table", suite="build-openbb-backends")
    workdir = instantiate_code_task(task, workdir=tmp_path / "repo", oracle=True)

    evaluation = evaluate_code_repository(task, workdir)

    assert evaluation.grade.passed
    assert evaluation.receipt["probes"][0]["passed"] is True
    assert evaluation.receipt["tests"]["test_count"] >= 1
    assert evaluation.receipt["tests"]["garbage_mutation_rejected"] is True
    assert evaluation.receipt["cleanup"]["orphan_process"] is False
    pid = evaluation.receipt["cleanup"]["pid"]
    assert isinstance(pid, int)
    if os.name != "nt":
        with pytest.raises(ProcessLookupError):
            os.kill(pid, 0)


def test_external_code_agent_receives_workdir_and_can_apply_solution(tmp_path: Path) -> None:
    task = find_task("market_movers_table", suite="build-openbb-backends")
    assert task.code_task is not None
    oracle = task.source_path.parent / task.code_task.oracle_path
    script = tmp_path / "agent.py"
    script.write_text(
        "import os, shutil\n"
        f"shutil.copytree({str(oracle)!r}, os.environ['WORKSPACE_BENCH_WORKDIR'], "
        "dirs_exist_ok=True)\n",
        encoding="utf-8",
    )
    command = f"{shlex.quote(sys.executable)} {shlex.quote(str(script))}"

    run = run_code_task(
        task=task,
        agent_command=command,
        workdir=tmp_path / "agent-repo",
    )

    assert run.exit_code == 0
    assert run.timed_out is False
    assert run.evaluation.grade.passed
    assert run.task_path.is_file()
    assert run.brief_path.is_file()
    assert (run.evaluation.workdir / ".workspace-bench" / "deployment-receipt.json").is_file()


def test_starter_fails_before_oracle_overlay(tmp_path: Path) -> None:
    task = find_task("market_movers_table", suite="build-openbb-backends")
    workdir = instantiate_code_task(task, workdir=tmp_path / "repo")

    starter = evaluate_code_repository(task, workdir)
    apply_oracle_overlay(task, workdir)
    oracle = evaluate_code_repository(task, workdir)

    assert not starter.grade.passed
    assert {issue.code for issue in starter.grade.issues} >= {
        "code_endpoint_placeholder",
        "code_tests_failed",
    }
    assert oracle.grade.passed
