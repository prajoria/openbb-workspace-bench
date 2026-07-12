"""Calibration metrics, costing, and empirical-label proposal tests."""

from __future__ import annotations

import json
from pathlib import Path
import runpy

import pytest

from workspace_bench.reports.metrics import summarize_result_rows, task_reliability_matrix
from workspace_bench.reports.model_compare import (
    ModelAdapter,
    ensure_run_manifest,
    finalize_usage,
    openai_usage,
)

PROPOSE = runpy.run_path(
    str(Path(__file__).resolve().parents[1] / "scripts/propose_measured_difficulty.py")
)["propose"]


def _row(
    task_ref: str,
    repeat: int,
    passed: bool,
    *,
    failed_calls: int = 0,
) -> dict:
    return {
        "id": task_ref.rsplit("/", 1)[-1],
        "qualified_id": task_ref,
        "family": task_ref.split("/")[-2],
        "difficulty": "medium",
        "repeat": repeat,
        "passed": passed,
        "state_passed": passed,
        "runtime_passed": passed,
        "runtime_checks_total": 1,
        "browser_verdict": "pending",
        "tool_call_count": 4,
        "failed_tool_call_count": failed_calls,
        "input_tokens": 10,
        "output_tokens": 5,
        "total_tokens": 15,
        "wall_time_seconds": 2.0,
        "cost_usd": 0.01,
    }


def test_calibration_metrics_include_variance_recovery_and_cost() -> None:
    rows = [
        _row("build-openbb-apps/forms/a", 1, True, failed_calls=1),
        _row("build-openbb-apps/forms/a", 2, False),
        _row("build-openbb-apps/debug/b", 1, True),
        _row("build-openbb-apps/debug/b", 2, True),
    ]

    summary = summarize_result_rows(rows)
    matrix = task_reliability_matrix(rows)

    assert summary["strict_pass_rate"] == 0.75
    assert summary["invalid_tool_call_rate"] == 1 / 16
    assert summary["median_turns"] == 4
    assert summary["recovery_after_failure_rate"] == 1.0
    assert summary["flip_rate"] == 0.5
    assert summary["pass_at_k"] == 1.0
    assert summary["pass_power_k"] == 0.5
    assert summary["cost_usd"] == 0.04
    forms = next(item for item in matrix if item["family"] == "forms")
    assert forms["outcomes"] == [True, False]
    assert forms["flip_rate"] == 1.0


def test_openai_usage_prefers_provider_cost_and_can_estimate() -> None:
    usage = openai_usage(
        {
            "usage": {
                "prompt_tokens": 100,
                "completion_tokens": 20,
                "total_tokens": 120,
                "cost": 0.004,
            }
        }
    )
    adapter = ModelAdapter("m", "M", "", {}, "openrouter", "vendor/model")
    reported = finalize_usage(
        adapter,
        {
            "api_calls": 1,
            **usage,
            "provider_cost_reported": True,
        },
    )
    priced_adapter = ModelAdapter(
        "p",
        "P",
        "",
        {},
        "openai",
        "model",
        input_cost_per_million=2.0,
        cached_input_cost_per_million=0.2,
        output_cost_per_million=8.0,
        pricing_source="published",
    )
    estimated = finalize_usage(
        priced_adapter,
        {
            "api_calls": 1,
            "input_tokens": 100,
            "cached_tokens": 80,
            "output_tokens": 20,
            "total_tokens": 120,
            "provider_cost_reported": False,
        },
    )

    assert reported["cost_usd"] == 0.004
    assert reported["cost_source"] == "provider"
    assert estimated["cost_usd"] == 0.000216
    assert estimated["cost_source"] == "published"


def test_resume_manifest_rejects_incompatible_cells(tmp_path) -> None:
    path = tmp_path / "model.manifest.json"
    manifest = {"schema_version": "v1", "model": "a", "tasks": ["one"]}
    ensure_run_manifest(path, manifest, resume=False)
    ensure_run_manifest(path, manifest, resume=True)

    with pytest.raises(ValueError, match="manifest differs"):
        ensure_run_manifest(path, {**manifest, "tasks": ["two"]}, resume=True)
    assert json.loads(path.read_text(encoding="utf-8")) == manifest

    legacy = tmp_path / "legacy.manifest.json"
    legacy.write_text(
        json.dumps({**manifest, "pricing": {"input_per_million": 1.0}}),
        encoding="utf-8",
    )
    ensure_run_manifest(legacy, manifest, resume=True)
    assert json.loads(legacy.read_text(encoding="utf-8")) == manifest


def test_empirical_difficulty_proposal_emits_reviewable_override_table() -> None:
    tasks = [
        ("build-openbb-apps/types/easy", "easy"),
        ("build-openbb-apps/forms/medium", "hard"),
        ("build-openbb-apps/debug/hard", "medium"),
    ]
    model_a = {
        "model": {"slug": "frontier"},
        "results": [
            {
                "qualified_id": ref,
                "family": ref.split("/")[-2],
                "difficulty": old,
                "repeat": repeat,
                "passed": ref.endswith(("easy", "medium")),
            }
            for ref, old in tasks
            for repeat in (1, 2)
        ],
    }
    model_b = {
        "model": {"slug": "small"},
        "results": [
            {
                "qualified_id": ref,
                "family": ref.split("/")[-2],
                "difficulty": old,
                "repeat": repeat,
                "passed": ref.endswith("easy"),
            }
            for ref, old in tasks
            for repeat in (1, 2)
        ],
    }
    proposal = PROPOSE(
        [model_a, model_b],
        {
            "competent_models": ["frontier", "small"],
            "frontier_models": ["frontier"],
            "small_models": ["small"],
            "overrides": {"build-openbb-apps/charts/existing": "hard"},
        },
    )

    raw = {row["task_ref"]: row["raw_proposed"] for row in proposal["rows"]}
    proposed = {row["task_ref"]: row["proposed"] for row in proposal["rows"]}
    assert raw == {
        "build-openbb-apps/debug/hard": "hard",
        "build-openbb-apps/forms/medium": "medium",
        "build-openbb-apps/types/easy": "easy",
    }
    assert proposed == {
        "build-openbb-apps/debug/hard": "hard",
        "build-openbb-apps/forms/medium": "hard",
        "build-openbb-apps/types/easy": "easy",
    }
    assert proposal["override_table"]["bands"] == {"easy": 1, "medium": 0, "hard": 2}
    assert proposal["override_table"]["overrides"] == {
        "build-openbb-apps/charts/existing": "hard",
        "build-openbb-apps/debug/hard": "hard",
    }
