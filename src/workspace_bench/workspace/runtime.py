"""Real-HTTP runtime verification for task-owned deterministic datasets."""

from __future__ import annotations

import atexit
import copy
import hashlib
import json
import threading
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

from workspace_bench.core.models import (
    DeploymentProbeOutcome,
    DeploymentReceipt,
    DeploymentReceiptCounts,
    GradeIssue,
    JsonDict,
    RuntimeChecks,
    RuntimeDataset,
    Task,
)
from workspace_bench.workspace.widget_params import flatten_params


SSRM_TABLE_TYPES = {"table_ssrm", "ssrm_table"}
TABLE_TYPES = {"table", "live_grid"} | SSRM_TABLE_TYPES
CHART_TYPES = {"chart", "chart-highcharts", "chart-vegalite", "advanced_charting"}
TEXT_TYPES = {"markdown", "html"}
POST_TYPES = SSRM_TABLE_TYPES
PLACEHOLDER_TEXT = {
    "placeholder",
    "todo",
    "tbd",
    "coming soon",
    "lorem ipsum",
    "not implemented",
    "n/a",
}


@dataclass(frozen=True)
class RuntimeGrade:
    """The runtime-only part of a task grade."""

    score: float
    passed: bool
    checks_passed: int
    checks_total: int
    issues: tuple[GradeIssue, ...]
    deployment_receipt: DeploymentReceipt | None


@dataclass(frozen=True)
class RuntimeRoute:
    """One response installed on the shared evaluator fixture server."""

    dataset: RuntimeDataset


class _RuntimeServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), _RuntimeRequestHandler)
        self.routes: dict[str, RuntimeRoute] = {}
        self.route_lock = threading.Lock()
        self.request_count = 0
        self.route_counter = 0

    @property
    def base_url(self) -> str:
        host_value = self.server_address[0]
        host = host_value.decode("ascii") if isinstance(host_value, bytes) else str(host_value)
        port = int(self.server_address[1])
        return f"http://{host}:{port}"

    def install(self, dataset: RuntimeDataset) -> str:
        with self.route_lock:
            self.route_counter += 1
            token = f"{self.route_counter:08d}"
            self.routes[token] = RuntimeRoute(dataset=dataset)
        return f"{self.base_url}/__workspace_bench_runtime__/{token}"

    def remove(self, url: str) -> None:
        token = urlparse(url).path.rsplit("/", 1)[-1]
        with self.route_lock:
            self.routes.pop(token, None)


class _RuntimeRequestHandler(BaseHTTPRequestHandler):
    server: _RuntimeServer

    def do_GET(self) -> None:  # noqa: N802
        self._serve()

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        request_payload: JsonDict = {}
        if length:
            try:
                parsed = json.loads(self.rfile.read(length))
                if isinstance(parsed, dict):
                    request_payload = parsed
            except (UnicodeDecodeError, json.JSONDecodeError):
                request_payload = {}
        self._serve(request_payload)

    def _serve(self, request_payload: JsonDict | None = None) -> None:
        token = urlparse(self.path).path.rsplit("/", 1)[-1]
        with self.server.route_lock:
            route = self.server.routes.get(token)
            self.server.request_count += 1
        if route is None:
            self._send(b'{"error":"unavailable runtime endpoint"}', 404)
            return
        dataset = route.dataset
        if dataset.raw_body is not None:
            body = dataset.raw_body.encode("utf-8")
        else:
            body = json.dumps(
                materialize_dataset(dataset, request_payload or {}), sort_keys=True
            ).encode("utf-8")
        self._send(body, dataset.status)

    def _send(self, body: bytes, status: int) -> None:
        self.send_response(status)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


_SERVER: _RuntimeServer | None = None
_SERVER_THREAD: threading.Thread | None = None
_SERVER_LOCK = threading.Lock()


