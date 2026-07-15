"""Report prompt-diversity statistics for the bundled suites.

Generated benchmarks trade lexical diversity for certification: every prompt
is rendered from a template site with at least three semantically identical
phrasings, selected by a stable task-id hash. This script quantifies what
that yields on the shipped JSON, for the benchmark card and for anyone
evaluating template-ness.

Usage:
    uv run python scripts/audits/report_prompt_stats.py [--json]
"""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SUITES = {
    "smoke": REPO / "src/workspace_bench/task_suites/smoke",
    "enterprise-apps-default": (
        REPO / "src/workspace_bench/task_suites/enterprise_apps_default"
    ),
    "enterprise-apps-usage": REPO / "src/workspace_bench/task_suites/enterprise_apps_usage",
    "build-openbb-apps": (REPO / "src/workspace_bench/task_suites/build_openbb_apps"),
}
EXPECTED_TASKS = {
    "smoke": 80,
    "enterprise-apps-default": 138,
    "enterprise-apps-usage": 336,
    "build-openbb-apps": 236,
}
# The smoke ladder repeats each family's declarative prompt across levels
# 0-2 on purpose (same instruction, different execution context) and adds
# one open prompt per family: 2 distinct prompts x 20 families.
EXPECTED_DISTINCT_PROMPTS = {
    "smoke": 40,
    "enterprise-apps-default": 69,
}
PROMPT_WORD_CAPS = {
    "smoke": 100,
    "enterprise-apps-default": 1_000,
    "enterprise-apps-usage": 350,
    "build-openbb-apps": 180,
}
BUILD_SPECIFICATION_LEVEL_COUNTS = {
    "explicit": 60,
    "partially-specified": 92,
    "open-brief": 84,
}
# Task files store specification_level only when it deviates from the
# difficulty default, so stats reconstruct the effective level.
DEFAULT_SPECIFICATION_LEVEL = {
    "easy": "explicit",
    "medium": "partially-specified",
    "hard": "open-brief",
}


def effective_specification_level(task: dict) -> str:
    return str(
        task.get("specification_level")
        or DEFAULT_SPECIFICATION_LEVEL.get(str(task.get("difficulty")), "")
    )
BUILD_DIFFICULTY_COUNTS = json.loads(
    (REPO / "src/workspace_bench/core/measured_difficulty.json").read_text()
)["bands"]


def suite_stats(suite_dir: Path) -> dict:
    tasks: list[dict] = []
    for path in sorted(suite_dir.rglob("*.json"), key=lambda item: item.name):
        # Suite-root JSON (manifest, reference answer corpora) is metadata.
        if path.parent == suite_dir:
            continue
        tasks.append(json.loads(path.read_text()))
    prompts = [str(task["prompt"]) for task in tasks]
    word_counts = [len(prompt.split()) for prompt in prompts]
    duplicates = [prompt for prompt, count in Counter(prompts).items() if count > 1]
    by_difficulty = {}
    for difficulty in ("easy", "medium", "hard"):
        counts = [
            len(str(task["prompt"]).split())
            for task in tasks
            if task.get("difficulty") == difficulty
        ]
        if counts:
            by_difficulty[difficulty] = {
                "tasks": len(counts),
                "prompt_words_min": min(counts),
                "prompt_words_median": int(statistics.median(counts)),
                "prompt_words_max": max(counts),
            }
    by_specification_level = {}
    for level in ("explicit", "partially-specified", "open-brief"):
        counts = [
            len(str(task["prompt"]).split())
            for task in tasks
            if effective_specification_level(task) == level
        ]
        if counts:
            by_specification_level[level] = {
                "tasks": len(counts),
                "prompt_words_min": min(counts),
                "prompt_words_median": int(statistics.median(counts)),
                "prompt_words_max": max(counts),
            }
    return {
        "tasks": len(prompts),
        "distinct_prompts": len(set(prompts)),
        "duplicate_prompt_count": len(duplicates),
        "prompt_words_min": min(word_counts),
        "prompt_words_median": int(statistics.median(word_counts)),
        "prompt_words_max": max(word_counts),
        "by_difficulty": by_difficulty,
        "by_specification_level": by_specification_level,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    report = {name: suite_stats(path) for name, path in SUITES.items()}
    passed = all(
        stats["tasks"] == EXPECTED_TASKS[name]
        and stats["distinct_prompts"]
        == EXPECTED_DISTINCT_PROMPTS.get(name, stats["tasks"])
        and stats["prompt_words_max"] <= PROMPT_WORD_CAPS[name]
        for name, stats in report.items()
    ) and all(
        report["build-openbb-apps"]["by_difficulty"][difficulty]["tasks"] == count
        for difficulty, count in BUILD_DIFFICULTY_COUNTS.items()
    ) and all(
        report["build-openbb-apps"]["by_specification_level"][level]["tasks"]
        == count
        for level, count in BUILD_SPECIFICATION_LEVEL_COUNTS.items()
    )
    if args.json:
        print(json.dumps(report, indent=2))
        return 0 if passed else 1
    for name, stats in report.items():
        print(
            f"{name}: {stats['distinct_prompts']}/{stats['tasks']} distinct prompts; "
            f"words min/median/max {stats['prompt_words_min']}/"
            f"{stats['prompt_words_median']}/{stats['prompt_words_max']}"
        )
        if name == "build-openbb-apps":
            for difficulty, values in stats["by_difficulty"].items():
                print(
                    f"  {difficulty}: {values['tasks']} tasks; words min/median/max "
                    f"{values['prompt_words_min']}/{values['prompt_words_median']}/"
                    f"{values['prompt_words_max']}"
                )
            for level, values in stats["by_specification_level"].items():
                print(
                    f"  specification {level}: {values['tasks']} tasks; words "
                    f"min/median/max {values['prompt_words_min']}/"
                    f"{values['prompt_words_median']}/{values['prompt_words_max']}"
                )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
