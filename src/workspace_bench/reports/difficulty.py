"""Propose empirical task difficulty from two or more model result sets."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

DIFFICULTIES = ("easy", "medium", "hard")


def discover_results(inputs: list[str]) -> list[Path]:
    candidates: list[Path] = []
    for raw in inputs:
        path = Path(raw)
        candidates.extend(path.rglob("*.json") if path.is_dir() else [path])
    results = []
    for path in sorted(set(candidates)):
        if path.name == "comparison.json" or path.name.endswith(
            (".checkpoint.json", ".manifest.json")
        ):
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(payload, dict) and isinstance(payload.get("results"), list):
            results.append(path)
    return results


def propose(
    result_payloads: list[dict[str, Any]], config: dict[str, Any]
) -> dict[str, Any]:
    thresholds = config.get("thresholds") or {}
    easy_min = float(thresholds.get("easy_min_competent_rate", 0.8))
    medium_min = float(thresholds.get("medium_min_competent_rate", 0.4))
    hard_frontier_max = float(thresholds.get("hard_max_frontier_rate", 0.8))
    hard_small_max = float(thresholds.get("hard_max_small_rate", 0.2))
    review_policy = config.get("review_policy") or {}
    minimum_repeats = int(review_policy.get("minimum_repeats", 2))
    if minimum_repeats < 2:
        raise ValueError("review_policy.minimum_repeats must be at least 2")
    model_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    workspace_baselines: set[str] = set()
    for payload in result_payloads:
        model = payload.get("model") or {}
        slug = str(model.get("slug") or model.get("id") or "unknown")
        model_rows[slug].extend(payload.get("results") or [])
        workspace_baselines.add(
            str((payload.get("benchmark") or {}).get("workspace_baseline") or "unknown")
        )
    if len(workspace_baselines) > 1:
        raise ValueError(
            "difficulty proposals cannot mix workspace baselines: "
            f"{sorted(workspace_baselines)}"
        )
    if len(model_rows) < 2:
        raise ValueError("difficulty proposals require at least two distinct model result sets")

    all_models = sorted(model_rows)
    competent = _role_models(config.get("competent_models"), all_models, "competent")
    frontier = _role_models(config.get("frontier_models"), all_models, "frontier")
    small = _role_models(config.get("small_models"), all_models, "small", allow_empty=True)
    task_rates: dict[str, dict[str, float]] = defaultdict(dict)
    task_outcomes: dict[str, dict[str, list[bool]]] = defaultdict(dict)
    task_repeats: dict[str, dict[str, list[int]]] = defaultdict(dict)
    metadata: dict[str, tuple[str, str, str]] = {}
    for slug, rows in model_rows.items():
        grouped: dict[str, list[tuple[int, bool]]] = defaultdict(list)
        for row in rows:
            task_ref = str(row.get("qualified_id") or row.get("id"))
            grouped[task_ref].append((int(row.get("repeat", 1)), bool(row.get("passed"))))
            metadata[task_ref] = (
                str(row.get("difficulty") or "medium"),
                str(row.get("family") or "unknown"),
                str(
                    row.get("specification_level")
                    or {
                        "easy": "explicit",
                        "medium": "partially-specified",
                        "hard": "open-brief",
                    }.get(str(row.get("difficulty") or "medium"), "partially-specified")
                ),
            )
        for task_ref, repeat_outcomes in grouped.items():
            repeats = [repeat for repeat, _ in repeat_outcomes]
            if len(repeats) != len(set(repeats)):
                raise ValueError(f"{task_ref} has duplicate repeats for {slug}")
            ordered = [outcome for _, outcome in sorted(repeat_outcomes)]
            outcomes = ordered
            task_rates[task_ref][slug] = sum(outcomes) / len(outcomes)
            task_outcomes[task_ref][slug] = outcomes
            task_repeats[task_ref][slug] = sorted(repeats)

    rows = []
    for task_ref in sorted(task_rates):
        rates = task_rates[task_ref]
        missing = [slug for slug in competent if slug not in rates]
        if missing:
            raise ValueError(f"{task_ref} is missing competent model results: {missing}")
        competent_rates = [rates[slug] for slug in competent]
        frontier_rates = [rates[slug] for slug in frontier if slug in rates]
        small_rates = [rates[slug] for slug in small if slug in rates]
        competent_mean = mean(competent_rates)
        frontier_mean = mean(frontier_rates) if frontier_rates else competent_mean
        small_mean = mean(small_rates) if small_rates else None
        if min(competent_rates) >= easy_min:
            raw_proposed = "easy"
            reason = "every competent model meets the easy threshold"
        elif competent_mean >= medium_min:
            raw_proposed = "medium"
            reason = "competent-model mean is in the medium band"
        elif frontier_mean < hard_frontier_max and (
            small_mean is None or small_mean <= hard_small_max
        ):
            raw_proposed = "hard"
            reason = "frontier meaningfully fails and small models rarely pass"
        else:
            raw_proposed = "medium"
            reason = "mixed evidence does not meet the hard rule"
        old, family, specification_level = metadata[task_ref]
        required_models = sorted(set(competent + frontier + small))
        complete_repeats = all(
            len(task_repeats[task_ref].get(slug, [])) >= minimum_repeats
            for slug in required_models
        )
        all_selected_outcomes = [
            outcome
            for slug in required_models
            for outcome in task_outcomes[task_ref].get(slug, [])
        ]
        competent_outcomes = [
            outcome
            for slug in competent
            for outcome in task_outcomes[task_ref].get(slug, [])
        ]
        frontier_outcomes = [
            outcome
            for slug in frontier
            for outcome in task_outcomes[task_ref].get(slug, [])
        ]
        small_outcomes = [
            outcome
            for slug in small
            for outcome in task_outcomes[task_ref].get(slug, [])
        ]
        if family == "debug" and complete_repeats and not any(all_selected_outcomes):
            proposed = "hard"
            decision = "approved: debug task had zero passes across every selected model"
        elif raw_proposed == old:
            proposed = old
            decision = "unchanged: raw band matches the current label"
        elif not complete_repeats:
            proposed = old
            decision = "retained: fewer than the required repeats were present"
        elif raw_proposed == "easy" and all(competent_outcomes):
            proposed = "easy"
            decision = "approved: every competent-model repeat passed"
        elif raw_proposed == "medium":
            proposed = "medium"
            decision = (
                "approved: complete repeated evidence places the task in the "
                "intermediate band"
            )
        elif (
            raw_proposed == "hard"
            and not any(competent_outcomes)
            and not any(frontier_outcomes)
            and not any(small_outcomes)
        ):
            proposed = "hard"
            decision = "approved: competent/frontier/small evidence was unanimously failing"
        else:
            proposed = old
            decision = (
                "retained: intermediate evidence lies within one repeat of a band boundary"
            )
        rows.append(
            {
                "task_ref": task_ref,
                "family": family,
                "specification_level": specification_level,
                "old": old,
                "raw_proposed": raw_proposed,
                "proposed": proposed,
                "changed": old != proposed,
                "reason": reason,
                "decision": decision,
                "evidence": {
                    "model_pass_rates": {slug: rates.get(slug) for slug in all_models},
                    "model_repeats": {
                        slug: task_repeats[task_ref].get(slug, []) for slug in all_models
                    },
                    "complete_repeats": complete_repeats,
                    "competent_mean": round(competent_mean, 4),
                    "competent_min": round(min(competent_rates), 4),
                    "frontier_mean": round(frontier_mean, 4),
                    "small_mean": round(small_mean, 4) if small_mean is not None else None,
                },
            }
        )
    proposed_bands = Counter(row["proposed"] for row in rows)
    overrides = dict(config.get("overrides") or {})
    structural_band = {
        "explicit": "easy",
        "partially-specified": "medium",
        "open-brief": "hard",
    }
    for row in rows:
        task_ref = row["task_ref"]
        if row["proposed"] == structural_band[row["specification_level"]]:
            overrides.pop(task_ref, None)
        else:
            overrides[task_ref] = row["proposed"]
    return {
        "schema_version": "workspace-bench-difficulty-proposal/v1",
        "workspace_baseline": next(iter(workspace_baselines), "unknown"),
        "models": all_models,
        "roles": {
            "competent": competent,
            "frontier": frontier,
            "small": small,
        },
        "thresholds": {
            "easy_min_competent_rate": easy_min,
            "medium_min_competent_rate": medium_min,
            "hard_max_frontier_rate": hard_frontier_max,
            "hard_max_small_rate": hard_small_max,
        },
        "review_policy": {
            "minimum_repeats": minimum_repeats,
            "knife_edge_episodes": 1,
            "unanimous_endpoint_exception": True,
            "debug_zero_passes_hard": True,
        },
        "rows": rows,
        "override_table": {
            "schema_version": "workspace-bench-measured-difficulty/v1",
            "measurement": config.get("measurement") or {},
            "thresholds": {
                "easy_min_competent_rate": easy_min,
                "medium_min_competent_rate": medium_min,
                "hard_max_frontier_rate": hard_frontier_max,
                "hard_max_small_rate": hard_small_max,
            },
            "roles": {
                "competent": competent,
                "frontier": frontier,
                "small": small,
            },
            "review_policy": {
                "minimum_repeats": minimum_repeats,
                "knife_edge_episodes": 1,
                "unanimous_endpoint_exception": True,
                "debug_zero_passes_hard": True,
            },
            "bands": {difficulty: proposed_bands[difficulty] for difficulty in DIFFICULTIES},
            "overrides": overrides,
        },
    }


def _role_models(
    configured: Any,
    available: list[str],
    role: str,
    *,
    allow_empty: bool = False,
) -> list[str]:
    selected = available if configured is None else configured
    if not isinstance(selected, list) or not all(isinstance(item, str) for item in selected):
        raise ValueError(f"{role}_models must be a list of model slugs")
    unknown = sorted(set(selected) - set(available))
    if unknown:
        raise ValueError(f"{role}_models contains unavailable models: {unknown}")
    if not selected and not allow_empty:
        raise ValueError(f"{role}_models must not be empty")
    return list(selected)


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Measured difficulty proposal",
        "",
        "> Review only. No generated task has been relabeled by this output.",
        f"> Workspace baseline: `{payload.get('workspace_baseline', 'unknown')}`.",
        "",
        "| Task ref | Family | Old | Raw band | Approved | Evidence |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in payload["rows"]:
        rates = ", ".join(
            f"{slug}={rate:.0%}" if rate is not None else f"{slug}=missing"
            for slug, rate in row["evidence"]["model_pass_rates"].items()
        )
        lines.append(
            f"| `{row['task_ref']}` | {row['family']} | {row['old']} | "
            f"{row['raw_proposed']} | {row['proposed']} | {rates}; "
            f"{row['decision']} |"
        )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Model result JSON files or directories.")
    parser.add_argument("--bands", required=True, help="Bands/role configuration JSON.")
    parser.add_argument("--output", required=True, help="Proposal JSON output path.")
    parser.add_argument("--markdown", help="Optional review-table Markdown path.")
    parser.add_argument(
        "--apply-overrides",
        help="Write the conservatively approved override table to this source JSON path.",
    )
    args = parser.parse_args(argv)
    paths = discover_results(args.inputs)
    payloads = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    config = json.loads(Path(args.bands).read_text(encoding="utf-8"))
    try:
        proposal = propose(payloads, config)
    except ValueError as error:
        parser.error(str(error))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(proposal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.markdown:
        markdown = Path(args.markdown)
        markdown.parent.mkdir(parents=True, exist_ok=True)
        markdown.write_text(render_markdown(proposal), encoding="utf-8")
    if args.apply_overrides:
        override_path = Path(args.apply_overrides)
        override_path.parent.mkdir(parents=True, exist_ok=True)
        override_path.write_text(
            json.dumps(proposal["override_table"], indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    changed = sum(row["changed"] for row in proposal["rows"])
    print(f"Wrote {output}: {len(proposal['rows'])} tasks, {changed} proposed changes")
    if args.apply_overrides:
        print(f"Applied approved overrides to {args.apply_overrides}")
    else:
        print("No relabels were applied; review override_table before applying it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
