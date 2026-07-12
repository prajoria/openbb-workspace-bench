"""Manifest validation and optional Playwright browser certification."""

from __future__ import annotations

import json
import re
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from importlib import resources
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from workspace_bench.browser.mock_server import MockWorkspaceServer
from workspace_bench.browser.task_backend import TaskBackendModel, TaskBackendServer
from workspace_bench.core.models import JsonDict, RuntimeDataset, Task
from workspace_bench.core.runner import find_task
from workspace_bench.workspace.runtime import bind_dataset


MANIFEST_SCHEMA_VERSION = "workspace-bench-browser-subset/v1"
VERDICT_SCHEMA_VERSION = "workspace-bench-browser-verdict/v1"
CATEGORY_COUNTS = {
    "native_content": 4,
    "tables_grids": 4,
    "charts": 4,
    "forms_buttons": 4,
    "parameterized_widgets": 4,
    "multi_widget_apps": 4,
    "shared_interaction_apps": 3,
    "repair_live_update": 3,
}
INTERACTION_OPS = {
    "set_param",
    "submit_form",
    "sort_column",
    "switch_tab",
    "refresh_widget",
}
SELECTOR_KEYS = {
    "add_backend_button",
    "backend_url_input",
    "backend_submit_button",
    "backend_ready",
    "app_add_button",
    "widget_add_button",
    "rendered_widget",
    "tab_button",
    "param_input",
    "form_submit",
    "column_header",
    "refresh_widget",
}


@dataclass(frozen=True)
class EvidenceExpectation:
    widget_id: str
    fragments: tuple[str, ...]


@dataclass(frozen=True)
class Interaction:
    op: Literal[
        "set_param",
        "submit_form",
        "sort_column",
        "switch_tab",
        "refresh_widget",
    ]
    widget_id: str | None = None
    param: str | None = None
    value: Any = None
    column: str | None = None
    tab: str | None = None


@dataclass(frozen=True)
class CertificationEntry:
    task_ref: str
    category: str
    rationale: str
    oracle_backend: str
    expected_widgets: tuple[str, ...]
    interactions: tuple[Interaction, ...]
    expected_evidence: tuple[EvidenceExpectation, ...]
    self_test: bool = False


@dataclass(frozen=True)
class _ExternalBackend:
    """Already-running agent backend adapted to the browser harness interface."""

    base_url: str
    model: TaskBackendModel

    def __enter__(self) -> "_ExternalBackend":
        return self

    def __exit__(self, *_args: Any) -> None:
        return None


def load_certification_subset(path: Path | None = None) -> tuple[CertificationEntry, ...]:
    """Load and structurally validate the committed certification manifest."""

    if path is None:
        raw = (
            resources.files("workspace_bench.browser")
            .joinpath("cert_subset.json")
            .read_text(encoding="utf-8")
        )
    else:
        raw = path.read_text(encoding="utf-8")
    payload = json.loads(raw)
    if not isinstance(payload, dict) or payload.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        raise ValueError(f"browser subset must use {MANIFEST_SCHEMA_VERSION}")
    raw_entries = payload.get("entries")
    if not isinstance(raw_entries, list):
        raise ValueError("browser subset entries must be a list")
    entries = tuple(_parse_entry(item) for item in raw_entries)
    task_refs = [entry.task_ref for entry in entries]
    if len(task_refs) != len(set(task_refs)):
        raise ValueError("browser subset task_ref values must be unique")
    observed = {category: 0 for category in CATEGORY_COUNTS}
    for entry in entries:
        if entry.category not in observed:
            raise ValueError(f"unknown browser subset category {entry.category!r}")
        observed[entry.category] += 1
    if observed != CATEGORY_COUNTS:
        raise ValueError(f"browser subset category counts are {observed}, expected {CATEGORY_COUNTS}")
    if sum(entry.self_test for entry in entries) < 3:
        raise ValueError("browser subset must mark at least three self-test entries")
    return entries