def get_runtime_server() -> _RuntimeServer:
    """Return the process-wide threaded fixture server, starting it once."""

    global _SERVER, _SERVER_THREAD
    with _SERVER_LOCK:
        if _SERVER is None:
            _SERVER = _RuntimeServer()
            _SERVER_THREAD = threading.Thread(
                target=_SERVER.serve_forever,
                name="workspace-bench-runtime-fixtures",
                daemon=True,
            )
            _SERVER_THREAD.start()
        return _SERVER


def shutdown_runtime_server() -> None:
    """Stop the shared server. Primarily useful to isolated tests."""

    global _SERVER, _SERVER_THREAD
    with _SERVER_LOCK:
        server, thread = _SERVER, _SERVER_THREAD
        _SERVER, _SERVER_THREAD = None, None
    if server is not None:
        server.shutdown()
        server.server_close()
    if thread is not None:
        thread.join(timeout=5)


atexit.register(shutdown_runtime_server)


def declared_fields(definition: JsonDict) -> set[str]:
    """Return response fields explicitly consumed by a widget definition."""

    fields: set[str] = set()
    data = definition.get("data")
    if isinstance(data, list):
        for row in data:
            if isinstance(row, dict):
                fields.update(str(key) for key in row)
    if isinstance(data, dict):
        table = data.get("table")
        if isinstance(table, dict):
            columns = table.get("columnsDefs")
            if isinstance(columns, list):
                for column in columns:
                    if not isinstance(column, dict):
                        continue
                    field = column.get("field")
                    if isinstance(field, str) and field:
                        fields.add(field)
                    render_params = column.get("renderFnParams")
                    if isinstance(render_params, dict):
                        for key in ("colorValueKey", "valueKey", "labelKey"):
                            value = render_params.get(key)
                            if isinstance(value, str) and value:
                                fields.add(value)
        for key in (
            "categoryField",
            "categoryKey",
            "xField",
            "xKey",
            "yField",
            "yKey",
            "valueField",
            "valueKey",
        ):
            value = data.get(key)
            if isinstance(value, str) and value:
                fields.add(value)
        series = data.get("series")
        if isinstance(series, list):
            for item in series:
                if isinstance(item, str) and item:
                    fields.add(item)
                elif isinstance(item, dict):
                    for key in ("field", "key", "valueField", "yField"):
                        value = item.get(key)
                        if isinstance(value, str) and value:
                            fields.add(value)
    return fields


def bind_dataset(
    definition: JsonDict,
    widget_id: str,
    datasets: tuple[RuntimeDataset, ...],
    *,
    pinned_paths: bool = False,
) -> RuntimeDataset | None:
    """Bind a widget by field compatibility, using widget identity as a tie-break."""

    required = declared_fields(definition)
    endpoint = definition.get("endpoint")
    compatible = [dataset for dataset in datasets if required.issubset(dataset.fields)]
    if pinned_paths:
        endpoint_path = _endpoint_path(endpoint)
        compatible = [dataset for dataset in compatible if dataset.path == endpoint_path]
    if not compatible:
        return None
    return min(
        compatible,
        key=lambda dataset: (
            dataset.widget_id != widget_id,
            len(set(dataset.fields) - required),
            dataset.name,
        ),
    )


def synthesize_params(definition: JsonDict) -> JsonDict:
    """Build deterministic representative values from a widget param schema."""

    result: JsonDict = {}
    for param in flatten_params(definition, recurse=True):
        name = param.get("paramName")
        param_type = param.get("type")
        if not isinstance(name, str) or not name or not isinstance(param_type, str):
            raise ValueError("every runtime parameter needs paramName and type")
        options = param.get("options")
        option_values = [
            item.get("value") if isinstance(item, dict) else item
            for item in options
        ] if isinstance(options, list) else []
        value: Any
        if (
            param_type == "date"
            and isinstance(param.get("value"), str)
            and param["value"].startswith("$currentDate")
        ):
            value = "2026-01-15"
        elif "value" in param and param["value"] not in (None, [], ""):
            value = param["value"]
        elif "default" in param and param["default"] not in (None, [], ""):
            value = param["default"]
        elif option_values:
            value = option_values[:2] if param.get("multiSelect") else option_values[0]
        else:
            value = _fixed_param_value(param_type, name, bool(param.get("multiSelect")))
        result[name] = value
    return result


