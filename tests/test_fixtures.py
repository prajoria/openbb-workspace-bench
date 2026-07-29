from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from workspace_bench.workspace.fixtures import (
    build_daloopa_backend,
    build_getting_started_backend,
    build_stark_enterprise_backend,
)


REPO = Path(__file__).resolve().parents[1]
STARK_DATA_PATH = REPO / "src/workspace_bench/data/backends/stark_enterprise_x.json"
DALOOPA_DATA_PATH = REPO / "src/workspace_bench/data/backends/support_daloopa_skills.json"


def _load_generator(name: str):
    path = REPO / f"scripts/generators/{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_stark_data_generator():
    return _load_generator("generate_stark_data")


def test_getting_started_backend_serves_transcribed_data() -> None:
    backend = build_getting_started_backend()

    widgets = backend.widgets_json()
    assert backend.slug == "getting-started"
    assert "price_performance" not in widgets
    assert "table_widget_with_grouping_by_cell_click" in widgets

    rows = backend.fetch_widget_data(
        "table_widget_with_grouping_by_cell_click", {"symbol": "AAPL"}
    )
    assert rows[0] == {
        "change": 2.5,
        "price": 150.25,
        "symbol": "AAPL",
        "volume": 45_000_000,
    }


def test_stark_enterprise_backend_exposes_demo_catalog() -> None:
    backend = build_stark_enterprise_backend()

    assert len(backend.widgets) == 349
    assert len(backend.apps) == 23
    schema = backend.get_widget_schema(
        "equity_research_workbench_company_company_tear_sheet"
    )
    rows = backend.fetch_widget_data(
        "equity_research_workbench_company_company_tear_sheet",
        {"ticker": "LLY", "period": "YTD"},
    )

    assert schema["origin"] == "Bench Stark Enterprise"
    assert schema["grid_data"]
    assert rows
    # Real backends return business rows only; the widget id is never echoed
    # in data payloads (live-parity finding, 2026-07-12).
    assert "widget_id" not in rows[0]
    assert {"metric", "value", "change"}.issubset(rows[0])

    filtered_rows = backend.fetch_widget_data(
        "portfolio_command_center_holdings_sector_exposure",
        {"fund": "Flagship Long/Short", "period": "YTD"},
    )
    assert filtered_rows
    assert all(row["fund"] == "Flagship Long/Short" for row in filtered_rows)
    assert all(row["period"] == "YTD" for row in filtered_rows)


def test_stark_enterprise_baked_data_is_complete_deterministic_and_typed() -> None:
    generator = _load_stark_data_generator()
    raw = json.loads(STARK_DATA_PATH.read_text())

    first = generator.bake_stark_data(json.loads(json.dumps(raw)))
    second = generator.bake_stark_data(json.loads(json.dumps(raw)))
    third = generator.bake_stark_data(json.loads(json.dumps(first)))

    assert first == second
    assert first == third
    assert len(first["widgets"]) == 349
    assert all(widget.get("data") not in (None, [], {}) for widget in first["widgets"].values())

    var_rows = first["widgets"]["risk_exposure_monitor_dashboard_var_trend"]["data"]
    var_values = [row["var_usd"] for row in var_rows]
    assert var_values
    assert all(value < 0 for value in var_values)

    weight_rows = first["widgets"][
        "rebalance_scenario_lab_drift_current_vs_target_weights"
    ]["data"]
    weight_values = [row["weight"] for row in weight_rows]
    assert weight_values
    assert all(0 <= value <= 1 for value in weight_values)
    assert sum(weight_values) <= 1.0


