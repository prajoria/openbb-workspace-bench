from __future__ import annotations

import json
import os
import socket
import subprocess
import time
from collections import Counter
from pathlib import Path
from urllib.request import Request, urlopen

import pytest

from workspace_bench.browser.certification import (
    CATEGORY_COUNTS,
    browser_certify,
    dry_run_subset,
    load_certification_subset,
    load_code_certification_entry,
    validate_entry,
)
from workspace_bench.browser.task_backend import TaskBackendServer
from workspace_bench.core.runner import find_task
from workspace_bench.code_tasks import instantiate_code_task


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


def test_code_flagship_is_an_optional_browser_entry() -> None:
    entry = load_code_certification_entry()

    assert entry.task_ref == "build-openbb-backends/backend-code/risk_command_center_product"
    assert entry.self_test is True
    assert entry.expected_widgets == ("risk_overview", "factor_exposures")


@pytest.mark.browser
def test_browser_self_test_runs_real_playwright_and_writes_artifacts(tmp_path: Path) -> None:
    pytest.importorskip("playwright.sync_api")
    from playwright.sync_api import Error, sync_playwright

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            browser.close()
    except Error as error:
        pytest.skip(f"Playwright Chromium is unavailable: {error}")

    code_task = find_task("risk_command_center_product", suite="build-openbb-backends")
    code_workdir = instantiate_code_task(code_task, workdir=tmp_path / "code-repo", oracle=True)
    subprocess.run(["uv", "sync", "--quiet"], cwd=code_workdir, check=True)
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = int(sock.getsockname()[1])
    process = subprocess.Popen(
        [
            str(
                code_workdir
                / ".venv"
                / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
            ),
            "-m",
            "uvicorn",
            "app:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=code_workdir,
    )
    try:
        time.sleep(0.4)
        result = browser_certify(
            task_ref="build-openbb-apps/types/chains_heatmap_html",
            self_test=True,
            output_root=tmp_path,
            code_task_backend=f"http://127.0.0.1:{port}",
        )
    finally:
        process.terminate()
        process.wait(timeout=5)

    assert result["passed"] is True
    assert result["task_count"] == 2
    for verdict in result["results"]:
        assert Path(verdict["artifacts"]["screenshot"]).stat().st_size > 0
        assert Path(verdict["artifacts"]["trace"]).stat().st_size > 0
        assert json.loads(Path(verdict["verdict"]).read_text())["passed"] is True
