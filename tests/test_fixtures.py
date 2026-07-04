from __future__ import annotations

import importlib.util
import json
import threading
from pathlib import Path
from urllib.request import urlopen

from workspace_bench.workspace.fixtures import (
    build_equities_backend,
    build_stark_enterprise_backend,
    make_fixture_server,
)


REPO = Path(__file__).resolve().parents[1]
STARK_DATA_PATH = REPO / "src/workspace_bench/workspace/data/stark_enterprise.json"


def _load_stark_data_generator():
    path = REPO / "scripts/generate_stark_data.py"
    spec = importlib.util.spec_from_file_location("generate_stark_data", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_equities_backend_catalog_and_data_are_deterministic() -> None:
    backend = build_equities_backend()

    widgets = backend.widgets_json()
    assert "price_performance" in widgets
    assert widgets["price_performance"]["params"][0]["requires_options_lookup"] is True

    rows = backend.fetch_widget_data("price_performance", {"symbol": "AAPL"})
    assert rows[-1] == {"date": "2026-01-15", "close": 196.10, "return_pct": 0.014}


def test_fixture_backend_http_server_serves_workspace_contract() -> None:
    backend = build_equities_backend()
    server = make_fixture_server(backend, port=0)
    host, port = server.server_address
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with urlopen(f"http://{host}:{port}/widgets.json", timeout=5) as response:
            widgets = json.loads(response.read().decode("utf-8"))
        with urlopen(
            f"http://{host}:{port}/price-performance?symbol=AAPL", timeout=5
        ) as response:
            rows = json.loads(response.read().decode("utf-8"))
        with urlopen(f"http://{host}:{port}/symbols", timeout=5) as response:
            symbols = json.loads(response.read().decode("utf-8"))
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    assert "estimate_history" in widgets
    assert rows[-1]["close"] == 196.10
    assert symbols[0] == {"label": "AAPL", "value": "AAPL"}


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
    assert rows[0]["widget_id"] == "equity_research_workbench_company_company_tear_sheet"
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
