"""Fast representative slice of the systematic adversarial grader matrix."""

from __future__ import annotations

import pytest

from workspace_bench.core.adversarial import (
    NEVER_INSTANTIATED,
    ONE_WIDGET_MISSING,
    evaluate_adversarial_candidate,
    generate_adversarial_candidates,
    run_adversarial_matrix,
)
from workspace_bench.core.runner import TaskRunner, find_task, load_builtin_tasks


CASES = (
    ("workspace-tasks/research_analyst/earnings_prep_level4", NEVER_INSTANTIATED),
    ("workspace-tasks/trading_desk/chart_deck_level4", ONE_WIDGET_MISSING),
)


@pytest.mark.parametrize(("task_ref", "archetype"), CASES)
def test_invalid_candidate_fails_for_its_isolated_intended_reason(
    task_ref: str,
    archetype: str,
) -> None:
    task = find_task(task_ref)
    oracle = TaskRunner().run(task, "oracle")
    candidate = next(
        candidate
        for candidate in generate_adversarial_candidates(task, oracle)
        if candidate.archetype == archetype
    )

    result = evaluate_adversarial_candidate(task, oracle, candidate)

    assert result.oracle_clean
    assert result.oracle_grade.passed
    assert not result.candidate_grade.passed
    assert candidate.primary_code in result.observed_codes
    assert result.expected_code_observed
    assert result.passed


def test_adversarial_matrix_rejects_every_applicable_trading_desk_mutant() -> None:
    tasks = [
        task
        for task in load_builtin_tasks("workspace-tasks")
        if task.family == "trading_desk"
    ]

    matrix = run_adversarial_matrix(tasks, runtime_sample_per_family=1)
    rows = matrix.rows()

    assert tasks
    assert rows
    assert all(row["applicable"] > 0 and row["exercised"] > 0 for row in rows)
    assert all(row["expected_code_observed"] == row["exercised"] for row in rows)
    assert {archetype for _family, archetype in matrix.applicable} == {
        "never_instantiated",
        "one_widget_missing",
        "invalid_setting",
    }
    assert {result.candidate.archetype for result in matrix.results} == {
        archetype for _family, archetype in matrix.applicable
    }
    assert matrix.survivors == ()
    assert matrix.wrong_reason == ()
    assert matrix.dirty_oracles == ()
    assert all(
        result.candidate.primary_code in result.observed_codes
        for result in matrix.results
    )
    assert matrix.passed
