"""Generate the enterprise-apps-default suite: every product prompt of every app.

One task per (enterprise app, bundled product prompt). Prompts are carried
byte-verbatim from the Stark catalog — the benchmark never edits what the
product asks — and grading is outcomes-only: the agent must leave a note
artifact that cites exact facts recoverable from the app's served widget data
(which forces real data reads without constraining the tool path) plus the
prompt's own anchor terms.

Rubric provenance: widget relevance and fact fields are first derived
mechanically (token overlap between the prompt and widget identities), then
reviewed per prompt; every reviewed adjustment lives in RUBRIC_OVERRIDES so
derivation and judgment stay separable. Difficulty is a placeholder pending
empirical measurement (see the suite README).

Tasks start inside the app (``initial_state.active_dashboard``) on top of the
default-workspace-v1 baseline declared by the suite manifest.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))

from dataclasses import replace  # noqa: E402

from workspace_bench.core.episode import WorkspaceEpisode  # noqa: E402
from workspace_bench.core.models import Task, TaskSuiteManifest, ToolCall  # noqa: E402

CATALOG_PATH = REPO / "src/workspace_bench/workspace/data/stark_enterprise.json"
OUT_DIR = REPO / "src/workspace_bench/task_suites/enterprise_apps_default"
ORIGIN = "Bench Stark Enterprise"
SUITE_ID = "workspace-bench-enterprise-apps-default"
WORKSPACE_BASELINE = "default-v1"
MAX_GRADED_TERMS = 6

STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "of",
    "for",
    "with",
    "that",
    "which",
    "should",
    "be",
    "to",
    "by",
    "in",
    "on",
    "before",
    "since",
    "where",
    "what",
    "their",
    "needs",
    "needed",
    "into",
    "from",
    "each",
    "its",
    "are",
    "is",
    "draft",
    "create",
    "build",
    "prepare",
    "explain",
    "identify",
    "find",
    "summarize",
    "compare",
    "highlight",
    "rank",
    "list",
    "review",
    "current",
    "last",
    "next",
    "open",
    "selected",
    "because",
}

PREFERRED_FACT_FIELDS = (
    "var_usd",
    "drawdown_usd",
    "loss_usd",
    "weight",
    "exposure",
    "latency_ms",
    "breach_count",
    "alert_count",
    "exception_count",
    "order_count",
    "count",
    "return",
    "price_usd",
    "value_usd",
    "aum_usd",
    "score",
    "value",
)

# Reviewed rubric adjustments, keyed by (app_slug, prompt_index). Supported
# keys: "widgets" (ordered widget ids to read/cite), "prompt_terms" (verbatim
# anchor words from the prompt). Derivation fills anything not overridden.
RUBRIC_OVERRIDES: dict[tuple[str, int], dict] = {
    ("portfolio_command_center", 1): {
        "widgets": [
            "portfolio_command_center_holdings_sector_exposure",
            "portfolio_command_center_overview_limit_utilization",
            "portfolio_command_center_actions_trade_ideas",
        ],
        "prompt_terms": ["overnight", "exposures"],
    },
    ("portfolio_command_center", 3): {
        "widgets": [
            "portfolio_command_center_overview_top_alerts",
            "portfolio_command_center_overview_limit_utilization",
            "portfolio_command_center_actions_approval_checklist",
        ],
        "prompt_terms": ["alerts", "escalated"],
    },
    ("rebalance_scenario_lab", 1): {
        "widgets": [
            "rebalance_scenario_lab_drift_current_vs_target_weights",
            "rebalance_scenario_lab_rebalance_liquidity_impact",
            "rebalance_scenario_lab_rebalance_restricted_list_checks",
        ],
        "prompt_terms": ["rebalance", "drift"],
    },
    ("rebalance_scenario_lab", 2): {
        "widgets": [
            "rebalance_scenario_lab_rebalance_proposed_trades",
            "rebalance_scenario_lab_rebalance_liquidity_impact",
            "rebalance_scenario_lab_drift_constraint_utilization",
        ],
        "prompt_terms": ["constraints", "compliance"],
    },
    ("rebalance_scenario_lab", 3): {
        "widgets": [
            "rebalance_scenario_lab_approval_implementation_readiness",
            "rebalance_scenario_lab_drift_drift_by_sleeve",
            "rebalance_scenario_lab_approval_approval_checklist",
        ],
        "prompt_terms": ["implementation", "approval"],
    },
    ("strategy_health_monitor", 1): {
        "widgets": [
            "strategy_health_monitor_performance_sleeve_performance",
            "strategy_health_monitor_themes_crowded_names",
            "strategy_health_monitor_capacity_capacity_utilization",
        ],
        "prompt_terms": ["drawdown", "capacity"],
    },
    ("strategy_health_monitor", 2): {
        "prompt_terms": ["conviction", "capacity"],
    },
    ("equity_research_workbench", 1): {
        "widgets": [
            "equity_research_workbench_company_consensus_revisions",
            "equity_research_workbench_valuation_valuation_assumption_log",
            "equity_research_workbench_thesis_analyst_thesis_note",
        ],
        "prompt_terms": ["estimates", "valuation"],
    },
    ("equity_research_workbench", 2): {
        "widgets": [
            "equity_research_workbench_coverage_price_target_upside",
            "equity_research_workbench_coverage_price_target_history",
            "equity_research_workbench_valuation_dcf_sensitivity",
        ],
        "prompt_terms": ["sensitivity", "valuation"],
    },
    ("equity_research_workbench", 3): {
        "widgets": [
            "equity_research_workbench_thesis_catalysts_and_risks",
            "equity_research_workbench_thesis_draft_research_review",
            "equity_research_workbench_thesis_sell_side_research_pdfs",
        ],
        "prompt_terms": ["catalysts", "approvals"],
    },
    ("earnings_estimates_monitor", 2): {
        "widgets": [
            "earnings_estimates_monitor_post_earnings_price_reaction",
            "earnings_estimates_monitor_transcript_management_tone",
            "earnings_estimates_monitor_post_earnings_post_earnings_checklist",
        ],
        "prompt_terms": ["transcript", "checklist"],
    },
    ("earnings_estimates_monitor", 3): {
        "widgets": [
            "earnings_estimates_monitor_post_earnings_thesis_change_log",
            "earnings_estimates_monitor_estimates_consensus_revisions",
            "earnings_estimates_monitor_transcript_management_tone",
        ],
        "prompt_terms": ["management", "commentary"],
    },
    ("corporate_access_meeting_notes", 1): {
        "widgets": [
            "corporate_access_meeting_notes_claims_management_claims_tracker",
            "corporate_access_meeting_notes_meetings_expert_calls",
            "corporate_access_meeting_notes_compliance_mnpi_attestation_status",
        ],
        "prompt_terms": ["MNPI", "follow-ups"],
    },
    ("corporate_access_meeting_notes", 2): {
        "prompt_terms": ["meetings", "compliance"],
    },
    ("corporate_access_meeting_notes", 3): {
        "prompt_terms": ["management", "evidence"],
    },
    ("execution_desk", 1): {
        "widgets": [
            "execution_desk_blotter_order_risk_queue",
            "execution_desk_exceptions_restricted_list_checks",
            "execution_desk_fills_vwap_and_arrival_slippage",
        ],
        "prompt_terms": ["liquidity", "slippage"],
    },
    ("execution_desk", 2): {
        "prompt_terms": ["fills", "arrival"],
    },
    ("execution_desk", 3): {
        "widgets": [
            "execution_desk_exceptions_rejected_orders",
            "execution_desk_exceptions_restricted_list_checks",
            "execution_desk_exceptions_surveillance_alerts",
        ],
        "prompt_terms": ["execution", "exception"],
    },
    ("liquidity_tca_workbench", 1): {
        "prompt_terms": ["execution", "shortfall"],
    },
    ("liquidity_tca_workbench", 2): {
        "widgets": [
            "liquidity_tca_workbench_brokers_broker_scorecard",
            "liquidity_tca_workbench_brokers_fill_quality_by_broker",
            "liquidity_tca_workbench_tca_slippage_by_algo",
        ],
        "prompt_terms": ["commission", "slippage"],
    },
    ("liquidity_tca_workbench", 3): {
        "widgets": [
            "liquidity_tca_workbench_notes_post_trade_review_queue",
            "liquidity_tca_workbench_notes_broker_exception_follow_ups",
            "liquidity_tca_workbench_tca_slippage_by_algo",
        ],
        "prompt_terms": ["broker", "parameter"],
    },
    ("risk_exposure_monitor", 1): {
        "prompt_terms": ["concentration", "breaches"],
    },
    ("risk_exposure_monitor", 2): {
        "widgets": [
            "risk_exposure_monitor_drilldown_position_risk_contribution",
            "risk_exposure_monitor_drilldown_marginal_var",
            "risk_exposure_monitor_exposures_exposure_table",
        ],
        "prompt_terms": ["positions", "VaR"],
    },
    ("stress_liquidity_lab", 1): {
        "widgets": [
            "stress_liquidity_lab_stress_tests_scenario_loss_waterfall",
            "stress_liquidity_lab_liquidity_days_to_liquidate",
            "stress_liquidity_lab_liquidity_redemption_stress",
        ],
        "prompt_terms": ["liquidation", "redemption"],
    },
    ("stress_liquidity_lab", 2): {
        "prompt_terms": ["assumptions", "committee"],
    },
    ("client_360", 1): {
        "widgets": [
            "client_360_portfolio_view_client_returns",
            "client_360_portfolio_view_exposure_summary",
            "client_360_flows_subscriptions_and_redemptions",
        ],
        "prompt_terms": ["performance", "investor"],
    },
    ("client_360", 2): {
        "widgets": [
            "client_360_flows_subscriptions_and_redemptions",
            "client_360_meeting_prep_open_requests",
            "client_360_client_book_relationship_metrics",
        ],
        "prompt_terms": ["redemption", "unresolved"],
    },
    ("reporting_factsheet_studio", 1): {
        "widgets": [
            "reporting_factsheet_studio_performance_monthly_returns",
            "reporting_factsheet_studio_performance_attribution_summary",
            "reporting_factsheet_studio_ddqs_ddq_and_rfp_tracker",
        ],
        "prompt_terms": ["performance", "attribution"],
    },
    ("reporting_factsheet_studio", 3): {
        "widgets": [
            "reporting_factsheet_studio_performance_monthly_returns",
            "reporting_factsheet_studio_performance_attribution_summary",
            "reporting_factsheet_studio_commentary_approved_commentary_library",
        ],
        "prompt_terms": ["attribution", "commentary"],
    },
    ("compliance_surveillance_hub", 1): {
        "widgets": [
            "compliance_surveillance_hub_alerts_surveillance_alerts",
            "compliance_surveillance_hub_restricted_list_restricted_and_watch_list",
            "compliance_surveillance_hub_audit_investigation_evidence",
        ],
        "prompt_terms": ["surveillance", "severity"],
    },
    ("compliance_surveillance_hub", 2): {
        "widgets": [
            "compliance_surveillance_hub_personal_trading_employee_trades",
            "compliance_surveillance_hub_personal_trading_policy_breaches",
            "compliance_surveillance_hub_alerts_surveillance_alerts",
        ],
        "prompt_terms": ["compliance", "leadership"],
    },
    ("compliance_surveillance_hub", 3): {
        "widgets": [
            "compliance_surveillance_hub_audit_investigation_evidence",
            "compliance_surveillance_hub_audit_investigation_notes",
            "compliance_surveillance_hub_personal_trading_policy_breaches",
        ],
        "prompt_terms": ["investigation", "remediation"],
    },
    ("mnpi_research_review", 1): {
        "widgets": [
            "mnpi_research_review_mnpi_log_wall_crossings",
            "mnpi_research_review_meetings_company_meeting_logs",
            "mnpi_research_review_research_draft_research_review",
        ],
        "prompt_terms": ["crossings", "meetings"],
    },
    ("mnpi_research_review", 2): {
        "widgets": [
            "mnpi_research_review_research_draft_research_review",
            "mnpi_research_review_evidence_research_approval_evidence",
            "mnpi_research_review_evidence_evidence_and_sign_off_history",
        ],
        "prompt_terms": ["research", "evidence"],
    },
    ("mnpi_research_review", 3): {
        "widgets": [
            "mnpi_research_review_evidence_research_approval_evidence",
            "mnpi_research_review_research_reviewer_comments",
            "mnpi_research_review_evidence_evidence_and_sign_off_history",
        ],
        "prompt_terms": ["attestations", "unresolved"],
    },
    ("fund_operations_control_tower", 1): {
        "widgets": [
            "fund_operations_control_tower_trade_lifecycle_failed_trades",
            "fund_operations_control_tower_recons_custodian_breaks",
            "fund_operations_control_tower_pricing_nav_exceptions",
        ],
        "prompt_terms": ["operations", "exceptions"],
    },
    ("fund_operations_control_tower", 2): {
        "widgets": [
            "fund_operations_control_tower_recons_custodian_breaks",
            "fund_operations_control_tower_recons_break_aging",
            "fund_operations_control_tower_trade_lifecycle_settlement_exceptions",
        ],
        "prompt_terms": ["breaks", "settlement"],
    },
    ("fund_operations_control_tower", 3): {
        "widgets": [
            "fund_operations_control_tower_trade_lifecycle_settlement_exceptions",
            "fund_operations_control_tower_pricing_nav_exceptions",
            "fund_operations_control_tower_corporate_actions_election_deadlines",
        ],
        "prompt_terms": ["operational", "escalation"],
    },
    ("nav_fees_close_dashboard", 1): {
        "widgets": [
            "nav_fees_close_dashboard_nav_nav_bridge",
            "nav_fees_close_dashboard_fees_fee_accruals",
            "nav_fees_close_dashboard_close_close_dependency_register",
        ],
        "prompt_terms": ["dependencies", "exceptions"],
    },
    ("nav_fees_close_dashboard", 2): {
        "widgets": [
            "nav_fees_close_dashboard_nav_nav_sign_off_tasks",
            "nav_fees_close_dashboard_close_close_exceptions",
            "nav_fees_close_dashboard_close_close_dependency_register",
        ],
        "prompt_terms": ["NAV", "sign-off"],
    },
    ("nav_fees_close_dashboard", 3): {
        "widgets": [
            "nav_fees_close_dashboard_fees_fee_accruals",
            "nav_fees_close_dashboard_cash_cash_break_aging",
            "nav_fees_close_dashboard_close_close_exceptions",
        ],
        "prompt_terms": ["exceptions", "controller"],
    },
    ("executive_investment_dashboard", 1): {
        "prompt_terms": ["AUM", "stress"],
    },
    ("executive_investment_dashboard", 2): {
        "prompt_terms": ["issues", "CIO"],
    },
    ("executive_investment_dashboard", 3): {
        "prompt_terms": ["performance", "flows"],
    },
    ("cio_investment_committee_pack", 2): {
        "widgets": [
            "cio_investment_committee_pack_allocations_recommended_changes",
            "cio_investment_committee_pack_allocations_capacity",
            "cio_investment_committee_pack_research_changed_ratings",
        ],
        "prompt_terms": ["recommendations", "allocation"],
    },
    ("workspace_data_control_center", 2): {
        "widgets": [
            "workspace_data_control_center_entitlements_app_and_widget_permissions",
            "workspace_data_control_center_entitlements_sensitive_dataset_flags",
            "workspace_data_control_center_ai_access_copilot_visibility_flags",
        ],
        "prompt_terms": ["restricted", "production"],
    },
    ("workspace_data_control_center", 3): {
        "widgets": [
            "workspace_data_control_center_usage_app_usage",
            "workspace_data_control_center_usage_export_activity",
            "workspace_data_control_center_ai_access_prompt_audit",
        ],
        "prompt_terms": ["usage", "prompt-audit"],
    },
    ("vendor_dataset_monitor", 1): {
        "widgets": [
            "vendor_dataset_monitor_slas_latency_by_feed",
            "vendor_dataset_monitor_slas_freshness_exceptions",
            "vendor_dataset_monitor_quality_validation_errors",
        ],
        "prompt_terms": ["validation", "freshness"],
    },
    ("quant_research_backtest_lab", 1): {
        "widgets": [
            "quant_research_backtest_lab_signals_signal_metrics",
            "quant_research_backtest_lab_backtest_backtest_performance",
            "quant_research_backtest_lab_risk_model_factor_exposure_table",
        ],
        "prompt_terms": ["signal", "exposures"],
    },
    ("quant_research_backtest_lab", 2): {
        "prompt_terms": ["signals", "turnover"],
    },
    ("quant_research_backtest_lab", 3): {
        "widgets": [
            "quant_research_backtest_lab_signals_signal_metrics",
            "quant_research_backtest_lab_backtest_backtest_performance",
            "quant_research_backtest_lab_risk_model_factor_exposure_table",
        ],
        "prompt_terms": ["approval", "model"],
    },
    ("healthcare_research_dashboard", 1): {
        "widgets": [
            "healthcare_research_dashboard_clinical_clinical_probability_funnel",
            "healthcare_research_dashboard_commercial_tam_scenarios",
            "healthcare_research_dashboard_commercial_prescription_trend",
        ],
        "prompt_terms": ["prescriptions", "probability"],
    },
    ("healthcare_research_dashboard", 3): {
        "widgets": [
            "healthcare_research_dashboard_clinical_kol_meeting_notes",
            "healthcare_research_dashboard_documents_research_document_checklist",
            "healthcare_research_dashboard_clinical_clinical_probability_funnel",
        ],
        "prompt_terms": ["KOL", "follow-up"],
    },
    ("crypto_research_dashboard", 1): {
        "prompt_terms": ["liquidity", "liquidation"],
    },
    ("crypto_research_dashboard", 2): {
        "widgets": [
            "crypto_research_dashboard_derivatives_funding_and_basis",
            "crypto_research_dashboard_on_chain_on_chain_activity",
            "crypto_research_dashboard_market_price_and_volume",
        ],
        "prompt_terms": ["derivatives", "positioning"],
    },
    ("crypto_research_dashboard", 3): {
        "widgets": [
            "crypto_research_dashboard_market_price_and_volume",
            "crypto_research_dashboard_on_chain_on_chain_activity",
            "crypto_research_dashboard_derivatives_funding_and_basis",
        ],
        "prompt_terms": ["thesis", "on-chain"],
    },
}


def slugify_id(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def app_widget_ids(app: dict) -> list[str]:
    seen: list[str] = []
    for tab in app.get("tabs", {}).values():
        for layout in tab.get("layout", []):
            widget_id = str(layout.get("i", ""))
            if widget_id and widget_id != "navigation_bar" and widget_id not in seen:
                seen.append(widget_id)
    return seen


def widget_layout_params(app: dict, widget_id: str) -> dict:
    for tab in app.get("tabs", {}).values():
        for layout in tab.get("layout", []):
            if str(layout.get("i")) == widget_id:
                return dict((layout.get("state") or {}).get("params") or {})
    return {}


def tokenize(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z][a-z\-&]+", text.lower())
        if token not in STOPWORDS and len(token) > 3
    ]


def derive_widgets(app: dict, widgets: dict, prompt: str, count: int = 3) -> list[str]:
    """Rank the app's widgets by identity-token overlap with the prompt."""

    prompt_tokens = set(tokenize(prompt))
    scored: list[tuple[float, int, str]] = []
    for position, widget_id in enumerate(app_widget_ids(app)):
        definition = widgets.get(widget_id) or {}
        identity = " ".join(
            [
                widget_id.replace("_", " "),
                str(definition.get("name", "")),
                str(definition.get("description", "")),
            ]
        )
        overlap = len(prompt_tokens & set(tokenize(identity)))
        scored.append((-float(overlap), position, widget_id))
    scored.sort()
    return [widget_id for _, _, widget_id in scored[:count]]


