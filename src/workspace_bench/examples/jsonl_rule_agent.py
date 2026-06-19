"""Tiny JSONL agent used for Workspace Bench quick starts."""

from __future__ import annotations

import json
import os
from pathlib import Path


def main() -> int:
    task_path = Path(os.environ["WORKSPACE_BENCH_TASK_JSON"])
    output_path = Path(os.environ["WORKSPACE_BENCH_OUTPUT_JSONL"])
    task = json.loads(task_path.read_text(encoding="utf-8"))
    scenario_id = task["scenario"]["id"]

    calls = []
    if scenario_id == "l1_add_price_widget":
        calls = [
            {"tool": "get_workspace_snapshot", "args": {}},
            {"tool": "list_available_widgets", "args": {"origin": "Bench Equities"}},
            {
                "tool": "get_widget_schema",
                "args": {
                    "origin": "Bench Equities",
                    "widget_id": "price_performance",
                },
            },
            {
                "tool": "get_params_options",
                "args": {
                    "origin": "Bench Equities",
                    "widget_id": "price_performance",
                    "param_name": "symbol",
                },
            },
            {
                "tool": "create_widget",
                "args": {
                    "origin": "Bench Equities",
                    "widget_id": "price_performance",
                    "data_args": {"symbol": "AAPL"},
                },
            },
            {
                "tool": "update_widget_layout",
                "args": {
                    "widget_id": "price_performance",
                    "x": 0,
                    "y": 0,
                    "w": 20,
                    "h": 12,
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
