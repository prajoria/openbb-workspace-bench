# WorkspaceBench Scenario Catalog

Auto-generated from the bundled scenario JSON files — regenerate with
`python scripts/generate_scenario_catalog.py` after editing scenarios.

## How grading works

Every criterion below becomes one or more boolean checks in `grade_scenario`
(`src/workspace_bench/core/graders.py`):

- **Strict pass** requires *every* check to pass. One failed check fails the scenario.
- **Score** is partial credit: `checks_passed / checks_total`.
- Each failed check emits a stable **issue code** (shown per criterion below), so
  failures aggregate meaningfully across runs.
- For external agent runs, a **process failure** (non-zero exit, timeout, unparseable
  tool-call output) also fails the attempt regardless of state.
- Widget `data_args` use **nested subset matching**: extra args are fine, expected keys
  must match exactly.
- Generated-widget and tool-result content checks are **case-insensitive** and accept
  widget-name aliases ("price_performance" ≈ "price performance") and numeric
  equivalence (0.5 ≈ 50%).
- The **no-op baseline score** shown per scenario is the partial credit an agent gets for
  doing nothing — the gap to 1.0 is what the scenario actually demands. Release gates
  require the no-op to *fail* every scenario and the oracle trace to *pass* every one.

## Pack: workspace-bench-v1 (300 scenarios)

### L0 — Inspect & answer (28)

#### `gen_t0_inspect_read_holdings_table_2` — Inspect Holdings Table

**L0** · workspace-inspection · workflow: portfolio-risk-review · portfolio-management · difficulty: easy · split: train · no-op baseline score: 0.600

> Call read_widget with widget_id holdings_table for the existing Bench Portfolio/holdings_table widget, then add a note mentioning holdings.

