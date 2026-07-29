"""Deterministic OpenBB Workspace fixture backends."""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from importlib import resources
from typing import Any

from workspace_bench.core.models import JsonDict
from workspace_bench.workspace.widget_params import flatten_params


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
        del data_args
        if widget_id:
            self.get_widget_schema(widget_id)
        if widget_id and widget_id in self.widgets:
            schema = self.widgets[widget_id]
            for param in flatten_params(schema, recurse=False):
                if param.get("paramName") == param_name:
                    options = param.get("options") or []
                    if isinstance(options, list):
                        return copy.deepcopy(options)
        return []

    def fetch_widget_data(
        self, widget_id: str, data_args: JsonDict | None = None
    ) -> Any:
        data_args = data_args or {}
        if widget_id in self.widgets:
            definition = self.widgets[widget_id]
            samples_by_args = definition.get("sampleDataByArgs")
            if isinstance(samples_by_args, list):
                for sample in samples_by_args:
                    sample_args = sample.get("dataArgs", {})
                    if all(data_args.get(key) == value for key, value in sample_args.items()):
                        return copy.deepcopy(sample.get("data"))
                for sample in samples_by_args:
                    sample_args = sample.get("dataArgs", {})
                    if all(sample_args.get(key) == value for key, value in data_args.items()):
                        return copy.deepcopy(sample.get("data"))
            if "sampleData" in definition:
                return copy.deepcopy(definition["sampleData"])
            if self.slug.startswith("stark-enterprise") and "data" in definition:
                return _stark_widget_data(definition["data"], data_args)
            if self.slug == "support-daloopa-skills" and "data" in definition:
                return _daloopa_widget_data(definition["data"], data_args)
            if self.slug in {"getting-started", "widget-examples"}:
                return []
            return _generic_widget_data(widget_id, self.widgets[widget_id], data_args)
        raise KeyError(f"Unknown widget data endpoint for {widget_id!r}")

    def fetch_http_path(self, path: str, query: JsonDict) -> Any:
        if path == "/widgets.json":
            return self.widgets_json()
        if path == "/apps.json":
            return self.apps_json()
        for widget_id, definition in self.widgets.items():
            if str(definition.get("endpoint", "")).strip("/") == path.strip("/"):
                return self.fetch_widget_data(widget_id, query)
            for param in flatten_params(definition, recurse=False):
                if str(param.get("optionsEndpoint", "")).strip("/") == path.strip("/"):
                    options = param.get("options")
                    if isinstance(options, list):
                        return copy.deepcopy(options)
        raise KeyError(f"Unknown fixture path {path}")


def build_equities_backend(url: str = "http://127.0.0.1:9101") -> FixtureBackend:
    """Compatibility alias for the transcribed getting-started backend."""

    return build_getting_started_backend(url)


def build_stark_enterprise_backend(
    url: str = "http://127.0.0.1:9104",
) -> FixtureBackend:
    """Build Stark data world X, the canonical Stark enterprise backend."""

    data_path = resources.files("workspace_bench.data") / "backends" / "stark_enterprise_x.json"
    with data_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return FixtureBackend(
        "stark-enterprise-x",
        "Bench Stark Enterprise",
        payload["widgets"],
        payload["apps"],
        url,
    )


# X is the canonical world under its own builder above.
build_stark_enterprise_x_backend = build_stark_enterprise_backend

# Interchangeable Stark data worlds: one catalog, one display name, different
# baked numbers. A workspace may connect at most one at a time.
STARK_DATA_WORLDS = ("stark-enterprise-x", "stark-enterprise-y")

# Task files authored before the slug renames keep resolving; the loader and
# baseline merge normalize these to the canonical slugs.
LEGACY_BACKEND_SLUGS = {
    "stark-enterprise": "stark-enterprise-x",
    "daloopa": "support-daloopa-skills",
}


def build_stark_enterprise_y_backend(url: str = "http://127.0.0.1:9109") -> FixtureBackend:
    """Stark data world Y: the same catalog over materially different data.

    Loaded from the self-contained ``backends/stark_enterprise_y.json``, which
    is produced — and its widget-contract invariants certified — by
    ``scripts/generators/generate_stark_world_y.py``. Catalog equality with
    the canonical file is guarded by tests.
    """

    data_path = (
        resources.files("workspace_bench.data")
        / "backends"
        / "stark_enterprise_y.json"
    )
    with data_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return FixtureBackend(
        "stark-enterprise-y",
        "Bench Stark Enterprise",
        payload["widgets"],
        payload["apps"],
        url,
    )


# Replacement vocabularies used by the world-Y generator for entity fields not
# backed by a declared param. Pools are disjoint from the canonical data's
# tickers and chosen by the original value's domain, so a crypto widget keeps
# crypto assets.
_EQUITY_SUBSTITUTION_POOL = ("TSM", "COST", "AMD", "CRM", "ORCL", "NFLX", "GOOGL", "AMZN")
_CRYPTO_SUBSTITUTION_POOL = ("AVAX", "DOT", "LINK", "MATIC", "ATOM", "XRP", "ADA", "DOGE")
_CRYPTO_CANONICAL_ASSETS = frozenset({"BTC", "ETH", "SOL", "ARB", "BASE"})
_FREE_ENTITY_FIELDS = {"ticker", "symbol"}


