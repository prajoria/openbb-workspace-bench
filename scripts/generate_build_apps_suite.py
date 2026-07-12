"""Generate the WorkspaceBench build-openbb-apps collection (v3 ladder).

TMax-style compositional generation for the AUTHORING skill: every task asks the
agent to produce valid widgets.json / apps.json payloads that the workspace accepts.
Families mirror the onboarding reference app (each family = one tab theme of
getting-started/reference-backend), so widget-type coverage is by construction:

    types settings params forms aggrid charts advanced grouping | apps extend | e2e

The v3 functional ladder:
    r0 build and place one guided widget
    r1 publish and open a one-tab app
    r2 deliver a composed widget workflow
    r3 interpret, build, and open a multi-widget app brief
    r4 operate what you built (build -> publish -> instantiate -> configure -> note)

Every task exposes the complete Workspace tool surface. The generator keeps an
exact oracle payload internally, while the public prompt describes the intended
outcome and the grader requires a usable widget/app in final Workspace state.

    236 tasks = 10 x 5 x 4 + 12 e2e capstones + 24 debug repairs

Usage:
    uv run python scripts/generate_build_apps_suite.py            # full build + certify + write
    uv run python scripts/generate_build_apps_suite.py --partial  # build available families, certify, no write
"""

from __future__ import annotations

import importlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from build_apps_suite import common as c  # noqa: E402
from workspace_bench.workspace.widget_params import flatten_params  # noqa: E402

FAMILY_MODULES = [
    "fam_types", "fam_settings", "fam_params", "fam_forms",
    "fam_aggrid", "fam_charts", "fam_advanced", "fam_grouping",
    "fam_apps", "fam_extend",
    "fam_e2e",
    "fam_debug",
]


def build_families(partial: bool, only: list[str] | None = None) -> list[str]:
    loaded, missing = [], []
    selected = FAMILY_MODULES if not only else [m for m in FAMILY_MODULES if m in only]
    for module_name in selected:
        try:
            module = importlib.import_module(f"build_apps_suite.{module_name}")
            module.build()
        except Exception as error:  # noqa: BLE001 - partial builds tolerate WIP siblings
            if partial:
                missing.append(f"{module_name} ({type(error).__name__}: {error})")
                continue
            raise
        loaded.append(module_name)
    if missing:
        print("PARTIAL BUILD — missing/broken modules:")
        for name in missing:
            print(f"  - {name}")
    return loaded


# ---------------------------------------------------------------------------
# Quotas
# ---------------------------------------------------------------------------

def authored_widget_types(tasks: list[dict]) -> Counter:
    types: Counter = Counter()
    for task in tasks:
        for call in task["oracle_tool_calls"]:
            if call.get("tool") != "manage_backends":
                continue
            for definition in (call.get("args", {}).get("widgets_json") or {}).values():
                types[definition.get("type", "table")] += 1
    return types


def authored_param_types(tasks: list[dict]) -> Counter:
    ptypes: Counter = Counter()
    for task in tasks:
        for call in task["oracle_tool_calls"]:
            if call.get("tool") != "manage_backends":
                continue
            for definition in (call.get("args", {}).get("widgets_json") or {}).values():
                for param in flatten_params(definition, recurse=True):
                    ptypes[param.get("type", "text")] += 1
    return ptypes


def op_counts(tasks: list[dict]) -> Counter:
    ops: Counter = Counter()
    for task in tasks:
        for call in task["oracle_tool_calls"]:
            if call.get("tool") != "manage_backends":
                continue
            args = call.get("args", {})
            operation = args.get("operation")
            if operation == "add" and "widgets_json" in args:
                ops["add_custom"] += 1
            if operation == "refresh" and ("widgets_json" in args or "apps_json" in args):
                ops["refresh_payload"] += 1
            if "apps_json" in args:
                ops["apps_payload"] += 1
    return ops


def family_type_coverage(tasks: list[dict]) -> dict[str, set]:
    """Widget types each family actually writes (oracle payloads)."""

    coverage: dict[str, set] = {}
    for task in tasks:
        family = task["_family"]
        for call in task["oracle_tool_calls"]:
            if call.get("tool") != "manage_backends":
                continue
            for definition in (call.get("args", {}).get("widgets_json") or {}).values():
                coverage.setdefault(family, set()).add(definition.get("type", "table"))
    return coverage


