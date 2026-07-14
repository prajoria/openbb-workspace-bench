from __future__ import annotations

import pytest

from workspace_bench.core.models import FixtureBackendRef, TaskSuiteManifest
from workspace_bench.core.runner import (
    load_builtin_tasks,
    task_workspace_baseline,
)
from workspace_bench.workspace.default_setup import (
    DEFAULT_WORKSPACE_VERSION,
    ONBOARD_A_WORKSPACE_VERSION,
    ONBOARD_B_WORKSPACE_VERSION,
    apply_workspace_baseline,
    baseline_fixture_backends,
    build_default_workspace,
    default_workspace_hash,
    required_baseline_backends,
)
from workspace_bench.workspace.widget_params import rects_overlap
from workspace_bench.workspace.fixtures import (
    build_stark_enterprise_backend,
    build_stark_enterprise_x_backend,
    build_stark_enterprise_y_backend,
)
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


def test_usage_and_default_suites_declare_the_default_workspace() -> None:
    usage_task = load_builtin_tasks("enterprise-apps-usage")[0]
    default_task = load_builtin_tasks("enterprise-apps-default")[0]

    assert task_workspace_baseline(usage_task) == DEFAULT_WORKSPACE_VERSION
    assert task_workspace_baseline(default_task) == DEFAULT_WORKSPACE_VERSION


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
        "stark-enterprise-x",
        "support-daloopa-skills",
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


_ONBOARD_EXPECTED_NAMES = {
    ONBOARD_A_WORKSPACE_VERSION: [
        "Home",
        "Portfolio Command Center",
        "Equity Research Workbench",
        "Compliance Surveillance Hub",
        "Morning Markets",
        "IC Prep - Q3 Review",
        "Ops Daily Checks",
    ],
    ONBOARD_B_WORKSPACE_VERSION: [
        "Home",
        "Execution Desk",
        "Risk & Exposure Monitor",
        "Fund Operations Control Tower",
        "Trade Desk Morning",
        "Client Review Pack",
        "Quant Ideas Scratchpad",
    ],
}


@pytest.mark.parametrize(
    "version", [ONBOARD_A_WORKSPACE_VERSION, ONBOARD_B_WORKSPACE_VERSION]
)
def test_stark_onboard_workspace_composition(version: str) -> None:
    state = build_default_workspace(version)
    dashboards = state["dashboards"]
    stark = build_stark_enterprise_backend()
    app_names = {str(app["name"]) for app in stark.apps}

    names = [dashboard["name"] for dashboard in dashboards]
    assert names == _ONBOARD_EXPECTED_NAMES[version]
    personal = dashboards[4:]
    assert all(dashboard["name"] not in app_names for dashboard in personal)

    for dashboard in dashboards[1:]:
        tab_ids = {tab["id"] for tab in dashboard["tabs"]}
        rects_by_tab: dict[str, list[dict]] = {}
        for widget in dashboard["widgets"]:
            assert widget["origin"] == stark.name
            assert widget["widget_id"] in stark.widgets
            assert widget["tab_id"] in tab_ids
            layout = widget["layout"]
            assert layout["x"] >= 0 and layout["y"] >= 0
            assert layout["w"] > 0 and layout["h"] > 0
            assert layout["x"] + layout["w"] <= 40
            rects_by_tab.setdefault(widget["tab_id"], []).append(layout)
        for rects in rects_by_tab.values():
            for index, rect in enumerate(rects):
                for other in rects[index + 1 :]:
                    assert not rects_overlap(rect, other)

    # Personal dashboards mix widgets across at least two source apps each.
    for dashboard in personal:
        prefixes = {widget["widget_id"].split("_")[0] for widget in dashboard["widgets"]}
        assert len(prefixes) >= 2

    assert default_workspace_hash(version) == default_workspace_hash(version)
    assert default_workspace_hash(version) != default_workspace_hash(
        DEFAULT_WORKSPACE_VERSION
    )


def test_onboard_a_and_b_are_distinct_worlds() -> None:
    assert default_workspace_hash(ONBOARD_A_WORKSPACE_VERSION) != default_workspace_hash(
        ONBOARD_B_WORKSPACE_VERSION
    )


def test_onboard_baseline_resolves_in_simulated_workspace() -> None:
    manifest = TaskSuiteManifest(
        suite_id="onboard-test",
        workspace_baseline=ONBOARD_A_WORKSPACE_VERSION,
    )
    fixtures, state = apply_workspace_baseline(manifest, (), {})

    assert [fixture.name for fixture in fixtures] == ["stark-enterprise-x"]
    workspace = SimulatedWorkspace()
    workspace.reset(backends=fixtures, initial_state=state)
    assert len(workspace.snapshot()["dashboards"]) == 7


