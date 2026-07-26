# WorkspaceBench Task Catalog

Auto-generated from the bundled task JSON files — regenerate with
`python scripts/generators/generate_task_catalog.py` after editing tasks.
All three deterministic simulator suites are included.

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

> Call read_widget with origin 'Bench Stark Enterprise' and widget_id 'client_360_client_book_client_accounts'. The widget sits on the active dashboard, so those two arguments are all the call needs.

- Initial workspace: dashboard "Smoke read_widget"; 1 tab(s): overview; 1 seeded widget(s): client_360_client_book_client_accounts({"client": "Atlas Pension", "region": "Americas", "period": "YTD"})
- Allowed tools (1): `read_widget`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_read_widget_level1`

**level1** · category: - · specification: -

> Call read_widget with origin 'Bench Stark Enterprise' and widget_id 'client_360_client_book_client_accounts'. The widget sits on the active dashboard, so those two arguments are all the call needs.

- Initial workspace: dashboard "Smoke read_widget"; 1 tab(s): overview; 1 seeded widget(s): client_360_client_book_client_accounts({"client": "Atlas Pension", "region": "Americas", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `smoke_read_widget_level2`

**level2** · category: - · specification: -

> Call read_widget with origin 'Bench Stark Enterprise' and widget_id 'client_360_client_book_client_accounts'. The widget sits on the active dashboard, so those two arguments are all the call needs.

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



## Suite: workspace-tasks (120 tasks)

### client_advisor (20)

#### `client_review_level0`

**level0** · category: story · specification: -

> On the open Quarterly Client Review dashboard, add Company Fundamentals and Segment Breakdown from Bench Daloopa, both with parameters ticker set to AAPL and period set to 2026Q1. Please have the financial picture and revenue mix ready on the same basis before the client meeting.

- Initial workspace: dashboard "Quarterly Client Review"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Quarterly Client Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "AAPL", "period": "2026Q1"} → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_segment_breakdown` with data_args ⊇ {"ticker": "AAPL", "period": "2026Q1"} → `missing_widget`

#### `client_review_level1`

**level1** · category: story · specification: -

> On the open Quarterly Client Review dashboard, add the company financials and Segment Breakdown from Bench Daloopa, both with parameters ticker set to AAPL and period set to 2026Q1. Please have the financial picture and revenue mix ready on the same basis before the client meeting.

- Initial workspace: dashboard "Quarterly Client Review"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Quarterly Client Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "AAPL", "period": "2026Q1"} → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_segment_breakdown` with data_args ⊇ {"ticker": "AAPL", "period": "2026Q1"} → `missing_widget`

#### `client_review_level2`

**level2** · category: story · specification: -

> On the open Quarterly Client Review dashboard, add Company Fundamentals and Segment Breakdown from Bench Daloopa, both with ticker set to AAPL and period set by the 2026 first-quarter review policy. Please keep the financial picture and revenue mix on the same basis for the client meeting.

- Initial workspace: dashboard "Quarterly Client Review"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Quarterly Client Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "AAPL", "period": "2026Q1"} → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_segment_breakdown` with data_args ⊇ {"ticker": "AAPL", "period": "2026Q1"} → `missing_widget`

#### `client_review_level3`

**level3** · category: story · specification: -

> On the open Quarterly Client Review dashboard, correct the stale Company Fundamentals instance from Bench Daloopa that has parameters ticker MSFT and period 2025Q4 to ticker AAPL and period 2026Q1. The separate Company Fundamentals instance with parameters ticker TSLA and period 2025Q4 belongs to another client conversation and must stay untouched. Also add fresh Company Fundamentals and Segment Breakdown from Bench Daloopa, both with parameters ticker AAPL and period 2026Q1. Keep every other view and note on the dashboard exactly as it is so the review remains ready to explain. Read the Daloopa Tearsheet skill and leave a Client Review Sourcing Note recording the sourcing field its workflow requires for every Daloopa-sourced figure.

- Initial workspace: dashboard "Quarterly Client Review"; 1 tab(s): review; 4 seeded widget(s): daloopa_company_fundamentals({"ticker": "MSFT", "period": "2025Q4"}), daloopa_company_fundamentals({"ticker": "TSLA", "period": "2025Q4"}), daloopa_segment_breakdown({"ticker": "MSFT", "period": "2025Q4"}), daloopa_company_directory({}); 1 seeded generated widget(s): note "Prior Client Review Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Quarterly Client Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥2× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "AAPL", "period": "2026Q1"} on tab `review` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "TSLA", "period": "2025Q4"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_segment_breakdown` with data_args ⊇ {"ticker": "AAPL", "period": "2026Q1"} on tab `review` → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_segment_breakdown` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q4"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Client Review Note" whose content mentions "Prior review: retain the Tesla comparison and Microsoft's 2025Q4 segment mix for the client's follow-up questions." on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Client Review Sourcing" whose content mentions "source_url" on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_4c1` must sit at exactly x=0, y=0, w=20, h=12 on tab `review` → `layout_mismatch`
- **Layout** `w_8a7` must sit at exactly x=20, y=0, w=20, h=12 on tab `review` → `layout_mismatch`
- **Layout** `w_2f9` must sit at exactly x=0, y=12, w=20, h=12 on tab `review` → `layout_mismatch`
- **Layout** `w_6d3` must sit at exactly x=20, y=12, w=20, h=12 on tab `review` → `layout_mismatch`
- **Layout** `w_b45` must sit at exactly x=0, y=24, w=40, h=8 on tab `review` → `layout_mismatch`

#### `client_review_level4`

**level4** · category: story · specification: -

> Build the client's review register before the meeting: add a Client Review Service backend serving a Review Register table, publish Client Review App with Review Register on its Review tab, and instantiate the app. On the open Quarterly Client Review dashboard, add the built Review Register and correct the stale Company Fundamentals instance from Bench Daloopa that has parameters ticker MSFT and period 2025Q4 to ticker AAPL and period 2026Q1. The separate Company Fundamentals instance with parameters ticker TSLA and period 2025Q4 belongs to another client conversation and must stay untouched. Add fresh Company Fundamentals and Segment Breakdown from Bench Daloopa, both with parameters ticker AAPL and period 2026Q1. Keep every other view and note on the dashboard exactly as it is so the review remains ready to explain. Read the Daloopa Tearsheet skill and leave a Client Review Sourcing Note recording the sourcing field its workflow requires for every Daloopa-sourced figure.

- Initial workspace: dashboard "Quarterly Client Review"; 1 tab(s): review; 4 seeded widget(s): daloopa_company_fundamentals({"ticker": "MSFT", "period": "2025Q4"}), daloopa_company_fundamentals({"ticker": "TSLA", "period": "2025Q4"}), daloopa_segment_breakdown({"ticker": "MSFT", "period": "2025Q4"}), daloopa_company_directory({}); 1 seeded generated widget(s): note "Prior Client Review Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Quarterly Client Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Client Review Service/review_register` on tab `review` → `missing_widget`
- **Widget** ≥2× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "AAPL", "period": "2026Q1"} on tab `review` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "TSLA", "period": "2025Q4"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_segment_breakdown` with data_args ⊇ {"ticker": "AAPL", "period": "2026Q1"} on tab `review` → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_segment_breakdown` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q4"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Client Review Note" whose content mentions "Prior review: retain the Tesla comparison and Microsoft's 2025Q4 segment mix for the client's follow-up questions." on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Client Review Sourcing" whose content mentions "source_url" on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_4c1` must sit at exactly x=0, y=0, w=20, h=12 on tab `review` → `layout_mismatch`
- **Layout** `w_8a7` must sit at exactly x=20, y=0, w=20, h=12 on tab `review` → `layout_mismatch`
- **Layout** `w_2f9` must sit at exactly x=0, y=12, w=20, h=12 on tab `review` → `layout_mismatch`
- **Layout** `w_6d3` must sit at exactly x=20, y=12, w=20, h=12 on tab `review` → `layout_mismatch`
- **Layout** `w_b45` must sit at exactly x=0, y=24, w=40, h=8 on tab `review` → `layout_mismatch`
- **Tool result** of `manage_apps` must contain "Client Review App", "Review", "Client Review Service" (agent must actually retrieve the data) → `missing_tool_result`

#### `holdings_watch_level0`

**level0** · category: story · specification: -

> On the open Client Holdings Watch dashboard, correct Live Grid from the Onboarding App for Devs in Getting Started from parameter symbol TSLA to AAPL before the call.

