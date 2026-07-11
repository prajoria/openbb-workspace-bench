# Release Checklist

Use this checklist before announcing a public Workspace Bench release.

## Required

- [ ] `uv run --extra dev pytest` passes.
- [ ] `uv run workspace-bench validate --collection core --min-scenarios 300` passes with release checks green.
- [ ] `uv run workspace-bench validate --collection build-openbb-apps --min-scenarios 212` passes with release checks green.
- [ ] `uv run workspace-bench run --agent oracle` passes all scenarios (both collections).
- [ ] `uv run workspace-bench run --agent noop` fails every scenario (both collections).
- [ ] `uv run workspace-bench export-task --scenario gen_t0_create_price_performance_aapl --output /tmp/workspace-task.json` succeeds.
- [ ] `uv run workspace-bench run-agent-command --scenario gen_t0_create_price_performance_aapl --agent-command "python -m workspace_bench.examples.jsonl_rule_agent"` passes.
- [ ] `uv run workspace-bench report --collection core --output runs/reports/benchmark-report.md` succeeds.
- [ ] `uv run --extra live python scripts/audit_hosted_surface.py` reports no missing tools, prompts, or resources against the hosted Workspace MCP (needs `WORKSPACE_MCP_TOKEN` in `.env`).
- [ ] Scenario counts: exactly 300 in `core`, exactly 212 in `build-openbb-apps` (512 total).
- [ ] `core` split counts are 180 train, 60 validation, and 60 test.
- [ ] Novelty fingerprints and scenario ids are unique in both collections.
- [ ] Coverage quotas pass in both collections (core: backend, difficulty, widget-pair, L2 dashboard, grader-check quotas; build-openbb-apps: widget-type/param-type ownership, difficulty bands, per-tier graded-check caps).
- [ ] The build-openbb-apps official gating curve (gpt-4.1-mini, one fresh end-to-end run) is strictly decreasing with no tied tiers.
- [ ] Published runs under `runs/comparison/` are single clean end-to-end runs — no `summary.patched` field in any result file.
- [ ] `runs/reports/collections.json` is compiled from the published run directories (`core-*`, `build-*`).
- [ ] README quick start, collections table, and aggregate command are accurate.
- [ ] `docs/scenario-catalog.md` is regenerated and covers both collections (512 entries).
- [ ] `docs/contributing.md` explains how to add scenarios and collections.
- [ ] Repository URL in `pyproject.toml` is correct.
- [ ] License decision is made before open-source publication.
- [ ] CI is green.

## Strongly Recommended Before Wider Launch

- [ ] Add at least one real Workspace MCP sidecar parity run.
- [ ] Add a hidden or held-out scenario split.
- [ ] Add an optional Docker or compose workflow for fixture backend serving.
- [ ] Publish a short benchmark report with coverage, baselines, and limitations.

## Claims to Avoid Until Verified

- Do not claim live OpenBB Workspace execution until the real sidecar adapter has parity evidence.
- Do not claim financial reasoning coverage beyond the included deterministic fixture domains.
