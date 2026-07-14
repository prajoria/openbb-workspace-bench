"""Versioned default Workspace initial states for task suites.

Suites select two independent axes in their manifest, tasks may override
either axis, and both mix and match:

- ``workspace_baseline`` — a versioned initial state (which dashboards exist
  when the episode starts). ``all-stark-enterprise-apps`` is built from the Stark catalog
  (Home plus every app); the onboard states are loaded from the materialized
  files under ``data/initial_states/`` produced by
  ``scripts/generators/generate_onboard_states.py``.
- ``workspace_backends`` — the fixture backends connected to the Workspace.
  Omitted, it falls back to the baseline version's default backend set.

Each initial-state version declares the backends it requires; a manifest that
overrides ``workspace_backends`` without them is rejected at episode setup.
"""

from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Callable
from dataclasses import replace
from importlib import resources

from workspace_bench.core.models import (
    KNOWN_WORKSPACE_BASELINES,
    FixtureBackendRef,
    JsonDict,
    TaskSuiteManifest,
)
from workspace_bench.workspace.fixtures import (
    LEGACY_BACKEND_SLUGS,
    STARK_DATA_WORLDS,
    FixtureBackend,
    build_stark_enterprise_backend,
)
from workspace_bench.workspace.widget_params import sanitize_data_args


DEFAULT_WORKSPACE_VERSION = "all-stark-enterprise-apps"
ONBOARD_A_WORKSPACE_VERSION = "stark-onboard-a"
ONBOARD_B_WORKSPACE_VERSION = "stark-onboard-b"

_DEFAULT_BASELINE_BACKENDS: dict[str, tuple[str, ...]] = {
    DEFAULT_WORKSPACE_VERSION: (
        "stark-enterprise-x",
        "support-daloopa-skills",
        "getting-started",
        "widget-examples",
    ),
    ONBOARD_A_WORKSPACE_VERSION: ("stark-enterprise-x",),
    ONBOARD_B_WORKSPACE_VERSION: ("stark-enterprise-x",),
}

_REQUIRED_BASELINE_BACKENDS: dict[str, tuple[str, ...]] = {
    DEFAULT_WORKSPACE_VERSION: ("stark-enterprise-x",),
    ONBOARD_A_WORKSPACE_VERSION: ("stark-enterprise-x",),
    ONBOARD_B_WORKSPACE_VERSION: ("stark-enterprise-x",),
}


def build_default_workspace(version: str = DEFAULT_WORKSPACE_VERSION) -> JsonDict:
    """Build the initial state for a versioned default Workspace."""

    _require_known_version(version)
    return _INITIAL_STATE_BUILDERS[version]()


def _build_default_v1_state() -> JsonDict:
    stark = build_stark_enterprise_backend()
    dashboards: list[JsonDict] = [_home_dashboard()]
    for app in stark.apps:
        dashboards.append(_instantiate_app(stark, app))
    return {"dashboards": dashboards}


def _load_initial_state_file(filename: str) -> JsonDict:
    path = (
        resources.files("workspace_bench.data") / "initial_states" / filename
    )
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload["initial_state"]


def _home_dashboard() -> JsonDict:
    return {
        "name": "Home",
        "tabs": [{"id": "", "name": ""}],
        "widgets": [],
        "activate": True,
    }


def _instantiate_app(stark: FixtureBackend, app: JsonDict) -> JsonDict:
    tabs = app.get("tabs", {})
    if not isinstance(tabs, dict):
        raise ValueError(f"Stark app {app.get('name')!r} tabs must be an object")
    dashboard_tabs: list[JsonDict] = []
    dashboard_widgets: list[JsonDict] = []
    for tab in tabs.values():
        tab_id = str(tab["id"])
        dashboard_tabs.append({"id": tab_id, "name": str(tab["name"])})
        for entry in tab.get("layout", []):
            widget_id = str(entry["i"])
            definition = stark.widgets[widget_id]
            raw_data_args = entry.get("state", {}).get("params", {}) or {}
            data_args = sanitize_data_args(
                definition,
                copy.deepcopy(raw_data_args),
                mode="create",
            )
            dashboard_widgets.append(
                {
                    "origin": stark.name,
                    "widget_id": widget_id,
                    "tab_id": tab_id,
                    "layout": {
                        key: copy.deepcopy(entry[key])
                        for key in ("x", "y", "w", "h")
                    },
                    "data_args": data_args,
                }
            )
    return {
        "name": str(app["name"]),
        "tabs": dashboard_tabs,
        "widgets": dashboard_widgets,
        "activate": False,
    }