- Novelty: Unique inspect/t0 exercise using add_generative_widget, get_workspace_snapshot, read_widget with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, repeated_snapshots, too_many_invalid_calls on portfolio; artifact generated:note@*:holdings.
- Fixture backends: portfolio
- Initial workspace: dashboard "Inspect Board"; 1 seeded widget(s): holdings_table({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "holdings" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `read_widget` with args ⊇ {"widget_id": "holdings_table"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_inspect_read_macro_timeseries_1` — Inspect Macro Timeseries

**L0** · workspace-inspection · workflow: macro-rates-review · macro · difficulty: easy · split: train · no-op baseline score: 0.600

> After calling read_widget with widget_id macro_timeseries for the existing Bench Macro/macro_timeseries widget, add a note mentioning DGS10.

- Novelty: Unique inspect/t0 exercise using add_generative_widget, get_workspace_snapshot, read_widget with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, repeated_snapshots, too_many_invalid_calls on macro; artifact generated:note@*:DGS10.
- Fixture backends: macro
- Initial workspace: dashboard "Inspect Board"; 1 seeded widget(s): macro_timeseries({"series": "DGS10"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "DGS10" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `read_widget` with args ⊇ {"widget_id": "macro_timeseries"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_inspect_read_portfolio_command_center_overview_workflow_overview_3` — Inspect Workflow Overview

**L0** · workspace-inspection · workflow: portfolio-morning-review · portfolio-management · difficulty: easy · split: train · no-op baseline score: 0.750

> Call read_widget with widget_id portfolio_command_center_overview_workflow_overview for the existing Bench Stark Enterprise/portfolio_command_center_overview_workflow_overview widget, then add a note mentioning stark.

- Novelty: Unique inspect/t0 exercise using add_generative_widget, get_workspace_snapshot, read_widget with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/strategy_health_monitor_themes_crowded_names@; generated:note@*:stark.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Inspect Board"; 2 seeded widget(s): portfolio_command_center_overview_workflow_overview({}), strategy_health_monitor_themes_crowded_names({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_themes_crowded_names` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "stark" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `read_widget` with args ⊇ {"widget_id": "portfolio_command_center_overview_workflow_overview"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_inspect_read_price_performance_0` — Inspect Price Performance

**L0** · workspace-inspection · workflow: equity-tearsheet · equity-research · difficulty: easy · split: validation · no-op baseline score: 0.600

> Use read_widget with widget_id price_performance to inspect the existing Bench Equities/price_performance widget, then add a note mentioning AAPL.

- Novelty: Unique inspect/t0 exercise using add_generative_widget, get_workspace_snapshot, read_widget with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, repeated_snapshots, too_many_invalid_calls on equities; artifact generated:note@*:AAPL.
- Fixture backends: equities
- Initial workspace: dashboard "Inspect Board"; 1 seeded widget(s): price_performance({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "AAPL" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `read_widget` with args ⊇ {"widget_id": "price_performance"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_prompts_fetch_workspace_session_context_1` — Fetch Prompt workspace_session_context

**L0** · prompt-access · workflow: workspace-guidance · mcp-prompts · difficulty: easy · split: train · no-op baseline score: 0.571

> Call get_workspace_prompt with name workspace_session_context and add a note mentioning current-dashboard current-tab session grounding.

- Novelty: Unique prompts/t0 exercise using add_generative_widget, get_workspace_prompt, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on equities, portfolio; artifact prompts:workspace_session_context; widgets:Bench Portfolio/holdings_table@; generated:note@*:current-dashboard.
- Fixture backends: equities, portfolio
- Initial workspace: dashboard "Prompt Review"; 1 seeded widget(s): holdings_table({})
- Allowed tools (3): `get_workspace_snapshot`, `get_workspace_prompt`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "current-dashboard" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_session_context"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_workspace_prompt` must contain "current-dashboard current-tab session grounding" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_prompts_fetch_workspace_session_context_3` — Fetch Prompt workspace_session_context

**L0** · prompt-access · workflow: workspace-guidance · mcp-prompts · difficulty: easy · split: train · no-op baseline score: 0.571

> Use get_workspace_prompt with name workspace_session_context, then add a note mentioning current-dashboard current-tab session grounding.

- Novelty: Unique prompts/t0 exercise using add_generative_widget, get_workspace_prompt, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on equities, portfolio; artifact prompts:workspace_session_context; widgets:Bench Portfolio/sector_exposure@; generated:note@*:current-dashboard.
- Fixture backends: equities, portfolio
- Initial workspace: dashboard "Prompt Review"; 1 seeded widget(s): sector_exposure({})
- Allowed tools (3): `get_workspace_snapshot`, `get_workspace_prompt`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "current-dashboard" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_session_context"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_workspace_prompt` must contain "current-dashboard current-tab session grounding" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_prompts_fetch_workspace_tool_usage_0` — Fetch Prompt workspace_tool_usage

**L0** · prompt-access · workflow: workspace-guidance · mcp-prompts · difficulty: easy · split: train · no-op baseline score: 0.571

> Use get_workspace_prompt with name workspace_tool_usage, then add a note mentioning schema-before-create workspace tool discipline.

- Novelty: Unique prompts/t0 exercise using add_generative_widget, get_workspace_prompt, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on equities, portfolio; artifact prompts:workspace_tool_usage; widgets:Bench Portfolio/risk_metrics@; generated:note@*:schema-before-create.
- Fixture backends: equities, portfolio
- Initial workspace: dashboard "Prompt Review"; 1 seeded widget(s): risk_metrics({})
- Allowed tools (3): `get_workspace_snapshot`, `get_workspace_prompt`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "schema-before-create" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_tool_usage"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_prompts_fetch_workspace_tool_usage_2` — Fetch Prompt workspace_tool_usage

**L0** · prompt-access · workflow: workspace-guidance · mcp-prompts · difficulty: easy · split: validation · no-op baseline score: 0.571

> Use get_workspace_prompt with name workspace_tool_usage, then add a note mentioning schema-before-create workspace tool discipline.

- Novelty: Unique prompts/t0 exercise using add_generative_widget, get_workspace_prompt, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on equities, portfolio; artifact prompts:workspace_tool_usage; widgets:Bench Portfolio/holdings_table@; generated:note@*:schema-before-create.
- Fixture backends: equities, portfolio
- Initial workspace: dashboard "Prompt Review"; 1 seeded widget(s): holdings_table({})
- Allowed tools (3): `get_workspace_snapshot`, `get_workspace_prompt`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "schema-before-create" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_tool_usage"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_resources_skill_finance_comps` — Read Skill Resource finance-comps

**L0** · resource-access · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.333

> Call read_workspace_resource with uri openbb://workspace/skills/finance-comps, then add a note mentioning peer set.

- Novelty: Unique resources/t0 exercise using add_generative_widget, get_workspace_snapshot, read_workspace_resource with checks layout_out_of_grid, missing_generated_widget, missing_resource_read, too_many_invalid_calls on equities; artifact resource:openbb://workspace/skills/finance-comps; generated:note@*:peer set.
- Fixture backends: equities
- Initial workspace: dashboard "Resource Review"
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "peer set" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/skills/finance-comps` must contain "Comps workflow" (agent must actually retrieve the resource) → `missing_resource_read`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_resources_skill_finance_earnings_prep` — Read Skill Resource finance-earnings-prep

**L0** · resource-access · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.333

> Use read_workspace_resource with uri openbb://workspace/skills/finance-earnings-prep and add a note mentioning surprise drivers.

- Novelty: Unique resources/t0 exercise using add_generative_widget, get_workspace_snapshot, read_workspace_resource with checks layout_out_of_grid, missing_generated_widget, missing_resource_read, too_many_invalid_calls on equities; artifact resource:openbb://workspace/skills/finance-earnings-prep; generated:note@*:surprise drivers.
- Fixture backends: equities
- Initial workspace: dashboard "Resource Review"
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "surprise drivers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/skills/finance-earnings-prep` must contain "Earnings prep workflow" (agent must actually retrieve the resource) → `missing_resource_read`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_resources_skill_finance_guidance_tracker` — Read Skill Resource finance-guidance-tracker

**L0** · resource-access · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.333

> After calling read_workspace_resource with uri openbb://workspace/skills/finance-guidance-tracker, add a note mentioning management claims.

- Novelty: Unique resources/t0 exercise using add_generative_widget, get_workspace_snapshot, read_workspace_resource with checks layout_out_of_grid, missing_generated_widget, missing_resource_read, too_many_invalid_calls on equities; artifact resource:openbb://workspace/skills/finance-guidance-tracker; generated:note@*:management claims.
- Fixture backends: equities
- Initial workspace: dashboard "Resource Review"
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "management claims" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/skills/finance-guidance-tracker` must contain "Guidance tracker workflow" (agent must actually retrieve the resource) → `missing_resource_read`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_resources_skill_finance_tearsheet` — Read Skill Resource finance-tearsheet

**L0** · resource-access · workflow: equity-tearsheet · equity-research · difficulty: easy · split: validation · no-op baseline score: 0.333

> Use read_workspace_resource with uri openbb://workspace/skills/finance-tearsheet and add a note mentioning valuation.

- Novelty: Unique resources/t0 exercise using add_generative_widget, get_workspace_snapshot, read_workspace_resource with checks layout_out_of_grid, missing_generated_widget, missing_resource_read, too_many_invalid_calls on equities; artifact resource:openbb://workspace/skills/finance-tearsheet; generated:note@*:valuation.
- Fixture backends: equities
- Initial workspace: dashboard "Resource Review"
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "valuation" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/skills/finance-tearsheet` must contain "Tearsheet workflow" (agent must actually retrieve the resource) → `missing_resource_read`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_note_fact_close_aapl` — Grounded Note: Close Aapl

**L0** · workspace-inspection · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.800

> Review the existing AAPL price widget and add a note with the latest close from the data.

- Novelty: Unique note/t1 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/price_performance@*; generated:note@*:AAPL,196.10.
- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): price_performance({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "AAPL", "196.10" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_note_fact_close_msft` — Grounded Note: Close Msft

**L0** · workspace-inspection · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.800

> Use the existing MSFT price widget data to add a note with the latest close from the data.

- Novelty: Unique note/t1 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/price_performance@*; generated:note@*:MSFT,451.25.
- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): price_performance({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "MSFT", "451.25" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_note_fact_macro_10y` — Grounded Note: Macro 10Y

**L0** · workspace-inspection · workflow: macro-rates-review · macro · difficulty: medium · split: validation · no-op baseline score: 0.800

> Use the existing 10Y series widget data to add a note with the series id and its latest value from the data.

- Novelty: Unique note/t1 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls on macro; artifact widgets:Bench Macro/macro_timeseries@*; generated:note@*:DGS10,4.16.
- Fixture backends: macro
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): macro_timeseries({"series": "DGS10"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "DGS10", "4.16" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_note_fact_top_holding` — Grounded Note: Top Holding

**L0** · workspace-inspection · workflow: portfolio-risk-review · portfolio-management · difficulty: medium · split: test · no-op baseline score: 0.800

> Use the existing holdings widget data to add a note naming the largest position and its exact weight from the data.

- Novelty: Unique note/t1 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls on portfolio; artifact widgets:Bench Portfolio/holdings_table@*; generated:note@*:MSFT,0.34.
- Fixture backends: portfolio
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): holdings_table({})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`
- **Generated note** ≥1× whose content mentions "MSFT", "0.34" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_note_twofacts_estimates_aapl` — Two-Fact Note: Estimates Aapl

**L0** · workspace-inspection · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.833

> Add a note on the overview tab with the 2026Q1 EPS estimate and the revenue estimate from the data after reviewing the existing AAPL estimates widget.

- Novelty: Unique note/t2 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tab, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/estimate_history@overview; tabs:overview; generated:note@overview:AAPL,2.31.
- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 tab(s): overview; 1 seeded widget(s): estimate_history({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "AAPL"} on tab `overview` → `missing_widget`
- **Generated note** ≥1× whose content mentions "AAPL", "2.31", "94.8" on tab `overview` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_note_twofacts_estimates_msft` — Two-Fact Note: Estimates Msft

**L0** · workspace-inspection · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.833

> Add a note on the overview tab with the 2026Q1 EPS estimate and the revenue estimate from the data after reviewing the existing MSFT estimates widget.

- Novelty: Unique note/t2 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tab, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/estimate_history@overview; tabs:overview; generated:note@overview:MSFT,3.42.
- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 tab(s): overview; 1 seeded widget(s): estimate_history({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "MSFT"} on tab `overview` → `missing_widget`
- **Generated note** ≥1× whose content mentions "MSFT", "3.42", "71.2" on tab `overview` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_note_twofacts_fundamentals_aapl` — Two-Fact Note: Fundamentals Aapl

**L0** · workspace-inspection · workflow: equity-tearsheet · equity-research · difficulty: medium · split: validation · no-op baseline score: 0.833

> Use the existing AAPL fundamentals widget data to add a note on the overview tab with the gross margin and the net cash from the data.

- Novelty: Unique note/t2 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tab, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/fundamental_metrics@overview; tabs:overview; generated:note@overview:AAPL,0.462.
- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 tab(s): overview; 1 seeded widget(s): fundamental_metrics({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "AAPL"} on tab `overview` → `missing_widget`
- **Generated note** ≥1× whose content mentions "AAPL", "0.462", "54.0" on tab `overview` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_note_twofacts_fundamentals_nvda` — Two-Fact Note: Fundamentals Nvda

**L0** · workspace-inspection · workflow: equity-tearsheet · equity-research · difficulty: medium · split: test · no-op baseline score: 0.833

> Add a note on the overview tab with the gross margin and the buyback yield from the data after reviewing the existing NVDA fundamentals widget.

- Novelty: Unique note/t2 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tab, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/fundamental_metrics@overview; tabs:overview; generated:note@overview:NVDA,0.742.
- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 tab(s): overview; 1 seeded widget(s): fundamental_metrics({"symbol": "NVDA"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "NVDA"} on tab `overview` → `missing_widget`
- **Generated note** ≥1× whose content mentions "NVDA", "0.742", "0.004" on tab `overview` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_note_synthesis_aapl_msft_closes` — Synthesis Note: Aapl Msft Closes

**L0** · workspace-inspection · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.857

> Add a note with each latest close from the data after comparing the existing AAPL and MSFT price widgets.

- Novelty: Unique note/t3 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/price_performance@*,Bench Equities/price_performance@*; generated:note@*:AAPL,196.10.
- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), price_performance({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "AAPL", "196.10", "MSFT", "451.25" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_note_synthesis_fed_vs_10y` — Synthesis Note: Fed Vs 10Y

**L0** · workspace-inspection · workflow: macro-rates-review · macro · difficulty: hard · split: train · no-op baseline score: 0.857

> Add a note with both latest values from the data after reviewing the Fed Funds and 10Y Treasury widgets.

- Novelty: Unique note/t3 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls on macro; artifact widgets:Bench Macro/macro_timeseries@*,Bench Macro/macro_timeseries@*; generated:note@*:FEDFUNDS,4.12.
- Fixture backends: macro
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): macro_timeseries({"series": "FEDFUNDS"}), macro_timeseries({"series": "DGS10"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "FEDFUNDS"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "FEDFUNDS", "4.12", "DGS10", "4.16" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_note_synthesis_holdings_beta` — Synthesis Note: Holdings Beta

**L0** · workspace-inspection · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: validation · no-op baseline score: 0.857

> Use the holdings and risk metrics widget data to add a note with the largest position weight and the portfolio beta from the data.

- Novelty: Unique note/t3 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls on portfolio; artifact widgets:Bench Portfolio/holdings_table@*,Bench Portfolio/risk_metrics@*; generated:note@*:MSFT,0.34.
- Fixture backends: portfolio
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): holdings_table({}), risk_metrics({})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Generated note** ≥1× whose content mentions "MSFT", "0.34", "1.18" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_note_synthesis_nvda_close_eps` — Synthesis Note: Nvda Close Eps

**L0** · workspace-inspection · workflow: equity-tearsheet · equity-research · difficulty: medium · split: test · no-op baseline score: 0.857

> Review the NVDA price and estimates widgets and add a note with the latest close and the 2026Q1 EPS estimate from the data.

- Novelty: Unique note/t3 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/estimate_history@*,Bench Equities/price_performance@*; generated:note@*:NVDA,179.45.
- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): price_performance({"symbol": "NVDA"}), estimate_history({"symbol": "NVDA"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "NVDA", "179.45", "1.18" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_note_crossbackend_aapl_vs_rates` — Cross-Backend Note: Aapl Vs Rates

**L0** · workspace-inspection · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: train · no-op baseline score: 0.857

> Review the AAPL price and 10Y Treasury widgets and add a note with the latest close and the latest 10Y value from the data.

- Novelty: Unique note/t4 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls on equities, macro; artifact widgets:Bench Equities/price_performance@*,Bench Macro/macro_timeseries@*; generated:note@*:AAPL,196.10.
- Fixture backends: equities, macro
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), macro_timeseries({"series": "DGS10"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "AAPL", "196.10", "4.16" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_note_crossbackend_book_vs_fed` — Cross-Backend Note: Book Vs Fed

**L0** · workspace-inspection · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: train · no-op baseline score: 0.857

> Review the risk metrics and Fed Funds widgets and add a note with the portfolio beta and the latest FEDFUNDS value from the data.

- Novelty: Unique note/t4 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls on macro, portfolio; artifact widgets:Bench Macro/macro_timeseries@*,Bench Portfolio/risk_metrics@*; generated:note@*:1.18,4.12.
- Fixture backends: macro, portfolio
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): risk_metrics({}), macro_timeseries({"series": "FEDFUNDS"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "FEDFUNDS"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "1.18", "4.12" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_note_crossbackend_exposure_cpi` — Cross-Backend Note: Exposure Cpi

**L0** · workspace-inspection · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: train · no-op baseline score: 0.857

> Use the sector exposure and CPI widget data to add a note with the largest sector weight and the latest CPI value from the data.

- Novelty: Unique note/t4 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls on macro, portfolio; artifact widgets:Bench Macro/macro_timeseries@*,Bench Portfolio/sector_exposure@*; generated:note@*:Technology,0.86.
- Fixture backends: macro, portfolio
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): sector_exposure({}), macro_timeseries({"series": "CPIAUCSL"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "CPIAUCSL"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "Technology", "0.86", "322.4" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_note_crossbackend_msft_vs_curve` — Cross-Backend Note: Msft Vs Curve

**L0** · workspace-inspection · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: test · no-op baseline score: 0.857

> Review the MSFT fundamentals and yield curve widgets and add a note with the gross margin and the 30Y yield from the data.

- Novelty: Unique note/t4 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls on equities, macro; artifact widgets:Bench Equities/fundamental_metrics@*,Bench Macro/yield_curve@*; generated:note@*:MSFT,0.694.
- Fixture backends: equities, macro
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): fundamental_metrics({"symbol": "MSFT"}), yield_curve({})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/yield_curve` → `missing_widget`
- **Generated note** ≥1× whose content mentions "MSFT", "0.694", "4.48" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

### L1 — Single-widget operations (124)

#### `gen_t0_create_latest_news_aapl` — Create Latest News

**L1** · widget-creation · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.667

> From the Bench Equities backend, create a Latest News widget (widget_id latest_news) on the active dashboard with data_args {"symbol": "AAPL", "limit": 5}.

- Novelty: Unique create/t0 exercise using create_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/latest_news@*.
- Fixture backends: equities
- Initial workspace: dashboard "Creation Task"
- Allowed tools (3): `get_workspace_snapshot`, `create_widget`, `read_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL", "limit": 5} → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_create_price_performance_aapl` — Create Price Performance

**L1** · widget-creation · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.667

> From the Bench Equities backend, create a Price Performance widget (widget_id price_performance) on the active dashboard with data_args {"symbol": "AAPL"}.

- Novelty: Unique create/t0 exercise using create_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/price_performance@*.
- Fixture backends: equities
- Initial workspace: dashboard "Creation Task"
- Allowed tools (3): `get_workspace_snapshot`, `create_widget`, `read_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_create_risk_metrics_plain` — Create Risk Metrics

**L1** · widget-creation · workflow: portfolio-risk-review · portfolio-management · difficulty: easy · split: train · no-op baseline score: 0.667

> Create a Risk Metrics widget (widget_id risk_metrics) from the Bench Portfolio backend on the active dashboard.

- Novelty: Unique create/t0 exercise using create_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, too_many_invalid_calls on portfolio; artifact widgets:Bench Portfolio/risk_metrics@*.
- Fixture backends: portfolio
- Initial workspace: dashboard "Creation Task"
- Allowed tools (3): `get_workspace_snapshot`, `create_widget`, `read_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_create_yield_curve_plain` — Create Yield Curve

**L1** · widget-creation · workflow: macro-rates-review · macro · difficulty: easy · split: validation · no-op baseline score: 0.667

> Create a Yield Curve widget (widget_id yield_curve) from the Bench Macro backend on the active dashboard.

- Novelty: Unique create/t0 exercise using create_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, too_many_invalid_calls on macro; artifact widgets:Bench Macro/yield_curve@*.
- Fixture backends: macro
- Initial workspace: dashboard "Creation Task"
- Allowed tools (3): `get_workspace_snapshot`, `create_widget`, `read_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/yield_curve` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_delete_alerts_47` — Remove Top Alerts

**L1** · widget-update · workflow: portfolio-morning-review · portfolio-management · difficulty: easy · split: train · no-op baseline score: 0.800

> This dashboard no longer needs the Top Alerts widget; remove it.

- Novelty: Unique delete/t0 exercise using delete_widget, get_workspace_snapshot with checks layout_out_of_grid, repeated_snapshots, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact id:gen_t0_delete_alerts_47.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Removal Task"; 1 seeded widget(s): portfolio_command_center_overview_top_alerts({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥0× `Bench Stark Enterprise/portfolio_command_center_overview_top_alerts` → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_delete_news_12` — Remove Latest News

**L1** · widget-update · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.800

> The Latest News widget is no longer needed on this dashboard. Remove it.

- Novelty: Unique delete/t0 exercise using delete_widget, get_workspace_snapshot with checks layout_out_of_grid, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact id:gen_t0_delete_news_12.
- Fixture backends: equities
- Initial workspace: dashboard "Removal Task"; 1 seeded widget(s): latest_news({"symbol": "AAPL", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥0× `Bench Equities/latest_news` → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_delete_performance_18` — Remove Price Performance

**L1** · widget-update · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.800

> This dashboard no longer needs the Price Performance widget; remove it.

- Novelty: Unique delete/t0 exercise using delete_widget, get_workspace_snapshot with checks layout_out_of_grid, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact id:gen_t0_delete_performance_18.
- Fixture backends: equities
- Initial workspace: dashboard "Removal Task"; 1 seeded widget(s): price_performance({"symbol": "NVDA"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥0× `Bench Equities/price_performance` → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_delete_timeseries_17` — Remove Macro Timeseries

**L1** · widget-update · workflow: macro-rates-review · macro · difficulty: easy · split: validation · no-op baseline score: 0.800

> The Macro Timeseries widget is no longer needed on this dashboard. Remove it.

- Novelty: Unique delete/t0 exercise using delete_widget, get_workspace_snapshot with checks layout_out_of_grid, repeated_snapshots, too_many_invalid_calls, too_many_widgets on macro; artifact id:gen_t0_delete_timeseries_17.
- Fixture backends: macro
- Initial workspace: dashboard "Removal Task"; 1 seeded widget(s): macro_timeseries({"series": "DGS2"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥0× `Bench Macro/macro_timeseries` → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_layout_halve_price_msft` — Layout: Halve Price Msft

**L1** · layout-management · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.857

> Resize the MSFT price widget to half width (20 columns). Keep its position.

- Novelty: Unique layout/t0 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tab, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/price_performance@charts; layouts:price_performance::charts:0:2:20:12; tabs:charts.
- Fixture backends: equities
- Initial workspace: dashboard "Layout Task"; 1 tab(s): charts; 1 seeded widget(s): price_performance({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `charts` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} on tab `charts` → `missing_widget`
- **Layout** `price_performance` must sit at exactly x=0, y=2, w=20, h=12 on tab `charts` → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_layout_move_news_right` — Layout: Move News Right

**L1** · layout-management · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.857

> Keep the AAPL news widget's size and move it to start at column 20.

- Novelty: Unique layout/t0 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tab, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/latest_news@charts; layouts:latest_news::charts:20:0:20:10; tabs:charts.
- Fixture backends: equities
- Initial workspace: dashboard "Layout Task"; 1 tab(s): charts; 1 seeded widget(s): latest_news({"symbol": "AAPL", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `charts` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL", "limit": 5} on tab `charts` → `missing_widget`
- **Layout** `latest_news` must sit at exactly x=20, y=0, w=20, h=10 on tab `charts` → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_layout_shorten_estimates_nvda` — Layout: Shorten Estimates Nvda

**L1** · layout-management · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.857

> Keep the NVDA estimates widget's position and width, but reduce its height to 8 rows.

- Novelty: Unique layout/t0 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tab, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/estimate_history@charts; layouts:estimate_history::charts:0:0:20:8; tabs:charts.
- Fixture backends: equities
- Initial workspace: dashboard "Layout Task"; 1 tab(s): charts; 1 seeded widget(s): estimate_history({"symbol": "NVDA"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `charts` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "NVDA"} on tab `charts` → `missing_widget`
- **Layout** `estimate_history` must sit at exactly x=0, y=0, w=20, h=8 on tab `charts` → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_layout_widen_fundamentals_aapl` — Layout: Widen Fundamentals Aapl

**L1** · layout-management · workflow: equity-tearsheet · equity-research · difficulty: easy · split: validation · no-op baseline score: 0.857

> Widen the AAPL fundamentals widget to 20 columns. Keep its position and height.

- Novelty: Unique layout/t0 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tab, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/fundamental_metrics@charts; layouts:fundamental_metrics::charts:0:0:20:8; tabs:charts.
- Fixture backends: equities
- Initial workspace: dashboard "Layout Task"; 1 tab(s): charts; 1 seeded widget(s): fundamental_metrics({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `charts` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "AAPL"} on tab `charts` → `missing_widget`
- **Layout** `fundamental_metrics` must sit at exactly x=0, y=0, w=20, h=8 on tab `charts` → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_nav_rename_compliance_day` — Rename To Daily Compliance Control

**L1** · workspace-navigation · workflow: compliance-surveillance · compliance · difficulty: easy · split: train · no-op baseline score: 0.667

> Rename the active dashboard to Daily Compliance Control.

- Novelty: Unique navigate/t0 exercise using manage_dashboard with checks dashboard_name, layout_out_of_grid, missing_tool_call, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/strategy_health_monitor_themes_factor_tilts@overview.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Alert Triage"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_themes_factor_tilts({})
- Allowed tools (2): `get_workspace_snapshot`, `manage_dashboard`
- Turn budget: 4 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Daily Compliance Control" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_themes_factor_tilts` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "Daily Compliance Control"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_nav_rename_equity_desk` — Rename To Equity Desk Monitor

**L1** · workspace-navigation · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.333

> Rename the active dashboard to Equity Desk Monitor.

- Novelty: Unique navigate/t0 exercise using manage_dashboard with checks dashboard_name, layout_out_of_grid, missing_tool_call, too_many_invalid_calls on equities; artifact id:gen_t0_nav_rename_equity_desk.
- Fixture backends: equities
- Initial workspace: dashboard "Desk View"; 1 tab(s): overview
- Allowed tools (2): `get_workspace_snapshot`, `manage_dashboard`
- Turn budget: 4 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Equity Desk Monitor" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "Equity Desk Monitor"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_nav_rename_execution_open` — Rename To Execution Morning Board

**L1** · workspace-navigation · workflow: execution-exception-review · execution · difficulty: easy · split: train · no-op baseline score: 0.667

> Rename the active dashboard to Execution Morning Board.

- Novelty: Unique navigate/t0 exercise using manage_dashboard with checks dashboard_name, layout_out_of_grid, missing_tool_call, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/strategy_health_monitor_themes_thematic_baskets@overview.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Desk Board"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_themes_thematic_baskets({})
- Allowed tools (2): `get_workspace_snapshot`, `manage_dashboard`
- Turn budget: 4 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Execution Morning Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_themes_thematic_baskets` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "Execution Morning Board"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_nav_rename_macro_watch` — Rename To Rates Watch

**L1** · workspace-navigation · workflow: macro-rates-review · macro · difficulty: easy · split: validation · no-op baseline score: 0.333

> Rename the active dashboard to Rates Watch.

- Novelty: Unique navigate/t0 exercise using manage_dashboard with checks dashboard_name, layout_out_of_grid, missing_tool_call, too_many_invalid_calls on macro; artifact id:gen_t0_nav_rename_macro_watch.
- Fixture backends: macro
- Initial workspace: dashboard "Macro Board"; 1 tab(s): overview
- Allowed tools (2): `get_workspace_snapshot`, `manage_dashboard`
- Turn budget: 4 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Rates Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "Rates Watch"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_note_handover` — Desk Handover

**L1** · workspace-inspection · workflow: portfolio-morning-review · portfolio-management · difficulty: easy · split: train · no-op baseline score: 0.667

> On the dashboard, add a note named Desk Handover stating that the EU book is flat and the US open checklist is complete.

- Novelty: Unique note/t0 exercise using add_generative_widget, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact generated:note@*:EU book,checklist.
- Fixture backends: equities
- Initial workspace: dashboard "Notes Board"
- Allowed tools (2): `get_workspace_snapshot`, `add_generative_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Desk Handover" whose content mentions "EU book", "checklist" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_note_outage` — Vendor Outage

**L1** · workspace-inspection · workflow: portfolio-morning-review · portfolio-management · difficulty: easy · split: train · no-op baseline score: 0.667

> Add a note named Vendor Outage saying the FactSet feed is degraded and fallback pricing is active.

- Novelty: Unique note/t0 exercise using add_generative_widget, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact generated:note@*:FactSet,fallback.
- Fixture backends: equities
- Initial workspace: dashboard "Notes Board"
- Allowed tools (2): `get_workspace_snapshot`, `add_generative_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Vendor Outage" whose content mentions "FactSet", "fallback" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_note_reminder` — Compliance Reminder

**L1** · workspace-inspection · workflow: portfolio-morning-review · portfolio-management · difficulty: easy · split: train · no-op baseline score: 0.667

> On the dashboard, add a note named Compliance Reminder stating that attestations are due Friday and trading in restricted names is blocked.

- Novelty: Unique note/t0 exercise using add_generative_widget, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact generated:note@*:attestations,restricted.
- Fixture backends: equities
- Initial workspace: dashboard "Notes Board"
- Allowed tools (2): `get_workspace_snapshot`, `add_generative_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Compliance Reminder" whose content mentions "attestations", "restricted" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_note_standup` — Morning Standup

**L1** · workspace-inspection · workflow: portfolio-morning-review · portfolio-management · difficulty: easy · split: validation · no-op baseline score: 0.667

> Create a note named Morning Standup that says the desk meeting moved to 9am and the risk review is at noon.

- Novelty: Unique note/t0 exercise using add_generative_widget, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact generated:note@*:9am,noon.
- Fixture backends: equities
- Initial workspace: dashboard "Notes Board"
- Allowed tools (2): `get_workspace_snapshot`, `add_generative_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Morning Standup" whose content mentions "9am", "noon" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_params_sector_client_360_meeting_prep_relationship_metrics_3` — Use Sector Options For Relationship Metrics

**L1** · parameter-discovery · workflow: client-meeting-prep · client-ir · difficulty: easy · split: train · no-op baseline score: 0.625

> Use get_params_options for Bench Stark Enterprise/client_360_meeting_prep_relationship_metrics parameter sector, choose Consumer Staples, and create that widget with sector=Consumer Staples.

- Novelty: Unique params/t0 exercise using create_widget, get_params_options, get_workspace_snapshot with checks layout_out_of_grid, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/client_360_meeting_prep_relationship_metrics@*,Bench Stark Enterprise/strategy_health_monitor_watchlist_names_near_action_levels@.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Parameter Options"; 1 seeded widget(s): strategy_health_monitor_watchlist_names_near_action_levels({})
- Allowed tools (3): `get_workspace_snapshot`, `get_params_options`, `create_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/client_360_meeting_prep_relationship_metrics` with data_args ⊇ {"sector": "Consumer Staples"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_watchlist_names_near_action_levels` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "client_360_meeting_prep_relationship_metrics", "param_name": "sector"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_params_options` must contain "Consumer Staples" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_params_sector_sector_exposure_2` — Use Sector Options For Sector Exposure

**L1** · parameter-discovery · workflow: portfolio-risk-review · portfolio-management · difficulty: easy · split: train · no-op baseline score: 0.400

> Call get_params_options for Bench Portfolio/sector_exposure parameter sector, choose Technology, and create that widget with sector=Technology.

- Novelty: Unique params/t0 exercise using create_widget, get_params_options, get_workspace_snapshot with checks layout_out_of_grid, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, too_many_invalid_calls on portfolio; artifact widgets:Bench Portfolio/sector_exposure@*.
- Fixture backends: portfolio
- Initial workspace: dashboard "Parameter Options"
- Allowed tools (3): `get_workspace_snapshot`, `get_params_options`, `create_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` with data_args ⊇ {"sector": "Technology"} → `missing_widget`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "sector_exposure", "param_name": "sector"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_params_options` must contain "Technology" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_params_series_macro_timeseries_1` — Use Series Options For Macro Timeseries

**L1** · parameter-discovery · workflow: macro-rates-review · macro · difficulty: easy · split: train · no-op baseline score: 0.400

> Use get_params_options for Bench Macro/macro_timeseries parameter series, choose DGS10, and create that widget with series=DGS10.

- Novelty: Unique params/t0 exercise using create_widget, get_params_options, get_workspace_snapshot with checks layout_out_of_grid, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, too_many_invalid_calls on macro; artifact widgets:Bench Macro/macro_timeseries@*.
- Fixture backends: macro
- Initial workspace: dashboard "Parameter Options"
- Allowed tools (3): `get_workspace_snapshot`, `get_params_options`, `create_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "macro_timeseries", "param_name": "series"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_params_options` must contain "DGS10" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_params_symbol_price_performance_0` — Use Symbol Options For Price Performance

**L1** · parameter-discovery · workflow: equity-tearsheet · equity-research · difficulty: easy · split: validation · no-op baseline score: 0.400

> Use get_params_options for Bench Equities/price_performance parameter symbol, choose AAPL, and create that widget with symbol=AAPL.

- Novelty: Unique params/t0 exercise using create_widget, get_params_options, get_workspace_snapshot with checks layout_out_of_grid, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/price_performance@*.
- Fixture backends: equities
- Initial workspace: dashboard "Parameter Options"
- Allowed tools (3): `get_workspace_snapshot`, `get_params_options`, `create_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "price_performance", "param_name": "symbol"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_params_options` must contain "AAPL" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_read_attribution` — Read Data: Attribution Summary

**L1** · data-reading · workflow: portfolio-morning-review · portfolio-management · difficulty: easy · split: train · no-op baseline score: 0.400

> On the Bench Stark Enterprise Attribution Summary widget, use get_widget_data, then add a short note that cites portfolio_command_center_attribution_attribution_summary and says you reviewed the data.

- Novelty: Unique read/t0 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:portfolio_command_center_attribution_attribution_summary,data.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): portfolio_command_center_attribution_attribution_summary({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "portfolio_command_center_attribution_attribution_summary", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "portfolio_command_center_attribution_attribution_summary"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "portfolio_command_center_attribution_attribution_summary" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_read_latency` — Read Data: Latency by Feed

**L1** · data-reading · workflow: vendor-sla-monitoring · data-platform · difficulty: easy · split: train · no-op baseline score: 0.400

> On the Bench Stark Enterprise Latency by Feed widget, use get_widget_data, then add a short note that cites vendor_dataset_monitor_slas_latency_by_feed and says you reviewed the data.

- Novelty: Unique read/t0 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:vendor_dataset_monitor_slas_latency_by_feed,data.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): vendor_dataset_monitor_slas_latency_by_feed({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "vendor_dataset_monitor_slas_latency_by_feed", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "vendor_dataset_monitor_slas_latency_by_feed"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "vendor_dataset_monitor_slas_latency_by_feed" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_read_limits` — Read Data: Limit Utilization

**L1** · data-reading · workflow: risk-review · risk · difficulty: easy · split: train · no-op baseline score: 0.400

> On the Bench Stark Enterprise Limit Utilization widget, use get_widget_data, then add a short note that cites risk_exposure_monitor_limits_limit_utilization and says you reviewed the data.

- Novelty: Unique read/t0 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:risk_exposure_monitor_limits_limit_utilization,data.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): risk_exposure_monitor_limits_limit_utilization({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "risk_exposure_monitor_limits_limit_utilization", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "risk_exposure_monitor_limits_limit_utilization"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "risk_exposure_monitor_limits_limit_utilization" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_read_order_status` — Read Data: Order Status Metrics

**L1** · data-reading · workflow: execution-exception-review · execution · difficulty: easy · split: validation · no-op baseline score: 0.400

> On the Bench Stark Enterprise Order Status Metrics widget, use get_widget_data, then add a short note that cites execution_desk_blotter_order_status_metrics and says you reviewed the data.

- Novelty: Unique read/t0 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:execution_desk_blotter_order_status_metrics,data.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): execution_desk_blotter_order_status_metrics({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "execution_desk_blotter_order_status_metrics", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "execution_desk_blotter_order_status_metrics"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "execution_desk_blotter_order_status_metrics" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_skill_finance_comps` — Read The Finance Comps Skill

**L1** · skill-access · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.667

> Call get_skill_content with slug finance-comps, then add a note on the active dashboard naming the Finance Comps skill. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t0 exercise using add_generative_widget, get_skill_content, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/strategy_health_monitor_watchlist_trade_ideas@overview; generated:note@*:Finance Comps.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_watchlist_trade_ideas({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_watchlist_trade_ideas` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Finance Comps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-comps"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_skill_finance_earnings_prep` — Read The Finance Earnings Prep Skill

**L1** · skill-access · workflow: earnings-prep · equity-research · difficulty: easy · split: train · no-op baseline score: 0.667

> After calling get_skill_content with slug finance-earnings-prep, add a note on the active dashboard naming the Finance Earnings Prep skill. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t0 exercise using add_generative_widget, get_skill_content, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/stress_liquidity_lab_liquidity_crowded_names@overview; generated:note@*:Finance Earnings Prep.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_liquidity_crowded_names({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_liquidity_crowded_names` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Finance Earnings Prep" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-earnings-prep"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_skill_finance_guidance_tracker` — Read The Finance Guidance Tracker Skill

**L1** · skill-access · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.667

> Call get_skill_content with slug finance-guidance-tracker, then add a note on the active dashboard naming the Finance Guidance Tracker skill. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t0 exercise using add_generative_widget, get_skill_content, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/stress_liquidity_lab_liquidity_redemption_stress@overview; generated:note@*:Finance Guidance Tracker.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_liquidity_redemption_stress({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_liquidity_redemption_stress` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Finance Guidance Tracker" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-guidance-tracker"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_skill_finance_tearsheet` — Read The Finance Tearsheet Skill

**L1** · skill-access · workflow: equity-tearsheet · equity-research · difficulty: easy · split: validation · no-op baseline score: 0.667

> Call get_skill_content with slug finance-tearsheet, then add a note on the active dashboard naming the Finance Tearsheet skill. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t0 exercise using add_generative_widget, get_skill_content, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/stress_liquidity_lab_overview_workflow_overview@overview; generated:note@*:Finance Tearsheet.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_overview_workflow_overview({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_overview_workflow_overview` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Finance Tearsheet" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-tearsheet"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_update_period_mtd_56` — Set Portfolio Snapshot period To MTD

**L1** · widget-update · workflow: portfolio-morning-review · portfolio-management · difficulty: easy · split: train · no-op baseline score: 0.750

> Set the Portfolio Snapshot widget's period to MTD. Update the existing widget.

- Novelty: Unique update/t0 exercise using get_workspace_snapshot, update_widget with checks layout_out_of_grid, missing_widget, repeated_snapshots, too_many_invalid_calls on stark-enterprise; artifact widgets:Bench Stark Enterprise/portfolio_command_center_overview_portfolio_snapshot@*.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): portfolio_command_center_overview_portfolio_snapshot({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_overview_portfolio_snapshot` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "MTD"} → `missing_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_update_series_dgs10_17` — Set Macro Timeseries series To DGS10

**L1** · widget-update · workflow: macro-rates-review · macro · difficulty: easy · split: train · no-op baseline score: 0.750

> Set the Macro Timeseries widget's series to DGS10. Update the existing widget.

- Novelty: Unique update/t0 exercise using get_workspace_snapshot, update_widget with checks layout_out_of_grid, missing_widget, repeated_snapshots, too_many_invalid_calls on macro; artifact widgets:Bench Macro/macro_timeseries@*.
- Fixture backends: macro
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): macro_timeseries({"series": "DGS2"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_update_symbol_aapl_18` — Set Price Performance symbol To AAPL

**L1** · widget-update · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.750

> For the existing Price Performance widget, set symbol to AAPL.

- Novelty: Unique update/t0 exercise using get_workspace_snapshot, update_widget with checks layout_out_of_grid, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/price_performance@*.
- Fixture backends: equities
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): price_performance({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t0_update_symbol_msft_12` — Set Latest News symbol To MSFT

**L1** · widget-update · workflow: equity-tearsheet · equity-research · difficulty: easy · split: validation · no-op baseline score: 0.750

> Update the existing Latest News widget by setting symbol to MSFT.

- Novelty: Unique update/t0 exercise using get_workspace_snapshot, update_widget with checks layout_out_of_grid, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/latest_news@*.
- Fixture backends: equities
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): latest_news({"symbol": "NVDA", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "MSFT", "limit": 5} → `missing_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_create_estimate_history_nvda` — Add Estimate History With Discovery

**L1** · widget-creation · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.667

> Discover the widget catalog and its schema before creating, then add the Estimate History widget for NVDA to the active dashboard.

- Novelty: Unique create/t1 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/estimate_history@*.
- Fixture backends: equities
- Initial workspace: dashboard "Creation Task"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `read_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_create_macro_timeseries_dgs10` — Add Macro Timeseries With Discovery

**L1** · widget-creation · workflow: macro-rates-review · macro · difficulty: medium · split: train · no-op baseline score: 0.667

> Add the Macro Timeseries widget for DGS10 to the active dashboard. Discover the widget catalog and its schema before creating.

- Novelty: Unique create/t1 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro; artifact widgets:Bench Macro/macro_timeseries@*.
- Fixture backends: macro
- Initial workspace: dashboard "Creation Task"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `read_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_create_price_performance_msft` — Add Price Performance With Discovery

**L1** · widget-creation · workflow: equity-tearsheet · equity-research · difficulty: easy · split: validation · no-op baseline score: 0.667

> Discover the widget catalog and its schema before creating, then add the Price Performance widget for MSFT to the active dashboard.

- Novelty: Unique create/t1 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/price_performance@*.
- Fixture backends: equities
- Initial workspace: dashboard "Creation Task"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `read_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_create_sector_exposure_plain` — Add Sector Exposure With Discovery

**L1** · widget-creation · workflow: portfolio-risk-review · portfolio-management · difficulty: medium · split: test · no-op baseline score: 0.667

> Add the Sector Exposure widget to the active dashboard. Discover the widget catalog and its schema before creating.

- Novelty: Unique create/t1 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio; artifact widgets:Bench Portfolio/sector_exposure@*.
- Fixture backends: portfolio
- Initial workspace: dashboard "Creation Task"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `read_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_delete_dup_news_12` — Remove Duplicate Latest News

**L1** · widget-update · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.857

> The dashboard has two identical Latest News widgets. Remove exactly one so a single copy remains; do not change the one that stays.

- Novelty: Unique delete/t1 exercise using delete_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/latest_news@*.
- Fixture backends: equities
- Initial workspace: dashboard "Duplicate Cleanup"; 2 seeded widget(s): latest_news({"symbol": "MSFT", "limit": 5}), latest_news({"symbol": "MSFT", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "MSFT", "limit": 5} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_delete_dup_performance_18` — Remove Duplicate Price Performance

**L1** · widget-update · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.857

> The dashboard has two identical Price Performance widgets. Remove exactly one so a single copy remains; do not change the one that stays.

- Novelty: Unique delete/t1 exercise using delete_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/price_performance@*.
- Fixture backends: equities
- Initial workspace: dashboard "Duplicate Cleanup"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), price_performance({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_delete_dup_status_48` — Remove Duplicate Vendor SLA Status

**L1** · widget-update · workflow: vendor-sla-monitoring · data-platform · difficulty: medium · split: validation · no-op baseline score: 0.857

> There are two identical Vendor SLA Status widgets on the dashboard. Remove exactly one so a single copy remains; do not change the one that stays.

- Novelty: Unique delete/t1 exercise using delete_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status@*.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Duplicate Cleanup"; 2 seeded widget(s): vendor_dataset_monitor_slas_vendor_sla_status({"vendor": "FactSet"}), vendor_dataset_monitor_slas_vendor_sla_status({"vendor": "FactSet"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"vendor": "FactSet"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_delete_dup_timeseries_17` — Remove Duplicate Macro Timeseries

**L1** · widget-update · workflow: macro-rates-review · macro · difficulty: medium · split: test · no-op baseline score: 0.857

> There are two identical Macro Timeseries widgets on the dashboard. Remove exactly one so a single copy remains; do not change the one that stays.

- Novelty: Unique delete/t1 exercise using delete_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on macro; artifact widgets:Bench Macro/macro_timeseries@*.
- Fixture backends: macro
- Initial workspace: dashboard "Duplicate Cleanup"; 2 seeded widget(s): macro_timeseries({"series": "DGS10"}), macro_timeseries({"series": "DGS10"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_inspect_fix_estimate_history_1` — Find And Fix Misconfigured Estimate History

**L1** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.600

> After calling read_widget with widget_id estimate_history, update the widget configured with symbol=AAPL so symbol=NVDA.

- Novelty: Unique inspect/t1 exercise using get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, missing_tool_call, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/estimate_history@*.
- Fixture backends: equities
- Initial workspace: dashboard "Inspect Repair"; 1 seeded widget(s): estimate_history({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_inspect_fix_macro_timeseries_2` — Find And Fix Misconfigured Macro Timeseries

**L1** · workspace-repair · workflow: macro-rates-review · macro · difficulty: medium · split: train · no-op baseline score: 0.600

> Call read_widget with widget_id macro_timeseries, find the widget configured with series=FEDFUNDS, and update_widget so series=DGS10.

- Novelty: Unique inspect/t1 exercise using get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, missing_tool_call, missing_widget, repeated_snapshots, too_many_invalid_calls on macro; artifact widgets:Bench Macro/macro_timeseries@*.
- Fixture backends: macro
- Initial workspace: dashboard "Inspect Repair"; 1 seeded widget(s): macro_timeseries({"series": "FEDFUNDS"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_inspect_fix_price_performance_0` — Find And Fix Misconfigured Price Performance

**L1** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: easy · split: validation · no-op baseline score: 0.600

> After calling read_widget with widget_id price_performance, update the widget configured with symbol=MSFT so symbol=AAPL.

- Novelty: Unique inspect/t1 exercise using get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, missing_tool_call, missing_widget, repeated_snapshots, too_many_invalid_calls on equities; artifact widgets:Bench Equities/price_performance@*.
- Fixture backends: equities
- Initial workspace: dashboard "Inspect Repair"; 1 seeded widget(s): price_performance({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_inspect_fix_quant_research_backtest_lab_risk_model_factor_exposure_table_3` — Find And Fix Misconfigured Factor Exposure Table

**L1** · workspace-repair · workflow: risk-review · risk · difficulty: medium · split: test · no-op baseline score: 0.600

> Call read_widget with widget_id quant_research_backtest_lab_risk_model_factor_exposure_table, find the widget configured with sector=Technology, and update_widget so sector=Consumer Staples.

- Novelty: Unique inspect/t1 exercise using get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, missing_tool_call, missing_widget, repeated_snapshots, too_many_invalid_calls on stark-enterprise; artifact widgets:Bench Stark Enterprise/quant_research_backtest_lab_risk_model_factor_exposure_table@*.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Inspect Repair"; 1 seeded widget(s): quant_research_backtest_lab_risk_model_factor_exposure_table({"sector": "Technology"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/quant_research_backtest_lab_risk_model_factor_exposure_table` with data_args ⊇ {"sector": "Consumer Staples"} → `missing_widget`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_layout_preserve_estimates_fundamentals_msft` — Move Without Disturbing: Estimates Fundamentals Msft

**L1** · layout-management · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.857

> Keeping its size, move the MSFT fundamentals widget beside the estimates widget at column 24, row 0. Do not move the estimates widget.

- Novelty: Unique layout/t1 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on equities; artifact layouts:estimate_history:::0:0:24:12,fundamental_metrics:::24:0:16:8.
- Fixture backends: equities
- Initial workspace: dashboard "Preserve Layout Task"; 2 seeded widget(s): estimate_history({"symbol": "MSFT"}), fundamental_metrics({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `estimate_history` must sit at exactly x=0, y=0, w=24, h=12 → `layout_mismatch`
- **Layout** `fundamental_metrics` must sit at exactly x=24, y=0, w=16, h=8 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_layout_preserve_macro_pair` — Move Without Disturbing: Macro Pair

**L1** · layout-management · workflow: macro-rates-review · macro · difficulty: medium · split: train · no-op baseline score: 0.857

> Do not move the series widget; move the yield curve widget beside the 10Y series widget so it starts at column 20, row 0, keeping its size.

- Novelty: Unique layout/t1 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on macro; artifact layouts:macro_timeseries:::0:0:20:10,yield_curve:::20:0:20:10.
- Fixture backends: macro
- Initial workspace: dashboard "Preserve Layout Task"; 2 seeded widget(s): macro_timeseries({"series": "DGS10"}), yield_curve({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `macro_timeseries` must sit at exactly x=0, y=0, w=20, h=10 → `layout_mismatch`
- **Layout** `yield_curve` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_layout_preserve_portfolio_pair` — Move Without Disturbing: Portfolio Pair

**L1** · layout-management · workflow: portfolio-risk-review · portfolio-management · difficulty: medium · split: validation · no-op baseline score: 0.857

> Keeping its size, move the sector exposure widget beside the holdings widget at column 24, row 0. Do not move the holdings widget.

- Novelty: Unique layout/t1 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on portfolio; artifact layouts:holdings_table:::0:0:24:12,sector_exposure:::24:0:16:10.
- Fixture backends: portfolio
- Initial workspace: dashboard "Preserve Layout Task"; 2 seeded widget(s): holdings_table({}), sector_exposure({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `holdings_table` must sit at exactly x=0, y=0, w=24, h=12 → `layout_mismatch`
- **Layout** `sector_exposure` must sit at exactly x=24, y=0, w=16, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_layout_preserve_price_news_aapl` — Move Without Disturbing: Price News Aapl

**L1** · layout-management · workflow: equity-tearsheet · equity-research · difficulty: easy · split: test · no-op baseline score: 0.857

> Keeping its size, move the AAPL news widget up beside the price widget at column 20, row 0. Do not move the price widget.

- Novelty: Unique layout/t1 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on equities; artifact layouts:latest_news:::20:0:20:10,price_performance:::0:0:20:12.
- Fixture backends: equities
- Initial workspace: dashboard "Preserve Layout Task"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), latest_news({"symbol": "AAPL", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `price_performance` must sit at exactly x=0, y=0, w=20, h=12 → `layout_mismatch`
- **Layout** `latest_news` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_nav_rename_both_client_review` — Rename Dashboard And Tab: Client Review Agenda

**L1** · workspace-navigation · workflow: client-meeting-prep · client-ir · difficulty: easy · split: train · no-op baseline score: 0.500

> Change the active dashboard's name to Client Review Agenda; also rename the Overview tab to Talking Points.

- Novelty: Unique navigate/t1 exercise using manage_dashboard, manage_navigation_bar with checks dashboard_name, layout_out_of_grid, missing_tab, missing_tool_call, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/stress_liquidity_lab_sign_off_risk_committee_comments@overview; tabs:talking-points.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Client Prep"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_sign_off_risk_committee_comments({})
- Allowed tools (4): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Review Agenda" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `talking-points` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_sign_off_risk_committee_comments` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "Client Review Agenda"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "rename_tabs"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_nav_rename_both_earnings_week` — Rename Dashboard And Tab: Earnings Week Planner

**L1** · workspace-navigation · workflow: earnings-prep · equity-research · difficulty: medium · split: train · no-op baseline score: 0.200

> Rename the active dashboard to Earnings Week Planner and rename the Overview tab to Calendar.

- Novelty: Unique navigate/t1 exercise using manage_dashboard, manage_navigation_bar with checks dashboard_name, layout_out_of_grid, missing_tab, missing_tool_call, too_many_invalid_calls on equities; artifact tabs:calendar.
- Fixture backends: equities
- Initial workspace: dashboard "Earnings Board"; 1 tab(s): overview
- Allowed tools (4): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Earnings Week Planner" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `calendar` must exist (matched by tab id) → `missing_tab`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "Earnings Week Planner"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "rename_tabs"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_nav_rename_both_ops_close` — Rename Dashboard And Tab: Fund Close Control

**L1** · workspace-navigation · workflow: vendor-sla-monitoring · data-platform · difficulty: easy · split: validation · no-op baseline score: 0.500

> Rename the active dashboard to Fund Close Control and rename the Overview tab to Close Checklist.

- Novelty: Unique navigate/t1 exercise using manage_dashboard, manage_navigation_bar with checks dashboard_name, layout_out_of_grid, missing_tab, missing_tool_call, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/stress_liquidity_lab_sign_off_sign_off_tracker@overview; tabs:close-checklist.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Ops Board"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_sign_off_sign_off_tracker({})
- Allowed tools (4): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Fund Close Control" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `close-checklist` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_sign_off_sign_off_tracker` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "Fund Close Control"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "rename_tabs"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_nav_rename_both_pm_morning` — Rename Dashboard And Tab: PM Morning Review

**L1** · workspace-navigation · workflow: portfolio-morning-review · portfolio-management · difficulty: medium · split: test · no-op baseline score: 0.200

> Rename the active dashboard to PM Morning Review and rename the Overview tab to Holdings View.

- Novelty: Unique navigate/t1 exercise using manage_dashboard, manage_navigation_bar with checks dashboard_name, layout_out_of_grid, missing_tab, missing_tool_call, too_many_invalid_calls on portfolio; artifact tabs:holdings-view.
- Fixture backends: portfolio
- Initial workspace: dashboard "PM Board"; 1 tab(s): overview
- Allowed tools (4): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "PM Morning Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `holdings-view` must exist (matched by tab id) → `missing_tab`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "PM Morning Review"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "rename_tabs"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_params_schema_sector_client_360_portfolio_view_exposure_summary_7` — Discover Schema Then Options For Exposure Summary

**L1** · parameter-discovery · workflow: client-meeting-prep · client-ir · difficulty: medium · split: train · no-op baseline score: 0.667

> Before creating Bench Stark Enterprise/client_360_portfolio_view_exposure_summary with sector=Consumer Staples, discover the catalog and schema and call get_params_options for sector.

- Novelty: Unique params/t1 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, too_many_widgets, unlisted_widget_id on stark-enterprise; artifact widgets:Bench Stark Enterprise/client_360_portfolio_view_exposure_summary@*,Bench Stark Enterprise/stress_liquidity_lab_stress_tests_historical_shocks@.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Parameter Options"; 1 seeded widget(s): stress_liquidity_lab_stress_tests_historical_shocks({})
- Allowed tools (5): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/client_360_portfolio_view_exposure_summary` with data_args ⊇ {"sector": "Consumer Staples"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_stress_tests_historical_shocks` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "client_360_portfolio_view_exposure_summary", "param_name": "sector"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_params_options` must contain "Consumer Staples" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_params_schema_sector_sector_exposure_6` — Discover Schema Then Options For Sector Exposure

**L1** · parameter-discovery · workflow: portfolio-risk-review · portfolio-management · difficulty: medium · split: train · no-op baseline score: 0.400

> Discover the catalog and schema for Bench Portfolio/sector_exposure, call get_params_options for sector, then create it with sector=Technology.

- Novelty: Unique params/t1 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio; artifact widgets:Bench Portfolio/sector_exposure@*.
- Fixture backends: portfolio
- Initial workspace: dashboard "Parameter Options"
- Allowed tools (5): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` with data_args ⊇ {"sector": "Technology"} → `missing_widget`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "sector_exposure", "param_name": "sector"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_params_options` must contain "Technology" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_params_schema_series_macro_timeseries_5` — Discover Schema Then Options For Macro Timeseries

**L1** · parameter-discovery · workflow: macro-rates-review · macro · difficulty: easy · split: validation · no-op baseline score: 0.400

> Before creating Bench Macro/macro_timeseries with series=DGS10, discover the catalog and schema and call get_params_options for series.

- Novelty: Unique params/t1 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro; artifact widgets:Bench Macro/macro_timeseries@*.
- Fixture backends: macro
- Initial workspace: dashboard "Parameter Options"
- Allowed tools (5): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "macro_timeseries", "param_name": "series"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_params_options` must contain "DGS10" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_params_schema_symbol_price_performance_4` — Discover Schema Then Options For Price Performance

**L1** · parameter-discovery · workflow: equity-tearsheet · equity-research · difficulty: easy · split: test · no-op baseline score: 0.400

> For Bench Equities/price_performance, discover the catalog and schema, call get_params_options for symbol, then create it with symbol=AAPL.

- Novelty: Unique params/t1 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/price_performance@*.
- Fixture backends: equities
- Initial workspace: dashboard "Parameter Options"
- Allowed tools (5): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "price_performance", "param_name": "symbol"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_params_options` must contain "AAPL" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_read_alert_trend` — Read Data: Alert Trend

**L1** · data-reading · workflow: compliance-surveillance · compliance · difficulty: easy · split: train · no-op baseline score: 0.400

> Use get_widget_data on the Bench Stark Enterprise Alert Trend widget, then add a short note that cites compliance_surveillance_hub_alerts_alert_trend and says you reviewed the data.

- Novelty: Unique read/t1 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:compliance_surveillance_hub_alerts_alert_trend,data.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): compliance_surveillance_hub_alerts_alert_trend({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "compliance_surveillance_hub_alerts_alert_trend", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "compliance_surveillance_hub_alerts_alert_trend"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "compliance_surveillance_hub_alerts_alert_trend" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_read_break_aging` — Read Data: Break Aging

**L1** · data-reading · workflow: vendor-sla-monitoring · data-platform · difficulty: medium · split: train · no-op baseline score: 0.400

> On the Bench Stark Enterprise Break Aging widget, use get_widget_data, then add a short note that cites fund_operations_control_tower_recons_break_aging and says you reviewed the data.

- Novelty: Unique read/t1 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:fund_operations_control_tower_recons_break_aging,data.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): fund_operations_control_tower_recons_break_aging({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "fund_operations_control_tower_recons_break_aging", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "fund_operations_control_tower_recons_break_aging"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "fund_operations_control_tower_recons_break_aging" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_read_pipeline` — Read Data: Pipeline by Stage

**L1** · data-reading · workflow: client-meeting-prep · client-ir · difficulty: easy · split: validation · no-op baseline score: 0.400

> Use get_widget_data on the Bench Stark Enterprise Pipeline by Stage widget, then add a short note that cites client_360_flows_pipeline_by_stage and says you reviewed the data.

- Novelty: Unique read/t1 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:client_360_flows_pipeline_by_stage,data.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): client_360_flows_pipeline_by_stage({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "client_360_flows_pipeline_by_stage", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "client_360_flows_pipeline_by_stage"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "client_360_flows_pipeline_by_stage" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_read_strategy_health` — Read Data: Strategy Health Metrics

**L1** · data-reading · workflow: portfolio-morning-review · portfolio-management · difficulty: medium · split: test · no-op baseline score: 0.400

> On the Bench Stark Enterprise Strategy Health Metrics widget, use get_widget_data, then add a short note that cites strategy_health_monitor_performance_strategy_health_metrics and says you reviewed the data.

- Novelty: Unique read/t1 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:strategy_health_monitor_performance_strategy_health_metrics,data.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): strategy_health_monitor_performance_strategy_health_metrics({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "strategy_health_monitor_performance_strategy_health_metrics", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "strategy_health_monitor_performance_strategy_health_metrics"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "strategy_health_monitor_performance_strategy_health_metrics" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_skill_finance_comps` — Apply Finance Comps Workflow Notes

**L1** · skill-access · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.571

> Call get_skill_content with slug finance-comps, then add a note on the active dashboard that captures the workflow steps for an analyst. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t1 exercise using add_generative_widget, get_skill_content, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/vendor_dataset_monitor_incidents_freshness_exceptions@overview; generated:note@*:comps,peer set.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_incidents_freshness_exceptions({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_incidents_freshness_exceptions` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "comps", "peer set" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-comps"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Comps workflow", "peer set", "valuation multiples" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_skill_finance_earnings_prep` — Apply Finance Earnings Prep Workflow Notes

**L1** · skill-access · workflow: earnings-prep · equity-research · difficulty: easy · split: train · no-op baseline score: 0.571

> After calling get_skill_content with slug finance-earnings-prep, add a note on the active dashboard that captures the workflow steps for an analyst. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t1 exercise using add_generative_widget, get_skill_content, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/vendor_dataset_monitor_incidents_incident_timeline@overview; generated:note@*:earnings prep,surprise drivers.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_incidents_incident_timeline({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_incidents_incident_timeline` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "earnings prep", "surprise drivers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-earnings-prep"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Earnings prep workflow", "surprise drivers", "portfolio manager" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_skill_finance_guidance_tracker` — Apply Finance Guidance Tracker Workflow Notes

**L1** · skill-access · workflow: equity-tearsheet · equity-research · difficulty: medium · split: validation · no-op baseline score: 0.571

> Call get_skill_content with slug finance-guidance-tracker, then add a note on the active dashboard that captures the workflow steps for an analyst. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t1 exercise using add_generative_widget, get_skill_content, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/vendor_dataset_monitor_overview_workflow_overview@overview; generated:note@*:guidance,claims.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_overview_workflow_overview({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_overview_workflow_overview` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "guidance", "claims" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-guidance-tracker"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Guidance tracker workflow", "management claims", "evidence gaps" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_skill_finance_tearsheet` — Apply Finance Tearsheet Workflow Notes

**L1** · skill-access · workflow: equity-tearsheet · equity-research · difficulty: easy · split: test · no-op baseline score: 0.571

> After calling get_skill_content with slug finance-tearsheet, add a note on the active dashboard that captures the workflow steps for an analyst. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t1 exercise using add_generative_widget, get_skill_content, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/vendor_dataset_monitor_quality_affected_apps@overview; generated:note@*:tearsheet,valuation.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_quality_affected_apps({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_quality_affected_apps` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "tearsheet", "valuation" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-tearsheet"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Tearsheet workflow", "valuation", "investment conclusion" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_update_series_fedfunds_17` — Update Macro Timeseries (CPIAUCSL To FEDFUNDS)

**L1** · widget-update · workflow: macro-rates-review · macro · difficulty: medium · split: train · no-op baseline score: 0.667

> The existing Macro Timeseries widget currently shows CPIAUCSL. Update that widget to FEDFUNDS; do not create a new one and leave no widget showing the old value.

- Novelty: Unique update/t1 exercise using get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on macro; artifact widgets:Bench Macro/macro_timeseries@*.
- Fixture backends: macro
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): macro_timeseries({"series": "CPIAUCSL"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "FEDFUNDS"} → `missing_widget`
- **Widget** ≥0× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "CPIAUCSL"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_update_status_escalated_44` — Update Rejected Orders (Open To Escalated)

**L1** · widget-update · workflow: execution-exception-review · execution · difficulty: medium · split: train · no-op baseline score: 0.667

> The Rejected Orders widget currently shows Open. Update the existing widget to Escalated; do not create a new one and leave no widget showing the old value.

- Novelty: Unique update/t1 exercise using get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/execution_desk_exceptions_rejected_orders@*.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): execution_desk_exceptions_rejected_orders({"desk": "US Equities", "status": "Open"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_exceptions_rejected_orders` with data_args ⊇ {"desk": "US Equities", "status": "Escalated"} → `missing_widget`
- **Widget** ≥0× `Bench Stark Enterprise/execution_desk_exceptions_rejected_orders` with data_args ⊇ {"status": "Open"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_update_symbol_nvda_17` — Update Estimate History (AAPL To NVDA)

**L1** · widget-update · workflow: equity-tearsheet · equity-research · difficulty: easy · split: validation · no-op baseline score: 0.667

> The Estimate History widget currently shows AAPL. Update the existing widget to NVDA; do not create a new one and leave no widget showing the old value.

- Novelty: Unique update/t1 exercise using get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/estimate_history@*.
- Fixture backends: equities
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): estimate_history({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Widget** ≥0× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_update_symbol_nvda_20` — Update Fundamental Metrics (MSFT To NVDA)

**L1** · widget-update · workflow: equity-tearsheet · equity-research · difficulty: easy · split: test · no-op baseline score: 0.667

> Update the existing Fundamental Metrics widget from MSFT to NVDA; do not create a new one and leave no widget showing the old value.

- Novelty: Unique update/t1 exercise using get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/fundamental_metrics@*.
- Fixture backends: equities
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): fundamental_metrics({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Widget** ≥0× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_create_place_fundamental_metrics_aapl` — Add And Place Fundamental Metrics (AAPL)

**L1** · widget-creation · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.400

> Fetch the widget schema and confirm the symbol value through the parameter options before creating the Fundamental Metrics widget for AAPL, then place it at exactly x=0, y=0, width 10, height 8.

- Novelty: Unique create/t2 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/fundamental_metrics@*; layouts:fundamental_metrics:::0:0:10:8.
- Fixture backends: equities
- Initial workspace: dashboard "Placement Task"
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `read_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Layout** `fundamental_metrics` must sit at exactly x=0, y=0, w=10, h=8 → `layout_mismatch`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "fundamental_metrics", "param_name": "symbol"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_create_place_latest_news_msft` — Add And Place Latest News (MSFT)

**L1** · widget-creation · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.400

> Fetch the widget schema and confirm the symbol value through the parameter options before creating the Latest News widget for MSFT, then place it at exactly x=20, y=0, width 20, height 10.

- Novelty: Unique create/t2 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/latest_news@*; layouts:latest_news:::20:0:20:10.
- Fixture backends: equities
- Initial workspace: dashboard "Placement Task"
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `read_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "MSFT", "limit": 5} → `missing_widget`
- **Layout** `latest_news` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "latest_news", "param_name": "symbol"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_create_place_macro_timeseries_fedfunds` — Add And Place Macro Timeseries (FEDFUNDS)

**L1** · widget-creation · workflow: macro-rates-review · macro · difficulty: medium · split: validation · no-op baseline score: 0.400

> Fetch the widget schema and confirm the series value through the parameter options before creating the Macro Timeseries widget for FEDFUNDS, then place it at exactly x=0, y=2, width 20, height 10.

- Novelty: Unique create/t2 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro; artifact widgets:Bench Macro/macro_timeseries@*; layouts:macro_timeseries:::0:2:20:10.
- Fixture backends: macro
- Initial workspace: dashboard "Placement Task"
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `read_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "FEDFUNDS"} → `missing_widget`
- **Layout** `macro_timeseries` must sit at exactly x=0, y=2, w=20, h=10 → `layout_mismatch`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "macro_timeseries", "param_name": "series"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_create_place_price_performance_nvda` — Add And Place Price Performance (NVDA)

**L1** · widget-creation · workflow: equity-tearsheet · equity-research · difficulty: medium · split: test · no-op baseline score: 0.400

> Fetch the widget schema and confirm the symbol value through the parameter options before creating the Price Performance widget for NVDA, then place it at exactly x=0, y=2, width 20, height 12.

- Novelty: Unique create/t2 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/price_performance@*; layouts:price_performance:::0:2:20:12.
- Fixture backends: equities
- Initial workspace: dashboard "Placement Task"
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `read_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Layout** `price_performance` must sit at exactly x=0, y=2, w=20, h=12 → `layout_mismatch`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "price_performance", "param_name": "symbol"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_delete_similar_estimate_history_msft` — Remove Only The Duplicate MSFT Widget

**L1** · widget-update · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.900

> This dashboard has three Estimate History widgets: two identical ones for MSFT and one for NVDA. Remove exactly one duplicate MSFT widget; keep the other and keep the NVDA widget untouched.

- Novelty: Unique delete/t2 exercise using delete_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/estimate_history@*,Bench Equities/estimate_history@*.
- Fixture backends: equities
- Initial workspace: dashboard "Similar Cleanup"; 3 seeded widget(s): estimate_history({"symbol": "MSFT"}), estimate_history({"symbol": "MSFT"}), estimate_history({"symbol": "NVDA"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_delete_similar_latest_news_nvda` — Remove Only The Duplicate NVDA Widget

**L1** · widget-update · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.900

> This dashboard has three Latest News widgets: two identical ones for NVDA and one for AAPL. Remove exactly one duplicate NVDA widget; keep the other and keep the AAPL widget untouched.

- Novelty: Unique delete/t2 exercise using delete_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/latest_news@*,Bench Equities/latest_news@*.
- Fixture backends: equities
- Initial workspace: dashboard "Similar Cleanup"; 3 seeded widget(s): latest_news({"symbol": "NVDA", "limit": 5}), latest_news({"symbol": "NVDA", "limit": 5}), latest_news({"symbol": "AAPL", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_delete_similar_macro_timeseries_dgs10` — Remove Only The Duplicate DGS10 Widget

**L1** · widget-update · workflow: macro-rates-review · macro · difficulty: medium · split: validation · no-op baseline score: 0.900

> Three Macro Timeseries widgets are on this dashboard: two identical ones for DGS10 and one for DGS2. Remove exactly one duplicate DGS10 widget; keep the other and keep the DGS2 widget untouched.

- Novelty: Unique delete/t2 exercise using delete_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on macro; artifact widgets:Bench Macro/macro_timeseries@*,Bench Macro/macro_timeseries@*.
- Fixture backends: macro
- Initial workspace: dashboard "Similar Cleanup"; 3 seeded widget(s): macro_timeseries({"series": "DGS10"}), macro_timeseries({"series": "DGS10"}), macro_timeseries({"series": "DGS2"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS2"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_delete_similar_price_performance_aapl` — Remove Only The Duplicate AAPL Widget

**L1** · widget-update · workflow: equity-tearsheet · equity-research · difficulty: medium · split: test · no-op baseline score: 0.900

> Remove exactly one duplicate AAPL Price Performance widget from the two identical AAPL copies, while keeping the other duplicate and the MSFT widget untouched.

- Novelty: Unique delete/t2 exercise using delete_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/price_performance@*,Bench Equities/price_performance@*.
- Fixture backends: equities
- Initial workspace: dashboard "Similar Cleanup"; 3 seeded widget(s): price_performance({"symbol": "AAPL"}), price_performance({"symbol": "AAPL"}), price_performance({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_layout_arrange_split_macro` — Arrange: Split Macro

**L1** · layout-management · workflow: macro-rates-review · macro · difficulty: medium · split: train · no-op baseline score: 0.714

> Arrange the macro widgets side by side: the 10Y series on the left half and the yield curve on the right half, both 10 rows tall starting at row 0.

- Novelty: Unique layout/t2 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on macro; artifact layouts:macro_timeseries:::0:0:20:10,yield_curve:::20:0:20:10.
- Fixture backends: macro
- Initial workspace: dashboard "Arrangement Task"; 2 seeded widget(s): macro_timeseries({"series": "DGS10"}), yield_curve({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `macro_timeseries` must sit at exactly x=0, y=0, w=20, h=10 → `layout_mismatch`
- **Layout** `yield_curve` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_layout_arrange_split_portfolio` — Arrange: Split Portfolio

**L1** · layout-management · workflow: portfolio-risk-review · portfolio-management · difficulty: medium · split: train · no-op baseline score: 0.714

> Set the portfolio layout with holdings left at width 24 and sector exposure right at width 16, both 12 rows tall starting at row 0.

- Novelty: Unique layout/t2 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on portfolio; artifact layouts:holdings_table:::0:0:24:12,sector_exposure:::24:0:16:12.
- Fixture backends: portfolio
- Initial workspace: dashboard "Arrangement Task"; 2 seeded widget(s): holdings_table({}), sector_exposure({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `holdings_table` must sit at exactly x=0, y=0, w=24, h=12 → `layout_mismatch`
- **Layout** `sector_exposure` must sit at exactly x=24, y=0, w=16, h=12 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_layout_arrange_split_price_news_aapl` — Arrange: Split Price News Aapl

**L1** · layout-management · workflow: equity-tearsheet · equity-research · difficulty: medium · split: validation · no-op baseline score: 0.714

> Place the AAPL price widget on the left half and the AAPL news widget on the right half, side by side, both 12 rows tall starting at row 0.

- Novelty: Unique layout/t2 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on equities; artifact layouts:latest_news:::20:0:20:12,price_performance:::0:0:20:12.
- Fixture backends: equities
- Initial workspace: dashboard "Arrangement Task"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), latest_news({"symbol": "AAPL", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `price_performance` must sit at exactly x=0, y=0, w=20, h=12 → `layout_mismatch`
- **Layout** `latest_news` must sit at exactly x=20, y=0, w=20, h=12 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_layout_arrange_stack_price_news_nvda` — Arrange: Stack Price News Nvda

**L1** · layout-management · workflow: equity-tearsheet · equity-research · difficulty: medium · split: test · no-op baseline score: 0.714

> Arrange the NVDA widgets full-width with price on top (rows 0-12, 40 columns) and news below it (10 rows tall starting at row 12, 40 columns).

- Novelty: Unique layout/t2 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on equities; artifact layouts:latest_news:::0:12:40:10,price_performance:::0:0:40:12.
- Fixture backends: equities
- Initial workspace: dashboard "Arrangement Task"; 2 seeded widget(s): price_performance({"symbol": "NVDA"}), latest_news({"symbol": "NVDA", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `price_performance` must sit at exactly x=0, y=0, w=40, h=12 → `layout_mismatch`
- **Layout** `latest_news` must sit at exactly x=0, y=12, w=40, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_nav_expand_client_expansion` — Expand To Client Command Center

**L1** · workspace-navigation · workflow: client-meeting-prep · client-ir · difficulty: medium · split: train · no-op baseline score: 0.556

> Rename the active dashboard to Client Command Center, add a new tab named Open Requests, and add a note on the new tab that mentions open requests and says items are pending.

- Novelty: Unique navigate/t2 exercise using add_generative_widget, manage_dashboard, manage_navigation_bar, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_tab, missing_tool_call, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/vendor_dataset_monitor_slas_sla_breach_history@overview; tabs:open-requests,overview; generated:note@open-requests:open requests,pending.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Client Board"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_slas_sla_breach_history({})
- Allowed tools (5): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Command Center" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `open-requests` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_slas_sla_breach_history` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "open requests", "pending" on tab `open-requests` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "add_tabs"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_nav_expand_research_expansion` — Expand To Research Command Center

**L1** · workspace-navigation · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.556

> Change the active dashboard's name to Research Command Center; add a new tab named Draft Reviews; then add a note on the new tab that mentions draft reviews and says items are pending.

- Novelty: Unique navigate/t2 exercise using add_generative_widget, manage_dashboard, manage_navigation_bar, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_tab, missing_tool_call, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/vendor_dataset_monitor_vendors_incident_log@overview; tabs:draft-reviews,overview; generated:note@draft-reviews:draft reviews,pending.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Research Board"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_vendors_incident_log({})
- Allowed tools (5): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Research Command Center" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `draft-reviews` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_incident_log` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "draft reviews", "pending" on tab `draft-reviews` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "add_tabs"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_nav_expand_risk_expansion` — Expand To Risk Command Center

**L1** · workspace-navigation · workflow: risk-review · risk · difficulty: medium · split: validation · no-op baseline score: 0.556

> Rename the active dashboard to Risk Command Center, add a new tab named Stress Results, and add a note on the new tab that mentions stress results and says items are pending.

- Novelty: Unique navigate/t2 exercise using add_generative_widget, manage_dashboard, manage_navigation_bar, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_tab, missing_tool_call, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/vendor_dataset_monitor_vendors_sla_metrics@overview; tabs:overview,stress-results; generated:note@stress-results:stress results,pending.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Risk Board"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_vendors_sla_metrics({})
- Allowed tools (5): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Risk Command Center" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `stress-results` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_sla_metrics` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "stress results", "pending" on tab `stress-results` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "add_tabs"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_nav_expand_vendor_expansion` — Expand To Vendor Control Center

**L1** · workspace-navigation · workflow: vendor-sla-monitoring · data-platform · difficulty: medium · split: test · no-op baseline score: 0.556

> Rename the active dashboard to Vendor Control Center, add a new tab named Incident Log, and add a note on the new tab that mentions incident log and says items are pending.

- Novelty: Unique navigate/t2 exercise using add_generative_widget, manage_dashboard, manage_navigation_bar, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_tab, missing_tool_call, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/vendor_dataset_monitor_vendors_vendor_contract_terms@overview; tabs:incident-log,overview; generated:note@incident-log:incident log,pending.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Vendor Board"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_vendors_vendor_contract_terms({})
- Allowed tools (5): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vendor Control Center" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `incident-log` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_vendor_contract_terms` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "incident log", "pending" on tab `incident-log` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "add_tabs"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_read_broker_scorecard` — Read Data: Broker Scorecard

**L1** · data-reading · workflow: execution-exception-review · execution · difficulty: medium · split: train · no-op baseline score: 0.400

> Use get_widget_data for the Bench Stark Enterprise Broker Scorecard widget; find the exact score for execution_desk_fills_broker_scorecard, then add a note that cites each widget id, the field name, and the exact value.

- Novelty: Unique read/t2 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:execution_desk_fills_broker_scorecard,score.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): execution_desk_fills_broker_scorecard({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "execution_desk_fills_broker_scorecard", "score", "68.41" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "execution_desk_fills_broker_scorecard"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "execution_desk_fills_broker_scorecard", "score", "68.41" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_read_issuer_conc` — Read Data: Issuer Concentration

**L1** · data-reading · workflow: portfolio-morning-review · portfolio-management · difficulty: medium · split: train · no-op baseline score: 0.400

> On the Bench Stark Enterprise Issuer Concentration widget, use get_widget_data, find the exact score for portfolio_command_center_holdings_issuer_concentration, then add a note that cites each widget id, the field name, and the exact value.

- Novelty: Unique read/t2 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:portfolio_command_center_holdings_issuer_concentration,score.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): portfolio_command_center_holdings_issuer_concentration({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "portfolio_command_center_holdings_issuer_concentration", "score", "94.45" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "portfolio_command_center_holdings_issuer_concentration"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "portfolio_command_center_holdings_issuer_concentration", "score", "94.45" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_read_sla_metrics` — Read Data: SLA Metrics

**L1** · data-reading · workflow: vendor-sla-monitoring · data-platform · difficulty: medium · split: validation · no-op baseline score: 0.400

> Use get_widget_data for the Bench Stark Enterprise SLA Metrics widget; find the exact value for vendor_dataset_monitor_vendors_sla_metrics, then add a note that cites each widget id, the field name, and the exact value.

- Novelty: Unique read/t2 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:vendor_dataset_monitor_vendors_sla_metrics,value.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): vendor_dataset_monitor_vendors_sla_metrics({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "vendor_dataset_monitor_vendors_sla_metrics", "value", "63.73" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "vendor_dataset_monitor_vendors_sla_metrics"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "vendor_dataset_monitor_vendors_sla_metrics", "value", "63.73" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_read_var_trend` — Read Data: VaR Trend

**L1** · data-reading · workflow: risk-review · risk · difficulty: medium · split: test · no-op baseline score: 0.400

> On the Bench Stark Enterprise VaR Trend widget, use get_widget_data, find the exact var_usd for risk_exposure_monitor_dashboard_var_trend, then add a note that cites each widget id, the field name, and the exact value.

- Novelty: Unique read/t2 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:risk_exposure_monitor_dashboard_var_trend,var_usd.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): risk_exposure_monitor_dashboard_var_trend({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "risk_exposure_monitor_dashboard_var_trend", "var_usd", "-222500" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "risk_exposure_monitor_dashboard_var_trend"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "risk_exposure_monitor_dashboard_var_trend", "var_usd", "-222500" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_skill_finance_comps` — File Finance Comps Under Its Own Tab

**L1** · skill-access · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.556

> After calling get_skill_content with slug finance-comps, add a new tab named Comps and put a note on that tab capturing the workflow steps. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t2 exercise using add_generative_widget, get_skill_content, get_workspace_snapshot, manage_navigation_bar, navigate_workspace with checks layout_out_of_grid, missing_generated_widget, missing_tab, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/workspace_data_control_center_ai_access_app_usage@overview; tabs:comps,overview; generated:note@comps:comps,peer set.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_ai_access_app_usage({})
- Allowed tools (5): `get_workspace_snapshot`, `get_skill_content`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `comps` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_ai_access_app_usage` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "comps", "peer set" on tab `comps` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-comps"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Comps workflow", "peer set", "valuation multiples" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_skill_finance_earnings_prep` — File Finance Earnings Prep Under Its Own Tab

**L1** · skill-access · workflow: earnings-prep · equity-research · difficulty: medium · split: train · no-op baseline score: 0.556

> Call get_skill_content with slug finance-earnings-prep. Add a new tab named Earnings Prep and put a note on that tab capturing the workflow steps. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t2 exercise using add_generative_widget, get_skill_content, get_workspace_snapshot, manage_navigation_bar, navigate_workspace with checks layout_out_of_grid, missing_generated_widget, missing_tab, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/workspace_data_control_center_ai_access_copilot_visibility_flags@overview; tabs:earnings-prep,overview; generated:note@earnings-prep:earnings prep,surprise drivers.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_ai_access_copilot_visibility_flags({})
- Allowed tools (5): `get_workspace_snapshot`, `get_skill_content`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `earnings-prep` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_ai_access_copilot_visibility_flags` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "earnings prep", "surprise drivers" on tab `earnings-prep` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-earnings-prep"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Earnings prep workflow", "surprise drivers", "portfolio manager" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_skill_finance_guidance_tracker` — File Finance Guidance Tracker Under Its Own Tab

**L1** · skill-access · workflow: equity-tearsheet · equity-research · difficulty: medium · split: validation · no-op baseline score: 0.556

> Call get_skill_content with slug finance-guidance-tracker. Add a new tab named Guidance and put a note on that tab capturing the workflow steps. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t2 exercise using add_generative_widget, get_skill_content, get_workspace_snapshot, manage_navigation_bar, navigate_workspace with checks layout_out_of_grid, missing_generated_widget, missing_tab, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/workspace_data_control_center_ai_access_prompt_audit@overview; tabs:guidance,overview; generated:note@guidance:guidance,claims.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_ai_access_prompt_audit({})
- Allowed tools (5): `get_workspace_snapshot`, `get_skill_content`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `guidance` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_ai_access_prompt_audit` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "guidance", "claims" on tab `guidance` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-guidance-tracker"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Guidance tracker workflow", "management claims", "evidence gaps" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_skill_finance_tearsheet` — File Finance Tearsheet Under Its Own Tab

**L1** · skill-access · workflow: equity-tearsheet · equity-research · difficulty: medium · split: test · no-op baseline score: 0.556

> Use get_skill_content with slug finance-tearsheet. Add a new tab named Tearsheet and put a note on that tab capturing the workflow steps. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t2 exercise using add_generative_widget, get_skill_content, get_workspace_snapshot, manage_navigation_bar, navigate_workspace with checks layout_out_of_grid, missing_generated_widget, missing_tab, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/workspace_data_control_center_data_health_failed_jobs_trend@overview; tabs:overview,tearsheet; generated:note@tearsheet:tearsheet,valuation.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_data_health_failed_jobs_trend({})
- Allowed tools (5): `get_workspace_snapshot`, `get_skill_content`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `tearsheet` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_data_health_failed_jobs_trend` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "tearsheet", "valuation" on tab `tearsheet` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-tearsheet"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Tearsheet workflow", "valuation", "investment conclusion" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_update_pick_series_dgs2_17` — Update Only The DGS2 Macro Timeseries

**L1** · widget-update · workflow: macro-rates-review · macro · difficulty: medium · split: train · no-op baseline score: 0.800

> Leave the DGS10 Macro Timeseries widget untouched, and update only the DGS2 Macro Timeseries widget to FEDFUNDS.

- Novelty: Unique update/t2 exercise using get_workspace_snapshot, update_widget with checks layout_out_of_grid, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on macro; artifact widgets:Bench Macro/macro_timeseries@*,Bench Macro/macro_timeseries@*.
- Fixture backends: macro
- Initial workspace: dashboard "Selective Update Task"; 2 seeded widget(s): macro_timeseries({"series": "DGS10"}), macro_timeseries({"series": "DGS2"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "FEDFUNDS"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥0× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS2"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_update_pick_symbol_msft_18` — Update Only The MSFT Price Performance

**L1** · widget-update · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.800

> Leave the AAPL Price Performance widget untouched, and update only the MSFT Price Performance widget to NVDA.

- Novelty: Unique update/t2 exercise using get_workspace_snapshot, update_widget with checks layout_out_of_grid, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/price_performance@*,Bench Equities/price_performance@*.
- Fixture backends: equities
- Initial workspace: dashboard "Selective Update Task"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), price_performance({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥0× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_update_pick_symbol_nvda_12` — Update Only The NVDA Latest News

**L1** · widget-update · workflow: equity-tearsheet · equity-research · difficulty: medium · split: validation · no-op baseline score: 0.800

> Leave the AAPL Latest News widget untouched, and update only the NVDA Latest News widget to MSFT.

- Novelty: Unique update/t2 exercise using get_workspace_snapshot, update_widget with checks layout_out_of_grid, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/latest_news@*,Bench Equities/latest_news@*.
- Fixture backends: equities
- Initial workspace: dashboard "Selective Update Task"; 2 seeded widget(s): latest_news({"symbol": "AAPL", "limit": 5}), latest_news({"symbol": "NVDA", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥0× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_update_pick_vendor_factset_48` — Update Only The FactSet Vendor SLA Status

**L1** · widget-update · workflow: vendor-sla-monitoring · data-platform · difficulty: medium · split: test · no-op baseline score: 0.800

> This dashboard has two Vendor SLA Status widgets: one for Bloomberg and one for FactSet. Update only the FactSet one to Refinitiv; leave the Bloomberg widget untouched.

- Novelty: Unique update/t2 exercise using get_workspace_snapshot, update_widget with checks layout_out_of_grid, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status@*,Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status@*.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Selective Update Task"; 2 seeded widget(s): vendor_dataset_monitor_slas_vendor_sla_status({"vendor": "Bloomberg"}), vendor_dataset_monitor_slas_vendor_sla_status({"vendor": "FactSet"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"vendor": "Bloomberg"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"vendor": "Refinitiv"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥0× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"vendor": "FactSet"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_create_preserve_fundamental_metrics_msft` — Extend Dashboard With Fundamental Metrics

**L1** · widget-creation · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.857

> A Estimate History widget is already on this dashboard. Add the Fundamental Metrics widget for MSFT next to it without disturbing the existing widget or overlapping it.

- Novelty: Unique create/t3 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, too_many_widgets, unlisted_widget_id on equities; artifact widgets:Bench Equities/estimate_history@*,Bench Equities/fundamental_metrics@*.
- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): estimate_history({"symbol": "MSFT"})
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `read_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_create_preserve_latest_news_aapl` — Extend Dashboard With Latest News

**L1** · widget-creation · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.857

> This dashboard already has a Price Performance widget. Add the Latest News widget for AAPL next to it without disturbing the existing widget or overlapping it.

- Novelty: Unique create/t3 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, too_many_widgets, unlisted_widget_id on equities; artifact widgets:Bench Equities/latest_news@*,Bench Equities/price_performance@*.
- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): price_performance({"symbol": "AAPL"})
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `read_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL", "limit": 5} → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_create_preserve_risk_metrics_plain` — Extend Dashboard With Risk Metrics

**L1** · widget-creation · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: validation · no-op baseline score: 0.857

> This dashboard already has a Holdings Table widget. Add the Risk Metrics widget next to it without disturbing the existing widget or overlapping it.

- Novelty: Unique create/t3 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, too_many_widgets, unlisted_widget_id on portfolio; artifact widgets:Bench Portfolio/holdings_table@*,Bench Portfolio/risk_metrics@*.
- Fixture backends: portfolio
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): holdings_table({})
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `read_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_create_preserve_yield_curve_plain` — Extend Dashboard With Yield Curve

**L1** · widget-creation · workflow: macro-rates-review · macro · difficulty: medium · split: test · no-op baseline score: 0.857

> Keep the existing Macro Timeseries widget undisturbed and non-overlapped while adding the Yield Curve widget next to it.

- Novelty: Unique create/t3 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_out_of_grid, layout_overlap, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, too_many_widgets, unlisted_widget_id on macro; artifact widgets:Bench Macro/macro_timeseries@*,Bench Macro/yield_curve@*.
- Fixture backends: macro
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): macro_timeseries({"series": "DGS10"})
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `read_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Macro/yield_curve` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_read_client_pair` — Read Data: Client Accounts and Relationship Metrics

**L1** · data-reading · workflow: client-meeting-prep · client-ir · difficulty: hard · split: train · no-op baseline score: 0.375

> On the Bench Stark Enterprise Client Accounts and Relationship Metrics widgets, use get_widget_data, then add a short note that cites client_360_client_book_client_accounts and client_360_client_book_relationship_metrics and says you reviewed the data.

- Novelty: Unique read/t3 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:client_360_client_book_client_accounts,client_360_client_book_relationship_metrics.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): client_360_client_book_client_accounts({"fund": "Flagship Long/Short", "period": "YTD"}), client_360_client_book_relationship_metrics({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "client_360_client_book_client_accounts", "client_360_client_book_relationship_metrics", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "client_360_client_book_client_accounts"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "client_360_client_book_relationship_metrics"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "client_360_client_book_client_accounts" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "client_360_client_book_relationship_metrics" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t3_read_exec_pair` — Read Data: Fills Table and Broker Scorecard

**L1** · data-reading · workflow: execution-exception-review · execution · difficulty: medium · split: train · no-op baseline score: 0.375

> Use get_widget_data for the Bench Stark Enterprise Fills Table and Broker Scorecard widgets; then add a short note that cites execution_desk_fills_fills_table and execution_desk_fills_broker_scorecard and says you reviewed the data.

- Novelty: Unique read/t3 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:execution_desk_fills_fills_table,execution_desk_fills_broker_scorecard.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): execution_desk_fills_fills_table({"fund": "Flagship Long/Short", "period": "YTD"}), execution_desk_fills_broker_scorecard({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "execution_desk_fills_fills_table", "execution_desk_fills_broker_scorecard", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "execution_desk_fills_fills_table"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "execution_desk_fills_broker_scorecard"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "execution_desk_fills_fills_table" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "execution_desk_fills_broker_scorecard" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t3_read_risk_pair` — Read Data: VaR Trend and Drawdown

**L1** · data-reading · workflow: risk-review · risk · difficulty: medium · split: validation · no-op baseline score: 0.375

> On the Bench Stark Enterprise VaR Trend and Drawdown widgets, use get_widget_data, then add a short note that cites risk_exposure_monitor_dashboard_var_trend and risk_exposure_monitor_dashboard_drawdown and says you reviewed the data.

- Novelty: Unique read/t3 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:risk_exposure_monitor_dashboard_var_trend,risk_exposure_monitor_dashboard_drawdown.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): risk_exposure_monitor_dashboard_var_trend({"fund": "Flagship Long/Short", "period": "YTD"}), risk_exposure_monitor_dashboard_drawdown({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "risk_exposure_monitor_dashboard_var_trend", "risk_exposure_monitor_dashboard_drawdown", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "risk_exposure_monitor_dashboard_var_trend"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "risk_exposure_monitor_dashboard_drawdown"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "risk_exposure_monitor_dashboard_var_trend" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "risk_exposure_monitor_dashboard_drawdown" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t3_read_vendor_pair` — Read Data: Vendor SLA Status and Latency by Feed

**L1** · data-reading · workflow: vendor-sla-monitoring · data-platform · difficulty: hard · split: test · no-op baseline score: 0.375

> On the Bench Stark Enterprise Vendor SLA Status and Latency by Feed widgets, use get_widget_data, then add a short note that cites vendor_dataset_monitor_slas_vendor_sla_status and vendor_dataset_monitor_slas_latency_by_feed and says you reviewed the data.

- Novelty: Unique read/t3 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:vendor_dataset_monitor_slas_vendor_sla_status,vendor_dataset_monitor_slas_latency_by_feed.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): vendor_dataset_monitor_slas_vendor_sla_status({"fund": "Flagship Long/Short", "period": "YTD"}), vendor_dataset_monitor_slas_latency_by_feed({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "vendor_dataset_monitor_slas_vendor_sla_status", "vendor_dataset_monitor_slas_latency_by_feed", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "vendor_dataset_monitor_slas_vendor_sla_status"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "vendor_dataset_monitor_slas_latency_by_feed"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "vendor_dataset_monitor_slas_vendor_sla_status" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "vendor_dataset_monitor_slas_latency_by_feed" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t3_skill_finance_comps` — Apply Finance Comps With AAPL

**L1** · skill-access · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.333

> Call get_skill_content with slug finance-comps. Following that workflow, add the Fundamental Metrics widget for AAPL to the active dashboard, then add a note that applies the skill's workflow steps to this widget. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t3 exercise using add_generative_widget, create_widget, get_skill_content, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/fundamental_metrics@*; generated:note@*:comps,peer set.
- Fixture backends: equities
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview
- Allowed tools (6): `get_workspace_snapshot`, `get_skill_content`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "comps", "peer set", "AAPL" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-comps"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Comps workflow", "peer set", "valuation multiples" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_skill_finance_earnings_prep` — Apply Finance Earnings Prep With AAPL

**L1** · skill-access · workflow: earnings-prep · equity-research · difficulty: medium · split: train · no-op baseline score: 0.333

> Call get_skill_content with slug finance-earnings-prep. Following that workflow, add the Estimate History widget for AAPL to the active dashboard, then add a note that applies the skill's workflow steps to this widget. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t3 exercise using add_generative_widget, create_widget, get_skill_content, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/estimate_history@*; generated:note@*:earnings prep,surprise drivers.
- Fixture backends: equities
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview
- Allowed tools (6): `get_workspace_snapshot`, `get_skill_content`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "earnings prep", "surprise drivers", "AAPL" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-earnings-prep"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Earnings prep workflow", "surprise drivers", "portfolio manager" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_skill_finance_guidance_tracker` — Apply Finance Guidance Tracker With AAPL

**L1** · skill-access · workflow: equity-tearsheet · equity-research · difficulty: hard · split: validation · no-op baseline score: 0.333

> Call get_skill_content with slug finance-guidance-tracker. Following that workflow, add the Latest News widget for AAPL to the active dashboard, then add a note that applies the skill's workflow steps to this widget. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t3 exercise using add_generative_widget, create_widget, get_skill_content, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/latest_news@*; generated:note@*:guidance,claims.
- Fixture backends: equities
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview
- Allowed tools (6): `get_workspace_snapshot`, `get_skill_content`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL", "limit": 5} → `missing_widget`
- **Generated note** ≥1× whose content mentions "guidance", "claims", "AAPL" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-guidance-tracker"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Guidance tracker workflow", "management claims", "evidence gaps" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_skill_finance_tearsheet` — Apply Finance Tearsheet With MSFT

**L1** · skill-access · workflow: equity-tearsheet · equity-research · difficulty: medium · split: test · no-op baseline score: 0.333

> After calling get_skill_content with slug finance-tearsheet, follow that workflow by adding the Price Performance widget for MSFT to the active dashboard, then add a note that applies the skill's workflow steps to this widget. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t3 exercise using add_generative_widget, create_widget, get_skill_content, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/price_performance@*; generated:note@*:tearsheet,valuation.
- Fixture backends: equities
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview
- Allowed tools (6): `get_workspace_snapshot`, `get_skill_content`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "tearsheet", "valuation", "MSFT" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-tearsheet"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Tearsheet workflow", "valuation", "investment conclusion" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_layout_grid_grid_eq` — Three-Widget Grid: Grid Eq

**L1** · layout-management · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.667

> Arrange the three AAPL widgets into a grid: price at columns 0-20 rows 0-12, news at columns 20-40 rows 0-12, and estimates full-width below them (40 columns, 8 rows, starting at row 12).

- Novelty: Unique layout/t4 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on equities; artifact layouts::widget_001::0:0:20:12,:widget_002::20:0:20:12,:widget_003::0:12:40:8.
- Fixture backends: equities
- Initial workspace: dashboard "Grid Task"; 3 seeded widget(s): price_performance({"symbol": "AAPL"}), latest_news({"symbol": "AAPL", "limit": 5}), estimate_history({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `widget_001` must sit at exactly x=0, y=0, w=20, h=12 → `layout_mismatch`
- **Layout** `widget_002` must sit at exactly x=20, y=0, w=20, h=12 → `layout_mismatch`
- **Layout** `widget_003` must sit at exactly x=0, y=12, w=40, h=8 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_layout_grid_grid_eq_mixed` — Three-Widget Grid: Grid Eq Mixed

**L1** · layout-management · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.667

> Arrange the three MSFT widgets: price full-width on top (40 columns, 10 rows), then estimates at columns 0-20 and fundamentals at columns 20-40, both 10 rows starting at row 10.

- Novelty: Unique layout/t4 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on equities; artifact layouts::widget_001::0:0:40:10,:widget_002::0:10:20:10,:widget_003::20:10:20:10.
- Fixture backends: equities
- Initial workspace: dashboard "Grid Task"; 3 seeded widget(s): price_performance({"symbol": "MSFT"}), estimate_history({"symbol": "MSFT"}), fundamental_metrics({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `widget_001` must sit at exactly x=0, y=0, w=40, h=10 → `layout_mismatch`
- **Layout** `widget_002` must sit at exactly x=0, y=10, w=20, h=10 → `layout_mismatch`
- **Layout** `widget_003` must sit at exactly x=20, y=10, w=20, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_layout_grid_grid_macro` — Three-Widget Grid: Grid Macro

**L1** · layout-management · workflow: macro-rates-review · macro · difficulty: hard · split: train · no-op baseline score: 0.667

> Set the three macro widgets as a grid: the 2Y series at columns 0-20 rows 0-10, the 10Y series at columns 20-40 rows 0-10, and the yield curve full-width below them (40 columns, 10 rows, starting at row 10).

- Novelty: Unique layout/t4 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on macro; artifact layouts::widget_001::0:0:20:10,:widget_002::20:0:20:10,:widget_003::0:10:40:10.
- Fixture backends: macro
- Initial workspace: dashboard "Grid Task"; 3 seeded widget(s): macro_timeseries({"series": "DGS2"}), macro_timeseries({"series": "DGS10"}), yield_curve({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `widget_001` must sit at exactly x=0, y=0, w=20, h=10 → `layout_mismatch`
- **Layout** `widget_002` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Layout** `widget_003` must sit at exactly x=0, y=10, w=40, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_layout_grid_grid_portfolio` — Three-Widget Grid: Grid Portfolio

**L1** · layout-management · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: test · no-op baseline score: 0.667

> Arrange the three portfolio widgets into a grid: holdings at columns 0-24 rows 0-12, sector exposure at columns 24-40 rows 0-12, and risk metrics full-width below them (40 columns, 8 rows, starting at row 12).

- Novelty: Unique layout/t4 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on portfolio; artifact layouts::widget_001::0:0:24:12,:widget_002::24:0:16:12,:widget_003::0:12:40:8.
- Fixture backends: portfolio
- Initial workspace: dashboard "Grid Task"; 3 seeded widget(s): holdings_table({}), sector_exposure({}), risk_metrics({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `widget_001` must sit at exactly x=0, y=0, w=24, h=12 → `layout_mismatch`
- **Layout** `widget_002` must sit at exactly x=24, y=0, w=16, h=12 → `layout_mismatch`
- **Layout** `widget_003` must sit at exactly x=0, y=12, w=40, h=8 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_read_pm_values` — Read Data: Portfolio Snapshot and Top Alerts

**L1** · data-reading · workflow: portfolio-morning-review · portfolio-management · difficulty: hard · split: train · no-op baseline score: 0.375

> Use get_widget_data for the Bench Stark Enterprise Portfolio Snapshot and Top Alerts widgets; find the exact value for portfolio_command_center_overview_portfolio_snapshot and alert_count for portfolio_command_center_overview_top_alerts, then add a note that cites each widget id, the field name, and the exact value.

- Novelty: Unique read/t4 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:portfolio_command_center_overview_portfolio_snapshot,value.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): portfolio_command_center_overview_portfolio_snapshot({"fund": "Flagship Long/Short", "period": "YTD"}), portfolio_command_center_overview_top_alerts({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "portfolio_command_center_overview_portfolio_snapshot", "value", "87.94", "portfolio_command_center_overview_top_alerts", "alert_count", "193" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "portfolio_command_center_overview_portfolio_snapshot"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "portfolio_command_center_overview_top_alerts"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "portfolio_command_center_overview_portfolio_snapshot", "value", "87.94" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "portfolio_command_center_overview_top_alerts", "alert_count", "193" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t4_read_quant_values` — Read Data: Signal Metrics and Backtest Performance

**L1** · data-reading · workflow: risk-review · risk · difficulty: hard · split: train · no-op baseline score: 0.375

> Use get_widget_data for the Bench Stark Enterprise Signal Metrics and Backtest Performance widgets; find the exact value for quant_research_backtest_lab_signals_signal_metrics and score for quant_research_backtest_lab_backtest_backtest_performance, then add a note that cites each widget id, the field name, and the exact value.

- Novelty: Unique read/t4 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:quant_research_backtest_lab_signals_signal_metrics,value.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): quant_research_backtest_lab_signals_signal_metrics({"fund": "Flagship Long/Short", "period": "YTD"}), quant_research_backtest_lab_backtest_backtest_performance({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "quant_research_backtest_lab_signals_signal_metrics", "value", "83.92", "quant_research_backtest_lab_backtest_backtest_performance", "score", "35.41" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "quant_research_backtest_lab_signals_signal_metrics"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "quant_research_backtest_lab_backtest_backtest_performance"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "quant_research_backtest_lab_signals_signal_metrics", "value", "83.92" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "quant_research_backtest_lab_backtest_backtest_performance", "score", "35.41" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t4_read_risk_values` — Read Data: Risk Snapshot and Limit Utilization

**L1** · data-reading · workflow: risk-review · risk · difficulty: hard · split: train · no-op baseline score: 0.375

> Use get_widget_data for the Bench Stark Enterprise Risk Snapshot and Limit Utilization widgets; find the exact value for risk_exposure_monitor_dashboard_risk_snapshot and exposure for risk_exposure_monitor_limits_limit_utilization, then add a note that cites each widget id, the field name, and the exact value.

- Novelty: Unique read/t4 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:risk_exposure_monitor_dashboard_risk_snapshot,value.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): risk_exposure_monitor_dashboard_risk_snapshot({"fund": "Flagship Long/Short", "period": "YTD"}), risk_exposure_monitor_limits_limit_utilization({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "risk_exposure_monitor_dashboard_risk_snapshot", "value", "0.2878", "risk_exposure_monitor_limits_limit_utilization", "exposure", "0.0339" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "risk_exposure_monitor_dashboard_risk_snapshot"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "risk_exposure_monitor_limits_limit_utilization"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "risk_exposure_monitor_dashboard_risk_snapshot", "value", "0.2878" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "risk_exposure_monitor_limits_limit_utilization", "exposure", "0.0339" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t4_read_stress_values` — Read Data: Days to Liquidate and Risk Snapshot

**L1** · data-reading · workflow: risk-review · risk · difficulty: hard · split: test · no-op baseline score: 0.375

> Use get_widget_data on the Bench Stark Enterprise Days to Liquidate and Risk Snapshot widgets, find the exact score for stress_liquidity_lab_liquidity_days_to_liquidate and value for stress_liquidity_lab_stress_tests_risk_snapshot, then add a note that cites each widget id, the field name, and the exact value.

- Novelty: Unique read/t4 exercise using add_generative_widget, get_widget_data, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact generated:note@*:stress_liquidity_lab_liquidity_days_to_liquidate,score.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): stress_liquidity_lab_liquidity_days_to_liquidate({"fund": "Flagship Long/Short", "period": "YTD"}), stress_liquidity_lab_stress_tests_risk_snapshot({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "stress_liquidity_lab_liquidity_days_to_liquidate", "score", "62.96", "stress_liquidity_lab_stress_tests_risk_snapshot", "value", "83.56" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "stress_liquidity_lab_liquidity_days_to_liquidate"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "stress_liquidity_lab_stress_tests_risk_snapshot"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "stress_liquidity_lab_liquidity_days_to_liquidate", "score", "62.96" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "stress_liquidity_lab_stress_tests_risk_snapshot", "value", "83.56" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t4_skill_finance_comps` — Grounded Finance Comps For NVDA

**L1** · skill-access · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.286

> Use get_skill_content with slug finance-comps. Following that workflow, add the Fundamental Metrics widget for NVDA, read its data, and add a note that cites the exact key value from the data. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t4 exercise using add_generative_widget, create_widget, get_skill_content, get_widget_data, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/fundamental_metrics@*; generated:note@*:NVDA,0.742.
- Fixture backends: equities
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview
- Allowed tools (7): `get_workspace_snapshot`, `get_skill_content`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `get_widget_data`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "NVDA", "0.742", "peer set" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-comps"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"widget_id": "fundamental_metrics"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Comps workflow", "peer set", "valuation multiples" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_skill_finance_earnings_prep` — Grounded Finance Earnings Prep For MSFT

**L1** · skill-access · workflow: earnings-prep · equity-research · difficulty: hard · split: train · no-op baseline score: 0.286

> After calling get_skill_content with slug finance-earnings-prep, follow that workflow by adding the Estimate History widget for MSFT, reading its data, and adding a note that cites the exact key value from the data. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t4 exercise using add_generative_widget, create_widget, get_skill_content, get_widget_data, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/estimate_history@*; generated:note@*:MSFT,3.42.
- Fixture backends: equities
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview
- Allowed tools (7): `get_workspace_snapshot`, `get_skill_content`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `get_widget_data`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "MSFT", "3.42", "surprise drivers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-earnings-prep"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"widget_id": "estimate_history"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Earnings prep workflow", "surprise drivers", "portfolio manager" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_skill_finance_guidance_tracker` — Grounded Finance Guidance Tracker For NVDA

**L1** · skill-access · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.286

> Use get_skill_content with slug finance-guidance-tracker. Following that workflow, add the Estimate History widget for NVDA, read its data, and add a note that cites the exact key value from the data. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t4 exercise using add_generative_widget, create_widget, get_skill_content, get_widget_data, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/estimate_history@*; generated:note@*:NVDA,1.18.
- Fixture backends: equities
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview
- Allowed tools (7): `get_workspace_snapshot`, `get_skill_content`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `get_widget_data`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "NVDA", "1.18", "claims" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-guidance-tracker"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"widget_id": "estimate_history"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Guidance tracker workflow", "management claims", "evidence gaps" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_skill_finance_tearsheet` — Grounded Finance Tearsheet For AAPL

**L1** · skill-access · workflow: equity-tearsheet · equity-research · difficulty: hard · split: test · no-op baseline score: 0.286

> Call get_skill_content with slug finance-tearsheet. Following that workflow, add the Price Performance widget for AAPL, read its data, and add a note that cites the exact key value from the data. Omit dashboard_id when adding the note.

- Novelty: Unique skills/t4 exercise using add_generative_widget, create_widget, get_skill_content, get_widget_data, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/price_performance@*; generated:note@*:AAPL,196.10.
- Fixture backends: equities
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview
- Allowed tools (7): `get_workspace_snapshot`, `get_skill_content`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `get_widget_data`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "AAPL", "196.10", "valuation" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-tearsheet"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"widget_id": "price_performance"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Tearsheet workflow", "valuation", "investment conclusion" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

### L2 — Dashboard construction (76)

#### `gen_t0_backends_add_equities` — Register Bench Equities

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: easy · split: train · no-op baseline score: 0.250

> Use manage_backends with operation add and name equities for Bench Equities; then use manage_backends with operation list.

- Novelty: Unique backends/t0 exercise using manage_backends with checks layout_out_of_grid, missing_tool_call, missing_tool_result, too_many_invalid_calls on equities; artifact id:gen_t0_backends_add_equities.
- Initial workspace: dashboard "Backend Registration"
- Allowed tools (1): `manage_backends`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "list"} must appear in the trace → `missing_tool_call`
- **Tool result** of `manage_backends` must contain "Bench Equities" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_backends_add_macro` — Register Bench Macro

**L2** · dashboard-construction · workflow: macro-rates-review · macro · difficulty: easy · split: train · no-op baseline score: 0.250

> Call manage_backends with operation add and name macro to register Bench Macro, then call manage_backends with operation list.

- Novelty: Unique backends/t0 exercise using manage_backends with checks layout_out_of_grid, missing_tool_call, missing_tool_result, too_many_invalid_calls on macro; artifact id:gen_t0_backends_add_macro.
- Initial workspace: dashboard "Backend Registration"
- Allowed tools (1): `manage_backends`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "list"} must appear in the trace → `missing_tool_call`
- **Tool result** of `manage_backends` must contain "Bench Macro" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_backends_add_portfolio` — Register Bench Portfolio

**L2** · dashboard-construction · workflow: portfolio-risk-review · portfolio-management · difficulty: easy · split: train · no-op baseline score: 0.250

> Use manage_backends with operation add and name portfolio for Bench Portfolio; then use manage_backends with operation list.

- Novelty: Unique backends/t0 exercise using manage_backends with checks layout_out_of_grid, missing_tool_call, missing_tool_result, too_many_invalid_calls on portfolio; artifact id:gen_t0_backends_add_portfolio.
- Initial workspace: dashboard "Backend Registration"
- Allowed tools (1): `manage_backends`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "list"} must appear in the trace → `missing_tool_call`
- **Tool result** of `manage_backends` must contain "Bench Portfolio" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_backends_add_stark_enterprise` — Register Bench Stark Enterprise

**L2** · dashboard-construction · workflow: earnings-prep · equity-research · difficulty: easy · split: validation · no-op baseline score: 0.250

> With manage_backends, use operation add and name stark-enterprise to register Bench Stark Enterprise, then list it with operation list.

- Novelty: Unique backends/t0 exercise using manage_backends with checks layout_out_of_grid, missing_tool_call, missing_tool_result, too_many_invalid_calls on stark-enterprise; artifact id:gen_t0_backends_add_stark_enterprise.
- Initial workspace: dashboard "Backend Registration"
- Allowed tools (1): `manage_backends`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "list"} must appear in the trace → `missing_tool_call`
- **Tool result** of `manage_backends` must contain "Bench Stark Enterprise" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_backends_add_widget_earnings_estimates_monitor_post_earnings_post_earnings_checklist_3` — Register Backend And Add Post-Earnings Checklist

**L2** · dashboard-construction · workflow: earnings-prep · equity-research · difficulty: medium · split: train · no-op baseline score: 0.500

> Call manage_backends with operation add and name stark-enterprise to register Bench Stark Enterprise; then discover earnings_estimates_monitor_post_earnings_post_earnings_checklist, fetch its schema, and add Bench Stark Enterprise/earnings_estimates_monitor_post_earnings_post_earnings_checklist to the active dashboard.

- Novelty: Unique backends/t1 exercise using create_widget, get_widget_schema, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on stark-enterprise; artifact widgets:Bench Stark Enterprise/earnings_estimates_monitor_post_earnings_post_earnings_checklist@*.
- Initial workspace: dashboard "Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_post_earnings_post_earnings_checklist` → `missing_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_backends_add_widget_holdings_table_2` — Register Backend And Add Holdings Table

**L2** · dashboard-construction · workflow: portfolio-risk-review · portfolio-management · difficulty: medium · split: train · no-op baseline score: 0.500

> Use manage_backends with operation add and name portfolio; then discover holdings_table, fetch its schema, and create Bench Portfolio/holdings_table on the active dashboard.

- Novelty: Unique backends/t1 exercise using create_widget, get_widget_schema, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio; artifact widgets:Bench Portfolio/holdings_table@*.
- Initial workspace: dashboard "Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_backends_add_widget_macro_timeseries_1` — Register Backend And Add Macro Timeseries

**L2** · dashboard-construction · workflow: macro-rates-review · macro · difficulty: easy · split: validation · no-op baseline score: 0.500

> Use manage_backends with operation add and name macro; then discover macro_timeseries, fetch its schema, and create Bench Macro/macro_timeseries with data_args {"series": "DGS10"} on the active dashboard.

- Novelty: Unique backends/t1 exercise using create_widget, get_widget_schema, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro; artifact widgets:Bench Macro/macro_timeseries@*.
- Initial workspace: dashboard "Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_backends_add_widget_price_performance_0` — Register Backend And Add Price Performance

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: easy · split: test · no-op baseline score: 0.500

> Use manage_backends with operation add and name equities; then discover price_performance, fetch its schema, and create Bench Equities/price_performance with data_args {"symbol": "AAPL"} on the active dashboard.

- Novelty: Unique backends/t1 exercise using create_widget, get_widget_schema, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/price_performance@*.
- Initial workspace: dashboard "Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_prompts_tool_usage_healthcare_research_dashboard_documents_healthcare_thesis_note_3` — Follow Tool Usage Prompt For Healthcare Thesis Note

**L2** · dashboard-construction · workflow: healthcare-catalyst-review · healthcare-research · difficulty: medium · split: train · no-op baseline score: 0.750

> Before creating Bench Stark Enterprise/healthcare_research_dashboard_documents_healthcare_thesis_note, call get_workspace_prompt with name workspace_tool_usage and follow it by discovering schema.

- Novelty: Unique prompts/t1 exercise using create_widget, get_widget_schema, get_workspace_prompt, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, too_many_widgets, unlisted_widget_id on stark-enterprise; artifact prompts:workspace_tool_usage; widgets:Bench Stark Enterprise/healthcare_research_dashboard_documents_healthcare_thesis_note@*,Bench Stark Enterprise/stress_liquidity_lab_stress_tests_risk_snapshot@.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Prompt Build"; 1 seeded widget(s): stress_liquidity_lab_stress_tests_risk_snapshot({})
- Allowed tools (5): `get_workspace_snapshot`, `get_workspace_prompt`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/healthcare_research_dashboard_documents_healthcare_thesis_note` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_stress_tests_risk_snapshot` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_prompts_tool_usage_macro_timeseries_1` — Follow Tool Usage Prompt For Macro Timeseries

**L2** · dashboard-construction · workflow: macro-rates-review · macro · difficulty: easy · split: train · no-op baseline score: 0.500

> Call get_workspace_prompt with name workspace_tool_usage, then follow it by discovering schema before creating Bench Macro/macro_timeseries with data_args {"series": "DGS10"}.

- Novelty: Unique prompts/t1 exercise using create_widget, get_widget_schema, get_workspace_prompt, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro; artifact prompts:workspace_tool_usage; widgets:Bench Macro/macro_timeseries@*.
- Fixture backends: macro
- Initial workspace: dashboard "Prompt Build"
- Allowed tools (5): `get_workspace_snapshot`, `get_workspace_prompt`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_prompts_tool_usage_price_performance_0` — Follow Tool Usage Prompt For Price Performance

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: easy · split: validation · no-op baseline score: 0.500

> Before creating Bench Equities/price_performance with data_args {"symbol": "AAPL"}, call get_workspace_prompt with name workspace_tool_usage and follow it by discovering schema.

- Novelty: Unique prompts/t1 exercise using create_widget, get_widget_schema, get_workspace_prompt, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact prompts:workspace_tool_usage; widgets:Bench Equities/price_performance@*.
- Fixture backends: equities
- Initial workspace: dashboard "Prompt Build"
- Allowed tools (5): `get_workspace_snapshot`, `get_workspace_prompt`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_prompts_tool_usage_risk_metrics_2` — Follow Tool Usage Prompt For Risk Metrics

**L2** · dashboard-construction · workflow: portfolio-risk-review · portfolio-management · difficulty: medium · split: test · no-op baseline score: 0.500

> Call get_workspace_prompt with name workspace_tool_usage, then follow it by discovering schema before creating Bench Portfolio/risk_metrics.

- Novelty: Unique prompts/t1 exercise using create_widget, get_widget_schema, get_workspace_prompt, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio; artifact prompts:workspace_tool_usage; widgets:Bench Portfolio/risk_metrics@*.
- Fixture backends: portfolio
- Initial workspace: dashboard "Prompt Build"
- Allowed tools (5): `get_workspace_snapshot`, `get_workspace_prompt`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t1_resources_index_client_360` — Read App Index For Client 360

**L2** · dashboard-construction · workflow: portfolio-morning-review · portfolio-management · difficulty: medium · split: train · no-op baseline score: 0.667

> After calling read_workspace_resource with uri openbb://workspace/app-builder/index, add a note naming the Client 360 template id client-360.

- Novelty: Unique resources/t1 exercise using add_generative_widget, get_workspace_snapshot, read_workspace_resource with checks layout_out_of_grid, missing_generated_widget, missing_resource_read, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact resource:openbb://workspace/app-builder/index; widgets:Bench Stark Enterprise/stress_liquidity_lab_stress_tests_scenario_loss_waterfall@; generated:note@*:Client 360,client-360.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "App Index Review"; 1 seeded widget(s): stress_liquidity_lab_stress_tests_scenario_loss_waterfall({})
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_stress_tests_scenario_loss_waterfall` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Client 360", "client-360" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "Client 360", "client-360" (agent must actually retrieve the resource) → `missing_resource_read`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_resources_index_equity_earnings_review` — Read App Index For Equity Earnings Review

**L2** · dashboard-construction · workflow: portfolio-morning-review · portfolio-management · difficulty: easy · split: train · no-op baseline score: 0.333

> After calling read_workspace_resource with uri openbb://workspace/app-builder/index, add a note naming the Equity Earnings Review template id equity-earnings-review.

- Novelty: Unique resources/t1 exercise using add_generative_widget, get_workspace_snapshot, read_workspace_resource with checks layout_out_of_grid, missing_generated_widget, missing_resource_read, too_many_invalid_calls on equities; artifact resource:openbb://workspace/app-builder/index; generated:note@*:Equity Earnings Review,equity-earnings-review.
- Fixture backends: equities
- Initial workspace: dashboard "App Index Review"
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Equity Earnings Review", "equity-earnings-review" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "Equity Earnings Review", "equity-earnings-review" (agent must actually retrieve the resource) → `missing_resource_read`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_resources_index_portfolio_command_center` — Read App Index For Portfolio Command Center

**L2** · dashboard-construction · workflow: portfolio-morning-review · portfolio-management · difficulty: easy · split: validation · no-op baseline score: 0.667

> Call read_workspace_resource with uri openbb://workspace/app-builder/index and add a note naming the Portfolio Command Center template id portfolio-command-center.

- Novelty: Unique resources/t1 exercise using add_generative_widget, get_workspace_snapshot, read_workspace_resource with checks layout_out_of_grid, missing_generated_widget, missing_resource_read, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact resource:openbb://workspace/app-builder/index; widgets:Bench Stark Enterprise/vendor_dataset_monitor_incidents_affected_apps@; generated:note@*:Portfolio Command Center,portfolio-command-center.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "App Index Review"; 1 seeded widget(s): vendor_dataset_monitor_incidents_affected_apps({})
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_incidents_affected_apps` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Portfolio Command Center", "portfolio-command-center" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "Portfolio Command Center", "portfolio-command-center" (agent must actually retrieve the resource) → `missing_resource_read`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_resources_index_risk_exposure_monitor` — Read App Index For Risk Exposure Monitor

**L2** · dashboard-construction · workflow: portfolio-morning-review · portfolio-management · difficulty: medium · split: test · no-op baseline score: 0.667

> After calling read_workspace_resource with uri openbb://workspace/app-builder/index, add a note naming the Risk Exposure Monitor template id risk-exposure-monitor.

- Novelty: Unique resources/t1 exercise using add_generative_widget, get_workspace_snapshot, read_workspace_resource with checks layout_out_of_grid, missing_generated_widget, missing_resource_read, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact resource:openbb://workspace/app-builder/index; widgets:Bench Stark Enterprise/vendor_dataset_monitor_incidents_blast_radius_summary@; generated:note@*:Risk Exposure Monitor,risk-exposure-monitor.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "App Index Review"; 1 seeded widget(s): vendor_dataset_monitor_incidents_blast_radius_summary({})
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_incidents_blast_radius_summary` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Risk Exposure Monitor", "risk-exposure-monitor" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "Risk Exposure Monitor", "risk-exposure-monitor" (agent must actually retrieve the resource) → `missing_resource_read`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_backends_cross_equity_research_workbench_company_ownership_snapshot_risk_metrics_2` — Register Two Backends: Ownership Snapshot And Risk Metrics

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.400

> After registering backend names stark-enterprise and portfolio, fetch each widget's schema and add Bench Stark Enterprise/equity_research_workbench_company_ownership_snapshot and Bench Portfolio/risk_metrics to the active dashboard.

- Novelty: Unique backends/t2 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio, stark-enterprise; artifact widgets:Bench Portfolio/risk_metrics@*,Bench Stark Enterprise/equity_research_workbench_company_ownership_snapshot@*.
- Initial workspace: dashboard "Cross Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 12 · oracle reference trace: 9 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/equity_research_workbench_company_ownership_snapshot` → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Tool call** ≥2× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_backends_cross_fundamental_metrics_holdings_table_3` — Register Two Backends: Fundamental Metrics And Holdings Table

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.400

> Register backend names equities and portfolio; then fetch each widget's schema and add Bench Equities/fundamental_metrics with data_args {"symbol": "NVDA"} and Bench Portfolio/holdings_table to the active dashboard.

- Novelty: Unique backends/t2 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities, portfolio; artifact widgets:Bench Equities/fundamental_metrics@*,Bench Portfolio/holdings_table@*.
- Initial workspace: dashboard "Cross Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 12 · oracle reference trace: 9 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`
- **Tool call** ≥2× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_backends_cross_latest_news_yield_curve_0` — Register Two Backends: Latest News And Yield Curve

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: medium · split: validation · no-op baseline score: 0.400

> Register backend names equities and macro; then fetch each widget's schema and add Bench Equities/latest_news with data_args {"limit": 5, "symbol": "MSFT"} and Bench Macro/yield_curve to the active dashboard.

- Novelty: Unique backends/t2 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities, macro; artifact widgets:Bench Equities/latest_news@*,Bench Macro/yield_curve@*.
- Initial workspace: dashboard "Cross Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 12 · oracle reference trace: 9 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "MSFT", "limit": 5} → `missing_widget`
- **Widget** ≥1× `Bench Macro/yield_curve` → `missing_widget`
- **Tool call** ≥2× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_backends_cross_sector_exposure_macro_timeseries_1` — Register Two Backends: Sector Exposure And Macro Timeseries

**L2** · dashboard-construction · workflow: portfolio-risk-review · portfolio-management · difficulty: medium · split: test · no-op baseline score: 0.400

> Register both backends by name (portfolio, macro); then fetch each widget's schema and add Bench Portfolio/sector_exposure and Bench Macro/macro_timeseries with data_args {"series": "FEDFUNDS"} to the active dashboard.

- Novelty: Unique backends/t2 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro, portfolio; artifact widgets:Bench Macro/macro_timeseries@*,Bench Portfolio/sector_exposure@*.
- Initial workspace: dashboard "Cross Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 12 · oracle reference trace: 9 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "FEDFUNDS"} → `missing_widget`
- **Tool call** ≥2× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_inspect_deduplicate_latest_news_0` — Find Duplicate Latest News

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.818

> Inspect the dashboard, identify the duplicate latest_news among the seeded widgets, and remove exactly one duplicate while preserving the price_performance widget.

- Novelty: Unique inspect/t2 exercise using delete_widget, get_workspace_snapshot, read_widget with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/latest_news@*,Bench Equities/price_performance@*.
- Fixture backends: equities
- Initial workspace: dashboard "Inspect Deduplicate"; 3 seeded widget(s): latest_news({"symbol": "AAPL", "limit": 5}), latest_news({"symbol": "AAPL", "limit": 5}), price_performance({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL", "limit": 5} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_inspect_deduplicate_macro_timeseries_1` — Find Duplicate Macro Timeseries

**L2** · dashboard-construction · workflow: macro-rates-review · macro · difficulty: medium · split: train · no-op baseline score: 0.818

> Preserve the yield_curve widget while inspecting the dashboard, identifying the duplicate macro_timeseries among the seeded widgets, and removing exactly one duplicate.

- Novelty: Unique inspect/t2 exercise using delete_widget, get_workspace_snapshot, read_widget with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on macro; artifact widgets:Bench Macro/macro_timeseries@*,Bench Macro/yield_curve@*.
- Fixture backends: macro
- Initial workspace: dashboard "Inspect Deduplicate"; 3 seeded widget(s): macro_timeseries({"series": "DGS2"}), macro_timeseries({"series": "DGS2"}), yield_curve({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS2"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Macro/yield_curve` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_inspect_deduplicate_rebalance_scenario_lab_drift_drift_by_sleeve_3` — Find Duplicate Drift by Sleeve

**L2** · dashboard-construction · workflow: portfolio-morning-review · portfolio-management · difficulty: medium · split: validation · no-op baseline score: 0.818

> After inspecting the dashboard, identify the duplicate rebalance_scenario_lab_drift_drift_by_sleeve among the seeded widgets and remove exactly one duplicate while preserving the rebalance_scenario_lab_overview_workflow_overview widget.

- Novelty: Unique inspect/t2 exercise using delete_widget, get_workspace_snapshot, read_widget with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/rebalance_scenario_lab_drift_drift_by_sleeve@*,Bench Stark Enterprise/rebalance_scenario_lab_overview_workflow_overview@*.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Inspect Deduplicate"; 3 seeded widget(s): rebalance_scenario_lab_drift_drift_by_sleeve({}), rebalance_scenario_lab_drift_drift_by_sleeve({}), rebalance_scenario_lab_overview_workflow_overview({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/rebalance_scenario_lab_drift_drift_by_sleeve` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/rebalance_scenario_lab_overview_workflow_overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_inspect_deduplicate_risk_metrics_2` — Find Duplicate Risk Metrics

**L2** · dashboard-construction · workflow: portfolio-risk-review · portfolio-management · difficulty: medium · split: test · no-op baseline score: 0.818

> Preserve the holdings_table widget while inspecting the dashboard, identifying the duplicate risk_metrics among the seeded widgets, and removing exactly one duplicate.

- Novelty: Unique inspect/t2 exercise using delete_widget, get_workspace_snapshot, read_widget with checks layout_out_of_grid, layout_overlap, missing_tool_call, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on portfolio; artifact widgets:Bench Portfolio/holdings_table@*,Bench Portfolio/risk_metrics@*.
- Fixture backends: portfolio
- Initial workspace: dashboard "Inspect Deduplicate"; 3 seeded widget(s): risk_metrics({}), risk_metrics({}), holdings_table({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_params_place_sector_compliance_surveillance_hub_audit_access_and_export_logs_11` — Options-Constrained Placement For Access and Export Logs

**L2** · dashboard-construction · workflow: compliance-surveillance · compliance · difficulty: medium · split: train · no-op baseline score: 0.667

> Create Bench Stark Enterprise/compliance_surveillance_hub_audit_access_and_export_logs after fetching the widget schema and using get_params_options to choose Consumer Staples for sector, then place it at x=20, y=0, width 20, height 10.

- Novelty: Unique params/t2 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, too_many_widgets, unlisted_widget_id on stark-enterprise; artifact widgets:Bench Stark Enterprise/compliance_surveillance_hub_audit_access_and_export_logs@*,Bench Stark Enterprise/vendor_dataset_monitor_vendors_vendor_sla_status@; layouts:compliance_surveillance_hub_audit_access_and_export_logs:::20:0:20:10.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Parameter Placement"; 1 seeded widget(s): vendor_dataset_monitor_vendors_vendor_sla_status({})
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_audit_access_and_export_logs` with data_args ⊇ {"sector": "Consumer Staples"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_vendor_sla_status` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Layout** `compliance_surveillance_hub_audit_access_and_export_logs` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Tool result** of `get_params_options` must contain "Consumer Staples" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_params_place_sector_sector_exposure_10` — Options-Constrained Placement For Sector Exposure

**L2** · dashboard-construction · workflow: portfolio-risk-review · portfolio-management · difficulty: medium · split: train · no-op baseline score: 0.400

> Create Bench Portfolio/sector_exposure after fetching the widget schema and using get_params_options to choose Technology for sector, then place it at x=0, y=0, width 20, height 10.

- Novelty: Unique params/t2 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio; artifact widgets:Bench Portfolio/sector_exposure@*; layouts:sector_exposure:::0:0:20:10.
- Fixture backends: portfolio
- Initial workspace: dashboard "Parameter Placement"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` with data_args ⊇ {"sector": "Technology"} → `missing_widget`
- **Layout** `sector_exposure` must sit at exactly x=0, y=0, w=20, h=10 → `layout_mismatch`
- **Tool result** of `get_params_options` must contain "Technology" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_params_place_series_macro_timeseries_9` — Options-Constrained Placement For Macro Timeseries

**L2** · dashboard-construction · workflow: macro-rates-review · macro · difficulty: medium · split: validation · no-op baseline score: 0.400

> Create Bench Macro/macro_timeseries after fetching the widget schema and using get_params_options to choose DGS10 for series, then place it at x=20, y=0, width 20, height 10.

- Novelty: Unique params/t2 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro; artifact widgets:Bench Macro/macro_timeseries@*; layouts:macro_timeseries:::20:0:20:10.
- Fixture backends: macro
- Initial workspace: dashboard "Parameter Placement"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Layout** `macro_timeseries` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Tool result** of `get_params_options` must contain "DGS10" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_params_place_symbol_price_performance_8` — Options-Constrained Placement For Price Performance

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: medium · split: test · no-op baseline score: 0.400

> Create Bench Equities/price_performance after fetching the widget schema and using get_params_options to choose AAPL for symbol, then place it at x=0, y=0, width 20, height 10.

- Novelty: Unique params/t2 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/price_performance@*; layouts:price_performance:::0:0:20:10.
- Fixture backends: equities
- Initial workspace: dashboard "Parameter Placement"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Layout** `price_performance` must sit at exactly x=0, y=0, w=20, h=10 → `layout_mismatch`
- **Tool result** of `get_params_options` must contain "AAPL" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_prompts_session_tab_estimates_estimate_history` — Use Session Prompt On Estimates

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.429

> After fetching workspace_session_context, add a Estimates tab, navigate to it, fetch the widget schema, create Bench Equities/estimate_history with data_args {"symbol": "MSFT"} there, and add a note mentioning Estimates on that tab.

- Novelty: Unique prompts/t2 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_prompt, list_available_widgets, manage_navigation_bar, navigate_workspace with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tab, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact prompts:workspace_session_context; widgets:Bench Equities/estimate_history@estimates; tabs:estimates,overview; generated:note@estimates:Estimates.
- Fixture backends: equities
- Initial workspace: dashboard "Prompt Session"; 1 tab(s): overview
- Allowed tools (7): `get_workspace_prompt`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `estimates` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "MSFT"} on tab `estimates` → `missing_widget`
- **Generated note** ≥1× whose content mentions "Estimates" on tab `estimates` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool result** of `get_workspace_prompt` must contain "current-dashboard current-tab session grounding" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_prompts_session_tab_exposure_sector_exposure` — Use Session Prompt On Exposure

**L2** · dashboard-construction · workflow: portfolio-risk-review · portfolio-management · difficulty: medium · split: train · no-op baseline score: 0.429

> After fetching workspace_session_context, add a Exposure tab, navigate to it, fetch the widget schema, create Bench Portfolio/sector_exposure there, and add a note mentioning Exposure on that tab.

- Novelty: Unique prompts/t2 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_prompt, list_available_widgets, manage_navigation_bar, navigate_workspace with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tab, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio; artifact prompts:workspace_session_context; widgets:Bench Portfolio/sector_exposure@exposure; tabs:exposure,overview; generated:note@exposure:Exposure.
- Fixture backends: portfolio
- Initial workspace: dashboard "Prompt Session"; 1 tab(s): overview
- Allowed tools (7): `get_workspace_prompt`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `exposure` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Portfolio/sector_exposure` on tab `exposure` → `missing_widget`
- **Generated note** ≥1× whose content mentions "Exposure" on tab `exposure` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool result** of `get_workspace_prompt` must contain "current-dashboard current-tab session grounding" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_prompts_session_tab_ops_liquidity_tca_workbench_tca_slippage_by_algo` — Use Session Prompt On Ops

**L2** · dashboard-construction · workflow: execution-exception-review · execution · difficulty: medium · split: validation · no-op baseline score: 0.636

> After fetching workspace_session_context, add a Ops tab, navigate to it, fetch the widget schema, create Bench Stark Enterprise/liquidity_tca_workbench_tca_slippage_by_algo there, and add a note mentioning Ops on that tab.

- Novelty: Unique prompts/t2 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_prompt, list_available_widgets, manage_navigation_bar, navigate_workspace with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tab, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, too_many_widgets, unlisted_widget_id on stark-enterprise; artifact prompts:workspace_session_context; widgets:Bench Stark Enterprise/liquidity_tca_workbench_tca_slippage_by_algo@ops,Bench Stark Enterprise/workspace_data_control_center_ai_access_ai_usage_by_role@overview; tabs:ops,overview; generated:note@ops:Ops.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Prompt Session"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_ai_access_ai_usage_by_role({})
- Allowed tools (7): `get_workspace_prompt`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `ops` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/liquidity_tca_workbench_tca_slippage_by_algo` on tab `ops` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_ai_access_ai_usage_by_role` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Ops" on tab `ops` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool result** of `get_workspace_prompt` must contain "current-dashboard current-tab session grounding" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_prompts_session_tab_rates_yield_curve` — Use Session Prompt On Rates

**L2** · dashboard-construction · workflow: macro-rates-review · macro · difficulty: medium · split: test · no-op baseline score: 0.429

> Fetch workspace_session_context, add a Rates tab, navigate to it, fetch the widget schema, create Bench Macro/yield_curve there, and add a note mentioning Rates on that tab.

- Novelty: Unique prompts/t2 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_prompt, list_available_widgets, manage_navigation_bar, navigate_workspace with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tab, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro; artifact prompts:workspace_session_context; widgets:Bench Macro/yield_curve@rates; tabs:overview,rates; generated:note@rates:Rates.
- Fixture backends: macro
- Initial workspace: dashboard "Prompt Session"; 1 tab(s): overview
- Allowed tools (7): `get_workspace_prompt`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `rates` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Macro/yield_curve` on tab `rates` → `missing_widget`
- **Generated note** ≥1× whose content mentions "Rates" on tab `rates` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool result** of `get_workspace_prompt` must contain "current-dashboard current-tab session grounding" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t2_resources_instantiate_compliance_surveillance_hub` — Read Index Then Instantiate Compliance Surveillance Hub

**L2** · dashboard-construction · workflow: portfolio-morning-review · portfolio-management · difficulty: medium · split: train · no-op baseline score: 0.250

> Use the app-builder index resource openbb://workspace/app-builder/index, then instantiate template compliance-surveillance-hub as a dashboard named Compliance Resource Dashboard.

- Novelty: Unique resources/t2 exercise using manage_apps, manage_backends, read_workspace_resource with checks dashboard_name, layout_out_of_grid, missing_resource_read, missing_tool_call, too_many_invalid_calls on stark-enterprise; artifact resource:openbb://workspace/app-builder/index; apps:compliance-surveillance-hub.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `read_workspace_resource`, `manage_backends`, `manage_apps`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Compliance Resource Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "compliance-surveillance-hub" (agent must actually retrieve the resource) → `missing_resource_read`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_resources_instantiate_equity_earnings_review` — Read Index Then Instantiate Equity Earnings Review

**L2** · dashboard-construction · workflow: earnings-prep · equity-research · difficulty: medium · split: train · no-op baseline score: 0.250

> After reading the app-builder index resource openbb://workspace/app-builder/index, instantiate template equity-earnings-review as a dashboard named Equity Resource Dashboard.

- Novelty: Unique resources/t2 exercise using manage_apps, manage_backends, read_workspace_resource with checks dashboard_name, layout_out_of_grid, missing_resource_read, missing_tool_call, too_many_invalid_calls on equities; artifact resource:openbb://workspace/app-builder/index; apps:equity-earnings-review.
- Fixture backends: equities
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `read_workspace_resource`, `manage_backends`, `manage_apps`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Equity Resource Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "equity-earnings-review" (agent must actually retrieve the resource) → `missing_resource_read`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_resources_instantiate_execution_desk` — Read Index Then Instantiate Execution Desk

**L2** · dashboard-construction · workflow: portfolio-morning-review · portfolio-management · difficulty: medium · split: validation · no-op baseline score: 0.250

> Read the app-builder index resource at openbb://workspace/app-builder/index, then instantiate template execution-desk as a dashboard named Execution Resource Dashboard.

- Novelty: Unique resources/t2 exercise using manage_apps, manage_backends, read_workspace_resource with checks dashboard_name, layout_out_of_grid, missing_resource_read, missing_tool_call, too_many_invalid_calls on stark-enterprise; artifact resource:openbb://workspace/app-builder/index; apps:execution-desk.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `read_workspace_resource`, `manage_backends`, `manage_apps`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Execution Resource Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "execution-desk" (agent must actually retrieve the resource) → `missing_resource_read`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_resources_instantiate_vendor_dataset_monitor` — Read Index Then Instantiate Vendor & Dataset Monitor

**L2** · dashboard-construction · workflow: portfolio-morning-review · portfolio-management · difficulty: medium · split: test · no-op baseline score: 0.250

> Read the app-builder index resource at openbb://workspace/app-builder/index, then instantiate template vendor-dataset-monitor as a dashboard named Vendor Resource Dashboard.

- Novelty: Unique resources/t2 exercise using manage_apps, manage_backends, read_workspace_resource with checks dashboard_name, layout_out_of_grid, missing_resource_read, missing_tool_call, too_many_invalid_calls on stark-enterprise; artifact resource:openbb://workspace/app-builder/index; apps:vendor-dataset-monitor.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `read_workspace_resource`, `manage_backends`, `manage_apps`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vendor Resource Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "vendor-dataset-monitor" (agent must actually retrieve the resource) → `missing_resource_read`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t3_backends_refresh_earnings_estimates_monitor_post_earnings_post_earnings_checklist_3` — Refresh Backend Before Building Post-Earnings Checklist

**L2** · dashboard-construction · workflow: earnings-prep · equity-research · difficulty: hard · split: train · no-op baseline score: 0.400

> After registering backend name stark-enterprise and refreshing Bench Stark Enterprise, add Bench Stark Enterprise/earnings_estimates_monitor_post_earnings_post_earnings_checklist and document that the backend was refreshed.

- Novelty: Unique backends/t3 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on stark-enterprise; artifact widgets:Bench Stark Enterprise/earnings_estimates_monitor_post_earnings_post_earnings_checklist@*; generated:note@*:refreshed,Bench Stark Enterprise.
- Initial workspace: dashboard "Backend Refresh Build"
- Allowed tools (6): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_post_earnings_post_earnings_checklist` → `missing_widget`
- **Generated note** ≥1× whose content mentions "refreshed", "Bench Stark Enterprise" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "refresh"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_backends_refresh_holdings_table_2` — Refresh Backend Before Building Holdings Table

**L2** · dashboard-construction · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: train · no-op baseline score: 0.400

> Register Bench Portfolio with backend name portfolio, refresh it, then add Bench Portfolio/holdings_table and document that the backend was refreshed.

- Novelty: Unique backends/t3 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio; artifact widgets:Bench Portfolio/holdings_table@*; generated:note@*:refreshed,Bench Portfolio.
- Initial workspace: dashboard "Backend Refresh Build"
- Allowed tools (6): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`
- **Generated note** ≥1× whose content mentions "refreshed", "Bench Portfolio" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "refresh"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_backends_refresh_macro_timeseries_1` — Refresh Backend Before Building Macro Timeseries

**L2** · dashboard-construction · workflow: macro-rates-review · macro · difficulty: medium · split: validation · no-op baseline score: 0.400

> Register backend name macro for Bench Macro, refresh it, then add Bench Macro/macro_timeseries with data_args {"series": "DGS10"} and document that the backend was refreshed.

- Novelty: Unique backends/t3 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro; artifact widgets:Bench Macro/macro_timeseries@*; generated:note@*:refreshed,Bench Macro.
- Initial workspace: dashboard "Backend Refresh Build"
- Allowed tools (6): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "refreshed", "Bench Macro" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "refresh"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_backends_refresh_price_performance_0` — Refresh Backend Before Building Price Performance

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: medium · split: test · no-op baseline score: 0.400

> After registering backend name equities and refreshing Bench Equities, add Bench Equities/price_performance with data_args {"symbol": "AAPL"} and document that the backend was refreshed.

- Novelty: Unique backends/t3 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/price_performance@*; generated:note@*:refreshed,Bench Equities.
- Initial workspace: dashboard "Backend Refresh Build"
- Allowed tools (6): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "refreshed", "Bench Equities" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "refresh"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_params_companion_sector_corporate_access_meeting_notes_claims_evidence_and_sign_off_history_3` — Options-Constrained Pair For Evidence and Sign-Off History

**L2** · dashboard-construction · workflow: compliance-surveillance · compliance · difficulty: hard · split: train · no-op baseline score: 0.545

> Use get_params_options to set Bench Stark Enterprise/corporate_access_meeting_notes_claims_evidence_and_sign_off_history sector=Communication Services, then add companion widget corporate_access_meeting_notes_claims_management_claims_tracker. Arrange both without overlap.

- Novelty: Unique params/t3 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, too_many_widgets, unlisted_widget_id on stark-enterprise; artifact widgets:Bench Stark Enterprise/corporate_access_meeting_notes_claims_evidence_and_sign_off_history@*,Bench Stark Enterprise/corporate_access_meeting_notes_claims_management_claims_tracker@*,Bench Stark Enterprise/workspace_data_control_center_entitlements_role_coverage@; layouts:corporate_access_meeting_notes_claims_evidence_and_sign_off_history:::0:0:20:10,corporate_access_meeting_notes_claims_management_claims_tracker:::20:0:20:10.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Parameter Pair"; 1 seeded widget(s): workspace_data_control_center_entitlements_role_coverage({})
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`
- Turn budget: 13 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/corporate_access_meeting_notes_claims_evidence_and_sign_off_history` with data_args ⊇ {"sector": "Communication Services"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/corporate_access_meeting_notes_claims_management_claims_tracker` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_entitlements_role_coverage` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Layout** `corporate_access_meeting_notes_claims_evidence_and_sign_off_history` must sit at exactly x=0, y=0, w=20, h=10 → `layout_mismatch`
- **Layout** `corporate_access_meeting_notes_claims_management_claims_tracker` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Tool result** of `get_params_options` must contain "Communication Services" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_params_companion_sector_sector_exposure_2` — Options-Constrained Pair For Sector Exposure

**L2** · dashboard-construction · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: train · no-op baseline score: 0.286

> Set Bench Portfolio/sector_exposure sector=Technology using get_params_options, then add companion widget risk_metrics. Arrange both without overlap.

- Novelty: Unique params/t3 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio; artifact widgets:Bench Portfolio/risk_metrics@*,Bench Portfolio/sector_exposure@*; layouts:risk_metrics:::20:0:20:10,sector_exposure:::0:0:20:10.
- Fixture backends: portfolio
- Initial workspace: dashboard "Parameter Pair"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`
- Turn budget: 13 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` with data_args ⊇ {"sector": "Technology"} → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Layout** `sector_exposure` must sit at exactly x=0, y=0, w=20, h=10 → `layout_mismatch`
- **Layout** `risk_metrics` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Tool result** of `get_params_options` must contain "Technology" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_params_companion_series_macro_timeseries_1` — Options-Constrained Pair For Macro Timeseries

**L2** · dashboard-construction · workflow: macro-rates-review · macro · difficulty: medium · split: validation · no-op baseline score: 0.286

> Use get_params_options to set Bench Macro/macro_timeseries series=DGS2, then add companion widget yield_curve. Arrange both without overlap.

- Novelty: Unique params/t3 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro; artifact widgets:Bench Macro/macro_timeseries@*,Bench Macro/yield_curve@*; layouts:macro_timeseries:::0:0:20:10,yield_curve:::20:0:20:10.
- Fixture backends: macro
- Initial workspace: dashboard "Parameter Pair"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`
- Turn budget: 13 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS2"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/yield_curve` → `missing_widget`
- **Layout** `macro_timeseries` must sit at exactly x=0, y=0, w=20, h=10 → `layout_mismatch`
- **Layout** `yield_curve` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Tool result** of `get_params_options` must contain "DGS2" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_params_companion_symbol_price_performance_0` — Options-Constrained Pair For Price Performance

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: medium · split: test · no-op baseline score: 0.286

> After using get_params_options for Bench Equities/price_performance symbol=AAPL, add companion widget latest_news and arrange both without overlap.

- Novelty: Unique params/t3 exercise using create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/latest_news@*,Bench Equities/price_performance@*; layouts:latest_news:::20:0:20:10,price_performance:::0:0:20:10.
- Fixture backends: equities
- Initial workspace: dashboard "Parameter Pair"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`
- Turn budget: 13 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL", "limit": 5} → `missing_widget`
- **Layout** `price_performance` must sit at exactly x=0, y=0, w=20, h=10 → `layout_mismatch`
- **Layout** `latest_news` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Tool result** of `get_params_options` must contain "AAPL" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_prompts_dashboard_aapl_prompt_dashboard` — AAPL Prompt Dashboard

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.286

> After fetching workspace_tool_usage, create dashboard AAPL Prompt Dashboard, add Bench Equities/price_performance with data_args {"symbol": "AAPL"} and Bench Equities/latest_news with data_args {"limit": 5, "symbol": "AAPL"} with schema-first discipline, and add a note mentioning AAPL and schema.

- Novelty: Unique prompts/t3 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_prompt, list_available_widgets, manage_dashboard with checks dashboard_name, layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact prompts:workspace_tool_usage; widgets:Bench Equities/latest_news@*,Bench Equities/price_performance@*; generated:note@*:AAPL,schema.
- Fixture backends: equities
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (6): `get_workspace_prompt`, `manage_dashboard`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 9 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "AAPL Prompt Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL", "limit": 5} → `missing_widget`
- **Generated note** ≥1× whose content mentions "AAPL", "schema" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_prompts_dashboard_macro_prompt_dashboard` — Macro Prompt Dashboard

**L2** · dashboard-construction · workflow: macro-rates-review · macro · difficulty: medium · split: train · no-op baseline score: 0.286

> Get workspace_tool_usage, create dashboard Macro Prompt Dashboard, add Bench Macro/macro_timeseries with data_args {"series": "DGS2"} and Bench Macro/yield_curve with schema-first discipline, and add a note mentioning DGS2 and schema.

- Novelty: Unique prompts/t3 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_prompt, list_available_widgets, manage_dashboard with checks dashboard_name, layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro; artifact prompts:workspace_tool_usage; widgets:Bench Macro/macro_timeseries@*,Bench Macro/yield_curve@*; generated:note@*:DGS2,schema.
- Fixture backends: macro
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (6): `get_workspace_prompt`, `manage_dashboard`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 9 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Macro Prompt Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS2"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/yield_curve` → `missing_widget`
- **Generated note** ≥1× whose content mentions "DGS2", "schema" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_prompts_dashboard_portfolio_prompt_dashboard` — Portfolio Prompt Dashboard

**L2** · dashboard-construction · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: validation · no-op baseline score: 0.286

> After fetching workspace_tool_usage, create dashboard Portfolio Prompt Dashboard, add Bench Portfolio/holdings_table and Bench Portfolio/risk_metrics with schema-first discipline, and add a note mentioning holdings and schema.

- Novelty: Unique prompts/t3 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_prompt, list_available_widgets, manage_dashboard with checks dashboard_name, layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio; artifact prompts:workspace_tool_usage; widgets:Bench Portfolio/holdings_table@*,Bench Portfolio/risk_metrics@*; generated:note@*:holdings,schema.
- Fixture backends: portfolio
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (6): `get_workspace_prompt`, `manage_dashboard`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 9 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Portfolio Prompt Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Generated note** ≥1× whose content mentions "holdings", "schema" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_prompts_dashboard_stark_prompt_dashboard` — Stark Prompt Dashboard

**L2** · dashboard-construction · workflow: compliance-surveillance · compliance · difficulty: hard · split: test · no-op baseline score: 0.286

> Fetch workspace_tool_usage, create dashboard Stark Prompt Dashboard, add Bench Stark Enterprise/mnpi_research_review_research_draft_research_review and Bench Stark Enterprise/mnpi_research_review_research_evidence_and_sign_off_history with schema-first discipline, and add a note mentioning stark and schema.

- Novelty: Unique prompts/t3 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_prompt, list_available_widgets, manage_dashboard with checks dashboard_name, layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on stark-enterprise; artifact prompts:workspace_tool_usage; widgets:Bench Stark Enterprise/mnpi_research_review_research_draft_research_review@*,Bench Stark Enterprise/mnpi_research_review_research_evidence_and_sign_off_history@*; generated:note@*:stark,schema.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (6): `get_workspace_prompt`, `manage_dashboard`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 9 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Stark Prompt Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/mnpi_research_review_research_draft_research_review` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/mnpi_research_review_research_evidence_and_sign_off_history` → `missing_widget`
- **Generated note** ≥1× whose content mentions "stark", "schema" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_resources_skill_build_finance_comps` — Build From Skill Resource finance-comps

**L2** · dashboard-construction · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: train · no-op baseline score: 0.400

> Read resource openbb://workspace/skills/finance-comps, add Bench Portfolio/sector_exposure, and add a note that mentions peer set.

- Novelty: Unique resources/t3 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, read_workspace_resource with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_resource_read, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio; artifact resource:openbb://workspace/skills/finance-comps; widgets:Bench Portfolio/sector_exposure@*; generated:note@*:peer set.
- Fixture backends: portfolio
- Initial workspace: dashboard "Resource Build"
- Allowed tools (6): `get_workspace_snapshot`, `read_workspace_resource`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`
- **Generated note** ≥1× whose content mentions "peer set" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/skills/finance-comps` must contain "peer set" (agent must actually retrieve the resource) → `missing_resource_read`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_resources_skill_build_finance_earnings_prep` — Build From Skill Resource finance-earnings-prep

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.400

> Use read_workspace_resource on openbb://workspace/skills/finance-earnings-prep, then add Bench Equities/estimate_history with data_args {"symbol": "AAPL"} and add a note that mentions surprise drivers.

- Novelty: Unique resources/t3 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, read_workspace_resource with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_resource_read, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact resource:openbb://workspace/skills/finance-earnings-prep; widgets:Bench Equities/estimate_history@*; generated:note@*:surprise drivers.
- Fixture backends: equities
- Initial workspace: dashboard "Resource Build"
- Allowed tools (6): `get_workspace_snapshot`, `read_workspace_resource`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "surprise drivers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/skills/finance-earnings-prep` must contain "surprise drivers" (agent must actually retrieve the resource) → `missing_resource_read`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_resources_skill_build_finance_guidance_tracker` — Build From Skill Resource finance-guidance-tracker

**L2** · dashboard-construction · workflow: portfolio-morning-review · portfolio-management · difficulty: hard · split: validation · no-op baseline score: 0.667

> Use read_workspace_resource on openbb://workspace/skills/finance-guidance-tracker, then add Bench Stark Enterprise/executive_investment_dashboard_risk_limit_utilization and add a note that mentions evidence gaps.

- Novelty: Unique resources/t3 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, read_workspace_resource with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_resource_read, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, too_many_widgets, unlisted_widget_id on stark-enterprise; artifact resource:openbb://workspace/skills/finance-guidance-tracker; widgets:Bench Stark Enterprise/executive_investment_dashboard_risk_limit_utilization@*,Bench Stark Enterprise/workspace_data_control_center_entitlements_sensitive_dataset_flags@; generated:note@*:evidence gaps.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Resource Build"; 1 seeded widget(s): workspace_data_control_center_entitlements_sensitive_dataset_flags({})
- Allowed tools (6): `get_workspace_snapshot`, `read_workspace_resource`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/executive_investment_dashboard_risk_limit_utilization` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_entitlements_sensitive_dataset_flags` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "evidence gaps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/skills/finance-guidance-tracker` must contain "evidence gaps" (agent must actually retrieve the resource) → `missing_resource_read`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_resources_skill_build_finance_tearsheet` — Build From Skill Resource finance-tearsheet

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: medium · split: test · no-op baseline score: 0.400

> Read resource openbb://workspace/skills/finance-tearsheet, add Bench Equities/fundamental_metrics with data_args {"symbol": "MSFT"}, and add a note that mentions valuation.

- Novelty: Unique resources/t3 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, read_workspace_resource with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_resource_read, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact resource:openbb://workspace/skills/finance-tearsheet; widgets:Bench Equities/fundamental_metrics@*; generated:note@*:valuation.
- Fixture backends: equities
- Initial workspace: dashboard "Resource Build"
- Allowed tools (6): `get_workspace_snapshot`, `read_workspace_resource`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "valuation" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/skills/finance-tearsheet` must contain "valuation" (agent must actually retrieve the resource) → `missing_resource_read`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_backends_multi_equities_macro` — Multi-Backend Build: Equities Macro

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.333

> Register backend names equities, macro, build a dashboard with Bench Equities/price_performance with data_args {"symbol": "AAPL"} and Bench Macro/macro_timeseries with data_args {"series": "DGS10"}, and add a note mentioning AAPL and DGS10.

- Novelty: Unique backends/t4 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities, macro; artifact widgets:Bench Equities/price_performance@*,Bench Macro/macro_timeseries@*; generated:note@*:AAPL,DGS10.
- Initial workspace: dashboard "Multi Backend Build"
- Allowed tools (6): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "AAPL", "DGS10" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥2× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_backends_multi_equities_portfolio` — Multi-Backend Build: Equities Portfolio

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.333

> After registering backend names equities, portfolio, build a dashboard with Bench Equities/latest_news with data_args {"limit": 5, "symbol": "NVDA"} and Bench Portfolio/holdings_table, and add a note mentioning NVDA and holdings.

- Novelty: Unique backends/t4 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities, portfolio; artifact widgets:Bench Equities/latest_news@*,Bench Portfolio/holdings_table@*; generated:note@*:NVDA,holdings.
- Initial workspace: dashboard "Multi Backend Build"
- Allowed tools (6): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "NVDA", "limit": 5} → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`
- **Generated note** ≥1× whose content mentions "NVDA", "holdings" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥2× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_backends_multi_portfolio_macro` — Multi-Backend Build: Portfolio Macro

**L2** · dashboard-construction · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: train · no-op baseline score: 0.333

> After registering backend names portfolio, macro, build a dashboard with Bench Portfolio/risk_metrics and Bench Macro/yield_curve, and add a note mentioning portfolio and yield curve.

- Novelty: Unique backends/t4 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro, portfolio; artifact widgets:Bench Macro/yield_curve@*,Bench Portfolio/risk_metrics@*; generated:note@*:portfolio,yield curve.
- Initial workspace: dashboard "Multi Backend Build"
- Allowed tools (6): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Widget** ≥1× `Bench Macro/yield_curve` → `missing_widget`
- **Generated note** ≥1× whose content mentions "portfolio", "yield curve" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥2× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_backends_multi_stark_portfolio` — Multi-Backend Build: Stark Portfolio

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: hard · split: test · no-op baseline score: 0.333

> Register backend names stark-enterprise, portfolio, build a dashboard with Bench Stark Enterprise/equity_research_workbench_valuation_football_field and Bench Portfolio/sector_exposure, and add a note mentioning stark and sector exposure.

- Novelty: Unique backends/t4 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_backends with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio, stark-enterprise; artifact widgets:Bench Portfolio/sector_exposure@*,Bench Stark Enterprise/equity_research_workbench_valuation_football_field@*; generated:note@*:stark,sector exposure.
- Initial workspace: dashboard "Multi Backend Build"
- Allowed tools (6): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/equity_research_workbench_valuation_football_field` → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`
- **Generated note** ≥1× whose content mentions "stark", "sector exposure" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥2× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_create_cross_aapl_rates` — Cross-Backend Build: Aapl Rates

**L2** · widget-creation · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.400

> Add these two widgets to the active dashboard: the Price Performance widget from Bench Equities for AAPL and the Macro Timeseries widget from Bench Macro for DGS10. Then add a note mentioning AAPL and DGS10.

- Novelty: Unique create/t4 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities, macro; artifact widgets:Bench Equities/price_performance@*,Bench Macro/macro_timeseries@*; generated:note@*:AAPL,DGS10.
- Fixture backends: equities, macro
- Initial workspace: dashboard "Cross-Backend Task"
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 8 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "AAPL", "DGS10" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_create_cross_book_inflation` — Cross-Backend Build: Book Inflation

**L2** · widget-creation · workflow: macro-rates-review · macro · difficulty: hard · split: train · no-op baseline score: 0.400

> On the active dashboard, add these two widgets: the Holdings Table widget from Bench Portfolio and the Macro Timeseries widget from Bench Macro for CPIAUCSL. Then add a note mentioning holdings and CPIAUCSL.

- Novelty: Unique create/t4 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro, portfolio; artifact widgets:Bench Macro/macro_timeseries@*,Bench Portfolio/holdings_table@*; generated:note@*:holdings,CPIAUCSL.
- Fixture backends: macro, portfolio
- Initial workspace: dashboard "Cross-Backend Task"
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 8 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "CPIAUCSL"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "holdings", "CPIAUCSL" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_create_cross_msft_exposure` — Cross-Backend Build: Msft Exposure

**L2** · widget-creation · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.400

> On the active dashboard, add these two widgets: the Latest News widget from Bench Equities for MSFT and the Sector Exposure widget from Bench Portfolio. Then add a note mentioning MSFT and sector exposure.

- Novelty: Unique create/t4 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities, portfolio; artifact widgets:Bench Equities/latest_news@*,Bench Portfolio/sector_exposure@*; generated:note@*:MSFT,sector exposure.
- Fixture backends: equities, portfolio
- Initial workspace: dashboard "Cross-Backend Task"
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 8 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "MSFT", "limit": 5} → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`
- **Generated note** ≥1× whose content mentions "MSFT", "sector exposure" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_create_cross_nvda_curve` — Cross-Backend Build: Nvda Curve

**L2** · widget-creation · workflow: equity-tearsheet · equity-research · difficulty: hard · split: test · no-op baseline score: 0.400

> Build the active dashboard with these two widgets: the Price Performance widget from Bench Equities for NVDA and the Yield Curve widget from Bench Macro. Add a note mentioning NVDA and yield curve.

- Novelty: Unique create/t4 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities, macro; artifact widgets:Bench Equities/price_performance@*,Bench Macro/yield_curve@*; generated:note@*:NVDA,yield curve.
- Fixture backends: equities, macro
- Initial workspace: dashboard "Cross-Backend Task"
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 8 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/yield_curve` → `missing_widget`
- **Generated note** ≥1× whose content mentions "NVDA", "yield curve" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_nav_hub_book_hub` — Build Out Book Hub

**L2** · workspace-navigation · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: train · no-op baseline score: 0.429

> Set the active dashboard name to Book Hub, add a new tab named Exposure, put the Sector Exposure widget on it, and add a note on the same tab mentioning exposure and book hub.

- Novelty: Unique navigate/t4 exercise using add_generative_widget, create_widget, get_widget_schema, list_available_widgets, manage_dashboard, manage_navigation_bar, navigate_workspace with checks dashboard_name, layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tab, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio; artifact widgets:Bench Portfolio/sector_exposure@exposure; tabs:exposure,overview; generated:note@exposure:exposure,book hub.
- Fixture backends: portfolio
- Initial workspace: dashboard "Starter Board"; 1 tab(s): overview
- Allowed tools (8): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Book Hub" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `exposure` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Portfolio/sector_exposure` on tab `exposure` → `missing_widget`
- **Generated note** ≥1× whose content mentions "exposure", "book hub" on tab `exposure` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_nav_hub_desk_hub` — Build Out Desk Hub

**L2** · workspace-navigation · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.429

> Set the active dashboard name to Desk Hub, add a new tab named News, put the Latest News widget for NVDA on it, and add a note on the same tab mentioning news and desk hub.

- Novelty: Unique navigate/t4 exercise using add_generative_widget, create_widget, get_widget_schema, list_available_widgets, manage_dashboard, manage_navigation_bar, navigate_workspace with checks dashboard_name, layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tab, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/latest_news@news; tabs:news,overview; generated:note@news:news,desk hub.
- Fixture backends: equities
- Initial workspace: dashboard "Starter Board"; 1 tab(s): overview
- Allowed tools (8): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Desk Hub" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `news` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "NVDA", "limit": 5} on tab `news` → `missing_widget`
- **Generated note** ≥1× whose content mentions "news", "desk hub" on tab `news` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_nav_hub_earnings_hub` — Build Out Earnings Hub

**L2** · workspace-navigation · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.429

> Rename the active dashboard to Earnings Hub, add a new tab named Estimates, put the Estimate History widget for AAPL on it, and add a note on the same tab mentioning estimates and earnings hub.

- Novelty: Unique navigate/t4 exercise using add_generative_widget, create_widget, get_widget_schema, list_available_widgets, manage_dashboard, manage_navigation_bar, navigate_workspace with checks dashboard_name, layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tab, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/estimate_history@estimates; tabs:estimates,overview; generated:note@estimates:estimates,earnings hub.
- Fixture backends: equities
- Initial workspace: dashboard "Starter Board"; 1 tab(s): overview
- Allowed tools (8): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Earnings Hub" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `estimates` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "AAPL"} on tab `estimates` → `missing_widget`
- **Generated note** ≥1× whose content mentions "estimates", "earnings hub" on tab `estimates` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_nav_hub_rates_hub` — Build Out Rates Hub

**L2** · workspace-navigation · workflow: macro-rates-review · macro · difficulty: hard · split: test · no-op baseline score: 0.429

> Rename the active dashboard to Rates Hub, add a new tab named Curve, put the Yield Curve widget on it, and add a note on the same tab mentioning curve and rates hub.

- Novelty: Unique navigate/t4 exercise using add_generative_widget, create_widget, get_widget_schema, list_available_widgets, manage_dashboard, manage_navigation_bar, navigate_workspace with checks dashboard_name, layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tab, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro; artifact widgets:Bench Macro/yield_curve@curve; tabs:curve,overview; generated:note@curve:curve,rates hub.
- Fixture backends: macro
- Initial workspace: dashboard "Starter Board"; 1 tab(s): overview
- Allowed tools (8): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Rates Hub" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `curve` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Macro/yield_curve` on tab `curve` → `missing_widget`
- **Generated note** ≥1× whose content mentions "curve", "rates hub" on tab `curve` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_params_cross_aapl_macro` — Cross-Backend Options Build: Aapl Macro

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.286

> Build a dashboard with these two widgets after using parameter options for both: Bench Equities/price_performance symbol=AAPL; Bench Macro/macro_timeseries series=DGS10. Add a note mentioning AAPL and DGS10.

- Novelty: Unique params/t4 exercise using add_generative_widget, create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities, macro; artifact widgets:Bench Equities/price_performance@*,Bench Macro/macro_timeseries@*; generated:note@*:AAPL,DGS10.
- Fixture backends: equities, macro
- Initial workspace: dashboard "Cross Options"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "AAPL", "DGS10" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "price_performance", "param_name": "symbol"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "macro_timeseries", "param_name": "series"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_params_cross_nvda_rates` — Cross-Backend Options Build: Nvda Rates

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.286

> Build a dashboard with these two widgets after using parameter options for both: Bench Equities/estimate_history symbol=NVDA; Bench Macro/macro_timeseries series=FEDFUNDS. Add a note mentioning NVDA and FEDFUNDS.

- Novelty: Unique params/t4 exercise using add_generative_widget, create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities, macro; artifact widgets:Bench Equities/estimate_history@*,Bench Macro/macro_timeseries@*; generated:note@*:NVDA,FEDFUNDS.
- Fixture backends: equities, macro
- Initial workspace: dashboard "Cross Options"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "FEDFUNDS"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "NVDA", "FEDFUNDS" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "estimate_history", "param_name": "symbol"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "macro_timeseries", "param_name": "series"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_params_cross_portfolio_sector` — Cross-Backend Options Build: Portfolio Sector

**L2** · dashboard-construction · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: train · no-op baseline score: 0.286

> Build a two-widget dashboard using parameter options for both widgets: Bench Portfolio/sector_exposure sector=Technology; Bench Macro/macro_timeseries series=CPIAUCSL. Add a note mentioning Technology and CPIAUCSL.

- Novelty: Unique params/t4 exercise using add_generative_widget, create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro, portfolio; artifact widgets:Bench Macro/macro_timeseries@*,Bench Portfolio/sector_exposure@*; generated:note@*:Technology,CPIAUCSL.
- Fixture backends: macro, portfolio
- Initial workspace: dashboard "Cross Options"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` with data_args ⊇ {"sector": "Technology"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "CPIAUCSL"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "Technology", "CPIAUCSL" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "sector_exposure", "param_name": "sector"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "macro_timeseries", "param_name": "series"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_params_cross_stark_sector` — Cross-Backend Options Build: Stark Sector

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: hard · split: test · no-op baseline score: 0.286

> Using parameter options for both widgets, build a two-widget dashboard with Bench Stark Enterprise/crypto_research_dashboard_derivatives_liquidation_heatmap sector=Consumer Staples; Bench Portfolio/risk_metrics sector=Consumer Staples. Add a note mentioning Consumer Staples and options.

- Novelty: Unique params/t4 exercise using add_generative_widget, create_widget, get_params_options, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio, stark-enterprise; artifact widgets:Bench Portfolio/risk_metrics@*,Bench Stark Enterprise/crypto_research_dashboard_derivatives_liquidation_heatmap@*; generated:note@*:Consumer Staples,options.
- Fixture backends: portfolio, stark-enterprise
- Initial workspace: dashboard "Cross Options"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/crypto_research_dashboard_derivatives_liquidation_heatmap` with data_args ⊇ {"sector": "Consumer Staples"} → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/risk_metrics` with data_args ⊇ {"sector": "Consumer Staples"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "Consumer Staples", "options" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "crypto_research_dashboard_derivatives_liquidation_heatmap", "param_name": "sector"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "risk_metrics", "param_name": "sector"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_prompts_cross_prompt_cross_aapl_rates` — Prompt Cross AAPL Rates

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.250

> Get workspace_tool_usage and workspace_session_context, create Prompt Cross AAPL Rates, build the cross-backend dashboard with Bench Equities/price_performance with data_args {"symbol": "AAPL"} and Bench Macro/macro_timeseries with data_args {"series": "DGS10"}, and add a note mentioning AAPL and DGS10 and current-dashboard.

- Novelty: Unique prompts/t4 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_prompt, list_available_widgets, manage_dashboard with checks dashboard_name, layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities, macro; artifact prompts:workspace_session_context,workspace_tool_usage; widgets:Bench Equities/price_performance@*,Bench Macro/macro_timeseries@*; generated:note@*:AAPL,DGS10.
- Fixture backends: equities, macro
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (6): `get_workspace_prompt`, `manage_dashboard`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Prompt Cross AAPL Rates" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "AAPL", "DGS10", "current-dashboard" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_tool_usage"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_session_context"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_prompts_cross_prompt_cross_book_cpi` — Prompt Cross Book CPI

**L2** · dashboard-construction · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: train · no-op baseline score: 0.250

> After fetching workspace_tool_usage and workspace_session_context, create Prompt Cross Book CPI, build the cross-backend dashboard with Bench Portfolio/sector_exposure and Bench Macro/macro_timeseries with data_args {"series": "CPIAUCSL"}, and add a note mentioning sector and CPIAUCSL and current-dashboard.

- Novelty: Unique prompts/t4 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_prompt, list_available_widgets, manage_dashboard with checks dashboard_name, layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro, portfolio; artifact prompts:workspace_session_context,workspace_tool_usage; widgets:Bench Macro/macro_timeseries@*,Bench Portfolio/sector_exposure@*; generated:note@*:sector,CPIAUCSL.
- Fixture backends: macro, portfolio
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (6): `get_workspace_prompt`, `manage_dashboard`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Prompt Cross Book CPI" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "CPIAUCSL"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "sector", "CPIAUCSL", "current-dashboard" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_tool_usage"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_session_context"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_prompts_cross_prompt_cross_nvda_holdings` — Prompt Cross NVDA Holdings

**L2** · dashboard-construction · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.250

> Fetch workspace_tool_usage and workspace_session_context, create Prompt Cross NVDA Holdings, build the cross-backend dashboard with Bench Equities/estimate_history with data_args {"symbol": "NVDA"} and Bench Portfolio/holdings_table, and add a note mentioning NVDA and holdings and current-dashboard.

- Novelty: Unique prompts/t4 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_prompt, list_available_widgets, manage_dashboard with checks dashboard_name, layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities, portfolio; artifact prompts:workspace_session_context,workspace_tool_usage; widgets:Bench Equities/estimate_history@*,Bench Portfolio/holdings_table@*; generated:note@*:NVDA,holdings.
- Fixture backends: equities, portfolio
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (6): `get_workspace_prompt`, `manage_dashboard`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Prompt Cross NVDA Holdings" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`
- **Generated note** ≥1× whose content mentions "NVDA", "holdings", "current-dashboard" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_tool_usage"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_session_context"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_prompts_cross_prompt_cross_stark_risk` — Prompt Cross Stark Risk

**L2** · dashboard-construction · workflow: portfolio-morning-review · portfolio-management · difficulty: hard · split: test · no-op baseline score: 0.250

> Get workspace_tool_usage and workspace_session_context, create Prompt Cross Stark Risk, build the cross-backend dashboard with Bench Stark Enterprise/portfolio_command_center_actions_analyst_conviction and Bench Portfolio/risk_metrics, and add a note mentioning stark and risk and current-dashboard.

- Novelty: Unique prompts/t4 exercise using add_generative_widget, create_widget, get_widget_schema, get_workspace_prompt, list_available_widgets, manage_dashboard with checks dashboard_name, layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio, stark-enterprise; artifact prompts:workspace_session_context,workspace_tool_usage; widgets:Bench Portfolio/risk_metrics@*,Bench Stark Enterprise/portfolio_command_center_actions_analyst_conviction@*; generated:note@*:stark,risk.
- Fixture backends: portfolio, stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (6): `get_workspace_prompt`, `manage_dashboard`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Prompt Cross Stark Risk" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_analyst_conviction` → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Generated note** ≥1× whose content mentions "stark", "risk", "current-dashboard" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_tool_usage"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_session_context"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_resources_full_client_360` — Index-Guided App Extension: Client 360

**L2** · dashboard-construction · workflow: client-meeting-prep · client-ir · difficulty: hard · split: train · no-op baseline score: 0.200

> After reading the app-builder index resource openbb://workspace/app-builder/index, instantiate client-360 as Client Resource Command, navigate to flows, add widget client_360_flows_pipeline_by_stage, and add a note mentioning pipeline and resource.

- Novelty: Unique resources/t4 exercise using add_generative_widget, create_widget, get_widget_schema, manage_apps, manage_backends, navigate_workspace, read_workspace_resource with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_resource_read, missing_widget, schema_not_called_before_create, too_many_invalid_calls on stark-enterprise; artifact resource:openbb://workspace/app-builder/index; apps:client-360; widgets:Bench Stark Enterprise/client_360_flows_pipeline_by_stage@flows; generated:note@flows:pipeline,resource.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (7): `read_workspace_resource`, `manage_backends`, `manage_apps`, `navigate_workspace`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Resource Command" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/client_360_flows_pipeline_by_stage` on tab `flows` → `missing_widget`
- **Generated note** ≥1× whose content mentions "pipeline", "resource" on tab `flows` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "client-360" (agent must actually retrieve the resource) → `missing_resource_read`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`

#### `gen_t4_resources_full_portfolio_command_center` — Index-Guided App Extension: Portfolio Command Center

**L2** · dashboard-construction · workflow: portfolio-morning-review · portfolio-management · difficulty: hard · split: train · no-op baseline score: 0.200

> Read the app-builder index resource at openbb://workspace/app-builder/index, instantiate portfolio-command-center as PM Resource Command, navigate to holdings, add widget portfolio_command_center_holdings_sector_exposure, and add a note mentioning sector exposure and resource.

- Novelty: Unique resources/t4 exercise using add_generative_widget, create_widget, get_widget_schema, manage_apps, manage_backends, navigate_workspace, read_workspace_resource with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_resource_read, missing_widget, schema_not_called_before_create, too_many_invalid_calls on stark-enterprise; artifact resource:openbb://workspace/app-builder/index; apps:portfolio-command-center; widgets:Bench Stark Enterprise/portfolio_command_center_holdings_sector_exposure@holdings; generated:note@holdings:sector exposure,resource.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (7): `read_workspace_resource`, `manage_backends`, `manage_apps`, `navigate_workspace`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "PM Resource Command" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_holdings_sector_exposure` on tab `holdings` → `missing_widget`
- **Generated note** ≥1× whose content mentions "sector exposure", "resource" on tab `holdings` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "portfolio-command-center" (agent must actually retrieve the resource) → `missing_resource_read`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`

#### `gen_t4_resources_full_risk_exposure_monitor` — Index-Guided App Extension: Risk & Exposure Monitor

**L2** · dashboard-construction · workflow: risk-review · risk · difficulty: hard · split: train · no-op baseline score: 0.200

> After reading the app-builder index resource openbb://workspace/app-builder/index, instantiate risk-exposure-monitor as Risk Resource Command, navigate to limits, add widget risk_exposure_monitor_limits_limit_utilization, and add a note mentioning limit utilization and resource.

- Novelty: Unique resources/t4 exercise using add_generative_widget, create_widget, get_widget_schema, manage_apps, manage_backends, navigate_workspace, read_workspace_resource with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_resource_read, missing_widget, schema_not_called_before_create, too_many_invalid_calls on stark-enterprise; artifact resource:openbb://workspace/app-builder/index; apps:risk-exposure-monitor; widgets:Bench Stark Enterprise/risk_exposure_monitor_limits_limit_utilization@limits; generated:note@limits:limit utilization,resource.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (7): `read_workspace_resource`, `manage_backends`, `manage_apps`, `navigate_workspace`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Risk Resource Command" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/risk_exposure_monitor_limits_limit_utilization` on tab `limits` → `missing_widget`
- **Generated note** ≥1× whose content mentions "limit utilization", "resource" on tab `limits` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "risk-exposure-monitor" (agent must actually retrieve the resource) → `missing_resource_read`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`

#### `gen_t4_resources_full_vendor_dataset_monitor` — Index-Guided App Extension: Vendor & Dataset Monitor

**L2** · dashboard-construction · workflow: vendor-sla-monitoring · data-platform · difficulty: hard · split: test · no-op baseline score: 0.200

> After reading the app-builder index resource openbb://workspace/app-builder/index, instantiate vendor-dataset-monitor as Vendor Resource Command, navigate to incidents, add widget vendor_dataset_monitor_incidents_incident_log, and add a note mentioning incident log and resource.

- Novelty: Unique resources/t4 exercise using add_generative_widget, create_widget, get_widget_schema, manage_apps, manage_backends, navigate_workspace, read_workspace_resource with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_resource_read, missing_widget, schema_not_called_before_create, too_many_invalid_calls on stark-enterprise; artifact resource:openbb://workspace/app-builder/index; apps:vendor-dataset-monitor; widgets:Bench Stark Enterprise/vendor_dataset_monitor_incidents_incident_log@incidents; generated:note@incidents:incident log,resource.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (7): `read_workspace_resource`, `manage_backends`, `manage_apps`, `navigate_workspace`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vendor Resource Command" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_incidents_incident_log` on tab `incidents` → `missing_widget`
- **Generated note** ≥1× whose content mentions "incident log", "resource" on tab `incidents` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "vendor-dataset-monitor" (agent must actually retrieve the resource) → `missing_resource_read`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`

### L3 — Apps, skills & delegation (40)

#### `gen_t0_app_client_360` — Instantiate Client 360

**L3** · app-instantiation · workflow: client-meeting-prep · client-ir · difficulty: easy · split: train · no-op baseline score: 0.333

> Create a new dashboard named Client Review Workspace by instantiating the Client 360 app from the Bench Stark Enterprise backend.

- Novelty: Unique apps/t0 exercise using manage_apps, manage_backends with checks dashboard_name, layout_out_of_grid, missing_tool_call, too_many_invalid_calls on stark-enterprise; artifact apps:Client 360.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `get_workspace_snapshot`, `manage_backends`, `manage_apps`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Review Workspace" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_app_execution_desk` — Instantiate Execution Desk

**L3** · app-instantiation · workflow: execution-exception-review · execution · difficulty: easy · split: train · no-op baseline score: 0.333

> From the Bench Stark Enterprise backend, instantiate the Execution Desk app as a new dashboard named AM Execution Desk.

- Novelty: Unique apps/t0 exercise using manage_apps, manage_backends with checks dashboard_name, layout_out_of_grid, missing_tool_call, too_many_invalid_calls on stark-enterprise; artifact apps:Execution Desk.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `get_workspace_snapshot`, `manage_backends`, `manage_apps`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "AM Execution Desk" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_app_risk_exposure_monitor` — Instantiate Risk & Exposure Monitor

**L3** · app-instantiation · workflow: risk-review · risk · difficulty: easy · split: train · no-op baseline score: 0.333

> Instantiate the Risk & Exposure Monitor app from the Bench Stark Enterprise backend as a new dashboard named Risk Watch.

- Novelty: Unique apps/t0 exercise using manage_apps, manage_backends with checks dashboard_name, layout_out_of_grid, missing_tool_call, too_many_invalid_calls on stark-enterprise; artifact apps:Risk & Exposure Monitor.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `get_workspace_snapshot`, `manage_backends`, `manage_apps`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Risk Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_app_vendor_dataset_monitor` — Instantiate Vendor & Dataset Monitor

**L3** · app-instantiation · workflow: vendor-sla-monitoring · data-platform · difficulty: easy · split: validation · no-op baseline score: 0.333

> From the Bench Stark Enterprise backend, instantiate the Vendor & Dataset Monitor app as a new dashboard named Data Vendor Watch.

- Novelty: Unique apps/t0 exercise using manage_apps, manage_backends with checks dashboard_name, layout_out_of_grid, missing_tool_call, too_many_invalid_calls on stark-enterprise; artifact apps:Vendor & Dataset Monitor.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `get_workspace_snapshot`, `manage_backends`, `manage_apps`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Data Vendor Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_delegate_client_single` — Delegate One Task: Client Single

**L3** · mcp-tool-use · workflow: client-meeting-prep · client-ir · difficulty: easy · split: train · no-op baseline score: 0.667

> Call assign_tasks_to_agents with one task_request using id ir-analyst for client meeting prep work: Prepare talking points and open requests for the client meeting.

- Novelty: Unique delegate/t0 exercise using assign_tasks_to_agents, get_workspace_snapshot with checks layout_out_of_grid, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:ir-analyst; widgets:Bench Stark Enterprise/strategy_health_monitor_capacity_liquidity_capacity_curve@overview.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_capacity_liquidity_capacity_curve({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_capacity_liquidity_capacity_curve` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "ir-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_delegate_earnings_single` — Delegate One Task: Earnings Single

**L3** · mcp-tool-use · workflow: earnings-prep · equity-research · difficulty: easy · split: train · no-op baseline score: 0.667

> For earnings prep work, call assign_tasks_to_agents with one task_request using id coverage-analyst: Review estimate revisions and transcript tone for earnings prep.

- Novelty: Unique delegate/t0 exercise using assign_tasks_to_agents, get_workspace_snapshot with checks layout_out_of_grid, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:coverage-analyst; widgets:Bench Stark Enterprise/strategy_health_monitor_overview_workflow_overview@overview.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_overview_workflow_overview({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_overview_workflow_overview` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "coverage-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_delegate_risk_single` — Delegate One Task: Risk Single

**L3** · mcp-tool-use · workflow: risk-review · risk · difficulty: easy · split: train · no-op baseline score: 0.667

> Call assign_tasks_to_agents with one task_request using id stress-analyst for risk review work: Run the historical stress scenarios and summarize losses.

- Novelty: Unique delegate/t0 exercise using assign_tasks_to_agents, get_workspace_snapshot with checks layout_out_of_grid, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:stress-analyst; widgets:Bench Stark Enterprise/strategy_health_monitor_performance_gross_and_net_exposure@overview.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_performance_gross_and_net_exposure({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_performance_gross_and_net_exposure` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "stress-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t0_delegate_vendor_single` — Delegate One Task: Vendor Single

**L3** · mcp-tool-use · workflow: vendor-sla-monitoring · data-platform · difficulty: easy · split: validation · no-op baseline score: 0.667

> Call assign_tasks_to_agents with one task_request using id triage-analyst for vendor sla monitoring work: Triage the open vendor incident log by severity.

- Novelty: Unique delegate/t0 exercise using assign_tasks_to_agents, get_workspace_snapshot with checks layout_out_of_grid, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:triage-analyst; widgets:Bench Stark Enterprise/strategy_health_monitor_performance_sleeve_performance@overview.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_performance_sleeve_performance({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_performance_sleeve_performance` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "triage-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_app_compliance_surveillance_hub` — Instantiate Compliance Surveillance Hub (Checked)

**L3** · app-instantiation · workflow: compliance-surveillance · compliance · difficulty: easy · split: train · no-op baseline score: 0.143

> Create a new dashboard named Daily Surveillance Board by instantiating the Compliance Surveillance Hub app from the Bench Stark Enterprise backend.

- Novelty: Unique apps/t1 exercise using manage_apps, manage_backends with checks dashboard_name, layout_out_of_grid, missing_tab, missing_widget, too_many_invalid_calls on stark-enterprise; artifact apps:Compliance Surveillance Hub; widgets:Bench Stark Enterprise/compliance_surveillance_hub_alerts_surveillance_alerts@alerts,Bench Stark Enterprise/compliance_surveillance_hub_audit_access_and_export_logs@audit; tabs:alerts,audit,overview.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (4): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Daily Surveillance Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `alerts` must exist (matched by tab id) → `missing_tab`
- **Tab** `audit` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_surveillance_alerts` on tab `alerts` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_audit_access_and_export_logs` on tab `audit` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_app_earnings_estimates_monitor` — Instantiate Earnings & Estimates Monitor (Checked)

**L3** · app-instantiation · workflow: earnings-prep · equity-research · difficulty: medium · split: train · no-op baseline score: 0.143

> Create a new dashboard named Earnings Season Monitor by instantiating the Earnings & Estimates Monitor app from the Bench Stark Enterprise backend.

- Novelty: Unique apps/t1 exercise using manage_apps, manage_backends with checks dashboard_name, layout_out_of_grid, missing_tab, missing_widget, too_many_invalid_calls on stark-enterprise; artifact apps:Earnings & Estimates Monitor; widgets:Bench Stark Enterprise/earnings_estimates_monitor_calendar_upcoming_earnings@calendar,Bench Stark Enterprise/earnings_estimates_monitor_estimates_consensus_revisions@estimates; tabs:calendar,estimates,overview.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (4): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Earnings Season Monitor" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `calendar` must exist (matched by tab id) → `missing_tab`
- **Tab** `estimates` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_calendar_upcoming_earnings` on tab `calendar` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_estimates_consensus_revisions` on tab `estimates` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_app_equity_research_workbench` — Instantiate Equity Research Workbench (Checked)

**L3** · app-instantiation · workflow: equity-tearsheet · equity-research · difficulty: easy · split: validation · no-op baseline score: 0.143

> From the Bench Stark Enterprise backend, instantiate the Equity Research Workbench app as a new dashboard named Coverage Workbench.

- Novelty: Unique apps/t1 exercise using manage_apps, manage_backends with checks dashboard_name, layout_out_of_grid, missing_tab, missing_widget, too_many_invalid_calls on stark-enterprise; artifact apps:Equity Research Workbench; widgets:Bench Stark Enterprise/equity_research_workbench_company_company_tear_sheet@company,Bench Stark Enterprise/equity_research_workbench_coverage_coverage_universe@coverage; tabs:company,coverage,overview.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (4): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Coverage Workbench" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `company` must exist (matched by tab id) → `missing_tab`
- **Tab** `coverage` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/equity_research_workbench_company_company_tear_sheet` on tab `company` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/equity_research_workbench_coverage_coverage_universe` on tab `coverage` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_app_executive_investment_dashboard` — Instantiate Executive Investment Dashboard (Checked)

**L3** · app-instantiation · workflow: portfolio-morning-review · portfolio-management · difficulty: medium · split: test · no-op baseline score: 0.143

> Instantiate the Executive Investment Dashboard app from the Bench Stark Enterprise backend as a new dashboard named Executive Morning Brief.

- Novelty: Unique apps/t1 exercise using manage_apps, manage_backends with checks dashboard_name, layout_out_of_grid, missing_tab, missing_widget, too_many_invalid_calls on stark-enterprise; artifact apps:Executive Investment Dashboard; widgets:Bench Stark Enterprise/executive_investment_dashboard_firm_overview_firm_snapshot@firm_overview,Bench Stark Enterprise/executive_investment_dashboard_issues_major_open_issues@issues; tabs:firm_overview,issues,overview.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (4): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Executive Morning Brief" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `firm_overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `issues` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/executive_investment_dashboard_firm_overview_firm_snapshot` on tab `firm_overview` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/executive_investment_dashboard_issues_major_open_issues` on tab `issues` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_delegate_client_pair` — Delegate Two Tasks: Client Pair

**L3** · mcp-tool-use · workflow: client-meeting-prep · client-ir · difficulty: medium · split: train · no-op baseline score: 0.667

> For client meeting prep work, call assign_tasks_to_agents with two task_requests using ids ir-analyst and portfolio-analyst.

- Novelty: Unique delegate/t1 exercise using assign_tasks_to_agents, get_workspace_snapshot with checks layout_out_of_grid, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:ir-analyst,portfolio-analyst; widgets:Bench Stark Enterprise/stress_liquidity_lab_scenarios_portfolio_impact@overview.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_scenarios_portfolio_impact({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_scenarios_portfolio_impact` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "ir-analyst", "portfolio-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_delegate_compliance_pair` — Delegate Two Tasks: Compliance Pair

**L3** · mcp-tool-use · workflow: compliance-surveillance · compliance · difficulty: medium · split: train · no-op baseline score: 0.667

> Call assign_tasks_to_agents with two task_requests using ids alerts-analyst and restricted-analyst for compliance surveillance work.

- Novelty: Unique delegate/t1 exercise using assign_tasks_to_agents, get_workspace_snapshot with checks layout_out_of_grid, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:alerts-analyst,restricted-analyst; widgets:Bench Stark Enterprise/stress_liquidity_lab_scenarios_position_impact_table@overview.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_scenarios_position_impact_table({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_scenarios_position_impact_table` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "alerts-analyst", "restricted-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_delegate_earnings_pair` — Delegate Two Tasks: Earnings Pair

**L3** · mcp-tool-use · workflow: earnings-prep · equity-research · difficulty: easy · split: validation · no-op baseline score: 0.667

> Use assign_tasks_to_agents with two task_requests using ids coverage-analyst and model-analyst for earnings prep work.

- Novelty: Unique delegate/t1 exercise using assign_tasks_to_agents, get_workspace_snapshot with checks layout_out_of_grid, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:coverage-analyst,model-analyst; widgets:Bench Stark Enterprise/stress_liquidity_lab_sign_off_approval_checklist@overview.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_sign_off_approval_checklist({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_sign_off_approval_checklist` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "coverage-analyst", "model-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t1_delegate_risk_pair` — Delegate Two Tasks: Risk Pair

**L3** · mcp-tool-use · workflow: risk-review · risk · difficulty: easy · split: test · no-op baseline score: 0.667

> Use assign_tasks_to_agents with two task_requests using ids stress-analyst and limits-analyst for risk review work.

- Novelty: Unique delegate/t1 exercise using assign_tasks_to_agents, get_workspace_snapshot with checks layout_out_of_grid, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:limits-analyst,stress-analyst; widgets:Bench Stark Enterprise/stress_liquidity_lab_sign_off_residual_risk_actions@overview.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_sign_off_residual_risk_actions({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_sign_off_residual_risk_actions` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "stress-analyst", "limits-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_app_note_nav_fees_close_dashboard` — Instantiate NAV, Fees & Close Dashboard And Brief

**L3** · app-instantiation · workflow: vendor-sla-monitoring · data-platform · difficulty: medium · split: train · no-op baseline score: 0.125

> From the Bench Stark Enterprise backend, instantiate the NAV, Fees & Close Dashboard app as a new dashboard named Monthly Close Control, then add a note on the Close tab mentioning close checklist and exceptions.

- Novelty: Unique apps/t2 exercise using add_generative_widget, manage_apps, manage_backends, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_tab, missing_widget, too_many_invalid_calls on stark-enterprise; artifact apps:NAV, Fees & Close Dashboard; widgets:Bench Stark Enterprise/nav_fees_close_dashboard_cash_cash_movements@cash,Bench Stark Enterprise/nav_fees_close_dashboard_close_close_exceptions@close; tabs:cash,close,overview; generated:note@close:close checklist,exceptions.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Monthly Close Control" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `cash` must exist (matched by tab id) → `missing_tab`
- **Tab** `close` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/nav_fees_close_dashboard_cash_cash_movements` on tab `cash` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/nav_fees_close_dashboard_close_close_exceptions` on tab `close` → `missing_widget`
- **Generated note** ≥1× whose content mentions "close checklist", "exceptions" on tab `close` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_app_note_quant_research_backtest_lab` — Instantiate Quant Research & Backtest Lab And Brief

**L3** · app-instantiation · workflow: risk-review · risk · difficulty: medium · split: train · no-op baseline score: 0.111

> Instantiate the Quant Research & Backtest Lab app from the Bench Stark Enterprise backend as a new dashboard named Signal Research Lab, then add a note on the Signals tab mentioning signal and decay.

- Novelty: Unique apps/t2 exercise using add_generative_widget, manage_apps, manage_backends, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_tab, missing_widget, too_many_invalid_calls on stark-enterprise; artifact apps:Quant Research & Backtest Lab; widgets:Bench Stark Enterprise/quant_research_backtest_lab_backtest_backtest_performance@backtest,Bench Stark Enterprise/quant_research_backtest_lab_optimization_efficient_frontier@optimization; tabs:backtest,optimization,overview,signals; generated:note@signals:signal,decay.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Signal Research Lab" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `backtest` must exist (matched by tab id) → `missing_tab`
- **Tab** `optimization` must exist (matched by tab id) → `missing_tab`
- **Tab** `signals` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/quant_research_backtest_lab_backtest_backtest_performance` on tab `backtest` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/quant_research_backtest_lab_optimization_efficient_frontier` on tab `optimization` → `missing_widget`
- **Generated note** ≥1× whose content mentions "signal", "decay" on tab `signals` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_app_note_reporting_factsheet_studio` — Instantiate Reporting & Factsheet Studio And Brief

**L3** · app-instantiation · workflow: client-meeting-prep · client-ir · difficulty: medium · split: validation · no-op baseline score: 0.111

> Create a new dashboard named Factsheet Control by instantiating the Reporting & Factsheet Studio app from the Bench Stark Enterprise backend, then add a note on the Factsheets tab mentioning factsheet and distribution.

- Novelty: Unique apps/t2 exercise using add_generative_widget, manage_apps, manage_backends, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_tab, missing_widget, too_many_invalid_calls on stark-enterprise; artifact apps:Reporting & Factsheet Studio; widgets:Bench Stark Enterprise/reporting_factsheet_studio_commentary_approved_commentary_library@commentary,Bench Stark Enterprise/reporting_factsheet_studio_ddqs_ddq_and_rfp_tracker@ddqs; tabs:commentary,ddqs,factsheets,overview; generated:note@factsheets:factsheet,distribution.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Factsheet Control" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `commentary` must exist (matched by tab id) → `missing_tab`
- **Tab** `ddqs` must exist (matched by tab id) → `missing_tab`
- **Tab** `factsheets` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/reporting_factsheet_studio_commentary_approved_commentary_library` on tab `commentary` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/reporting_factsheet_studio_ddqs_ddq_and_rfp_tracker` on tab `ddqs` → `missing_widget`
- **Generated note** ≥1× whose content mentions "factsheet", "distribution" on tab `factsheets` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_app_note_stress_liquidity_lab` — Instantiate Stress & Liquidity Lab And Brief

**L3** · app-instantiation · workflow: risk-review · risk · difficulty: medium · split: test · no-op baseline score: 0.111

> Create a new dashboard named Quarterly Stress Review by instantiating the Stress & Liquidity Lab app from the Bench Stark Enterprise backend, then add a note on the Sign Off tab mentioning sign off and residual risk.

- Novelty: Unique apps/t2 exercise using add_generative_widget, manage_apps, manage_backends, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_tab, missing_widget, too_many_invalid_calls on stark-enterprise; artifact apps:Stress & Liquidity Lab; widgets:Bench Stark Enterprise/stress_liquidity_lab_liquidity_days_to_liquidate@liquidity,Bench Stark Enterprise/stress_liquidity_lab_scenarios_scenario_builder_assumptions@scenarios; tabs:liquidity,overview,scenarios,sign_off; generated:note@sign_off:sign off,residual risk.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Quarterly Stress Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `liquidity` must exist (matched by tab id) → `missing_tab`
- **Tab** `scenarios` must exist (matched by tab id) → `missing_tab`
- **Tab** `sign_off` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_liquidity_days_to_liquidate` on tab `liquidity` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_scenarios_scenario_builder_assumptions` on tab `scenarios` → `missing_widget`
- **Generated note** ≥1× whose content mentions "sign off", "residual risk" on tab `sign_off` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_delegate_client_note` — Delegate And Coordinate: Client Note

**L3** · mcp-tool-use · workflow: client-meeting-prep · client-ir · difficulty: medium · split: train · no-op baseline score: 0.571

> For client meeting prep work, call assign_tasks_to_agents with two task_requests using ids ir-analyst and portfolio-analyst. Then add a coordinator note naming both workstreams on the active dashboard; omit dashboard_id when adding the note.

- Novelty: Unique delegate/t2 exercise using add_generative_widget, assign_tasks_to_agents, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:ir-analyst,portfolio-analyst; widgets:Bench Stark Enterprise/vendor_dataset_monitor_quality_row_count_drift@overview; generated:note@*:ir analyst,portfolio analyst.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_quality_row_count_drift({})
- Allowed tools (3): `get_workspace_snapshot`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_quality_row_count_drift` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "ir analyst", "portfolio analyst", "client meeting" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "ir-analyst", "portfolio-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_delegate_earnings_note` — Delegate And Coordinate: Earnings Note

**L3** · mcp-tool-use · workflow: earnings-prep · equity-research · difficulty: medium · split: train · no-op baseline score: 0.571

> Call assign_tasks_to_agents with two task_requests using ids coverage-analyst and model-analyst for earnings prep work. Then add a coordinator note naming both workstreams on the active dashboard; omit dashboard_id when adding the note.

- Novelty: Unique delegate/t2 exercise using add_generative_widget, assign_tasks_to_agents, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:coverage-analyst,model-analyst; widgets:Bench Stark Enterprise/vendor_dataset_monitor_quality_validation_errors@overview; generated:note@*:coverage analyst,model analyst.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_quality_validation_errors({})
- Allowed tools (3): `get_workspace_snapshot`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_quality_validation_errors` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "coverage analyst", "model analyst", "earnings prep" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "coverage-analyst", "model-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_delegate_ops_note` — Delegate And Coordinate: Ops Note

**L3** · mcp-tool-use · workflow: vendor-sla-monitoring · data-platform · difficulty: medium · split: validation · no-op baseline score: 0.571

> Call assign_tasks_to_agents with two task_requests using ids triage-analyst and sla-analyst for vendor sla monitoring work. Then add a coordinator note naming both workstreams on the active dashboard; omit dashboard_id when adding the note.

- Novelty: Unique delegate/t2 exercise using add_generative_widget, assign_tasks_to_agents, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:sla-analyst,triage-analyst; widgets:Bench Stark Enterprise/vendor_dataset_monitor_slas_freshness_exceptions@overview; generated:note@*:triage analyst,sla analyst.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_slas_freshness_exceptions({})
- Allowed tools (3): `get_workspace_snapshot`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_slas_freshness_exceptions` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "triage analyst", "sla analyst", "vendor" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "triage-analyst", "sla-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t2_delegate_risk_note` — Delegate And Coordinate: Risk Note

**L3** · mcp-tool-use · workflow: risk-review · risk · difficulty: medium · split: test · no-op baseline score: 0.571

> Call assign_tasks_to_agents with two task_requests using ids stress-analyst and limits-analyst for risk review work. Then add a coordinator note naming both workstreams on the active dashboard; omit dashboard_id when adding the note.

- Novelty: Unique delegate/t2 exercise using add_generative_widget, assign_tasks_to_agents, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:limits-analyst,stress-analyst; widgets:Bench Stark Enterprise/vendor_dataset_monitor_slas_latency_by_feed@overview; generated:note@*:stress analyst,limits analyst.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_slas_latency_by_feed({})
- Allowed tools (3): `get_workspace_snapshot`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_slas_latency_by_feed` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "stress analyst", "limits analyst", "risk review" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "stress-analyst", "limits-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t3_app_extend_fund_operations_control_tower` — Instantiate And Extend Fund Operations Control Tower

**L3** · app-instantiation · workflow: vendor-sla-monitoring · data-platform · difficulty: hard · split: train · no-op baseline score: 0.111

> Instantiate the Fund Operations Control Tower app from the Bench Stark Enterprise backend as a new dashboard named Ops Control Room. Then add the Break Aging widget (id fund_operations_control_tower_recons_break_aging) to the Recons tab of the new dashboard.

- Novelty: Unique apps/t3 exercise using create_widget, get_widget_schema, manage_apps, manage_backends, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_tab, missing_widget, schema_not_called_before_create, too_many_invalid_calls on stark-enterprise; artifact apps:Fund Operations Control Tower; widgets:Bench Stark Enterprise/fund_operations_control_tower_corporate_actions_corporate_action_calendar@corporate_actions,Bench Stark Enterprise/fund_operations_control_tower_pricing_stale_prices@pricing,Bench Stark Enterprise/fund_operations_control_tower_recons_break_aging@recons; tabs:corporate_actions,overview,pricing,recons.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (7): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Ops Control Room" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `corporate_actions` must exist (matched by tab id) → `missing_tab`
- **Tab** `pricing` must exist (matched by tab id) → `missing_tab`
- **Tab** `recons` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_corporate_actions_corporate_action_calendar` on tab `corporate_actions` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_pricing_stale_prices` on tab `pricing` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_recons_break_aging` on tab `recons` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`

#### `gen_t3_app_extend_portfolio_command_center` — Instantiate And Extend Portfolio Command Center

**L3** · app-instantiation · workflow: portfolio-morning-review · portfolio-management · difficulty: medium · split: train · no-op baseline score: 0.111

> Create a new dashboard named PM Command Post by instantiating the Portfolio Command Center app from the Bench Stark Enterprise backend. Then add the Sector Exposure widget (id portfolio_command_center_holdings_sector_exposure) to the Holdings tab of the new dashboard.

- Novelty: Unique apps/t3 exercise using create_widget, get_widget_schema, manage_apps, manage_backends, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_tab, missing_widget, schema_not_called_before_create, too_many_invalid_calls on stark-enterprise; artifact apps:Portfolio Command Center; widgets:Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas@actions,Bench Stark Enterprise/portfolio_command_center_attribution_brinson_attribution@attribution,Bench Stark Enterprise/portfolio_command_center_holdings_sector_exposure@holdings; tabs:actions,attribution,holdings,overview.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (7): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "PM Command Post" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `actions` must exist (matched by tab id) → `missing_tab`
- **Tab** `attribution` must exist (matched by tab id) → `missing_tab`
- **Tab** `holdings` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` on tab `actions` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_attribution_brinson_attribution` on tab `attribution` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_holdings_sector_exposure` on tab `holdings` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`

#### `gen_t3_app_extend_rebalance_scenario_lab` — Instantiate And Extend Rebalance & Scenario Lab

**L3** · app-instantiation · workflow: portfolio-morning-review · portfolio-management · difficulty: medium · split: validation · no-op baseline score: 0.125

> Create a new dashboard named Rebalance Studio by instantiating the Rebalance & Scenario Lab app from the Bench Stark Enterprise backend. Then add the Drift by Sleeve widget (id rebalance_scenario_lab_drift_drift_by_sleeve) to the Drift tab of the new dashboard.

- Novelty: Unique apps/t3 exercise using create_widget, get_widget_schema, manage_apps, manage_backends, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_tab, missing_widget, schema_not_called_before_create, too_many_invalid_calls on stark-enterprise; artifact apps:Rebalance & Scenario Lab; widgets:Bench Stark Enterprise/rebalance_scenario_lab_approval_approval_checklist@approval,Bench Stark Enterprise/rebalance_scenario_lab_drift_current_vs_target_weights@drift,Bench Stark Enterprise/rebalance_scenario_lab_drift_drift_by_sleeve@drift; tabs:approval,drift,overview.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (7): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Rebalance Studio" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `approval` must exist (matched by tab id) → `missing_tab`
- **Tab** `drift` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/rebalance_scenario_lab_approval_approval_checklist` on tab `approval` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/rebalance_scenario_lab_drift_current_vs_target_weights` on tab `drift` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/rebalance_scenario_lab_drift_drift_by_sleeve` on tab `drift` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`

#### `gen_t3_app_extend_strategy_health_monitor` — Instantiate And Extend Strategy Health Monitor

**L3** · app-instantiation · workflow: portfolio-morning-review · portfolio-management · difficulty: hard · split: test · no-op baseline score: 0.111

> Instantiate the Strategy Health Monitor app from the Bench Stark Enterprise backend as a new dashboard named Strategy Health Desk. Then add the Catalyst Calendar widget (id strategy_health_monitor_watchlist_catalyst_calendar) to the Watchlist tab of the new dashboard.

- Novelty: Unique apps/t3 exercise using create_widget, get_widget_schema, manage_apps, manage_backends, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_tab, missing_widget, schema_not_called_before_create, too_many_invalid_calls on stark-enterprise; artifact apps:Strategy Health Monitor; widgets:Bench Stark Enterprise/strategy_health_monitor_capacity_capacity_utilization@capacity,Bench Stark Enterprise/strategy_health_monitor_performance_strategy_health_metrics@performance,Bench Stark Enterprise/strategy_health_monitor_watchlist_catalyst_calendar@watchlist; tabs:capacity,overview,performance,watchlist.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (7): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Strategy Health Desk" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `capacity` must exist (matched by tab id) → `missing_tab`
- **Tab** `performance` must exist (matched by tab id) → `missing_tab`
- **Tab** `watchlist` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_capacity_capacity_utilization` on tab `capacity` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_performance_strategy_health_metrics` on tab `performance` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_watchlist_catalyst_calendar` on tab `watchlist` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`

#### `gen_t3_delegate_skill_comps_skill` — Delegate Per The Finance Comps Skill

**L3** · mcp-tool-use · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.444

> Use get_skill_content with slug finance-comps to understand the workflow. Then call assign_tasks_to_agents with two task_requests using ids peers-analyst and multiples-analyst covering that workflow, and add a coordinator note naming both workstreams. Omit dashboard_id when adding the note.

- Novelty: Unique delegate/t3 exercise using add_generative_widget, assign_tasks_to_agents, get_skill_content, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:multiples-analyst,peers-analyst; widgets:Bench Stark Enterprise/workspace_data_control_center_data_health_feed_status@overview; generated:note@*:peers analyst,multiples analyst.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_data_health_feed_status({})
- Allowed tools (4): `get_workspace_snapshot`, `get_skill_content`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_data_health_feed_status` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "peers analyst", "multiples analyst", "comps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-comps"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Comps workflow", "peer set", "valuation multiples" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `assign_tasks_to_agents` must contain "peers-analyst", "multiples-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t3_delegate_skill_earnings_skill` — Delegate Per The Finance Earnings Prep Skill

**L3** · mcp-tool-use · workflow: earnings-prep · equity-research · difficulty: medium · split: train · no-op baseline score: 0.444

> Call get_skill_content with slug finance-earnings-prep to understand the workflow. Then call assign_tasks_to_agents with two task_requests using ids coverage-analyst and model-analyst covering that workflow, and add a coordinator note naming both workstreams. Omit dashboard_id when adding the note.

- Novelty: Unique delegate/t3 exercise using add_generative_widget, assign_tasks_to_agents, get_skill_content, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:coverage-analyst,model-analyst; widgets:Bench Stark Enterprise/workspace_data_control_center_data_health_latency_and_freshness@overview; generated:note@*:coverage analyst,model analyst.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_data_health_latency_and_freshness({})
- Allowed tools (4): `get_workspace_snapshot`, `get_skill_content`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_data_health_latency_and_freshness` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "coverage analyst", "model analyst", "earnings prep" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-earnings-prep"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Earnings prep workflow", "surprise drivers", "portfolio manager" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `assign_tasks_to_agents` must contain "coverage-analyst", "model-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t3_delegate_skill_guidance_skill` — Delegate Per The Finance Guidance Tracker Skill

**L3** · mcp-tool-use · workflow: equity-tearsheet · equity-research · difficulty: hard · split: validation · no-op baseline score: 0.444

> Use get_skill_content with slug finance-guidance-tracker to understand the workflow. Then call assign_tasks_to_agents with two task_requests using ids claims-analyst and evidence-analyst covering that workflow, and add a coordinator note naming both workstreams. Omit dashboard_id when adding the note.

- Novelty: Unique delegate/t3 exercise using add_generative_widget, assign_tasks_to_agents, get_skill_content, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:claims-analyst,evidence-analyst; widgets:Bench Stark Enterprise/workspace_data_control_center_entitlements_app_and_widget_permissions@overview; generated:note@*:claims analyst,evidence analyst.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_entitlements_app_and_widget_permissions({})
- Allowed tools (4): `get_workspace_snapshot`, `get_skill_content`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_entitlements_app_and_widget_permissions` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "claims analyst", "evidence analyst", "guidance" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-guidance-tracker"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Guidance tracker workflow", "management claims", "evidence gaps" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `assign_tasks_to_agents` must contain "claims-analyst", "evidence-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t3_delegate_skill_tearsheet_skill` — Delegate Per The Finance Tearsheet Skill

**L3** · mcp-tool-use · workflow: equity-tearsheet · equity-research · difficulty: medium · split: test · no-op baseline score: 0.444

> After calling get_skill_content with slug finance-tearsheet to understand the workflow, call assign_tasks_to_agents with two task_requests using ids valuation-analyst and catalyst-analyst covering that workflow, and add a coordinator note naming both workstreams. Omit dashboard_id when adding the note.

- Novelty: Unique delegate/t3 exercise using add_generative_widget, assign_tasks_to_agents, get_skill_content, get_workspace_snapshot with checks layout_out_of_grid, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact tasks:catalyst-analyst,valuation-analyst; widgets:Bench Stark Enterprise/workspace_data_control_center_entitlements_copilot_visibility_flags@overview; generated:note@*:valuation analyst,catalyst analyst.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_entitlements_copilot_visibility_flags({})
- Allowed tools (4): `get_workspace_snapshot`, `get_skill_content`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_entitlements_copilot_visibility_flags` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "valuation analyst", "catalyst analyst", "tearsheet" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-tearsheet"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Tearsheet workflow", "valuation", "investment conclusion" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `assign_tasks_to_agents` must contain "valuation-analyst", "catalyst-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`

#### `gen_t4_app_full_corporate_access_meeting_notes` — Instantiate, Extend, And Brief Corporate Access & Meeting Notes

**L3** · app-instantiation · workflow: compliance-surveillance · compliance · difficulty: hard · split: train · no-op baseline score: 0.100

> Create a new dashboard named Corporate Access Log by instantiating the Corporate Access & Meeting Notes app from the Bench Stark Enterprise backend. Then add the Expert Calls widget (id corporate_access_meeting_notes_meetings_expert_calls) to the Meetings tab, and add a note on the same tab mentioning expert calls and meeting calendar.

- Novelty: Unique apps/t4 exercise using add_generative_widget, create_widget, get_widget_schema, manage_apps, manage_backends, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_tab, missing_widget, schema_not_called_before_create, too_many_invalid_calls on stark-enterprise; artifact apps:Corporate Access & Meeting Notes; widgets:Bench Stark Enterprise/corporate_access_meeting_notes_claims_management_claims_tracker@claims,Bench Stark Enterprise/corporate_access_meeting_notes_compliance_mnpi_attestation_status@compliance,Bench Stark Enterprise/corporate_access_meeting_notes_meetings_expert_calls@meetings; tabs:claims,compliance,meetings,overview; generated:note@meetings:expert calls,meeting calendar.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (8): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Corporate Access Log" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `claims` must exist (matched by tab id) → `missing_tab`
- **Tab** `compliance` must exist (matched by tab id) → `missing_tab`
- **Tab** `meetings` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/corporate_access_meeting_notes_claims_management_claims_tracker` on tab `claims` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/corporate_access_meeting_notes_compliance_mnpi_attestation_status` on tab `compliance` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/corporate_access_meeting_notes_meetings_expert_calls` on tab `meetings` → `missing_widget`
- **Generated note** ≥1× whose content mentions "expert calls", "meeting calendar" on tab `meetings` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`

#### `gen_t4_app_full_crypto_research_dashboard` — Instantiate, Extend, And Brief Crypto Research Dashboard

**L3** · app-instantiation · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.111

> Create a new dashboard named Digital Assets Desk by instantiating the Crypto Research Dashboard app from the Bench Stark Enterprise backend. Then add the Crypto Market Metrics widget (id crypto_research_dashboard_market_crypto_market_metrics) to the Market tab, and add a note on the same tab mentioning market metrics and token.

- Novelty: Unique apps/t4 exercise using add_generative_widget, create_widget, get_widget_schema, manage_apps, manage_backends, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_tab, missing_widget, schema_not_called_before_create, too_many_invalid_calls on stark-enterprise; artifact apps:Crypto Research Dashboard; widgets:Bench Stark Enterprise/crypto_research_dashboard_derivatives_crypto_volatility_surface@derivatives,Bench Stark Enterprise/crypto_research_dashboard_market_crypto_market_metrics@market,Bench Stark Enterprise/crypto_research_dashboard_market_crypto_market_metrics@market; tabs:derivatives,market,overview; generated:note@market:market metrics,token.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (8): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Digital Assets Desk" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `derivatives` must exist (matched by tab id) → `missing_tab`
- **Tab** `market` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/crypto_research_dashboard_derivatives_crypto_volatility_surface` on tab `derivatives` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/crypto_research_dashboard_market_crypto_market_metrics` on tab `market` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/crypto_research_dashboard_market_crypto_market_metrics` on tab `market` → `missing_widget`
- **Generated note** ≥1× whose content mentions "market metrics", "token" on tab `market` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`

#### `gen_t4_app_full_healthcare_research_dashboard` — Instantiate, Extend, And Brief Healthcare Research Dashboard

**L3** · app-instantiation · workflow: healthcare-catalyst-review · healthcare-research · difficulty: hard · split: train · no-op baseline score: 0.111

> Instantiate the Healthcare Research Dashboard app from the Bench Stark Enterprise backend as a new dashboard named Biotech Catalyst Desk. Then add the Regulatory Timeline widget (id healthcare_research_dashboard_clinical_regulatory_timeline) to the Clinical tab, and add a note on the same tab mentioning regulatory timeline and catalysts.

- Novelty: Unique apps/t4 exercise using add_generative_widget, create_widget, get_widget_schema, manage_apps, manage_backends, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_tab, missing_widget, schema_not_called_before_create, too_many_invalid_calls on stark-enterprise; artifact apps:Healthcare Research Dashboard; widgets:Bench Stark Enterprise/healthcare_research_dashboard_clinical_regulatory_timeline@clinical,Bench Stark Enterprise/healthcare_research_dashboard_clinical_trial_catalyst_calendar@clinical,Bench Stark Enterprise/healthcare_research_dashboard_commercial_drug_revenue_bridge@commercial; tabs:clinical,commercial,overview; generated:note@clinical:regulatory timeline,catalysts.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (8): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Biotech Catalyst Desk" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `clinical` must exist (matched by tab id) → `missing_tab`
- **Tab** `commercial` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/healthcare_research_dashboard_clinical_trial_catalyst_calendar` on tab `clinical` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/healthcare_research_dashboard_commercial_drug_revenue_bridge` on tab `commercial` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/healthcare_research_dashboard_clinical_regulatory_timeline` on tab `clinical` → `missing_widget`
- **Generated note** ≥1× whose content mentions "regulatory timeline", "catalysts" on tab `clinical` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`

#### `gen_t4_app_full_mnpi_research_review` — Instantiate, Extend, And Brief MNPI & Research Review

**L3** · app-instantiation · workflow: compliance-surveillance · compliance · difficulty: hard · split: test · no-op baseline score: 0.100

> From the Bench Stark Enterprise backend, instantiate the MNPI & Research Review app as a new dashboard named MNPI Control Desk. Then add the Reviewer Comments widget (id mnpi_research_review_research_reviewer_comments) to the Research tab, and add a note on the same tab mentioning reviewer comments and sign off.

- Novelty: Unique apps/t4 exercise using add_generative_widget, create_widget, get_widget_schema, manage_apps, manage_backends, navigate_workspace with checks dashboard_name, layout_out_of_grid, missing_generated_widget, missing_tab, missing_widget, schema_not_called_before_create, too_many_invalid_calls on stark-enterprise; artifact apps:MNPI & Research Review; widgets:Bench Stark Enterprise/mnpi_research_review_evidence_evidence_and_sign_off_history@evidence,Bench Stark Enterprise/mnpi_research_review_meetings_company_meeting_logs@meetings,Bench Stark Enterprise/mnpi_research_review_research_reviewer_comments@research; tabs:evidence,meetings,overview,research; generated:note@research:reviewer comments,sign off.
- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (8): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "MNPI Control Desk" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `evidence` must exist (matched by tab id) → `missing_tab`
- **Tab** `meetings` must exist (matched by tab id) → `missing_tab`
- **Tab** `research` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/mnpi_research_review_evidence_evidence_and_sign_off_history` on tab `evidence` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/mnpi_research_review_meetings_company_meeting_logs` on tab `meetings` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/mnpi_research_review_research_reviewer_comments` on tab `research` → `missing_widget`
- **Generated note** ≥1× whose content mentions "reviewer comments", "sign off" on tab `research` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`

#### `gen_t4_delegate_build_earnings_build` — Delegate And Equip: Earnings Build

**L3** · mcp-tool-use · workflow: earnings-prep · equity-research · difficulty: hard · split: train · no-op baseline score: 0.600

> Call assign_tasks_to_agents with two task_requests using ids revisions-analyst and reaction-analyst. Then add the Consensus Revisions widget (id earnings_estimates_monitor_estimates_consensus_revisions) from the Bench Stark Enterprise backend so the workstreams have their data, and add a coordinator note naming both workstreams. Omit dashboard_id when adding the note.

- Novelty: Unique delegate/t4 exercise using add_generative_widget, assign_tasks_to_agents, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, too_many_widgets, unlisted_widget_id on stark-enterprise; artifact tasks:reaction-analyst,revisions-analyst; widgets:Bench Stark Enterprise/earnings_estimates_monitor_estimates_consensus_revisions@*,Bench Stark Enterprise/workspace_data_control_center_overview_workflow_overview@overview; generated:note@*:revisions analyst,reaction analyst.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_overview_workflow_overview({})
- Allowed tools (6): `get_workspace_snapshot`, `assign_tasks_to_agents`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_estimates_consensus_revisions` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_overview_workflow_overview` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "revisions analyst", "reaction analyst", "consensus revisions" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "revisions-analyst", "reaction-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_delegate_build_exec_build` — Delegate And Equip: Exec Build

**L3** · mcp-tool-use · workflow: execution-exception-review · execution · difficulty: hard · split: train · no-op baseline score: 0.600

> Call assign_tasks_to_agents with two task_requests using ids rejects-analyst and restricted-analyst. Then add the Rejected Orders widget (id execution_desk_exceptions_rejected_orders) from the Bench Stark Enterprise backend so the workstreams have their data, and add a coordinator note naming both workstreams. Omit dashboard_id when adding the note.

- Novelty: Unique delegate/t4 exercise using add_generative_widget, assign_tasks_to_agents, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, too_many_widgets, unlisted_widget_id on stark-enterprise; artifact tasks:rejects-analyst,restricted-analyst; widgets:Bench Stark Enterprise/execution_desk_exceptions_rejected_orders@*,Bench Stark Enterprise/workspace_data_control_center_usage_app_usage@overview; generated:note@*:rejects analyst,restricted analyst.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_usage_app_usage({})
- Allowed tools (6): `get_workspace_snapshot`, `assign_tasks_to_agents`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_exceptions_rejected_orders` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_usage_app_usage` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "rejects analyst", "restricted analyst", "rejected orders" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "rejects-analyst", "restricted-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_delegate_build_risk_build` — Delegate And Equip: Risk Build

**L3** · mcp-tool-use · workflow: risk-review · risk · difficulty: hard · split: train · no-op baseline score: 0.600

> Call assign_tasks_to_agents with two task_requests using ids var-analyst and stress-analyst. Then add the VaR Trend widget (id risk_exposure_monitor_dashboard_var_trend) from the Bench Stark Enterprise backend so the workstreams have their data, and add a coordinator note naming both workstreams. Omit dashboard_id when adding the note.

- Novelty: Unique delegate/t4 exercise using add_generative_widget, assign_tasks_to_agents, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, too_many_widgets, unlisted_widget_id on stark-enterprise; artifact tasks:stress-analyst,var-analyst; widgets:Bench Stark Enterprise/risk_exposure_monitor_dashboard_var_trend@*,Bench Stark Enterprise/workspace_data_control_center_usage_export_activity@overview; generated:note@*:var analyst,stress analyst.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_usage_export_activity({})
- Allowed tools (6): `get_workspace_snapshot`, `assign_tasks_to_agents`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_var_trend` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_usage_export_activity` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "var analyst", "stress analyst", "var trend" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "var-analyst", "stress-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_delegate_build_vendor_build` — Delegate And Equip: Vendor Build

**L3** · mcp-tool-use · workflow: vendor-sla-monitoring · data-platform · difficulty: hard · split: test · no-op baseline score: 0.600

> After assigning two task_requests with ids triage-analyst and sla-analyst through assign_tasks_to_agents, add the Incident Log widget (id vendor_dataset_monitor_incidents_incident_log) from the Bench Stark Enterprise backend so the workstreams have their data, and add a coordinator note naming both workstreams. Omit dashboard_id when adding the note.

- Novelty: Unique delegate/t4 exercise using add_generative_widget, assign_tasks_to_agents, create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_tool_result, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, too_many_widgets, unlisted_widget_id on stark-enterprise; artifact tasks:sla-analyst,triage-analyst; widgets:Bench Stark Enterprise/vendor_dataset_monitor_incidents_incident_log@*,Bench Stark Enterprise/workspace_data_control_center_usage_export_review_queue@overview; generated:note@*:triage analyst,sla analyst.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_usage_export_review_queue({})
- Allowed tools (6): `get_workspace_snapshot`, `assign_tasks_to_agents`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_incidents_incident_log` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_usage_export_review_queue` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "triage analyst", "sla analyst", "incident log" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "triage-analyst", "sla-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

### L4 — Repair (32)

#### `gen_t3_delete_note_exposure_16` — Remove Duplicate Sector Exposure And Document

**L4** · workspace-repair · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: train · no-op baseline score: 0.750

> Two identical Sector Exposure widgets are on this dashboard. Remove exactly one duplicate, then add a note saying the duplicate was removed.

- Novelty: Unique delete/t3 exercise using add_generative_widget, delete_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on portfolio; artifact widgets:Bench Portfolio/sector_exposure@*; generated:note@*:duplicate,removed.
- Fixture backends: portfolio
- Initial workspace: dashboard "Duplicate Repair"; 2 seeded widget(s): sector_exposure({}), sector_exposure({})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `delete_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "duplicate", "removed" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_delete_note_history_17` — Remove Duplicate Estimate History And Document

**L4** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.750

> Two identical Estimate History widgets are on this dashboard. Remove exactly one duplicate, then add a note saying the duplicate was removed.

- Novelty: Unique delete/t3 exercise using add_generative_widget, delete_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/estimate_history@*; generated:note@*:duplicate,removed.
- Fixture backends: equities
- Initial workspace: dashboard "Duplicate Repair"; 2 seeded widget(s): estimate_history({"symbol": "AAPL"}), estimate_history({"symbol": "AAPL"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `delete_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "duplicate", "removed" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_delete_note_metrics_20` — Remove Duplicate Fundamental Metrics And Document

**L4** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: medium · split: validation · no-op baseline score: 0.750

> This dashboard has two identical Fundamental Metrics widgets. Remove exactly one duplicate, then add a note saying the duplicate was removed.

- Novelty: Unique delete/t3 exercise using add_generative_widget, delete_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/fundamental_metrics@*; generated:note@*:duplicate,removed.
- Fixture backends: equities
- Initial workspace: dashboard "Duplicate Repair"; 2 seeded widget(s): fundamental_metrics({"symbol": "NVDA"}), fundamental_metrics({"symbol": "NVDA"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `delete_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "duplicate", "removed" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_delete_note_orders_36` — Remove Duplicate Live Orders And Document

**L4** · workspace-repair · workflow: execution-exception-review · execution · difficulty: hard · split: test · no-op baseline score: 0.750

> This dashboard has two identical Live Orders widgets. Remove exactly one duplicate, then add a note saying the duplicate was removed.

- Novelty: Unique delete/t3 exercise using add_generative_widget, delete_widget, get_workspace_snapshot with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/execution_desk_blotter_live_orders@*; generated:note@*:duplicate,removed.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Duplicate Repair"; 2 seeded widget(s): execution_desk_blotter_live_orders({"status": "Open"}), execution_desk_blotter_live_orders({"status": "Open"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `delete_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` with data_args ⊇ {"status": "Open"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "duplicate", "removed" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_inspect_overlap_holdings_table_2` — Inspect And Repair Overlap Holdings Table

**L4** · workspace-repair · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: train · no-op baseline score: 0.625

> Move the overlapping sector_exposure widget to x=24, y=0, w=16, h=10 after inspecting the dashboard and finding it.

- Novelty: Unique inspect/t3 exercise using get_workspace_snapshot, read_widget, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_call, repeated_snapshots, too_many_invalid_calls on portfolio; artifact layouts::widget_001::0:0:24:10,:widget_002::24:0:16:10.
- Fixture backends: portfolio
- Initial workspace: dashboard "Inspect Overlap"; 2 seeded widget(s): holdings_table({}), sector_exposure({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `widget_001` must sit at exactly x=0, y=0, w=24, h=10 → `layout_mismatch`
- **Layout** `widget_002` must sit at exactly x=24, y=0, w=16, h=10 → `layout_mismatch`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_inspect_overlap_macro_timeseries_1` — Inspect And Repair Overlap Macro Timeseries

**L4** · workspace-repair · workflow: macro-rates-review · macro · difficulty: medium · split: train · no-op baseline score: 0.625

> Move the overlapping yield_curve widget to x=24, y=0, w=16, h=10 after inspecting the dashboard and finding it.

- Novelty: Unique inspect/t3 exercise using get_workspace_snapshot, read_widget, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_call, repeated_snapshots, too_many_invalid_calls on macro; artifact layouts::widget_001::0:0:24:10,:widget_002::24:0:16:10.
- Fixture backends: macro
- Initial workspace: dashboard "Inspect Overlap"; 2 seeded widget(s): macro_timeseries({"series": "DGS10"}), yield_curve({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `widget_001` must sit at exactly x=0, y=0, w=24, h=10 → `layout_mismatch`
- **Layout** `widget_002` must sit at exactly x=24, y=0, w=16, h=10 → `layout_mismatch`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_inspect_overlap_price_performance_0` — Inspect And Repair Overlap Price Performance

**L4** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: medium · split: validation · no-op baseline score: 0.625

> Inspect the dashboard, find the overlapping latest_news widget, and move it to x=24, y=0, w=16, h=10.

- Novelty: Unique inspect/t3 exercise using get_workspace_snapshot, read_widget, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_call, repeated_snapshots, too_many_invalid_calls on equities; artifact layouts::widget_001::0:0:24:10,:widget_002::24:0:16:10.
- Fixture backends: equities
- Initial workspace: dashboard "Inspect Overlap"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), latest_news({"symbol": "AAPL", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `widget_001` must sit at exactly x=0, y=0, w=24, h=10 → `layout_mismatch`
- **Layout** `widget_002` must sit at exactly x=24, y=0, w=16, h=10 → `layout_mismatch`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_inspect_overlap_reporting_factsheet_studio_commentary_disclosure_checklist_3` — Inspect And Repair Overlap Disclosure Checklist

**L4** · workspace-repair · workflow: client-meeting-prep · client-ir · difficulty: hard · split: test · no-op baseline score: 0.625

> Find the overlapping reporting_factsheet_studio_commentary_pm_quote_bank widget after inspecting the dashboard, and move it to x=24, y=0, w=16, h=10.

- Novelty: Unique inspect/t3 exercise using get_workspace_snapshot, read_widget, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, missing_tool_call, repeated_snapshots, too_many_invalid_calls on stark-enterprise; artifact layouts::widget_001::0:0:24:10,:widget_002::24:0:16:10.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Inspect Overlap"; 2 seeded widget(s): reporting_factsheet_studio_commentary_disclosure_checklist({}), reporting_factsheet_studio_commentary_pm_quote_bank({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `widget_001` must sit at exactly x=0, y=0, w=24, h=10 → `layout_mismatch`
- **Layout** `widget_002` must sit at exactly x=24, y=0, w=16, h=10 → `layout_mismatch`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_layout_overlap_overlap_estimates_fund_msft` — Repair Overlap: Overlap Estimates Fund Msft

**L4** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.714

> The MSFT estimates and fundamentals widgets overlap. Move the fundamentals widget to start at column 24 with its current size. Do not move the estimates widget.

- Novelty: Unique layout/t3 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on equities; artifact layouts:estimate_history:::0:0:24:12,fundamental_metrics:::24:0:16:8.
- Fixture backends: equities
- Initial workspace: dashboard "Overlap Repair"; 2 seeded widget(s): estimate_history({"symbol": "MSFT"}), fundamental_metrics({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `estimate_history` must sit at exactly x=0, y=0, w=24, h=12 → `layout_mismatch`
- **Layout** `fundamental_metrics` must sit at exactly x=24, y=0, w=16, h=8 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_layout_overlap_overlap_macro` — Repair Overlap: Overlap Macro

**L4** · workspace-repair · workflow: macro-rates-review · macro · difficulty: hard · split: train · no-op baseline score: 0.714

> The yield curve widget overlaps the 10Y series widget. Move the yield curve widget to start at column 20 with its current size. Do not move the series widget.

- Novelty: Unique layout/t3 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on macro; artifact layouts:macro_timeseries:::0:0:20:10,yield_curve:::20:0:20:10.
- Fixture backends: macro
- Initial workspace: dashboard "Overlap Repair"; 2 seeded widget(s): macro_timeseries({"series": "DGS10"}), yield_curve({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `macro_timeseries` must sit at exactly x=0, y=0, w=20, h=10 → `layout_mismatch`
- **Layout** `yield_curve` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_layout_overlap_overlap_portfolio` — Repair Overlap: Overlap Portfolio

**L4** · workspace-repair · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: validation · no-op baseline score: 0.714

> Do not move the holdings widget; resolve the overlap by moving the sector exposure widget to start at column 24 with its current size.

- Novelty: Unique layout/t3 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on portfolio; artifact layouts:holdings_table:::0:0:24:12,sector_exposure:::24:0:16:10.
- Fixture backends: portfolio
- Initial workspace: dashboard "Overlap Repair"; 2 seeded widget(s): holdings_table({}), sector_exposure({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `holdings_table` must sit at exactly x=0, y=0, w=24, h=12 → `layout_mismatch`
- **Layout** `sector_exposure` must sit at exactly x=24, y=0, w=16, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_layout_overlap_overlap_price_news_aapl` — Repair Overlap: Overlap Price News Aapl

**L4** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: medium · split: test · no-op baseline score: 0.714

> Do not move the AAPL price widget; resolve the overlap by moving the news widget to start at column 20 with its current size.

- Novelty: Unique layout/t3 exercise using get_workspace_snapshot, update_widget_layout with checks layout_mismatch, layout_out_of_grid, layout_overlap, repeated_snapshots, too_many_invalid_calls on equities; artifact layouts:latest_news:::20:0:20:10,price_performance:::0:0:20:12.
- Fixture backends: equities
- Initial workspace: dashboard "Overlap Repair"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), latest_news({"symbol": "AAPL", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `price_performance` must sit at exactly x=0, y=0, w=20, h=12 → `layout_mismatch`
- **Layout** `latest_news` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_nav_addtab_curve` — Add The Missing Curve Tab

**L4** · workspace-repair · workflow: macro-rates-review · macro · difficulty: hard · split: train · no-op baseline score: 0.750

> Keep the existing Overview tab intact while adding a tab named Curve and placing the Yield Curve widget on it.

- Novelty: Unique navigate/t3 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_navigation_bar, navigate_workspace with checks layout_out_of_grid, layout_overlap, missing_tab, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on macro; artifact widgets:Bench Macro/macro_timeseries@overview,Bench Macro/yield_curve@curve; tabs:curve,overview.
- Fixture backends: macro
- Initial workspace: dashboard "Incomplete Review"; 1 tab(s): overview; 1 seeded widget(s): macro_timeseries({"series": "DGS10"})
- Allowed tools (6): `get_workspace_snapshot`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `curve` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} on tab `overview` → `missing_widget`
- **Widget** ≥1× `Bench Macro/yield_curve` on tab `curve` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_nav_addtab_estimates_msft` — Add The Missing Estimates Tab

**L4** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.750

> This dashboard is missing its Estimates tab. Add a tab named Estimates and put the Estimate History widget for MSFT on it. Keep the existing Overview tab intact.

- Novelty: Unique navigate/t3 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_navigation_bar, navigate_workspace with checks layout_out_of_grid, layout_overlap, missing_tab, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/estimate_history@estimates,Bench Equities/price_performance@overview; tabs:estimates,overview.
- Fixture backends: equities
- Initial workspace: dashboard "Incomplete Review"; 1 tab(s): overview; 1 seeded widget(s): price_performance({"symbol": "MSFT"})
- Allowed tools (6): `get_workspace_snapshot`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `estimates` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} on tab `overview` → `missing_widget`
- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "MSFT"} on tab `estimates` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_nav_addtab_fundamentals_aapl` — Add The Missing Fundamentals Tab

**L4** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: medium · split: validation · no-op baseline score: 0.750

> Keep the existing Overview tab intact while adding a tab named Fundamentals and placing the Fundamental Metrics widget for AAPL on it.

- Novelty: Unique navigate/t3 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_navigation_bar, navigate_workspace with checks layout_out_of_grid, layout_overlap, missing_tab, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on equities; artifact widgets:Bench Equities/fundamental_metrics@fundamentals,Bench Equities/price_performance@overview; tabs:fundamentals,overview.
- Fixture backends: equities
- Initial workspace: dashboard "Incomplete Review"; 1 tab(s): overview; 1 seeded widget(s): price_performance({"symbol": "AAPL"})
- Allowed tools (6): `get_workspace_snapshot`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `fundamentals` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} on tab `overview` → `missing_widget`
- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "AAPL"} on tab `fundamentals` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_nav_addtab_risk` — Add The Missing Risk Tab

**L4** · workspace-repair · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: test · no-op baseline score: 0.750

> This dashboard is missing its Risk tab. Add a tab named Risk and put the Risk Metrics widget on it. Keep the existing Overview tab intact.

- Novelty: Unique navigate/t3 exercise using create_widget, get_widget_schema, get_workspace_snapshot, list_available_widgets, manage_navigation_bar, navigate_workspace with checks layout_out_of_grid, layout_overlap, missing_tab, missing_widget, repeated_snapshots, schema_not_called_before_create, too_many_invalid_calls, unlisted_widget_id on portfolio; artifact widgets:Bench Portfolio/holdings_table@overview,Bench Portfolio/risk_metrics@risk; tabs:overview,risk.
- Fixture backends: portfolio
- Initial workspace: dashboard "Incomplete Review"; 1 tab(s): overview; 1 seeded widget(s): holdings_table({})
- Allowed tools (6): `get_workspace_snapshot`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `risk` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Portfolio/holdings_table` on tab `overview` → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/risk_metrics` on tab `risk` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: every `create_widget` must be preceded by a successful `get_widget_schema` for that same origin/widget → `schema_not_called_before_create`
- **Trace**: schema/create calls may only use widget ids previously returned by `list_available_widgets` → `unlisted_widget_id`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_update_repair_news_msft_aapl` — Repair Latest News

**L4** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: medium · split: train · no-op baseline score: 0.571

> This AAPL desk dashboard mistakenly shows MSFT news. Repair the widget to AAPL and add a note saying what was repaired, mentioning both values.

- Novelty: Unique update/t3 exercise using add_generative_widget, get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/latest_news@*; generated:note@*:MSFT,AAPL.
- Fixture backends: equities
- Initial workspace: dashboard "Repair Task"; 1 seeded widget(s): latest_news({"symbol": "MSFT"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥0× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "MSFT", "AAPL", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_update_repair_risk_fund` — Repair Risk Snapshot

**L4** · workspace-repair · workflow: risk-review · risk · difficulty: hard · split: train · no-op baseline score: 0.571

> This Flagship Long/Short risk dashboard has its snapshot configured for Global Macro. Repair the widget to Flagship Long/Short and add a note saying what was repaired, mentioning both values.

- Novelty: Unique update/t3 exercise using add_generative_widget, get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/risk_exposure_monitor_dashboard_risk_snapshot@*; generated:note@*:Global Macro,Flagship Long/Short.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Repair Task"; 1 seeded widget(s): risk_exposure_monitor_dashboard_risk_snapshot({"fund": "Global Macro"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_risk_snapshot` with data_args ⊇ {"fund": "Flagship Long/Short"} → `missing_widget`
- **Widget** ≥0× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_risk_snapshot` with data_args ⊇ {"fund": "Global Macro"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Global Macro", "Flagship Long/Short", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_update_repair_series_fedfunds_cpi` — Repair Macro Timeseries

**L4** · workspace-repair · workflow: macro-rates-review · macro · difficulty: hard · split: validation · no-op baseline score: 0.571

> This inflation dashboard mistakenly shows the FEDFUNDS series. Repair the widget to CPIAUCSL and add a note saying what was repaired, mentioning both values.

- Novelty: Unique update/t3 exercise using add_generative_widget, get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on macro; artifact widgets:Bench Macro/macro_timeseries@*; generated:note@*:FEDFUNDS,CPIAUCSL.
- Fixture backends: macro
- Initial workspace: dashboard "Repair Task"; 1 seeded widget(s): macro_timeseries({"series": "FEDFUNDS"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "CPIAUCSL"} → `missing_widget`
- **Widget** ≥0× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "FEDFUNDS"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "FEDFUNDS", "CPIAUCSL", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t3_update_repair_ticker_nvda_msft` — Repair Price Performance

**L4** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: medium · split: test · no-op baseline score: 0.571

> This MSFT review dashboard mistakenly shows NVDA in the price widget. Repair the widget to MSFT; then add a note saying what was repaired and mentioning both values.

- Novelty: Unique update/t3 exercise using add_generative_widget, get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/price_performance@*; generated:note@*:NVDA,MSFT.
- Fixture backends: equities
- Initial workspace: dashboard "Repair Task"; 1 seeded widget(s): price_performance({"symbol": "NVDA"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Widget** ≥0× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "NVDA", "MSFT", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_delete_then_fix_news_aapl_12` — Deduplicate And Fix Latest News

**L4** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.700

> Remove exactly one duplicate from the two identical Latest News widgets for NVDA; then update the remaining widget to AAPL and add a note mentioning AAPL and the word repaired.

- Novelty: Unique delete/t4 exercise using add_generative_widget, delete_widget, get_workspace_snapshot, update_widget with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/latest_news@*; generated:note@*:AAPL,repaired.
- Fixture backends: equities
- Initial workspace: dashboard "Dedup And Fix"; 2 seeded widget(s): latest_news({"symbol": "NVDA", "limit": 5}), latest_news({"symbol": "NVDA", "limit": 5})
- Allowed tools (5): `get_workspace_snapshot`, `read_widget`, `delete_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥0× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "AAPL", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_delete_then_fix_performance_nvda_18` — Deduplicate And Fix Price Performance

**L4** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.700

> Remove exactly one duplicate from the two identical Price Performance widgets for AAPL; then update the remaining widget to NVDA and add a note mentioning NVDA and the word repaired.

- Novelty: Unique delete/t4 exercise using add_generative_widget, delete_widget, get_workspace_snapshot, update_widget with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/price_performance@*; generated:note@*:NVDA,repaired.
- Fixture backends: equities
- Initial workspace: dashboard "Dedup And Fix"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), price_performance({"symbol": "AAPL"})
- Allowed tools (5): `get_workspace_snapshot`, `read_widget`, `delete_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥0× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "NVDA", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_delete_then_fix_status_escalated_48` — Deduplicate And Fix Vendor SLA Status

**L4** · workspace-repair · workflow: vendor-sla-monitoring · data-platform · difficulty: hard · split: train · no-op baseline score: 0.700

> The dashboard contains two identical Vendor SLA Status widgets for Open, but the desk actually needs Escalated. Remove exactly one duplicate, update the remaining widget to Escalated, and add a note mentioning Escalated and the word repaired.

- Novelty: Unique delete/t4 exercise using add_generative_widget, delete_widget, get_workspace_snapshot, update_widget with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status@*; generated:note@*:Escalated,repaired.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Dedup And Fix"; 2 seeded widget(s): vendor_dataset_monitor_slas_vendor_sla_status({"status": "Open"}), vendor_dataset_monitor_slas_vendor_sla_status({"status": "Open"})
- Allowed tools (5): `get_workspace_snapshot`, `read_widget`, `delete_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"status": "Escalated"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥0× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"status": "Open"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Escalated", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_delete_then_fix_timeseries_dgs2_17` — Deduplicate And Fix Macro Timeseries

**L4** · workspace-repair · workflow: macro-rates-review · macro · difficulty: hard · split: test · no-op baseline score: 0.700

> This dashboard has two identical Macro Timeseries widgets for DGS10, and the desk actually needs DGS2. Remove exactly one duplicate, update the remaining widget to DGS2, and add a note mentioning DGS2 and the word repaired.

- Novelty: Unique delete/t4 exercise using add_generative_widget, delete_widget, get_workspace_snapshot, update_widget with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on macro; artifact widgets:Bench Macro/macro_timeseries@*; generated:note@*:DGS2,repaired.
- Fixture backends: macro
- Initial workspace: dashboard "Dedup And Fix"; 2 seeded widget(s): macro_timeseries({"series": "DGS10"}), macro_timeseries({"series": "DGS10"})
- Allowed tools (5): `get_workspace_snapshot`, `read_widget`, `delete_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS2"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥0× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "DGS2", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_inspect_repair_brief_macro_timeseries_1` — Ambient Repair And Brief Macro Timeseries

**L4** · workspace-repair · workflow: macro-rates-review · macro · difficulty: hard · split: train · no-op baseline score: 0.636

> Inspect the dashboard, find the widget with series=DGS2, repair it to DGS10, keep the companion widget, and add a note mentioning the repair.

- Novelty: Unique inspect/t4 exercise using add_generative_widget, get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on macro; artifact widgets:Bench Macro/macro_timeseries@*,Bench Macro/yield_curve@*; generated:note@*:DGS2,DGS10.
- Fixture backends: macro
- Initial workspace: dashboard "Inspect Full Repair"; 2 seeded widget(s): yield_curve({}), macro_timeseries({"series": "DGS2"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/yield_curve` → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Widget** ≥0× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS2"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "DGS2", "DGS10", "repair" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_inspect_repair_brief_price_performance_0` — Ambient Repair And Brief Price Performance

**L4** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.636

> Keep the companion widget while finding the widget with symbol=MSFT, repairing it to AAPL, and adding a note mentioning the repair after inspecting the dashboard.

- Novelty: Unique inspect/t4 exercise using add_generative_widget, get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/latest_news@*,Bench Equities/price_performance@*; generated:note@*:MSFT,AAPL.
- Fixture backends: equities
- Initial workspace: dashboard "Inspect Full Repair"; 2 seeded widget(s): latest_news({"symbol": "AAPL", "limit": 5}), price_performance({"symbol": "MSFT"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL", "limit": 5} → `missing_widget`
- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥0× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "MSFT", "AAPL", "repair" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_inspect_repair_brief_reporting_factsheet_studio_factsheets_risk_stats_3` — Ambient Repair And Brief Risk Stats

**L4** · workspace-repair · workflow: client-meeting-prep · client-ir · difficulty: hard · split: train · no-op baseline score: 0.636

> After inspecting the dashboard, find the widget with sector=Consumer Staples, repair it to Technology, keep the companion widget, and add a note mentioning the repair.

- Novelty: Unique inspect/t4 exercise using add_generative_widget, get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/reporting_factsheet_studio_factsheets_risk_stats@*,Bench Stark Enterprise/reporting_factsheet_studio_overview_workflow_overview@*; generated:note@*:Consumer Staples,Technology.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Inspect Full Repair"; 2 seeded widget(s): reporting_factsheet_studio_overview_workflow_overview({}), reporting_factsheet_studio_factsheets_risk_stats({"sector": "Consumer Staples"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/reporting_factsheet_studio_overview_workflow_overview` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/reporting_factsheet_studio_factsheets_risk_stats` with data_args ⊇ {"sector": "Technology"} → `missing_widget`
- **Widget** ≥0× `Bench Stark Enterprise/reporting_factsheet_studio_factsheets_risk_stats` with data_args ⊇ {"sector": "Consumer Staples"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Consumer Staples", "Technology", "repair" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_inspect_repair_brief_sector_exposure_2` — Ambient Repair And Brief Sector Exposure

**L4** · workspace-repair · workflow: portfolio-risk-review · portfolio-management · difficulty: hard · split: test · no-op baseline score: 0.636

> After inspecting the dashboard, find the widget with sector=Consumer Staples, repair it to Technology, keep the companion widget, and add a note mentioning the repair.

- Novelty: Unique inspect/t4 exercise using add_generative_widget, get_workspace_snapshot, read_widget, update_widget with checks layout_out_of_grid, layout_overlap, missing_generated_widget, missing_tool_call, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on portfolio; artifact widgets:Bench Portfolio/risk_metrics@*,Bench Portfolio/sector_exposure@*; generated:note@*:Consumer Staples,Technology.
- Fixture backends: portfolio
- Initial workspace: dashboard "Inspect Full Repair"; 2 seeded widget(s): risk_metrics({}), sector_exposure({"sector": "Consumer Staples"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/sector_exposure` with data_args ⊇ {"sector": "Technology"} → `missing_widget`
- **Widget** ≥0× `Bench Portfolio/sector_exposure` with data_args ⊇ {"sector": "Consumer Staples"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Consumer Staples", "Technology", "repair" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_update_double_aapl_desk` — Double Repair: Aapl Desk

**L4** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.545

> Two fixes on this AAPL desk dashboard: the price widget shows MSFT, and the news widget shows only 1 article (desk standard is 5). Repair both existing widgets and add a note mentioning AAPL and the word repaired.

- Novelty: Unique update/t4 exercise using add_generative_widget, get_workspace_snapshot, update_widget with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/latest_news@*,Bench Equities/price_performance@*; generated:note@*:AAPL,repaired.
- Fixture backends: equities
- Initial workspace: dashboard "Double Repair Task"; 2 seeded widget(s): price_performance({"symbol": "MSFT"}), latest_news({"symbol": "AAPL", "limit": 1})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥0× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL", "limit": 5} → `missing_widget`
- **Widget** ≥0× `Bench Equities/latest_news` with data_args ⊇ {"limit": 1} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "AAPL", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_update_double_nvda_switch` — Double Repair: Nvda Switch

**L4** · workspace-repair · workflow: equity-tearsheet · equity-research · difficulty: hard · split: train · no-op baseline score: 0.545

> The dashboard is meant to track NVDA, while the price widget shows AAPL and the estimates widget shows MSFT. Repair both existing widgets to NVDA and add a note mentioning NVDA and the word repaired.

- Novelty: Unique update/t4 exercise using add_generative_widget, get_workspace_snapshot, update_widget with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on equities; artifact widgets:Bench Equities/estimate_history@*,Bench Equities/price_performance@*; generated:note@*:NVDA,repaired.
- Fixture backends: equities
- Initial workspace: dashboard "Double Repair Task"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), estimate_history({"symbol": "MSFT"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Widget** ≥0× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Widget** ≥0× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "NVDA", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_update_double_rates_switch` — Double Repair: Rates Switch

**L4** · workspace-repair · workflow: macro-rates-review · macro · difficulty: hard · split: train · no-op baseline score: 0.545

> The first macro widget is DGS2 but should be DGS10, and the second is FEDFUNDS but should be CPIAUCSL. Repair both existing widgets and add a note mentioning DGS10, CPIAUCSL, and the word repaired.

- Novelty: Unique update/t4 exercise using add_generative_widget, get_workspace_snapshot, update_widget with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on macro; artifact widgets:Bench Macro/macro_timeseries@*,Bench Macro/macro_timeseries@*; generated:note@*:DGS10,CPIAUCSL.
- Fixture backends: macro
- Initial workspace: dashboard "Double Repair Task"; 2 seeded widget(s): macro_timeseries({"series": "DGS2"}), macro_timeseries({"series": "FEDFUNDS"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Widget** ≥0× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS2"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "CPIAUCSL"} → `missing_widget`
- **Widget** ≥0× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "FEDFUNDS"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "DGS10", "CPIAUCSL", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`

#### `gen_t4_update_double_stark_ops` — Double Repair: Stark Ops

**L4** · workspace-repair · workflow: vendor-sla-monitoring · data-platform · difficulty: hard · split: test · no-op baseline score: 0.545

> The ops dashboard has two wrong settings: Vendor SLA Status is Open but should be Escalated, and Portfolio Snapshot is YTD but should be MTD. Repair both existing widgets and add a note mentioning Escalated, MTD, and the word repaired.

- Novelty: Unique update/t4 exercise using add_generative_widget, get_workspace_snapshot, update_widget with checks layout_out_of_grid, missing_generated_widget, missing_widget, repeated_snapshots, too_many_invalid_calls, too_many_widgets on stark-enterprise; artifact widgets:Bench Stark Enterprise/portfolio_command_center_overview_portfolio_snapshot@*,Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status@*; generated:note@*:Escalated,MTD.
- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Double Repair Task"; 2 seeded widget(s): vendor_dataset_monitor_slas_vendor_sla_status({"vendor": "FactSet", "status": "Open"}), portfolio_command_center_overview_portfolio_snapshot({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"vendor": "FactSet", "status": "Escalated"} → `missing_widget`
- **Widget** ≥0× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"status": "Open"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_overview_portfolio_snapshot` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "MTD"} → `missing_widget`
- **Widget** ≥0× `Bench Stark Enterprise/portfolio_command_center_overview_portfolio_snapshot` with data_args ⊇ {"period": "YTD"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Escalated", "MTD", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Trace**: ≤0 invalid tool call(s) in the whole episode → `too_many_invalid_calls`
- **Trace**: ≤1 consecutive `get_workspace_snapshot` call(s) → `repeated_snapshots`


---

Total: 300 scenarios.