def load_code_certification_entry(path: Path | None = None) -> CertificationEntry:
    """Load the single optional code-track flagship browser entry."""

    raw = (
        resources.files("workspace_bench.browser")
        .joinpath("code_cert_subset.json")
        .read_text(encoding="utf-8")
        if path is None
        else path.read_text(encoding="utf-8")
    )
    payload = json.loads(raw)
    if (
        not isinstance(payload, dict)
        or payload.get("schema_version") != "workspace-bench-browser-code-subset/v0"
        or payload.get("optional") is not True
    ):
        raise ValueError("code browser subset must be an optional v0 manifest")
    return _parse_entry(payload.get("entry"))


def _parse_entry(payload: Any) -> CertificationEntry:
    if not isinstance(payload, dict):
        raise ValueError("browser subset entry must be an object")
    required_strings = ("task_ref", "category", "rationale", "oracle_backend")
    for field in required_strings:
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            raise ValueError(f"browser subset entry needs non-empty {field}")
    widgets = payload.get("expected_widgets")
    if not isinstance(widgets, list) or not widgets or not all(
        isinstance(item, str) and item for item in widgets
    ):
        raise ValueError(f"{payload['task_ref']} expected_widgets must be non-empty strings")
    raw_interactions = payload.get("interactions")
    if not isinstance(raw_interactions, list) or not raw_interactions:
        raise ValueError(f"{payload['task_ref']} needs a declarative interaction script")
    interactions: list[Interaction] = []
    for item in raw_interactions:
        if not isinstance(item, dict) or item.get("op") not in INTERACTION_OPS:
            raise ValueError(f"{payload['task_ref']} contains an invalid interaction")
        interactions.append(
            Interaction(
                op=item["op"],
                widget_id=item.get("widget_id"),
                param=item.get("param"),
                value=item.get("value"),
                column=item.get("column"),
                tab=item.get("tab"),
            )
        )
    raw_evidence = payload.get("expected_evidence")
    if not isinstance(raw_evidence, list) or not raw_evidence:
        raise ValueError(f"{payload['task_ref']} needs expected_evidence")
    evidence: list[EvidenceExpectation] = []
    for item in raw_evidence:
        if not isinstance(item, dict):
            raise ValueError(f"{payload['task_ref']} evidence must be objects")
        fragments = item.get("fragments")
        widget_id = item.get("widget_id")
        if (
            not isinstance(widget_id, str)
            or not isinstance(fragments, list)
            or not fragments
            or not all(isinstance(fragment, str) and fragment for fragment in fragments)
        ):
            raise ValueError(f"{payload['task_ref']} contains malformed evidence")
        evidence.append(EvidenceExpectation(widget_id, tuple(fragments)))
    return CertificationEntry(
        task_ref=payload["task_ref"],
        category=payload["category"],
        rationale=payload["rationale"],
        oracle_backend=payload["oracle_backend"],
        expected_widgets=tuple(widgets),
        interactions=tuple(interactions),
        expected_evidence=tuple(evidence),
        self_test=bool(payload.get("self_test", False)),
    )