def task_widget_data(
    definition: JsonDict,
    widget_id: str,
    checks: RuntimeChecks,
) -> tuple[Any, str | None]:
    """Resolve one custom widget against episode-owned deterministic data.

    The returned error is deliberately product-facing: it describes the backend
    response contract without exposing evaluator issue codes or rubric details.
    """

    dataset = bind_dataset(
        definition,
        widget_id,
        checks.datasets,
        pinned_paths=checks.pinned_paths,
    )
    compatible = dataset is not None
    if dataset is None:
        dataset = _identity_dataset(widget_id, checks.datasets)
    if dataset is None:
        return None, "The backend returned no data for this widget."
    if checks.pinned_paths and dataset.path != _endpoint_path(definition.get("endpoint")):
        return None, f"The configured endpoint {definition.get('endpoint')!r} was not found."
    form_error = _form_endpoint_error(definition, dataset)
    if form_error is not None:
        return None, form_error
    if not 200 <= dataset.status < 300:
        return None, f"The backend endpoint returned HTTP {dataset.status}."
    if dataset.raw_body is not None:
        try:
            payload = json.loads(dataset.raw_body)
        except json.JSONDecodeError:
            return None, "The backend response was not valid JSON."
    else:
        payload = materialize_dataset(dataset, {})
    if not compatible:
        missing = sorted(declared_fields(definition) - set(dataset.fields))
        return None, f"The backend response is missing declared fields: {missing}."
    shape_error = _shape_error(definition, payload)
    if shape_error is not None:
        return None, f"The backend response does not match the widget definition: {shape_error}"
    if _contains_placeholder(payload):
        return None, "The backend response contains placeholder data."
    return payload, None


