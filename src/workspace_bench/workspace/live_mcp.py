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
from workspace_bench.core.graders import grade_task
from workspace_bench.core.models import JsonDict, RunResult, Task, ToolCall, ToolTraceEvent
from workspace_bench.workspace.simulated_workspace import SimulatedWorkspace
from workspace_bench.workspace.tool_surface import WORKSPACE_TOOL_NAMES


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
# The live MCP exposes these two canonical synthetic tools as a resource and a
# prompt, respectively. Every actual tool expectation is derived from the one
# canonical tool surface so additions cannot silently drift between runners.
EXPECTED_MCP_TOOLS = set(WORKSPACE_TOOL_NAMES) - {
    "read_workspace_resource",
    "get_workspace_prompt",
}
EXPECTED_MCP_PROMPTS = {"workspace_tool_usage", "workspace_session_context"}
EXPECTED_MCP_RESOURCES = {
    "openbb://workspace/app-builder/index",
    "openbb://workspace/overview/what-is-workspace",
    "openbb://workspace/overview/ai-agent-contract",
    "openbb://workspace/contract/backend",
    "openbb://workspace/specs/widgets-json",
    "openbb://workspace/specs/apps-json",
    "openbb://workspace/specs/widget-types",
    "openbb://workspace/specs/widget-parameters",
    "openbb://workspace/specs/layout-grid",
    "openbb://workspace/guides/build-an-app",
    "openbb://workspace/guides/review-app",
    "openbb://workspace/guides/debug-app",
    "openbb://workspace/guides/convert-endpoint-to-widget",
    "openbb://workspace/examples/generic-http/minimal",
    "openbb://workspace/examples/python-fastapi/minimal",
    "openbb://workspace/validation/common-errors",
}


@dataclass(frozen=True)
class LiveMcpRunResult:
    """Result for one task run through a live Workspace MCP sidecar."""

    run_result: RunResult
    mcp_tools: tuple[str, ...]
    mcp_prompts: tuple[str, ...]
    mcp_resources: tuple[str, ...]
    surface_issues: tuple[str, ...]
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
        query = _single_payload(args.get("param_options_queries"), "param_options_queries")
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
    task: Task,
    base_url: str = "http://127.0.0.1:8787",
    agent: BenchAgent | str = "oracle",
    replace_existing_session: bool = False,
    check_surface: bool = False,
) -> LiveMcpRunResult:
    """Run a task through a live Workspace MCP sidecar."""

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
    workspace.reset(backends=task.fixtures, initial_state=task.initial_state)
    initial_snapshot = workspace.snapshot()
    trace: list[ToolTraceEvent] = []
    mcp_tools: tuple[str, ...] = ()
    mcp_prompts: tuple[str, ...] = ()
    mcp_resources: tuple[str, ...] = ()
    surface_issues: tuple[str, ...] = ()
    health_with_bridge: JsonDict = {}

    async with _BrowserBridge(
        deps=deps,
        base_url=normalized_base_url,
        workspace=workspace,
    ) as bridge:
        health_with_bridge = await _health(deps.httpx, normalized_base_url)
        async with deps.streamablehttp_client(f"{normalized_base_url}/mcp") as streams:
            read_stream, write_stream, _ = streams
            async with deps.ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tool_result = await session.list_tools()
                mcp_tools = tuple(tool.name for tool in tool_result.tools)
                mcp_prompts = await _list_prompt_names(session)
                mcp_resources = await _list_resource_uris(session)
                if check_surface:
                    surface_issues = _surface_issues(
                        tools=mcp_tools,
                        prompts=mcp_prompts,
                        resources=mcp_resources,
                    )
                for index, call in enumerate(resolved_agent.tool_calls(task), start=1):
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
    grade = grade_task(
        task,
        final_snapshot,
        tuple(trace),
        initial_snapshot=initial_snapshot,
    )
    return LiveMcpRunResult(
        run_result=RunResult(
            task=task,
            grade=grade,
            trace=tuple(trace),
            final_snapshot=final_snapshot,
        ),
        mcp_tools=mcp_tools,
        mcp_prompts=mcp_prompts,
        mcp_resources=mcp_resources,
        surface_issues=surface_issues,
        bridge_commands=tuple(bridge.commands),
        health_before=health_before,
        health_with_bridge=health_with_bridge,
        health_after=health_after,
    )


async def _list_prompt_names(session: Any) -> tuple[str, ...]:
    try:
        result = await session.list_prompts()
    except Exception:  # noqa: BLE001 - optional surface check handles absence.
        return ()
    return tuple(prompt.name for prompt in getattr(result, "prompts", []) or [])


