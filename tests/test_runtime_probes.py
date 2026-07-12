from __future__ import annotations

import socket

import pytest

from workspace_bench.core.models import RuntimeDataset, Task
from workspace_bench.core.graders import grade_task
from workspace_bench.workspace.runtime import (
    bind_dataset,
    get_runtime_server,
    grade_runtime,
    synthesize_params,
)


def _task(dataset: dict, *, pinned_paths: bool = False) -> Task:
    return Task.from_dict(
        {
            "id": "runtime_probe_test",
            "category": "platform",
            "family": "runtime",
            "difficulty": "easy",
            "prompt": "Verify the runtime fixture.",
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": ["manage_backends"],
            "success": {
                "runtime_checks": {
                    "datasets": [dataset],
                    "pinned_paths": pinned_paths,
                }
            },
            "oracle_tool_calls": [
                {"tool": "manage_backends", "args": {"operation": "list"}}
            ],
            "limits": {},
        }
    )


def _dataset(**updates: object) -> dict:
    dataset = {
        "name": "prices",
        "widget_id": "prices",
        "fields": ["symbol", "close"],
        "path": "/prices",
        "payload": [{"symbol": "AAPL", "close": 196.1}],
    }
    dataset.update(updates)
    return dataset


def _snapshot(definition_updates: dict | None = None) -> dict:
    definition = {
        "name": "Prices",
        "description": "Closing prices.",
        "type": "table",
        "endpoint": "/prices",
        "data": {
            "table": {
                "columnsDefs": [
                    {"field": "symbol"},
                    {"field": "close"},
                ]
            }
        },
    }
    definition.update(definition_updates or {})
    return {
        "custom_backends": {
            "backend_001": {
                "name": "Price Data",
                "url": "http://agent-backend.invalid:7777",
                "widgets_json": {"prices": definition},
                "apps_json": [],
                "warnings": [],
            }
        }
    }


def _codes(task: Task, snapshot: dict) -> set[str]:
    return {issue.code for issue in grade_runtime(task, snapshot).issues}


def test_runtime_probe_uses_a_bound_socket_and_reuses_server() -> None:
    server = get_runtime_server()
    with socket.create_connection(server.server_address, timeout=2):
        pass
    before = server.request_count

    first = grade_runtime(_task(_dataset()), _snapshot())
    same_server = get_runtime_server()
    second = grade_runtime(_task(_dataset()), _snapshot())

    assert first.passed and second.passed
    assert same_server is server
    assert server.request_count == before + 2


def test_seeded_rows_ssrm_is_paged_sorted_filtered_and_counted() -> None:
    dataset = _dataset(
        payload=None,
        fields=["symbol", "close"],
        payload_spec={
            "generator": "seeded_rows",
            "seed": 17,
            "n_rows": 10_000,
            "schema": {"symbol": "string", "close": "number"},
            "data_key": "rows",
        },
    )
    task = _task(dataset)
    snapshot = _snapshot(
        {
            "type": "table_ssrm",
            "data": {
                "dataKey": "rows",
                "table": {"columnsDefs": [{"field": "symbol"}, {"field": "close"}]},
            },
        }
    )
    before = get_runtime_server().request_count

    grade = grade_runtime(task, snapshot)

    assert grade.passed
    assert get_runtime_server().request_count == before + 3


def test_dataset_binding_is_field_driven_with_identity_as_tiebreak() -> None:
    definition = _snapshot()["custom_backends"]["backend_001"]["widgets_json"]["prices"]
    datasets = (
        RuntimeDataset("other", "other", ("symbol", "close", "volume"), []),
        RuntimeDataset("exact", "prices", ("symbol", "close"), []),
    )

    assert bind_dataset(definition, "prices", datasets) == datasets[1]
    definition["data"]["table"]["columnsDefs"].append({"field": "bogus"})
    assert bind_dataset(definition, "prices", datasets) is None


def test_param_synthesis_prefers_defaults_options_dates_and_multiselect() -> None:
    params = synthesize_params(
        {
            "params": [
                {"paramName": "symbol", "type": "ticker", "value": "MSFT"},
                {
                    "paramName": "desk",
                    "type": "text",
                    "options": [{"value": "rates"}, {"value": "credit"}],
                },
                {"paramName": "as_of_date", "type": "date"},
                {
                    "paramName": "regions",
                    "type": "endpoint",
                    "multiSelect": True,
                    "options": ["US", "EU", "APAC"],
                },
            ]
        }
    )

    assert params == {
        "symbol": "MSFT",
        "desk": "rates",
        "as_of_date": "2026-01-15",
        "regions": ["US", "EU"],
    }


