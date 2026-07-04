# Release Checklist

Use this checklist before announcing a public Workspace Bench release.

## Required for v1.0

- [ ] `uv run --extra dev pytest` passes.
- [ ] `uv run --extra dev workspace-bench validate --pack all --min-scenarios 300` passes with release checks green.
- [ ] `uv run --extra dev workspace-bench run --agent oracle` passes all scenarios.
- [ ] `uv run --extra dev workspace-bench run --agent noop` fails every scenario.
- [ ] `uv run --extra dev workspace-bench export-task --scenario gen_t0_create_price_performance_aapl --output /tmp/workspace-task.json` succeeds.
- [ ] `uv run --extra dev workspace-bench run-agent-command --scenario gen_t0_create_price_performance_aapl --agent-command "python -m workspace_bench.examples.jsonl_rule_agent"` passes.
- [ ] `uv run --extra dev workspace-bench report --pack all --output runs/reports/benchmark-report.md` succeeds.
- [ ] `uv run --extra live python scripts/audit_hosted_surface.py` reports no missing tools, prompts, or resources against the hosted Workspace MCP (needs `WORKSPACE_MCP_TOKEN` in `.env`).
- [ ] Scenario count is exactly 300 for the bundled release.
- [ ] Split counts are 180 train, 60 validation, and 60 test.
- [ ] Novelty fingerprints are unique.
- [ ] Backend, difficulty, widget-pair, L2 dashboard, and grader-check quotas pass.
- [ ] README quick start is accurate.
- [ ] `CONTRIBUTING.md` explains how to add scenarios.
- [ ] Repository URL in `pyproject.toml` is correct.
- [ ] License decision is made before open-source publication.
- [ ] CI is green.

## Strongly Recommended Before Wider Launch

- [ ] Add at least one real Workspace MCP sidecar parity run.
- [ ] Add results for at least one non-oracle agent.
- [ ] Add a hidden or held-out scenario split.
- [ ] Add an optional Docker or compose workflow for fixture backend serving.
- [ ] Publish a short benchmark report with coverage, baselines, and limitations.

## Claims to Avoid Until Verified

- Do not claim live OpenBB Workspace execution until the real sidecar adapter has parity evidence.
- Do not claim model leaderboard quality until real agent baselines are included.
- Do not claim financial reasoning coverage beyond the included deterministic fixture domains.
