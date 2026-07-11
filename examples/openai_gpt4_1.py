"""GPT-4.1 Workspace Bench agent adapter.

This template runs the OpenAI API ``gpt-4.1`` model against
``workspace-bench run-agent-command``. It reads ``OPENAI_API_KEY`` from the
environment first, then from a local ``.env`` file, and writes JSONL tool calls
for the harness.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from ollama_agent import (
    build_prompt,
    extract_tool_calls,
    normalize_tool_calls,
    write_debug_file,
)


MODEL = "gpt-4.1"
DEFAULT_BASE_URL = "https://api.openai.com/v1"


def main() -> int:
    try:
        task_path = Path(os.environ["WORKSPACE_BENCH_TASK_JSON"])
        output_path = Path(os.environ["WORKSPACE_BENCH_OUTPUT_JSONL"])
    except KeyError as error:
        print(f"Missing required env var: {error.args[0]}", file=sys.stderr)
        return 2

    load_dotenv()
    run_dir = Path(os.environ.get("WORKSPACE_BENCH_RUN_DIR", output_path.parent))
    task = json.loads(task_path.read_text(encoding="utf-8"))
    prompt = build_prompt(task)
    write_debug_file(run_dir / "openai_prompt.txt", prompt)

    try:
        content = call_openai(prompt)
        write_debug_file(run_dir / "openai_response.txt", content)
        calls = extract_tool_calls(content)
        calls = normalize_tool_calls(calls, allowed_tools=task["task"]["allowed_tools"])
    except Exception as error:  # noqa: BLE001 - adapter should fail visibly.
        print(f"OpenAI agent failed: {error}", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "".join(json.dumps(call, sort_keys=True) + "\n" for call in calls),
        encoding="utf-8",
    )
    return 0


def load_dotenv() -> None:
    env_path = Path(os.environ.get("OPENAI_ENV_FILE", ".env"))
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = strip_env_value(value.strip())
        os.environ.setdefault(key, value)


def strip_env_value(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def call_openai(prompt: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in the environment or .env")

    base_url = os.environ.get("OPENAI_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    timeout = float(os.environ.get("OPENAI_TIMEOUT", "120"))
    temperature = float(os.environ.get("OPENAI_TEMPERATURE", "0"))

    payload = {
        "model": MODEL,
        "temperature": temperature,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "workspace_tool_call_plan",
                "schema": tool_call_plan_schema(),
                "strict": False,
            },
        },
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
        f"{base_url}/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API request failed: HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"could not reach OpenAI API at {base_url}") from error

    try:
        content = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise ValueError(f"OpenAI returned no message content: {body!r}") from error
    if not isinstance(content, str) or not content.strip():
        raise ValueError(f"OpenAI returned empty message content: {body!r}")
    return content


def tool_call_plan_schema() -> dict[str, Any]:
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
                    "additionalProperties": False,
                },
            }
        },
        "required": ["tool_calls"],
        "additionalProperties": False,
    }


if __name__ == "__main__":
    raise SystemExit(main())