def validate_entry(entry: CertificationEntry, *, probe_backend: bool = True) -> JsonDict:
    """Validate task, oracle contract, evidence provenance, and interactions."""

    task = find_task(entry.task_ref)
    server = TaskBackendServer(task, backend_name=entry.oracle_backend)
    model = server.model
    widget_ids = set(model.widgets)
    missing = set(entry.expected_widgets) - widget_ids
    if missing:
        raise ValueError(f"{entry.task_ref} expected widgets are absent: {sorted(missing)}")
    evidence_widgets = {item.widget_id for item in entry.expected_evidence}
    if evidence_widgets != set(entry.expected_widgets):
        raise ValueError(
            f"{entry.task_ref} evidence widgets {sorted(evidence_widgets)} do not match expected widgets"
        )
    runtime = task.success.runtime
    if runtime is None:
        raise ValueError(f"{entry.task_ref} has no runtime datasets")
    for expectation in entry.expected_evidence:
        definition = model.widgets[expectation.widget_id]
        dataset = bind_dataset(
            definition,
            expectation.widget_id,
            runtime.datasets,
            pinned_paths=runtime.pinned_paths,
        )
        if dataset is None:
            raise ValueError(f"{entry.task_ref}/{expectation.widget_id} has no bound dataset")
        serialized = _dataset_text(dataset)
        absent = [fragment for fragment in expectation.fragments if fragment.casefold() not in serialized]
        if absent:
            raise ValueError(
                f"{entry.task_ref}/{expectation.widget_id} evidence is not dataset-derived: {absent}"
            )
    for interaction in entry.interactions:
        _validate_interaction(entry, task, model, interaction)

    probe_count = 0
    if probe_backend:
        server.start()
        try:
            probe_count = _probe_task_backend(server)
        finally:
            server.close()
    else:
        server.close()
    return {
        "task_ref": entry.task_ref,
        "category": entry.category,
        "backend": entry.oracle_backend,
        "widgets": len(entry.expected_widgets),
        "interactions": len(entry.interactions),
        "evidence_fragments": sum(len(item.fragments) for item in entry.expected_evidence),
        "http_probes": probe_count,
        "passed": True,
    }


def _dataset_text(dataset: RuntimeDataset) -> str:
    value = dataset.raw_body if dataset.raw_body is not None else dataset.payload
    return json.dumps(value, sort_keys=True).casefold()


def _validate_interaction(
    entry: CertificationEntry,
    task: Task,
    model: TaskBackendModel,
    interaction: Interaction,
) -> None:
    if interaction.op == "switch_tab":
        tabs = {
            str(tab.get("name"))
            for app in model.apps
            for tab in _app_tabs(app)
        } | {
            str(tab.get("id"))
            for app in model.apps
            for tab in _app_tabs(app)
        }
        if not interaction.tab or interaction.tab not in tabs:
            raise ValueError(f"{entry.task_ref} interaction references unknown tab {interaction.tab!r}")
        return
    if not interaction.widget_id or interaction.widget_id not in model.widgets:
        raise ValueError(
            f"{entry.task_ref} interaction references unknown widget {interaction.widget_id!r}"
        )
    definition = model.widgets[interaction.widget_id]
    if interaction.op == "refresh_widget":
        return
    params = _flatten_params(definition)
    if interaction.op == "set_param":
        if interaction.param not in {param.get("paramName") for param in params}:
            raise ValueError(
                f"{entry.task_ref}/{interaction.widget_id} has no param {interaction.param!r}"
            )
        return
    if interaction.op == "submit_form":
        forms = {
            param.get("paramName")
            for param in definition.get("params", [])
            if isinstance(param, dict) and param.get("type") == "form"
        }
        if interaction.param not in forms:
            raise ValueError(
                f"{entry.task_ref}/{interaction.widget_id} has no form {interaction.param!r}"
            )
        return
    if interaction.op == "sort_column":
        runtime = task.success.runtime
        assert runtime is not None
        dataset = bind_dataset(definition, interaction.widget_id, runtime.datasets)
        fields = set(dataset.fields) if dataset is not None else set()
        for column in definition.get("data", {}).get("table", {}).get("columnsDefs", []):
            field = column.get("field") if isinstance(column, dict) else None
            if isinstance(field, str):
                fields.add(field)
        if interaction.column not in fields:
            raise ValueError(
                f"{entry.task_ref}/{interaction.widget_id} has no column {interaction.column!r}"
            )


def _flatten_params(definition: JsonDict) -> list[JsonDict]:
    flattened: list[JsonDict] = []
    for param in definition.get("params", []):
        if not isinstance(param, dict):
            continue
        flattened.append(param)
        children = param.get("inputParams")
        if isinstance(children, list):
            flattened.extend(child for child in children if isinstance(child, dict))
    return flattened


