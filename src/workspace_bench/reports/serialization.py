"""Shared serialization helpers for benchmark grades."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from workspace_bench.core.models import GradeResult


def grade_summary(grade: GradeResult, *, include_passed: bool = True) -> dict[str, Any]:
    """Serialize every scored grade dimension in the canonical field order."""

    payload: dict[str, Any] = {"score": grade.score}
    if include_passed:
        payload["passed"] = grade.passed
    payload.update(
        {
            "state_score": grade.state_score,
            "state_passed": grade.state_passed,
            "state_checks_passed": grade.state_checks_passed,
            "state_checks_total": grade.state_checks_total,
            "trace_score": grade.trace_score,
            "trace_passed": grade.trace_passed,
            "trace_checks_passed": grade.trace_checks_passed,
            "trace_checks_total": grade.trace_checks_total,
            "runtime_score": grade.runtime_score,
            "runtime_passed": grade.runtime_passed,
            "runtime_checks_passed": grade.runtime_checks_passed,
            "runtime_checks_total": grade.runtime_checks_total,
            "deployment_receipt": (
                asdict(grade.deployment_receipt)
                if grade.deployment_receipt is not None
                else None
            ),
            "polish_score": grade.polish_score,
            "polish_checks_passed": grade.polish_checks_passed,
            "polish_checks_total": grade.polish_checks_total,
            "polish_issues": [
                {"code": issue.code, "message": issue.message}
                for issue in grade.polish_issues
            ],
            "checks_passed": grade.checks_passed,
            "checks_total": grade.checks_total,
            "issues": [
                {"code": issue.code, "message": issue.message} for issue in grade.issues
            ],
        }
    )
    return payload
