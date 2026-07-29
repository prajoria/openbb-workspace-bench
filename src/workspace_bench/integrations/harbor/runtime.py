"""Trusted Harbor runtime: MCP gateway, browser bridge, and episode recorder."""

from __future__ import annotations

import argparse
import asyncio
import json
from copy import deepcopy
from contextlib import suppress
from pathlib import Path
from typing import Any, Awaitable, Callable, TypeVar
from urllib.parse import urlsplit, urlunsplit

from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.tools.tool import ToolResult
from mcp.types import TextContent

from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.models import (
    FINAL_ANSWER_TOOL,
    JsonDict,
    ToolCall,
    ToolTraceEvent,
    final_answer_from_trace,
    final_answer_text,
)
from workspace_bench.integrations.harbor.artifacts import (
    EPISODE_SCHEMA_VERSION,
    atomic_write_json,
    trace_event_payload,
)
from workspace_bench.integrations.harbor.bundle import load_sealed_task
from workspace_bench.workspace.live_mcp import (
    bridge_command_to_simulator_call,
    execute_bridge_command,
)


T = TypeVar("T")


class EpisodeRecorder:
    """Own the canonical trace and atomically publish trusted runtime state."""

    def __init__(
        self,
        *,
        episode: WorkspaceEpisode,
        artifact_path: Path,
        metadata: JsonDict,
    ) -> None:
        self.episode = episode
        self.artifact_path = artifact_path
        self.metadata = metadata
        self.bridge_events: list[JsonDict] = []
        self.rejections: list[JsonDict] = []
        self.final_snapshot: JsonDict | None = None
        self.finalized = False
        self.status = "starting"

    @property
    def trace(self) -> list[ToolTraceEvent]:
        return self.episode.trace

    @property
    def answered(self) -> bool:
        return final_answer_from_trace(tuple(self.trace)) is not None

    def append(self, name: str, args: JsonDict, result: JsonDict) -> None:
        event = ToolTraceEvent(
            index=len(self.trace) + 1,
            call=ToolCall(name=name, args=args),
            ok=bool(result.get("ok")),
            result=result,
        )
        self.trace.append(event)
        self.persist()

    def reject(self, name: str, args: JsonDict, result: JsonDict) -> None:
        """Retain non-trace terminal rejections without changing native grades."""

        self.rejections.append(
            {
                "index": len(self.rejections) + 1,
                "call": {"name": name, "args": args},
                "result": result,
            }
        )
        self.persist()

    def persist(self, *, status: str | None = None) -> None:
        if status is not None:
            self.status = status
        payload = {
            "schema_version": EPISODE_SCHEMA_VERSION,
            "task": self.metadata,
            "status": self.status,
            "initial_snapshot": self.episode.initial_snapshot,
            "final_snapshot": self.final_snapshot,
            "trace": [trace_event_payload(event) for event in self.trace],
            "bridge_events": self.bridge_events,
            "rejections": self.rejections,
            "answered": self.answered,
            "final_answer": final_answer_from_trace(tuple(self.trace)),
            "turns_used": len(self.trace),
            "max_turns": self.episode.max_turns,
            "turns_exhausted": bool(
                self.episode.max_turns and len(self.trace) >= self.episode.max_turns
            ),
            "finalized": self.finalized,
        }
        atomic_write_json(self.artifact_path, payload)

    def finalize(self) -> None:
        """Capture the final snapshot exactly once after Harbor stops main."""

        if not self.finalized:
            self.final_snapshot = self.episode.snapshot()
            self.finalized = True
        self.persist(status="finalized")


def structured_result(payload: JsonDict) -> ToolResult:
    """Return a normal MCP tool result carrying a benchmark response object."""

    return ToolResult(
        content=[TextContent(type="text", text=json.dumps(payload, sort_keys=True))],
        structured_content=payload,
    )


def tool_result_payload(result: Any, command: str) -> JsonDict:
    """Normalize FastMCP internal and MCP-client result spellings."""

    structured = getattr(result, "structured_content", None)
    if structured is None:
        structured = getattr(result, "structuredContent", None)
    if isinstance(structured, dict):
        return structured
    for item in getattr(result, "content", []) or []:
        text = getattr(item, "text", None)
        if not isinstance(text, str):
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    return {
        "ok": True,
        "command": command,
        "message": "MCP call returned no structured payload.",
        "data": None,
        "error": None,
    }


def canonical_bridge_result(recorder: EpisodeRecorder, event: JsonDict) -> JsonDict:
    """Remove live transport metadata while retaining the raw bridge audit event."""

    result = deepcopy(event["result"])
    result["request_id"] = None
    if event.get("translated_tool") == "get_workspace_snapshot":
        data = result.get("data")
        if isinstance(data, dict):
            workspace = recorder.episode.workspace
            data["workspace_state"] = {
                "current_dashboard_uuid": workspace.active_dashboard_id,
                "current_tab_id": workspace.active_tab_id,
            }
    return result


def call_error(command: str, code: str, message: str, *, retryable: bool = False) -> JsonDict:
    return {
        "ok": False,
        "command": command,
        "request_id": None,
        "message": message,
        "data": None,
        "error": {"code": code, "message": message, "retryable": retryable},
    }


