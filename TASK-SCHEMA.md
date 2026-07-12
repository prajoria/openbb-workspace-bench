# Task & Success Schema

Reference for authoring task JSON. See [README](README.md) for the
project overview and [CONTRIBUTING](CONTRIBUTING.md) for the authoring workflow.

Tasks are strict JSON objects under
`src/workspace_bench/task_suites/<suite>/<family>/`; private
`--task-dir` trees use the same schema. Unknown fields are rejected.

## Task fields

| field | contract |
| --- | --- |
| `id` | Stable local slug. The public identity is `suite/family/task`. |
| `category`, `family` | Required workflow kind (`read`, `single-widget`, `dashboard`, `platform`, or `repair`) and generator/verifier family. Neither is inferred from paths or tags. |
| `specification_level` | Structural prompt level: `explicit`, `partially-specified`, or `open-brief`. Written only when it deviates from the difficulty default (easy→explicit, medium→partially-specified, hard→open-brief). |
| `difficulty` | Measured `easy`, `medium`, or `hard` reporting label. |
| `split` | `train`, `validation`, `test`, or private-suite `dev`; otherwise the suite default, then `dev`. |
| `business_terms` | Optional declared allowlist of genuine verbatim business identifiers in less-specified prompts; omitted when empty. |
| `prompt` | Analyst-facing instruction. |
| `fixtures`, `initial_state` | Deterministic backend references and optional seeded dashboards, tabs, widgets, apps, generated widgets, or repair state. |
| `allowed_tools`, `limits` | Agent-visible Workspace MCP tool surface and budgets such as `max_turns`. |
| `success` | Evaluator-only deterministic `SuccessCriteria`. |
| `oracle_tool_calls` | Known-good reference trajectory; it is evidence, not the only valid solution. |
| `code_task` | Experimental code-track contract: confined starter/oracle paths, argv install/start/test commands, health path, timeouts, manifest requirements, and typed HTTP probes. |

`workspace-bench export-task` publishes prompt, business terms, metadata,
fixtures, initial state, tools, limits, protocol, suite hash, and Git
provenance. It deliberately excludes `success` and `oracle_tool_calls`.

`specification_level` and `difficulty` are independent. Specification level
controls prompt structure, openness linting, exact-versus-capability grading,
and graded-check caps. Difficulty is measured from calibration evidence and
never changes prompt rendering or grader selection. Explicit tasks can name a
complete implementation contract; partially specified tasks provide a business
outcome and one or two declared anchors; open briefs describe the user,
subject, actions, and genuine constraints while leaving ids, widget types,
paths, fields, tabs, and geometry to the agent.

## SuccessCriteria

| field | what it checks |
| --- | --- |
| `required_dashboard_name_contains`, `required_tabs` | Required active-dashboard phrase and tab ids. |
| `required_widgets` | Origin/widget id, subset-matched `data_args`, optional tab, and min/max instance counts. |
| `required_generated_widgets` | Type, optional name/tab, minimum count, and case-insensitive semantic `data_contains` facts. |
| `required_widget_defs`, `required_app_defs` | Exact custom-backend manifest contracts for structurally explicit tasks. |
| `required_capabilities` | Architecture-neutral business capability, bound to runtime datasets by widget kind, covered fields, parameter kinds, and business-significant config. |
| `capability_connections` | Required source/target capability edge through the final app's real shared-parameter graph. |
| `business_names`, `app_structure` | Opt-in business-critical dashboard/app/tab names and generic app/reference/layout integrity. |
| `required_layouts`, `layout` | Exact move/resize outcomes plus grid-bound and no-overlap invariants. |
| `required_tool_calls`, `required_tool_results`, `required_resource_reads` | Nested-subset call arguments and required fragments from successful tool results or exact resource URIs. |
| `runtime_checks` | Task-owned datasets and evaluator HTTP probes, with optional pinned paths and request timeout. |
| `polish` | Desirable authored details reported separately; never gates strict pass. |

A required capability names one or more `runtime_checks.datasets`, selects a
widget kind (`any`, table/grid/chart-like, metric, form, or a native content
kind), and may require fields, parameter kinds, and meaningful configuration.
Several runtime-valid widgets may jointly cover its fields; one combined widget
may cover compatible capabilities. Connections are derived from actual
`apps.json` shared-parameter groups, so group names and oracle ids are not
compared. Use `business_names` only when the literal name is part of the brief.

Each runtime dataset has a unique `name`, authored `widget_id`, field
vocabulary, JSON `payload`, and optional `path` or `form_endpoint`; negative
fixtures may provide `status` or `raw_body`. Paths are flexible unless
`pinned_paths` is true. The evaluator remaps the authored backend to its own
localhost server, synthesizes representative parameters, issues GET or POST,
and rejects unreachable/non-2xx endpoints, malformed or incompatible JSON,
empty placeholder data, invalid parameter schemas, and broken form submission
contracts.

For generated widgets, `data_contains` is the semantic contract. It searches
serialized data plus name, description, and tab id case-insensitively, with
supported aliases and numeric equivalence.

Oracle traces smoke-test task correctness and can bootstrap SFT/RL exports, but
the grader is the source of truth. For experimental `code_task` entries the
oracle is a solved-file overlay instead; paths cannot escape the task fixture,
commands are argv arrays, every manifest endpoint needs a typed probe, starter
tests must fail before implementation, and the oracle plus test-sensitivity
mutation must pass validation.

The simulator surface includes snapshot, dashboard/navigation, widget
discovery/data/create/update/layout/delete/read, generated-widget, backend/app,
skill/resource/prompt, and delegation tools. The complete per-task oracle-tool
matrix and generated task catalog live under `runs/reports/`.