async def _list_resource_uris(session: Any) -> tuple[str, ...]:
    try:
        result = await session.list_resources()
    except Exception:  # noqa: BLE001 - optional surface check handles absence.
        return ()
    return tuple(str(resource.uri) for resource in getattr(result, "resources", []) or [])


def _surface_issues(
    *,
    tools: tuple[str, ...],
    prompts: tuple[str, ...],
    resources: tuple[str, ...],
) -> tuple[str, ...]:
    issues: list[str] = []
    for label, expected, observed in (
        ("tool", EXPECTED_MCP_TOOLS, set(tools)),
        ("prompt", EXPECTED_MCP_PROMPTS, set(prompts)),
        ("resource", EXPECTED_MCP_RESOURCES, set(resources)),
    ):
        missing = sorted(expected - observed)
        if missing:
            issues.append(f"missing {label}(s): {', '.join(missing)}")
    return tuple(issues)


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
        # The real sidecar validates dashboard ids as UUIDs; the simulator
        # issues counter ids (dash_001), so drop workspace_state rather than
        # send an id the server would reject.
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
    if call.name == "read_workspace_resource":
        return await _call_mcp_resource(session, call)
    if call.name == "get_workspace_prompt":
        return await _call_mcp_prompt(session, call)
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


async def _call_mcp_resource(session: Any, call: ToolCall) -> JsonDict:
    uri = str(call.args.get("uri", ""))
    if not uri:
        return _synthetic_mcp_error(
            command=call.name,
            code="invalid_request",
            message="read_workspace_resource requires uri.",
        )
    try:
        result = await session.read_resource(uri)
    except Exception as error:  # noqa: BLE001 - failures are trace events.
        return _synthetic_mcp_error(
            command=call.name,
            code="mcp_resource_read_failed",
            message=str(error),
        )
    return _resource_result_payload(result, uri)


async def _call_mcp_prompt(session: Any, call: ToolCall) -> JsonDict:
    name = str(call.args.get("name", ""))
    if not name:
        return _synthetic_mcp_error(
            command=call.name,
            code="invalid_request",
            message="get_workspace_prompt requires name.",
        )
    arguments = call.args.get("arguments")
    if arguments is not None and not isinstance(arguments, dict):
        return _synthetic_mcp_error(
            command=call.name,
            code="invalid_request",
            message="get_workspace_prompt arguments must be an object when provided.",
        )
    try:
        result = await session.get_prompt(name, arguments=arguments)
    except Exception as error:  # noqa: BLE001 - failures are trace events.
        return _synthetic_mcp_error(
            command=call.name,
            code="mcp_prompt_get_failed",
            message=str(error),
        )
    return _prompt_result_payload(result, name)


def _synthetic_mcp_error(*, command: str, code: str, message: str) -> JsonDict:
    return {
        "ok": False,
        "command": command,
        "message": message,
        "data": None,
        "error": {"code": code, "message": message, "retryable": False},
    }


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


def _resource_result_payload(result: Any, uri: str) -> JsonDict:
    contents = []
    text_parts = []
    for item in getattr(result, "contents", []) or []:
        text = getattr(item, "text", None)
        blob = getattr(item, "blob", None)
        item_uri = str(getattr(item, "uri", uri))
        mime_type = getattr(item, "mimeType", None)
        payload: JsonDict = {"uri": item_uri}
        if mime_type:
            payload["mime_type"] = mime_type
        if isinstance(text, str):
            payload["text"] = text
            text_parts.append(text)
        elif isinstance(blob, str):
            payload["blob"] = blob
        contents.append(payload)
    return {
        "ok": True,
        "command": "read_workspace_resource",
        "message": "ok",
        "data": {
            "uri": uri,
            "contents": contents,
            "text": "\n".join(text_parts),
        },
        "error": None,
    }


def _prompt_result_payload(result: Any, name: str) -> JsonDict:
    messages = []
    text_parts = []
    for message in getattr(result, "messages", []) or []:
        role = getattr(message, "role", None)
        content = getattr(message, "content", None)
        text = _mcp_content_text(content)
        payload: JsonDict = {}
        if role:
            payload["role"] = role
        if text is not None:
            payload["content"] = text
            text_parts.append(text)
        messages.append(payload)
    return {
        "ok": True,
        "command": "get_workspace_prompt",
        "message": "ok",
        "data": {
            "name": name,
            "description": getattr(result, "description", None),
            "messages": messages,
            "text": "\n".join(text_parts),
        },
        "error": None,
    }


def _mcp_content_text(content: Any) -> str | None:
    if isinstance(content, str):
        return content
    text = getattr(content, "text", None)
    if isinstance(text, str):
        return text
    return None