def test_workspace_backends_axis_mixes_and_matches() -> None:
    assert baseline_fixture_backends(ONBOARD_A_WORKSPACE_VERSION) == ("stark-enterprise-x",)
    assert required_baseline_backends(ONBOARD_A_WORKSPACE_VERSION) == ("stark-enterprise-x",)

    override = TaskSuiteManifest.from_dict(
        {
            "suite_id": "mix-test",
            "workspace_baseline": ONBOARD_A_WORKSPACE_VERSION,
            "workspace_backends": ["stark-enterprise-x", "getting-started"],
        }
    )
    fixtures, _ = apply_workspace_baseline(override, (), {})
    assert [fixture.name for fixture in fixtures] == ["stark-enterprise-x", "getting-started"]

    backends_only = TaskSuiteManifest.from_dict(
        {"suite_id": "mix-test", "workspace_backends": ["stark-enterprise-x"]}
    )
    task_state = {"dashboard": {"name": "Task Dashboard"}}
    fixtures, state = apply_workspace_baseline(backends_only, (), task_state)
    assert [fixture.name for fixture in fixtures] == ["stark-enterprise-x"]
    assert state == task_state

    missing_required = TaskSuiteManifest.from_dict(
        {
            "suite_id": "mix-test",
            "workspace_baseline": ONBOARD_A_WORKSPACE_VERSION,
            "workspace_backends": ["support-daloopa-skills"],
        }
    )
    with pytest.raises(ValueError, match="requires backends"):
        apply_workspace_baseline(missing_required, (), {})


def test_task_suite_manifest_validates_workspace_backends() -> None:
    with pytest.raises(ValueError, match="workspace_backends"):
        TaskSuiteManifest.from_dict({"suite_id": "x", "workspace_backends": []})
    with pytest.raises(ValueError, match="unique"):
        TaskSuiteManifest.from_dict(
            {"suite_id": "x", "workspace_backends": ["stark-enterprise-x", "stark-enterprise-x"]}
        )


def test_stark_data_worlds_share_catalog_and_differ_only_in_data() -> None:
    canonical = build_stark_enterprise_backend()
    world_x = build_stark_enterprise_x_backend()
    world_y = build_stark_enterprise_y_backend()

    assert canonical.name == world_x.name == world_y.name
    assert world_x.widgets == canonical.widgets
    assert world_y.widgets != canonical.widgets
    assert world_y.apps == canonical.apps

    def catalog(backend) -> dict:
        return {
            widget_id: {key: value for key, value in definition.items() if key != "data"}
            for widget_id, definition in backend.widgets.items()
        }

    assert catalog(world_y) == catalog(world_x)
    # Determinism: rebuilding Y yields identical data.
    assert build_stark_enterprise_y_backend().widgets == world_y.widgets
    # Filters keep working against values that exist in world Y's data.
    rows_y = world_y.widgets["risk_exposure_monitor_dashboard_var_trend"]["data"]
    period = rows_y[0]["period"]
    filtered = world_y.fetch_widget_data(
        "risk_exposure_monitor_dashboard_var_trend", {"period": period}
    )
    assert filtered and all(row["period"] == period for row in filtered)


def test_world_y_varies_rows_and_entities_within_widget_contracts() -> None:
    from workspace_bench.workspace.fixtures import (
        _CRYPTO_SUBSTITUTION_POOL,
        _EQUITY_SUBSTITUTION_POOL,
        _FREE_ENTITY_FIELDS,
    )

    substitution_pool = set(_EQUITY_SUBSTITUTION_POOL) | set(_CRYPTO_SUBSTITUTION_POOL)
    from workspace_bench.workspace.widget_params import flatten_params

    canonical = build_stark_enterprise_backend()
    world_y = build_stark_enterprise_y_backend()

    shrunk = 0
    grown = 0
    free_entity_fields_seen = 0
    for widget_id, definition in canonical.widgets.items():
        rows_c = definition.get("data")
        if not isinstance(rows_c, list) or not all(isinstance(r, dict) for r in rows_c):
            continue
        rows_y = world_y.widgets[widget_id]["data"]
        assert 2 <= len(rows_y) <= round(len(rows_c) * 1.5)
        if len(rows_y) < len(rows_c):
            shrunk += 1
        elif len(rows_y) > len(rows_c):
            grown += 1
        declared = {}
        for param in flatten_params(definition):
            name, options = param.get("paramName"), param.get("options")
            if name and isinstance(options, list):
                values = {
                    option.get("value") if isinstance(option, dict) else option
                    for option in options
                }
                values = {v for v in values if isinstance(v, str) and v}
                if values:
                    declared[str(name)] = values
        for row in rows_y:
            for field, value in row.items():
                if not isinstance(value, str):
                    continue
                if field in declared:
                    # Param-backed values stay inside the widget's own options.
                    assert value in declared[field], (widget_id, field, value)
                elif field in _FREE_ENTITY_FIELDS:
                    free_entity_fields_seen += 1
                    assert value in substitution_pool, (widget_id, field, value)
                elif len(rows_y) > len(rows_c):
                    # Growth is only allowed when every string column is
                    # managed, so clones never copy an identity column.
                    raise AssertionError((widget_id, field, value))

    # The variation is broad, not cosmetic: rows are lost in many widgets,
    # gained in some, and free entity fields really substitute.
    assert shrunk > 100
    assert grown >= 10
    assert free_entity_fields_seen > 0
    canonical_entities = {
        row[field]
        for definition in canonical.widgets.values()
        if isinstance(definition.get("data"), list)
        for row in definition["data"]
        if isinstance(row, dict)
        for field in _FREE_ENTITY_FIELDS
        if isinstance(row.get(field), str)
    }
    assert not canonical_entities & substitution_pool


