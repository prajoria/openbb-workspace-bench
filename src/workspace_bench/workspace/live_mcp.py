"""Live Workspace MCP smoke runner.

This module exercises a running ``workspace-mcp`` sidecar over streamable HTTP.
It emulates the browser bridge with the benchmark simulator, so calls traverse:

agent trace -> real MCP HTTP server -> real websocket bridge -> simulator.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from workspace_bench.agents import BenchAgent, build_agent
from workspace_bench.graders import grade_scenario
from workspace_bench.models import JsonDict, RunResult, Scenario, ToolCall, ToolTraceEvent
from workspace_bench.simulated_workspace import SimulatedWorkspace


SNAPSHOT_FIELDS = {
    "generated_at",
    "workspace_state",
    "workspace_options",
    "dashboards",
    "dashboard_composition",
    "widgets",
    "context",
    "artifacts",
    "files",
    "tools",
    "skills",
}


@dataclass(frozen=True)
class LiveMcpRunResult:
    """Result for one scenario run through a live Workspace MCP sidecar."""

    run_result: RunResult
    mcp_tools: tuple[str, ...]
    bridge_commands: tuple[str, ...]
    health_before: JsonDict
    health_with_bridge: JsonDict
    health_after: JsonDict


def bridge_command_to_simulator_call(command: JsonDict) -> tuple[str, JsonDict]:
    """Translate browser-bridge command payloads into simulator tool calls."""

    command_name = str(command.get("command", ""))
    args = {
        key: value
        for key, value in command.items()
        if key not in {"command", "request_id"} and value is not None
    }

    if command_name == "update_dashboard_layout":
        return "update_widget_layout", args

    if command_name == "get_widget_data":
        source = _single_payload(args.get("data_sources"), "data_sources")
        return (
            "get_widget_data",
            {
                "origin": source.get("origin"),
                "widget_id": source.get("widget_id") or source.get("id"),
                "data_args": source.get("data_args")
                or source.get("input_args")
                or source.get("params")
                or {},
                "widget_uuid": source.get("widget_uuid"),
                "ssm_request": source.get("ssm_request"),
            },
        )

    if command_name == "get_params_options":
        query = _single_payload(
            args.get("param_options_queries"), "param_options_queries"
        )
        return (
            "get_params_options",
            {
                "origin": query.get("origin"),
                "widget_id": query.get("widget_id") or query.get("id"),
                "param_name": query.get("param_name") or query.get("param"),
                "data_args": query.get("data_args")
                or query.get("options_endpoint_input_args")
                or query.get("params")
                or {},
            },
        )

    return command_name, args


async def run_workspace_mcp_smoke(
    *,
    scenario: Scenario,
    base_url: str = "http://127.0.0.1:8787",
    agent: BenchAgent | str = "oracle",
    replace_existing_session: bool = False,
) -> LiveMcpRunResult:
    """Run a scenario through a live Workspace MCP sidecar."""

    deps = _load_live_dependencies()
    normalized_base_url = base_url.rstrip("/")
    health_before = await _health(deps.httpx, normalized_base_url)
    if health_before.get("browser_connected") and not replace_existing_session:
        raise RuntimeError(
            "workspace-mcp already has a browser connected. Re-run with "
            "--replace-browser-session to let the smoke test replace it."
        )

    resolved_agent = build_agent(agent) if isinstance(agent, str) else agent
    workspace = SimulatedWorkspace()
    workspace.reset(backends=scenario.fixtures, initial_state=scenario.initial_state)
    trace: list[ToolTraceEvent] = []
    mcp_tools: tuple[str, ...] = ()
    health_with_bridge: JsonDict = {}

    async with _BrowserBridge(
        deps=deps,
        base_url=normalized_base_url,
        workspace=workspace,
    ) as bridge:
        health_with_bridge = await _health(deps.httpx, normalized_base_url)
        async with deps.streamablehttp_client(
            f"{normalized_base_url}/mcp"
        ) as streams:
            read_stream, write_stream, _ = streams
            async with deps.ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tool_result = await session.list_tools()
                mcp_tools = tuple(tool.name for tool in tool_result.tools)
                for index, call in enumerate(resolved_agent.tool_calls(scenario), start=1):
                    payload = await _call_mcp_tool(session, call)
                    trace.append(
                        ToolTraceEvent(
                            index=index,
                            call=call,
                            ok=bool(payload.get("ok")),
                            result=payload,
                        )
                    )

    health_after = await _health(deps.httpx, normalized_base_url)
    final_snapshot = workspace.snapshot()
    grade = grade_scenario(scenario, final_snapshot, tuple(trace))
    return LiveMcpRunResult(
        run_result=RunResult(
            scenario=scenario,
            grade=grade,
            trace=tuple(trace),
            final_snapshot=final_snapshot,
        ),
        mcp_tools=mcp_tools,
        bridge_commands=tuple(bridge.commands),
        health_before=health_before,
        health_with_bridge=health_with_bridge,
        health_after=health_after,
    )


@dataclass(frozen=True)
class _LiveDependencies:
    httpx: Any
    websockets: Any
    ClientSession: Any
    streamablehttp_client: Any


def _load_live_dependencies() -> _LiveDependencies:
    try:
        import httpx
        import websockets
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client
    except ImportError as error:
        raise RuntimeError(
            "Live Workspace MCP smoke tests require optional dependencies. "
            "Install with `uv sync --extra live` or run with "
            "`uv run --extra live workspace-bench smoke-workspace-mcp ...`."
        ) from error

    return _LiveDependencies(
        httpx=httpx,
        websockets=websockets,
        ClientSession=ClientSession,
        streamablehttp_client=streamablehttp_client,
    )


class _BrowserBridge:
    def __init__(
        self,
        *,
        deps: _LiveDependencies,
        base_url: str,
        workspace: SimulatedWorkspace,
    ) -> None:
        self._deps = deps
        self._base_url = base_url
        self._workspace = workspace
        self._ws_cm: Any = None
        self._ws: Any = None
        self._task: asyncio.Task[None] | None = None
        self.commands: list[str] = []

    async def __aenter__(self) -> "_BrowserBridge":
        async with self._deps.httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/bridge/session/start",
                json={
                    "client_name": "workspace-bench",
                    "current_dashboard_id": self._workspace.active_dashboard_id,
                    "current_tab_id": self._workspace.active_tab_id,
                },
            )
            response.raise_for_status()
            websocket_url = response.json()["websocket_url"]

        self._ws_cm = self._deps.websockets.connect(websocket_url)
        self._ws = await self._ws_cm.__aenter__()
        ready = json.loads(await self._ws.recv())
        if ready.get("type") != "session_ready":
            raise RuntimeError(f"Workspace bridge did not become ready: {ready!r}")
        self._task = asyncio.create_task(self._serve())
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        if self._ws_cm is not None:
            await self._ws_cm.__aexit__(exc_type, exc, tb)

    async def _serve(self) -> None:
        assert self._ws is not None
        while True:
            message = json.loads(await self._ws.recv())
            if message.get("type") != "command_request":
                continue
            command = message["command"]
            self.commands.append(str(command.get("command")))
            result = execute_bridge_command(self._workspace, command)
            await self._send_session_context()
            await self._ws.send(json.dumps({"type": "command_result", "result": result}))

    async def _send_session_context(self) -> None:
        assert self._ws is not None
        await self._ws.send(
            json.dumps(
                {
                    "type": "session_context_changed",
                    "session": {
                        "current_dashboard_id": self._workspace.active_dashboard_id,
                        "current_tab_id": self._workspace.active_tab_id,
                    },
                }
            )
        )


def execute_bridge_command(workspace: SimulatedWorkspace, command: JsonDict) -> JsonDict:
    """Execute one real sidecar bridge command against the simulator."""

    original_command = str(command.get("command", ""))
    tool_name, args = bridge_command_to_simulator_call(command)
    result = workspace.call_tool(tool_name, args)
    result["command"] = original_command
    result["request_id"] = command.get("request_id")
    if original_command == "get_workspace_snapshot" and result.get("ok"):
        result["data"] = _mcp_compatible_snapshot(result.get("data") or {})
    return result


def _mcp_compatible_snapshot(snapshot: JsonDict) -> JsonDict:
    payload = {key: value for key, value in snapshot.items() if key in SNAPSHOT_FIELDS}
    workspace_state = payload.get("workspace_state")
    if isinstance(workspace_state, dict):
        dashboard_uuid = workspace_state.get("current_dashboard_uuid")
        try:
            UUID(str(dashboard_uuid))
        except (TypeError, ValueError):
            payload.pop("workspace_state", None)
    return payload


def _single_payload(value: Any, field_name: str) -> JsonDict:
    if not isinstance(value, list) or len(value) != 1 or not isinstance(value[0], dict):
        raise ValueError(f"{field_name} must contain exactly one object")
    return value[0]


async def _health(httpx: Any, base_url: str) -> JsonDict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/health")
        response.raise_for_status()
        return response.json()


async def _call_mcp_tool(session: Any, call: ToolCall) -> JsonDict:
    try:
        result = await session.call_tool(call.name, call.args)
    except Exception as error:  # noqa: BLE001 - failures are trace events.
        return {
            "ok": False,
            "command": call.name,
            "message": str(error),
            "data": None,
            "error": {"code": "mcp_call_failed", "message": str(error)},
        }
    return _tool_result_payload(result, call.name)


def _tool_result_payload(result: Any, command: str) -> JsonDict:
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
        "ok": not bool(getattr(result, "isError", False)),
        "command": command,
        "message": "MCP call returned no structured payload.",
        "data": None,
        "error": None,
    }
