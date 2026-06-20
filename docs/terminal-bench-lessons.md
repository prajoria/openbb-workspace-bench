# Terminal-Bench Lessons for Workspace Bench

This document captures the Terminal-Bench/Harbor ideas worth adopting now, without turning Workspace Bench into a full container benchmark or requiring product rewrites.

## Adopted Now

### 1. Task Metadata

Terminal-Bench tasks are easy to browse because they have difficulty, tags, and categories. Workspace Bench uses more explicit axes:

- `level`
- `capability`
- `workflow`
- `domain`
- `subdomain`
- `difficulty`
- `tags`
- `source`

High ROI: lets us build subsets such as `--level L2 --tag multi-widget`, compare by Workspace capability, compare by finance workflow, and create benchmark cards.

Low effort: pure scenario JSON and CLI changes.

### 2. Dataset Manifest

`workspace-bench manifest --json` emits a machine-readable dataset card:

- benchmark name/version
- canary GUID
- scenario count
- levels/capabilities/workflows/domains/subdomains/difficulties/tags
- per-scenario summaries

High ROI: useful for leaderboards, regression dashboards, and published eval artifacts.

Low effort: derived from existing scenario metadata.

### 3. Validation Command

`workspace-bench validate` checks:

- scenario metadata hygiene
- oracle trace passes
- no-op baseline fails

High ROI: prevents weak or broken scenarios from entering the benchmark.

Low effort: reuses existing runner and graders.

### 4. Filtering

`workspace-bench list` and `workspace-bench run` support:

- `--level`
- `--capability`
- `--workflow`
- `--domain`
- `--subdomain`
- `--difficulty`
- `--tag`

High ROI: needed for small eval slices, curricula, and RL subsets.

Low effort: in-memory filtering over loaded scenarios.

### 5. Aggregate Result Summaries

Run JSON now includes:

- total/passed/failed
- mean score
- pass counts by level
- per-scenario metadata

High ROI: makes local runs closer to leaderboard-ready artifacts.

Low effort: computed from existing `RunResult` objects.

### 6. Contamination Canary

Workspace Bench now includes a canary GUID exposed by:

```bash
workspace-bench canary
```

High ROI: establishes an anti-contamination norm early.

Low effort: one constant and a CLI command.

### 7. Task Envelope Export

`workspace-bench export-task` writes a public agent-facing task envelope. It includes the prompt, metadata, fixtures, initial state, allowed tools, and output protocol, while excluding success criteria and oracle traces.

High ROI: makes scenarios portable and clarifies the evaluated-agent contract.

Low effort: derived from existing scenario JSON.

### 8. External Agent Command

`workspace-bench run-agent-command` evaluates any command that writes JSONL tool calls. This is the first BYO-agent contract.

High ROI: agent teams can benchmark their own systems without importing package internals.

Low effort: reuses the simulator, trace format, and graders.

### 9. Private Task Packs

Most commands now accept `--scenario-dir`, so teams can run private scenario packs with the same validation and grading commands as the public benchmark.

High ROI: lets users bring their own data and workflows.

Low effort: loads scenario JSON from a directory.

## Defer For Now

### Docker-First Execution

Terminal-Bench uses containers as the main isolation boundary. Workspace Bench should eventually support this, but the simulator is more useful for rapid iteration and RL rollouts today.

Recommended next step: provide an optional `Dockerfile` and compose file for fixture backend smoke tests, not full mandatory Docker execution.

### Public Leaderboard

Leaderboard submission rules require stable task release, anti-contamination policy, versioned results, and external reproducibility. Workspace Bench is not ready for that yet.

Recommended next step: save result JSON artifacts with `workspace-bench run --json` and trace artifacts with `--trace-dir`.

### Full ATIF/SFT Export

Harbor has mature trace export paths for SFT. Workspace Bench traces are already structured, but not a conversation format.

Recommended next step: add a small converter from trace JSON to a ShareGPT-style or ATIF-like format once real model rollouts are available.

### Interactive Model Runner

The external-agent command still evaluates trace-producing agents. For local
model baselines, `workspace-bench compare-models` now runs an interactive loop
backed by `WorkspaceEpisode.step`, so the model can observe after every tool
call.

Recommended next step: reuse the same episode API and the live sidecar bridge
mapping to expose the simulator as an MCP server for arbitrary external agents.

## Practical Takeaway

The winning pattern is not "copy Terminal-Bench." It is:

1. keep Workspace Bench domain-specific and MCP-native
2. add Terminal-Bench-style hygiene around task metadata, validation, slicing, results, and contamination
3. defer container/cloud/leaderboard work until the benchmark has real model baselines and hidden/generated splits