def test_any_stark_world_satisfies_the_baseline_requirement() -> None:
    manifest = TaskSuiteManifest.from_dict(
        {
            "suite_id": "world-test",
            "workspace_baseline": ONBOARD_A_WORKSPACE_VERSION,
            "workspace_backends": ["stark-enterprise-y"],
        }
    )
    fixtures, state = apply_workspace_baseline(manifest, (), {})

    assert [fixture.name for fixture in fixtures] == ["stark-enterprise-y"]
    workspace = SimulatedWorkspace()
    workspace.reset(backends=fixtures, initial_state=state)
    assert len(workspace.snapshot()["dashboards"]) == 7


def test_at_most_one_stark_world_per_episode() -> None:
    manifest = TaskSuiteManifest.from_dict(
        {
            "suite_id": "world-test",
            "workspace_baseline": ONBOARD_A_WORKSPACE_VERSION,
            "workspace_backends": ["stark-enterprise-x", "stark-enterprise-y"],
        }
    )
    with pytest.raises(ValueError, match="one Stark data world"):
        apply_workspace_baseline(manifest, (), {})


def test_workspace_skills_axis_filters_the_skill_surface() -> None:
    from dataclasses import replace

    from workspace_bench.core.episode import WorkspaceEpisode
    from workspace_bench.core.models import Task

    manifest = TaskSuiteManifest.from_dict(
        {
            "suite_id": "skills-test",
            "workspace_baseline": ONBOARD_A_WORKSPACE_VERSION,
            "workspace_skills": ["finance-earnings-prep", "finance-comps"],
        }
    )
    task = Task.from_dict(
        {
            "id": "probe",
            "category": "read",
            "family": "probe",
            "difficulty": "easy",
            "prompt": "probe",
            "allowed_tools": ["get_skill_content"],
            "success": {},
            "oracle_tool_calls": [{"tool": "get_skill_content", "args": {}}],
            "limits": {"max_turns": 1},
        }
    )
    episode = WorkspaceEpisode(replace(task, suite=manifest))

    listed = {skill["slug"] for skill in episode.workspace.skills.values()}
    assert listed == {"finance-earnings-prep", "finance-comps"}
    snapshot_skills = {skill["slug"] for skill in episode.snapshot()["skills"]}
    assert snapshot_skills == listed

    # Task-level override wins over the manifest.
    override = replace(task, suite=manifest, workspace_skills=("daloopa-tearsheet",))
    episode = WorkspaceEpisode(override)
    assert set(episode.workspace.skills) == {"daloopa-tearsheet"}

    with pytest.raises(KeyError, match="Unknown workspace skill"):
        WorkspaceEpisode(
            replace(task, suite=manifest, workspace_skills=("no-such-skill",))
        )
    with pytest.raises(ValueError, match="workspace_skills"):
        TaskSuiteManifest.from_dict({"suite_id": "x", "workspace_skills": []})


def test_empty_string_baseline_means_explicitly_none() -> None:
    manifest = TaskSuiteManifest.from_dict(
        {"suite_id": "clear-test", "workspace_baseline": DEFAULT_WORKSPACE_VERSION}
    )
    task_state = {"dashboard": {"name": "Task Dashboard"}}
    fixtures, state = apply_workspace_baseline(
        manifest,
        (),
        task_state,
        baseline_override="",
        backends_override=("stark-enterprise-x",),
    )

    # The task-level "" clears the suite baseline: bare workspace, task state
    # untouched, only the declared backends connected.
    assert state == task_state
    assert [fixture.name for fixture in fixtures] == ["stark-enterprise-x"]

    manifest_none = TaskSuiteManifest.from_dict(
        {"suite_id": "clear-test", "workspace_baseline": ""}
    )
    assert manifest_none.workspace_baseline == ""


def test_task_level_axis_overrides_win_over_the_manifest() -> None:
    manifest = TaskSuiteManifest.from_dict(
        {"suite_id": "override-test", "workspace_baseline": DEFAULT_WORKSPACE_VERSION}
    )
    fixtures, state = apply_workspace_baseline(
        manifest,
        (),
        {},
        baseline_override=ONBOARD_B_WORKSPACE_VERSION,
        backends_override=("stark-enterprise-y",),
    )

    assert [fixture.name for fixture in fixtures] == ["stark-enterprise-y"]
    assert [dashboard["name"] for dashboard in state["dashboards"]] == (
        _ONBOARD_EXPECTED_NAMES[ONBOARD_B_WORKSPACE_VERSION]
    )