def family_param_coverage(tasks: list[dict]) -> dict[str, set]:
    coverage: dict[str, set] = {}
    for task in tasks:
        family = task["_family"]
        for call in task["oracle_tool_calls"]:
            if call.get("tool") != "manage_backends":
                continue
            for definition in (call.get("args", {}).get("widgets_json") or {}).values():
                for param in flatten_params(definition, recurse=True):
                    coverage.setdefault(family, set()).add(param.get("type", "text"))
    return coverage


def quota_report(tasks: list[dict], partial: bool) -> list[tuple[str, object, str, bool]]:
    total = len(tasks)
    report: list[tuple[str, object, str, bool]] = []
    difficulties = Counter(task["difficulty"] for task in tasks)
    specification_levels = Counter(task["specification_level"] for task in tasks)
    if not partial:
        report.append(("total tasks", total, "= 236", total == 236))
        expected_bands = "/".join(
            str(BUILD_DIFFICULTY_BANDS[band]) for band in ("easy", "medium", "hard")
        )
        report.append((
            "difficulty easy/medium/hard",
            f"{difficulties['easy']}/{difficulties['medium']}/{difficulties['hard']}",
            expected_bands,
            all(
                difficulties[band] == count
                for band, count in BUILD_DIFFICULTY_BANDS.items()
            ),
        ))
        expected_specification_levels = "/".join(
            str(BUILD_SPECIFICATION_LEVEL_BANDS[level])
            for level in ("explicit", "partially-specified", "open-brief")
        )
        report.append((
            "specification explicit/partial/open",
            "/".join(
                str(specification_levels[level])
                for level in ("explicit", "partially-specified", "open-brief")
            ),
            expected_specification_levels,
            all(
                specification_levels[level] == count
                for level, count in BUILD_SPECIFICATION_LEVEL_BANDS.items()
            ),
        ))
        types = authored_widget_types(tasks)
        report.append((
            "built widget types", len(types), ">= 16 distinct (full catalog)",
            len(types) >= 16,
        ))
        param_types = authored_param_types(tasks)
        report.append((
            "built param types", len(param_types), ">= 9 distinct",
            len(param_types) >= 9,
        ))
        # ownership BY CONSTRUCTION: each family writes every type it owns
        type_cov = family_type_coverage(tasks)
        for family, owned in sorted(c.TYPE_OWNERSHIP.items()):
            observed = type_cov.get(family, set())
            missing = owned - observed
            report.append((
                f"{family} owns widget types", sorted(missing) or "all",
                f"writes all of {sorted(owned)}", not missing,
            ))
        param_cov = family_param_coverage(tasks)
        for family, owned in sorted(c.PARAM_OWNERSHIP.items()):
            observed = param_cov.get(family, set())
            missing = owned - observed
            report.append((
                f"{family} owns param types", sorted(missing) or "all",
                f"writes all of {sorted(owned)}", not missing,
            ))
        ops = op_counts(tasks)
        report.append((
            "custom adds (add + widgets_json)", ops["add_custom"], ">= 120",
            ops["add_custom"] >= 120,
        ))
        report.append((
            "payload refreshes", ops["refresh_payload"], ">= 16",
            ops["refresh_payload"] >= 16,
        ))
        report.append((
            "apps.json payloads", ops["apps_payload"], ">= 100",
            ops["apps_payload"] >= 100,
        ))
        widget_def_tasks = sum(
            1 for s in tasks if s["success"].get("required_widget_defs")
        )
        app_def_tasks = sum(
            1 for s in tasks if s["success"].get("required_app_defs")
        )
        capability_tasks = sum(
            1 for s in tasks if s["success"].get("required_capabilities")
        )
        report.append((
            "tasks grading exact widget defs", widget_def_tasks, ">= 40",
            widget_def_tasks >= 40,
        ))
        report.append((
            "tasks grading exact app defs", app_def_tasks, ">= 20",
            app_def_tasks >= 20,
        ))
        report.append((
            "tasks grading capabilities", capability_tasks, ">= 140",
            capability_tasks >= 140,
        ))
        empty_contracts = sum(
            not (
                capability.get("must_cover_fields")
                or capability.get("required_param_kinds")
                or capability.get("required_config")
            )
            for task in tasks
            for capability in task["success"].get("required_capabilities", [])
        )
        report.append((
            "empty capability contracts", empty_contracts, "= 0",
            empty_contracts == 0,
        ))
        missing_form_contracts = sum(
            capability.get("widget_kind") == "form"
            and (
                "form" not in capability.get("required_param_kinds", [])
                or not any(
                    dataset.get("name") in capability.get("datasets", [])
                    and dataset.get("form_endpoint")
                    for dataset in task["success"]["runtime_checks"]["datasets"]
                )
            )
            for task in tasks
            for capability in task["success"].get("required_capabilities", [])
        )
        report.append((
            "form capabilities without POST contracts", missing_form_contracts, "= 0",
            missing_form_contracts == 0,
        ))
    fingerprints = [c.novelty_fingerprint(task) for task in tasks]
    report.append((
        "novelty fingerprints", len(set(fingerprints)), f"= {total}",
        len(set(fingerprints)) == total,
    ))
    # Local ids need only be unique inside a family; the canonical identity is
    # suite/family/task and each family has its own directory.
    ids = [(task["_family"], task["id"]) for task in tasks]
    duplicate_ids = sorted({sid for sid in ids if ids.count(sid) > 1})
    report.append((
        "family/task ids unique", duplicate_ids or "all", f"{total} distinct",
        not duplicate_ids,
    ))
    id_ok = all(re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", task["id"]) for task in tasks)
    report.append(("local id convention", id_ok, "snake_case", id_ok))
    return report


# ---------------------------------------------------------------------------
# In-process certification: oracle passes, no-op fails, for every task.
# ---------------------------------------------------------------------------

# Per-task graded-check caps per level. Strict pass ~= q^N: uncontrolled check
# mass (N) drove the level curve instead of per-check difficulty (q) — v2 round-11
# root-cause finding; the discipline is permanent. v3 ladder: r1 grades the
# widget as a 3-check anchor (skill proven at r0) + the app wrapper fully, so
# its cap sits just above r0; r3 is focus-widget-full + sibling anchors + app.
# These internal generation-rung caps are collapsed into public specification-
# level caps by `workspace-bench validate`; generation rungs are not metadata.
CHECK_CAPS = {"r0": 20, "r1": 24, "r2": 26, "r3": 36, "r4": 34, "debug": 42}
from workspace_bench.core.suite_checks import (  # noqa: E402
    BUILD_DIFFICULTY_BANDS,
    BUILD_SPECIFICATION_LEVEL_BANDS,
    task_payload_digest,
)


def certify(tasks: list[dict]) -> tuple[list[str], dict[str, int]]:
    from workspace_bench.core.episode import WorkspaceEpisode
    from workspace_bench.core.models import Task

    failures: list[str] = []
    check_counts: dict[str, int] = {}
    for raw in tasks:
        payload = {k: v for k, v in raw.items() if not k.startswith("_")}
        try:
            task = Task.from_dict(payload)
        except Exception as error:  # noqa: BLE001
            failures.append(f"{raw['id']}: from_dict failed: {error}")
            continue
        episode = WorkspaceEpisode(task)
        for call in task.oracle_tool_calls:
            episode.step(call)
        grade = episode.grade()
        declarative_checks = grade.checks_total - grade.runtime_checks_total
        check_counts[raw["id"]] = declarative_checks
        if not grade.passed:
            issues = "; ".join(
                f"{issue.code}: {issue.message}" for issue in grade.issues[:3]
            )
            failures.append(f"{raw['id']}: oracle graded FAIL: {issues}")
        cap = CHECK_CAPS[raw["_rung"]]
        if declarative_checks > cap:
            failures.append(
                f"{raw['id']}: grades {declarative_checks} declarative checks, over the "
                f"{raw['_rung']} cap of {cap} (use anchor checks for "
                "preserved/secondary artifacts)"
            )
        noop = WorkspaceEpisode(task)
        noop_grade = noop.grade()
        if noop_grade.passed:
            failures.append(f"{raw['id']}: no-op agent PASSED (task too weak)")
        if len(task.oracle_tool_calls) > task.limits.get("max_turns", 99):
            failures.append(f"{raw['id']}: oracle longer than max_turns")
    return failures, check_counts


def main() -> int:
    partial = "--partial" in sys.argv
    only: list[str] | None = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1].split(",")
        partial = True
    loaded = build_families(partial, only)
    tasks = c.SCENARIOS
    print(f"Built {len(tasks)} tasks from {len(loaded)} family module(s).")
    task_refs = {
        f"build-openbb-apps/{task['_family']}/{task['id']}" for task in tasks
    }
    unknown_overrides = sorted(set(c.MEASURED_DIFFICULTY_OVERRIDES) - task_refs)
    if unknown_overrides:
        print(f"Unknown measured-difficulty task refs: {unknown_overrides}")
        return 1

    matrix = c.build_matrix(tasks)
    if not partial:
        c.assert_lattice(matrix)
    c.assign_splits(tasks)
    for task in tasks:
        c.add_novelty(task)

    report = quota_report(tasks, partial)
    failed_quotas = [name for name, _, _, ok in report if not ok]

    print("\nCertifying (oracle passes, no-op fails)...")
    failures, check_counts = certify(tasks)
    if check_counts:
        from collections import defaultdict
        tier_n = defaultdict(list)
        for task in tasks:
            if task["id"] in check_counts:
                tier_n[task["_rung"]].append(check_counts[task["id"]])
        print(
            "graded checks per task by internal generator rung "
            "(specification levels are audited separately):"
        )
        for level in c.ALL_RUNGS:
            counts = tier_n.get(level, [])
            if counts:
                print(f"  {level}: mean={sum(counts)/len(counts):5.1f} "
                      f"max={max(counts)} cap={CHECK_CAPS[level]}")

    print("\nInternal generator-rung allocation (not measured difficulty):")
    print(f"{'family':12s}" + "".join(f"{t:>7s}" for t in c.ALL_RUNGS) + f"{'total':>7s}")
    for family in sorted(matrix):
        row = matrix[family]
        print(
            f"{family:12s}" + "".join(f"{row.get(t, 0):7d}" for t in c.ALL_RUNGS)
            + f"{sum(row.values()):7d}"
        )
    totals = {t: sum(row.get(t, 0) for row in matrix.values()) for t in c.ALL_RUNGS}
    print(
        f"{'TOTAL':12s}" + "".join(f"{totals[t]:7d}" for t in c.ALL_RUNGS)
        + f"{sum(totals.values()):7d}"
    )

    print("\nQuota report")
    for name, observed, expected, ok in report:
        print(f"{'PASS' if ok else 'FAIL':4s} {name:38s} observed={observed} expected={expected}")

    if failures:
        print(f"\nCERTIFICATION FAILURES ({len(failures)}):")
        for failure in failures[:40]:
            print(f"  - {failure}")
        if len(failures) > 40:
            print(f"  ... and {len(failures) - 40} more")
        return 1
    if failed_quotas:
        print(f"\nQUOTA FAILURES: {failed_quotas}")
        return 1
    print("\nAll tasks certified: oracle passes, no-op fails.")

    if partial:
        print("Partial mode: nothing written.")
        return 0

    out_dir = c.BUNDLED_OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    for stale in out_dir.rglob("*.json"):
        if stale.name != "task_suite.json":
            stale.unlink()
    for candidate in sorted(out_dir.rglob("*"), reverse=True):
        if candidate.is_dir() and not any(candidate.iterdir()):
            candidate.rmdir()
    payloads = [
        {key: value for key, value in task.items() if not key.startswith("_")}
        for task in tasks
    ]
    for payload in payloads:
        family_dir = out_dir / payload["family"]
        family_dir.mkdir(parents=True, exist_ok=True)
        (family_dir / f"{payload['id']}.json").write_text(
            json.dumps(payload, indent=2) + "\n"
        )
    manifest = {
        "suite_id": "build-openbb-apps",
        "visibility": "public",
        "default_split": "train",
        "content_sha256": task_payload_digest(payloads),
        "description": (
            "WorkspaceBench build-openbb-apps collection: agents receive open product "
            "briefs, choose from the full Workspace tool surface, build valid custom "
            "backends, and prove the result by placing widgets or instantiating apps. "
            "The 236 tasks are organized by product family and labeled independently "
            "by difficulty."
        ),
    }
    (out_dir / "task_suite.json").write_text(json.dumps(manifest, indent=2) + "\n")
    init_py = out_dir / "__init__.py"
    if not init_py.exists():
        init_py.write_text("")
    print(f"Wrote {len(tasks)} tasks to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
