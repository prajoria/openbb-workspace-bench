"""Local static server for the bundled mock Workspace page."""

from __future__ import annotations

import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
from typing import Any


class _MockServer(ThreadingHTTPServer):
    daemon_threads = True

    @property
    def base_url(self) -> str:
        host, port = self.server_address[:2]
        host_text = host.decode("ascii") if isinstance(host, bytes) else str(host)
        return f"http://{host_text}:{port}"


class _MockHandler(BaseHTTPRequestHandler):
    server: _MockServer

    def do_GET(self) -> None:  # noqa: N802
        if self.path not in {"/", "/index.html"}:
            self.send_error(404)
            return
        body = (
            resources.files("workspace_bench.workspace.browser")
            .joinpath("mock_workspace.html")
            .read_bytes()
        )
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


class MockWorkspaceServer:
    """Context-managed server for the browser self-test page."""

    def __init__(self, host: str = "127.0.0.1", port: int = 0) -> None:
        self._server = _MockServer((host, port), _MockHandler)
        self._thread: threading.Thread | None = None

    @property
    def base_url(self) -> str:
        return self._server.base_url

    def start(self) -> "MockWorkspaceServer":
        self._thread = threading.Thread(
            target=self._serve,
            name="workspace-bench-mock-workspace",
            daemon=True,
        )
        self._thread.start()
        return self

    def _serve(self) -> None:
        self._server.serve_forever(poll_interval=0.01)

    def close(self) -> None:
        self._server.shutdown()
        self._server.server_close()
        if self._thread is not None:
            self._thread.join(timeout=5)
            self._thread = None

    def __enter__(self) -> "MockWorkspaceServer":
        return self.start()

    def __exit__(self, *args: object) -> None:
        self.close()
