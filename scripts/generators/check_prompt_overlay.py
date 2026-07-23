"""Fast gate for authored prompts: apply the overlay, run the full battery.

Builds the suite records in memory, applies ``prompt_overlay.json`` (only
entries whose ``spec_sha256`` matches the freshly computed spec), and runs
``validate_payloads`` plus the level-contract report. Prints compact per-task
failures for the authoring loop. This is the inner loop; a full
``generate_usage_suite.py`` run (which also writes files and replays the
oracle/no-op certification) remains the final gate before committing.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_usage_suite as gen  # noqa: E402


def main() -> int:
    records = gen.build_tasks()
    specs = {
        str(record.payload["id"]): gen._compute_prompt_spec(record)
        for record in records
    }
    try:
        stats = gen._apply_prompt_overlay(records, specs)
    except AssertionError as err:
        print(f"FAIL: {err}")
        return 1
    total = len(records)
    print(
        f"overlay: {stats['applied']} applied, {stats['stale']} stale, "
        f"{stats['unknown']} unknown, {total - stats['applied']} still template"
    )
    if stats["unknown"]:
        print("note: unknown entries name tasks that no longer exist")
    try:
        gen.validate_payloads(records)
    except AssertionError as err:
        print(f"FAIL: {err}")
        return 1
    gen._report_level_contract(records)
    print("checker: assertion battery green")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
