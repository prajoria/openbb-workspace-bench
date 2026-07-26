# Workspace Tasks

Tasks: 120

The benchmark's flagship suite: 120 agent-authored tasks of operating a
lived-in financial workspace - 6 personas x 4 stories x 5 levels.

- **Personas** (one directory each): `portfolio_manager`, `fund_operations`,
  `research_analyst`, `trading_desk`, `compliance_risk`, `client_advisor`.
  Each is a voice contract defined in `task_templates/<persona>/README.md`.
- **Stories**: four per persona, each a storyline in that person's day with a
  facts block as the single source of truth (`task_templates/<persona>/*.md`).
- **Levels**: every story climbs the same five-rung ladder, one difficulty
  dial per rung - `level0` Execute (everything stated), `level1` Find (target
  described, never named), `level2` Derive (a stated policy carries one hidden
  graded value), `level3` Ground (a knowledge source determines a graded fact;
  the world is populated and preservation-graded, including a stale twin of
  the target), `level4` Compose (build a backend, publish an app, instantiate
  it, use what was built).

Episodes run **closed-world** by default: the agent is not shown the initial
workspace state and must discover it through `get_workspace_snapshot`
(`WORKSPACE_BENCH_SHOW_INITIAL_STATE=1` restores the legacy open-world
prompt).

No script generated these tasks. They were authored by agents working under
the contracts in `.claude/skills/` (task-author, task-validator,
task-level-fairness, workspace-bench-tasks-orchestrator), certified by
oracle/no-op replay, and gated per persona on a gpt-4.1-mini calibration
staircase (three repeats; pooled 85/60/36/17/0 across the suite - see
`scripts/audits/calibrate_workspace_tasks.py` and
`runs/reports/workspace-tasks-calibration.json`). The model board is compiled
by `scripts/audits/compile_workspace_tasks_board.py` into
`runs/reports/workspace-tasks-board.json`.

```bash
# certify: oracle passes, no-op fails, quotas hold
uv run workspace-bench validate --suite workspace-tasks

# run a model
uv run python -m workspace_bench.reports.model_compare \
  --model openai:gpt-4.1-mini --suite workspace-tasks
```