def grade_runtime(task: Task, final_snapshot: JsonDict) -> RuntimeGrade:
    """Probe all final custom-backend widgets over the shared real HTTP server."""

    checks = task.success.runtime
    if checks is None:
        return RuntimeGrade(1.0, True, 0, 0, (), None)
    issues: list[GradeIssue] = []
    probe_outcomes: list[DeploymentProbeOutcome] = []
    passed = 0
    total = 0

    def check(condition: bool, code: str, message: str) -> None:
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
        else:
            issues.append(GradeIssue(code=code, message=message))

    def check_probe(
        condition: bool,
        code: str,
        message: str,
        *,
        backend_name: str,
        widget_id: str,
        endpoint: object,
        method: str,
        dataset_name: str | None,
    ) -> None:
        check(condition, code, message)
        probe_outcomes.append(
            DeploymentProbeOutcome(
                backend_name=backend_name,
                widget_id=widget_id,
                endpoint=str(endpoint) if endpoint is not None else "",
                method=method,
                dataset_name=dataset_name,
                passed=condition,
                outcome="passed" if condition else "failed",
                issue_code=None if condition else code,
            )
        )

    custom_backends = final_snapshot.get("custom_backends") or {}
    if not isinstance(custom_backends, dict) or not custom_backends:
        check(False, "endpoint_unreachable", "No declared custom backend endpoints were available.")
        return RuntimeGrade(
            0.0,
            False,
            passed,
            total,
            tuple(issues),
            _deployment_receipt(final_snapshot, probe_outcomes),
        )

    for backend in custom_backends.values():
        if not isinstance(backend, dict):
            continue
        backend_name = str(backend.get("name", "custom backend"))
        base_url = str(backend.get("url", ""))
        widgets = backend.get("widgets_json") or {}
        if not isinstance(widgets, dict):
            continue
        for widget_id, raw_definition in widgets.items():
            label = f"{backend_name}/{widget_id}"
            if not isinstance(raw_definition, dict):
                check_probe(
                    False,
                    "endpoint_response_incompatible",
                    f"{label}: widget definition is malformed.",
                    backend_name=backend_name,
                    widget_id=str(widget_id),
                    endpoint="",
                    method="UNKNOWN",
                    dataset_name=None,
                )
                continue
            definition = raw_definition
            endpoint = definition.get("endpoint")
            method = _request_method(definition)
            resolved = _resolve_endpoint(base_url, endpoint)
            if resolved is None:
                check_probe(
                    False,
                    "endpoint_unreachable",
                    f"{label}: endpoint {endpoint!r} cannot be resolved.",
                    backend_name=backend_name,
                    widget_id=str(widget_id),
                    endpoint=endpoint,
                    method=method,
                    dataset_name=None,
                )
                continue
            try:
                params = synthesize_params(definition)
            except ValueError as error:
                check_probe(
                    False,
                    "endpoint_params_invalid",
                    f"{label}: {error}.",
                    backend_name=backend_name,
                    widget_id=str(widget_id),
                    endpoint=endpoint,
                    method=method,
                    dataset_name=None,
                )
                continue

            dataset = bind_dataset(
                definition,
                str(widget_id),
                checks.datasets,
                pinned_paths=checks.pinned_paths,
            )
            compatible = dataset is not None
            if dataset is None:
                dataset = _identity_dataset(str(widget_id), checks.datasets)
            if dataset is None:
                check_probe(
                    False,
                    "endpoint_response_incompatible",
                    f"{label}: no task dataset covers fields {sorted(declared_fields(definition))}.",
                    backend_name=backend_name,
                    widget_id=str(widget_id),
                    endpoint=endpoint,
                    method=method,
                    dataset_name=None,
                )
                continue

            if checks.pinned_paths and dataset.path != _endpoint_path(endpoint):
                server = get_runtime_server()
                unavailable_url = (
                    f"{server.base_url}/__workspace_bench_runtime__/missing"
                )
                _, failure = _request_json(
                    unavailable_url,
                    definition,
                    params,
                    timeout=checks.request_timeout_ms / 1000,
                )
                code = failure[0] if failure is not None else "endpoint_unreachable"
                check_probe(
                    False,
                    code,
                    f"{label}: pinned endpoint {endpoint!r} is unavailable.",
                    backend_name=backend_name,
                    widget_id=str(widget_id),
                    endpoint=endpoint,
                    method=method,
                    dataset_name=dataset.name,
                )
                continue

            form_error = _form_endpoint_error(definition, dataset)
            if form_error is not None:
                check_probe(
                    False,
                    "form_submission_incompatible",
                    f"{label}: {form_error}",
                    backend_name=backend_name,
                    widget_id=str(widget_id),
                    endpoint=endpoint,
                    method=method,
                    dataset_name=dataset.name,
                )
                continue

            server = get_runtime_server()
            probe_url = server.install(dataset)
            try:
                response, failure = _request_json(
                    probe_url,
                    definition,
                    params,
                    timeout=checks.request_timeout_ms / 1000,
                )
                if failure is None and str(definition.get("type")) in SSRM_TABLE_TYPES:
                    failure = _verify_ssrm_paging(
                        probe_url,
                        definition,
                        params,
                        dataset,
                        timeout=checks.request_timeout_ms / 1000,
                    )
            finally:
                server.remove(probe_url)
            if failure is not None:
                code, message = failure
                check_probe(
                    False,
                    code,
                    f"{label}: {message}",
                    backend_name=backend_name,
                    widget_id=str(widget_id),
                    endpoint=endpoint,
                    method=method,
                    dataset_name=dataset.name,
                )
                continue
            if not compatible:
                check_probe(
                    False,
                    "endpoint_response_incompatible",
                    f"{label}: response fields do not cover {sorted(declared_fields(definition))}.",
                    backend_name=backend_name,
                    widget_id=str(widget_id),
                    endpoint=endpoint,
                    method=method,
                    dataset_name=dataset.name,
                )
                continue
            shape_error = _shape_error(definition, response)
            if shape_error is not None:
                check_probe(
                    False,
                    "endpoint_response_incompatible",
                    f"{label}: {shape_error}",
                    backend_name=backend_name,
                    widget_id=str(widget_id),
                    endpoint=endpoint,
                    method=method,
                    dataset_name=dataset.name,
                )
                continue
            if _contains_placeholder(response):
                check_probe(
                    False,
                    "endpoint_response_placeholder",
                    f"{label}: response contains placeholder data.",
                    backend_name=backend_name,
                    widget_id=str(widget_id),
                    endpoint=endpoint,
                    method=method,
                    dataset_name=dataset.name,
                )
                continue
            check_probe(
                True,
                "runtime_endpoint_usable",
                f"{label}: endpoint returned usable data.",
                backend_name=backend_name,
                widget_id=str(widget_id),
                endpoint=endpoint,
                method=method,
                dataset_name=dataset.name,
            )

    if total == 0:
        check(False, "endpoint_unreachable", "Custom backends declared no widget endpoints to probe.")
    return RuntimeGrade(
        passed / total,
        not issues,
        passed,
        total,
        tuple(issues),
        _deployment_receipt(final_snapshot, probe_outcomes),
    )