def _app_tabs(app: JsonDict) -> list[JsonDict]:
    tabs = app.get("tabs", {})
    return [tab for tab in tabs.values() if isinstance(tab, dict)] if isinstance(tabs, dict) else []


def _probe_task_backend(server: TaskBackendServer) -> int:
    count = 0
    for path in ("/health", "/widgets.json", "/apps.json"):
        with urlopen(server.base_url + path, timeout=2) as response:
            if response.status != 200 or response.headers.get("Access-Control-Allow-Origin") is None:
                raise ValueError(f"task backend probe failed for {path}")
            json.load(response)
            count += 1
    for widget_id, definition in server.model.widgets.items():
        endpoint = definition.get("endpoint")
        if not isinstance(endpoint, str):
            raise ValueError(f"{server.model.task_ref}/{widget_id} has no endpoint")
        method = "POST" if definition.get("type") == "ssrm_table" else "GET"
        data = b'{"startRow":0,"endRow":100}' if method == "POST" else None
        request = Request(urljoin(server.base_url + "/", endpoint.lstrip("/")), data=data, method=method)
        request.add_header("Content-Type", "application/json")
        with urlopen(request, timeout=2) as response:
            if response.status != 200:
                raise ValueError(f"task backend endpoint failed for {widget_id}")
            json.load(response)
            count += 1
    return count


def dry_run_subset(entries: tuple[CertificationEntry, ...]) -> JsonDict:
    """Validate all selected entries without importing or launching Playwright."""

    started = time.monotonic()
    results = [validate_entry(entry) for entry in entries]
    return {
        "mode": "dry-run",
        "passed": True,
        "task_count": len(results),
        "category_counts": {
            category: sum(result["category"] == category for result in results)
            for category in CATEGORY_COUNTS
        },
        "http_probes": sum(int(result["http_probes"]) for result in results),
        "duration_ms": round((time.monotonic() - started) * 1000),
        "results": results,
    }


def load_selectors(path: Path | None = None) -> dict[str, str]:
    """Load default selectors, optionally replacing values from a local override."""

    default_payload = json.loads(
        resources.files("workspace_bench.browser")
        .joinpath("selectors.json")
        .read_text(encoding="utf-8")
    )
    if not isinstance(default_payload, dict):
        raise ValueError("bundled browser selectors must be an object")
    selectors = {str(key): str(value) for key, value in default_payload.items()}
    if path is not None:
        override = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(override, dict) or not all(
            isinstance(key, str) and isinstance(value, str) for key, value in override.items()
        ):
            raise ValueError("selector override must be a string-to-string JSON object")
        selectors.update(override)
    missing = SELECTOR_KEYS - set(selectors)
    if missing:
        raise ValueError(f"browser selectors are missing keys: {sorted(missing)}")
    return selectors


def select_entries(
    *,
    task_ref: str | None,
    all_entries: bool,
    self_test: bool,
    dry_run: bool,
) -> tuple[CertificationEntry, ...]:
    entries = load_certification_subset()
    if task_ref:
        selected = tuple(entry for entry in entries if entry.task_ref == task_ref)
        if not selected:
            raise KeyError(f"{task_ref!r} is not in the browser certification subset")
        return selected
    if all_entries or dry_run:
        return entries
    if self_test:
        return tuple(entry for entry in entries if entry.self_test)
    raise ValueError("browser certification requires --task or --all")


