"""Generate the stark-enterprise-y data file.

World Y is a self-contained materialized sibling of the canonical Stark
backend: the same catalog (widgets, params, options, apps) over
deterministically different rows, written as a complete
``backends/stark_enterprise_y.json`` that ``build_stark_enterprise_y_backend``
loads directly. This script derives the rows from the canonical file,
certifies the widget-contract invariants, and writes the full payload. Re-run
it only to regenerate the file; hand edits to the file are allowed as long as
validation stays green. Catalog equality with the canonical file is guarded by
tests, not by construction.

Derivation rules, seeded per (variant, widget, row, field):
- Row counts shrink per widget (never below two rows) — or grow up to 1.5x in
  widgets whose string columns are all schema-managed, where clones differ in
  every string column through the per-index transforms.
- String fields backed by a declared param re-draw values from that param's
  own options, so filters and prompt vocabulary stay accurate.
- Free ticker/symbol fields substitute from domain-aware pools disjoint from
  the canonical vocabulary (crypto widgets stay crypto).
- Numeric values scale by a sign-preserving factor in [0.6, 1.6).
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from workspace_bench.core.models import JsonDict
from workspace_bench.workspace.fixtures import (
    _CRYPTO_CANONICAL_ASSETS,
    _CRYPTO_SUBSTITUTION_POOL,
    _EQUITY_SUBSTITUTION_POOL,
    _FREE_ENTITY_FIELDS,
    build_stark_enterprise_backend,
)
from workspace_bench.workspace.widget_params import flatten_params

VARIANT = "y"
OUTPUT_PATH = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "workspace_bench"
    / "data"
    / "backends"
    / "stark_enterprise_y.json"
)


def derive_data_by_widget() -> dict[str, list[JsonDict]]:
    canonical = build_stark_enterprise_backend()
    result: dict[str, list[JsonDict]] = {}
    for widget_id, definition in canonical.widgets.items():
        rows = definition.get("data")
        if not isinstance(rows, list) or not rows or not all(
            isinstance(row, dict) for row in rows
        ):
            continue
        options_by_field = _options_by_field(definition)
        kept = _variant_row_subset(widget_id, rows, options_by_field)
        for index, row in enumerate(kept):
            for field, value in row.items():
                row[field] = _variant_value(widget_id, index, field, value, options_by_field)
        result[widget_id] = kept
    return result


def _options_by_field(definition: JsonDict) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for param in flatten_params(definition):
        name = param.get("paramName")
        options = param.get("options")
        if not name or not isinstance(options, list):
            continue
        values = [
            option.get("value") if isinstance(option, dict) else option
            for option in options
        ]
        string_values = [value for value in values if isinstance(value, str) and value]
        if string_values:
            result[str(name)] = string_values
    return result


def _variant_row_subset(
    widget_id: str,
    rows: list[Any],
    options_by_field: dict[str, list[str]],
) -> list[JsonDict]:
    count = len(rows)
    if count <= 2:
        return [copy.deepcopy(row) for row in rows]
    # Rows may only grow when every string column is managed (param-backed or
    # an entity field): clones then differ in every string column through the
    # per-index transforms, instead of copying an identity column verbatim.
    managed = set(options_by_field) | _FREE_ENTITY_FIELDS
    growable = not any(
        isinstance(value, str) and field not in managed
        for row in rows
        for field, value in row.items()
    )
    span = 900 if growable else 500
    factor = 0.6 + (_seed_int(VARIANT, widget_id, "rows") % span) / 1000
    ceiling = round(count * 1.5) if growable else count
    target = min(ceiling, max(2, round(count * factor)))
    if target <= count:
        ranked = sorted(
            range(count),
            key=lambda index: _seed_int(VARIANT, widget_id, "keep", str(index)),
        )
        return [copy.deepcopy(rows[index]) for index in sorted(ranked[:target])]
    grown = [copy.deepcopy(row) for row in rows]
    for extra in range(target - count):
        grown.append(copy.deepcopy(rows[extra % count]))
    return grown


def _variant_value(
    widget_id: str,
    index: int,
    field: str,
    value: Any,
    options_by_field: dict[str, list[str]],
) -> Any:
    if isinstance(value, str):
        declared = options_by_field.get(field)
        if declared:
            offset = _seed_int(VARIANT, widget_id, "assign", field)
            return declared[(offset + index) % len(declared)]
        if field in _FREE_ENTITY_FIELDS:
            offset = _seed_int(VARIANT, widget_id, "entity", field)
            pool = (
                _CRYPTO_SUBSTITUTION_POOL
                if value in _CRYPTO_CANONICAL_ASSETS
                else _EQUITY_SUBSTITUTION_POOL
            )
            return pool[(offset + index) % len(pool)]
        return value
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return value
    factor = 0.6 + (_seed_int(VARIANT, widget_id, str(index), field) % 1000) / 1000
    scaled = value * factor
    if isinstance(value, int):
        return int(round(scaled))
    return round(scaled, _float_decimals(value))


def _seed_int(*parts: str) -> int:
    digest = hashlib.sha256(":".join(parts).encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big")


def _float_decimals(value: float) -> int:
    text = repr(value)
    if "e" in text or "E" in text or "." not in text:
        return 4
    return min(len(text.split(".", 1)[1]), 6)


def certify(data_by_widget: dict[str, list[JsonDict]]) -> dict[str, int]:
    canonical = build_stark_enterprise_backend()
    substitution_pool = set(_EQUITY_SUBSTITUTION_POOL) | set(_CRYPTO_SUBSTITUTION_POOL)
    failures: list[str] = []
    shrunk = grown = same = 0
    for widget_id, rows in data_by_widget.items():
        definition = canonical.widgets.get(widget_id)
        if definition is None:
            failures.append(f"{widget_id}: not in the canonical catalog")
            continue
        canonical_rows = definition["data"]
        if not 2 <= len(rows) <= round(len(canonical_rows) * 1.5):
            failures.append(f"{widget_id}: row count {len(rows)} out of bounds")
        if len(rows) < len(canonical_rows):
            shrunk += 1
        elif len(rows) > len(canonical_rows):
            grown += 1
        else:
            same += 1
        declared = _options_by_field(definition)
        for row in rows:
            for field, value in row.items():
                if not isinstance(value, str):
                    continue
                if field in declared and value not in declared[field]:
                    failures.append(f"{widget_id}: {field}={value!r} outside options")
                elif field in _FREE_ENTITY_FIELDS and field not in declared:
                    if value not in substitution_pool:
                        failures.append(f"{widget_id}: {field}={value!r} outside pool")
                elif field not in declared and field not in _FREE_ENTITY_FIELDS:
                    if len(rows) > len(canonical_rows):
                        failures.append(
                            f"{widget_id}: grew with unmanaged string column {field!r}"
                        )
    if failures:
        raise RuntimeError(
            "World Y certification failed:\n" + "\n".join(failures[:20])
        )
    return {"widgets": len(data_by_widget), "shrunk": shrunk, "same": same, "grown": grown}


def main() -> int:
    canonical = build_stark_enterprise_backend()
    data_by_widget = derive_data_by_widget()
    stats = certify(data_by_widget)
    widgets = copy.deepcopy(canonical.widgets)
    for widget_id, rows in data_by_widget.items():
        widgets[widget_id]["data"] = rows
    payload = {
        "source": {
            "derived_from": "backends/stark_enterprise_x.json",
            "generator": "scripts/generators/generate_stark_world_y.py",
            "method": (
                "self-contained copy of the canonical catalog with seeded "
                "deterministic data variation within widget contracts: row "
                "counts shrink or grow, param-backed fields re-drawn from "
                "declared options, entity fields from domain-aware pools, "
                "numerics scaled 0.6-1.6 sign-preserving"
            ),
        },
        "widgets": widgets,
        "apps": copy.deepcopy(canonical.apps),
    }
    OUTPUT_PATH.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {OUTPUT_PATH.name}: {stats['widgets']} widgets "
        f"({stats['shrunk']} shrunk, {stats['same']} same, {stats['grown']} grown)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
