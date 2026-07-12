"""Generate the experimental 12-task build-openbb-backends code suite."""

from __future__ import annotations

import hashlib
import json
import pprint
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
OUTPUT = REPO / "src/workspace_bench/core/task_suites/build_openbb_backends/backend_code"
SCHEMA_VERSION = "workspace-bench-task"
CODE_SCHEMA_VERSION = "workspace-bench-code-task/v0"
INSTALL = ["uv", "sync", "--quiet"]
START = [
    "{python}",
    "-m",
    "uvicorn",
    "app:app",
    "--host",
    "127.0.0.1",
    "--port",
    "{port}",
]
TEST = ["{python}", "-m", "pytest", "-q", "--junitxml={junit}"]


JsonDict = dict[str, Any]


@dataclass(frozen=True)
class Definition:
    task_id: str
    title: str
    prompt: str
    difficulty: str
    split: str
    tags: tuple[str, ...]
    starter_app: str
    oracle_files: JsonDict
    tests: str
    probes: tuple[JsonDict, ...]
    require_apps: bool = False
    extra_starter_files: JsonDict = field(default_factory=dict)


def _widget(
    name: str,
    endpoint: str,
    widget_type: str,
    *,
    fields: tuple[tuple[str, str], ...] = (),
    params: list[JsonDict] | None = None,
    data: JsonDict | None = None,
) -> JsonDict:
    definition: JsonDict = {
        "name": name,
        "description": f"{name} business data",
        "type": widget_type,
        "endpoint": endpoint,
        "gridData": {"w": 20, "h": 10},
    }
    if fields:
        definition["data"] = {
            "table": {
                "columnsDefs": [
                    {"field": key, "headerName": label, "cellDataType": _column_type(key)}
                    for key, label in fields
                ]
            }
        }
    if params:
        definition["params"] = params
    if data:
        definition["data"] = data
    return definition


def _column_type(field_name: str) -> str:
    return "number" if any(
        token in field_name
        for token in ("price", "volume", "size", "revenue", "margin", "notional", "score")
    ) else "text"


def _app_source(
    widgets: JsonDict,
    routes: str,
    *,
    apps: list[JsonDict] | None = None,
    cors: bool = True,
    health: JsonDict | None = None,
    extra_imports: str = "",
) -> str:
    fastapi_import = "from fastapi import FastAPI"
    if "HTTPException" in routes:
        fastapi_import += ", HTTPException"
    optional_imports = ""
    if cors:
        optional_imports += "from fastapi.middleware.cors import CORSMiddleware\n"
    if "BaseModel" in routes:
        optional_imports += "from pydantic import BaseModel\n"
    middleware = (
        "app.add_middleware(CORSMiddleware, allow_origins=['*'], "
        "allow_methods=['*'], allow_headers=['*'])\n"
        if cors
        else ""
    )
    apps_route = (
        "\n@app.get('/apps.json')\ndef apps_json():\n    return APPS\n" if apps is not None else ""
    )
    return (
        "from typing import Any\n\n"
        f"{fastapi_import}\n"
        f"{optional_imports}"
        f"{extra_imports}\n"
        f"WIDGETS: dict[str, Any] = {pprint.pformat(widgets, sort_dicts=True, width=96)}\n"
        f"APPS: list[dict[str, Any]] = {pprint.pformat(apps or [], sort_dicts=True, width=96)}\n"
        f"HEALTH = {pprint.pformat(health or {'ok': True}, sort_dicts=True)}\n\n"
        "app = FastAPI(title='WorkspaceBench backend')\n"
        f"{middleware}\n"
        "@app.get('/health')\n"
        "def health():\n"
        "    return HEALTH\n\n"
        "@app.get('/widgets.json')\n"
        "def widgets_json():\n"
        "    return WIDGETS\n"
        f"{apps_route}\n"
        f"{routes.strip()}\n"
    )


def _layout_app(name: str, widgets: tuple[str, ...]) -> list[JsonDict]:
    layout = [
        {"i": widget_id, "x": index * 20, "y": 0, "w": 20, "h": 10}
        for index, widget_id in enumerate(widgets)
    ]
    return [
        {
            "template_id": name.lower().replace(" ", "-"),
            "name": name,
            "description": f"{name} application",
            "tabs": {"main": {"id": "main", "name": "Overview", "layout": layout}},
        }
    ]


def _probe(
    name: str,
    path: str,
    widget_id: str | None,
    fields: tuple[str, ...],
    *,
    method: str = "GET",
    query: JsonDict | None = None,
    body: JsonDict | None = None,
    types: JsonDict | None = None,
    expected: JsonDict | None = None,
    minimum: int = 1,
) -> JsonDict:
    return {
        "name": name,
        "method": method,
        "path": path,
        "widget_id": widget_id,
        "query": query or {},
        "json_body": body or {},
        "required_fields": list(fields),
        "field_types": types or {},
        "expected_values": expected or {},
        "minimum_items": minimum,
    }


