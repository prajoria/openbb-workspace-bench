# `smoke` taskset

Tasks: 80

## Purpose

A pass means the agent can complete one minimal, observable round trip for
each canonical Workspace MCP tool or knowledge surface, at every rung of a
four-level execution ladder, without changing any seeded baseline dashboard.

## Ladder

Every tool family appears once per level, and each rung changes exactly one
variable — first the tool surface, then the workspace state, then prompt
openness — so a score delta between adjacent levels isolates one capability:

| level | allowed tools | workspace baseline | prompt | max turns |
| --- | --- | --- | --- | --- |
| `level0` | the target tool only | `""` (bare workspace) | declarative | 1 |
| `level1` | full tool surface | `""` (bare workspace) | declarative | 2 |
| `level2` | full tool surface | `stark-onboard-a` | declarative | 2 |
| `level3` | full tool surface | `stark-onboard-a` | open — business intent, no widget ids | 4 |

## Workspace axes

Every task declares its axes explicitly: the Stark data world
`stark-enterprise-x` as the connected backend (the `list_available_widgets`
family also connects `getting-started` to smoke the multi-origin path), the
six Daloopa skills, and — on `level2`/`level3` — the `stark-onboard-a`
initial state. Read and mutation families are spread across different Stark
apps rather than pinning one widget.

Task files hold to the smoke field profile: only `id`, `family`,
`difficulty`, `prompt`, `setup` (the workspace axes, `allowed_tools`, and —
solely in tasks that seed a mutation target — `initial_state`), and `eval`
(grading criteria plus the `reference_trace` trajectory and the
harness-enforced `max_turns`). Call-graded families set
`calls_match_reference: true` instead of duplicating the reference as
explicit required calls: each reference call is graded as written except
steps annotated `optional` (skippable discovery) or narrowed by
`graded_args`. `category` is derived from the family by the loader;
`fixtures`, `business_terms`, and `specification_level` never appear.

Agents see only the prompt and the setup block. The entire `eval` block is
sealed: grading criteria, the reference trajectory, and the turn budget are
never exported, and the harness refuses calls past `max_turns` — agents are
expected to pursue the fastest outcome, not pace themselves.

## Generation method

`ai-authored-direct`. Tasks are written directly in
`scripts/generators/generate_smoke_suite.py`, with no scaling step; the
generator deterministically certifies and rewrites the taskset.

## Axes

Family names are the target Workspace MCP tool or knowledge surface, with one
task per family per level. The specification level is left to the loader's
defaults: `level0`–`level2` are explicit, `level3` is partially specified.

| Axis | File-derived counts |
| --- | --- |
| `family` | 20 families, 4 tasks each: `add_generative_widget`, `assign_tasks_to_agents`, `create_widget`, `delete_widget`, `get_params_options`, `get_skill_content`, `get_widget_data`, `get_widget_schema`, `get_workspace_prompt`, `get_workspace_snapshot`, `list_available_widgets`, `manage_apps`, `manage_backends`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `read_widget`, `read_workspace_resource`, `update_widget`, `update_widget_layout` |
| `category` (derived) | `read` 36; `single-widget` 20; `dashboard` 16; `platform` 8 |
| `difficulty` | `level0` 20; `level1` 20; `level2` 20; `level3` 20 |

## Gates

Generation requires the reference trace to pass, the no-op trace to fail,
exactly one call to the target family tool, no more than six graded checks,
the per-level tool-surface and baseline contract, and no mutation of a seeded
baseline dashboard. `workspace-bench validate --taskset smoke` rechecks schema
validity, reference success, no-op failure, and the smoke field profile
(field allowlist, no redundant defaults, level contract, one task per family
per level, explicit workspace axes).

## Limitations

This is a harness-fidelity taskset, not broad workflow coverage. Pure reads
have no durable state outcome, so smoke alone permits argument-matched trace
checks for those reads. `assign_tasks_to_agents` only verifies that the
request envelope round-trips; it does not prove downstream work. The live
sidecar cannot replay registry mutations or the agent-envelope echo, so live
eligibility is narrower than simulator eligibility.

### Live eligibility

Eligibility is evaluated per task; `level0` rows are representative for the
family (higher levels replay the same target call plus read-only discovery).

| Tool or surface | Eligible | Reason when excluded |
| --- | --- | --- |
| `get_workspace_snapshot` | yes | |
| `manage_dashboard` | yes | |
| `manage_navigation_bar` | yes | |
| `navigate_workspace` | yes | |
| `list_available_widgets` | yes | |
| `get_widget_schema` | yes | |
| `get_params_options` | yes | |
| `get_widget_data` | yes | |
| `create_widget` | yes | |
| `update_widget` | yes | |
| `update_widget_layout` | yes | |
| `delete_widget` | yes | |
| `add_generative_widget` | yes | |
| `read_widget` | yes | |
| `manage_backends` | yes | list operation is read-only against a production workspace |
| `manage_apps` | no | app registry changes and instantiation are not replayed |
| `get_skill_content` | yes | |
| `read_workspace_resource` | yes | |
| `get_workspace_prompt` | yes | |
| `assign_tasks_to_agents` | no | agent-envelope echoes are not replayed |
