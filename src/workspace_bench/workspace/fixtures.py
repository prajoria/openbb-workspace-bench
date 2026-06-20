"""Deterministic OpenBB Workspace fixture backends."""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
from typing import Any
from urllib.parse import parse_qs, urlparse

from workspace_bench.models import JsonDict


SYMBOLS = ["AAPL", "MSFT", "NVDA"]
SECTORS = ["Technology", "Communication Services", "Consumer Staples"]


PRICE_ROWS: dict[str, list[JsonDict]] = {
    "AAPL": [
        {"date": "2026-01-12", "close": 188.20, "return_pct": -0.011},
        {"date": "2026-01-13", "close": 190.85, "return_pct": 0.014},
        {"date": "2026-01-14", "close": 193.40, "return_pct": 0.013},
        {"date": "2026-01-15", "close": 196.10, "return_pct": 0.014},
    ],
    "MSFT": [
        {"date": "2026-01-12", "close": 442.10, "return_pct": 0.006},
        {"date": "2026-01-13", "close": 439.70, "return_pct": -0.005},
        {"date": "2026-01-14", "close": 446.30, "return_pct": 0.015},
        {"date": "2026-01-15", "close": 451.25, "return_pct": 0.011},
    ],
    "NVDA": [
        {"date": "2026-01-12", "close": 171.10, "return_pct": 0.018},
        {"date": "2026-01-13", "close": 175.90, "return_pct": 0.028},
        {"date": "2026-01-14", "close": 173.20, "return_pct": -0.015},
        {"date": "2026-01-15", "close": 179.45, "return_pct": 0.036},
    ],
}

NEWS_ROWS: dict[str, list[JsonDict]] = {
    "AAPL": [
        {
            "title": "Apple services revenue reaches new high",
            "date": "2026-01-15",
            "author": "Bench News",
            "excerpt": "Services and wearables offset slower hardware upgrades.",
            "body": "Fixture article for AAPL services mix.",
        },
        {
            "title": "Analysts focus on AI device roadmap",
            "date": "2026-01-14",
            "author": "Bench News",
            "excerpt": "Investors are watching on-device AI features and margins.",
            "body": "Fixture article for AAPL AI roadmap.",
        },
    ],
    "MSFT": [
        {
            "title": "Azure growth remains the center of the Microsoft debate",
            "date": "2026-01-15",
            "author": "Bench News",
            "excerpt": "Cloud revenue and AI infrastructure spending dominate estimates.",
            "body": "Fixture article for MSFT cloud growth.",
        }
    ],
    "NVDA": [
        {
            "title": "NVIDIA data center backlog expands",
            "date": "2026-01-15",
            "author": "Bench News",
            "excerpt": "Hyperscaler orders support the next two quarters of revenue.",
            "body": "Fixture article for NVDA backlog.",
        }
    ],
}

ESTIMATE_ROWS: dict[str, list[JsonDict]] = {
    "AAPL": [
        {"quarter": "2026Q1", "eps_estimate": 2.31, "revenue_estimate_b": 94.8},
        {"quarter": "2026Q2", "eps_estimate": 1.78, "revenue_estimate_b": 88.5},
        {"quarter": "2026Q3", "eps_estimate": 1.63, "revenue_estimate_b": 84.1},
    ],
    "MSFT": [
        {"quarter": "2026Q1", "eps_estimate": 3.42, "revenue_estimate_b": 71.2},
        {"quarter": "2026Q2", "eps_estimate": 3.55, "revenue_estimate_b": 73.0},
        {"quarter": "2026Q3", "eps_estimate": 3.72, "revenue_estimate_b": 75.6},
    ],
    "NVDA": [
        {"quarter": "2026Q1", "eps_estimate": 1.18, "revenue_estimate_b": 39.4},
        {"quarter": "2026Q2", "eps_estimate": 1.26, "revenue_estimate_b": 42.1},
        {"quarter": "2026Q3", "eps_estimate": 1.33, "revenue_estimate_b": 45.7},
    ],
}

FUNDAMENTAL_ROWS: dict[str, list[JsonDict]] = {
    "AAPL": [
        {"metric": "gross_margin", "value": 0.462},
        {"metric": "net_cash_b", "value": 54.0},
        {"metric": "buyback_yield", "value": 0.034},
    ],
    "MSFT": [
        {"metric": "gross_margin", "value": 0.694},
        {"metric": "net_cash_b", "value": 67.5},
        {"metric": "buyback_yield", "value": 0.008},
    ],
    "NVDA": [
        {"metric": "gross_margin", "value": 0.742},
        {"metric": "net_cash_b", "value": 31.3},
        {"metric": "buyback_yield", "value": 0.004},
    ],
}

