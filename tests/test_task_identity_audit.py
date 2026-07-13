from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts/audits"))

from audit_task_identity import (  # noqa: E402
    audit_prompt_openness,
    audit_task,
    repeated_token_phrase,
)
from audit_release_consistency import audit_text  # noqa: E402


def test_repeated_token_phrase_finds_join_scars() -> None:
    assert repeated_token_phrase("post_earnings_post_earnings_checklist".split("_")) == (
        "post_earnings"
    )
    assert repeated_token_phrase("drift_drift_by_sleeve".split("_")) == "drift"
    assert repeated_token_phrase("price_performance_aapl".split("_")) is None


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


def _open_prompt_task(specification_level: str, prompt: str, terms: list[str]) -> dict:
    return {
        "id": "revision_monitor",
        "specification_level": specification_level,
        "prompt": prompt,
        "business_terms": terms,
        "oracle_tool_calls": [
            {
                "tool": "manage_backends",
                "args": {
                    "name": "Earnings Source",
                    "url": "http://localhost:7805",
                    "widgets_json": {
                        "revision_grid": {
                            "type": "table_ssrm",
                            "endpoint": "/revision-momentum",
                            "refetchInterval": 30000,
                            "params": [{"paramName": "ticker", "type": "ticker"}],
                            "data": {
                                "table": {
                                    "columnsDefs": [
                                        {"field": "revised_up"},
                                        {"field": "revised_down"},
                                    ]
                                }
                            },
                        }
                    },
                    "apps_json": [
                        {
                            "name": "Revision Room",
                            "tabs": {
                                "monitor": {
                                    "name": "Monitor",
                                    "layout": [
                                        {"i": "revision_grid", "x": 0, "y": 0, "w": 20, "h": 8}
                                    ],
                                }
                            },
                        }
                    ],
                },
            }
        ],
    }


def test_hard_prompt_openness_flags_oracle_implementation_details() -> None:
    task = _open_prompt_task(
        "open-brief",
        "Build revision_grid as a table_ssrm at /revision-momentum with revised_up; "
        'place it at {"x": 0, "y": 0, "w": 20, "h": 8}.',
        [],
    )
    reasons = [
        finding.reason for finding in audit_prompt_openness("build-openbb-apps", "aggrid", task)
    ]
    assert sum("implementation_identifier_leak" in reason for reason in reasons) >= 4
    assert any("layout_coordinate_leak" in reason for reason in reasons)


def test_medium_prompt_openness_allows_only_declared_anchors() -> None:
    task = _open_prompt_task(
        "partially-specified",
        "Build an earnings revision monitor anchored on `ticker` and `revised_up`.",
        ["ticker", "revised_up"],
    )
    assert not audit_prompt_openness("build-openbb-apps", "aggrid", task)
    task["prompt"] += " Use /revision-momentum."
    findings = audit_prompt_openness("build-openbb-apps", "aggrid", task)
    assert any("endpoint path" in finding.reason for finding in findings)


def test_hard_prompt_openness_masks_declared_business_product_name() -> None:
    task = _open_prompt_task(
        "open-brief",
        "Deliver the desk product called Revision Room for an earnings analyst.",
        ["Revision Room"],
    )
    assert not audit_prompt_openness("build-openbb-apps", "aggrid", task)


def test_release_consistency_allows_only_explicitly_archived_counts() -> None:
    path = Path("README.md")
    content = """# Current\n212 tasks\n## Archived Baselines\nformer 212 and 512 tasks\n## Evaluate Your Agent\n512 tasks\n"""
    findings = audit_text(path, content)
    assert [finding.line for finding in findings] == [2, 6]


def test_release_consistency_flags_cross_phase_claims() -> None:
    stale = (
        "The "
        + str(236)
        + " open product briefs have no "
        + "browser harness and no "
        + "runtime verification.\n"
    )
    findings = audit_text(
        Path("example.md"),
        stale,
    )
    reasons = {finding.reason for finding in findings}
    assert "stale claim (build_prompt_level_collapse)" in reasons
    assert "stale claim (browser_harness_outdated)" in reasons
    assert "stale claim (runtime_verification_denial)" in reasons


def test_release_consistency_rejects_wrong_archetype_count() -> None:
    findings = audit_text(Path("README.md"), "The matrix covers eight archetypes.\n")
    assert [finding.reason for finding in findings] == [
        "wrong adversarial archetype count: eight (expected twelve)"
    ]