def _deployment_receipt(
    final_snapshot: JsonDict,
    probe_outcomes: list[DeploymentProbeOutcome],
) -> DeploymentReceipt:
    """Summarize evaluator-observed deployment state without model-authored evidence."""

    custom_backends = final_snapshot.get("custom_backends") or {}
    backend_names: set[str] = set()
    app_ids: set[str] = set()
    if isinstance(custom_backends, dict):
        for backend in custom_backends.values():
            if not isinstance(backend, dict):
                continue
            backend_name = backend.get("name")
            if isinstance(backend_name, str) and backend_name:
                backend_names.add(backend_name)
            apps = backend.get("apps_json") or []
            if not isinstance(apps, list):
                continue
            for app in apps:
                if not isinstance(app, dict):
                    continue
                app_id = app.get("template_id") or app.get("id") or app.get("name")
                if isinstance(app_id, str) and app_id:
                    app_ids.add(app_id)

    dashboard_ids: set[str] = set()
    dashboards = final_snapshot.get("dashboard_compositions") or {}
    if isinstance(dashboards, dict):
        for key, dashboard in dashboards.items():
            if not isinstance(dashboard, dict):
                continue
            widgets = dashboard.get("widgets") or []
            if not isinstance(widgets, list) or not any(
                isinstance(widget, dict) and widget.get("origin") in backend_names
                for widget in widgets
            ):
                continue
            dashboard_id = dashboard.get("dashboard_id") or key
            if isinstance(dashboard_id, str) and dashboard_id:
                dashboard_ids.add(dashboard_id)

    passed = sum(outcome.passed for outcome in probe_outcomes)
    counts = DeploymentReceiptCounts(
        backends=len(backend_names),
        apps=len(app_ids),
        instantiated_dashboards=len(dashboard_ids),
        widget_probes=len(probe_outcomes),
        widget_probes_passed=passed,
        widget_probes_failed=len(probe_outcomes) - passed,
    )
    return DeploymentReceipt(
        backend_names=tuple(sorted(backend_names)),
        app_ids=tuple(sorted(app_ids)),
        instantiated_dashboard_ids=tuple(sorted(dashboard_ids)),
        widget_probes=tuple(probe_outcomes),
        counts=counts,
    )


