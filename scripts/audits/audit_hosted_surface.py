"""Read-only surface audit of the hosted OpenBB Workspace MCP.

Connects to the hosted MCP endpoint with a bearer token, lists tools,
prompts, and resources, and diffs them against the surface that
workspace-bench tasks assume. No tool calls are made; nothing is
mutated.

Usage:

    uv run --extra live python scripts/audits/audit_hosted_surface.py

Reads ``WORKSPACE_MCP_TOKEN`` from the environment first, then from a local
``.env`` file. Override the endpoint with ``WORKSPACE_MCP_URL``. Exits
non-zero when an expected tool, prompt, or resource is missing from the
hosted deployment or a tool schema changed incompatibly; additions are
reported but do not fail the audit.

The single source of truth is the committed baseline
``runs/hosted-surface/tool_schemas.json``. After reviewing a reported
compatible drift, promote the observed surface to be the new baseline with:

    uv run --extra live python scripts/audits/audit_hosted_surface.py --update-baseline
"""

from __future__ import annotations

import asyncio
import hashlib
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
DEFAULT_RESOURCE_BASELINE = Path("runs/hosted-surface/resource_catalog.json")


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    update_baseline = "--update-baseline" in args
    token = load_token()
    if not token:
        keys = " or ".join(TOKEN_KEYS)
        print(f"Missing {keys} in the environment or .env", file=sys.stderr)
        return 2
    url = os.environ.get("WORKSPACE_MCP_URL") or load_env_value(("WORKSPACE_MCP_URL",)) or DEFAULT_URL
    try:
        surface = asyncio.run(fetch_surface(url, token))
    except Exception as error:  # noqa: BLE001 - audit should fail visibly.
        print(f"Could not audit {url}: {error}", file=sys.stderr)
        return 2
    return report(url, surface, update_baseline=update_baseline)


def load_token() -> str | None:
    for key in TOKEN_KEYS:
        if os.environ.get(key):
            return os.environ[key]
    return load_env_value(TOKEN_KEYS)


def load_env_value(keys: tuple[str, ...]) -> str | None:
    env_path = Path(os.environ.get("WORKSPACE_MCP_ENV_FILE", ".env"))
    if not env_path.exists():
        return None
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip().removeprefix("export ").strip()
        if "=" not in line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        if key.strip() in keys:
            return value.strip().strip("'\"")
    return None


async def fetch_surface(url: str, token: str) -> dict[str, object]:
    try:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client
    except ImportError as error:
        raise RuntimeError(
            "The hosted surface audit requires optional dependencies. "
            "Run with `uv run --extra live python scripts/audits/audit_hosted_surface.py`."
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
        "resources": {
            str(resource.uri): {
                "uri": str(resource.uri),
                "name": str(resource.name),
                "description": str(resource.description or ""),
                "mime_type": str(resource.mimeType or ""),
            }
            for resource in resources
        },
    }


def report(url: str, surface: dict[str, object], *, update_baseline: bool = False) -> int:
    tools = surface["tools"]
    assert isinstance(tools, dict)
    resources = surface["resources"]
    assert isinstance(resources, dict)
    observed = {
        "tool": set(tools),
        "prompt": surface["prompts"],
        "resource": set(resources),
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
    resource_baseline_path = Path(
        os.environ.get(
            "WORKSPACE_MCP_RESOURCE_BASELINE", str(DEFAULT_RESOURCE_BASELINE)
        )
    )
    if not resource_baseline_path.exists():
        print(f"Missing resource-catalog baseline: {resource_baseline_path}", file=sys.stderr)
        return 2
    resource_baseline = json.loads(resource_baseline_path.read_text(encoding="utf-8"))
    expected_resource_hashes = {
        str(item["uri"]): str(item["catalog_sha256"])
        for item in resource_baseline.get("resources", [])
    }

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

    resource_drift = [
        uri
        for uri, expected_hash in expected_resource_hashes.items()
        if uri in resources and _resource_catalog_hash(resources[uri]) != expected_hash
    ]
    if resource_drift:
        failed = True
        print(
            "resource catalog compatibility: FAIL (descriptor changed: "
            + ", ".join(resource_drift)
            + ")"
        )
    else:
        print("resource catalog compatibility: OK")

    if update_baseline:
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        baseline_path.write_text(
            json.dumps(tools, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"Promoted observed surface to baseline: {baseline_path}")
        resource_baseline_path.write_text(
            json.dumps(
                {
                    "schema_version": "workspace-bench-live-resource-catalog/v1",
                    "server": str(surface["server"]),
                    "hash_contract": (
                        "sha256 of canonical JSON {description,mime_type,name,uri}"
                    ),
                    "resources": [
                        {
                            "uri": uri,
                            "catalog_sha256": _resource_catalog_hash(metadata),
                        }
                        for uri, metadata in sorted(resources.items())
                    ],
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"Promoted observed resource catalog: {resource_baseline_path}")

    if failed:
        print("FAIL: hosted surface is missing expected entries.", file=sys.stderr)
        return 1
    print("OK: hosted surface covers everything the tasks assume.")
    return 0


def _resource_catalog_hash(metadata: object) -> str:
    assert isinstance(metadata, dict)
    canonical = json.dumps(
        {
            key: str(metadata.get(key, ""))
            for key in ("description", "mime_type", "name", "uri")
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