MACRO_SERIES_ROWS: dict[str, list[JsonDict]] = {
    "FEDFUNDS": [
        {"date": "2025-10-31", "value": 4.38},
        {"date": "2025-11-30", "value": 4.25},
        {"date": "2025-12-31", "value": 4.12},
    ],
    "DGS2": [
        {"date": "2026-01-13", "value": 3.82},
        {"date": "2026-01-14", "value": 3.79},
        {"date": "2026-01-15", "value": 3.75},
    ],
    "DGS10": [
        {"date": "2026-01-13", "value": 4.21},
        {"date": "2026-01-14", "value": 4.18},
        {"date": "2026-01-15", "value": 4.16},
    ],
    "CPIAUCSL": [
        {"date": "2025-10-31", "value": 321.1},
        {"date": "2025-11-30", "value": 321.8},
        {"date": "2025-12-31", "value": 322.4},
    ],
}

YIELD_CURVE_ROWS = [
    {"tenor": "3M", "yield": 4.02},
    {"tenor": "2Y", "yield": 3.75},
    {"tenor": "5Y", "yield": 3.92},
    {"tenor": "10Y", "yield": 4.16},
    {"tenor": "30Y", "yield": 4.48},
]

HOLDINGS_ROWS = [
    {
        "symbol": "AAPL",
        "sector": "Technology",
        "market_value": 220000,
        "weight": 0.28,
        "day_return": 0.014,
    },
    {
        "symbol": "MSFT",
        "sector": "Technology",
        "market_value": 265000,
        "weight": 0.34,
        "day_return": 0.011,
    },
    {
        "symbol": "NVDA",
        "sector": "Technology",
        "market_value": 185000,
        "weight": 0.24,
        "day_return": 0.036,
    },
    {
        "symbol": "KO",
        "sector": "Consumer Staples",
        "market_value": 110000,
        "weight": 0.14,
        "day_return": -0.003,
    },
]

EXPOSURE_ROWS = [
    {"sector": "Technology", "weight": 0.86, "market_value": 670000},
    {"sector": "Consumer Staples", "weight": 0.14, "market_value": 110000},
]

RISK_ROWS = [
    {"metric": "portfolio_beta", "value": 1.18},
    {"metric": "one_day_var_95", "value": -18200},
    {"metric": "top_position_weight", "value": 0.34},
]