def widget_fact(widgets: dict, widget_id: str) -> tuple[str, str] | None:
    """One (field, exact value) fact from the widget's baked rows."""

    payload = (widgets.get(widget_id) or {}).get("data")
    rows = (
        payload
        if isinstance(payload, list)
        else (payload.get("series") if isinstance(payload, dict) else None)
    )
    if not isinstance(rows, list):
        return None
    for row in rows:
        if not isinstance(row, dict):
            continue
        for field in PREFERRED_FACT_FIELDS:
            if field in row and isinstance(row[field], (int, float)):
                return field, _fact_value(row[field])
        for field, value in row.items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return field, _fact_value(value)
    return None


def _fact_value(value: float | int) -> str:
    if isinstance(value, int):
        return str(value)
    return f"{value:g}"


def derive_prompt_terms(prompt: str, count: int = 2) -> list[str]:
    """The prompt's most distinctive words, kept verbatim for note anchoring."""

    tokens = [token for token in tokenize(prompt) if "-" not in token and "&" not in token]
    ranked = sorted(set(tokens), key=lambda token: (-len(token), tokens.index(token)))
    return ranked[:count]


def build_tasks() -> list[dict]:
    catalog = load_catalog()
    widgets = catalog["widgets"]
    tasks: list[dict] = []
    for app in catalog["apps"]:
        app_slug = slugify_id(str(app.get("template_id") or app["name"]))
        for index, prompt in enumerate(app.get("prompts") or [], start=1):
            override = RUBRIC_OVERRIDES.get((app_slug, index), {})
            chosen = override.get("widgets") or derive_widgets(app, widgets, prompt)
            prompt_terms = override.get("prompt_terms") or derive_prompt_terms(prompt)
            facts: list[tuple[str, str]] = []
            fact_sources: list[str] = []
            for widget_id in chosen:
                fact = widget_fact(widgets, widget_id)
                if fact:
                    facts.append(fact)
                    fact_sources.append(widget_id)
            facts = facts[: MAX_GRADED_TERMS - len(prompt_terms) - 1]
            fact_sources = fact_sources[: len(facts)]
            note_terms = list(prompt_terms) + [value for _, value in facts]
            note_text = (
                f"{prompt.split('.')[0].strip()}: "
                + "; ".join(
                    f"{widget_id.rsplit('_', 1)[-1]} {field} is {value}"
                    for widget_id, (field, value) in zip(fact_sources, facts)
                )
                + ". Anchors: "
                + ", ".join(prompt_terms)
                + "."
            )
            oracle = [{"tool": "get_workspace_snapshot", "args": {}}]
            for widget_id in fact_sources or chosen[:2]:
                oracle.append(
                    {
                        "tool": "get_widget_data",
                        "args": {
                            "origin": ORIGIN,
                            "widget_id": widget_id,
                            "data_args": widget_layout_params(app, widget_id),
                        },
                    }
                )
            oracle.append(
                {
                    "tool": "add_generative_widget",
                    "args": {
                        "widget_type": "note",
                        "name": f"{app['name']} Note",
                        "data": note_text,
                    },
                }
            )
            tasks.append(
                {
                    "id": f"{app_slug}_p{index}",
                    "category": "read",
                    "family": app_slug,
                    "difficulty": "medium",
                    "prompt": prompt,
                    "fixtures": {"backends": [{"name": "stark-enterprise"}]},
                    "initial_state": {"active_dashboard": app["name"]},
                    "allowed_tools": [
                        "get_workspace_snapshot",
                        "navigate_workspace",
                        "get_widget_data",
                        "read_widget",
                        "add_generative_widget",
                    ],
                    "success": {
                        "required_generated_widgets": [
                            {"widget_type": "note", "data_contains": note_terms}
                        ]
                    },
                    "oracle_tool_calls": oracle,
                    "limits": {"max_turns": 2 * len(oracle) + 4},
                }
            )
    return tasks