def _request_json(
    url: str,
    definition: JsonDict,
    params: JsonDict,
    *,
    timeout: float,
    ssm_request: JsonDict | None = None,
) -> tuple[Any, tuple[str, str] | None]:
    method = "POST" if _request_method(definition) == "POST" else "GET"
    if method == "POST":
        body_payload: JsonDict = dict(params)
        if str(definition.get("type")) in SSRM_TABLE_TYPES:
            body_payload.update(
                ssm_request
                or {"startRow": 0, "endRow": 100, "sortModel": [], "filterModel": {}}
            )
        body = json.dumps(body_payload, sort_keys=True).encode("utf-8")
        request = Request(url, data=body, method="POST", headers={"Content-Type": "application/json"})
    else:
        request_url = f"{url}?{urlencode(params, doseq=True)}" if params else url
        request = Request(request_url, method="GET")
    try:
        with urlopen(request, timeout=timeout) as response:
            status = response.status
            raw = response.read()
    except HTTPError as error:
        code = "endpoint_unreachable" if error.code == 404 else "endpoint_bad_status"
        return None, (code, f"HTTP {error.code} from runtime endpoint.")
    except (URLError, TimeoutError, OSError) as error:
        return None, ("endpoint_unreachable", f"request failed: {error}.")
    if not 200 <= status < 300:
        return None, ("endpoint_bad_status", f"HTTP {status} from runtime endpoint.")
    try:
        return json.loads(raw.decode("utf-8")), None
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        return None, ("endpoint_response_malformed", f"response is not parseable JSON: {error}.")


def materialize_dataset(dataset: RuntimeDataset, request: JsonDict) -> Any:
    """Materialize a compact fixture payload or deterministic generated page."""
    spec = dataset.payload_spec
    if spec is None:
        return copy.deepcopy(dataset.payload)
    rows = _seeded_rows(spec)
    sort_model = request.get("sortModel")
    filter_model = request.get("filterModel")
    if isinstance(filter_model, dict):
        rows = [row for row in rows if _ssrm_filter_match(row, filter_model)]
    if isinstance(sort_model, list):
        for sort in reversed(sort_model):
            if not isinstance(sort, dict):
                continue
            field = sort.get("colId") or sort.get("field")
            if isinstance(field, str):
                rows.sort(key=lambda row: (row.get(field) is None, row.get(field)), reverse=sort.get("sort") == "desc")
    if "startRow" in request or "endRow" in request:
        start = max(0, int(request.get("startRow", 0)))
        end = max(start, int(request.get("endRow", start + 100)))
        data_key = str(spec.get("data_key", "rows"))
        return {data_key: rows[start:end], "lastRow": len(rows)}
    return rows


def _seeded_rows(spec: JsonDict) -> list[JsonDict]:
    seed = int(spec["seed"])
    schema = spec["schema"]
    assert isinstance(schema, dict)
    return [
        {
            str(field): _seeded_value(seed, index, str(field), kind)
            for field, kind in schema.items()
        }
        for index in range(int(spec["n_rows"]))
    ]


def _seeded_value(seed: int, index: int, field: str, kind: Any) -> Any:
    digest = hashlib.sha256(f"{seed}:{index}:{field}".encode()).hexdigest()
    if isinstance(kind, dict) and isinstance(kind.get("values"), list) and kind["values"]:
        values = kind["values"]
        return values[int(digest[:8], 16) % len(values)]
    kind_name = str(kind)
    if kind_name == "integer":
        return int(digest[:8], 16) % 100_000
    if kind_name == "number":
        return round((int(digest[:10], 16) % 10_000_000) / 10_000, 4)
    if kind_name == "boolean":
        return bool(int(digest[0], 16) % 2)
    if kind_name == "date":
        day = int(digest[:8], 16) % 365
        return f"2025-{day // 31 + 1:02d}-{day % 28 + 1:02d}"
    return f"{field}_{index:05d}_{digest[:6]}"


def _ssrm_filter_match(row: JsonDict, filters: JsonDict) -> bool:
    for field, raw_filter in filters.items():
        if not isinstance(raw_filter, dict):
            continue
        expected = raw_filter.get("filter")
        actual = row.get(field)
        operation = raw_filter.get("type", "equals")
        if operation == "contains":
            if str(expected).casefold() not in str(actual).casefold():
                return False
        elif actual != expected:
            return False
    return True


