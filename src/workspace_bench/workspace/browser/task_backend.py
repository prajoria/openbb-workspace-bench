"""Serve one task's oracle backend and deterministic runtime datasets."""

from __future__ import annotations

import json
import threading
from copy import deepcopy
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse

from workspace_bench.core.models import JsonDict, RuntimeDataset, Task
from workspace_bench.core.runner import TaskRunner
from workspace_bench.workspace.runtime import bind_dataset


@dataclass(frozen=True)
class TaskBackendModel:
    """The oracle-authored backend contract and routes for one task."""

    task_ref: str
    backend_name: str
    widgets: JsonDict
    apps: list[JsonDict]
    datasets_by_path: dict[str, RuntimeDataset]
    auxiliary_payloads: dict[str, Any]


def build_task_backend_model(task: Task, backend_name: str | None = None) -> TaskBackendModel:
    """Materialize an oracle backend without modifying task or grader state."""

    runtime = task.success.runtime
    if runtime is None:
        raise ValueError(f"{task.qualified_id} has no runtime_checks datasets")
    snapshot = TaskRunner().run(task, "oracle").final_snapshot
    backends = list(snapshot.get("custom_backends", {}).values())
    if backend_name is not None:
        backends = [backend for backend in backends if backend.get("name") == backend_name]
    if len(backends) != 1:
        names = sorted(str(backend.get("name")) for backend in backends)
        raise ValueError(
            f"{task.qualified_id} needs exactly one selected oracle backend; found {names}"
        )
    backend = backends[0]
    name = backend.get("name")
    widgets = backend.get("widgets_json")
    apps = backend.get("apps_json")
    if not isinstance(name, str) or not isinstance(widgets, dict) or not isinstance(apps, list):
        raise ValueError(f"{task.qualified_id} oracle backend snapshot is malformed")

    served_widgets = deepcopy(widgets)
    routes: dict[str, RuntimeDataset] = {}
    auxiliary: dict[str, Any] = {}
    for widget_id, raw_definition in served_widgets.items():
        if not isinstance(widget_id, str) or not isinstance(raw_definition, dict):
            raise ValueError(f"{task.qualified_id} contains a malformed widget definition")
        dataset = bind_dataset(
            raw_definition,
            widget_id,
            runtime.datasets,
            pinned_paths=runtime.pinned_paths,
        )
        endpoint = raw_definition.get("endpoint")
        if dataset is None or not isinstance(endpoint, str):
            raise ValueError(f"{task.qualified_id}/{widget_id} cannot bind a runtime endpoint")
        served_path = dataset.path or _normal_path(endpoint)
        raw_definition["endpoint"] = _normal_path(served_path)
        routes[_normal_path(served_path)] = dataset
        _collect_auxiliary_routes(raw_definition, dataset, auxiliary)

    for dataset in runtime.datasets:
        if dataset.path:
            routes.setdefault(_normal_path(dataset.path), dataset)
    return TaskBackendModel(
        task_ref=task.qualified_id,
        backend_name=name,
        widgets=served_widgets,
        apps=[app for app in apps if isinstance(app, dict)],
        datasets_by_path=routes,
        auxiliary_payloads=auxiliary,
    )


def _collect_auxiliary_routes(
    definition: JsonDict,
    dataset: RuntimeDataset,
    routes: dict[str, Any],
) -> None:
    params = definition.get("params", [])
    if not isinstance(params, list):
        return
    for param in params:
        if not isinstance(param, dict):
            continue
        options_endpoint = param.get("optionsEndpoint")
        if isinstance(options_endpoint, str):
            options = param.get("options")
            routes[_normal_path(options_endpoint)] = (
                options if isinstance(options, list) and options else _option_payload(param)
            )
        endpoint = param.get("endpoint")
        if isinstance(endpoint, str):
            routes[_normal_path(endpoint)] = {
                "ok": True,
                "dataset": dataset.name,
                "payload": dataset.payload,
            }
        input_params = param.get("inputParams")
        if isinstance(input_params, list):
            for child in input_params:
                if not isinstance(child, dict):
                    continue
                child_options = child.get("optionsEndpoint")
                if isinstance(child_options, str):
                    routes[_normal_path(child_options)] = _option_payload(child)