def browser_certify(
    *,
    task_ref: str | None = None,
    all_entries: bool = False,
    headed: bool = False,
    workspace_url: str = "https://pro.openbb.co",
    auth_state: Path | None = None,
    self_test: bool = False,
    dry_run: bool = False,
    selectors_path: Path | None = None,
    output_root: Path = Path("runs/browser-cert"),
    code_task_backend: str | None = None,
) -> JsonDict:
    """Run dry validation or real Playwright certification for selected tasks."""

    entries = select_entries(
        task_ref=task_ref,
        all_entries=all_entries,
        self_test=self_test,
        dry_run=dry_run,
    )
    if dry_run:
        if code_task_backend is not None:
            raise ValueError("the code-task browser entry is a Chromium self-test, not a dry-run")
        return dry_run_subset(entries)
    if code_task_backend is not None and not self_test:
        raise ValueError("--code-task-backend requires --self-test")
    selectors = load_selectors(selectors_path)
    sync_playwright = _sync_playwright()
    output_root.mkdir(parents=True, exist_ok=True)
    results: list[JsonDict] = []
    mock_server = MockWorkspaceServer().start() if self_test else None
    target_url = mock_server.base_url if mock_server is not None else workspace_url
    if not self_test and auth_state is None:
        raise ValueError("real Workspace certification requires --auth-state from --setup-auth")
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=not headed)
            try:
                for entry in entries:
                    result = _run_browser_entry(
                        browser,
                        entry,
                        selectors,
                        workspace_url=target_url,
                        auth_state=auth_state,
                        self_test=self_test,
                        output_root=output_root,
                    )
                    results.append(result)
                if code_task_backend is not None:
                    code_entry = load_code_certification_entry()
                    code_model = _external_backend_model(code_entry, code_task_backend)
                    results.append(
                        _run_browser_entry(
                            browser,
                            code_entry,
                            selectors,
                            workspace_url=target_url,
                            auth_state=None,
                            self_test=True,
                            output_root=output_root,
                            external_backend=_ExternalBackend(code_task_backend, code_model),
                        )
                    )
            finally:
                browser.close()
    finally:
        if mock_server is not None:
            mock_server.close()
    return {
        "mode": "self-test" if self_test else "workspace",
        "passed": all(bool(result["passed"]) for result in results),
        "task_count": len(results),
        "passed_count": sum(bool(result["passed"]) for result in results),
        "results": results,
    }


