# WorkspaceBench Task Catalog

Auto-generated from the bundled task JSON files — regenerate with
`python scripts/generators/generate_task_catalog.py` after editing tasks.
All four deterministic simulator suites are included.

## How grading works

Every criterion below becomes one or more boolean checks in `grade_task`
(`src/workspace_bench/core/graders.py`):

- **Strict pass** requires *every* check to pass. One failed check fails the task.
- **Score** is outcome partial credit: the mean pass fraction across semantic state-check codes.
  Trace-policy checks are reported separately and join state success for strict pass/fail.
- Each failed check emits a stable **issue code** (shown per criterion below), so
  failures aggregate meaningfully across runs.
- For external agent runs, a **process failure** (non-zero exit, timeout, unparseable
  tool-call output) also fails the attempt regardless of state.
- Widget `data_args` use **nested subset matching**: extra args are fine, expected keys
  must match exactly.
- Generated-widget and tool-result content checks are **case-insensitive** and accept
  widget-name aliases ("price_performance" ≈ "price performance") and numeric
  equivalence (0.5 ≈ 50%).
- The **no-op baseline score** shown per task is the partial credit an agent gets for
  doing nothing — the gap to 1.0 is what the task actually demands. Release gates
  require the no-op to *fail* every task and the oracle trace to *pass* every one.

## Suite: smoke (80 tasks)

### add_generative_widget (4)

#### `smoke_add_generative_widget_level0`

**level0** · category: - · specification: -

> Use add_generative_widget to add a note named 'Smoke Note' with any short text.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (1): `add_generative_widget`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Smoke Note" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `smoke_add_generative_widget_level1`

**level1** · category: - · specification: -

> Use add_generative_widget to add a note named 'Smoke Note' with any short text.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Smoke Note" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `smoke_add_generative_widget_level2`

**level2** · category: - · specification: -

> Use add_generative_widget to add a note named 'Smoke Note' with any short text.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Smoke Note" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `smoke_add_generative_widget_level3`

**level3** · category: - · specification: -

> Leave a short note named 'Smoke Note' on the current dashboard.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Smoke Note" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### assign_tasks_to_agents (4)

#### `smoke_assign_tasks_to_agents_level0`

**level0** · category: - · specification: -

> Call assign_tasks_to_agents with one task request having id 'smoke-envelope' and description 'Return the Workspace smoke envelope.'

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (1): `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_assign_tasks_to_agents_level1`

**level1** · category: - · specification: -

> Call assign_tasks_to_agents with one task request having id 'smoke-envelope' and description 'Return the Workspace smoke envelope.'

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_assign_tasks_to_agents_level2`

**level2** · category: - · specification: -

> Call assign_tasks_to_agents with one task request having id 'smoke-envelope' and description 'Return the Workspace smoke envelope.'

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_assign_tasks_to_agents_level3`

**level3** · category: - · specification: -

> Delegate one follow-up job to the agent fleet asking it to return the Workspace smoke envelope.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### create_widget (4)

#### `smoke_create_widget_level0`

**level0** · category: - · specification: -

> Use create_widget to add widget_id 'compliance_surveillance_hub_alerts_alert_trend' from origin 'Bench Stark Enterprise' to the current dashboard with data_args severity 'High', status 'Open', period 'YTD'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (1): `create_widget`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_alert_trend` with data_args ⊇ {"severity": "High", "status": "Open", "period": "YTD"} → `missing_widget`

#### `smoke_create_widget_level1`

**level1** · category: - · specification: -

> Use create_widget to add widget_id 'compliance_surveillance_hub_alerts_alert_trend' from origin 'Bench Stark Enterprise' to the current dashboard with data_args severity 'High', status 'Open', period 'YTD'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_alert_trend` with data_args ⊇ {"severity": "High", "status": "Open", "period": "YTD"} → `missing_widget`

#### `smoke_create_widget_level2`

**level2** · category: - · specification: -

> Use create_widget to add widget_id 'compliance_surveillance_hub_alerts_alert_trend' from origin 'Bench Stark Enterprise' to the current dashboard with data_args severity 'High', status 'Open', period 'YTD'.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_alert_trend` with data_args ⊇ {"severity": "High", "status": "Open", "period": "YTD"} → `missing_widget`

#### `smoke_create_widget_level3`

**level3** · category: - · specification: -

> Add the Alert Trend widget from Bench Stark Enterprise to the current dashboard, set up to track open high-severity alerts year-to-date.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_alert_trend` with data_args ⊇ {"severity": "High", "status": "Open", "period": "YTD"} → `missing_widget`

### delete_widget (4)

#### `smoke_delete_widget_level0`

**level0** · category: - · specification: -

> Use delete_widget to remove the seeded widget_id 'nav_fees_close_dashboard_close_close_exceptions' from origin 'Bench Stark Enterprise'.

- Initial workspace: dashboard "Smoke delete_widget"; 1 tab(s): overview; 1 seeded widget(s): nav_fees_close_dashboard_close_close_exceptions({"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"})
- Allowed tools (1): `delete_widget`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥0× `Bench Stark Enterprise/nav_fees_close_dashboard_close_close_exceptions` → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

#### `smoke_delete_widget_level1`

**level1** · category: - · specification: -

> Use delete_widget to remove the seeded widget_id 'nav_fees_close_dashboard_close_close_exceptions' from origin 'Bench Stark Enterprise'.