@dataclass(frozen=True)
class FixtureBackend:
    """Deterministic Workspace backend fixture."""

    slug: str
    name: str
    widgets: dict[str, JsonDict]
    apps: list[JsonDict]
    default_url: str

    def widgets_json(self) -> JsonDict:
        return copy.deepcopy(self.widgets)

    def apps_json(self) -> list[JsonDict]:
        return copy.deepcopy(self.apps)

    def list_available_widgets(self) -> list[JsonDict]:
        return [
            {
                "origin": self.name,
                "widget_id": widget_id,
                "name": definition["name"],
                "description": definition.get("description", ""),
                "type": definition.get("type"),
                "category": definition.get("category"),
                "grid_data": definition.get("gridData"),
            }
            for widget_id, definition in self.widgets.items()
        ]

    def get_widget_schema(self, widget_id: str) -> JsonDict:
        if widget_id not in self.widgets:
            raise KeyError(f"Unknown widget_id {widget_id!r} for backend {self.name}")
        payload = copy.deepcopy(self.widgets[widget_id])
        payload["origin"] = self.name
        payload["widget_id"] = widget_id
        payload["grid_data"] = payload.get("gridData")
        return payload

    def get_param_options(
        self, widget_id: str, param_name: str, data_args: JsonDict | None = None
    ) -> list[JsonDict]:
        if widget_id:
            self.get_widget_schema(widget_id)
        if param_name == "symbol":
            return [{"label": symbol, "value": symbol} for symbol in SYMBOLS]
        if param_name == "series":
            return [
                {"label": "Fed Funds", "value": "FEDFUNDS"},
                {"label": "2Y Treasury", "value": "DGS2"},
                {"label": "10Y Treasury", "value": "DGS10"},
                {"label": "CPI", "value": "CPIAUCSL"},
            ]
        if param_name == "sector":
            return [{"label": sector, "value": sector} for sector in SECTORS]
        if widget_id and widget_id in self.widgets:
            schema = self.widgets[widget_id]
            for param in schema.get("params", []) or []:
                if param.get("paramName") == param_name:
                    options = param.get("options") or []
                    if isinstance(options, list):
                        return copy.deepcopy(options)
        return []

    def fetch_widget_data(
        self, widget_id: str, data_args: JsonDict | None = None
    ) -> Any:
        data_args = data_args or {}
        symbol = str(data_args.get("symbol", "AAPL")).upper()
        series = str(data_args.get("series", "FEDFUNDS")).upper()
        limit = int(data_args.get("limit", 10))

        if widget_id == "price_performance":
            return copy.deepcopy(PRICE_ROWS.get(symbol, []))
        if widget_id == "latest_news":
            return copy.deepcopy(NEWS_ROWS.get(symbol, [])[:limit])
        if widget_id == "estimate_history":
            return copy.deepcopy(ESTIMATE_ROWS.get(symbol, []))
        if widget_id == "fundamental_metrics":
            return copy.deepcopy(FUNDAMENTAL_ROWS.get(symbol, []))
        if widget_id == "macro_timeseries":
            return copy.deepcopy(MACRO_SERIES_ROWS.get(series, []))
        if widget_id == "yield_curve":
            return copy.deepcopy(YIELD_CURVE_ROWS)
        if widget_id == "holdings_table":
            return copy.deepcopy(HOLDINGS_ROWS)
        if widget_id == "sector_exposure":
            return copy.deepcopy(EXPOSURE_ROWS)
        if widget_id == "risk_metrics":
            return copy.deepcopy(RISK_ROWS)
        if widget_id in self.widgets:
            return _generic_widget_data(widget_id, self.widgets[widget_id], data_args)
        raise KeyError(f"Unknown widget data endpoint for {widget_id!r}")

    def fetch_http_path(self, path: str, query: JsonDict) -> Any:
        if path == "/widgets.json":
            return self.widgets_json()
        if path == "/apps.json":
            return self.apps_json()
        if path == "/symbols":
            return self.get_param_options("", "symbol")
        if path == "/series":
            return self.get_param_options("", "series")
        for widget_id, definition in self.widgets.items():
            if definition.get("endpoint") == path:
                return self.fetch_widget_data(widget_id, query)
        raise KeyError(f"Unknown fixture path {path}")


def _symbol_param(default: str = "AAPL") -> JsonDict:
    return {
        "paramName": "symbol",
        "type": "endpoint",
        "label": "Symbol",
        "description": "Public company ticker symbol.",
        "value": default,
        "optionsEndpoint": "/symbols",
        "requires_options_lookup": True,
    }


def _series_param(default: str = "FEDFUNDS") -> JsonDict:
    return {
        "paramName": "series",
        "type": "endpoint",
        "label": "Series",
        "description": "Macroeconomic time-series identifier.",
        "value": default,
        "optionsEndpoint": "/series",
        "requires_options_lookup": True,
    }


def _limit_param(default: int = 5) -> JsonDict:
    return {
        "paramName": "limit",
        "type": "number",
        "label": "Limit",
        "description": "Maximum number of rows to return.",
        "value": default,
    }


def _table_columns(fields: list[tuple[str, str, str]]) -> JsonDict:
    return {
        "table": {
            "columnsDefs": [
                {"field": field, "headerName": header, "cellDataType": kind}
                for field, header, kind in fields
            ]
        }
    }


