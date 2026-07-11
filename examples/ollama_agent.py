"""Ollama-backed Workspace Bench agent adapter.

This is a template for running a local open-weight model against
``workspace-bench run-agent-command``. It uses Ollama's local HTTP API and
expects the model to emit a JSON object with a ``tool_calls`` array.

The tool reference and fixture hints are imported from the packaged
``workspace_bench.agents.model_adapter_helpers`` so this example never
drifts from what the interactive harness shows models.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from workspace_bench.agents.model_adapter_helpers import (
    TOOL_REFERENCE,
    fixture_origin_hints,
    fixture_widget_hints,
    strip_code_fence,
)


DEFAULT_MODEL = "gpt-oss:20b"
DEFAULT_BASE_URL = "http://127.0.0.1:11434"


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