def _verify_ssrm_paging(
    url: str,
    definition: JsonDict,
    params: JsonDict,
    dataset: RuntimeDataset,
    *,
    timeout: float,
) -> tuple[str, str] | None:
    spec = dataset.payload_spec
    if spec is None:
        return None
    n_rows = int(spec["n_rows"])
    data_key = str(spec.get("data_key", "rows"))
    start = max(0, n_rows - 27)
    partial, failure = _request_json(
        url,
        definition,
        params,
        timeout=timeout,
        ssm_request={"startRow": start, "endRow": n_rows + 20, "sortModel": [], "filterModel": {}},
    )
    if failure is not None:
        return failure
    if not isinstance(partial, dict) or len(partial.get(data_key, [])) != 27 or partial.get("lastRow") != n_rows:
        return "endpoint_response_incompatible", "SSRM partial page or total count is incorrect."
    rows = _seeded_rows(spec)
    field = next(iter(spec["schema"]))
    expected = rows[0][field]
    filtered, failure = _request_json(
        url,
        definition,
        params,
        timeout=timeout,
        ssm_request={
            "startRow": 0,
            "endRow": 50,
            "sortModel": [{"colId": field, "sort": "desc"}],
            "filterModel": {field: {"type": "equals", "filter": expected}},
        },
    )
    expected_rows = [row for row in rows if row[field] == expected]
    observed = filtered.get(data_key, []) if isinstance(filtered, dict) else []
    if (
        failure is not None
        or not isinstance(filtered, dict)
        or filtered.get("lastRow") != len(expected_rows)
        or any(row.get(field) != expected for row in observed)
        or observed != sorted(observed, key=lambda row: row.get(field), reverse=True)
    ):
        return "endpoint_response_incompatible", "SSRM sort/filter passthrough is incorrect."
    return None


def _shape_error(definition: JsonDict, payload: Any) -> str | None:
    widget_type = str(definition.get("type", "table"))
    if widget_type in TABLE_TYPES:
        rows = _table_rows(definition, payload)
        if not isinstance(rows, list) or not rows or not all(isinstance(row, dict) for row in rows):
            return "table/grid response must contain a non-empty list of objects."
        if widget_type == "live_grid":
            data = definition.get("data") or {}
            row_id = data.get("wsRowIdColumn") if isinstance(data, dict) else None
            if isinstance(row_id, str) and any(row_id not in row for row in rows):
                return f"live-grid row identifier {row_id!r} is missing from returned rows."
        for field in sorted(declared_fields(definition)):
            if any(field not in row for row in rows):
                return f"declared column {field!r} is missing from returned rows."
            if all(row.get(field) is None for row in rows):
                return f"declared column {field!r} is all null."
        return None
    if widget_type in CHART_TYPES:
        if isinstance(payload, list) and payload and all(isinstance(row, dict) for row in payload):
            for field in declared_fields(definition):
                if any(field not in row for row in payload):
                    return f"declared chart field {field!r} is missing."
                if all(row.get(field) is None for row in payload):
                    return f"declared chart field {field!r} is all null."
            if not declared_fields(definition) and not any(
                any(isinstance(value, (int, float)) and not isinstance(value, bool) for value in row.values())
                for row in payload
            ):
                return "chart response has no numeric series values."
            return None
        if isinstance(payload, dict) and payload and any(
            payload.get(key) not in (None, [], {}) for key in ("data", "series", "spec", "datasets")
        ):
            return None
        return "chart response cannot construct categories and series."
    if widget_type == "metric":
        return None if _non_empty(payload) else "metric response is empty."
    if widget_type in TEXT_TYPES:
        if isinstance(payload, str) and payload.strip():
            return None
        if isinstance(payload, dict) and any(
            isinstance(payload.get(key), str) and payload[key].strip()
            for key in ("content", "markdown", "html", "text")
        ):
            return None
        return f"{widget_type} response must contain non-empty text."
    fields = sorted(declared_fields(definition))
    if fields and isinstance(payload, list) and payload and all(
        isinstance(row, dict) for row in payload
    ):
        for field in fields:
            if any(field not in row for row in payload):
                return f"declared field {field!r} is missing from returned rows."
            if all(row.get(field) is None for row in payload):
                return f"declared field {field!r} is all null."
    if fields and isinstance(payload, dict):
        for field in fields:
            if field not in payload:
                return f"declared field {field!r} is missing."
            if payload.get(field) is None:
                return f"declared field {field!r} is null."
    return None if _non_empty(payload) else f"{widget_type} response is empty."


