from __future__ import annotations

import json
from urllib.request import Request, urlopen


from workspace_bench.core.models import Task
from workspace_bench.workspace.task_backend import TaskBackendServer


def _form_backend_task() -> Task:
    widget = {
        "name": "Access Review Form",
        "description": "Capture an access review decision.",
        "endpoint": "/access-review",
        "type": "markdown",
        "gridData": {"w": 12, "h": 8},
        "params": [
            {
                "paramName": "review",
                "type": "form",
                "label": "Access Review",
                "endpoint": "/access-review-submit",
                "method": "POST",
                "inputParams": [
                    {
                        "paramName": "user_name",
                        "type": "text",
                        "label": "User",
                        "value": "analyst1",
                    },
                    {
                        "paramName": "approved",
                        "type": "boolean",
                        "label": "Approved",
                        "value": False,
                    },
                ],
            }
        ],
    }
    return Task.from_dict(
        {
            "id": "task_backend_form_probe",
            "category": "platform",
            "family": "runtime",
            "difficulty": "easy",
            "prompt": "Serve the oracle backend for the access review form.",
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": ["manage_backends"],
            "success": {
                "runtime_checks": {
                    "datasets": [
                        {
                            "name": "surveillance-data__access_review_form",
                            "widget_id": "access_review_form",
                            "fields": [],
                            "path": "/access-review",
                            "payload": (
                                "Access Review Form fixture-backed runtime summary."
                            ),
                            "form_endpoint": "/access-review-submit",
                        }
                    ],
                    "pinned_paths": False,
                }
            },
            "oracle_tool_calls": [
                {
                    "tool": "manage_backends",
                    "args": {
                        "operation": "add",
                        "name": "Surveillance Data",
                        "url": "http://localhost:7807",
                        "widgets_json": {"access_review_form": widget},
                    },
                }
            ],
            "limits": {},
        }
    )


def test_task_backend_serves_oracle_metadata_datasets_forms_and_cors() -> None:
    task = _form_backend_task()
    with TaskBackendServer(task, backend_name="Surveillance Data") as server:
        with urlopen(server.base_url + "/widgets.json", timeout=2) as response:
            widgets = json.load(response)
            assert response.headers["Access-Control-Allow-Origin"] == "*"
        assert set(widgets) == {"access_review_form"}

        with urlopen(server.base_url + "/access-review", timeout=2) as response:
            assert json.load(response) == "Access Review Form fixture-backed runtime summary."

        request = Request(
            server.base_url + "/access-review-submit",
            data=b'{"user_name":"analyst1","approved":true}',
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=2) as response:
            submitted = json.load(response)
        assert submitted["ok"] is True
        assert {item["path"] for item in server.request_log} >= {
            "/widgets.json",
            "/access-review",
            "/access-review-submit",
        }
