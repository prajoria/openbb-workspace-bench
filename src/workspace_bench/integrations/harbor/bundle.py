"""Sealed task-bundle loading shared by the Harbor runtime and verifier."""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path
from typing import Any

from workspace_bench.core.models import JsonDict, Task, TaskSuiteManifest


BUNDLE_SCHEMA_VERSION = "workspace-bench-harbor-bundle/v1"


def canonical_json_bytes(payload: object) -> bytes:
    """Serialize JSON deterministically for bundle identity checks."""

    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()


def bundle_sha256(payload: object) -> str:
    """Return the deterministic digest for a JSON-compatible payload."""

    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def load_bundle(path: Path) -> JsonDict:
    """Load and minimally validate one sealed Harbor bundle."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("sealed task bundle must contain a JSON object")
    if payload.get("schema_version") != BUNDLE_SCHEMA_VERSION:
        raise ValueError(
            "unsupported sealed task bundle schema: "
            f"{payload.get('schema_version')!r}"
        )
    if not isinstance(payload.get("task"), dict):
        raise ValueError("sealed task bundle is missing task")
    if not isinstance(payload.get("suite"), dict):
        raise ValueError("sealed task bundle is missing suite")
    return payload


def load_sealed_task(path: Path) -> tuple[Task, JsonDict]:
    """Reconstruct the canonical Task and return it with bundle metadata."""

    bundle = load_bundle(path)
    suite = TaskSuiteManifest.from_dict(bundle["suite"])
    task_payload: dict[str, Any] = dict(bundle["task"])

    defaults = dict(suite.task_defaults or {})
    eval_defaults = defaults.pop("eval", None)
    task_payload = {**defaults, **task_payload}
    if eval_defaults and isinstance(task_payload.get("eval"), dict):
        task_payload["eval"] = {**eval_defaults, **task_payload["eval"]}
    task_payload.setdefault("family", bundle.get("family"))

    task = replace(Task.from_dict(task_payload), suite=suite)
    expected_id = bundle.get("qualified_id")
    if expected_id and task.qualified_id != expected_id:
        raise ValueError(
            f"sealed task identity mismatch: expected {expected_id!r}, "
            f"loaded {task.qualified_id!r}"
        )
    metadata = dict(bundle.get("provenance") or {})
    metadata.update(
        {
            "qualified_id": task.qualified_id,
            "suite_content_sha256": suite.content_sha256,
            "bundle_sha256": bundle_sha256(bundle),
        }
    )
    return task, metadata

