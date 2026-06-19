# WorkspaceBench Eval-to-Training Platform Roadmap

## Summary

Build this in three milestones, with **Eval Platform** first:

1. **Eval Platform Core**: make WorkspaceBench a credible, repeatable benchmark with splits, repeated-run reliability metrics, hidden/private packs, and cleaner model comparison.
2. **Trace/Data Export**: turn successful and failed rollouts into portable training/evaluation datasets.
3. **Gym/RL Adapter**: expose the same benchmark core through a Gymnasium-style environment for RL and rollout collection.

WorkspaceBench remains the source of truth. Gym, SFT, and RL integrations are adapters on top.

## Milestone 1: Eval Platform Core

- Promote `examples/compare_models.py` into a first-class CLI command, likely `workspace-bench compare-models`.
- Keep the current interactive runner behavior as default.
- Add official repeated-run metrics:
  - `pass_rate`: strict per-attempt pass rate, process failures count as failed.
  - `task_pass_rate`: pass rate excluding provider/process failures.
  - `pass@k`: a scenario passes if any of `k` attempts passes.
  - `pass^k`: a scenario passes only if all of `k` attempts pass.
  - `mean_score`: average partial-credit score across attempts.
- Add result JSON fields:
  - `attempt_count`
  - `repeats`
  - `valid_attempts`
  - `process_failures`
  - `task_failures`
  - `pass_at_k`
  - `pass_power_k`
- Add scenario split support:
  - Optional scenario field: `"split": "dev" | "validation" | "test" | "train"`.
  - Existing bundled scenarios default to `"dev"` if missing.
  - CLI filter: `--split dev|validation|test|train`.
- Add task-pack manifest support:
  - Optional `task_pack.json` in scenario directories.
  - Fields: `pack_id`, `release_id`, `version`, `visibility`, `default_split`, `description`.
  - `visibility` values: `public`, `private`, `hidden`.
- Improve private/hidden pack flow:
  - Existing `--scenario-dir` remains supported.
  - Hidden packs can be evaluated locally without exposing prompts/success criteria in public result summaries.
  - Public reports include scenario IDs and scores; hidden reports can redact prompt/success details.
- Add comparison report upgrades:
  - Charts can use `pass-rate`, `task-pass-rate`, `pass-at-k`, `pass-power-k`, or `mean-score`.
  - `analysis.md` includes reliability table when `--repeats > 1`.
  - Failure tables separate task issues from provider/process failures.

## Milestone 2: Trace And Training Data Export

- Add canonical rollout artifact schema:
  - `task`
  - `messages`
  - `tool_calls`
  - `tool_results`
  - `final_snapshot`
  - `grade`
  - `metadata`
- Add CLI command: `workspace-bench export-rollouts`.
  - Inputs: comparison run directory, trace directory, or oracle traces.
  - Outputs: normalized rollout JSONL.
- Add CLI command: `workspace-bench export-sft`.
  - Formats:
    - `sharegpt`
    - `openai_messages`
    - `tool_call_jsonl`
  - Default includes only passing attempts.
  - Option `--include-failures` includes failed attempts with grade metadata.
- Add CLI command: `workspace-bench export-preferences`.
  - Creates pairs from repeated attempts on the same scenario:
    - chosen: passing or higher-score trace
    - rejected: failing or lower-score trace
- Keep training data export separate from benchmark publishing.
  - Public benchmark scenarios and oracle traces should not automatically become training data unless explicitly exported.

## Milestone 3: Gym/RL Adapter

- Add optional dependency group: `gym`.
  - Includes `gymnasium`.
- Add `WorkspaceGymEnv`.
  - Location: `workspace_bench.envs`.
  - Core methods:
    - `reset(seed=None, options=None)`
    - `step(action)`
    - `close()`
    - `render()`
- Use structured JSON action format:
  - `{"tool": "create_widget", "args": {...}}`
- Observation format:
  - `task`
  - `allowed_tools`
  - `last_tool_result`
  - `snapshot`
  - `turn_index`
  - `remaining_turns`
- Reward behavior:
  - Default sparse reward: final grade score at episode end.
  - Optional process reward:
    - valid tool call bonus
    - invalid tool call penalty
    - schema-before-create bonus
    - repeated snapshot penalty
- Done/truncated behavior:
  - `done=True` when model emits a configured done action or scenario satisfies success.
  - `truncated=True` when max turns is reached.
- Add vectorized rollout helper later, not in the first Gym implementation.

## Public Interfaces To Add

- CLI:
  - `workspace-bench compare-models`
  - `workspace-bench export-rollouts`
  - `workspace-bench export-sft`
  - `workspace-bench export-preferences`
- Scenario schema:
  - optional `split`
- Task pack manifest:
  - optional `task_pack.json`
- Python:
  - `workspace_bench.envs.WorkspaceGymEnv`
  - `workspace_bench.exports.RolloutRecord`
  - `workspace_bench.metrics.compute_reliability_metrics`

## Test Plan

- Unit tests:
  - split parsing defaults to `dev`
  - `--split` filters bundled and private scenarios correctly
  - `pass@k` and `pass^k` calculations are correct
  - process failures are excluded from `task_pass_rate`
  - hidden task-pack summaries redact prompt/success fields
  - rollout export preserves message/tool/result ordering
  - SFT export emits valid target formats
  - Gym env reset/step/done/truncated behavior is deterministic
- Integration tests:
  - `workspace-bench validate --scenario-dir ...`
  - `workspace-bench compare-models --repeats 2 --metric pass-at-k`
  - `workspace-bench export-sft --only-passing`
  - oracle traces still pass all bundled scenarios
  - noop baseline still fails all bundled scenarios
- Acceptance criteria:
  - Existing 25-scenario validation still passes.
  - Existing agent command contract remains backward compatible.
  - Reports clearly distinguish task failures from process failures.
  - A repeated run can answer: "How reliable is this model across attempts?"

## Assumptions

- First priority is **benchmark credibility**, not full RL training.
- WorkspaceBench remains the main package identity.
- Gymnasium is an optional adapter, not the core abstraction.
- Existing public scenarios stay usable without adding split metadata immediately.
- Hidden/private packs are local-directory based first; remote registry support is out of scope for the first pass.