def certify(tasks: list[dict], catalog: dict) -> None:
    manifest = TaskSuiteManifest(
        suite_id=SUITE_ID,
        visibility="public",
        workspace_baseline=WORKSPACE_BASELINE,
    )
    product_prompts = {prompt for app in catalog["apps"] for prompt in (app.get("prompts") or [])}
    for payload in tasks:
        assert payload["prompt"] in product_prompts, (
            f"{payload['id']}: prompt is not byte-verbatim from the product catalog"
        )
        assert set(payload["success"]) == {"required_generated_widgets"}, (
            f"{payload['id']}: rubric must stay outcomes-only"
        )
        terms = payload["success"]["required_generated_widgets"][0]["data_contains"]
        assert 2 <= len(terms) <= MAX_GRADED_TERMS, (
            f"{payload['id']}: graded terms out of range ({len(terms)})"
        )
        task = replace(Task.from_dict(json.loads(json.dumps(payload))), suite=manifest)
        episode = WorkspaceEpisode(task=task)
        for call_payload in payload["oracle_tool_calls"]:
            result = episode.step(ToolCall(call_payload["tool"], call_payload.get("args", {})))
            assert result.get("ok"), (
                f"{payload['id']}: oracle call {call_payload['tool']} failed: "
                f"{(result.get('error') or {}).get('message')}"
            )
        grade = episode.grade()
        assert grade.passed, f"{payload['id']}: oracle does not pass: " + "; ".join(
            f"{issue.code}: {issue.message}" for issue in grade.issues
        )
        noop_episode = WorkspaceEpisode(task=task)
        assert not noop_episode.grade().passed, f"{payload['id']}: noop passes"


def main() -> int:
    catalog = load_catalog()
    tasks = build_tasks()
    ids = [task["id"] for task in tasks]
    duplicate_ids = [task_id for task_id, count in Counter(ids).items() if count > 1]
    assert not duplicate_ids, f"duplicate task ids: {duplicate_ids}"
    certify(tasks, catalog)
    if OUT_DIR.exists():
        for stale in OUT_DIR.rglob("*.json"):
            if stale.name != "task_suite.json":
                stale.unlink()
    for payload in tasks:
        family_dir = OUT_DIR / payload["family"]
        family_dir.mkdir(parents=True, exist_ok=True)
        (family_dir / f"{payload['id']}.json").write_text(
            json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    (OUT_DIR / "__init__.py").write_text("", encoding="utf-8")
    manifest_payload = {
        "suite_id": SUITE_ID,
        "visibility": "public",
        "workspace_baseline": WORKSPACE_BASELINE,
        "description": (
            "Every bundled product prompt of every enterprise app, run inside "
            "the default workspace and graded on outcome artifacts only."
        ),
    }
    (OUT_DIR / "task_suite.json").write_text(
        json.dumps(manifest_payload, indent=1) + "\n", encoding="utf-8"
    )
    print(f"Wrote {len(tasks)} tasks to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
