# Release Checklist

Use this checklist before announcing a public Workspace Bench release.

## Required

- [ ] `uv run --extra dev ruff check src tests scripts` passes.
- [ ] `uv run --extra dev mypy src scripts` passes.
- [ ] `uv run --extra dev pytest` passes.
- [ ] `uv run python scripts/audits/audit_task_identity.py` reports 0 findings across 338 tasks.
- [ ] `uv run python scripts/audits/report_prompt_stats.py` reports unique prompts within the documented per-taskset word caps.
- [ ] `uv run python scripts/audits/audit_release_consistency.py` reports zero stale active counts or cross-phase claims across release-facing docs, metadata, CLI text, CI, and tests.
- [ ] Workspace-tasks validation passes on the default Workspace with release checks green: `uv run workspace-bench validate --taskset workspace-tasks --min-tasks 120`.
- [ ] `uv run workspace-bench adversarial --taskset workspace-tasks` reports zero survivors, wrong-reason failures, and dirty oracles.
- [ ] `uv run workspace-bench run --agent oracle` passes every workspace-tasks task; the other tasksets prove oracle pass through their `validate` commands above.
- [ ] `uv run workspace-bench run --agent noop` fails every workspace-tasks task; the taskset validations prove their own no-op baselines.
- [ ] `uv run --extra dev workspace-bench export-task --task workspace-tasks/research_analyst/earnings_prep_level0 --output /tmp/workspace-task.json` succeeds.
- [ ] `uv run --extra dev workspace-bench run-agent-command --task workspace-tasks/portfolio_manager/morning_briefing_level0 --agent-command "python -m workspace_bench.agents.rule_agent"` passes.
- [ ] `uv run workspace-bench report --taskset workspace-tasks --output runs/reports/benchmark-report.md` succeeds.
- [ ] `uv run --extra live python scripts/audits/audit_hosted_surface.py` reports no missing tools, prompts, or resources against the hosted Workspace MCP (needs `WORKSPACE_MCP_TOKEN` in `.env`).
- [ ] Stable task counts: 80 in `smoke`, 138 in `enterprise-apps-default`, exactly 120 in `workspace-tasks` (338 tasks total).
- [ ] Novelty fingerprints and task ids are unique in the quota-checked taskset.
- [ ] Coverage quotas pass via `validate` (workspace-tasks: backend, difficulty, widget-pair, dashboard-category, grader-check quotas).
- [ ] `runs/reports/workspace-tasks-board.json` and `workspace-tasks-calibration.json`/`.md` match the README board notes (raw run directories are not committed); any recomputation requires re-running the models against the current tasksets.
- [ ] README quick start, tasksets table, and aggregate command are accurate.
- [ ] Per-taskset READMEs are present, use the shared structure, and state task counts verified by `audit_release_consistency.py`.
- [ ] `runs/reports/task-catalog.md` is regenerated and covers all three deterministic simulator tasksets; `tool-coverage-matrix.md` and `tool-matrix-data.json` are regenerated beside it.
- [ ] Root `CONTRIBUTING.md` explains how to add tasks and tasksets.
- [ ] Repository URL in `pyproject.toml` is correct.
- [ ] The smoke taskset sweeps green through live-parity against the hosted Workspace MCP bridge (`uv run --extra live workspace-bench live-parity --task smoke/get_widget_data/smoke_get_widget_data_level0` per eligible task) — the strongest harness-fidelity evidence the repo produces.
- [ ] The answer judge is calibrated against the pinned local judge model: `uv run python scripts/audits/audit_judge_calibration.py --repeats 3` passes (all exemplars PASS; shallow, off-topic, and injection mutants FAIL; verdicts stable). Local gate — CI stays deterministic-only.
- [ ] `LICENSE` (MIT) is present and the README badge matches.
- [ ] `uv lock --check` passes and `uv build` produces both sdist and wheel.
- [ ] CI is green.

## Strongly Recommended Before Wider Launch

- [ ] Add at least one real Workspace MCP sidecar parity run.
- [ ] Add a hidden taskset.
- [ ] Add an optional Docker or compose workflow for fixture backend serving.
- [ ] Publish a short benchmark report with coverage, baselines, and limitations.

## Claims to Avoid Until Verified

- Do not claim live OpenBB Workspace execution: the harness runs the deterministic simulator plus the MCP sidecar smoke and live-parity paths, never the real product UI.
- Do not claim financial reasoning coverage beyond the included deterministic fixture domains.
