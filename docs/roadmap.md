# WorkspaceBench Roadmap

WorkspaceBench is a benchmark-first platform for testing agents that operate on
OpenBB Workspace state. The benchmark core is the source of truth for tasks,
workspace simulation, tool calls, grading, and results.

## 1. Repo Organization And Documentation

- Keep the CLI at `workspace_bench.cli`.
- Keep the package root small. Use `workspace_bench.__init__` for a few common
  convenience exports and put implementation modules inside focused packages.
- Organize implementation code into focused packages:
  - `core`: scenarios, episodes, runner, models, grading
  - `workspace`: simulator, fixtures, live MCP smoke bridge
  - `agents`: oracle/noop agents, JSONL command protocol, model adapter helpers
  - `reports`: model comparison, metrics, charts
  - `exports`: rollout, SFT, preference, and trace export logic
  - `rl`: Gym-style environment and RL helpers

## 2. Benchmark Core Hardening

- Keep scenarios explicit about prompt, fixtures, allowed tools, limits, split,
  tags, oracle calls, and deterministic success criteria.
- Support public, private, and hidden task packs through local scenario
  directories and `task_pack.json`.
- Validate that oracle passes, noop fails, scenario metadata is complete, and
  malformed scenarios fail with useful messages.
- Keep strict pass/fail separate from partial score and preserve stable issue
  codes.

## 3. Agent Harness And Model Comparison

- Keep JSONL tool calls as the common external-agent contract.
- Maintain example adapters for Ollama, GPT-4.1, and a rule-based JSONL agent.
- Support repeated runs, live colored PASS/FAIL output, timestamped run
  directories, JSON reports, Markdown analysis, SVG charts, and PNG charts.
- Report pass rate, task pass rate, mean score, pass@k, and pass^k.

## 4. Export And Dataset Layer

- Use a canonical rollout schema with task, messages, tool calls, tool results,
  final snapshot, grade, and metadata.
- Export canonical rollouts, SFT records, and chosen/rejected preference pairs.
- Include passing attempts by default and failed attempts only when explicitly
  requested.
- Keep training data export separate from benchmark publishing.

## 5. RL Adapter

- Expose `WorkspaceGymEnv` as an optional Gym-style wrapper around the benchmark.
- Use structured JSON actions: `{"tool": "tool_name", "args": {...}}`.
- Return observations with task, allowed tools, last tool result, snapshot,
  turn index, and remaining turns.
- Keep rewards configurable between sparse final grade and process rewards.

## 6. Training Platform Foundations

- Version exported datasets with benchmark release, scenario pack, model, run
  timestamp, and export schema version.
- Provide recipes for SFT, preference optimization, and RL rollout collection.
- Do not add heavyweight trainer dependencies to the base package.

## 7. Public Readiness

- Keep README quickstarts current.
- Maintain docs for scenario building, agent adapters, export formats, private
  task packs, and benchmark limitations.
- Validate the bundled 300-scenario release before releases.
- Make benchmark results reproducible, explainable, and safe to compare.
