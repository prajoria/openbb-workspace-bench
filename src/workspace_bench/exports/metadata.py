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
    TaskSuiteManifest,
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
    task_suite: TaskSuiteManifest | None = None,
    exported_at: str | None = None,
) -> list[RolloutRecord]:
    """Return rollout records with benchmark and task-pack metadata attached."""

    timestamp = exported_at or _utc_now()
    annotated = []
    for record in records:
        metadata = dict(record.metadata)
        metadata.update(base_export_metadata(exported_at=timestamp))
        if task_suite is not None:
            metadata["task_suite"] = {
                "suite_id": task_suite.suite_id,
                "release_id": task_suite.release_id,
                "version": task_suite.version,
                "visibility": task_suite.visibility,
                "default_split": task_suite.default_split,
            }
        annotated.append(replace(record, metadata=metadata))
    return annotated


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