def test_daloopa_backend_exposes_skill_data_surface() -> None:
    backend = build_daloopa_backend()

    assert len(backend.widgets) == 10
    # Standalone vendor feed by design: composition is exercised through the
    # daloopa-* workspace skills, not pre-built app templates.
    assert backend.apps == []

    schema = backend.get_widget_schema("daloopa_company_fundamentals")
    assert schema["origin"] == "Bench Daloopa"
    assert schema["grid_data"]

    directory = backend.fetch_widget_data("daloopa_company_directory", {})
    assert {"company_id", "latest_calendar_quarter", "latest_fiscal_quarter"}.issubset(
        directory[0]
    )
    assert {row["ticker"] for row in directory} == {
        "AAPL",
        "MSFT",
        "NVDA",
        "NFLX",
        "TSLA",
        "AMZN",
    }

    rows = backend.fetch_widget_data(
        "daloopa_company_fundamentals", {"ticker": "AAPL", "period": "2026Q1"}
    )
    assert rows
    assert all(row["ticker"] == "AAPL" for row in rows)
    assert all(row["calendar_period"] == "2026Q1" for row in rows)
    # Every Daloopa-sourced figure carries a fundamental_id citation link
    # (data-access.md Section 4 of the plugin skills).
    assert all(
        row["source_url"] == f"https://daloopa.com/src/{row['fundamental_id']}"
        for row in rows
    )

    docs = backend.fetch_widget_data(
        "daloopa_document_search", {"ticker": "MSFT", "doc_type": "10-Q"}
    )
    assert docs
    assert all(doc["doc_type"] == "10-Q" and doc["ticker"] == "MSFT" for doc in docs)
    assert all(
        doc["url"] == f"https://marketplace.daloopa.com/document/{doc['document_id']}"
        for doc in docs
    )

    note = backend.fetch_widget_data("daloopa_coverage_note", {})
    assert isinstance(note, str)
    assert "daloopa.com/src/" in note


def test_daloopa_skills_reference_only_existing_widgets() -> None:
    from workspace_bench.workspace.simulated_workspace import WORKSPACE_SKILLS

    backend = build_daloopa_backend()
    daloopa_skills = {
        slug: skill for slug, skill in WORKSPACE_SKILLS.items() if slug.startswith("daloopa-")
    }
    assert set(daloopa_skills) == {
        "daloopa-tearsheet",
        "daloopa-earnings-review",
        "daloopa-guidance-tracker",
        "daloopa-inflection",
        "daloopa-capital-allocation",
        "daloopa-industry",
    }
    for skill in daloopa_skills.values():
        referenced = set(re.findall(r"daloopa_[a-z_]+", skill["content"]))
        assert referenced, skill["slug"]
        assert referenced.issubset(backend.widgets), skill["slug"]
        # Every workflow enforces the plugin's mandatory citation rule.
        assert "source_url" in skill["content"], skill["slug"]


def test_daloopa_baked_data_is_deterministic_and_internally_consistent() -> None:
    generator = _load_generator("generate_daloopa_data")

    first = generator.build_daloopa_catalog()
    second = generator.build_daloopa_catalog()
    assert first == second
    # The committed catalog must match a fresh generation exactly.
    assert json.loads(json.dumps(first)) == json.loads(DALOOPA_DATA_PATH.read_text())

    widgets = first["widgets"]
    assert all(widget.get("data") not in (None, [], {}) for widget in widgets.values())

    # Fiscal labels follow each company's fiscal year end.
    fundamentals = widgets["daloopa_company_fundamentals"]["data"]
    fiscal = {
        (row["ticker"], row["calendar_period"]): row["fiscal_period"]
        for row in fundamentals
    }
    assert fiscal[("AAPL", "2026Q1")] == "FQ2'26"
    assert fiscal[("MSFT", "2026Q1")] == "FQ3'26"
    assert fiscal[("NVDA", "2026Q1")] == "FQ1'27"
    assert fiscal[("NFLX", "2026Q1")] == "FQ1'26"

    # Free cash flow equals operating cash flow minus capex, per row set.
    by_key: dict[tuple[str, str], dict[str, float]] = {}
    for row in fundamentals:
        by_key.setdefault((row["ticker"], row["calendar_period"]), {})[
            row["series"]
        ] = row["value"]
    for values in by_key.values():
        assert values["Free Cash Flow"] == round(
            values["Operating Cash Flow"] - values["Capital Expenditures"], 1
        )

    # Guidance verdicts agree with the low/high band; unreported quarters pend.
    for row in widgets["daloopa_management_guidance"]["data"]:
        if row["actual"] is None:
            assert row["verdict"] == "Pending"
        elif row["actual"] > row["guidance_high"]:
            assert row["verdict"] == "Beat"
        elif row["actual"] < row["guidance_low"]:
            assert row["verdict"] == "Missed"
        else:
            assert row["verdict"] == "In Line"

    # OHLCV rows are self-consistent.
    for row in widgets["daloopa_stock_prices"]["data"]:
        assert row["low"] <= min(row["open"], row["close"])
        assert row["high"] >= max(row["open"], row["close"])
        assert row["volume"] > 0
