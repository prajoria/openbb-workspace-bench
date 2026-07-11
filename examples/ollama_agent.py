"""Ollama-backed Workspace Bench agent adapter.

This is a template for running a local open-weight model against
``workspace-bench run-agent-command``. It uses Ollama's local HTTP API and
expects the model to emit a JSON object with a ``tool_calls`` array.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_MODEL = "gpt-oss:20b"
DEFAULT_BASE_URL = "http://127.0.0.1:11434"
FIXTURE_ORIGINS = {
    "equities": "Bench Equities",
    "macro": "Bench Macro",
    "portfolio": "Bench Portfolio",
}
WIDGET_HINTS = {
    "Bench Equities": {
        "price_performance": {
            "data_args": {"symbol": "AAPL"},
            "note": "Use symbol, not ticker.",
        },
        "latest_news": {
            "data_args": {"symbol": "AAPL", "limit": 5},
            "note": "Use symbol for the company ticker.",
        },
        "estimate_history": {
            "data_args": {"symbol": "AAPL"},
            "note": "Use symbol for the company ticker.",
        },
        "fundamental_metrics": {
            "data_args": {"symbol": "AAPL"},
            "note": "Use symbol for the company ticker.",
        },
    },
    "Bench Macro": {
        "macro_timeseries": {
            "data_args": {"series": "DGS2"},
            "note": "Use series for macro identifiers such as FEDFUNDS, DGS2, DGS10, CPIAUCSL.",
        },
        "yield_curve": {"data_args": {}, "note": "No required data_args."},
    },
    "Bench Portfolio": {
        "holdings_table": {"data_args": {}, "note": "No required data_args."},
        "sector_exposure": {"data_args": {}, "note": "No required data_args."},
        "risk_metrics": {"data_args": {}, "note": "No required data_args."},
    },
}


TOOL_REFERENCE = {
    "get_workspace_snapshot": {
        "description": "Inspect current dashboard, tabs, widgets, layouts, and backends.",
        "args": {},
    },
    "manage_dashboard": {
        "description": "Create, read, or rename dashboards.",
        "args": {
            "operation": "create|read|update",
            "name": "string, required for create/update",
            "dashboard_id": "string, optional",
            "activate": "boolean, optional for create",
        },
    },
    "manage_navigation_bar": {
        "description": "Create, add, remove, or rename dashboard tabs.",
        "args": {
            "operation": "create|add_tabs|remove_tabs|rename_tabs",
            "tabs": [{"name": "Tab Name"}],
            "rename_map": {"old-tab-id": "New Name"},
            "dashboard_id": "string, optional",
        },
    },
    "navigate_workspace": {
        "description": "Switch active dashboard or tab.",
        "args": {
            "operation": "dashboard|tab",
            "dashboard_id": "string, optional for tab, required for dashboard",
            "tab_id": "string, optional for dashboard, required for tab",
        },
    },
    "list_available_widgets": {
        "description": "List widgets for a backend origin such as Bench Equities.",
        "args": {"origin": "string, optional", "backend_id": "string, optional"},
    },
    "get_widget_schema": {
        "description": "Get schema for one listed widget.",
        "args": {"origin": "string", "widget_id": "string"},
    },
    "get_params_options": {
        "description": "Fetch options for a schema parameter that requires lookup.",
        "args": {
            "origin": "string",
            "widget_id": "string",
            "param_name": "string",
            "data_args": "object, optional",
        },
    },
    "get_widget_data": {
        "description": "Fetch fixture data for one widget.",
        "args": {
            "origin": "string",
            "widget_id": "string",
            "data_args": "object, optional",
        },
    },
    "create_widget": {
        "description": "Create a regular Workspace widget.",
        "args": {
            "origin": "string",
            "widget_id": "string",
            "data_args": "object, optional",
            "ui_args": "object, optional",
            "dashboard_id": "string, optional",
        },
    },
    "update_widget": {
        "description": "Update widget data_args or ui_args. Do not use for layout.",
        "args": {
            "widget_uuid": "string, preferred when known",
            "widget_id": "string, only when exactly one exists",
            "data_args": "object, optional",
            "ui_args": "object, optional",
            "dashboard_id": "string, optional",
        },
    },
    "update_widget_layout": {
        "description": "Move or resize one widget.",
        "args": {
            "widget_uuid": "string, preferred when known",
            "widget_id": "string, only when exactly one exists",
            "x": "number",
            "y": "number",
            "w": "number",
            "h": "number",
            "tab_id": "string, optional",
            "dashboard_id": "string, optional",
        },
    },
    "delete_widget": {
        "description": "Delete one widget.",
        "args": {
            "widget_uuid": "string, preferred when known",
            "widget_id": "string, only when exactly one exists",
            "dashboard_id": "string, optional",
        },
    },
    "add_generative_widget": {
        "description": "Add generated note, table, chart, or HTML widget.",
        "args": {
            "widget_type": "note|table|chart|html",
            "name": "string, optional",
            "data": "string for note/html; array for table/chart",
            "description": "string, optional",
            "chart_params": "object with chartType, xKey, yKey for chart",
            "inner_tab": "string tab id, optional",
            "dashboard_id": "string, optional",
        },
    },
    "read_widget": {
        "description": "Read one existing widget.",
        "args": {
            "widget_uuid": "string, preferred when known",
            "widget_id": "string, only when exactly one exists",
            "dashboard_id": "string, optional",
        },
    },
    "manage_backends": {
        "description": "List, add, or refresh fixture backends.",
        "args": {
            "operation": "list|add|refresh",
            "name": "string, required for add",
            "backend_id": "string, optional",
            "url": "string, optional",
        },
    },
    "manage_apps": {
        "description": "List, read, or instantiate app templates from a backend.",
        "args": {
            "operation": "list|read|instantiate",
            "backend_id": "string",
            "app_name": "string, optional",
            "template_id": "string, optional",
            "dashboard_name": "string, optional for instantiate",
            "activate": "boolean, optional",
        },
    },
}


def main() -> int:
    try:
        task_path = Path(os.environ["WORKSPACE_BENCH_TASK_JSON"])
        output_path = Path(os.environ["WORKSPACE_BENCH_OUTPUT_JSONL"])
    except KeyError as error:
        print(f"Missing required env var: {error.args[0]}", file=sys.stderr)
        return 2

    run_dir = Path(os.environ.get("WORKSPACE_BENCH_RUN_DIR", output_path.parent))
    task = json.loads(task_path.read_text(encoding="utf-8"))
    prompt = build_prompt(task)
    write_debug_file(run_dir / "ollama_prompt.txt", prompt)

    try:
        content = call_ollama(prompt)
        write_debug_file(run_dir / "ollama_response.txt", content)
        calls = extract_tool_calls(content)
        calls = normalize_tool_calls(calls, allowed_tools=task["task"]["allowed_tools"])
    except Exception as error:  # noqa: BLE001 - adapter should fail visibly.
        print(f"Ollama agent failed: {error}", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "".join(json.dumps(call, sort_keys=True) + "\n" for call in calls),
        encoding="utf-8",
    )
    return 0


def build_prompt(task: dict[str, Any]) -> str:
    task = task["task"]
    allowed_tools = task["allowed_tools"]
    origin_hints = fixture_origin_hints(task["fixtures"])
    widget_hints = fixture_widget_hints(origin_hints)
    tool_reference = {
        name: TOOL_REFERENCE[name]
        for name in allowed_tools
        if name in TOOL_REFERENCE
    }

    public_task = {
        "id": task["id"],
        "title": task["title"],
        "level": task["level"],
        "capability": task["capability"],
        "workflow": task["workflow"],
        "domain": task["domain"],
        "subdomain": task["subdomain"],
        "difficulty": task["difficulty"],
        "prompt": task["prompt"],
        "fixtures": task["fixtures"],
        "origin_hints": origin_hints,
        "widget_hints": widget_hints,
        "initial_state": task["initial_state"],
        "allowed_tools": allowed_tools,
        "limits": task.get("limits", {}),
    }

    return "\n".join(
        [
            "You are controlling OpenBB Workspace through tool calls.",
            "Return only valid JSON. Do not use Markdown.",
            "",
            "This runner is non-interactive. You will not receive observations after each call.",
            "You must emit the complete tool-call plan now.",
            "",
            "Your output must be a JSON object with this shape:",
            '{"tool_calls": [{"tool": "tool_name", "args": {}}]}',
            "",
            "Do not return only one inspection call unless the task can be solved with one call.",
            "Use only allowed tools.",
            "When a tool asks for origin, use the display origin from origin_hints, not the fixture slug.",
            "Every create_widget call must include origin and widget_id at the top level of args.",
            "Every get_widget_schema call must include origin and widget_id at the top level of args.",
            "Use widget_hints for exact data_args keys. Do not invent alternative parameter names.",
            "If create_widget is allowed, first call list_available_widgets for the same origin.",
            "If create_widget and get_widget_schema are both allowed, you must call get_widget_schema before create_widget or the run fails.",
            "For single-widget creation tasks, use this sequence when the tools are allowed: get_workspace_snapshot, list_available_widgets, get_widget_schema, get_params_options if useful, create_widget.",
            "For layout changes, use update_widget_layout, not update_widget.",
            "",
            "Available tool reference:",
            json.dumps(tool_reference, indent=2, sort_keys=True),
            "",
            "Task:",
            json.dumps(public_task, indent=2, sort_keys=True),
        ]
    )


def fixture_origin_hints(fixtures: dict[str, Any]) -> dict[str, str]:
    hints = {}
    for backend in fixtures.get("backends", []):
        if not isinstance(backend, dict):
            continue
        name = backend.get("name")
        if isinstance(name, str):
            hints[name] = FIXTURE_ORIGINS.get(name, name)
    return hints


def fixture_widget_hints(origin_hints: dict[str, str]) -> dict[str, Any]:
    return {
        origin: WIDGET_HINTS[origin]
        for origin in origin_hints.values()
        if origin in WIDGET_HINTS
    }


def call_ollama(prompt: str) -> str:
    base_url = os.environ.get("OLLAMA_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    model = os.environ.get("OLLAMA_MODEL", DEFAULT_MODEL)
    timeout = float(os.environ.get("OLLAMA_TIMEOUT", "120"))
    temperature = float(os.environ.get("OLLAMA_TEMPERATURE", "0"))

    payload = {
        "model": model,
        "stream": False,
        "format": tool_call_response_schema(),
        "options": {"temperature": temperature},
        "messages": [
            {
                "role": "system",
                "content": (
                    "You produce only JSON objects containing tool_calls for an eval harness. "
                    "Never include prose."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url}/api/chat",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as error:
        raise RuntimeError(
            f"could not reach Ollama at {base_url}. Is `ollama serve` running?"
        ) from error

    content = (body.get("message") or {}).get("content")
    if not isinstance(content, str) or not content.strip():
        raise ValueError(f"Ollama returned no message content: {body!r}")
    return content


def extract_tool_calls(content: str) -> list[dict[str, Any]]:
    text = strip_code_fence(content.strip())
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = json.loads(extract_first_json_block(text))

    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        if "tool" in payload or "name" in payload:
            return [payload]
        for key in ("tool_calls", "calls", "actions"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    raise ValueError("model output must be a JSON array or object with tool_calls")


def tool_call_response_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "tool_calls": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "tool": {"type": "string"},
                        "args": {"type": "object"},
                    },
                    "required": ["tool", "args"],
                },
            }
        },
        "required": ["tool_calls"],
    }


def normalize_tool_calls(
    calls: list[dict[str, Any]], *, allowed_tools: list[str]
) -> list[dict[str, Any]]:
    normalized = []
    allowed = set(allowed_tools)
    for index, call in enumerate(calls, start=1):
        if not isinstance(call, dict):
            raise ValueError(f"tool call {index} must be an object")
        tool = call.get("tool") or call.get("name")
        args = call.get("args", {})
        if not isinstance(tool, str) or not tool:
            raise ValueError(f"tool call {index} is missing tool/name")
        if allowed and tool not in allowed:
            raise ValueError(f"tool call {index} used disallowed tool {tool!r}")
        if not isinstance(args, dict):
            raise ValueError(f"tool call {index} args must be an object")
        normalized.append({"tool": tool, "args": args})
    return normalized


def strip_code_fence(text: str) -> str:
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL)
    return fence.group(1).strip() if fence else text


def extract_first_json_block(text: str) -> str:
    start = min(
        [index for index in (text.find("["), text.find("{")) if index != -1],
        default=-1,
    )
    if start == -1:
        raise ValueError("no JSON object or array found in model output")

    opening = text[start]
    closing = "]" if opening == "[" else "}"
    depth = 0
    in_string = False
    escape = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError("unterminated JSON object or array in model output")


def write_debug_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
