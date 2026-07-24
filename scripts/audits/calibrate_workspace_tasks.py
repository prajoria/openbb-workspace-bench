"""Per-persona calibration gate for the workspace_tasks suite.

When a persona's stories are complete (4 stories x 6 levels = 24 tasks), this
gate runs a mid-capability model (gpt-4.1-mini by default) over those tasks
with 3 repeats and checks the level staircase:

    pass(level0) >= pass(level1) >= ... >= pass(level5)

Each persona's result is merged into a ledger so that, once every persona has
been gated, ``--aggregate`` pools all attempts and reports the suite-wide
per-level curve alongside each persona's own.

Usage:
    uv run python scripts/audits/calibrate_workspace_tasks.py --persona portfolio_manager
    uv run python scripts/audits/calibrate_workspace_tasks.py --persona fund_operations --from-run runs/comparison/workspace-tasks-gpt-4.1-mini-fund_operations
    uv run python scripts/audits/calibrate_workspace_tasks.py --aggregate

Exit code is non-zero when the staircase is violated - treat it as a gate.
A violation is a signal to investigate, not to tune: per the suite's history,
a task failing level0 on every repeat is a defect fingerprint (fix the task),
while a mid-ladder wobble at 12 attempts/level may be noise (note it for the
persona review).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import subprocess
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
SUITE_DIR = REPO / "src" / "workspace_bench" / "task_suites" / "workspace_tasks"
DEFAULT_LEDGER = REPO / "runs" / "reports" / "workspace-tasks-calibration.json"
DEFAULT_REPORT = REPO / "runs" / "reports" / "workspace-tasks-calibration.md"
LEVELS = tuple(f"level{i}" for i in range(6))
DEFAULT_MODEL = "openai:gpt-4.1-mini"
DEFAULT_REPEATS = 3


def _model_slug(model: str) -> str:
    return model.replace(":", "-").replace("/", "-")


def run_model(persona: str, model: str, repeats: int, output_dir: Path, concurrency: int) -> None:
    """Invoke the existing model harness over one persona's tasks."""

    cmd = [
        "uv", "run", "workspace-bench",
        "--model", model,
        "--task-dir", str(SUITE_DIR),
        "--family", persona,
        "--repeats", str(repeats),
        "--run-name", f"workspace-tasks-{_model_slug(model)}-{persona}",
        "--output-dir", str(output_dir),
        "--concurrency", str(concurrency),
    ]
    print("running:", " ".join(cmd), flush=True)
    completed = subprocess.run(cmd, cwd=REPO, check=False)
    if completed.returncode not in (0, 1):
        # 0 = all passed, 1 = some tasks failed (normal for calibration);
        # anything else is a harness failure worth stopping on.
        raise SystemExit(f"model run exited with {completed.returncode}")


def _iter_result_rows(value: Any):
    """Yield per-attempt result rows regardless of the JSON's exact nesting."""

    if isinstance(value, dict):
        if {"id", "difficulty", "passed"} <= set(value):
            yield value
        else:
            for child in value.values():
                yield from _iter_result_rows(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_result_rows(child)


def collect(output_dir: Path, model: str, persona: str) -> dict[str, dict[str, int]]:
    """Tally passes/attempts per level from a stored run directory."""

    results_path = output_dir / f"{_model_slug(model)}.json"
    candidates = sorted(output_dir.glob("*.json"))
    rows_file = results_path if results_path.exists() else None
    if rows_file is None:
        for candidate in candidates:
            if candidate.name not in {"comparison.json"} and not candidate.name.endswith(
                (".checkpoint.json", ".manifest.json")
            ):
                rows_file = candidate
                break
    if rows_file is None:
        raise SystemExit(f"no results JSON found in {output_dir}")
    payload = json.loads(rows_file.read_text(encoding="utf-8"))
    tally: dict[str, dict[str, int]] = {
        level: {"passes": 0, "attempts": 0} for level in LEVELS
    }
    for row in _iter_result_rows(payload):
        if row.get("family") not in (None, persona):
            continue
        level = str(row["difficulty"])
        if level not in tally:
            continue
        tally[level]["attempts"] += 1
        tally[level]["passes"] += 1 if row.get("passed") else 0
    if all(cell["attempts"] == 0 for cell in tally.values()):
        raise SystemExit(f"no attempts found for persona {persona!r} in {rows_file}")
    return tally


def rates(tally: dict[str, dict[str, int]]) -> list[float | None]:
    out: list[float | None] = []
    for level in LEVELS:
        cell = tally[level]
        out.append(cell["passes"] / cell["attempts"] if cell["attempts"] else None)
    return out


def staircase_ok(tally: dict[str, dict[str, int]]) -> tuple[bool, list[str]]:
    """level0 >= level1 >= ... >= level5, ties allowed; gaps in data flagged."""

    violations: list[str] = []
    series = [(level, rate) for level, rate in zip(LEVELS, rates(tally)) if rate is not None]
    for (lo_name, lo), (hi_name, hi) in zip(series, series[1:]):
        if hi > lo + 1e-9:
            violations.append(
                f"{hi_name} ({hi:.0%}) > {lo_name} ({lo:.0%}) - inversion"
            )
    return (not violations, violations)


def print_curve(label: str, tally: dict[str, dict[str, int]]) -> None:
    parts = []
    for level, rate in zip(LEVELS, rates(tally)):
        cell = tally[level]
        parts.append(
            f"{level[-1]}:{'—' if rate is None else f'{rate:.0%}'}"
            f"({cell['passes']}/{cell['attempts']})"
        )
    print(f"{label}: " + "  ".join(parts))


def load_ledger(path: Path) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"model": None, "repeats": None, "personas": {}}


