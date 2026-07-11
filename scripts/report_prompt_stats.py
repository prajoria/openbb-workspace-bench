"""Report prompt-diversity statistics for the bundled suites.

Generated benchmarks trade lexical diversity for certification: every prompt
is rendered from a template site with at least three semantically identical
phrasings, selected by a stable task-id hash. This script quantifies what
that yields on the shipped JSON, for the benchmark card and for anyone
evaluating template-ness.

Usage:
    uv run python scripts/report_prompt_stats.py [--json]
"""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SUITES = {
    "core": REPO / "src/workspace_bench/core/task_suites/workspace_bench_v1",
    "build-openbb-apps": (
        REPO / "src/workspace_bench/core/task_suites/workspace_bench_v2_build_openbb_apps"
    ),
}


def suite_stats(suite_dir: Path) -> dict:
    prompts: list[str] = []
    for path in sorted(suite_dir.glob("*.json")):
        if path.name == "task_suite.json":
            continue
        prompts.append(json.loads(path.read_text())["prompt"])
    word_counts = [len(prompt.split()) for prompt in prompts]
    duplicates = [
        prompt for prompt, count in Counter(prompts).items() if count > 1
    ]
    return {
        "tasks": len(prompts),
        "distinct_prompts": len(set(prompts)),
        "duplicate_prompt_count": len(duplicates),
        "prompt_words_min": min(word_counts),
        "prompt_words_median": int(statistics.median(word_counts)),
        "prompt_words_max": max(word_counts),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    report = {name: suite_stats(path) for name, path in SUITES.items()}
    if args.json:
        print(json.dumps(report, indent=2))
        return 0
    for name, stats in report.items():
        print(
            f"{name}: {stats['distinct_prompts']}/{stats['tasks']} distinct prompts; "
            f"words min/median/max {stats['prompt_words_min']}/"
            f"{stats['prompt_words_median']}/{stats['prompt_words_max']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