def _tests(body: str) -> str:
    return (
        "from fastapi.testclient import TestClient\n\n"
        "from app import app\n\n"
        "client = TestClient(app)\n\n"
        "def test_cors_and_manifests():\n"
        "    response = client.get('/widgets.json', headers={'Origin': 'http://localhost'})\n"
        "    assert response.status_code == 200\n"
        "    assert response.headers.get('access-control-allow-origin') == '*'\n\n"
        f"{body.strip()}\n"
    )


def definitions() -> tuple[Definition, ...]:
    movers = _widget(
        "Market Movers",
        "/movers",
        "table",
        fields=(("symbol", "Symbol"), ("change_pct", "Change %"), ("volume", "Volume")),
    )
    task1_oracle = _app_source(
        {"market_movers": movers},
        """
MOVERS = [
    {'symbol': 'NVDA', 'change_pct': 4.2, 'volume': 51_200_000},
    {'symbol': 'AAPL', 'change_pct': -1.1, 'volume': 43_100_000},
]

@app.get('/movers')
def market_movers():
    return MOVERS
""",
    )
    task1_starter = _app_source(
        {"market_movers": movers},
        """
@app.get('/movers')
def market_movers():
    return [{'symbol': 'TODO', 'change_pct': None, 'volume': None}]
""",
    )

    auctions = _widget(
        "Treasury Auction Calendar",
        "/auctions",
        "table",
        fields=(
            ("auction_date", "Auction Date"),
            ("security", "Security"),
            ("size_billion", "Size ($bn)"),
        ),
    )
    task2_oracle = _app_source(
        {"auction_calendar": auctions},
        """
@app.get('/auctions')
def auction_calendar():
    return [
        {'auction_date': '2026-08-11', 'security': '3-Year Note', 'size_billion': 58.0},
        {'auction_date': '2026-08-12', 'security': '10-Year Note', 'size_billion': 42.0},
    ]
""",
    )
    task2_starter = _app_source(
        {"auction_calendar": auctions},
        """
@app.get('/auctions')
def auction_calendar():
    return [{'date': '2026-08-11', 'instrument': '3Y', 'amount': 58.0}]
""",
    )

    risk_widgets = {
        "risk_score": _widget("Portfolio Risk Score", "/risk/score", "metric"),
        "risk_commentary": _widget("Risk Commentary", "/risk/commentary", "markdown"),
    }
    task3_oracle = _app_source(
        risk_widgets,
        """
@app.get('/risk/score')
def risk_score():
    return {'label': 'Portfolio risk', 'value': risk_summary()['score'], 'unit': '/100'}

@app.get('/risk/commentary')
def risk_commentary():
    return {'markdown': risk_summary()['commentary']}
""",
        extra_imports="from analytics import risk_summary\n",
    )
    task3_starter = _app_source(
        risk_widgets,
        """
@app.get('/risk/score')
def risk_score():
    return {'label': 'Portfolio risk', 'value': 'TODO'}

@app.get('/risk/commentary')
def risk_commentary():
    return {'markdown': 'Coming soon'}
""",
    )

    chart_data = {
        "categoryField": "quarter",
        "series": [{"field": "revenue"}, {"field": "operating_margin"}],
    }
    revenue_widget = _widget(
        "Revenue and Margin Trend", "/revenue-trend", "chart", data=chart_data
    )
    task4_oracle = _app_source(
        {"revenue_trend": revenue_widget},
        """
@app.get('/revenue-trend')
def revenue_trend():
    return [
        {'quarter': 'Q1 2026', 'revenue': 12.4, 'operating_margin': 18.2},
        {'quarter': 'Q2 2026', 'revenue': 13.1, 'operating_margin': 19.0},
        {'quarter': 'Q3 2026', 'revenue': 14.0, 'operating_margin': 20.1},
    ]
""",
    )
    task4_starter = _app_source(
        {"revenue_trend": revenue_widget},
        """
@app.get('/revenue-trend')
def revenue_trend():
    return []
""",
    )

    price_params = [
        {"paramName": "ticker", "label": "Ticker", "type": "ticker", "value": "AAPL"},
        {"paramName": "start_date", "label": "Start", "type": "date", "value": "2026-01-01"},
        {"paramName": "end_date", "label": "End", "type": "date", "value": "2026-01-31"},
    ]
    prices = _widget(
        "Historical Prices",
        "/prices",
        "table",
        fields=(("ticker", "Ticker"), ("date", "Date"), ("close", "Close")),
        params=price_params,
    )
    task5_oracle = _app_source(
        {"historical_prices": prices},
        """
@app.get('/prices')
def historical_prices(ticker: str, start_date: str, end_date: str):
    return [
        {'ticker': ticker.upper(), 'date': start_date, 'close': 101.25},
        {'ticker': ticker.upper(), 'date': end_date, 'close': 103.50},
    ]
""",
    )
    task5_starter = _app_source(
        {"historical_prices": prices},
        """
@app.get('/prices')
def historical_prices(ticker: str = 'AAPL', start_date: str = '', end_date: str = ''):
    return [{'ticker': 'AAPL', 'date': '2026-01-01', 'close': 100.0}]
""",
    )

    form_params = [
        {
            "paramName": "add_symbol",
            "label": "Add symbol",
            "type": "form",
            "endpoint": "/watchlist/add",
            "method": "POST",
            "inputParams": [
                {"paramName": "symbol", "label": "Symbol", "type": "text"},
                {"paramName": "note", "label": "Note", "type": "text"},
            ],
        }
    ]
    watchlist = _widget(
        "Research Watchlist",
        "/watchlist",
        "table",
        fields=(("symbol", "Symbol"), ("note", "Note")),
        params=form_params,
    )
    task6_oracle = _app_source(
        {"research_watchlist": watchlist},
        """
class WatchlistItem(BaseModel):
    symbol: str
    note: str

WATCHLIST = [{'symbol': 'AAPL', 'note': 'Earnings review'}]

@app.get('/watchlist')
def get_watchlist():
    return WATCHLIST

@app.post('/watchlist/add')
def add_watchlist(item: WatchlistItem):
    row = {'symbol': item.symbol.upper(), 'note': item.note}
    WATCHLIST.append(row)
    return {'accepted': True, **row}
""",
    )
    task6_starter = _app_source(
        {"research_watchlist": watchlist},
        """
WATCHLIST = [{'symbol': 'AAPL', 'note': 'Earnings review'}]

@app.get('/watchlist')
def get_watchlist():
    return WATCHLIST

@app.post('/watchlist/add')
def add_watchlist(payload: dict):
    return {'accepted': True}
""",
    )

    order_fields = (
        ("order_id", "Order ID"),
        ("symbol", "Symbol"),
        ("price", "Price"),
        ("status", "Status"),
    )
    orders = _widget("Order Search", "/orders/search", "ssrm_table", fields=order_fields)
    orders["data"]["dataKey"] = "rows"
    order_rows = [
        {"order_id": "O-1", "symbol": "AAPL", "price": 185.0, "status": "open"},
        {"order_id": "O-2", "symbol": "MSFT", "price": 420.0, "status": "filled"},
        {"order_id": "O-3", "symbol": "NVDA", "price": 900.0, "status": "open"},
        {"order_id": "O-4", "symbol": "TSLA", "price": 250.0, "status": "open"},
        {"order_id": "O-5", "symbol": "JPM", "price": 210.0, "status": "filled"},
    ]
    task7_oracle = _app_source(
        {"order_search": orders},
        f"""
ORDERS = {pprint.pformat(order_rows, sort_dicts=True)}

@app.post('/orders/search')
def order_search(payload: dict):
    rows = list(ORDERS)
    sort_model = payload.get('sortModel') or []
    if sort_model:
        key = sort_model[0].get('colId', 'order_id')
        rows.sort(key=lambda row: str(row.get(key, '')), reverse=sort_model[0].get('sort') == 'desc')
    start = max(int(payload.get('startRow', 0)), 0)
    end = max(int(payload.get('endRow', start + 100)), start)
    page = rows[start:end]
    return {{
        'rows': page,
        'totalRows': len(rows),
        'page_size': len(page),
        'first_symbol': page[0]['symbol'] if page else None,
    }}
""",
    )
    task7_starter = _app_source(
        {"order_search": orders},
        f"""
ORDERS = {pprint.pformat(order_rows, sort_dicts=True)}

@app.post('/orders/search')
def order_search(payload: dict):
    return {{'rows': ORDERS, 'totalRows': len(ORDERS), 'page_size': len(ORDERS), 'first_symbol': ORDERS[0]['symbol']}}
""",
    )

    portfolio_widgets = {
        "portfolio_summary": _widget("Portfolio Summary", "/portfolio/summary", "metric"),
        "portfolio_positions": _widget(
            "Portfolio Positions",
            "/portfolio/positions",
            "table",
            fields=(("symbol", "Symbol"), ("weight", "Weight"), ("market_value", "Market Value")),
        ),
    }
    portfolio_app = _layout_app("Portfolio Monitor", tuple(portfolio_widgets))
    task8_oracle = _app_source(
        portfolio_widgets,
        """
@app.get('/portfolio/summary')
def portfolio_summary():
    return {'label': 'Portfolio value', 'value': 1250000, 'currency': 'USD'}

@app.get('/portfolio/positions')
def portfolio_positions():
    return [
        {'symbol': 'AAPL', 'weight': 0.32, 'market_value': 400000},
        {'symbol': 'MSFT', 'weight': 0.28, 'market_value': 350000},
    ]
""",
        apps=portfolio_app,
    )
    task8_starter = _app_source(
        portfolio_widgets,
        """
@app.get('/portfolio/summary')
def portfolio_summary():
    return {'label': 'Portfolio value', 'value': 'TODO'}

@app.get('/portfolio/positions')
def portfolio_positions():
    return []
""",
        apps=[
            {
                "template_id": "portfolio-monitor",
                "name": "Portfolio Monitor",
                "tabs": {
                    "main": {
                        "id": "main",
                        "name": "Overview",
                        "layout": [
                            {"i": "missing_widget", "x": 0, "y": 0, "w": 20, "h": 10}
                        ],
                    }
                },
            }
        ],
    )

    repair_widgets = {
        "service_status": _widget("Service Status", "/status", "metric"),
        "incident_queue": _widget(
            "Incident Queue",
            "/incidents",
            "table",
            fields=(("incident_id", "Incident"), ("severity", "Severity"), ("owner", "Owner")),
        ),
    }
    task9_oracle = _app_source(
        repair_widgets,
        """
@app.get('/status')
def service_status():
    return {'label': 'API status', 'value': 'operational'}

@app.get('/incidents')
def incidents():
    return [
        {'incident_id': 'INC-104', 'severity': 'high', 'owner': 'platform'},
        {'incident_id': 'INC-105', 'severity': 'medium', 'owner': 'data'},
    ]
""",
    )
    task9_starter = _app_source(
        repair_widgets,
        """
@app.get('/status')
def service_status():
    return {'label': 'API status', 'value': 'operational'}

@app.get('/incidents')
def incidents():
    raise HTTPException(status_code=500, detail='database mapping failed')
""",
        cors=False,
    )

    trades = _widget(
        "Client Trades",
        "/client-trades",
        "table",
        fields=(("client_name", "Client"), ("notional", "Notional"), ("side", "Side")),
    )
    task10_oracle = _app_source(
        {"client_trades": trades},
        """
@app.get('/client-trades')
def client_trades():
    return [
        {'client_name': 'Northstar Fund', 'notional': 2500000, 'side': 'buy'},
        {'client_name': 'Atlas Capital', 'notional': 1750000, 'side': 'sell'},
    ]
""",
    )
    task10_starter = _app_source(
        {"client_trades": trades},
        """
@app.get('/client-trades')
def client_trades():
    return [{'customer': 'Northstar Fund', 'amount': 2500000, 'direction': 'buy'}]
""",
    )

    equities = _widget(
        "Equity Snapshot",
        "/equities",
        "table",
        fields=(("symbol", "Symbol"), ("price", "Price"), ("sector", "Sector")),
    )
    credit = _widget(
        "Credit Spreads",
        "/credit-spreads",
        "table",
        fields=(("issuer", "Issuer"), ("rating", "Rating"), ("spread_bps", "Spread bps")),
    )
    task11_oracle = _app_source(
        {"equity_snapshot": equities, "credit_spreads": credit},
        """
@app.get('/equities')
def equities():
    return [{'symbol': 'AAPL', 'price': 201.5, 'sector': 'Technology'}]

@app.get('/credit-spreads')
def credit_spreads():
    return [
        {'issuer': 'Acme Industrial', 'rating': 'BBB', 'spread_bps': 142},
        {'issuer': 'Northstar Bank', 'rating': 'A', 'spread_bps': 88},
    ]
""",
    )
    task11_starter = _app_source(
        {"equity_snapshot": equities},
        """
@app.get('/equities')
def equities():
    return [{'symbol': 'AAPL', 'price': 201.5, 'sector': 'Technology'}]
""",
    )

    product_widgets = {
        "risk_overview": _widget("Risk Overview", "/risk/overview", "metric"),
        "factor_exposures": _widget(
            "Factor Exposures",
            "/risk/exposures",
            "table",
            fields=(("factor", "Factor"), ("exposure", "Exposure"), ("limit", "Limit")),
        ),
    }
    product_apps = _layout_app("Risk Command Center", tuple(product_widgets))
    task12_oracle = _app_source(
        product_widgets,
        """
@app.get('/risk/overview')
def risk_overview():
    return {'label': 'Risk utilization', 'value': 63.4, 'status': 'within limit'}

@app.get('/risk/exposures')
def risk_exposures():
    return [
        {'factor': 'Technology', 'exposure': 0.28, 'limit': 0.35},
        {'factor': 'Rates duration', 'exposure': 4.2, 'limit': 6.0},
    ]
""",
        apps=product_apps,
        health={"ok": True, "service": "risk-command-center", "version": "1.0.0"},
    )
    task12_starter = _app_source(
        {},
        """
# Implement the product endpoints described in TASK_BRIEF.md.
""",
        apps=[],
        health={"ok": True, "service": "starter"},
    )

    return (
        Definition(
            "market_movers_table",
            "Implement a market movers table backend",
            "Implement the existing Market Movers table contract. Serve widgets.json with the "
            "declared symbol, percentage-change, and volume columns; implement GET /movers with "
            "at least two typed, non-placeholder rows; preserve CORS, health, and the pinned tests.",
            "easy",
            "train",
            ("single-table", "implementation"),
            task1_starter,
            {"app.py": task1_oracle},
            _tests(
                """
def test_market_movers_contract():
    widgets = client.get('/widgets.json').json()
    assert 'market_movers' in widgets
    rows = client.get('/movers').json()
    assert len(rows) >= 2
    assert {'symbol', 'change_pct', 'volume'} <= rows[0].keys()
    assert isinstance(rows[0]['volume'], int)
"""
            ),
            (
                _probe(
                    "market movers",
                    "/movers",
                    "market_movers",
                    ("symbol", "change_pct", "volume"),
                    types={"symbol": "string", "change_pct": "number", "volume": "integer"},
                    minimum=2,
                ),
            ),
        ),
        Definition(
            "treasury_auctions_table",
            "Implement a Treasury auction calendar",
            "Complete the Treasury auction calendar backend. Keep the supplied OpenBB table "
            "manifest and return dated security rows with numeric auction size in billions from "
            "GET /auctions. Leave the health endpoint, CORS, and tests operational.",
            "easy",
            "train",
            ("single-table", "implementation"),
            task2_starter,
            {"app.py": task2_oracle},
            _tests(
                """
def test_auction_contract():
    rows = client.get('/auctions').json()
    assert len(rows) == 2
    assert rows[0]['auction_date'].startswith('2026-')
    assert isinstance(rows[0]['size_billion'], float)
    assert 'Note' in rows[0]['security']
"""
            ),
            (
                _probe(
                    "auction rows",
                    "/auctions",
                    "auction_calendar",
                    ("auction_date", "security", "size_billion"),
                    types={"auction_date": "string", "security": "string", "size_billion": "number"},
                    minimum=2,
                ),
            ),
        ),
        Definition(
            "risk_metric_and_commentary",
            "Build shared risk metric and commentary widgets",
            "Finish both supplied risk widgets. Put the shared portfolio-risk calculation in "
            "analytics.py, then serve a numeric metric from /risk/score and meaningful markdown "
            "from /risk/commentary. Both endpoints must use that shared module and keep CORS/tests green.",
            "easy",
            "train",
            ("multi-widget", "shared-module"),
            task3_starter,
            {
                "app.py": task3_oracle,
                "analytics.py": (
                    "def risk_summary():\n"
                    "    return {'score': 64.5, 'commentary': '**Moderate risk:** concentration "
                    "is elevated in technology, while duration remains within policy.'}\n"
                ),
            },
            _tests(
                """
def test_shared_risk_outputs():
    score = client.get('/risk/score').json()
    note = client.get('/risk/commentary').json()
    assert isinstance(score['value'], float)
    assert 0 < score['value'] < 100
    assert 'risk' in note['markdown'].lower()
    assert len(note['markdown']) > 30
"""
            ),
            (
                _probe(
                    "risk score",
                    "/risk/score",
                    "risk_score",
                    ("label", "value"),
                    types={"label": "string", "value": "number"},
                ),
                _probe(
                    "risk commentary",
                    "/risk/commentary",
                    "risk_commentary",
                    ("markdown",),
                    types={"markdown": "string"},
                ),
            ),
            extra_starter_files={
                "analytics.py": "def risk_summary():\n    return {'score': None, 'commentary': 'TODO'}\n"
            },
        ),
        Definition(
            "revenue_margin_chart",
            "Build a revenue and margin chart endpoint",
            "A finance leader needs a chart-ready quarterly view of revenue and operating margin. "
            "Complete the supplied backend so Workspace can construct both declared series from "
            "at least three ordered quarters. Retain the repository's interface and quality gates.",
            "medium",
            "train",
            ("chart", "implementation"),
            task4_starter,
            {"app.py": task4_oracle},
            _tests(
                """
def test_chart_series_are_constructable():
    rows = client.get('/revenue-trend').json()
    assert len(rows) >= 3
    assert all({'quarter', 'revenue', 'operating_margin'} <= row.keys() for row in rows)
    assert all(isinstance(row['revenue'], float) for row in rows)
"""
            ),
            (
                _probe(
                    "quarterly chart series",
                    "/revenue-trend",
                    "revenue_trend",
                    ("quarter", "revenue", "operating_margin"),
                    types={"quarter": "string", "revenue": "number", "operating_margin": "number"},
                    minimum=3,
                ),
            ),
        ),
        Definition(
            "parameterized_price_history",
            "Implement parameterized price history",
            "An equity analyst needs historical prices filtered by ticker and inclusive date range. "
            "Honor the supplied ticker, start_date, and end_date query contract at the HTTP layer; "
            "the response must make the selected instrument and date boundaries unambiguous.",
            "medium",
            "validation",
            ("parameters", "dates", "ticker"),
            task5_starter,
            {"app.py": task5_oracle},
            _tests(
                """
def test_query_parameters_drive_payload():
    rows = client.get('/prices', params={'ticker': 'MSFT', 'start_date': '2026-02-01', 'end_date': '2026-02-28'}).json()
    assert {row['ticker'] for row in rows} == {'MSFT'}
    assert rows[0]['date'] == '2026-02-01'
    assert rows[-1]['date'] == '2026-02-28'
"""
            ),
            (
                _probe(
                    "MSFT February",
                    "/prices",
                    "historical_prices",
                    ("ticker", "date", "close"),
                    query={"ticker": "MSFT", "start_date": "2026-02-01", "end_date": "2026-02-28"},
                    types={"ticker": "string", "date": "string", "close": "number"},
                    expected={"ticker": "MSFT", "date": "2026-02-28"},
                    minimum=2,
                ),
                _probe(
                    "NVDA March",
                    "/prices",
                    "historical_prices",
                    ("ticker", "date", "close"),
                    query={"ticker": "NVDA", "start_date": "2026-03-03", "end_date": "2026-03-21"},
                    expected={"ticker": "NVDA", "date": "2026-03-21"},
                    minimum=2,
                ),
            ),
        ),
        Definition(
            "mutable_watchlist_form",
            "Implement a stateful watchlist form",
            "A research desk needs to add symbols and notes through a Workspace form and see each "
            "accepted submission in the table immediately afterward. Implement the declared POST "
            "contract with in-process state; normalize tickers and preserve existing entries.",
            "medium",
            "validation",
            ("form", "post", "state"),
            task6_starter,
            {"app.py": task6_oracle},
            _tests(
                """
def test_submission_mutates_watchlist():
    response = client.post('/watchlist/add', json={'symbol': 'tsla', 'note': 'Delivery watch'})
    assert response.status_code == 200
    rows = client.get('/watchlist').json()
    assert {'symbol': 'TSLA', 'note': 'Delivery watch'} in rows
"""
            ),
            (
                _probe(
                    "initial watchlist",
                    "/watchlist",
                    "research_watchlist",
                    ("symbol", "note"),
                    types={"symbol": "string", "note": "string"},
                ),
                _probe(
                    "submit watchlist",
                    "/watchlist/add",
                    None,
                    ("accepted", "symbol", "note"),
                    method="POST",
                    body={"symbol": "tsla", "note": "Delivery watch"},
                    expected={"accepted": True, "symbol": "TSLA"},
                ),
                _probe(
                    "watchlist persisted",
                    "/watchlist",
                    "research_watchlist",
                    ("symbol", "note"),
                    expected={"symbol": "TSLA", "note": "Delivery watch"},
                    minimum=2,
                ),
            ),
        ),
        Definition(
            "server_side_order_grid",
            "Implement server-side order pagination and sorting",
            "Execution operations needs a responsive server-side order grid. Implement POST-backed "
            "pagination and single-column sorting from the supplied row-model request. Return the "
            "requested slice, total row count, page size, and first visible symbol accurately.",
            "hard",
            "test",
            ("ssrm", "pagination", "sorting"),
            task7_starter,
            {"app.py": task7_oracle},
            _tests(
                """
def test_grid_honors_sort_and_page():
    payload = {'startRow': 1, 'endRow': 3, 'sortModel': [{'colId': 'symbol', 'sort': 'desc'}]}
    result = client.post('/orders/search', json=payload).json()
    assert result['totalRows'] == 5
    assert result['page_size'] == 2
    assert result['first_symbol'] == 'NVDA'
    assert [row['symbol'] for row in result['rows']] == ['NVDA', 'MSFT']
"""
            ),
            (
                _probe(
                    "sorted order page",
                    "/orders/search",
                    "order_search",
                    ("order_id", "symbol", "price", "status"),
                    method="POST",
                    body={"startRow": 1, "endRow": 3, "sortModel": [{"colId": "symbol", "sort": "desc"}]},
                    types={"order_id": "string", "symbol": "string", "price": "number", "status": "string"},
                    expected={"totalRows": 5, "page_size": 2, "first_symbol": "NVDA"},
                    minimum=2,
                ),
            ),
        ),
        Definition(
            "portfolio_monitor_app",
            "Build a multi-widget portfolio app",
            "A portfolio manager needs one installable app combining a portfolio-value summary and "
            "position detail. Finish both data contracts and apps.json so its non-overlapping layout "
            "references only widgets this backend actually serves.",
            "medium",
            "train",
            ("apps-json", "multi-widget", "layout"),
            task8_starter,
            {"app.py": task8_oracle},
            _tests(
                """
def test_app_references_served_widgets():
    widgets = client.get('/widgets.json').json()
    app_data = client.get('/apps.json').json()[0]
    refs = {item['i'] for item in app_data['tabs']['main']['layout']}
    assert refs == set(widgets)
    assert isinstance(client.get('/portfolio/summary').json()['value'], int)
    assert client.get('/portfolio/positions').json()[0]['symbol'] == 'AAPL'
"""
            ),
            (
                _probe(
                    "portfolio summary",
                    "/portfolio/summary",
                    "portfolio_summary",
                    ("label", "value", "currency"),
                    types={"label": "string", "value": "number", "currency": "string"},
                ),
                _probe(
                    "portfolio positions",
                    "/portfolio/positions",
                    "portfolio_positions",
                    ("symbol", "weight", "market_value"),
                    types={"symbol": "string", "weight": "number", "market_value": "number"},
                    minimum=2,
                ),
            ),
            require_apps=True,
        ),
        Definition(
            "repair_incident_backend",
            "Repair an incident backend without regressions",
            "Diagnose and repair the supplied incident backend. The incident queue currently fails "
            "and browser access is broken, while service status already works. Restore typed incident "
            "rows and CORS without regressing the healthy status endpoint or changing public ids.",
            "medium",
            "validation",
            ("repair", "cors", "regression"),
            task9_starter,
            {"app.py": task9_oracle},
            _tests(
                """
def test_existing_status_stays_green():
    assert client.get('/status').json() == {'label': 'API status', 'value': 'operational'}

def test_incident_queue_is_repaired():
    response = client.get('/incidents')
    assert response.status_code == 200
    assert {'incident_id', 'severity', 'owner'} <= response.json()[0].keys()
"""
            ),
            (
                _probe(
                    "existing status",
                    "/status",
                    "service_status",
                    ("label", "value"),
                    expected={"value": "operational"},
                ),
                _probe(
                    "repaired incidents",
                    "/incidents",
                    "incident_queue",
                    ("incident_id", "severity", "owner"),
                    types={"incident_id": "string", "severity": "string", "owner": "string"},
                    minimum=2,
                ),
            ),
        ),
        Definition(
            "repair_trade_column_contract",
            "Reconcile a trade table manifest and payload",
            "The client-trades widget declares business columns the endpoint never returns. Reconcile "
            "the implementation and manifest into one coherent contract for client name, notional, "
            "and side. Keep the public widget usable and the test suite meaningful.",
            "medium",
            "test",
            ("repair", "manifest", "columns"),
            task10_starter,
            {"app.py": task10_oracle},
            _tests(
                """
def test_manifest_columns_exist_in_payload():
    widget = client.get('/widgets.json').json()['client_trades']
    fields = {item['field'] for item in widget['data']['table']['columnsDefs']}
    rows = client.get('/client-trades').json()
    assert fields == {'client_name', 'notional', 'side'}
    assert all(fields <= row.keys() for row in rows)
"""
            ),
            (
                _probe(
                    "client trade rows",
                    "/client-trades",
                    "client_trades",
                    ("client_name", "notional", "side"),
                    types={"client_name": "string", "notional": "number", "side": "string"},
                    minimum=2,
                ),
            ),
        ),
        Definition(
            "extend_equities_with_credit",
            "Extend an equities backend with credit data",
            "Extend the working equity backend for a cross-asset desk that now also needs issuer "
            "ratings and spread levels. Preserve every existing equity contract and test while adding "
            "a coherent second credit domain to widgets.json and the HTTP API.",
            "hard",
            "test",
            ("extend", "multi-domain", "regression"),
            task11_starter,
            {"app.py": task11_oracle},
            _tests(
                """
def test_existing_equity_domain_is_unchanged():
    assert client.get('/equities').json() == [{'symbol': 'AAPL', 'price': 201.5, 'sector': 'Technology'}]

def test_credit_domain_is_added():
    widgets = client.get('/widgets.json').json()
    assert {'equity_snapshot', 'credit_spreads'} <= widgets.keys()
    rows = client.get('/credit-spreads').json()
    assert len(rows) >= 2
    assert {'issuer', 'rating', 'spread_bps'} <= rows[0].keys()
"""
            ),
            (
                _probe(
                    "preserved equities",
                    "/equities",
                    "equity_snapshot",
                    ("symbol", "price", "sector"),
                    expected={"symbol": "AAPL"},
                ),
                _probe(
                    "new credit domain",
                    "/credit-spreads",
                    "credit_spreads",
                    ("issuer", "rating", "spread_bps"),
                    types={"issuer": "string", "rating": "string", "spread_bps": "integer"},
                    minimum=2,
                ),
            ),
        ),
        Definition(
            "risk_command_center_product",
            "Build a complete risk command center backend",
            "Ship a small risk command center for a portfolio team. It needs a production-style health "
            "contract, an at-a-glance risk utilization view, factor exposures with policy limits, and "
            "an installable Workspace app that lays out the experience cleanly. Leave real tests that "
            "protect the product behavior and keep the backend localhost-ready.",
            "hard",
            "test",
            ("mini-product", "apps-json", "health", "browser-flagship"),
            task12_starter,
            {"app.py": task12_oracle},
            _tests(
                """
def test_full_risk_product():
    health = client.get('/health').json()
    assert health['service'] == 'risk-command-center'
    assert health['version'] == '1.0.0'
    widgets = client.get('/widgets.json').json()
    assert set(widgets) == {'risk_overview', 'factor_exposures'}
    app_data = client.get('/apps.json').json()[0]
    assert app_data['name'] == 'Risk Command Center'
    assert isinstance(client.get('/risk/overview').json()['value'], float)
    assert len(client.get('/risk/exposures').json()) >= 2
"""
            ),
            (
                _probe(
                    "product health",
                    "/health",
                    None,
                    ("ok", "service", "version"),
                    expected={"ok": True, "service": "risk-command-center", "version": "1.0.0"},
                ),
                _probe(
                    "risk overview",
                    "/risk/overview",
                    "risk_overview",
                    ("label", "value", "status"),
                    types={"label": "string", "value": "number", "status": "string"},
                ),
                _probe(
                    "factor exposures",
                    "/risk/exposures",
                    "factor_exposures",
                    ("factor", "exposure", "limit"),
                    types={"factor": "string", "exposure": "number", "limit": "number"},
                    minimum=2,
                ),
            ),
            require_apps=True,
        ),
    )


