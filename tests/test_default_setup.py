from __future__ import annotations

import pytest

from workspace_bench.core.models import FixtureBackendRef, TaskSuiteManifest
from workspace_bench.core.runner import (
    load_builtin_tasks,
    override_tasks_workspace_baseline,
    task_workspace_baseline,
)
from workspace_bench.workspace.default_setup import (
    DEFAULT_WORKSPACE_VERSION,
    apply_workspace_baseline,
    build_default_workspace,
    default_workspace_hash,
)
from workspace_bench.workspace.fixtures import build_stark_enterprise_backend
from workspace_bench.workspace.simulated_workspace import SimulatedWorkspace
from workspace_bench.workspace.widget_params import flatten_params, sanitize_data_args


def _baseline_manifest() -> TaskSuiteManifest:
    return TaskSuiteManifest(
        suite_id="baseline-test",
        workspace_baseline=DEFAULT_WORKSPACE_VERSION,
    )


def test_default_workspace_build_and_hash_are_deterministic() -> None:
    first = build_default_workspace()
    second = build_default_workspace()

    assert first == second
    assert default_workspace_hash(DEFAULT_WORKSPACE_VERSION) == default_workspace_hash(
        DEFAULT_WORKSPACE_VERSION
    )


def test_task_suite_manifest_validates_workspace_baseline() -> None:
    manifest = TaskSuiteManifest.from_dict(
        {"suite_id": "baseline-test", "workspace_baseline": DEFAULT_WORKSPACE_VERSION}
    )

    assert manifest.workspace_baseline == DEFAULT_WORKSPACE_VERSION
    with pytest.raises(ValueError, match="workspace_baseline"):
        TaskSuiteManifest.from_dict(
            {"suite_id": "baseline-test", "workspace_baseline": "default-v2"}
        )


def test_workspace_baseline_override_preserves_manifest_default() -> None:
    usage_task = load_builtin_tasks("enterprise-apps-usage")[0]
    default_task = load_builtin_tasks("enterprise-apps-default")[0]

    assert task_workspace_baseline(usage_task) == "minimal"
    assert task_workspace_baseline(default_task) == DEFAULT_WORKSPACE_VERSION
    overridden = override_tasks_workspace_baseline(
        [usage_task], DEFAULT_WORKSPACE_VERSION
    )[0]
    restored = override_tasks_workspace_baseline([default_task], "minimal")[0]
    assert task_workspace_baseline(overridden) == DEFAULT_WORKSPACE_VERSION
    assert task_workspace_baseline(restored) == "minimal"
    assert overridden.source_path == usage_task.source_path


def test_default_workspace_maps_all_stark_apps_and_declared_params() -> None:
    state = build_default_workspace()
    dashboards = state["dashboards"]
    stark = build_stark_enterprise_backend()

    assert len(dashboards) == 24
    assert dashboards[0] == {
        "name": "Home",
        "tabs": [{"id": "", "name": ""}],
        "widgets": [],
        "activate": True,
    }
    assert [dashboard["name"] for dashboard in dashboards[1:]] == [
        app["name"] for app in stark.apps
    ]

    for dashboard in dashboards[1:]:
        assert dashboard["activate"] is False
        for widget in dashboard["widgets"]:
            assert widget["origin"] == stark.name
            definition = stark.widgets[widget["widget_id"]]
            declared = {
                str(param["paramName"])
                for param in flatten_params(definition)
                if param.get("paramName")
            }
            assert set(widget["data_args"]) <= declared

    sample = dashboards[1]["widgets"][0]
    assert sanitize_data_args(
        stark.widgets[sample["widget_id"]],
        sample["data_args"],
        mode="create",
    ) == sample["data_args"]


def test_workspace_baseline_merge_appends_dashboard_and_dedupes_fixtures() -> None:
    task_dashboard = {
        "name": "Task Dashboard",
        "activate": True,
        "tabs": [{"id": "task", "name": "Task"}],
        "widgets": [],
    }
    fixtures, state = apply_workspace_baseline(
        _baseline_manifest(),
        (
            FixtureBackendRef("daloopa"),
            FixtureBackendRef("equities"),
            FixtureBackendRef("equities"),
        ),
        {
            "dashboard": task_dashboard,
            "custom_backends": [{"name": "Task Backend"}],
        },
    )

    assert [fixture.name for fixture in fixtures] == [
        "stark-enterprise",
        "daloopa",
        "getting-started",
        "widget-examples",
        "equities",
    ]
    assert state["dashboards"][-1] == task_dashboard
    assert state["custom_backends"] == [{"name": "Task Backend"}]

    workspace = SimulatedWorkspace()
    workspace.reset(backends=fixtures, initial_state=state)
    snapshot = workspace.snapshot()
    assert snapshot["dashboard_composition"]["name"] == "Task Dashboard"


def test_workspace_baseline_keeps_home_active_without_explicit_activation() -> None:
    fixtures, state = apply_workspace_baseline(
        _baseline_manifest(),
        (),
        {"dashboard": {"name": "Inactive Task Dashboard"}},
    )

    assert state["dashboards"][-1]["activate"] is False
    workspace = SimulatedWorkspace()
    workspace.reset(backends=fixtures, initial_state=state)
    assert workspace.snapshot()["dashboard_composition"]["name"] == "Home"


def test_simulated_workspace_resets_with_default_workspace() -> None:
    fixtures, state = apply_workspace_baseline(_baseline_manifest(), (), {})
    workspace = SimulatedWorkspace()

    workspace.reset(backends=fixtures, initial_state=state)

    assert len(workspace.snapshot()["dashboards"]) == 24
