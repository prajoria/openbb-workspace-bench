"""Tiny JSONL agent used for Workspace Bench quick starts."""

from __future__ import annotations

import json
import os
from pathlib import Path


def main() -> int:
    task_path = Path(os.environ["WORKSPACE_BENCH_TASK_JSON"])
    output_path = Path(os.environ["WORKSPACE_BENCH_OUTPUT_JSONL"])
    task = json.loads(task_path.read_text(encoding="utf-8"))
    task_id = task["task"]["id"]

    calls = []
    if task_id == "price_performance_aapl":
        calls = [
            {"tool": "get_workspace_snapshot", "args": {}},
            {
                "tool": "create_widget",
                "args": {
                    "origin": "Bench Equities",
                    "widget_id": "price_performance",
                    "data_args": {"symbol": "AAPL"},
                },
            },
        ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "".join(json.dumps(call, sort_keys=True) + "\n" for call in calls),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