def _pyproject(task_id: str) -> str:
    return f"""[project]
name = "workspace-bench-{task_id.replace('_', '-')}"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "fastapi==0.116.1",
  "httpx==0.28.1",
  "pytest==8.4.1",
  "uvicorn==0.35.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
"""


def _readme(definition: Definition) -> str:
    return f"""# {definition.title}

This is the starter repository for `{definition.task_id}`.

## Commands

```bash
uv sync
uv run uvicorn app:app --host 127.0.0.1 --port 8000
uv run pytest -q
```

The evaluator injects its own ephemeral port and requires CORS-compatible JSON responses.
Read `TASK_BRIEF.md` in an instantiated run for the business brief.
"""


def _task_payload(definition: Definition) -> JsonDict:
    fixture_root = f"fixtures/{definition.task_id}"
    return {
        "schema_version": SCHEMA_VERSION,
        "id": definition.task_id,
        "title": definition.title,
        "category": "repair" if "repair" in definition.tags else "platform",
        "family": "backend-code",
        "capability": "build-real-backend",
        "workflow": "custom-backend-development",
        "domain": "engineering",
        "subdomain": "openbb-custom-backends",
        "difficulty": definition.difficulty,
        "split": definition.split,
        "tags": ["build-openbb-backends", "experimental-v0", *definition.tags],
        "source": "WorkspaceBench Phase 10 authored code track",
        "novelty": f"Real-code backend task: {definition.task_id}",
        "prompt": definition.prompt,
        "business_terms": [],
        "fixtures": {"backends": []},
        "initial_state": {},
        "allowed_tools": ["filesystem", "shell"],
        "success": {},
        "oracle_tool_calls": [],
        "limits": {"max_turns": 40 if definition.difficulty == "hard" else 24},
        "code_task": {
            "schema_version": CODE_SCHEMA_VERSION,
            "starter_path": f"{fixture_root}/starter",
            "oracle_path": f"{fixture_root}/oracle",
            "install_command": INSTALL,
            "start_command": START,
            "test_command": TEST,
            "health_path": "/health",
            "require_apps": definition.require_apps,
            "probes": list(definition.probes),
            "startup_timeout_ms": 20000,
            "request_timeout_ms": 3000,
            "command_timeout_ms": 120000,
            "core_module": "app.py",
        },
    }


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    generated = definitions()
    if len(generated) != 12 or len({item.task_id for item in generated}) != 12:
        raise AssertionError("backend code suite must contain exactly 12 unique tasks")
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    _write_text(OUTPUT.parent / "__init__.py", '"""Experimental real-code backend suite."""')
    _write_text(OUTPUT / "__init__.py", '"""Generated backend-code task family."""')

    payloads: list[JsonDict] = []
    for definition in generated:
        payload = _task_payload(definition)
        payloads.append(payload)
        _write_text(
            OUTPUT / f"{definition.task_id}.json",
            json.dumps(payload, indent=2, sort_keys=True),
        )
        starter = OUTPUT / "fixtures" / definition.task_id / "starter"
        oracle = OUTPUT / "fixtures" / definition.task_id / "oracle"
        _write_text(starter / "pyproject.toml", _pyproject(definition.task_id))
        _write_text(starter / "README.md", _readme(definition))
        _write_text(starter / "app.py", definition.starter_app)
        _write_text(starter / "tests" / "test_backend.py", definition.tests)
        for relative, content in definition.extra_starter_files.items():
            _write_text(starter / relative, str(content))
        for relative, content in definition.oracle_files.items():
            _write_text(oracle / relative, str(content))

    digest = hashlib.sha256(
        b"".join(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
            for payload in payloads
        )
    ).hexdigest()
    manifest = {
        "suite_id": "build-openbb-backends",
        "visibility": "public",
        "default_split": "train",
        "description": (
            "Experimental v0 real-code track: agents edit pinned FastAPI starter repositories; "
            "the evaluator launches their process and grades manifests, HTTP behavior, and tests."
        ),
        "content_sha256": digest,
    }
    _write_text(OUTPUT.parent / "task_suite.json", json.dumps(manifest, indent=2, sort_keys=True))
    print(f"Wrote {len(payloads)} code tasks to {OUTPUT.parent}")
    print(f"content_sha256={digest}")


if __name__ == "__main__":
    main()
