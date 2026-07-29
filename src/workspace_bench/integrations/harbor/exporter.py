"""Materialize canonical Workspace Bench tasks as self-contained Harbor tasks."""

from __future__ import annotations

import hashlib
import json
import shutil
import stat
import subprocess
import tarfile
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Any

from workspace_bench.agents import OracleAgent
from workspace_bench.core.models import Task
from workspace_bench.core.runner import find_task
from workspace_bench.integrations.harbor.bundle import BUNDLE_SCHEMA_VERSION


HARBOR_VERSION = "0.20.0"
REFERENCE_TASK = (
    "enterprise-apps-default/compliance_surveillance_hub/"
    "compliance_surveillance_hub_p3_x"
)
DEFAULT_WORKSPACE_MCP_REPO = Path.home() / "Documents/git/workspace-mcp"


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _git_provenance(repo: Path) -> dict[str, Any]:
    return {
        "git_commit": _git(repo, "rev-parse", "HEAD"),
        "source_dirty": bool(_git(repo, "status", "--porcelain")),
    }


def _workspace_bench_source_sha256(repo: Path) -> str:
    """Hash the exact package inputs copied into generated Docker contexts."""

    digest = hashlib.sha256()
    candidates = [repo / "pyproject.toml", *(repo / "src").rglob("*")]
    for path in sorted(
        (candidate for candidate in candidates if candidate.is_file()),
        key=lambda candidate: candidate.relative_to(repo).as_posix(),
    ):
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        relative = path.relative_to(repo).as_posix().encode()
        digest.update(relative)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _write(path: Path, content: str, *, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if executable:
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def _write_json(path: Path, payload: object) -> None:
    _write(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _copy_workspace_bench_source(repo: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for filename in ("pyproject.toml", "README.md", "LICENSE"):
        shutil.copy2(repo / filename, destination / filename)
    shutil.copytree(
        repo / "src",
        destination / "src",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )


def _safe_extract_tar(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive) as handle:
        root = destination.resolve()
        for member in handle.getmembers():
            target = (destination / member.name).resolve()
            if target != root and root not in target.parents:
                raise ValueError(f"git archive contains unsafe path: {member.name}")
        handle.extractall(destination)


def _archive_workspace_mcp(repo: Path, commit: str, destination: Path) -> None:
    with tempfile.NamedTemporaryFile(suffix=".tar") as temporary:
        subprocess.run(
            [
                "git",
                "-C",
                str(repo),
                "archive",
                "--format=tar",
                "-o",
                temporary.name,
                commit,
                "pyproject.toml",
                "README.md",
                "workspace_mcp",
            ],
            check=True,
        )
        _safe_extract_tar(Path(temporary.name), destination)


def _source_payload(task: Task) -> dict[str, Any]:
    if task.source_path is None:
        raise ValueError("Harbor export requires a task with a canonical source file")
    payload = json.loads(task.source_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"task source is not an object: {task.source_path}")
    return payload


def _bundle(task: Task, bench_repo: Path, workspace_mcp_repo: Path) -> dict[str, Any]:
    if task.suite is None:
        raise ValueError("Harbor export requires a task-suite manifest")
    bench = _git_provenance(bench_repo)
    sidecar = _git_provenance(workspace_mcp_repo)
    return {
        "schema_version": BUNDLE_SCHEMA_VERSION,
        "qualified_id": task.qualified_id,
        "family": task.family,
        "task": _source_payload(task),
        "suite": asdict(task.suite),
        "provenance": {
            "workspace_bench_git_commit": bench["git_commit"],
            "workspace_bench_source_dirty": bench["source_dirty"],
            "workspace_bench_source_mode": "working-tree-package-copy",
            "workspace_bench_source_sha256": _workspace_bench_source_sha256(
                bench_repo
            ),
            "workspace_mcp_git_commit": sidecar["git_commit"],
            "workspace_mcp_source_dirty": sidecar["source_dirty"],
            "workspace_mcp_source_mode": "git-archive",
            "harbor_version": HARBOR_VERSION,
            "adapter_schema": "workspace-bench-harbor/v1",
        },
    }


def _task_toml(task: Task) -> str:
    assert task.suite is not None
    safe_name = "--".join((task.suite.suite_id, task.family, task.id)).replace("_", "-")
    return f'''schema_version = "1.3"

artifacts = [
  {{ source = "/var/lib/workspace-bench/episode.json", service = "workspace-runtime" }},
]

[task]
name = "openbb/{safe_name}"
description = "Generated OpenBB Workspace Bench task for Harbor."
authors = [{{ name = "OpenBB Workspace Bench contributors" }}]
keywords = ["openbb", "workspace", "mcp", "benchmark", "{task.suite.suite_id}"]

[metadata]
benchmark = "openbb-workspace-bench"
suite = "{task.suite.suite_id}"
family = "{task.family}"
task_id = "{task.id}"
qualified_id = "{task.qualified_id}"
category = "{task.category}"
difficulty = "{task.difficulty}"
specification_level = "{task.specification_level}"
suite_content_sha256 = "{task.suite.content_sha256 or ''}"
adapter_schema = "workspace-bench-harbor/v1"
track = "harbor-native"
harbor_version = "{HARBOR_VERSION}"

[agent]
timeout_sec = 900.0

[verifier]
timeout_sec = 300.0
environment_mode = "separate"

[[verifier.collect]]
service = "workspace-runtime"
command = "python -m workspace_bench.integrations.harbor.runtime finalize --timeout 30"
timeout_sec = 45.0

[verifier.environment]
cpus = 1
memory_mb = 2048
storage_mb = 4096

[environment]
network_mode = "public"
build_timeout_sec = 1200.0
cpus = 2
memory_mb = 4096
storage_mb = 10240

[[environment.mcp_servers]]
name = "openbb-workspace"
transport = "streamable-http"
url = "http://workspace-runtime:8790/mcp"
'''


def _compose(task: Task) -> str:
    image = f"workspace-bench-harbor-{task.id.replace('_', '-')}"
    return f'''services:
  main:
    depends_on:
      workspace-runtime:
        condition: service_healthy
    networks:
      - agent

  workspace-mcp:
    image: {image}:runtime
    build:
      context: ./runtime
    command:
      - workspace-mcp
      - --host
      - 0.0.0.0
      - --port
      - "8787"
      - --mcp-path
      - /mcp
      - --command-timeout-seconds
      - "30"
    expose:
      - "8787"
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8787/health', timeout=2)"]
      interval: 2s
      timeout: 5s
      retries: 30
      start_period: 5s
    networks:
      - trusted

  workspace-runtime:
    image: {image}:runtime
    build:
      context: ./runtime
    command:
      - python
      - -m
      - workspace_bench.integrations.harbor.runtime
      - serve
      - --task
      - /opt/workspace-bench-task/sealed-task.json
      - --artifact
      - /var/lib/workspace-bench/episode.json
    depends_on:
      workspace-mcp:
        condition: service_healthy
    expose:
      - "8790"
    healthcheck:
      test: ["CMD", "python", "-c", "import pathlib,socket; assert pathlib.Path('/run/workspace-bench/ready').is_file(); s=socket.create_connection(('127.0.0.1',8790),2); s.close()"]
      interval: 2s
      timeout: 5s
      retries: 30
      start_period: 5s
    networks:
      - agent
      - trusted

networks:
  agent: {{}}
  trusted:
    internal: true
'''


RUNTIME_DOCKERFILE = '''FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1

COPY vendor/rl-workspace /opt/rl-workspace
COPY vendor/workspace-mcp /opt/workspace-mcp
RUN pip install --no-cache-dir "/opt/rl-workspace[live]" /opt/workspace-mcp

COPY sealed-task.json /opt/workspace-bench-task/sealed-task.json
WORKDIR /opt/workspace-bench-task
'''


MAIN_DOCKERFILE = '''FROM python:3.13-slim

RUN pip install --no-cache-dir "mcp>=1.27.0"
WORKDIR /app
'''


VERIFIER_DOCKERFILE = '''FROM python:3.13-slim

COPY vendor/rl-workspace /opt/rl-workspace
RUN pip install --no-cache-dir /opt/rl-workspace
COPY sealed-task.json /tests/sealed-task.json
COPY test.sh /tests/test.sh
RUN chmod +x /tests/test.sh
WORKDIR /tests
'''


TEST_SH = '''#!/bin/sh
set -eu

python -m workspace_bench.integrations.harbor.verifier \\
  --task /tests/sealed-task.json \\
  --episode /var/lib/workspace-bench/episode.json \\
  --output /logs/verifier
'''


REPLAY_PY = '''from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def replay(url: str, calls_path: Path) -> None:
    calls = json.loads(calls_path.read_text(encoding="utf-8"))
    async with streamablehttp_client(url) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            for call in calls:
                await session.call_tool(call["name"], call.get("args") or {})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://workspace-runtime:8790/mcp")
    parser.add_argument("--calls", type=Path, default=Path("/solution/oracle.json"))
    args = parser.parse_args()
    asyncio.run(replay(args.url, args.calls))


if __name__ == "__main__":
    main()
'''


SOLVE_SH = '''#!/bin/sh
set -eu
python /solution/replay.py --calls /solution/oracle.json
'''


def _instruction(task: Task) -> str:
    max_turns = int(task.limits.get("max_turns", 12))
    return f'''Use the OpenBB Workspace MCP tools to complete this task:

{task.prompt}

When the work is complete, submit the response with the `final_answer` MCP
tool. Returning prose without calling `final_answer` does not complete the
episode.

This episode permits at most {max_turns} MCP tool calls in total, and the
`final_answer` submission counts as one of those calls. Reserve one call for
`final_answer`; calls made after the budget is exhausted are rejected.
'''


def _assert_public_files_are_sealed(task: Task, destination: Path) -> None:
    public_text = "\n".join(
        (destination / relative).read_text(encoding="utf-8")
        for relative in ("instruction.md", "task.toml", "environment/Dockerfile")
    )
    leaks = ["reference_trace", "reference_answer", '"eval"']
    if task.reference_answer:
        leaks.append(task.reference_answer)
    observed = [needle for needle in leaks if needle in public_text]
    if observed:
        raise RuntimeError(f"generated public Harbor files leak sealed data: {observed}")


def export_harbor_task(
    *,
    task_ref: str = REFERENCE_TASK,
    output_root: Path = Path("build/harbor"),
    workspace_mcp_repo: Path = DEFAULT_WORKSPACE_MCP_REPO,
    overwrite: bool = False,
) -> Path:
    """Generate one self-contained Harbor task from a canonical bundled task."""

    task = find_task(task_ref)
    if task.suite is None:
        raise ValueError(f"task has no suite: {task_ref}")
    workspace_mcp_repo = workspace_mcp_repo.expanduser().resolve()
    if not (workspace_mcp_repo / "workspace_mcp").is_dir():
        raise FileNotFoundError(f"workspace-mcp repository not found: {workspace_mcp_repo}")
    bench_repo = Path(__file__).resolve().parents[4]
    destination = output_root / task.suite.suite_id / task.family / task.id
    if destination.exists():
        if not overwrite:
            raise FileExistsError(
                f"Harbor task already exists: {destination}; pass overwrite=True"
            )
        shutil.rmtree(destination)
    destination.mkdir(parents=True)

    bundle = _bundle(task, bench_repo, workspace_mcp_repo)
    _write(destination / "instruction.md", _instruction(task))
    _write(destination / "task.toml", _task_toml(task))
    _write(destination / "environment/Dockerfile", MAIN_DOCKERFILE)
    _write(destination / "environment/docker-compose.yaml", _compose(task))

    runtime = destination / "environment/runtime"
    _write(runtime / "Dockerfile", RUNTIME_DOCKERFILE)
    _write_json(runtime / "sealed-task.json", bundle)
    _copy_workspace_bench_source(bench_repo, runtime / "vendor/rl-workspace")
    sidecar_commit = bundle["provenance"]["workspace_mcp_git_commit"]
    _archive_workspace_mcp(
        workspace_mcp_repo,
        sidecar_commit,
        runtime / "vendor/workspace-mcp",
    )

    tests = destination / "tests"
    _write(tests / "Dockerfile", VERIFIER_DOCKERFILE)
    _write(tests / "test.sh", TEST_SH, executable=True)
    _write_json(tests / "sealed-task.json", bundle)
    _copy_workspace_bench_source(bench_repo, tests / "vendor/rl-workspace")

    oracle = [
        {"name": call.name, "args": call.args}
        for call in OracleAgent().tool_calls(task)
    ]
    _write(destination / "solution/solve.sh", SOLVE_SH, executable=True)
    _write(destination / "solution/replay.py", REPLAY_PY)
    _write_json(destination / "solution/oracle.json", oracle)

    _assert_public_files_are_sealed(task, destination)
    _write_json(
        destination / "adapter-manifest.json",
        {
            "schema_version": "workspace-bench-harbor-adapter-manifest/v1",
            "qualified_id": task.qualified_id,
            "harbor_version": HARBOR_VERSION,
            "workspace_mcp_commit": sidecar_commit,
            "workspace_mcp_source_dirty": bundle["provenance"][
                "workspace_mcp_source_dirty"
            ],
            "source_mode": "generated",
        },
    )
    return destination