def build_equities_backend(url: str = "http://127.0.0.1:9101") -> FixtureBackend:
    widgets = {
        "price_performance": {
            "name": "Price Performance",
            "description": "Daily closing prices and return percentages for US equities.",
            "type": "table",
            "endpoint": "/price-performance",
            "category": "Equities",
            "gridData": {"w": 20, "h": 12},
            "params": [_symbol_param()],
            "data": _table_columns(
                [
                    ("date", "Date", "dateString"),
                    ("close", "Close", "number"),
                    ("return_pct", "Return", "number"),
                ]
            ),
        },
        "latest_news": {
            "name": "Latest News",
            "description": "Recent company news articles for the selected ticker.",
            "type": "newsfeed",
            "endpoint": "/latest-news",
            "category": "Equities",
            "gridData": {"w": 20, "h": 10},
            "params": [_symbol_param(), _limit_param()],
        },
        "estimate_history": {
            "name": "Estimate History",
            "description": "Quarterly EPS and revenue estimates for the selected ticker.",
            "type": "table",
            "endpoint": "/estimate-history",
            "category": "Equities",
            "gridData": {"w": 20, "h": 12},
            "params": [_symbol_param()],
            "data": _table_columns(
                [
                    ("quarter", "Quarter", "text"),
                    ("eps_estimate", "EPS Estimate", "number"),
                    ("revenue_estimate_b", "Revenue Estimate ($B)", "number"),
                ]
            ),
        },
        "fundamental_metrics": {
            "name": "Fundamental Metrics",
            "description": "Gross margin, net cash, and buyback metrics for a ticker.",
            "type": "metric",
            "endpoint": "/fundamental-metrics",
            "category": "Equities",
            "gridData": {"w": 10, "h": 8},
            "params": [_symbol_param()],
        },
    }
    apps = [
        {
            "name": "Equity Earnings Review",
            "template_id": "equity-earnings-review",
            "description": "Two-tab earnings dashboard with prices, news, estimates, and fundamentals.",
            "allowCustomization": True,
            "tabs": {
                "overview": {
                    "id": "overview",
                    "name": "Overview",
                    "layout": [
                        {
                            "i": "price_performance",
                            "x": 0,
                            "y": 2,
                            "w": 20,
                            "h": 12,
                            "state": {"params": {"symbol": "AAPL"}},
                        },
                        {
                            "i": "latest_news",
                            "x": 20,
                            "y": 2,
                            "w": 20,
                            "h": 12,
                            "state": {"params": {"symbol": "AAPL", "limit": 5}},
                        },
                    ],
                },
                "estimates": {
                    "id": "estimates",
                    "name": "Estimates",
                    "layout": [
                        {
                            "i": "estimate_history",
                            "x": 0,
                            "y": 2,
                            "w": 24,
                            "h": 12,
                            "state": {"params": {"symbol": "AAPL"}},
                        },
                        {
                            "i": "fundamental_metrics",
                            "x": 24,
                            "y": 2,
                            "w": 16,
                            "h": 8,
                            "state": {"params": {"symbol": "AAPL"}},
                        },
                    ],
                },
            },
            "groups": [
                {
                    "name": "Group 1",
                    "type": "endpointParam",
                    "paramName": "symbol",
                    "widgetIds": [
                        "price_performance",
                        "latest_news",
                        "estimate_history",
                        "fundamental_metrics",
                    ],
                    "defaultValue": "AAPL",
                }
            ],
            "prompts": [
                "What changed most in the latest AAPL estimate set?",
                "Which news items matter for margins?",
                "How has the stock traded into earnings?",
            ],
        }
    ]
    return FixtureBackend("equities", "Bench Equities", widgets, apps, url)


def build_macro_backend(url: str = "http://127.0.0.1:9102") -> FixtureBackend:
    widgets = {
        "macro_timeseries": {
            "name": "Macro Time Series",
            "description": "Historical macroeconomic series values by date.",
            "type": "table",
            "endpoint": "/macro-timeseries",
            "category": "Macro",
            "gridData": {"w": 20, "h": 10},
            "params": [_series_param()],
            "data": _table_columns(
                [("date", "Date", "dateString"), ("value", "Value", "number")]
            ),
        },
        "yield_curve": {
            "name": "Yield Curve",
            "description": "US Treasury yield curve by tenor.",
            "type": "table",
            "endpoint": "/yield-curve",
            "category": "Macro",
            "gridData": {"w": 20, "h": 10},
            "params": [],
            "data": _table_columns(
                [("tenor", "Tenor", "text"), ("yield", "Yield", "number")]
            ),
        },
    }
    apps: list[JsonDict] = []
    return FixtureBackend("macro", "Bench Macro", widgets, apps, url)


def build_portfolio_backend(url: str = "http://127.0.0.1:9103") -> FixtureBackend:
    widgets = {
        "holdings_table": {
            "name": "Holdings",
            "description": "Portfolio holdings with market value, sector, weight, and daily return.",
            "type": "table",
            "endpoint": "/holdings",
            "category": "Portfolio",
            "gridData": {"w": 24, "h": 12},
            "params": [],
            "data": _table_columns(
                [
                    ("symbol", "Symbol", "text"),
                    ("sector", "Sector", "text"),
                    ("market_value", "Market Value", "number"),
                    ("weight", "Weight", "number"),
                    ("day_return", "Day Return", "number"),
                ]
            ),
        },
        "sector_exposure": {
            "name": "Sector Exposure",
            "description": "Portfolio exposure grouped by sector.",
            "type": "table",
            "endpoint": "/sector-exposure",
            "category": "Portfolio",
            "gridData": {"w": 16, "h": 10},
            "params": [],
            "data": _table_columns(
                [
                    ("sector", "Sector", "text"),
                    ("weight", "Weight", "number"),
                    ("market_value", "Market Value", "number"),
                ]
            ),
        },
        "risk_metrics": {
            "name": "Risk Metrics",
            "description": "Portfolio beta, one-day VaR, and concentration metrics.",
            "type": "metric",
            "endpoint": "/risk-metrics",
            "category": "Portfolio",
            "gridData": {"w": 16, "h": 8},
            "params": [],
        },
    }
    apps: list[JsonDict] = []
    return FixtureBackend("portfolio", "Bench Portfolio", widgets, apps, url)


