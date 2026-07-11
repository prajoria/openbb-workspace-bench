# Release Checklist

Use this checklist before announcing a public Workspace Bench release.

## Required

- [ ] `uv run --extra dev ruff check src tests scripts examples` passes.
- [ ] `uv run --extra dev mypy src/workspace_bench` passes.
- [ ] `uv run --extra dev pytest` passes.
- [ ] `uv run workspace-bench validate --suite core --min-tasks 300` passes with release checks green.
- [ ] `uv run workspace-bench validate --suite build-openbb-apps --min-tasks 212` passes with release checks green.
- [ ] `uv run workspace-bench run --agent oracle` passes all tasks (both suites).
- [ ] `uv run workspace-bench run --agent noop` fails every task (both suites).
- [ ] `uv run workspace-bench export-task --task gen_t0_create_price_performance_aapl --output /tmp/workspace-task.json` succeeds.
- [ ] `uv run workspace-bench run-agent-command --task gen_t0_create_price_performance_aapl --agent-command "python -m workspace_bench.examples.jsonl_rule_agent"` passes.
- [ ] `uv run workspace-bench report --suite core --output runs/reports/benchmark-report.md` succeeds.
- [ ] `uv run --extra live python scripts/audit_hosted_surface.py` reports no missing tools, prompts, or resources against the hosted Workspace MCP (needs `WORKSPACE_MCP_TOKEN` in `.env`).
- [ ] Task counts: exactly 300 in `core`, exactly 212 in `build-openbb-apps` (512 total).
- [ ] Split counts are 150/75/75 (`core`) and 106/53/53 (`build-openbb-apps`) train/validation/test, with every family/level cell contributing one validation and one test task.
- [ ] Novelty fingerprints and task ids are unique in both suites.
- [ ] Coverage quotas pass in both suites via `validate` (core: backend, difficulty, widget-pair, dashboard-category, grader-check quotas; build-openbb-apps: widget-type/param-type ownership, difficulty bands, per-level graded-check caps).
- [ ] The build-openbb-apps official gating curve (gpt-4.1-mini, one fresh end-to-end run) is strictly decreasing with no tied levels.
- [ ] Published runs under `runs/comparison/` are single clean end-to-end runs — no `summary.patched` field in any result file.
- [ ] `runs/reports/suites.json` is compiled from the published run directories (`core-*`, `build-*`).
- [ ] `runs/reports/significance.json` is recomputed (`scripts/compute_significance.py`) and the README board notes match it.
- [ ] README quick start, suites table, and aggregate command are accurate.
- [ ] `docs/task-catalog.md` is regenerated and covers both suites (512 entries).
- [ ] `docs/contributing.md` explains how to add tasks and suites.
- [ ] Repository URL in `pyproject.toml` is correct.
- [ ] License decision is made before open-source publication.
- [ ] CI is green.

## Strongly Recommended Before Wider Launch

- [ ] Add at least one real Workspace MCP sidecar parity run.
- [ ] Add a hidden or held-out task split.
- [ ] Add an optional Docker or compose workflow for fixture backend serving.
- [ ] Publish a short benchmark report with coverage, baselines, and limitations.

## Claims to Avoid Until Verified

- Do not claim live OpenBB Workspace execution until the real sidecar adapter has parity evidence.
- Do not claim financial reasoning coverage beyond the included deterministic fixture domains.
