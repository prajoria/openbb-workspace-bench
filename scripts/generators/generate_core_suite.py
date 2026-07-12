"""Generate the bundled WorkspaceBench core suite (tool-centric ladders).

TMax-style compositional generation, restructured so that **every family is
anchored on one MCP tool and carries a complete r0-r4 ladder**:

    15 tool families x 5 levels x 4 tasks = 300

Levels are structural (composition, pathology, discovery pressure, budget),
never adjectives. Difficulty labels are balanced across the suite rather than
used as level names: r0 is easy, r2 is medium, r4 is hard, while each r1 cell
splits 2 easy / 2 medium and each r3 cell splits 2 medium / 2 hard. This yields
90 easy / 120 medium / 90 hard for the 300-task lattice. Higher levels
*compose* the anchor tool with others, so a r4 run requires several MCP tools in
a single episode while the anchor stays central.

Discipline rule: where a task enforces schema-before-create, levels r0-r2
instruct the discipline explicitly in the prompt; levels r3-r4 expect it
unprompted — looking before touching without being told is part of what makes
the upper levels hard.

Each prompt site uses a deterministic phrasing pool with at least three
semantically identical full-prompt variants. The selected surface wording is
`md5(task_id) % len(pool)`, so the same task id keeps the same prompt
forever without using randomness.

Certification: `workspace-bench validate --suite core --min-tasks 300`
must report oracle pass and no-op fail for every task.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from _assembly import (
    ArtifactDiscriminator,
    CheckTypePolicy,
    NoveltyPolicy,
    PhrasingSelector,
    SplitAssigner,
    TaskAssembler,
    build_matrix,
    difficulty_for,
    snap,
    uniform_four_way_pattern,
)
from workspace_bench.core.models import TASK_SCHEMA_VERSION
from workspace_bench.core.suite_checks import task_payload_digest
from workspace_bench.workspace.fixtures import get_fixture_backend

REPO = Path(__file__).resolve().parents[2]
STARK = json.loads((REPO / "src/workspace_bench/workspace/data/stark_enterprise.json").read_text())
BUNDLED_OUT_DIR = REPO / "src/workspace_bench/task_suites/core"
OUT_DIRS = (BUNDLED_OUT_DIR,)

STK = "Bench Stark Enterprise"
EQ, MACRO, PF = "Bench Equities", "Bench Macro", "Bench Portfolio"

GRID = {"within_grid": True, "no_overlaps": True, "grid_width": 40}
TRACE_FULL = {
    "max_invalid_tool_calls": 0,
    "must_call_schema_before_create": True,
    "forbid_invented_widget_ids": True,
    "max_repeated_snapshots": 1,
}
TRACE_BASIC = {"max_invalid_tool_calls": 0, "max_repeated_snapshots": 1}

RUNG_DIFFICULTY = {"r0": "easy", "r1": "easy", "r2": "medium", "r3": "hard", "r4": "hard"}
RUNG_SLACK = {"r0": 3, "r1": 3, "r2": 3, "r3": 3, "r4": 2}

SCENARIOS: list[dict] = []
CELL_COUNTS: dict[tuple[str, str], int] = defaultdict(int)
PROMPT_POOL_SIZES: dict[str, int] = {}


# Curated public identities for tasks whose authored ids contain generator
# coordinates, repeated stems, or overly long enterprise widget paths. Keep
# this explicit: already-good ids must remain byte-identical, while future
# audits can point directly at the legacy construction that needs cleanup.
PUBLIC_ID_RENAMES = {
    "add_widget_earnings_estimates_monitor_post_earnings_post_earnings_checklist_3":
        "register_backend_and_add_post_earnings_checklist",
    "add_widget_holdings_table_2": "register_backend_and_add_holdings_table",
    "add_widget_macro_timeseries_1": "register_backend_and_add_macro_timeseries",
    "add_widget_price_performance_0": "register_backend_and_add_price_performance",
    "cross_equity_research_workbench_company_ownership_snapshot_risk_metrics_2":
        "register_two_backends_ownership_snapshot_and_risk_metrics",
    "cross_fundamental_metrics_holdings_table_3":
        "register_two_backends_fundamental_metrics_and_holdings_table",
    "cross_latest_news_yield_curve_0":
        "register_two_backends_latest_news_and_yield_curve",
    "cross_sector_exposure_macro_timeseries_1":
        "register_two_backends_sector_exposure_and_macro_timeseries",
    "refresh_earnings_estimates_monitor_post_earnings_post_earnings_checklist_3":
        "refresh_backend_before_building_post_earnings_checklist",
    "refresh_holdings_table_2": "refresh_backend_before_building_holdings_table",
    "refresh_macro_timeseries_1": "refresh_backend_before_building_macro_timeseries",
    "refresh_price_performance_0": "refresh_backend_before_building_price_performance",
    "alerts_47": "remove_top_alerts",
    "dup_news_12": "remove_duplicate_latest_news",
    "dup_performance_18": "remove_duplicate_price_performance",
    "dup_status_48": "remove_duplicate_vendor_sla_status",
    "dup_timeseries_17": "remove_duplicate_macro_timeseries",
    "news_12": "remove_latest_news",
    "note_exposure_16": "remove_duplicate_sector_exposure_and_document",
    "note_history_17": "remove_duplicate_estimate_history_and_document",
    "note_metrics_20": "remove_duplicate_fundamental_metrics_and_document",
    "note_orders_36": "remove_duplicate_live_orders_and_document",
    "performance_18": "remove_price_performance",
    "then_fix_news_aapl_12": "deduplicate_and_fix_latest_news",
    "then_fix_performance_nvda_18": "deduplicate_and_fix_price_performance",
    "then_fix_status_escalated_48": "deduplicate_and_fix_vendor_sla_status",
    "then_fix_timeseries_dgs2_17": "deduplicate_and_fix_macro_timeseries",
    "timeseries_17": "remove_macro_timeseries",
    "deduplicate_latest_news_0": "find_duplicate_latest_news",
    "deduplicate_macro_timeseries_1": "find_duplicate_macro_timeseries",
    "deduplicate_rebalance_scenario_lab_drift_drift_by_sleeve_3":
        "find_duplicate_drift_by_sleeve",
    "deduplicate_risk_metrics_2": "find_duplicate_risk_metrics",
    "fix_estimate_history_1": "find_and_fix_misconfigured_estimate_history",
    "fix_macro_timeseries_2": "find_and_fix_misconfigured_macro_timeseries",
    "fix_price_performance_0": "find_and_fix_misconfigured_price_performance",
    "fix_quant_research_backtest_lab_risk_model_factor_exposure_table_3":
        "find_and_fix_misconfigured_factor_exposure_table",
    "overlap_holdings_table_2": "inspect_and_repair_overlap_holdings_table",
    "overlap_macro_timeseries_1": "inspect_and_repair_overlap_macro_timeseries",
    "overlap_price_performance_0": "inspect_and_repair_overlap_price_performance",
    "overlap_reporting_factsheet_studio_commentary_disclosure_checklist_3":
        "inspect_and_repair_overlap_disclosure_checklist",
    "read_holdings_table_2": "inspect_holdings_table",
    "read_macro_timeseries_1": "inspect_macro_timeseries",
    "read_portfolio_command_center_overview_workflow_overview_3":
        "inspect_workflow_overview",
    "read_price_performance_0": "inspect_price_performance",
    "repair_brief_macro_timeseries_1": "ambient_repair_and_brief_macro_timeseries",
    "repair_brief_price_performance_0": "ambient_repair_and_brief_price_performance",
    "repair_brief_reporting_factsheet_studio_factsheets_risk_stats_3":
        "ambient_repair_and_brief_risk_stats",
    "repair_brief_sector_exposure_2": "ambient_repair_and_brief_sector_exposure",
    "grid_grid_eq": "equity_three_widget_grid",
    "grid_grid_eq_mixed": "mixed_equity_three_widget_grid",
    "grid_grid_macro": "macro_three_widget_grid",
    "grid_grid_portfolio": "portfolio_three_widget_grid",
    "overlap_overlap_estimates_fund_msft": "repair_msft_estimates_overlap",
    "overlap_overlap_macro": "repair_macro_overlap",
    "overlap_overlap_portfolio": "repair_portfolio_overlap",
    "overlap_overlap_price_news_aapl": "repair_aapl_price_news_overlap",
    "companion_sector_corporate_access_meeting_notes_claims_evidence_and_sign_off_history_3":
        "options_constrained_pair_for_evidence_and_sign_off_history",
    "companion_sector_sector_exposure_2":
        "options_constrained_pair_for_sector_exposure",
    "companion_series_macro_timeseries_1":
        "options_constrained_pair_for_macro_timeseries",
    "companion_symbol_price_performance_0":
        "options_constrained_pair_for_price_performance",
    "place_sector_compliance_surveillance_hub_audit_access_and_export_logs_11":
        "options_constrained_placement_for_access_and_export_logs",
    "place_sector_sector_exposure_10":
        "options_constrained_placement_for_sector_exposure",
    "place_series_macro_timeseries_9":
        "options_constrained_placement_for_macro_timeseries",
    "place_symbol_price_performance_8":
        "options_constrained_placement_for_price_performance",
    "schema_sector_client_360_portfolio_view_exposure_summary_7":
        "discover_schema_then_options_for_exposure_summary",
    "schema_sector_sector_exposure_6":
        "discover_schema_then_options_for_sector_exposure",
    "schema_series_macro_timeseries_5":
        "discover_schema_then_options_for_macro_timeseries",
    "schema_symbol_price_performance_4":
        "discover_schema_then_options_for_price_performance",
    "sector_client_360_meeting_prep_relationship_metrics_3":
        "use_sector_options_for_relationship_metrics",
    "sector_sector_exposure_2": "use_sector_options_for_sector_exposure",
    "series_macro_timeseries_1": "use_series_options_for_macro_timeseries",
    "symbol_price_performance_0": "use_symbol_options_for_price_performance",
    "fetch_workspace_session_context_1": "session_context_grounding_note",
    "fetch_workspace_session_context_3": "session_context_grounding_review",
    "fetch_workspace_tool_usage_0": "tool_usage_schema_note",
    "fetch_workspace_tool_usage_2": "tool_usage_schema_summary",
    "session_tab_ops_liquidity_tca_workbench_tca_slippage_by_algo":
        "session_prompt_ops_slippage",
    "tool_usage_healthcare_research_dashboard_documents_healthcare_thesis_note_3":
        "follow_tool_usage_prompt_for_healthcare_thesis_note",
    "tool_usage_macro_timeseries_1": "follow_tool_usage_prompt_for_macro_timeseries",
    "tool_usage_price_performance_0":
        "follow_tool_usage_prompt_for_price_performance",
    "tool_usage_risk_metrics_2": "follow_tool_usage_prompt_for_risk_metrics",
    "period_mtd_56": "set_portfolio_snapshot_period_to_mtd",
    "pick_series_dgs2_17": "update_only_the_dgs2_macro_timeseries",
    "pick_symbol_msft_18": "update_only_the_msft_price_performance",
    "pick_symbol_nvda_12": "update_only_the_nvda_latest_news",
    "pick_vendor_factset_48": "update_only_the_factset_vendor_sla_status",
    "series_dgs10_17": "set_macro_timeseries_series_to_dgs10",
    "series_fedfunds_17": "update_macro_timeseries_cpiaucsl_to_fedfunds",
    "status_escalated_44": "update_rejected_orders_open_to_escalated",
    "symbol_aapl_18": "set_price_performance_symbol_to_aapl",
    "symbol_msft_12": "set_latest_news_symbol_to_msft",
    "symbol_nvda_17": "update_estimate_history_aapl_to_nvda",
    "symbol_nvda_20": "update_fundamental_metrics_msft_to_nvda",
}


def public_id(task_id: str) -> str:
    """Return the durable public identity for an authored task id."""

    return PUBLIC_ID_RENAMES.get(task_id, task_id)


def clean_title(title: str) -> str:
    """Remove adjacent repeated words introduced by joined title stems."""

    words = title.split()
    cleaned: list[str] = []
    for word in words:
        normalized = re.sub(r"[^a-z0-9]", "", word.lower())
        previous = re.sub(r"[^a-z0-9]", "", cleaned[-1].lower()) if cleaned else ""
        if normalized and normalized == previous:
            continue
        cleaned.append(word)
    return " ".join(cleaned)


def clean_prompt(prompt: str) -> str:
    """Replace known machine-glued enterprise ids with business names."""

    replacements = {
        "earnings_estimates_monitor_post_earnings_post_earnings_checklist":
            "Post-Earnings Checklist",
        "rebalance_scenario_lab_drift_drift_by_sleeve": "Drift by Sleeve",
        "rebalance_scenario_lab_overview_workflow_overview": "Workflow Overview",
        "portfolio_command_center_attribution_attribution_summary": "Attribution Summary",
        "execution_desk_fills_fills_table": "Fills Table",
        "quant_research_backtest_lab_backtest_backtest_performance":
            "Backtest Performance",
    }
    for scar, replacement in replacements.items():
        prompt = prompt.replace(scar, replacement)
    return prompt


phrased = PhrasingSelector(PROMPT_POOL_SIZES, normalize_id=public_id)


def stark_value(widget_id: str) -> float:
    return round((sum(ord(c) for c in widget_id) % 9000) / 100, 2)


def _fact_value(value: object) -> str:
    return str(value)


def _numeric(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def stark_fact(widget_id: str) -> tuple[str, str]:
    payload = STARK["widgets"][widget_id]["data"]
    preferred = (
        "var_usd", "drawdown_usd", "loss_usd", "weight", "exposure",
        "latency_ms", "breach_count", "alert_count", "exception_count",
        "order_count", "count", "return", "price_usd", "value_usd",
        "aum_usd", "score", "value",
    )
    if isinstance(payload, list):
        for row in payload:
            if not isinstance(row, dict):
                continue
            for field in preferred:
                if field in row and _numeric(row[field]):
                    return field, _fact_value(row[field])
            for field, value in row.items():
                if field != "widget_id" and _numeric(value):
                    return field, _fact_value(value)
    if isinstance(payload, dict):
        series = payload.get("series")
        if isinstance(series, list):
            for point in series:
                if isinstance(point, dict) and _numeric(point.get("value")):
                    return "value", _fact_value(point["value"])
        for field, value in payload.items():
            if field != "widget_id" and _numeric(value):
                return field, _fact_value(value)
    if isinstance(payload, str):
        match = re.search(r"synthetic ([a-z0-9_]+) reading is (-?\d+(?:\.\d+)?)", payload)
        if match:
            return match.group(1), match.group(2)
    raise AssertionError(f"no baked Stark fact available for {widget_id}")


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-")


def fixture_for(origin: str) -> str:
    return {EQ: "equities", MACRO: "macro", PF: "portfolio", STK: "stark-enterprise"}[origin]


def core_workflow(origin: str) -> tuple[str, str]:
    return {EQ: ("equity-tearsheet", "equity-research"),
            MACRO: ("macro-rates-review", "macro"),
            PF: ("portfolio-risk-review", "portfolio-management")}[origin]


STARK_META = {
    "risk_exposure_monitor": ("risk-review", "risk"),
    "execution_desk": ("execution-exception-review", "execution"),
    "client_360": ("client-meeting-prep", "client-ir"),
    "earnings_estimates_monitor": ("earnings-prep", "equity-research"),
    "vendor_dataset_monitor": ("vendor-sla-monitoring", "data-platform"),
    "compliance_surveillance_hub": ("compliance-surveillance", "compliance"),
    "portfolio_command_center": ("portfolio-morning-review", "portfolio-management"),
    "strategy_health_monitor": ("portfolio-morning-review", "portfolio-management"),
    "fund_operations_control_tower": ("vendor-sla-monitoring", "data-platform"),
    "quant_research_backtest_lab": ("risk-review", "risk"),
    "healthcare_research_dashboard": ("healthcare-catalyst-review", "healthcare-research"),
    "equity_research_workbench": ("equity-tearsheet", "equity-research"),
    "stress_liquidity_lab": ("risk-review", "risk"),
    "executive_investment_dashboard": ("portfolio-morning-review", "portfolio-management"),
    "nav_fees_close_dashboard": ("vendor-sla-monitoring", "data-platform"),
    "liquidity_tca_workbench": ("execution-exception-review", "execution"),
    "mnpi_research_review": ("compliance-surveillance", "compliance"),
    "corporate_access_meeting_notes": ("compliance-surveillance", "compliance"),
    "reporting_factsheet_studio": ("client-meeting-prep", "client-ir"),
    "cio_investment_committee_pack": ("portfolio-morning-review", "portfolio-management"),
    "workspace_data_control_center": ("vendor-sla-monitoring", "data-platform"),
    "crypto_research_dashboard": ("equity-tearsheet", "equity-research"),
}


def stark_family(key: str) -> tuple[str, str]:
    key = key.replace("-", "_")
    for prefix, pair in STARK_META.items():
        if key.startswith(prefix):
            return pair
    return ("portfolio-morning-review", "portfolio-management")


def wf(origin: str, widget_id: str = "") -> tuple[str, str]:
    return stark_family(widget_id) if origin == STK else core_workflow(origin)


_CATEGORY_CODE_TO_CATEGORY = {
    "L0": "read", "L1": "single-widget", "L2": "dashboard",
    "L3": "platform", "L4": "repair", "L5": "platform",
}


def _attach_backend_runtime_checks(task: dict) -> None:
    """Embed the deterministic catalogs registered by core backend tasks."""

    fixture_names = []
    for call in task.get("oracle_tool_calls", []):
        args = call.get("args", {})
        if call.get("tool") == "manage_backends" and args.get("operation") == "add":
            name = args.get("name")
            if isinstance(name, str) and name not in fixture_names:
                fixture_names.append(name)
    datasets = []
    for fixture_name in fixture_names:
        backend = get_fixture_backend(fixture_name)
        for widget_id, definition in sorted(backend.widgets_json().items()):
            payload = backend.fetch_widget_data(widget_id, {})
            fields = sorted(_response_fields(payload))
            datasets.append(
                {
                    "name": f"{backend.slug}__{widget_id}",
                    "widget_id": widget_id,
                    "fields": fields,
                    "path": str(definition.get("endpoint", "/")),
                    "payload": payload,
                }
            )
    if datasets:
        task.setdefault("success", {})["runtime_checks"] = {
            "datasets": datasets,
            "pinned_paths": False,
        }


def _response_fields(payload: object) -> set[str]:
    if isinstance(payload, dict):
        fields = set(payload)
        for value in payload.values():
            fields.update(_response_fields(value))
        return fields
    if isinstance(payload, list):
        list_fields: set[str] = set()
        for value in payload:
            list_fields.update(_response_fields(value))
        return list_fields
    return set()


def _ensure_widget_discovery(task: dict) -> None:
    """Insert a same-origin list before schema/create use when listing is available."""

    if "list_available_widgets" not in task.get("allowed_tools", []):
        return
    listed: set[str] = set()
    calls: list[dict] = []
    for call in task.get("oracle_tool_calls", []):
        name = call.get("tool")
        args = call.get("args", {})
        origin = str(args.get("origin") or args.get("backend_name") or "")
        if name in {"get_widget_schema", "create_widget"} and origin not in listed:
            calls.append(
                {"tool": "list_available_widgets", "args": {"origin": origin}}
            )
            listed.add(origin)
        calls.append(call)
        if name == "list_available_widgets" and origin:
            listed.add(origin)
    task["oracle_tool_calls"] = calls


def _set_core_category(task: dict, family: str) -> None:
    del family
    # Templates declare a category code; map it to the public category axis.
    task["category"] = _CATEGORY_CODE_TO_CATEGORY[task.pop("category_code", "L1")]


def _normalize_core_identity(task: dict) -> None:
    task["id"] = public_id(task["id"])
    task["title"] = clean_title(task["title"])
    task["prompt"] = clean_prompt(task["prompt"])


def _noop_task_stage(task: dict, family: str, level: str, cell_index: int) -> None:
    del task, family, level, cell_index


def _set_core_difficulty(task: dict, family: str, level: str, cell_index: int) -> None:
    del family
    task["difficulty"] = difficulty_for(level, cell_index)


def _core_tag_prefixes(family: str, level: str, cell_index: int) -> tuple[str]:
    del level, cell_index
    return (f"family-{family}",)


def _finalize_core_task(task: dict, family: str, level: str, cell_index: int) -> None:
    del level, cell_index
    task.setdefault("success", {}).setdefault("workspace_checks", {})[
        "preserve_other_dashboards"
    ] = True
    _ensure_widget_discovery(task)
    if family == "backends":
        _attach_backend_runtime_checks(task)


add = TaskAssembler(
    scenarios=SCENARIOS,
    cell_counts=CELL_COUNTS,
    source="workspace-bench-gen",
    schema_version=TASK_SCHEMA_VERSION,
    rung_slack=RUNG_SLACK,
    set_category=_set_core_category,
    normalize_identity=_normalize_core_identity,
    after_identity=_noop_task_stage,
    set_difficulty=_set_core_difficulty,
    tag_prefixes=_core_tag_prefixes,
    finalize_task=_finalize_core_task,
).add


def seeded(name: str, widgets: list[dict], tabs: list[dict] | None = None) -> dict:
    dash: dict = {"name": name, "activate": True, "tabs": tabs or [{"id": "", "name": ""}]}
    if widgets:
        dash["widgets"] = widgets
    return {"dashboard": dash}


def note_call(name: str, text: str) -> dict:
    return {"tool": "add_generative_widget",
            "args": {"widget_type": "note", "name": name, "data": text}}


def discovery(origin: str, widget_id: str, data_args: dict,
              options_param: str | None = None) -> list[dict]:
    calls = [
        {"tool": "list_available_widgets", "args": {"origin": origin}},
        {"tool": "get_widget_schema", "args": {"origin": origin, "widget_id": widget_id}},
    ]
    if options_param:
        calls.append({"tool": "get_params_options",
                      "args": {"origin": origin, "widget_id": widget_id,
                                "param_name": options_param}})
    calls.append({"tool": "create_widget",
                  "args": {"origin": origin, "widget_id": widget_id, "data_args": data_args}})
    return calls


# Fixture fact tables (mirror workspace_bench.workspace.fixtures)
CLOSES = {"AAPL": "196.10", "MSFT": "451.25", "NVDA": "179.45"}
EPS_Q1 = {"AAPL": "2.31", "MSFT": "3.42", "NVDA": "1.18"}
REV_Q1 = {"AAPL": "94.8", "MSFT": "71.2", "NVDA": "39.4"}
MARGIN = {"AAPL": "0.462", "MSFT": "0.694", "NVDA": "0.742"}
MACRO_LATEST = {"FEDFUNDS": "4.12", "DGS2": "3.75", "DGS10": "4.16", "CPIAUCSL": "322.4"}
EQ_NAME = {"price_performance": "Price Performance", "latest_news": "Latest News",
           "estimate_history": "Estimate History", "fundamental_metrics": "Fundamental Metrics"}


def wname(origin: str, widget_id: str) -> str:
    if origin == STK:
        return STARK["widgets"][widget_id]["name"]
    return EQ_NAME.get(widget_id, widget_id.replace("_", " ").title())


def data_args_text(data_args: dict) -> str:
    return f" with data_args {json.dumps(data_args, sort_keys=True)}" if data_args else ""


def widget_ref(origin: str, widget_id: str, data_args: dict | None = None) -> str:
    return f"{origin}/{widget_id}{data_args_text(data_args or {})}"


def joined(items: list[str]) -> str:
    return " and ".join(items)


# ===========================================================================
# Family CREATE — anchor: create_widget
# ===========================================================================

CREATE_T0: list[tuple[str, str, dict[str, Any]]] = [
    (EQ, "price_performance", {"symbol": "AAPL"}),
    (EQ, "latest_news", {"symbol": "AAPL", "limit": 5}),
    (MACRO, "yield_curve", {}),
    (PF, "risk_metrics", {}),
]
for origin, widget_id, data_args in CREATE_T0:
    workflow, sub = wf(origin, widget_id)
    slug = f"{widget_id}_{str(data_args.get('symbol', data_args.get('series', 'plain'))).lower()}"
    add("create", "r0", {
        "id": f"{slug}",
        "title": f"Create {wname(origin, widget_id)}",
        "category_code": "L1", "capability": "widget-creation", "workflow": workflow,
        "subdomain": sub, "tags": ["widget-creation"],
        "prompt": phrased(f"{slug}", [
            (f"Create a {wname(origin, widget_id)} widget (widget_id {widget_id}) from "
             f"the {origin} backend on the active dashboard"
             + (f" with data_args {json.dumps(data_args)}." if data_args else ".")),
            (f"On the active dashboard, create a {wname(origin, widget_id)} widget "
             f"(widget_id {widget_id}) from the {origin} backend"
             + (f" with data_args {json.dumps(data_args)}." if data_args else ".")),
            (f"From the {origin} backend, create a {wname(origin, widget_id)} widget "
             f"(widget_id {widget_id}) on the active dashboard"
             + (f" with data_args {json.dumps(data_args)}." if data_args else ".")),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Creation Task", []),
        "allowed_tools": ["get_workspace_snapshot", "create_widget", "read_widget"],
        "success": {
            "required_widgets": [{"origin": origin, "widget_id": widget_id,
                                    "data_args": data_args, "min_count": 1}],
            "layout": GRID, "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(), {"tool": "create_widget",
                                        "args": {"origin": origin, "widget_id": widget_id,
                                                  "data_args": data_args}}],
    })

CREATE_T1: list[tuple[str, str, dict[str, Any]]] = [
    (EQ, "price_performance", {"symbol": "MSFT"}),
    (EQ, "estimate_history", {"symbol": "NVDA"}),
    (MACRO, "macro_timeseries", {"series": "DGS10"}),
    (PF, "sector_exposure", {}),
]
for origin, widget_id, data_args in CREATE_T1:
    workflow, sub = wf(origin, widget_id)
    slug = f"{widget_id}_{str(data_args.get('symbol', data_args.get('series', 'plain'))).lower()}"
    value = data_args.get("symbol") or data_args.get("series")
    add("create", "r1", {
        "id": f"{slug}",
        "title": f"Add {wname(origin, widget_id)} With Discovery",
        "category_code": "L1", "capability": "widget-creation", "workflow": workflow,
        "subdomain": sub, "tags": ["widget-creation", "schema-discovery"],
        "prompt": phrased(f"{slug}", [
            (f"Add the {wname(origin, widget_id)} widget"
             + (f" for {value}" if value else "")
             + " to the active dashboard. Discover the widget catalog and its schema "
               "before creating."),
            (f"To the active dashboard, add the {wname(origin, widget_id)} widget"
             + (f" for {value}" if value else "")
             + ". Discover the widget catalog and its schema before creating."),
            ("Discover the widget catalog and its schema before creating, then add the "
             f"{wname(origin, widget_id)} widget"
             + (f" for {value}" if value else "")
             + " to the active dashboard."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Creation Task", []),
        "allowed_tools": ["get_workspace_snapshot", "list_available_widgets",
                           "get_widget_schema", "get_params_options", "create_widget",
                           "read_widget"],
        "success": {
            "required_widgets": [{"origin": origin, "widget_id": widget_id,
                                    "data_args": data_args, "min_count": 1}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": [snap()] + discovery(origin, widget_id, data_args),
    })

CREATE_T2: list[tuple[str, str, dict[str, Any], str, tuple[int, int, int, int]]] = [
    (EQ, "price_performance", {"symbol": "NVDA"}, "symbol", (0, 2, 20, 12)),
    (EQ, "latest_news", {"symbol": "MSFT", "limit": 5}, "symbol", (20, 0, 20, 10)),
    (EQ, "fundamental_metrics", {"symbol": "AAPL"}, "symbol", (0, 0, 10, 8)),
    (MACRO, "macro_timeseries", {"series": "FEDFUNDS"}, "series", (0, 2, 20, 10)),
]
for origin, widget_id, data_args, param, (x, y, w, h) in CREATE_T2:
    workflow, sub = wf(origin, widget_id)
    value = data_args[param]
    add("create", "r2", {
        "id": f"place_{widget_id}_{str(value).lower()}",
        "title": f"Add And Place {wname(origin, widget_id)} ({value})",
        "category_code": "L1", "capability": "widget-creation", "workflow": workflow,
        "subdomain": sub, "tags": ["widget-creation", "layout"],
        "prompt": phrased(f"place_{widget_id}_{str(value).lower()}", [
            (f"Add the {wname(origin, widget_id)} widget for {value} and place it at "
             f"exactly x={x}, y={y}, width {w}, height {h}. Fetch the widget schema and "
             f"confirm the {param} value through the parameter options before creating."),
            (f"Place a {wname(origin, widget_id)} widget for {value} at exactly x={x}, "
             f"y={y}, width {w}, height {h}. Fetch the widget schema and confirm the "
             f"{param} value through the parameter options before creating."),
            (f"Fetch the widget schema and confirm the {param} value through the parameter "
             f"options before creating the {wname(origin, widget_id)} widget for {value}, "
             f"then place it at exactly x={x}, y={y}, width {w}, height {h}."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Placement Task", []),
        "allowed_tools": ["get_workspace_snapshot", "list_available_widgets",
                           "get_widget_schema", "get_params_options", "create_widget",
                           "update_widget_layout", "read_widget"],
        "success": {
            "required_widgets": [{"origin": origin, "widget_id": widget_id,
                                    "data_args": data_args, "min_count": 1}],
            "required_layouts": [{"widget_id": widget_id, "x": x, "y": y, "w": w, "h": h}],
            "required_tool_calls": [{"tool": "get_params_options",
                                       "args_contains": {"widget_id": widget_id,
                                                          "param_name": param}}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": [snap()] + discovery(origin, widget_id, data_args, param)
        + [{"tool": "update_widget_layout",
             "args": {"widget_id": widget_id, "x": x, "y": y, "w": w, "h": h}}],
    })

CREATE_T3: list[tuple[str, str, dict[str, Any], str, dict[str, Any]]] = [
    (EQ, "price_performance", {"symbol": "AAPL"}, "latest_news",
     {"symbol": "AAPL", "limit": 5}),
    (MACRO, "macro_timeseries", {"series": "DGS10"}, "yield_curve", {}),
    (PF, "holdings_table", {}, "risk_metrics", {}),
    (EQ, "estimate_history", {"symbol": "MSFT"}, "fundamental_metrics", {"symbol": "MSFT"}),
]
for origin, seed_id, seed_args, new_id, new_args in CREATE_T3:
    workflow, sub = wf(origin, new_id)
    add("create", "r3", {
        "id": f"preserve_{new_id}_{str(new_args.get('symbol', 'plain')).lower()}",
        "title": f"Extend Dashboard With {wname(origin, new_id)}",
        "category_code": "L1", "capability": "widget-creation", "workflow": workflow,
        "subdomain": sub, "tags": ["widget-creation", "preservation"],
        "prompt": phrased(
            f"preserve_{new_id}_{str(new_args.get('symbol', 'plain')).lower()}",
            [
                (f"This dashboard already has a {wname(origin, seed_id)} widget. Add the "
                 f"{wname(origin, new_id)} widget"
                 + (f" for {new_args.get('symbol')}" if new_args.get("symbol") else "")
                 + " next to it without disturbing the existing widget or overlapping it."),
                (f"A {wname(origin, seed_id)} widget is already on this dashboard. Add the "
                 f"{wname(origin, new_id)} widget"
                 + (f" for {new_args.get('symbol')}" if new_args.get("symbol") else "")
                 + " next to it without disturbing the existing widget or overlapping it."),
                (f"Keep the existing {wname(origin, seed_id)} widget undisturbed and "
                 f"non-overlapped while adding the {wname(origin, new_id)} widget"
                 + (f" for {new_args.get('symbol')}" if new_args.get("symbol") else "")
                 + " next to it."),
            ],
        ),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Existing Review",
                                 [{"origin": origin, "widget_id": seed_id,
                                   "data_args": seed_args,
                                   "layout": {"x": 0, "y": 0, "w": 20, "h": 12}}]),
        "allowed_tools": ["get_workspace_snapshot", "list_available_widgets",
                           "get_widget_schema", "get_params_options", "create_widget",
                           "update_widget_layout", "read_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": seed_id, "data_args": seed_args,
                 "min_count": 1, "max_count": 1},
                {"origin": origin, "widget_id": new_id, "data_args": new_args,
                 "min_count": 1},
            ],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": [snap()] + discovery(origin, new_id, new_args)
        + [{"tool": "update_widget_layout",
             "args": {"widget_id": new_id, "x": 20, "y": 0, "w": 20, "h": 10}}],
    })

CREATE_T4: list[
    tuple[str, list[tuple[str, str, dict[str, Any]]], list[str], str]
] = [
    ("aapl_rates", [(EQ, "price_performance", {"symbol": "AAPL"}),
                     (MACRO, "macro_timeseries", {"series": "DGS10"})],
     ["AAPL", "DGS10"], "AAPL price against the DGS10 rates backdrop."),
    ("nvda_curve", [(EQ, "price_performance", {"symbol": "NVDA"}),
                     (MACRO, "yield_curve", {})],
     ["NVDA", "yield curve"], "NVDA price with the yield curve for rate context."),
    ("book_inflation", [(PF, "holdings_table", {}),
                          (MACRO, "macro_timeseries", {"series": "CPIAUCSL"})],
     ["holdings", "CPIAUCSL"], "Holdings reviewed against the CPIAUCSL inflation series."),
    ("msft_exposure", [(EQ, "latest_news", {"symbol": "MSFT", "limit": 5}),
                         (PF, "sector_exposure", {})],
     ["MSFT", "sector exposure"], "MSFT news next to the book's sector exposure."),
]
for slug, widgets, note_facts, note_text in CREATE_T4:
    origins = sorted({o for o, _, _ in widgets})
    workflow, sub = wf(origins[0], widgets[0][1])
    oracle = [snap()]
    for origin, widget_id, data_args in widgets:
        oracle += discovery(origin, widget_id, data_args)
    oracle.append(note_call("Build Note", note_text))
    add("create", "r4", {
        "id": f"cross_{slug}",
        "title": f"Cross-Backend Build: {slug.replace('_', ' ').title()}",
        "category_code": "L2", "capability": "widget-creation", "workflow": workflow,
        "subdomain": sub, "tags": ["widget-creation", "cross-backend"],
        "prompt": phrased(f"cross_{slug}", [
            ("Add these two widgets to the active dashboard: "
             + " and ".join(f"the {wname(o, wid)} widget from {o}"
                             + (f" for {a.get('symbol') or a.get('series')}"
                                if (a.get('symbol') or a.get('series')) else "")
                             for o, wid, a in widgets)
             + f". Then add a note mentioning {note_facts[0]} and {note_facts[1]}."),
            ("On the active dashboard, add these two widgets: "
             + " and ".join(f"the {wname(o, wid)} widget from {o}"
                             + (f" for {a.get('symbol') or a.get('series')}"
                                if (a.get('symbol') or a.get('series')) else "")
                             for o, wid, a in widgets)
             + f". Then add a note mentioning {note_facts[0]} and {note_facts[1]}."),
            ("Build the active dashboard with these two widgets: "
             + " and ".join(f"the {wname(o, wid)} widget from {o}"
                             + (f" for {a.get('symbol') or a.get('series')}"
                                if (a.get('symbol') or a.get('series')) else "")
                             for o, wid, a in widgets)
             + f". Add a note mentioning {note_facts[0]} and {note_facts[1]}."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(o)} for o in origins]},
        "initial_state": seeded("Cross-Backend Task", []),
        "allowed_tools": ["get_workspace_snapshot", "list_available_widgets",
                           "get_widget_schema", "get_params_options", "create_widget",
                           "update_widget_layout", "add_generative_widget"],
        "success": {
            "required_widgets": [
                {"origin": o, "widget_id": wid, "data_args": a, "min_count": 1}
                for o, wid, a in widgets],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": note_facts}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": oracle,
    })


# ===========================================================================
# Family UPDATE — anchor: update_widget
# ===========================================================================

UPDATE_T0: list[tuple[str, str, dict[str, Any], str, str]] = [
    (EQ, "price_performance", {"symbol": "MSFT"}, "symbol", "AAPL"),
    (EQ, "latest_news", {"symbol": "NVDA", "limit": 5}, "symbol", "MSFT"),
    (MACRO, "macro_timeseries", {"series": "DGS2"}, "series", "DGS10"),
    (STK, "portfolio_command_center_overview_portfolio_snapshot",
     {"fund": "Flagship Long/Short", "period": "YTD"}, "period", "MTD"),
]
for origin, widget_id, seed_args, param, new_value in UPDATE_T0:
    workflow, sub = wf(origin, widget_id)
    add("update", "r0", {
        "id": f"{param}_{str(new_value).lower().replace(' ', '_')}_{stark_value(widget_id):.0f}",
        "title": f"Set {wname(origin, widget_id)} {param} To {new_value}",
        "category_code": "L1", "capability": "widget-update", "workflow": workflow,
        "subdomain": sub, "tags": ["update-widget"],
        "prompt": phrased(
            f"{param}_{str(new_value).lower().replace(' ', '_')}_{stark_value(widget_id):.0f}",
            [
                (f"Set the {wname(origin, widget_id)} widget's {param} to {new_value}. "
                 "Update the existing widget."),
                (f"Update the existing {wname(origin, widget_id)} widget by setting "
                 f"{param} to {new_value}."),
                (f"For the existing {wname(origin, widget_id)} widget, set {param} to "
                 f"{new_value}."),
            ],
        ),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Update Task",
                                 [{"origin": origin, "widget_id": widget_id,
                                   "data_args": seed_args,
                                   "layout": {"x": 0, "y": 0, "w": 20, "h": 12}}]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "update_widget"],
        "success": {
            "required_widgets": [{"origin": origin, "widget_id": widget_id,
                                    "data_args": {**seed_args, param: new_value},
                                    "min_count": 1}],
            "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(), {"tool": "update_widget",
                                        "args": {"widget_uuid": "widget_001",
                                                  "data_args": {param: new_value}}}],
    })

UPDATE_T1 = [
    (EQ, "estimate_history", {"symbol": "AAPL"}, "symbol", "NVDA"),
    (EQ, "fundamental_metrics", {"symbol": "MSFT"}, "symbol", "NVDA"),
    (MACRO, "macro_timeseries", {"series": "CPIAUCSL"}, "series", "FEDFUNDS"),
    (STK, "execution_desk_exceptions_rejected_orders",
     {"desk": "US Equities", "status": "Open"}, "status", "Escalated"),
]
for origin, widget_id, seed_args, param, new_value in UPDATE_T1:
    workflow, sub = wf(origin, widget_id)
    old_value = seed_args[param]
    add("update", "r1", {
        "id": f"{param}_{str(new_value).lower().replace(' ', '_')}_{stark_value(widget_id):.0f}",
        "title": f"Update {wname(origin, widget_id)} ({old_value} To {new_value})",
        "category_code": "L1", "capability": "widget-update", "workflow": workflow,
        "subdomain": sub, "tags": ["update-widget"],
        "prompt": phrased(
            f"{param}_{str(new_value).lower().replace(' ', '_')}_{stark_value(widget_id):.0f}",
            [
                (f"The {wname(origin, widget_id)} widget currently shows {old_value}. "
                 f"Update the existing widget to {new_value}; do not create a new one and "
                 "leave no widget showing the old value."),
                (f"The existing {wname(origin, widget_id)} widget currently shows "
                 f"{old_value}. Update that widget to {new_value}; do not create a new one "
                 "and leave no widget showing the old value."),
                (f"Update the existing {wname(origin, widget_id)} widget from {old_value} "
                 f"to {new_value}; do not create a new one and leave no widget showing the "
                 "old value."),
            ],
        ),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Update Task",
                                 [{"origin": origin, "widget_id": widget_id,
                                   "data_args": seed_args,
                                   "layout": {"x": 0, "y": 0, "w": 20, "h": 12}}]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "update_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id,
                 "data_args": {**seed_args, param: new_value}, "min_count": 1},
                {"origin": origin, "widget_id": widget_id,
                 "data_args": {param: old_value}, "min_count": 0, "max_count": 0},
            ],
            "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "read_widget", "args": {"widget_id": widget_id}},
                               {"tool": "update_widget",
                                "args": {"widget_uuid": "widget_001",
                                          "data_args": {param: new_value}}}],
    })

UPDATE_T2 = [
    (EQ, "price_performance", "symbol", "AAPL", "MSFT", "NVDA"),
    (MACRO, "macro_timeseries", "series", "DGS10", "DGS2", "FEDFUNDS"),
    (EQ, "latest_news", "symbol", "AAPL", "NVDA", "MSFT"),
    (STK, "vendor_dataset_monitor_slas_vendor_sla_status", "vendor",
     "Bloomberg", "FactSet", "Refinitiv"),
]
for origin, widget_id, param, keep_value, target_value, new_value in UPDATE_T2:
    workflow, sub = wf(origin, widget_id)
    extra = {"limit": 5} if widget_id == "latest_news" else {}
    add("update", "r2", {
        "id": f"pick_{param}_{str(target_value).lower()}_{stark_value(widget_id):.0f}",
        "title": f"Update Only The {target_value} {wname(origin, widget_id)}",
        "category_code": "L1", "capability": "widget-update", "workflow": workflow,
        "subdomain": sub, "tags": ["update-widget", "distractors"],
        "prompt": phrased(
            f"pick_{param}_{str(target_value).lower()}_{stark_value(widget_id):.0f}",
            [
                (f"This dashboard has two {wname(origin, widget_id)} widgets: one for "
                 f"{keep_value} and one for {target_value}. Update only the {target_value} "
                 f"one to {new_value}; leave the {keep_value} widget untouched."),
                (f"Two {wname(origin, widget_id)} widgets are on this dashboard: one for "
                 f"{keep_value} and one for {target_value}. Only update the {target_value} "
                 f"one to {new_value}; leave the {keep_value} widget untouched."),
                (f"Leave the {keep_value} {wname(origin, widget_id)} widget untouched, and "
                 f"update only the {target_value} {wname(origin, widget_id)} widget to "
                 f"{new_value}."),
            ],
        ),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Selective Update Task", [
            {"origin": origin, "widget_id": widget_id,
             "data_args": {param: keep_value, **extra},
             "layout": {"x": 0, "y": 0, "w": 20, "h": 10}},
            {"origin": origin, "widget_id": widget_id,
             "data_args": {param: target_value, **extra},
             "layout": {"x": 20, "y": 0, "w": 20, "h": 10}},
        ]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "update_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": {param: keep_value},
                 "min_count": 1, "max_count": 1},
                {"origin": origin, "widget_id": widget_id, "data_args": {param: new_value},
                 "min_count": 1, "max_count": 1},
                {"origin": origin, "widget_id": widget_id, "data_args": {param: target_value},
                 "min_count": 0, "max_count": 0},
            ],
            "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(), {"tool": "update_widget",
                                        "args": {"widget_uuid": "widget_002",
                                                  "data_args": {param: new_value}}}],
    })

UPDATE_T3 = [
    ("ticker_nvda_msft", EQ, "price_performance", "symbol", "NVDA", "MSFT",
     "This MSFT review dashboard mistakenly shows NVDA in the price widget."),
    ("news_msft_aapl", EQ, "latest_news", "symbol", "MSFT", "AAPL",
     "This AAPL desk dashboard mistakenly shows MSFT news."),
    ("series_fedfunds_cpi", MACRO, "macro_timeseries", "series", "FEDFUNDS", "CPIAUCSL",
     "This inflation dashboard mistakenly shows the FEDFUNDS series."),
    ("risk_fund", STK, "risk_exposure_monitor_dashboard_risk_snapshot", "fund",
     "Global Macro", "Flagship Long/Short",
     "This Flagship Long/Short risk dashboard has its snapshot configured for Global Macro."),
]
for slug, origin, widget_id, param, old_value, new_value, context in UPDATE_T3:
    workflow, sub = wf(origin, widget_id)
    add("update", "r3", {
        "id": f"repair_{slug}",
        "title": f"Repair {wname(origin, widget_id)}",
        "category_code": "L4", "capability": "workspace-repair", "workflow": workflow,
        "subdomain": sub, "tags": ["repair", "update-widget"],
        "prompt": phrased(f"repair_{slug}", [
            (f"{context} Repair the widget to {new_value} and add a note saying what "
             "was repaired, mentioning both values."),
            (f"{context} Repair the widget to {new_value}; then add a note saying what "
             "was repaired and mentioning both values."),
            (f"{context} Add a note saying what was repaired and mentioning both values "
             f"after you repair the widget to {new_value}."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Repair Task",
                                 [{"origin": origin, "widget_id": widget_id,
                                   "data_args": {param: old_value},
                                   "layout": {"x": 0, "y": 0, "w": 20, "h": 12}}]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "update_widget",
                           "add_generative_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": {param: new_value},
                 "min_count": 1},
                {"origin": origin, "widget_id": widget_id, "data_args": {param: old_value},
                 "min_count": 0, "max_count": 0},
            ],
            "required_generated_widgets": [
                {"widget_type": "note",
                 "data_contains": [str(old_value), str(new_value), "repaired"]}],
            "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "read_widget", "args": {"widget_id": widget_id}},
                               {"tool": "update_widget",
                                "args": {"widget_uuid": "widget_001",
                                          "data_args": {param: new_value}}},
                               note_call("Repair Note",
                                         f"Repaired {widget_id} from {old_value} to "
                                         f"{new_value}.")],
    })

UPDATE_T4: list[
    tuple[
        str,
        str,
        list[tuple[str, dict[str, Any], dict[str, Any]]],
        list[str],
        list[str],
    ]
] = [
    ("aapl_desk", EQ,
     [("price_performance", {"symbol": "MSFT"}, {"symbol": "AAPL"}),
      ("latest_news", {"symbol": "AAPL", "limit": 1}, {"limit": 5})],
     ["AAPL", "repaired"],
     [
         "Two fixes on this AAPL desk dashboard: the price widget shows MSFT, and the news "
         "widget shows only 1 article (desk standard is 5). Repair both existing widgets and add "
         "a note mentioning AAPL and the word repaired.",
         "On this AAPL desk dashboard, repair two existing widgets: the price widget shows "
         "MSFT, and the news widget shows only 1 article (desk standard is 5). Repair both "
         "existing widgets and add a note mentioning AAPL and the word repaired.",
         "This AAPL desk dashboard needs two repairs: the price widget should show AAPL, not "
         "MSFT, and the news widget should show 5 articles, not only 1. Repair both existing "
         "widgets and add a note mentioning AAPL and the word repaired.",
     ]),
    ("nvda_switch", EQ,
     [("price_performance", {"symbol": "AAPL"}, {"symbol": "NVDA"}),
      ("estimate_history", {"symbol": "MSFT"}, {"symbol": "NVDA"})],
     ["NVDA", "repaired"],
     [
         "This dashboard should track NVDA, but the price widget shows AAPL and the estimates "
         "widget shows MSFT. Repair both existing widgets to NVDA and add a note mentioning "
         "NVDA and the word repaired.",
         "The dashboard is meant to track NVDA, while the price widget shows AAPL and the "
         "estimates widget shows MSFT. Repair both existing widgets to NVDA and add a note "
         "mentioning NVDA and the word repaired.",
         "Repair the existing widgets on this NVDA dashboard: change the price widget from "
         "AAPL to NVDA and the estimates widget from MSFT to NVDA, then add a note "
         "mentioning NVDA and the word repaired.",
     ]),
    ("rates_switch", MACRO,
     [("macro_timeseries", {"series": "DGS2"}, {"series": "DGS10"}),
      ("macro_timeseries", {"series": "FEDFUNDS"}, {"series": "CPIAUCSL"})],
     ["DGS10", "CPIAUCSL", "repaired"],
     [
         "Two series are wrong on this dashboard: the first macro widget should show DGS10 (not "
         "DGS2) and the second should show CPIAUCSL (not FEDFUNDS). Repair both existing "
         "widgets and add a note mentioning DGS10, CPIAUCSL, and the word repaired.",
         "On this dashboard, repair two macro series: the first widget should show DGS10 (not "
         "DGS2), and the second should show CPIAUCSL (not FEDFUNDS). Repair both existing "
         "widgets and add a note mentioning DGS10, CPIAUCSL, and the word repaired.",
         "The first macro widget is DGS2 but should be DGS10, and the second is FEDFUNDS but "
         "should be CPIAUCSL. Repair both existing widgets and add a note mentioning DGS10, "
         "CPIAUCSL, and the word repaired.",
     ]),
    ("stark_ops", STK,
     [("vendor_dataset_monitor_slas_vendor_sla_status",
       {"vendor": "FactSet", "status": "Open"}, {"status": "Escalated"}),
      ("portfolio_command_center_overview_portfolio_snapshot",
       {"fund": "Flagship Long/Short", "period": "YTD"}, {"period": "MTD"})],
     ["Escalated", "MTD", "repaired"],
     [
         "Two fixes on this ops dashboard: the Vendor SLA Status widget should show Escalated "
         "items (not Open), and the Portfolio Snapshot should show MTD (not YTD). Repair both "
         "existing widgets and add a note mentioning Escalated, MTD, and the word repaired.",
         "On this ops dashboard, repair the Vendor SLA Status widget to show Escalated items "
         "(not Open) and the Portfolio Snapshot to show MTD (not YTD). Repair both existing "
         "widgets and add a note mentioning Escalated, MTD, and the word repaired.",
         "The ops dashboard has two wrong settings: Vendor SLA Status is Open but should be "
         "Escalated, and Portfolio Snapshot is YTD but should be MTD. Repair both existing "
         "widgets and add a note mentioning Escalated, MTD, and the word repaired.",
     ]),
]
for slug, origin, updates, note_facts, prompt_variants in UPDATE_T4:
    workflow, sub = wf(origin, updates[0][0])
    seeds, oracle = [], [snap()]
    checks: list[dict] = []
    for index, (widget_id, seed_args, delta) in enumerate(updates):
        seeds.append({"origin": origin, "widget_id": widget_id, "data_args": seed_args,
                       "layout": {"x": (index % 2) * 20, "y": (index // 2) * 12,
                                   "w": 20, "h": 10}})
        oracle.append({"tool": "update_widget",
                        "args": {"widget_uuid": f"widget_{index + 1:03d}",
                                  "data_args": delta}})
        merged = {**seed_args, **delta}
        checks.append({"origin": origin, "widget_id": widget_id, "data_args": merged,
                        "min_count": 1})
        changed_key = next(iter(delta))
        checks.append({"origin": origin, "widget_id": widget_id,
                        "data_args": {changed_key: seed_args[changed_key]},
                        "min_count": 0, "max_count": 0})
    oracle.append(note_call("Repair Note", "Repaired: " + ", ".join(note_facts) + "."))
    add("update", "r4", {
        "id": f"double_{slug}",
        "title": f"Double Repair: {slug.replace('_', ' ').title()}",
        "category_code": "L4", "capability": "workspace-repair", "workflow": workflow,
        "subdomain": sub, "tags": ["repair", "update-widget", "combo"],
        "prompt": phrased(f"double_{slug}", prompt_variants),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Double Repair Task", seeds),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "update_widget",
                           "add_generative_widget"],
        "success": {
            "required_widgets": checks,
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": note_facts}],
            "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": oracle,
    })


# ===========================================================================
# Family DELETE — anchor: delete_widget
# ===========================================================================

DELETE_T0: list[tuple[str, str, dict[str, Any]]] = [
    (EQ, "latest_news", {"symbol": "AAPL", "limit": 5}),
    (EQ, "price_performance", {"symbol": "NVDA"}),
    (MACRO, "macro_timeseries", {"series": "DGS2"}),
    (STK, "portfolio_command_center_overview_top_alerts", {}),
]
for origin, widget_id, data_args in DELETE_T0:
    workflow, sub = wf(origin, widget_id)
    add("delete", "r0", {
        "id": f"{widget_id.rsplit('_', 1)[-1]}_{stark_value(widget_id):.0f}",
        "title": f"Remove {wname(origin, widget_id)}",
        "category_code": "L1", "capability": "widget-update", "workflow": workflow,
        "subdomain": sub, "tags": ["delete-widget"],
        "prompt": phrased(
            f"{widget_id.rsplit('_', 1)[-1]}_{stark_value(widget_id):.0f}",
            [
                (f"The {wname(origin, widget_id)} widget is no longer needed on this "
                 "dashboard. Remove it."),
                (f"Remove the {wname(origin, widget_id)} widget from this dashboard because "
                 "it is no longer needed."),
                (f"This dashboard no longer needs the {wname(origin, widget_id)} widget; "
                 "remove it."),
            ],
        ),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Removal Task",
                                 [{"origin": origin, "widget_id": widget_id,
                                   "data_args": data_args,
                                   "layout": {"x": 0, "y": 0, "w": 20, "h": 10}}]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "delete_widget"],
        "success": {
            "required_widgets": [{"origin": origin, "widget_id": widget_id,
                                    "data_args": {}, "min_count": 0, "max_count": 0}],
            "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(), {"tool": "delete_widget",
                                        "args": {"widget_uuid": "widget_001"}}],
    })

DELETE_T1: list[tuple[str, str, dict[str, Any]]] = [
    (EQ, "latest_news", {"symbol": "MSFT", "limit": 5}),
    (EQ, "price_performance", {"symbol": "AAPL"}),
    (MACRO, "macro_timeseries", {"series": "DGS10"}),
    (STK, "vendor_dataset_monitor_slas_vendor_sla_status", {"vendor": "FactSet"}),
]
for origin, widget_id, data_args in DELETE_T1:
    workflow, sub = wf(origin, widget_id)
    add("delete", "r1", {
        "id": f"dup_{widget_id.rsplit('_', 1)[-1]}_{stark_value(widget_id):.0f}",
        "title": f"Remove Duplicate {wname(origin, widget_id)}",
        "category_code": "L1", "capability": "widget-update", "workflow": workflow,
        "subdomain": sub, "tags": ["delete-widget"],
        "prompt": phrased(
            f"dup_{widget_id.rsplit('_', 1)[-1]}_{stark_value(widget_id):.0f}",
            [
                (f"The dashboard has two identical {wname(origin, widget_id)} widgets. "
                 "Remove exactly one so a single copy remains; do not change the one that "
                 "stays."),
                (f"There are two identical {wname(origin, widget_id)} widgets on the "
                 "dashboard. Remove exactly one so a single copy remains; do not change the "
                 "one that stays."),
                (f"Remove exactly one of the two identical {wname(origin, widget_id)} "
                 "widgets, leaving a single copy, and do not change the one that stays."),
            ],
        ),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Duplicate Cleanup", [
            {"origin": origin, "widget_id": widget_id, "data_args": dict(data_args),
             "layout": {"x": 0, "y": 0, "w": 20, "h": 10}},
            {"origin": origin, "widget_id": widget_id, "data_args": dict(data_args),
             "layout": {"x": 20, "y": 0, "w": 20, "h": 10}},
        ]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "delete_widget"],
        "success": {
            "required_widgets": [{"origin": origin, "widget_id": widget_id,
                                    "data_args": data_args, "min_count": 1, "max_count": 1}],
            "layout": GRID, "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(), {"tool": "delete_widget",
                                        "args": {"widget_uuid": "widget_002"}}],
    })

DELETE_T2 = [
    (EQ, "price_performance", "symbol", "AAPL", "MSFT"),
    (EQ, "latest_news", "symbol", "NVDA", "AAPL"),
    (MACRO, "macro_timeseries", "series", "DGS10", "DGS2"),
    (EQ, "estimate_history", "symbol", "MSFT", "NVDA"),
]
for origin, widget_id, param, dup_value, keep_value in DELETE_T2:
    workflow, sub = wf(origin, widget_id)
    extra = {"limit": 5} if widget_id == "latest_news" else {}
    add("delete", "r2", {
        "id": f"similar_{widget_id}_{dup_value.lower()}",
        "title": f"Remove Only The Duplicate {dup_value} Widget",
        "category_code": "L1", "capability": "widget-update", "workflow": workflow,
        "subdomain": sub, "tags": ["delete-widget", "distractors"],
        "prompt": phrased(f"similar_{widget_id}_{dup_value.lower()}", [
            (f"This dashboard has three {wname(origin, widget_id)} widgets: two "
             f"identical ones for {dup_value} and one for {keep_value}. Remove exactly "
             f"one duplicate {dup_value} widget; keep the other and keep the "
             f"{keep_value} widget untouched."),
            (f"Three {wname(origin, widget_id)} widgets are on this dashboard: two "
             f"identical ones for {dup_value} and one for {keep_value}. Remove exactly one "
             f"duplicate {dup_value} widget; keep the other and keep the {keep_value} "
             "widget untouched."),
            (f"Remove exactly one duplicate {dup_value} {wname(origin, widget_id)} widget "
             f"from the two identical {dup_value} copies, while keeping the other duplicate "
             f"and the {keep_value} widget untouched."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Similar Cleanup", [
            {"origin": origin, "widget_id": widget_id,
             "data_args": {param: dup_value, **extra},
             "layout": {"x": 0, "y": 0, "w": 20, "h": 10}},
            {"origin": origin, "widget_id": widget_id,
             "data_args": {param: dup_value, **extra},
             "layout": {"x": 20, "y": 0, "w": 20, "h": 10}},
            {"origin": origin, "widget_id": widget_id,
             "data_args": {param: keep_value, **extra},
             "layout": {"x": 0, "y": 10, "w": 20, "h": 10}},
        ]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "delete_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": {param: dup_value},
                 "min_count": 1, "max_count": 1},
                {"origin": origin, "widget_id": widget_id, "data_args": {param: keep_value},
                 "min_count": 1, "max_count": 1},
            ],
            "layout": GRID, "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(), {"tool": "delete_widget",
                                        "args": {"widget_uuid": "widget_002"}}],
    })

DELETE_T3 = [
    (EQ, "fundamental_metrics", {"symbol": "NVDA"}),
    (EQ, "estimate_history", {"symbol": "AAPL"}),
    (PF, "sector_exposure", {}),
    (STK, "execution_desk_blotter_live_orders", {"status": "Open"}),
]
for origin, widget_id, data_args in DELETE_T3:
    workflow, sub = wf(origin, widget_id)
    add("delete", "r3", {
        "id": f"note_{widget_id.rsplit('_', 1)[-1]}_{stark_value(widget_id):.0f}",
        "title": f"Remove Duplicate {wname(origin, widget_id)} And Document",
        "category_code": "L4", "capability": "workspace-repair", "workflow": workflow,
        "subdomain": sub, "tags": ["repair", "delete-widget"],
        "prompt": phrased(
            f"note_{widget_id.rsplit('_', 1)[-1]}_{stark_value(widget_id):.0f}",
            [
                (f"This dashboard has two identical {wname(origin, widget_id)} widgets. "
                 "Remove exactly one duplicate, then add a note saying the duplicate was "
                 "removed."),
                (f"Two identical {wname(origin, widget_id)} widgets are on this dashboard. "
                 "Remove exactly one duplicate, then add a note saying the duplicate was "
                 "removed."),
                (f"Remove exactly one duplicate from the two identical "
                 f"{wname(origin, widget_id)} widgets, then add a note saying the duplicate "
                 "was removed."),
            ],
        ),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Duplicate Repair", [
            {"origin": origin, "widget_id": widget_id, "data_args": dict(data_args),
             "layout": {"x": 0, "y": 0, "w": 20, "h": 10}},
            {"origin": origin, "widget_id": widget_id, "data_args": dict(data_args),
             "layout": {"x": 20, "y": 0, "w": 20, "h": 10}},
        ]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "delete_widget",
                           "add_generative_widget"],
        "success": {
            "required_widgets": [{"origin": origin, "widget_id": widget_id,
                                    "data_args": data_args, "min_count": 1, "max_count": 1}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": ["duplicate", "removed"]}],
            "layout": GRID, "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "delete_widget", "args": {"widget_uuid": "widget_002"}},
                               note_call("Cleanup Note",
                                         "Removed the duplicate widget; one copy remains.")],
    })

DELETE_T4 = [
    (EQ, "price_performance", "symbol", "AAPL", "NVDA"),
    (EQ, "latest_news", "symbol", "NVDA", "AAPL"),
    (MACRO, "macro_timeseries", "series", "DGS10", "DGS2"),
    (STK, "vendor_dataset_monitor_slas_vendor_sla_status", "status", "Open", "Escalated"),
]
for origin, widget_id, param, dup_value, new_value in DELETE_T4:
    workflow, sub = wf(origin, widget_id)
    extra = {"limit": 5} if widget_id == "latest_news" else {}
    add("delete", "r4", {
        "id": f"then_fix_{widget_id.rsplit('_', 1)[-1]}_{str(new_value).lower()}_{stark_value(widget_id):.0f}",
        "title": f"Deduplicate And Fix {wname(origin, widget_id)}",
        "category_code": "L4", "capability": "workspace-repair", "workflow": workflow,
        "subdomain": sub, "tags": ["repair", "delete-widget", "combo"],
        "prompt": phrased(
            f"then_fix_{widget_id.rsplit('_', 1)[-1]}_{str(new_value).lower()}_{stark_value(widget_id):.0f}",
            [
                (f"This dashboard has two identical {wname(origin, widget_id)} widgets for "
                 f"{dup_value}, and the desk actually needs {new_value}. Remove exactly one "
                 f"duplicate, update the remaining widget to {new_value}, and add a note "
                 f"mentioning {new_value} and the word repaired."),
                (f"The dashboard contains two identical {wname(origin, widget_id)} widgets "
                 f"for {dup_value}, but the desk actually needs {new_value}. Remove exactly "
                 f"one duplicate, update the remaining widget to {new_value}, and add a note "
                 f"mentioning {new_value} and the word repaired."),
                (f"Remove exactly one duplicate from the two identical "
                 f"{wname(origin, widget_id)} widgets for {dup_value}; then update the "
                 f"remaining widget to {new_value} and add a note mentioning {new_value} "
                 "and the word repaired."),
            ],
        ),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Dedup And Fix", [
            {"origin": origin, "widget_id": widget_id,
             "data_args": {param: dup_value, **extra},
             "layout": {"x": 0, "y": 0, "w": 20, "h": 10}},
            {"origin": origin, "widget_id": widget_id,
             "data_args": {param: dup_value, **extra},
             "layout": {"x": 20, "y": 0, "w": 20, "h": 10}},
        ]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "delete_widget",
                           "update_widget", "add_generative_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": {param: new_value},
                 "min_count": 1, "max_count": 1},
                {"origin": origin, "widget_id": widget_id, "data_args": {param: dup_value},
                 "min_count": 0, "max_count": 0},
            ],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": [str(new_value), "repaired"]}],
            "layout": GRID, "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "delete_widget", "args": {"widget_uuid": "widget_002"}},
                               {"tool": "update_widget",
                                "args": {"widget_uuid": "widget_001",
                                          "data_args": {param: new_value}}},
                               note_call("Repair Note",
                                         f"Removed the duplicate and repaired to {new_value}.")],
    })


# ===========================================================================
# Family LAYOUT — anchor: update_widget_layout
# ===========================================================================

LAYOUT_T0: list[
    tuple[str, str, dict[str, Any], dict[str, int], dict[str, int], list[str]]
] = [
    ("halve_price_msft", "price_performance", {"symbol": "MSFT"},
     {"x": 0, "y": 2, "w": 40, "h": 12}, {"x": 0, "y": 2, "w": 20, "h": 12},
     [
         "Resize the MSFT price widget to half width (20 columns). Keep its position.",
         "Keep the MSFT price widget in place and resize it to half width (20 columns).",
         "Change the MSFT price widget to half width (20 columns) without moving its position.",
     ]),
    ("move_news_right", "latest_news", {"symbol": "AAPL", "limit": 5},
     {"x": 0, "y": 0, "w": 20, "h": 10}, {"x": 20, "y": 0, "w": 20, "h": 10},
     [
         "Move the AAPL news widget to start at column 20. Keep its size.",
         "Keep the AAPL news widget's size and move it to start at column 20.",
         "Set the AAPL news widget to start at column 20 while keeping its size.",
     ]),
    ("shorten_estimates_nvda", "estimate_history", {"symbol": "NVDA"},
     {"x": 0, "y": 0, "w": 20, "h": 12}, {"x": 0, "y": 0, "w": 20, "h": 8},
     [
         "Reduce the NVDA estimates widget height to 8 rows. Keep its position and width.",
         "Keep the NVDA estimates widget's position and width, but reduce its height to 8 rows.",
         "Set the NVDA estimates widget height to 8 rows without changing its position or width.",
     ]),
    ("widen_fundamentals_aapl", "fundamental_metrics", {"symbol": "AAPL"},
     {"x": 0, "y": 0, "w": 10, "h": 8}, {"x": 0, "y": 0, "w": 20, "h": 8},
     [
         "Widen the AAPL fundamentals widget to 20 columns. Keep its position and height.",
         "Keep the AAPL fundamentals widget's position and height, but widen it to 20 columns.",
         "Set the AAPL fundamentals widget width to 20 columns without changing its position or height.",
     ]),
]
for slug, widget_id, data_args, seed_layout, target, prompt_variants in LAYOUT_T0:
    add("layout", "r0", {
        "id": f"{slug}",
        "title": f"Layout: {slug.replace('_', ' ').title()}",
        "category_code": "L1", "capability": "layout-management",
        "workflow": "equity-tearsheet", "subdomain": "equity-research",
        "tags": ["layout"],
        "prompt": phrased(f"{slug}", prompt_variants),
        "fixtures": {"backends": [{"name": "equities"}]},
        "initial_state": seeded("Layout Task",
                                 [{"origin": EQ, "widget_id": widget_id,
                                   "data_args": data_args, "tab_id": "charts",
                                   "layout": dict(seed_layout)}],
                                 tabs=[{"id": "charts", "name": "Charts"}]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "update_widget_layout"],
        "success": {
            "required_tabs": ["charts"],
            "required_widgets": [{"origin": EQ, "widget_id": widget_id,
                                    "data_args": data_args, "tab_id": "charts"}],
            "required_layouts": [{"widget_id": widget_id, "tab_id": "charts", **target}],
            "layout": GRID, "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "update_widget_layout",
                                "args": {"widget_id": widget_id, "tab_id": "charts",
                                          **target}}],
    })

LAYOUT_T1 = [
    ("price_news_aapl",
     ("price_performance", {"symbol": "AAPL"}, {"x": 0, "y": 0, "w": 20, "h": 12}),
     ("latest_news", {"symbol": "AAPL", "limit": 5},
      {"x": 0, "y": 12, "w": 20, "h": 10}, {"x": 20, "y": 0, "w": 20, "h": 10}),
     [
         "Move the AAPL news widget up beside the price widget: it should start at column 20, "
         "row 0, keeping its size. Do not move the price widget.",
         "Do not move the price widget; move the AAPL news widget beside it so it starts at "
         "column 20, row 0, keeping its size.",
         "Keeping its size, move the AAPL news widget up beside the price widget at column "
         "20, row 0. Do not move the price widget.",
     ]),
    ("estimates_fundamentals_msft",
     ("estimate_history", {"symbol": "MSFT"}, {"x": 0, "y": 0, "w": 24, "h": 12}),
     ("fundamental_metrics", {"symbol": "MSFT"},
      {"x": 0, "y": 12, "w": 16, "h": 8}, {"x": 24, "y": 0, "w": 16, "h": 8}),
     [
         "Move the MSFT fundamentals widget beside the estimates widget: it should start at "
         "column 24, row 0, keeping its size. Do not move the estimates widget.",
         "Do not move the estimates widget; move the MSFT fundamentals widget beside it so "
         "it starts at column 24, row 0, keeping its size.",
         "Keeping its size, move the MSFT fundamentals widget beside the estimates widget at "
         "column 24, row 0. Do not move the estimates widget.",
     ]),
    ("macro_pair",
     ("macro_timeseries", {"series": "DGS10"}, {"x": 0, "y": 0, "w": 20, "h": 10}),
     ("yield_curve", {}, {"x": 0, "y": 10, "w": 20, "h": 10},
      {"x": 20, "y": 0, "w": 20, "h": 10}),
     [
         "Move the yield curve widget beside the 10Y series widget: it should start at column "
         "20, row 0, keeping its size. Do not move the series widget.",
         "Do not move the series widget; move the yield curve widget beside the 10Y series "
         "widget so it starts at column 20, row 0, keeping its size.",
         "Keeping its size, move the yield curve widget beside the 10Y series widget at "
         "column 20, row 0. Do not move the series widget.",
     ]),
    ("portfolio_pair",
     ("holdings_table", {}, {"x": 0, "y": 0, "w": 24, "h": 12}),
     ("sector_exposure", {}, {"x": 0, "y": 12, "w": 16, "h": 10},
      {"x": 24, "y": 0, "w": 16, "h": 10}),
     [
         "Move the sector exposure widget beside the holdings widget: it should start at column "
         "24, row 0, keeping its size. Do not move the holdings widget.",
         "Do not move the holdings widget; move the sector exposure widget beside it so it "
         "starts at column 24, row 0, keeping its size.",
         "Keeping its size, move the sector exposure widget beside the holdings widget at "
         "column 24, row 0. Do not move the holdings widget.",
     ]),
]
LAYOUT_T1_ORIGINS = {"price_news_aapl": EQ, "estimates_fundamentals_msft": EQ,
                      "macro_pair": MACRO, "portfolio_pair": PF}
for slug, (wid_a, args_a, layout_a), (wid_b, args_b, seed_b, target_b), prompt_variants in LAYOUT_T1:
    origin = LAYOUT_T1_ORIGINS[slug]
    workflow, sub = wf(origin)
    add("layout", "r1", {
        "id": f"preserve_{slug}",
        "title": f"Move Without Disturbing: {slug.replace('_', ' ').title()}",
        "category_code": "L1", "capability": "layout-management", "workflow": workflow,
        "subdomain": sub, "tags": ["layout", "preservation"],
        "prompt": phrased(f"preserve_{slug}", prompt_variants),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Preserve Layout Task", [
            {"origin": origin, "widget_id": wid_a, "data_args": args_a,
             "layout": dict(layout_a)},
            {"origin": origin, "widget_id": wid_b, "data_args": args_b,
             "layout": dict(seed_b)},
        ]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "update_widget_layout"],
        "success": {
            "required_layouts": [
                {"widget_id": wid_a, **layout_a},
                {"widget_id": wid_b, **target_b},
            ],
            "layout": GRID, "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "update_widget_layout",
                                "args": {"widget_id": wid_b, **target_b}}],
    })

LAYOUT_T2 = [
    ("split_price_news_aapl", EQ,
     ("price_performance", {"symbol": "AAPL"}, {"x": 0, "y": 0, "w": 20, "h": 12}),
     ("latest_news", {"symbol": "AAPL", "limit": 5}, {"x": 20, "y": 0, "w": 20, "h": 12}),
     [
         "Arrange the AAPL widgets side by side: price on the left half and news on the right "
         "half, both 12 rows tall starting at row 0.",
         "Place the AAPL price widget on the left half and the AAPL news widget on the right "
         "half, side by side, both 12 rows tall starting at row 0.",
         "Set the AAPL widgets side by side with price on the left half and news on the "
         "right half; both should be 12 rows tall starting at row 0.",
     ]),
    ("stack_price_news_nvda", EQ,
     ("price_performance", {"symbol": "NVDA"}, {"x": 0, "y": 0, "w": 40, "h": 12}),
     ("latest_news", {"symbol": "NVDA", "limit": 5}, {"x": 0, "y": 12, "w": 40, "h": 10}),
     [
         "Stack the NVDA widgets full-width: price on top (rows 0-12, 40 columns) and news "
         "below it (10 rows tall starting at row 12, 40 columns).",
         "Arrange the NVDA widgets full-width with price on top (rows 0-12, 40 columns) and "
         "news below it (10 rows tall starting at row 12, 40 columns).",
         "Put the NVDA price widget full-width on top (rows 0-12, 40 columns), with NVDA "
         "news full-width below it (10 rows tall starting at row 12, 40 columns).",
     ]),
    ("split_macro", MACRO,
     ("macro_timeseries", {"series": "DGS10"}, {"x": 0, "y": 0, "w": 20, "h": 10}),
     ("yield_curve", {}, {"x": 20, "y": 0, "w": 20, "h": 10}),
     [
         "Arrange the macro widgets side by side: the 10Y series on the left half and the yield "
         "curve on the right half, both 10 rows tall starting at row 0.",
         "Place the 10Y series macro widget on the left half and the yield curve on the right "
         "half, side by side, both 10 rows tall starting at row 0.",
         "Set the macro widgets side by side with the 10Y series on the left half and the "
         "yield curve on the right half; both should be 10 rows tall starting at row 0.",
     ]),
    ("split_portfolio", PF,
     ("holdings_table", {}, {"x": 0, "y": 0, "w": 24, "h": 12}),
     ("sector_exposure", {}, {"x": 24, "y": 0, "w": 16, "h": 12}),
     [
         "Arrange the portfolio widgets: holdings on the left with width 24 and sector exposure "
         "to its right with width 16, both 12 rows tall starting at row 0.",
         "Place holdings on the left with width 24 and sector exposure to its right with "
         "width 16; both portfolio widgets should be 12 rows tall starting at row 0.",
         "Set the portfolio layout with holdings left at width 24 and sector exposure right "
         "at width 16, both 12 rows tall starting at row 0.",
     ]),
]
for slug, origin, (wid_a, args_a, target_a), (wid_b, args_b, target_b), prompt_variants in LAYOUT_T2:
    workflow, sub = wf(origin)
    add("layout", "r2", {
        "id": f"arrange_{slug}",
        "title": f"Arrange: {slug.replace('_', ' ').title()}",
        "category_code": "L1", "capability": "layout-management", "workflow": workflow,
        "subdomain": sub, "tags": ["layout", "multi-widget"],
        "prompt": phrased(f"arrange_{slug}", prompt_variants),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Arrangement Task", [
            {"origin": origin, "widget_id": wid_a, "data_args": args_a,
             "layout": {"x": 0, "y": 0, "w": 18, "h": 9}},
            {"origin": origin, "widget_id": wid_b, "data_args": args_b,
             "layout": {"x": 0, "y": 9, "w": 18, "h": 9}},
        ]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "update_widget_layout"],
        "success": {
            "required_layouts": [
                {"widget_id": wid_a, **target_a},
                {"widget_id": wid_b, **target_b},
            ],
            "layout": GRID, "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "update_widget_layout",
                                "args": {"widget_id": wid_a, **target_a}},
                               {"tool": "update_widget_layout",
                                "args": {"widget_id": wid_b, **target_b}}],
    })

LAYOUT_T3 = [
    ("overlap_price_news_aapl", EQ,
     ("price_performance", {"symbol": "AAPL"}, {"x": 0, "y": 0, "w": 20, "h": 12}),
     ("latest_news", {"symbol": "AAPL", "limit": 5}, {"x": 10, "y": 0, "w": 20, "h": 10},
      {"x": 20, "y": 0, "w": 20, "h": 10}),
     [
         "The AAPL price and news widgets overlap. Move the news widget to start at column 20 "
         "with its current size. Do not move the price widget.",
         "The AAPL news widget overlaps the price widget. Move the news widget to start at "
         "column 20 with its current size. Do not move the price widget.",
         "Do not move the AAPL price widget; resolve the overlap by moving the news widget "
         "to start at column 20 with its current size.",
     ]),
    ("overlap_estimates_fund_msft", EQ,
     ("estimate_history", {"symbol": "MSFT"}, {"x": 0, "y": 0, "w": 24, "h": 12}),
     ("fundamental_metrics", {"symbol": "MSFT"}, {"x": 20, "y": 0, "w": 16, "h": 8},
      {"x": 24, "y": 0, "w": 16, "h": 8}),
     [
         "The MSFT estimates and fundamentals widgets overlap. Move the fundamentals widget to "
         "start at column 24 with its current size. Do not move the estimates widget.",
         "The MSFT fundamentals widget overlaps the estimates widget. Move the fundamentals "
         "widget to start at column 24 with its current size. Do not move the estimates widget.",
         "Do not move the MSFT estimates widget; resolve the overlap by moving the "
         "fundamentals widget to start at column 24 with its current size.",
     ]),
    ("overlap_macro", MACRO,
     ("macro_timeseries", {"series": "DGS10"}, {"x": 0, "y": 0, "w": 20, "h": 10}),
     ("yield_curve", {}, {"x": 15, "y": 0, "w": 20, "h": 10},
      {"x": 20, "y": 0, "w": 20, "h": 10}),
     [
         "The 10Y series and yield curve widgets overlap. Move the yield curve widget to start "
         "at column 20 with its current size. Do not move the series widget.",
         "The yield curve widget overlaps the 10Y series widget. Move the yield curve widget "
         "to start at column 20 with its current size. Do not move the series widget.",
         "Do not move the 10Y series widget; resolve the overlap by moving the yield curve "
         "widget to start at column 20 with its current size.",
     ]),
    ("overlap_portfolio", PF,
     ("holdings_table", {}, {"x": 0, "y": 0, "w": 24, "h": 12}),
     ("sector_exposure", {}, {"x": 20, "y": 0, "w": 16, "h": 10},
      {"x": 24, "y": 0, "w": 16, "h": 10}),
     [
         "The holdings and sector exposure widgets overlap. Move the sector exposure widget to "
         "start at column 24 with its current size. Do not move the holdings widget.",
         "The sector exposure widget overlaps the holdings widget. Move the sector exposure "
         "widget to start at column 24 with its current size. Do not move the holdings widget.",
         "Do not move the holdings widget; resolve the overlap by moving the sector exposure "
         "widget to start at column 24 with its current size.",
     ]),
]
for slug, origin, (wid_a, args_a, layout_a), (wid_b, args_b, seed_b, target_b), prompt_variants in LAYOUT_T3:
    workflow, sub = wf(origin)
    add("layout", "r3", {
        "id": f"overlap_{slug}",
        "title": f"Repair Overlap: {slug.replace('_', ' ').title()}",
        "category_code": "L4", "capability": "workspace-repair", "workflow": workflow,
        "subdomain": sub, "tags": ["repair", "layout"],
        "prompt": phrased(f"overlap_{slug}", prompt_variants),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Overlap Repair", [
            {"origin": origin, "widget_id": wid_a, "data_args": args_a,
             "layout": dict(layout_a)},
            {"origin": origin, "widget_id": wid_b, "data_args": args_b,
             "layout": dict(seed_b)},
        ]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "update_widget_layout"],
        "success": {
            "required_layouts": [
                {"widget_id": wid_a, **layout_a},
                {"widget_id": wid_b, **target_b},
            ],
            "layout": GRID, "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "update_widget_layout",
                                "args": {"widget_id": wid_b, **target_b}}],
    })

LAYOUT_T4: list[
    tuple[str, str, list[tuple[str, dict[str, Any], dict[str, int]]], list[str]]
] = [
    ("grid_eq", EQ,
     [("price_performance", {"symbol": "AAPL"}, {"x": 0, "y": 0, "w": 20, "h": 12}),
      ("latest_news", {"symbol": "AAPL", "limit": 5}, {"x": 20, "y": 0, "w": 20, "h": 12}),
      ("estimate_history", {"symbol": "AAPL"}, {"x": 0, "y": 12, "w": 40, "h": 8})],
     [
         "Arrange the three AAPL widgets into a grid: price at columns 0-20 rows 0-12, news at "
         "columns 20-40 rows 0-12, and estimates full-width below them (40 columns, 8 rows, "
         "starting at row 12).",
         "Create a three-widget AAPL grid with price at columns 0-20 rows 0-12, news at "
         "columns 20-40 rows 0-12, and estimates full-width below them (40 columns, 8 rows, "
         "starting at row 12).",
         "Set the three AAPL widgets as a grid: price at columns 0-20 rows 0-12, news at "
         "columns 20-40 rows 0-12, and estimates full-width below them (40 columns, 8 rows, "
         "starting at row 12).",
     ]),
    ("grid_macro", MACRO,
     [("macro_timeseries", {"series": "DGS2"}, {"x": 0, "y": 0, "w": 20, "h": 10}),
      ("macro_timeseries", {"series": "DGS10"}, {"x": 20, "y": 0, "w": 20, "h": 10}),
      ("yield_curve", {}, {"x": 0, "y": 10, "w": 40, "h": 10})],
     [
         "Arrange the three macro widgets into a grid: the 2Y series at columns 0-20 rows 0-10, "
         "the 10Y series at columns 20-40 rows 0-10, and the yield curve full-width below them "
         "(40 columns, 10 rows, starting at row 10).",
         "Create a three-widget macro grid with the 2Y series at columns 0-20 rows 0-10, "
         "the 10Y series at columns 20-40 rows 0-10, and the yield curve full-width below "
         "them (40 columns, 10 rows, starting at row 10).",
         "Set the three macro widgets as a grid: the 2Y series at columns 0-20 rows 0-10, "
         "the 10Y series at columns 20-40 rows 0-10, and the yield curve full-width below "
         "them (40 columns, 10 rows, starting at row 10).",
     ]),
    ("grid_portfolio", PF,
     [("holdings_table", {}, {"x": 0, "y": 0, "w": 24, "h": 12}),
      ("sector_exposure", {}, {"x": 24, "y": 0, "w": 16, "h": 12}),
      ("risk_metrics", {}, {"x": 0, "y": 12, "w": 40, "h": 8})],
     [
         "Arrange the three portfolio widgets into a grid: holdings at columns 0-24 rows 0-12, "
         "sector exposure at columns 24-40 rows 0-12, and risk metrics full-width below them "
         "(40 columns, 8 rows, starting at row 12).",
         "Create a three-widget portfolio grid with holdings at columns 0-24 rows 0-12, "
         "sector exposure at columns 24-40 rows 0-12, and risk metrics full-width below them "
         "(40 columns, 8 rows, starting at row 12).",
         "Set the three portfolio widgets as a grid: holdings at columns 0-24 rows 0-12, "
         "sector exposure at columns 24-40 rows 0-12, and risk metrics full-width below them "
         "(40 columns, 8 rows, starting at row 12).",
     ]),
    ("grid_eq_mixed", EQ,
     [("price_performance", {"symbol": "MSFT"}, {"x": 0, "y": 0, "w": 40, "h": 10}),
      ("estimate_history", {"symbol": "MSFT"}, {"x": 0, "y": 10, "w": 20, "h": 10}),
      ("fundamental_metrics", {"symbol": "MSFT"}, {"x": 20, "y": 10, "w": 20, "h": 10})],
     [
         "Arrange the three MSFT widgets: price full-width on top (40 columns, 10 rows), then "
         "estimates at columns 0-20 and fundamentals at columns 20-40, both 10 rows starting at "
         "row 10.",
         "Create a three-widget MSFT layout with price full-width on top (40 columns, 10 rows), "
         "then estimates at columns 0-20 and fundamentals at columns 20-40, both 10 rows "
         "starting at row 10.",
         "Set the three MSFT widgets with price full-width on top (40 columns, 10 rows), then "
         "estimates at columns 0-20 and fundamentals at columns 20-40, both 10 rows starting "
         "at row 10.",
     ]),
]
for slug, origin, targets, prompt_variants in LAYOUT_T4:
    workflow, sub = wf(origin)
    uuids = [f"widget_{i + 1:03d}" for i in range(len(targets))]
    seeds = [
        {"origin": origin, "widget_id": wid, "data_args": args,
         "layout": {"x": 2 + i * 4, "y": 2 + i * 11, "w": 16, "h": 9}}
        for i, (wid, args, _) in enumerate(targets)
    ]
    add("layout", "r4", {
        "id": f"grid_{slug}",
        "title": f"Three-Widget Grid: {slug.replace('_', ' ').title()}",
        "category_code": "L1", "capability": "layout-management", "workflow": workflow,
        "subdomain": sub, "tags": ["layout", "multi-widget", "combo"],
        "prompt": phrased(f"grid_{slug}", prompt_variants),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Grid Task", seeds),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "update_widget_layout"],
        "success": {
            "required_layouts": [
                {"widget_uuid": uuids[i], **target}
                for i, (_, _, target) in enumerate(targets)
            ],
            "layout": GRID, "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap()] + [
            {"tool": "update_widget_layout",
             "args": {"widget_uuid": uuids[i], **target}}
            for i, (_, _, target) in enumerate(targets)
        ],
    })


# ===========================================================================
# Family NOTE — anchor: add_generative_widget
# ===========================================================================

NOTE_T0 = [
    ("standup", "Morning Standup",
     [
         "Add a note named Morning Standup saying the desk meeting moved to 9am and the risk "
         "review is at noon.",
         "Create a note named Morning Standup that says the desk meeting moved to 9am and the "
         "risk review is at noon.",
         "On the dashboard, add a note named Morning Standup stating that the desk meeting "
         "moved to 9am and the risk review is at noon.",
     ], ["9am", "noon"],
     "Desk meeting moved to 9am; risk review is at noon."),
    ("handover", "Desk Handover",
     [
         "Add a note named Desk Handover saying the EU book is flat and the US open checklist "
         "is complete.",
         "Create a note named Desk Handover that says the EU book is flat and the US open "
         "checklist is complete.",
         "On the dashboard, add a note named Desk Handover stating that the EU book is flat "
         "and the US open checklist is complete.",
     ], ["EU book", "checklist"],
     "EU book is flat; the US open checklist is complete."),
    ("reminder", "Compliance Reminder",
     [
         "Add a note named Compliance Reminder saying attestations are due Friday and trading "
         "in restricted names is blocked.",
         "Create a note named Compliance Reminder that says attestations are due Friday and "
         "trading in restricted names is blocked.",
         "On the dashboard, add a note named Compliance Reminder stating that attestations "
         "are due Friday and trading in restricted names is blocked.",
     ], ["attestations", "restricted"],
     "Attestations due Friday; trading in restricted names is blocked."),
    ("outage", "Vendor Outage",
     [
         "Add a note named Vendor Outage saying the FactSet feed is degraded and fallback "
         "pricing is active.",
         "Create a note named Vendor Outage that says the FactSet feed is degraded and "
         "fallback pricing is active.",
         "On the dashboard, add a note named Vendor Outage stating that the FactSet feed is "
         "degraded and fallback pricing is active.",
     ], ["FactSet", "fallback"],
     "FactSet feed degraded; fallback pricing is active."),
]
for slug, name, prompt_variants, facts, text in NOTE_T0:
    add("note", "r0", {
        "id": f"{slug}",
        "title": name,
        "category_code": "L1", "capability": "workspace-inspection",
        "workflow": "portfolio-morning-review", "subdomain": "portfolio-management",
        "tags": ["note"],
        "prompt": phrased(f"{slug}", prompt_variants),
        "fixtures": {"backends": [{"name": "equities"}]},
        "initial_state": seeded("Notes Board", []),
        "allowed_tools": ["get_workspace_snapshot", "add_generative_widget"],
        "success": {
            "required_generated_widgets": [
                {"widget_type": "note", "name_contains": name, "data_contains": facts}],
            "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(), note_call(name, text)],
    })

NOTE_T1 = [
    ("close_aapl", EQ, "price_performance", {"symbol": "AAPL"},
     [
         "Review the existing AAPL price widget and add a note with the latest close from the "
         "data.",
         "Use the existing AAPL price widget data to add a note with the latest close from the "
         "data.",
         "Add a note with the latest close from the data after reviewing the existing AAPL "
         "price widget.",
     ], ["AAPL", CLOSES["AAPL"]], f"Latest AAPL close is {CLOSES['AAPL']}."),
    ("close_msft", EQ, "price_performance", {"symbol": "MSFT"},
     [
         "Review the existing MSFT price widget and add a note with the latest close from the "
         "data.",
         "Use the existing MSFT price widget data to add a note with the latest close from the "
         "data.",
         "Add a note with the latest close from the data after reviewing the existing MSFT "
         "price widget.",
     ], ["MSFT", CLOSES["MSFT"]], f"Latest MSFT close is {CLOSES['MSFT']}."),
    ("macro_10y", MACRO, "macro_timeseries", {"series": "DGS10"},
     [
         "Review the existing 10Y series widget and add a note with the series id and its "
         "latest value from the data.",
         "Use the existing 10Y series widget data to add a note with the series id and its "
         "latest value from the data.",
         "Add a note with the series id and its latest value from the data after reviewing "
         "the existing 10Y series widget.",
     ], ["DGS10", MACRO_LATEST["DGS10"]],
     f"Latest DGS10 value is {MACRO_LATEST['DGS10']}."),
    ("top_holding", PF, "holdings_table", {},
     [
         "Review the existing holdings widget and add a note naming the largest position and "
         "its exact weight from the data.",
         "Use the existing holdings widget data to add a note naming the largest position and "
         "its exact weight from the data.",
         "Add a note naming the largest position and its exact weight from the data after "
         "reviewing the existing holdings widget.",
     ], ["MSFT", "0.34"],
     "Largest position: MSFT at 0.34."),
]
for slug, origin, widget_id, data_args, prompt_variants, facts, text in NOTE_T1:
    workflow, sub = wf(origin)
    add("note", "r1", {
        "id": f"fact_{slug}",
        "title": f"Grounded Note: {slug.replace('_', ' ').title()}",
        "category_code": "L0", "capability": "workspace-inspection", "workflow": workflow,
        "subdomain": sub, "tags": ["note", "read-only"],
        "prompt": phrased(f"fact_{slug}", prompt_variants),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Existing Review",
                                 [{"origin": origin, "widget_id": widget_id,
                                   "data_args": data_args,
                                   "layout": {"x": 0, "y": 0, "w": 20, "h": 12}}]),
        "allowed_tools": ["get_workspace_snapshot", "get_widget_data",
                           "add_generative_widget"],
        "success": {
            "required_widgets": [{"origin": origin, "widget_id": widget_id,
                                    "data_args": data_args, "min_count": 1}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": facts}],
            "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "get_widget_data",
                                "args": {"origin": origin, "widget_id": widget_id,
                                          "data_args": data_args}},
                               note_call("Answer Note", text)],
    })

NOTE_T2 = [
    ("estimates_aapl", "estimate_history", {"symbol": "AAPL"},
     [
         "Review the existing AAPL estimates widget and add a note on the overview tab with the "
         "2026Q1 EPS estimate and the revenue estimate from the data.",
         "Use the existing AAPL estimates widget data to add a note on the overview tab with "
         "the 2026Q1 EPS estimate and the revenue estimate from the data.",
         "Add a note on the overview tab with the 2026Q1 EPS estimate and the revenue estimate "
         "from the data after reviewing the existing AAPL estimates widget.",
     ],
     ["AAPL", EPS_Q1["AAPL"], REV_Q1["AAPL"]],
     f"AAPL 2026Q1: EPS {EPS_Q1['AAPL']}, revenue {REV_Q1['AAPL']}B."),
    ("estimates_msft", "estimate_history", {"symbol": "MSFT"},
     [
         "Review the existing MSFT estimates widget and add a note on the overview tab with the "
         "2026Q1 EPS estimate and the revenue estimate from the data.",
         "Use the existing MSFT estimates widget data to add a note on the overview tab with "
         "the 2026Q1 EPS estimate and the revenue estimate from the data.",
         "Add a note on the overview tab with the 2026Q1 EPS estimate and the revenue estimate "
         "from the data after reviewing the existing MSFT estimates widget.",
     ],
     ["MSFT", EPS_Q1["MSFT"], REV_Q1["MSFT"]],
     f"MSFT 2026Q1: EPS {EPS_Q1['MSFT']}, revenue {REV_Q1['MSFT']}B."),
    ("fundamentals_nvda", "fundamental_metrics", {"symbol": "NVDA"},
     [
         "Review the existing NVDA fundamentals widget and add a note on the overview tab with "
         "the gross margin and the buyback yield from the data.",
         "Use the existing NVDA fundamentals widget data to add a note on the overview tab "
         "with the gross margin and the buyback yield from the data.",
         "Add a note on the overview tab with the gross margin and the buyback yield from the "
         "data after reviewing the existing NVDA fundamentals widget.",
     ],
     ["NVDA", MARGIN["NVDA"], "0.004"],
     f"NVDA: gross margin {MARGIN['NVDA']}, buyback yield 0.004."),
    ("fundamentals_aapl", "fundamental_metrics", {"symbol": "AAPL"},
     [
         "Review the existing AAPL fundamentals widget and add a note on the overview tab with "
         "the gross margin and the net cash from the data.",
         "Use the existing AAPL fundamentals widget data to add a note on the overview tab "
         "with the gross margin and the net cash from the data.",
         "Add a note on the overview tab with the gross margin and the net cash from the data "
         "after reviewing the existing AAPL fundamentals widget.",
     ],
     ["AAPL", MARGIN["AAPL"], "54.0"],
     f"AAPL: gross margin {MARGIN['AAPL']}, net cash 54.0B."),
]
for slug, widget_id, data_args, prompt_variants, facts, text in NOTE_T2:
    add("note", "r2", {
        "id": f"twofacts_{slug}",
        "title": f"Two-Fact Note: {slug.replace('_', ' ').title()}",
        "category_code": "L0", "capability": "workspace-inspection",
        "workflow": "equity-tearsheet", "subdomain": "equity-research",
        "tags": ["note", "read-only"],
        "prompt": phrased(f"twofacts_{slug}", prompt_variants),
        "fixtures": {"backends": [{"name": "equities"}]},
        "initial_state": seeded("Existing Review",
                                 [{"origin": EQ, "widget_id": widget_id,
                                   "data_args": data_args, "tab_id": "overview",
                                   "layout": {"x": 0, "y": 0, "w": 20, "h": 12}}],
                                 tabs=[{"id": "overview", "name": "Overview"}]),
        "allowed_tools": ["get_workspace_snapshot", "get_widget_data",
                           "add_generative_widget"],
        "success": {
            "required_tabs": ["overview"],
            "required_widgets": [{"origin": EQ, "widget_id": widget_id,
                                    "data_args": data_args, "tab_id": "overview",
                                    "min_count": 1}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": facts, "tab_id": "overview"}],
            "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "get_widget_data",
                                "args": {"origin": EQ, "widget_id": widget_id,
                                          "data_args": data_args}},
                               note_call("Answer Note", text)],
    })

NOTE_T3: list[
    tuple[str, str, list[tuple[str, dict[str, Any]]], list[str], list[str], str]
] = [
    ("aapl_msft_closes", EQ,
     [("price_performance", {"symbol": "AAPL"}), ("price_performance", {"symbol": "MSFT"})],
     [
         "Compare the existing AAPL and MSFT price widgets and add a note with each latest "
         "close from the data.",
         "Use the existing AAPL and MSFT price widget data to add a note with each latest "
         "close from the data.",
         "Add a note with each latest close from the data after comparing the existing AAPL "
         "and MSFT price widgets.",
     ],
     ["AAPL", CLOSES["AAPL"], "MSFT", CLOSES["MSFT"]],
     f"Latest closes: AAPL {CLOSES['AAPL']}, MSFT {CLOSES['MSFT']}."),
    ("nvda_close_eps", EQ,
     [("price_performance", {"symbol": "NVDA"}), ("estimate_history", {"symbol": "NVDA"})],
     [
         "Review the NVDA price and estimates widgets and add a note with the latest close and "
         "the 2026Q1 EPS estimate from the data.",
         "Use the NVDA price and estimates widget data to add a note with the latest close "
         "and the 2026Q1 EPS estimate from the data.",
         "Add a note with the latest close and the 2026Q1 EPS estimate from the data after "
         "reviewing the NVDA price and estimates widgets.",
     ],
     ["NVDA", CLOSES["NVDA"], EPS_Q1["NVDA"]],
     f"NVDA: close {CLOSES['NVDA']}; 2026Q1 EPS {EPS_Q1['NVDA']}."),
    ("fed_vs_10y", MACRO,
     [("macro_timeseries", {"series": "FEDFUNDS"}),
      ("macro_timeseries", {"series": "DGS10"})],
     [
         "Review the Fed Funds and 10Y Treasury widgets and add a note with both latest values "
         "from the data.",
         "Use the Fed Funds and 10Y Treasury widget data to add a note with both latest values "
         "from the data.",
         "Add a note with both latest values from the data after reviewing the Fed Funds and "
         "10Y Treasury widgets.",
     ],
     ["FEDFUNDS", MACRO_LATEST["FEDFUNDS"], "DGS10", MACRO_LATEST["DGS10"]],
     f"FEDFUNDS latest {MACRO_LATEST['FEDFUNDS']}; DGS10 latest {MACRO_LATEST['DGS10']}."),
    ("holdings_beta", PF,
     [("holdings_table", {}), ("risk_metrics", {})],
     [
         "Review the holdings and risk metrics widgets and add a note with the largest position "
         "weight and the portfolio beta from the data.",
         "Use the holdings and risk metrics widget data to add a note with the largest "
         "position weight and the portfolio beta from the data.",
         "Add a note with the largest position weight and the portfolio beta from the data "
         "after reviewing the holdings and risk metrics widgets.",
     ],
     ["MSFT", "0.34", "1.18"],
     "MSFT largest at 0.34; portfolio beta 1.18."),
]
for slug, origin, note_widgets, prompt_variants, facts, text in NOTE_T3:
    workflow, sub = wf(origin)
    seeds = [
        {"origin": origin, "widget_id": wid, "data_args": args,
         "layout": {"x": (i % 2) * 20, "y": (i // 2) * 12, "w": 20, "h": 10}}
        for i, (wid, args) in enumerate(note_widgets)
    ]
    oracle = [snap()]
    for wid, args in note_widgets:
        oracle.append({"tool": "get_widget_data",
                        "args": {"origin": origin, "widget_id": wid, "data_args": args}})
    oracle.append(note_call("Answer Note", text))
    add("note", "r3", {
        "id": f"synthesis_{slug}",
        "title": f"Synthesis Note: {slug.replace('_', ' ').title()}",
        "category_code": "L0", "capability": "workspace-inspection", "workflow": workflow,
        "subdomain": sub, "tags": ["note", "read-only", "multi-widget"],
        "prompt": phrased(f"synthesis_{slug}", prompt_variants),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Existing Review", seeds),
        "allowed_tools": ["get_workspace_snapshot", "get_widget_data",
                           "add_generative_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": wid, "data_args": args, "min_count": 1}
                for wid, args in note_widgets],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": facts}],
            "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": oracle,
    })

NOTE_T4 = [
    ("exposure_cpi",
     [(PF, "sector_exposure", {}), (MACRO, "macro_timeseries", {"series": "CPIAUCSL"})],
     [
         "Review the sector exposure and CPI widgets and add a note with the largest sector "
         "weight and the latest CPI value from the data.",
         "Use the sector exposure and CPI widget data to add a note with the largest sector "
         "weight and the latest CPI value from the data.",
         "Add a note with the largest sector weight and the latest CPI value from the data "
         "after reviewing the sector exposure and CPI widgets.",
     ],
     ["Technology", "0.86", MACRO_LATEST["CPIAUCSL"]],
     f"Technology exposure 0.86; latest CPI {MACRO_LATEST['CPIAUCSL']}."),
    ("aapl_vs_rates",
     [(EQ, "price_performance", {"symbol": "AAPL"}),
      (MACRO, "macro_timeseries", {"series": "DGS10"})],
     [
         "Review the AAPL price and 10Y Treasury widgets and add a note with the latest close "
         "and the latest 10Y value from the data.",
         "Use the AAPL price and 10Y Treasury widget data to add a note with the latest close "
         "and the latest 10Y value from the data.",
         "Add a note with the latest close and the latest 10Y value from the data after "
         "reviewing the AAPL price and 10Y Treasury widgets.",
     ],
     ["AAPL", CLOSES["AAPL"], MACRO_LATEST["DGS10"]],
     f"AAPL close {CLOSES['AAPL']} against the 10Y at {MACRO_LATEST['DGS10']}."),
    ("book_vs_fed",
     [(PF, "risk_metrics", {}), (MACRO, "macro_timeseries", {"series": "FEDFUNDS"})],
     [
         "Review the risk metrics and Fed Funds widgets and add a note with the portfolio beta "
         "and the latest FEDFUNDS value from the data.",
         "Use the risk metrics and Fed Funds widget data to add a note with the portfolio beta "
         "and the latest FEDFUNDS value from the data.",
         "Add a note with the portfolio beta and the latest FEDFUNDS value from the data after "
         "reviewing the risk metrics and Fed Funds widgets.",
     ],
     ["1.18", MACRO_LATEST["FEDFUNDS"]],
     f"Portfolio beta 1.18 with Fed Funds at {MACRO_LATEST['FEDFUNDS']}."),
    ("msft_vs_curve",
     [(EQ, "fundamental_metrics", {"symbol": "MSFT"}), (MACRO, "yield_curve", {})],
     [
         "Review the MSFT fundamentals and yield curve widgets and add a note with the gross "
         "margin and the 30Y yield from the data.",
         "Use the MSFT fundamentals and yield curve widget data to add a note with the gross "
         "margin and the 30Y yield from the data.",
         "Add a note with the gross margin and the 30Y yield from the data after reviewing "
         "the MSFT fundamentals and yield curve widgets.",
     ],
     ["MSFT", MARGIN["MSFT"], "4.48"],
     f"MSFT gross margin {MARGIN['MSFT']}; 30Y yield 4.48."),
]
for slug, widgets, prompt_variants, facts, text in NOTE_T4:
    origins = sorted({o for o, _, _ in widgets})
    seeds = [
        {"origin": o, "widget_id": wid, "data_args": args,
         "layout": {"x": (i % 2) * 20, "y": (i // 2) * 12, "w": 20, "h": 10}}
        for i, (o, wid, args) in enumerate(widgets)
    ]
    oracle = [snap()]
    for o, wid, args in widgets:
        oracle.append({"tool": "get_widget_data",
                        "args": {"origin": o, "widget_id": wid, "data_args": args}})
    oracle.append(note_call("Answer Note", text))
    add("note", "r4", {
        "id": f"crossbackend_{slug}",
        "title": f"Cross-Backend Note: {slug.replace('_', ' ').title()}",
        "category_code": "L0", "capability": "workspace-inspection",
        "workflow": "portfolio-risk-review", "subdomain": "portfolio-management",
        "tags": ["note", "read-only", "cross-backend"],
        "prompt": phrased(f"crossbackend_{slug}", prompt_variants),
        "fixtures": {"backends": [{"name": fixture_for(o)} for o in origins]},
        "initial_state": seeded("Existing Review", seeds),
        "allowed_tools": ["get_workspace_snapshot", "get_widget_data",
                           "add_generative_widget"],
        "success": {
            "required_widgets": [
                {"origin": o, "widget_id": wid, "data_args": args, "min_count": 1}
                for o, wid, args in widgets],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": facts}],
            "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": oracle,
    })


# ===========================================================================
# Family READ — anchor: get_widget_data
# ===========================================================================

STK_ARGS = {"fund": "Flagship Long/Short", "period": "YTD"}


def read_task(level: str, slug: str, widgets: list[str], facts_mode: str) -> None:
    """facts_mode: 'id' (cite widget ids) or 'value' (cite exact baked fixture facts)."""
    primary = widgets[0]
    workflow, sub = stark_family(primary)
    seeds = [
        {"origin": STK, "widget_id": wid, "data_args": dict(STK_ARGS), "tab_id": "main",
         "layout": {"x": (i % 2) * 20, "y": 2 + (i // 2) * 12, "w": 20, "h": 10}}
        for i, wid in enumerate(widgets)
    ]
    note_facts: list[str] = []
    result_checks = []
    value_facts: dict[str, tuple[str, str]] = {}
    for wid in widgets:
        if facts_mode == "id":
            note_facts.append(wid)
            result_checks.append({"tool": "get_widget_data", "data_contains": [wid]})
        else:
            field, value = stark_fact(wid)
            value_facts[wid] = (field, value)
            note_facts += [wid, field, value]
            result_checks.append(
                {"tool": "get_widget_data", "data_contains": [wid, field, value]}
            )
    if facts_mode == "id":
        note_facts.append("data")
    oracle = [snap()]
    for i, wid in enumerate(widgets):
        oracle.append({"tool": "get_widget_data",
                        "args": {"origin": STK, "widget_id": wid,
                                  "widget_uuid": f"widget_{i + 1:03d}",
                                  "data_args": dict(STK_ARGS)}})
    if facts_mode == "id":
        text = "Reviewed the data returned by " + " and ".join(widgets) + "."
    else:
        text = "; ".join(
            f"{wid} {value_facts[wid][0]} is {value_facts[wid][1]}"
            for wid in widgets
        ) + "."
    oracle.append(note_call("Data Note", text))
    names = " and ".join(STARK["widgets"][wid]["name"] for wid in widgets)
    if facts_mode == "id":
        ask = ("then add a short note that cites "
               + (f"{widgets[0]}" if len(widgets) == 1 else " and ".join(widgets))
               + " and says you reviewed the data.")
    else:
        targets = " and ".join(
            f"{value_facts[wid][0]} for {wid}" for wid in widgets
        )
        ask = (
            f"find the exact {targets}, then add a note that cites each widget id, "
            "the field name, and the exact value."
        )
    add("read", level, {
        "id": slug,
        "title": f"Read Data: {names}",
        "category_code": "L1", "capability": "data-reading", "workflow": workflow,
        "subdomain": sub, "tags": ["data-reading", "stark"],
        "prompt": phrased(slug, [
            (f"Use get_widget_data on the Bench Stark Enterprise "
             f"{names} widget{'s' if len(widgets) > 1 else ''}, {ask}"),
            (f"On the Bench Stark Enterprise {names} "
             f"widget{'s' if len(widgets) > 1 else ''}, use get_widget_data, {ask}"),
            (f"Use get_widget_data for the Bench Stark Enterprise {names} "
             f"widget{'s' if len(widgets) > 1 else ''}; {ask}"),
        ]),
        "fixtures": {"backends": [{"name": "stark-enterprise"}]},
        "initial_state": seeded("Data Review", seeds,
                                 tabs=[{"id": "main", "name": "Main"}]),
        "allowed_tools": ["get_workspace_snapshot", "get_widget_data", "read_widget",
                           "add_generative_widget"],
        "success": {
            "required_tool_calls": [
                {"tool": "get_widget_data",
                 "args_contains": {"origin": STK, "widget_id": wid}}
                for wid in widgets],
            "required_tool_results": result_checks,
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": note_facts}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": oracle,
    })


for slug, wid in [
    ("limits", "risk_exposure_monitor_limits_limit_utilization"),
    ("attribution", "portfolio_command_center_attribution_attribution_summary"),
    ("order_status", "execution_desk_blotter_order_status_metrics"),
    ("latency", "vendor_dataset_monitor_slas_latency_by_feed"),
]:
    read_task("r0", slug, [wid], "id")

for slug, wid in [
    ("alert_trend", "compliance_surveillance_hub_alerts_alert_trend"),
    ("pipeline", "client_360_flows_pipeline_by_stage"),
    ("strategy_health", "strategy_health_monitor_performance_strategy_health_metrics"),
    ("break_aging", "fund_operations_control_tower_recons_break_aging"),
]:
    read_task("r1", slug, [wid], "id")

for slug, wid in [
    ("var_trend", "risk_exposure_monitor_dashboard_var_trend"),
    ("issuer_conc", "portfolio_command_center_holdings_issuer_concentration"),
    ("broker_scorecard", "execution_desk_fills_broker_scorecard"),
    ("sla_metrics", "vendor_dataset_monitor_vendors_sla_metrics"),
]:
    read_task("r2", slug, [wid], "value")

for slug, wids in [
    ("risk_pair", ["risk_exposure_monitor_dashboard_var_trend",
                     "risk_exposure_monitor_dashboard_drawdown"]),
    ("exec_pair", ["execution_desk_fills_fills_table",
                     "execution_desk_fills_broker_scorecard"]),
    ("vendor_pair", ["vendor_dataset_monitor_slas_vendor_sla_status",
                       "vendor_dataset_monitor_slas_latency_by_feed"]),
    ("client_pair", ["client_360_client_book_client_accounts",
                       "client_360_client_book_relationship_metrics"]),
]:
    read_task("r3", slug, wids, "id")

for slug, wids in [
    ("risk_values", ["risk_exposure_monitor_dashboard_risk_snapshot",
                       "risk_exposure_monitor_limits_limit_utilization"]),
    ("pm_values", ["portfolio_command_center_overview_portfolio_snapshot",
                     "portfolio_command_center_overview_top_alerts"]),
    ("quant_values", ["quant_research_backtest_lab_signals_signal_metrics",
                        "quant_research_backtest_lab_backtest_backtest_performance"]),
    ("stress_values", ["stress_liquidity_lab_liquidity_days_to_liquidate",
                         "stress_liquidity_lab_stress_tests_risk_snapshot"]),
]:
    read_task("r4", slug, wids, "value")


# ===========================================================================
# Family APPS — anchor: manage_apps
# ===========================================================================

APPS_BY_TEMPLATE = {app["template_id"]: app for app in STARK["apps"]}


def app_checks(app: dict, count: int = 2) -> tuple[list[str], list[tuple[str, str]]]:
    tabs, widgets = [], []
    for tab_id in sorted(app["tabs"]):
        if tab_id == "overview":
            continue
        layout = app["tabs"][tab_id].get("layout", [])
        if layout:
            tabs.append(tab_id)
            widgets.append((layout[0]["i"], tab_id))
        if len(widgets) == count:
            break
    return tabs, widgets


def instantiate_oracle(app: dict, dash_name: str) -> list[dict]:
    return [
        {"tool": "manage_backends", "args": {"operation": "list"}},
        {"tool": "manage_apps",
         "args": {"operation": "instantiate", "backend_id": "backend_001",
                   "app_name": app["name"], "dashboard_name": dash_name,
                   "activate": True}},
    ]


APPS_T0 = [
    ("risk-exposure-monitor", "Risk Watch"),
    ("execution-desk", "AM Execution Desk"),
    ("client-360", "Client Review Workspace"),
    ("vendor-dataset-monitor", "Data Vendor Watch"),
]
for template_id, dash_name in APPS_T0:
    app = APPS_BY_TEMPLATE[template_id]
    workflow, sub = stark_family(template_id)
    add("apps", "r0", {
        "id": f"{template_id.replace('-', '_')}",
        "title": f"Instantiate {app['name']}",
        "category_code": "L3", "capability": "app-instantiation", "workflow": workflow,
        "subdomain": sub, "tags": ["apps", "stark"],
        "prompt": phrased(f"{template_id.replace('-', '_')}", [
            (f"Instantiate the {app['name']} app from the Bench Stark Enterprise "
             f"backend as a new dashboard named {dash_name}."),
            (f"From the Bench Stark Enterprise backend, instantiate the {app['name']} app "
             f"as a new dashboard named {dash_name}."),
            (f"Create a new dashboard named {dash_name} by instantiating the {app['name']} "
             "app from the Bench Stark Enterprise backend."),
        ]),
        "fixtures": {"backends": [{"name": "stark-enterprise"}]},
        "initial_state": {},
        "allowed_tools": ["get_workspace_snapshot", "manage_backends", "manage_apps"],
        "success": {
            "required_dashboard_name_contains": dash_name,
            "required_tool_calls": [
                {"tool": "manage_apps", "args_contains": {"operation": "instantiate"}}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": instantiate_oracle(app, dash_name),
    })

APPS_T1 = [
    ("compliance-surveillance-hub", "Daily Surveillance Board"),
    ("equity-research-workbench", "Coverage Workbench"),
    ("earnings-estimates-monitor", "Earnings Season Monitor"),
    ("executive-investment-dashboard", "Executive Morning Brief"),
]
for template_id, dash_name in APPS_T1:
    app = APPS_BY_TEMPLATE[template_id]
    workflow, sub = stark_family(template_id)
    check_tabs, check_widgets = app_checks(app)
    add("apps", "r1", {
        "id": f"{template_id.replace('-', '_')}",
        "title": f"Instantiate {app['name']} (Checked)",
        "category_code": "L3", "capability": "app-instantiation", "workflow": workflow,
        "subdomain": sub, "tags": ["apps", "stark"],
        "prompt": phrased(f"{template_id.replace('-', '_')}", [
            (f"Instantiate the {app['name']} app from the Bench Stark Enterprise "
             f"backend as a new dashboard named {dash_name}."),
            (f"From the Bench Stark Enterprise backend, instantiate the {app['name']} app "
             f"as a new dashboard named {dash_name}."),
            (f"Create a new dashboard named {dash_name} by instantiating the {app['name']} "
             "app from the Bench Stark Enterprise backend."),
        ]),
        "fixtures": {"backends": [{"name": "stark-enterprise"}]},
        "initial_state": {},
        "allowed_tools": ["get_workspace_snapshot", "manage_backends", "manage_apps",
                           "navigate_workspace"],
        "success": {
            "required_dashboard_name_contains": dash_name,
            "required_tabs": ["overview"] + check_tabs,
            "required_widgets": [
                {"origin": STK, "widget_id": wid, "tab_id": tab, "min_count": 1}
                for wid, tab in check_widgets],
            "layout": {"within_grid": True, "grid_width": 40},
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": instantiate_oracle(app, dash_name),
    })

APPS_T2 = [
    ("stress-liquidity-lab", "Quarterly Stress Review", "sign_off",
     ["sign off", "residual risk"], "Sign off tracker reviewed; residual risk actions open."),
    ("quant-research-backtest-lab", "Signal Research Lab", "signals",
     ["signal", "decay"], "Signal leaderboard reviewed; watch signal decay."),
    ("nav-fees-close-dashboard", "Monthly Close Control", "close",
     ["close checklist", "exceptions"], "Close checklist in progress; NAV exceptions open."),
    ("reporting-factsheet-studio", "Factsheet Control", "factsheets",
     ["factsheet", "distribution"], "Factsheet preview done; distribution status pending."),
]
for template_id, dash_name, note_tab, note_facts, note_text in APPS_T2:
    app = APPS_BY_TEMPLATE[template_id]
    workflow, sub = stark_family(template_id)
    check_tabs, check_widgets = app_checks(app)
    if note_tab not in check_tabs:
        check_tabs = sorted(set(check_tabs + [note_tab]))
    add("apps", "r2", {
        "id": f"note_{template_id.replace('-', '_')}",
        "title": f"Instantiate {app['name']} And Brief",
        "category_code": "L3", "capability": "app-instantiation", "workflow": workflow,
        "subdomain": sub, "tags": ["apps", "stark", "note"],
        "prompt": phrased(f"note_{template_id.replace('-', '_')}", [
            (f"Instantiate the {app['name']} app from the Bench Stark Enterprise "
             f"backend as a new dashboard named {dash_name}, then add a note on the "
             f"{note_tab.replace('_', ' ').title()} tab mentioning {note_facts[0]} "
             f"and {note_facts[1]}."),
            (f"From the Bench Stark Enterprise backend, instantiate the {app['name']} app "
             f"as a new dashboard named {dash_name}, then add a note on the "
             f"{note_tab.replace('_', ' ').title()} tab mentioning {note_facts[0]} and "
             f"{note_facts[1]}."),
            (f"Create a new dashboard named {dash_name} by instantiating the {app['name']} "
             "app from the Bench Stark Enterprise backend, then add a note on the "
             f"{note_tab.replace('_', ' ').title()} tab mentioning {note_facts[0]} and "
             f"{note_facts[1]}."),
        ]),
        "fixtures": {"backends": [{"name": "stark-enterprise"}]},
        "initial_state": {},
        "allowed_tools": ["get_workspace_snapshot", "manage_backends", "manage_apps",
                           "navigate_workspace", "add_generative_widget"],
        "success": {
            "required_dashboard_name_contains": dash_name,
            "required_tabs": ["overview"] + check_tabs,
            "required_widgets": [
                {"origin": STK, "widget_id": wid, "tab_id": tab, "min_count": 1}
                for wid, tab in check_widgets],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": note_facts, "tab_id": note_tab}],
            "layout": {"within_grid": True, "grid_width": 40},
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": instantiate_oracle(app, dash_name) + [
            {"tool": "navigate_workspace", "args": {"operation": "tab", "tab_id": note_tab}},
            note_call("Brief Note", note_text)],
    })

APPS_T3 = [
    ("portfolio-command-center", "PM Command Post", "holdings",
     "portfolio_command_center_holdings_sector_exposure"),
    ("rebalance-scenario-lab", "Rebalance Studio", "drift",
     "rebalance_scenario_lab_drift_drift_by_sleeve"),
    ("strategy-health-monitor", "Strategy Health Desk", "watchlist",
     "strategy_health_monitor_watchlist_catalyst_calendar"),
    ("fund-operations-control-tower", "Ops Control Room", "recons",
     "fund_operations_control_tower_recons_break_aging"),
]
for template_id, dash_name, target_tab, extra_widget in APPS_T3:
    app = APPS_BY_TEMPLATE[template_id]
    workflow, sub = stark_family(template_id)
    check_tabs, check_widgets = app_checks(app)
    if target_tab not in check_tabs:
        check_tabs = sorted(set(check_tabs + [target_tab]))
    add("apps", "r3", {
        "id": f"extend_{template_id.replace('-', '_')}",
        "title": f"Instantiate And Extend {app['name']}",
        "category_code": "L3", "capability": "app-instantiation", "workflow": workflow,
        "subdomain": sub, "tags": ["apps", "stark", "widget-creation"],
        "prompt": phrased(f"extend_{template_id.replace('-', '_')}", [
            (f"Instantiate the {app['name']} app from the Bench Stark Enterprise "
             f"backend as a new dashboard named {dash_name}. Then add the "
             f"{STARK['widgets'][extra_widget]['name']} widget (id {extra_widget}) to "
             f"the {target_tab.replace('_', ' ').title()} tab of the new dashboard."),
            (f"From the Bench Stark Enterprise backend, instantiate the {app['name']} app "
             f"as a new dashboard named {dash_name}. Then add the "
             f"{STARK['widgets'][extra_widget]['name']} widget (id {extra_widget}) to "
             f"the {target_tab.replace('_', ' ').title()} tab of the new dashboard."),
            (f"Create a new dashboard named {dash_name} by instantiating the {app['name']} "
             "app from the Bench Stark Enterprise backend. Then add the "
             f"{STARK['widgets'][extra_widget]['name']} widget (id {extra_widget}) to the "
             f"{target_tab.replace('_', ' ').title()} tab of the new dashboard."),
        ]),
        "fixtures": {"backends": [{"name": "stark-enterprise"}]},
        "initial_state": {},
        "allowed_tools": ["get_workspace_snapshot", "manage_backends", "manage_apps",
                           "navigate_workspace", "list_available_widgets",
                           "get_widget_schema", "create_widget"],
        "success": {
            "required_dashboard_name_contains": dash_name,
            "required_tabs": ["overview"] + check_tabs,
            "required_widgets": [
                {"origin": STK, "widget_id": wid, "tab_id": tab, "min_count": 1}
                for wid, tab in check_widgets
            ] + [{"origin": STK, "widget_id": extra_widget, "tab_id": target_tab,
                   "min_count": 1}],
            "layout": {"within_grid": True, "grid_width": 40},
            "trace_checks": {"max_invalid_tool_calls": 0,
                              "must_call_schema_before_create": True},
        },
        "oracle_tool_calls": instantiate_oracle(app, dash_name) + [
            {"tool": "navigate_workspace",
             "args": {"operation": "tab", "tab_id": target_tab}},
            {"tool": "get_widget_schema",
             "args": {"origin": STK, "widget_id": extra_widget}},
            {"tool": "create_widget",
             "args": {"origin": STK, "widget_id": extra_widget, "data_args": {}}}],
    })

APPS_T4 = [
    ("mnpi-research-review", "MNPI Control Desk", "research",
     "mnpi_research_review_research_reviewer_comments",
     ["reviewer comments", "sign off"],
     "Reviewer comments tracked; evidence sign off pending."),
    ("healthcare-research-dashboard", "Biotech Catalyst Desk", "clinical",
     "healthcare_research_dashboard_clinical_regulatory_timeline",
     ["regulatory timeline", "catalysts"],
     "Regulatory timeline added; clinical catalysts tracked."),
    ("crypto-research-dashboard", "Digital Assets Desk", "market",
     "crypto_research_dashboard_market_crypto_market_metrics",
     ["market metrics", "token"],
     "Crypto market metrics added for the token book."),
    ("corporate-access-meeting-notes", "Corporate Access Log", "meetings",
     "corporate_access_meeting_notes_meetings_expert_calls",
     ["expert calls", "meeting calendar"],
     "Expert calls tracked against the meeting calendar."),
]
for template_id, dash_name, target_tab, extra_widget, note_facts, note_text in APPS_T4:
    app = APPS_BY_TEMPLATE[template_id]
    workflow, sub = stark_family(template_id)
    check_tabs, check_widgets = app_checks(app)
    if target_tab not in check_tabs:
        check_tabs = sorted(set(check_tabs + [target_tab]))
    add("apps", "r4", {
        "id": f"full_{template_id.replace('-', '_')}",
        "title": f"Instantiate, Extend, And Brief {app['name']}",
        "category_code": "L3", "capability": "app-instantiation", "workflow": workflow,
        "subdomain": sub, "tags": ["apps", "stark", "widget-creation", "note"],
        "prompt": phrased(f"full_{template_id.replace('-', '_')}", [
            (f"Instantiate the {app['name']} app from the Bench Stark Enterprise "
             f"backend as a new dashboard named {dash_name}. Then add the "
             f"{STARK['widgets'][extra_widget]['name']} widget (id {extra_widget}) to "
             f"the {target_tab.replace('_', ' ').title()} tab, and add a note on the "
             f"same tab mentioning {note_facts[0]} and {note_facts[1]}."),
            (f"From the Bench Stark Enterprise backend, instantiate the {app['name']} app "
             f"as a new dashboard named {dash_name}. Then add the "
             f"{STARK['widgets'][extra_widget]['name']} widget (id {extra_widget}) to "
             f"the {target_tab.replace('_', ' ').title()} tab, and add a note on the same "
             f"tab mentioning {note_facts[0]} and {note_facts[1]}."),
            (f"Create a new dashboard named {dash_name} by instantiating the {app['name']} "
             "app from the Bench Stark Enterprise backend. Then add the "
             f"{STARK['widgets'][extra_widget]['name']} widget (id {extra_widget}) to the "
             f"{target_tab.replace('_', ' ').title()} tab, and add a note on the same tab "
             f"mentioning {note_facts[0]} and {note_facts[1]}."),
        ]),
        "fixtures": {"backends": [{"name": "stark-enterprise"}]},
        "initial_state": {},
        "allowed_tools": ["get_workspace_snapshot", "manage_backends", "manage_apps",
                           "navigate_workspace", "list_available_widgets",
                           "get_widget_schema", "create_widget", "add_generative_widget"],
        "success": {
            "required_dashboard_name_contains": dash_name,
            "required_tabs": ["overview"] + check_tabs,
            "required_widgets": [
                {"origin": STK, "widget_id": wid, "tab_id": tab, "min_count": 1}
                for wid, tab in check_widgets
            ] + [{"origin": STK, "widget_id": extra_widget, "tab_id": target_tab,
                   "min_count": 1}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": note_facts,
                 "tab_id": target_tab}],
            "layout": {"within_grid": True, "grid_width": 40},
            "trace_checks": {"max_invalid_tool_calls": 0,
                              "must_call_schema_before_create": True},
        },
        "oracle_tool_calls": instantiate_oracle(app, dash_name) + [
            {"tool": "navigate_workspace",
             "args": {"operation": "tab", "tab_id": target_tab}},
            {"tool": "get_widget_schema",
             "args": {"origin": STK, "widget_id": extra_widget}},
            {"tool": "create_widget",
             "args": {"origin": STK, "widget_id": extra_widget, "data_args": {}}},
            note_call("Brief Note", note_text)],
    })


# ===========================================================================
# Family NAVIGATE — anchor: manage_dashboard / manage_navigation_bar
# ===========================================================================

NAV_T0 = [
    ("compliance_day", "Alert Triage", "Daily Compliance Control",
     "compliance-surveillance", "compliance", "stark-enterprise"),
    ("execution_open", "Desk Board", "Execution Morning Board",
     "execution-exception-review", "execution", "stark-enterprise"),
    ("equity_desk", "Desk View", "Equity Desk Monitor",
     "equity-tearsheet", "equity-research", "equities"),
    ("macro_watch", "Macro Board", "Rates Watch",
     "macro-rates-review", "macro", "macro"),
]
for slug, old_dash, new_dash, workflow, sub, fixture in NAV_T0:
    add("navigate", "r0", {
        "id": f"rename_{slug}",
        "title": f"Rename To {new_dash}",
        "category_code": "L1", "capability": "workspace-navigation", "workflow": workflow,
        "subdomain": sub, "tags": ["rename", "navigation"],
        "prompt": phrased(f"rename_{slug}", [
            f"Rename the active dashboard to {new_dash}.",
            f"Set the active dashboard name to {new_dash}.",
            f"Change the active dashboard's name to {new_dash}.",
        ]),
        "fixtures": {"backends": [{"name": fixture}]},
        "initial_state": seeded(old_dash, [], tabs=[{"id": "overview", "name": "Overview"}]),
        "allowed_tools": ["get_workspace_snapshot", "manage_dashboard"],
        "success": {
            "required_dashboard_name_contains": new_dash,
            "required_tool_calls": [
                {"tool": "manage_dashboard",
                 "args_contains": {"operation": "update", "name": new_dash}}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": [
            {"tool": "manage_dashboard", "args": {"operation": "update", "name": new_dash}}],
    })

NAV_T1 = [
    ("client_review", "Client Prep", "Client Review Agenda", "Overview", "Talking Points",
     "client-meeting-prep", "client-ir", "stark-enterprise"),
    ("ops_close", "Ops Board", "Fund Close Control", "Overview", "Close Checklist",
     "vendor-sla-monitoring", "data-platform", "stark-enterprise"),
    ("pm_morning", "PM Board", "PM Morning Review", "Overview", "Holdings View",
     "portfolio-morning-review", "portfolio-management", "portfolio"),
    ("earnings_week", "Earnings Board", "Earnings Week Planner", "Overview", "Calendar",
     "earnings-prep", "equity-research", "equities"),
]
for slug, old_dash, new_dash, old_tab, new_tab, workflow, sub, fixture in NAV_T1:
    add("navigate", "r1", {
        "id": f"rename_both_{slug}",
        "title": f"Rename Dashboard And Tab: {new_dash}",
        "category_code": "L1", "capability": "workspace-navigation", "workflow": workflow,
        "subdomain": sub, "tags": ["rename", "navigation"],
        "prompt": phrased(f"rename_both_{slug}", [
            (f"Rename the active dashboard to {new_dash} and rename the {old_tab} tab "
             f"to {new_tab}."),
            (f"Set the active dashboard name to {new_dash} and rename the {old_tab} tab "
             f"to {new_tab}."),
            (f"Change the active dashboard's name to {new_dash}; also rename the {old_tab} "
             f"tab to {new_tab}."),
        ]),
        "fixtures": {"backends": [{"name": fixture}]},
        "initial_state": seeded(old_dash, [], tabs=[{"id": "overview", "name": old_tab}]),
        "allowed_tools": ["get_workspace_snapshot", "manage_dashboard",
                           "manage_navigation_bar", "navigate_workspace"],
        "success": {
            "required_dashboard_name_contains": new_dash,
            "required_tabs": [slugify(new_tab)],
            "required_tool_calls": [
                {"tool": "manage_dashboard",
                 "args_contains": {"operation": "update", "name": new_dash}},
                {"tool": "manage_navigation_bar",
                 "args_contains": {"operation": "rename_tabs"}}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": [
            {"tool": "manage_dashboard", "args": {"operation": "update", "name": new_dash}},
            {"tool": "manage_navigation_bar",
             "args": {"operation": "rename_tabs", "rename_map": {"overview": new_tab}}}],
    })

NAV_T2 = [
    ("risk_expansion", "Risk Board", "Risk Command Center", "Stress Results",
     "risk-review", "risk", ["stress results", "pending"]),
    ("vendor_expansion", "Vendor Board", "Vendor Control Center", "Incident Log",
     "vendor-sla-monitoring", "data-platform", ["incident log", "pending"]),
    ("research_expansion", "Research Board", "Research Command Center", "Draft Reviews",
     "equity-tearsheet", "equity-research", ["draft reviews", "pending"]),
    ("client_expansion", "Client Board", "Client Command Center", "Open Requests",
     "client-meeting-prep", "client-ir", ["open requests", "pending"]),
]
for slug, old_dash, new_dash, new_tab, workflow, sub, note_facts in NAV_T2:
    tab_slug = slugify(new_tab)
    add("navigate", "r2", {
        "id": f"expand_{slug}",
        "title": f"Expand To {new_dash}",
        "category_code": "L1", "capability": "workspace-navigation", "workflow": workflow,
        "subdomain": sub, "tags": ["rename", "tabs", "navigation"],
        "prompt": phrased(f"expand_{slug}", [
            (f"Rename the active dashboard to {new_dash}, add a new tab named "
             f"{new_tab}, and add a note on the new tab that mentions {note_facts[0]} "
             "and says items are pending."),
            (f"Set the active dashboard name to {new_dash}, add a new tab named "
             f"{new_tab}, and add a note on the new tab that mentions {note_facts[0]} "
             "and says items are pending."),
            (f"Change the active dashboard's name to {new_dash}; add a new tab named "
             f"{new_tab}; then add a note on the new tab that mentions {note_facts[0]} "
             "and says items are pending."),
        ]),
        "fixtures": {"backends": [{"name": "stark-enterprise"}]},
        "initial_state": seeded(old_dash, [], tabs=[{"id": "overview", "name": "Overview"}]),
        "allowed_tools": ["get_workspace_snapshot", "manage_dashboard",
                           "manage_navigation_bar", "navigate_workspace",
                           "add_generative_widget"],
        "success": {
            "required_dashboard_name_contains": new_dash,
            "required_tabs": ["overview", tab_slug],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": note_facts, "tab_id": tab_slug}],
            "required_tool_calls": [
                {"tool": "manage_navigation_bar",
                 "args_contains": {"operation": "add_tabs"}}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": [
            {"tool": "manage_dashboard", "args": {"operation": "update", "name": new_dash}},
            {"tool": "manage_navigation_bar",
             "args": {"operation": "add_tabs", "tabs": [{"name": new_tab}]}},
            {"tool": "navigate_workspace", "args": {"operation": "tab", "tab_id": tab_slug}},
            note_call("Tab Note", f"Tracking {note_facts[0]}: items are pending review.")],
    })

NAV_T3 = [
    ("estimates_msft", EQ, "equities", "Estimates", "estimate_history",
     {"symbol": "MSFT"},
     ("price_performance", {"symbol": "MSFT"})),
    ("fundamentals_aapl", EQ, "equities", "Fundamentals", "fundamental_metrics",
     {"symbol": "AAPL"},
     ("price_performance", {"symbol": "AAPL"})),
    ("curve", MACRO, "macro", "Curve", "yield_curve", {},
     ("macro_timeseries", {"series": "DGS10"})),
    ("risk", PF, "portfolio", "Risk", "risk_metrics", {},
     ("holdings_table", {})),
]
for slug, origin, fixture, tab_name, new_widget, new_args, (seed_widget, seed_args) in NAV_T3:
    workflow, sub = wf(origin)
    tab_slug = slugify(tab_name)
    add("navigate", "r3", {
        "id": f"addtab_{slug}",
        "title": f"Add The Missing {tab_name} Tab",
        "category_code": "L4", "capability": "workspace-repair", "workflow": workflow,
        "subdomain": sub, "tags": ["repair", "tabs", "navigation"],
        "prompt": phrased(f"addtab_{slug}", [
            (f"This dashboard is missing its {tab_name} tab. Add a tab named "
             f"{tab_name} and put the {wname(origin, new_widget)} widget"
             + (f" for {new_args.get('symbol')}" if new_args.get("symbol") else "")
             + " on it. Keep the existing Overview tab intact."),
            (f"Add the missing {tab_name} tab to this dashboard and put the "
             f"{wname(origin, new_widget)} widget"
             + (f" for {new_args.get('symbol')}" if new_args.get("symbol") else "")
             + " on it. Keep the existing Overview tab intact."),
            (f"Keep the existing Overview tab intact while adding a tab named {tab_name} "
             f"and placing the {wname(origin, new_widget)} widget"
             + (f" for {new_args.get('symbol')}" if new_args.get("symbol") else "")
             + " on it."),
        ]),
        "fixtures": {"backends": [{"name": fixture}]},
        "initial_state": seeded("Incomplete Review",
                                 [{"origin": origin, "widget_id": seed_widget,
                                   "data_args": seed_args, "tab_id": "overview",
                                   "layout": {"x": 0, "y": 2, "w": 20, "h": 12}}],
                                 tabs=[{"id": "overview", "name": "Overview"}]),
        "allowed_tools": ["get_workspace_snapshot", "manage_navigation_bar",
                           "navigate_workspace", "list_available_widgets",
                           "get_widget_schema", "create_widget"],
        "success": {
            "required_tabs": ["overview", tab_slug],
            "required_widgets": [
                {"origin": origin, "widget_id": seed_widget, "data_args": seed_args,
                 "tab_id": "overview", "min_count": 1},
                {"origin": origin, "widget_id": new_widget, "data_args": new_args,
                 "tab_id": tab_slug, "min_count": 1},
            ],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "manage_navigation_bar",
                                "args": {"operation": "add_tabs",
                                          "tabs": [{"name": tab_name}]}},
                               {"tool": "navigate_workspace",
                                "args": {"operation": "tab", "tab_id": tab_slug}}]
        + discovery(origin, new_widget, new_args),
    })

NAV_T4: list[
    tuple[str, str, str, str, str, str, dict[str, Any], list[str], str]
] = [
    ("earnings_hub", EQ, "equities", "Earnings Hub", "Estimates",
     "estimate_history", {"symbol": "AAPL"}, ["estimates", "earnings hub"],
     "Earnings hub: estimates tab tracks the numbers into the print."),
    ("rates_hub", MACRO, "macro", "Rates Hub", "Curve",
     "yield_curve", {}, ["curve", "rates hub"],
     "Rates hub: curve tab holds the term-structure view."),
    ("book_hub", PF, "portfolio", "Book Hub", "Exposure",
     "sector_exposure", {}, ["exposure", "book hub"],
     "Book hub: exposure tab tracks sector concentrations."),
    ("desk_hub", EQ, "equities", "Desk Hub", "News",
     "latest_news", {"symbol": "NVDA", "limit": 5}, ["news", "desk hub"],
     "Desk hub: news tab tracks the NVDA tape."),
]
for slug, origin, fixture, new_dash, tab_name, new_widget, new_args, note_facts, note_text in NAV_T4:
    workflow, sub = wf(origin)
    tab_slug = slugify(tab_name)
    add("navigate", "r4", {
        "id": f"hub_{slug}",
        "title": f"Build Out {new_dash}",
        "category_code": "L2", "capability": "workspace-navigation", "workflow": workflow,
        "subdomain": sub, "tags": ["rename", "tabs", "navigation", "combo"],
        "prompt": phrased(f"hub_{slug}", [
            (f"Rename the active dashboard to {new_dash}, add a new tab named "
             f"{tab_name}, put the {wname(origin, new_widget)} widget"
             + (f" for {new_args.get('symbol')}" if new_args.get("symbol") else "")
             + f" on it, and add a note on the same tab mentioning {note_facts[0]} "
             f"and {note_facts[1]}."),
            (f"Set the active dashboard name to {new_dash}, add a new tab named "
             f"{tab_name}, put the {wname(origin, new_widget)} widget"
             + (f" for {new_args.get('symbol')}" if new_args.get("symbol") else "")
             + f" on it, and add a note on the same tab mentioning {note_facts[0]} "
             f"and {note_facts[1]}."),
            (f"Change the active dashboard's name to {new_dash}; add a new tab named "
             f"{tab_name}; put the {wname(origin, new_widget)} widget"
             + (f" for {new_args.get('symbol')}" if new_args.get("symbol") else "")
             + f" on it; then add a note on the same tab mentioning {note_facts[0]} "
             f"and {note_facts[1]}."),
        ]),
        "fixtures": {"backends": [{"name": fixture}]},
        "initial_state": seeded("Starter Board", [],
                                 tabs=[{"id": "overview", "name": "Overview"}]),
        "allowed_tools": ["get_workspace_snapshot", "manage_dashboard",
                           "manage_navigation_bar", "navigate_workspace",
                           "list_available_widgets", "get_widget_schema", "create_widget",
                           "add_generative_widget"],
        "success": {
            "required_dashboard_name_contains": new_dash,
            "required_tabs": ["overview", tab_slug],
            "required_widgets": [
                {"origin": origin, "widget_id": new_widget, "data_args": new_args,
                 "tab_id": tab_slug, "min_count": 1}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": note_facts, "tab_id": tab_slug}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": [
            {"tool": "manage_dashboard", "args": {"operation": "update", "name": new_dash}},
            {"tool": "manage_navigation_bar",
             "args": {"operation": "add_tabs", "tabs": [{"name": tab_name}]}},
            {"tool": "navigate_workspace", "args": {"operation": "tab", "tab_id": tab_slug}},
        ] + discovery(origin, new_widget, new_args) + [note_call("Hub Note", note_text)],
    })


# ===========================================================================
# Family SKILLS — anchor: get_skill_content
# ===========================================================================

SKILLS = {
    "finance-earnings-prep": ("Finance Earnings Prep",
                               ["Earnings prep workflow", "surprise drivers",
                                "portfolio manager"],
                               ["earnings prep", "surprise drivers"]),
    "finance-tearsheet": ("Finance Tearsheet",
                           ["Tearsheet workflow", "valuation", "investment conclusion"],
                           ["tearsheet", "valuation"]),
    "finance-guidance-tracker": ("Finance Guidance Tracker",
                                  ["Guidance tracker workflow", "management claims",
                                   "evidence gaps"],
                                  ["guidance", "claims"]),
    "finance-comps": ("Finance Comps",
                       ["Comps workflow", "peer set", "valuation multiples"],
                       ["comps", "peer set"]),
}
SKILL_SLUGS = list(SKILLS)


def skill_task(level: str, slug: str, extra: dict) -> None:
    skill_name, result_facts, note_facts = SKILLS[slug]
    base = {
        "id": slug.replace("-", "_"),
        "category_code": "L1", "capability": "skill-access",
        "workflow": "earnings-prep" if "earnings" in slug else "equity-tearsheet",
        "subdomain": "equity-research", "tags": ["skills", "mcp"],
        "fixtures": {"backends": [{"name": "stark-enterprise"}]},
        "initial_state": seeded("Skill Review", [],
                                 tabs=[{"id": "overview", "name": "Overview"}]),
    }
    base.update(extra)
    add("skills", level, base)


for slug in SKILL_SLUGS:
    skill_name, result_facts, note_facts = SKILLS[slug]
    skill_task("r0", slug, {
        "title": f"Read The {skill_name} Skill",
        "prompt": phrased(f"{slug.replace('-', '_')}", [
            (f"Call get_skill_content with slug {slug}, then add a note on the active "
             f"dashboard naming the {skill_name} skill. Omit dashboard_id when adding "
             "the note."),
            (f"Use get_skill_content with slug {slug}, then add a note on the active "
             f"dashboard naming the {skill_name} skill. Omit dashboard_id when adding "
             "the note."),
            (f"After calling get_skill_content with slug {slug}, add a note on the active "
             f"dashboard naming the {skill_name} skill. Omit dashboard_id when adding "
             "the note."),
        ]),
        "allowed_tools": ["get_workspace_snapshot", "get_skill_content",
                           "add_generative_widget"],
        "success": {
            "required_tool_calls": [
                {"tool": "get_skill_content", "args_contains": {"slug": slug}}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": [skill_name]}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "get_skill_content", "args": {"slug": slug}},
                               note_call("Skill Note",
                                         f"Read the {skill_name} skill for this desk.")],
    })

for slug in SKILL_SLUGS:
    skill_name, result_facts, note_facts = SKILLS[slug]
    skill_extra: dict[str, Any] = {
        "title": f"Apply {skill_name} Workflow Notes",
        "prompt": phrased(f"{slug.replace('-', '_')}", [
            (f"Call get_skill_content with slug {slug}, then add a note on the active "
             "dashboard that captures the workflow steps for an analyst. Omit "
             "dashboard_id when adding the note."),
            (f"Use get_skill_content with slug {slug}, then add a note on the active "
             "dashboard that captures the workflow steps for an analyst. Omit "
             "dashboard_id when adding the note."),
            (f"After calling get_skill_content with slug {slug}, add a note on the active "
             "dashboard that captures the workflow steps for an analyst. Omit "
             "dashboard_id when adding the note."),
        ]),
        "allowed_tools": ["get_workspace_snapshot", "get_skill_content",
                           "add_generative_widget"],
        "success": {
            "required_tool_calls": [
                {"tool": "get_skill_content", "args_contains": {"slug": slug}}],
            "required_tool_results": [
                {"tool": "get_skill_content", "data_contains": result_facts}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": note_facts}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "get_skill_content", "args": {"slug": slug}},
                               note_call(f"{skill_name} Note",
                                         f"{skill_name} workflow: "
                                         + "; ".join(note_facts) + ".")],
    }
    skill_task("r1", slug, skill_extra)

SKILL_T2_TABS = {"finance-earnings-prep": "Earnings Prep", "finance-tearsheet": "Tearsheet",
                  "finance-guidance-tracker": "Guidance", "finance-comps": "Comps"}
for slug in SKILL_SLUGS:
    skill_name, result_facts, note_facts = SKILLS[slug]
    tab_name = SKILL_T2_TABS[slug]
    tab_slug = slugify(tab_name)
    skill_task("r2", slug, {
        "title": f"File {skill_name} Under Its Own Tab",
        "prompt": phrased(f"{slug.replace('-', '_')}", [
            (f"Call get_skill_content with slug {slug}. Add a new tab named "
             f"{tab_name} and put a note on that tab capturing the workflow steps. "
             "Omit dashboard_id when adding the note."),
            (f"Use get_skill_content with slug {slug}. Add a new tab named {tab_name} "
             "and put a note on that tab capturing the workflow steps. Omit dashboard_id "
             "when adding the note."),
            (f"After calling get_skill_content with slug {slug}, add a new tab named "
             f"{tab_name} and put a note on that tab capturing the workflow steps. Omit "
             "dashboard_id when adding the note."),
        ]),
        "allowed_tools": ["get_workspace_snapshot", "get_skill_content",
                           "manage_navigation_bar", "navigate_workspace",
                           "add_generative_widget"],
        "success": {
            "required_tabs": ["overview", tab_slug],
            "required_tool_calls": [
                {"tool": "get_skill_content", "args_contains": {"slug": slug}}],
            "required_tool_results": [
                {"tool": "get_skill_content", "data_contains": result_facts}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": note_facts, "tab_id": tab_slug}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "get_skill_content", "args": {"slug": slug}},
                               {"tool": "manage_navigation_bar",
                                "args": {"operation": "add_tabs",
                                          "tabs": [{"name": tab_name}]}},
                               {"tool": "navigate_workspace",
                                "args": {"operation": "tab", "tab_id": tab_slug}},
                               note_call(f"{skill_name} Note",
                                         f"{skill_name} workflow: "
                                         + "; ".join(note_facts) + ".")],
    })

SKILL_T3: list[tuple[str, str, str, dict[str, Any]]] = [
    ("finance-tearsheet", EQ, "price_performance", {"symbol": "MSFT"}),
    ("finance-earnings-prep", EQ, "estimate_history", {"symbol": "AAPL"}),
    ("finance-guidance-tracker", EQ, "latest_news", {"symbol": "AAPL", "limit": 5}),
    ("finance-comps", EQ, "fundamental_metrics", {"symbol": "AAPL"}),
]
for slug, origin, widget_id, data_args in SKILL_T3:
    skill_name, result_facts, note_facts = SKILLS[slug]
    value = data_args.get("symbol", "")
    skill_task("r3", slug, {
        "title": f"Apply {skill_name} With {value}",
        "fixtures": {"backends": [{"name": "equities"}]},
        "prompt": phrased(f"{slug.replace('-', '_')}", [
            (f"Call get_skill_content with slug {slug}. Following that workflow, add "
             f"the {wname(origin, widget_id)} widget for {value} to the active "
             "dashboard, then add a note that applies the skill's workflow steps to "
             "this widget. Omit dashboard_id when adding the note."),
            (f"Use get_skill_content with slug {slug}. Following that workflow, add the "
             f"{wname(origin, widget_id)} widget for {value} to the active dashboard, then "
             "add a note that applies the skill's workflow steps to this widget. Omit "
             "dashboard_id when adding the note."),
            (f"After calling get_skill_content with slug {slug}, follow that workflow by "
             f"adding the {wname(origin, widget_id)} widget for {value} to the active "
             "dashboard, then add a note that applies the skill's workflow steps to this "
             "widget. Omit dashboard_id when adding the note."),
        ]),
        "allowed_tools": ["get_workspace_snapshot", "get_skill_content",
                           "list_available_widgets", "get_widget_schema", "create_widget",
                           "add_generative_widget"],
        "success": {
            "required_tool_calls": [
                {"tool": "get_skill_content", "args_contains": {"slug": slug}}],
            "required_tool_results": [
                {"tool": "get_skill_content", "data_contains": result_facts}],
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": data_args,
                 "min_count": 1}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": note_facts + [value]}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "get_skill_content", "args": {"slug": slug}}]
        + discovery(origin, widget_id, data_args)
        + [note_call("Skill Note",
                     f"{value} {note_facts[0]}: " + "; ".join(note_facts) + ".")],
    })

SKILL_T4 = [
    ("finance-tearsheet", "price_performance", {"symbol": "AAPL"},
     ["AAPL", CLOSES["AAPL"], "valuation"],
     f"AAPL tearsheet: close {CLOSES['AAPL']}; valuation next."),
    ("finance-earnings-prep", "estimate_history", {"symbol": "MSFT"},
     ["MSFT", EPS_Q1["MSFT"], "surprise drivers"],
     f"MSFT earnings prep: 2026Q1 EPS {EPS_Q1['MSFT']}; surprise drivers listed."),
    ("finance-comps", "fundamental_metrics", {"symbol": "NVDA"},
     ["NVDA", MARGIN["NVDA"], "peer set"],
     f"NVDA comps: gross margin {MARGIN['NVDA']} against the peer set."),
    ("finance-guidance-tracker", "estimate_history", {"symbol": "NVDA"},
     ["NVDA", EPS_Q1["NVDA"], "claims"],
     f"NVDA guidance: 2026Q1 EPS {EPS_Q1['NVDA']}; management claims tracked."),
]
for slug, widget_id, data_args, note_facts, note_text in SKILL_T4:
    skill_name, result_facts, _ = SKILLS[slug]
    value = data_args["symbol"]
    skill_task("r4", slug, {
        "title": f"Grounded {skill_name} For {value}",
        "fixtures": {"backends": [{"name": "equities"}]},
        "prompt": phrased(f"{slug.replace('-', '_')}", [
            (f"Call get_skill_content with slug {slug}. Following that workflow, add "
             f"the {wname(EQ, widget_id)} widget for {value}, read its data, and add "
             "a note that cites the exact key value from the data. Omit dashboard_id "
             "when adding the note."),
            (f"Use get_skill_content with slug {slug}. Following that workflow, add the "
             f"{wname(EQ, widget_id)} widget for {value}, read its data, and add a note "
             "that cites the exact key value from the data. Omit dashboard_id when adding "
             "the note."),
            (f"After calling get_skill_content with slug {slug}, follow that workflow by "
             f"adding the {wname(EQ, widget_id)} widget for {value}, reading its data, and "
             "adding a note that cites the exact key value from the data. Omit dashboard_id "
             "when adding the note."),
        ]),
        "allowed_tools": ["get_workspace_snapshot", "get_skill_content",
                           "list_available_widgets", "get_widget_schema", "create_widget",
                           "get_widget_data", "add_generative_widget"],
        "success": {
            "required_tool_calls": [
                {"tool": "get_skill_content", "args_contains": {"slug": slug}},
                {"tool": "get_widget_data",
                 "args_contains": {"widget_id": widget_id}}],
            "required_tool_results": [
                {"tool": "get_skill_content", "data_contains": result_facts}],
            "required_widgets": [
                {"origin": EQ, "widget_id": widget_id, "data_args": data_args,
                 "min_count": 1}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": note_facts}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "get_skill_content", "args": {"slug": slug}}]
        + discovery(EQ, widget_id, data_args)
        + [{"tool": "get_widget_data",
             "args": {"origin": EQ, "widget_id": widget_id, "data_args": data_args}},
            note_call("Skill Note", note_text)],
    })


# ===========================================================================
# Family DELEGATE — anchor: assign_tasks_to_agents
# ===========================================================================

def task_request(tid: str, desc: str) -> dict:
    return {"id": tid, "description": desc,
            "assigned_holder_url": f"workspace://agents/{tid.rsplit('-', 1)[0]}",
            "assigned_agent_id": f"{tid.rsplit('-', 1)[0]}-agent"}


DELEGATE_T0 = [
    ("earnings_single", "coverage-analyst",
     "Review estimate revisions and transcript tone for earnings prep.",
     "earnings-prep", "equity-research"),
    ("risk_single", "stress-analyst",
     "Run the historical stress scenarios and summarize losses.",
     "risk-review", "risk"),
    ("client_single", "ir-analyst",
     "Prepare talking points and open requests for the client meeting.",
     "client-meeting-prep", "client-ir"),
    ("vendor_single", "triage-analyst",
     "Triage the open vendor incident log by severity.",
     "vendor-sla-monitoring", "data-platform"),
]
for slug, tid, desc, workflow, sub in DELEGATE_T0:
    add("delegate", "r0", {
        "id": f"{slug}",
        "title": f"Delegate One Task: {slug.replace('_', ' ').title()}",
        "category_code": "L3", "capability": "mcp-tool-use", "workflow": workflow,
        "subdomain": sub, "tags": ["delegation", "agents", "mcp"],
        "prompt": phrased(f"{slug}", [
            (f"Call assign_tasks_to_agents with one task_request using id {tid} for "
             f"{workflow.replace('-', ' ')} work: {desc}"),
            (f"Use assign_tasks_to_agents with one task_request using id {tid} for "
             f"{workflow.replace('-', ' ')} work: {desc}"),
            (f"For {workflow.replace('-', ' ')} work, call assign_tasks_to_agents with one "
             f"task_request using id {tid}: {desc}"),
        ]),
        "fixtures": {"backends": [{"name": "stark-enterprise"}]},
        "initial_state": seeded("Delegation Board", [],
                                 tabs=[{"id": "overview", "name": "Overview"}]),
        "allowed_tools": ["get_workspace_snapshot", "assign_tasks_to_agents"],
        "success": {
            "required_tool_calls": [{"tool": "assign_tasks_to_agents"}],
            "required_tool_results": [
                {"tool": "assign_tasks_to_agents", "data_contains": [tid]}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "assign_tasks_to_agents",
                                "args": {"task_requests": [task_request(tid, desc)]}}],
    })

DELEGATE_T1 = [
    ("earnings_pair", "earnings-prep", "equity-research",
     [("coverage-analyst", "Review estimate revisions and transcript tone."),
      ("model-analyst", "Check the internal versus street model bridge.")]),
    ("risk_pair", "risk-review", "risk",
     [("stress-analyst", "Run historical stress scenarios and summarize losses."),
      ("limits-analyst", "Review limit utilization and current breaches.")]),
    ("client_pair", "client-meeting-prep", "client-ir",
     [("ir-analyst", "Prepare talking points and open requests."),
      ("portfolio-analyst", "Summarize client portfolio performance and exposure.")]),
    ("compliance_pair", "compliance-surveillance", "compliance",
     [("alerts-analyst", "Triage open surveillance alerts by severity."),
      ("restricted-analyst", "Verify restricted list changes against orders.")]),
]
for slug, workflow, sub, tasks in DELEGATE_T1:
    task_ids = [tid for tid, _ in tasks]
    add("delegate", "r1", {
        "id": f"{slug}",
        "title": f"Delegate Two Tasks: {slug.replace('_', ' ').title()}",
        "category_code": "L3", "capability": "mcp-tool-use", "workflow": workflow,
        "subdomain": sub, "tags": ["delegation", "agents", "mcp"],
        "prompt": phrased(f"{slug}", [
            (f"Call assign_tasks_to_agents with two task_requests using ids "
             f"{task_ids[0]} and {task_ids[1]} for {workflow.replace('-', ' ')} work."),
            (f"Use assign_tasks_to_agents with two task_requests using ids {task_ids[0]} "
             f"and {task_ids[1]} for {workflow.replace('-', ' ')} work."),
            (f"For {workflow.replace('-', ' ')} work, call assign_tasks_to_agents with two "
             f"task_requests using ids {task_ids[0]} and {task_ids[1]}."),
        ]),
        "fixtures": {"backends": [{"name": "stark-enterprise"}]},
        "initial_state": seeded("Delegation Board", [],
                                 tabs=[{"id": "overview", "name": "Overview"}]),
        "allowed_tools": ["get_workspace_snapshot", "assign_tasks_to_agents"],
        "success": {
            "required_tool_calls": [{"tool": "assign_tasks_to_agents"}],
            "required_tool_results": [
                {"tool": "assign_tasks_to_agents", "data_contains": task_ids}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "assign_tasks_to_agents",
                                "args": {"task_requests": [
                                    task_request(tid, desc) for tid, desc in tasks]}}],
    })

DELEGATE_T2 = [
    ("earnings_note", "earnings-prep", "equity-research",
     [("coverage-analyst", "Review estimate revisions and transcript tone."),
      ("model-analyst", "Check the internal versus street model bridge.")],
     ["coverage analyst", "model analyst", "earnings prep"]),
    ("risk_note", "risk-review", "risk",
     [("stress-analyst", "Run historical stress scenarios and summarize losses."),
      ("limits-analyst", "Review limit utilization and current breaches.")],
     ["stress analyst", "limits analyst", "risk review"]),
    ("client_note", "client-meeting-prep", "client-ir",
     [("ir-analyst", "Prepare talking points and open requests."),
      ("portfolio-analyst", "Summarize client portfolio performance and exposure.")],
     ["ir analyst", "portfolio analyst", "client meeting"]),
    ("ops_note", "vendor-sla-monitoring", "data-platform",
     [("triage-analyst", "Triage the open vendor incident log."),
      ("sla-analyst", "Check SLA breach history for the affected vendor.")],
     ["triage analyst", "sla analyst", "vendor"]),
]
for slug, workflow, sub, tasks, note_facts in DELEGATE_T2:
    task_ids = [tid for tid, _ in tasks]
    add("delegate", "r2", {
        "id": f"{slug}",
        "title": f"Delegate And Coordinate: {slug.replace('_', ' ').title()}",
        "category_code": "L3", "capability": "mcp-tool-use", "workflow": workflow,
        "subdomain": sub, "tags": ["delegation", "agents", "mcp", "note"],
        "prompt": phrased(f"{slug}", [
            (f"Call assign_tasks_to_agents with two task_requests using ids "
             f"{task_ids[0]} and {task_ids[1]} for {workflow.replace('-', ' ')} work. "
             "Then add a coordinator note naming both workstreams on the active "
             "dashboard; omit dashboard_id when adding the note."),
            (f"Use assign_tasks_to_agents with two task_requests using ids {task_ids[0]} "
             f"and {task_ids[1]} for {workflow.replace('-', ' ')} work. Then add a "
             "coordinator note naming both workstreams on the active dashboard; omit "
             "dashboard_id when adding the note."),
            (f"For {workflow.replace('-', ' ')} work, call assign_tasks_to_agents with two "
             f"task_requests using ids {task_ids[0]} and {task_ids[1]}. Then add a "
             "coordinator note naming both workstreams on the active dashboard; omit "
             "dashboard_id when adding the note."),
        ]),
        "fixtures": {"backends": [{"name": "stark-enterprise"}]},
        "initial_state": seeded("Delegation Board", [],
                                 tabs=[{"id": "overview", "name": "Overview"}]),
        "allowed_tools": ["get_workspace_snapshot", "assign_tasks_to_agents",
                           "add_generative_widget"],
        "success": {
            "required_tool_calls": [{"tool": "assign_tasks_to_agents"}],
            "required_tool_results": [
                {"tool": "assign_tasks_to_agents", "data_contains": task_ids}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": note_facts}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "assign_tasks_to_agents",
                                "args": {"task_requests": [
                                    task_request(tid, desc) for tid, desc in tasks]}},
                               note_call("Delegation Note",
                                         "; ".join(note_facts) + ".")],
    })

DELEGATE_T3 = [
    ("earnings_skill", "finance-earnings-prep",
     [("coverage-analyst", "Review estimate revisions and transcript tone."),
      ("model-analyst", "Check the internal versus street model bridge.")],
     ["coverage analyst", "model analyst", "earnings prep"]),
    ("tearsheet_skill", "finance-tearsheet",
     [("valuation-analyst", "Build the valuation section of the tearsheet."),
      ("catalyst-analyst", "List catalysts and risks for the tearsheet.")],
     ["valuation analyst", "catalyst analyst", "tearsheet"]),
    ("guidance_skill", "finance-guidance-tracker",
     [("claims-analyst", "Extract management claims from the call."),
      ("evidence-analyst", "List evidence gaps against prior guidance.")],
     ["claims analyst", "evidence analyst", "guidance"]),
    ("comps_skill", "finance-comps",
     [("peers-analyst", "Define the peer set and normalize metrics."),
      ("multiples-analyst", "Compare valuation multiples and flag outliers.")],
     ["peers analyst", "multiples analyst", "comps"]),
]
for slug, skill_slug, tasks, note_facts in DELEGATE_T3:
    skill_name, result_facts, _ = SKILLS[skill_slug]
    task_ids = [tid for tid, _ in tasks]
    add("delegate", "r3", {
        "id": f"skill_{slug}",
        "title": f"Delegate Per The {skill_name} Skill",
        "category_code": "L3", "capability": "mcp-tool-use",
        "workflow": "earnings-prep" if "earnings" in skill_slug else "equity-tearsheet",
        "subdomain": "equity-research",
        "tags": ["delegation", "agents", "mcp", "skills"],
        "prompt": phrased(f"skill_{slug}", [
            (f"Call get_skill_content with slug {skill_slug} to understand the "
             f"workflow. Then call assign_tasks_to_agents with two task_requests "
             f"using ids {task_ids[0]} and {task_ids[1]} covering that workflow, and "
             "add a coordinator note naming both workstreams. Omit dashboard_id when "
             "adding the note."),
            (f"Use get_skill_content with slug {skill_slug} to understand the workflow. "
             f"Then call assign_tasks_to_agents with two task_requests using ids "
             f"{task_ids[0]} and {task_ids[1]} covering that workflow, and add a "
             "coordinator note naming both workstreams. Omit dashboard_id when adding the "
             "note."),
            (f"After calling get_skill_content with slug {skill_slug} to understand the "
             f"workflow, call assign_tasks_to_agents with two task_requests using ids "
             f"{task_ids[0]} and {task_ids[1]} covering that workflow, and add a "
             "coordinator note naming both workstreams. Omit dashboard_id when adding the "
             "note."),
        ]),
        "fixtures": {"backends": [{"name": "stark-enterprise"}]},
        "initial_state": seeded("Delegation Board", [],
                                 tabs=[{"id": "overview", "name": "Overview"}]),
        "allowed_tools": ["get_workspace_snapshot", "get_skill_content",
                           "assign_tasks_to_agents", "add_generative_widget"],
        "success": {
            "required_tool_calls": [
                {"tool": "get_skill_content", "args_contains": {"slug": skill_slug}},
                {"tool": "assign_tasks_to_agents"}],
            "required_tool_results": [
                {"tool": "get_skill_content", "data_contains": result_facts},
                {"tool": "assign_tasks_to_agents", "data_contains": task_ids}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": note_facts}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "get_skill_content", "args": {"slug": skill_slug}},
                               {"tool": "assign_tasks_to_agents",
                                "args": {"task_requests": [
                                    task_request(tid, desc) for tid, desc in tasks]}},
                               note_call("Delegation Note",
                                         "; ".join(note_facts) + ".")],
    })

DELEGATE_T4 = [
    ("vendor_build", "vendor-sla-monitoring", "data-platform",
     [("triage-analyst", "Triage the open vendor incident log."),
      ("sla-analyst", "Check SLA breach history for the affected vendor.")],
     "vendor_dataset_monitor_incidents_incident_log",
     ["triage analyst", "sla analyst", "incident log"]),
    ("exec_build", "execution-exception-review", "execution",
     [("rejects-analyst", "Investigate rejected orders on the desk."),
      ("restricted-analyst", "Cross-check restricted list checks against fills.")],
     "execution_desk_exceptions_rejected_orders",
     ["rejects analyst", "restricted analyst", "rejected orders"]),
    ("earnings_build", "earnings-prep", "equity-research",
     [("revisions-analyst", "Track consensus revisions into the print."),
      ("reaction-analyst", "Prepare the post-earnings price reaction view.")],
     "earnings_estimates_monitor_estimates_consensus_revisions",
     ["revisions analyst", "reaction analyst", "consensus revisions"]),
    ("risk_build", "risk-review", "risk",
     [("var-analyst", "Summarize the VaR trend for the committee."),
      ("stress-analyst", "Prepare the stress loss summary.")],
     "risk_exposure_monitor_dashboard_var_trend",
     ["var analyst", "stress analyst", "var trend"]),
]
for slug, workflow, sub, tasks, widget_id, note_facts in DELEGATE_T4:
    task_ids = [tid for tid, _ in tasks]
    add("delegate", "r4", {
        "id": f"build_{slug}",
        "title": f"Delegate And Equip: {slug.replace('_', ' ').title()}",
        "category_code": "L3", "capability": "mcp-tool-use", "workflow": workflow,
        "subdomain": sub, "tags": ["delegation", "agents", "mcp", "widget-creation"],
        "prompt": phrased(f"build_{slug}", [
            (f"Call assign_tasks_to_agents with two task_requests using ids "
             f"{task_ids[0]} and {task_ids[1]}. Then add the "
             f"{STARK['widgets'][widget_id]['name']} widget (id {widget_id}) from the "
             "Bench Stark Enterprise backend so the workstreams have their data, and "
             "add a coordinator note naming both workstreams. Omit dashboard_id when "
             "adding the note."),
            (f"Use assign_tasks_to_agents with two task_requests using ids {task_ids[0]} "
             f"and {task_ids[1]}. Then add the {STARK['widgets'][widget_id]['name']} "
             f"widget (id {widget_id}) from the Bench Stark Enterprise backend so the "
             "workstreams have their data, and add a coordinator note naming both "
             "workstreams. Omit dashboard_id when adding the note."),
            (f"After assigning two task_requests with ids {task_ids[0]} and {task_ids[1]} "
             "through assign_tasks_to_agents, add the "
             f"{STARK['widgets'][widget_id]['name']} widget (id {widget_id}) from the Bench "
             "Stark Enterprise backend so the workstreams have their data, and add a "
             "coordinator note naming both workstreams. Omit dashboard_id when adding the "
             "note."),
        ]),
        "fixtures": {"backends": [{"name": "stark-enterprise"}]},
        "initial_state": seeded("Delegation Board", [],
                                 tabs=[{"id": "overview", "name": "Overview"}]),
        "allowed_tools": ["get_workspace_snapshot", "assign_tasks_to_agents",
                           "list_available_widgets", "get_widget_schema", "create_widget",
                           "add_generative_widget"],
        "success": {
            "required_tool_calls": [{"tool": "assign_tasks_to_agents"}],
            "required_tool_results": [
                {"tool": "assign_tasks_to_agents", "data_contains": task_ids}],
            "required_widgets": [
                {"origin": STK, "widget_id": widget_id, "data_args": {}, "min_count": 1}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": note_facts}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "assign_tasks_to_agents",
                                "args": {"task_requests": [
                                    task_request(tid, desc) for tid, desc in tasks]}}]
        + discovery(STK, widget_id, {})
        + [note_call("Delegation Note", "; ".join(note_facts) + ".")],
    })


# ===========================================================================
# Family PARAMS — anchor: get_params_options
# ===========================================================================

STARK_WIDGET_IDS = sorted(STARK["widgets"])


def sw(index: int) -> str:
    return STARK_WIDGET_IDS[index % len(STARK_WIDGET_IDS)]


PARAM_VALUES = {
    "symbol": ["AAPL", "MSFT", "NVDA"],
    "series": ["FEDFUNDS", "DGS2", "DGS10", "CPIAUCSL"],
    "sector": ["Technology", "Consumer Staples", "Communication Services"],
}


def params_case(index: int) -> tuple[str, str, str, str]:
    cases = [
        (EQ, "price_performance", "symbol", "AAPL"),
        (MACRO, "macro_timeseries", "series", "DGS10"),
        (PF, "sector_exposure", "sector", "Technology"),
        (STK, sw(20 + index), "sector", "Consumer Staples"),
    ]
    return cases[index % len(cases)]


def params_oracle(
    origin: str,
    widget_id: str,
    param: str,
    value: str,
    *,
    schema_first: bool,
) -> list[dict]:
    calls = [snap()]
    if schema_first:
        calls.extend(
            [
                {"tool": "list_available_widgets", "args": {"origin": origin}},
                {
                    "tool": "get_widget_schema",
                    "args": {"origin": origin, "widget_id": widget_id},
                },
            ]
        )
    calls.extend(
        [
            {
                "tool": "get_params_options",
                "args": {
                    "origin": origin,
                    "widget_id": widget_id,
                    "param_name": param,
                },
            },
            {
                "tool": "create_widget",
                "args": {
                    "origin": origin,
                    "widget_id": widget_id,
                    "data_args": {param: value},
                },
            },
        ]
    )
    return calls


for idx in range(4):
    origin, widget_id, param, value = params_case(idx)
    workflow, sub = wf(origin, widget_id)
    add("params", "r0", {
        "id": f"{param}_{widget_id}_{idx}",
        "title": f"Use {param.title()} Options For {wname(origin, widget_id)}",
        "category_code": "L1", "capability": "parameter-discovery", "workflow": workflow,
        "subdomain": sub, "tags": ["params", "options"],
        "prompt": phrased(f"{param}_{widget_id}_{idx}", [
            (f"Call get_params_options for {origin}/{widget_id} parameter {param}, "
             f"choose {value}, and create that widget with {param}={value}."),
            (f"Use get_params_options for {origin}/{widget_id} parameter {param}, choose "
             f"{value}, and create that widget with {param}={value}."),
            (f"For {origin}/{widget_id}, call get_params_options on parameter {param}, "
             f"choose {value}, and create that widget with {param}={value}."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Parameter Options", []),
        "allowed_tools": ["get_workspace_snapshot", "get_params_options", "create_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": {param: value}}],
            "required_tool_calls": [
                {"tool": "get_params_options",
                 "args_contains": {"widget_id": widget_id, "param_name": param}}],
            "required_tool_results": [
                {"tool": "get_params_options", "data_contains": [value]}],
            "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": params_oracle(origin, widget_id, param, value,
                                           schema_first=False),
    })

for idx in range(4, 8):
    origin, widget_id, param, value = params_case(idx)
    workflow, sub = wf(origin, widget_id)
    add("params", "r1", {
        "id": f"schema_{param}_{widget_id}_{idx}",
        "title": f"Discover Schema Then Options For {wname(origin, widget_id)}",
        "category_code": "L1", "capability": "parameter-discovery", "workflow": workflow,
        "subdomain": sub, "tags": ["params", "schema-discovery"],
        "prompt": phrased(f"schema_{param}_{widget_id}_{idx}", [
            (f"Discover the catalog and schema for {origin}/{widget_id}, call "
             f"get_params_options for {param}, then create it with {param}={value}."),
            (f"For {origin}/{widget_id}, discover the catalog and schema, call "
             f"get_params_options for {param}, then create it with {param}={value}."),
            (f"Before creating {origin}/{widget_id} with {param}={value}, discover the "
             f"catalog and schema and call get_params_options for {param}."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Parameter Options", []),
        "allowed_tools": ["get_workspace_snapshot", "list_available_widgets",
                           "get_widget_schema", "get_params_options", "create_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": {param: value}}],
            "required_tool_calls": [
                {"tool": "get_params_options",
                 "args_contains": {"widget_id": widget_id, "param_name": param}}],
            "required_tool_results": [
                {"tool": "get_params_options", "data_contains": [value]}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": params_oracle(origin, widget_id, param, value,
                                           schema_first=True),
    })

for idx in range(8, 12):
    origin, widget_id, param, value = params_case(idx)
    workflow, sub = wf(origin, widget_id)
    target = {"x": (idx % 2) * 20, "y": 0, "w": 20, "h": 10}
    add("params", "r2", {
        "id": f"place_{param}_{widget_id}_{idx}",
        "title": f"Options-Constrained Placement For {wname(origin, widget_id)}",
        "category_code": "L2", "capability": "dashboard-construction", "workflow": workflow,
        "subdomain": sub, "tags": ["params", "layout"],
        "prompt": phrased(f"place_{param}_{widget_id}_{idx}", [
            (f"Use get_params_options to choose {value} for {param}, fetch the widget "
             f"schema, create {origin}/{widget_id}, and place it at x={target['x']}, "
             "y=0, width 20, height 10."),
            (f"Choose {value} for {param} with get_params_options, fetch the widget "
             f"schema, create {origin}/{widget_id}, and place it at x={target['x']}, "
             "y=0, width 20, height 10."),
            (f"Create {origin}/{widget_id} after fetching the widget schema and using "
             f"get_params_options to choose {value} for {param}, then place it at "
             f"x={target['x']}, y=0, width 20, height 10."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Parameter Placement", []),
        "allowed_tools": ["get_workspace_snapshot", "list_available_widgets",
                           "get_widget_schema", "get_params_options", "create_widget",
                           "update_widget_layout"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": {param: value}}],
            "required_layouts": [{"widget_id": widget_id, **target}],
            "required_tool_results": [
                {"tool": "get_params_options", "data_contains": [value]}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": params_oracle(origin, widget_id, param, value,
                                           schema_first=True)
        + [{"tool": "update_widget_layout", "args": {"widget_id": widget_id, **target}}],
    })

PARAM_T3 = [
    (EQ, "price_performance", "symbol", "AAPL", "latest_news", {"symbol": "AAPL", "limit": 5}),
    (MACRO, "macro_timeseries", "series", "DGS2", "yield_curve", {}),
    (PF, "sector_exposure", "sector", "Technology", "risk_metrics", {}),
    (STK, sw(44), "sector", "Communication Services", sw(45), {}),
]
for idx, (origin, widget_id, param, value, companion, companion_args) in enumerate(PARAM_T3):
    workflow, sub = wf(origin, widget_id)
    add("params", "r3", {
        "id": f"companion_{param}_{widget_id}_{idx}",
        "title": f"Options-Constrained Pair For {wname(origin, widget_id)}",
        "category_code": "L2", "capability": "dashboard-construction", "workflow": workflow,
        "subdomain": sub, "tags": ["params", "multi-widget"],
        "prompt": phrased(f"companion_{param}_{widget_id}_{idx}", [
            (f"Use get_params_options to set {origin}/{widget_id} {param}={value}, "
             f"then add companion widget {companion}. Arrange both without overlap."),
            (f"Set {origin}/{widget_id} {param}={value} using get_params_options, then "
             f"add companion widget {companion}. Arrange both without overlap."),
            (f"After using get_params_options for {origin}/{widget_id} {param}={value}, "
             f"add companion widget {companion} and arrange both without overlap."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Parameter Pair", []),
        "allowed_tools": ["get_workspace_snapshot", "list_available_widgets",
                           "get_widget_schema", "get_params_options", "create_widget",
                           "update_widget_layout"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": {param: value}},
                {"origin": origin, "widget_id": companion, "data_args": companion_args},
            ],
            "required_layouts": [
                {"widget_id": widget_id, "x": 0, "y": 0, "w": 20, "h": 10},
                {"widget_id": companion, "x": 20, "y": 0, "w": 20, "h": 10},
            ],
            "required_tool_results": [
                {"tool": "get_params_options", "data_contains": [value]}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": params_oracle(origin, widget_id, param, value,
                                           schema_first=True)
        + discovery(origin, companion, companion_args)
        + [
            {"tool": "update_widget_layout",
             "args": {"widget_id": widget_id, "x": 0, "y": 0, "w": 20, "h": 10}},
            {"tool": "update_widget_layout",
             "args": {"widget_id": companion, "x": 20, "y": 0, "w": 20, "h": 10}},
        ],
    })

PARAM_T4: list[tuple[str, list[tuple[str, str, str, str]], list[str]]] = [
    ("aapl_macro", [(EQ, "price_performance", "symbol", "AAPL"),
                    (MACRO, "macro_timeseries", "series", "DGS10")],
     ["AAPL", "DGS10"]),
    ("portfolio_sector", [(PF, "sector_exposure", "sector", "Technology"),
                          (MACRO, "macro_timeseries", "series", "CPIAUCSL")],
     ["Technology", "CPIAUCSL"]),
    ("stark_sector", [(STK, sw(60), "sector", "Consumer Staples"),
                      (PF, "risk_metrics", "sector", "Consumer Staples")],
     ["Consumer Staples", "options"]),
    ("nvda_rates", [(EQ, "estimate_history", "symbol", "NVDA"),
                    (MACRO, "macro_timeseries", "series", "FEDFUNDS")],
     ["NVDA", "FEDFUNDS"]),
]
for slug, param_widgets, facts in PARAM_T4:
    origins = sorted({origin for origin, *_ in param_widgets})
    oracle = [snap()]
    required_widgets = []
    for origin, widget_id, param, value in param_widgets:
        oracle += discovery(origin, widget_id, {param: value}, param)
        required_widgets.append(
            {"origin": origin, "widget_id": widget_id, "data_args": {param: value}}
        )
    oracle.append(note_call("Options Note", "Options used: " + ", ".join(facts) + "."))
    workflow, sub = wf(param_widgets[0][0], param_widgets[0][1])
    add("params", "r4", {
        "id": f"cross_{slug}",
        "title": f"Cross-Backend Options Build: {slug.replace('_', ' ').title()}",
        "category_code": "L2", "capability": "dashboard-construction", "workflow": workflow,
        "subdomain": sub, "tags": ["params", "cross-backend", "note"],
        "prompt": phrased(f"cross_{slug}", [
            ("Build a two-widget dashboard using parameter options for both widgets: "
             + "; ".join(
                 f"{origin}/{widget_id} {param}={value}"
                 for origin, widget_id, param, value in param_widgets
             )
             + ". Add a note mentioning " + " and ".join(facts) + "."),
            ("Using parameter options for both widgets, build a two-widget dashboard with "
             + "; ".join(
                 f"{origin}/{widget_id} {param}={value}"
                 for origin, widget_id, param, value in param_widgets
             )
             + ". Add a note mentioning " + " and ".join(facts) + "."),
            ("Build a dashboard with these two widgets after using parameter options for "
             "both: "
             + "; ".join(
                 f"{origin}/{widget_id} {param}={value}"
                 for origin, widget_id, param, value in param_widgets
             )
             + ". Add a note mentioning " + " and ".join(facts) + "."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)} for origin in origins]},
        "initial_state": seeded("Cross Options", []),
        "allowed_tools": ["get_workspace_snapshot", "list_available_widgets",
                           "get_widget_schema", "get_params_options", "create_widget",
                           "add_generative_widget"],
        "success": {
            "required_widgets": required_widgets,
            "required_tool_calls": [
                {"tool": "get_params_options",
                 "args_contains": {"widget_id": widget_id, "param_name": param}}
                for origin, widget_id, param, value in param_widgets],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": facts}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": oracle,
    })


# ===========================================================================
# Family BACKENDS — anchor: manage_backends
# ===========================================================================

BACKEND_CASES = [
    ("equities", EQ, "price_performance", {"symbol": "AAPL"}),
    ("macro", MACRO, "macro_timeseries", {"series": "DGS10"}),
    ("portfolio", PF, "holdings_table", {}),
    ("stark-enterprise", STK, sw(80), {}),
]


def backend_build_oracle(fixture: str, origin: str, widget_id: str, data_args: dict) -> list[dict]:
    return [
        {"tool": "manage_backends", "args": {"operation": "add", "name": fixture}},
        {"tool": "manage_backends", "args": {"operation": "list"}},
    ] + discovery(origin, widget_id, data_args)


for idx, (fixture, origin, widget_id, data_args) in enumerate(BACKEND_CASES):
    workflow, sub = wf(origin, widget_id)
    add("backends", "r0", {
        "id": f"add_{fixture.replace('-', '_')}",
        "title": f"Register {origin}",
        "category_code": "L2", "capability": "dashboard-construction", "workflow": workflow,
        "subdomain": sub, "tags": ["backends"],
        "prompt": phrased(f"add_{fixture.replace('-', '_')}", [
            (f"Call manage_backends with operation add and name {fixture} to register "
             f"{origin}, then call manage_backends with operation list."),
            (f"Use manage_backends with operation add and name {fixture} for {origin}; "
             "then use manage_backends with operation list."),
            (f"With manage_backends, use operation add and name {fixture} to register "
             f"{origin}, then list it with operation list."),
        ]),
        "fixtures": {"backends": []},
        "initial_state": seeded("Backend Registration", []),
        "allowed_tools": ["manage_backends"],
        "success": {
            "required_tool_calls": [
                {"tool": "manage_backends", "args_contains": {"operation": "add"}},
                {"tool": "manage_backends", "args_contains": {"operation": "list"}},
            ],
            "required_tool_results": [
                {"tool": "manage_backends", "data_contains": [origin]}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": [
            {"tool": "manage_backends", "args": {"operation": "add", "name": fixture}},
            {"tool": "manage_backends", "args": {"operation": "list"}},
        ],
    })

for idx, (fixture, origin, widget_id, data_args) in enumerate(BACKEND_CASES):
    workflow, sub = wf(origin, widget_id)
    target_widget = widget_ref(origin, widget_id, data_args)
    add("backends", "r1", {
        "id": f"add_widget_{widget_id}_{idx}",
        "title": f"Register Backend And Add {wname(origin, widget_id)}",
        "category_code": "L2", "capability": "dashboard-construction", "workflow": workflow,
        "subdomain": sub, "tags": ["backends", "widget-creation"],
        "prompt": phrased(f"add_widget_{widget_id}_{idx}", [
            (f"Call manage_backends with operation add and name {fixture} to register "
             f"{origin}; then discover {widget_id}, fetch its schema, and add "
             f"{target_widget} to the active dashboard."),
            (f"After calling manage_backends with operation add and name {fixture} for "
             f"{origin}, discover {widget_id}, fetch its schema, and add "
             f"{target_widget} to the active dashboard."),
            (f"Use manage_backends with operation add and name {fixture}; then discover "
             f"{widget_id}, fetch its schema, and create {target_widget} on the active "
             "dashboard."),
        ]),
        "fixtures": {"backends": []},
        "initial_state": seeded("Backend Build", []),
        "allowed_tools": ["manage_backends", "get_workspace_snapshot",
                           "list_available_widgets", "get_widget_schema",
                           "create_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": data_args}],
            "required_tool_calls": [
                {"tool": "manage_backends", "args_contains": {"operation": "add"}}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": backend_build_oracle(fixture, origin, widget_id, data_args),
    })

BACKEND_T2: list[
    tuple[str, str, str, dict[str, Any], str, str, str, dict[str, Any]]
] = [
    ("equities", EQ, "latest_news", {"symbol": "MSFT", "limit": 5}, "macro", MACRO,
     "yield_curve", {}),
    ("portfolio", PF, "sector_exposure", {}, "macro", MACRO, "macro_timeseries",
     {"series": "FEDFUNDS"}),
    ("stark-enterprise", STK, sw(90), {}, "portfolio", PF, "risk_metrics", {}),
    ("equities", EQ, "fundamental_metrics", {"symbol": "NVDA"}, "portfolio", PF,
     "holdings_table", {}),
]
for idx, (fixture_a, origin_a, widget_a, args_a, fixture_b, origin_b, widget_b, args_b) in enumerate(BACKEND_T2):
    workflow, sub = wf(origin_a, widget_a)
    widget_a_ref = widget_ref(origin_a, widget_a, args_a)
    widget_b_ref = widget_ref(origin_b, widget_b, args_b)
    add("backends", "r2", {
        "id": f"cross_{widget_a}_{widget_b}_{idx}",
        "title": f"Register Two Backends: {wname(origin_a, widget_a)} And {wname(origin_b, widget_b)}",
        "category_code": "L2", "capability": "dashboard-construction", "workflow": workflow,
        "subdomain": sub, "tags": ["backends", "cross-backend"],
        "prompt": phrased(f"cross_{widget_a}_{widget_b}_{idx}", [
            (f"Register backend names {fixture_a} and {fixture_b}; then fetch each "
             f"widget's schema and add {widget_a_ref} and {widget_b_ref} to the active "
             "dashboard."),
            (f"After registering backend names {fixture_a} and {fixture_b}, fetch each "
             f"widget's schema and add {widget_a_ref} and {widget_b_ref} to the active "
             "dashboard."),
            (f"Register both backends by name ({fixture_a}, {fixture_b}); then fetch "
             f"each widget's schema and add {widget_a_ref} and {widget_b_ref} to the "
             "active dashboard."),
        ]),
        "fixtures": {"backends": []},
        "initial_state": seeded("Cross Backend Build", []),
        "allowed_tools": ["manage_backends", "get_workspace_snapshot",
                           "list_available_widgets", "get_widget_schema",
                           "create_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin_a, "widget_id": widget_a, "data_args": args_a},
                {"origin": origin_b, "widget_id": widget_b, "data_args": args_b},
            ],
            "required_tool_calls": [
                {"tool": "manage_backends", "args_contains": {"operation": "add"},
                 "min_count": 2}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": [
            {"tool": "manage_backends", "args": {"operation": "add", "name": fixture_a}},
            {"tool": "manage_backends", "args": {"operation": "add", "name": fixture_b}},
            snap(),
        ] + discovery(origin_a, widget_a, args_a) + discovery(origin_b, widget_b, args_b),
    })

for idx, (fixture, origin, widget_id, data_args) in enumerate(BACKEND_CASES):
    workflow, sub = wf(origin, widget_id)
    target_widget = widget_ref(origin, widget_id, data_args)
    add("backends", "r3", {
        "id": f"refresh_{widget_id}_{idx}",
        "title": f"Refresh Backend Before Building {wname(origin, widget_id)}",
        "category_code": "L2", "capability": "dashboard-construction", "workflow": workflow,
        "subdomain": sub, "tags": ["backends", "refresh"],
        "prompt": phrased(f"refresh_{widget_id}_{idx}", [
            (f"Register backend name {fixture} for {origin}, refresh it, then add "
             f"{target_widget} and document that the backend was refreshed."),
            (f"After registering backend name {fixture} and refreshing {origin}, add "
             f"{target_widget} and document that the backend was refreshed."),
            (f"Register {origin} with backend name {fixture}, refresh it, then add "
             f"{target_widget} and document that the backend was refreshed."),
        ]),
        "fixtures": {"backends": []},
        "initial_state": seeded("Backend Refresh Build", []),
        "allowed_tools": ["manage_backends", "get_workspace_snapshot",
                           "list_available_widgets", "get_widget_schema",
                           "create_widget", "add_generative_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": data_args}],
            "required_tool_calls": [
                {"tool": "manage_backends", "args_contains": {"operation": "refresh"}}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": ["refreshed", origin]}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": [
            {"tool": "manage_backends", "args": {"operation": "add", "name": fixture}},
            {"tool": "manage_backends",
             "args": {"operation": "refresh", "backend_id": "backend_001"}},
            snap(),
        ] + discovery(origin, widget_id, data_args)
        + [note_call("Backend Note", f"{origin} backend refreshed before build.")],
    })

BACKEND_T4: list[
    tuple[str, list[tuple[str, str, str, dict[str, Any]]], list[str]]
] = [
    ("equities_macro", [("equities", EQ, "price_performance", {"symbol": "AAPL"}),
                        ("macro", MACRO, "macro_timeseries", {"series": "DGS10"})],
     ["AAPL", "DGS10"]),
    ("portfolio_macro", [("portfolio", PF, "risk_metrics", {}),
                         ("macro", MACRO, "yield_curve", {})],
     ["portfolio", "yield curve"]),
    ("stark_portfolio", [("stark-enterprise", STK, sw(104), {}),
                         ("portfolio", PF, "sector_exposure", {})],
     ["stark", "sector exposure"]),
    ("equities_portfolio", [("equities", EQ, "latest_news", {"symbol": "NVDA", "limit": 5}),
                            ("portfolio", PF, "holdings_table", {})],
     ["NVDA", "holdings"]),
]
for slug, backend_widgets, facts in BACKEND_T4:
    oracle = []
    for fixture, origin, widget_id, args in backend_widgets:
        oracle.append({"tool": "manage_backends", "args": {"operation": "add", "name": fixture}})
    oracle.append(snap())
    for _fixture_name, origin, widget_id, args in backend_widgets:
        oracle += discovery(origin, widget_id, args)
    oracle.append(note_call("Backend Build Note", "Built with " + " and ".join(facts) + "."))
    workflow, sub = wf(backend_widgets[0][1], backend_widgets[0][2])
    backend_names = ", ".join(fixture for fixture, _, _, _ in backend_widgets)
    widget_refs = joined([
        widget_ref(origin, widget_id, args)
        for _fixture_name, origin, widget_id, args in backend_widgets
    ])
    add("backends", "r4", {
        "id": f"multi_{slug}",
        "title": f"Multi-Backend Build: {slug.replace('_', ' ').title()}",
        "category_code": "L2", "capability": "dashboard-construction", "workflow": workflow,
        "subdomain": sub, "tags": ["backends", "cross-backend", "note"],
        "prompt": phrased(f"multi_{slug}", [
            (f"Register backend names {backend_names}, build a dashboard with "
             f"{widget_refs}, and add a note mentioning {joined(facts)}."),
            (f"After registering backend names {backend_names}, build a dashboard with "
             f"{widget_refs}, and add a note mentioning {joined(facts)}."),
            (f"Register the needed backends by exact name ({backend_names}); then build "
             f"a dashboard with {widget_refs}, and add a note mentioning {joined(facts)}."),
        ]),
        "fixtures": {"backends": []},
        "initial_state": seeded("Multi Backend Build", []),
        "allowed_tools": ["manage_backends", "get_workspace_snapshot",
                           "list_available_widgets", "get_widget_schema",
                           "create_widget", "add_generative_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": args}
                for _fixture_name, origin, widget_id, args in backend_widgets],
            "required_tool_calls": [
                {"tool": "manage_backends", "args_contains": {"operation": "add"},
                 "min_count": 2}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": facts}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": oracle,
    })


# ===========================================================================
# Family RESOURCES — anchor: read_workspace_resource
# ===========================================================================

RESOURCE_SKILLS = [
    ("finance-earnings-prep", "Earnings prep workflow", "surprise drivers"),
    ("finance-tearsheet", "Tearsheet workflow", "valuation"),
    ("finance-guidance-tracker", "Guidance tracker workflow", "management claims"),
    ("finance-comps", "Comps workflow", "peer set"),
]

for idx, (slug, phrase, note_fact) in enumerate(RESOURCE_SKILLS):
    uri = f"openbb://workspace/skills/{slug}"
    add("resources", "r0", {
        "id": f"skill_{slug.replace('-', '_')}",
        "title": f"Read Skill Resource {slug}",
        "category_code": "L0", "capability": "resource-access", "workflow": "equity-tearsheet",
        "subdomain": "equity-research", "tags": ["resources", "skills"],
        "prompt": phrased(f"skill_{slug.replace('-', '_')}", [
            (f"Call read_workspace_resource with uri {uri}, then add a note mentioning "
             f"{note_fact}."),
            (f"Use read_workspace_resource with uri {uri} and add a note mentioning "
             f"{note_fact}."),
            (f"After calling read_workspace_resource with uri {uri}, add a note mentioning "
             f"{note_fact}."),
        ]),
        "fixtures": {"backends": [{"name": "equities"}]},
        "initial_state": seeded("Resource Review", []),
        "allowed_tools": ["get_workspace_snapshot", "read_workspace_resource",
                           "add_generative_widget"],
        "success": {
            "required_resource_reads": [
                {"uri": uri, "data_contains": [phrase]}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": [note_fact]}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "read_workspace_resource", "args": {"uri": uri}},
                               note_call("Resource Note", f"Resource guidance: {note_fact}.")],
    })

RESOURCE_INDEX_CASES = [
    ("equities", "Equity Earnings Review", "equity-earnings-review"),
    ("stark-enterprise", "Portfolio Command Center", "portfolio-command-center"),
    ("stark-enterprise", "Risk Exposure Monitor", "risk-exposure-monitor"),
    ("stark-enterprise", "Client 360", "client-360"),
]
for idx, (fixture, app_name, template_id) in enumerate(RESOURCE_INDEX_CASES):
    add("resources", "r1", {
        "id": f"index_{template_id.replace('-', '_')}",
        "title": f"Read App Index For {app_name}",
        "category_code": "L2", "capability": "dashboard-construction",
        "workflow": "portfolio-morning-review", "subdomain": "portfolio-management",
        "tags": ["resources", "apps"],
        "prompt": phrased(f"index_{template_id.replace('-', '_')}", [
            ("Call read_workspace_resource with uri openbb://workspace/app-builder/index "
             f"and add a note naming the {app_name} template id {template_id}."),
            ("Use read_workspace_resource with uri openbb://workspace/app-builder/index "
             f"and add a note naming the {app_name} template id {template_id}."),
            ("After calling read_workspace_resource with uri "
             "openbb://workspace/app-builder/index, add a note naming the "
             f"{app_name} template id {template_id}."),
        ]),
        "fixtures": {"backends": [{"name": fixture}]},
        "initial_state": seeded("App Index Review", []),
        "allowed_tools": ["get_workspace_snapshot", "read_workspace_resource",
                           "add_generative_widget"],
        "success": {
            "required_resource_reads": [
                {"uri": "openbb://workspace/app-builder/index",
                 "data_contains": [app_name, template_id]}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": [app_name, template_id]}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": [
            snap(),
            {"tool": "read_workspace_resource",
             "args": {"uri": "openbb://workspace/app-builder/index"}},
            note_call("App Index Note", f"{app_name} uses template {template_id}."),
        ],
    })

RESOURCE_T2 = [
    ("equities", "equity-earnings-review", "Equity Resource Dashboard"),
    ("stark-enterprise", "vendor-dataset-monitor", "Vendor Resource Dashboard"),
    ("stark-enterprise", "execution-desk", "Execution Resource Dashboard"),
    ("stark-enterprise", "compliance-surveillance-hub", "Compliance Resource Dashboard"),
]
for fixture, template_id, dash_name in RESOURCE_T2:
    app = APPS_BY_TEMPLATE[template_id] if template_id in APPS_BY_TEMPLATE else {
        "name": "Equity Earnings Review"
    }
    add("resources", "r2", {
        "id": f"instantiate_{template_id.replace('-', '_')}",
        "title": f"Read Index Then Instantiate {app['name']}",
        "category_code": "L2", "capability": "dashboard-construction",
        "workflow": "earnings-prep" if fixture == "equities" else "portfolio-morning-review",
        "subdomain": "equity-research" if fixture == "equities" else "portfolio-management",
        "tags": ["resources", "apps"],
        "prompt": phrased(f"instantiate_{template_id.replace('-', '_')}", [
            ("Read the app-builder index resource at openbb://workspace/app-builder/index, "
             f"then instantiate template {template_id} as a dashboard named {dash_name}."),
            ("After reading the app-builder index resource "
             f"openbb://workspace/app-builder/index, instantiate template {template_id} "
             f"as a dashboard named {dash_name}."),
            ("Use the app-builder index resource openbb://workspace/app-builder/index, "
             f"then instantiate template {template_id} as a dashboard named {dash_name}."),
        ]),
        "fixtures": {"backends": [{"name": fixture}]},
        "initial_state": {},
        "allowed_tools": ["read_workspace_resource", "manage_backends", "manage_apps"],
        "success": {
            "required_dashboard_name_contains": dash_name,
            "required_resource_reads": [
                {"uri": "openbb://workspace/app-builder/index",
                 "data_contains": [template_id]}],
            "required_tool_calls": [
                {"tool": "manage_apps", "args_contains": {"operation": "instantiate"}}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": [
            {"tool": "read_workspace_resource",
             "args": {"uri": "openbb://workspace/app-builder/index"}},
            {"tool": "manage_backends", "args": {"operation": "list"}},
            {"tool": "manage_apps",
             "args": {"operation": "instantiate", "backend_id": "backend_001",
                       "template_id": template_id, "dashboard_name": dash_name,
                       "activate": True}},
        ],
    })

RESOURCE_T3 = [
    ("finance-earnings-prep", EQ, "estimate_history", {"symbol": "AAPL"}, "surprise drivers"),
    ("finance-tearsheet", EQ, "fundamental_metrics", {"symbol": "MSFT"}, "valuation"),
    ("finance-comps", PF, "sector_exposure", {}, "peer set"),
    ("finance-guidance-tracker", STK, sw(132), {}, "evidence gaps"),
]
for slug, origin, widget_id, data_args, fact in RESOURCE_T3:
    uri = f"openbb://workspace/skills/{slug}"
    workflow, sub = wf(origin, widget_id)
    target_widget = widget_ref(origin, widget_id, data_args)
    add("resources", "r3", {
        "id": f"skill_build_{slug.replace('-', '_')}",
        "title": f"Build From Skill Resource {slug}",
        "category_code": "L2", "capability": "dashboard-construction", "workflow": workflow,
        "subdomain": sub, "tags": ["resources", "widget-creation"],
        "prompt": phrased(f"skill_build_{slug.replace('-', '_')}", [
            (f"Read resource {uri}, add {target_widget}, and add a note that "
             f"mentions {fact}."),
            (f"After reading resource {uri}, add {target_widget} and add a note that "
             f"mentions {fact}."),
            (f"Use read_workspace_resource on {uri}, then add {target_widget} and add "
             f"a note that mentions {fact}."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Resource Build", []),
        "allowed_tools": ["get_workspace_snapshot", "read_workspace_resource",
                           "list_available_widgets", "get_widget_schema", "create_widget",
                           "add_generative_widget"],
        "success": {
            "required_resource_reads": [{"uri": uri, "data_contains": [fact]}],
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": data_args}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": [fact]}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "read_workspace_resource", "args": {"uri": uri}}]
        + discovery(origin, widget_id, data_args)
        + [note_call("Resource Build Note", f"Built from resource guidance: {fact}.")],
    })

RESOURCE_T4 = [
    ("portfolio-command-center", "PM Resource Command", "holdings",
     "portfolio_command_center_holdings_sector_exposure", ["sector exposure", "resource"]),
    ("risk-exposure-monitor", "Risk Resource Command", "limits",
     "risk_exposure_monitor_limits_limit_utilization", ["limit utilization", "resource"]),
    ("client-360", "Client Resource Command", "flows",
     "client_360_flows_pipeline_by_stage", ["pipeline", "resource"]),
    ("vendor-dataset-monitor", "Vendor Resource Command", "incidents",
     "vendor_dataset_monitor_incidents_incident_log", ["incident log", "resource"]),
]
for template_id, dash_name, tab_id, extra_widget, facts in RESOURCE_T4:
    app = APPS_BY_TEMPLATE[template_id]
    add("resources", "r4", {
        "id": f"full_{template_id.replace('-', '_')}",
        "title": f"Index-Guided App Extension: {app['name']}",
        "category_code": "L2", "capability": "dashboard-construction",
        "workflow": stark_family(template_id)[0], "subdomain": stark_family(template_id)[1],
        "tags": ["resources", "apps", "widget-creation"],
        "prompt": phrased(f"full_{template_id.replace('-', '_')}", [
            ("Read the app-builder index resource at openbb://workspace/app-builder/index, "
             f"instantiate {template_id} as {dash_name}, navigate to {tab_id}, add widget "
             f"{extra_widget}, and add a note mentioning {facts[0]} and resource."),
            ("After reading the app-builder index resource "
             f"openbb://workspace/app-builder/index, instantiate {template_id} as "
             f"{dash_name}, navigate to {tab_id}, add widget {extra_widget}, and add a "
             f"note mentioning {facts[0]} and resource."),
            ("Use the app-builder index resource openbb://workspace/app-builder/index, "
             f"instantiate {template_id} as {dash_name}, navigate to {tab_id}, add widget "
             f"{extra_widget}, and add a note mentioning {facts[0]} and resource."),
        ]),
        "fixtures": {"backends": [{"name": "stark-enterprise"}]},
        "initial_state": {},
        "allowed_tools": ["read_workspace_resource", "manage_backends", "manage_apps",
                           "navigate_workspace", "get_widget_schema", "create_widget",
                           "add_generative_widget"],
        "success": {
            "required_dashboard_name_contains": dash_name,
            "required_resource_reads": [
                {"uri": "openbb://workspace/app-builder/index",
                 "data_contains": [template_id]}],
            "required_widgets": [
                {"origin": STK, "widget_id": extra_widget, "tab_id": tab_id}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": facts, "tab_id": tab_id}],
            "layout": {"within_grid": True, "grid_width": 40},
            "trace_checks": {"max_invalid_tool_calls": 0,
                              "must_call_schema_before_create": True},
        },
        "oracle_tool_calls": [
            {"tool": "read_workspace_resource",
             "args": {"uri": "openbb://workspace/app-builder/index"}},
            {"tool": "manage_backends", "args": {"operation": "list"}},
            {"tool": "manage_apps",
             "args": {"operation": "instantiate", "backend_id": "backend_001",
                       "template_id": template_id, "dashboard_name": dash_name,
                       "activate": True}},
            {"tool": "navigate_workspace", "args": {"operation": "tab", "tab_id": tab_id}},
            {"tool": "get_widget_schema", "args": {"origin": STK, "widget_id": extra_widget}},
            {"tool": "create_widget", "args": {"origin": STK, "widget_id": extra_widget}},
            note_call("Resource Extension Note", f"{facts[0]} added from resource guidance."),
        ],
    })


# ===========================================================================
# Family PROMPTS — anchor: get_workspace_prompt
# ===========================================================================

PROMPT_NAMES = ["workspace_tool_usage", "workspace_session_context"]

for idx, name in enumerate(PROMPT_NAMES * 2):
    phrase = ("schema-before-create workspace tool discipline"
              if name == "workspace_tool_usage"
              else "current-dashboard current-tab session grounding")
    add("prompts", "r0", {
        "id": f"fetch_{name}_{idx}",
        "title": f"Fetch Prompt {name}",
        "category_code": "L0", "capability": "prompt-access", "workflow": "workspace-guidance",
        "domain": "workspace-usability", "subdomain": "mcp-prompts",
        "tags": ["prompts", "mcp"],
        "prompt": phrased(f"fetch_{name}_{idx}", [
            (f"Call get_workspace_prompt with name {name} and add a note mentioning "
             f"{phrase}."),
            (f"Use get_workspace_prompt with name {name}, then add a note mentioning "
             f"{phrase}."),
            (f"After calling get_workspace_prompt with name {name}, add a note mentioning "
             f"{phrase}."),
        ]),
        "fixtures": {"backends": [{"name": "equities"}]},
        "initial_state": seeded("Prompt Review", []),
        "allowed_tools": ["get_workspace_snapshot", "get_workspace_prompt",
                           "add_generative_widget"],
        "success": {
            "required_tool_calls": [
                {"tool": "get_workspace_prompt", "args_contains": {"name": name}}],
            "required_tool_results": [
                {"tool": "get_workspace_prompt", "data_contains": [phrase]}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": [phrase.split()[0]]}],
            "trace_checks": {"max_invalid_tool_calls": 0},
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "get_workspace_prompt", "args": {"name": name}},
                               note_call("Prompt Note", f"Prompt guidance: {phrase}.")],
    })

PROMPT_T1 = [
    (EQ, "price_performance", {"symbol": "AAPL"}),
    (MACRO, "macro_timeseries", {"series": "DGS10"}),
    (PF, "risk_metrics", {}),
    (STK, sw(160), {}),
]
for idx, (origin, widget_id, data_args) in enumerate(PROMPT_T1):
    workflow, sub = wf(origin, widget_id)
    target_widget = widget_ref(origin, widget_id, data_args)
    add("prompts", "r1", {
        "id": f"tool_usage_{widget_id}_{idx}",
        "title": f"Follow Tool Usage Prompt For {wname(origin, widget_id)}",
        "category_code": "L2", "capability": "dashboard-construction", "workflow": workflow,
        "domain": "workspace-usability" if origin == STK else "finance",
        "subdomain": sub, "tags": ["prompts", "schema-discovery"],
        "prompt": phrased(f"tool_usage_{widget_id}_{idx}", [
            ("Call get_workspace_prompt with name workspace_tool_usage, then follow it "
             f"by discovering schema before creating {target_widget}."),
            ("Use get_workspace_prompt with name workspace_tool_usage, then follow it "
             f"by discovering schema before creating {target_widget}."),
            (f"Before creating {target_widget}, call get_workspace_prompt with name "
             "workspace_tool_usage and follow it by discovering schema."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Prompt Build", []),
        "allowed_tools": ["get_workspace_snapshot", "get_workspace_prompt",
                           "list_available_widgets", "get_widget_schema", "create_widget"],
        "success": {
            "required_tool_results": [
                {"tool": "get_workspace_prompt",
                 "data_contains": ["schema-before-create workspace tool discipline"]}],
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": data_args}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "get_workspace_prompt",
                                "args": {"name": "workspace_tool_usage"}}]
        + discovery(origin, widget_id, data_args),
    })

PROMPT_T2 = [
    ("Estimates", EQ, "estimate_history", {"symbol": "MSFT"}),
    ("Rates", MACRO, "yield_curve", {}),
    ("Exposure", PF, "sector_exposure", {}),
    ("Ops", STK, sw(176), {}),
]
for tab_name, origin, widget_id, data_args in PROMPT_T2:
    workflow, sub = wf(origin, widget_id)
    tab_slug = slugify(tab_name)
    target_widget = widget_ref(origin, widget_id, data_args)
    add("prompts", "r2", {
        "id": f"session_tab_{tab_slug}_{widget_id}",
        "title": f"Use Session Prompt On {tab_name}",
        "category_code": "L2", "capability": "dashboard-construction", "workflow": workflow,
        "subdomain": sub, "tags": ["prompts", "tabs"],
        "prompt": phrased(f"session_tab_{tab_slug}_{widget_id}", [
            (f"Fetch workspace_session_context, add a {tab_name} tab, navigate to it, "
             f"fetch the widget schema, create {target_widget} there, and add a note "
             f"mentioning {tab_name} on that tab."),
            (f"Get workspace_session_context, add a {tab_name} tab, navigate to it, "
             f"fetch the widget schema, create {target_widget} there, and add a note "
             f"mentioning {tab_name} on that tab."),
            (f"After fetching workspace_session_context, add a {tab_name} tab, navigate to "
             f"it, fetch the widget schema, create {target_widget} there, and add a "
             f"note mentioning {tab_name} on that tab."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Prompt Session", [], tabs=[{"id": "overview", "name": "Overview"}]),
        "allowed_tools": ["get_workspace_prompt", "manage_navigation_bar",
                           "navigate_workspace", "list_available_widgets",
                           "get_widget_schema", "create_widget", "add_generative_widget"],
        "success": {
            "required_tabs": ["overview", tab_slug],
            "required_tool_results": [
                {"tool": "get_workspace_prompt",
                 "data_contains": ["current-dashboard current-tab session grounding"]}],
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": data_args,
                 "tab_id": tab_slug}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": [tab_name], "tab_id": tab_slug}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": [
            {"tool": "get_workspace_prompt", "args": {"name": "workspace_session_context"}},
            {"tool": "manage_navigation_bar",
             "args": {"operation": "add_tabs", "tabs": [{"name": tab_name}]}},
            {"tool": "navigate_workspace", "args": {"operation": "tab", "tab_id": tab_slug}},
        ] + discovery(origin, widget_id, data_args)
        + [note_call("Session Prompt Note", f"{tab_name} built using current tab guidance.")],
    })

PROMPT_T3: list[
    tuple[str, list[tuple[str, str, dict[str, Any]]], list[str]]
] = [
    ("AAPL Prompt Dashboard", [(EQ, "price_performance", {"symbol": "AAPL"}),
                               (EQ, "latest_news", {"symbol": "AAPL", "limit": 5})],
     ["AAPL", "schema"]),
    ("Macro Prompt Dashboard", [(MACRO, "macro_timeseries", {"series": "DGS2"}),
                                (MACRO, "yield_curve", {})],
     ["DGS2", "schema"]),
    ("Portfolio Prompt Dashboard", [(PF, "holdings_table", {}),
                                    (PF, "risk_metrics", {})],
     ["holdings", "schema"]),
    ("Stark Prompt Dashboard", [(STK, sw(190), {}), (STK, sw(191), {})],
     ["stark", "schema"]),
]
for dash_name, prompt_widgets, facts in PROMPT_T3:
    origins = sorted({origin for origin, _, _ in prompt_widgets})
    oracle = [
        {"tool": "get_workspace_prompt", "args": {"name": "workspace_tool_usage"}},
        {"tool": "manage_dashboard", "args": {"operation": "create", "name": dash_name}},
    ]
    required_widgets = []
    for origin, widget_id, data_args in prompt_widgets:
        oracle += discovery(origin, widget_id, data_args)
        required_widgets.append(
            {"origin": origin, "widget_id": widget_id, "data_args": data_args}
        )
    oracle.append(note_call("Prompt Build Note", "Prompt build used " + " and ".join(facts) + "."))
    workflow, sub = wf(prompt_widgets[0][0], prompt_widgets[0][1])
    widget_refs = joined([widget_ref(origin, widget_id, data_args)
                          for origin, widget_id, data_args in prompt_widgets])
    add("prompts", "r3", {
        "id": f"dashboard_{slugify(dash_name).replace('-', '_')}",
        "title": dash_name,
        "category_code": "L2", "capability": "dashboard-construction", "workflow": workflow,
        "subdomain": sub, "tags": ["prompts", "multi-widget"],
        "prompt": phrased(f"dashboard_{slugify(dash_name).replace('-', '_')}", [
            (f"Fetch workspace_tool_usage, create dashboard {dash_name}, add {widget_refs} "
             f"with schema-first discipline, and add a note mentioning {joined(facts)}."),
            (f"Get workspace_tool_usage, create dashboard {dash_name}, add {widget_refs} "
             f"with schema-first discipline, and add a note mentioning {joined(facts)}."),
            (f"After fetching workspace_tool_usage, create dashboard {dash_name}, add "
             f"{widget_refs} with schema-first discipline, and add a note mentioning "
             f"{joined(facts)}."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)} for origin in origins]},
        "initial_state": {},
        "allowed_tools": ["get_workspace_prompt", "manage_dashboard",
                           "list_available_widgets", "get_widget_schema",
                           "create_widget", "add_generative_widget"],
        "success": {
            "required_dashboard_name_contains": dash_name,
            "required_tool_results": [
                {"tool": "get_workspace_prompt",
                 "data_contains": ["schema-before-create workspace tool discipline"]}],
            "required_widgets": required_widgets,
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": facts}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": oracle,
    })

PROMPT_T4: list[
    tuple[str, list[tuple[str, str, dict[str, Any]]], list[str]]
] = [
    ("Prompt Cross AAPL Rates", [(EQ, "price_performance", {"symbol": "AAPL"}),
                                 (MACRO, "macro_timeseries", {"series": "DGS10"})],
     ["AAPL", "DGS10", "current-dashboard"]),
    ("Prompt Cross Book CPI", [(PF, "sector_exposure", {}),
                               (MACRO, "macro_timeseries", {"series": "CPIAUCSL"})],
     ["sector", "CPIAUCSL", "current-dashboard"]),
    ("Prompt Cross Stark Risk", [(STK, sw(210), {}), (PF, "risk_metrics", {})],
     ["stark", "risk", "current-dashboard"]),
    ("Prompt Cross NVDA Holdings", [(EQ, "estimate_history", {"symbol": "NVDA"}),
                                    (PF, "holdings_table", {})],
     ["NVDA", "holdings", "current-dashboard"]),
]
for dash_name, prompt_widgets, facts in PROMPT_T4:
    origins = sorted({origin for origin, _, _ in prompt_widgets})
    oracle = [
        {"tool": "get_workspace_prompt", "args": {"name": "workspace_tool_usage"}},
        {"tool": "get_workspace_prompt", "args": {"name": "workspace_session_context"}},
        {"tool": "manage_dashboard", "args": {"operation": "create", "name": dash_name}},
    ]
    required_widgets = []
    for origin, widget_id, data_args in prompt_widgets:
        oracle += discovery(origin, widget_id, data_args)
        required_widgets.append(
            {"origin": origin, "widget_id": widget_id, "data_args": data_args}
        )
    oracle.append(note_call("Prompt Cross Note", "Prompt cross build: " + ", ".join(facts) + "."))
    workflow, sub = wf(prompt_widgets[0][0], prompt_widgets[0][1])
    widget_refs = joined([widget_ref(origin, widget_id, data_args)
                          for origin, widget_id, data_args in prompt_widgets])
    add("prompts", "r4", {
        "id": f"cross_{slugify(dash_name).replace('-', '_')}",
        "title": dash_name,
        "category_code": "L2", "capability": "dashboard-construction", "workflow": workflow,
        "subdomain": sub, "tags": ["prompts", "cross-backend"],
        "prompt": phrased(f"cross_{slugify(dash_name).replace('-', '_')}", [
            (f"Fetch workspace_tool_usage and workspace_session_context, create "
             f"{dash_name}, build the cross-backend dashboard with {widget_refs}, and "
             f"add a note mentioning {joined(facts)}."),
            (f"Get workspace_tool_usage and workspace_session_context, create "
             f"{dash_name}, build the cross-backend dashboard with {widget_refs}, and "
             f"add a note mentioning {joined(facts)}."),
            (f"After fetching workspace_tool_usage and workspace_session_context, create "
             f"{dash_name}, build the cross-backend dashboard with {widget_refs}, and "
             f"add a note mentioning {joined(facts)}."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)} for origin in origins]},
        "initial_state": {},
        "allowed_tools": ["get_workspace_prompt", "manage_dashboard",
                           "list_available_widgets", "get_widget_schema",
                           "create_widget", "add_generative_widget"],
        "success": {
            "required_dashboard_name_contains": dash_name,
            "required_tool_calls": [
                {"tool": "get_workspace_prompt", "args_contains": {"name": "workspace_tool_usage"}},
                {"tool": "get_workspace_prompt", "args_contains": {"name": "workspace_session_context"}},
            ],
            "required_widgets": required_widgets,
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": facts}],
            "layout": GRID, "trace_checks": TRACE_FULL,
        },
        "oracle_tool_calls": oracle,
    })


# ===========================================================================
# Family INSPECT — anchor: read_widget / get_workspace_snapshot
# ===========================================================================

INSPECT_T0 = [
    (EQ, "price_performance", {"symbol": "AAPL"}, ["AAPL"]),
    (MACRO, "macro_timeseries", {"series": "DGS10"}, ["DGS10"]),
    (PF, "holdings_table", {}, ["holdings"]),
    (STK, sw(230), {}, ["stark"]),
]
for idx, (origin, widget_id, data_args, facts) in enumerate(INSPECT_T0):
    workflow, sub = wf(origin, widget_id)
    facts_text = joined(facts)
    add("inspect", "r0", {
        "id": f"read_{widget_id}_{idx}",
        "title": f"Inspect {wname(origin, widget_id)}",
        "category_code": "L0", "capability": "workspace-inspection", "workflow": workflow,
        "subdomain": sub, "tags": ["inspect", "read-widget"],
        "prompt": phrased(f"read_{widget_id}_{idx}", [
            (f"Call read_widget with widget_id {widget_id} for the existing "
             f"{origin}/{widget_id} widget, then add a note mentioning {facts_text}."),
            (f"Use read_widget with widget_id {widget_id} to inspect the existing "
             f"{origin}/{widget_id} widget, then add a note mentioning {facts_text}."),
            (f"After calling read_widget with widget_id {widget_id} for the existing "
             f"{origin}/{widget_id} widget, add a note mentioning {facts_text}."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Inspect Board", [
            {"origin": origin, "widget_id": widget_id, "data_args": data_args,
             "layout": {"x": 0, "y": 0, "w": 20, "h": 10}},
        ]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "add_generative_widget"],
        "success": {
            "required_tool_calls": [{"tool": "read_widget", "args_contains": {"widget_id": widget_id}}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": facts}],
            "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "read_widget", "args": {"widget_id": widget_id}},
                               note_call("Inspect Note", f"Inspected {widget_id}: {' '.join(facts)}.")],
    })

INSPECT_T1 = [
    (EQ, "price_performance", "symbol", "MSFT", "AAPL"),
    (EQ, "estimate_history", "symbol", "AAPL", "NVDA"),
    (MACRO, "macro_timeseries", "series", "FEDFUNDS", "DGS10"),
    (STK, sw(240), "sector", "Technology", "Consumer Staples"),
]
for idx, (origin, widget_id, param, wrong_value, right_value) in enumerate(INSPECT_T1):
    workflow, sub = wf(origin, widget_id)
    add("inspect", "r1", {
        "id": f"fix_{widget_id}_{idx}",
        "title": f"Find And Fix Misconfigured {wname(origin, widget_id)}",
        "category_code": "L1", "capability": "workspace-repair", "workflow": workflow,
        "subdomain": sub, "tags": ["inspect", "repair"],
        "prompt": phrased(f"fix_{widget_id}_{idx}", [
            (f"Call read_widget with widget_id {widget_id}, find the widget configured "
             f"with {param}={wrong_value}, and update_widget so {param}={right_value}."),
            (f"Use read_widget with widget_id {widget_id} to inspect the widget configured "
             f"with {param}={wrong_value}, then update_widget so {param}={right_value}."),
            (f"After calling read_widget with widget_id {widget_id}, update the widget "
             f"configured with {param}={wrong_value} so {param}={right_value}."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Inspect Repair", [
            {"origin": origin, "widget_id": widget_id, "data_args": {param: wrong_value},
             "layout": {"x": 0, "y": 0, "w": 20, "h": 10}},
        ]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "update_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": widget_id, "data_args": {param: right_value}}],
            "required_tool_calls": [{"tool": "read_widget"}],
            "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "read_widget", "args": {"widget_id": widget_id}},
                               {"tool": "update_widget",
                                "args": {"widget_uuid": "widget_001",
                                          "data_args": {param: right_value}}}],
    })

INSPECT_T2 = [
    (EQ, "latest_news", {"symbol": "AAPL", "limit": 5}, "price_performance", {"symbol": "AAPL"}),
    (MACRO, "macro_timeseries", {"series": "DGS2"}, "yield_curve", {}),
    (PF, "risk_metrics", {}, "holdings_table", {}),
    (STK, sw(250), {}, sw(251), {}),
]
for idx, (origin, dup_widget, dup_args, keep_widget, keep_args) in enumerate(INSPECT_T2):
    workflow, sub = wf(origin, dup_widget)
    add("inspect", "r2", {
        "id": f"deduplicate_{dup_widget}_{idx}",
        "title": f"Find Duplicate {wname(origin, dup_widget)}",
        "category_code": "L2", "capability": "dashboard-construction", "workflow": workflow,
        "subdomain": sub, "tags": ["inspect", "delete-widget"],
        "prompt": phrased(f"deduplicate_{dup_widget}_{idx}", [
            (f"Inspect the dashboard, identify the duplicate {dup_widget} among the "
             "seeded widgets, and remove exactly one duplicate while preserving the "
             f"{keep_widget} widget."),
            (f"After inspecting the dashboard, identify the duplicate {dup_widget} among "
             "the seeded widgets and remove exactly one duplicate while preserving the "
             f"{keep_widget} widget."),
            (f"Preserve the {keep_widget} widget while inspecting the dashboard, identifying "
             f"the duplicate {dup_widget} among the seeded widgets, and removing exactly "
             "one duplicate."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Inspect Deduplicate", [
            {"origin": origin, "widget_id": dup_widget, "data_args": dup_args,
             "layout": {"x": 0, "y": 0, "w": 20, "h": 10}},
            {"origin": origin, "widget_id": dup_widget, "data_args": dup_args,
             "layout": {"x": 20, "y": 0, "w": 20, "h": 10}},
            {"origin": origin, "widget_id": keep_widget, "data_args": keep_args,
             "layout": {"x": 0, "y": 10, "w": 20, "h": 10}},
        ]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "delete_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": dup_widget, "data_args": dup_args,
                 "min_count": 1, "max_count": 1},
                {"origin": origin, "widget_id": keep_widget, "data_args": keep_args,
                 "min_count": 1, "max_count": 1},
            ],
            "required_tool_calls": [{"tool": "read_widget", "min_count": 1}],
            "layout": GRID, "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "read_widget", "args": {"widget_uuid": "widget_002"}},
                               {"tool": "delete_widget", "args": {"widget_uuid": "widget_002"}}],
    })

INSPECT_T3 = [
    (EQ, "price_performance", {"symbol": "AAPL"}, "latest_news", {"symbol": "AAPL", "limit": 5}),
    (MACRO, "macro_timeseries", {"series": "DGS10"}, "yield_curve", {}),
    (PF, "holdings_table", {}, "sector_exposure", {}),
    (STK, sw(260), {}, sw(261), {}),
]
for idx, (origin, left_widget, left_args, right_widget, right_args) in enumerate(INSPECT_T3):
    workflow, sub = wf(origin, left_widget)
    add("inspect", "r3", {
        "id": f"overlap_{left_widget}_{idx}",
        "title": f"Inspect And Repair Overlap {wname(origin, left_widget)}",
        "category_code": "L4", "capability": "workspace-repair", "workflow": workflow,
        "subdomain": sub, "tags": ["inspect", "layout", "repair"],
        "prompt": phrased(f"overlap_{left_widget}_{idx}", [
            (f"Inspect the dashboard, find the overlapping {right_widget} widget, and move "
             "it to x=24, y=0, w=16, h=10."),
            (f"Find the overlapping {right_widget} widget after inspecting the dashboard, "
             "and move it to x=24, y=0, w=16, h=10."),
            (f"Move the overlapping {right_widget} widget to x=24, y=0, w=16, h=10 after "
             "inspecting the dashboard and finding it."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Inspect Overlap", [
            {"origin": origin, "widget_id": left_widget, "data_args": left_args,
             "layout": {"x": 0, "y": 0, "w": 24, "h": 10}},
            {"origin": origin, "widget_id": right_widget, "data_args": right_args,
             "layout": {"x": 10, "y": 0, "w": 20, "h": 10}},
        ]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "update_widget_layout"],
        "success": {
            "required_layouts": [
                {"widget_uuid": "widget_001", "x": 0, "y": 0, "w": 24, "h": 10},
                {"widget_uuid": "widget_002", "x": 24, "y": 0, "w": 16, "h": 10},
            ],
            "required_tool_calls": [{"tool": "read_widget", "min_count": 1}],
            "layout": GRID, "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "read_widget", "args": {"widget_uuid": "widget_002"}},
                               {"tool": "update_widget_layout",
                                "args": {"widget_uuid": "widget_002",
                                          "x": 24, "y": 0, "w": 16, "h": 10}}],
    })

INSPECT_T4 = [
    (EQ, "price_performance", "symbol", "MSFT", "AAPL", "latest_news", {"symbol": "AAPL", "limit": 5}),
    (MACRO, "macro_timeseries", "series", "DGS2", "DGS10", "yield_curve", {}),
    (PF, "sector_exposure", "sector", "Consumer Staples", "Technology", "risk_metrics", {}),
    (STK, sw(270), "sector", "Consumer Staples", "Technology", sw(271), {}),
]
for idx, (origin, wrong_widget, param, wrong_value, right_value, companion, companion_args) in enumerate(INSPECT_T4):
    workflow, sub = wf(origin, wrong_widget)
    add("inspect", "r4", {
        "id": f"repair_brief_{wrong_widget}_{idx}",
        "title": f"Ambient Repair And Brief {wname(origin, wrong_widget)}",
        "category_code": "L4", "capability": "workspace-repair", "workflow": workflow,
        "subdomain": sub, "tags": ["inspect", "repair", "note"],
        "prompt": phrased(f"repair_brief_{wrong_widget}_{idx}", [
            (f"Inspect the dashboard, find the widget with {param}={wrong_value}, "
             f"repair it to {right_value}, keep the companion widget, and add a note "
             "mentioning the repair."),
            (f"After inspecting the dashboard, find the widget with {param}={wrong_value}, "
             f"repair it to {right_value}, keep the companion widget, and add a note "
             "mentioning the repair."),
            (f"Keep the companion widget while finding the widget with {param}={wrong_value}, "
             f"repairing it to {right_value}, and adding a note mentioning the repair after "
             "inspecting the dashboard."),
        ]),
        "fixtures": {"backends": [{"name": fixture_for(origin)}]},
        "initial_state": seeded("Inspect Full Repair", [
            {"origin": origin, "widget_id": companion, "data_args": companion_args,
             "layout": {"x": 0, "y": 0, "w": 20, "h": 10}},
            {"origin": origin, "widget_id": wrong_widget, "data_args": {param: wrong_value},
             "layout": {"x": 20, "y": 0, "w": 20, "h": 10}},
        ]),
        "allowed_tools": ["get_workspace_snapshot", "read_widget", "update_widget",
                           "add_generative_widget"],
        "success": {
            "required_widgets": [
                {"origin": origin, "widget_id": companion, "data_args": companion_args},
                {"origin": origin, "widget_id": wrong_widget,
                 "data_args": {param: right_value}},
                {"origin": origin, "widget_id": wrong_widget,
                 "data_args": {param: wrong_value}, "min_count": 0, "max_count": 0},
            ],
            "required_tool_calls": [{"tool": "read_widget", "min_count": 1}],
            "required_generated_widgets": [
                {"widget_type": "note", "data_contains": [str(wrong_value), str(right_value), "repair"]}],
            "layout": GRID, "trace_checks": TRACE_BASIC,
        },
        "oracle_tool_calls": [snap(),
                               {"tool": "read_widget", "args": {"widget_uuid": "widget_002"}},
                               {"tool": "update_widget",
                                "args": {"widget_uuid": "widget_002",
                                          "data_args": {param: right_value}}},
                               note_call("Inspect Repair Note",
                                         f"Repair changed {wrong_value} to {right_value}.")],
    })


# ===========================================================================
# Write the suite + print the distribution matrix
# ===========================================================================

RUNGS = ["r0", "r1", "r2", "r3", "r4"]
EXPECTED_FAMILIES = {
    "apps", "backends", "create", "delegate", "delete", "inspect", "layout",
    "navigate", "note", "params", "prompts", "read", "resources", "skills",
    "update",
}


def backend_slug(name: str) -> str:
    return {
        "equities": "equities",
        EQ: "equities",
        "macro": "macro",
        MACRO: "macro",
        "portfolio": "portfolio",
        PF: "portfolio",
        "stark-enterprise": "stark-enterprise",
        STK: "stark-enterprise",
    }.get(name, name)


def task_backends(task: dict) -> set[str]:
    backends = {
        backend_slug(str(backend.get("name")))
        for backend in task.get("fixtures", {}).get("backends", [])
    }
    for call in task.get("oracle_tool_calls", []):
        if call.get("tool") != "manage_backends":
            continue
        args = call.get("args", {})
        if args.get("operation") == "add" and args.get("name"):
            backends.add(backend_slug(str(args["name"])))
    return backends


def positive_required_widget_pairs(task: dict) -> set[tuple[str, str]]:
    pairs = set()
    for req in task.get("success", {}).get("required_widgets", []):
        if int(req.get("min_count", 1)) <= 0:
            continue
        pairs.add((str(req.get("origin")), str(req.get("widget_id"))))
    return pairs


def check_type_counts(tasks: list[dict]) -> Counter:
    counts: Counter = Counter()
    for task in tasks:
        success = task.get("success", {})
        if success.get("required_dashboard_name_contains"):
            counts["dashboard_name"] += 1
        if success.get("required_tabs"):
            counts["missing_tab"] += 1
        for req in success.get("required_widgets", []):
            if int(req.get("min_count", 1)) > 0:
                counts["missing_widget"] += 1
            if req.get("max_count") is not None:
                counts["too_many_widgets"] += 1
        if success.get("required_generated_widgets"):
            counts["missing_generated_widget"] += 1
        if success.get("required_layouts"):
            counts["layout_mismatch"] += 1
        if success.get("required_tool_calls"):
            counts["missing_tool_call"] += 1
        if success.get("required_tool_results"):
            counts["missing_tool_result"] += 1
        if success.get("required_resource_reads"):
            counts["missing_resource_read"] += 1
        layout = success.get("layout", {})
        if layout.get("within_grid", True):
            counts["layout_out_of_grid"] += 1
        if layout.get("no_overlaps"):
            counts["layout_overlap"] += 1
        trace = success.get("trace_checks", {})
        if trace.get("max_invalid_tool_calls", 0) is not None:
            counts["too_many_invalid_calls"] += 1
        if trace.get("must_call_schema_before_create"):
            counts["schema_not_called_before_create"] += 1
        if trace.get("forbid_invented_widget_ids"):
            counts["unlisted_widget_id"] += 1
        if trace.get("max_repeated_snapshots") is not None:
            counts["repeated_snapshots"] += 1
    return counts


task_check_types = CheckTypePolicy(
    success_checks={
        "required_tabs": "missing_tab",
        "required_generated_widgets": "missing_generated_widget",
        "required_layouts": "layout_mismatch",
        "required_tool_calls": "missing_tool_call",
        "required_tool_results": "missing_tool_result",
        "required_resource_reads": "missing_resource_read",
    },
    widget_mode="cardinality",
    within_grid_default=True,
    max_invalid_tool_calls_default=0,
    include_forbid_invented_widget_ids=True,
)


def _core_artifact_parts(task: dict) -> list[str]:
    success = task.get("success", {})
    parts: list[str] = []
    for req in success.get("required_resource_reads", []):
        parts.append(f"resource:{req.get('uri')}")
    prompt_names = [
        str(call.get("args", {}).get("name"))
        for call in task.get("oracle_tool_calls", [])
        if call.get("tool") == "get_workspace_prompt"
    ]
    if prompt_names:
        parts.append("prompts:" + ",".join(sorted(prompt_names)))
    app_templates = [
        str(call.get("args", {}).get("template_id") or call.get("args", {}).get("app_name"))
        for call in task.get("oracle_tool_calls", [])
        if call.get("tool") == "manage_apps"
    ]
    if app_templates:
        parts.append("apps:" + ",".join(sorted(app_templates)))
    task_ids = []
    for call in task.get("oracle_tool_calls", []):
        if call.get("tool") == "assign_tasks_to_agents":
            for task in call.get("args", {}).get("task_requests", []):
                task_ids.append(str(task.get("id")))
    if task_ids:
        parts.append("tasks:" + ",".join(sorted(task_ids)))
    return parts


artifact_discriminator = ArtifactDiscriminator(
    leading_parts=_core_artifact_parts,
    include_layouts=True,
)
_NOVELTY = NoveltyPolicy(
    check_types=task_check_types,
    task_backends=task_backends,
    artifact_discriminator=artifact_discriminator,
)
novelty_fingerprint = _NOVELTY.fingerprint
add_novelty = _NOVELTY.add_description

# Uniform per-cell pattern so every (family, level) cell contributes one
# validation and one test task: per-level curves stay computable on the
# held-out splits (the earlier level-skewed patterns left r0 absent from
# test and r4 absent from validation).
assign_splits = SplitAssigner(uniform_four_way_pattern)


def assert_lattice(matrix: dict[str, dict[str, int]]) -> None:
    assert set(matrix) == EXPECTED_FAMILIES, (
        f"expected families {sorted(EXPECTED_FAMILIES)}, got {sorted(matrix)}"
    )
    for family in EXPECTED_FAMILIES:
        for level in RUNGS:
            assert matrix[family].get(level, 0) == 4, (
                f"{family}/{level} expected 4, got {matrix[family].get(level, 0)}"
            )


def quota_report(tasks: list[dict]) -> list[tuple[str, int | str, str, bool]]:
    total = len(tasks)
    categories = Counter(s["category"] for s in tasks)
    difficulties = Counter(s["difficulty"] for s in tasks)
    backend_counts = Counter(
        backend for task in tasks for backend in task_backends(task)
    )
    widget_pairs = {
        pair for task in tasks for pair in positive_required_widget_pairs(task)
    }
    checks = check_type_counts(tasks)
    fingerprints = [novelty_fingerprint(task) for task in tasks]
    unique_fingerprints = len(set(fingerprints))
    report: list[tuple[str, int | str, str, bool]] = []
    report.append((
        "dashboard-construction category",
        categories["dashboard"],
        f">= {int(total * 0.15)}",
        categories["dashboard"] >= total * 0.15,
    ))
    for backend in ("equities", "macro", "portfolio", "stark-enterprise"):
        report.append((
            f"{backend} backend coverage",
            backend_counts[backend],
            f">= {int(total * 0.15)}",
            backend_counts[backend] >= total * 0.15,
        ))
    difficulty_ok = (
        abs(difficulties["easy"] - total * 0.30) <= total * 0.05
        and abs(difficulties["medium"] - total * 0.40) <= total * 0.05
        and abs(difficulties["hard"] - total * 0.30) <= total * 0.05
    )
    report.append((
        "difficulty easy/medium/hard",
        f"{difficulties['easy']}/{difficulties['medium']}/{difficulties['hard']}",
        "90/120/90 +-15",
        difficulty_ok,
    ))
    report.append((
        "distinct required widget pairs",
        len(widget_pairs),
        ">= 120",
        len(widget_pairs) >= 120,
    ))
    for check_name in sorted(checks):
        report.append((f"grader check {check_name}", checks[check_name], ">= 10", checks[check_name] >= 10))
    report.append((
        "novelty fingerprints",
        unique_fingerprints,
        f"= {len(tasks)}",
        unique_fingerprints == len(tasks),
    ))
    return report


def uses_fixed_widget_uuid(task: dict) -> bool:
    payload = json.dumps(
        {
            "oracle": task.get("oracle_tool_calls", []),
            "layouts": task.get("success", {}).get("required_layouts", []),
        },
        sort_keys=True,
    )
    return "widget_uuid" in payload


def replaces_active_dashboard(task: dict) -> bool:
    for call in task.get("oracle_tool_calls", []):
        args = call.get("args", {})
        if call.get("tool") == "manage_dashboard" and args.get("operation") == "create":
            return True
        if call.get("tool") == "manage_apps" and args.get("operation") == "instantiate":
            return True
    return False


def has_fixture(task: dict, slug: str) -> bool:
    return any(
        backend_slug(str(backend.get("name"))) == slug
        for backend in task.get("fixtures", {}).get("backends", [])
    )


def append_fixture(task: dict, slug: str) -> None:
    if has_fixture(task, slug):
        return
    task.setdefault("fixtures", {}).setdefault("backends", []).append({"name": slug})


def append_companion_widget(task: dict, origin: str, widget_id: str) -> None:
    dashboard = task.setdefault("initial_state", {}).setdefault(
        "dashboard",
        {"name": "Coverage Board", "activate": True, "tabs": [{"id": "", "name": ""}]},
    )
    tabs = dashboard.setdefault("tabs", [{"id": "", "name": ""}])
    tab_id = str(tabs[0].get("id", ""))
    widgets = dashboard.setdefault("widgets", [])
    y = 500 + len(widgets) * 6
    widgets.append(
        {
            "origin": origin,
            "widget_id": widget_id,
            "data_args": {},
            "tab_id": tab_id,
            "layout": {"x": 0, "y": y, "w": 8, "h": 4},
        }
    )
    task.setdefault("success", {}).setdefault("required_widgets", []).append(
        {
            "origin": origin,
            "widget_id": widget_id,
            "data_args": {},
            "tab_id": tab_id,
            "min_count": 1,
            "max_count": 1,
        }
    )


def add_diversity_companions(tasks: list[dict]) -> None:
    portfolio_widgets = ["holdings_table", "sector_exposure", "risk_metrics", "holdings_table"]
    prompt_t0 = [
        task for task in tasks
        if task["_family"] == "prompts" and task["_rung"] == "r0"
    ]
    for task, widget_id in zip(sorted(prompt_t0, key=lambda item: item["id"]), portfolio_widgets):
        append_fixture(task, "portfolio")
        append_companion_widget(task, PF, widget_id)

    used_pairs = {
        pair for task in tasks for pair in positive_required_widget_pairs(task)
    }
    eligible = [
        task for task in tasks
        if has_fixture(task, "stark-enterprise")
        and task.get("initial_state", {}).get("dashboard")
        and not uses_fixed_widget_uuid(task)
        and not replaces_active_dashboard(task)
    ]
    companion_index = 290
    for task in sorted(eligible, key=lambda item: item["id"]):
        if len({
            pair for item in tasks for pair in positive_required_widget_pairs(item)
        }) >= 125:
            break
        while (STK, sw(companion_index)) in used_pairs:
            companion_index += 1
        widget_id = sw(companion_index)
        append_companion_widget(task, STK, widget_id)
        used_pairs.add((STK, widget_id))
        companion_index += 1


def prompt_pool_report(tasks: list[dict]) -> tuple[int, Counter, int]:
    source_lines = Path(__file__).read_text().splitlines()
    prompt_fields = sum(line.lstrip().startswith('"prompt":') for line in source_lines)
    phrased_fields = sum(line.lstrip().startswith('"prompt": phrased(') for line in source_lines)
    assert prompt_fields == phrased_fields, (
        f"prompt fields must all use phrased(): {phrased_fields}/{prompt_fields}"
    )
    assert len(PROMPT_POOL_SIZES) == prompt_fields, (
        f"executed prompt sites {len(PROMPT_POOL_SIZES)} != source prompt fields {prompt_fields}"
    )
    undersized = {
        site: size for site, size in PROMPT_POOL_SIZES.items()
        if size < 3
    }
    assert not undersized, f"prompt pools need >=3 variants: {undersized}"
    pool_sizes = Counter(PROMPT_POOL_SIZES.values())
    distinct_prompts = len({task["prompt"] for task in tasks})
    return len(PROMPT_POOL_SIZES), pool_sizes, distinct_prompts


def main() -> None:
    for directory in OUT_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
        for stale in directory.rglob("*.json"):
            if stale.name != "task_suite.json":
                stale.unlink()
        for candidate in sorted(directory.rglob("*"), reverse=True):
            if candidate.is_dir() and not any(candidate.iterdir()):
                candidate.rmdir()
    pairs = [(task["family"], task["id"]) for task in SCENARIOS]
    duplicate_pairs = {pair for pair in pairs if pairs.count(pair) > 1}
    for task in SCENARIOS:
        if (task["family"], task["id"]) in duplicate_pairs:
            task["id"] = re.sub(r"[^a-z0-9]+", "_", task["title"].lower()).strip("_")
    pairs = [(task["family"], task["id"]) for task in SCENARIOS]
    dupes = sorted({pair for pair in pairs if pairs.count(pair) > 1})
    assert not dupes, f"duplicate ids: {dupes}"

    add_diversity_companions(SCENARIOS)
    assign_splits(SCENARIOS)
    matrix = build_matrix(SCENARIOS)
    assert_lattice(matrix)
    for task in SCENARIOS:
        add_novelty(task)
    report = quota_report(SCENARIOS)
    failed = [name for name, _, _, ok in report if not ok]
    assert not failed, "quota failure(s): " + ", ".join(failed)
    prompt_sites, prompt_pool_sizes, distinct_prompts = prompt_pool_report(SCENARIOS)

    for task in SCENARIOS:
        task.pop("_family")
        task.pop("_rung")
        for directory in OUT_DIRS:
            family_dir = directory / task["family"]
            family_dir.mkdir(parents=True, exist_ok=True)
            (family_dir / f"{task['id']}.json").write_text(
                json.dumps(task, indent=2) + "\n")

    manifest = {
        "suite_id": "core",
        "visibility": "public",
        "default_split": "train",
        "content_sha256": task_payload_digest(SCENARIOS),
        "description": (
            "WorkspaceBench core collection: 15 MCP-surface families and 300 tasks. "
            "Splits are deterministic 150/75/75 train/validation/test; difficulty is "
            "recorded independently as easy, medium, or hard."
        ),
    }
    for directory in OUT_DIRS:
        (directory / "task_suite.json").write_text(json.dumps(manifest, indent=2) + "\n")

    print(f"Wrote {len(SCENARIOS)} tasks to {', '.join(str(d) for d in OUT_DIRS)}\n")
    print(
        "Prompt phrasing pools: "
        f"{prompt_sites} sites; pool sizes {dict(sorted(prompt_pool_sizes.items()))}"
    )
    print(f"Distinct surface prompt phrasings used: {distinct_prompts}/{len(SCENARIOS)}\n")
    print(f"{'family':12s}" + "".join(f"{t:>5s}" for t in RUNGS) + f"{'total':>7s}")
    for family in sorted(matrix):
        row = matrix[family]
        print(f"{family:12s}" + "".join(f"{row.get(t, 0):5d}" for t in RUNGS)
              + f"{sum(row.values()):7d}")
    totals = {t: sum(row.get(t, 0) for row in matrix.values()) for t in RUNGS}
    print(f"{'TOTAL':12s}" + "".join(f"{totals[t]:5d}" for t in RUNGS)
          + f"{sum(totals.values()):7d}")
    print("\nQuota report")
    for name, observed, expected, ok in report:
        status = "PASS" if ok else "FAIL"
        print(f"{status:4s} {name:36s} observed={observed} expected={expected}")


if __name__ == "__main__":
    main()