def response_shape_error(definition: JsonDict, payload: Any) -> str | None:
    """Validate a real backend payload with the shared runtime shape semantics."""

    return _shape_error(definition, payload)


def _table_rows(definition: JsonDict, payload: Any) -> Any:
    data = definition.get("data")
    data_key = data.get("dataKey") if isinstance(data, dict) else None
    if isinstance(data_key, str) and isinstance(payload, dict):
        return payload.get(data_key)
    if isinstance(payload, dict) and isinstance(payload.get("rows"), list):
        return payload["rows"]
    return payload


def _contains_placeholder(payload: Any) -> bool:
    if isinstance(payload, str):
        normalized = " ".join(payload.lower().split())
        return normalized in PLACEHOLDER_TEXT or any(
            marker in normalized for marker in ("lorem ipsum", "coming soon", "not implemented")
        )
    if isinstance(payload, dict):
        return any(_contains_placeholder(value) for value in payload.values())
    if isinstance(payload, list):
        return any(_contains_placeholder(value) for value in payload)
    return False


def contains_placeholder(payload: Any) -> bool:
    """Return whether a payload contains an obvious unfinished-value marker."""

    return _contains_placeholder(payload)


def _non_empty(payload: Any) -> bool:
    if payload is None:
        return False
    if isinstance(payload, str):
        return bool(payload.strip())
    if isinstance(payload, (list, dict)):
        return bool(payload)
    return True


def _fixed_param_value(param_type: str, name: str, multi_select: bool) -> Any:
    if multi_select:
        return ["AAPL", "MSFT"]
    if param_type == "date" or "date" in name.lower():
        return "2026-01-15"
    if param_type == "number":
        return 10
    if param_type == "boolean":
        return False
    if param_type == "button":
        return True
    if param_type in {"text", "endpoint", "ticker", "tabs", "form"}:
        return "AAPL" if name.lower() in {"symbol", "ticker"} else "fixture-value"
    raise ValueError(f"unsupported parameter type {param_type!r}")


def _request_method(definition: JsonDict) -> str:
    if str(definition.get("type")) in POST_TYPES:
        return "POST"
    methods = {
        str(param.get("method", "GET")).upper()
        for param in flatten_params(definition, recurse=True)
        if param.get("method")
    }
    return "POST" if "POST" in methods else "GET"


def _resolve_endpoint(base_url: str, endpoint: Any) -> str | None:
    if not isinstance(endpoint, str) or not endpoint.strip():
        return None
    base = base_url if base_url.endswith("/") else f"{base_url}/"
    resolved = urljoin(base, endpoint)
    parsed = urlparse(resolved)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    return resolved


def _endpoint_path(endpoint: Any) -> str | None:
    if not isinstance(endpoint, str) or not endpoint:
        return None
    parsed = urlparse(endpoint)
    return parsed.path or "/"


def _identity_dataset(
    widget_id: str, datasets: tuple[RuntimeDataset, ...]
) -> RuntimeDataset | None:
    return next((dataset for dataset in datasets if dataset.widget_id == widget_id), None)


def _form_endpoint_error(
    definition: JsonDict,
    dataset: RuntimeDataset,
) -> str | None:
    if dataset.form_endpoint is None:
        return None
    submitted = {
        _endpoint_path(param.get("endpoint"))
        for param in flatten_params(definition, recurse=True)
        if str(param.get("method", "GET")).upper() == "POST"
        and param.get("endpoint")
    }
    if dataset.form_endpoint in submitted:
        return None
    return (
        "The form submission route does not match the backend contract; "
        f"expected {dataset.form_endpoint!r}."
    )
