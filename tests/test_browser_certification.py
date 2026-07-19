from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from urllib.request import Request, urlopen


from workspace_bench.core.models import Task
from workspace_bench.workspace.browser.certification import (
    browser_certify,
    load_certification_subset,
)
from workspace_bench.workspace.browser.task_backend import TaskBackendServer


def test_certification_manifest_is_empty_pending_reauthoring() -> None:
    # The previous 30-entry subset certified the retired app-building suite.
    # An empty manifest must load cleanly; certification then fails closed.
    assert load_certification_subset() == ()


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


def test_browser_certification_fails_closed_when_no_tasks_are_selected(
    monkeypatch,
    tmp_path: Path,
) -> None:
    from workspace_bench.workspace.browser import certification

    monkeypatch.setattr(certification, "load_certification_subset", lambda: ())

    dry_result = browser_certify(dry_run=True, output_root=tmp_path)

    class FakeBrowser:
        def close(self) -> None:
            return None

    @contextmanager
    def fake_sync_playwright():
        yield SimpleNamespace(
            chromium=SimpleNamespace(launch=lambda **_kwargs: FakeBrowser())
        )

    monkeypatch.setattr(certification, "_sync_playwright", lambda: fake_sync_playwright)
    browser_result = browser_certify(
        all_entries=True,
        auth_state=tmp_path / "unused-auth.json",
        output_root=tmp_path,
    )

    for result in (dry_result, browser_result):
        assert result["passed"] is False
        assert result["task_count"] == 0
        assert result["results"] == []
