# Release Checklist

Use this checklist before announcing a public Workspace Bench release.

## Required for v0.1

- [ ] `uv run --extra dev pytest` passes.
- [ ] `uv run --extra dev workspace-bench validate --min-scenarios 25` passes.
- [ ] `uv run --extra dev workspace-bench run --agent oracle` passes all scenarios.
- [ ] `uv run --extra dev workspace-bench export-task --scenario l1_add_price_widget --output /tmp/workspace-task.json` succeeds.
- [ ] `uv run --extra dev workspace-bench run-agent-command --scenario l1_add_price_widget --agent-command "python -m workspace_bench.examples.jsonl_rule_agent"` passes.
- [ ] `uv run --extra dev workspace-bench report --output docs/benchmark-report.md` is regenerated.
- [ ] Scenario count is at least 25.
- [ ] No-op baseline fails every scenario.
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
