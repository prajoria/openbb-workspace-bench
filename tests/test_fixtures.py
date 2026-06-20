from __future__ import annotations

import json
import threading
from urllib.request import urlopen

from workspace_bench.workspace.fixtures import (
    build_equities_backend,
    build_stark_enterprise_backend,
    make_fixture_server,
)


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
    assert rows[0]["ticker"] == "LLY"
