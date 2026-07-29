# Integrations

Adapters that run Workspace Bench tasks inside external harnesses while the
native task JSON, simulator, and grader stay authoritative.

## `harbor/`

The [Harbor](https://harborframework.com/) adapter behind the
`workspace-bench export-harbor` CLI command (see the Harbor Adapter section of
the top-level README for usage):

- `exporter.py` — materializes one canonical task as a self-contained Harbor
  task directory under `build/harbor/`, archiving the `workspace-mcp`
  sidecar's committed `HEAD` alongside it.
- `bundle.py` — sealed task-bundle loading shared by the runtime and
  verifier.
- `runtime.py` — the trusted in-container runtime: the task-aware MCP gateway
  the agent talks to, the browser bridge, and the episode recorder.
- `artifacts.py` — trusted episode artifact helpers (finalized after the
  agent stops).
- `verifier.py` — replays the recorded episode through the existing
  `grade_task` implementation in a separate verifier context, keeping the
  sealed evaluator and reference trace out of the agent's reach.

Tests live in `tests/test_harbor_integration.py` and
`tests/test_harbor_runtime.py`.