def build_getting_started_backend(
    url: str = "http://127.0.0.1:9106",
) -> FixtureBackend:
    """Build the transcribed OpenBB getting-started fixture backend."""

    data_path = resources.files("workspace_bench.data") / "backends" / "getting_started.json"
    with data_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return FixtureBackend(
        "getting-started",
        "Getting Started",
        payload["widgets"],
        payload["apps"],
        url,
    )


def build_widget_examples_backend(
    url: str = "http://127.0.0.1:9107",
) -> FixtureBackend:
    """Build the transcribed OpenBB widget-examples fixture backend."""

    data_path = resources.files("workspace_bench.data") / "backends" / "widget_examples.json"
    with data_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return FixtureBackend(
        "widget-examples",
        "Widget Examples",
        payload["widgets"],
        payload["apps"],
        url,
    )


def build_daloopa_backend(url: str = "http://127.0.0.1:9105") -> FixtureBackend:
    """Build the deterministic Daloopa fundamentals fixture backend.

    The catalog mirrors the data surface consumed by the Daloopa Claude
    plugin skills (github.com/daloopa/daloopa-plugin-claude) and is authored
    by scripts/generators/generate_daloopa_data.py.
    """

    data_path = resources.files("workspace_bench.data") / "backends" / "support_daloopa_skills.json"
    with data_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return FixtureBackend(
        "support-daloopa-skills",
        "Bench Daloopa",
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
        for param in flatten_params(definition, recurse=False)
        if param.get("paramName")
    }
    value = round((sum(ord(char) for char in widget_id) % 9000) / 100, 2)
    # Real backends return business rows only — never the widget id or other
    # envelope metadata (verified against the live Workspace MCP bridge).
    base = {
        "category": category,
        "status": params.get("status", "Open"),
        "period": params.get("period", "YTD"),
        "fund": params.get("fund", "Flagship Long/Short"),
        "ticker": params.get("ticker", params.get("symbol", "AAPL")),
        "value": value,
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
            {"metric": "change", **base, "value": round(value / 10, 2)},
        ]
    return [
        {"row": 1, "metric": "priority", **base},
        {
            "row": 2,
            "metric": "risk_or_opportunity",
            **base,
            "status": "In Review",
            "value": round(value * 1.15, 2),
        },
        {
            "row": 3,
            "metric": "action_required",
            **base,
            "status": "Approved",
            "value": round(value * 0.85, 2),
        },
    ]


def _stark_widget_data(payload: Any, data_args: JsonDict) -> Any:
    data = copy.deepcopy(payload)
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        return data

    filter_fields = {"status", "desk", "vendor", "fund", "period"}
    filters = {
        key: data_args[key]
        for key in filter_fields
        if key in data_args and any(key in row for row in data)
    }
    if not filters:
        return data

    filtered = [
        row
        for row in data
        if all(str(row.get(key)) == str(value) for key, value in filters.items())
    ]
    return filtered or data


# Daloopa param names mapped to the baked row fields they filter on.
_DALOOPA_FILTER_FIELDS = {
    "ticker": "ticker",
    "period": "calendar_period",
    "doc_type": "doc_type",
    "category": "category",
}


def _daloopa_widget_data(payload: Any, data_args: JsonDict) -> Any:
    data = copy.deepcopy(payload)
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        return data

    filters = {
        field: data_args[param]
        for param, field in _DALOOPA_FILTER_FIELDS.items()
        if param in data_args and any(field in row for row in data)
    }
    if not filters:
        return data

    filtered = [
        row
        for row in data
        if all(str(row.get(field)) == str(value) for field, value in filters.items())
    ]
    return filtered or data


def default_fixture_backends() -> dict[str, FixtureBackend]:
    """Return all built-in fixture backends keyed by slug and display name."""

    backends = [
        build_stark_enterprise_backend(),
        build_daloopa_backend(),
        build_getting_started_backend(),
        build_widget_examples_backend(),
        build_stark_enterprise_y_backend(),
    ]
    result: dict[str, FixtureBackend] = {}
    for backend in backends:
        result[backend.slug] = backend
        # Data-world variants share a display name; the canonical backend
        # (registered first) keeps the display-name key.
        result.setdefault(backend.name, backend)
    for legacy, canonical in LEGACY_BACKEND_SLUGS.items():
        result[legacy] = result[canonical]
    # Keep the historical CLI slugs as lookup aliases without exposing the
    # retired invented catalogs.
    result["equities"] = result["getting-started"]
    result["macro"] = result["getting-started"]
    result["portfolio"] = result["widget-examples"]
    return result


def get_fixture_backend(name: str) -> FixtureBackend:
    backends = default_fixture_backends()
    try:
        return backends[name]
    except KeyError as error:
        available = sorted({backend.slug for backend in backends.values()})
        raise KeyError(f"Unknown fixture backend {name!r}. Available: {available}") from error
