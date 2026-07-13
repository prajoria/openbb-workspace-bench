from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Callable

import pytest

from workspace_bench.workspace.backend_validation import (
    WIDGET_VIZ_TYPE_ALIASES,
    WIDGET_VIZ_TYPES,
)
from workspace_bench.workspace.fixtures import (
    FixtureBackend,
    build_getting_started_backend,
    build_widget_examples_backend,
    default_fixture_backends,
)
from workspace_bench.workspace.widget_params import flatten_params, sanitize_data_args


REPO = Path(__file__).resolve().parents[1]
GENERATOR_PATH = REPO / "scripts/generators/generate_reference_fixture_data.py"
DATA_DIR = REPO / "src/workspace_bench/workspace/data"


def _load_generator() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "generate_reference_fixture_data", GENERATOR_PATH
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("builder", "catalog_name", "expected_count"),
    [
        (build_getting_started_backend, "getting_started.json", 70),
        (build_widget_examples_backend, "widget_examples.json", 30),
    ],
)
def test_reference_catalogs_preserve_types_and_param_defaults(
    builder: Callable[[], FixtureBackend],
    catalog_name: str,
    expected_count: int,
) -> None:
    # Observed reference counts: getting-started=70, widget-examples=30.
    backend = builder()
    payload = json.loads((DATA_DIR / catalog_name).read_text(encoding="utf-8"))

    assert backend.widgets == payload["widgets"]
    assert len(backend.widgets) == expected_count > 0
    for definition in backend.widgets.values():
        assert definition["type"] in WIDGET_VIZ_TYPES
        assert definition["type"] not in WIDGET_VIZ_TYPE_ALIASES
        params = flatten_params(definition)
        defaults = {
            str(param["paramName"]): param["value"]
            for param in params
            if param.get("paramName") and param.get("value") is not None
        }
        sanitized = sanitize_data_args(definition, {}, mode="create")
        assert all(sanitized[name] == value for name, value in defaults.items())


@pytest.mark.parametrize(
    "backend",
    [build_getting_started_backend(), build_widget_examples_backend()],
)
def test_reference_backends_expose_schema_and_generic_table_data(
    backend: FixtureBackend,
) -> None:
    sample_id = next(iter(backend.widgets))
    schema = backend.get_widget_schema(sample_id)
    assert schema["widget_id"] == sample_id
    assert schema["origin"] == backend.name

    table_id = next(
        widget_id
        for widget_id, definition in backend.widgets.items()
        if definition["type"] == "table"
    )
    rows = backend.fetch_widget_data(table_id, {})
    assert isinstance(rows, list)
    assert rows


def test_reference_fixture_registry_uses_slug_and_display_name() -> None:
    registry = default_fixture_backends()

    assert registry["getting-started"] is registry["Getting Started"]
    assert registry["widget-examples"] is registry["Widget Examples"]


@pytest.mark.skipif(
    not (REPO / "references/openbb-backend-examples").exists(),
    reason="reference source repo is local-only material; committed catalogs are still validated",
)
def test_reference_generator_is_byte_deterministic(tmp_path: Path) -> None:
    generator = _load_generator()
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"

    generator.main(output_dir=first_dir)
    generator.main(output_dir=second_dir)

    for name in ("getting_started.json", "widget_examples.json"):
        first = (first_dir / name).read_bytes()
        second = (second_dir / name).read_bytes()
        assert hashlib.sha256(first).digest() == hashlib.sha256(second).digest()
        assert first == (DATA_DIR / name).read_bytes()


def test_reference_generator_missing_repo_error_names_source(tmp_path: Path) -> None:
    generator = _load_generator()

    with pytest.raises(FileNotFoundError, match="backend-examples-for-openbb-workspace"):
        generator.main(reference_repo=tmp_path / "missing", output_dir=tmp_path)
