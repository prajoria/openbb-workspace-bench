"""Versioned default Workspace initial states for task suites."""

from __future__ import annotations

import copy
import hashlib
import json

from workspace_bench.core.models import FixtureBackendRef, JsonDict, TaskSuiteManifest
from workspace_bench.workspace.fixtures import build_stark_enterprise_backend
from workspace_bench.workspace.widget_params import sanitize_data_args


DEFAULT_WORKSPACE_VERSION = "default-v1"

_BASELINE_FIXTURE_BACKENDS: dict[str, tuple[str, ...]] = {
    DEFAULT_WORKSPACE_VERSION: (
        "stark-enterprise",
        "daloopa",
        "getting-started",
        "widget-examples",
    ),
}


def build_default_workspace(version: str = DEFAULT_WORKSPACE_VERSION) -> JsonDict:
    """Build the initial state for a versioned default Workspace."""

    _require_known_version(version)
    stark = build_stark_enterprise_backend()
    dashboards: list[JsonDict] = [
        {
            "name": "Home",
            "tabs": [{"id": "", "name": ""}],
            "widgets": [],
            "activate": True,
        }
    ]

    for app in stark.apps:
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
        dashboards.append(
            {
                "name": str(app["name"]),
                "tabs": dashboard_tabs,
                "widgets": dashboard_widgets,
                "activate": False,
            }
        )

    return {"dashboards": dashboards}


def baseline_fixture_backends(version: str) -> tuple[str, ...]:
    """Return fixture backend names attached by a default Workspace version."""

    _require_known_version(version)
    return _BASELINE_FIXTURE_BACKENDS[version]


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
) -> tuple[tuple[FixtureBackendRef, ...], JsonDict]:
    """Apply a suite baseline beneath a task's fixtures and initial state."""

    version = manifest.workspace_baseline if manifest else None
    if version is None:
        return task_fixtures, task_initial_state

    baseline_state = build_default_workspace(version)
    merged_state = copy.deepcopy(task_initial_state)
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

    fixtures = tuple(
        FixtureBackendRef(name=name) for name in baseline_fixture_backends(version)
    )
    seen_names = {fixture.name for fixture in fixtures}
    merged_fixtures = list(fixtures)
    for fixture in task_fixtures:
        if fixture.name in seen_names:
            continue
        merged_fixtures.append(fixture)
        seen_names.add(fixture.name)
    return tuple(merged_fixtures), merged_state


def _require_known_version(version: str) -> None:
    if version not in _BASELINE_FIXTURE_BACKENDS:
        raise ValueError(f"unknown default Workspace version: {version!r}")
