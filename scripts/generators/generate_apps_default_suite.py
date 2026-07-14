"""Generate judge-graded enterprise app tasks over Stark data worlds X and Y.

Each bundled product prompt is emitted twice with byte-identical wording and
reference read calls. The final reply and sealed reference answer come from the
manually written answer corpus for the task's exact data world.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))

from dataclasses import replace  # noqa: E402

from workspace_bench.core.episode import WorkspaceEpisode  # noqa: E402
from workspace_bench.core.models import (  # noqa: E402
    JsonDict,
    Task,
    TaskSuiteManifest,
    ToolCall,
)
from workspace_bench.core.suite_checks import task_payload_digest  # noqa: E402
from workspace_bench.workspace.fixtures import (  # noqa: E402
    FixtureBackend,
    build_stark_enterprise_backend,
    build_stark_enterprise_y_backend,
)
from workspace_bench.core.models import WORKSPACE_TOOL_NAMES  # noqa: E402
from workspace_bench.workspace.simulated_workspace import WORKSPACE_SKILLS  # noqa: E402

OUT_DIR = REPO / "src/workspace_bench/task_suites/enterprise_apps_default"
REFERENCE_ANSWERS_PATH = OUT_DIR / "reference_answers.json"
ORIGIN = "Bench Stark Enterprise"
SUITE_ID = "workspace-bench-enterprise-apps-default"
WORKSPACE_BASELINE = "all-stark-enterprise-apps"
TASK_DEFAULTS: JsonDict = {"category": "read", "difficulty": "medium"}
ALLOWED_TOOLS = (*WORKSPACE_TOOL_NAMES, "final_answer")

NUMBER_TOKEN_RE = re.compile(
    r"(?<![\w.])[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?(?![\w.])"
)

# These are the reviewed get_widget_data selections from the July exemplar
# round. X/Y twins use the same list; only the backend rows differ.
REFERENCE_READS: dict[tuple[str, int], list[str]] = {
    ("cio_investment_committee_pack", 1): [
        "cio_investment_committee_pack_agenda_decisions_required",
        "cio_investment_committee_pack_allocations_capital_allocation",
        "cio_investment_committee_pack_allocations_recommended_changes",
        "cio_investment_committee_pack_allocations_capacity",
        "cio_investment_committee_pack_decisions_follow_ups",
        "cio_investment_committee_pack_research_top_ideas",
        "cio_investment_committee_pack_research_major_catalysts",
    ],
    ("cio_investment_committee_pack", 2): [
        "cio_investment_committee_pack_allocations_recommended_changes",
        "cio_investment_committee_pack_allocations_capacity",
        "cio_investment_committee_pack_research_changed_ratings",
        "cio_investment_committee_pack_research_major_catalysts",
    ],
    ("cio_investment_committee_pack", 3): [
        "cio_investment_committee_pack_agenda_ic_agenda",
        "cio_investment_committee_pack_agenda_decisions_required",
        "cio_investment_committee_pack_decisions_decision_log",
    ],
    ("client_360", 1): [
        "client_360_client_book_mandate_terms",
        "client_360_flows_subscriptions_and_redemptions",
        "client_360_meeting_prep_open_requests",
        "client_360_meeting_prep_approved_talking_points",
        "client_360_portfolio_view_client_returns",
        "client_360_portfolio_view_exposure_summary",
    ],
    ("client_360", 2): [
        "client_360_client_book_relationship_metrics",
        "client_360_flows_subscriptions_and_redemptions",
        "client_360_meeting_prep_open_requests",
    ],
    ("client_360", 3): [
        "client_360_meeting_prep_approved_talking_points",
        "client_360_portfolio_view_client_portfolio_summary",
        "client_360_portfolio_view_client_returns",
    ],
    ("compliance_surveillance_hub", 1): [
        "compliance_surveillance_hub_alerts_surveillance_alerts",
        "compliance_surveillance_hub_audit_investigation_evidence",
        "compliance_surveillance_hub_restricted_list_restricted_and_watch_list",
    ],
    ("compliance_surveillance_hub", 2): [
        "compliance_surveillance_hub_alerts_surveillance_alerts",
        "compliance_surveillance_hub_personal_trading_employee_trades",
        "compliance_surveillance_hub_personal_trading_policy_breaches",
        "compliance_surveillance_hub_personal_trading_pre_clearance_queue",
        "compliance_surveillance_hub_restricted_list_restricted_and_watch_list",
        "compliance_surveillance_hub_audit_access_and_export_logs",
    ],
    ("compliance_surveillance_hub", 3): [
        "compliance_surveillance_hub_audit_investigation_evidence",
        "compliance_surveillance_hub_personal_trading_policy_breaches",
    ],
    ("corporate_access_meeting_notes", 1): [
        "corporate_access_meeting_notes_claims_management_claims_tracker",
        "corporate_access_meeting_notes_compliance_mnpi_attestation_status",
        "corporate_access_meeting_notes_compliance_compliance_follow_ups",
        "corporate_access_meeting_notes_meetings_expert_calls",
        "corporate_access_meeting_notes_notes_follow_ups",
    ],
    ("corporate_access_meeting_notes", 2): [
        "corporate_access_meeting_notes_compliance_mnpi_attestation_status",
        "corporate_access_meeting_notes_compliance_restricted_tags",
        "corporate_access_meeting_notes_compliance_compliance_follow_ups",
        "corporate_access_meeting_notes_meetings_meeting_calendar",
        "corporate_access_meeting_notes_meetings_expert_calls",
        "corporate_access_meeting_notes_notes_meeting_notes_index",
        "corporate_access_meeting_notes_claims_management_claims_tracker",
        "corporate_access_meeting_notes_claims_thesis_change_log",
        "corporate_access_meeting_notes_claims_evidence_and_sign_off_history",
    ],
    ("corporate_access_meeting_notes", 3): [
        "corporate_access_meeting_notes_claims_management_claims_tracker",
        "corporate_access_meeting_notes_claims_thesis_change_log",
        "corporate_access_meeting_notes_claims_evidence_and_sign_off_history",
        "corporate_access_meeting_notes_compliance_mnpi_attestation_status",
        "corporate_access_meeting_notes_meetings_expert_calls",
    ],
    ("crypto_research_dashboard", 1): [
        "crypto_research_dashboard_derivatives_funding_and_basis",
        "crypto_research_dashboard_derivatives_liquidation_heatmap",
        "crypto_research_dashboard_market_price_and_volume",
        "crypto_research_dashboard_on_chain_on_chain_activity",
    ],
    ("crypto_research_dashboard", 2): [
        "crypto_research_dashboard_derivatives_funding_and_basis",
        "crypto_research_dashboard_market_price_and_volume",
        "crypto_research_dashboard_on_chain_on_chain_activity",
    ],
    ("crypto_research_dashboard", 3): [
        "crypto_research_dashboard_derivatives_funding_and_basis",
        "crypto_research_dashboard_market_price_and_volume",
        "crypto_research_dashboard_on_chain_on_chain_activity",
        "crypto_research_dashboard_research_crypto_research_pdfs",
    ],
    ("earnings_estimates_monitor", 1): [
        "earnings_estimates_monitor_calendar_upcoming_earnings",
        "earnings_estimates_monitor_calendar_surprise_history",
        "earnings_estimates_monitor_calendar_catalyst_calendar",
        "earnings_estimates_monitor_estimates_internal_vs_street_bridge",
    ],
    ("earnings_estimates_monitor", 2): [
        "earnings_estimates_monitor_post_earnings_price_reaction",
        "earnings_estimates_monitor_post_earnings_rating_and_target_changes",
        "earnings_estimates_monitor_post_earnings_post_earnings_checklist",
        "earnings_estimates_monitor_transcript_transcript_theme_extraction",
        "earnings_estimates_monitor_transcript_management_tone",
    ],
    ("earnings_estimates_monitor", 3): [
        "earnings_estimates_monitor_estimates_consensus_revisions",
        "earnings_estimates_monitor_post_earnings_thesis_change_log",
        "earnings_estimates_monitor_transcript_management_tone",
    ],
    ("equity_research_workbench", 1): [
        "equity_research_workbench_company_ownership_snapshot",
        "equity_research_workbench_company_consensus_revisions",
        "equity_research_workbench_coverage_coverage_universe",
        "equity_research_workbench_thesis_bull_base_bear",
        "equity_research_workbench_valuation_valuation_assumption_log",
    ],
    ("equity_research_workbench", 2): [
        "equity_research_workbench_coverage_price_target_history",
        "equity_research_workbench_coverage_price_target_upside",
        "equity_research_workbench_valuation_dcf_sensitivity",
    ],
    ("equity_research_workbench", 3): [
        "equity_research_workbench_thesis_catalysts_and_risks",
        "equity_research_workbench_thesis_sell_side_research_pdfs",
        "equity_research_workbench_thesis_draft_research_review",
    ],
    ("execution_desk", 1): [
        "execution_desk_blotter_order_risk_queue",
        "execution_desk_exceptions_rejected_orders",
        "execution_desk_exceptions_restricted_list_checks",
        "execution_desk_fills_vwap_and_arrival_slippage",
        "execution_desk_market_context_spread_and_depth",
        "execution_desk_market_context_order_book_depth",
    ],
    ("execution_desk", 2): [
        "execution_desk_fills_fills_table",
        "execution_desk_fills_vwap_and_arrival_slippage",
        "execution_desk_fills_broker_scorecard",
    ],
    ("execution_desk", 3): [
        "execution_desk_exceptions_rejected_orders",
        "execution_desk_exceptions_restricted_list_checks",
        "execution_desk_exceptions_surveillance_alerts",
    ],
    ("executive_investment_dashboard", 1): [
        "executive_investment_dashboard_firm_overview_aum_by_strategy",
        "executive_investment_dashboard_firm_overview_net_flows",
        "executive_investment_dashboard_issues_major_open_issues",
        "executive_investment_dashboard_performance_returns_by_strategy",
        "executive_investment_dashboard_performance_drawdown_summary",
        "executive_investment_dashboard_risk_stress_loss_summary",
    ],
    ("executive_investment_dashboard", 2): [
        "executive_investment_dashboard_issues_major_open_issues",
        "executive_investment_dashboard_issues_decision_log",
    ],
    ("executive_investment_dashboard", 3): [
        "executive_investment_dashboard_firm_overview_net_flows",
        "executive_investment_dashboard_performance_returns_by_strategy",
        "executive_investment_dashboard_performance_drawdown_summary",
        "executive_investment_dashboard_risk_top_risks",
        "executive_investment_dashboard_risk_stress_loss_summary",
        "executive_investment_dashboard_risk_limit_utilization",
    ],
    ("fund_operations_control_tower", 1): [
        "fund_operations_control_tower_trade_lifecycle_failed_trades",
        "fund_operations_control_tower_recons_custodian_breaks",
        "fund_operations_control_tower_corporate_actions_corporate_action_calendar",
        "fund_operations_control_tower_pricing_stale_prices",
        "fund_operations_control_tower_pricing_nav_exceptions",
        "fund_operations_control_tower_pricing_vendor_price_differences",
    ],
    ("fund_operations_control_tower", 2): [
        "fund_operations_control_tower_pricing_nav_exceptions",
        "fund_operations_control_tower_recons_custodian_breaks",
        "fund_operations_control_tower_recons_break_aging",
        "fund_operations_control_tower_trade_lifecycle_settlement_exceptions",
    ],
    ("fund_operations_control_tower", 3): [
        "fund_operations_control_tower_corporate_actions_corporate_action_calendar",
        "fund_operations_control_tower_corporate_actions_election_deadlines",
        "fund_operations_control_tower_pricing_stale_prices",
        "fund_operations_control_tower_pricing_vendor_price_differences",
        "fund_operations_control_tower_pricing_nav_exceptions",
        "fund_operations_control_tower_recons_custodian_breaks",
        "fund_operations_control_tower_trade_lifecycle_failed_trades",
        "fund_operations_control_tower_trade_lifecycle_settlement_exceptions",
    ],
    ("healthcare_research_dashboard", 1): [
        "healthcare_research_dashboard_clinical_trial_catalyst_calendar",
        "healthcare_research_dashboard_clinical_clinical_probability_funnel",
        "healthcare_research_dashboard_commercial_tam_scenarios",
        "healthcare_research_dashboard_commercial_prescription_trend",
        "healthcare_research_dashboard_coverage_healthcare_coverage_universe",
        "healthcare_research_dashboard_documents_research_document_checklist",
    ],
    ("healthcare_research_dashboard", 2): [
        "healthcare_research_dashboard_clinical_clinical_probability_funnel",
        "healthcare_research_dashboard_commercial_drug_revenue_bridge",
        "healthcare_research_dashboard_commercial_tam_scenarios",
    ],
    ("healthcare_research_dashboard", 3): [
        "healthcare_research_dashboard_clinical_trial_catalyst_calendar",
        "healthcare_research_dashboard_clinical_clinical_probability_funnel",
        "healthcare_research_dashboard_clinical_kol_meeting_notes",
        "healthcare_research_dashboard_commercial_tam_scenarios",
        "healthcare_research_dashboard_commercial_prescription_trend",
        "healthcare_research_dashboard_coverage_healthcare_coverage_universe",
        "healthcare_research_dashboard_documents_research_document_checklist",
    ],
    ("liquidity_tca_workbench", 1): [
        "liquidity_tca_workbench_liquidity_adv_and_order_size",
        "liquidity_tca_workbench_liquidity_volume_profile",
        "liquidity_tca_workbench_tca_implementation_shortfall",
        "liquidity_tca_workbench_tca_venue_flow_sankey",
    ],
    ("liquidity_tca_workbench", 2): [
        "liquidity_tca_workbench_brokers_broker_scorecard",
        "liquidity_tca_workbench_brokers_fill_quality_by_broker",
        "liquidity_tca_workbench_tca_slippage_by_algo",
    ],
    ("liquidity_tca_workbench", 3): [
        "liquidity_tca_workbench_notes_post_trade_review_queue",
        "liquidity_tca_workbench_notes_broker_exception_follow_ups",
        "liquidity_tca_workbench_tca_slippage_by_algo",
    ],
    ("mnpi_research_review", 1): [
        "mnpi_research_review_evidence_evidence_and_sign_off_history",
        "mnpi_research_review_meetings_company_meeting_logs",
        "mnpi_research_review_mnpi_log_wall_crossings",
        "mnpi_research_review_research_draft_research_review",
        "mnpi_research_review_research_price_target_approval",
    ],
    ("mnpi_research_review", 2): [
        "mnpi_research_review_evidence_evidence_and_sign_off_history",
        "mnpi_research_review_evidence_research_approval_evidence",
        "mnpi_research_review_research_draft_research_review",
    ],
    ("mnpi_research_review", 3): [
        "mnpi_research_review_evidence_evidence_and_sign_off_history",
        "mnpi_research_review_evidence_research_approval_evidence",
        "mnpi_research_review_research_reviewer_comments",
    ],
    ("nav_fees_close_dashboard", 1): [
        "nav_fees_close_dashboard_cash_cash_break_aging",
        "nav_fees_close_dashboard_close_close_dependency_register",
        "nav_fees_close_dashboard_fees_fee_accruals",
        "nav_fees_close_dashboard_nav_nav_bridge",
        "nav_fees_close_dashboard_nav_nav_exceptions",
    ],
    ("nav_fees_close_dashboard", 2): [
        "nav_fees_close_dashboard_close_close_exceptions",
        "nav_fees_close_dashboard_close_close_dependency_register",
        "nav_fees_close_dashboard_nav_nav_sign_off_tasks",
    ],
    ("nav_fees_close_dashboard", 3): [
        "nav_fees_close_dashboard_cash_cash_movements",
        "nav_fees_close_dashboard_cash_fx_cash_and_overdrafts",
        "nav_fees_close_dashboard_cash_cash_break_aging",
        "nav_fees_close_dashboard_close_close_exceptions",
        "nav_fees_close_dashboard_fees_fee_accruals",
        "nav_fees_close_dashboard_nav_nav_exceptions",
    ],
    ("portfolio_command_center", 1): [
        "portfolio_command_center_holdings_sector_exposure",
        "portfolio_command_center_overview_limit_utilization",
        "portfolio_command_center_actions_trade_ideas",
    ],
    ("portfolio_command_center", 2): [
        "portfolio_command_center_actions_analyst_conviction",
        "portfolio_command_center_holdings_holdings_table",
        "portfolio_command_center_holdings_slow_portfolio_marks",
    ],
    ("portfolio_command_center", 3): [
        "portfolio_command_center_actions_approval_checklist",
        "portfolio_command_center_overview_top_alerts",
        "portfolio_command_center_overview_limit_utilization",
    ],
    ("quant_research_backtest_lab", 1): [
        "quant_research_backtest_lab_backtest_backtest_performance",
        "quant_research_backtest_lab_risk_model_factor_exposure_table",
        "quant_research_backtest_lab_signals_signal_metrics",
    ],
    ("quant_research_backtest_lab", 2): [
        "quant_research_backtest_lab_signals_signal_metrics",
        "quant_research_backtest_lab_signals_signal_leaderboard",
        "quant_research_backtest_lab_signals_signal_decay",
    ],
    ("quant_research_backtest_lab", 3): [
        "quant_research_backtest_lab_backtest_backtest_performance",
        "quant_research_backtest_lab_backtest_drawdown_path",
        "quant_research_backtest_lab_backtest_trade_simulation",
        "quant_research_backtest_lab_risk_model_factor_exposure_table",
        "quant_research_backtest_lab_signals_signal_metrics",
    ],
    ("rebalance_scenario_lab", 1): [
        "rebalance_scenario_lab_drift_current_vs_target_weights",
        "rebalance_scenario_lab_rebalance_liquidity_impact",
        "rebalance_scenario_lab_rebalance_restricted_list_checks",
        "rebalance_scenario_lab_scenarios_scenario_p_l_waterfall",
    ],
    ("rebalance_scenario_lab", 2): [
        "rebalance_scenario_lab_drift_constraint_utilization",
        "rebalance_scenario_lab_rebalance_proposed_trades",
        "rebalance_scenario_lab_rebalance_liquidity_impact",
        "rebalance_scenario_lab_rebalance_restricted_list_checks",
    ],
    ("rebalance_scenario_lab", 3): [
        "rebalance_scenario_lab_approval_approval_checklist",
        "rebalance_scenario_lab_approval_implementation_readiness",
        "rebalance_scenario_lab_drift_drift_by_sleeve",
    ],
    ("reporting_factsheet_studio", 1): [
        "reporting_factsheet_studio_commentary_approved_commentary_library",
        "reporting_factsheet_studio_commentary_disclosure_checklist",
        "reporting_factsheet_studio_ddqs_ddq_and_rfp_tracker",
        "reporting_factsheet_studio_performance_monthly_returns",
        "reporting_factsheet_studio_performance_attribution_summary",
        "reporting_factsheet_studio_performance_risk_stats",
    ],
    ("reporting_factsheet_studio", 2): [
        "reporting_factsheet_studio_commentary_approved_commentary_library",
        "reporting_factsheet_studio_commentary_pm_quote_bank",
        "reporting_factsheet_studio_commentary_disclosure_checklist",
        "reporting_factsheet_studio_ddqs_disclosure_exceptions",
        "reporting_factsheet_studio_factsheets_factsheet_preview",
        "reporting_factsheet_studio_factsheets_factsheet_distribution_status",
    ],
    ("reporting_factsheet_studio", 3): [
        "reporting_factsheet_studio_commentary_approved_commentary_library",
        "reporting_factsheet_studio_performance_monthly_returns",
        "reporting_factsheet_studio_performance_attribution_summary",
        "reporting_factsheet_studio_performance_risk_stats",
    ],
    ("risk_exposure_monitor", 1): [
        "risk_exposure_monitor_dashboard_var_trend",
        "risk_exposure_monitor_dashboard_stress_loss_surface",
        "risk_exposure_monitor_drilldown_marginal_var",
        "risk_exposure_monitor_drilldown_position_risk_contribution",
        "risk_exposure_monitor_exposures_issuer_concentration",
        "risk_exposure_monitor_limits_breaches_and_warnings",
        "risk_exposure_monitor_limits_limit_utilization",
    ],
    ("risk_exposure_monitor", 2): [
        "risk_exposure_monitor_drilldown_position_risk_contribution",
        "risk_exposure_monitor_drilldown_marginal_var",
        "risk_exposure_monitor_exposures_exposure_table",
        "risk_exposure_monitor_exposures_issuer_concentration",
    ],
    ("risk_exposure_monitor", 3): [
        "risk_exposure_monitor_limits_limit_utilization",
        "risk_exposure_monitor_limits_breaches_and_warnings",
        "risk_exposure_monitor_limits_limit_breach_trend",
    ],
    ("strategy_health_monitor", 1): [
        "strategy_health_monitor_capacity_capacity_utilization",
        "strategy_health_monitor_performance_sleeve_performance",
        "strategy_health_monitor_themes_crowded_names",
    ],
    ("strategy_health_monitor", 2): [
        "strategy_health_monitor_capacity_capacity_utilization",
        "strategy_health_monitor_capacity_liquidity_capacity_curve",
        "strategy_health_monitor_themes_factor_tilts",
    ],
    ("strategy_health_monitor", 3): [
        "strategy_health_monitor_themes_crowded_names",
        "strategy_health_monitor_watchlist_names_near_action_levels",
        "strategy_health_monitor_watchlist_catalyst_calendar",
    ],
    ("stress_liquidity_lab", 1): [
        "stress_liquidity_lab_liquidity_days_to_liquidate",
        "stress_liquidity_lab_liquidity_crowded_names",
        "stress_liquidity_lab_liquidity_redemption_stress",
        "stress_liquidity_lab_stress_tests_scenario_loss_waterfall",
    ],
    ("stress_liquidity_lab", 2): [
        "stress_liquidity_lab_liquidity_days_to_liquidate",
        "stress_liquidity_lab_scenarios_scenario_builder_assumptions",
    ],
    ("stress_liquidity_lab", 3): [
        "stress_liquidity_lab_sign_off_sign_off_tracker",
        "stress_liquidity_lab_sign_off_residual_risk_actions",
    ],
    ("vendor_dataset_monitor", 1): [
        "vendor_dataset_monitor_incidents_incident_log",
        "vendor_dataset_monitor_incidents_blast_radius_summary",
        "vendor_dataset_monitor_quality_validation_errors",
        "vendor_dataset_monitor_quality_affected_apps",
        "vendor_dataset_monitor_slas_latency_by_feed",
        "vendor_dataset_monitor_slas_freshness_exceptions",
    ],
    ("vendor_dataset_monitor", 2): [
        "vendor_dataset_monitor_quality_validation_errors",
        "vendor_dataset_monitor_quality_row_count_drift",
        "vendor_dataset_monitor_quality_affected_apps",
    ],
    ("vendor_dataset_monitor", 3): [
        "vendor_dataset_monitor_incidents_incident_log",
        "vendor_dataset_monitor_incidents_blast_radius_summary",
        "vendor_dataset_monitor_overview_workflow_overview",
        "vendor_dataset_monitor_quality_validation_errors",
        "vendor_dataset_monitor_quality_row_count_drift",
        "vendor_dataset_monitor_quality_affected_apps",
    ],
    ("workspace_data_control_center", 1): [
        "workspace_data_control_center_ai_access_copilot_visibility_flags",
        "workspace_data_control_center_data_health_feed_status",
        "workspace_data_control_center_data_health_failed_jobs_trend",
        "workspace_data_control_center_entitlements_app_and_widget_permissions",
        "workspace_data_control_center_entitlements_role_coverage",
        "workspace_data_control_center_entitlements_sensitive_dataset_flags",
        "workspace_data_control_center_usage_export_activity",
    ],
    ("workspace_data_control_center", 2): [
        "workspace_data_control_center_ai_access_copilot_visibility_flags",
        "workspace_data_control_center_entitlements_app_and_widget_permissions",
        "workspace_data_control_center_entitlements_sensitive_dataset_flags",
    ],
    ("workspace_data_control_center", 3): [
        "workspace_data_control_center_ai_access_prompt_audit",
        "workspace_data_control_center_usage_app_usage",
        "workspace_data_control_center_usage_export_activity",
        "workspace_data_control_center_usage_export_review_queue",
    ],
}


def slugify_id(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def widget_layout_params(app: JsonDict, widget_id: str) -> JsonDict:
    tabs = app.get("tabs", {})
    if not isinstance(tabs, dict):
        return {}
    for tab in tabs.values():
        if not isinstance(tab, dict):
            continue
        for layout in tab.get("layout", []):
            if not isinstance(layout, dict) or str(layout.get("i")) != widget_id:
                continue
            state = layout.get("state") or {}
            if isinstance(state, dict) and isinstance(state.get("params"), dict):
                return dict(state["params"])
    return {}


def load_reference_answers() -> dict[str, str]:
    payload = json.loads(REFERENCE_ANSWERS_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict), "reference answer corpus must be a JSON object"
    source = payload.get("source")
    assert isinstance(source, dict), "reference answer corpus is missing source metadata"
    assert source.get("authored_by") == "gpt-5.6sol via codex"
    answers = payload.get("answers")
    assert isinstance(answers, dict), "reference answer corpus is missing answers"
    assert all(isinstance(key, str) for key in answers)
    assert all(isinstance(value, str) and value.strip() for value in answers.values())
    return {str(key): str(value) for key, value in answers.items()}


def _reference(
    app: JsonDict,
    reads: list[str],
    answer: str,
) -> list[JsonDict]:
    calls: list[JsonDict] = [{"tool": "get_workspace_snapshot", "args": {}}]
    for widget_id in reads:
        calls.append(
            {
                "tool": "get_widget_data",
                "args": {
                    "origin": ORIGIN,
                    "widget_id": widget_id,
                    "data_args": widget_layout_params(app, widget_id),
                },
            }
        )
    # The reference trace holds only the workspace interactions; the reply
    # lives in eval.reference_answer and the oracle replay synthesizes the
    # final_answer submission from it.
    return calls


def build_tasks(
    canonical: FixtureBackend,
    world_y: FixtureBackend,
    answers: dict[str, str],
) -> list[tuple[str, JsonDict]]:
    expected_read_keys = {
        (slugify_id(str(app.get("template_id") or app["name"])), index)
        for app in canonical.apps
        for index, _prompt in enumerate(app.get("prompts") or [], start=1)
    }
    missing_reads = sorted(expected_read_keys - REFERENCE_READS.keys())
    assert not missing_reads, f"missing reviewed reference reads: {missing_reads}"
    unexpected_reads = sorted(REFERENCE_READS.keys() - expected_read_keys)
    assert not unexpected_reads, f"unexpected reviewed reference reads: {unexpected_reads}"
    expected_answer_ids = {
        f"{family}_p{index}_{world}"
        for family, index in expected_read_keys
        for world in ("x", "y")
    }
    missing_answers = sorted(expected_answer_ids - answers.keys())
    assert not missing_answers, f"missing authored answers: {missing_answers}"
    unexpected_answers = sorted(answers.keys() - expected_answer_ids)
    assert not unexpected_answers, f"unexpected authored answers: {unexpected_answers}"

    tasks: list[tuple[str, JsonDict]] = []
    for app in canonical.apps:
        family = slugify_id(str(app.get("template_id") or app["name"]))
        for index, prompt in enumerate(app.get("prompts") or [], start=1):
            base_id = f"{family}_p{index}"
            reads = REFERENCE_READS[(family, index)]
            pair: list[JsonDict] = []
            for suffix, backend in (("_x", canonical), ("_y", world_y)):
                task_id = base_id + suffix
                answer = answers[task_id]
                reference = _reference(app, reads, answer)
                payload: JsonDict = {
                    "id": task_id,
                    "prompt": prompt,
                    "setup": {
                        "workspace_baseline": WORKSPACE_BASELINE,
                        "workspace_backends": [backend.slug],
                        "workspace_skills": sorted(WORKSPACE_SKILLS),
                        "default_selected_dashboard": app["name"],
                        "allowed_tools": list(ALLOWED_TOOLS),
                    },
                    "eval": {
                        "judge_evaluation": True,
                        "reference_trace": reference,
                        "reference_answer": answer,
                        "limits": {"max_turns": len(reference) + 3},
                    },
                }
                pair.append(payload)
                tasks.append((family, payload))
            assert pair[0]["prompt"] == pair[1]["prompt"]
            x_evaluation = pair[0]["eval"]
            y_evaluation = pair[1]["eval"]
            assert isinstance(x_evaluation, dict) and isinstance(y_evaluation, dict)
            x_reference = x_evaluation["reference_trace"]
            y_reference = y_evaluation["reference_trace"]
            assert isinstance(x_reference, list) and isinstance(y_reference, list)
            assert x_reference == y_reference, (
                f"{base_id}: X/Y reference reads differ"
            )
            assert x_evaluation["reference_answer"] != y_evaluation["reference_answer"], (
                f"{base_id}: X/Y authored answers must differ"
            )
    return tasks


def _manifest_payload(content_sha256: str | None = None) -> JsonDict:
    payload: JsonDict = {
        "suite_id": SUITE_ID,
        "visibility": "public",
        "task_defaults": dict(TASK_DEFAULTS),
        "description": (
            "69 byte-verbatim enterprise-app product prompts, each run twice "
            "as an _x/_y pair on the stark-enterprise-x and stark-enterprise-y "
            "data worlds, graded by the suite judge against a reference "
            "trajectory with a deterministic final-answer gate."
        ),
    }
    if content_sha256 is not None:
        payload["content_sha256"] = content_sha256
    return payload


def _normalized_number(token: str) -> str:
    return token.replace(",", "").removesuffix("%")


def _number_tokens(text: str) -> list[tuple[str, str]]:
    return [
        (match.group(0), _normalized_number(match.group(0)))
        for match in NUMBER_TOKEN_RE.finditer(text)
    ]


def _served_rows(reference: list[Any], backend: FixtureBackend) -> list[Any]:
    rows: list[Any] = []
    for call in reference:
        assert isinstance(call, dict)
        if call.get("tool") != "get_widget_data":
            continue
        args = call.get("args")
        assert isinstance(args, dict)
        widget_id = args.get("widget_id")
        data_args = args.get("data_args")
        assert isinstance(widget_id, str)
        assert isinstance(data_args, dict)
        rows.append(backend.fetch_widget_data(widget_id, data_args))
    return rows


def certify_groundedness(
    tasks: list[tuple[str, JsonDict]],
    backends: tuple[FixtureBackend, FixtureBackend],
) -> None:
    backend_by_slug = {backend.slug: backend for backend in backends}
    offenders: list[tuple[str, str]] = []
    for _family, payload in tasks:
        task_id = str(payload["id"])
        setup = payload["setup"]
        evaluation = payload["eval"]
        assert isinstance(setup, dict) and isinstance(evaluation, dict)
        workspace_backends = setup["workspace_backends"]
        reference = evaluation["reference_trace"]
        answer = evaluation["reference_answer"]
        assert isinstance(workspace_backends, list) and len(workspace_backends) == 1
        assert isinstance(reference, list) and isinstance(answer, str)
        backend = backend_by_slug[str(workspace_backends[0])]
        served_text = json.dumps(
            _served_rows(reference, backend),
            ensure_ascii=False,
            separators=(",", ":"),
        )
        served_numbers = {normalized for _raw, normalized in _number_tokens(served_text)}
        offenders.extend(
            (task_id, raw)
            for raw, normalized in _number_tokens(answer)
            if normalized not in served_numbers
        )
    assert not offenders, "authored answer groundedness failures:\n" + "\n".join(
        f"- {task_id}: {figure}" for task_id, figure in offenders
    )


def certify(
    tasks: list[tuple[str, JsonDict]],
    canonical: FixtureBackend,
    world_y: FixtureBackend,
) -> None:
    manifest = TaskSuiteManifest.from_dict(_manifest_payload())
    product_prompts = {
        prompt for app in canonical.apps for prompt in (app.get("prompts") or [])
    }
    ids = [str(payload["id"]) for _family, payload in tasks]
    duplicate_ids = [task_id for task_id, count in Counter(ids).items() if count > 1]
    assert not duplicate_ids, f"duplicate task ids: {duplicate_ids}"
    assert len(tasks) == 138, f"expected 138 tasks, got {len(tasks)}"
    certify_groundedness(tasks, (canonical, world_y))

    expected_top_level = ["id", "prompt", "setup", "eval"]
    expected_setup = [
        "workspace_baseline",
        "workspace_backends",
        "workspace_skills",
        "default_selected_dashboard",
        "allowed_tools",
    ]
    expected_eval = [
        "judge_evaluation",
        "reference_trace",
        "reference_answer",
        "limits",
    ]
    for family, payload in tasks:
        task_id = str(payload["id"])
        assert list(payload) == expected_top_level, f"{task_id}: wrong top-level schema"
        setup = payload["setup"]
        evaluation = payload["eval"]
        assert isinstance(setup, dict) and list(setup) == expected_setup
        assert isinstance(evaluation, dict) and list(evaluation) == expected_eval
        assert task_id.endswith(("_x", "_y")), f"{task_id}: missing world suffix"
        assert setup["workspace_baseline"] == WORKSPACE_BASELINE
        assert setup["allowed_tools"] == list(ALLOWED_TOOLS)
        assert payload["prompt"] in product_prompts, (
            f"{task_id}: prompt is not byte-verbatim from the product catalog"
        )
        reference = evaluation["reference_trace"]
        reference_answer = evaluation["reference_answer"]
        limits = evaluation["limits"]
        assert isinstance(reference, list)
        assert isinstance(reference_answer, str)
        assert isinstance(limits, dict)
        assert limits["max_turns"] == len(reference) + 3
        assert all(
            isinstance(call, dict) and call.get("tool") != "final_answer"
            for call in reference
        ), f"{task_id}: reference_trace must hold only workspace interactions"

        task = replace(
            Task.from_dict({**TASK_DEFAULTS, "family": family, **payload}),
            suite=manifest,
        )
        episode = WorkspaceEpisode(task=task)
        for call_payload in [
            *reference,
            {"tool": "final_answer", "args": {"text": reference_answer}},
        ]:
            assert isinstance(call_payload, dict)
            result = episode.step(ToolCall.from_dict(call_payload))
            assert result.get("ok"), (
                f"{task_id}: reference call {call_payload.get('tool')} failed: "
                f"{(result.get('error') or {}).get('message')}"
            )
        grade = episode.grade()
        assert grade.passed, f"{task_id}: reference does not pass: " + "; ".join(
            f"{issue.code}: {issue.message}" for issue in grade.issues
        )
        noop_grade = WorkspaceEpisode(task=task).grade()
        assert not noop_grade.passed, f"{task_id}: no-op passes"
        assert any(issue.code == "missing_final_answer" for issue in noop_grade.issues), (
            f"{task_id}: no-op did not fail missing_final_answer"
        )


def main() -> int:
    canonical = build_stark_enterprise_backend()
    world_y = build_stark_enterprise_y_backend()
    answers = load_reference_answers()
    tasks = build_tasks(canonical, world_y, answers)
    certify(tasks, canonical, world_y)
    if OUT_DIR.exists():
        for stale in OUT_DIR.rglob("*.json"):
            if stale.name not in {"task_suite.json", REFERENCE_ANSWERS_PATH.name}:
                stale.unlink()
    for family, payload in tasks:
        family_dir = OUT_DIR / family
        family_dir.mkdir(parents=True, exist_ok=True)
        (family_dir / f"{payload['id']}.json").write_text(
            json.dumps(payload, indent=1, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    (OUT_DIR / "__init__.py").write_text("", encoding="utf-8")
    (OUT_DIR / "task_suite.json").write_text(
        json.dumps(
            _manifest_payload(task_payload_digest([payload for _, payload in tasks])),
            indent=1,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print("Certified 138/138 authored answers for numeric groundedness")
    print(f"Wrote {len(tasks)} tasks to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
