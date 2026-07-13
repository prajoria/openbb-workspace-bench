"""Unit tests for the pure live-parity helpers (no network)."""

from __future__ import annotations

import pytest

from workspace_bench.core.models import Task
from workspace_bench.core.runner import find_task
from workspace_bench.workspace.live_parity import (
    DEFAULT_ORIGIN_MAP,
    LiveParityIneligible,
    PlaceholderMapper,
    check_eligibility,
    derive_seed_plan,
    extract_dashboard_id,
    extract_widget_uuid,
    grade_agreement,
    map_origin_values,
    normalize_live_snapshot,
)


@pytest.fixture()
def stark_read_task() -> Task:
    return find_task("enterprise-apps-usage/read/alert_trend")


def test_map_origin_values_rewrites_only_origin_keys() -> None:
    payload = {
        "origin": "Bench Stark Enterprise",
        "note": "keep Bench Stark Enterprise in prose",
        "nested": [{"backend_name": "Bench Stark Enterprise", "widget_id": "w"}],
    }
    mapped = map_origin_values(payload, DEFAULT_ORIGIN_MAP)
    assert mapped["origin"] == "Stark Fund"
    assert mapped["nested"][0]["backend_name"] == "Stark Fund"
    assert mapped["note"] == "keep Bench Stark Enterprise in prose"
    assert payload["origin"] == "Bench Stark Enterprise"  # input untouched


def test_placeholder_mapper_round_trips_widget_uuids() -> None:
    mapper = PlaceholderMapper()
    assert mapper.record_widget("live-aaa") == "widget_001"
    assert mapper.record_widget("live-bbb") == "widget_002"
    mapper.record_dashboard("live-dash")
    outgoing = mapper.to_live({"widget_uuid": "widget_002", "dashboard_id": "dash_001"})
    assert outgoing == {"widget_uuid": "live-bbb", "dashboard_id": "live-dash"}
    incoming = mapper.to_sim({"widgets": [{"widget_uuid": "live-aaa"}]})
    assert incoming == {"widgets": [{"widget_uuid": "widget_001"}]}


def test_extract_widget_uuid_finds_nested_ids() -> None:
    assert (
        extract_widget_uuid({"data": {"widget": {"widget_uuid": "u-1", "name": "x"}}})
        == "u-1"
    )
    assert extract_widget_uuid({"data": {"widgets": [{"widget_uuid": "u-2"}]}}) == "u-2"
    assert extract_widget_uuid({"data": {"name": "no uuid"}}) is None


def test_extract_dashboard_id_reads_common_shapes() -> None:
    assert extract_dashboard_id({"data": {"dashboard_id": "d-1"}}) == "d-1"
    assert extract_dashboard_id({"data": {"dashboard": {"id": "d-2"}}}) == "d-2"
    assert extract_dashboard_id({"data": {"other": 1}}) is None


def test_eligibility_accepts_stark_read_task(stark_read_task: Task) -> None:
    check_eligibility(stark_read_task, DEFAULT_ORIGIN_MAP)


@pytest.mark.parametrize(
    "task_ref",
    [
        "enterprise-apps-usage/create/price_performance_aapl",
        "enterprise-apps-usage/create/sector_exposure_plain",
    ],
)
def test_eligibility_accepts_transcribed_production_origins(task_ref: str) -> None:
    check_eligibility(find_task(task_ref), DEFAULT_ORIGIN_MAP)


def test_eligibility_rejects_unmapped_origin(stark_read_task: Task) -> None:
    with pytest.raises(LiveParityIneligible, match="without a live mapping"):
        check_eligibility(stark_read_task, {"Some Other Backend": "X"})


def test_eligibility_rejects_unreplayable_oracle_tool() -> None:
    task = find_task("enterprise-apps-usage/backends/add_stark_enterprise")
    with pytest.raises(LiveParityIneligible):
        check_eligibility(task, DEFAULT_ORIGIN_MAP)


def test_seed_plan_reproduces_initial_dashboard(stark_read_task: Task) -> None:
    plan = derive_seed_plan(stark_read_task)
    kinds = [step.kind for step in plan.steps]
    assert kinds == ["dashboard", "tabs", "activate_tab", "widget", "layout"]
    assert plan.dashboard_name == "Data Review"
    assert plan.tab_ids == ("main",)
    assert plan.seeded_widget_count == 1
    create = plan.steps[0].call
    assert create.name == "manage_dashboard"
    assert "workspace-bench parity" in str(create.args["name"])
    widget = plan.steps[3].call
    assert widget.args["origin"] == "Bench Stark Enterprise"
    assert widget.args["data_args"] == {"fund": "Flagship Long/Short", "period": "YTD"}