@pytest.mark.parametrize(
    ("task", "snapshot", "code"),
    [
        (
            _task(_dataset()),
            _snapshot({"endpoint": ""}),
            "endpoint_unreachable",
        ),
        (
            _task(_dataset(status=503)),
            _snapshot(),
            "endpoint_bad_status",
        ),
        (
            _task(_dataset(raw_body="{")),
            _snapshot(),
            "endpoint_response_malformed",
        ),
        (
            _task(_dataset()),
            _snapshot(
                {
                    "data": {
                        "table": {
                            "columnsDefs": [
                                {"field": "symbol"},
                                {"field": "field_no_dataset_serves"},
                            ]
                        }
                    }
                }
            ),
            "endpoint_response_incompatible",
        ),
        (
            _task(_dataset(payload=[{"symbol": "AAPL", "close": "placeholder"}])),
            _snapshot(),
            "endpoint_response_placeholder",
        ),
        (
            _task(_dataset()),
            _snapshot(
                {
                    "params": [
                        {"paramName": "window", "type": "unsupported-runtime-param"}
                    ]
                }
            ),
            "endpoint_params_invalid",
        ),
    ],
)
def test_runtime_failure_codes(task: Task, snapshot: dict, code: str) -> None:
    assert code in _codes(task, snapshot)


def test_pinned_endpoint_path_must_match_task_dataset() -> None:
    task = _task(_dataset(), pinned_paths=True)

    assert "endpoint_unreachable" in _codes(task, _snapshot({"endpoint": "/missing"}))


def test_chart_declared_series_cannot_be_all_null() -> None:
    task = _task(
        _dataset(
            fields=["symbol", "close"],
            payload=[{"symbol": "AAPL", "close": None}],
        )
    )
    snapshot = _snapshot(
        {
            "type": "chart",
            "data": {"categoryField": "symbol", "series": [{"field": "close"}]},
        }
    )

    assert "endpoint_response_incompatible" in _codes(task, snapshot)


def test_form_submission_contract_has_a_dedicated_issue_code() -> None:
    task = _task(_dataset(form_endpoint="/submit"))
    snapshot = _snapshot(
        {
            "params": [
                {
                    "paramName": "review",
                    "type": "form",
                    "method": "POST",
                    "endpoint": "/wrong-submit",
                    "inputParams": [
                        {"paramName": "comment", "type": "text"},
                    ],
                }
            ]
        }
    )

    assert "form_submission_incompatible" in _codes(task, snapshot)


def test_runtime_is_a_first_class_strict_grade_dimension() -> None:
    task = _task(_dataset(status=503))

    grade = grade_task(task, _snapshot(), ())

    assert grade.state_passed
    assert grade.trace_passed
    assert not grade.runtime_passed
    assert not grade.passed
    assert grade.score == 0.5


def test_runtime_grade_emits_machine_generated_deployment_receipt() -> None:
    snapshot = _snapshot()
    snapshot["custom_backends"]["backend_001"]["apps_json"] = [
        {"template_id": "price-app", "name": "Price App"}
    ]
    snapshot["dashboard_compositions"] = {
        "dash_001": {"dashboard_id": "dash_001", "widgets": []},
        "dash_002": {
            "dashboard_id": "dash_002",
            "widgets": [{"origin": "Price Data", "widget_id": "prices"}],
        },
    }

    grade = grade_runtime(_task(_dataset()), snapshot)

    assert grade.deployment_receipt is not None
    receipt = grade.deployment_receipt
    assert receipt.backend_names == ("Price Data",)
    assert receipt.app_ids == ("price-app",)
    assert receipt.instantiated_dashboard_ids == ("dash_002",)
    assert receipt.counts.widget_probes == 1
    assert receipt.counts.widget_probes_passed == 1
    assert receipt.widget_probes[0].dataset_name == "prices"
    assert receipt.widget_probes[0].outcome == "passed"