def _option_payload(param: JsonDict) -> list[JsonDict]:
    value = param.get("value")
    values = value if isinstance(value, list) else [value]
    usable = [item for item in values if item not in (None, "", [])]
    if not usable:
        usable = ["AAPL", "MSFT", "NVDA"]
    return [{"label": str(item), "value": item} for item in usable]


class _TaskBackendHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(
        self,
        address: tuple[str, int],
        model: TaskBackendModel,
        cors_origin: str,
    ) -> None:
        super().__init__(address, _TaskBackendHandler)
        self.model = model
        self.cors_origin = cors_origin
        self.request_log: list[JsonDict] = []
        self.request_lock = threading.Lock()

    @property
    def base_url(self) -> str:
        host, port = self.server_address[:2]
        host_text = host.decode("ascii") if isinstance(host, bytes) else str(host)
        return f"http://{host_text}:{port}"


class _TaskBackendHandler(BaseHTTPRequestHandler):
    server: _TaskBackendHTTPServer

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        self._serve("GET")

    def do_POST(self) -> None:  # noqa: N802
        self._serve("POST")

    def _serve(self, method: str) -> None:
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8") if length else ""
        query = {key: values[-1] for key, values in parse_qs(parsed.query).items()}
        with self.server.request_lock:
            self.server.request_log.append(
                {"method": method, "path": parsed.path, "query": query, "body": body}
            )
        if parsed.path == "/widgets.json":
            self._json(self.server.model.widgets)
            return
        if parsed.path == "/apps.json":
            self._json(self.server.model.apps)
            return
        if parsed.path == "/health":
            self._json(
                {
                    "ok": True,
                    "task": self.server.model.task_ref,
                    "backend": self.server.model.backend_name,
                }
            )
            return
        dataset = self.server.model.datasets_by_path.get(_normal_path(parsed.path))
        if dataset is not None:
            if dataset.raw_body is not None:
                self._send(
                    dataset.raw_body.encode("utf-8"),
                    dataset.status,
                    "application/json; charset=utf-8",
                )
            else:
                self._json(dataset.payload, status=dataset.status)
            return
        auxiliary = self.server.model.auxiliary_payloads.get(_normal_path(parsed.path))
        if auxiliary is not None:
            self._json(auxiliary)
            return
        self._json({"error": f"unknown task backend path: {parsed.path}"}, status=404)

    def _json(self, payload: Any, status: int = 200) -> None:
        self._send(
            json.dumps(payload, indent=2, sort_keys=True).encode("utf-8"),
            status,
            "application/json; charset=utf-8",
        )

    def _send(self, body: bytes, status: int, content_type: str) -> None:
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", self.server.cors_origin)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")

    def log_message(self, format: str, *args: Any) -> None:
        return


class TaskBackendServer:
    """Threaded lifecycle wrapper used by the CLI, dry-run, and browser harness."""

    def __init__(
        self,
        task: Task,
        *,
        backend_name: str | None = None,
        host: str = "127.0.0.1",
        port: int = 0,
        cors_origin: str = "*",
    ) -> None:
        self.model = build_task_backend_model(task, backend_name)
        self._server = _TaskBackendHTTPServer((host, port), self.model, cors_origin)
        self._thread: threading.Thread | None = None

    @property
    def base_url(self) -> str:
        return self._server.base_url

    @property
    def request_log(self) -> tuple[JsonDict, ...]:
        with self._server.request_lock:
            return tuple(self._server.request_log)

    def start(self) -> "TaskBackendServer":
        if self._thread is None:
            self._thread = threading.Thread(
                target=self._serve,
                name=f"task-backend-{self.model.task_ref}",
                daemon=True,
            )
            self._thread.start()
        return self

    def _serve(self) -> None:
        self._server.serve_forever(poll_interval=0.01)

    def serve_forever(self) -> None:
        self._server.serve_forever()

    def close(self) -> None:
        if self._thread is not None:
            self._server.shutdown()
            self._thread.join(timeout=5)
            self._thread = None
        self._server.server_close()

    def __enter__(self) -> "TaskBackendServer":
        return self.start()

    def __exit__(self, *args: object) -> None:
        self.close()


def _normal_path(value: str) -> str:
    path = urlparse(value).path or "/"
    return path if path.startswith("/") else f"/{path}"