def test_normalize_live_snapshot_rebuilds_sim_shape(stark_read_task: Task) -> None:
    mapper = PlaceholderMapper()
    mapper.record_dashboard("live-dash")
    mapper.record_widget("live-w1")
    mapper.record_widget("live-w2")
    dashboard_info = {
        "id": "live-dash",
        "tabs": [
            {
                "tab_id": "main",
                "tab_name": "Main",
                "widgets": [
                    {"widget_uuid": "live-w1", "name": "Alert Trend"},
                    {"widget_uuid": "live-w2", "name": "Data Note"},
                ],
                "layout": [
                    {"widget_uuid": "live-w1", "x": 0, "y": 2, "w": 20, "h": 10},
                    {"widget_uuid": "live-w2", "x": 0, "y": 12, "w": 20, "h": 6},
                ],
            }
        ],
    }
    widget_details = {
        "live-w1": {
            "origin": "Stark Fund",
            "widget_id": "compliance_surveillance_hub_alerts_alert_trend",
            "name": "Alert Trend",
            "data_args": {"fund": "Flagship Long/Short", "period": "YTD"},
        },
        "live-w2": {
            "origin": "",
            "widget_id": "",
            "name": "Data Note",
            "data": "Reviewed the data returned by compliance_surveillance_hub_alerts_alert_trend.",
        },
    }
    snapshot = normalize_live_snapshot(
        task=stark_read_task,
        dashboard_info=dashboard_info,
        dashboard_name="Data Review",
        widget_details=widget_details,
        generated_uuids={"live-w2"},
        generated_meta={"live-w2": {"widget_type": "note"}},
        mapper=mapper,
        reverse_origin_map={"Stark Fund": "Bench Stark Enterprise"},
    )
    composition = snapshot["dashboard_composition"]
    assert composition["name"] == "Data Review"
    assert [tab["id"] for tab in composition["tabs"]] == ["main"]
    widgets = composition["widgets"]
    assert widgets[0]["widget_uuid"] == "widget_001"
    assert widgets[0]["origin"] == "Bench Stark Enterprise"
    assert widgets[0]["type"] == "table"
    assert widgets[0]["generated"] is False
    assert widgets[1]["generated"] is True
    assert widgets[1]["type"] == "note"
    assert "alert_trend" in str(widgets[1]["generated_data"])
    assert widgets[1]["layout"]["tab_id"] == "main"


def test_normalized_snapshot_grades_like_the_simulator(stark_read_task: Task) -> None:
    """The live-shaped snapshot from the test above passes the real grader."""

    from workspace_bench.core.graders import grade_task
    from workspace_bench.core.models import ToolTraceEvent

    mapper = PlaceholderMapper()
    mapper.record_dashboard("live-dash")
    mapper.record_widget("live-w1")
    mapper.record_widget("live-w2")
    snapshot = normalize_live_snapshot(
        task=stark_read_task,
        dashboard_info={
            "id": "live-dash",
            "tabs": [
                {
                    "tab_id": "main",
                    "tab_name": "Main",
                    "widgets": [
                        {"widget_uuid": "live-w1", "name": "Alert Trend"},
                        {"widget_uuid": "live-w2", "name": "Data Note"},
                    ],
                    "layout": [
                        {"widget_uuid": "live-w1", "x": 0, "y": 2, "w": 20, "h": 10},
                        {"widget_uuid": "live-w2", "x": 0, "y": 12, "w": 20, "h": 6},
                    ],
                }
            ],
        },
        dashboard_name="Data Review",
        widget_details={
            "live-w1": {
                "origin": "Stark Fund",
                "widget_id": "compliance_surveillance_hub_alerts_alert_trend",
                "name": "Alert Trend",
                "data_args": {"fund": "Flagship Long/Short", "period": "YTD"},
            },
            "live-w2": {
                "origin": "",
                "widget_id": "",
                "name": "Data Note",
                "data": (
                    "Reviewed the data returned by "
                    "compliance_surveillance_hub_alerts_alert_trend."
                ),
            },
        },
        generated_uuids={"live-w2"},
        generated_meta={"live-w2": {"widget_type": "note"}},
        mapper=mapper,
        reverse_origin_map={"Stark Fund": "Bench Stark Enterprise"},
    )
    trace = tuple(
        ToolTraceEvent(
            index=index + 1,
            call=call,
            ok=True,
            result={
                "ok": True,
                "data": [{"alert_count": 15, "fund": "Flagship Long/Short"}],
            },
        )
        for index, call in enumerate(stark_read_task.oracle_tool_calls)
    )
    grade = grade_task(stark_read_task, snapshot, trace)
    assert grade.passed, [f"{i.code}: {i.message}" for i in grade.issues]


def test_grade_agreement_reports_issue_deltas(stark_read_task: Task) -> None:
    from workspace_bench.core.graders import grade_task

    empty_snapshot = {"dashboard_composition": {"name": "", "tabs": [], "widgets": []}}
    failing = grade_task(stark_read_task, empty_snapshot, ())
    agreement = grade_agreement(failing, failing)
    assert agreement["verdict_agree"] is True
    assert agreement["structural_agree"] is True
    assert agreement["live_only_structural"] == []
    assert agreement["live_only_data_content"] == []
    assert agreement["issues_in_both"]
