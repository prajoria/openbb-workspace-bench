"""Generate the WorkspaceBench build-openbb-apps collection (v3 ladder).

TMax-style compositional generation for the AUTHORING skill: every task asks the
agent to produce valid widgets.json / apps.json payloads that the workspace accepts.
Families mirror the onboarding reference app (each family = one tab theme of
getting-started/reference-backend), so widget-type coverage is by construction:

    types settings params forms aggrid charts advanced grouping | apps extend | e2e

The v3 level ladder (Didier alignment, 2026-07-08):
    t0 one widget with the right schema (exact-JSON brief)
    t1 ship it as an app (widget + one-tab apps.json wrapper)
    t2 one widget, >=2 composed requirements (words + derivation, never JSON)
    t3 the app takes shape (2-3 widgets + multi-tab app + placement)
    t4 operate what you built (build -> publish -> instantiate -> place -> note)

    212 tasks = 10 x 5 x 4 + 12 (e2e capstone exists only at t4)

Usage:
    uv run python scripts/generate_build_apps_suite.py            # full build + certify + write
    uv run python scripts/generate_build_apps_suite.py --partial  # build available families, certify, no write
"""

from __future__ import annotations

import importlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from build_apps_suite import common as c  # noqa: E402

FAMILY_MODULES = [
    "fam_types", "fam_settings", "fam_params", "fam_forms",
    "fam_aggrid", "fam_charts", "fam_advanced", "fam_grouping",
    "fam_apps", "fam_extend",
    "fam_e2e",
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
                params = definition.get("params") or []
                flat = []
                for entry in params:
                    flat.extend(entry if isinstance(entry, list) else [entry])
                for param in flat:
                    if isinstance(param, dict):
                        ptypes[param.get("type", "text")] += 1
                        for inner in param.get("inputParams") or []:
                            if isinstance(inner, dict):
                                ptypes[inner.get("type", "text")] += 1
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
                params = definition.get("params") or []
                flat = []
                for entry in params:
                    flat.extend(entry if isinstance(entry, list) else [entry])
                for param in flat:
                    if isinstance(param, dict):
                        coverage.setdefault(family, set()).add(param.get("type", "text"))
                        for inner in param.get("inputParams") or []:
                            if isinstance(inner, dict):
                                coverage.setdefault(family, set()).add(
                                    inner.get("type", "text")
                                )
    return coverage


def quota_report(tasks: list[dict], partial: bool) -> list[tuple[str, object, str, bool]]:
    total = len(tasks)
    report: list[tuple[str, object, str, bool]] = []
    difficulties = Counter(task["difficulty"] for task in tasks)
    if not partial:
        report.append(("total tasks", total, "= 212", total == 212))
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
        report.append((
            "tasks grading widget defs", widget_def_tasks, ">= 160",
            widget_def_tasks >= 160,
        ))
        report.append((
            "tasks grading app defs", app_def_tasks, ">= 100",
            app_def_tasks >= 100,
        ))
    fingerprints = [c.novelty_fingerprint(task) for task in tasks]
    report.append((
        "novelty fingerprints", len(set(fingerprints)), f"= {total}",
        len(set(fingerprints)) == total,
    ))
    # duplicate ids silently overwrite each other's files at write time
    ids = [task["id"] for task in tasks]
    duplicate_ids = sorted({sid for sid in ids if ids.count(sid) > 1})
    report.append((
        "task ids unique", duplicate_ids or "all", f"{total} distinct",
        not duplicate_ids,
    ))
    id_ok = all(
        task["id"].startswith(f"auth_{task['_level']}_{task['_family']}_")
        for task in tasks
    )
    report.append(("id convention auth_<level>_<family>_", id_ok, "all", id_ok))
    return report


# ---------------------------------------------------------------------------
# In-process certification: oracle passes, no-op fails, for every task.
# ---------------------------------------------------------------------------

# Per-task graded-check caps per level. Strict pass ~= q^N: uncontrolled check
# mass (N) drove the level curve instead of per-check difficulty (q) — v2 round-11
# root-cause finding; the discipline is permanent. v3 ladder: t1 grades the
# widget as a 3-check anchor (skill proven at t0) + the app wrapper fully, so
# its cap sits just above t0; t3 is focus-widget-full + sibling anchors + app.
# The caps live in the package so `workspace-bench validate` re-verifies the
# same gate on the shipped suite.
from workspace_bench.core.suite_checks import (  # noqa: E402
    BUILD_CHECK_CAPS as CHECK_CAPS,
    BUILD_DIFFICULTY_BANDS,
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
        oracle_ok = True
        for call in task.oracle_tool_calls:
            result = episode.step(call)
            if not result.get("ok"):
                failures.append(
                    f"{raw['id']}: oracle call {call.name} rejected: "
                    f"{(result.get('error') or {}).get('message')}"
                )
                oracle_ok = False
                break
        if oracle_ok:
            grade = episode.grade()
            check_counts[raw["id"]] = grade.checks_total
            if not grade.passed:
                issues = "; ".join(
                    f"{issue.code}: {issue.message}" for issue in grade.issues[:3]
                )
                failures.append(f"{raw['id']}: oracle graded FAIL: {issues}")
            cap = CHECK_CAPS[raw["_level"]]
            if grade.checks_total > cap:
                failures.append(
                    f"{raw['id']}: grades {grade.checks_total} checks, over the "
                    f"{raw['_level']} cap of {cap} (use anchor checks for "
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
                tier_n[task["_level"]].append(check_counts[task["id"]])
        print("graded checks per task (mean/max, cap):")
        for level in c.LEVELS:
            counts = tier_n.get(level, [])
            if counts:
                print(f"  {level}: mean={sum(counts)/len(counts):5.1f} "
                      f"max={max(counts)} cap={CHECK_CAPS[level]}")

    print(f"\n{'family':12s}" + "".join(f"{t:>5s}" for t in c.LEVELS) + f"{'total':>7s}")
    for family in sorted(matrix):
        row = matrix[family]
        print(
            f"{family:12s}" + "".join(f"{row.get(t, 0):5d}" for t in c.LEVELS)
            + f"{sum(row.values()):7d}"
        )
    totals = {t: sum(row.get(t, 0) for row in matrix.values()) for t in c.LEVELS}
    print(
        f"{'TOTAL':12s}" + "".join(f"{totals[t]:5d}" for t in c.LEVELS)
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
    for stale in out_dir.glob("*.json"):
        stale.unlink()
    for task in tasks:
        payload = {k: v for k, v in task.items() if not k.startswith("_")}
        (out_dir / f"{payload['id']}.json").write_text(
            json.dumps(payload, indent=2) + "\n"
        )
    manifest = {
        "suite_id": "workspace-bench-v2-build-openbb-apps",
        "release_id": "workspace-bench-v2-build-openbb-apps",
        "version": "2.0.0",
        "visibility": "public",
        "default_split": "train",
        "description": (
            "WorkspaceBench build-openbb-apps collection: the agent writes valid "
            "widgets.json / apps.json payloads for custom backends. Families "
            "mirror the onboarding reference app (types, settings, params, forms, "
            "aggrid, charts, advanced, grouping, apps, extend) x the v3 ladder "
            "(t0 schema, t1 ship-as-app, t2 composed requirements, t3 multi-widget "
            "app, t4 orchestrate), 4 per cell, plus a 12-task e2e capstone at "
            "t4 (212 total). Certified oracle-passes / no-op-fails; validation "
            "mirrors the real workspace frontend."
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