_INITIAL_STATE_BUILDERS: dict[str, Callable[[], JsonDict]] = {
    DEFAULT_WORKSPACE_VERSION: _build_default_v1_state,
    ONBOARD_A_WORKSPACE_VERSION: lambda: _load_initial_state_file("stark_onboard_a.json"),
    ONBOARD_B_WORKSPACE_VERSION: lambda: _load_initial_state_file("stark_onboard_b.json"),
}

if set(KNOWN_WORKSPACE_BASELINES) != set(_INITIAL_STATE_BUILDERS):
    raise RuntimeError(
        "KNOWN_WORKSPACE_BASELINES and default_setup builders are out of sync"
    )


def baseline_fixture_backends(version: str) -> tuple[str, ...]:
    """Return the default fixture backends of a default Workspace version."""

    _require_known_version(version)
    return _DEFAULT_BASELINE_BACKENDS[version]


def required_baseline_backends(version: str) -> tuple[str, ...]:
    """Return the backends an initial-state version cannot resolve without."""

    _require_known_version(version)
    return _REQUIRED_BASELINE_BACKENDS[version]


def default_workspace_hash(version: str) -> str:
    """Return the SHA-256 digest of a canonical default Workspace state."""

    canonical = json.dumps(
        build_default_workspace(version),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def apply_workspace_baseline(
    manifest: TaskSuiteManifest | None,
    task_fixtures: tuple[FixtureBackendRef, ...],
    task_initial_state: JsonDict,
    *,
    baseline_override: str | None = None,
    backends_override: tuple[str, ...] | None = None,
) -> tuple[tuple[FixtureBackendRef, ...], JsonDict]:
    """Apply a suite's baseline axes beneath a task's fixtures and state.

    A task-level override (state-variant tasks) wins over the suite manifest
    on each axis independently.
    """

    version = (
        baseline_override
        if baseline_override is not None
        else (manifest.workspace_baseline if manifest else None)
    )
    if version == "":
        # Explicitly no baseline (a task-level "" clears a suite baseline).
        version = None
    backend_names = (
        backends_override
        if backends_override is not None
        else (manifest.workspace_backends if manifest else None)
    )
    if version is None and backend_names is None:
        return task_fixtures, task_initial_state

    if backend_names is None:
        assert version is not None
        backend_names = baseline_fixture_backends(version)
    else:
        # Pre-rename manifests and tasks reference legacy slugs.
        backend_names = tuple(
            LEGACY_BACKEND_SLUGS.get(name, name) for name in backend_names
        )
        if version is not None:
            available = set(backend_names)
            missing = sorted(
                required
                for required in required_baseline_backends(version)
                if required not in available
                # Any Stark data world satisfies a Stark requirement: the
                # worlds share one catalog and display name and differ only
                # in data.
                and not (
                    required in STARK_DATA_WORLDS
                    and available & set(STARK_DATA_WORLDS)
                )
            )
            if missing:
                raise ValueError(
                    f"workspace_baseline {version!r} requires backends {missing}; "
                    "add them to workspace_backends"
                )

    merged_state = copy.deepcopy(task_initial_state)
    if version is not None:
        baseline_state = build_default_workspace(version)
        task_dashboard = merged_state.pop("dashboard", None)
        task_dashboards = merged_state.pop("dashboards", None)
        appended_dashboards: list[JsonDict] = []
        if isinstance(task_dashboards, list) and task_dashboards:
            appended_dashboards.extend(
                copy.deepcopy(item) for item in task_dashboards if isinstance(item, dict)
            )
        elif isinstance(task_dashboard, dict):
            appended_dashboards.append(copy.deepcopy(task_dashboard))
        for dashboard in appended_dashboards:
            dashboard.setdefault("activate", False)
        merged_state["dashboards"] = [
            *baseline_state["dashboards"],
            *appended_dashboards,
        ]

    fixtures = tuple(FixtureBackendRef(name=name) for name in backend_names)
    seen_names = {fixture.name for fixture in fixtures}
    merged_fixtures = list(fixtures)
    for fixture in task_fixtures:
        # Pre-rename task files reference legacy slugs; dedupe canonically.
        canonical = LEGACY_BACKEND_SLUGS.get(fixture.name, fixture.name)
        if canonical in seen_names:
            continue
        merged_fixtures.append(
            fixture if fixture.name == canonical else replace(fixture, name=canonical)
        )
        seen_names.add(canonical)
    worlds = [fixture.name for fixture in merged_fixtures if fixture.name in STARK_DATA_WORLDS]
    if len(worlds) > 1:
        raise ValueError(
            f"at most one Stark data world may be connected per episode; got {worlds}"
        )
    return tuple(merged_fixtures), merged_state


def _require_known_version(version: str) -> None:
    if version not in _INITIAL_STATE_BUILDERS:
        raise ValueError(f"unknown default Workspace version: {version!r}")