class EpisodeMiddleware(Middleware):
    """Enforce task semantics and record calls before schema validation."""

    def __init__(self, recorder: EpisodeRecorder) -> None:
        self.recorder = recorder
        self.lock = asyncio.Lock()

    async def on_list_tools(self, context: Any, call_next: Callable[[Any], Awaitable[Any]]) -> Any:
        tools = await call_next(context)
        allowed = set(self.recorder.episode.task.allowed_tools)
        return [tool for tool in tools if tool.name in allowed]

    async def on_call_tool(
        self,
        context: MiddlewareContext[Any],
        call_next: Callable[[MiddlewareContext[Any]], Awaitable[ToolResult]],
    ) -> ToolResult:
        name = str(context.message.name)
        args = dict(context.message.arguments or {})
        async with self.lock:
            terminal = self._terminal_rejection(name)
            if terminal is not None:
                self.recorder.reject(name, args, terminal)
                return structured_result(terminal)

            if name not in self.recorder.episode.task.allowed_tools:
                result = call_error(
                    name,
                    "invalid_request",
                    f"Tool {name!r} is not allowed.",
                )
                self.recorder.append(name, args, result)
                return structured_result(result)

            bridge_count = len(self.recorder.bridge_events)
            try:
                raw_result = await call_next(context)
                result = tool_result_payload(raw_result, name)
                new_bridge_events = self.recorder.bridge_events[bridge_count:]
                if (
                    len(new_bridge_events) == 1
                    and new_bridge_events[0].get("translated_tool") == name
                ):
                    result = canonical_bridge_result(
                        self.recorder, new_bridge_events[0]
                    )
            except Exception as error:  # noqa: BLE001 - invalid calls are benchmark events.
                result = call_error(
                    name,
                    "mcp_call_failed",
                    str(error),
                    retryable=True,
                )
                raw_result = structured_result(result)
            self.recorder.append(name, args, result)
            return raw_result

    def _terminal_rejection(self, name: str) -> JsonDict | None:
        if self.recorder.answered:
            return call_error(
                name,
                "episode_completed",
                "A final answer was already submitted; the episode is complete.",
            )
        episode = self.recorder.episode
        if episode.max_turns and len(episode.trace) >= episode.max_turns:
            return call_error(
                name,
                "turn_budget_exhausted",
                "The episode's turn budget is exhausted; the call was not executed.",
            )
        return None


class BrowserBridge:
    """Persistent simulated Workspace browser connected to the real sidecar."""

    def __init__(self, *, base_url: str, recorder: EpisodeRecorder) -> None:
        self.base_url = base_url.rstrip("/")
        self.recorder = recorder
        self._httpx: Any = None
        self._websockets: Any = None
        self._ws_context: Any = None
        self._ws: Any = None
        self._serve_task: asyncio.Task[None] | None = None

    async def __aenter__(self) -> "BrowserBridge":
        import httpx
        import websockets

        self._httpx = httpx
        self._websockets = websockets
        workspace = self.recorder.episode.workspace
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/bridge/session/start",
                json={
                    "client_name": "workspace-bench-harbor",
                    "current_dashboard_id": workspace.active_dashboard_id,
                    "current_tab_id": workspace.active_tab_id,
                },
            )
            response.raise_for_status()
            returned_url = str(response.json()["websocket_url"])

        returned = urlsplit(returned_url)
        upstream = urlsplit(self.base_url)
        websocket_url = urlunsplit(
            (returned.scheme, upstream.netloc, returned.path, returned.query, returned.fragment)
        )
        self._ws_context = websockets.connect(websocket_url)
        self._ws = await self._ws_context.__aenter__()
        ready = json.loads(await self._ws.recv())
        if ready.get("type") != "session_ready":
            raise RuntimeError(f"Workspace bridge did not become ready: {ready!r}")
        self._serve_task = asyncio.create_task(self._serve())
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        if self._serve_task is not None:
            self._serve_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._serve_task
        if self._ws_context is not None:
            await self._ws_context.__aexit__(exc_type, exc, tb)

    async def _serve(self) -> None:
        assert self._ws is not None
        workspace = self.recorder.episode.workspace
        while True:
            message = json.loads(await self._ws.recv())
            if message.get("type") != "command_request":
                continue
            command = dict(message["command"])
            translated_tool, translated_args = bridge_command_to_simulator_call(command)
            result = execute_bridge_command(workspace, command)
            self.recorder.bridge_events.append(
                {
                    "index": len(self.recorder.bridge_events) + 1,
                    "command": command,
                    "translated_tool": translated_tool,
                    "translated_args": translated_args,
                    "result": result,
                }
            )
            await self._send_session_context()
            await self._ws.send(json.dumps({"type": "command_result", "result": result}))

    async def _send_session_context(self) -> None:
        assert self._ws is not None
        workspace = self.recorder.episode.workspace
        await self._ws.send(
            json.dumps(
                {
                    "type": "session_context_changed",
                    "session": {
                        "current_dashboard_id": workspace.active_dashboard_id,
                        "current_tab_id": workspace.active_tab_id,
                    },
                }
            )
        )


