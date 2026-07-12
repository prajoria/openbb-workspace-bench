#!/usr/bin/env python3
"""Bake deterministic synthetic data into the Stark enterprise fixture catalog."""

from __future__ import annotations

import json
import random
import re
from datetime import date, timedelta
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = REPO / "src/workspace_bench/workspace/data/stark_enterprise.json"

VENDORS = ["Bloomberg", "FactSet", "Refinitiv", "S&P Global", "MSCI", "ICE"]
BROKERS = ["Goldman Sachs", "Morgan Stanley", "J.P. Morgan", "Citi", "UBS", "Barclays"]
TICKERS = ["AAPL", "MSFT", "NVDA", "LLY", "JPM", "XOM", "TSLA", "AVGO"]
FUNDS = [
    "Flagship Long/Short",
    "Global Opportunities",
    "Credit Plus",
    "Macro Absolute Return",
    "Healthcare Alpha",
]
DESKS = ["US Equities", "EU Equities", "Macro", "Credit", "Options", "ETF"]
CLIENTS = [
    "Atlas Pension",
    "Northstar Endowment",
    "Meridian Family Office",
    "Horizon Sovereign",
]
STRATEGIES = ["Global Equities", "Credit", "Macro", "Multi-Asset", "Quant"]
CRYPTO = ["BTC", "ETH", "SOL", "ARB", "BASE"]
STATUSES = ["Open", "In Review", "Escalated", "Approved", "Closed"]
PERIODS = ["YTD", "QTD", "MTD", "1D", "1Y"]

JsonValue = dict[str, Any] | list[Any] | str | int | float | bool | None


def semantic_kind(widget_id: str) -> str:
    """Return the first matching synthetic value family for a widget id."""

    key = widget_id.lower()
    rules = [
        (r"var|drawdown|loss", "negative_dollars"),
        (r"weight|exposure", "weight"),
        (r"latency", "latency"),
        (r"count|breach|alert|exception|order", "count"),
        (r"return|yield", "return"),
        (r"price|value|aum", "dollars"),
    ]
    for pattern, kind in rules:
        if re.search(pattern, key):
            return kind
    return "float"


def _schema_data(value: Any) -> bool:
    return isinstance(value, dict) and isinstance(value.get("table"), dict)


def _param_default(widget: dict[str, Any], name: str, fallback: Any) -> Any:
    for param in widget.get("params", []) or []:
        if param.get("paramName") == name and param.get("value") not in (None, ""):
            return param["value"]
    return fallback


def _text_key(widget_id: str, widget: dict[str, Any]) -> str:
    return f"{widget_id} {widget.get('name', '')} {widget.get('category', '')}".lower()


def _first_column(widget_id: str, widget: dict[str, Any]) -> tuple[str, list[str]]:
    key = _text_key(widget_id, widget)
    if any(token in key for token in ("vendor", "dataset", "feed", "sla")):
        return "vendor", VENDORS
    if any(token in key for token in ("broker", "fill", "tca")):
        return "broker", BROKERS
    if any(token in key for token in ("desk", "order", "execution", "blotter")):
        return "desk", DESKS
    if any(token in key for token in ("ticker", "symbol", "issuer", "company", "earnings")):
        return "ticker", TICKERS
    if any(token in key for token in ("client", "account", "investor")):
        return "client", CLIENTS
    if "crypto" in key:
        return "symbol", CRYPTO
    if "strategy" in key:
        return "strategy", STRATEGIES
    return "fund", FUNDS


def _value_field(widget_id: str, kind: str) -> str:
    key = widget_id.lower()
    if kind == "negative_dollars":
        if "drawdown" in key:
            return "drawdown_usd"
        if "loss" in key:
            return "loss_usd"
        return "var_usd"
    if kind == "weight":
        return "weight" if "weight" in key else "exposure"
    if kind == "latency":
        return "latency_ms"
    if kind == "count":
        if "breach" in key:
            return "breach_count"
        if "alert" in key:
            return "alert_count"
        if "exception" in key:
            return "exception_count"
        if "order" in key:
            return "order_count"
        return "count"
    if kind == "return":
        return "return"
    if kind == "dollars":
        if "aum" in key:
            return "aum_usd"
        if "price" in key:
            return "price_usd"
        return "value_usd"
    return "score"


