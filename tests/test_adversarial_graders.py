"""Fast representative slice of the systematic adversarial grader matrix."""

from __future__ import annotations

import pytest

from workspace_bench.core.adversarial import (
    BROKEN_FORM_SUBMISSION,
    COLLAPSED_CONNECTED_PAIR,
    FIELDLESS_CONTRIBUTOR,
    INCOMPATIBLE_VALUES,
    INVALID_SETTING,
    NEVER_INSTANTIATED,
    NOTE_ONLY_PROOF,
    ONE_WIDGET_MISSING,
    SEVERED_SHARED_INTERACTION,
    SELF_SATISFIED_CONNECTION,
    STRIPPED_APP_PROMPTS,
    WRONG_ENDPOINT_DATA,
    evaluate_adversarial_candidate,
    generate_adversarial_candidates,
    run_adversarial_matrix,
)
from workspace_bench.core.runner import TaskRunner, find_task, load_builtin_tasks


CASES = (
    ("core/backends/add_equities", WRONG_ENDPOINT_DATA),
    ("build-openbb-apps/apps/earnings_desk", NEVER_INSTANTIATED),
    ("build-openbb-apps/e2e/case_triage", ONE_WIDGET_MISSING),
    ("build-openbb-apps/charts/earnings_chart_room", INCOMPATIBLE_VALUES),
    ("build-openbb-apps/forms/vendor_review_form", BROKEN_FORM_SUBMISSION),
    ("build-openbb-apps/grouping/click_season_desk", SEVERED_SHARED_INTERACTION),
    ("build-openbb-apps/advanced/live_orders_grid_ship", INVALID_SETTING),
    ("build-openbb-apps/debug/execution_broken_group", COLLAPSED_CONNECTED_PAIR),
    ("build-openbb-apps/settings/alert_metric_room", FIELDLESS_CONTRIBUTOR),
    ("build-openbb-apps/debug/execution_broken_group", SELF_SATISFIED_CONNECTION),
    ("build-openbb-apps/e2e/case_triage", NOTE_ONLY_PROOF),
    ("build-openbb-apps/apps/vol_overview", STRIPPED_APP_PROMPTS),
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


def test_adversarial_matrix_rejects_every_applicable_grouping_mutant() -> None:
    tasks = [
        task
        for task in load_builtin_tasks("build-openbb-apps")
        if task.family == "grouping"
    ]

    matrix = run_adversarial_matrix(tasks, runtime_sample_per_family=1)
    rows = matrix.rows()

    assert tasks
    assert rows
    assert all(row["applicable"] > 0 and row["exercised"] > 0 for row in rows)
    assert all(row["expected_code_observed"] == row["exercised"] for row in rows)
    assert {archetype for _family, archetype in matrix.applicable} == {
        "fieldless_contributor",
        "incompatible_values",
        "never_instantiated",
        "note_only_proof",
        "one_widget_missing",
        "severed_shared_interaction",
        "wrong_endpoint_data",
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