def build_stark_enterprise_backend(
    url: str = "http://127.0.0.1:9104",
) -> FixtureBackend:
    """Build the deterministic Stark enterprise demo fixture backend."""

    data_path = resources.files("workspace_bench.workspace.data") / "stark_enterprise.json"
    with data_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return FixtureBackend(
        "stark-enterprise",
        "Bench Stark Enterprise",
        payload["widgets"],
        payload["apps"],
        url,
    )


def _generic_widget_data(
    widget_id: str, definition: JsonDict, data_args: JsonDict
) -> Any:
    name = str(definition.get("name", widget_id))
    widget_type = str(definition.get("type", "table"))
    category = str(definition.get("category", "Workspace"))
    params = {
        str(param.get("paramName")): data_args.get(
            str(param.get("paramName")), param.get("value")
        )
        for param in definition.get("params", []) or []
        if param.get("paramName")
    }
    base = {
        "widget_id": widget_id,
        "widget_name": name,
        "category": category,
        "status": params.get("status", "Open"),
        "period": params.get("period", "YTD"),
        "fund": params.get("fund", "Flagship Long/Short"),
        "ticker": params.get("ticker", params.get("symbol", "AAPL")),
        "workflow": widget_id.rsplit("_", 1)[0],
        "value": round((sum(ord(char) for char in widget_id) % 9000) / 100, 2),
    }
    if widget_type == "markdown":
        return (
            f"{name}: deterministic fixture summary for {category}. "
            f"Status {base['status']}; period {base['period']}; "
            f"fund {base['fund']}; ticker {base['ticker']}."
        )
    if widget_type == "metric":
        return [
            {"metric": "primary_value", **base},
            {"metric": "change", **base, "value": round(base["value"] / 10, 2)},
        ]
    return [
        {"row": 1, "metric": "priority", **base},
        {
            "row": 2,
            "metric": "risk_or_opportunity",
            **base,
            "status": "In Review",
            "value": round(base["value"] * 1.15, 2),
        },
        {
            "row": 3,
            "metric": "action_required",
            **base,
            "status": "Approved",
            "value": round(base["value"] * 0.85, 2),
        },
    ]


def default_fixture_backends() -> dict[str, FixtureBackend]:
    """Return all built-in fixture backends keyed by slug and display name."""

    backends = [
        build_equities_backend(),
        build_macro_backend(),
        build_portfolio_backend(),
        build_stark_enterprise_backend(),
    ]
    result: dict[str, FixtureBackend] = {}
    for backend in backends:
        result[backend.slug] = backend
        result[backend.name] = backend
    return result


def get_fixture_backend(name: str) -> FixtureBackend:
    backends = default_fixture_backends()
    try:
        return backends[name]
    except KeyError as error:
        available = sorted({backend.slug for backend in backends.values()})
        raise KeyError(f"Unknown fixture backend {name!r}. Available: {available}") from error


class FixtureRequestHandler(BaseHTTPRequestHandler):
    """HTTP handler serving one fixture backend."""

    backend: FixtureBackend

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self._send_cors()
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        query = {
            key: values[-1] if len(values) == 1 else values
            for key, values in parse_qs(parsed.query).items()
        }
        try:
            payload = self.backend.fetch_http_path(parsed.path, query)
        except KeyError as error:
            self._send_json({"error": str(error)}, status=404)
            return
        self._send_json(payload)

    def _send_json(self, payload: Any, status: int = 200) -> None:
        body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self._send_cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")

    def log_message(self, format: str, *args: Any) -> None:
        return


def make_fixture_server(
    backend: FixtureBackend, host: str = "127.0.0.1", port: int = 9101
) -> ThreadingHTTPServer:
    """Create a blocking stdlib HTTP server for a fixture backend."""

    handler = type(
        f"{backend.slug.title()}FixtureRequestHandler",
        (FixtureRequestHandler,),
        {"backend": backend},
    )
    return ThreadingHTTPServer((host, port), handler)