def _values(rng: random.Random, kind: str, count: int) -> list[int | float]:
    if kind == "negative_dollars":
        return [-rng.randrange(5_000, 250_001, 500) for _ in range(count)]
    if kind == "weight":
        remaining = rng.uniform(0.55, 0.95)
        values: list[float] = []
        for index in range(count):
            if index == count - 1:
                value = remaining
            else:
                value = rng.uniform(0.01, max(0.02, remaining / (count - index)))
            value = min(value, remaining)
            values.append(round(value, 4))
            remaining = max(0.0, remaining - value)
        return values
    if kind == "latency":
        return [rng.randint(5, 900) for _ in range(count)]
    if kind == "count":
        return [rng.randint(0, 250) for _ in range(count)]
    if kind == "return":
        return [round(rng.uniform(-0.05, 0.12), 4) for _ in range(count)]
    if kind == "dollars":
        return [round(rng.uniform(1_000, 250_000), 2) for _ in range(count)]
    return [round(rng.uniform(0, 100), 2) for _ in range(count)]


def _series_values(rng: random.Random, kind: str, count: int) -> list[int | float]:
    if kind == "negative_dollars":
        current: int | float = -rng.randrange(40_000, 160_001, 500)
        values: list[int | float] = []
        for _ in range(count):
            current += rng.randrange(-12_000, 12_001, 500)
            values.append(min(-5_000, max(-250_000, current)))
        return values
    if kind == "weight":
        current = rng.uniform(0.08, 0.45)
        values = []
        for _ in range(count):
            current = min(0.95, max(0.0, current + rng.uniform(-0.035, 0.04)))
            values.append(round(current, 4))
        return values
    if kind == "latency":
        current = rng.randint(80, 420)
        values = []
        for _ in range(count):
            current = min(900, max(5, current + rng.randint(-65, 70)))
            values.append(current)
        return values
    if kind == "count":
        current = rng.randint(20, 160)
        values = []
        for _ in range(count):
            current = min(250, max(0, current + rng.randint(-24, 28)))
            values.append(current)
        return values
    if kind == "return":
        current = rng.uniform(-0.015, 0.06)
        values = []
        for _ in range(count):
            current = min(0.12, max(-0.05, current + rng.uniform(-0.012, 0.014)))
            values.append(round(current, 4))
        return values
    if kind == "dollars":
        current = rng.uniform(20_000, 180_000)
        values = []
        for _ in range(count):
            current = max(1_000, current + rng.uniform(-8_000, 12_000))
            values.append(round(current, 2))
        return values
    current = rng.uniform(20, 80)
    values = []
    for _ in range(count):
        current = min(100, max(0, current + rng.uniform(-6, 7)))
        values.append(round(current, 2))
    return values


def _ordered_pool(pool: list[str], first_value: Any) -> list[str]:
    values = list(pool)
    if isinstance(first_value, str) and first_value:
        if first_value in values:
            values.remove(first_value)
        values.insert(0, first_value)
    return values


def _row_context(index: int, widget: dict[str, Any], first_field: str) -> dict[str, str]:
    context = {
        "period": _ordered_pool(PERIODS, _param_default(widget, "period", "YTD"))[
            index % len(PERIODS)
        ],
        "status": _ordered_pool(STATUSES, _param_default(widget, "status", "Open"))[
            index % len(STATUSES)
        ],
        "fund": _ordered_pool(FUNDS, _param_default(widget, "fund", "Flagship Long/Short"))[
            index % len(FUNDS)
        ],
        "desk": _ordered_pool(DESKS, _param_default(widget, "desk", "US Equities"))[
            index % len(DESKS)
        ],
        "vendor": _ordered_pool(VENDORS, _param_default(widget, "vendor", "Bloomberg"))[
            index % len(VENDORS)
        ],
    }
    context.pop(first_field, None)
    return context