- Initial workspace: dashboard "Smoke delete_widget"; 1 tab(s): overview; 1 seeded widget(s): nav_fees_close_dashboard_close_close_exceptions({"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥0× `Bench Stark Enterprise/nav_fees_close_dashboard_close_close_exceptions` → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

#### `smoke_delete_widget_level2`

**level2** · category: - · specification: -

> Use delete_widget to remove the seeded widget_id 'nav_fees_close_dashboard_close_close_exceptions' from origin 'Bench Stark Enterprise'.

- Initial workspace: dashboard "Smoke delete_widget"; 1 tab(s): overview; 1 seeded widget(s): nav_fees_close_dashboard_close_close_exceptions({"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥0× `Bench Stark Enterprise/nav_fees_close_dashboard_close_close_exceptions` → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

#### `smoke_delete_widget_level3`

**level3** · category: - · specification: -

> Clear out the only widget on the 'Smoke delete_widget' dashboard.

- Initial workspace: dashboard "Smoke delete_widget"; 1 tab(s): overview; 1 seeded widget(s): nav_fees_close_dashboard_close_close_exceptions({"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥0× `Bench Stark Enterprise/nav_fees_close_dashboard_close_close_exceptions` → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

### get_params_options (4)

#### `smoke_get_params_options_level0`

**level0** · category: - · specification: -

> Call get_params_options for param_name 'period' of widget_id 'earnings_estimates_monitor_calendar_upcoming_earnings' from origin 'Bench Stark Enterprise'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (1): `get_params_options`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_params_options_level1`

**level1** · category: - · specification: -

> Call get_params_options for param_name 'period' of widget_id 'earnings_estimates_monitor_calendar_upcoming_earnings' from origin 'Bench Stark Enterprise'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_params_options_level2`

**level2** · category: - · specification: -

> Call get_params_options for param_name 'period' of widget_id 'earnings_estimates_monitor_calendar_upcoming_earnings' from origin 'Bench Stark Enterprise'.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_params_options_level3`

**level3** · category: - · specification: -

> Find out which period choices the Upcoming Earnings widget from Bench Stark Enterprise supports.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### get_skill_content (4)

#### `smoke_get_skill_content_level0`

**level0** · category: - · specification: -

> Call get_skill_content with slug 'daloopa-tearsheet'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (1): `get_skill_content`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_skill_content_level1`

**level1** · category: - · specification: -

> Call get_skill_content with slug 'daloopa-tearsheet'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_skill_content_level2`

**level2** · category: - · specification: -

> Call get_skill_content with slug 'daloopa-tearsheet'.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_skill_content_level3`

**level3** · category: - · specification: -

> Pull up the Daloopa tearsheet workflow skill.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### get_widget_data (4)

#### `smoke_get_widget_data_level0`

**level0** · category: - · specification: -

> Call get_widget_data for origin 'Bench Stark Enterprise' and widget_id 'risk_exposure_monitor_dashboard_var_trend' with data_args portfolio 'Global Equity' and period 'YTD'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (1): `get_widget_data`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_widget_data_level1`

**level1** · category: - · specification: -

> Call get_widget_data for origin 'Bench Stark Enterprise' and widget_id 'risk_exposure_monitor_dashboard_var_trend' with data_args portfolio 'Global Equity' and period 'YTD'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_widget_data_level2`

**level2** · category: - · specification: -

> Call get_widget_data for origin 'Bench Stark Enterprise' and widget_id 'risk_exposure_monitor_dashboard_var_trend' with data_args portfolio 'Global Equity' and period 'YTD'.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_widget_data_level3`

**level3** · category: - · specification: -

> Fetch the year-to-date VaR Trend numbers for the Global Equity portfolio from Bench Stark Enterprise.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### get_widget_schema (4)

#### `smoke_get_widget_schema_level0`

**level0** · category: - · specification: -

> Call get_widget_schema for origin 'Bench Stark Enterprise' and widget_id 'portfolio_command_center_actions_trade_ideas'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (1): `get_widget_schema`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_widget_schema_level1`

**level1** · category: - · specification: -

> Call get_widget_schema for origin 'Bench Stark Enterprise' and widget_id 'portfolio_command_center_actions_trade_ideas'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_widget_schema_level2`

**level2** · category: - · specification: -

> Call get_widget_schema for origin 'Bench Stark Enterprise' and widget_id 'portfolio_command_center_actions_trade_ideas'.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_widget_schema_level3`

**level3** · category: - · specification: -

> Look up the full schema of the Trade Ideas widget offered by Bench Stark Enterprise.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### get_workspace_prompt (4)

#### `smoke_get_workspace_prompt_level0`

**level0** · category: - · specification: -

> Call get_workspace_prompt with name 'workspace_tool_usage'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (1): `get_workspace_prompt`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_workspace_prompt_level1`

**level1** · category: - · specification: -

> Call get_workspace_prompt with name 'workspace_tool_usage'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_workspace_prompt_level2`

**level2** · category: - · specification: -

> Call get_workspace_prompt with name 'workspace_tool_usage'.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_workspace_prompt_level3`

**level3** · category: - · specification: -

> Fetch the workspace guidance prompt about disciplined tool usage.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### get_workspace_snapshot (4)

#### `smoke_get_workspace_snapshot_level0`

**level0** · category: - · specification: -

> Call get_workspace_snapshot once.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (1): `get_workspace_snapshot`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_workspace_snapshot_level1`

**level1** · category: - · specification: -

> Call get_workspace_snapshot once.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_workspace_snapshot_level2`

**level2** · category: - · specification: -

> Call get_workspace_snapshot once.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_get_workspace_snapshot_level3`

**level3** · category: - · specification: -

> Get a complete picture of what is currently in this workspace.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### list_available_widgets (4)

#### `smoke_list_available_widgets_level0`

**level0** · category: - · specification: -

> Call list_available_widgets for origin 'Getting Started'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`, `getting-started`
- Allowed tools (1): `list_available_widgets`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_list_available_widgets_level1`

**level1** · category: - · specification: -

> Call list_available_widgets for origin 'Getting Started'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`, `getting-started`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_list_available_widgets_level2`

**level2** · category: - · specification: -

> Call list_available_widgets for origin 'Getting Started'.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`, `getting-started`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_list_available_widgets_level3`

**level3** · category: - · specification: -

> See which widgets the Getting Started backend offers.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`, `getting-started`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### manage_apps (4)

#### `smoke_manage_apps_level0`

**level0** · category: - · specification: -

> Use manage_apps operation='instantiate' with backend_id 'backend_001', template_id 'portfolio-command-center', dashboard_name 'Smoke Instantiated App', and activate true.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (1): `manage_apps`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Smoke Instantiated App" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`

#### `smoke_manage_apps_level1`

**level1** · category: - · specification: -

> Use manage_apps operation='instantiate' with backend_id 'backend_001', template_id 'portfolio-command-center', dashboard_name 'Smoke Instantiated App', and activate true.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Smoke Instantiated App" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`

#### `smoke_manage_apps_level2`

**level2** · category: - · specification: -

> Use manage_apps operation='instantiate' with backend_id 'backend_001', template_id 'portfolio-command-center', dashboard_name 'Smoke Instantiated App', and activate true.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Smoke Instantiated App" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`

#### `smoke_manage_apps_level3`

**level3** · category: - · specification: -

> Open a fresh copy of the Portfolio Command Center app as a new dashboard named 'Smoke Instantiated App' and switch to it.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Smoke Instantiated App" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`

### manage_backends (4)

#### `smoke_manage_backends_level0`

**level0** · category: - · specification: -

> Call manage_backends operation='list' once.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (1): `manage_backends`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_manage_backends_level1`

**level1** · category: - · specification: -

> Call manage_backends operation='list' once.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_manage_backends_level2`

**level2** · category: - · specification: -

> Call manage_backends operation='list' once.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_manage_backends_level3`

**level3** · category: - · specification: -

> Check which data backends this workspace is connected to.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### manage_dashboard (4)

#### `smoke_manage_dashboard_level0`

**level0** · category: - · specification: -

> Use manage_dashboard operation='update' with dashboard_id 'dash_001' to rename the current dashboard to 'Smoke Renamed Dashboard'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (1): `manage_dashboard`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Smoke Renamed Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`

#### `smoke_manage_dashboard_level1`

**level1** · category: - · specification: -

> Use manage_dashboard operation='update' with dashboard_id 'dash_001' to rename the current dashboard to 'Smoke Renamed Dashboard'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Smoke Renamed Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`

#### `smoke_manage_dashboard_level2`

**level2** · category: - · specification: -

> Use manage_dashboard operation='update' with dashboard_id 'dash_001' to rename the current dashboard to 'Smoke Renamed Dashboard'.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Smoke Renamed Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`

#### `smoke_manage_dashboard_level3`

**level3** · category: - · specification: -

> Rename the dashboard you are currently working in to 'Smoke Renamed Dashboard'.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Smoke Renamed Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`

### manage_navigation_bar (4)

#### `smoke_manage_navigation_bar_level0`

**level0** · category: - · specification: -

> Use manage_navigation_bar operation='create' on the current dashboard with tabs named 'Overview' and 'Details'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (1): `manage_navigation_bar`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `details` must exist (matched by tab id) → `missing_tab`

#### `smoke_manage_navigation_bar_level1`

**level1** · category: - · specification: -

> Use manage_navigation_bar operation='create' on the current dashboard with tabs named 'Overview' and 'Details'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `details` must exist (matched by tab id) → `missing_tab`

#### `smoke_manage_navigation_bar_level2`

**level2** · category: - · specification: -

> Use manage_navigation_bar operation='create' on the current dashboard with tabs named 'Overview' and 'Details'.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `details` must exist (matched by tab id) → `missing_tab`

#### `smoke_manage_navigation_bar_level3`

**level3** · category: - · specification: -

> Organize the current dashboard into two tabs called 'Overview' and 'Details'.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `details` must exist (matched by tab id) → `missing_tab`

### navigate_workspace (4)

#### `smoke_navigate_workspace_level0`

**level0** · category: - · specification: -

> Use navigate_workspace operation='tab' to switch to tab_id 'details'.

- Initial workspace: dashboard "Smoke navigate_workspace"; 2 tab(s): overview, details
- Allowed tools (1): `navigate_workspace`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_navigate_workspace_level1`

**level1** · category: - · specification: -

> Use navigate_workspace operation='tab' to switch to tab_id 'details'.

- Initial workspace: dashboard "Smoke navigate_workspace"; 2 tab(s): overview, details
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_navigate_workspace_level2`

**level2** · category: - · specification: -

> Use navigate_workspace operation='tab' to switch to tab_id 'details'.

- Initial workspace: dashboard "Smoke navigate_workspace"; 2 tab(s): overview, details
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_navigate_workspace_level3`

**level3** · category: - · specification: -

> Switch over to the Details tab of the current dashboard.

- Initial workspace: dashboard "Smoke navigate_workspace"; 2 tab(s): overview, details
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### read_widget (4)

#### `smoke_read_widget_level0`

**level0** · category: - · specification: -

> Call read_widget for the seeded widget_id 'client_360_client_book_client_accounts' from origin 'Bench Stark Enterprise'.

- Initial workspace: dashboard "Smoke read_widget"; 1 tab(s): overview; 1 seeded widget(s): client_360_client_book_client_accounts({"client": "Atlas Pension", "region": "Americas", "period": "YTD"})
- Allowed tools (1): `read_widget`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_read_widget_level1`

**level1** · category: - · specification: -

> Call read_widget for the seeded widget_id 'client_360_client_book_client_accounts' from origin 'Bench Stark Enterprise'.

- Initial workspace: dashboard "Smoke read_widget"; 1 tab(s): overview; 1 seeded widget(s): client_360_client_book_client_accounts({"client": "Atlas Pension", "region": "Americas", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_read_widget_level2`

**level2** · category: - · specification: -

> Call read_widget for the seeded widget_id 'client_360_client_book_client_accounts' from origin 'Bench Stark Enterprise'.

- Initial workspace: dashboard "Smoke read_widget"; 1 tab(s): overview; 1 seeded widget(s): client_360_client_book_client_accounts({"client": "Atlas Pension", "region": "Americas", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_read_widget_level3`

**level3** · category: - · specification: -

> Read the configuration of the only widget on the 'Smoke read_widget' dashboard.

- Initial workspace: dashboard "Smoke read_widget"; 1 tab(s): overview; 1 seeded widget(s): client_360_client_book_client_accounts({"client": "Atlas Pension", "region": "Americas", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### read_workspace_resource (4)

#### `smoke_read_workspace_resource_level0`

**level0** · category: - · specification: -

> Call read_workspace_resource with uri 'openbb://workspace/specs/widget-types'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (1): `read_workspace_resource`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_read_workspace_resource_level1`

**level1** · category: - · specification: -

> Call read_workspace_resource with uri 'openbb://workspace/specs/widget-types'.

- Initial workspace: bare workspace; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_read_workspace_resource_level2`

**level2** · category: - · specification: -

> Call read_workspace_resource with uri 'openbb://workspace/specs/widget-types'.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_read_workspace_resource_level3`

**level3** · category: - · specification: -

> Open the workspace documentation resource that lists the supported widget types.

- Initial workspace: baseline `stark-onboard-a`; backends `stark-enterprise-x`
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### update_widget (4)

#### `smoke_update_widget_level0`

**level0** · category: - · specification: -

> Use update_widget on the seeded widget_id 'strategy_health_monitor_capacity_capacity_utilization' from origin 'Bench Stark Enterprise' to set data_args period to 'MTD'.

- Initial workspace: dashboard "Smoke update_widget"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_capacity_capacity_utilization({"strategy": "Global Equities", "period": "YTD"})
- Allowed tools (1): `update_widget`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_capacity_capacity_utilization` with data_args ⊇ {"period": "MTD"} → `missing_widget`

#### `smoke_update_widget_level1`

**level1** · category: - · specification: -

> Use update_widget on the seeded widget_id 'strategy_health_monitor_capacity_capacity_utilization' from origin 'Bench Stark Enterprise' to set data_args period to 'MTD'.

- Initial workspace: dashboard "Smoke update_widget"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_capacity_capacity_utilization({"strategy": "Global Equities", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_capacity_capacity_utilization` with data_args ⊇ {"period": "MTD"} → `missing_widget`

#### `smoke_update_widget_level2`

**level2** · category: - · specification: -

> Use update_widget on the seeded widget_id 'strategy_health_monitor_capacity_capacity_utilization' from origin 'Bench Stark Enterprise' to set data_args period to 'MTD'.

- Initial workspace: dashboard "Smoke update_widget"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_capacity_capacity_utilization({"strategy": "Global Equities", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_capacity_capacity_utilization` with data_args ⊇ {"period": "MTD"} → `missing_widget`

#### `smoke_update_widget_level3`

**level3** · category: - · specification: -

> On the 'Smoke update_widget' dashboard, switch the Capacity Utilization widget to show the month-to-date view.

- Initial workspace: dashboard "Smoke update_widget"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_capacity_capacity_utilization({"strategy": "Global Equities", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_capacity_capacity_utilization` with data_args ⊇ {"period": "MTD"} → `missing_widget`

### update_widget_layout (4)

#### `smoke_update_widget_layout_level0`

**level0** · category: - · specification: -

> Use update_widget_layout on the seeded widget_id 'vendor_dataset_monitor_incidents_incident_log' from origin 'Bench Stark Enterprise' to place it at x 0, y 0, w 20, h 10 on tab_id 'overview'.

- Initial workspace: dashboard "Smoke update_widget_layout"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_incidents_incident_log({"vendor": "FactSet", "status": "Open", "period": "YTD"})
- Allowed tools (1): `update_widget_layout`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `vendor_dataset_monitor_incidents_incident_log` must sit at exactly x=0, y=0, w=20, h=10 on tab `overview` → `layout_mismatch`

#### `smoke_update_widget_layout_level1`

**level1** · category: - · specification: -

> Use update_widget_layout on the seeded widget_id 'vendor_dataset_monitor_incidents_incident_log' from origin 'Bench Stark Enterprise' to place it at x 0, y 0, w 20, h 10 on tab_id 'overview'.

- Initial workspace: dashboard "Smoke update_widget_layout"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_incidents_incident_log({"vendor": "FactSet", "status": "Open", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `vendor_dataset_monitor_incidents_incident_log` must sit at exactly x=0, y=0, w=20, h=10 on tab `overview` → `layout_mismatch`

#### `smoke_update_widget_layout_level2`

**level2** · category: - · specification: -

> Use update_widget_layout on the seeded widget_id 'vendor_dataset_monitor_incidents_incident_log' from origin 'Bench Stark Enterprise' to place it at x 0, y 0, w 20, h 10 on tab_id 'overview'.

- Initial workspace: dashboard "Smoke update_widget_layout"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_incidents_incident_log({"vendor": "FactSet", "status": "Open", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `vendor_dataset_monitor_incidents_incident_log` must sit at exactly x=0, y=0, w=20, h=10 on tab `overview` → `layout_mismatch`

#### `smoke_update_widget_layout_level3`

**level3** · category: - · specification: -

> On the 'Smoke update_widget_layout' dashboard, resize the Incident Log widget to half width (20 columns) and 10 rows at the top-left of its tab.

- Initial workspace: dashboard "Smoke update_widget_layout"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_incidents_incident_log({"vendor": "FactSet", "status": "Open", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `vendor_dataset_monitor_incidents_incident_log` must sit at exactly x=0, y=0, w=20, h=10 on tab `overview` → `layout_mismatch`


## Suite: enterprise-apps-default (138 tasks)

### cio_investment_committee_pack (6)

#### `cio_investment_committee_pack_p1_x`

**medium** · category: read · specification: -

> Create the investment committee packet summary with decisions required, allocation changes, capacity, research, and follow-ups.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "CIO / Investment Committee Pack"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 8 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `cio_investment_committee_pack_p1_y`

**medium** · category: read · specification: -

> Create the investment committee packet summary with decisions required, allocation changes, capacity, research, and follow-ups.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "CIO / Investment Committee Pack"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 8 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `cio_investment_committee_pack_p2_x`

**medium** · category: read · specification: -

> Identify recommendations where risk, liquidity, or research evidence conflicts with the proposed allocation.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "CIO / Investment Committee Pack"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `cio_investment_committee_pack_p2_y`

**medium** · category: read · specification: -

> Identify recommendations where risk, liquidity, or research evidence conflicts with the proposed allocation.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "CIO / Investment Committee Pack"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `cio_investment_committee_pack_p3_x`

**medium** · category: read · specification: -

> Draft the decision log update after committee review.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "CIO / Investment Committee Pack"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `cio_investment_committee_pack_p3_y`

**medium** · category: read · specification: -

> Draft the decision log update after committee review.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "CIO / Investment Committee Pack"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### client_360 (6)

#### `client_360_p1_x`

**medium** · category: read · specification: -

> Prepare an investor meeting brief with mandate context, performance, exposure, flows, requests, and approved talking points.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Client 360"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `client_360_p1_y`

**medium** · category: read · specification: -

> Prepare an investor meeting brief with mandate context, performance, exposure, flows, requests, and approved talking points.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Client 360"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `client_360_p2_x`

**medium** · category: read · specification: -

> Identify client accounts with redemption risk or unresolved service issues.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Client 360"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `client_360_p2_y`

**medium** · category: read · specification: -

> Identify client accounts with redemption risk or unresolved service issues.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Client 360"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `client_360_p3_x`

**medium** · category: read · specification: -

> Draft a concise response to the client using only approved commentary and current portfolio context.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Client 360"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `client_360_p3_y`

**medium** · category: read · specification: -

> Draft a concise response to the client using only approved commentary and current portfolio context.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Client 360"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### compliance_surveillance_hub (6)

#### `compliance_surveillance_hub_p1_x`

**medium** · category: read · specification: -

> Triage open surveillance alerts by severity, age, restricted-list overlap, and audit evidence.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Compliance Surveillance Hub"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `compliance_surveillance_hub_p1_y`

**medium** · category: read · specification: -

> Triage open surveillance alerts by severity, age, restricted-list overlap, and audit evidence.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Compliance Surveillance Hub"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `compliance_surveillance_hub_p2_x`

**medium** · category: read · specification: -

> Identify employee trades or research activity that should be escalated to compliance leadership.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Compliance Surveillance Hub"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `compliance_surveillance_hub_p2_y`

**medium** · category: read · specification: -

> Identify employee trades or research activity that should be escalated to compliance leadership.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Compliance Surveillance Hub"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `compliance_surveillance_hub_p3_x`

**medium** · category: read · specification: -

> Draft the investigation summary with evidence, next owner, and remediation status.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Compliance Surveillance Hub"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `compliance_surveillance_hub_p3_y`

**medium** · category: read · specification: -

> Draft the investigation summary with evidence, next owner, and remediation status.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Compliance Surveillance Hub"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### corporate_access_meeting_notes (6)

#### `corporate_access_meeting_notes_p1_x`

**medium** · category: read · specification: -

> Create a pre-meeting brief with prior claims, open follow-ups, expert-call context, and MNPI controls.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Corporate Access & Meeting Notes"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `corporate_access_meeting_notes_p1_y`

**medium** · category: read · specification: -

> Create a pre-meeting brief with prior claims, open follow-ups, expert-call context, and MNPI controls.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Corporate Access & Meeting Notes"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `corporate_access_meeting_notes_p2_x`

**medium** · category: read · specification: -

> Flag meetings or notes that require compliance review before research can be distributed.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Corporate Access & Meeting Notes"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `corporate_access_meeting_notes_p2_y`

**medium** · category: read · specification: -

> Flag meetings or notes that require compliance review before research can be distributed.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Corporate Access & Meeting Notes"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `corporate_access_meeting_notes_p3_x`

**medium** · category: read · specification: -

> Summarize management claims that changed the investment thesis and list the evidence still required.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Corporate Access & Meeting Notes"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `corporate_access_meeting_notes_p3_y`

**medium** · category: read · specification: -

> Summarize management claims that changed the investment thesis and list the evidence still required.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Corporate Access & Meeting Notes"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### crypto_research_dashboard (6)

#### `crypto_research_dashboard_p1_x`

**medium** · category: read · specification: -

> Summarize crypto market structure: price action, liquidity, on-chain activity, funding, basis, and liquidation risk.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Crypto Research Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `crypto_research_dashboard_p1_y`

**medium** · category: read · specification: -

> Summarize crypto market structure: price action, liquidity, on-chain activity, funding, basis, and liquidation risk.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Crypto Research Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `crypto_research_dashboard_p2_x`

**medium** · category: read · specification: -

> Identify assets where derivatives positioning conflicts with on-chain flow or spot market behavior.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Crypto Research Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `crypto_research_dashboard_p2_y`

**medium** · category: read · specification: -

> Identify assets where derivatives positioning conflicts with on-chain flow or spot market behavior.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Crypto Research Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `crypto_research_dashboard_p3_x`

**medium** · category: read · specification: -

> Draft the token thesis update using market, on-chain, derivatives, and research-document context.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Crypto Research Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `crypto_research_dashboard_p3_y`

**medium** · category: read · specification: -

> Draft the token thesis update using market, on-chain, derivatives, and research-document context.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Crypto Research Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### earnings_estimates_monitor (6)

#### `earnings_estimates_monitor_p1_x`

**medium** · category: read · specification: -

> Prepare the earnings preview: internal versus street estimates, expected surprise drivers, and trade setup.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Earnings & Estimates Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_estimates_monitor_p1_y`

**medium** · category: read · specification: -

> Prepare the earnings preview: internal versus street estimates, expected surprise drivers, and trade setup.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Earnings & Estimates Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_estimates_monitor_p2_x`

**medium** · category: read · specification: -

> Summarize post-earnings action items from price reaction, transcript tone, rating changes, and checklist status.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Earnings & Estimates Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_estimates_monitor_p2_y`

**medium** · category: read · specification: -

> Summarize post-earnings action items from price reaction, transcript tone, rating changes, and checklist status.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Earnings & Estimates Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_estimates_monitor_p3_x`

**medium** · category: read · specification: -

> Identify companies where estimate revisions and management commentary create a material thesis change.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Earnings & Estimates Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_estimates_monitor_p3_y`

**medium** · category: read · specification: -

> Identify companies where estimate revisions and management commentary create a material thesis change.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Earnings & Estimates Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### equity_research_workbench (6)

#### `equity_research_workbench_p1_x`

**medium** · category: read · specification: -

> Summarize what changed in coverage, estimates, valuation, ownership, and thesis since the last review.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Equity Research Workbench"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `equity_research_workbench_p1_y`

**medium** · category: read · specification: -

> Summarize what changed in coverage, estimates, valuation, ownership, and thesis since the last review.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Equity Research Workbench"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `equity_research_workbench_p2_x`

**medium** · category: read · specification: -

> Compare internal target price, street range, upside, and valuation sensitivity for the selected ticker.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Equity Research Workbench"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `equity_research_workbench_p2_y`

**medium** · category: read · specification: -

> Compare internal target price, street range, upside, and valuation sensitivity for the selected ticker.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Equity Research Workbench"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `equity_research_workbench_p3_x`

**medium** · category: read · specification: -

> Draft the analyst call prep note with catalysts, risks, research approvals, and open evidence gaps.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Equity Research Workbench"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `equity_research_workbench_p3_y`

**medium** · category: read · specification: -

> Draft the analyst call prep note with catalysts, risks, research approvals, and open evidence gaps.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Equity Research Workbench"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### execution_desk (6)

#### `execution_desk_p1_x`

**medium** · category: read · specification: -

> Prioritize the live blotter by liquidity, rejection risk, restricted-list status, and expected slippage.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Execution Desk"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `execution_desk_p1_y`

**medium** · category: read · specification: -

> Prioritize the live blotter by liquidity, rejection risk, restricted-list status, and expected slippage.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Execution Desk"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `execution_desk_p2_x`

**medium** · category: read · specification: -

> Explain which fills underperformed arrival price and whether broker, venue, or algo choice drove the outcome.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Execution Desk"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `execution_desk_p2_y`

**medium** · category: read · specification: -

> Explain which fills underperformed arrival price and whether broker, venue, or algo choice drove the outcome.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Execution Desk"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `execution_desk_p3_x`

**medium** · category: read · specification: -

> Draft an end-of-day execution exception report for the PM and COO.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Execution Desk"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `execution_desk_p3_y`

**medium** · category: read · specification: -

> Draft an end-of-day execution exception report for the PM and COO.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Execution Desk"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### executive_investment_dashboard (6)

#### `executive_investment_dashboard_p1_x`

**medium** · category: read · specification: -

> Write the executive briefing: firm AUM, flows, strategy returns, drawdown, stress risk, and major open issues.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Executive Investment Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `executive_investment_dashboard_p1_y`

**medium** · category: read · specification: -

> Write the executive briefing: firm AUM, flows, strategy returns, drawdown, stress risk, and major open issues.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Executive Investment Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `executive_investment_dashboard_p2_x`

**medium** · category: read · specification: -

> Identify which issues require CEO, CIO, COO, or CRO attention this week.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Executive Investment Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `executive_investment_dashboard_p2_y`

**medium** · category: read · specification: -

> Identify which issues require CEO, CIO, COO, or CRO attention this week.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Executive Investment Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `executive_investment_dashboard_p3_x`

**medium** · category: read · specification: -

> Explain whether performance, flows, and risk are moving consistently across strategies.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Executive Investment Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `executive_investment_dashboard_p3_y`

**medium** · category: read · specification: -

> Explain whether performance, flows, and risk are moving consistently across strategies.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Executive Investment Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### fund_operations_control_tower (6)

#### `fund_operations_control_tower_p1_x`

**medium** · category: read · specification: -

> Create the operations morning checklist: failed trades, recon breaks, corporate actions, pricing exceptions, and owners.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Fund Operations Control Tower"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `fund_operations_control_tower_p1_y`

**medium** · category: read · specification: -

> Create the operations morning checklist: failed trades, recon breaks, corporate actions, pricing exceptions, and owners.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Fund Operations Control Tower"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `fund_operations_control_tower_p2_x`

**medium** · category: read · specification: -

> Prioritize breaks by age, dollar impact, settlement risk, and downstream NAV impact.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Fund Operations Control Tower"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `fund_operations_control_tower_p2_y`

**medium** · category: read · specification: -

> Prioritize breaks by age, dollar impact, settlement risk, and downstream NAV impact.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Fund Operations Control Tower"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `fund_operations_control_tower_p3_x`

**medium** · category: read · specification: -

> Explain which operational issues need escalation before market open or NAV strike.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Fund Operations Control Tower"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 9 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `fund_operations_control_tower_p3_y`

**medium** · category: read · specification: -

> Explain which operational issues need escalation before market open or NAV strike.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Fund Operations Control Tower"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 9 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### healthcare_research_dashboard (6)

#### `healthcare_research_dashboard_p1_x`

**medium** · category: read · specification: -

> Prepare the healthcare analyst brief: coverage, clinical catalysts, probability funnel, TAM, prescriptions, and research documents.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Healthcare Research Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `healthcare_research_dashboard_p1_y`

**medium** · category: read · specification: -

> Prepare the healthcare analyst brief: coverage, clinical catalysts, probability funnel, TAM, prescriptions, and research documents.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Healthcare Research Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `healthcare_research_dashboard_p2_x`

**medium** · category: read · specification: -

> Identify names where clinical probability and commercial revenue scenarios imply a thesis change.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Healthcare Research Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `healthcare_research_dashboard_p2_y`

**medium** · category: read · specification: -

> Identify names where clinical probability and commercial revenue scenarios imply a thesis change.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Healthcare Research Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `healthcare_research_dashboard_p3_x`

**medium** · category: read · specification: -

> Draft the KOL follow-up plan with open questions and evidence needed for the investment committee.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Healthcare Research Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 8 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `healthcare_research_dashboard_p3_y`

**medium** · category: read · specification: -

> Draft the KOL follow-up plan with open questions and evidence needed for the investment committee.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Healthcare Research Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 8 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### liquidity_tca_workbench (6)

#### `liquidity_tca_workbench_p1_x`

**medium** · category: read · specification: -

> Recommend execution tactics by order size, volume profile, venue flow, and expected implementation shortfall.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Liquidity & TCA Workbench"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `liquidity_tca_workbench_p1_y`

**medium** · category: read · specification: -

> Recommend execution tactics by order size, volume profile, venue flow, and expected implementation shortfall.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Liquidity & TCA Workbench"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `liquidity_tca_workbench_p2_x`

**medium** · category: read · specification: -

> Rank brokers by fill quality, commission, latency, and slippage for the selected desk.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Liquidity & TCA Workbench"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `liquidity_tca_workbench_p2_y`

**medium** · category: read · specification: -

> Rank brokers by fill quality, commission, latency, and slippage for the selected desk.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Liquidity & TCA Workbench"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `liquidity_tca_workbench_p3_x`

**medium** · category: read · specification: -

> Summarize post-trade review items that require broker follow-up or algo parameter changes.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Liquidity & TCA Workbench"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `liquidity_tca_workbench_p3_y`

**medium** · category: read · specification: -

> Summarize post-trade review items that require broker follow-up or algo parameter changes.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Liquidity & TCA Workbench"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### mnpi_research_review (6)

#### `mnpi_research_review_p1_x`

**medium** · category: read · specification: -

> Review the MNPI case file: wall crossings, meetings, research drafts, target changes, and sign-off history.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "MNPI & Research Review"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `mnpi_research_review_p1_y`

**medium** · category: read · specification: -

> Review the MNPI case file: wall crossings, meetings, research drafts, target changes, and sign-off history.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "MNPI & Research Review"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `mnpi_research_review_p2_x`

**medium** · category: read · specification: -

> Identify research items that cannot be published until compliance evidence is complete.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "MNPI & Research Review"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `mnpi_research_review_p2_y`

**medium** · category: read · specification: -

> Identify research items that cannot be published until compliance evidence is complete.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "MNPI & Research Review"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `mnpi_research_review_p3_x`

**medium** · category: read · specification: -

> Create the approval narrative for legal review with unresolved risks and required attestations.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "MNPI & Research Review"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `mnpi_research_review_p3_y`

**medium** · category: read · specification: -

> Create the approval narrative for legal review with unresolved risks and required attestations.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "MNPI & Research Review"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### nav_fees_close_dashboard (6)

#### `nav_fees_close_dashboard_p1_x`

**medium** · category: read · specification: -

> Prepare the close package: NAV bridge, tolerance exceptions, fee accruals, cash breaks, and unresolved dependencies.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "NAV, Fees & Close Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `nav_fees_close_dashboard_p1_y`

**medium** · category: read · specification: -

> Prepare the close package: NAV bridge, tolerance exceptions, fee accruals, cash breaks, and unresolved dependencies.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "NAV, Fees & Close Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `nav_fees_close_dashboard_p2_x`

**medium** · category: read · specification: -

> Identify items that could delay the daily or monthly NAV sign-off.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "NAV, Fees & Close Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `nav_fees_close_dashboard_p2_y`

**medium** · category: read · specification: -

> Identify items that could delay the daily or monthly NAV sign-off.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "NAV, Fees & Close Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `nav_fees_close_dashboard_p3_x`

**medium** · category: read · specification: -

> Summarize fee, cash, and pricing exceptions that require fund controller approval.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "NAV, Fees & Close Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `nav_fees_close_dashboard_p3_y`

**medium** · category: read · specification: -

> Summarize fee, cash, and pricing exceptions that require fund controller approval.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "NAV, Fees & Close Dashboard"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### portfolio_command_center (6)

#### `portfolio_command_center_p1_x`

**medium** · category: read · specification: -

> Prepare the PM morning note: overnight P&L, largest active exposures, limit pressure, and trade actions by urgency.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Portfolio Command Center"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `portfolio_command_center_p1_y`

**medium** · category: read · specification: -

> Prepare the PM morning note: overnight P&L, largest active exposures, limit pressure, and trade actions by urgency.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Portfolio Command Center"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `portfolio_command_center_p2_x`

**medium** · category: read · specification: -

> Find holdings where conviction, liquidity, and risk contribution disagree with the current portfolio weight.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Portfolio Command Center"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `portfolio_command_center_p2_y`

**medium** · category: read · specification: -

> Find holdings where conviction, liquidity, and risk contribution disagree with the current portfolio weight.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Portfolio Command Center"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `portfolio_command_center_p3_x`

**medium** · category: read · specification: -

> Explain which alerts should be escalated to the CIO before the opening risk meeting.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Portfolio Command Center"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `portfolio_command_center_p3_y`

**medium** · category: read · specification: -

> Explain which alerts should be escalated to the CIO before the opening risk meeting.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Portfolio Command Center"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### quant_research_backtest_lab (6)

#### `quant_research_backtest_lab_p1_x`

**medium** · category: read · specification: -

> Evaluate whether the selected model is production-ready using signal quality, backtest path, risk exposures, and capacity.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Quant Research & Backtest Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `quant_research_backtest_lab_p1_y`

**medium** · category: read · specification: -

> Evaluate whether the selected model is production-ready using signal quality, backtest path, risk exposures, and capacity.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Quant Research & Backtest Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `quant_research_backtest_lab_p2_x`

**medium** · category: read · specification: -

> Identify signals with attractive IC but unacceptable turnover, crowding, or liquidity cost.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Quant Research & Backtest Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `quant_research_backtest_lab_p2_y`

**medium** · category: read · specification: -

> Identify signals with attractive IC but unacceptable turnover, crowding, or liquidity cost.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Quant Research & Backtest Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `quant_research_backtest_lab_p3_x`

**medium** · category: read · specification: -

> Draft the model review memo for PM and risk approval.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Quant Research & Backtest Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `quant_research_backtest_lab_p3_y`

**medium** · category: read · specification: -

> Draft the model review memo for PM and risk approval.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Quant Research & Backtest Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### rebalance_scenario_lab (6)

#### `rebalance_scenario_lab_p1_x`

**medium** · category: read · specification: -

> Draft a rebalance recommendation that balances target drift, liquidity cost, restricted-list checks, and scenario downside.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Rebalance & Scenario Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `rebalance_scenario_lab_p1_y`

**medium** · category: read · specification: -

> Draft a rebalance recommendation that balances target drift, liquidity cost, restricted-list checks, and scenario downside.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Rebalance & Scenario Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `rebalance_scenario_lab_p2_x`

**medium** · category: read · specification: -

> Identify proposed trades that should be resized or delayed because of ADV usage, constraints, or compliance blockers.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Rebalance & Scenario Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `rebalance_scenario_lab_p2_y`

**medium** · category: read · specification: -

> Identify proposed trades that should be resized or delayed because of ADV usage, constraints, or compliance blockers.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Rebalance & Scenario Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `rebalance_scenario_lab_p3_x`

**medium** · category: read · specification: -

> Create an approval memo with implementation risk, residual drift, and the decision needed from the PM.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Rebalance & Scenario Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `rebalance_scenario_lab_p3_y`

**medium** · category: read · specification: -

> Create an approval memo with implementation risk, residual drift, and the decision needed from the PM.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Rebalance & Scenario Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### reporting_factsheet_studio (6)

#### `reporting_factsheet_studio_p1_x`

**medium** · category: read · specification: -

> Build the monthly reporting checklist: performance, attribution, risk stats, commentary, disclosures, and DDQ blockers.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Reporting & Factsheet Studio"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `reporting_factsheet_studio_p1_y`

**medium** · category: read · specification: -

> Build the monthly reporting checklist: performance, attribution, risk stats, commentary, disclosures, and DDQ blockers.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Reporting & Factsheet Studio"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `reporting_factsheet_studio_p2_x`

**medium** · category: read · specification: -

> Find factsheet language that needs approval before external distribution.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Reporting & Factsheet Studio"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `reporting_factsheet_studio_p2_y`

**medium** · category: read · specification: -

> Find factsheet language that needs approval before external distribution.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Reporting & Factsheet Studio"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `reporting_factsheet_studio_p3_x`

**medium** · category: read · specification: -

> Summarize what changed in returns, attribution, risk, and client-facing commentary for the selected period.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Reporting & Factsheet Studio"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `reporting_factsheet_studio_p3_y`

**medium** · category: read · specification: -

> Summarize what changed in returns, attribution, risk, and client-facing commentary for the selected period.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Reporting & Factsheet Studio"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### risk_exposure_monitor (6)

#### `risk_exposure_monitor_p1_x`

**medium** · category: read · specification: -

> Prepare the risk officer briefing: VaR drivers, stress losses, concentration, breaches, and recommended actions.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Risk & Exposure Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 8 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `risk_exposure_monitor_p1_y`

**medium** · category: read · specification: -

> Prepare the risk officer briefing: VaR drivers, stress losses, concentration, breaches, and recommended actions.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Risk & Exposure Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 8 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `risk_exposure_monitor_p2_x`

**medium** · category: read · specification: -

> Identify positions contributing disproportionate marginal VaR or stress P&L relative to their portfolio weight.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Risk & Exposure Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `risk_exposure_monitor_p2_y`

**medium** · category: read · specification: -

> Identify positions contributing disproportionate marginal VaR or stress P&L relative to their portfolio weight.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Risk & Exposure Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `risk_exposure_monitor_p3_x`

**medium** · category: read · specification: -

> Explain which limits are closest to escalation and what portfolio changes would reduce utilization.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Risk & Exposure Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `risk_exposure_monitor_p3_y`

**medium** · category: read · specification: -

> Explain which limits are closest to escalation and what portfolio changes would reduce utilization.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Risk & Exposure Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### strategy_health_monitor (6)

#### `strategy_health_monitor_p1_x`

**medium** · category: read · specification: -

> Rank strategy sleeves by return quality, drawdown behavior, crowding, and remaining capacity.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Strategy Health Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `strategy_health_monitor_p1_y`

**medium** · category: read · specification: -

> Rank strategy sleeves by return quality, drawdown behavior, crowding, and remaining capacity.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Strategy Health Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `strategy_health_monitor_p2_x`

**medium** · category: read · specification: -

> Highlight themes where factor tilt or liquidity capacity is inconsistent with PM conviction.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Strategy Health Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `strategy_health_monitor_p2_y`

**medium** · category: read · specification: -

> Highlight themes where factor tilt or liquidity capacity is inconsistent with PM conviction.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Strategy Health Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `strategy_health_monitor_p3_x`

**medium** · category: read · specification: -

> Build the weekly strategy-health brief for the CIO with watchlist names and catalyst risk.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Strategy Health Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `strategy_health_monitor_p3_y`

**medium** · category: read · specification: -

> Build the weekly strategy-health brief for the CIO with watchlist names and catalyst risk.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Strategy Health Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### stress_liquidity_lab (6)

#### `stress_liquidity_lab_p1_x`

**medium** · category: read · specification: -

> Summarize the selected stress scenario with portfolio loss, liquidation days, crowded names, and redemption impact.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Stress & Liquidity Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `stress_liquidity_lab_p1_y`

**medium** · category: read · specification: -

> Summarize the selected stress scenario with portfolio loss, liquidation days, crowded names, and redemption impact.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Stress & Liquidity Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `stress_liquidity_lab_p2_x`

**medium** · category: read · specification: -

> Find assumptions that should be challenged before the risk committee signs off.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Stress & Liquidity Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `stress_liquidity_lab_p2_y`

**medium** · category: read · specification: -

> Find assumptions that should be challenged before the risk committee signs off.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Stress & Liquidity Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `stress_liquidity_lab_p3_x`

**medium** · category: read · specification: -

> Create the committee sign-off note with unresolved actions and owners.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Stress & Liquidity Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `stress_liquidity_lab_p3_y`

**medium** · category: read · specification: -

> Create the committee sign-off note with unresolved actions and owners.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Stress & Liquidity Lab"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### vendor_dataset_monitor (6)

#### `vendor_dataset_monitor_p1_x`

**medium** · category: read · specification: -

> Prepare the vendor SLA report by latency, freshness, validation failures, incidents, and affected fund apps.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Vendor & Dataset Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vendor_dataset_monitor_p1_y`

**medium** · category: read · specification: -

> Prepare the vendor SLA report by latency, freshness, validation failures, incidents, and affected fund apps.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Vendor & Dataset Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vendor_dataset_monitor_p2_x`

**medium** · category: read · specification: -

> Identify data quality issues that create trading, risk, reporting, or compliance impact.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Vendor & Dataset Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vendor_dataset_monitor_p2_y`

**medium** · category: read · specification: -

> Identify data quality issues that create trading, risk, reporting, or compliance impact.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Vendor & Dataset Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vendor_dataset_monitor_p3_x`

**medium** · category: read · specification: -

> Draft the vendor escalation note with affected datasets, app impact, and owner actions.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Vendor & Dataset Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vendor_dataset_monitor_p3_y`

**medium** · category: read · specification: -

> Draft the vendor escalation note with affected datasets, app impact, and owner actions.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Vendor & Dataset Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### workspace_data_control_center (6)

#### `workspace_data_control_center_p1_x`

**medium** · category: read · specification: -

> Audit data platform readiness: failed jobs, stale feeds, entitlements, exports, and Copilot visibility flags.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Workspace Data Control Center"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 8 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `workspace_data_control_center_p1_y`

**medium** · category: read · specification: -

> Audit data platform readiness: failed jobs, stale feeds, entitlements, exports, and Copilot visibility flags.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Workspace Data Control Center"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 8 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `workspace_data_control_center_p2_x`

**medium** · category: read · specification: -

> Identify apps or widgets whose data or AI access should be restricted before a fund demo or production rollout.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Workspace Data Control Center"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `workspace_data_control_center_p2_y`

**medium** · category: read · specification: -

> Identify apps or widgets whose data or AI access should be restricted before a fund demo or production rollout.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Workspace Data Control Center"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `workspace_data_control_center_p3_x`

**medium** · category: read · specification: -

> Summarize usage, export, and prompt-audit activity for the platform owner.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-x`; active dashboard "Workspace Data Control Center"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `workspace_data_control_center_p3_y`

**medium** · category: read · specification: -

> Summarize usage, export, and prompt-audit activity for the platform owner.

- Initial workspace: baseline `all-stark-enterprise-apps`; backends `stark-enterprise-y`; active dashboard "Workspace Data Control Center"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):



## Suite: enterprise-apps-usage (192 tasks)

### curate (24)

#### `compliance_alert_review_level0`

**level0** · category: dashboard · specification: -

> Compliance-alert opening board: add Bench Stark Enterprise — Compliance Surveillance Hub, Open Alert Metrics to the current board.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` → `missing_widget`

#### `compliance_alert_review_level1`

**level1** · category: dashboard · specification: -

> Compliance-alert discovery board: add Bench Stark Enterprise — Compliance Surveillance Hub, Policy Breaches to the current board.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_personal_trading_policy_breaches` → `missing_widget`

#### `compliance_alert_review_level2`

**level2** · category: dashboard · specification: -

> Compliance-alert paired board: add Bench Stark Enterprise — Compliance Surveillance Hub, Open Alert Metrics; Bench Stark Enterprise — Compliance Surveillance Hub, Policy Breaches to the current board.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_personal_trading_policy_breaches` → `missing_widget`

#### `compliance_alert_review_level3`

**level3** · category: dashboard · specification: -

> Compliance-alert cross-catalog board: add Bench Stark Enterprise — Compliance Surveillance Hub, Open Alert Metrics; Getting Started — Getting Started, Markdown Widget with Number Input to the current board.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` → `missing_widget`
- **Widget** ≥1× `Getting Started/markdown_widget_with_number_input` → `missing_widget`

#### `compliance_alert_review_level4`

**level4** · category: dashboard · specification: -

> Compliance-alert governed board: follow the Finance Guidance Tracker skill (finance-guidance-tracker), add Bench Stark Enterprise — Compliance Surveillance Hub, Open Alert Metrics; Getting Started — Getting Started, Markdown Widget with Number Input, and add a Compliance-alert Governance note naming evidence gaps.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` → `missing_widget`
- **Widget** ≥1× `Getting Started/markdown_widget_with_number_input` → `missing_widget`
- **Generated note** ≥1× named ~"Compliance-alert Governance" whose content mentions "evidence gaps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `compliance_alert_review_level5`

**level5** · category: platform · specification: -

> Compliance-alert build board: add Wave Three Compliance Review with a Compliance Review Register table and publish and instantiate Compliance Review App on Review; also add Bench Stark Enterprise — Compliance Surveillance Hub, Open Alert Metrics; Getting Started — Getting Started, Markdown Widget with Number Input. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Guidance Tracker skill (finance-guidance-tracker) and add a Compliance-alert Build Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Compliance Review/compliance_review_register` on tab `review` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` → `missing_widget`
- **Widget** ≥1× `Getting Started/markdown_widget_with_number_input` → `missing_widget`
- **Generated note** ≥1× named ~"Compliance-alert Build Note" whose content mentions "evidence gaps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `decision_briefing_level0`

**level0** · category: single-widget · specification: -

> The PM wants Bench Stark Enterprise's Portfolio Command Center, Trade Ideas, on the open Wave One Decision Brief board, with fund set to Flagship Long/Short and period set to YTD.

- Initial workspace: dashboard "Wave One Decision Brief"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "YTD"} → `missing_widget`

#### `decision_briefing_level1`

**level1** · category: single-widget · specification: -

> On the open Wave One Decision Brief board, find Bench Stark Enterprise's Portfolio Command Center, Trade Ideas, and add it for Flagship Long/Short and YTD.

- Initial workspace: dashboard "Wave One Decision Brief"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "YTD"} → `missing_widget`

#### `decision_briefing_level2`

**level2** · category: single-widget · specification: -

> Prepare the open Wave One Decision Brief board under the quarterly PM briefing policy. Add Bench Stark Enterprise's Portfolio Command Center, Trade Ideas, for Flagship Long/Short; quarterly means QTD.

- Initial workspace: dashboard "Wave One Decision Brief"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "QTD"} → `missing_widget`

#### `decision_briefing_level3`

**level3** · category: dashboard · specification: -

> Set up the open Wave One Decision Brief board: place Bench Stark Enterprise's Portfolio Command Center, Trade Ideas, for Flagship Long/Short and QTD beside Getting Started's Car Manufacturer Performance for TSLA and 2024. Put Trade Ideas at x 0, y 0, width 20, height 14 and the manufacturer view at x 20, y 0, width 20, height 14.

- Initial workspace: dashboard "Wave One Decision Brief"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "QTD"} → `missing_widget`
- **Widget** ≥1× `Getting Started/company_performance` with data_args ⊇ {"company": "TSLA", "year": 2024} → `missing_widget`

#### `decision_briefing_level4`

**level4** · category: dashboard · specification: -

> Use Workspace session guidance to prepare the open Wave One Decision Brief board: place Bench Stark Enterprise's Portfolio Command Center, Trade Ideas, for Flagship Long/Short and QTD beside Getting Started's Car Manufacturer Performance for TSLA and 2024. Put Trade Ideas at x 0, y 0, width 20, height 14 and the manufacturer view at x 20, y 0, width 20, height 14.

- Initial workspace: dashboard "Wave One Decision Brief"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "QTD"} → `missing_widget`
- **Widget** ≥1× `Getting Started/company_performance` with data_args ⊇ {"company": "TSLA", "year": 2024} → `missing_widget`

#### `decision_briefing_level5`

**level5** · category: platform · specification: -

> The PM needs a Decision Tile Backend with a Decision Summary Tile metric. Author and add it, then instantiate its Decision Briefing App. On Briefing, place Bench Stark Enterprise's Portfolio Command Center, Trade Ideas, beside Getting Started's Car Manufacturer Performance at y 10, x 0 and x 20, each width 20 and height 14. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Daloopa Capital Allocation skill (daloopa-capital-allocation) and add a Decision Briefing Build Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` on tab `briefing` → `missing_widget`
- **Widget** ≥1× `Getting Started/company_performance` on tab `briefing` → `missing_widget`
- **Widget** ≥1× `Decision Tile Backend/decision_summary_tile` → `missing_widget`
- **Generated note** ≥1× named ~"Decision Briefing Build Note" whose content mentions "Free Cash Flow" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_quality_review_level0`

**level0** · category: dashboard · specification: -

> Execution-quality opening board: add Bench Stark Enterprise — Execution Desk, Live Orders to the current board.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` → `missing_widget`

#### `execution_quality_review_level1`

**level1** · category: dashboard · specification: -

> Execution-quality discovery board: add Bench Stark Enterprise — Execution Desk, Broker Scorecard to the current board.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_fills_broker_scorecard` → `missing_widget`

#### `execution_quality_review_level2`

**level2** · category: dashboard · specification: -

> Execution-quality paired board: add Bench Stark Enterprise — Execution Desk, Live Orders; Bench Stark Enterprise — Execution Desk, Broker Scorecard to the current board.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_fills_broker_scorecard` → `missing_widget`

#### `execution_quality_review_level3`

**level3** · category: dashboard · specification: -

> Execution-quality cross-catalog board: add Bench Stark Enterprise — Execution Desk, Live Orders; Getting Started — Getting Started, Multi PDF Viewer - URL to the current board.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` → `missing_widget`
- **Widget** ≥1× `Getting Started/multi_pdf_url` → `missing_widget`

#### `execution_quality_review_level4`

**level4** · category: dashboard · specification: -

> Execution-quality governed board: follow the Finance Comps skill (finance-comps), add Bench Stark Enterprise — Execution Desk, Live Orders; Getting Started — Getting Started, Multi PDF Viewer - URL, and add a Execution-quality Governance note naming outliers.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` → `missing_widget`
- **Widget** ≥1× `Getting Started/multi_pdf_url` → `missing_widget`
- **Generated note** ≥1× named ~"Execution-quality Governance" whose content mentions "outliers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_quality_review_level5`

**level5** · category: platform · specification: -

> Execution-quality build board: add Wave Three Execution Review with a Execution Review Register table and publish and instantiate Execution Review App on Quality; also add Bench Stark Enterprise — Execution Desk, Live Orders; Getting Started — Getting Started, Multi PDF Viewer - URL. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Comps skill (finance-comps) and add a Execution-quality Build Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Execution Review/execution_review_register` on tab `quality` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` → `missing_widget`
- **Widget** ≥1× `Getting Started/multi_pdf_url` → `missing_widget`
- **Generated note** ≥1× named ~"Execution-quality Build Note" whose content mentions "outliers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `market_telemetry_level0`

**level0** · category: single-widget · specification: -

> Add Getting Started's Stock Price Trends - Line Sparklines with First/Last Points to the open Wave Two Market Telemetry board.

- Initial workspace: dashboard "Wave Two Market Telemetry"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/sparkline_line` → `missing_widget`

#### `market_telemetry_level1`

**level1** · category: single-widget · specification: -

> On the open Wave Two Market Telemetry board, add Getting Started's live-updating grid with real-time WebSocket updates for AAPL.

- Initial workspace: dashboard "Wave Two Market Telemetry"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/live_grid_data` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`

#### `market_telemetry_level2`

**level2** · category: single-widget · specification: -

> Prepare the open Wave Two Market Telemetry board for the quarterly liquidity policy. Add Widget Examples' [MOCK DATA] Tabs + Dropdown Combined; quarterly liquidity means quarterly and liquidity. Place it at x 0, y 0, width 40, height 14.

- Initial workspace: dashboard "Wave Two Market Telemetry"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/tabs_with_dropdown` with data_args ⊇ {"period": "quarterly", "category": "liquidity"} → `missing_widget`

#### `market_telemetry_level3`

**level3** · category: dashboard · specification: -

> Build out the open Wave Two Market Telemetry board with Getting Started's Stock Price Trends - Line Sparklines with First/Last Points beside Widget Examples' [MOCK DATA] Tabs + Dropdown Combined for quarterly liquidity. Put the trends at x 0, y 0, width 20, height 12 and the ratio view at x 20, y 0, width 20, height 12.

- Initial workspace: dashboard "Wave Two Market Telemetry"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/sparkline_line` → `missing_widget`
- **Widget** ≥1× `Widget Examples/tabs_with_dropdown` with data_args ⊇ {"period": "quarterly", "category": "liquidity"} → `missing_widget`

#### `market_telemetry_level4`

**level4** · category: dashboard · specification: -

> Using Workspace session guidance, finish the open Wave Two Market Telemetry board with Getting Started's Stock Price Trends - Line Sparklines with First/Last Points beside Widget Examples' [MOCK DATA] Tabs + Dropdown Combined for quarterly liquidity. Put them at x 0 and x 20, y 0, each width 20 and height 12.

- Initial workspace: dashboard "Wave Two Market Telemetry"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/sparkline_line` → `missing_widget`
- **Widget** ≥1× `Widget Examples/tabs_with_dropdown` with data_args ⊇ {"period": "quarterly", "category": "liquidity"} → `missing_widget`

#### `market_telemetry_level5`

**level5** · category: platform · specification: -

> Author and add a Telemetry Summary Backend with a Telemetry Summary Tile metric, then instantiate its Market Telemetry App. On Monitor, place Getting Started's Stock Price Trends - Line Sparklines with First/Last Points beside Widget Examples' [MOCK DATA] Tabs + Dropdown Combined at y 10, x 0 and x 20, each width 20 and height 12. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Tearsheet skill (finance-tearsheet) and add a Market Telemetry Build Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/sparkline_line` on tab `monitor` → `missing_widget`
- **Widget** ≥1× `Widget Examples/tabs_with_dropdown` on tab `monitor` → `missing_widget`
- **Widget** ≥1× `Telemetry Summary Backend/telemetry_summary_tile` → `missing_widget`
- **Generated note** ≥1× named ~"Market Telemetry Build Note" whose content mentions "price action" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### extend (24)

#### `guidance_service_lifecycle_level0`

**level0** · category: platform · specification: -

> Guidance-service level-0 service: add a custom backend Wave Three Guidance Service with the Evidence Gaps table. Widget ids are the snake_case of widget names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `guidance_service_lifecycle_level1`

**level1** · category: platform · specification: -

> Guidance-service level-1 service: add a custom backend Wave Three Guidance Service with the Changed Assumptions table. Widget ids are the snake_case of widget names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `guidance_service_lifecycle_level2`

**level2** · category: platform · specification: -

> Guidance-service paired service: add a custom backend Wave Three Guidance Service with Evidence Gaps and Changed Assumptions tables. Widget ids are the snake_case of widget names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `guidance_service_lifecycle_level3`

**level3** · category: platform · specification: -

> Guidance-service app service: add a custom backend Wave Three Guidance Service with Evidence Gaps and Changed Assumptions tables, publish Guidance Service App on Review, and instantiate it. Widget ids are the snake_case of widget names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Guidance Service/evidence_gaps` on tab `review` → `missing_widget`
- **Widget** ≥1× `Wave Three Guidance Service/changed_assumptions` on tab `review` → `missing_widget`

#### `guidance_service_lifecycle_level4`

**level4** · category: platform · specification: -

> Guidance-service governed service: follow the Finance Guidance Tracker skill (finance-guidance-tracker); add a custom backend Wave Three Guidance Service with Evidence Gaps and Changed Assumptions tables, publish Guidance Service App on Review, and instantiate it. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Guidance Service/evidence_gaps` on tab `review` → `missing_widget`
- **Widget** ≥1× `Wave Three Guidance Service/changed_assumptions` on tab `review` → `missing_widget`

#### `guidance_service_lifecycle_level5`

**level5** · category: platform · specification: -

> Guidance-service complete service: follow the widgets manifest specification; add a custom backend Wave Three Guidance Service with Evidence Gaps, Changed Assumptions, Management Claims tables, publish Guidance Service App with Review and Archive tabs, and instantiate it. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Guidance Tracker skill (finance-guidance-tracker) and add a Guidance-service Governing Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Guidance Service/evidence_gaps` on tab `review` → `missing_widget`
- **Widget** ≥1× `Wave Three Guidance Service/changed_assumptions` on tab `review` → `missing_widget`
- **Widget** ≥1× `Wave Three Guidance Service/management_claims` on tab `archive` → `missing_widget`
- **Generated note** ≥1× named ~"Guidance-service Governing Note" whose content mentions "evidence gaps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `inflection_service_lifecycle_level0`

**level0** · category: platform · specification: -

> Inflection-service level-0 service: add a custom backend Wave Three Inflection Service with the Growth-Rate Reversals table. Widget ids are the snake_case of widget names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `inflection_service_lifecycle_level1`

**level1** · category: platform · specification: -

> Inflection-service level-1 service: add a custom backend Wave Three Inflection Service with the Quarterly Series Monitor table. Widget ids are the snake_case of widget names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `inflection_service_lifecycle_level2`

**level2** · category: platform · specification: -

> Inflection-service paired service: add a custom backend Wave Three Inflection Service with Growth-Rate Reversals and Quarterly Series Monitor tables. Widget ids are the snake_case of widget names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `inflection_service_lifecycle_level3`

**level3** · category: platform · specification: -

> Inflection-service app service: add a custom backend Wave Three Inflection Service with Growth-Rate Reversals and Quarterly Series Monitor tables, publish Inflection Service App on Review, and instantiate it. Widget ids are the snake_case of widget names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Inflection Service/growth_rate_reversals` on tab `review` → `missing_widget`
- **Widget** ≥1× `Wave Three Inflection Service/quarterly_series_monitor` on tab `review` → `missing_widget`

#### `inflection_service_lifecycle_level4`

**level4** · category: platform · specification: -

> Inflection-service governed service: follow the Daloopa Inflection skill (daloopa-inflection); add a custom backend Wave Three Inflection Service with Growth-Rate Reversals and Quarterly Series Monitor tables, publish Inflection Service App on Review, and instantiate it. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Inflection Service/growth_rate_reversals` on tab `review` → `missing_widget`
- **Widget** ≥1× `Wave Three Inflection Service/quarterly_series_monitor` on tab `review` → `missing_widget`

#### `inflection_service_lifecycle_level5`

**level5** · category: platform · specification: -

> Inflection-service complete service: follow the widgets manifest specification; add a custom backend Wave Three Inflection Service with Growth-Rate Reversals, Quarterly Series Monitor, Inflection Evidence Log tables, publish Inflection Service App with Review and Archive tabs, and instantiate it. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Daloopa Inflection skill (daloopa-inflection) and add a Inflection-service Governing Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Inflection Service/growth_rate_reversals` on tab `review` → `missing_widget`
- **Widget** ≥1× `Wave Three Inflection Service/quarterly_series_monitor` on tab `review` → `missing_widget`
- **Widget** ≥1× `Wave Three Inflection Service/inflection_evidence_log` on tab `archive` → `missing_widget`
- **Generated note** ≥1× named ~"Inflection-service Governing Note" whose content mentions "growth-rate reversals" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `research_feed_lifecycle_level0`

**level0** · category: platform · specification: -

> On the open Research Feed Staging board, review the connected backends and refresh Wave Two Research Feed so Research Feed Pulse has the description Refreshed research feed.

- Initial workspace: dashboard "Research Feed Staging"; 1 tab(s): feed; 1 seeded widget(s): research_feed_pulse({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `research_feed_lifecycle_level1`

**level1** · category: platform · specification: -

> From the open Research Feed Staging board, review the connected backends, then refresh Wave Two Research Feed so Research Feed App has one non-overlapping Research Feed Pulse placement on Feed.

- Initial workspace: dashboard "Research Feed Staging"; 1 tab(s): feed; 1 seeded widget(s): research_feed_pulse({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `research_feed_lifecycle_level2`

**level2** · category: platform · specification: -

> Add a minimal Wave Two Research Feed backend serving a Research Feed Pulse table at /research-feed. Widget ids are the snake_case of widget names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `research_feed_lifecycle_level3`

**level3** · category: platform · specification: -

> Publish and add Wave Two Research Feed with Research Feed Pulse and a Research Feed App containing Feed. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `research_feed_lifecycle_level4`

**level4** · category: platform · specification: -

> Set up and add Wave Two Research Feed with Research Feed Pulse and Source Freshness Alert, publish Research Feed App with both on Feed, and instantiate it. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Two Research Feed/research_feed_pulse` on tab `feed` → `missing_widget`
- **Widget** ≥1× `Wave Two Research Feed/source_freshness_alert` on tab `feed` → `missing_widget`

#### `research_feed_lifecycle_level5`

**level5** · category: platform · specification: -

> Complete the research service with Wave Two Research Feed, Research Feed Pulse, Source Freshness Alert, and Archive Coverage Watch. Add the backend, publish Research Feed App with Feed and Archive tabs, and instantiate it. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Daloopa Capital Allocation skill (daloopa-capital-allocation) and add a Research Feed Build Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Two Research Feed/research_feed_pulse` on tab `feed` → `missing_widget`
- **Widget** ≥1× `Wave Two Research Feed/source_freshness_alert` on tab `feed` → `missing_widget`
- **Widget** ≥1× `Wave Two Research Feed/archive_coverage_watch` on tab `archive` → `missing_widget`
- **Generated note** ≥1× named ~"Research Feed Build Note" whose content mentions "Dividends Paid" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `risk_service_lifecycle_level0`

**level0** · category: platform · specification: -

> On the open Risk Service Staging board, review the connected backends and refresh Wave One Risk Service so its Wave One Risk Signal description is Refreshed risk signal feed.

- Initial workspace: dashboard "Risk Service Staging"; 1 tab(s): monitor; 1 seeded widget(s): wave_one_risk_signal({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `risk_service_lifecycle_level1`

**level1** · category: platform · specification: -

> Review the connected backends on the open Risk Service Staging board, then refresh Wave One Risk Service so Wave One Risk App has one non-overlapping Wave One Risk Signal placement on Monitor.

- Initial workspace: dashboard "Risk Service Staging"; 1 tab(s): monitor; 1 seeded widget(s): wave_one_risk_signal({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `risk_service_lifecycle_level2`

**level2** · category: platform · specification: -

> Add a minimal Wave One Risk Service backend that serves a Wave One Risk Signal table at /risk-signal. Widget ids are the snake_case of widget names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `risk_service_lifecycle_level3`

**level3** · category: platform · specification: -

> The risk desk needs Wave One Risk Service with its Wave One Risk Signal and a Wave One Risk App containing Monitor. Publish and add it. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `risk_service_lifecycle_level4`

**level4** · category: platform · specification: -

> Set up Wave One Risk Service with Wave One Risk Signal and Wave One Limit Alert. Author and add the service, publish Wave One Risk App with both on Monitor, and instantiate it. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave One Risk Service/wave_one_risk_signal` on tab `monitor` → `missing_widget`
- **Widget** ≥1× `Wave One Risk Service/wave_one_limit_alert` on tab `monitor` → `missing_widget`

#### `risk_service_lifecycle_level5`

**level5** · category: platform · specification: -

> Complete the risk desk build with Wave One Risk Service, Wave One Risk Signal, Wave One Limit Alert, and Wave One Stress Watch. Add the service, publish Wave One Risk App with Monitor and Stress tabs, and instantiate it. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Guidance Tracker skill (finance-guidance-tracker) and add a Risk Service Build Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave One Risk Service/wave_one_risk_signal` on tab `monitor` → `missing_widget`
- **Widget** ≥1× `Wave One Risk Service/wave_one_limit_alert` on tab `monitor` → `missing_widget`
- **Widget** ≥1× `Wave One Risk Service/wave_one_stress_watch` on tab `stress` → `missing_widget`
- **Generated note** ≥1× named ~"Risk Service Build Note" whose content mentions "evidence gaps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### handoff (24)

#### `consensus_exception_handoff_level0`

**level0** · category: read · specification: -

> Consensus-exception direct handoff: on the open Consensus Exception Handoff board, read Bench Daloopa's Consensus Estimates with ticker AAPL, then add a Consensus-exception Direct Note recording the exact Total Revenue actual and consensus for 2026Q1.

- Initial workspace: dashboard "Consensus Exception Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Consensus-exception Direct Note" whose content mentions "102070.1", "99404.2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `consensus_exception_handoff_level1`

**level1** · category: read · specification: -

> Consensus-exception discovered handoff: on the open Consensus Exception Handoff board, read Bench Daloopa's Consensus Estimates with ticker AAPL, then add a Consensus-exception Discovered Note recording the exact Total Revenue actual and consensus for 2026Q1.

- Initial workspace: dashboard "Consensus Exception Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Consensus-exception Discovered Note" whose content mentions "102070.1", "99404.2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `consensus_exception_handoff_level2`

**level2** · category: read · specification: -

> Consensus-exception analyst handoff: on the open Consensus Exception Handoff board, read Bench Daloopa's Consensus Estimates with ticker AAPL, then add a Consensus-exception Analyst Note recording the exact Total Revenue actual and consensus for 2026Q1.

- Initial workspace: dashboard "Consensus Exception Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Consensus-exception Analyst Note" whose content mentions "102070.1", "99404.2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `consensus_exception_handoff_level3`

**level3** · category: read · specification: -

> Consensus-exception desk handoff: on the open Consensus Exception Handoff board, read Bench Daloopa's Consensus Estimates with ticker AAPL, then add a Consensus-exception Desk Note recording the exact Total Revenue actual and consensus for 2026Q1.

- Initial workspace: dashboard "Consensus Exception Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Consensus-exception Desk Note" whose content mentions "102070.1", "99404.2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `consensus_exception_handoff_level4`

**level4** · category: dashboard · specification: -

> Consensus-exception governed handoff: follow the Daloopa Earnings Review skill (daloopa-earnings-review) on the open Consensus Exception Handoff board, read Bench Daloopa's Consensus Estimates with ticker AAPL, add a Consensus-exception Governed Handoff note recording the exact Total Revenue actual and consensus for 2026Q1 and consensus, then delegate the follow-up.

- Initial workspace: dashboard "Consensus Exception Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Consensus-exception Governed Handoff" whose content mentions "consensus", "102070.1", "99404.2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `consensus_exception_handoff_level5`

**level5** · category: platform · specification: -

> Consensus-exception build handoff: add Wave Three Consensus Handoff with a Consensus Handoff Register table, publish and instantiate Consensus Handoff App with one Handoff tab, add a Consensus-exception Build Handoff note grounded in Bench Daloopa's Consensus Estimates with the exact Total Revenue actual and consensus for 2026Q1 and the Daloopa Earnings Review skill (daloopa-earnings-review)'s governing concept, then delegate. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Consensus Handoff/consensus_handoff_register` on tab `handoff` → `missing_widget`
- **Generated note** ≥1× named ~"Consensus-exception Build Handoff" whose content mentions "consensus", "102070.1", "99404.2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_handoff_level0`

**level0** · category: read · specification: -

> On the open Earnings Handoff board, read Bench Stark Enterprise's Earnings & Estimates Monitor, Upcoming Earnings, for Healthcare, LLY, and YTD. Add an LLY Earnings Handoff note with the exact score and status.

- Initial workspace: dashboard "Earnings Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"LLY Earnings Handoff" whose content mentions "27.63", "Open" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_handoff_level1`

**level1** · category: read · specification: -

> Build the Apple note on the open Earnings Handoff board. Find Bench Stark Enterprise's Earnings & Estimates Monitor, Upcoming Earnings, for Technology, AAPL, and QTD, then add an Apple Earnings Handoff note with the exact score and status.

- Initial workspace: dashboard "Earnings Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Apple Earnings Handoff" whose content mentions "6.52", "In Review" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_handoff_level2`

**level2** · category: read · specification: -

> Prepare a Microsoft note on the open Earnings Handoff board under the current-month handoff policy. Read Bench Stark Enterprise's Earnings & Estimates Monitor, Upcoming Earnings, for Technology and MSFT; current month means MTD. Add a Microsoft Earnings Handoff note with the exact score and status.

- Initial workspace: dashboard "Earnings Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Microsoft Earnings Handoff" whose content mentions "89.94", "Escalated" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_handoff_level3`

**level3** · category: platform · specification: -

> For the open Earnings Handoff board, follow Finance Earnings Prep governance and read Bench Stark Enterprise's Earnings & Estimates Monitor, Upcoming Earnings, for Technology, AAPL, and QTD. Add a Governed Apple Handoff note with the exact score and status.

- Initial workspace: dashboard "Earnings Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Governed Apple Handoff" whose content mentions "6.52", "In Review" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_handoff_level4`

**level4** · category: platform · specification: -

> Handle the coverage follow-up route from the open Earnings Handoff board under Finance Earnings Prep governance. Read Bench Stark Enterprise's Earnings & Estimates Monitor, Upcoming Earnings, for Healthcare, LLY, and YTD; add an LLY Delegation Handoff note with exact score and status, then delegate the coverage follow-up.

- Initial workspace: dashboard "Earnings Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"LLY Delegation Handoff" whose content mentions "27.63", "Open" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_handoff_level5`

**level5** · category: platform · specification: -

> From the open Earnings Handoff board, author and add a minimal custom Earnings Handoff Backend with one Earnings Handoff Register. Publish and instantiate Earnings Handoff App with one Handoff tab, add an Earnings Build Handoff note naming Earnings Handoff App and Earnings Handoff Register, then delegate the build-review follow-up. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Earnings Prep skill (finance-earnings-prep) and record its governing concept in the note.

- Initial workspace: dashboard "Earnings Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Earnings Handoff Backend/earnings_handoff_register` on tab `handoff` → `missing_widget`
- **Generated note** ≥1× named ~"Earnings Build Handoff" whose content mentions "Earnings Handoff App", "Earnings Handoff Register", "street numbers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `news_desk_handoff_level0`

**level0** · category: read · specification: -

> On the open News Desk Handoff board, read Getting Started's Sample News Feed with category set to business and limit set to 2. Add a Markets News Handoff note with the exact lead title and author.

- Initial workspace: dashboard "News Desk Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Markets News Handoff" whose content mentions "Global Markets Rally on Positive Economic Data", "Robert Williams" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `news_desk_handoff_level1`

**level1** · category: read · specification: -

> Find Getting Started's Sample News Feed from the open News Desk Handoff board for technology, limited to 2, then add a Technology News Handoff note with the exact lead title and author.

- Initial workspace: dashboard "News Desk Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Technology News Handoff" whose content mentions "AI Breakthrough: New Model Achieves Human-Level Reasoning", "Sarah Johnson" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `news_desk_handoff_level2`

**level2** · category: read · specification: -

> Prepare a Science News Handoff note on the open News Desk Handoff board under the science route. Read Getting Started's Sample News Feed for that route, limited to 2, and pin the exact lead title and author.

- Initial workspace: dashboard "News Desk Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Science News Handoff" whose content mentions "Scientists Discover New Earth-like Exoplanet in Habitable Zone", "Dr. Emily Rogers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `news_desk_handoff_level3`

**level3** · category: platform · specification: -

> Using Workspace session guidance on the open News Desk Handoff board, read Getting Started's Sample News Feed for business, limited to 2. Add a Governed Expansion Handoff note with the exact second title and author.

- Initial workspace: dashboard "News Desk Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Governed Expansion Handoff" whose content mentions "E-commerce Giant Announces Major Expansion into Southeast Asia", "Lisa Anderson" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `news_desk_handoff_level4`

**level4** · category: platform · specification: -

> Handle the science follow-up route from the open News Desk Handoff board under Workspace session guidance. Read Getting Started's Sample News Feed for science, limited to 2; add a Science Delegation Handoff note with the exact lead title and author, then delegate the editorial follow-up.

- Initial workspace: dashboard "News Desk Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Science Delegation Handoff" whose content mentions "Scientists Discover New Earth-like Exoplanet in Habitable Zone", "Dr. Emily Rogers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `news_desk_handoff_level5`

**level5** · category: platform · specification: -

> Starting from the open News Desk Handoff board, author and add a minimal custom News Handoff Backend with one News Handoff Register. Publish and instantiate News Handoff App with one Handoff tab, add a News Build Handoff note naming News Handoff App and News Handoff Register, then delegate the build-review follow-up. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Tearsheet skill (finance-tearsheet) and record its governing concept in the note.

- Initial workspace: dashboard "News Desk Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `News Handoff Backend/news_handoff_register` on tab `handoff` → `missing_widget`
- **Generated note** ≥1× named ~"News Build Handoff" whose content mentions "News Handoff App", "News Handoff Register", "catalysts" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `segment_mix_handoff_level0`

**level0** · category: read · specification: -

> Segment-mix direct handoff: on the open Segment Mix Handoff board, read Bench Daloopa's Segment Breakdown with ticker AAPL, period 2026Q1, then add a Segment-mix Direct Note recording the top segment and its exact revenue_musd.

- Initial workspace: dashboard "Segment Mix Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Segment-mix Direct Note" whose content mentions "iPhone", "52365.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `segment_mix_handoff_level1`

**level1** · category: read · specification: -

> Segment-mix discovered handoff: on the open Segment Mix Handoff board, read Bench Daloopa's Segment Breakdown with ticker AAPL, period 2026Q1, then add a Segment-mix Discovered Note recording the top segment and its exact revenue_musd.

- Initial workspace: dashboard "Segment Mix Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Segment-mix Discovered Note" whose content mentions "iPhone", "52365.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `segment_mix_handoff_level2`

**level2** · category: read · specification: -

> Segment-mix analyst handoff: on the open Segment Mix Handoff board, read Bench Daloopa's Segment Breakdown with ticker AAPL, period 2026Q1, then add a Segment-mix Analyst Note recording the top segment and its exact revenue_musd.

- Initial workspace: dashboard "Segment Mix Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Segment-mix Analyst Note" whose content mentions "iPhone", "52365.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `segment_mix_handoff_level3`

**level3** · category: read · specification: -

> Segment-mix desk handoff: on the open Segment Mix Handoff board, read Bench Daloopa's Segment Breakdown with ticker AAPL, period 2026Q1, then add a Segment-mix Desk Note recording the top segment and its exact revenue_musd.

- Initial workspace: dashboard "Segment Mix Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Segment-mix Desk Note" whose content mentions "iPhone", "52365.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `segment_mix_handoff_level4`

**level4** · category: dashboard · specification: -

> Segment-mix governed handoff: follow the Daloopa Tearsheet skill (daloopa-tearsheet) on the open Segment Mix Handoff board, read Bench Daloopa's Segment Breakdown with ticker AAPL, period 2026Q1, add a Segment-mix Governed Handoff note recording the top segment and its exact revenue_musd and mix, then delegate the follow-up.

- Initial workspace: dashboard "Segment Mix Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Segment-mix Governed Handoff" whose content mentions "mix", "iPhone", "52365.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `segment_mix_handoff_level5`

**level5** · category: platform · specification: -

> Segment-mix build handoff: add Wave Three Segment Handoff with a Segment Handoff Register table, publish and instantiate Segment Handoff App with one Handoff tab, add a Segment-mix Build Handoff note grounded in Bench Daloopa's Segment Breakdown with the top segment and its exact revenue_musd and the Daloopa Tearsheet skill (daloopa-tearsheet)'s governing concept, then delegate. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Segment Handoff/segment_handoff_register` on tab `handoff` → `missing_widget`
- **Generated note** ≥1× named ~"Segment-mix Build Handoff" whose content mentions "mix", "iPhone", "52365.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### organize (24)

#### `client_onboarding_flow_level0`

**level0** · category: dashboard · specification: -

> For client operations, create a dashboard named Wave Two Client Onboarding and make it the active board.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `client_onboarding_flow_level1`

**level1** · category: dashboard · specification: -

> Create and activate Wave Two Client Onboarding with Intake and Review tabs for the operations team.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `client_onboarding_flow_level2`

**level2** · category: dashboard · specification: -

> Operations needs you to create and activate Wave Two Client Onboarding with Intake, Review, and Approval tabs, then open Review.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Wave Two Client Onboarding" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `intake` must exist (matched by tab id) → `missing_tab`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Tab** `approval` must exist (matched by tab id) → `missing_tab`

#### `client_onboarding_flow_level3`

**level3** · category: dashboard · specification: -

> On the open Client Onboarding Staging board, rename the dashboard to Wave Two Client Onboarding and change Intake to Client Intake. Preserve Review and every other workspace item.

- Initial workspace: dashboard "Client Onboarding Staging"; 2 tab(s): intake, review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `client_onboarding_flow_level4`

**level4** · category: dashboard · specification: -

> Client operations needs a governed setup: following Workspace session guidance, create and activate Wave Two Client Onboarding with Client Intake, Due Diligence, and Approval tabs in that order.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `client_onboarding_flow_level5`

**level5** · category: platform · specification: -

> Author and add a Client Onboarding Backend with Client Intake Queue and Approval Log table views, then publish and instantiate a Client Onboarding App with Intake and Approvals tabs. Follow the apps manifest specification. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Guidance Tracker skill (finance-guidance-tracker) and add a Client Onboarding Build Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Client Onboarding Backend/client_intake_queue` on tab `intake` → `missing_widget`
- **Widget** ≥1× `Client Onboarding Backend/approval_log` on tab `approvals` → `missing_widget`
- **Generated note** ≥1× named ~"Client Onboarding Build Note" whose content mentions "changed assumptions" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `committee_navigation_level0`

**level0** · category: dashboard · specification: -

> Create a dashboard named Wave One Committee Review for the committee and make it the active board.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `committee_navigation_level1`

**level1** · category: dashboard · specification: -

> Create Wave One Committee Review as the active committee board, with Agenda and Evidence tabs.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `committee_navigation_level2`

**level2** · category: dashboard · specification: -

> The committee needs an active Wave One Committee Review board with Agenda and Evidence tabs. Create it, then open Evidence.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Wave One Committee Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `agenda` must exist (matched by tab id) → `missing_tab`
- **Tab** `evidence` must exist (matched by tab id) → `missing_tab`

#### `committee_navigation_level3`

**level3** · category: dashboard · specification: -

> On the open Committee Review Staging board, rename the dashboard to Wave One Committee Review and change its Agenda tab to Decision Agenda. Keep Evidence and all other workspace content intact.

- Initial workspace: dashboard "Committee Review Staging"; 2 tab(s): agenda, evidence
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `committee_navigation_level4`

**level4** · category: dashboard · specification: -

> Following Workspace session guidance, create and activate Wave One Committee Review with Decision Agenda, Evidence, and Sign-Off tabs in that order.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `committee_navigation_level5`

**level5** · category: platform · specification: -

> The committee needs a Committee Navigation Backend with Agenda Queue and Evidence Register table views. Author and add it, publish a Committee Review App with Agenda and Evidence tabs, and instantiate it. Follow the apps manifest specification. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Earnings Prep skill (finance-earnings-prep) and add a Committee Navigation Build Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Committee Navigation Backend/agenda_queue` on tab `agenda` → `missing_widget`
- **Widget** ≥1× `Committee Navigation Backend/evidence_register` on tab `evidence` → `missing_widget`
- **Generated note** ≥1× named ~"Committee Navigation Build Note" whose content mentions "transcript tone" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `due_diligence_media_room_level0`

**level0** · category: dashboard · specification: -

> Media-room board start: create and open Due Diligence Media Room.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Due Diligence Media Room" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`

#### `due_diligence_media_room_level1`

**level1** · category: dashboard · specification: -

> Media-room tab setup: create and open Due Diligence Media Room, then add Overview and Review tabs.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Due Diligence Media Room" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`

#### `due_diligence_media_room_level2`

**level2** · category: dashboard · specification: -

> Media-room level-2 layout: create and open Due Diligence Media Room, add Overview and Review tabs, then add Getting Started's Video Library with Transcript.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Due Diligence Media Room" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Getting Started/get_video_with_transcript` → `missing_widget`

#### `due_diligence_media_room_level3`

**level3** · category: dashboard · specification: -

> Media-room level-3 layout: create and open Due Diligence Media Room, add Overview and Review tabs, then add Getting Started's Video Library with Transcript, Getting Started's PDF Widget with URL.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Due Diligence Media Room" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Getting Started/get_video_with_transcript` → `missing_widget`
- **Widget** ≥1× `Getting Started/pdf_widget_url` → `missing_widget`

#### `due_diligence_media_room_level4`

**level4** · category: dashboard · specification: -

> Media-room governed layout: follow the Finance Tearsheet skill (finance-tearsheet); create and open Due Diligence Media Room, add Catalysts and Risks tabs, and add Getting Started's Video Library with Transcript, Widget Examples's URL PDF files.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Due Diligence Media Room" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `catalysts` must exist (matched by tab id) → `missing_tab`
- **Tab** `risks` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Getting Started/get_video_with_transcript` → `missing_widget`
- **Widget** ≥1× `Widget Examples/url_pdf` → `missing_widget`

#### `due_diligence_media_room_level5`

**level5** · category: platform · specification: -

> Media-room navigation build: add Wave Three Media Room with a Media Review Register table, publish and instantiate Media Room App on Media, then add Getting Started's PDF Widget with URL, Widget Examples's URL PDF files. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Tearsheet skill (finance-tearsheet) and add a Media-room Build Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Media Room/media_review_register` on tab `media` → `missing_widget`
- **Widget** ≥1× `Getting Started/pdf_widget_url` → `missing_widget`
- **Widget** ≥1× `Widget Examples/url_pdf` → `missing_widget`
- **Generated note** ≥1× named ~"Media-room Build Note" whose content mentions "catalysts" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `visualization_gallery_level0`

**level0** · category: dashboard · specification: -

> Visualization-gallery board start: create and open Visualization Gallery.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Visualization Gallery" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`

#### `visualization_gallery_level1`

**level1** · category: dashboard · specification: -

> Visualization-gallery tab setup: create and open Visualization Gallery, then add Overview and Review tabs.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Visualization Gallery" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`

#### `visualization_gallery_level2`

**level2** · category: dashboard · specification: -

> Visualization-gallery level-2 layout: create and open Visualization Gallery, add Overview and Review tabs, then add Getting Started's Chains TVL Highcharts.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Visualization Gallery" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Getting Started/chains_highchart` → `missing_widget`

#### `visualization_gallery_level3`

**level3** · category: dashboard · specification: -

> Visualization-gallery level-3 layout: create and open Visualization Gallery, add Overview and Review tabs, then add Getting Started's Chains TVL Highcharts, Getting Started's Vega-Lite Bar Demo.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Visualization Gallery" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Getting Started/chains_highchart` → `missing_widget`
- **Widget** ≥1× `Getting Started/vega_bar` → `missing_widget`

#### `visualization_gallery_level4`

**level4** · category: dashboard · specification: -

> Visualization-gallery governed layout: follow the Finance Comps skill (finance-comps); create and open Visualization Gallery, add Valuation Multiples and Outliers tabs, and add Getting Started's Chains TVL Highcharts, Widget Examples's Vega-Lite Scatter Demo.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Visualization Gallery" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `valuation-multiples` must exist (matched by tab id) → `missing_tab`
- **Tab** `outliers` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Getting Started/chains_highchart` → `missing_widget`
- **Widget** ≥1× `Widget Examples/vega_scatter_demo` → `missing_widget`

#### `visualization_gallery_level5`

**level5** · category: platform · specification: -

> Visualization-gallery navigation build: add Wave Three Visualization Gallery with a Visualization Review Register table, publish and instantiate Visualization Gallery App on Gallery, then add Getting Started's Vega-Lite Bar Demo, Widget Examples's Vega-Lite Scatter Demo. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Comps skill (finance-comps) and add a Visualization-gallery Build Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Visualization Gallery/visualization_review_register` on tab `gallery` → `missing_widget`
- **Widget** ≥1× `Getting Started/vega_bar` → `missing_widget`
- **Widget** ≥1× `Widget Examples/vega_scatter_demo` → `missing_widget`
- **Generated note** ≥1× named ~"Visualization-gallery Build Note" whose content mentions "valuation multiples" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### parameterize (24)

#### `client_intake_controls_level0`

**level0** · category: single-widget · specification: -

> Client-intake level-0 change: on the open Client Intake Controls board, set Financial Entry Form with client_first_name set to Maya, client_last_name set to Chen, risk_profile set to Moderate, add_record set to True and preserve the other views.

- Initial workspace: dashboard "Client Intake Controls"; 1 tab(s): review; 3 seeded widget(s): form_submit_widget({"client_first_name": "Alex", "client_last_name": "Rivera", "risk_profile": "Conservative", "add_record": false}), all_forms({"client_first_name": "Taylor", "client_last_name": "Morgan", "risk_profile": "Balanced", "add_record": false}), markdown_widget_with_text_input({"name": "Pending"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/form_submit_widget` with data_args ⊇ {"client_first_name": "Maya", "client_last_name": "Chen", "risk_profile": "Moderate", "add_record": true} → `missing_widget`

#### `client_intake_controls_level1`

**level1** · category: single-widget · specification: -

> Client-intake level-1 change: on the open Client Intake Controls board, set Financial Entry Form with client_first_name Maya, client_last_name Chen, risk_profile Moderate, add_record True and preserve the other views.

- Initial workspace: dashboard "Client Intake Controls"; 1 tab(s): review; 3 seeded widget(s): form_submit_widget({"client_first_name": "Alex", "client_last_name": "Rivera", "risk_profile": "Conservative", "add_record": false}), all_forms({"client_first_name": "Taylor", "client_last_name": "Morgan", "risk_profile": "Balanced", "add_record": false}), markdown_widget_with_text_input({"name": "Pending"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/form_submit_widget` with data_args ⊇ {"client_first_name": "Maya", "client_last_name": "Chen", "risk_profile": "Moderate", "add_record": true} → `missing_widget`

#### `client_intake_controls_level2`

**level2** · category: single-widget · specification: -

> Client-intake level-2 change: on the open Client Intake Controls board, set Entry Form with client_first_name Noah, client_last_name Patel, risk_profile Balanced, add_record True and preserve the other views.

- Initial workspace: dashboard "Client Intake Controls"; 1 tab(s): review; 3 seeded widget(s): form_submit_widget({"client_first_name": "Alex", "client_last_name": "Rivera", "risk_profile": "Conservative", "add_record": false}), all_forms({"client_first_name": "Taylor", "client_last_name": "Morgan", "risk_profile": "Balanced", "add_record": false}), markdown_widget_with_text_input({"name": "Pending"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/all_forms` with data_args ⊇ {"client_first_name": "Noah", "client_last_name": "Patel", "risk_profile": "Balanced", "add_record": true} → `missing_widget`

#### `client_intake_controls_level3`

**level3** · category: single-widget · specification: -

> Client-intake paired change: on the open Client Intake Controls board, set Entry Form with client_first_name Noah, client_last_name Patel, risk_profile Balanced, add_record True; set Markdown Widget with Text Input with name Intake Ready; preserve the first view.

- Initial workspace: dashboard "Client Intake Controls"; 1 tab(s): review; 3 seeded widget(s): form_submit_widget({"client_first_name": "Alex", "client_last_name": "Rivera", "risk_profile": "Conservative", "add_record": false}), all_forms({"client_first_name": "Taylor", "client_last_name": "Morgan", "risk_profile": "Balanced", "add_record": false}), markdown_widget_with_text_input({"name": "Pending"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/all_forms` with data_args ⊇ {"client_first_name": "Noah", "client_last_name": "Patel", "risk_profile": "Balanced", "add_record": true} → `missing_widget`
- **Widget** ≥1× `Getting Started/markdown_widget_with_text_input` with data_args ⊇ {"name": "Intake Ready"} → `missing_widget`

#### `client_intake_controls_level4`

**level4** · category: single-widget · specification: -

> Client-intake governed change: follow the Widget Parameters resource (openbb://workspace/specs/widget-parameters) on the open Client Intake Controls board, then set Financial Entry Form with client_first_name Maya, client_last_name Chen, risk_profile Moderate, add_record True and preserve the other views. The governing concepts are form, button.

- Initial workspace: dashboard "Client Intake Controls"; 1 tab(s): review; 3 seeded widget(s): form_submit_widget({"client_first_name": "Alex", "client_last_name": "Rivera", "risk_profile": "Conservative", "add_record": false}), all_forms({"client_first_name": "Taylor", "client_last_name": "Morgan", "risk_profile": "Balanced", "add_record": false}), markdown_widget_with_text_input({"name": "Pending"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/form_submit_widget` with data_args ⊇ {"client_first_name": "Maya", "client_last_name": "Chen", "risk_profile": "Moderate", "add_record": true} → `missing_widget`

#### `client_intake_controls_level5`

**level5** · category: platform · specification: -

> Client-intake build tuning: add a custom backend Wave Three Intake Tuning with a Intake Control Panel table carrying risk_profile and client_last_name params, publish and instantiate Intake Tuning App on Controls, then set the live Intake Control Panel to risk_profile Moderate, client_last_name Chen. Follow the widgets manifest specification. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Widget Parameters resource (openbb://workspace/specs/widget-parameters) and add a Client-intake Tuning Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Intake Tuning/intake_control_panel` with data_args ⊇ {"risk_profile": "Moderate", "client_last_name": "Chen"} on tab `controls` → `missing_widget`
- **Generated note** ≥1× named ~"Client-intake Tuning Note" whose content mentions "form" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `crypto_display_controls_level0`

**level0** · category: single-widget · specification: -

> Crypto-display level-0 change: on the open Crypto Display Controls board, set Binance OHLC with symbol set to ethusdt, interval set to 1m, exchange set to binancef and preserve the other views.

- Initial workspace: dashboard "Crypto Display Controls"; 1 tab(s): review; 3 seeded widget(s): html_binance_ohlc({"symbol": "BTCUSDT", "interval": "30m", "exchange": "BinanceUS"}), omni_sql_widget({"prompt": "SELECT * FROM DATA LIMIT 5"}), moving_parameters_example({"datePicker1": "$currentDate-1d", "textBox1": "Hello!", "TrueFalse": true, "daysPicker1": "1"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/html_binance_ohlc` with data_args ⊇ {"symbol": "ethusdt", "interval": "1m", "exchange": "binancef"} → `missing_widget`

#### `crypto_display_controls_level1`

**level1** · category: single-widget · specification: -

> Crypto-display level-1 change: on the open Crypto Display Controls board, set Binance OHLC with symbol ethusdt, interval 1m, exchange binancef and preserve the other views.

- Initial workspace: dashboard "Crypto Display Controls"; 1 tab(s): review; 3 seeded widget(s): html_binance_ohlc({"symbol": "BTCUSDT", "interval": "30m", "exchange": "BinanceUS"}), omni_sql_widget({"prompt": "SELECT * FROM DATA LIMIT 5"}), moving_parameters_example({"datePicker1": "$currentDate-1d", "textBox1": "Hello!", "TrueFalse": true, "daysPicker1": "1"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/html_binance_ohlc` with data_args ⊇ {"symbol": "ethusdt", "interval": "1m", "exchange": "binancef"} → `missing_widget`

#### `crypto_display_controls_level2`

**level2** · category: single-widget · specification: -

> Crypto-display level-2 change: on the open Crypto Display Controls board, set SQL Query Widget with prompt SELECT * FROM DATA LIMIT 3 and preserve the other views.

- Initial workspace: dashboard "Crypto Display Controls"; 1 tab(s): review; 3 seeded widget(s): html_binance_ohlc({"symbol": "BTCUSDT", "interval": "30m", "exchange": "BinanceUS"}), omni_sql_widget({"prompt": "SELECT * FROM DATA LIMIT 5"}), moving_parameters_example({"datePicker1": "$currentDate-1d", "textBox1": "Hello!", "TrueFalse": true, "daysPicker1": "1"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/omni_sql_widget` with data_args ⊇ {"prompt": "SELECT * FROM DATA LIMIT 3"} → `missing_widget`

#### `crypto_display_controls_level3`

**level3** · category: single-widget · specification: -

> Crypto-display paired change: on the open Crypto Display Controls board, set SQL Query Widget with prompt SELECT * FROM DATA LIMIT 3; set Moving Parameters Example with datePicker1 $currentDate-1d, textBox1 Ready, TrueFalse True, daysPicker1 1; preserve the first view.

- Initial workspace: dashboard "Crypto Display Controls"; 1 tab(s): review; 3 seeded widget(s): html_binance_ohlc({"symbol": "BTCUSDT", "interval": "30m", "exchange": "BinanceUS"}), omni_sql_widget({"prompt": "SELECT * FROM DATA LIMIT 5"}), moving_parameters_example({"datePicker1": "$currentDate-1d", "textBox1": "Hello!", "TrueFalse": true, "daysPicker1": "1"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/omni_sql_widget` with data_args ⊇ {"prompt": "SELECT * FROM DATA LIMIT 3"} → `missing_widget`
- **Widget** ≥1× `Widget Examples/moving_parameters_example` with data_args ⊇ {"datePicker1": "$currentDate-1d", "textBox1": "Ready", "TrueFalse": true, "daysPicker1": "1"} → `missing_widget`

#### `crypto_display_controls_level4`

**level4** · category: single-widget · specification: -

> Crypto-display governed change: follow the Daloopa Inflection skill (daloopa-inflection) on the open Crypto Display Controls board, then set SQL Query Widget with prompt SELECT * FROM DATA LIMIT 3 -- growth-rate reversals and preserve the other views. The governing concepts are growth-rate reversals.

- Initial workspace: dashboard "Crypto Display Controls"; 1 tab(s): review; 3 seeded widget(s): html_binance_ohlc({"symbol": "BTCUSDT", "interval": "30m", "exchange": "BinanceUS"}), omni_sql_widget({"prompt": "SELECT * FROM DATA LIMIT 5"}), moving_parameters_example({"datePicker1": "$currentDate-1d", "textBox1": "Hello!", "TrueFalse": true, "daysPicker1": "1"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/omni_sql_widget` with data_args ⊇ {"prompt": "SELECT * FROM DATA LIMIT 3 -- growth-rate reversals"} → `missing_widget`

#### `crypto_display_controls_level5`

**level5** · category: platform · specification: -

> Crypto-display build tuning: add a custom backend Wave Three Display Tuning with a Display Control Panel table carrying symbol and interval params, publish and instantiate Display Tuning App on Controls, then set the live Display Control Panel to symbol ethusdt, interval 1m. Follow the widgets manifest specification. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Daloopa Inflection skill (daloopa-inflection) and add a Crypto-display Tuning Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Display Tuning/display_control_panel` with data_args ⊇ {"symbol": "ethusdt", "interval": "1m"} on tab `controls` → `missing_widget`
- **Generated note** ≥1× named ~"Crypto-display Tuning Note" whose content mentions "growth-rate reversals" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `crypto_document_controls_level0`

**level0** · category: single-widget · specification: -

> On the open Crypto Document Controls board, set Whitepapers with filenames set to ethereum.pdf and category set to l1, preserving every other view.

- Initial workspace: dashboard "Crypto Document Controls"; 1 tab(s): review; 3 seeded widget(s): whitepapers({"filenames": "bitcoin.pdf", "category": "all"}), coindesk_news({"limit": 10, "lang": "EN"}), multi_pdf_base64({"pdf_name": "Bitcoin Whitepaper"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/whitepapers` with data_args ⊇ {"filenames": "ethereum.pdf", "category": "l1"} → `missing_widget`

#### `crypto_document_controls_level1`

**level1** · category: single-widget · specification: -

> Use the whitepaper PDF on the open Crypto Document Controls board to show Solana's solana.pdf from the l1 collection, leaving the rest alone.

- Initial workspace: dashboard "Crypto Document Controls"; 1 tab(s): review; 3 seeded widget(s): whitepapers({"filenames": "bitcoin.pdf", "category": "all"}), coindesk_news({"limit": 10, "lang": "EN"}), multi_pdf_base64({"pdf_name": "Bitcoin Whitepaper"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/whitepapers` with data_args ⊇ {"filenames": "solana.pdf", "category": "l1"} → `missing_widget`

#### `crypto_document_controls_level2`

**level2** · category: single-widget · specification: -

> Apply the DeFi research set to Whitepapers on the open Crypto Document Controls board and preserve the surrounding document views.

- Initial workspace: dashboard "Crypto Document Controls"; 1 tab(s): review; 3 seeded widget(s): whitepapers({"filenames": "bitcoin.pdf", "category": "all"}), coindesk_news({"limit": 10, "lang": "EN"}), multi_pdf_base64({"pdf_name": "Bitcoin Whitepaper"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/whitepapers` with data_args ⊇ {"filenames": "solana.pdf", "category": "defi"} → `missing_widget`

#### `crypto_document_controls_level3`

**level3** · category: single-widget · specification: -

> Retune Whitepapers on the open Crypto Document Controls board to ethereum.pdf from l1. Keep CoinDesk News and every other view unchanged.

- Initial workspace: dashboard "Crypto Document Controls"; 1 tab(s): review; 3 seeded widget(s): whitepapers({"filenames": "bitcoin.pdf", "category": "all"}), coindesk_news({"limit": 10, "lang": "EN"}), multi_pdf_base64({"pdf_name": "Bitcoin Whitepaper"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/whitepapers` with data_args ⊇ {"filenames": "ethereum.pdf", "category": "l1"} → `missing_widget`
- **Widget** ≥1× `Widget Examples/coindesk_news` → `missing_widget`

#### `crypto_document_controls_level4`

**level4** · category: single-widget · specification: -

> Using Workspace session guidance, prepare the open Crypto Document Controls board with Whitepapers on ethereum.pdf from l1 and CoinDesk News limited to 6 in ES. Preserve the PDF viewer.

- Initial workspace: dashboard "Crypto Document Controls"; 1 tab(s): review; 3 seeded widget(s): whitepapers({"filenames": "bitcoin.pdf", "category": "all"}), coindesk_news({"limit": 10, "lang": "EN"}), multi_pdf_base64({"pdf_name": "Bitcoin Whitepaper"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/whitepapers` with data_args ⊇ {"filenames": "ethereum.pdf", "category": "l1"} → `missing_widget`
- **Widget** ≥1× `Widget Examples/coindesk_news` with data_args ⊇ {"limit": 6, "lang": "ES"} → `missing_widget`

#### `crypto_document_controls_level5`

**level5** · category: platform · specification: -

> Document-controls build tuning: add a custom backend Wave Two Document Tuning with a Document Control Panel table carrying filenames and category params, publish and instantiate Document Tuning App on Controls, then set the live Document Control Panel to filenames solana.pdf, category l1. Follow the widgets manifest specification. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Tearsheet skill (finance-tearsheet) and add a Document-controls Tuning Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Two Document Tuning/document_control_panel` with data_args ⊇ {"filenames": "solana.pdf", "category": "l1"} on tab `controls` → `missing_widget`
- **Generated note** ≥1× named ~"Document-controls Tuning Note" whose content mentions "price action" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `technology_decision_inputs_level0`

**level0** · category: single-widget · specification: -

> On the open Technology Decision Inputs board, switch Car Manufacturer Performance with company set to TSLA and year set to 2023, and leave every other view unchanged.

- Initial workspace: dashboard "Technology Decision Inputs"; 1 tab(s): review; 3 seeded widget(s): company_performance({"company": "TM", "year": 2024}), earnings_estimates_monitor_calendar_upcoming_earnings({"sector": "Healthcare", "ticker": "LLY", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_performance` with data_args ⊇ {"company": "TSLA", "year": 2023} → `missing_widget`

#### `technology_decision_inputs_level1`

**level1** · category: single-widget · specification: -

> Look over the open Technology Decision Inputs board, then change Car Manufacturer Performance to TSLA and 2022 while preserving everything else.

- Initial workspace: dashboard "Technology Decision Inputs"; 1 tab(s): review; 3 seeded widget(s): company_performance({"company": "TM", "year": 2024}), earnings_estimates_monitor_calendar_upcoming_earnings({"sector": "Healthcare", "ticker": "LLY", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_performance` with data_args ⊇ {"company": "TSLA", "year": 2022} → `missing_widget`

#### `technology_decision_inputs_level2`

**level2** · category: single-widget · specification: -

> Apply the current Tesla model-year policy on the open Technology Decision Inputs board. Set Car Manufacturer Performance to company TSLA and year 2024, the current model year, and preserve the rest of the board.

- Initial workspace: dashboard "Technology Decision Inputs"; 1 tab(s): review; 3 seeded widget(s): company_performance({"company": "TM", "year": 2024}), earnings_estimates_monitor_calendar_upcoming_earnings({"sector": "Healthcare", "ticker": "LLY", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_performance` with data_args ⊇ {"company": "TSLA", "year": 2024} → `missing_widget`

#### `technology_decision_inputs_level3`

**level3** · category: single-widget · specification: -

> Retune Upcoming Earnings on the open Technology Decision Inputs board to Technology, AAPL, and QTD. Keep Car Manufacturer Performance and every other view as they are.

- Initial workspace: dashboard "Technology Decision Inputs"; 1 tab(s): review; 3 seeded widget(s): company_performance({"company": "TM", "year": 2024}), earnings_estimates_monitor_calendar_upcoming_earnings({"sector": "Healthcare", "ticker": "LLY", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_calendar_upcoming_earnings` with data_args ⊇ {"sector": "Technology", "ticker": "AAPL", "period": "QTD"} → `missing_widget`
- **Widget** ≥1× `Getting Started/company_performance` → `missing_widget`

#### `technology_decision_inputs_level4`

**level4** · category: single-widget · specification: -

> Prepare the open Technology Decision Inputs board for the quarterly review under Finance Earnings Prep governance. Set Upcoming Earnings to Technology, AAPL, and QTD, and Trade Ideas to Flagship Long/Short and QTD. Preserve Car Manufacturer Performance.

- Initial workspace: dashboard "Technology Decision Inputs"; 1 tab(s): review; 3 seeded widget(s): company_performance({"company": "TM", "year": 2024}), earnings_estimates_monitor_calendar_upcoming_earnings({"sector": "Healthcare", "ticker": "LLY", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_calendar_upcoming_earnings` with data_args ⊇ {"sector": "Technology", "ticker": "AAPL", "period": "QTD"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "QTD"} → `missing_widget`

#### `technology_decision_inputs_level5`

**level5** · category: platform · specification: -

> Decision-inputs build tuning: add a custom backend Wave One Decision Tuning with a Decision Input Panel table carrying company and period params, publish and instantiate Decision Tuning App on Controls, then set the live Decision Input Panel to company TSLA, period QTD. Follow the widgets manifest specification. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Earnings Prep skill (finance-earnings-prep) and add a Decision-inputs Tuning Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave One Decision Tuning/decision_input_panel` with data_args ⊇ {"company": "TSLA", "period": "QTD"} on tab `controls` → `missing_widget`
- **Generated note** ≥1× named ~"Decision-inputs Tuning Note" whose content mentions "internal estimates" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### platform (24)

#### `cited_research_operations_level0`

**level0** · category: platform · specification: -

> From the open Cited Research Operations board, read the Daloopa Tearsheet skill (daloopa-tearsheet). Add a Daloopa Tearsheet Workflow note that records the workflow title and its period-math anchor.

- Initial workspace: dashboard "Cited Research Operations"; 1 tab(s): research
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Daloopa Tearsheet Workflow" whose content mentions "Daloopa tearsheet workflow", "latest_calendar_quarter" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `cited_research_operations_level1`

**level1** · category: platform · specification: -

> On the open Cited Research Operations board, follow Daloopa Tearsheet governance and add Bench Daloopa's Company Directory.

- Initial workspace: dashboard "Cited Research Operations"; 1 tab(s): research
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` → `missing_widget`

#### `cited_research_operations_level2`

**level2** · category: platform · specification: -

> Use Daloopa Guidance Tracker governance on the open Cited Research Operations board and add Bench Daloopa's Management Guidance for NVDA.

- Initial workspace: dashboard "Cited Research Operations"; 1 tab(s): research
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Daloopa/daloopa_management_guidance` with data_args ⊇ {"ticker": "NVDA"} → `missing_widget`

#### `cited_research_operations_level3`

**level3** · category: dashboard · specification: -

> For the open Cited Research Operations board, use Daloopa Industry governance to place two Bench Daloopa Company Fundamentals views, one for MSFT in 2025Q4 and one for NVDA in 2025Q4.

- Initial workspace: dashboard "Cited Research Operations"; 1 tab(s): research
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q4"} → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "NVDA", "period": "2025Q4"} → `missing_widget`

#### `cited_research_operations_level4`

**level4** · category: dashboard · specification: -

> Combine Daloopa Capital Allocation governance with Workspace session guidance on the open Cited Research Operations board. Add Bench Daloopa's Company Fundamentals for AMZN in 2026Q1 and a Citation Protocol note naming source_url and calendar_period.

- Initial workspace: dashboard "Cited Research Operations"; 1 tab(s): research
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "AMZN", "period": "2026Q1"} → `missing_widget`
- **Generated note** ≥1× named ~"Citation Protocol" whose content mentions "source_url", "calendar_period" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `cited_research_operations_level5`

**level5** · category: platform · specification: -

> Following Daloopa Tearsheet governance, author and add a Cited Research Backend with a Citation Review Queue, then publish and instantiate a Cited Research App with a Research tab. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Cited Research Backend/citation_review_queue` on tab `research` → `missing_widget`

#### `comps_governance_level0`

**level0** · category: platform · specification: -

> Comps-governance level-0 workflow: read the Finance Comps skill (finance-comps) and add a Comps-governance Starter Note containing valuation multiples.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Comps-governance Starter Note" whose content mentions "valuation multiples" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `comps_governance_level1`

**level1** · category: platform · specification: -

> Comps-governance level-1 workflow: read the Finance Comps skill (finance-comps) and add a Comps-governance Discovery Note containing valuation multiples.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Comps-governance Discovery Note" whose content mentions "valuation multiples" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `comps_governance_level2`

**level2** · category: platform · specification: -

> Comps-governance governed placement: read the Finance Comps skill (finance-comps), then add Getting Started's Plotly Chart with Theme and Toolbar using Config File for valuation multiples.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/plotly_chart_with_theme_and_toolbar_using_config_file` → `missing_widget`

#### `comps_governance_level3`

**level3** · category: platform · specification: -

> Comps-governance paired workflow: read the Finance Comps skill (finance-comps), then add Getting Started's Plotly Chart with Theme and Toolbar using Config File, Widget Examples's Chains chart example Plotly with raw data to support valuation multiples.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/plotly_chart_with_theme_and_toolbar_using_config_file` → `missing_widget`
- **Widget** ≥1× `Widget Examples/chains_plotly` → `missing_widget`

#### `comps_governance_level4`

**level4** · category: platform · specification: -

> Comps-governance governed synthesis: follow the Finance Comps skill (finance-comps), add Getting Started's Plotly Chart with Theme and Toolbar using Config File, Widget Examples's Chains chart example Plotly with raw data, and add a Comps-governance Governed Note containing valuation multiples.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/plotly_chart_with_theme_and_toolbar_using_config_file` → `missing_widget`
- **Widget** ≥1× `Widget Examples/chains_plotly` → `missing_widget`
- **Generated note** ≥1× named ~"Comps-governance Governed Note" whose content mentions "valuation multiples" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `comps_governance_level5`

**level5** · category: platform · specification: -

> Comps-governance governed build: read the Finance Comps skill (finance-comps), add Wave Three Comps Governance with a Comps Governance Register table, publish and instantiate Comps Governance App on Comparables, and add a Comps-governance Build Note containing valuation multiples. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Comps Governance/comps_governance_register` on tab `comparables` → `missing_widget`
- **Generated note** ≥1× named ~"Comps-governance Build Note" whose content mentions "valuation multiples" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `governed_earnings_brief_level0`

**level0** · category: platform · specification: -

> Read the Finance Earnings Prep skill (finance-earnings-prep) for the open Governed Earnings Brief board. Add an Earnings Prep Workflow note that records the workflow title and its first and fourth actions.

- Initial workspace: dashboard "Governed Earnings Brief"; 1 tab(s): overview
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Earnings Prep Workflow" whose content mentions "Earnings prep workflow", "internal estimates", "transcript tone" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `governed_earnings_brief_level1`

**level1** · category: platform · specification: -

> On the open Governed Earnings Brief board, consult Finance Earnings Prep governance and add an Earnings Governance Actions note that names internal estimates and transcript tone.

- Initial workspace: dashboard "Governed Earnings Brief"; 1 tab(s): overview
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Earnings Governance Actions" whose content mentions "internal estimates", "transcript tone" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `governed_earnings_brief_level2`

**level2** · category: platform · specification: -

> Review the backend contract resource (openbb://workspace/contract/backend) for the open Governed Earnings Brief board, then add a Backend Contract Actions note recording the two contract items listed between the manifest files and authentication.

- Initial workspace: dashboard "Governed Earnings Brief"; 1 tab(s): overview
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Backend Contract Actions" whose content mentions "endpoints", "CORS" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `governed_earnings_brief_level3`

**level3** · category: dashboard · specification: -

> Use Workspace session guidance on the open Governed Earnings Brief board. Add an Actions tab and place a Session Grounding note there naming current-dashboard and current-tab.

- Initial workspace: dashboard "Governed Earnings Brief"; 1 tab(s): overview
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Session Grounding" whose content mentions "current-dashboard", "current-tab" on tab `actions` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `governed_earnings_brief_level4`

**level4** · category: dashboard · specification: -

> For the open Governed Earnings Brief board, combine Finance Earnings Prep governance with Workspace session guidance. Add an Actions tab and an Earnings Session Actions note there naming action items and current-dashboard.

- Initial workspace: dashboard "Governed Earnings Brief"; 1 tab(s): overview
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Earnings Session Actions" whose content mentions "action items", "current-dashboard" on tab `actions` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `governed_earnings_brief_level5`

**level5** · category: platform · specification: -

> The desk wants a Governed Earnings Backend with an Earnings Action Register. Following the build-an-app guide, author and add it, publish a Governed Earnings App with an Actions tab, and instantiate it. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Governed Earnings Backend/earnings_action_register` on tab `actions` → `missing_widget`

#### `investment_snapshot_governance_level0`

**level0** · category: platform · specification: -

> Investment-snapshot level-0 workflow: read the Finance Tearsheet skill (finance-tearsheet) and add a Investment-snapshot Starter Note containing price action.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Investment-snapshot Starter Note" whose content mentions "price action" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `investment_snapshot_governance_level1`

**level1** · category: platform · specification: -

> Investment-snapshot level-1 workflow: read the Finance Tearsheet skill (finance-tearsheet) and add a Investment-snapshot Discovery Note containing price action.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Investment-snapshot Discovery Note" whose content mentions "price action" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `investment_snapshot_governance_level2`

**level2** · category: platform · specification: -

> Investment-snapshot governed placement: read the Finance Tearsheet skill (finance-tearsheet), then add Getting Started's TradingView Chart for price action.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/udf` → `missing_widget`

#### `investment_snapshot_governance_level3`

**level3** · category: platform · specification: -

> Investment-snapshot paired workflow: read the Finance Tearsheet skill (finance-tearsheet), then add Getting Started's TradingView Chart, Getting Started's HTML Widget to support price action.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/udf` → `missing_widget`
- **Widget** ≥1× `Getting Started/html_widget` → `missing_widget`

#### `investment_snapshot_governance_level4`

**level4** · category: platform · specification: -

> Investment-snapshot governed synthesis: follow the Finance Tearsheet skill (finance-tearsheet), add Getting Started's TradingView Chart, Getting Started's HTML Widget, and add a Investment-snapshot Governed Note containing price action.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/udf` → `missing_widget`
- **Widget** ≥1× `Getting Started/html_widget` → `missing_widget`
- **Generated note** ≥1× named ~"Investment-snapshot Governed Note" whose content mentions "price action" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `investment_snapshot_governance_level5`

**level5** · category: platform · specification: -

> Investment-snapshot governed build: read the Finance Tearsheet skill (finance-tearsheet), add Wave Three Investment Snapshot with a Investment Snapshot Register table, publish and instantiate Investment Snapshot App on Snapshot, and add a Investment-snapshot Build Note containing price action. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Investment Snapshot/investment_snapshot_register` on tab `snapshot` → `missing_widget`
- **Generated note** ≥1× named ~"Investment-snapshot Build Note" whose content mentions "price action" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### repair (24)

#### `manufacturer_details_repair_level0`

**level0** · category: repair · specification: -

> Car Manufacturer Details on the open Manufacturer Detail Repair board has company set to F and year set to 2022. Set company to F and year back to 2024.

- Initial workspace: dashboard "Manufacturer Detail Repair"; 1 tab(s): details; 2 seeded widget(s): company_details({"company": "F", "year": 2022}), markdown_widget({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_details` with data_args ⊇ {"company": "F", "year": 2024} → `missing_widget`

#### `manufacturer_details_repair_level1`

**level1** · category: repair · specification: -

> On the open Manufacturer Detail Repair board, restore Car Manufacturer Details to company F and year 2024. Preserve Markdown Widget and every other workspace item.

- Initial workspace: dashboard "Manufacturer Detail Repair"; 1 tab(s): details; 2 seeded widget(s): company_details({"company": "F", "year": 2022}), markdown_widget({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_details` with data_args ⊇ {"company": "F", "year": 2024} → `missing_widget`
- **Widget** ≥1× `Getting Started/markdown_widget` → `missing_widget`

#### `manufacturer_details_repair_level2`

**level2** · category: repair · specification: -

> The open Manufacturer Detail Repair board has an extra Car Manufacturer Details copy. The manufacturer-duplicate marker identifies it; remove that copy so exactly one remains, and preserve Markdown Widget.

- Initial workspace: dashboard "Manufacturer Detail Repair"; 1 tab(s): details; 3 seeded widget(s): company_details({"company": "F", "year": 2024}), company_details({"company": "F", "year": 2024}), markdown_widget({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_details` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/markdown_widget` → `missing_widget`

#### `manufacturer_details_repair_level3`

**level3** · category: repair · specification: -

> Car Manufacturer Details overlaps Markdown Widget on the open Manufacturer Detail Repair board. Move Car Manufacturer Details to x 0, y 10, width 40, height 14 on Details while preserving its settings.

- Initial workspace: dashboard "Manufacturer Detail Repair"; 1 tab(s): details; 2 seeded widget(s): company_details({"company": "F", "year": 2024}), markdown_widget({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_details` → `missing_widget`
- **Widget** ≥1× `Getting Started/markdown_widget` → `missing_widget`

#### `manufacturer_details_repair_level4`

**level4** · category: repair · specification: -

> Clean up the open Manufacturer Detail Repair board. Restore the primary Car Manufacturer Details to F and 2024; the manufacturer-duplicate marker identifies the extra copy. Move the primary to x 0, y 10, width 40, height 14 on Details, and preserve Markdown Widget.

- Initial workspace: dashboard "Manufacturer Detail Repair"; 1 tab(s): details; 3 seeded widget(s): company_details({"company": "F", "year": 2022}), company_details({"company": "F", "year": 2022}), markdown_widget({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_details` with data_args ⊇ {"company": "F", "year": 2024} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/markdown_widget` → `missing_widget`

#### `manufacturer_details_repair_level5`

**level5** · category: repair · specification: -

> Detail-queue backend rebuild: Wave Two Detail Repair was lost from the workspace; on the open Custom Detail Repair board, rebuild it from scratch: add a custom backend Wave Two Detail Repair with a Manufacturer Detail Queue table, publish Detail Repair App, and instantiate it with one non-overlapping Manufacturer Detail Queue placement on Details, keeping all other workspace content. Follow the widgets manifest specification. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Daloopa Industry skill (daloopa-industry) and add a Detail-queue Rebuild Note recording its governing concept.

- Initial workspace: dashboard "Custom Detail Repair"; 1 tab(s): details
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Two Detail Repair/manufacturer_detail_queue` on tab `details` → `missing_widget`
- **Generated note** ≥1× named ~"Detail-queue Rebuild Note" whose content mentions "peers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `nav_exception_station_level0`

**level0** · category: repair · specification: -

> NAV Exceptions on the open NAV Repair Staging board has fund set to Flagship Long/Short, status set to Open, and period set to QTD. Set fund to Flagship Long/Short, status to Open, and period back to YTD.

- Initial workspace: dashboard "NAV Repair Staging"; 1 tab(s): exceptions; 2 seeded widget(s): fund_operations_control_tower_pricing_nav_exceptions({"fund": "Flagship Long/Short", "status": "Open", "period": "QTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_pricing_nav_exceptions` with data_args ⊇ {"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"} → `missing_widget`

#### `nav_exception_station_level1`

**level1** · category: repair · specification: -

> On the open NAV Repair Staging board, fix the NAV Exceptions setting by restoring Flagship Long/Short, Open, and YTD. Preserve Trade Ideas and every other workspace item.

- Initial workspace: dashboard "NAV Repair Staging"; 1 tab(s): exceptions; 2 seeded widget(s): fund_operations_control_tower_pricing_nav_exceptions({"fund": "Flagship Long/Short", "status": "Closed", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_pricing_nav_exceptions` with data_args ⊇ {"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` → `missing_widget`

#### `nav_exception_station_level2`

**level2** · category: repair · specification: -

> The open NAV Repair Staging board has an extra NAV Exceptions copy. The duplicate-cleanup marker identifies it; remove that copy so exactly one remains, and preserve Trade Ideas and all other content.

- Initial workspace: dashboard "NAV Repair Staging"; 1 tab(s): exceptions; 3 seeded widget(s): fund_operations_control_tower_pricing_nav_exceptions({"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"}), fund_operations_control_tower_pricing_nav_exceptions({"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_pricing_nav_exceptions` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` → `missing_widget`

#### `nav_exception_station_level3`

**level3** · category: repair · specification: -

> Fix the overlap on the open NAV Repair Staging board without disturbing Trade Ideas. Move NAV Exceptions to x 0, y 14, width 40, and height 14 on Exceptions, preserving all parameters and remaining workspace content.

- Initial workspace: dashboard "NAV Repair Staging"; 1 tab(s): exceptions; 2 seeded widget(s): fund_operations_control_tower_pricing_nav_exceptions({"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_pricing_nav_exceptions` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` → `missing_widget`

#### `nav_exception_station_level4`

**level4** · category: repair · specification: -

> Clean up the open NAV Repair Staging board. Restore the primary NAV Exceptions view to Flagship Long/Short, Open, and YTD; the duplicate-cleanup marker identifies the extra copy. Move the primary to x 0, y 14, width 40, height 14 on Exceptions, and preserve Trade Ideas.

- Initial workspace: dashboard "NAV Repair Staging"; 1 tab(s): exceptions; 3 seeded widget(s): fund_operations_control_tower_pricing_nav_exceptions({"fund": "Flagship Long/Short", "status": "Closed", "period": "YTD"}), fund_operations_control_tower_pricing_nav_exceptions({"fund": "Flagship Long/Short", "status": "Closed", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_pricing_nav_exceptions` with data_args ⊇ {"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` → `missing_widget`

#### `nav_exception_station_level5`

**level5** · category: repair · specification: -

> NAV-exception backend rebuild: Wave One NAV Repair was lost from the workspace; on the open Custom NAV Repair Staging board, rebuild it from scratch: add a custom backend Wave One NAV Repair with a NAV Exception Queue table, publish NAV Repair App, and instantiate it with one non-overlapping NAV Exception Queue placement on Exceptions, keeping all other workspace content. Follow the widgets manifest specification. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Daloopa Guidance Tracker skill (daloopa-guidance-tracker) and add a NAV-exception Rebuild Note recording its governing concept.

- Initial workspace: dashboard "Custom NAV Repair Staging"; 1 tab(s): exceptions
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave One NAV Repair/nav_exception_queue` on tab `exceptions` → `missing_widget`
- **Generated note** ≥1× named ~"NAV-exception Rebuild Note" whose content mentions "Missed" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `protocol_display_repair_level0`

**level0** · category: repair · specification: -

> Protocol-display direct fix: on the open Protocol Display Repair board, set Defi Llama Protocol Details with protocol_id set to uniswap.

- Initial workspace: dashboard "Protocol Display Repair"; 1 tab(s): review; 2 seeded widget(s): defi_llama_protocol_details({"protocol_id": "aave"}), demo_data_ssrm({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/defi_llama_protocol_details` with data_args ⊇ {"protocol_id": "uniswap"} → `missing_widget`

#### `protocol_display_repair_level1`

**level1** · category: repair · specification: -

> Protocol-display preserved fix: on the open Protocol Display Repair board, restore Defi Llama Protocol Details with protocol_id uniswap and preserve Demo Financial Data (SSRM).

- Initial workspace: dashboard "Protocol Display Repair"; 1 tab(s): review; 2 seeded widget(s): defi_llama_protocol_details({"protocol_id": "aave"}), demo_data_ssrm({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/defi_llama_protocol_details` with data_args ⊇ {"protocol_id": "uniswap"} → `missing_widget`
- **Widget** ≥1× `Widget Examples/demo_data_ssrm` → `missing_widget`

#### `protocol_display_repair_level2`

**level2** · category: repair · specification: -

> Protocol-display duplicate cleanup: the open Protocol Display Repair board has an extra Defi Llama Protocol Details; the protocol-display duplicate marker identifies it. Remove that copy and preserve Demo Financial Data (SSRM).

- Initial workspace: dashboard "Protocol Display Repair"; 1 tab(s): review; 3 seeded widget(s): defi_llama_protocol_details({"protocol_id": "uniswap"}), demo_data_ssrm({}), defi_llama_protocol_details({"protocol_id": "uniswap"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/defi_llama_protocol_details` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Widget Examples/demo_data_ssrm` → `missing_widget`

#### `protocol_display_repair_level3`

**level3** · category: repair · specification: -

> Protocol-display overlap fix: on the open Protocol Display Repair board, move Demo Financial Data (SSRM) to x 0, y 12, width 40, height 12 on Review; preserve Defi Llama Protocol Details.

- Initial workspace: dashboard "Protocol Display Repair"; 1 tab(s): review; 2 seeded widget(s): defi_llama_protocol_details({"protocol_id": "uniswap"}), demo_data_ssrm({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/defi_llama_protocol_details` → `missing_widget`
- **Widget** ≥1× `Widget Examples/demo_data_ssrm` → `missing_widget`

#### `protocol_display_repair_level4`

**level4** · category: repair · specification: -

> Protocol-display governed repair: follow the Daloopa Inflection skill (daloopa-inflection) on the open Protocol Display Repair board, restore Defi Llama Protocol Details with protocol_id uniswap, preserve Demo Financial Data (SSRM), and add a Protocol-display Governance Note naming growth-rate reversals.

- Initial workspace: dashboard "Protocol Display Repair"; 1 tab(s): review; 2 seeded widget(s): defi_llama_protocol_details({"protocol_id": "aave"}), demo_data_ssrm({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/defi_llama_protocol_details` with data_args ⊇ {"protocol_id": "uniswap"} → `missing_widget`
- **Widget** ≥1× `Widget Examples/demo_data_ssrm` → `missing_widget`
- **Generated note** ≥1× named ~"Protocol-display Governance Note" whose content mentions "growth-rate reversals" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `protocol_display_repair_level5`

**level5** · category: repair · specification: -

> Protocol-display backend rebuild: Wave Three Protocol Repair was lost from the workspace; on the open Protocol-display Backend Repair board, rebuild it from scratch: add a custom backend Wave Three Protocol Repair with a Protocol Repair Queue table, publish Protocol Repair App, and instantiate it with one non-overlapping Protocol Repair Queue placement on Protocols, keeping all other workspace content. Follow the widgets manifest specification. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Daloopa Inflection skill (daloopa-inflection) and add a Protocol-display Rebuild Note recording its governing concept.

- Initial workspace: dashboard "Protocol-display Backend Repair"; 1 tab(s): protocols
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Protocol Repair/protocol_repair_queue` on tab `protocols` → `missing_widget`
- **Generated note** ≥1× named ~"Protocol-display Rebuild Note" whose content mentions "growth-rate reversals" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_freshness_repair_level0`

**level0** · category: repair · specification: -

> Vendor-freshness direct fix: on the open Vendor Freshness Repair board, set SLA Metrics with vendor set to Bloomberg, status set to Open, period set to QTD.

- Initial workspace: dashboard "Vendor Freshness Repair"; 1 tab(s): review; 2 seeded widget(s): vendor_dataset_monitor_vendors_sla_metrics({"vendor": "FactSet", "status": "Closed", "period": "1Y"}), vendor_dataset_monitor_vendors_vendor_contract_terms({"vendor": "FactSet", "status": "Open", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_sla_metrics` with data_args ⊇ {"vendor": "Bloomberg", "status": "Open", "period": "QTD"} → `missing_widget`

#### `vendor_freshness_repair_level1`

**level1** · category: repair · specification: -

> Vendor-freshness preserved fix: on the open Vendor Freshness Repair board, restore SLA Metrics with vendor Bloomberg, status Open, period QTD and preserve Vendor Contract Terms.

- Initial workspace: dashboard "Vendor Freshness Repair"; 1 tab(s): review; 2 seeded widget(s): vendor_dataset_monitor_vendors_sla_metrics({"vendor": "FactSet", "status": "Closed", "period": "1Y"}), vendor_dataset_monitor_vendors_vendor_contract_terms({"vendor": "FactSet", "status": "Open", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_sla_metrics` with data_args ⊇ {"vendor": "Bloomberg", "status": "Open", "period": "QTD"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_vendor_contract_terms` → `missing_widget`

#### `vendor_freshness_repair_level2`

**level2** · category: repair · specification: -

> Vendor-freshness duplicate cleanup: the open Vendor Freshness Repair board has an extra SLA Metrics; the vendor-freshness duplicate marker identifies it. Remove that copy and preserve Vendor Contract Terms.

- Initial workspace: dashboard "Vendor Freshness Repair"; 1 tab(s): review; 3 seeded widget(s): vendor_dataset_monitor_vendors_sla_metrics({"vendor": "Bloomberg", "status": "Open", "period": "QTD"}), vendor_dataset_monitor_vendors_vendor_contract_terms({"vendor": "FactSet", "status": "Open", "period": "YTD"}), vendor_dataset_monitor_vendors_sla_metrics({"vendor": "Bloomberg", "status": "Open", "period": "QTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_sla_metrics` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_vendor_contract_terms` → `missing_widget`

#### `vendor_freshness_repair_level3`

**level3** · category: repair · specification: -

> Vendor-freshness overlap fix: on the open Vendor Freshness Repair board, move Vendor Contract Terms to x 0, y 12, width 40, height 12 on Review; preserve SLA Metrics.

- Initial workspace: dashboard "Vendor Freshness Repair"; 1 tab(s): review; 2 seeded widget(s): vendor_dataset_monitor_vendors_sla_metrics({"vendor": "Bloomberg", "status": "Open", "period": "QTD"}), vendor_dataset_monitor_vendors_vendor_contract_terms({"vendor": "FactSet", "status": "Open", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_sla_metrics` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_vendor_contract_terms` → `missing_widget`

#### `vendor_freshness_repair_level4`

**level4** · category: repair · specification: -

> Vendor-freshness governed repair: follow the Finance Guidance Tracker skill (finance-guidance-tracker) on the open Vendor Freshness Repair board, restore SLA Metrics with vendor Bloomberg, status Open, period QTD, preserve Vendor Contract Terms, and add a Vendor-freshness Governance Note naming evidence gaps.

- Initial workspace: dashboard "Vendor Freshness Repair"; 1 tab(s): review; 2 seeded widget(s): vendor_dataset_monitor_vendors_sla_metrics({"vendor": "FactSet", "status": "Closed", "period": "1Y"}), vendor_dataset_monitor_vendors_vendor_contract_terms({"vendor": "FactSet", "status": "Open", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_sla_metrics` with data_args ⊇ {"vendor": "Bloomberg", "status": "Open", "period": "QTD"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_vendor_contract_terms` → `missing_widget`
- **Generated note** ≥1× named ~"Vendor-freshness Governance Note" whose content mentions "evidence gaps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_freshness_repair_level5`

**level5** · category: repair · specification: -

> Vendor-freshness backend rebuild: Wave Three Vendor Repair was lost from the workspace; on the open Vendor-freshness Backend Repair board, rebuild it from scratch: add a custom backend Wave Three Vendor Repair with a Vendor Repair Queue table, publish Vendor Repair App, and instantiate it with one non-overlapping Vendor Repair Queue placement on Incidents, keeping all other workspace content. Follow the widgets manifest specification. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Guidance Tracker skill (finance-guidance-tracker) and add a Vendor-freshness Rebuild Note recording its governing concept.

- Initial workspace: dashboard "Vendor-freshness Backend Repair"; 1 tab(s): incidents
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Vendor Repair/vendor_repair_queue` on tab `incidents` → `missing_widget`
- **Generated note** ≥1× named ~"Vendor-freshness Rebuild Note" whose content mentions "evidence gaps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### retrieve (24)

#### `closing_tape_lookup_level0`

**level0** · category: read · specification: -

> Read the daily OHLCV rows in Bench Daloopa's Stock Prices with ticker set to NVDA, then report the latest date and exact close.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `closing_tape_lookup_level1`

**level1** · category: read · specification: -

> Find the daily OHLCV rows in Bench Daloopa's Stock Prices for Netflix and give me the latest date and exact close.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `closing_tape_lookup_level2`

**level2** · category: read · specification: -

> Pull the latest date and exact close from the daily OHLCV rows in Bench Daloopa's Stock Prices for the EV tape policy; that policy means the Tesla coverage name.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `closing_tape_lookup_level3`

**level3** · category: read · specification: -

> On the open Closing Tape Review board, read the daily OHLCV rows in Bench Daloopa's configured Stock Prices view without changing it and report the latest date, exact close, and volume.

- Initial workspace: dashboard "Closing Tape Review"; 1 tab(s): review; 1 seeded widget(s): daloopa_stock_prices({"ticker": "MSFT"})
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `closing_tape_lookup_level4`

**level4** · category: read · specification: -

> Use Daloopa Tearsheet governance to review the daily OHLCV rows in Bench Daloopa's Stock Prices for Apple, then report the latest date and exact close.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `closing_tape_lookup_level5`

**level5** · category: platform · specification: -

> Build and add a Wave Two Closing Tape backend with a Closing Tape Lookup table for NVDA, instantiate its Closing Tape App, read the result, and report the latest date and exact close. Follow the widgets manifest specification. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Daloopa Tearsheet skill (daloopa-tearsheet) and add a Closing Tape Build Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Two Closing Tape/closing_tape_lookup` with data_args ⊇ {"ticker": "NVDA"} on tab `tape` → `missing_widget`
- **Generated note** ≥1× named ~"Closing Tape Build Note" whose content mentions "latest_calendar_quarter" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_lookup_level0`

**level0** · category: read · specification: -

> Read Upcoming Earnings in Bench Stark Enterprise's Earnings & Estimates Monitor for Healthcare, LLY, and YTD, and report the exact score and status.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_lookup_level1`

**level1** · category: read · specification: -

> Find Upcoming Earnings in Bench Stark Enterprise's Earnings & Estimates Monitor, set the view to Technology, AAPL, and QTD, and give me the exact score and status.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_lookup_level2`

**level2** · category: read · specification: -

> I need MSFT's exact score and status from Upcoming Earnings in Bench Stark Enterprise's Earnings & Estimates Monitor. Use Technology for the coverage sector; the current-month policy means MTD.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_lookup_level3`

**level3** · category: read · specification: -

> On the open Earnings & Estimates Monitor board, read Bench Stark Enterprise's configured Upcoming Earnings view without changing it, and report LLY's exact YTD score and change.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Earnings & Estimates Monitor"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_lookup_level4`

**level4** · category: read · specification: -

> Review Apple's earnings under Finance Earnings Prep governance. In Bench Stark Enterprise's Earnings & Estimates Monitor, use Upcoming Earnings for Technology, AAPL, and QTD, then report the exact score and status.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_lookup_level5`

**level5** · category: platform · specification: -

> The desk needs a Wave One Earnings Lookup backend with an Earnings Status Lookup table for LLY and YTD. Build and add it, instantiate its Earnings Lookup App, read the lookup, and report the exact score and status. Follow the widgets manifest specification. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Earnings Prep skill (finance-earnings-prep) and add a Earnings Lookup Build Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave One Earnings Lookup/earnings_status_lookup` with data_args ⊇ {"ticker": "LLY", "period": "YTD"} on tab `lookup` → `missing_widget`
- **Generated note** ≥1× named ~"Earnings Lookup Build Note" whose content mentions "surprise drivers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `live_quote_lookup_level0`

**level0** · category: read · specification: -

> Live-quote morning request: read Widget Examples's Live Grid with symbol AAPL, then report the exact symbol and price shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `live_quote_lookup_level1`

**level1** · category: read · specification: -

> Live-quote discovery request: read Widget Examples's Live Grid with symbol AAPL, then report the exact symbol and price shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `live_quote_lookup_level2`

**level2** · category: read · specification: -

> Live-quote analyst request: read Widget Examples's Live Grid with symbol AAPL, then report the exact symbol and price shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `live_quote_lookup_level3`

**level3** · category: read · specification: -

> Live-quote desk request: read Widget Examples's Live Grid with symbol AAPL, then report the exact symbol and price shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `live_quote_lookup_level4`

**level4** · category: read · specification: -

> Live-quote governed request: follow the Finance Tearsheet skill (finance-tearsheet), read Widget Examples's Live Grid with symbol AAPL, report the exact symbol and price shown, and add a Live-quote Governance Note that records price action.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Live-quote Governance Note" whose content mentions "price action" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `live_quote_lookup_level5`

**level5** · category: platform · specification: -

> Live-quote build request: add Wave Three Live Quote with a Live Quote Lookup table, carrying symbol and last_price columns; publish and instantiate Live Quote App on Quotes, read it with symbol AAPL, and report the exact symbol and last_price values shown. Follow the widgets manifest specification. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Finance Tearsheet skill (finance-tearsheet) and add a Live-quote Build Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Live Quote/live_quote_lookup` with data_args ⊇ {"symbol": "AAPL"} on tab `quotes` → `missing_widget`
- **Generated note** ≥1× named ~"Live-quote Build Note" whose content mentions "price action" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `operating_driver_lookup_level0`

**level0** · category: read · specification: -

> Operating-driver morning request: read Bench Daloopa's Operating KPIs with ticker AAPL, period 2026Q1, then report the exact calendar_period and Installed Base Active Devices value shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `operating_driver_lookup_level1`

**level1** · category: read · specification: -

> Operating-driver discovery request: read Bench Daloopa's Operating KPIs with ticker AAPL, period 2026Q1, then report the exact calendar_period and Installed Base Active Devices value shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `operating_driver_lookup_level2`

**level2** · category: read · specification: -

> Operating-driver analyst request: read Bench Daloopa's Operating KPIs with ticker AAPL, period 2026Q1, then report the exact calendar_period and Installed Base Active Devices value shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `operating_driver_lookup_level3`

**level3** · category: read · specification: -

> Operating-driver desk request: read Bench Daloopa's Operating KPIs with ticker AAPL, period 2026Q1, then report the exact calendar_period and Installed Base Active Devices value shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `operating_driver_lookup_level4`

**level4** · category: read · specification: -

> Operating-driver governed request: follow the Daloopa Inflection skill (daloopa-inflection), read Bench Daloopa's Operating KPIs with ticker AAPL, period 2026Q1, report the exact calendar_period and Installed Base Active Devices value shown, and add a Operating-driver Governance Note that records growth-rate reversals.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Operating-driver Governance Note" whose content mentions "growth-rate reversals" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `operating_driver_lookup_level5`

**level5** · category: platform · specification: -

> Operating-driver build request: add Wave Three Operating Drivers with a Operating Driver Lookup table, carrying fiscal_period and driver_value columns; publish and instantiate Operating Driver App on Drivers, read it with ticker AAPL, period 2026Q1, and report the exact fiscal_period and driver_value values shown. Follow the widgets manifest specification. Widget ids are the snake_case of widget names; tab ids are the snake_case of tab names. Follow the Daloopa Inflection skill (daloopa-inflection) and add a Operating-driver Build Note recording its governing concept.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Wave Three Operating Drivers/operating_driver_lookup` with data_args ⊇ {"ticker": "AAPL", "period": "2026Q1"} on tab `drivers` → `missing_widget`
- **Generated note** ≥1× named ~"Operating-driver Build Note" whose content mentions "growth-rate reversals" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`


## Suite: build-openbb-apps (236 tasks)

### advanced (20)

#### `case_prompt_omni`

**hard** · category: platform · specification: partially-specified

> Create a usable cases and compliance alerts workflow for a surveillance analyst. The workspace must cover hidden-prompt question answering over case evidence. The source contract must retain `prompt`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `case_qa_omni`

**medium** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Surveillance Data' at http://localhost:7807. Implement the live or advanced interaction correctly. The experience needs Case Q&A (`case_qa_omni`, omni) using `/case-qa` for ask questions over the surveillance case corpus; user controls: Prompt (`prompt`, text). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Surveillance Data/case_qa_omni` → `missing_widget`

#### `case_qa_omni_app`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for cases and compliance alerts. The workspace must cover ask questions over the surveillance case corpus. Leave the complete working workspace open for review. Use `prompt` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `case_qa_omni_ship`

**hard** · category: platform · specification: -

> Build a surveillance analyst a dependable cases and compliance alerts workspace. The workspace must cover ask questions over the surveillance case corpus. The workspace must cover open surveillance alerts. The workspace must cover open alert count. Analysts need to inspect alert ID, desk, severity, age days. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Surveillance QA', 'case QA', 'Surveillance Data', 'Show high severity cases'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Surveillance QA", "case QA", "Surveillance Data", "Show high severity cases" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `case_room_omni_room`

**hard** · category: platform · specification: -

> The desk needs a production-ready cases and compliance alerts workflow for a surveillance analyst. The workspace must cover question answering over surveillance cases. The workspace must cover open surveillance alerts. The workspace must cover open alert count. Analysts need to inspect alert ID, desk, severity, age days. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `live_orders_grid`

**easy** · category: platform · specification: -

> Connect the backend and make its first widget usable on the current dashboard. Use 'Execution Desk Data' at http://localhost:7806. Implement the live or advanced interaction correctly. The experience needs Live Orders Grid (`live_orders_grid`, live_grid) using `/live-orders` for streaming order blotter over websocket; stream updates from `live-orders-ws`; stream row id `order_id`; columns: order_id (text), px (number, showCellChange). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Execution Desk Data/live_orders_grid` → `missing_widget`

#### `live_orders_grid_app`

**medium** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Execution Desk Data' at http://localhost:7806. Implement the live or advanced interaction correctly. The experience needs Live Orders Grid (`live_orders_grid`, live_grid) using `/live-orders` for streaming order blotter over websocket; stream updates from `live-orders-ws`; stream row id `order_id`; columns: order_id (text), px (number, showCellChange). Organize it as app 'Live Order Tape' with tabs Orders (live_orders_grid). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Live Order Tape" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Execution Desk Data/live_orders_grid` on tab `orders` → `missing_widget`

#### `live_orders_grid_ship`

**hard** · category: platform · specification: -

> Build an execution analyst a dependable orders and venue quality workspace. The workspace must cover live order activity. The workspace must cover open execution exceptions. The workspace must cover live open orders blotter. Analysts need to inspect order ID, price, symbol, quantity, status. Large result sets must stay responsive while analysts filter and page through them. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Execution Live Grid', 'live stream', 'Execution Desk Data', 'EDGX'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Execution Live Grid", "live stream", "Execution Desk Data", "EDGX" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `macro_advanced_chart_room`

**hard** · category: platform · specification: -

> Build a rates strategist a dependable rates and Treasury markets workspace. The workspace must cover market history for treasury futures. The workspace must cover the Treasury yield curve. The workspace must cover current 2s10s spread in bps. Leave the complete working workspace open for review. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `orders_ops_stream_room`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for orders and venue quality. The workspace must cover streaming order tape for the ops room. The workspace must cover open execution exceptions. Analysts need to inspect order ID, price. Large result sets must stay responsive while analysts filter and page through them. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use `venue_scope` and `order_id` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `orders_stream`

**hard** · category: platform · specification: partially-specified

> Create a usable orders and venue quality workflow for an execution analyst. The workspace must cover streaming orders with a stable row id. Analysts need to inspect order ID, price. Large result sets must stay responsive while analysts filter and page through them. The source contract must retain `venue` and `order_id`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `rates_advanced_chart`

**medium** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Rates Watch Data' at http://localhost:7803. Implement the live or advanced interaction correctly. The experience needs Rates Advanced Chart (`rates_advanced_chart`, advanced_charting) using `/rates-udf` for tradingView advanced charting for the 10Y yield future; default symbol `US10Y`; update frequency `30000`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Rates Watch Data/rates_advanced_chart` → `missing_widget`

#### `rates_advanced_chart_app`

**hard** · category: platform · specification: partially-specified

> Create a usable rates and Treasury markets workflow for a rates strategist. The workspace must cover market history for the 10Y yield future. Leave the complete working workspace open for review. The source contract must retain `Rates Watch Data`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `rates_live_chart_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover market history for treasury futures. The workspace must cover the Treasury yield curve. The workspace must cover current 2s10s spread in bps. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Rates Advanced Live', 'Treasury futures', 'Rates Watch Data', 'ZB'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Rates Advanced Live", "Treasury futures", "Rates Watch Data", "ZB" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `rates_symbol_chart`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a rates strategist covering rates and Treasury markets. The workspace must cover tradingView analysis with a selectable symbol. An analyst can filter the analysis by ticker. Keep these source-contract anchors: `symbol`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vix_advanced`

**medium** · category: platform · specification: explicit

> Make the requested backend widget available and working in the current view. Use 'Vol Desk Data' at http://localhost:7801. Implement the live or advanced interaction correctly. The experience needs VIX Advanced Chart (`vix_advanced`, advanced_charting) using `/udf` for tradingView advanced charting for VIX futures; default symbol `VIX`; update frequency `60000`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vol Desk Data/vix_advanced` → `missing_widget`

#### `vix_advanced_app`

**easy** · category: platform · specification: -

> Publish the requested app and open it in Workspace to verify it works. Use 'Vol Desk Data' at http://localhost:7801. Implement the live or advanced interaction correctly. The experience needs VIX Advanced Chart (`vix_advanced`, advanced_charting) using `/udf` for tradingView advanced charting for VIX futures; default symbol `VIX`; update frequency `60000`. Organize it as app 'Vol Advanced' with tabs Chart (vix_advanced). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vol Advanced" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Vol Desk Data/vix_advanced` on tab `chart` → `missing_widget`

#### `vix_advanced_ship`

**hard** · category: platform · specification: -

> Build a volatility analyst a dependable volatility and derivatives workspace. The workspace must cover market history for VIX futures. The workspace must cover current volatility regime score. The workspace must cover daily CBOE VIX closes with returns. Analysts need to inspect date, close, return percentage. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Vol Advanced Live', 'VIX futures', 'Vol Desk Data', 'VX2', 'ticker'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Vol Advanced Live", "VIX futures", "Vol Desk Data", "VX2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `vix_room_chart_room`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for volatility and derivatives. The workspace must cover market history for VIX futures. The workspace must cover daily CBOE VIX closes with returns. Analysts need to inspect date, close, return percentage. An analyst can adjust the relevant numeric scope. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use `window_days` and `window` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vol_symbol_chart`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a volatility analyst covering volatility and derivatives. The workspace must cover market history for volatility futures. Keep these source-contract anchors: `venue`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### aggrid (20)

#### `alert_queue_app`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for cases and compliance alerts. The workspace must cover open surveillance alerts. Analysts need to inspect alert ID, desk, severity, age days. Leave the complete working workspace open for review. Use `severity` and `alert_id` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `auction_calendar`

**medium** · category: platform · specification: explicit

> Make the requested backend widget available and working in the current view. Use 'Rates Watch Data' at http://localhost:7803. Make the data grid behavior and columns usable. The experience needs Auction Calendar (`auction_calendar`, table) using `/auction-calendar` for upcoming treasury auctions; columns: date (dateString), security (text), size_bn (number). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Rates Watch Data/auction_calendar` → `missing_widget`

#### `auction_watch`

**hard** · category: platform · specification: partially-specified

> Create a usable rates and Treasury markets workflow for a rates strategist. The workspace must cover upcoming treasury auctions. Analysts need to inspect auction date, security, size billions, bid to cover. The source contract must retain `auction_date` and `security`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `case_aging`

**hard** · category: platform · specification: -

> The desk needs a production-ready cases and compliance alerts workflow for a surveillance analyst. The workspace must cover open surveillance cases by age bucket. The workspace must cover open surveillance alerts. The workspace must cover open alert count. Analysts need to inspect case ID, desk, age days, alert ID, severity. Leave the complete working workspace open for review. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `chain_flows`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a digital-assets analyst covering chain activity and liquidity. The workspace must cover net flows by chain. The workspace must cover current gas price snapshot. Analysts need to inspect chain, inflow USD, outflow USD, net percentage. Leave the complete working workspace open for review. Keep these source-contract anchors: `chain` and `inflow_usd`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `chains_table_app`

**medium** · category: platform · specification: explicit

> Publish the requested app and open it in Workspace to verify it works. Use 'Chain TVL Data' at http://localhost:7802. Make the data grid behavior and columns usable. The experience needs Top Chains by TVL (`chains_table`, table) using `/chains-table` for current TVL of all chains from the desk aggregator; columns: name (text), tvl_usd (number, int), change_1d (number, percent, greenRed). Organize it as app 'Chains Board' with tabs Overview (chains_table). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Chains Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Chain TVL Data/chains_table` on tab `overview` → `missing_widget`

#### `earnings_ship`

**hard** · category: platform · specification: -

> An equity-research analyst needs a decision-ready Workspace for earnings and estimates. The workspace must cover beat/miss by ticker this season. The workspace must cover average EPS surprise last 4 quarters. The workspace must cover preview note for the earnings call. Analysts need to inspect ticker, EPS surprise percentage, revenue beat. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Season Tracker', 'season', 'Earnings Prep Data', 'MSFT', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Season Tracker", "season", "Earnings Prep Data", "MSFT" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `estimates_ssrm`

**hard** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Earnings Prep Data' at http://localhost:7805. Make the data grid behavior and columns usable. The experience needs Estimates Explorer (SSRM) (`estimates_ssrm`, table_ssrm) using `/estimates-ssrm` for server-side sorted and filtered estimates dataset; user controls: Symbol (`symbol`, endpoint) from `/symbols`; data key `rows`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Earnings Prep Data/estimates_ssrm` → `missing_widget`

#### `execution_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready orders and venue quality workflow for an execution analyst. The workspace must cover execution quality by venue. The workspace must cover open execution exceptions. The workspace must cover slippage distribution by venue. Analysts need to inspect venue, fills, slippage percentage. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Execution Room', 'venues', 'Execution Desk Data', 'EDGX'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Execution Room", "venues", "Execution Desk Data", "EDGX" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `fill_quality`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an execution analyst covering orders and venue quality. The workspace must cover fill quality by venue. Analysts need to inspect venue, fills, slippage percentage, as of. Keep these source-contract anchors: `venue` and `fills`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `healthcare_ship`

**hard** · category: platform · specification: -

> A healthcare-research analyst needs a decision-ready Workspace for clinical catalysts and pipelines. The workspace must cover upcoming trial readouts. The workspace must cover catalysts in the next 30 days. The workspace must cover FDA decision and notice feed. Analysts need to inspect ticker, phase, readout. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Readout Desk', 'readouts', 'Healthcare Research Data', 'II'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Readout Desk", "readouts", "Healthcare Research Data", "II" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `latency_history`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for vendor service levels. The workspace must cover vendor latency history. The workspace must cover count of open SLA breaches. Analysts need to inspect vendor, day, latency milliseconds, breach. Leave the complete working workspace open for review. Use `vendor` and `day` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `open_orders`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Execution Desk Data' at http://localhost:7806. Make the data grid behavior and columns usable. The experience needs Open Orders (`open_orders`, table) using `/open-orders` for live open orders blotter; columns: order_id (text), symbol (text), qty (number, int), status (text, titleCase). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Execution Desk Data/open_orders` → `missing_widget`

#### `rates_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover upcoming treasury auctions. The workspace must cover current 2s10s spread in bps. The workspace must cover desk commentary on the rates day. Analysts need to inspect auction date, security, size billions. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Auction Desk', 'auctions', 'Rates Watch Data', '30Y Bond'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Auction Desk", "auctions", "Rates Watch Data", "30Y Bond" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `realized_screen`

**medium** · category: platform · specification: -

> Deliver an analyst-ready Workspace solution for volatility and derivatives. The workspace must cover realized volatility by tenor. Analysts need to inspect tenor, realized percentage, as of. Use `tenor` and `realized_pct` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `realized_vol_grid`

**hard** · category: platform · specification: -

> Build a volatility analyst a dependable volatility and derivatives workspace. The workspace must cover realized volatility by tenor. The workspace must cover term structure for VIX futures by expiry. The workspace must cover current volatility regime score. Analysts need to inspect tenor, realized percentage, as of. Leave the complete working workspace open for review. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `revision_grid`

**medium** · category: platform · specification: -

> Create a usable earnings and estimates workflow for an equity-research analyst. The workspace must cover street revision momentum by ticker. Analysts need to inspect ticker, revised up, revised down, momentum percentage. Large result sets must stay responsive while analysts filter and page through them. The source contract must retain `ticker` and `revised_up`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `trial_catalysts_app`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for clinical catalysts and pipelines. The workspace must cover upcoming clinical trial readouts. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Use `ticker` and `phase` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vendor_sla_table_app`

**medium** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Vendor SLA Data' at http://localhost:7804. Make the data grid behavior and columns usable. The experience needs Vendor SLA Status (`vendor_sla_table`, table) using `/vendor-sla` for vendor SLA state with breach flags; user controls: Status (`status`, text); columns: vendor (text), status (text, titleCase), latency_ms (number), breach (boolean). Organize it as app 'Vendor Ops' with tabs Vendors (vendor_sla_table). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vendor Ops" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Vendor SLA Data/vendor_sla_table` on tab `vendors` → `missing_widget`

#### `vix_history`

**medium** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Vol Desk Data' at http://localhost:7801. Make the data grid behavior and columns usable. The experience needs VIX History (`vix_history`, table) using `/vix-history` for daily CBOE VIX closes with returns; user controls: Window (`window`, number); columns: date (dateString), close (number), return_pct (number, percent, greenRed). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vol Desk Data/vix_history` → `missing_widget`

### apps (20)

#### `alert_metric_wrap`

**easy** · category: platform · specification: -

> Implement the requested app and confirm it by opening it in Workspace. Use 'Surveillance Data' at http://localhost:7807. Treat the app layout and navigation as the product outcome. The experience needs Open Alerts (`alert_metric`, metric) using `/alert-count` for open alert count. Organize it as app 'Alert Board' with tabs Alerts (alert_metric). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Alert Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Surveillance Data/alert_metric` on tab `alerts` → `missing_widget`

#### `case_command`

**hard** · category: platform · specification: -

> A surveillance analyst needs a decision-ready Workspace for cases and compliance alerts. The workspace must cover notes for one surveillance case. The workspace must cover open surveillance alerts. The workspace must cover open alert count. Analysts need to inspect alert ID, desk, severity, age days. Leave the complete working workspace open for review. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `catalyst_metric_wrap`

**hard** · category: platform · specification: partially-specified

> Create a usable clinical catalysts and pipelines workflow for a healthcare-research analyst. The workspace must cover catalysts in the next 30 days. Leave the complete working workspace open for review. The source contract must retain `Healthcare Research Data`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `chain_deck`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a digital-assets analyst covering chain activity and liquidity. The workspace must cover current TVL of all chains from the desk aggregator. The workspace must cover comparison of chain TVL. Analysts need to inspect name, TVL USD, change one-day. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `chain` and `name`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_command`

**hard** · category: platform · specification: partially-specified

> Create a usable the requested financial dataset workflow for an investment analyst. The workspace must cover holdings dataset for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. The workspace must cover sector Exposure for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. The workspace must cover portfolio Snapshot for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. Analysts need to inspect ticker, company, sector, weight, active weight, pnl, rating, bucket, value. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. The source contract must retain `fund` and `period`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_desk`

**hard** · category: platform · specification: -

> An equity-research analyst needs a decision-ready Workspace for earnings and estimates. The workspace must cover EPS beat and miss history. The workspace must cover street estimate revisions by quarter. The workspace must cover average EPS surprise last 4 quarters. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `gas_metric_wrap`

**hard** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Bench Stark Enterprise' at http://localhost:7809. Treat the app layout and navigation as the product outcome. The experience needs Risk Snapshot (`risk_exposure_monitor_dashboard_risk_snapshot`, metric) using `/risk_exposure_monitor_dashboard_risk_snapshot` for risk & Exposure Monitor (Risk User). Institutional demo view modeled on fund operating workflows; user controls: Portfolio (`portfolio`, text), Scenario (`scenario`, text), Period (`period`, text). Organize it as app 'Enterprise Risk Board' with tabs Risk (risk_exposure_monitor_dashboard_risk_snapshot). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Enterprise Risk Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_risk_snapshot` on tab `risk` → `missing_widget`

#### `healthcare_ship`

**hard** · category: platform · specification: -

> A healthcare-research analyst needs a decision-ready Workspace for clinical catalysts and pipelines. The workspace must cover upcoming clinical trial readouts. The workspace must cover catalysts in the next 30 days. The workspace must cover pipeline distribution by phase. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Trial Desk', 'catalysts', 'Healthcare Research Data', 'MRNA', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Trial Desk", "catalysts", "Healthcare Research Data", "MRNA" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `order_watch`

**hard** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Execution Desk Data' at http://localhost:7806. Treat the app layout and navigation as the product outcome. The experience needs Open Orders (`open_orders`, table) using `/open-orders` for live open orders blotter; columns: order_id (text), symbol (text), qty (number, int), status (text, titleCase); Exceptions (`exception_metric`, metric) using `/exception-count` for open execution exceptions. Organize it as app 'Order Watch' with tabs Orders (open_orders, exception_metric) with 2 starter prompt(s). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Order Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Execution Desk Data/open_orders` on tab `orders` → `missing_widget`
- **Widget** ≥1× `Execution Desk Data/exception_metric` on tab `orders` → `missing_widget`

#### `rates_desk`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for the requested financial dataset. The workspace must cover holdings dataset for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. The workspace must cover exposure Treemap for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. Analysts need to inspect ticker, company, sector, weight, active weight, pnl, rating. An analyst can toggle the relevant screening constraint. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use `fund` and `period` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `rates_morning`

**hard** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Rates Watch Data' at http://localhost:7803. Treat the app layout and navigation as the product outcome. The experience needs Yield Curve (`yield_curve`, chart) using `/yield-curve` for plotly treasury yield curve snapshot; consume the raw backend payload; 2s10s Spread (`curve_spread_metric`, metric) using `/curve-spread` for current 2s10s spread in bps. Organize it as app 'Rates Morning' with tabs Morning (yield_curve, curve_spread_metric) with 2 starter prompt(s). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Rates Morning" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Rates Watch Data/yield_curve` on tab `morning` → `missing_widget`
- **Widget** ≥1× `Rates Watch Data/curve_spread_metric` on tab `morning` → `missing_widget`

#### `sla_ship`

**hard** · category: platform · specification: -

> Build a vendor-operations manager a dependable vendor service levels workspace. The workspace must cover count of open SLA breaches. The workspace must cover vendor SLA state with breach flags. The workspace must cover vendor incident notices feed. Analysts need to inspect vendor, status, latency milliseconds, breach. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Vendor Live', 'vendors', 'Vendor SLA Data', 'detail'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Vendor Live", "vendors", "Vendor SLA Data", "detail" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `surprise_metric_wrap`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for earnings and estimates. The workspace must cover average EPS surprise last 4 quarters. Leave the complete working workspace open for review. Use `Earnings Prep Data` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `surveillance_morning`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a surveillance analyst covering cases and compliance alerts. The workspace must cover open surveillance alerts. The workspace must cover notes for one surveillance case. The workspace must cover open alert count. Analysts need to inspect alert ID, desk, severity, age days. Leave the complete working workspace open for review. Keep these source-contract anchors: `severity` and `case_id`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `tvl_ship`

**hard** · category: platform · specification: -

> A digital-assets analyst needs a decision-ready Workspace for chain activity and liquidity. The workspace must cover current TVL of all chains from the desk aggregator. The workspace must cover current gas price snapshot. The workspace must cover comparison of chain TVL. Analysts need to inspect name, TVL USD, change one-day. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Chain Live', 'chains', 'Chain TVL Data', 'Solana'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Chain Live", "chains", "Chain TVL Data", "Solana" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `vendor_board`

**medium** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Vendor SLA Data' at http://localhost:7804. Treat the app layout and navigation as the product outcome. The experience needs Vendor SLA Status (`vendor_sla_table`, table) using `/vendor-sla` for vendor SLA state with breach flags; user controls: Status (`status`, text); columns: vendor (text), status (text, titleCase), latency_ms (number), breach (boolean); Open Breaches (`breach_metric`, metric) using `/breach-count` for count of open SLA breaches. Organize it as app 'Vendor Board' with tabs Vendors (vendor_sla_table, breach_metric). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vendor Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Vendor SLA Data/vendor_sla_table` on tab `vendors` → `missing_widget`
- **Widget** ≥1× `Vendor SLA Data/breach_metric` on tab `vendors` → `missing_widget`

#### `vendor_command`

**medium** · category: platform · specification: -

> Build a working Workspace experience for a vendor-operations manager covering vendor service levels. The workspace must cover vendor SLA state with breach flags. The workspace must cover count of open SLA breaches. The workspace must cover vendor incident notices feed. Analysts need to inspect vendor, status, latency milliseconds, breach. Leave the complete working workspace open for review. Keep these source-contract anchors: `status` and `vendor`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vol_morning`

**medium** · category: platform · specification: -

> Deliver an analyst-ready Workspace solution for volatility and derivatives. The workspace must cover daily CBOE VIX closes with returns. The workspace must cover term structure for VIX futures by expiry. The workspace must cover current volatility regime score. Analysts need to inspect date, close, return percentage. An analyst can adjust the relevant numeric scope. Leave the complete working workspace open for review. Use `window` and `date` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vol_overview`

**hard** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Bench Stark Enterprise' at http://localhost:7809. Treat the app layout and navigation as the product outcome. The experience needs Holdings Table (`portfolio_command_center_holdings_holdings_table`, table) using `/portfolio_command_center_holdings_holdings_table` for portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows; user controls: Fund (`fund`, text), Period (`period`, text); columns: ticker (number, int), company (text), sector (text), weight (number, percent), active_weight (number, percent), pnl (number, int, greenRed), rating (text); Portfolio Snapshot (`portfolio_command_center_overview_portfolio_snapshot`, metric) using `/portfolio_command_center_overview_portfolio_snapshot` for portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows; user controls: Fund (`fund`, text), Period (`period`, text). Organize it as app 'Enterprise Portfolio Control' with tabs Overview (portfolio_command_center_holdings_holdings_table, portfolio_command_center_overview_portfolio_snapshot) with 2 starter prompt(s). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Enterprise Portfolio Control" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_holdings_holdings_table` on tab `overview` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_overview_portfolio_snapshot` on tab `overview` → `missing_widget`

#### `vol_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready the requested financial dataset workflow for an investment analyst. The workspace must cover holdings dataset for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. The workspace must cover portfolio Snapshot for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. The workspace must cover exposure Treemap for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. Analysts need to inspect ticker, company, sector, weight, active weight, pnl, rating. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Enterprise Portfolio Live', 'enterprise portfolio', 'Bench Stark Enterprise', 'Flagship Long/Short'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Enterprise Portfolio Live", "enterprise portfolio", "Bench Stark Enterprise", "Flagship Long/Short" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

### charts (20)

#### `chain_flow_highchart`

**hard** · category: platform · specification: partially-specified

> Create a usable chain activity and liquidity workflow for a digital-assets analyst. The workspace must cover highcharts chain flow analysis. The source contract must retain `chain`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `chains_highchart`

**medium** · category: platform · specification: explicit

> Make the requested backend widget available and working in the current view. Use 'Chain TVL Data' at http://localhost:7802. Choose a working chart representation for the data. The experience needs TVL by Chain (Highcharts) (`chains_highchart`, chart-highcharts) using `/chains-highchart` for highcharts rendering of chain TVL; cache for 15 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Chain TVL Data/chains_highchart` → `missing_widget`

#### `chains_highchart_app`

**medium** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Chain TVL Data' at http://localhost:7802. Choose a working chart representation for the data. The experience needs TVL by Chain (Highcharts) (`chains_highchart`, chart-highcharts) using `/chains-highchart` for highcharts rendering of chain TVL. Organize it as app 'Chain Highchart' with tabs Chains (chains_highchart). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Chain Highchart" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Chain TVL Data/chains_highchart` on tab `chains` → `missing_widget`

#### `chains_highchart_room`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for chain activity and liquidity. The workspace must cover comparisons of chain TVL. The workspace must cover current TVL of all chains from the desk aggregator. Analysts need to inspect name, TVL USD, change one-day. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use `chain_scope` and `name` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_chart`

**hard** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Earnings Prep Data' at http://localhost:7805. Choose a working chart representation for the data. The experience needs EPS History (`earnings_chart`, chart) using `/eps-history` for plotly EPS beat/miss history; user controls: Symbol (`symbol`, endpoint) from `/symbols`; cache for 15 minutes; consume the raw backend payload. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Earnings Prep Data/earnings_chart` → `missing_widget`

#### `earnings_chart_app`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover EPS beat and miss history. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Keep these source-contract anchors: `symbol`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_chart_room`

**hard** · category: platform · specification: -

> The desk needs a production-ready earnings and estimates workflow for an equity-research analyst. The workspace must cover EPS beat and miss history. The workspace must cover street estimate revisions by quarter. The workspace must cover average EPS surprise last 4 quarters. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_ship`

**hard** · category: platform · specification: -

> An equity-research analyst needs a decision-ready Workspace for earnings and estimates. The workspace must cover EPS beat and miss history. The workspace must cover average EPS surprise last 4 quarters. The workspace must cover street estimate revisions by quarter. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Earnings Chart Live', 'earnings history', 'Earnings Prep Data', 'MSFT', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Earnings Chart Live", "earnings history", "Earnings Prep Data", "MSFT" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `healthcare_ship`

**hard** · category: platform · specification: -

> A healthcare-research analyst needs a decision-ready Workspace for clinical catalysts and pipelines. The workspace must cover distribution of pipeline phase mix. The workspace must cover catalysts in the next 30 days. The workspace must cover upcoming clinical trial readouts. Analysts need to inspect ticker, phase, readout date. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Pipeline Chart Live', 'pipeline phases', 'Healthcare Research Data', 'III', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Pipeline Chart Live", "pipeline phases", "Healthcare Research Data", "III" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `phase_mix_vegalite`

**hard** · category: platform · specification: partially-specified

> Create a usable clinical catalysts and pipelines workflow for a healthcare-research analyst. The workspace must cover vega-Lite phase mix analysis. The source contract must retain `phase`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `pipeline_vegalite`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Healthcare Research Data' at http://localhost:7808. Choose a working chart representation for the data. The experience needs Pipeline Mix (Vega-Lite) (`pipeline_vegalite`, chart-vegalite) using `/pipeline-vegalite` for vega-Lite bar spec of pipeline phase mix; cache for 30 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Healthcare Research Data/pipeline_vegalite` → `missing_widget`

#### `pipeline_vegalite_app`

**hard** · category: platform · specification: partially-specified

> Create a usable clinical catalysts and pipelines workflow for a healthcare-research analyst. The workspace must cover distribution of pipeline phase mix. Leave the complete working workspace open for review. The source contract must retain `phase`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `pipeline_vegalite_room`

**hard** · category: platform · specification: -

> The desk needs a production-ready clinical catalysts and pipelines workflow for a healthcare-research analyst. The workspace must cover distribution of pipeline phase mix. The workspace must cover upcoming clinical trial readouts. The workspace must cover catalysts in the next 30 days. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `rates_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover the Treasury yield curve. The workspace must cover current 2s10s spread in bps. The workspace must cover desk commentary on the rates day. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Rates Chart Live', 'yield curve', 'Rates Watch Data', '5s30s'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Rates Chart Live", "yield curve", "Rates Watch Data", "5s30s" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `symbol_momentum_chart`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for earnings and estimates. The workspace must cover plotly momentum analysis by symbol. An analyst can filter the analysis by ticker. Use `symbol` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `tvl_ship`

**hard** · category: platform · specification: -

> A digital-assets analyst needs a decision-ready Workspace for chain activity and liquidity. The workspace must cover comparisons of chain TVL. The workspace must cover current gas price snapshot. The workspace must cover current TVL of all chains from the desk aggregator. Analysts need to inspect name, TVL USD, change one-day. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Chain Chart Live', 'chain TVL', 'Chain TVL Data', 'Solana'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Chain Chart Live", "chain TVL", "Chain TVL Data", "Solana" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `venue_slippage_chart`

**hard** · category: platform · specification: partially-specified

> Create a usable orders and venue quality workflow for an execution analyst. The workspace must cover plotly slippage analysis by venue. The source contract must retain `venue`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `yield_curve`

**hard** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Rates Watch Data' at http://localhost:7803. Choose a working chart representation for the data. The experience needs Yield Curve (`yield_curve`, chart) using `/yield-curve` for plotly treasury yield curve snapshot; cache for 15 minutes; consume the raw backend payload. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Rates Watch Data/yield_curve` → `missing_widget`

#### `yield_curve_app`

**hard** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Rates Watch Data' at http://localhost:7803. Choose a working chart representation for the data. The experience needs Yield Curve (`yield_curve`, chart) using `/yield-curve` for plotly treasury yield curve snapshot; consume the raw backend payload. Organize it as app 'Yield Curve App' with tabs Curve (yield_curve). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Yield Curve App" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Rates Watch Data/yield_curve` on tab `curve` → `missing_widget`

#### `yield_curve_room`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for rates and Treasury markets. The workspace must cover the Treasury yield curve. The workspace must cover current 2s10s spread in bps. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use `curve_scope` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### debug (24)

#### `execution_broken_group`

**medium** · category: repair · specification: open-brief

> Execution analysts report that changing review scope no longer keeps the overview and detail aligned in Execution Recovery Room. Diagnose the existing Execution Repair Data connection, repair it in place, and retest the affected workflow with live data before handing it back. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification note that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_dangling_app`

**easy** · category: repair · specification: partially-specified

> An incident in Execution Recovery Room means the detail tab opens to an empty space after a retired panel was removed. Investigate the connected Execution Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification note that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_data_mismatch`

**hard** · category: repair · specification: partially-specified

> An incident in Execution Recovery Room means the overview loads but a declared analyst field is absent. Investigate the connected Execution Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification HTML card that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_duplicate_backend`

**hard** · category: repair · specification: partially-specified

> An incident in Execution Recovery Room means two identically named backend connections now compete for the app. Investigate the connected Execution Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification note that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "delete"} must appear in the trace → `missing_tool_call`

#### `execution_invalid_widget`

**hard** · category: repair · specification: partially-specified

> Restore Execution Recovery Room for execution analysts: one panel disappeared after a backend definition update. Work through the existing Execution Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification note that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_silent_second_tab`

**easy** · category: repair · specification: open-brief

> An incident in Execution Recovery Room means the primary view works while a secondary view silently fails to load. Investigate the connected Execution Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification note that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 17 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_wrong_form_endpoint`

**easy** · category: repair · specification: open-brief

> An incident in Execution Recovery Room means the intake form accepts input but submission does nothing. Investigate the connected Execution Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification note that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_wrong_live_row_id`

**hard** · category: repair · specification: -

> Restore Execution Recovery Room for execution analysts: live updates overwrite the wrong rows and make the queue unstable. Work through the existing Execution Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification HTML card that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `surveillance_broken_group`

**easy** · category: repair · specification: open-brief

> An incident in Surveillance Recovery Room means changing review scope no longer keeps the overview and detail aligned. Investigate the connected Surveillance Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification note that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `surveillance_dangling_app`

**easy** · category: repair · specification: partially-specified

> An incident in Surveillance Recovery Room means the detail tab opens to an empty space after a retired panel was removed. Investigate the connected Surveillance Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification note that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `surveillance_data_mismatch`

**medium** · category: repair · specification: -

> Surveillance analysts report that the overview loads but a declared analyst field is absent in Surveillance Recovery Room. Diagnose the existing Surveillance Repair Data connection, repair it in place, and retest the affected workflow with live data before handing it back. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification note that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `surveillance_duplicate_backend`

**hard** · category: repair · specification: partially-specified

> An incident in Surveillance Recovery Room means two identically named backend connections now compete for the app. Investigate the connected Surveillance Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification note that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "delete"} must appear in the trace → `missing_tool_call`

#### `surveillance_invalid_widget`

**hard** · category: repair · specification: partially-specified

> An incident in Surveillance Recovery Room means one panel disappeared after a backend definition update. Investigate the connected Surveillance Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification HTML card that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `surveillance_silent_second_tab`

**hard** · category: repair · specification: -

> Restore Surveillance Recovery Room for surveillance analysts: the primary view works while a secondary view silently fails to load. Work through the existing Surveillance Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification HTML card that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 17 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `surveillance_wrong_form_endpoint`

**medium** · category: repair · specification: open-brief

> Restore Surveillance Recovery Room for surveillance analysts: the intake form accepts input but submission does nothing. Work through the existing Surveillance Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification note that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `surveillance_wrong_live_row_id`

**easy** · category: repair · specification: open-brief

> Restore Surveillance Recovery Room for surveillance analysts: live updates overwrite the wrong rows and make the queue unstable. Work through the existing Surveillance Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification note that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_broken_group`

**hard** · category: repair · specification: -

> An incident in Vendor Recovery Room means changing review scope no longer keeps the overview and detail aligned. Investigate the connected Vendor Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification HTML card that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_dangling_app`

**easy** · category: repair · specification: partially-specified

> Restore Vendor Recovery Room for vendor operations analysts: the detail tab opens to an empty space after a retired panel was removed. Work through the existing Vendor Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification note that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_data_mismatch`

**medium** · category: repair · specification: -

> Restore Vendor Recovery Room for vendor operations analysts: the overview loads but a declared analyst field is absent. Work through the existing Vendor Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification note that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_duplicate_backend`

**hard** · category: repair · specification: partially-specified

> Restore Vendor Recovery Room for vendor operations analysts: two identically named backend connections now compete for the app. Work through the existing Vendor Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification HTML card that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "delete"} must appear in the trace → `missing_tool_call`

#### `vendor_invalid_widget`

**hard** · category: repair · specification: partially-specified

> Vendor operations analysts report that one panel disappeared after a backend definition update in Vendor Recovery Room. Diagnose the existing Vendor Repair Data connection, repair it in place, and retest the affected workflow with live data before handing it back. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification HTML card that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_silent_second_tab`

**easy** · category: repair · specification: open-brief

> An incident in Vendor Recovery Room means the primary view works while a secondary view silently fails to load. Investigate the connected Vendor Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification note that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 17 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_wrong_form_endpoint`

**medium** · category: repair · specification: open-brief

> An incident in Vendor Recovery Room means the intake form accepts input but submission does nothing. Investigate the connected Vendor Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification note that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_wrong_live_row_id`

**hard** · category: repair · specification: -

> Restore Vendor Recovery Room for vendor operations analysts: live updates overwrite the wrong rows and make the queue unstable. Work through the existing Vendor Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification HTML card that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### e2e (12)

#### `case_triage`

**hard** · category: platform · specification: -

> A surveillance analyst needs a decision-ready Workspace for cases and compliance alerts. The workspace must cover case owners, priorities, and SLA days. The workspace must cover notes for one surveillance case. Analysts need to inspect case ID, owner, priority, SLA days. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Case Triage', 'Surveillance Data', 'C-1048'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Case Triage", "case triage", "Surveillance Data", "C-1048" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `catalyst_calendar`

**hard** · category: platform · specification: -

> Build a healthcare-research analyst a dependable clinical catalysts and pipelines workspace. The workspace must cover healthcare catalysts and impact scores. The workspace must cover catalysts in the next 30 days. Analysts need to inspect ticker, event, event date, impact score. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Catalyst Calendar', 'Healthcare Research Data', 'PFE', 'ticker'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Catalyst Calendar", "catalyst calendar", "Healthcare Research Data", "PFE" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `chain_flows`

**hard** · category: platform · specification: -

> A digital-assets analyst needs a decision-ready Workspace for chain activity and liquidity. The workspace must cover net chain flows and fee share. The workspace must cover current gas price snapshot. Analysts need to inspect chain, net flow USD, fee percentage, as of. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Chain Flows', 'Chain TVL Data', 'Solana'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Chain Flows", "chain flows", "Chain TVL Data", "Solana" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `compliance_surveillance`

**hard** · category: platform · specification: -

> The desk needs a production-ready cases and compliance alerts workflow for a surveillance analyst. The workspace must cover open surveillance cases by severity. The workspace must cover open alert count. Analysts need to inspect case ID, desk, severity, age days. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Compliance Surveillance', 'surveillance', 'Surveillance Data', 'C-1044'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Compliance Surveillance", "surveillance", "Surveillance Data", "C-1044" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `earnings_season`

**hard** · category: platform · specification: -

> An equity-research analyst needs a decision-ready Workspace for earnings and estimates. The workspace must cover earnings surprises and report dates. The workspace must cover average EPS surprise last 4 quarters. Analysts need to inspect ticker, EPS surprise percentage, revenue beat, report date. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Earnings Season', 'Earnings Prep Data', 'MSFT', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Earnings Season", "earnings season", "Earnings Prep Data", "MSFT" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `execution_monitor`

**hard** · category: platform · specification: -

> An execution analyst needs a decision-ready Workspace for orders and venue quality. The workspace must cover venue execution quality and rejects. The workspace must cover open execution exceptions. Analysts need to inspect venue, orders, reject rate percentage, as of. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Execution Monitor', 'Execution Desk Data', 'EDGX'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Execution Monitor", "execution monitor", "Execution Desk Data", "EDGX" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `healthcare_pipeline`

**hard** · category: platform · specification: -

> Build a healthcare-research analyst a dependable clinical catalysts and pipelines workspace. The workspace must cover healthcare pipeline programs by phase. The workspace must cover pipeline distribution by phase. Analysts need to inspect ticker, phase, programs, readout date. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Healthcare Pipeline', 'pipeline', 'Healthcare Research Data', 'MRNA', 'ticker'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Healthcare Pipeline", "pipeline", "Healthcare Research Data", "MRNA" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `macro_morning`

**hard** · category: platform · specification: -

> Build a rates strategist a dependable rates and Treasury markets workspace. The workspace must cover rates morning levels and changes. The workspace must cover the Treasury yield curve. Analysts need to inspect series, level, change bp, as of. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Macro Morning', 'Rates Watch Data', 'DGS2'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Macro Morning", "macro morning", "Rates Watch Data", "DGS2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `rates_auctions`

**hard** · category: platform · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover upcoming auctions and demand metrics. The workspace must cover current 2s10s spread in bps. Analysts need to inspect auction date, security, size billions, bid to cover. An analyst can choose the relevant business date. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Rates Auctions', 'Rates Watch Data', '2026-07-15', 'date'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Rates Auctions", "rates auctions", "Rates Watch Data", "2026-07-15" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `research_room`

**hard** · category: platform · specification: -

> Build an investment analyst a dependable the requested financial dataset workspace. The workspace must cover analyst research actions by ticker. The workspace must cover sector Exposure for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. Analysts need to inspect ticker, analyst, rating, upside percentage, bucket, value. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Research Room', 'Bench Stark Enterprise', 'MSFT', 'ticker'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Research Room", "research room", "Bench Stark Enterprise", "MSFT" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `vendor_ops`

**hard** · category: platform · specification: -

> The desk needs a production-ready vendor service levels workflow for a vendor-operations manager. The workspace must cover vendor uptime and latency posture. The workspace must cover count of open SLA breaches. Analysts need to inspect vendor, uptime percentage, latency milliseconds, status. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Vendor Ops', 'Vendor SLA Data', 'QuoteStream'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Vendor Ops", "vendor ops", "Vendor SLA Data", "QuoteStream" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `vol_cockpit`

**hard** · category: platform · specification: -

> A volatility analyst needs a decision-ready Workspace for volatility and derivatives. The workspace must cover implied and realized volatility by tenor. The workspace must cover market history for VIX futures. Analysts need to inspect tenor, iv percentage, realized percentage, as of. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Vol Cockpit', 'Vol Desk Data', '3M'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Vol Cockpit", "vol cockpit", "Vol Desk Data", "3M" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

### extend (20)

#### `add_catalyst_metric`

**medium** · category: repair · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Healthcare Research Data' at http://localhost:7808. Repair the existing backend without regressing working content. The experience needs Pipeline by Phase (`pipeline_chart`, chart) using `/pipeline-by-phase` for plotly pipeline distribution by phase; consume the raw backend payload; Catalysts 30d (`catalyst_metric`, metric) using `/catalyst-count` for catalysts in the next 30 days; cache for 15 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Healthcare Research Data/pipeline_chart` → `missing_widget`

#### `add_curve_spread_metric`

**easy** · category: repair · specification: -

> Make the requested backend widget available and working in the current view. Use 'Rates Watch Data' at http://localhost:7803. Repair the existing backend without regressing working content. The experience needs Yield Curve (`yield_curve`, chart) using `/yield-curve` for plotly treasury yield curve snapshot; consume the raw backend payload; 2s10s Spread (`curve_spread_metric`, metric) using `/curve-spread` for current 2s10s spread in bps; cache for 15 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Rates Watch Data/yield_curve` → `missing_widget`

#### `add_exception_metric`

**easy** · category: repair · specification: -

> Make the requested backend widget available and working in the current view. Use 'Execution Desk Data' at http://localhost:7806. Repair the existing backend without regressing working content. The experience needs Open Orders (`open_orders`, table) using `/open-orders` for live open orders blotter; columns: order_id (text), symbol (text), qty (number, int), status (text, titleCase); Exceptions (`exception_metric`, metric) using `/exception-count` for open execution exceptions; cache for 15 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Execution Desk Data/open_orders` → `missing_widget`

#### `add_vol_regime_metric`

**hard** · category: repair · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Vol Desk Data' at http://localhost:7801. Repair the existing backend without regressing working content. The experience needs VIX Term Structure (`vix_term_structure`, chart) using `/vix-term-structure` for plotly curve of VIX futures by expiry; consume the raw backend payload; Vol Regime (`vol_regime_metric`, metric) using `/vol-regime` for current volatility regime score; cache for 15 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vol Desk Data/vix_term_structure` → `missing_widget`

#### `diagnose_earnings`

**hard** · category: repair · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. The workspace must cover average EPS surprise last 4 quarters. The workspace must cover preview note for the earnings call. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. Keep these source-contract anchors: `symbol` and `quarter`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `diagnose_healthcare`

**hard** · category: repair · specification: partially-specified

> Deliver an analyst-ready Workspace solution for clinical catalysts and pipelines. The workspace must cover upcoming clinical trial readouts. The workspace must cover distribution of pipeline phase mix. The workspace must cover FDA decision and notice feed. The workspace must cover catalysts in the next 30 days. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. Use `ticker` and `phase` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `diagnose_rates`

**hard** · category: repair · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover upcoming treasury auctions. The workspace must cover desk commentary on the rates day. The workspace must cover current 2s10s spread in bps. The workspace must cover the Treasury yield curve. Analysts need to inspect date, security, size billions. Preserve all working content while correcting the requested workflow. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `diagnose_sla`

**hard** · category: repair · specification: -

> Build a vendor-operations manager a dependable vendor service levels workspace. The workspace must cover vendor SLA state with breach flags. The workspace must cover count of open SLA breaches. The workspace must cover vendor incident notices feed. The workspace must cover runbook for SLA escalations. Analysts need to inspect vendor, status, latency milliseconds, breach. Preserve all working content while correcting the requested workflow. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `modify_case_notes`

**hard** · category: repair · specification: partially-specified

> Create a usable cases and compliance alerts workflow for a surveillance analyst. The workspace must cover notes for one surveillance case. The workspace must cover open alert count. The source contract must retain `case_id`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `modify_rates_commentary`

**hard** · category: repair · specification: partially-specified

> Create a usable rates and Treasury markets workflow for a rates strategist. The workspace must cover desk commentary on the rates day. The workspace must cover current 2s10s spread in bps. The source contract must retain `series`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `modify_trial_catalysts`

**hard** · category: repair · specification: partially-specified

> Deliver an analyst-ready Workspace solution for clinical catalysts and pipelines. The workspace must cover upcoming clinical trial readouts. The workspace must cover catalysts in the next 30 days. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. Use `ticker` and `phase` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `modify_vol_screener`

**hard** · category: repair · specification: partially-specified

> Deliver an analyst-ready Workspace solution for volatility and derivatives. The workspace must cover screen names by implied-vol criteria. The workspace must cover current volatility regime score. An analyst can filter the analysis by ticker. An analyst can choose the relevant business date. An analyst can toggle the relevant screening constraint. Use `ticker` and `as_of` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `place_alert_metric`

**hard** · category: repair · specification: partially-specified

> Create a usable cases and compliance alerts workflow for a surveillance analyst. The workspace must cover open surveillance alerts. The workspace must cover open alert count. Analysts need to inspect alert ID, desk, severity, age days. Leave the complete working workspace open for review. The source contract must retain `severity` and `alert_id`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `place_breach_metric`

**hard** · category: repair · specification: partially-specified

> Create a usable vendor service levels workflow for a vendor-operations manager. The workspace must cover vendor SLA state with breach flags. The workspace must cover count of open SLA breaches. Analysts need to inspect vendor, status, latency milliseconds, breach. Leave the complete working workspace open for review. The source contract must retain `status` and `vendor`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `place_curve_spread_metric`

**medium** · category: repair · specification: explicit

> Publish the requested app and open it in Workspace to verify it works. Use 'Rates Watch Data' at http://localhost:7803. Repair the existing backend without regressing working content. The experience needs Auction Calendar (`auction_calendar`, table) using `/auction-calendar` for upcoming treasury auctions; columns: date (dateString), security (text), size_bn (number); 2s10s Spread (`curve_spread_metric`, metric) using `/curve-spread` for current 2s10s spread in bps. Organize it as app 'Auction Review' with tabs Auctions (auction_calendar, curve_spread_metric). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Auction Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Rates Watch Data/auction_calendar` on tab `auctions` → `missing_widget`
- **Widget** ≥1× `Rates Watch Data/curve_spread_metric` on tab `auctions` → `missing_widget`

#### `place_vol_regime_metric`

**medium** · category: repair · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Vol Desk Data' at http://localhost:7801. Repair the existing backend without regressing working content. The experience needs VIX History (`vix_history`, table) using `/vix-history` for daily CBOE VIX closes with returns; user controls: Window (`window`, number); columns: date (dateString), close (number), return_pct (number, percent, greenRed); Vol Regime (`vol_regime_metric`, metric) using `/vol-regime` for current volatility regime score. Organize it as app 'Vol Review' with tabs Overview (vix_history, vol_regime_metric). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vol Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Vol Desk Data/vix_history` on tab `overview` → `missing_widget`
- **Widget** ≥1× `Vol Desk Data/vol_regime_metric` on tab `overview` → `missing_widget`

#### `repair_compliance`

**hard** · category: repair · specification: -

> The desk needs a production-ready cases and compliance alerts workflow for a surveillance analyst. The workspace must cover ask questions over the surveillance case corpus. The workspace must cover open alert count. Leave the complete working workspace open for review. Preserve all working content while correcting the requested workflow. Add a short completion note that naturally includes the desk-required terms 'Case Repair Live', 'case repair', 'Surveillance Data', 'Show high severity cases'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Case Repair Live", "case repair", "Surveillance Data", "Show high severity cases" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `repair_execution`

**hard** · category: repair · specification: -

> The desk needs a production-ready orders and venue quality workflow for an execution analyst. The workspace must cover live order activity. The workspace must cover open execution exceptions. Analysts need to inspect order ID, price. Large result sets must stay responsive while analysts filter and page through them. Leave the complete working workspace open for review. Preserve all working content while correcting the requested workflow. Add a short completion HTML card that naturally includes the desk-required terms 'Execution Repair Live', 'execution repair', 'Execution Desk Data', 'EDGX'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Execution Repair Live", "execution repair", "Execution Desk Data", "EDGX" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `repair_rates`

**hard** · category: repair · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover desk commentary on the rates day. The workspace must cover current 2s10s spread in bps. Leave the complete working workspace open for review. Preserve all working content while correcting the requested workflow. Add a short completion HTML card that naturally includes the desk-required terms 'Rates Repair Live', 'rates repair', 'Rates Watch Data', 'DGS2'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Rates Repair Live", "rates repair", "Rates Watch Data", "DGS2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `repair_vol`

**hard** · category: repair · specification: -

> A volatility analyst needs a decision-ready Workspace for volatility and derivatives. The workspace must cover market history for VIX futures. The workspace must cover current volatility regime score. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Preserve all working content while correcting the requested workflow. Add a short completion note that naturally includes the desk-required terms 'Vol Repair Live', 'vol regime', 'Vol Desk Data', 'VX2', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Vol Repair Live", "vol regime", "Vol Desk Data", "VX2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

### forms (20)

#### `access_review_form`

**medium** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Surveillance Data' at http://localhost:7807. Make the submission workflow functional. The experience needs Access Review Form (`access_review_form`, markdown) using `/access-review` for capture an access review decision; user controls: Access Review (`review`, form) with User, Approved, Save. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Surveillance Data/access_review_form` → `missing_widget`

#### `case_escalation_form_app`

**hard** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Surveillance Data' at http://localhost:7807. Make the submission workflow functional. The experience needs Case Escalation Form (`case_escalation_form`, table) using `/case-escalation` for escalate a surveillance case to a reviewer; user controls: Escalation (`escalation`, form) with Case, Due date, Escalate. Organize it as app 'Case Escalation' with tabs Cases (case_escalation_form). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Case Escalation" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Surveillance Data/case_escalation_form` on tab `cases` → `missing_widget`

#### `case_intake_room`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a surveillance analyst covering cases and compliance alerts. The workspace must cover escalate a surveillance case to a reviewer. The workspace must cover open surveillance alerts. Analysts need to inspect alert ID, desk, severity, age days. An analyst can choose the relevant business date. The user can enter the required details and submit the workflow. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `escalation` and `case_id`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `compliance_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready cases and compliance alerts workflow for a surveillance analyst. The workspace must cover escalate a surveillance case to a reviewer. The workspace must cover open alert count. The workspace must cover open surveillance alerts. Analysts need to inspect alert ID, desk, severity, age days. An analyst can choose the relevant business date. The user can enter the required details and submit the workflow. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Case Intake Live', 'case intake', 'Surveillance Data', 'C-1044', 'date'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Case Intake Live", "case intake", "Surveillance Data", "C-1044" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `curve_comment_form_app`

**hard** · category: platform · specification: partially-specified

> Create a usable rates and Treasury markets workflow for a rates strategist. The workspace must cover submit a curve desk comment. The user can enter the required details and submit the workflow. Leave the complete working workspace open for review. The source contract must retain `comment` and `series`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `exception_intake_room`

**hard** · category: platform · specification: -

> An execution analyst needs a decision-ready Workspace for orders and venue quality. The workspace must cover record an execution venue exception. The workspace must cover live open orders blotter. The workspace must cover open execution exceptions. Analysts need to inspect order ID, symbol, quantity, status. An analyst can adjust the relevant numeric scope. The user can enter the required details and submit the workflow. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `execution_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready orders and venue quality workflow for an execution analyst. The workspace must cover record an execution venue exception. The workspace must cover open execution exceptions. The workspace must cover live open orders blotter. Analysts need to inspect order ID, symbol, quantity, status. An analyst can adjust the relevant numeric scope. The user can enter the required details and submit the workflow. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Exception Intake Live', 'exception intake', 'Execution Desk Data', 'EDGX'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Exception Intake Live", "exception intake", "Execution Desk Data", "EDGX" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `healthcare_ship`

**hard** · category: platform · specification: -

> A healthcare-research analyst needs a decision-ready Workspace for clinical catalysts and pipelines. The workspace must cover capture a clinical trial readout note. The workspace must cover catalysts in the next 30 days. The workspace must cover upcoming clinical trial readouts. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. An analyst can choose the relevant business date. The user can enter the required details and submit the workflow. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Trial Intake Live', 'trial intake', 'Healthcare Research Data', 'MRNA', 'ticker', 'date'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Trial Intake Live", "trial intake", "Healthcare Research Data", "MRNA" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `incident_triage_form`

**hard** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Vendor SLA Data' at http://localhost:7804. Make the submission workflow functional. The experience needs Incident Triage Form (`incident_triage_form`, table) using `/incident-triage` for submit an incident triage record for review; user controls: Triage (`triage`, form) with Incident, Review date, Submit. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vendor SLA Data/incident_triage_form` → `missing_widget`

#### `policy_exception_form`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a surveillance analyst covering cases and compliance alerts. The workspace must cover submit a policy exception request. The user can enter the required details and submit the workflow. Keep these source-contract anchors: `exception` and `policy_id`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `sla_ship`

**hard** · category: platform · specification: -

> Build a vendor-operations manager a dependable vendor service levels workspace. The workspace must cover submit a new vendor record into the SLA register. The workspace must cover count of open SLA breaches. The workspace must cover vendor SLA state with breach flags. Analysts need to inspect vendor, status, latency milliseconds, breach. An analyst can adjust the relevant numeric scope. The user can enter the required details and submit the workflow. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Vendor Intake Live', 'vendor intake', 'Vendor SLA Data', 'QuoteStream'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Vendor Intake Live", "vendor intake", "Vendor SLA Data", "QuoteStream" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `threshold_update_form`

**hard** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Execution Desk Data' at http://localhost:7806. Make the submission workflow functional. The experience needs Threshold Update Form (`threshold_update_form`, table) using `/threshold-update` for submit a threshold change for operations; user controls: Threshold (`threshold`, form) with Limit, Owner, Apply. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Execution Desk Data/threshold_update_form` → `missing_widget`

#### `trade_break_form`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for orders and venue quality. The workspace must cover record a trade break for operations review. An analyst can adjust the relevant numeric scope. The user can enter the required details and submit the workflow. Use `break_item` and `trade_id` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `trial_intake_room`

**hard** · category: platform · specification: -

> Build a healthcare-research analyst a dependable clinical catalysts and pipelines workspace. The workspace must cover capture a clinical trial readout note. The workspace must cover upcoming clinical trial readouts. The workspace must cover catalysts in the next 30 days. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. An analyst can choose the relevant business date. The user can enter the required details and submit the workflow. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `trial_readout_form`

**hard** · category: platform · specification: partially-specified

> Create a usable clinical catalysts and pipelines workflow for a healthcare-research analyst. The workspace must cover capture a clinical trial readout note. An analyst can filter the analysis by ticker. An analyst can choose the relevant business date. The user can enter the required details and submit the workflow. The source contract must retain `readout` and `ticker`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vendor_intake_form`

**hard** · category: platform · specification: explicit

> Make the requested backend widget available and working in the current view. Use 'Vendor SLA Data' at http://localhost:7804. Make the submission workflow functional. The experience needs Vendor Intake Form (`vendor_intake_form`, table) using `/vendor-intake` for submit a new vendor record into the SLA register; user controls: New Vendor (`intake`, form) with Vendor, Tier, Add Vendor. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vendor SLA Data/vendor_intake_form` → `missing_widget`

#### `vendor_intake_form_app`

**hard** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Vendor SLA Data' at http://localhost:7804. Make the submission workflow functional. The experience needs Vendor Intake Form (`vendor_intake_form`, table) using `/vendor-intake` for submit a new vendor record into the SLA register; user controls: New Vendor (`intake`, form) with Vendor, Tier, Add Vendor. Organize it as app 'Vendor Intake' with tabs Intake (vendor_intake_form). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vendor Intake" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Vendor SLA Data/vendor_intake_form` on tab `intake` → `missing_widget`

#### `vendor_intake_room`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a vendor-operations manager covering vendor service levels. The workspace must cover submit a new vendor record into the SLA register. The workspace must cover vendor SLA state with breach flags. Analysts need to inspect vendor, status, latency milliseconds, breach. An analyst can adjust the relevant numeric scope. The user can enter the required details and submit the workflow. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `intake` and `vendor`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vendor_review_form`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a vendor-operations manager covering vendor service levels. The workspace must cover create a vendor review item. An analyst can choose the relevant business date. The user can enter the required details and submit the workflow. Keep these source-contract anchors: `review` and `vendor_name`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `venue_exception_form_app`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an execution analyst covering orders and venue quality. The workspace must cover record an execution venue exception. An analyst can adjust the relevant numeric scope. The user can enter the required details and submit the workflow. Leave the complete working workspace open for review. Keep these source-contract anchors: `exception` and `venue`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### grouping (20)

#### `chart_note_board`

**medium** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Earnings Prep Data' at http://localhost:7805. Make the cross-widget interaction work. The experience needs EPS History (`earnings_chart`, chart) using `/eps-history` for plotly EPS beat/miss history; user controls: Symbol (`symbol`, endpoint) from `/symbols`; consume the raw backend payload; Earnings Preview (`earnings_note`, markdown) using `/earnings-preview` for preview note for the earnings call; user controls: Symbol (`symbol`, endpoint) from `/symbols`. Organize it as app 'Chart Note Board' with tabs Preview (earnings_chart, earnings_note) with shared interactions Preview Symbol Sync across earnings_chart, earnings_note via `symbol`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Chart Note Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Earnings Prep Data/earnings_chart` on tab `preview` → `missing_widget`
- **Widget** ≥1× `Earnings Prep Data/earnings_note` on tab `preview` → `missing_widget`

#### `chart_preview_sync`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover EPS beat and miss history. The workspace must cover preview note for the earnings call. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `symbol`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `chart_sync_live`

**hard** · category: platform · specification: -

> Build an equity-research analyst a dependable earnings and estimates workspace. The workspace must cover EPS beat and miss history. The workspace must cover preview note for the earnings call. The workspace must cover street estimate revisions by quarter. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Chart Sync Live', 'linked earnings selection', 'Earnings Prep Data', 'MSFT', 'ticker'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Chart Sync Live", "linked earnings selection", "Earnings Prep Data", "MSFT" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `click_preview_desk`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover preview rows whose symbol cell syncs the app. The workspace must cover preview note for the earnings call. Analysts need to inspect symbol, revision percentage. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `symbol` and `revision_pct`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `click_revision_desk`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for earnings and estimates. The workspace must cover revision rows whose symbol cell syncs the app. The workspace must cover EPS beat and miss history. Analysts need to inspect symbol, revision percentage. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use `symbol` and `revision_pct` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `click_season_desk`

**hard** · category: platform · specification: -

> The desk needs a production-ready earnings and estimates workflow for an equity-research analyst. The workspace must cover season rows whose ticker selection links to revisions. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. Analysts need to inspect symbol, revision percentage, quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `click_summary_desk`

**hard** · category: platform · specification: -

> The desk needs a production-ready earnings and estimates workflow for an equity-research analyst. The workspace must cover summary rows whose ticker selection stays linked across analysis. The workspace must cover EPS beat and miss history. The workspace must cover preview note for the earnings call. Analysts need to inspect symbol, revision percentage. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `click_sync_live`

**hard** · category: platform · specification: -

> Build an equity-research analyst a dependable earnings and estimates workspace. The workspace must cover clickable live symbol rows for grouped review. The workspace must cover EPS beat and miss history. The workspace must cover preview HTML card for the earnings call. Analysts need to inspect symbol, revision percentage. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Click Sync Live', 'click sync', 'Earnings Prep Data', 'AAPL', 'ticker'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Click Sync Live", "click sync", "Earnings Prep Data", "AAPL" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `earnings_chart_app`

**hard** · category: platform · specification: explicit

> Publish the requested app and open it in Workspace to verify it works. Use 'Earnings Prep Data' at http://localhost:7805. Make the cross-widget interaction work. The experience needs EPS History (`earnings_chart`, chart) using `/eps-history` for plotly EPS beat/miss history; user controls: Symbol (`symbol`, endpoint) from `/symbols`; consume the raw backend payload. Organize it as app 'Chart Group App' with tabs Chart (earnings_chart) with shared interactions Chart Symbol Group across earnings_chart via `symbol`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Chart Group App" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Earnings Prep Data/earnings_chart` on tab `chart` → `missing_widget`

#### `earnings_note_app`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover preview note for the earnings call. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Keep these source-contract anchors: `symbol`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_review_sync`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `symbol` and `quarter`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_symbol_board`

**hard** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Earnings Prep Data' at http://localhost:7805. Make the cross-widget interaction work. The experience needs Estimate Revisions (`estimate_revisions`, table) using `/estimate-revisions` for street estimate revisions by quarter; user controls: Symbol (`symbol`, endpoint) from `/symbols`; columns: quarter (text), eps_estimate (number), revenue_estimate_b (number); EPS History (`earnings_chart`, chart) using `/eps-history` for plotly EPS beat/miss history; user controls: Symbol (`symbol`, endpoint) from `/symbols`; consume the raw backend payload. Organize it as app 'Earnings Symbol Board' with tabs Review (estimate_revisions, earnings_chart) with shared interactions Symbol Sync across estimate_revisions, earnings_chart via `symbol`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Earnings Symbol Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Earnings Prep Data/estimate_revisions` on tab `review` → `missing_widget`
- **Widget** ≥1× `Earnings Prep Data/earnings_chart` on tab `review` → `missing_widget`

#### `earnings_sync_live`

**hard** · category: platform · specification: -

> Build an equity-research analyst a dependable earnings and estimates workspace. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. The workspace must cover preview note for the earnings call. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Earnings Sync Live', 'symbol sync', 'Earnings Prep Data', 'MSFT', 'ticker'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Earnings Sync Live", "symbol sync", "Earnings Prep Data", "MSFT" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `estimate_revisions_app`

**hard** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Earnings Prep Data' at http://localhost:7805. Make the cross-widget interaction work. The experience needs Estimate Revisions (`estimate_revisions`, table) using `/estimate-revisions` for street estimate revisions by quarter; user controls: Symbol (`symbol`, endpoint) from `/symbols`; columns: quarter (text), eps_estimate (number), revenue_estimate_b (number). Organize it as app 'Revision Group App' with tabs Revisions (estimate_revisions) with shared interactions Revision Symbol Group across estimate_revisions via `symbol`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Revision Group App" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Earnings Prep Data/estimate_revisions` on tab `revisions` → `missing_widget`

#### `full_earnings_sync`

**hard** · category: platform · specification: partially-specified

> Create a usable earnings and estimates workflow for an equity-research analyst. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. The workspace must cover preview note for the earnings call. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. The source contract must retain `symbol` and `quarter`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `nvda_review_board`

**hard** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Earnings Prep Data' at http://localhost:7805. Make the cross-widget interaction work. The experience needs Estimate Revisions (`estimate_revisions`, table) using `/estimate-revisions` for street estimate revisions by quarter; user controls: Symbol (`symbol`, endpoint) from `/symbols`; columns: quarter (text), eps_estimate (number), revenue_estimate_b (number); EPS History (`earnings_chart`, chart) using `/eps-history` for plotly EPS beat/miss history; user controls: Symbol (`symbol`, endpoint) from `/symbols`; consume the raw backend payload. Organize it as app 'NVDA Review Board' with tabs NVDA (estimate_revisions, earnings_chart) with shared interactions NVDA Symbol Sync across estimate_revisions, earnings_chart via `symbol`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "NVDA Review Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Earnings Prep Data/estimate_revisions` on tab `nvda` → `missing_widget`
- **Widget** ≥1× `Earnings Prep Data/earnings_chart` on tab `nvda` → `missing_widget`

#### `preview_sync_live`

**hard** · category: platform · specification: -

> The desk needs a production-ready earnings and estimates workflow for an equity-research analyst. The workspace must cover preview HTML card for the earnings call. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Preview Sync Live', 'preview sync', 'Earnings Prep Data', 'AAPL', 'ticker'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Preview Sync Live", "preview sync", "Earnings Prep Data", "AAPL" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `revision_note_board`

**hard** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Earnings Prep Data' at http://localhost:7805. Make the cross-widget interaction work. The experience needs Estimate Revisions (`estimate_revisions`, table) using `/estimate-revisions` for street estimate revisions by quarter; user controls: Symbol (`symbol`, endpoint) from `/symbols`; columns: quarter (text), eps_estimate (number), revenue_estimate_b (number); Earnings Preview (`earnings_note`, markdown) using `/earnings-preview` for preview note for the earnings call; user controls: Symbol (`symbol`, endpoint) from `/symbols`. Organize it as app 'Revision Note Board' with tabs Notes (estimate_revisions, earnings_note) with shared interactions Revision Symbol Sync across estimate_revisions, earnings_note via `symbol`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Revision Note Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Earnings Prep Data/estimate_revisions` on tab `notes` → `missing_widget`
- **Widget** ≥1× `Earnings Prep Data/earnings_note` on tab `notes` → `missing_widget`

#### `revision_preview_sync`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover street estimate revisions by quarter. The workspace must cover preview note for the earnings call. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `symbol` and `quarter`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `symbol_click_summary_app`

**medium** · category: platform · specification: -

> Deliver an analyst-ready Workspace solution for earnings and estimates. The workspace must cover symbol rows that can drive a grouped app. Analysts need to inspect symbol, revision percentage. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Use `symbol` and `revision_pct` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### params (20)

#### `case_notes`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Surveillance Data' at http://localhost:7807. Make the user controls functional. The experience needs Case Notes (`case_notes`, markdown) using `/case-notes` for notes for one surveillance case; user controls: Case (`case_id`, text). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Surveillance Data/case_notes` → `missing_widget`

#### `case_notes_app`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for cases and compliance alerts. The workspace must cover notes for one surveillance case. Leave the complete working workspace open for review. Use `case_id` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_param_review`

**hard** · category: platform · specification: partially-specified

> Create a usable earnings and estimates workflow for an equity-research analyst. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. The source contract must retain `symbol` and `quarter`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_ship`

**hard** · category: platform · specification: -

> An equity-research analyst needs a decision-ready Workspace for earnings and estimates. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. The workspace must cover average EPS surprise last 4 quarters. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Earnings Symbol Live', 'symbol sync', 'Earnings Prep Data', 'MSFT', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Earnings Symbol Live", "symbol sync", "Earnings Prep Data", "MSFT" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `healthcare_ship`

**hard** · category: platform · specification: -

> A healthcare-research analyst needs a decision-ready Workspace for clinical catalysts and pipelines. The workspace must cover trial review filtered by symbol. The workspace must cover catalysts in the next 30 days. The workspace must cover upcoming clinical trial readouts. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Trial Symbol Live', 'trial symbol', 'Healthcare Research Data', 'PFE', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Trial Symbol Live", "trial symbol", "Healthcare Research Data", "PFE" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `kpi_param_tabs`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for earnings and estimates. The workspace must cover KPI dataset switched between growth and margin views. Use `view` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `kpi_tabs_table`

**medium** · category: platform · specification: explicit

> Make the requested backend widget available and working in the current view. Use 'Earnings Prep Data' at http://localhost:7805. Make the user controls functional. The experience needs KPI Tabs (`kpi_tabs_table`, table) using `/kpi-tabs` for kPI table with static and dynamic tab views; user controls: View (`view`, tabs). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Earnings Prep Data/kpi_tabs_table` → `missing_widget`

#### `rates_commentary_app`

**medium** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Rates Watch Data' at http://localhost:7803. Make the user controls functional. The experience needs Rates Commentary (`rates_commentary`, markdown) using `/rates-commentary` for desk commentary on the rates day; user controls: Series (`series`, endpoint) from `/series-options`. Organize it as app 'Series Commentary' with tabs Commentary (rates_commentary). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Series Commentary" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Rates Watch Data/rates_commentary` on tab `commentary` → `missing_widget`

#### `rates_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover rates commentary filtered by selected series. The workspace must cover current 2s10s spread in bps. The workspace must cover desk commentary on the rates day. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Rates Series Live', 'series preset', 'Rates Watch Data', 'DGS10'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Rates Series Live", "series preset", "Rates Watch Data", "DGS10" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `series_markdown`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a rates strategist covering rates and Treasury markets. The workspace must cover rates note for the selected time series. Keep these source-contract anchors: `series`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `symbol_param_desk`

**hard** · category: platform · specification: -

> An equity-research analyst needs a decision-ready Workspace for earnings and estimates. The workspace must cover preview note for the earnings call. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `trial_catalysts`

**medium** · category: platform · specification: explicit

> Make the requested backend widget available and working in the current view. Use 'Healthcare Research Data' at http://localhost:7808. Make the user controls functional. The experience needs Trial Catalysts (`trial_catalysts`, table) using `/trial-catalysts` for upcoming clinical trial readouts; user controls: Ticker (`ticker`, endpoint) from `/tickers`; columns: ticker (text), phase (text), readout_date (dateString). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Healthcare Research Data/trial_catalysts` → `missing_widget`

#### `trial_catalysts_app`

**medium** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Healthcare Research Data' at http://localhost:7808. Make the user controls functional. The experience needs Trial Catalysts (`trial_catalysts`, table) using `/trial-catalysts` for upcoming clinical trial readouts; user controls: Ticker (`ticker`, endpoint) from `/tickers`; columns: ticker (text), phase (text), readout_date (dateString). Organize it as app 'Catalyst Filter' with tabs Catalysts (trial_catalysts). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Catalyst Filter" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Healthcare Research Data/trial_catalysts` on tab `catalysts` → `missing_widget`

#### `trial_param_review`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a healthcare-research analyst covering clinical catalysts and pipelines. The workspace must cover upcoming clinical trial readouts. The workspace must cover pipeline distribution by phase. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Keep these source-contract anchors: `ticker` and `phase`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vendor_sla_table_app`

**medium** · category: platform · specification: -

> Create a usable vendor service levels workflow for a vendor-operations manager. The workspace must cover vendor SLA state with breach flags. Analysts need to inspect vendor, status, latency milliseconds, breach. Leave the complete working workspace open for review. The source contract must retain `status` and `vendor`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vix_history`

**medium** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Vol Desk Data' at http://localhost:7801. Make the user controls functional. The experience needs VIX History (`vix_history`, table) using `/vix-history` for daily CBOE VIX closes with returns; user controls: Window (`window`, number); columns: date (dateString), close (number), return_pct (number, percent, greenRed). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vol Desk Data/vix_history` → `missing_widget`

#### `vol_param_cockpit`

**hard** · category: platform · specification: -

> Build a volatility analyst a dependable volatility and derivatives workspace. The workspace must cover screen names by implied-vol criteria. The workspace must cover daily CBOE VIX closes with returns. The workspace must cover morning volatility commentary. Analysts need to inspect date, close, return percentage. An analyst can filter the analysis by ticker. An analyst can choose the relevant business date. An analyst can adjust the relevant numeric scope. An analyst can toggle the relevant screening constraint. Leave the complete working workspace open for review. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vol_screener`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for volatility and derivatives. The workspace must cover screen names by implied-vol criteria. An analyst can filter the analysis by ticker. An analyst can choose the relevant business date. An analyst can toggle the relevant screening constraint. Use `ticker` and `as_of` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vol_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready volatility and derivatives workflow for a volatility analyst. The workspace must cover volatility review filtered by symbol. The workspace must cover current volatility regime score. The workspace must cover daily CBOE VIX closes with returns. Analysts need to inspect date, close, return percentage. An analyst can filter the analysis by ticker. An analyst can toggle the relevant screening constraint. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Vol Symbol Live', 'vol symbol', 'Vol Desk Data', 'AAPL', 'ticker'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Vol Symbol Live", "vol symbol", "Vol Desk Data", "AAPL" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `windowed_vix_slice`

**hard** · category: platform · specification: partially-specified

> Create a usable volatility and derivatives workflow for a volatility analyst. The workspace must cover VIX analysis for a selected window and as-of date. An analyst can choose the relevant business date. An analyst can adjust the relevant numeric scope. The source contract must retain `window` and `as_of`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### settings (20)

#### `alert_metric_app`

**easy** · category: platform · specification: -

> Publish the requested app and open it in Workspace to verify it works. Use 'Surveillance Data' at http://localhost:7807. Implement the requested runtime and refresh behavior. The experience needs Open Alerts (`alert_metric`, metric) using `/alert-count` for open alert count; cache for 15 minutes. Organize it as app 'Alert Settings' with tabs Alerts (alert_metric). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Alert Settings" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Surveillance Data/alert_metric` on tab `alerts` → `missing_widget`

#### `alert_metric_room`

**hard** · category: platform · specification: -

> Build a surveillance analyst a dependable cases and compliance alerts workspace. The workspace must cover open alert count. The workspace must cover notes for one surveillance case. The workspace must cover latest surveillance policy digest. Leave the complete working workspace open for review. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `auction_cache_grid`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for rates and Treasury markets. The workspace must cover cached auction watchlist. Analysts need to inspect auction date, security, size billions. Use `auction_date` and `security` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `catalyst_metric_app`

**medium** · category: platform · specification: explicit

> Publish the requested app and open it in Workspace to verify it works. Use 'Healthcare Research Data' at http://localhost:7808. Implement the requested runtime and refresh behavior. The experience needs Catalysts 30d (`catalyst_metric`, metric) using `/catalyst-count` for catalysts in the next 30 days; refresh every 30 seconds; run on demand. Organize it as app 'Catalyst Settings' with tabs Catalysts (catalyst_metric). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Catalyst Settings" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Healthcare Research Data/catalyst_metric` on tab `catalysts` → `missing_widget`

#### `exception_metric`

**medium** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Execution Desk Data' at http://localhost:7806. Implement the requested runtime and refresh behavior. The experience needs Exceptions (`exception_metric`, metric) using `/exception-count` for open execution exceptions; refresh every 45 seconds; run on demand. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Execution Desk Data/exception_metric` → `missing_widget`

#### `exception_refresh_grid`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for orders and venue quality. The workspace must cover execution exceptions with manual refresh. Analysts need to inspect order ID, symbol, age min. Use `order_id` and `symbol` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `execution_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready orders and venue quality workflow for an execution analyst. The workspace must cover open execution exceptions. The workspace must cover live open orders blotter. The workspace must cover monthly venue scorecard document. Analysts need to inspect order ID, symbol, quantity, status. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Execution Config Live', 'on-demand updates', 'Execution Desk Data', 'urgent'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Execution Config Live", "on-demand updates", "Execution Desk Data", "urgent" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `gas_metric`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Chain TVL Data' at http://localhost:7802. Implement the requested runtime and refresh behavior. The experience needs Gas Now (`gas_metric`, metric) using `/gas-now` for current gas price snapshot; refresh every 30 seconds. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Chain TVL Data/gas_metric` → `missing_widget`

#### `gas_metric_room`

**hard** · category: platform · specification: partially-specified

> Create a usable chain activity and liquidity workflow for a digital-assets analyst. The workspace must cover current gas price snapshot. The workspace must cover written details for one protocol. Leave the complete working workspace open for review. The source contract must retain `protocol`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `gas_refresh_metric`

**hard** · category: platform · specification: partially-specified

> Create a usable chain activity and liquidity workflow for a digital-assets analyst. The workspace must cover auto-refreshing gas snapshot. The source contract must retain `Chain TVL Data`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `healthcare_ship`

**hard** · category: platform · specification: -

> A healthcare-research analyst needs a decision-ready Workspace for clinical catalysts and pipelines. The workspace must cover catalysts in the next 30 days. The workspace must cover upcoming clinical trial readouts. The workspace must cover pipeline distribution by phase. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Catalyst Config Live', 'Catalysts category', 'Healthcare Research Data', '60d', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Catalyst Config Live", "Catalysts category", "Healthcare Research Data", "60d" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `rates_commentary`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Rates Watch Data' at http://localhost:7803. Implement the requested runtime and refresh behavior. The experience needs Rates Commentary (`rates_commentary`, markdown) using `/rates-commentary` for desk commentary on the rates day; user controls: Series (`series`, endpoint) from `/series-options`; cache for 30 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Rates Watch Data/rates_commentary` → `missing_widget`

#### `rates_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover current 2s10s spread in bps. The workspace must cover desk commentary on the rates day. The workspace must cover the Treasury yield curve. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Rates Config Live', 'Macro category', 'Rates Watch Data', '5s30s'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Rates Config Live", "Macro category", "Rates Watch Data", "5s30s" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `runbook_markdown`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for vendor service levels. The workspace must cover configured SLA runbook note. Use `Vendor SLA Data` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `sla_runbook_app`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for vendor service levels. The workspace must cover runbook for SLA escalations. Leave the complete working workspace open for review. Use `Vendor SLA Data` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `surprise_metric_app`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover average EPS surprise last 4 quarters. Leave the complete working workspace open for review. Keep these source-contract anchors: `Earnings Prep Data`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `surprise_metric_room`

**hard** · category: platform · specification: -

> The desk needs a production-ready earnings and estimates workflow for an equity-research analyst. The workspace must cover average EPS surprise last 4 quarters. The workspace must cover preview note for the earnings call. The workspace must cover EPS beat and miss history. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vol_commentary_room`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a volatility analyst covering volatility and derivatives. The workspace must cover morning volatility commentary. The workspace must cover current volatility regime score. Leave the complete working workspace open for review. Keep these source-contract anchors: `desk`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vol_regime_metric`

**easy** · category: platform · specification: -

> Make the requested backend widget available and working in the current view. Use 'Vol Desk Data' at http://localhost:7801. Implement the requested runtime and refresh behavior. The experience needs Vol Regime (`vol_regime_metric`, metric) using `/vol-regime` for current volatility regime score; cache for 15 minutes; run on demand. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vol Desk Data/vol_regime_metric` → `missing_widget`

#### `vol_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready volatility and derivatives workflow for a volatility analyst. The workspace must cover current volatility regime score. The workspace must cover morning volatility commentary. The workspace must cover daily CBOE VIX closes with returns. Analysts need to inspect date, close, return percentage. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Vol Config Live', '15-minute cache', 'Vol Desk Data', 'stress'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Vol Config Live", "15-minute cache", "Vol Desk Data", "stress" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

### types (20)

#### `call_replay_video`

**hard** · category: platform · specification: partially-specified

> Create a usable earnings and estimates workflow for an equity-research analyst. The workspace must cover selected earnings replay video. The source contract must retain `video`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `case_notes_room`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a surveillance analyst covering cases and compliance alerts. The workspace must cover notes for one surveillance case. The workspace must cover latest surveillance policy digest. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `case_id` and `case_scope`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `chains_heatmap_html`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Chain TVL Data' at http://localhost:7802. Choose the native widget type that fits the content. The experience needs Chain Heatmap (`chains_heatmap_html`, html) using `/chains-heatmap` for raw HTML heatmap of chain flows; cache for 15 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Chain TVL Data/chains_heatmap_html` → `missing_widget`

#### `curve_monitor_iframe_app`

**medium** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Rates Watch Data' at http://localhost:7803. Choose the native widget type that fits the content. The experience needs Curve Monitor App (`curve_monitor_iframe`, iframe) using `http://localhost:5173` for embedded standalone curve monitor application. Organize it as app 'Curve Monitor' with tabs Monitor (curve_monitor_iframe). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Curve Monitor" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Rates Watch Data/curve_monitor_iframe` on tab `monitor` → `missing_widget`

#### `earnings_calls_video_app`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover replay library of earnings calls. Leave the complete working workspace open for review. Keep these source-contract anchors: `video`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_calls_video_room`

**hard** · category: platform · specification: -

> Build an equity-research analyst a dependable earnings and estimates workspace. The workspace must cover replay library of earnings calls. The workspace must cover preview note for the earnings call. The workspace must cover average EPS surprise last 4 quarters. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `evidence_files_app`

**hard** · category: platform · specification: partially-specified

> Create a usable cases and compliance alerts workflow for a surveillance analyst. The workspace must cover browse case evidence documents. Leave the complete working workspace open for review. The source contract must retain `file`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `evidence_files_room`

**hard** · category: platform · specification: -

> Build a surveillance analyst a dependable cases and compliance alerts workspace. The workspace must cover browse case evidence documents. The workspace must cover notes for one surveillance case. The workspace must cover open alert count. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `evidence_files_ship`

**hard** · category: platform · specification: -

> Build a surveillance analyst a dependable cases and compliance alerts workspace. The workspace must cover browse case evidence documents. The workspace must cover open alert count. The workspace must cover notes for one surveillance case. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Evidence Live', 'evidence', 'Surveillance Data'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Evidence Live", "evidence", "Surveillance Data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `fda_newsfeed_room`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a healthcare-research analyst covering clinical catalysts and pipelines. The workspace must cover FDA decision and notice feed. The workspace must cover catalysts in the next 30 days. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `therapy_area`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `gas_metric`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Chain TVL Data' at http://localhost:7802. Choose the native widget type that fits the content. The experience needs Gas Now (`gas_metric`, metric) using `/gas-now` for current gas price snapshot; cache for 15 minutes; run on demand. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Chain TVL Data/gas_metric` → `missing_widget`

#### `gas_priority_metric`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a digital-assets analyst covering chain activity and liquidity. The workspace must cover priority gas fee monitor. Keep these source-contract anchors: `Chain TVL Data`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `policy_digest_pdf`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for cases and compliance alerts. The workspace must cover current surveillance policy digest. Use `Surveillance Data` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `policy_digest_pdf_ship`

**hard** · category: platform · specification: -

> A surveillance analyst needs a decision-ready Workspace for cases and compliance alerts. The workspace must cover current surveillance policy digest. The workspace must cover open surveillance alerts. The workspace must cover notes for one surveillance case. Analysts need to inspect alert ID, desk, severity, age days. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Policy Digest Live', 'policy digest', 'Surveillance Data', 'C-2099'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Policy Digest Live", "policy digest", "Surveillance Data", "C-2099" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `sla_newsfeed_app`

**easy** · category: platform · specification: -

> Implement the requested app and confirm it by opening it in Workspace. Use 'Vendor SLA Data' at http://localhost:7804. Choose the native widget type that fits the content. The experience needs Vendor Notices (`sla_newsfeed`, newsfeed) using `/vendor-notices` for vendor incident notices feed. Organize it as app 'Vendor Notices' with tabs Notices (sla_newsfeed). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vendor Notices" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Vendor SLA Data/sla_newsfeed` on tab `notices` → `missing_widget`

#### `sla_newsfeed_ship`

**hard** · category: platform · specification: -

> Build a vendor-operations manager a dependable vendor service levels workspace. The workspace must cover vendor incident notices feed. The workspace must cover count of open SLA breaches. The workspace must cover vendor SLA state with breach flags. Analysts need to inspect vendor, status, latency milliseconds, breach. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Vendor Notice Room', 'notices', 'Vendor SLA Data', 'QuoteStream'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Vendor Notice Room", "notices", "Vendor SLA Data", "QuoteStream" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `venue_packet_pdf_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready orders and venue quality workflow for an execution analyst. The workspace must cover monthly venue scorecard packet. The workspace must cover open execution exceptions. The workspace must cover live open orders blotter. Analysts need to inspect order ID, symbol, quantity, status. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Venue Packet Live', 'venue packet', 'Execution Desk Data', 'EDGX'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Venue Packet Live", "venue packet", "Execution Desk Data", "EDGX" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `venue_pdf`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Execution Desk Data' at http://localhost:7806. Choose the native widget type that fits the content. The experience needs Venue Scorecard (`venue_pdf`, pdf) using `/venue-scorecard` for monthly venue scorecard PDF; cache for 30 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Execution Desk Data/venue_pdf` → `missing_widget`

#### `vol_commentary`

**easy** · category: platform · specification: -

> Register the backend and place the specified widget on the active dashboard. Use 'Vol Desk Data' at http://localhost:7801. Choose the native widget type that fits the content. The experience needs Vol Commentary (`vol_commentary`, markdown) using `/vol-commentary` for morning volatility commentary; user controls: Desk (`desk`, text); cache for 15 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vol Desk Data/vol_commentary` → `missing_widget`

#### `vol_playbook_note`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a volatility analyst covering volatility and derivatives. The workspace must cover written playbook for the vol desk. Keep these source-contract anchors: `section`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):



---

Total: 646 tasks.