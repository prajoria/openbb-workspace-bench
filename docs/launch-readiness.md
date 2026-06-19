# Launch Readiness

Workspace Bench is ready for an alpha benchmark release because it now has:

- 25 bundled deterministic scenarios
- L0-L4 task coverage
- equities, macro, and portfolio fixture domains
- cross-backend tasks
- app-template tasks
- repair and layout tasks
- scenario metadata and filtering
- validation gates
- oracle and no-op baselines
- report generation
- external agent command contract
- task envelope export
- configurable multi-model comparison
- rollout, SFT, and preference exports
- Gym-style RL adapter
- private scenario directory support
- live `workspace-mcp` sidecar smoke command
- CI configuration
- contribution and release docs

## Current Launch Positioning

Recommended wording:

> OpenBB Workspace Bench is a Terminal-Bench-style evaluation harness for agents that compose financial analyst workspaces through OpenBB Workspace MCP tools.

The current public release should be positioned as `workspace-core-v0` alpha. It supports simulator-backed evals, private task packs, external trace-producing agents, and live `workspace-mcp` sidecar smoke tests.

## Remaining Gaps

The most important gaps before a broader public leaderboard are:

1. Baseline results from real agents or models.
2. Hidden or generated scenario splits.
3. A browser-backed real Workspace runner, not only sidecar smoke with a simulated browser bridge.
4. Stronger data-dependent financial reasoning tasks.
5. A submission protocol and leaderboard policy.

The benchmark is strong enough to announce as an alpha developer release if the simulator-backed nature and leaderboard limitations are explicit.

## Alpha Release Checklist

- `uv run --extra dev python -m pytest`
- `uv run --extra dev workspace-bench validate --min-scenarios 25`
- `uv run --extra dev workspace-bench compare-models --models-file examples/models.example.json --difficulty easy --dry-run`
- `uv run --extra dev workspace-bench export-rollouts --oracle --scenario l1_add_price_widget --output /tmp/workspace-rollouts.jsonl`
- README quickstart commands match the CLI.
- `docs/benchmark-card.md` limitations are current.
- Hidden/private task-pack behavior is documented.
