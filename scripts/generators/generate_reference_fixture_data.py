#!/usr/bin/env python3
"""Transcribe OpenBB backend examples into deterministic fixture catalogs.

The getting-started catalog reads ``reference-backend/apps.json`` and every
``reference-backend/widgets_*.py`` registration. The widget-examples catalog
reads every ``widgets.json`` plus literal ``register_widget`` decorators and
``WIDGETS`` dictionaries below ``widget-types/``, ``parameters-types/``, and
``ssrm_mode/``. Python is parsed as AST and is never imported or executed.
"""

from __future__ import annotations

import ast
import copy
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, NamedTuple, cast

from workspace_bench.workspace.backend_validation import (
    WIDGET_VIZ_TYPE_ALIASES,
    WIDGET_VIZ_TYPES,
)
from workspace_bench.workspace.widget_params import flatten_params


REPO = Path(__file__).resolve().parents[2]
REFERENCE_REPO = REPO / "references/openbb-backend-examples"
DATA_DIR = REPO / "src/workspace_bench/workspace/data"
REFERENCE_REPO_URL = (
    "https://github.com/OpenBB-finance/backend-examples-for-openbb-workspace"
)
JsonDict = dict[str, Any]


class CatalogEntry(NamedTuple):
    """A widget definition and the source slug used to disambiguate it."""

    widget_id: str
    source_slug: str
    definition: JsonDict


def snake_slug(value: str, *, fallback: str = "widget") -> str:
    """Return a deterministic snake_case identifier."""

    separated = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", separated).strip("_").lower()
    return slug or fallback


def _literal_node(value: Any) -> ast.expr:
    expression = cast(ast.Expression, ast.parse(repr(value), mode="eval"))
    return cast(ast.expr, expression.body)


class _StableLiteralTransformer(ast.NodeTransformer):
    """Substitute resolved constants and unstable date expressions."""

    def __init__(self, constants: dict[str, Any]) -> None:
        self.constants = constants

    def visit_Name(self, node: ast.Name) -> ast.expr:
        if node.id in self.constants:
            return ast.copy_location(_literal_node(self.constants[node.id]), node)
        return node

    def visit_Call(self, node: ast.Call) -> ast.expr:
        if isinstance(node.func, ast.Attribute) and node.func.attr == "strftime":
            return ast.copy_location(ast.Constant(value="$currentDate-1d"), node)
        return cast(ast.expr, self.generic_visit(node))


def _safe_literal(node: ast.AST, constants: dict[str, Any]) -> Any:
    transformed = _StableLiteralTransformer(constants).visit(copy.deepcopy(node))
    ast.fix_missing_locations(transformed)
    return ast.literal_eval(transformed)


def _module_constants(tree: ast.Module) -> dict[str, Any]:
    constants: dict[str, Any] = {}
    changed = True
    while changed:
        changed = False
        for node in tree.body:
            if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                continue
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value_node = node.value
            if value_node is None:
                continue
            names = [target.id for target in targets if isinstance(target, ast.Name)]
            if len(names) != 1 or names[0] in constants:
                continue
            try:
                constants[names[0]] = _safe_literal(value_node, constants)
            except (ValueError, TypeError, SyntaxError):
                continue
            changed = True
    return constants


def _python_catalog(path: Path, source_slug: str) -> list[CatalogEntry]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    constants = _module_constants(tree)
    entries: list[CatalogEntry] = []

    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if not any(
                isinstance(target, ast.Name) and target.id == "WIDGETS"
                for target in targets
            ):
                continue
            if node.value is None:
                continue
            payload = _safe_literal(node.value, constants)
            if isinstance(payload, dict):
                for widget_id, definition in payload.items():
                    if isinstance(definition, dict):
                        entries.append(
                            CatalogEntry(str(widget_id), source_slug, definition)
                        )

        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for decorator in node.decorator_list:
            if not (
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, (ast.Name, ast.Attribute))
                and (
                    getattr(decorator.func, "id", None) == "register_widget"
                    or getattr(decorator.func, "attr", None) == "register_widget"
                )
                and decorator.args
            ):
                continue
            try:
                definition = _safe_literal(decorator.args[0], constants)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError(
                    f"Unable to extract widget registration from {path}:{node.lineno}"
                ) from error
            if not isinstance(definition, dict):
                raise ValueError(f"Widget registration is not a dict: {path}:{node.lineno}")
            raw_id = definition.get("widgetId") or definition.get("endpoint")
            if not isinstance(raw_id, str) or not raw_id:
                raise ValueError(f"Widget registration has no id: {path}:{node.lineno}")
            entries.append(CatalogEntry(raw_id, source_slug, definition))
    return entries


