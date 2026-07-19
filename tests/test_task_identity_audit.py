from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts/audits"))

from audit_task_identity import (  # noqa: E402
    audit_task,
    repeated_token_phrase,
)
from audit_release_consistency import audit_text  # noqa: E402


def test_repeated_token_phrase_finds_join_scars() -> None:
    assert repeated_token_phrase("post_earnings_post_earnings_checklist".split("_")) == (
        "post_earnings"
    )
    assert repeated_token_phrase("drift_drift_by_sleeve".split("_")) == "drift"
    assert repeated_token_phrase("decision_briefing_level0".split("_")) is None


def test_audit_task_flags_generator_identity_and_prompt_scars() -> None:
    findings = audit_task(
        "enterprise-apps-usage",
        "inspect",
        {
            "id": "inspect_drift_drift_3",
            "title": "Inspect Drift Drift",
            "prompt": "Use r3 and then then inspect {{widget}}.",
        },
    )
    reasons = {(finding.field, finding.reason.split(":", 1)[0]) for finding in findings}
    assert ("id", "repeated token phrase") in reasons
    assert ("id", "numeric generator suffix") in reasons
    assert ("prompt", "internal benchmark jargon") in reasons
    assert ("prompt", "placeholder residue") in reasons
    assert ("prompt", "repeated word") in reasons


def test_audit_task_allows_business_numeric_suffix() -> None:
    assert not audit_task(
        "enterprise-apps-usage",
        "apps",
        {
            "id": "client_360",
            "title": "Client 360",
            "prompt": "Open the Client 360 workspace for the relationship team.",
        },
    )


def test_release_consistency_allows_only_explicitly_archived_counts() -> None:
    path = Path("README.md")
    content = """# Current\n212 tasks\n## Archived Baselines\nformer 212 and 512 tasks\n## Evaluate Your Agent\n512 tasks\n"""
    findings = audit_text(path, content)
    assert [finding.line for finding in findings] == [2, 6]


def test_release_consistency_flags_cross_phase_claims() -> None:
    stale = (
        "The open product briefs have no "
        + "browser harness and no "
        + "runtime verification.\n"
    )
    findings = audit_text(
        Path("example.md"),
        stale,
    )
    reasons = {finding.reason for finding in findings}
    assert "stale claim (browser_harness_outdated)" in reasons
    assert "stale claim (runtime_verification_denial)" in reasons


def test_release_consistency_rejects_wrong_archetype_count() -> None:
    findings = audit_text(Path("README.md"), "The matrix covers eight archetypes.\n")
    assert [finding.reason for finding in findings] == [
        "wrong adversarial archetype count: eight (expected twelve)"
    ]
