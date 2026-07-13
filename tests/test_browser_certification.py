from __future__ import annotations

import json
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from urllib.request import Request, urlopen


from workspace_bench.browser.certification import (
    CATEGORY_COUNTS,
    browser_certify,
    dry_run_subset,
    load_certification_subset,
    validate_entry,
)
from workspace_bench.browser.task_backend import TaskBackendServer
from workspace_bench.core.runner import find_task


def test_certification_subset_has_exact_categories_and_dataset_evidence() -> None:
    entries = load_certification_subset()

    assert len(entries) == 30
    assert Counter(entry.category for entry in entries) == Counter(CATEGORY_COUNTS)
    assert len({entry.task_ref for entry in entries}) == 30
    assert sum(entry.self_test for entry in entries) == 3
    for entry in entries:
        result = validate_entry(entry, probe_backend=False)
        assert result["passed"]
        assert entry.rationale
        assert entry.interactions


def test_task_backend_serves_oracle_metadata_datasets_forms_and_cors() -> None:
    task = find_task("build-openbb-apps/forms/access_review_form")
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


def test_full_subset_dry_run_probes_all_backends() -> None:
    result = dry_run_subset(load_certification_subset())

    assert result["passed"] is True
    assert result["task_count"] == 30
    assert result["category_counts"] == CATEGORY_COUNTS
    assert result["http_probes"] >= 120


def test_browser_certification_fails_closed_when_no_tasks_are_selected(
    monkeypatch,
    tmp_path: Path,
) -> None:
    from workspace_bench.browser import certification

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