def create_gateway(upstream_url: str, recorder: EpisodeRecorder) -> tuple[FastMCP, EpisodeMiddleware]:
    """Build the agent-facing proxy plus the harness-level answer tool."""

    gateway = FastMCP.as_proxy(
        upstream_url,
        name="OpenBB Workspace Bench Gateway",
    )

    @gateway.tool(
        description=(
            "Submit the final response for this Workspace task. A successful call "
            "completes the episode."
        )
    )
    async def final_answer(
        text: str | None = None,
        answer: str | None = None,
        answer_text: str | None = None,
        data: str | None = None,
        content: str | None = None,
    ) -> JsonDict:
        args = {
            key: value
            for key, value in {
                "text": text,
                "answer": answer,
                "answer_text": answer_text,
                "data": data,
                "content": content,
            }.items()
            if value is not None
        }
        resolved = final_answer_text(args)
        if not isinstance(resolved, str) or not resolved.strip():
            return call_error(
                FINAL_ANSWER_TOOL,
                "invalid_request",
                "final_answer requires non-empty text.",
                retryable=True,
            )
        return {
            "ok": True,
            "command": FINAL_ANSWER_TOOL,
            "request_id": None,
            "message": "Final answer recorded; the episode is complete.",
            "data": None,
        }

    middleware = EpisodeMiddleware(recorder)
    gateway.add_middleware(middleware)
    return gateway, middleware


async def _handle_control(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    *,
    recorder: EpisodeRecorder,
    middleware: EpisodeMiddleware,
) -> None:
    try:
        command = (await reader.readline()).decode(errors="replace").strip()
        if command != "FINALIZE":
            writer.write(b"ERROR unsupported command\n")
        else:
            async with middleware.lock:
                recorder.finalize()
            writer.write(b"OK finalized\n")
        await writer.drain()
    finally:
        writer.close()
        await writer.wait_closed()


async def serve_runtime(args: argparse.Namespace) -> None:
    task, metadata = load_sealed_task(args.task)
    episode = WorkspaceEpisode(task)
    recorder = EpisodeRecorder(
        episode=episode,
        artifact_path=args.artifact,
        metadata=metadata,
    )
    recorder.persist(status="starting")
    gateway, middleware = create_gateway(args.upstream_mcp_url, recorder)

    args.control_socket.parent.mkdir(parents=True, exist_ok=True)
    args.control_socket.unlink(missing_ok=True)
    args.ready_file.parent.mkdir(parents=True, exist_ok=True)
    args.ready_file.unlink(missing_ok=True)

    async with BrowserBridge(base_url=args.workspace_mcp_url, recorder=recorder):
        control = await asyncio.start_unix_server(
            lambda reader, writer: _handle_control(
                reader,
                writer,
                recorder=recorder,
                middleware=middleware,
            ),
            path=args.control_socket,
        )
        recorder.persist(status="ready")
        args.ready_file.write_text("ready\n", encoding="utf-8")
        try:
            await gateway.run_async(
                transport="streamable-http",
                host=args.host,
                port=args.port,
                path="/mcp",
                stateless_http=True,
                show_banner=False,
            )
        finally:
            control.close()
            await control.wait_closed()
            args.ready_file.unlink(missing_ok=True)


async def request_finalize(socket_path: Path, timeout: float) -> None:
    reader, writer = await asyncio.wait_for(
        asyncio.open_unix_connection(socket_path), timeout=timeout
    )
    try:
        writer.write(b"FINALIZE\n")
        await writer.drain()
        response = await asyncio.wait_for(reader.readline(), timeout=timeout)
        if response != b"OK finalized\n":
            raise RuntimeError(response.decode(errors="replace").strip())
    finally:
        writer.close()
        await writer.wait_closed()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="workspace-bench-harbor-runtime")
    subparsers = parser.add_subparsers(dest="command", required=True)
    serve = subparsers.add_parser("serve")
    serve.add_argument("--task", type=Path, required=True)
    serve.add_argument("--artifact", type=Path, required=True)
    serve.add_argument("--workspace-mcp-url", default="http://workspace-mcp:8787")
    serve.add_argument("--upstream-mcp-url", default="http://workspace-mcp:8787/mcp")
    serve.add_argument("--host", default="0.0.0.0")
    serve.add_argument("--port", type=int, default=8790)
    serve.add_argument(
        "--control-socket",
        type=Path,
        default=Path("/run/workspace-bench/control.sock"),
    )
    serve.add_argument(
        "--ready-file",
        type=Path,
        default=Path("/run/workspace-bench/ready"),
    )
    finalize = subparsers.add_parser("finalize")
    finalize.add_argument(
        "--control-socket",
        type=Path,
        default=Path("/run/workspace-bench/control.sock"),
    )
    finalize.add_argument("--timeout", type=float, default=30.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "serve":
        asyncio.run(serve_runtime(args))
    else:
        asyncio.run(request_finalize(args.control_socket, args.timeout))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