def _json_catalog(path: Path, source_slug: str) -> list[CatalogEntry]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Widget catalog must be an object: {path}")
    return [
        CatalogEntry(str(widget_id), source_slug, definition)
        for widget_id, definition in payload.items()
        if isinstance(definition, dict)
    ]


def _normalize_definition(definition: JsonDict) -> JsonDict:
    normalized = copy.deepcopy(definition)
    widget_type = str(normalized.get("type", "table"))
    normalized["type"] = WIDGET_VIZ_TYPE_ALIASES.get(widget_type, widget_type)
    if normalized["type"] not in WIDGET_VIZ_TYPES:
        raise ValueError(
            f"Unsupported widget type {normalized['type']!r} in {normalized.get('name')!r}"
        )
    flatten_params(normalized)
    return normalized


def _merge_entries(entries: list[CatalogEntry]) -> tuple[dict[str, JsonDict], dict[str, str]]:
    base_ids = [snake_slug(entry.widget_id) for entry in entries]
    collisions = Counter(base_ids)
    widgets: dict[str, JsonDict] = {}
    id_map: dict[str, str] = {}
    for entry, base_id in sorted(
        zip(entries, base_ids, strict=True),
        key=lambda item: (item[0].source_slug, item[1], item[0].widget_id),
    ):
        widget_id = base_id
        if collisions[base_id] > 1:
            widget_id = f"{entry.source_slug}_{base_id}"
        if widget_id in widgets:
            raise ValueError(f"Widget id collision after prefixing: {widget_id}")
        widgets[widget_id] = _normalize_definition(entry.definition)
        id_map[entry.widget_id] = widget_id
    return widgets, id_map


def _rewrite_app_widget_ids(value: Any, id_map: dict[str, str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "i" and isinstance(child, str) and child in id_map:
                value[key] = id_map[child]
            else:
                _rewrite_app_widget_ids(child, id_map)
    elif isinstance(value, list):
        for child in value:
            _rewrite_app_widget_ids(child, id_map)


def build_getting_started(reference_repo: Path) -> JsonDict:
    """Build the onboarding catalog from the reference backend."""

    root = reference_repo / "reference-backend"
    entries: list[CatalogEntry] = []
    for path in sorted(root.glob("widgets_*.py")):
        entries.extend(_python_catalog(path, snake_slug(path.stem)))
    widgets, id_map = _merge_entries(entries)
    apps = json.loads((root / "apps.json").read_text(encoding="utf-8"))
    _rewrite_app_widget_ids(apps, id_map)
    return {"widgets": widgets, "apps": apps}


def _source_slug(path: Path, catalog_root: Path) -> str:
    relative = path.parent.relative_to(catalog_root)
    parts = relative.parts or (catalog_root.name,)
    return snake_slug("_".join(parts))


def build_widget_examples(reference_repo: Path) -> JsonDict:
    """Build the combined widget and parameter examples catalog."""

    entries: list[CatalogEntry] = []
    for directory_name in ("widget-types", "parameters-types", "ssrm_mode"):
        catalog_root = reference_repo / directory_name
        for path in sorted(catalog_root.rglob("widgets.json")):
            entries.extend(_json_catalog(path, _source_slug(path, catalog_root)))
        for path in sorted(catalog_root.rglob("*.py")):
            source_slug = _source_slug(path, catalog_root)
            entries.extend(_python_catalog(path, source_slug))
    widgets, _ = _merge_entries(entries)
    return {"widgets": widgets, "apps": []}


def _write_catalog(path: Path, payload: JsonDict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main(
    reference_repo: Path = REFERENCE_REPO,
    output_dir: Path = DATA_DIR,
) -> None:
    """Generate both reference fixture catalogs."""

    if not reference_repo.is_dir():
        raise FileNotFoundError(
            f"Reference repository not found at {reference_repo}. Clone {REFERENCE_REPO_URL}."
        )
    _write_catalog(
        output_dir / "getting_started.json", build_getting_started(reference_repo)
    )
    _write_catalog(
        output_dir / "widget_examples.json", build_widget_examples(reference_repo)
    )


if __name__ == "__main__":
    main()