def _run_browser_entry(
    browser: Any,
    entry: CertificationEntry,
    selectors: dict[str, str],
    *,
    workspace_url: str,
    auth_state: Path | None,
    self_test: bool,
    output_root: Path,
    external_backend: _ExternalBackend | None = None,
) -> JsonDict:
    started_at = datetime.now(UTC)
    started = time.monotonic()
    directory_name = (
        f"selftest-{entry.task_ref.rsplit('/', 1)[-1]}"
        if self_test
        else entry.task_ref.replace("/", "__")
    )
    output_dir = output_root / directory_name
    output_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = output_dir / "screenshot.png"
    trace_path = output_dir / "trace.zip"
    verdict_path = output_dir / "verdict.json"
    failed_requests: list[JsonDict] = []
    failed_responses: list[JsonDict] = []
    interaction_results: list[JsonDict] = []
    evidence_results: list[JsonDict] = []
    rendered_widgets: list[str] = []
    error: str | None = None
    context: Any = None
    page: Any = None
    trace_started = False

    backend_manager: TaskBackendServer | _ExternalBackend
    if external_backend is None:
        task = find_task(entry.task_ref)
        backend_manager = TaskBackendServer(task, backend_name=entry.oracle_backend)
    else:
        backend_manager = external_backend
    with backend_manager as backend:
        try:
            context_args: JsonDict = {"viewport": {"width": 1440, "height": 1000}}
            if auth_state is not None:
                context_args["storage_state"] = str(auth_state)
            context = browser.new_context(**context_args)
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
            trace_started = True
            page = context.new_page()

            def request_failed(request: Any) -> None:
                if request.url.startswith(backend.base_url):
                    failed_requests.append(
                        {"url": request.url, "method": request.method, "failure": request.failure}
                    )

            def response_seen(response: Any) -> None:
                if response.url.startswith(backend.base_url) and response.status >= 400:
                    failed_responses.append(
                        {"url": response.url, "status": response.status}
                    )

            page.on("requestfailed", request_failed)
            page.on("response", response_seen)
            page.goto(workspace_url, wait_until="domcontentloaded", timeout=30_000)
            page.locator(selectors["add_backend_button"]).click()
            page.locator(selectors["backend_url_input"]).fill(backend.base_url)
            page.locator(selectors["backend_submit_button"]).click()
            page.locator(selectors["backend_ready"]).wait_for(state="visible", timeout=15_000)

            if backend.model.apps:
                app_id = str(backend.model.apps[0].get("template_id"))
                page.locator(_format_selector(selectors["app_add_button"], app_id=app_id)).click()
            else:
                for widget_id in entry.expected_widgets:
                    page.locator(
                        _format_selector(selectors["widget_add_button"], widget_id=widget_id)
                    ).click()

            for widget_id in entry.expected_widgets:
                locator = page.locator(
                    _format_selector(selectors["rendered_widget"], widget_id=widget_id)
                )
                locator.wait_for(state="attached", timeout=15_000)
                rendered_widgets.append(widget_id)

            for interaction in entry.interactions:
                _perform_interaction(page, interaction, backend.model, selectors)
                interaction_results.append({**asdict(interaction), "passed": True})

            for expectation in entry.expected_evidence:
                _activate_widget_tab(page, expectation.widget_id, backend.model, selectors)
                locator = page.locator(
                    _format_selector(
                        selectors["rendered_widget"],
                        widget_id=expectation.widget_id,
                    )
                )
                locator.wait_for(state="visible", timeout=10_000)
                text = locator.inner_text(timeout=10_000)
                for fragment in expectation.fragments:
                    observed = fragment.casefold() in text.casefold()
                    evidence_results.append(
                        {
                            "widget_id": expectation.widget_id,
                            "fragment": fragment,
                            "observed": observed,
                        }
                    )
                    if not observed:
                        raise AssertionError(
                            f"{expectation.widget_id} did not render dataset fragment {fragment!r}"
                        )
            if failed_requests or failed_responses:
                raise AssertionError("one or more task-backend network requests failed")
        except Exception as exc:  # Browser failures must be captured in the verdict.
            error = f"{type(exc).__name__}: {exc}"
        finally:
            if page is not None:
                try:
                    page.screenshot(path=str(screenshot_path), full_page=True)
                except Exception as exc:
                    error = error or f"screenshot failed: {exc}"
            if context is not None and trace_started:
                try:
                    context.tracing.stop(path=str(trace_path))
                except Exception as exc:
                    error = error or f"trace failed: {exc}"
            if context is not None:
                context.close()

    passed = (
        error is None
        and not failed_requests
        and not failed_responses
        and len(rendered_widgets) == len(entry.expected_widgets)
        and all(bool(item["observed"]) for item in evidence_results)
    )
    verdict: JsonDict = {
        "schema_version": VERDICT_SCHEMA_VERSION,
        "task_ref": entry.task_ref,
        "category": entry.category,
        "mode": "self-test" if self_test else "workspace",
        "passed": passed,
        "started_at": started_at.isoformat(),
        "duration_ms": round((time.monotonic() - started) * 1000),
        "workspace_url": workspace_url,
        "backend_name": entry.oracle_backend,
        "expected_widgets": list(entry.expected_widgets),
        "rendered_widgets": rendered_widgets,
        "interactions": interaction_results,
        "evidence": evidence_results,
        "network": {
            "failed_requests": failed_requests,
            "failed_responses": failed_responses,
        },
        "artifacts": {
            "screenshot": str(screenshot_path),
            "trace": str(trace_path),
        },
        "error": error,
    }
    verdict_path.write_text(json.dumps(verdict, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {**verdict, "verdict": str(verdict_path)}


def _external_backend_model(entry: CertificationEntry, base_url: str) -> TaskBackendModel:
    """Read widgets/apps metadata from an already-running agent backend."""

    with urlopen(base_url.rstrip("/") + "/widgets.json", timeout=3) as response:
        widgets = json.load(response)
    with urlopen(base_url.rstrip("/") + "/apps.json", timeout=3) as response:
        apps = json.load(response)
    if not isinstance(widgets, dict) or not isinstance(apps, list):
        raise ValueError("code-task browser backend returned malformed manifests")
    missing = set(entry.expected_widgets) - set(widgets)
    if missing:
        raise ValueError(f"code-task browser backend is missing widgets: {sorted(missing)}")
    return TaskBackendModel(
        task_ref=entry.task_ref,
        backend_name=entry.oracle_backend,
        widgets=widgets,
        apps=[app for app in apps if isinstance(app, dict)],
        datasets_by_path={},
        auxiliary_payloads={},
    )


def _perform_interaction(
    page: Any,
    interaction: Interaction,
    model: TaskBackendModel,
    selectors: dict[str, str],
) -> None:
    if interaction.widget_id:
        _activate_widget_tab(page, interaction.widget_id, model, selectors)
    if interaction.op == "switch_tab":
        assert interaction.tab is not None
        page.locator(
            _format_selector(
                selectors["tab_button"],
                tab_id=_slug(interaction.tab),
                tab_name=interaction.tab,
            )
        ).click()
    elif interaction.op == "set_param":
        assert interaction.widget_id is not None and interaction.param is not None
        locator = page.locator(
            _format_selector(
                selectors["param_input"],
                widget_id=interaction.widget_id,
                param=interaction.param,
            )
        )
        locator.fill(str(interaction.value))
        locator.press("Tab")
    elif interaction.op == "submit_form":
        assert interaction.widget_id is not None and interaction.param is not None
        page.locator(
            _format_selector(
                selectors["form_submit"],
                widget_id=interaction.widget_id,
                param=interaction.param,
            )
        ).click()
    elif interaction.op == "sort_column":
        assert interaction.widget_id is not None and interaction.column is not None
        page.locator(
            _format_selector(
                selectors["column_header"],
                widget_id=interaction.widget_id,
                column=interaction.column,
            )
        ).click()
    elif interaction.op == "refresh_widget":
        assert interaction.widget_id is not None
        page.locator(
            _format_selector(
                selectors["refresh_widget"],
                widget_id=interaction.widget_id,
            )
        ).click()
    page.wait_for_timeout(150)


def _activate_widget_tab(
    page: Any,
    widget_id: str,
    model: TaskBackendModel,
    selectors: dict[str, str],
) -> None:
    for app in model.apps:
        for tab in _app_tabs(app):
            layout = tab.get("layout", [])
            if not isinstance(layout, list) or not any(
                isinstance(item, dict) and item.get("i") == widget_id for item in layout
            ):
                continue
            tab_id = str(tab.get("id", ""))
            tab_name = str(tab.get("name", ""))
            page.locator(
                _format_selector(
                    selectors["tab_button"],
                    tab_id=tab_id,
                    tab_name=tab_name,
                )
            ).click()
            page.wait_for_timeout(75)
            return


def _format_selector(template: str, **values: str) -> str:
    return template.format(**values)


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def _sync_playwright() -> Any:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        raise RuntimeError(
            "browser certification requires the optional browser extra: "
            "uv sync --extra browser && uv run playwright install chromium"
        ) from error
    return sync_playwright


def setup_browser_auth(
    *,
    workspace_url: str,
    auth_state: Path,
) -> None:
    """Open a headed browser and save storage state after a human login."""

    sync_playwright = _sync_playwright()
    auth_state.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(workspace_url, wait_until="domcontentloaded")
        input("Complete the Workspace login in the browser, then press Enter here to save state: ")
        context.storage_state(path=str(auth_state))
        browser.close()
