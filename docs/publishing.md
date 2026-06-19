# Publishing Guide

This folder is prepared as an alpha benchmark package for `workspace-core-v0`.

## Pre-Publish Gates

Run:

```bash
uv run --extra dev pytest
uv run --extra dev workspace-bench validate --min-scenarios 25
uv run --extra dev workspace-bench run --agent oracle
uv run --extra dev workspace-bench export-task --scenario l1_add_price_widget --output /tmp/workspace-task.json
uv run --extra dev workspace-bench run-agent-command \
  --scenario l1_add_price_widget \
  --agent-command "python -m workspace_bench.examples.jsonl_rule_agent"
uv run --extra dev workspace-bench report --output docs/benchmark-report.md
uv build
```

Optional, with a running local sidecar:

```bash
workspace-mcp --cors-allow https://pro.openbb.dev
uv run --extra live workspace-bench smoke-workspace-mcp \
  --url http://127.0.0.1:8787 \
  --scenario l1_add_price_widget \
  --json
```

## Release Artifacts

- `README.md`: primary getting-started guide
- `docs/benchmark-card.md`: scope, limitations, intended use
- `docs/benchmark-report.md`: current oracle/no-op scorecard
- `docs/agent-command.md`: BYO-agent protocol
- `docs/private-task-packs.md`: BYO-data/task-pack workflow
- `docs/training-recipes.md`: SFT, preference, and RL rollout export patterns
- `docs/contributing.md`: contribution paths for scenarios, graders, agents, exports, and RL
- `docs/launch-readiness.md`: release gate checklist
- `.github/workflows/ci.yml`: continuous validation

## Owner Decisions Before Public Announcement

- Confirm repository URL in `pyproject.toml`.
- Add the organization's chosen license if this will be open sourced.
- Decide whether `workspace-core-v0` oracle traces are public training data, evaluation-only data, or both.
- Decide whether to publish as a PyPI package, GitHub-only benchmark repo, or both.
- Decide whether leaderboard submissions require hidden/generated tasks.

## Claims That Are Currently Supported

Supported:

- simulator-backed Workspace MCP agent evaluation
- deterministic `workspace-core-v0` scenario set
- private task packs through `--scenario-dir`
- external trace-producing agents through `run-agent-command`
- live `workspace-mcp` sidecar smoke checks

Not yet supported:

- public model leaderboard quality
- hidden benchmark split
- real browser-backed Workspace execution as the default runner
- claims about live market-data financial reasoning