- Initial workspace: dashboard "Client Holdings Watch"; 1 tab(s): watch; 1 seeded widget(s): live_grid_data({"symbol": "TSLA"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Holdings Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Getting Started/live_grid_data` with data_args ⊇ {"symbol": "AAPL"} on tab `watch` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`

#### `holdings_watch_level1`

**level1** · category: story · specification: -

> On the open Client Holdings Watch dashboard, correct the live price watch from the Onboarding App for Devs in Getting Started from parameter symbol TSLA to AAPL before the call.

- Initial workspace: dashboard "Client Holdings Watch"; 1 tab(s): watch; 1 seeded widget(s): live_grid_data({"symbol": "TSLA"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Holdings Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Getting Started/live_grid_data` with data_args ⊇ {"symbol": "AAPL"} on tab `watch` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`

#### `holdings_watch_level2`

**level2** · category: story · specification: -

> On the open Client Holdings Watch dashboard, restore Live Grid from the Onboarding App for Devs in Getting Started from parameter symbol TSLA under the Apple holding policy for the client's Apple holding before the call.

- Initial workspace: dashboard "Client Holdings Watch"; 1 tab(s): watch; 1 seeded widget(s): live_grid_data({"symbol": "TSLA"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Holdings Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Getting Started/live_grid_data` with data_args ⊇ {"symbol": "AAPL"} on tab `watch` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`

#### `holdings_watch_level3`

**level3** · category: story · specification: -

> On the open Client Holdings Watch dashboard, correct the stale Live Grid from the Onboarding App for Devs in Getting Started that has parameter symbol TSLA to AAPL. The separate Live Grid with parameter symbol AAPL is already correct for the client's Apple holding and must stay untouched. Keep every other view and note exactly as it is so the client material stays ready for the call. Read the Finance Tearsheet skill and leave a Holdings Watch Governance Note recording what its workflow says to gather first and the three elements that includes.

- Initial workspace: dashboard "Client Holdings Watch"; 1 tab(s): watch; 3 seeded widget(s): live_grid_data({"symbol": "TSLA"}), live_grid_data({"symbol": "AAPL"}), sparkline_line({}); 1 seeded generated widget(s): note "Prior Client Watch Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Holdings Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `watch` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥2× `Getting Started/live_grid_data` with data_args ⊇ {"symbol": "AAPL"} on tab `watch` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/sparkline_line` on tab `watch` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Client Watch Note" whose content mentions "Prior call: Tesla was discussed as a comparison; retain this note in the client file." on tab `watch` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Holdings Watch Governance" whose content mentions "Gather price action first", "level", "trend", "recent events" on tab `watch` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_c7a` must sit at exactly x=0, y=0, w=20, h=9 on tab `watch` → `layout_mismatch`
- **Layout** `w_91e` must sit at exactly x=20, y=0, w=20, h=9 on tab `watch` → `layout_mismatch`
- **Layout** `w_4d2` must sit at exactly x=0, y=9, w=40, h=10 on tab `watch` → `layout_mismatch`
- **Layout** `w_b86` must sit at exactly x=0, y=19, w=40, h=8 on tab `watch` → `layout_mismatch`

#### `holdings_watch_level4`

**level4** · category: story · specification: -

> Build the client's holdings register before the call: add a Holdings Watch Service backend serving a Holdings Register table, publish Holdings Watch App with Holdings Register on its Watch tab, and instantiate the app. On the open Client Holdings Watch dashboard, add the built Holdings Register and correct the stale Live Grid from the Onboarding App for Devs in Getting Started that has parameter symbol TSLA to AAPL. The separate Live Grid with parameter symbol AAPL is already correct for the client's Apple holding and must stay untouched. Keep every other view and note exactly as it is so the client material stays ready for the call. Read the Finance Tearsheet skill and leave a Holdings Watch Governance Note recording what its workflow says to gather first and the three elements that includes.

- Initial workspace: dashboard "Client Holdings Watch"; 1 tab(s): watch; 3 seeded widget(s): live_grid_data({"symbol": "TSLA"}), live_grid_data({"symbol": "AAPL"}), sparkline_line({}); 1 seeded generated widget(s): note "Prior Client Watch Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Holdings Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `watch` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Holdings Watch Service/holdings_register` on tab `watch` → `missing_widget`
- **Widget** ≥2× `Getting Started/live_grid_data` with data_args ⊇ {"symbol": "AAPL"} on tab `watch` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/sparkline_line` on tab `watch` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Client Watch Note" whose content mentions "Prior call: Tesla was discussed as a comparison; retain this note in the client file." on tab `watch` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Holdings Watch Governance" whose content mentions "Gather price action first", "level", "trend", "recent events" on tab `watch` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_c7a` must sit at exactly x=0, y=0, w=20, h=9 on tab `watch` → `layout_mismatch`
- **Layout** `w_91e` must sit at exactly x=20, y=0, w=20, h=9 on tab `watch` → `layout_mismatch`
- **Layout** `w_4d2` must sit at exactly x=0, y=9, w=40, h=10 on tab `watch` → `layout_mismatch`
- **Layout** `w_b86` must sit at exactly x=0, y=19, w=40, h=8 on tab `watch` → `layout_mismatch`
- **Tool result** of `manage_apps` must contain "Holdings Watch App", "Watch", "Holdings Watch Service" (agent must actually retrieve the data) → `missing_tool_result`

#### `meeting_prep_level0`

**level0** · category: story · specification: -

> On the open Client Call Prep dashboard, read Client Returns from Bench Stark Enterprise's Client 360 with parameters client set to Northstar Endowment and period set to QTD. Before the call, leave a Client Call Performance Note recording the client, fund, return, change, and review status exactly as served.

- Initial workspace: dashboard "Client Call Prep"; 1 tab(s): prep
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Call Prep" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Generated note** ≥1× named ~"Client Call Performance" whose content mentions "Northstar Endowment", "Global Opportunities", "0.0524", "-0.0675", "In Review" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `meeting_prep_level1`

**level1** · category: story · specification: -

> On the open Client Call Prep dashboard, read the client's performance view from Bench Stark Enterprise's Client 360 with parameters client set to Northstar Endowment and period set to QTD. Before the call, leave a Client Call Performance Note recording the client, fund, return, change, and review status exactly as served.

- Initial workspace: dashboard "Client Call Prep"; 1 tab(s): prep
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Call Prep" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Generated note** ≥1× named ~"Client Call Performance" whose content mentions "Northstar Endowment", "Global Opportunities", "0.0524", "-0.0675", "In Review" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `meeting_prep_level2`

**level2** · category: story · specification: -

> On the open Client Call Prep dashboard, read Client Returns from Bench Stark Enterprise's Client 360 for Northstar Endowment with the period set by the quarterly call policy. Before the call, leave a Client Call Performance Note recording the client, fund, return, change, and review status exactly as served.

- Initial workspace: dashboard "Client Call Prep"; 1 tab(s): prep
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Call Prep" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Generated note** ≥1× named ~"Client Call Performance" whose content mentions "Northstar Endowment", "Global Opportunities", "0.0524", "-0.0675", "In Review" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `meeting_prep_level3`

**level3** · category: story · specification: -

> On the open Client Call Prep dashboard, correct the stale Client Returns instance from Bench Stark Enterprise's Client 360 that has parameters client Northstar Endowment and period YTD to client Northstar Endowment and period QTD. The separate Client Returns instance with parameters client Atlas Pension and period YTD belongs to a prior review and must stay untouched. Add a fresh Client Returns for Northstar Endowment and QTD, then read it with those parameters. Keep every other view and note exactly as it is. Before the call, read the Finance Tearsheet skill and leave a Client Call Performance Note recording the client, fund, return, change, and review status exactly as served, plus what the skill's workflow lists last.

- Initial workspace: dashboard "Client Call Prep"; 1 tab(s): prep; 4 seeded widget(s): client_360_portfolio_view_client_returns({"client": "Northstar Endowment", "period": "YTD"}), client_360_portfolio_view_client_returns({"client": "Atlas Pension", "period": "YTD"}), client_360_portfolio_view_exposure_summary({"client": "Meridian Family Office", "period": "MTD"}), client_360_meeting_prep_meeting_agenda({"client": "Horizon Sovereign", "period": "1D"}); 1 seeded generated widget(s): note "Prior Call Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Call Prep" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `prep` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥2× `Bench Stark Enterprise/client_360_portfolio_view_client_returns` with data_args ⊇ {"client": "Northstar Endowment", "period": "QTD"} on tab `prep` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/client_360_portfolio_view_client_returns` with data_args ⊇ {"client": "Atlas Pension", "period": "YTD"} on tab `prep` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/client_360_portfolio_view_exposure_summary` with data_args ⊇ {"client": "Meridian Family Office", "period": "MTD"} on tab `prep` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/client_360_meeting_prep_meeting_agenda` with data_args ⊇ {"client": "Horizon Sovereign", "period": "1D"} on tab `prep` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Call Note" whose content mentions "Prior call: retain the Atlas Pension year-to-date return view and the Meridian exposure follow-up for the next review." on tab `prep` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Client Call Performance" whose content mentions "Northstar Endowment", "Global Opportunities", "0.0524", "-0.0675", "In Review", "short investment conclusion a reader could act on" on tab `prep` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_3b7` must sit at exactly x=0, y=0, w=20, h=14 on tab `prep` → `layout_mismatch`
- **Layout** `w_8d2` must sit at exactly x=20, y=0, w=20, h=14 on tab `prep` → `layout_mismatch`
- **Layout** `w_5f9` must sit at exactly x=0, y=14, w=20, h=14 on tab `prep` → `layout_mismatch`
- **Layout** `w_a64` must sit at exactly x=0, y=28, w=40, h=8 on tab `prep` → `layout_mismatch`
- **Layout** `w_c81` must sit at exactly x=20, y=14, w=20, h=14 on tab `prep` → `layout_mismatch`

#### `meeting_prep_level4`

**level4** · category: story · specification: -

> Build the client's call file before the meeting: add a Call Prep Service backend serving a Call Notes Register table, publish Client Call Prep App with Call Notes Register on its Call Prep tab, and instantiate the app. On the open Client Call Prep dashboard, add the built Call Notes Register and correct the stale Client Returns instance from Bench Stark Enterprise's Client 360 that has parameters client Northstar Endowment and period YTD to client Northstar Endowment and period QTD. The separate Client Returns instance with parameters client Atlas Pension and period YTD belongs to a prior review and must stay untouched. Add a fresh Client Returns for Northstar Endowment and QTD, then read it with those parameters. Keep every other view and note exactly as it is. Before the call, read the Finance Tearsheet skill and leave a Client Call Performance Note recording the client, fund, return, change, and review status exactly as served, plus what the skill's workflow lists last.

- Initial workspace: dashboard "Client Call Prep"; 1 tab(s): prep; 4 seeded widget(s): client_360_portfolio_view_client_returns({"client": "Northstar Endowment", "period": "YTD"}), client_360_portfolio_view_client_returns({"client": "Atlas Pension", "period": "YTD"}), client_360_portfolio_view_exposure_summary({"client": "Meridian Family Office", "period": "MTD"}), client_360_meeting_prep_meeting_agenda({"client": "Horizon Sovereign", "period": "1D"}); 1 seeded generated widget(s): note "Prior Call Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Call Prep" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `prep` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Call Prep Service/call_notes_register` on tab `prep` → `missing_widget`
- **Widget** ≥2× `Bench Stark Enterprise/client_360_portfolio_view_client_returns` with data_args ⊇ {"client": "Northstar Endowment", "period": "QTD"} on tab `prep` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/client_360_portfolio_view_client_returns` with data_args ⊇ {"client": "Atlas Pension", "period": "YTD"} on tab `prep` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/client_360_portfolio_view_exposure_summary` with data_args ⊇ {"client": "Meridian Family Office", "period": "MTD"} on tab `prep` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/client_360_meeting_prep_meeting_agenda` with data_args ⊇ {"client": "Horizon Sovereign", "period": "1D"} on tab `prep` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Call Note" whose content mentions "Prior call: retain the Atlas Pension year-to-date return view and the Meridian exposure follow-up for the next review." on tab `prep` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Client Call Performance" whose content mentions "Northstar Endowment", "Global Opportunities", "0.0524", "-0.0675", "In Review", "short investment conclusion a reader could act on" on tab `prep` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_3b7` must sit at exactly x=0, y=0, w=20, h=14 on tab `prep` → `layout_mismatch`
- **Layout** `w_8d2` must sit at exactly x=20, y=0, w=20, h=14 on tab `prep` → `layout_mismatch`
- **Layout** `w_5f9` must sit at exactly x=0, y=14, w=20, h=14 on tab `prep` → `layout_mismatch`
- **Layout** `w_a64` must sit at exactly x=0, y=28, w=40, h=8 on tab `prep` → `layout_mismatch`
- **Layout** `w_c81` must sit at exactly x=20, y=14, w=20, h=14 on tab `prep` → `layout_mismatch`
- **Tool result** of `manage_apps` must contain "Client Call Prep App", "Call Prep", "Call Prep Service" (agent must actually retrieve the data) → `missing_tool_result`

#### `proposal_pack_level0`

**level0** · category: story · specification: -

> On the open Proposal Pack dashboard, add Company Fundamentals from Bench Daloopa with parameters ticker set to MSFT and period set to 2025Q4, and add Omni Widget with Citations from Widget Examples with parameter type set to markdown. Please have the figures and cited written summary ready before the client meeting.

- Initial workspace: dashboard "Proposal Pack"; 1 tab(s): pack
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Proposal Pack" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q4"} → `missing_widget`
- **Widget** ≥1× `Widget Examples/omni_widget_with_citations` with data_args ⊇ {"type": "markdown"} → `missing_widget`

#### `proposal_pack_level1`

**level1** · category: story · specification: -

> On the open Proposal Pack dashboard, add Company Fundamentals from Bench Daloopa with parameters ticker set to MSFT and period set to 2025Q4, along with the cited written summary from Widget Examples with parameter type set to markdown. Please have both ready to explain before the client meeting.

- Initial workspace: dashboard "Proposal Pack"; 1 tab(s): pack
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Proposal Pack" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q4"} → `missing_widget`
- **Widget** ≥1× `Widget Examples/omni_widget_with_citations` with data_args ⊇ {"type": "markdown"} → `missing_widget`

#### `proposal_pack_level2`

**level2** · category: story · specification: -

> On the open Proposal Pack dashboard, add Company Fundamentals from Bench Daloopa with ticker set to MSFT and period set to 2025Q4, and add Omni Widget with Citations from Widget Examples configured under the written-summary pack policy. Please have the figures and cited narrative ready before the client meeting.

- Initial workspace: dashboard "Proposal Pack"; 1 tab(s): pack
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Proposal Pack" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q4"} → `missing_widget`
- **Widget** ≥1× `Widget Examples/omni_widget_with_citations` with data_args ⊇ {"type": "markdown"} → `missing_widget`

#### `proposal_pack_level3`

**level3** · category: story · specification: -

> On the open Proposal Pack dashboard, correct the stale Company Fundamentals instance from Bench Daloopa that has parameters ticker MSFT and period 2025Q3 to ticker MSFT and period 2025Q4. The separate Company Fundamentals instance with parameters ticker TSLA and period 2025Q4 belongs to another client conversation and must stay untouched, and the existing Omni Widget with Citations from Widget Examples with parameter type chart is the approved visual appendix and must also stay untouched. Add fresh Company Fundamentals from Bench Daloopa with parameters ticker MSFT and period 2025Q4, plus a fresh Omni Widget with Citations from Widget Examples with parameter type markdown. Keep every other view and note on the dashboard exactly as it is so the pack remains ready to explain. Read the Daloopa Tearsheet skill and leave a Proposal Pack Sourcing Note recording the sourcing field its workflow requires for every Daloopa-sourced figure.

- Initial workspace: dashboard "Proposal Pack"; 1 tab(s): pack; 4 seeded widget(s): daloopa_company_fundamentals({"ticker": "MSFT", "period": "2025Q3"}), daloopa_company_fundamentals({"ticker": "TSLA", "period": "2025Q4"}), omni_widget_with_citations({"type": "chart"}), daloopa_company_directory({}); 1 seeded generated widget(s): note "Prior Proposal Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Proposal Pack" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `pack` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥2× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q4"} on tab `pack` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "TSLA", "period": "2025Q4"} on tab `pack` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Widget Examples/omni_widget_with_citations` with data_args ⊇ {"type": "markdown"} on tab `pack` → `missing_widget`
- **Widget** ≥1× `Widget Examples/omni_widget_with_citations` with data_args ⊇ {"type": "chart"} on tab `pack` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` on tab `pack` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Proposal Note" whose content mentions "Prior proposal: retain the Tesla comparison, the approved chart appendix, and the covered-company directory for the client's follow-up questions." on tab `pack` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Proposal Pack Sourcing" whose content mentions "source_url" on tab `pack` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_31c` must sit at exactly x=0, y=0, w=20, h=12 on tab `pack` → `layout_mismatch`
- **Layout** `w_7e2` must sit at exactly x=20, y=0, w=20, h=12 on tab `pack` → `layout_mismatch`
- **Layout** `w_a64` must sit at exactly x=0, y=12, w=40, h=15 on tab `pack` → `layout_mismatch`
- **Layout** `w_c08` must sit at exactly x=0, y=27, w=20, h=12 on tab `pack` → `layout_mismatch`
- **Layout** `w_f51` must sit at exactly x=20, y=27, w=20, h=8 on tab `pack` → `layout_mismatch`

#### `proposal_pack_level4`

**level4** · category: story · specification: -

> Build the client's proposal register before the meeting: add a Client Pack Service backend serving a Pack Register table, publish Client Pack App with Pack Register on its Pack tab, and instantiate the app. On the open Proposal Pack dashboard, add the built Pack Register and correct the stale Company Fundamentals instance from Bench Daloopa that has parameters ticker MSFT and period 2025Q3 to ticker MSFT and period 2025Q4. The separate Company Fundamentals instance with parameters ticker TSLA and period 2025Q4 belongs to another client conversation and must stay untouched, and the existing Omni Widget with Citations from Widget Examples with parameter type chart is the approved visual appendix and must also stay untouched. Add fresh Company Fundamentals from Bench Daloopa with parameters ticker MSFT and period 2025Q4, plus a fresh Omni Widget with Citations from Widget Examples with parameter type markdown. Keep every other view and note on the dashboard exactly as it is so the pack remains ready to explain. Read the Daloopa Tearsheet skill and leave a Proposal Pack Sourcing Note recording the sourcing field its workflow requires for every Daloopa-sourced figure.

- Initial workspace: dashboard "Proposal Pack"; 1 tab(s): pack; 4 seeded widget(s): daloopa_company_fundamentals({"ticker": "MSFT", "period": "2025Q3"}), daloopa_company_fundamentals({"ticker": "TSLA", "period": "2025Q4"}), omni_widget_with_citations({"type": "chart"}), daloopa_company_directory({}); 1 seeded generated widget(s): note "Prior Proposal Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Proposal Pack" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `pack` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Client Pack Service/pack_register` on tab `pack` → `missing_widget`
- **Widget** ≥2× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q4"} on tab `pack` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "TSLA", "period": "2025Q4"} on tab `pack` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Widget Examples/omni_widget_with_citations` with data_args ⊇ {"type": "markdown"} on tab `pack` → `missing_widget`
- **Widget** ≥1× `Widget Examples/omni_widget_with_citations` with data_args ⊇ {"type": "chart"} on tab `pack` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` on tab `pack` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Proposal Note" whose content mentions "Prior proposal: retain the Tesla comparison, the approved chart appendix, and the covered-company directory for the client's follow-up questions." on tab `pack` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Proposal Pack Sourcing" whose content mentions "source_url" on tab `pack` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_31c` must sit at exactly x=0, y=0, w=20, h=12 on tab `pack` → `layout_mismatch`
- **Layout** `w_7e2` must sit at exactly x=20, y=0, w=20, h=12 on tab `pack` → `layout_mismatch`
- **Layout** `w_a64` must sit at exactly x=0, y=12, w=40, h=15 on tab `pack` → `layout_mismatch`
- **Layout** `w_c08` must sit at exactly x=0, y=27, w=20, h=12 on tab `pack` → `layout_mismatch`
- **Layout** `w_f51` must sit at exactly x=20, y=27, w=20, h=8 on tab `pack` → `layout_mismatch`
- **Tool result** of `manage_apps` must contain "Client Pack App", "Pack", "Client Pack Service" (agent must actually retrieve the data) → `missing_tool_result`

### compliance_risk (20)

#### `alert_sweep_level0`

**level0** · category: story · specification: -

> On the open Alert Sweep dashboard, add Open Alert Metrics and Alert Trend from Bench Stark Enterprise's Compliance Surveillance Hub, both with parameters severity set to High, status set to Open, and period set to MTD.

- Initial workspace: dashboard "Alert Sweep"; 1 tab(s): sweep
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Alert Sweep" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` with data_args ⊇ {"severity": "High", "status": "Open", "period": "MTD"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_alert_trend` with data_args ⊇ {"severity": "High", "status": "Open", "period": "MTD"} → `missing_widget`

#### `alert_sweep_level1`

**level1** · category: story · specification: -

> On the open Alert Sweep dashboard, add the headline number for the alert queue and Alert Trend from Bench Stark Enterprise's Compliance Surveillance Hub. Use parameters severity High, status Open, and period MTD for both.

- Initial workspace: dashboard "Alert Sweep"; 1 tab(s): sweep
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Alert Sweep" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` with data_args ⊇ {"severity": "High", "status": "Open", "period": "MTD"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_alert_trend` with data_args ⊇ {"severity": "High", "status": "Open", "period": "MTD"} → `missing_widget`

#### `alert_sweep_level2`

**level2** · category: story · specification: -

> On the open Alert Sweep dashboard, add Open Alert Metrics and Alert Trend from Bench Stark Enterprise's Compliance Surveillance Hub, both with severity set to High, period set to MTD, and status set by the open-items sweep policy.

- Initial workspace: dashboard "Alert Sweep"; 1 tab(s): sweep
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Alert Sweep" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` with data_args ⊇ {"severity": "High", "status": "Open", "period": "MTD"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_alert_trend` with data_args ⊇ {"severity": "High", "status": "Open", "period": "MTD"} → `missing_widget`

#### `alert_sweep_level3`

**level3** · category: story · specification: -

> On the open Alert Sweep dashboard, correct the stale Open Alert Metrics instance from Bench Stark Enterprise's Compliance Surveillance Hub that has parameters severity Medium, status Closed, and period YTD to severity High, status Open, and period MTD. The separate Open Alert Metrics instance with parameters severity Low, status In Review, and period QTD is already correct for the quarterly review cut and must stay untouched. Also add fresh Open Alert Metrics and Alert Trend from the same app and origin, both with parameters severity High, status Open, and period MTD. Keep every other view and record on the dashboard exactly as it is so the sweep evidence remains intact. Read the Finance Guidance Tracker skill and leave an Alert Sweep Evidence Note recording what its workflow lists last.

- Initial workspace: dashboard "Alert Sweep"; 1 tab(s): sweep; 3 seeded widget(s): compliance_surveillance_hub_alerts_open_alert_metrics({"severity": "Medium", "status": "Closed", "period": "YTD"}), compliance_surveillance_hub_alerts_alert_trend({"severity": "Low", "status": "In Review", "period": "QTD"}), compliance_surveillance_hub_alerts_open_alert_metrics({"severity": "Low", "status": "In Review", "period": "QTD"}); 1 seeded generated widget(s): note "Prior Sweep Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Alert Sweep" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `sweep` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥2× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` with data_args ⊇ {"severity": "High", "status": "Open", "period": "MTD"} on tab `sweep` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` with data_args ⊇ {"severity": "Low", "status": "In Review", "period": "QTD"} on tab `sweep` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_alert_trend` with data_args ⊇ {"severity": "High", "status": "Open", "period": "MTD"} on tab `sweep` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_alert_trend` with data_args ⊇ {"severity": "Low", "status": "In Review", "period": "QTD"} on tab `sweep` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Sweep Note" whose content mentions "Prior sweep: retain the Medium-severity closed-item sample for the audit file." on tab `sweep` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Alert Sweep Evidence" whose content mentions "evidence gaps - the claims currently supported by nothing you can point to" on tab `sweep` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_a4b` must sit at exactly x=0, y=0, w=40, h=5 on tab `sweep` → `layout_mismatch`
- **Layout** `w_783` must sit at exactly x=0, y=5, w=20, h=14 on tab `sweep` → `layout_mismatch`
- **Layout** `w_ddd` must sit at exactly x=20, y=5, w=20, h=8 on tab `sweep` → `layout_mismatch`
- **Layout** `w_a93` must sit at exactly x=20, y=13, w=20, h=5 on tab `sweep` → `layout_mismatch`

#### `alert_sweep_level4`

**level4** · category: story · specification: -

> Build the sweep file: add a Sweep File Service backend serving a Sweep Register table, publish Sweep File App with Sweep Register on its Register tab, and instantiate the app. On the open Alert Sweep dashboard, add the built Sweep Register and correct the stale Open Alert Metrics instance from Bench Stark Enterprise's Compliance Surveillance Hub that has parameters severity Medium, status Closed, and period YTD to severity High, status Open, and period MTD. The separate Open Alert Metrics instance with parameters severity Low, status In Review, and period QTD is already correct for the quarterly review cut and must stay untouched. Add fresh Open Alert Metrics and Alert Trend from the same app and origin, both with parameters severity High, status Open, and period MTD. Keep every other view and record on the dashboard exactly as it is so the sweep evidence remains intact. Read the Finance Guidance Tracker skill and leave an Alert Sweep Evidence Note recording what its workflow lists last.

- Initial workspace: dashboard "Alert Sweep"; 1 tab(s): sweep; 3 seeded widget(s): compliance_surveillance_hub_alerts_open_alert_metrics({"severity": "Medium", "status": "Closed", "period": "YTD"}), compliance_surveillance_hub_alerts_alert_trend({"severity": "Low", "status": "In Review", "period": "QTD"}), compliance_surveillance_hub_alerts_open_alert_metrics({"severity": "Low", "status": "In Review", "period": "QTD"}); 1 seeded generated widget(s): note "Prior Sweep Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Alert Sweep" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `sweep` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Sweep File Service/sweep_register` on tab `sweep` → `missing_widget`
- **Widget** ≥2× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` with data_args ⊇ {"severity": "High", "status": "Open", "period": "MTD"} on tab `sweep` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` with data_args ⊇ {"severity": "Low", "status": "In Review", "period": "QTD"} on tab `sweep` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_alert_trend` with data_args ⊇ {"severity": "High", "status": "Open", "period": "MTD"} on tab `sweep` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_alert_trend` with data_args ⊇ {"severity": "Low", "status": "In Review", "period": "QTD"} on tab `sweep` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Sweep Note" whose content mentions "Prior sweep: retain the Medium-severity closed-item sample for the audit file." on tab `sweep` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Alert Sweep Evidence" whose content mentions "evidence gaps - the claims currently supported by nothing you can point to" on tab `sweep` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_a4b` must sit at exactly x=0, y=0, w=40, h=5 on tab `sweep` → `layout_mismatch`
- **Layout** `w_783` must sit at exactly x=0, y=5, w=20, h=14 on tab `sweep` → `layout_mismatch`
- **Layout** `w_ddd` must sit at exactly x=20, y=5, w=20, h=8 on tab `sweep` → `layout_mismatch`
- **Layout** `w_a93` must sit at exactly x=20, y=13, w=20, h=5 on tab `sweep` → `layout_mismatch`
- **Tool result** of `manage_apps` must contain "Sweep File App", "Register", "Sweep File Service" (agent must actually retrieve the data) → `missing_tool_result`

#### `breach_repair_level0`

**level0** · category: story · specification: -

> On the open Breach Review dashboard, repair Policy Breaches from Bench Stark Enterprise's Compliance Surveillance Hub by setting the parameters severity to High, status to Open, and period to QTD.

- Initial workspace: dashboard "Breach Review"; 1 tab(s): review; 1 seeded widget(s): compliance_surveillance_hub_personal_trading_policy_breaches({"severity": "High", "status": "Closed", "period": "1Y"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Breach Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_personal_trading_policy_breaches` with data_args ⊇ {"severity": "High", "status": "Open", "period": "QTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`

#### `breach_repair_level1`

**level1** · category: story · specification: -

> On the open Breach Review dashboard, repair the personal-trading breaches from Bench Stark Enterprise's Compliance Surveillance Hub by setting the parameters severity to High, status to Open, and period to QTD.

- Initial workspace: dashboard "Breach Review"; 1 tab(s): review; 1 seeded widget(s): compliance_surveillance_hub_personal_trading_policy_breaches({"severity": "High", "status": "Closed", "period": "1Y"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Breach Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_personal_trading_policy_breaches` with data_args ⊇ {"severity": "High", "status": "Open", "period": "QTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`

#### `breach_repair_level2`

**level2** · category: story · specification: -

> On the open Breach Review dashboard, restore Policy Breaches from Bench Stark Enterprise's Compliance Surveillance Hub to severity High and status Open, with the period configured under the quarter-under-review policy.

- Initial workspace: dashboard "Breach Review"; 1 tab(s): review; 1 seeded widget(s): compliance_surveillance_hub_personal_trading_policy_breaches({"severity": "High", "status": "Closed", "period": "1Y"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Breach Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_personal_trading_policy_breaches` with data_args ⊇ {"severity": "High", "status": "Open", "period": "QTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`

#### `breach_repair_level3`

**level3** · category: story · specification: -

> On the open Breach Review dashboard, repair the Policy Breaches view from Bench Stark Enterprise's Compliance Surveillance Hub that has parameters severity High, status Closed, and period 1Y: restore it to severity High, status Open, and period QTD. The separate Policy Breaches view with parameters severity Low, status In Review, and period MTD is already correct for its review cut and must not be changed. Keep every other view and record exactly as it is so the breach evidence remains intact. Read the Finance Guidance Tracker skill and leave a Breach Review Evidence Note recording what its workflow lists last.

- Initial workspace: dashboard "Breach Review"; 1 tab(s): review; 3 seeded widget(s): compliance_surveillance_hub_personal_trading_policy_breaches({"severity": "High", "status": "Closed", "period": "1Y"}), compliance_surveillance_hub_personal_trading_policy_breaches({"severity": "Low", "status": "In Review", "period": "MTD"}), compliance_surveillance_hub_personal_trading_pre_clearance_queue({"severity": "Medium", "status": "Approved", "period": "YTD"}); 1 seeded generated widget(s): note "Prior Breach Review Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Breach Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_personal_trading_policy_breaches` with data_args ⊇ {"severity": "High", "status": "Open", "period": "QTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_personal_trading_policy_breaches` with data_args ⊇ {"severity": "Low", "status": "In Review", "period": "MTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_personal_trading_pre_clearance_queue` with data_args ⊇ {"severity": "Medium", "status": "Approved", "period": "YTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Breach Review Note" whose content mentions "Prior review: retain the approved pre-clearance sample as evidence for the audit file." on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Breach Review Evidence Note" whose content mentions "evidence gaps" on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_b2b` must sit at exactly x=0, y=0, w=20, h=14 on tab `review` → `layout_mismatch`
- **Layout** `w_7b8` must sit at exactly x=20, y=0, w=20, h=14 on tab `review` → `layout_mismatch`
- **Layout** `w_a00` must sit at exactly x=0, y=14, w=20, h=14 on tab `review` → `layout_mismatch`
- **Layout** `w_4aa` must sit at exactly x=20, y=14, w=20, h=8 on tab `review` → `layout_mismatch`

#### `breach_repair_level4`

**level4** · category: story · specification: -

> Build the breach file: add a Breach Watch Service backend serving a Breach Register table, publish Breach Watch App with Breach Register on its Register tab, and instantiate the app. On the open Breach Review dashboard, add the built Breach Register and repair the Policy Breaches view from Bench Stark Enterprise's Compliance Surveillance Hub that has parameters severity High, status Closed, and period 1Y: restore it to severity High, status Open, and period QTD. The separate Policy Breaches view with parameters severity Low, status In Review, and period MTD is already correct for its review cut and must not be changed. Keep every other view and record exactly as it is so the breach evidence remains intact. Read the Finance Guidance Tracker skill and leave a Breach Review Evidence Note recording what its workflow lists last.

- Initial workspace: dashboard "Breach Review"; 1 tab(s): review; 3 seeded widget(s): compliance_surveillance_hub_personal_trading_policy_breaches({"severity": "High", "status": "Closed", "period": "1Y"}), compliance_surveillance_hub_personal_trading_policy_breaches({"severity": "Low", "status": "In Review", "period": "MTD"}), compliance_surveillance_hub_personal_trading_pre_clearance_queue({"severity": "Medium", "status": "Approved", "period": "YTD"}); 1 seeded generated widget(s): note "Prior Breach Review Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Breach Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Breach Watch Service/breach_register` on tab `review` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_personal_trading_policy_breaches` with data_args ⊇ {"severity": "High", "status": "Open", "period": "QTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_personal_trading_policy_breaches` with data_args ⊇ {"severity": "Low", "status": "In Review", "period": "MTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_personal_trading_pre_clearance_queue` with data_args ⊇ {"severity": "Medium", "status": "Approved", "period": "YTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Breach Review Note" whose content mentions "Prior review: retain the approved pre-clearance sample as evidence for the audit file." on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Breach Review Evidence Note" whose content mentions "evidence gaps" on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_b2b` must sit at exactly x=0, y=0, w=20, h=14 on tab `review` → `layout_mismatch`
- **Layout** `w_7b8` must sit at exactly x=20, y=0, w=20, h=14 on tab `review` → `layout_mismatch`
- **Layout** `w_a00` must sit at exactly x=0, y=14, w=20, h=14 on tab `review` → `layout_mismatch`
- **Layout** `w_4aa` must sit at exactly x=20, y=14, w=20, h=8 on tab `review` → `layout_mismatch`

#### `case_handoff_level0`

**level0** · category: story · specification: -

> On the open Case Review dashboard, read Expert Calls from Bench Stark Enterprise's MNPI & Research Review with parameters status set to In Review, severity set to High, and period set to MTD. Leave a Case Handoff Note recording the returned In Review fund and both exact scores as evidence for the reviewing team.

- Initial workspace: dashboard "Case Review"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Case Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Generated note** ≥1× named ~"Case Handoff Note" whose content mentions "Global Opportunities", "89.96", "21.55" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `case_handoff_level1`

**level1** · category: story · specification: -

> On the open Case Review dashboard, read the expert-network log from Bench Stark Enterprise's MNPI & Research Review with parameters status In Review, severity High, and period MTD. Leave a Case Handoff Note recording the returned In Review fund and both exact scores as evidence for the reviewing team.

- Initial workspace: dashboard "Case Review"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Case Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Generated note** ≥1× named ~"Case Handoff Note" whose content mentions "Global Opportunities", "89.96", "21.55" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `case_handoff_level2`

**level2** · category: story · specification: -

> On the open Case Review dashboard, read Expert Calls from Bench Stark Enterprise's MNPI & Research Review with status In Review, period MTD, and severity set by the escalation policy. Leave a Case Handoff Note recording the returned In Review fund and both exact scores as evidence for the reviewing team.

- Initial workspace: dashboard "Case Review"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Case Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Generated note** ≥1× named ~"Case Handoff Note" whose content mentions "Global Opportunities", "89.96", "21.55" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `case_handoff_level3`

**level3** · category: story · specification: -

> On the open Case Review dashboard, read Expert Calls from Bench Stark Enterprise's MNPI & Research Review with parameters status In Review, severity High, and period MTD, keeping everything already on the dashboard exactly as it is. Read the Finance Earnings Prep skill and leave a Case Handoff Note recording the returned In Review fund and both exact scores, plus the transcript-tone signal the skill identifies and what it often precedes.

- Initial workspace: dashboard "Case Review"; 1 tab(s): review; 2 seeded widget(s): mnpi_research_review_mnpi_log_expert_calls({"status": "Open", "severity": "Low", "period": "YTD"}), mnpi_research_review_mnpi_log_wall_crossings({"status": "Closed", "severity": "Medium", "period": "QTD"}); 1 seeded generated widget(s): note "Prior Case Review Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Case Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/mnpi_research_review_mnpi_log_expert_calls` with data_args ⊇ {"status": "Open", "severity": "Low", "period": "YTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/mnpi_research_review_mnpi_log_wall_crossings` with data_args ⊇ {"status": "Closed", "severity": "Medium", "period": "QTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Case Review Note" whose content mentions "Prior review: retain the closed Medium-severity wall-crossing sample as audit evidence." on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Case Handoff Note" whose content mentions "Global Opportunities", "89.96", "21.55", "hedged language", "precedes the numbers" on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_71a` must sit at exactly x=0, y=0, w=20, h=14 on tab `review` → `layout_mismatch`
- **Layout** `w_168` must sit at exactly x=20, y=0, w=20, h=14 on tab `review` → `layout_mismatch`
- **Layout** `w_a2e` must sit at exactly x=0, y=14, w=20, h=8 on tab `review` → `layout_mismatch`

#### `case_handoff_level4`

**level4** · category: story · specification: -

> Build the case file for handoff: add a Case File Service backend serving a Case Register table, publish Case File App with Case Register on its Cases tab, and instantiate the app. On the open Case Review dashboard, add the built Case Register, keeping everything already there exactly as it is. Read Expert Calls from Bench Stark Enterprise's MNPI & Research Review with parameters status In Review, severity High, and period MTD. Read the Finance Earnings Prep skill and leave a Case Handoff Note recording the returned In Review fund and both exact scores, plus the transcript-tone signal the skill identifies and what it often precedes. Hand the follow-up to the reviewing team.

- Initial workspace: dashboard "Case Review"; 1 tab(s): review; 2 seeded widget(s): mnpi_research_review_mnpi_log_expert_calls({"status": "Open", "severity": "Low", "period": "YTD"}), mnpi_research_review_mnpi_log_wall_crossings({"status": "Closed", "severity": "Medium", "period": "QTD"}); 1 seeded generated widget(s): note "Prior Case Review Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Case Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Case File Service/case_register` on tab `review` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/mnpi_research_review_mnpi_log_expert_calls` with data_args ⊇ {"status": "Open", "severity": "Low", "period": "YTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/mnpi_research_review_mnpi_log_wall_crossings` with data_args ⊇ {"status": "Closed", "severity": "Medium", "period": "QTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Case Review Note" whose content mentions "Prior review: retain the closed Medium-severity wall-crossing sample as audit evidence." on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Case Handoff Note" whose content mentions "Global Opportunities", "89.96", "21.55", "hedged language", "precedes the numbers" on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_71a` must sit at exactly x=0, y=0, w=20, h=14 on tab `review` → `layout_mismatch`
- **Layout** `w_168` must sit at exactly x=20, y=0, w=20, h=14 on tab `review` → `layout_mismatch`
- **Layout** `w_a2e` must sit at exactly x=0, y=14, w=20, h=8 on tab `review` → `layout_mismatch`
- **Tool result** of `manage_apps` must contain "Case File App", "Cases", "Case File Service" (agent must actually retrieve the data) → `missing_tool_result`

#### `var_monitor_level0`

**level0** · category: story · specification: -

> On the open Shock Watch dashboard, add VaR Trend from Bench Stark Enterprise's Risk & Exposure Monitor with parameters portfolio set to Long/Short Equity, scenario set to Rates +100bp, and period set to YTD.

- Initial workspace: dashboard "Shock Watch"; 1 tab(s): watch
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Shock Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_var_trend` with data_args ⊇ {"portfolio": "Long/Short Equity", "scenario": "Rates +100bp", "period": "YTD"} on tab `watch` → `missing_widget`

#### `var_monitor_level1`

**level1** · category: story · specification: -

> On the open Shock Watch dashboard, add the value-at-risk trend from Bench Stark Enterprise's Risk & Exposure Monitor with parameters portfolio Long/Short Equity, scenario Rates +100bp, and period YTD.

- Initial workspace: dashboard "Shock Watch"; 1 tab(s): watch
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Shock Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_var_trend` with data_args ⊇ {"portfolio": "Long/Short Equity", "scenario": "Rates +100bp", "period": "YTD"} on tab `watch` → `missing_widget`

#### `var_monitor_level2`

**level2** · category: story · specification: -

> On the open Shock Watch dashboard, add VaR Trend from Bench Stark Enterprise's Risk & Exposure Monitor with portfolio set to Long/Short Equity, period set to YTD, and scenario set by the rates-shock policy.

- Initial workspace: dashboard "Shock Watch"; 1 tab(s): watch
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Shock Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_var_trend` with data_args ⊇ {"portfolio": "Long/Short Equity", "scenario": "Rates +100bp", "period": "YTD"} on tab `watch` → `missing_widget`

#### `var_monitor_level3`

**level3** · category: story · specification: -

> On the open Shock Watch dashboard, correct the stale VaR Trend from Bench Stark Enterprise's Risk & Exposure Monitor that has parameters portfolio Global Equity, scenario Equity -10%, and period QTD to portfolio Long/Short Equity, scenario Rates +100bp, and period YTD. The separate VaR Trend with parameters portfolio Credit Opportunities, scenario Credit +150bp, and period MTD is already correct for the credit book and must stay untouched. Add a fresh VaR Trend for the same Long/Short Equity, Rates +100bp, YTD cut, and leave every other view and record exactly as it is so the risk evidence remains intact. Read the Daloopa Inflection skill and leave a Shock Watch Governance Note recording the growth cadence it says to compute first and what it flags as inflections.

- Initial workspace: dashboard "Shock Watch"; 1 tab(s): watch; 3 seeded widget(s): risk_exposure_monitor_dashboard_var_trend({"portfolio": "Global Equity", "scenario": "Equity -10%", "period": "QTD"}), risk_exposure_monitor_dashboard_risk_snapshot({"portfolio": "Global Equity", "scenario": "Equity -10%", "period": "YTD"}), risk_exposure_monitor_dashboard_var_trend({"portfolio": "Credit Opportunities", "scenario": "Credit +150bp", "period": "MTD"}); 1 seeded generated widget(s): note "Prior Shock Review Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Shock Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `watch` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥2× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_var_trend` with data_args ⊇ {"portfolio": "Long/Short Equity", "scenario": "Rates +100bp", "period": "YTD"} on tab `watch` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_var_trend` with data_args ⊇ {"portfolio": "Credit Opportunities", "scenario": "Credit +150bp", "period": "MTD"} on tab `watch` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_risk_snapshot` with data_args ⊇ {"portfolio": "Global Equity", "scenario": "Equity -10%", "period": "YTD"} on tab `watch` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Shock Review Note" whose content mentions "Prior review: retain the Global Equity downside sample as evidence for the limit file." on tab `watch` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Shock Watch Governance" whose content mentions "quarter-over-quarter growth per series", "growth-rate reversals" on tab `watch` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_42c` must sit at exactly x=0, y=0, w=20, h=14 on tab `watch` → `layout_mismatch`
- **Layout** `w_b7c` must sit at exactly x=20, y=0, w=20, h=5 on tab `watch` → `layout_mismatch`
- **Layout** `w_e4b` must sit at exactly x=20, y=5, w=20, h=8 on tab `watch` → `layout_mismatch`
- **Layout** `w_a9e` must sit at exactly x=20, y=13, w=20, h=14 on tab `watch` → `layout_mismatch`

#### `var_monitor_level4`

**level4** · category: story · specification: -

> Build the rates-shock file: add a Shock Watch Service backend serving a Shock Register table, publish Shock Watch App with Shock Register on its Register tab, and instantiate the app. On the open Shock Watch dashboard, add the built Shock Register and correct the stale VaR Trend from Bench Stark Enterprise's Risk & Exposure Monitor that has parameters portfolio Global Equity, scenario Equity -10%, and period QTD to portfolio Long/Short Equity, scenario Rates +100bp, and period YTD. The separate VaR Trend with parameters portfolio Credit Opportunities, scenario Credit +150bp, and period MTD is already correct for the credit book and must stay untouched. Add a fresh VaR Trend for the same Long/Short Equity, Rates +100bp, YTD cut. Keep every other view and record exactly as it is so the risk evidence remains intact. Read the Daloopa Inflection skill and leave a Shock Watch Governance Note recording the growth cadence it says to compute first and what it flags as inflections.

- Initial workspace: dashboard "Shock Watch"; 1 tab(s): watch; 3 seeded widget(s): risk_exposure_monitor_dashboard_var_trend({"portfolio": "Global Equity", "scenario": "Equity -10%", "period": "QTD"}), risk_exposure_monitor_dashboard_risk_snapshot({"portfolio": "Global Equity", "scenario": "Equity -10%", "period": "YTD"}), risk_exposure_monitor_dashboard_var_trend({"portfolio": "Credit Opportunities", "scenario": "Credit +150bp", "period": "MTD"}); 1 seeded generated widget(s): note "Prior Shock Review Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Shock Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `watch` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Shock Watch Service/shock_register` on tab `watch` → `missing_widget`
- **Widget** ≥2× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_var_trend` with data_args ⊇ {"portfolio": "Long/Short Equity", "scenario": "Rates +100bp", "period": "YTD"} on tab `watch` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_var_trend` with data_args ⊇ {"portfolio": "Credit Opportunities", "scenario": "Credit +150bp", "period": "MTD"} on tab `watch` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_risk_snapshot` with data_args ⊇ {"portfolio": "Global Equity", "scenario": "Equity -10%", "period": "YTD"} on tab `watch` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Shock Review Note" whose content mentions "Prior review: retain the Global Equity downside sample as evidence for the limit file." on tab `watch` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Shock Watch Governance" whose content mentions "quarter-over-quarter growth per series", "growth-rate reversals" on tab `watch` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_42c` must sit at exactly x=0, y=0, w=20, h=14 on tab `watch` → `layout_mismatch`
- **Layout** `w_b7c` must sit at exactly x=20, y=0, w=20, h=5 on tab `watch` → `layout_mismatch`
- **Layout** `w_e4b` must sit at exactly x=20, y=5, w=20, h=8 on tab `watch` → `layout_mismatch`
- **Layout** `w_a9e` must sit at exactly x=20, y=13, w=20, h=14 on tab `watch` → `layout_mismatch`
- **Tool result** of `manage_apps` must contain "Shock Watch App", "Register", "Shock Watch Service" (agent must actually retrieve the data) → `missing_tool_result`

### fund_operations (20)

#### `document_room_level0`

**level0** · category: story · specification: -

> On the open Filing Room dashboard, add Document Search from Bench Daloopa with parameters ticker set to AAPL and doc_type set to 10-K, then add Multi PDF Viewer - URL from Getting Started beside it - the audit pull is due before cutoff.

- Initial workspace: dashboard "Filing Room"; 1 tab(s): filings
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Daloopa/daloopa_document_search` with data_args ⊇ {"ticker": "AAPL", "doc_type": "10-K"} → `missing_widget`
- **Widget** ≥1× `Getting Started/multi_pdf_url` → `missing_widget`

#### `document_room_level1`

**level1** · category: story · specification: -

> Get the filings search from Bench Daloopa onto the open Filing Room dashboard for ticker AAPL and doc_type 10-K, with Multi PDF Viewer - URL from Getting Started beside it - audit needs the room checked before cutoff.

- Initial workspace: dashboard "Filing Room"; 1 tab(s): filings
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Daloopa/daloopa_document_search` with data_args ⊇ {"ticker": "AAPL", "doc_type": "10-K"} → `missing_widget`
- **Widget** ≥1× `Getting Started/multi_pdf_url` → `missing_widget`

#### `document_room_level2`

**level2** · category: story · specification: -

> Filing Room before cutoff: on the open dashboard, add Document Search from Bench Daloopa for ticker AAPL, with document type set by the annual-report pull policy. Put Multi PDF Viewer - URL from Getting Started beside it.

- Initial workspace: dashboard "Filing Room"; 1 tab(s): filings
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Daloopa/daloopa_document_search` with data_args ⊇ {"ticker": "AAPL", "doc_type": "10-K"} → `missing_widget`
- **Widget** ≥1× `Getting Started/multi_pdf_url` → `missing_widget`

#### `document_room_level3`

**level3** · category: story · specification: -

> On the open Filing Room dashboard, add Document Search from Bench Daloopa for ticker AAPL and doc_type 10-K; put Multi PDF Viewer - URL from Getting Started beside it. Keep everything already there exactly as is. Read the Daloopa Tearsheet skill; leave a Filing Room Governance note recording the identifier its final step says every Daloopa-sourced figure must be cited with.

- Initial workspace: dashboard "Filing Room"; 1 tab(s): filings; 2 seeded widget(s): daloopa_document_search({"ticker": "MSFT", "doc_type": "10-Q"}), daloopa_company_directory({}); 1 seeded generated widget(s): note "Prior Filing Sign-off"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Filing Room" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `filings` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Daloopa/daloopa_document_search` with data_args ⊇ {"ticker": "AAPL", "doc_type": "10-K"} on tab `filings` → `missing_widget`
- **Widget** ≥1× `Getting Started/multi_pdf_url` on tab `filings` → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_document_search` with data_args ⊇ {"ticker": "MSFT", "doc_type": "10-Q"} on tab `filings` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` on tab `filings` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Filing Sign-off" whose content mentions "Prior filing pull: MSFT quarterly filing checked and signed off." on tab `filings` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Filing Room Governance" whose content mentions "source_url" on tab `filings` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_290` must sit at exactly x=0, y=0, w=20, h=12 on tab `filings` → `layout_mismatch`
- **Layout** `w_810` must sit at exactly x=20, y=0, w=20, h=12 on tab `filings` → `layout_mismatch`
- **Layout** `w_72a` must sit at exactly x=0, y=12, w=20, h=8 on tab `filings` → `layout_mismatch`

#### `document_room_level4`

**level4** · category: story · specification: -

> Build the filing room service before the audit cutoff: add a Filing Room Service backend serving a Filing Register table; publish Filing Room App with Filing Register on its Filings tab; instantiate the app. On the open Filing Room dashboard, add the built Filing Register, Document Search from Bench Daloopa for ticker AAPL and doc_type 10-K, and Multi PDF Viewer - URL from Getting Started. Keep everything already there exactly as is. Read the Daloopa Tearsheet skill; leave a Filing Room Governance note recording the identifier its final step says every Daloopa-sourced figure must be cited with.

- Initial workspace: dashboard "Filing Room"; 1 tab(s): filings; 2 seeded widget(s): daloopa_document_search({"ticker": "MSFT", "doc_type": "10-Q"}), daloopa_company_directory({}); 1 seeded generated widget(s): note "Prior Filing Sign-off"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Filing Room" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `filings` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Filing Room Service/filing_register` on tab `filings` → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_document_search` with data_args ⊇ {"ticker": "AAPL", "doc_type": "10-K"} on tab `filings` → `missing_widget`
- **Widget** ≥1× `Getting Started/multi_pdf_url` on tab `filings` → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_document_search` with data_args ⊇ {"ticker": "MSFT", "doc_type": "10-Q"} on tab `filings` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` on tab `filings` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Filing Sign-off" whose content mentions "Prior filing pull: MSFT quarterly filing checked and signed off." on tab `filings` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Filing Room Governance" whose content mentions "source_url" on tab `filings` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_290` must sit at exactly x=0, y=0, w=20, h=12 on tab `filings` → `layout_mismatch`
- **Layout** `w_810` must sit at exactly x=20, y=0, w=20, h=12 on tab `filings` → `layout_mismatch`
- **Layout** `w_72a` must sit at exactly x=0, y=12, w=20, h=8 on tab `filings` → `layout_mismatch`

#### `form_tooling_level0`

**level0** · category: story · specification: -

> On the open Intake Tools dashboard, add Financial Entry Form and Example Backend Params from Widget Examples. Set daysPicker1 on Example Backend Params to 5 and leave its other parameters at their defaults.

- Initial workspace: dashboard "Intake Tools"; 1 tab(s): intake
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/form_submit_widget` on tab `intake` → `missing_widget`
- **Widget** ≥1× `Widget Examples/show_example_params` with data_args ⊇ {"daysPicker1": "5"} on tab `intake` → `missing_widget`

#### `form_tooling_level1`

**level1** · category: story · specification: -

> Add the intake form from Widget Examples to the open Intake Tools dashboard, with Example Backend Params beside it and daysPicker1 set to 5. Keep the tester's other parameters at their defaults.

- Initial workspace: dashboard "Intake Tools"; 1 tab(s): intake
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/form_submit_widget` on tab `intake` → `missing_widget`
- **Widget** ≥1× `Widget Examples/show_example_params` with data_args ⊇ {"daysPicker1": "5"} on tab `intake` → `missing_widget`

#### `form_tooling_level2`

**level2** · category: story · specification: -

> Intake Tools on the open dashboard: add Financial Entry Form and Example Backend Params from Widget Examples. Set daysPicker1 on Example Backend Params by the weekly window policy; leave its other parameters at their defaults.

- Initial workspace: dashboard "Intake Tools"; 1 tab(s): intake
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/form_submit_widget` on tab `intake` → `missing_widget`
- **Widget** ≥1× `Widget Examples/show_example_params` with data_args ⊇ {"daysPicker1": "5"} on tab `intake` → `missing_widget`

#### `form_tooling_level3`

**level3** · category: story · specification: -

> On the open Intake Tools dashboard, add Financial Entry Form and Example Backend Params from Widget Examples. Set daysPicker1 to 5 and leave the tester's other parameters at their defaults. Keep everything already there exactly as is. Under the widgets.json spec's Widget Parameters resource, leave an Intake Tooling Governance Note recording the parameter kind listed between endpoint and button.

- Initial workspace: dashboard "Intake Tools"; 1 tab(s): intake; 1 seeded widget(s): show_example_params({"datePicker1": "$currentDate-1d", "textBox1": "Hello!", "textBox2": "var1,var2,var3", "TrueFalse": true, "daysPicker1": "10"}); 1 seeded generated widget(s): note "Prior Intake Check"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Intake Tools" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `intake` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Widget Examples/form_submit_widget` on tab `intake` → `missing_widget`
- **Widget** ≥1× `Widget Examples/show_example_params` with data_args ⊇ {"daysPicker1": "5"} on tab `intake` → `missing_widget`
- **Widget** ≥1× `Widget Examples/show_example_params` with data_args ⊇ {"datePicker1": "$currentDate-1d", "textBox1": "Hello!", "textBox2": "var1,var2,var3", "TrueFalse": true, "daysPicker1": "10"} on tab `intake` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Intake Check" whose content mentions "Prior intake check: the month-end exception batch stays on its existing review window." on tab `intake` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Intake Tooling Governance Note" whose content mentions "form" on tab `intake` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_bf5` must sit at exactly x=0, y=0, w=20, h=9 on tab `intake` → `layout_mismatch`
- **Layout** `w_87d` must sit at exactly x=20, y=0, w=20, h=8 on tab `intake` → `layout_mismatch`

#### `form_tooling_level4`

**level4** · category: story · specification: -

> Build the intake service before cutoff: add an Intake Form Service backend serving an Intake Register table; publish Intake Controls App with Intake Register on its Register tab; instantiate the app. On the open Intake Tools dashboard, add the built Intake Register, Financial Entry Form, and Example Backend Params from Widget Examples. Set daysPicker1 to 5 and leave the tester's other parameters at their defaults. Keep everything already there exactly as is. Under the widgets.json spec's Widget Parameters resource, leave an Intake Tooling Governance Note recording the parameter kind listed between endpoint and button.

- Initial workspace: dashboard "Intake Tools"; 1 tab(s): intake; 1 seeded widget(s): show_example_params({"datePicker1": "$currentDate-1d", "textBox1": "Hello!", "textBox2": "var1,var2,var3", "TrueFalse": true, "daysPicker1": "10"}); 1 seeded generated widget(s): note "Prior Intake Check"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Intake Tools" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `intake` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Intake Form Service/intake_register` on tab `intake` → `missing_widget`
- **Widget** ≥1× `Widget Examples/form_submit_widget` on tab `intake` → `missing_widget`
- **Widget** ≥1× `Widget Examples/show_example_params` with data_args ⊇ {"daysPicker1": "5"} on tab `intake` → `missing_widget`
- **Widget** ≥1× `Widget Examples/show_example_params` with data_args ⊇ {"datePicker1": "$currentDate-1d", "textBox1": "Hello!", "textBox2": "var1,var2,var3", "TrueFalse": true, "daysPicker1": "10"} on tab `intake` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Intake Check" whose content mentions "Prior intake check: the month-end exception batch stays on its existing review window." on tab `intake` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Intake Tooling Governance Note" whose content mentions "form" on tab `intake` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_bf5` must sit at exactly x=0, y=0, w=20, h=9 on tab `intake` → `layout_mismatch`
- **Layout** `w_87d` must sit at exactly x=20, y=0, w=20, h=8 on tab `intake` → `layout_mismatch`

#### `nav_close_repair_level0`

**level0** · category: story · specification: -

> Repair Close Exceptions from Bench Stark Enterprise's NAV, Fees & Close Dashboard on the open Close Room dashboard: set fund to Flagship Long/Short, status to Open, and period to 1D so today's close is back on the right queue.

- Initial workspace: dashboard "Close Room"; 1 tab(s): close; 1 seeded widget(s): nav_fees_close_dashboard_close_close_exceptions({"fund": "Multi-Asset Fund", "status": "Closed", "period": "1Y"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/nav_fees_close_dashboard_close_close_exceptions` with data_args ⊇ {"fund": "Flagship Long/Short", "status": "Open", "period": "1D"} on tab `close` → `missing_widget`

#### `nav_close_repair_level1`

**level1** · category: story · specification: -

> Repair the close blotter from Bench Stark Enterprise's NAV, Fees & Close Dashboard on the open Close Room dashboard: Flagship Long/Short, Open, 1D. The close cutoff is coming up.

- Initial workspace: dashboard "Close Room"; 1 tab(s): close; 1 seeded widget(s): nav_fees_close_dashboard_close_close_exceptions({"fund": "Multi-Asset Fund", "status": "Closed", "period": "1Y"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/nav_fees_close_dashboard_close_close_exceptions` with data_args ⊇ {"fund": "Flagship Long/Short", "status": "Open", "period": "1D"} on tab `close` → `missing_widget`

#### `nav_close_repair_level2`

**level2** · category: story · specification: -

> Close repair on the open Close Room dashboard: restore Close Exceptions from Bench Stark Enterprise's NAV, Fees & Close Dashboard to Flagship Long/Short and Open, with period set by the close-day policy.

- Initial workspace: dashboard "Close Room"; 1 tab(s): close; 1 seeded widget(s): nav_fees_close_dashboard_close_close_exceptions({"fund": "Multi-Asset Fund", "status": "Closed", "period": "1Y"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/nav_fees_close_dashboard_close_close_exceptions` with data_args ⊇ {"fund": "Flagship Long/Short", "status": "Open", "period": "1D"} on tab `close` → `missing_widget`

#### `nav_close_repair_level3`

**level3** · category: story · specification: -

> Close repair on the open Close Room dashboard: Close Exceptions from Bench Stark Enterprise's NAV, Fees & Close Dashboard is showing Multi-Asset Fund, Closed, 1Y. Restore it to Flagship Long/Short, Open, 1D; keep everything already there exactly as is. Under the Daloopa Capital Allocation skill, leave a Close Governance Note recording which payout line its comparison adds to Share Buybacks before testing the total against Free Cash Flow.

- Initial workspace: dashboard "Close Room"; 1 tab(s): close; 3 seeded widget(s): nav_fees_close_dashboard_close_close_exceptions({"fund": "Multi-Asset Fund", "status": "Closed", "period": "1Y"}), nav_fees_close_dashboard_close_close_exceptions({"fund": "Income Fund", "status": "In Review", "period": "MTD"}), nav_fees_close_dashboard_close_close_notes({"fund": "Flagship Long/Short", "status": "Open", "period": "1D"}); 1 seeded generated widget(s): note "Prior Close Sign-Off"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Close Room" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `close` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/nav_fees_close_dashboard_close_close_exceptions` with data_args ⊇ {"fund": "Flagship Long/Short", "status": "Open", "period": "1D"} on tab `close` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/nav_fees_close_dashboard_close_close_exceptions` with data_args ⊇ {"fund": "Income Fund", "status": "In Review", "period": "MTD"} on tab `close` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/nav_fees_close_dashboard_close_close_notes` with data_args ⊇ {"fund": "Flagship Long/Short", "status": "Open", "period": "1D"} on tab `close` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Close Sign-Off" whose content mentions "Prior close: Income Fund cash break cleared under four-eyes review." on tab `close` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Close Governance Note" whose content mentions "Dividends Paid" on tab `close` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_455` must sit at exactly x=0, y=0, w=20, h=14 on tab `close` → `layout_mismatch`
- **Layout** `w_ef0` must sit at exactly x=20, y=0, w=20, h=14 on tab `close` → `layout_mismatch`
- **Layout** `w_67b` must sit at exactly x=0, y=14, w=40, h=10 on tab `close` → `layout_mismatch`
- **Layout** `w_087` must sit at exactly x=0, y=24, w=20, h=8 on tab `close` → `layout_mismatch`

#### `nav_close_repair_level4`

**level4** · category: story · specification: -

> Build the close watch before cutoff: add a Close Watch Service backend serving a Close Register table; publish Close Watch App with Close Register on its Close tab; instantiate the app. On the open Close Room dashboard, add the built Close Register. Close Exceptions from Bench Stark Enterprise's NAV, Fees & Close Dashboard is showing Multi-Asset Fund, Closed, 1Y; restore it to Flagship Long/Short, Open, 1D. Keep everything already there exactly as is. Read the Daloopa Capital Allocation skill; leave a Close Governance Note recording which payout line its comparison adds to Share Buybacks before testing the total against Free Cash Flow.

- Initial workspace: dashboard "Close Room"; 1 tab(s): close; 3 seeded widget(s): nav_fees_close_dashboard_close_close_exceptions({"fund": "Multi-Asset Fund", "status": "Closed", "period": "1Y"}), nav_fees_close_dashboard_close_close_exceptions({"fund": "Income Fund", "status": "In Review", "period": "MTD"}), nav_fees_close_dashboard_close_close_notes({"fund": "Flagship Long/Short", "status": "Open", "period": "1D"}); 1 seeded generated widget(s): note "Prior Close Sign-Off"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Close Room" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `close` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Close Watch Service/close_register` on tab `close` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/nav_fees_close_dashboard_close_close_exceptions` with data_args ⊇ {"fund": "Flagship Long/Short", "status": "Open", "period": "1D"} on tab `close` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/nav_fees_close_dashboard_close_close_exceptions` with data_args ⊇ {"fund": "Income Fund", "status": "In Review", "period": "MTD"} on tab `close` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/nav_fees_close_dashboard_close_close_notes` with data_args ⊇ {"fund": "Flagship Long/Short", "status": "Open", "period": "1D"} on tab `close` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Close Sign-Off" whose content mentions "Prior close: Income Fund cash break cleared under four-eyes review." on tab `close` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Close Governance Note" whose content mentions "Dividends Paid" on tab `close` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_455` must sit at exactly x=0, y=0, w=20, h=14 on tab `close` → `layout_mismatch`
- **Layout** `w_ef0` must sit at exactly x=20, y=0, w=20, h=14 on tab `close` → `layout_mismatch`
- **Layout** `w_67b` must sit at exactly x=0, y=14, w=40, h=10 on tab `close` → `layout_mismatch`
- **Layout** `w_087` must sit at exactly x=0, y=24, w=20, h=8 on tab `close` → `layout_mismatch`

#### `settlement_watch_level0`

**level0** · category: story · specification: -

> On the open Fails Watch dashboard, add Failed Trades and Settlement Exceptions from Bench Stark Enterprise's Fund Operations Control Tower, both with parameters fund set to Income Fund, status set to Open, and period set to 1D. I need today's open fails in front of the desk before the cutoff.

- Initial workspace: dashboard "Fails Watch"; 1 tab(s): watch
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_trade_lifecycle_failed_trades` with data_args ⊇ {"fund": "Income Fund", "status": "Open", "period": "1D"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_trade_lifecycle_settlement_exceptions` with data_args ⊇ {"fund": "Income Fund", "status": "Open", "period": "1D"} → `missing_widget`

#### `settlement_watch_level1`

**level1** · category: story · specification: -

> Get the fails queue and Settlement Exceptions onto the open Fails Watch dashboard from Bench Stark Enterprise's Fund Operations Control Tower. Use parameters fund Income Fund, status Open, and period 1D for both - cutoff review is next.

- Initial workspace: dashboard "Fails Watch"; 1 tab(s): watch
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_trade_lifecycle_failed_trades` with data_args ⊇ {"fund": "Income Fund", "status": "Open", "period": "1D"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_trade_lifecycle_settlement_exceptions` with data_args ⊇ {"fund": "Income Fund", "status": "Open", "period": "1D"} → `missing_widget`

#### `settlement_watch_level2`

**level2** · category: story · specification: -

> Fails watch on the open Fails Watch dashboard: add Failed Trades and Settlement Exceptions from Bench Stark Enterprise's Fund Operations Control Tower. For both, use fund Income Fund, status Open, and period set by the same-day fails policy.

- Initial workspace: dashboard "Fails Watch"; 1 tab(s): watch
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_trade_lifecycle_failed_trades` with data_args ⊇ {"fund": "Income Fund", "status": "Open", "period": "1D"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_trade_lifecycle_settlement_exceptions` with data_args ⊇ {"fund": "Income Fund", "status": "Open", "period": "1D"} → `missing_widget`

#### `settlement_watch_level3`

**level3** · category: story · specification: -

> Fails watch on the open Fails Watch dashboard: add Failed Trades and Settlement Exceptions from Bench Stark Enterprise's Fund Operations Control Tower for fund Income Fund, status Open, and period 1D. Keep everything already there exactly as is. Under the Finance Guidance Tracker skill, leave a Fails Cutoff Governance note recording what its workflow lists in its final step.

- Initial workspace: dashboard "Fails Watch"; 1 tab(s): watch; 2 seeded widget(s): fund_operations_control_tower_trade_lifecycle_failed_trades({"fund": "Global Opportunities", "status": "Closed", "period": "1Y"}), fund_operations_control_tower_trade_lifecycle_settlement_exceptions({"fund": "Multi-Asset Fund", "status": "In Review", "period": "MTD"}); 1 seeded generated widget(s): note "Prior Cutoff Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Fails Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `watch` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_trade_lifecycle_failed_trades` with data_args ⊇ {"fund": "Income Fund", "status": "Open", "period": "1D"} on tab `watch` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_trade_lifecycle_settlement_exceptions` with data_args ⊇ {"fund": "Income Fund", "status": "Open", "period": "1D"} on tab `watch` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_trade_lifecycle_failed_trades` with data_args ⊇ {"fund": "Global Opportunities", "status": "Closed", "period": "1Y"} on tab `watch` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_trade_lifecycle_settlement_exceptions` with data_args ⊇ {"fund": "Multi-Asset Fund", "status": "In Review", "period": "MTD"} on tab `watch` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Cutoff Note" whose content mentions "Prior cutoff: the Multi-Asset Fund review queue was carried to the next shift." on tab `watch` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Fails Cutoff Governance" whose content mentions "evidence gaps" on tab `watch` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_704` must sit at exactly x=0, y=0, w=40, h=5 on tab `watch` → `layout_mismatch`
- **Layout** `w_5f4` must sit at exactly x=0, y=5, w=20, h=14 on tab `watch` → `layout_mismatch`
- **Layout** `w_c0a` must sit at exactly x=20, y=5, w=20, h=8 on tab `watch` → `layout_mismatch`

#### `settlement_watch_level4`

**level4** · category: story · specification: -

> Build the cutoff file before the afternoon review: add a Fails Watch Service backend serving a Fails Register table; publish Fails Watch App with Fails Register on its Watch tab; instantiate the app. On the open Fails Watch dashboard, add the built Fails Register, Failed Trades, and Settlement Exceptions from Bench Stark Enterprise's Fund Operations Control Tower for fund Income Fund, status Open, and period 1D. Keep everything already there exactly as is. Read the Finance Guidance Tracker skill; leave a Fails Cutoff Governance note recording what its workflow lists in its final step.

- Initial workspace: dashboard "Fails Watch"; 1 tab(s): watch; 2 seeded widget(s): fund_operations_control_tower_trade_lifecycle_failed_trades({"fund": "Global Opportunities", "status": "Closed", "period": "1Y"}), fund_operations_control_tower_trade_lifecycle_settlement_exceptions({"fund": "Multi-Asset Fund", "status": "In Review", "period": "MTD"}); 1 seeded generated widget(s): note "Prior Cutoff Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Fails Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `watch` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Fails Watch Service/fails_register` on tab `watch` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_trade_lifecycle_failed_trades` with data_args ⊇ {"fund": "Income Fund", "status": "Open", "period": "1D"} on tab `watch` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_trade_lifecycle_settlement_exceptions` with data_args ⊇ {"fund": "Income Fund", "status": "Open", "period": "1D"} on tab `watch` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_trade_lifecycle_failed_trades` with data_args ⊇ {"fund": "Global Opportunities", "status": "Closed", "period": "1Y"} on tab `watch` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_trade_lifecycle_settlement_exceptions` with data_args ⊇ {"fund": "Multi-Asset Fund", "status": "In Review", "period": "MTD"} on tab `watch` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Cutoff Note" whose content mentions "Prior cutoff: the Multi-Asset Fund review queue was carried to the next shift." on tab `watch` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Fails Cutoff Governance" whose content mentions "evidence gaps" on tab `watch` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_704` must sit at exactly x=0, y=0, w=40, h=5 on tab `watch` → `layout_mismatch`
- **Layout** `w_5f4` must sit at exactly x=0, y=5, w=20, h=14 on tab `watch` → `layout_mismatch`
- **Layout** `w_c0a` must sit at exactly x=20, y=5, w=20, h=8 on tab `watch` → `layout_mismatch`

### portfolio_manager (20)

#### `allocation_read_level0`

**level0** · category: story · specification: -

> On the open Allocation Review dashboard, read Segment Breakdown from Bench Daloopa with ticker set to AAPL and period set to 2026Q1, then leave an Allocation Read Note recording the top segment and its exact revenue_musd - quoted to the decimal, the desk reuses this note.

- Initial workspace: dashboard "Allocation Review"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Allocation Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Generated note** ≥1× named ~"Allocation Read Note" whose content mentions "iPhone", "52365.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `allocation_read_level1`

**level1** · category: story · specification: -

> Read the segment split off Bench Daloopa - ticker AAPL, period 2026Q1 - and leave an Allocation Read Note on the open Allocation Review dashboard recording the top segment and its exact revenue_musd. Sizing the Apple position after the close.

- Initial workspace: dashboard "Allocation Review"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Allocation Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Generated note** ≥1× named ~"Allocation Read Note" whose content mentions "iPhone", "52365.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `allocation_read_level2`

**level2** · category: story · specification: -

> Read Segment Breakdown from Bench Daloopa for ticker AAPL, period per the latest covered quarter policy - the newest quarter the dataset covers - and leave an Allocation Read Note on the open Allocation Review dashboard recording the top segment and its exact revenue_musd.

- Initial workspace: dashboard "Allocation Review"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Allocation Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Generated note** ≥1× named ~"Allocation Read Note" whose content mentions "iPhone", "52365.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `allocation_read_level3`

**level3** · category: story · specification: -

> Read Segment Breakdown from Bench Daloopa with ticker AAPL, period 2026Q1, on the open Allocation Review dashboard, and keep everything already on the dashboard as is. Allocation reads run under the Daloopa Tearsheet skill - leave an Allocation Read Note recording the top segment, its exact revenue_musd, and what that skill says all period math anchors on.

- Initial workspace: dashboard "Allocation Review"; 1 tab(s): review; 2 seeded widget(s): daloopa_segment_breakdown({"ticker": "MSFT", "period": "2025Q4"}), daloopa_company_directory({}); 1 seeded generated widget(s): note "Prior Allocation Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Allocation Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Daloopa/daloopa_segment_breakdown` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q4"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Allocation Note" whose content mentions "Prior review: MSFT segment mix - Intelligent Cloud led the quarter." on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Allocation Read Note" whose content mentions "iPhone", "52365.6", "latest_calendar_quarter" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_7e2` must sit at exactly x=0, y=0, w=20, h=12 on tab `review` → `layout_mismatch`
- **Layout** `w_92e` must sit at exactly x=20, y=0, w=20, h=12 on tab `review` → `layout_mismatch`
- **Layout** `w_f41` must sit at exactly x=0, y=12, w=20, h=8 on tab `review` → `layout_mismatch`

#### `allocation_read_level4`

**level4** · category: story · specification: -

> Build the desk's allocation digest before the rebalance: add an Allocation Digest Service backend serving a Segment Digest table, publish Allocation Digest App with Segment Digest on its Digest tab, and instantiate the app. On the open Allocation Review dashboard, add the built Segment Digest, keeping everything already there as is. Read Segment Breakdown from Bench Daloopa with ticker AAPL, period 2026Q1, and under the Daloopa Tearsheet skill leave an Allocation Read Note recording the top segment, its exact revenue_musd, and what that skill says all period math anchors on.

- Initial workspace: dashboard "Allocation Review"; 1 tab(s): review; 2 seeded widget(s): daloopa_segment_breakdown({"ticker": "MSFT", "period": "2025Q4"}), daloopa_company_directory({}); 1 seeded generated widget(s): note "Prior Allocation Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Allocation Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Allocation Digest Service/segment_digest` on tab `review` → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_segment_breakdown` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q4"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Allocation Note" whose content mentions "Prior review: MSFT segment mix - Intelligent Cloud led the quarter." on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Allocation Read Note" whose content mentions "iPhone", "52365.6", "latest_calendar_quarter" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_7e2` must sit at exactly x=0, y=0, w=20, h=12 on tab `review` → `layout_mismatch`
- **Layout** `w_92e` must sit at exactly x=20, y=0, w=20, h=12 on tab `review` → `layout_mismatch`
- **Layout** `w_f41` must sit at exactly x=0, y=12, w=20, h=8 on tab `review` → `layout_mismatch`

#### `morning_briefing_level0`

**level0** · category: story · specification: -

> On the open PM Morning Briefing dashboard, add Trade Ideas from Bench Stark Enterprise's Portfolio Command Center with fund set to Flagship Long/Short and period set to QTD - the 9am call is about to start.

- Initial workspace: dashboard "PM Morning Briefing"; 1 tab(s): briefing
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "PM Morning Briefing" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "QTD"} → `missing_widget`

#### `morning_briefing_level1`

**level1** · category: story · specification: -

> Get the idea pipeline up on the open PM Morning Briefing dashboard before the 9am call - it lives in Bench Stark Enterprise's Portfolio Command Center. Flagship Long/Short, QTD.

- Initial workspace: dashboard "PM Morning Briefing"; 1 tab(s): briefing
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "PM Morning Briefing" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "QTD"} → `missing_widget`

#### `morning_briefing_level2`

**level2** · category: story · specification: -

> Prep the open PM Morning Briefing dashboard for the 9am call: Trade Ideas from Bench Stark Enterprise's Portfolio Command Center for Flagship Long/Short, configured per the quarterly briefing policy.

- Initial workspace: dashboard "PM Morning Briefing"; 1 tab(s): briefing
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "PM Morning Briefing" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "QTD"} → `missing_widget`

#### `morning_briefing_level3`

**level3** · category: story · specification: -

> On the open PM Morning Briefing dashboard, fix the stale Trade Ideas from Bench Stark Enterprise's Portfolio Command Center to Flagship Long/Short, QTD, and add a fresh Trade Ideas for the same fund and period. Keep everything else as is. Briefings run under the Daloopa Capital Allocation skill - leave a Morning Briefing Governance note recording what its final step says every figure is cited via.

- Initial workspace: dashboard "PM Morning Briefing"; 1 tab(s): briefing; 2 seeded widget(s): portfolio_command_center_actions_trade_ideas({"fund": "Global Opportunities", "period": "1Y"}), portfolio_command_center_overview_top_alerts({"fund": "Flagship Long/Short", "period": "1D"}); 1 seeded generated widget(s): note "Last Week Briefing Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "PM Morning Briefing" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `briefing` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥2× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "QTD"} on tab `briefing` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_overview_top_alerts` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "1D"} on tab `briefing` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Last Week Briefing Note" whose content mentions "Last week's briefing: watch Income Fund redemptions into month-end." on tab `briefing` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Morning Briefing Governance" whose content mentions "source_url" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_8d6` must sit at exactly x=0, y=0, w=20, h=14 on tab `briefing` → `layout_mismatch`
- **Layout** `w_f1b` must sit at exactly x=20, y=0, w=20, h=14 on tab `briefing` → `layout_mismatch`
- **Layout** `w_c6f` must sit at exactly x=0, y=14, w=20, h=8 on tab `briefing` → `layout_mismatch`

#### `morning_briefing_level4`

**level4** · category: story · specification: -

> Build the desk's briefing feed before the 9am call: add a Briefing Feed Service backend serving an Idea Register table, publish Briefing Feed App with Idea Register on its Briefing tab, and instantiate the app. On the open PM Morning Briefing dashboard, add the built Idea Register, fix the stale Trade Ideas from Bench Stark Enterprise's Portfolio Command Center to Flagship Long/Short, QTD, and add a fresh Trade Ideas for the same fund and period, keeping everything else as is. Read the Daloopa Capital Allocation skill and leave a Morning Briefing Governance note recording what its final step says every figure is cited via.

- Initial workspace: dashboard "PM Morning Briefing"; 1 tab(s): briefing; 2 seeded widget(s): portfolio_command_center_actions_trade_ideas({"fund": "Global Opportunities", "period": "1Y"}), portfolio_command_center_overview_top_alerts({"fund": "Flagship Long/Short", "period": "1D"}); 1 seeded generated widget(s): note "Last Week Briefing Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "PM Morning Briefing" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `briefing` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Briefing Feed Service/idea_register` on tab `briefing` → `missing_widget`
- **Widget** ≥2× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "QTD"} on tab `briefing` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_overview_top_alerts` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "1D"} on tab `briefing` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Last Week Briefing Note" whose content mentions "Last week's briefing: watch Income Fund redemptions into month-end." on tab `briefing` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Morning Briefing Governance" whose content mentions "source_url" on tab `briefing` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_8d6` must sit at exactly x=0, y=0, w=20, h=14 on tab `briefing` → `layout_mismatch`
- **Layout** `w_f1b` must sit at exactly x=20, y=0, w=20, h=14 on tab `briefing` → `layout_mismatch`
- **Layout** `w_c6f` must sit at exactly x=0, y=14, w=20, h=8 on tab `briefing` → `layout_mismatch`

#### `pm_handoff_level0`

**level0** · category: story · specification: -

> On the open PM Handoff Log dashboard, read Consensus Estimates from Bench Daloopa with ticker set to MSFT, then leave an Overnight Handoff Note recording the exact Total Revenue actual and consensus for 2026Q1 - quoted to the decimal, the overnight desk trades off this note.

- Initial workspace: dashboard "PM Handoff Log"; 1 tab(s): handoff
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "PM Handoff Log" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Generated note** ≥1× named ~"Overnight Handoff Note" whose content mentions "91934.6", "93202.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `pm_handoff_level1`

**level1** · category: story · specification: -

> End of day - pull the street numbers for MSFT off Bench Daloopa, actual against consensus, and leave an Overnight Handoff Note on the open PM Handoff Log dashboard recording the exact Total Revenue actual and consensus for 2026Q1. The overnight desk trades off this note.

- Initial workspace: dashboard "PM Handoff Log"; 1 tab(s): handoff
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "PM Handoff Log" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Generated note** ≥1× named ~"Overnight Handoff Note" whose content mentions "91934.6", "93202.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `pm_handoff_level2`

**level2** · category: story · specification: -

> Read Consensus Estimates from Bench Daloopa on the open PM Handoff Log dashboard for the line the mega-cap coverage policy covers - the policy names it by company, the Microsoft line, never by ticker - and leave an Overnight Handoff Note recording the exact Total Revenue actual and consensus for 2026Q1. The overnight desk trades off this note.

- Initial workspace: dashboard "PM Handoff Log"; 1 tab(s): handoff
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "PM Handoff Log" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Generated note** ≥1× named ~"Overnight Handoff Note" whose content mentions "91934.6", "93202.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `pm_handoff_level3`

**level3** · category: story · specification: -

> Close out the open PM Handoff Log dashboard for the overnight desk: read Consensus Estimates from Bench Daloopa with ticker MSFT and leave an Overnight Handoff Note with the exact Total Revenue actual and consensus for 2026Q1. The close-out runs under the Daloopa Earnings Review skill - the note also records the granularity that skill's first step sets for the consensus compare. Everything already on the dashboard stays as is.

- Initial workspace: dashboard "PM Handoff Log"; 1 tab(s): handoff; 1 seeded widget(s): daloopa_consensus_estimates({"ticker": "NVDA"}); 1 seeded generated widget(s): note "Prior Shift Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "PM Handoff Log" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `handoff` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Daloopa/daloopa_consensus_estimates` with data_args ⊇ {"ticker": "NVDA"} on tab `handoff` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Shift Note" whose content mentions "Prior shift: NVDA into the print - exception cleared, nothing carried over." on tab `handoff` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Overnight Handoff Note" whose content mentions "91934.6", "93202.6", "metric by metric" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_5b2` must sit at exactly x=0, y=0, w=20, h=12 on tab `handoff` → `layout_mismatch`
- **Layout** `w_5e3` must sit at exactly x=20, y=0, w=20, h=8 on tab `handoff` → `layout_mismatch`

#### `pm_handoff_level4`

**level4** · category: story · specification: -

> Build the desk's handoff log before the overnight shift: add a Handoff Log Service backend serving a Handoff Register table, publish Handoff Log App with Handoff Register on its Handoff tab, and instantiate the app. On the open PM Handoff Log dashboard, add the built Handoff Register, keeping everything already there as is. Then close out under the Daloopa Earnings Review skill: read Consensus Estimates from Bench Daloopa with ticker MSFT, leave an Overnight Handoff Note with the exact Total Revenue actual and consensus for 2026Q1 plus the granularity that skill's first step sets for the consensus compare, and delegate the follow-up to the coverage analyst.

- Initial workspace: dashboard "PM Handoff Log"; 1 tab(s): handoff; 1 seeded widget(s): daloopa_consensus_estimates({"ticker": "NVDA"}); 1 seeded generated widget(s): note "Prior Shift Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "PM Handoff Log" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `handoff` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Handoff Log Service/handoff_register` on tab `handoff` → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_consensus_estimates` with data_args ⊇ {"ticker": "NVDA"} on tab `handoff` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Shift Note" whose content mentions "Prior shift: NVDA into the print - exception cleared, nothing carried over." on tab `handoff` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Overnight Handoff Note" whose content mentions "91934.6", "93202.6", "metric by metric" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_5b2` must sit at exactly x=0, y=0, w=20, h=12 on tab `handoff` → `layout_mismatch`
- **Layout** `w_5e3` must sit at exactly x=20, y=0, w=20, h=8 on tab `handoff` → `layout_mismatch`

#### `price_watch_level0`

**level0** · category: story · specification: -

> On the open Price Watch dashboard, add Live Grid from Getting Started with symbol set to TSLA - I want it streaming before the open.

- Initial workspace: dashboard "Price Watch"; 1 tab(s): watch
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Price Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Getting Started/live_grid_data` with data_args ⊇ {"symbol": "TSLA"} → `missing_widget`

#### `price_watch_level1`

**level1** · category: story · specification: -

> Get the live-updating price grid up on the open Price Watch dashboard - it's in Getting Started. TSLA, before the open.

- Initial workspace: dashboard "Price Watch"; 1 tab(s): watch
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Price Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Getting Started/live_grid_data` with data_args ⊇ {"symbol": "TSLA"} → `missing_widget`

#### `price_watch_level2`

**level2** · category: story · specification: -

> Prep the open Price Watch dashboard before the open: Live Grid from Getting Started, with the symbol set per the EV watch policy - the desk keeps its electric-vehicle name streaming.

- Initial workspace: dashboard "Price Watch"; 1 tab(s): watch
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Price Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Getting Started/live_grid_data` with data_args ⊇ {"symbol": "TSLA"} → `missing_widget`

#### `price_watch_level3`

**level3** · category: story · specification: -

> On the open Price Watch dashboard, fix the stale Live Grid from Getting Started to TSLA and add a fresh Live Grid for the same symbol. Keep everything else as is. Price views on the desk run under the Finance Tearsheet skill - leave a Price Watch Governance note recording what its final step says to close with.

- Initial workspace: dashboard "Price Watch"; 1 tab(s): watch; 2 seeded widget(s): live_grid_data({"symbol": "MSFT"}), sparkline_line({}); 1 seeded generated widget(s): note "Watch Handoff Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Price Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `watch` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥2× `Getting Started/live_grid_data` with data_args ⊇ {"symbol": "TSLA"} on tab `watch` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/sparkline_line` on tab `watch` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Watch Handoff Note" whose content mentions "Prior session: the desk was watching MSFT into the print." on tab `watch` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Price Watch Governance" whose content mentions "investment conclusion" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_e89` must sit at exactly x=0, y=0, w=20, h=9 on tab `watch` → `layout_mismatch`
- **Layout** `w_6a3` must sit at exactly x=20, y=0, w=20, h=10 on tab `watch` → `layout_mismatch`
- **Layout** `w_a8a` must sit at exactly x=0, y=10, w=20, h=8 on tab `watch` → `layout_mismatch`

#### `price_watch_level4`

**level4** · category: story · specification: -

> Build the desk's watch feed before the open: add a Watch Feed Service backend serving a Watch Register table, publish Watch Feed App with Watch Register on its Watch tab, and instantiate the app. On the open Price Watch dashboard, add the built Watch Register, fix the stale Live Grid from Getting Started to TSLA, and add a fresh Live Grid for the same symbol, keeping everything else as is. Read the Finance Tearsheet skill and leave a Price Watch Governance note recording what its final step says to close with.

- Initial workspace: dashboard "Price Watch"; 1 tab(s): watch; 2 seeded widget(s): live_grid_data({"symbol": "MSFT"}), sparkline_line({}); 1 seeded generated widget(s): note "Watch Handoff Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Price Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `watch` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Watch Feed Service/watch_register` on tab `watch` → `missing_widget`
- **Widget** ≥2× `Getting Started/live_grid_data` with data_args ⊇ {"symbol": "TSLA"} on tab `watch` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/sparkline_line` on tab `watch` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Watch Handoff Note" whose content mentions "Prior session: the desk was watching MSFT into the print." on tab `watch` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Price Watch Governance" whose content mentions "investment conclusion" on tab `watch` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_e89` must sit at exactly x=0, y=0, w=20, h=9 on tab `watch` → `layout_mismatch`
- **Layout** `w_6a3` must sit at exactly x=20, y=0, w=20, h=10 on tab `watch` → `layout_mismatch`
- **Layout** `w_a8a` must sit at exactly x=0, y=10, w=20, h=8 on tab `watch` → `layout_mismatch`

### research_analyst (20)

#### `earnings_prep_level0`

**level0** · category: story · specification: -

> On the open Earnings Prep Desk dashboard, read Upcoming Earnings from Bench Stark Enterprise's Earnings & Estimates Monitor with sector set to Technology, ticker set to NVDA, and period set to QTD, then leave an Earnings Prep Note recording every returned row's ticker, change, score, and status exactly - the desk is building the preview from this note.

- Initial workspace: dashboard "Earnings Prep Desk"; 1 tab(s): prep
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Earnings Prep Note" whose content mentions "AAPL", "-0.0581", "6.52", "TSLA", "0.0579", "73.24", "In Review" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_prep_level1`

**level1** · category: story · specification: -

> Pull the earnings calendar from Bench Stark Enterprise's Earnings & Estimates Monitor for the open Earnings Prep Desk dashboard - sector Technology, ticker NVDA, period QTD - and leave an Earnings Prep Note recording every returned row's ticker, change, score, and status exactly. The preview goes out shortly.

- Initial workspace: dashboard "Earnings Prep Desk"; 1 tab(s): prep
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Earnings Prep Note" whose content mentions "AAPL", "-0.0581", "6.52", "TSLA", "0.0579", "73.24", "In Review" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_prep_level2`

**level2** · category: story · specification: -

> On the open Earnings Prep Desk dashboard, read Upcoming Earnings from Bench Stark Enterprise's Earnings & Estimates Monitor for sector Technology and ticker NVDA, with the period set by the current-quarter prep policy, then leave an Earnings Prep Note recording every returned row's ticker, change, score, and status exactly.

- Initial workspace: dashboard "Earnings Prep Desk"; 1 tab(s): prep
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Earnings Prep Note" whose content mentions "AAPL", "-0.0581", "6.52", "TSLA", "0.0579", "73.24", "In Review" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_prep_level3`

**level3** · category: story · specification: -

> On the open Earnings Prep Desk dashboard, read Upcoming Earnings from Bench Stark Enterprise's Earnings & Estimates Monitor with sector Technology, ticker NVDA, and period QTD, keeping everything already on the dashboard exactly as it is. Previews run under the Finance Earnings Prep skill - leave an Earnings Prep Note recording every returned row's ticker, change, score, and status exactly, plus what the skill's final step tells the analyst to produce for the PM across the three print outcomes.

- Initial workspace: dashboard "Earnings Prep Desk"; 1 tab(s): prep; 2 seeded widget(s): earnings_estimates_monitor_calendar_upcoming_earnings({"sector": "Healthcare", "ticker": "LLY", "period": "YTD"}), earnings_estimates_monitor_estimates_consensus_revisions({"sector": "Technology", "ticker": "AAPL", "period": "MTD"}); 1 seeded generated widget(s): note "Prior Prep Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Earnings Prep Desk" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `prep` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_calendar_upcoming_earnings` with data_args ⊇ {"sector": "Healthcare", "ticker": "LLY", "period": "YTD"} on tab `prep` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_estimates_consensus_revisions` with data_args ⊇ {"sector": "Technology", "ticker": "AAPL", "period": "MTD"} on tab `prep` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Prep Note" whose content mentions "Prior prep: AAPL revisions remain under review; carry no assumptions into the NVDA preview." on tab `prep` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Earnings Prep Note" whose content mentions "AAPL", "-0.0581", "6.52", "TSLA", "0.0579", "73.24", "In Review", "action items", "beat", "miss", "in-line print" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_36b` must sit at exactly x=0, y=0, w=20, h=14 on tab `prep` → `layout_mismatch`
- **Layout** `w_b8a` must sit at exactly x=20, y=0, w=20, h=14 on tab `prep` → `layout_mismatch`
- **Layout** `w_b01` must sit at exactly x=0, y=14, w=20, h=8 on tab `prep` → `layout_mismatch`

#### `earnings_prep_level4`

**level4** · category: story · specification: -

> Build the desk's prep-sheet workflow: add a Prep Sheet Service backend serving a Prep Register table, publish Prep Sheet App with Prep Register on its Prep tab, and instantiate the app. On the open Earnings Prep Desk dashboard, add the built Prep Register and keep everything already there exactly as it is. Read Upcoming Earnings from Bench Stark Enterprise's Earnings & Estimates Monitor with sector Technology, ticker NVDA, and period QTD, then under the Finance Earnings Prep skill leave an Earnings Prep Note recording every returned row's ticker, change, score, and status exactly, plus what the skill's final step tells the analyst to produce for the PM across the three print outcomes.

- Initial workspace: dashboard "Earnings Prep Desk"; 1 tab(s): prep; 2 seeded widget(s): earnings_estimates_monitor_calendar_upcoming_earnings({"sector": "Healthcare", "ticker": "LLY", "period": "YTD"}), earnings_estimates_monitor_estimates_consensus_revisions({"sector": "Technology", "ticker": "AAPL", "period": "MTD"}); 1 seeded generated widget(s): note "Prior Prep Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Earnings Prep Desk" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `prep` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Prep Sheet Service/prep_register` on tab `prep` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_calendar_upcoming_earnings` with data_args ⊇ {"sector": "Healthcare", "ticker": "LLY", "period": "YTD"} on tab `prep` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_estimates_consensus_revisions` with data_args ⊇ {"sector": "Technology", "ticker": "AAPL", "period": "MTD"} on tab `prep` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Prep Note" whose content mentions "Prior prep: AAPL revisions remain under review; carry no assumptions into the NVDA preview." on tab `prep` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Earnings Prep Note" whose content mentions "AAPL", "-0.0581", "6.52", "TSLA", "0.0579", "73.24", "In Review", "action items", "beat", "miss", "in-line print" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_36b` must sit at exactly x=0, y=0, w=20, h=14 on tab `prep` → `layout_mismatch`
- **Layout** `w_b8a` must sit at exactly x=20, y=0, w=20, h=14 on tab `prep` → `layout_mismatch`
- **Layout** `w_b01` must sit at exactly x=0, y=14, w=20, h=8 on tab `prep` → `layout_mismatch`

#### `guidance_tracker_level0`

**level0** · category: story · specification: -

> On the open Guidance Watch dashboard, read Management Guidance from Bench Daloopa with ticker set to NFLX, then leave a Guidance Tracker Note recording these Pending 2026Q2 ranges exactly: Total Revenue Guidance at 14617.6 to 15062.8 USD mn, Diluted EPS Guidance at 7.68 to 7.91 USD, and Paid Memberships Guidance at 329.6 to 339.7 mn.

- Initial workspace: dashboard "Guidance Watch"; 1 tab(s): guidance
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Guidance Tracker Note" whose content mentions "Total Revenue Guidance", "14617.6", "15062.8", "USD mn", "Diluted EPS Guidance", "7.68", "7.91", "Paid Memberships Guidance", "329.6", "339.7" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `guidance_tracker_level1`

**level1** · category: story · specification: -

> Pull management's promises from Bench Daloopa for ticker NFLX onto the open Guidance Watch dashboard, then leave a Guidance Tracker Note recording these Pending 2026Q2 ranges exactly: Total Revenue Guidance at 14617.6 to 15062.8 USD mn, Diluted EPS Guidance at 7.68 to 7.91 USD, and Paid Memberships Guidance at 329.6 to 339.7 mn. The desk needs the guide before the review.

- Initial workspace: dashboard "Guidance Watch"; 1 tab(s): guidance
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Guidance Tracker Note" whose content mentions "Total Revenue Guidance", "14617.6", "15062.8", "USD mn", "Diluted EPS Guidance", "7.68", "7.91", "Paid Memberships Guidance", "329.6", "339.7" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `guidance_tracker_level2`

**level2** · category: story · specification: -

> On the open Guidance Watch dashboard, read Management Guidance from Bench Daloopa with the ticker set by the streaming coverage policy - the pure-play streaming name on coverage - then leave a Guidance Tracker Note recording every Pending 2026Q2 series and its exact guidance_low, guidance_high, and unit.

- Initial workspace: dashboard "Guidance Watch"; 1 tab(s): guidance
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Guidance Tracker Note" whose content mentions "Total Revenue Guidance", "14617.6", "15062.8", "USD mn", "Diluted EPS Guidance", "7.68", "7.91", "Paid Memberships Guidance", "329.6", "339.7" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `guidance_tracker_level3`

**level3** · category: story · specification: -

> On the open Guidance Watch dashboard, read Management Guidance from Bench Daloopa with ticker NFLX and keep everything already on the dashboard exactly as it is. Guidance reviews run under the Daloopa Guidance Tracker skill - leave a Guidance Tracker Note recording every Pending 2026Q2 series and its exact guidance_low, guidance_high, and unit, plus how that skill says to weight quarters when characterizing the trend.

- Initial workspace: dashboard "Guidance Watch"; 1 tab(s): guidance; 2 seeded widget(s): daloopa_management_guidance({"ticker": "MSFT"}), daloopa_company_directory({}); 1 seeded generated widget(s): note "Prior Guidance Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Guidance Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `guidance` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Daloopa/daloopa_management_guidance` with data_args ⊇ {"ticker": "MSFT"} on tab `guidance` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` on tab `guidance` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Guidance Note" whose content mentions "Prior review: MSFT open guide remains under review; carry no assumptions into the NFLX tracker." on tab `guidance` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Guidance Tracker Note" whose content mentions "Total Revenue Guidance", "14617.6", "15062.8", "USD mn", "Diluted EPS Guidance", "7.68", "7.91", "Paid Memberships Guidance", "329.6", "339.7", "recent quarters over old ones" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_1d4` must sit at exactly x=0, y=0, w=20, h=12 on tab `guidance` → `layout_mismatch`
- **Layout** `w_91e` must sit at exactly x=20, y=0, w=20, h=12 on tab `guidance` → `layout_mismatch`
- **Layout** `w_036` must sit at exactly x=0, y=12, w=20, h=8 on tab `guidance` → `layout_mismatch`

#### `guidance_tracker_level4`

**level4** · category: story · specification: -

> Build the desk's guidance-tracking workflow: add a Guidance Watch Service backend serving a Guidance Register table, publish Guidance Watch App with Guidance Register on its Guidance tab, and instantiate the app. On the open Guidance Watch dashboard, add the built Guidance Register and keep everything already there exactly as it is. Read Management Guidance from Bench Daloopa with ticker NFLX, then under the Daloopa Guidance Tracker skill leave a Guidance Tracker Note recording every Pending 2026Q2 series and its exact guidance_low, guidance_high, and unit, plus how that skill says to weight quarters when characterizing the trend.

- Initial workspace: dashboard "Guidance Watch"; 1 tab(s): guidance; 2 seeded widget(s): daloopa_management_guidance({"ticker": "MSFT"}), daloopa_company_directory({}); 1 seeded generated widget(s): note "Prior Guidance Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Guidance Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `guidance` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Guidance Watch Service/guidance_register` on tab `guidance` → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_management_guidance` with data_args ⊇ {"ticker": "MSFT"} on tab `guidance` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` on tab `guidance` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Guidance Note" whose content mentions "Prior review: MSFT open guide remains under review; carry no assumptions into the NFLX tracker." on tab `guidance` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Guidance Tracker Note" whose content mentions "Total Revenue Guidance", "14617.6", "15062.8", "USD mn", "Diluted EPS Guidance", "7.68", "7.91", "Paid Memberships Guidance", "329.6", "339.7", "recent quarters over old ones" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_1d4` must sit at exactly x=0, y=0, w=20, h=12 on tab `guidance` → `layout_mismatch`
- **Layout** `w_91e` must sit at exactly x=20, y=0, w=20, h=12 on tab `guidance` → `layout_mismatch`
- **Layout** `w_036` must sit at exactly x=0, y=12, w=20, h=8 on tab `guidance` → `layout_mismatch`

#### `inflection_scan_level0`

**level0** · category: story · specification: -

> On the open Inflection Scan dashboard, read Operating KPIs from Bench Daloopa with ticker set to TSLA and period set to 2026Q1, then leave an Inflection Scan Note recording each KPI and its exact value and unit for the quarter.

- Initial workspace: dashboard "Inflection Scan"; 1 tab(s): scan
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Inflection Scan Note" whose content mentions "Vehicle Deliveries", "509.3", "units k", "Energy Storage Deployed", "12.8", "GWh" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `inflection_scan_level1`

**level1** · category: story · specification: -

> Pull the KPI trends from Bench Daloopa for TSLA, period 2026Q1, and leave an Inflection Scan Note on the open Inflection Scan dashboard recording each KPI and its exact value and unit for the quarter.

- Initial workspace: dashboard "Inflection Scan"; 1 tab(s): scan
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Inflection Scan Note" whose content mentions "Vehicle Deliveries", "509.3", "units k", "Energy Storage Deployed", "12.8", "GWh" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `inflection_scan_level2`

**level2** · category: story · specification: -

> Read Operating KPIs from Bench Daloopa for ticker TSLA, with period set by the fresh-quarter scan policy - the newest covered quarter in the dataset - and leave an Inflection Scan Note on the open Inflection Scan dashboard recording each KPI and its exact value and unit for that quarter.

- Initial workspace: dashboard "Inflection Scan"; 1 tab(s): scan
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Inflection Scan Note" whose content mentions "Vehicle Deliveries", "509.3", "units k", "Energy Storage Deployed", "12.8", "GWh" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `inflection_scan_level3`

**level3** · category: story · specification: -

> On the open Inflection Scan dashboard, read Operating KPIs from Bench Daloopa with ticker TSLA and period 2026Q1, then leave an Inflection Scan Note recording each KPI and its exact value and unit for the quarter. The scan runs under the Daloopa Inflection skill - the note must also record the growth cadence that skill says to compute first and what it flags as inflections. Keep everything already on the dashboard exactly as it is.

- Initial workspace: dashboard "Inflection Scan"; 1 tab(s): scan; 2 seeded widget(s): daloopa_kpi_metrics({"ticker": "TSLA", "period": "2025Q4"}), daloopa_company_directory({}); 1 seeded generated widget(s): note "Prior Scan Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Inflection Scan" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `scan` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Daloopa/daloopa_kpi_metrics` with data_args ⊇ {"ticker": "TSLA", "period": "2025Q4"} on tab `scan` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` on tab `scan` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Scan Note" whose content mentions "Prior scan: NVDA networking cadence softened into 2026Q1; keep the source trail intact." on tab `scan` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Inflection Scan Note" whose content mentions "Vehicle Deliveries", "509.3", "units k", "Energy Storage Deployed", "12.8", "GWh", "quarter-over-quarter growth per series", "growth-rate reversals" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_acb` must sit at exactly x=0, y=0, w=20, h=12 on tab `scan` → `layout_mismatch`
- **Layout** `w_c8e` must sit at exactly x=20, y=0, w=20, h=12 on tab `scan` → `layout_mismatch`
- **Layout** `w_bf8` must sit at exactly x=0, y=12, w=20, h=8 on tab `scan` → `layout_mismatch`

#### `inflection_scan_level4`

**level4** · category: story · specification: -

> Build the quarter's scan register: add an Inflection Scan Service backend serving a Reversal Register table, publish Inflection Scan App with Reversal Register on its Reversals tab, and instantiate the app. On the open Inflection Scan dashboard, add the built Reversal Register and keep everything already there exactly as it is. Then run the scan under the Daloopa Inflection skill: read Operating KPIs from Bench Daloopa with ticker TSLA and period 2026Q1, and leave an Inflection Scan Note recording each KPI and its exact value and unit plus the growth cadence the skill says to compute first and what it flags as inflections.

- Initial workspace: dashboard "Inflection Scan"; 1 tab(s): scan; 2 seeded widget(s): daloopa_kpi_metrics({"ticker": "TSLA", "period": "2025Q4"}), daloopa_company_directory({}); 1 seeded generated widget(s): note "Prior Scan Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Inflection Scan" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `scan` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Inflection Scan Service/reversal_register` on tab `scan` → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_kpi_metrics` with data_args ⊇ {"ticker": "TSLA", "period": "2025Q4"} on tab `scan` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` on tab `scan` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Scan Note" whose content mentions "Prior scan: NVDA networking cadence softened into 2026Q1; keep the source trail intact." on tab `scan` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Inflection Scan Note" whose content mentions "Vehicle Deliveries", "509.3", "units k", "Energy Storage Deployed", "12.8", "GWh", "quarter-over-quarter growth per series", "growth-rate reversals" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_acb` must sit at exactly x=0, y=0, w=20, h=12 on tab `scan` → `layout_mismatch`
- **Layout** `w_c8e` must sit at exactly x=20, y=0, w=20, h=12 on tab `scan` → `layout_mismatch`
- **Layout** `w_bf8` must sit at exactly x=0, y=12, w=20, h=8 on tab `scan` → `layout_mismatch`

#### `peer_compare_level0`

**level0** · category: story · specification: -

> On the open Peer Compare dashboard, add Company Fundamentals from Bench Daloopa twice: one with ticker set to MSFT and period set to 2025Q2, and one with ticker set to AMZN and period set to 2025Q2. I want both names in the same peer read for the quarter.

- Initial workspace: dashboard "Peer Compare"; 1 tab(s): compare
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q2"} → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "AMZN", "period": "2025Q2"} → `missing_widget`

#### `peer_compare_level1`

**level1** · category: story · specification: -

> Put the fundamentals table from Bench Daloopa on the open Peer Compare dashboard twice, one for MSFT and one for AMZN, both at 2025Q2. I need the cloud names on the same quarter.

- Initial workspace: dashboard "Peer Compare"; 1 tab(s): compare
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q2"} → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "AMZN", "period": "2025Q2"} → `missing_widget`

#### `peer_compare_level2`

**level2** · category: story · specification: -

> On the open Peer Compare dashboard, add Company Fundamentals from Bench Daloopa twice for period 2025Q2, choosing MSFT for Microsoft's line and the other ticker per the cloud pair policy - Microsoft plus the other covered cloud name. Keep the quarter identical so the peer read is comparable.

- Initial workspace: dashboard "Peer Compare"; 1 tab(s): compare
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q2"} → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "AMZN", "period": "2025Q2"} → `missing_widget`

#### `peer_compare_level3`

**level3** · category: story · specification: -

> On the open Peer Compare dashboard, add Company Fundamentals from Bench Daloopa twice, one for MSFT at 2025Q2 and one for AMZN at 2025Q2, and keep everything already on the dashboard as is. Peer comparisons run under the Daloopa Industry skill - leave a Peer Compare Governance note recording where its first step says the comparable set comes from.

- Initial workspace: dashboard "Peer Compare"; 1 tab(s): compare; 2 seeded widget(s): daloopa_company_fundamentals({"ticker": "AAPL", "period": "2026Q1"}), daloopa_company_directory({}); 1 seeded generated widget(s): note "Prior Peer Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Peer Compare" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `compare` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q2"} on tab `compare` → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "AMZN", "period": "2025Q2"} on tab `compare` → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "AAPL", "period": "2026Q1"} on tab `compare` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` on tab `compare` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Peer Note" whose content mentions "Prior peer read: AAPL remained the reference name; do not roll that view into the cloud comparison." on tab `compare` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Peer Compare Governance" whose content mentions "daloopa_company_directory" on tab `compare` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_15d` must sit at exactly x=0, y=0, w=20, h=12 on tab `compare` → `layout_mismatch`
- **Layout** `w_9f5` must sit at exactly x=20, y=0, w=20, h=12 on tab `compare` → `layout_mismatch`
- **Layout** `w_63e` must sit at exactly x=0, y=12, w=20, h=8 on tab `compare` → `layout_mismatch`

#### `peer_compare_level4`

**level4** · category: story · specification: -

> Build the desk's peer comparison service for the quarter: add a Peer Compare Service backend serving a Peer Register table, publish Peer Compare App with Peer Register on its Peers tab, and instantiate the app. On the open Peer Compare dashboard, add the built Peer Register and Company Fundamentals from Bench Daloopa twice, one for MSFT at 2025Q2 and one for AMZN at 2025Q2, keeping everything already there as is. Read the Daloopa Industry skill and leave a Peer Compare Governance note recording where its first step says the comparable set comes from.

- Initial workspace: dashboard "Peer Compare"; 1 tab(s): compare; 2 seeded widget(s): daloopa_company_fundamentals({"ticker": "AAPL", "period": "2026Q1"}), daloopa_company_directory({}); 1 seeded generated widget(s): note "Prior Peer Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Peer Compare" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `compare` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Peer Compare Service/peer_register` on tab `compare` → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q2"} on tab `compare` → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "AMZN", "period": "2025Q2"} on tab `compare` → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "AAPL", "period": "2026Q1"} on tab `compare` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` on tab `compare` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Peer Note" whose content mentions "Prior peer read: AAPL remained the reference name; do not roll that view into the cloud comparison." on tab `compare` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Peer Compare Governance" whose content mentions "daloopa_company_directory" on tab `compare` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_15d` must sit at exactly x=0, y=0, w=20, h=12 on tab `compare` → `layout_mismatch`
- **Layout** `w_9f5` must sit at exactly x=20, y=0, w=20, h=12 on tab `compare` → `layout_mismatch`
- **Layout** `w_63e` must sit at exactly x=0, y=12, w=20, h=8 on tab `compare` → `layout_mismatch`
- **Tool result** of `manage_apps` must contain "Peer Compare App", "Peers", "Peer Compare Service" (agent must actually retrieve the data) → `missing_tool_result`

### trading_desk (20)

#### `best_execution_file_level0`

**level0** · category: story · specification: -

> Blotter up on the open Best-Ex Review dashboard: add Live Orders and Broker Scorecard from Bench Stark Enterprise's Execution Desk, both with parameters desk set to US Equity and period set to QTD.

- Initial workspace: dashboard "Best-Ex Review"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Best-Ex Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` with data_args ⊇ {"desk": "US Equity", "period": "QTD"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_fills_broker_scorecard` with data_args ⊇ {"desk": "US Equity", "period": "QTD"} → `missing_widget`

#### `best_execution_file_level1`

**level1** · category: story · specification: -

> Get the live-order blotter and Broker Scorecard onto the open Best-Ex Review dashboard from Bench Stark Enterprise's Execution Desk. Parameters US Equity and QTD for both.

- Initial workspace: dashboard "Best-Ex Review"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Best-Ex Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` with data_args ⊇ {"desk": "US Equity", "period": "QTD"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_fills_broker_scorecard` with data_args ⊇ {"desk": "US Equity", "period": "QTD"} → `missing_widget`

#### `best_execution_file_level2`

**level2** · category: story · specification: -

> Best-ex file on the open Best-Ex Review dashboard: add Live Orders and Broker Scorecard from Bench Stark Enterprise's Execution Desk. For both, set desk by the US desk review policy and period to QTD.

- Initial workspace: dashboard "Best-Ex Review"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Best-Ex Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` with data_args ⊇ {"desk": "US Equity", "period": "QTD"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_fills_broker_scorecard` with data_args ⊇ {"desk": "US Equity", "period": "QTD"} → `missing_widget`

#### `best_execution_file_level3`

**level3** · category: story · specification: -

> Best-ex file on the open Best-Ex Review dashboard: add Live Orders and Broker Scorecard from Bench Stark Enterprise's Execution Desk, both with parameters desk US Equity and period QTD. Keep everything already there exactly as is. Under the Finance Comps skill, leave a Best-Ex Governance note recording what it says deserves premium or discount and what not to do with them.

- Initial workspace: dashboard "Best-Ex Review"; 1 tab(s): review; 2 seeded widget(s): execution_desk_blotter_live_orders({"desk": "EU Equity", "period": "YTD"}), execution_desk_fills_broker_scorecard({"desk": "Macro", "period": "MTD"}); 1 seeded generated widget(s): note "Prior Best-Ex Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Best-Ex Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` with data_args ⊇ {"desk": "US Equity", "period": "QTD"} on tab `review` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_fills_broker_scorecard` with data_args ⊇ {"desk": "US Equity", "period": "QTD"} on tab `review` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` with data_args ⊇ {"desk": "EU Equity", "period": "YTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_fills_broker_scorecard` with data_args ⊇ {"desk": "Macro", "period": "MTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Best-Ex Note" whose content mentions "Prior review: retain the EU Equity routing sample for the committee appendix." on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Best-Ex Governance" whose content mentions "outliers deserve premium or discount rather than deleting them" on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_da6` must sit at exactly x=0, y=0, w=40, h=14 on tab `review` → `layout_mismatch`
- **Layout** `w_918` must sit at exactly x=0, y=14, w=40, h=14 on tab `review` → `layout_mismatch`
- **Layout** `w_19f` must sit at exactly x=0, y=28, w=20, h=8 on tab `review` → `layout_mismatch`

#### `best_execution_file_level4`

**level4** · category: story · specification: -

> Build the committee file: add a Best-Ex File Service backend serving a Best-Ex Register table; publish Best-Ex File App with Best-Ex Register on its Review tab; instantiate the app. On the open Best-Ex Review dashboard, add the built Best-Ex Register, Live Orders, and Broker Scorecard from Bench Stark Enterprise's Execution Desk, with parameters desk US Equity and period QTD on both desk widgets. Keep everything already there exactly as is. Read the Finance Comps skill and leave a Best-Ex Governance note recording what it says deserves premium or discount and what not to do with them.

- Initial workspace: dashboard "Best-Ex Review"; 1 tab(s): review; 2 seeded widget(s): execution_desk_blotter_live_orders({"desk": "EU Equity", "period": "YTD"}), execution_desk_fills_broker_scorecard({"desk": "Macro", "period": "MTD"}); 1 seeded generated widget(s): note "Prior Best-Ex Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Best-Ex Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Best-Ex File Service/best_ex_register` on tab `review` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` with data_args ⊇ {"desk": "US Equity", "period": "QTD"} on tab `review` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_fills_broker_scorecard` with data_args ⊇ {"desk": "US Equity", "period": "QTD"} on tab `review` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` with data_args ⊇ {"desk": "EU Equity", "period": "YTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_fills_broker_scorecard` with data_args ⊇ {"desk": "Macro", "period": "MTD"} on tab `review` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Best-Ex Note" whose content mentions "Prior review: retain the EU Equity routing sample for the committee appendix." on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Best-Ex Governance" whose content mentions "outliers deserve premium or discount rather than deleting them" on tab `review` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_da6` must sit at exactly x=0, y=0, w=40, h=14 on tab `review` → `layout_mismatch`
- **Layout** `w_918` must sit at exactly x=0, y=14, w=40, h=14 on tab `review` → `layout_mismatch`
- **Layout** `w_19f` must sit at exactly x=0, y=28, w=20, h=8 on tab `review` → `layout_mismatch`

#### `chart_deck_level0`

**level0** · category: story · specification: -

> On the open Chart Deck dashboard, add Getting Started's TradingView Chart and Getting Started's Plotly Heatmap with its color_scale parameter set to Viridis.

- Initial workspace: dashboard "Chart Deck"; 1 tab(s): deck
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Chart Deck" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Getting Started/udf` → `missing_widget`
- **Widget** ≥1× `Getting Started/plotly_heatmap` with data_args ⊇ {"color_scale": "Viridis"} → `missing_widget`

#### `chart_deck_level1`

**level1** · category: story · specification: -

> On the open Chart Deck dashboard, add the candles chart from Getting Started and Getting Started's Plotly Heatmap with its color_scale parameter set to Viridis.

- Initial workspace: dashboard "Chart Deck"; 1 tab(s): deck
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Chart Deck" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Getting Started/udf` → `missing_widget`
- **Widget** ≥1× `Getting Started/plotly_heatmap` with data_args ⊇ {"color_scale": "Viridis"} → `missing_widget`

#### `chart_deck_level2`

**level2** · category: story · specification: -

> Chart Deck on the open dashboard: add Getting Started's TradingView Chart and Getting Started's Plotly Heatmap. Set the heatmap's color scale under the house palette policy, the desk's blue-green-yellow standard.

- Initial workspace: dashboard "Chart Deck"; 1 tab(s): deck
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Chart Deck" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Getting Started/udf` → `missing_widget`
- **Widget** ≥1× `Getting Started/plotly_heatmap` with data_args ⊇ {"color_scale": "Viridis"} → `missing_widget`

#### `chart_deck_level3`

**level3** · category: story · specification: -

> On the open Chart Deck dashboard, switch the Getting Started Plotly Heatmap still on Plasma to house-palette Viridis through its color_scale parameter, and add Getting Started's TradingView Chart. Leave the rest alone: the Inferno heatmap is correct for the other desk and must stay untouched. Read Workspace session guidance; leave a Chart Deck Governance note recording its stable phrase for anchoring work to the current dashboard and tab.

- Initial workspace: dashboard "Chart Deck"; 1 tab(s): deck; 4 seeded widget(s): plotly_heatmap({"color_scale": "Plasma"}), sparkline_line({}), plotly_chart({}), plotly_heatmap({"color_scale": "Inferno"}); 1 seeded generated widget(s): note "Prior Deck Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Chart Deck" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `deck` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Getting Started/udf` on tab `deck` → `missing_widget`
- **Widget** ≥1× `Getting Started/plotly_heatmap` with data_args ⊇ {"color_scale": "Viridis"} on tab `deck` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/plotly_heatmap` with data_args ⊇ {"color_scale": "Inferno"} on tab `deck` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/sparkline_line` on tab `deck` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/plotly_chart` on tab `deck` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Deck Note" whose content mentions "Prior deck: keep the cross-section view on the alternate palette through the close." on tab `deck` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Chart Deck Governance" whose content mentions "current-dashboard current-tab session grounding" on tab `deck` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_249` must sit at exactly x=0, y=0, w=20, h=15 on tab `deck` → `layout_mismatch`
- **Layout** `w_e5e` must sit at exactly x=20, y=0, w=20, h=10 on tab `deck` → `layout_mismatch`
- **Layout** `w_4ef` must sit at exactly x=20, y=10, w=20, h=8 on tab `deck` → `layout_mismatch`
- **Layout** `w_c57` must sit at exactly x=0, y=18, w=40, h=15 on tab `deck` → `layout_mismatch`
- **Layout** `w_b75` must sit at exactly x=0, y=33, w=20, h=15 on tab `deck` → `layout_mismatch`

#### `chart_deck_level4`

**level4** · category: story · specification: -

> Build the side-screen deck before the open: add a Chart Deck Service backend serving a Deck Register table; publish Chart Deck App with Deck Register on its Deck tab; instantiate the app. On the open Chart Deck dashboard, switch the Getting Started Plotly Heatmap still on Plasma to house-palette Viridis through its color_scale parameter; add the built Deck Register and Getting Started's TradingView Chart. Leave the rest alone: the Inferno heatmap is correct for the other desk and must stay untouched. Read Workspace session guidance; leave a Chart Deck Governance note recording its stable phrase for anchoring work to the current dashboard and tab.

- Initial workspace: dashboard "Chart Deck"; 1 tab(s): deck; 4 seeded widget(s): plotly_heatmap({"color_scale": "Plasma"}), sparkline_line({}), plotly_chart({}), plotly_heatmap({"color_scale": "Inferno"}); 1 seeded generated widget(s): note "Prior Deck Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Chart Deck" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `deck` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Chart Deck Service/deck_register` on tab `deck` → `missing_widget`
- **Widget** ≥1× `Getting Started/udf` on tab `deck` → `missing_widget`
- **Widget** ≥1× `Getting Started/plotly_heatmap` with data_args ⊇ {"color_scale": "Viridis"} on tab `deck` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/plotly_heatmap` with data_args ⊇ {"color_scale": "Inferno"} on tab `deck` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/sparkline_line` on tab `deck` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/plotly_chart` on tab `deck` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Deck Note" whose content mentions "Prior deck: keep the cross-section view on the alternate palette through the close." on tab `deck` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Chart Deck Governance" whose content mentions "current-dashboard current-tab session grounding" on tab `deck` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_249` must sit at exactly x=0, y=0, w=20, h=15 on tab `deck` → `layout_mismatch`
- **Layout** `w_e5e` must sit at exactly x=20, y=0, w=20, h=10 on tab `deck` → `layout_mismatch`
- **Layout** `w_4ef` must sit at exactly x=20, y=10, w=20, h=8 on tab `deck` → `layout_mismatch`
- **Layout** `w_c57` must sit at exactly x=0, y=18, w=40, h=15 on tab `deck` → `layout_mismatch`
- **Layout** `w_b75` must sit at exactly x=0, y=33, w=20, h=15 on tab `deck` → `layout_mismatch`

#### `embed_shelf_level0`

**level0** · category: story · specification: -

> On the open Desk Shelf dashboard, add Getting Started's HTML Widget and Getting Started's Video Library with its video_name parameter set to OpenBB Workspace Demo.

- Initial workspace: dashboard "Desk Shelf"; 1 tab(s): shelf
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Desk Shelf" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Getting Started/html_widget` → `missing_widget`
- **Widget** ≥1× `Getting Started/get_video` with data_args ⊇ {"video_name": "OpenBB Workspace Demo"} → `missing_widget`

#### `embed_shelf_level1`

**level1** · category: story · specification: -

> On the open Desk Shelf dashboard, add the internal tools page from Getting Started and Getting Started's Video Library with its video_name parameter set to OpenBB Workspace Demo.

- Initial workspace: dashboard "Desk Shelf"; 1 tab(s): shelf
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Desk Shelf" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Getting Started/html_widget` → `missing_widget`
- **Widget** ≥1× `Getting Started/get_video` with data_args ⊇ {"video_name": "OpenBB Workspace Demo"} → `missing_widget`

#### `embed_shelf_level2`

**level2** · category: story · specification: -

> Desk Shelf on the open dashboard: add the Getting Started component selected by the interactive-dashboard widget policy, plus Getting Started's Video Library with its video_name parameter set to OpenBB Workspace Demo.

- Initial workspace: dashboard "Desk Shelf"; 1 tab(s): shelf
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Desk Shelf" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Getting Started/html_widget` → `missing_widget`
- **Widget** ≥1× `Getting Started/get_video` with data_args ⊇ {"video_name": "OpenBB Workspace Demo"} → `missing_widget`

#### `embed_shelf_level3`

**level3** · category: story · specification: -

> On the open Desk Shelf dashboard, switch the Getting Started Video Library still showing Open Data Platform Demo to the desk demo, OpenBB Workspace Demo, through its video_name parameter; add Getting Started's HTML Widget. Leave the rest alone: the separate Video Library already showing OpenBB Workspace Demo is correct for the other desk and must stay untouched. Read the build-an-app guide; leave a Shelf Governance note recording the final two actions it lists.

- Initial workspace: dashboard "Desk Shelf"; 1 tab(s): shelf; 4 seeded widget(s): get_video({"video_name": "Open Data Platform Demo"}), sparkline_line({}), get_video_with_transcript({"video_name": "Open Data Platform Demo"}), get_video({"video_name": "OpenBB Workspace Demo"}); 1 seeded generated widget(s): note "Prior Shelf Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Desk Shelf" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `shelf` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Getting Started/html_widget` on tab `shelf` → `missing_widget`
- **Widget** ≥2× `Getting Started/get_video` with data_args ⊇ {"video_name": "OpenBB Workspace Demo"} on tab `shelf` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/sparkline_line` on tab `shelf` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/get_video_with_transcript` with data_args ⊇ {"video_name": "Open Data Platform Demo"} on tab `shelf` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Shelf Note" whose content mentions "Prior shelf: keep the data-platform walkthrough available through the onboarding cycle." on tab `shelf` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Shelf Governance" whose content mentions "validate, and register" on tab `shelf` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_57a` must sit at exactly x=0, y=0, w=20, h=12 on tab `shelf` → `layout_mismatch`
- **Layout** `w_3cf` must sit at exactly x=20, y=0, w=20, h=10 on tab `shelf` → `layout_mismatch`
- **Layout** `w_d02` must sit at exactly x=20, y=10, w=20, h=8 on tab `shelf` → `layout_mismatch`
- **Layout** `w_190` must sit at exactly x=0, y=12, w=20, h=12 on tab `shelf` → `layout_mismatch`
- **Layout** `w_079` must sit at exactly x=20, y=18, w=20, h=12 on tab `shelf` → `layout_mismatch`

#### `embed_shelf_level4`

**level4** · category: story · specification: -

> Build the desk shelf before the open: add a Shelf Service backend serving a Shelf Register table; publish Shelf App with Shelf Register on its Shelf tab; instantiate the app. On the open Desk Shelf dashboard, switch the Getting Started Video Library still showing Open Data Platform Demo to the desk demo, OpenBB Workspace Demo, through its video_name parameter; add the built Shelf Register and Getting Started's HTML Widget. Leave the rest alone: the separate Video Library already showing OpenBB Workspace Demo is correct for the other desk and must stay untouched. Read the build-an-app guide; leave a Shelf Governance note recording the final two actions it lists.

- Initial workspace: dashboard "Desk Shelf"; 1 tab(s): shelf; 4 seeded widget(s): get_video({"video_name": "Open Data Platform Demo"}), sparkline_line({}), get_video_with_transcript({"video_name": "Open Data Platform Demo"}), get_video({"video_name": "OpenBB Workspace Demo"}); 1 seeded generated widget(s): note "Prior Shelf Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Desk Shelf" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `shelf` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Shelf Service/shelf_register` on tab `shelf` → `missing_widget`
- **Widget** ≥1× `Getting Started/html_widget` on tab `shelf` → `missing_widget`
- **Widget** ≥2× `Getting Started/get_video` with data_args ⊇ {"video_name": "OpenBB Workspace Demo"} on tab `shelf` → `missing_widget`; and ≤2 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/sparkline_line` on tab `shelf` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/get_video_with_transcript` with data_args ⊇ {"video_name": "Open Data Platform Demo"} on tab `shelf` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Shelf Note" whose content mentions "Prior shelf: keep the data-platform walkthrough available through the onboarding cycle." on tab `shelf` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Shelf Governance" whose content mentions "validate, and register" on tab `shelf` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_57a` must sit at exactly x=0, y=0, w=20, h=12 on tab `shelf` → `layout_mismatch`
- **Layout** `w_3cf` must sit at exactly x=20, y=0, w=20, h=10 on tab `shelf` → `layout_mismatch`
- **Layout** `w_d02` must sit at exactly x=20, y=10, w=20, h=8 on tab `shelf` → `layout_mismatch`
- **Layout** `w_190` must sit at exactly x=0, y=12, w=20, h=12 on tab `shelf` → `layout_mismatch`
- **Layout** `w_079` must sit at exactly x=20, y=18, w=20, h=12 on tab `shelf` → `layout_mismatch`

#### `tape_and_news_level0`

**level0** · category: story · specification: -

> On the open Desk Tape dashboard, read Getting Started's Sample News Feed with category set to business and limit set to 3, then leave a Tape Lead Note recording the exact lead title and author.

- Initial workspace: dashboard "Desk Tape"; 1 tab(s): tape
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Desk Tape" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Generated note** ≥1× named ~"Tape Lead Note" whose content mentions "Global Markets Rally on Positive Economic Data", "Robert Williams" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `tape_and_news_level1`

**level1** · category: story · specification: -

> On the open Desk Tape dashboard, read the newswire from Getting Started for business, limited to 3, then leave a Tape Lead Note recording the exact lead title and author.

- Initial workspace: dashboard "Desk Tape"; 1 tab(s): tape
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Desk Tape" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Generated note** ≥1× named ~"Tape Lead Note" whose content mentions "Global Markets Rally on Positive Economic Data", "Robert Williams" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `tape_and_news_level2`

**level2** · category: story · specification: -

> Tape check on the open Desk Tape dashboard: read Getting Started's Sample News Feed under the market-open tape policy with limit 3. Leave a Tape Lead Note recording the exact lead title and author.

- Initial workspace: dashboard "Desk Tape"; 1 tab(s): tape
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Desk Tape" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Generated note** ≥1× named ~"Tape Lead Note" whose content mentions "Global Markets Rally on Positive Economic Data", "Robert Williams" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `tape_and_news_level3`

**level3** · category: story · specification: -

> Tape check on the open Desk Tape dashboard: read Getting Started's Sample News Feed for business, limited to 3, and keep everything already there exactly as is. Under the Finance Tearsheet skill, leave a Tape Lead Note recording the exact lead title and author plus the first input its workflow gathers.

- Initial workspace: dashboard "Desk Tape"; 1 tab(s): tape; 2 seeded widget(s): sample_newsfeed({"category": "tech", "limit": 5}), sparkline_line({}); 1 seeded generated widget(s): note "Prior Tape Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Desk Tape" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `tape` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Getting Started/sample_newsfeed` with data_args ⊇ {"category": "tech", "limit": 5} on tab `tape` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/sparkline_line` on tab `tape` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Tape Note" whose content mentions "Prior session: technology headlines stayed pinned through the close." on tab `tape` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Tape Lead Note" whose content mentions "Global Markets Rally on Positive Economic Data", "Robert Williams", "price action" on tab `tape` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_474` must sit at exactly x=0, y=0, w=20, h=14 on tab `tape` → `layout_mismatch`
- **Layout** `w_fe7` must sit at exactly x=20, y=0, w=20, h=10 on tab `tape` → `layout_mismatch`
- **Layout** `w_540` must sit at exactly x=20, y=10, w=20, h=8 on tab `tape` → `layout_mismatch`

#### `tape_and_news_level4`

**level4** · category: story · specification: -

> Build the tape digest before the open: add a Tape Digest Service backend serving a Tape Register table; publish Tape Digest App with Tape Register on its Digest tab; instantiate the app. On the open Desk Tape dashboard, add the built Tape Register and keep everything already there exactly as is. Read Getting Started's Sample News Feed for business, limited to 3; under the Finance Tearsheet skill, leave a Tape Lead Note recording the exact lead title and author plus the first input its workflow gathers.

- Initial workspace: dashboard "Desk Tape"; 1 tab(s): tape; 2 seeded widget(s): sample_newsfeed({"category": "tech", "limit": 5}), sparkline_line({}); 1 seeded generated widget(s): note "Prior Tape Note"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Desk Tape" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `tape` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Tape Digest Service/tape_register` on tab `tape` → `missing_widget`
- **Widget** ≥1× `Getting Started/sample_newsfeed` with data_args ⊇ {"category": "tech", "limit": 5} on tab `tape` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/sparkline_line` on tab `tape` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× named ~"Prior Tape Note" whose content mentions "Prior session: technology headlines stayed pinned through the close." on tab `tape` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Generated note** ≥1× named ~"Tape Lead Note" whose content mentions "Global Markets Rally on Positive Economic Data", "Robert Williams", "price action" on tab `tape` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Layout** `w_474` must sit at exactly x=0, y=0, w=20, h=14 on tab `tape` → `layout_mismatch`
- **Layout** `w_fe7` must sit at exactly x=20, y=0, w=20, h=10 on tab `tape` → `layout_mismatch`
- **Layout** `w_540` must sit at exactly x=20, y=10, w=20, h=8 on tab `tape` → `layout_mismatch`


---

Total: 338 tasks.