# `smoke` task suite

Tasks: 20

## Purpose

A pass means the agent can complete one minimal, observable round trip for each canonical Workspace MCP tool or knowledge surface without changing any seeded enterprise-app dashboard.

## Workspace baseline

The manifest declares `default-v1` because these tasks verify the tools against the same 23-dashboard default workspace users receive, including the requirement that targeted smoke mutations leave the seeded enterprise-app dashboards intact.

## Generation method

`ai-authored-direct`. Tasks are written directly in `scripts/generators/generate_smoke_suite.py`, with no scaling step; the generator deterministically certifies and rewrites the suite.

## Axes

Family names are the target Workspace MCP tool or knowledge surface, with one task per family. Category describes the outcome shape, difficulty is intentionally fixed at easy, and specification level is explicit because every prompt names the small requested operation.

| Axis | File-derived counts |
| --- | --- |
| `family` | 20 families, 1 task each: `add_generative_widget`, `assign_tasks_to_agents`, `create_widget`, `delete_widget`, `get_params_options`, `get_skill_content`, `get_widget_data`, `get_widget_schema`, `get_workspace_prompt`, `get_workspace_snapshot`, `list_available_widgets`, `manage_apps`, `manage_backends`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `read_widget`, `read_workspace_resource`, `update_widget`, `update_widget_layout` |
| `category` | `read` 9; `single-widget` 5; `dashboard` 4; `platform` 2 |
| `difficulty` | `easy` 20 |
| `specification_level` | `explicit` 20 |

## Gates

Generation requires the reference trace to pass, the no-op trace to fail, exactly one call to the target family tool, no more than four graded checks, and no mutation of a seeded enterprise-app dashboard. `workspace-bench validate --suite smoke` rechecks schema validity, reference success, and no-op failure.

## Limitations

This is a harness-fidelity suite, not broad workflow coverage. Pure reads have no durable state outcome, so smoke alone permits argument-matched trace checks for those reads. `assign_tasks_to_agents` only verifies that the request envelope round-trips; it does not prove downstream work. The live sidecar cannot replay registry mutations or the agent-envelope echo, so live eligibility is narrower than simulator eligibility.

### Live eligibility

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
| `manage_backends` | no | backend registry mutation and listing are not replayed |
| `manage_apps` | no | app registry changes and instantiation are not replayed |
| `get_skill_content` | yes | |
| `read_workspace_resource` | yes | |
| `get_workspace_prompt` | yes | |
| `assign_tasks_to_agents` | no | agent-envelope echoes are not replayed |