def table_payload(widget_id: str, widget: dict[str, Any], rng: random.Random) -> list[dict[str, Any]]:
    kind = semantic_kind(widget_id)
    first_field, first_pool = _first_column(widget_id, widget)
    value_field = _value_field(widget_id, kind)
    row_count = rng.randint(5, 10)
    values = _values(rng, kind, row_count)
    first_pool = _ordered_pool(first_pool, _param_default(widget, first_field, first_pool[0]))

    rows: list[dict[str, Any]] = []
    for index in range(row_count):
        row = {
            first_field: first_pool[index % len(first_pool)],
            "period": _param_default(widget, "period", "YTD")
            if index == 0
            else _row_context(index, widget, first_field)["period"],
            value_field: values[index],
            "change": round(rng.uniform(-0.08, 0.09), 4),
            "status": _param_default(widget, "status", "Open")
            if index == 0
            else _row_context(index, widget, first_field)["status"],
        }
        key = _text_key(widget_id, widget)
        if first_field != "fund" and any(token in key for token in ("fund", "portfolio", "nav")):
            row["fund"] = _row_context(index, widget, first_field)["fund"]
        if first_field != "desk" and any(token in key for token in ("desk", "order", "execution")):
            row["desk"] = _row_context(index, widget, first_field)["desk"]
        if first_field != "vendor" and any(token in key for token in ("vendor", "dataset", "feed")):
            row["vendor"] = _row_context(index, widget, first_field)["vendor"]
        rows.append(row)
    return rows


def metric_payload(widget_id: str, widget: dict[str, Any], rng: random.Random) -> list[dict[str, Any]]:
    kind = semantic_kind(widget_id)
    count = rng.randint(2, 4)
    values = _values(rng, kind, count)
    labels = ["primary", "secondary", "threshold", "watchlist"]
    return [
        {
            "metric": f"{widget.get('name', widget_id)} {labels[index]}",
            "value": values[index],
            "change": round(rng.uniform(-0.08, 0.09), 4),
        }
        for index in range(count)
    ]


def chart_payload(widget_id: str, widget: dict[str, Any], rng: random.Random) -> dict[str, Any]:
    kind = semantic_kind(widget_id)
    count = rng.randint(8, 12)
    start = date(2026, 1, 2) + timedelta(days=rng.randint(0, 10))
    values = _series_values(rng, kind, count)
    return {
        "series": [
            {
                "date": (start + timedelta(days=index)).isoformat(),
                "value": values[index],
            }
            for index in range(count)
        ],
    }


def markdown_payload(widget_id: str, widget: dict[str, Any], rng: random.Random) -> str:
    kind = semantic_kind(widget_id)
    field = _value_field(widget_id, kind)
    value = _values(rng, kind, 1)[0]
    name = widget.get("name", widget_id)
    category = widget.get("category", "Workspace")
    period = _param_default(widget, "period", "YTD")
    return (
        f"{widget_id}: {name} summarizes the {category} workflow for {period}. "
        f"The synthetic {field} reading is {value}, seeded from the widget id. "
        "Use this note as deterministic fixture prose for Stark data-reading tasks."
    )


def payload_for_widget(widget_id: str, widget: dict[str, Any]) -> JsonValue:
    rng = random.Random(f"stark-v1:{widget_id}")
    widget_type = str(widget.get("type", "table"))
    if widget_type == "metric":
        return metric_payload(widget_id, widget, rng)
    if widget_type == "chart":
        return chart_payload(widget_id, widget, rng)
    if widget_type == "markdown":
        return markdown_payload(widget_id, widget, rng)
    return table_payload(widget_id, widget, rng)


def bake_stark_data(catalog: dict[str, Any]) -> dict[str, Any]:
    for widget_id, widget in catalog["widgets"].items():
        if "schema_data" not in widget and _schema_data(widget.get("data")):
            widget["schema_data"] = widget["data"]
        widget["data"] = payload_for_widget(widget_id, widget)
    return catalog


def main(path: Path = DEFAULT_DATA_PATH) -> None:
    catalog = json.loads(path.read_text(encoding="utf-8"))
    bake_stark_data(catalog)
    path.write_text(json.dumps(catalog, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Baked Stark data for {len(catalog['widgets'])} widgets into {path}")


if __name__ == "__main__":
    main()
