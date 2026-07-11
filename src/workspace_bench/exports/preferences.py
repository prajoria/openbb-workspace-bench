"""Preference dataset helpers for repeated benchmark attempts."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from workspace_bench.exports.jsonl import write_jsonl
from workspace_bench.exports.schema import PREFERENCE_SCHEMA_VERSION, RolloutRecord
from workspace_bench.core.models import JsonDict


def build_preference_pairs(records: Iterable[RolloutRecord]) -> list[JsonDict]:
    """Create best-vs-worst pairs from repeated attempts on the same task."""

    grouped: dict[tuple[str | None, str | None], list[RolloutRecord]] = {}
    for record in records:
        key = (
            record.metadata.get("model_slug") or record.metadata.get("runner"),
            record.metadata.get("task_id"),
        )
        grouped.setdefault(key, []).append(record)

    pairs = []
    for (model_slug, task_id), attempts in grouped.items():
        if len(attempts) < 2:
            continue
        ranked = sorted(attempts, key=_preference_rank)
        rejected = ranked[0]
        chosen = ranked[-1]
        if _preference_rank(chosen) == _preference_rank(rejected):
            continue
        pairs.append(
            {
                "schema_version": PREFERENCE_SCHEMA_VERSION,
                "task_id": task_id,
                "model_slug": model_slug,
                "chosen": chosen.to_dict(),
                "rejected": rejected.to_dict(),
                "metadata": {
                    "chosen_score": chosen.metadata.get("score"),
                    "rejected_score": rejected.metadata.get("score"),
                    "chosen_passed": chosen.metadata.get("passed"),
                    "rejected_passed": rejected.metadata.get("passed"),
                },
            }
        )
    return pairs


def write_preferences_jsonl(
    records: Iterable[RolloutRecord],
    output_path: Path,
) -> int:
    return write_jsonl(build_preference_pairs(records), output_path)


def _preference_rank(record: RolloutRecord) -> tuple[int, float]:
    return (
        1 if record.metadata.get("passed") else 0,
        float(record.metadata.get("score") or 0.0),
    )