def save_ledger(path: Path, ledger: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def gate(args: argparse.Namespace) -> int:
    output_dir = (
        Path(args.from_run)
        if args.from_run
        else REPO / "runs" / "comparison" / f"workspace-tasks-{_model_slug(args.model)}-{args.persona}"
    )
    if not args.from_run:
        run_model(args.persona, args.model, args.repeats, output_dir, args.concurrency)
    tally = collect(output_dir, args.model, args.persona)
    ok, violations = staircase_ok(tally)
    print_curve(args.persona, tally)

    ledger = load_ledger(Path(args.ledger))
    if ledger.get("model") not in (None, args.model):
        print(
            f"warning: ledger holds runs for {ledger['model']!r}; do not mix models "
            "in one calibration series"
        )
    ledger["model"] = args.model
    ledger["repeats"] = args.repeats
    ledger["personas"][args.persona] = {
        "levels": tally,
        "monotone": ok,
        "run_dir": str(output_dir.relative_to(REPO)) if output_dir.is_relative_to(REPO) else str(output_dir),
        "recorded": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
    }
    save_ledger(Path(args.ledger), ledger)
    print(f"ledger updated: {args.ledger}")

    if ok:
        print(f"GATE PASS: {args.persona} staircase is monotone (ties allowed)")
        return 0
    print(f"GATE FAIL: {args.persona} staircase violated:")
    for violation in violations:
        print("  -", violation)
    print(
        "next: check whether the inverted level's failures repeat across attempts "
        "(defect fingerprint -> fix tasks) or scatter (noise -> note for review)"
    )
    return 1


def aggregate(args: argparse.Namespace) -> int:
    ledger = load_ledger(Path(args.ledger))
    personas = ledger.get("personas", {})
    if not personas:
        raise SystemExit(f"ledger {args.ledger} holds no persona results yet")
    pooled: dict[str, dict[str, int]] = {
        level: {"passes": 0, "attempts": 0} for level in LEVELS
    }
    lines = [
        "# workspace_tasks calibration",
        "",
        f"Model: `{ledger.get('model')}` - {ledger.get('repeats')} repeats per task, "
        f"{len(personas)} persona(s) recorded.",
        "",
        "| persona | " + " | ".join(LEVELS) + " | monotone |",
        "| --- | " + " | ".join("---:" for _ in LEVELS) + " | :-: |",
    ]
    for persona in sorted(personas):
        entry = personas[persona]
        tally = entry["levels"]
        print_curve(persona, tally)
        cells = []
        for level in LEVELS:
            cell = tally[level]
            pooled[level]["passes"] += cell["passes"]
            pooled[level]["attempts"] += cell["attempts"]
            cells.append(
                "—" if not cell["attempts"] else f"{cell['passes'] / cell['attempts']:.0%}"
            )
        lines.append(
            f"| {persona} | " + " | ".join(cells) + f" | {'yes' if entry.get('monotone') else 'NO'} |"
        )
    ok, violations = staircase_ok(pooled)
    print_curve("ALL PERSONAS", pooled)
    pooled_cells = [
        "—" if not pooled[level]["attempts"] else f"{pooled[level]['passes'] / pooled[level]['attempts']:.0%}"
        for level in LEVELS
    ]
    lines += [
        "| **all** | " + " | ".join(pooled_cells) + f" | {'yes' if ok else 'NO'} |",
        "",
    ]
    if not ok:
        lines.append("Aggregate staircase violations:")
        lines += [f"- {violation}" for violation in violations]
        lines.append("")
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).write_text("\n".join(lines), encoding="utf-8")
    print(f"report written: {args.report}")
    if ok:
        print("AGGREGATE PASS: pooled staircase is monotone (ties allowed)")
        return 0
    print("AGGREGATE FAIL:")
    for violation in violations:
        print("  -", violation)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--persona", help="Persona (task family) to gate.")
    parser.add_argument("--aggregate", action="store_true", help="Pool all recorded personas.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--repeats", type=int, default=DEFAULT_REPEATS)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument(
        "--from-run",
        help="Reuse a stored run directory instead of calling the model again.",
    )
    parser.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    args = parser.parse_args()
    if args.aggregate == bool(args.persona):
        parser.error("pass exactly one of --persona or --aggregate")
    return aggregate(args) if args.aggregate else gate(args)


if __name__ == "__main__":
    raise SystemExit(main())
