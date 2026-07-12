"""Read-only surface audit of the hosted OpenBB Workspace MCP.

Connects to the hosted MCP endpoint with a bearer token, lists tools,
prompts, and resources, and diffs them against the surface that
workspace-bench tasks assume. No tool calls are made; nothing is
mutated.

Usage:

    uv run --extra live python scripts/audit_hosted_surface.py

Reads ``WORKSPACE_MCP_TOKEN`` from the environment first, then from a local
``.env`` file. Override the endpoint with ``WORKSPACE_MCP_URL``. Exits
non-zero when an expected tool, prompt, or resource is missing from the
hosted deployment; additions are reported but do not fail the audit.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

from workspace_bench.workspace.live_mcp import (
    EXPECTED_MCP_PROMPTS,
    EXPECTED_MCP_RESOURCES,
    EXPECTED_MCP_TOOLS,
)
from workspace_bench.workspace.surface_audit import compare_tool_schemas


DEFAULT_URL = "https://backend.openbb.dev/mcp"
TOKEN_KEYS = ("WORKSPACE_MCP_TOKEN", "OPENBB_MCP_TOKEN")
DEFAULT_SCHEMA_BASELINE = Path("runs/hosted-surface/tool_schemas.json")


def main() -> int:
    token = load_token()
    if not token:
        keys = " or ".join(TOKEN_KEYS)
        print(f"Missing {keys} in the environment or .env", file=sys.stderr)
        return 2
    url = os.environ.get("WORKSPACE_MCP_URL", DEFAULT_URL)
    try:
        surface = asyncio.run(fetch_surface(url, token))
    except Exception as error:  # noqa: BLE001 - audit should fail visibly.
        print(f"Could not audit {url}: {error}", file=sys.stderr)
        return 2
    return report(url, surface)


def load_token() -> str | None:
    for key in TOKEN_KEYS:
        if os.environ.get(key):
            return os.environ[key]
    env_path = Path(os.environ.get("WORKSPACE_MCP_ENV_FILE", ".env"))
    if not env_path.exists():
        return None
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip().removeprefix("export ").strip()
        if "=" not in line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        if key.strip() in TOKEN_KEYS:
            return value.strip().strip("'\"")
    return None


async def fetch_surface(url: str, token: str) -> dict[str, object]:
    try:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client
    except ImportError as error:
        raise RuntimeError(
            "The hosted surface audit requires optional dependencies. "
            "Run with `uv run --extra live python scripts/audit_hosted_surface.py`."
        ) from error

    headers = {"Authorization": f"Bearer {token}"}
    async with streamablehttp_client(url, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            tools = (await session.list_tools()).tools
            prompts = (await session.list_prompts()).prompts
            resources = (await session.list_resources()).resources
    return {
        "server": f"{init.serverInfo.name} v{init.serverInfo.version}",
        "instructions": init.instructions or "",
        "tools": {tool.name: tool.inputSchema for tool in tools},
        "prompts": {prompt.name for prompt in prompts},
        "resources": {str(resource.uri) for resource in resources},
    }


def report(url: str, surface: dict[str, object]) -> int:
    tools = surface["tools"]
    assert isinstance(tools, dict)
    observed = {
        "tool": set(tools),
        "prompt": surface["prompts"],
        "resource": surface["resources"],
    }
    expected = {
        "tool": EXPECTED_MCP_TOOLS,
        "prompt": EXPECTED_MCP_PROMPTS,
        "resource": EXPECTED_MCP_RESOURCES,
    }
    baseline_path = Path(
        os.environ.get("WORKSPACE_MCP_SCHEMA_BASELINE", str(DEFAULT_SCHEMA_BASELINE))
    )
    if not baseline_path.exists():
        print(f"Missing tool-schema baseline: {baseline_path}", file=sys.stderr)
        return 2
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    if not isinstance(baseline, dict):
        print(f"Invalid tool-schema baseline: {baseline_path}", file=sys.stderr)
        return 2

    print(f"Audited {surface['server']} at {url}")
    failed = False
    for label in ("tool", "prompt", "resource"):
        observed_names = observed[label]
        assert isinstance(observed_names, set)
        missing = sorted(expected[label] - observed_names)
        added = sorted(observed_names - expected[label])
        print(f"{label}s: {len(observed_names)} observed", end="")
        if missing:
            failed = True
            print(f", MISSING {len(missing)}: {', '.join(missing)}", end="")
        if added:
            print(f", new (informational): {', '.join(added)}", end="")
        print()

    schema_issues = compare_tool_schemas(baseline, tools)
    if schema_issues:
        failed = True
        print(f"tool schema compatibility: FAIL ({len(schema_issues)} issue(s))")
        for issue in schema_issues[:30]:
            print(f"  - {issue}")
    else:
        print("tool schema compatibility: OK")

    run_dir = Path("runs/hosted-surface")
    run_dir.mkdir(parents=True, exist_ok=True)
    schema_path = run_dir / "latest_tool_schemas.json"
    schema_path.write_text(json.dumps(tools, indent=2, sort_keys=True), encoding="utf-8")
    instructions_path = run_dir / "instructions.txt"
    instructions_path.write_text(str(surface["instructions"]), encoding="utf-8")
    print(f"Wrote {schema_path} and {instructions_path}")

    if failed:
        print("FAIL: hosted surface is missing expected entries.", file=sys.stderr)
        return 1
    print("OK: hosted surface covers everything the tasks assume.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
