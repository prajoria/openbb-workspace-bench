"""Metadata helpers for exported benchmark datasets."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from typing import Iterable

from workspace_bench.exports.schema import ROLLOUT_SCHEMA_VERSION, RolloutRecord
from workspace_bench.core.models import (
    BENCHMARK_NAME,
    BENCHMARK_RELEASE_ID,
    BENCHMARK_VERSION,
    JsonDict,
    TaskPackManifest,
)


def base_export_metadata(*, exported_at: str | None = None) -> JsonDict:
    """Metadata that should travel with every training/eval export record."""

    return {
        "benchmark_name": BENCHMARK_NAME,
        "benchmark_version": BENCHMARK_VERSION,
        "benchmark_release_id": BENCHMARK_RELEASE_ID,
        "export_schema_version": ROLLOUT_SCHEMA_VERSION,
        "exported_at": exported_at or _utc_now(),
    }


def annotate_rollouts(
    records: Iterable[RolloutRecord],
    *,
    task_pack: TaskPackManifest | None = None,
    exported_at: str | None = None,
) -> list[RolloutRecord]:
    """Return rollout records with benchmark and task-pack metadata attached."""

    timestamp = exported_at or _utc_now()
    annotated = []
    for record in records:
        metadata = dict(record.metadata)
        metadata.update(base_export_metadata(exported_at=timestamp))
        if task_pack is not None:
            metadata["task_pack"] = {
                "pack_id": task_pack.pack_id,
                "release_id": task_pack.release_id,
                "version": task_pack.version,
                "visibility": task_pack.visibility,
                "default_split": task_pack.default_split,
            }
        annotated.append(replace(record, metadata=metadata))
    return annotated


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
