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



## Suite: enterprise-apps-usage (192 tasks)

### curate (24)

#### `compliance_alert_review_level0`

**level0** · category: dashboard · specification: -

> Add Open Alert Metrics from Bench Stark Enterprise's Compliance Surveillance Hub to the current dashboard.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` → `missing_widget`

#### `compliance_alert_review_level1`

**level1** · category: dashboard · specification: -

> Next, add Policy Breaches from Bench Stark Enterprise's Compliance Surveillance Hub to the current dashboard.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_personal_trading_policy_breaches` → `missing_widget`

#### `compliance_alert_review_level2`

**level2** · category: dashboard · specification: -

> Place both Open Alert Metrics from Bench Stark Enterprise's Compliance Surveillance Hub; Policy Breaches from Bench Stark Enterprise's Compliance Surveillance Hub on the current dashboard.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_personal_trading_policy_breaches` → `missing_widget`

#### `compliance_alert_review_level3`

**level3** · category: dashboard · specification: -

> Pull together Open Alert Metrics from Bench Stark Enterprise's Compliance Surveillance Hub; Markdown Widget with Number Input from Getting Started on the current dashboard.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` → `missing_widget`
- **Widget** ≥1× `Getting Started/markdown_widget_with_number_input` → `missing_widget`

#### `compliance_alert_review_level4`

**level4** · category: dashboard · specification: -

> Under the Finance Guidance Tracker skill, add Open Alert Metrics from Bench Stark Enterprise's Compliance Surveillance Hub; Markdown Widget with Number Input from Getting Started, and add a Compliance-alert Governance note naming evidence gaps.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` → `missing_widget`
- **Widget** ≥1× `Getting Started/markdown_widget_with_number_input` → `missing_widget`
- **Generated note** ≥1× named ~"Compliance-alert Governance" whose content mentions "evidence gaps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `compliance_alert_review_level5`

**level5** · category: platform · specification: -

> Launch Buildout Compliance Review: add it with a Compliance Review Register table and publish and instantiate Compliance Review App on Review, following the workspace's widgets.json spec; also add Open Alert Metrics from Bench Stark Enterprise's Compliance Surveillance Hub; Markdown Widget with Number Input from Getting Started.  Follow the Finance Guidance Tracker skill and add a Compliance-alert Build Note recording the final thing its workflow lists.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Compliance Review/compliance_review_register` on tab `review` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_open_alert_metrics` → `missing_widget`
- **Widget** ≥1× `Getting Started/markdown_widget_with_number_input` → `missing_widget`
- **Generated note** ≥1× named ~"Compliance-alert Build Note" whose content mentions "evidence gaps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `decision_briefing_level0`

**level0** · category: single-widget · specification: -

> The PM wants Bench Stark Enterprise's Portfolio Command Center, Trade Ideas, on the open Pilot Decision Brief dashboard, with fund set to Flagship Long/Short and period set to YTD.

- Initial workspace: dashboard "Pilot Decision Brief"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "YTD"} → `missing_widget`

#### `decision_briefing_level1`

**level1** · category: single-widget · specification: -

> On the open Pilot Decision Brief dashboard, find Bench Stark Enterprise's Portfolio Command Center, Trade Ideas, and add it for Flagship Long/Short and YTD.

- Initial workspace: dashboard "Pilot Decision Brief"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "YTD"} → `missing_widget`

#### `decision_briefing_level2`

**level2** · category: single-widget · specification: -

> Prepare the open Pilot Decision Brief dashboard under the quarterly PM briefing policy. Add Bench Stark Enterprise's Portfolio Command Center, Trade Ideas, for Flagship Long/Short; quarterly means QTD.

- Initial workspace: dashboard "Pilot Decision Brief"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "QTD"} → `missing_widget`

#### `decision_briefing_level3`

**level3** · category: dashboard · specification: -

> Set up the open Pilot Decision Brief dashboard: place Bench Stark Enterprise's Portfolio Command Center, Trade Ideas, for Flagship Long/Short and QTD beside Getting Started's Car Manufacturer Performance for TSLA and 2024. Put Trade Ideas at x 0, y 0, width 20, height 14 and the manufacturer view at x 20, y 0, width 20, height 14.

- Initial workspace: dashboard "Pilot Decision Brief"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "QTD"} → `missing_widget`
- **Widget** ≥1× `Getting Started/company_performance` with data_args ⊇ {"company": "TSLA", "year": 2024} → `missing_widget`

#### `decision_briefing_level4`

**level4** · category: dashboard · specification: -

> Use Workspace session guidance to prepare the open Pilot Decision Brief dashboard: place Bench Stark Enterprise's Portfolio Command Center, Trade Ideas, for Flagship Long/Short and QTD beside Getting Started's Car Manufacturer Performance for TSLA and 2024. Put Trade Ideas at x 0, y 0, width 20, height 14 and the manufacturer view at x 20, y 0, width 20, height 14.

- Initial workspace: dashboard "Pilot Decision Brief"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "QTD"} → `missing_widget`
- **Widget** ≥1× `Getting Started/company_performance` with data_args ⊇ {"company": "TSLA", "year": 2024} → `missing_widget`

#### `decision_briefing_level5`

**level5** · category: platform · specification: -

> The PM needs a Decision Tile Backend with a Decision Summary Tile metric. Author and add it to the workspace's widgets.json spec, then instantiate its Decision Briefing App. On Briefing, place Bench Stark Enterprise's Portfolio Command Center, Trade Ideas, beside Getting Started's Car Manufacturer Performance at y 10, x 0 and x 20, each width 20 and height 14. Follow the Daloopa Capital Allocation skill and add a Decision Briefing Build Note recording what buybacks plus payouts are compared against.

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

> Add Live Orders from Bench Stark Enterprise's Execution Desk to the current dashboard.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` → `missing_widget`

#### `execution_quality_review_level1`

**level1** · category: dashboard · specification: -

> Next, add Broker Scorecard from Bench Stark Enterprise's Execution Desk to the current dashboard.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_fills_broker_scorecard` → `missing_widget`

#### `execution_quality_review_level2`

**level2** · category: dashboard · specification: -

> Place both Live Orders from Bench Stark Enterprise's Execution Desk; Broker Scorecard from Bench Stark Enterprise's Execution Desk on the current dashboard.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_fills_broker_scorecard` → `missing_widget`

#### `execution_quality_review_level3`

**level3** · category: dashboard · specification: -

> Pull together Live Orders from Bench Stark Enterprise's Execution Desk; Multi PDF Viewer - URL from Getting Started on the current dashboard.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` → `missing_widget`
- **Widget** ≥1× `Getting Started/multi_pdf_url` → `missing_widget`

#### `execution_quality_review_level4`

**level4** · category: dashboard · specification: -

> Under the Finance Comps skill, add Live Orders from Bench Stark Enterprise's Execution Desk; Multi PDF Viewer - URL from Getting Started, and add a Execution-quality Governance note naming outliers.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` → `missing_widget`
- **Widget** ≥1× `Getting Started/multi_pdf_url` → `missing_widget`
- **Generated note** ≥1× named ~"Execution-quality Governance" whose content mentions "outliers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_quality_review_level5`

**level5** · category: platform · specification: -

> Launch Buildout Execution Review: add it with a Execution Review Register table and publish and instantiate Execution Review App on Quality, following the workspace's widgets.json spec; also add Live Orders from Bench Stark Enterprise's Execution Desk; Multi PDF Viewer - URL from Getting Started.  Follow the Finance Comps skill and add a Execution-quality Build Note recording what it says deserve premium or discount.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Execution Review/execution_review_register` on tab `quality` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` → `missing_widget`
- **Widget** ≥1× `Getting Started/multi_pdf_url` → `missing_widget`
- **Generated note** ≥1× named ~"Execution-quality Build Note" whose content mentions "outliers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `market_telemetry_level0`

**level0** · category: single-widget · specification: -

> Add Getting Started's Stock Price Trends - Line Sparklines with First/Last Points to the open Rollout Market Telemetry dashboard.

- Initial workspace: dashboard "Rollout Market Telemetry"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/sparkline_line` → `missing_widget`

#### `market_telemetry_level1`

**level1** · category: single-widget · specification: -

> On the open Rollout Market Telemetry dashboard, add Getting Started's live-updating grid with real-time WebSocket updates for AAPL.

- Initial workspace: dashboard "Rollout Market Telemetry"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/live_grid_data` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`

#### `market_telemetry_level2`

**level2** · category: single-widget · specification: -

> Prepare the open Rollout Market Telemetry dashboard for the quarterly liquidity policy. Add Widget Examples' [MOCK DATA] Tabs + Dropdown Combined; quarterly liquidity means quarterly and liquidity. Place it at x 0, y 0, width 40, height 14.

- Initial workspace: dashboard "Rollout Market Telemetry"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/tabs_with_dropdown` with data_args ⊇ {"period": "quarterly", "category": "liquidity"} → `missing_widget`

#### `market_telemetry_level3`

**level3** · category: dashboard · specification: -

> Build out the open Rollout Market Telemetry dashboard with Getting Started's Stock Price Trends - Line Sparklines with First/Last Points beside Widget Examples' [MOCK DATA] Tabs + Dropdown Combined for quarterly liquidity. Put the trends at x 0, y 0, width 20, height 12 and the ratio view at x 20, y 0, width 20, height 12.

- Initial workspace: dashboard "Rollout Market Telemetry"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/sparkline_line` → `missing_widget`
- **Widget** ≥1× `Widget Examples/tabs_with_dropdown` with data_args ⊇ {"period": "quarterly", "category": "liquidity"} → `missing_widget`

#### `market_telemetry_level4`

**level4** · category: dashboard · specification: -

> Using Workspace session guidance, finish the open Rollout Market Telemetry dashboard with Getting Started's Stock Price Trends - Line Sparklines with First/Last Points beside Widget Examples' [MOCK DATA] Tabs + Dropdown Combined for quarterly liquidity. Put them at x 0 and x 20, y 0, each width 20 and height 12.

- Initial workspace: dashboard "Rollout Market Telemetry"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/sparkline_line` → `missing_widget`
- **Widget** ≥1× `Widget Examples/tabs_with_dropdown` with data_args ⊇ {"period": "quarterly", "category": "liquidity"} → `missing_widget`

#### `market_telemetry_level5`

**level5** · category: platform · specification: -

> Author and add a Telemetry Summary Backend with a Telemetry Summary Tile metric, then instantiate its Market Telemetry App. On Monitor, place Getting Started's Stock Price Trends - Line Sparklines with First/Last Points beside Widget Examples' [MOCK DATA] Tabs + Dropdown Combined at y 10, x 0 and x 20, each width 20 and height 12. Follow the Finance Tearsheet skill and add a Market Telemetry Build Note recording the first input its workflow gathers.

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

> Add a Buildout Guidance Service custom backend with the Evidence Gaps table.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `guidance_service_lifecycle_level1`

**level1** · category: platform · specification: -

> Spin up Buildout Guidance Service with the Changed Assumptions table - add it as a custom backend.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `guidance_service_lifecycle_level2`

**level2** · category: platform · specification: -

> Set up Buildout Guidance Service with Evidence Gaps and Changed Assumptions tables - add it as a custom backend.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `guidance_service_lifecycle_level3`

**level3** · category: platform · specification: -

> Publish Buildout Guidance Service as an app: add the backend with Evidence Gaps and Changed Assumptions tables, publish Guidance Service App on Review, and instantiate it.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Guidance Service/evidence_gaps` on tab `review` → `missing_widget`
- **Widget** ≥1× `Buildout Guidance Service/changed_assumptions` on tab `review` → `missing_widget`

#### `guidance_service_lifecycle_level4`

**level4** · category: platform · specification: -

> In line with the Finance Guidance Tracker skill, add a custom backend Buildout Guidance Service with Evidence Gaps and Changed Assumptions tables, publish Guidance Service App on Review, and instantiate it.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Guidance Service/evidence_gaps` on tab `review` → `missing_widget`
- **Widget** ≥1× `Buildout Guidance Service/changed_assumptions` on tab `review` → `missing_widget`

#### `guidance_service_lifecycle_level5`

**level5** · category: platform · specification: -

> Build Buildout Guidance Service end to end, following the widgets.json spec: add the backend with Evidence Gaps, Changed Assumptions, Management Claims tables, publish Guidance Service App with Evidence Gaps and Changed Assumptions on Review and Management Claims on Archive, and instantiate it. Follow the Finance Guidance Tracker skill and add a Guidance-service Governing Note recording what management claims are compared with.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Guidance Service/evidence_gaps` on tab `review` → `missing_widget`
- **Widget** ≥1× `Buildout Guidance Service/changed_assumptions` on tab `review` → `missing_widget`
- **Widget** ≥1× `Buildout Guidance Service/management_claims` on tab `archive` → `missing_widget`
- **Generated note** ≥1× named ~"Guidance-service Governing Note" whose content mentions "prior guidance" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `inflection_service_lifecycle_level0`

**level0** · category: platform · specification: -

> Add a Buildout Inflection Service custom backend with the Growth-Rate Reversals table.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `inflection_service_lifecycle_level1`

**level1** · category: platform · specification: -

> Spin up Buildout Inflection Service with the Quarterly Series Monitor table - add it as a custom backend.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `inflection_service_lifecycle_level2`

**level2** · category: platform · specification: -

> Set up Buildout Inflection Service with Growth-Rate Reversals and Quarterly Series Monitor tables - add it as a custom backend.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `inflection_service_lifecycle_level3`

**level3** · category: platform · specification: -

> Publish Buildout Inflection Service as an app: add the backend with Growth-Rate Reversals and Quarterly Series Monitor tables, publish Inflection Service App on Review, and instantiate it.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Inflection Service/growth_rate_reversals` on tab `review` → `missing_widget`
- **Widget** ≥1× `Buildout Inflection Service/quarterly_series_monitor` on tab `review` → `missing_widget`

#### `inflection_service_lifecycle_level4`

**level4** · category: platform · specification: -

> In line with the Daloopa Inflection skill, add a custom backend Buildout Inflection Service with Growth-Rate Reversals and Quarterly Series Monitor tables, publish Inflection Service App on Review, and instantiate it.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Inflection Service/growth_rate_reversals` on tab `review` → `missing_widget`
- **Widget** ≥1× `Buildout Inflection Service/quarterly_series_monitor` on tab `review` → `missing_widget`

#### `inflection_service_lifecycle_level5`

**level5** · category: platform · specification: -

> Build Buildout Inflection Service end to end, following the widgets.json spec: add the backend with Growth-Rate Reversals, Quarterly Series Monitor, Inflection Evidence Log tables, publish Inflection Service App with Growth-Rate Reversals and Quarterly Series Monitor on Review and Inflection Evidence Log on Archive, and instantiate it. Follow the Daloopa Inflection skill and add a Inflection-service Governing Note recording the first growth cadence it computes.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Inflection Service/growth_rate_reversals` on tab `review` → `missing_widget`
- **Widget** ≥1× `Buildout Inflection Service/quarterly_series_monitor` on tab `review` → `missing_widget`
- **Widget** ≥1× `Buildout Inflection Service/inflection_evidence_log` on tab `archive` → `missing_widget`
- **Generated note** ≥1× named ~"Inflection-service Governing Note" whose content mentions "quarter-over-quarter" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `research_feed_lifecycle_level0`

**level0** · category: platform · specification: -

> On the open Research Feed Staging dashboard, review the connected backends and refresh Rollout Research Feed so Research Feed Pulse has the description Refreshed research feed.

- Initial workspace: dashboard "Research Feed Staging"; 1 tab(s): feed; 1 seeded widget(s): research_feed_pulse({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `research_feed_lifecycle_level1`

**level1** · category: platform · specification: -

> Add a minimal Rollout Research Feed backend serving a Research Feed Pulse table at /research-feed.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `research_feed_lifecycle_level2`

**level2** · category: platform · specification: -

> From the open Research Feed Staging dashboard, review the connected backends, then refresh Rollout Research Feed so Research Feed App has one non-overlapping Research Feed Pulse placement on Feed.

- Initial workspace: dashboard "Research Feed Staging"; 1 tab(s): feed; 1 seeded widget(s): research_feed_pulse({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `research_feed_lifecycle_level3`

**level3** · category: platform · specification: -

> Publish and add Rollout Research Feed with Research Feed Pulse and a Research Feed App containing Feed.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `research_feed_lifecycle_level4`

**level4** · category: platform · specification: -

> Set up and add Rollout Research Feed with Research Feed Pulse and Source Freshness Alert, publish Research Feed App with both on Feed, and instantiate it.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Rollout Research Feed/research_feed_pulse` on tab `feed` → `missing_widget`
- **Widget** ≥1× `Rollout Research Feed/source_freshness_alert` on tab `feed` → `missing_widget`

#### `research_feed_lifecycle_level5`

**level5** · category: platform · specification: -

> Complete the research service with Rollout Research Feed, Research Feed Pulse, Source Freshness Alert, and Archive Coverage Watch. Add the backend, publish Research Feed App with Research Feed Pulse and Source Freshness Alert on Feed and Archive Coverage Watch on Archive, and instantiate it.  Follow the Daloopa Capital Allocation skill and add a Research Feed Build Note recording the payout item added to buybacks in its comparison.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Rollout Research Feed/research_feed_pulse` on tab `feed` → `missing_widget`
- **Widget** ≥1× `Rollout Research Feed/source_freshness_alert` on tab `feed` → `missing_widget`
- **Widget** ≥1× `Rollout Research Feed/archive_coverage_watch` on tab `archive` → `missing_widget`
- **Generated note** ≥1× named ~"Research Feed Build Note" whose content mentions "Dividends Paid" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `risk_service_lifecycle_level0`

**level0** · category: platform · specification: -

> On the open Risk Service Staging dashboard, review the connected backends and refresh Pilot Risk Service so its Pilot Risk Signal description is Refreshed risk signal feed.

- Initial workspace: dashboard "Risk Service Staging"; 1 tab(s): monitor; 1 seeded widget(s): pilot_risk_signal({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `risk_service_lifecycle_level1`

**level1** · category: platform · specification: -

> Add a minimal Pilot Risk Service backend that serves a Pilot Risk Signal table at /risk-signal.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `risk_service_lifecycle_level2`

**level2** · category: platform · specification: -

> Review the connected backends on the open Risk Service Staging dashboard, then refresh Pilot Risk Service so Pilot Risk App has one non-overlapping Pilot Risk Signal placement on Monitor.

- Initial workspace: dashboard "Risk Service Staging"; 1 tab(s): monitor; 1 seeded widget(s): pilot_risk_signal({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `risk_service_lifecycle_level3`

**level3** · category: platform · specification: -

> The risk desk needs Pilot Risk Service with its Pilot Risk Signal and a Pilot Risk App containing Monitor. Publish and add it.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `risk_service_lifecycle_level4`

**level4** · category: platform · specification: -

> Set up Pilot Risk Service with Pilot Risk Signal and Pilot Limit Alert. Author and add the service, publish Pilot Risk App with both on Monitor, and instantiate it.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Pilot Risk Service/pilot_risk_signal` on tab `monitor` → `missing_widget`
- **Widget** ≥1× `Pilot Risk Service/pilot_limit_alert` on tab `monitor` → `missing_widget`

#### `risk_service_lifecycle_level5`

**level5** · category: platform · specification: -

> Complete the risk desk build with Pilot Risk Service, Pilot Risk Signal, Pilot Limit Alert, and Pilot Stress Watch. Add the service, publish Pilot Risk App with Pilot Risk Signal and Pilot Limit Alert on Monitor and Pilot Stress Watch on Stress, and instantiate it.  Follow the Finance Guidance Tracker skill and add a Risk Service Build Note recording the final thing its workflow lists.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Pilot Risk Service/pilot_risk_signal` on tab `monitor` → `missing_widget`
- **Widget** ≥1× `Pilot Risk Service/pilot_limit_alert` on tab `monitor` → `missing_widget`
- **Widget** ≥1× `Pilot Risk Service/pilot_stress_watch` on tab `stress` → `missing_widget`
- **Generated note** ≥1× named ~"Risk Service Build Note" whose content mentions "evidence gaps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### handoff (24)

#### `consensus_exception_handoff_level0`

**level0** · category: read · specification: -

> Read Consensus Estimates from Bench Daloopa on the open Consensus Exception Handoff dashboard with ticker AAPL, then add a Consensus-exception Direct Note recording the exact Total Revenue actual and consensus for 2026Q1.

- Initial workspace: dashboard "Consensus Exception Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Consensus-exception Direct Note" whose content mentions "102070.1", "99404.2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `consensus_exception_handoff_level1`

**level1** · category: read · specification: -

> Desk log - read Consensus Estimates from Bench Daloopa on the open Consensus Exception Handoff dashboard with ticker AAPL, then add a Consensus-exception Discovered Note recording the exact Total Revenue actual and consensus for 2026Q1.

- Initial workspace: dashboard "Consensus Exception Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Consensus-exception Discovered Note" whose content mentions "102070.1", "99404.2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `consensus_exception_handoff_level2`

**level2** · category: read · specification: -

> Handoff capture - read Consensus Estimates from Bench Daloopa on the open Consensus Exception Handoff dashboard with ticker AAPL, then add a Consensus-exception Analyst Note recording the exact Total Revenue actual and consensus for 2026Q1.

- Initial workspace: dashboard "Consensus Exception Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Consensus-exception Analyst Note" whose content mentions "102070.1", "99404.2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `consensus_exception_handoff_level3`

**level3** · category: read · specification: -

> Day wrap - read Consensus Estimates from Bench Daloopa on the open Consensus Exception Handoff dashboard with ticker AAPL, then add a Consensus-exception Desk Note recording the exact Total Revenue actual and consensus for 2026Q1.

- Initial workspace: dashboard "Consensus Exception Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Consensus-exception Desk Note" whose content mentions "102070.1", "99404.2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `consensus_exception_handoff_level4`

**level4** · category: dashboard · specification: -

> Close out the open Consensus Exception Handoff dashboard under the Daloopa Earnings Review skill: read Bench Daloopa's Consensus Estimates with ticker AAPL, add a Consensus-exception Governed Handoff note recording the exact Total Revenue actual and consensus for 2026Q1 and consensus, then delegate the follow-up.

- Initial workspace: dashboard "Consensus Exception Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Consensus-exception Governed Handoff" whose content mentions "consensus", "102070.1", "99404.2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `consensus_exception_handoff_level5`

**level5** · category: platform · specification: -

> Finish Consensus Exception Handoff with a build: add Buildout Consensus Handoff with a Consensus Handoff Register table per the workspace's widgets.json spec, publish and instantiate Consensus Handoff App with one Handoff tab, add a Consensus-exception Build Handoff note grounded in Bench Daloopa's Consensus Estimates with the exact Total Revenue actual and consensus for 2026Q1 and, from the Daloopa Earnings Review skill, what it tallies as Beat, In Line, and Missed, then delegate.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Consensus Handoff/consensus_handoff_register` on tab `handoff` → `missing_widget`
- **Generated note** ≥1× named ~"Consensus-exception Build Handoff" whose content mentions "verdicts", "102070.1", "99404.2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_handoff_level0`

**level0** · category: read · specification: -

> On the open Earnings Handoff dashboard, read Bench Stark Enterprise's Earnings & Estimates Monitor, Upcoming Earnings, for Healthcare, LLY, and YTD. Add an LLY Earnings Handoff note with the exact score and status.

- Initial workspace: dashboard "Earnings Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"LLY Earnings Handoff" whose content mentions "27.63", "Open" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_handoff_level1`

**level1** · category: read · specification: -

> Build the Apple note on the open Earnings Handoff dashboard. Find Bench Stark Enterprise's Earnings & Estimates Monitor, Upcoming Earnings, for Technology, AAPL, and QTD, then add an Apple Earnings Handoff note with the exact score and status.

- Initial workspace: dashboard "Earnings Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Apple Earnings Handoff" whose content mentions "6.52", "In Review" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_handoff_level2`

**level2** · category: read · specification: -

> Prepare a Microsoft note on the open Earnings Handoff dashboard under the current-month handoff policy. Read Bench Stark Enterprise's Earnings & Estimates Monitor, Upcoming Earnings, for Technology and MSFT; current month means MTD. Add a Microsoft Earnings Handoff note with the exact score and status.

- Initial workspace: dashboard "Earnings Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Microsoft Earnings Handoff" whose content mentions "89.94", "Escalated" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_handoff_level3`

**level3** · category: platform · specification: -

> For the open Earnings Handoff dashboard, follow Finance Earnings Prep governance and read Bench Stark Enterprise's Earnings & Estimates Monitor, Upcoming Earnings, for Technology, AAPL, and QTD. Add a Governed Apple Handoff note with the exact score and status.

- Initial workspace: dashboard "Earnings Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Governed Apple Handoff" whose content mentions "6.52", "In Review" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_handoff_level4`

**level4** · category: platform · specification: -

> Handle the coverage follow-up route from the open Earnings Handoff dashboard under Finance Earnings Prep governance. Read Bench Stark Enterprise's Earnings & Estimates Monitor, Upcoming Earnings, for Healthcare, LLY, and YTD; add an LLY Delegation Handoff note with exact score and status, then delegate the coverage follow-up.

- Initial workspace: dashboard "Earnings Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"LLY Delegation Handoff" whose content mentions "27.63", "Open" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_handoff_level5`

**level5** · category: platform · specification: -

> From the open Earnings Handoff dashboard, author and add a minimal custom Earnings Handoff Backend with one Earnings Handoff Register. Publish and instantiate Earnings Handoff App with one Handoff tab, add an Earnings Build Handoff note naming Earnings Handoff App and Earnings Handoff Register, then delegate the build-review follow-up. Follow the Finance Earnings Prep skill and record in the note what internal estimates are compared to.

- Initial workspace: dashboard "Earnings Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Earnings Handoff Backend/earnings_handoff_register` on tab `handoff` → `missing_widget`
- **Generated note** ≥1× named ~"Earnings Build Handoff" whose content mentions "Earnings Handoff App", "Earnings Handoff Register", "street numbers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `news_desk_handoff_level0`

**level0** · category: read · specification: -

> On the open News Desk Handoff dashboard, read Getting Started's Sample News Feed with category set to business and limit set to 2. Add a Markets News Handoff note with the exact lead title and author.

- Initial workspace: dashboard "News Desk Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Markets News Handoff" whose content mentions "Global Markets Rally on Positive Economic Data", "Robert Williams" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `news_desk_handoff_level1`

**level1** · category: read · specification: -

> Find Getting Started's Sample News Feed from the open News Desk Handoff dashboard for technology, limited to 2, then add a Technology News Handoff note with the exact lead title and author.

- Initial workspace: dashboard "News Desk Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Technology News Handoff" whose content mentions "AI Breakthrough: New Model Achieves Human-Level Reasoning", "Sarah Johnson" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `news_desk_handoff_level2`

**level2** · category: read · specification: -

> Prepare a Science News Handoff note on the open News Desk Handoff dashboard under the science route. Read Getting Started's Sample News Feed for that route, limited to 2, and pin the exact lead title and author.

- Initial workspace: dashboard "News Desk Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Science News Handoff" whose content mentions "Scientists Discover New Earth-like Exoplanet in Habitable Zone", "Dr. Emily Rogers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `news_desk_handoff_level3`

**level3** · category: platform · specification: -

> Using Workspace session guidance on the open News Desk Handoff dashboard, read Getting Started's Sample News Feed for business, limited to 2. Add a Governed Expansion Handoff note with the exact second title and author.

- Initial workspace: dashboard "News Desk Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Governed Expansion Handoff" whose content mentions "E-commerce Giant Announces Major Expansion into Southeast Asia", "Lisa Anderson" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `news_desk_handoff_level4`

**level4** · category: platform · specification: -

> Handle the science follow-up route from the open News Desk Handoff dashboard under Workspace session guidance. Read Getting Started's Sample News Feed for science, limited to 2; add a Science Delegation Handoff note with the exact lead title and author, then delegate the editorial follow-up.

- Initial workspace: dashboard "News Desk Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Science Delegation Handoff" whose content mentions "Scientists Discover New Earth-like Exoplanet in Habitable Zone", "Dr. Emily Rogers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `news_desk_handoff_level5`

**level5** · category: platform · specification: -

> Starting from the open News Desk Handoff dashboard, author and add a minimal custom News Handoff Backend with one News Handoff Register. Publish and instantiate News Handoff App with one Handoff tab, add a News Build Handoff note naming News Handoff App and News Handoff Register, then delegate the build-review follow-up. Follow the Finance Tearsheet skill and record in the note the input it gathers between valuation and risks.

- Initial workspace: dashboard "News Desk Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `News Handoff Backend/news_handoff_register` on tab `handoff` → `missing_widget`
- **Generated note** ≥1× named ~"News Build Handoff" whose content mentions "News Handoff App", "News Handoff Register", "catalysts" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `segment_mix_handoff_level0`

**level0** · category: read · specification: -

> Read Segment Breakdown from Bench Daloopa on the open Segment Mix Handoff dashboard with ticker AAPL, period 2026Q1, then add a Segment-mix Direct Note recording the top segment and its exact revenue_musd.

- Initial workspace: dashboard "Segment Mix Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Segment-mix Direct Note" whose content mentions "iPhone", "52365.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `segment_mix_handoff_level1`

**level1** · category: read · specification: -

> Desk log - read Segment Breakdown from Bench Daloopa on the open Segment Mix Handoff dashboard with ticker AAPL, period 2026Q1, then add a Segment-mix Discovered Note recording the top segment and its exact revenue_musd.

- Initial workspace: dashboard "Segment Mix Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Segment-mix Discovered Note" whose content mentions "iPhone", "52365.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `segment_mix_handoff_level2`

**level2** · category: read · specification: -

> Handoff capture - read Segment Breakdown from Bench Daloopa on the open Segment Mix Handoff dashboard with ticker AAPL, period 2026Q1, then add a Segment-mix Analyst Note recording the top segment and its exact revenue_musd.

- Initial workspace: dashboard "Segment Mix Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Segment-mix Analyst Note" whose content mentions "iPhone", "52365.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `segment_mix_handoff_level3`

**level3** · category: read · specification: -

> Day wrap - read Segment Breakdown from Bench Daloopa on the open Segment Mix Handoff dashboard with ticker AAPL, period 2026Q1, then add a Segment-mix Desk Note recording the top segment and its exact revenue_musd.

- Initial workspace: dashboard "Segment Mix Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Segment-mix Desk Note" whose content mentions "iPhone", "52365.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `segment_mix_handoff_level4`

**level4** · category: dashboard · specification: -

> Close out the open Segment Mix Handoff dashboard under the Daloopa Tearsheet skill: read Bench Daloopa's Segment Breakdown with ticker AAPL, period 2026Q1, add a Segment-mix Governed Handoff note recording the top segment and its exact revenue_musd and mix, then delegate the follow-up.

- Initial workspace: dashboard "Segment Mix Handoff"; 1 tab(s): review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Segment-mix Governed Handoff" whose content mentions "mix", "iPhone", "52365.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `segment_mix_handoff_level5`

**level5** · category: platform · specification: -

> Finish Segment Mix Handoff with a build: add Buildout Segment Handoff with a Segment Handoff Register table per the workspace's widgets.json spec, publish and instantiate Segment Handoff App with one Handoff tab, add a Segment-mix Build Handoff note grounded in Bench Daloopa's Segment Breakdown with the top segment and its exact revenue_musd and, from the Daloopa Tearsheet skill, the anchor it uses for all period math, then delegate.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Segment Handoff/segment_handoff_register` on tab `handoff` → `missing_widget`
- **Generated note** ≥1× named ~"Segment-mix Build Handoff" whose content mentions "latest_calendar_quarter", "iPhone", "52365.6" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### organize (24)

#### `client_onboarding_flow_level0`

**level0** · category: dashboard · specification: -

> For client operations, create a dashboard named Rollout Client Onboarding and make it the active dashboard.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `client_onboarding_flow_level1`

**level1** · category: dashboard · specification: -

> Create and activate Rollout Client Onboarding with Intake and Review tabs for the operations team.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `client_onboarding_flow_level2`

**level2** · category: dashboard · specification: -

> Operations needs you to create and activate Rollout Client Onboarding with Intake, Review, and Approval tabs, then open Review.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Rollout Client Onboarding" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `intake` must exist (matched by tab id) → `missing_tab`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`
- **Tab** `approval` must exist (matched by tab id) → `missing_tab`

#### `client_onboarding_flow_level3`

**level3** · category: dashboard · specification: -

> On the open Client Onboarding Staging dashboard, rename the dashboard to Rollout Client Onboarding and change Intake to Client Intake. Preserve Review and every other workspace item.

- Initial workspace: dashboard "Client Onboarding Staging"; 2 tab(s): intake, review
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `client_onboarding_flow_level4`

**level4** · category: dashboard · specification: -

> Client operations needs a governed setup: following Workspace session guidance, create and activate Rollout Client Onboarding with Client Intake, Due Diligence, and Approval tabs in that order.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `client_onboarding_flow_level5`

**level5** · category: platform · specification: -

> Author and add a Client Onboarding Backend with Client Intake Queue and Approval Log table views, then publish and instantiate a Client Onboarding App with Intake and Approvals tabs. Follow the apps.json spec.  Follow the Finance Guidance Tracker skill and add a Client Onboarding Build Note recording what it flags after comparing claims with guidance.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Client Onboarding Backend/client_intake_queue` on tab `intake` → `missing_widget`
- **Widget** ≥1× `Client Onboarding Backend/approval_log` on tab `approvals` → `missing_widget`
- **Generated note** ≥1× named ~"Client Onboarding Build Note" whose content mentions "changed assumptions" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `committee_navigation_level0`

**level0** · category: dashboard · specification: -

> Create a dashboard named Pilot Committee Review for the committee and make it the active dashboard.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `committee_navigation_level1`

**level1** · category: dashboard · specification: -

> Create Pilot Committee Review as the active committee dashboard, with Agenda and Evidence tabs.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `committee_navigation_level2`

**level2** · category: dashboard · specification: -

> The committee needs an active Pilot Committee Review dashboard with Agenda and Evidence tabs. Create it, then open Evidence.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Pilot Committee Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `agenda` must exist (matched by tab id) → `missing_tab`
- **Tab** `evidence` must exist (matched by tab id) → `missing_tab`

#### `committee_navigation_level3`

**level3** · category: dashboard · specification: -

> On the open Committee Review Staging dashboard, rename the dashboard to Pilot Committee Review and change its Agenda tab to Decision Agenda. Keep Evidence and all other workspace content intact.

- Initial workspace: dashboard "Committee Review Staging"; 2 tab(s): agenda, evidence
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `committee_navigation_level4`

**level4** · category: dashboard · specification: -

> Following Workspace session guidance, create and activate Pilot Committee Review with Decision Agenda, Evidence, and Sign-Off tabs in that order.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `committee_navigation_level5`

**level5** · category: platform · specification: -

> The committee needs a Committee Navigation Backend with Agenda Queue and Evidence Register table views. Author and add it, publish a Committee Review App with Agenda and Evidence tabs, and instantiate it. Follow the apps.json spec. Follow the Finance Earnings Prep skill and add a Committee Navigation Build Note recording what it inspects just before producing action items.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Committee Navigation Backend/agenda_queue` on tab `agenda` → `missing_widget`
- **Widget** ≥1× `Committee Navigation Backend/evidence_register` on tab `evidence` → `missing_widget`
- **Generated note** ≥1× named ~"Committee Navigation Build Note" whose content mentions "transcript tone" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `due_diligence_media_room_level0`

**level0** · category: dashboard · specification: -

> Create a dashboard named Due Diligence Media Room and open it.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Due Diligence Media Room" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`

#### `due_diligence_media_room_level1`

**level1** · category: dashboard · specification: -

> Set up Due Diligence Media Room: create and open it, then add Overview and Review tabs.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Due Diligence Media Room" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`

#### `due_diligence_media_room_level2`

**level2** · category: dashboard · specification: -

> Build Due Diligence Media Room from scratch: create and open it, add Overview and Review tabs, then add Getting Started's Video Library with Transcript.

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

> Lay out Due Diligence Media Room end to end: create and open it, add Overview and Review tabs, then add Getting Started's Video Library with Transcript, Getting Started's PDF Widget with URL.

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

> Apply the Finance Tearsheet skill: create and open Due Diligence Media Room, add Catalysts and Risks tabs, and add Getting Started's Video Library with Transcript, Widget Examples's URL PDF files.

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

> Assemble Buildout Media Room: add it with a Media Review Register table, publish and instantiate Media Room App on Media, following the workspace's widgets.json spec, then add Getting Started's PDF Widget with URL, Widget Examples's URL PDF files.  Follow the Finance Tearsheet skill and add a Media-room Build Note recording the input it gathers between valuation and risks.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Media Room/media_review_register` on tab `media` → `missing_widget`
- **Widget** ≥1× `Getting Started/pdf_widget_url` → `missing_widget`
- **Widget** ≥1× `Widget Examples/url_pdf` → `missing_widget`
- **Generated note** ≥1× named ~"Media-room Build Note" whose content mentions "catalysts" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `visualization_gallery_level0`

**level0** · category: dashboard · specification: -

> Create a dashboard named Visualization Gallery and open it.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Visualization Gallery" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`

#### `visualization_gallery_level1`

**level1** · category: dashboard · specification: -

> Set up Visualization Gallery: create and open it, then add Overview and Review tabs.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Visualization Gallery" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `review` must exist (matched by tab id) → `missing_tab`

#### `visualization_gallery_level2`

**level2** · category: dashboard · specification: -

> Build Visualization Gallery from scratch: create and open it, add Overview and Review tabs, then add Getting Started's Chains TVL Highcharts.

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

> Lay out Visualization Gallery end to end: create and open it, add Overview and Review tabs, then add Getting Started's Chains TVL Highcharts, Getting Started's Vega-Lite Bar Demo.

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

> Apply the Finance Comps skill: create and open Visualization Gallery, add Valuation Multiples and Outliers tabs, and add Getting Started's Chains TVL Highcharts, Widget Examples's Vega-Lite Scatter Demo.

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

> Assemble Buildout Visualization Gallery: add it with a Visualization Review Register table, publish and instantiate Visualization Gallery App on Gallery, following the workspace's widgets.json spec, then add Getting Started's Vega-Lite Bar Demo, Widget Examples's Vega-Lite Scatter Demo.  Follow the Finance Comps skill and add a Visualization-gallery Build Note recording what it compares after normalizing metrics.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Visualization Gallery/visualization_review_register` on tab `gallery` → `missing_widget`
- **Widget** ≥1× `Getting Started/vega_bar` → `missing_widget`
- **Widget** ≥1× `Widget Examples/vega_scatter_demo` → `missing_widget`
- **Generated note** ≥1× named ~"Visualization-gallery Build Note" whose content mentions "valuation multiples" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### parameterize (24)

#### `client_intake_controls_level0`

**level0** · category: single-widget · specification: -

> On the open Client Intake Controls dashboard, set Financial Entry Form: client_first_name to Maya, client_last_name to Chen, risk_profile to Moderate, add_record to True. Preserve the other views.

- Initial workspace: dashboard "Client Intake Controls"; 1 tab(s): review; 3 seeded widget(s): form_submit_widget({"client_first_name": "Alex", "client_last_name": "Rivera", "risk_profile": "Conservative", "add_record": false}), all_forms({"client_first_name": "Taylor", "client_last_name": "Morgan", "risk_profile": "Balanced", "add_record": false}), markdown_widget_with_text_input({"name": "Pending"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/form_submit_widget` with data_args ⊇ {"client_first_name": "Maya", "client_last_name": "Chen", "risk_profile": "Moderate", "add_record": true} → `missing_widget`

#### `client_intake_controls_level1`

**level1** · category: single-widget · specification: -

> Update Financial Entry Form on the open Client Intake Controls dashboard: set it with client_first_name Maya, client_last_name Chen, risk_profile Moderate, add_record True, and preserve the other views.

- Initial workspace: dashboard "Client Intake Controls"; 1 tab(s): review; 3 seeded widget(s): form_submit_widget({"client_first_name": "Alex", "client_last_name": "Rivera", "risk_profile": "Conservative", "add_record": false}), all_forms({"client_first_name": "Taylor", "client_last_name": "Morgan", "risk_profile": "Balanced", "add_record": false}), markdown_widget_with_text_input({"name": "Pending"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/form_submit_widget` with data_args ⊇ {"client_first_name": "Maya", "client_last_name": "Chen", "risk_profile": "Moderate", "add_record": true} → `missing_widget`

#### `client_intake_controls_level2`

**level2** · category: single-widget · specification: -

> Retune Entry Form on the open Client Intake Controls dashboard to client_first_name Noah, client_last_name Patel, risk_profile Balanced, add_record True, preserving the other views.

- Initial workspace: dashboard "Client Intake Controls"; 1 tab(s): review; 3 seeded widget(s): form_submit_widget({"client_first_name": "Alex", "client_last_name": "Rivera", "risk_profile": "Conservative", "add_record": false}), all_forms({"client_first_name": "Taylor", "client_last_name": "Morgan", "risk_profile": "Balanced", "add_record": false}), markdown_widget_with_text_input({"name": "Pending"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/all_forms` with data_args ⊇ {"client_first_name": "Noah", "client_last_name": "Patel", "risk_profile": "Balanced", "add_record": true} → `missing_widget`

#### `client_intake_controls_level3`

**level3** · category: single-widget · specification: -

> Updates for the open Client Intake Controls dashboard: set Entry Form with client_first_name Noah, client_last_name Patel, risk_profile Balanced, add_record True; set Markdown Widget with Text Input with name Intake Ready; preserve the first view.

- Initial workspace: dashboard "Client Intake Controls"; 1 tab(s): review; 3 seeded widget(s): form_submit_widget({"client_first_name": "Alex", "client_last_name": "Rivera", "risk_profile": "Conservative", "add_record": false}), all_forms({"client_first_name": "Taylor", "client_last_name": "Morgan", "risk_profile": "Balanced", "add_record": false}), markdown_widget_with_text_input({"name": "Pending"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/all_forms` with data_args ⊇ {"client_first_name": "Noah", "client_last_name": "Patel", "risk_profile": "Balanced", "add_record": true} → `missing_widget`
- **Widget** ≥1× `Getting Started/markdown_widget_with_text_input` with data_args ⊇ {"name": "Intake Ready"} → `missing_widget`

#### `client_intake_controls_level4`

**level4** · category: single-widget · specification: -

> Guided by the Widget Parameters resource (openbb://workspace/specs/widget-parameters), set Financial Entry Form with client_first_name Maya, client_last_name Chen, risk_profile Moderate, add_record True on the open Client Intake Controls dashboard, and preserve the other views. The governing concepts are form, button.

- Initial workspace: dashboard "Client Intake Controls"; 1 tab(s): review; 3 seeded widget(s): form_submit_widget({"client_first_name": "Alex", "client_last_name": "Rivera", "risk_profile": "Conservative", "add_record": false}), all_forms({"client_first_name": "Taylor", "client_last_name": "Morgan", "risk_profile": "Balanced", "add_record": false}), markdown_widget_with_text_input({"name": "Pending"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/form_submit_widget` with data_args ⊇ {"client_first_name": "Maya", "client_last_name": "Chen", "risk_profile": "Moderate", "add_record": true} → `missing_widget`

#### `client_intake_controls_level5`

**level5** · category: platform · specification: -

> Tune Buildout Intake Tuning end to end: add it as a custom backend with a Intake Control Panel table carrying risk_profile and client_last_name params, publish and instantiate Intake Tuning App on Controls, then set the live Intake Control Panel to risk_profile Moderate, client_last_name Chen. Follow the widgets.json spec.  Follow the Widget Parameters resource (openbb://workspace/specs/widget-parameters) and add a Client-intake Tuning Note recording the param kind it names between endpoint and button.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Intake Tuning/intake_control_panel` with data_args ⊇ {"risk_profile": "Moderate", "client_last_name": "Chen"} on tab `controls` → `missing_widget`
- **Generated note** ≥1× named ~"Client-intake Tuning Note" whose content mentions "form" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `crypto_display_controls_level0`

**level0** · category: single-widget · specification: -

> On the open Crypto Display Controls dashboard, set Binance OHLC: symbol to ethusdt, interval to 1m, exchange to binancef. Preserve the other views.

- Initial workspace: dashboard "Crypto Display Controls"; 1 tab(s): review; 3 seeded widget(s): html_binance_ohlc({"symbol": "BTCUSDT", "interval": "30m", "exchange": "BinanceUS"}), omni_sql_widget({"prompt": "SELECT * FROM DATA LIMIT 5"}), moving_parameters_example({"datePicker1": "$currentDate-1d", "textBox1": "Hello!", "TrueFalse": true, "daysPicker1": "1"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/html_binance_ohlc` with data_args ⊇ {"symbol": "ethusdt", "interval": "1m", "exchange": "binancef"} → `missing_widget`

#### `crypto_display_controls_level1`

**level1** · category: single-widget · specification: -

> Update Binance OHLC on the open Crypto Display Controls dashboard: set it with symbol ethusdt, interval 1m, exchange binancef, and preserve the other views.

- Initial workspace: dashboard "Crypto Display Controls"; 1 tab(s): review; 3 seeded widget(s): html_binance_ohlc({"symbol": "BTCUSDT", "interval": "30m", "exchange": "BinanceUS"}), omni_sql_widget({"prompt": "SELECT * FROM DATA LIMIT 5"}), moving_parameters_example({"datePicker1": "$currentDate-1d", "textBox1": "Hello!", "TrueFalse": true, "daysPicker1": "1"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/html_binance_ohlc` with data_args ⊇ {"symbol": "ethusdt", "interval": "1m", "exchange": "binancef"} → `missing_widget`

#### `crypto_display_controls_level2`

**level2** · category: single-widget · specification: -

> Retune SQL Query Widget on the open Crypto Display Controls dashboard to prompt SELECT * FROM DATA LIMIT 3, preserving the other views.

- Initial workspace: dashboard "Crypto Display Controls"; 1 tab(s): review; 3 seeded widget(s): html_binance_ohlc({"symbol": "BTCUSDT", "interval": "30m", "exchange": "BinanceUS"}), omni_sql_widget({"prompt": "SELECT * FROM DATA LIMIT 5"}), moving_parameters_example({"datePicker1": "$currentDate-1d", "textBox1": "Hello!", "TrueFalse": true, "daysPicker1": "1"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/omni_sql_widget` with data_args ⊇ {"prompt": "SELECT * FROM DATA LIMIT 3"} → `missing_widget`

#### `crypto_display_controls_level3`

**level3** · category: single-widget · specification: -

> Updates for the open Crypto Display Controls dashboard: set SQL Query Widget with prompt SELECT * FROM DATA LIMIT 3; set Moving Parameters Example with datePicker1 $currentDate-1d, textBox1 Ready, TrueFalse True, daysPicker1 1; preserve the first view.

- Initial workspace: dashboard "Crypto Display Controls"; 1 tab(s): review; 3 seeded widget(s): html_binance_ohlc({"symbol": "BTCUSDT", "interval": "30m", "exchange": "BinanceUS"}), omni_sql_widget({"prompt": "SELECT * FROM DATA LIMIT 5"}), moving_parameters_example({"datePicker1": "$currentDate-1d", "textBox1": "Hello!", "TrueFalse": true, "daysPicker1": "1"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/omni_sql_widget` with data_args ⊇ {"prompt": "SELECT * FROM DATA LIMIT 3"} → `missing_widget`
- **Widget** ≥1× `Widget Examples/moving_parameters_example` with data_args ⊇ {"datePicker1": "$currentDate-1d", "textBox1": "Ready", "TrueFalse": true, "daysPicker1": "1"} → `missing_widget`

#### `crypto_display_controls_level4`

**level4** · category: single-widget · specification: -

> Guided by the Daloopa Inflection skill, set SQL Query Widget with prompt SELECT * FROM DATA LIMIT 3 -- growth-rate reversals on the open Crypto Display Controls dashboard, and preserve the other views. The governing concepts are growth-rate reversals.

- Initial workspace: dashboard "Crypto Display Controls"; 1 tab(s): review; 3 seeded widget(s): html_binance_ohlc({"symbol": "BTCUSDT", "interval": "30m", "exchange": "BinanceUS"}), omni_sql_widget({"prompt": "SELECT * FROM DATA LIMIT 5"}), moving_parameters_example({"datePicker1": "$currentDate-1d", "textBox1": "Hello!", "TrueFalse": true, "daysPicker1": "1"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/omni_sql_widget` with data_args ⊇ {"prompt": "SELECT * FROM DATA LIMIT 3 -- growth-rate reversals"} → `missing_widget`

#### `crypto_display_controls_level5`

**level5** · category: platform · specification: -

> Tune Buildout Display Tuning end to end: add it as a custom backend with a Display Control Panel table carrying symbol and interval params, publish and instantiate Display Tuning App on Controls, then set the live Display Control Panel to symbol ethusdt, interval 1m. Follow the widgets.json spec.  Follow the Daloopa Inflection skill and add a Crypto-display Tuning Note recording what it flags as inflections.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Display Tuning/display_control_panel` with data_args ⊇ {"symbol": "ethusdt", "interval": "1m"} on tab `controls` → `missing_widget`
- **Generated note** ≥1× named ~"Crypto-display Tuning Note" whose content mentions "growth-rate reversals" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `crypto_document_controls_level0`

**level0** · category: single-widget · specification: -

> On the open Crypto Document Controls dashboard, set Whitepapers with filenames set to ethereum.pdf and category set to l1, preserving every other view.

- Initial workspace: dashboard "Crypto Document Controls"; 1 tab(s): review; 3 seeded widget(s): whitepapers({"filenames": "bitcoin.pdf", "category": "all"}), coindesk_news({"limit": 10, "lang": "EN"}), multi_pdf_base64({"pdf_name": "Bitcoin Whitepaper"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/whitepapers` with data_args ⊇ {"filenames": "ethereum.pdf", "category": "l1"} → `missing_widget`

#### `crypto_document_controls_level1`

**level1** · category: single-widget · specification: -

> Use the whitepaper PDF on the open Crypto Document Controls dashboard to show Solana's solana.pdf from the l1 collection, leaving the rest alone.

- Initial workspace: dashboard "Crypto Document Controls"; 1 tab(s): review; 3 seeded widget(s): whitepapers({"filenames": "bitcoin.pdf", "category": "all"}), coindesk_news({"limit": 10, "lang": "EN"}), multi_pdf_base64({"pdf_name": "Bitcoin Whitepaper"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/whitepapers` with data_args ⊇ {"filenames": "solana.pdf", "category": "l1"} → `missing_widget`

#### `crypto_document_controls_level2`

**level2** · category: single-widget · specification: -

> Apply the DeFi research set to Whitepapers on the open Crypto Document Controls dashboard and preserve the surrounding document views.

- Initial workspace: dashboard "Crypto Document Controls"; 1 tab(s): review; 3 seeded widget(s): whitepapers({"filenames": "bitcoin.pdf", "category": "all"}), coindesk_news({"limit": 10, "lang": "EN"}), multi_pdf_base64({"pdf_name": "Bitcoin Whitepaper"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/whitepapers` with data_args ⊇ {"filenames": "solana.pdf", "category": "defi"} → `missing_widget`

#### `crypto_document_controls_level3`

**level3** · category: single-widget · specification: -

> Retune Whitepapers on the open Crypto Document Controls dashboard to ethereum.pdf from l1. Keep CoinDesk News and every other view unchanged.

- Initial workspace: dashboard "Crypto Document Controls"; 1 tab(s): review; 3 seeded widget(s): whitepapers({"filenames": "bitcoin.pdf", "category": "all"}), coindesk_news({"limit": 10, "lang": "EN"}), multi_pdf_base64({"pdf_name": "Bitcoin Whitepaper"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/whitepapers` with data_args ⊇ {"filenames": "ethereum.pdf", "category": "l1"} → `missing_widget`
- **Widget** ≥1× `Widget Examples/coindesk_news` → `missing_widget`

#### `crypto_document_controls_level4`

**level4** · category: single-widget · specification: -

> Using Workspace session guidance, prepare the open Crypto Document Controls dashboard with Whitepapers on ethereum.pdf from l1 and CoinDesk News limited to 6 in ES. Preserve the PDF viewer.

- Initial workspace: dashboard "Crypto Document Controls"; 1 tab(s): review; 3 seeded widget(s): whitepapers({"filenames": "bitcoin.pdf", "category": "all"}), coindesk_news({"limit": 10, "lang": "EN"}), multi_pdf_base64({"pdf_name": "Bitcoin Whitepaper"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/whitepapers` with data_args ⊇ {"filenames": "ethereum.pdf", "category": "l1"} → `missing_widget`
- **Widget** ≥1× `Widget Examples/coindesk_news` with data_args ⊇ {"limit": 6, "lang": "ES"} → `missing_widget`

#### `crypto_document_controls_level5`

**level5** · category: platform · specification: -

> Tune Rollout Document Tuning end to end: add it as a custom backend with a Document Control Panel table carrying filenames and category params, publish and instantiate Document Tuning App on Controls, then set the live Document Control Panel to filenames solana.pdf, category l1. Follow the widgets.json spec.  Follow the Finance Tearsheet skill and add a Document-controls Tuning Note recording the first input its workflow gathers.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Rollout Document Tuning/document_control_panel` with data_args ⊇ {"filenames": "solana.pdf", "category": "l1"} on tab `controls` → `missing_widget`
- **Generated note** ≥1× named ~"Document-controls Tuning Note" whose content mentions "price action" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `technology_decision_inputs_level0`

**level0** · category: single-widget · specification: -

> On the open Technology Decision Inputs dashboard, switch Car Manufacturer Performance with company set to TSLA and year set to 2023, and leave every other view unchanged.

- Initial workspace: dashboard "Technology Decision Inputs"; 1 tab(s): review; 3 seeded widget(s): company_performance({"company": "TM", "year": 2024}), earnings_estimates_monitor_calendar_upcoming_earnings({"sector": "Healthcare", "ticker": "LLY", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_performance` with data_args ⊇ {"company": "TSLA", "year": 2023} → `missing_widget`

#### `technology_decision_inputs_level1`

**level1** · category: single-widget · specification: -

> Look over the open Technology Decision Inputs dashboard, then change Car Manufacturer Performance to TSLA and 2022 while preserving everything else.

- Initial workspace: dashboard "Technology Decision Inputs"; 1 tab(s): review; 3 seeded widget(s): company_performance({"company": "TM", "year": 2024}), earnings_estimates_monitor_calendar_upcoming_earnings({"sector": "Healthcare", "ticker": "LLY", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_performance` with data_args ⊇ {"company": "TSLA", "year": 2022} → `missing_widget`

#### `technology_decision_inputs_level2`

**level2** · category: single-widget · specification: -

> Apply the current Tesla model-year policy on the open Technology Decision Inputs dashboard. Set Car Manufacturer Performance to company TSLA and year 2024, the current model year, and preserve the rest of the dashboard.

- Initial workspace: dashboard "Technology Decision Inputs"; 1 tab(s): review; 3 seeded widget(s): company_performance({"company": "TM", "year": 2024}), earnings_estimates_monitor_calendar_upcoming_earnings({"sector": "Healthcare", "ticker": "LLY", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_performance` with data_args ⊇ {"company": "TSLA", "year": 2024} → `missing_widget`

#### `technology_decision_inputs_level3`

**level3** · category: single-widget · specification: -

> Retune Upcoming Earnings on the open Technology Decision Inputs dashboard to Technology, AAPL, and QTD. Keep Car Manufacturer Performance and every other view as they are.

- Initial workspace: dashboard "Technology Decision Inputs"; 1 tab(s): review; 3 seeded widget(s): company_performance({"company": "TM", "year": 2024}), earnings_estimates_monitor_calendar_upcoming_earnings({"sector": "Healthcare", "ticker": "LLY", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_calendar_upcoming_earnings` with data_args ⊇ {"sector": "Technology", "ticker": "AAPL", "period": "QTD"} → `missing_widget`
- **Widget** ≥1× `Getting Started/company_performance` → `missing_widget`

#### `technology_decision_inputs_level4`

**level4** · category: single-widget · specification: -

> Prepare the open Technology Decision Inputs dashboard for the quarterly review under Finance Earnings Prep governance. Set Upcoming Earnings to Technology, AAPL, and QTD, and Trade Ideas to Flagship Long/Short and QTD. Preserve Car Manufacturer Performance.

- Initial workspace: dashboard "Technology Decision Inputs"; 1 tab(s): review; 3 seeded widget(s): company_performance({"company": "TM", "year": 2024}), earnings_estimates_monitor_calendar_upcoming_earnings({"sector": "Healthcare", "ticker": "LLY", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_calendar_upcoming_earnings` with data_args ⊇ {"sector": "Technology", "ticker": "AAPL", "period": "QTD"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "QTD"} → `missing_widget`

#### `technology_decision_inputs_level5`

**level5** · category: platform · specification: -

> Tune Pilot Decision Tuning end to end: add it as a custom backend with a Decision Input Panel table carrying company and period params, publish and instantiate Decision Tuning App on Controls, then set the live Decision Input Panel to company TSLA, period QTD. Follow the widgets.json spec.  Follow the Finance Earnings Prep skill and add a Decision-inputs Tuning Note recording what it compares to street numbers first.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Pilot Decision Tuning/decision_input_panel` with data_args ⊇ {"company": "TSLA", "period": "QTD"} on tab `controls` → `missing_widget`
- **Generated note** ≥1× named ~"Decision-inputs Tuning Note" whose content mentions "internal estimates" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### platform (24)

#### `cited_research_operations_level0`

**level0** · category: platform · specification: -

> From the open Cited Research Operations dashboard, read the Daloopa Tearsheet skill. Add a Daloopa Tearsheet Workflow note that records the workflow title and its period-math anchor.

- Initial workspace: dashboard "Cited Research Operations"; 1 tab(s): research
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Daloopa Tearsheet Workflow" whose content mentions "Daloopa tearsheet workflow", "latest_calendar_quarter" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `cited_research_operations_level1`

**level1** · category: platform · specification: -

> On the open Cited Research Operations dashboard, follow Daloopa Tearsheet governance and add Bench Daloopa's Company Directory.

- Initial workspace: dashboard "Cited Research Operations"; 1 tab(s): research
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Daloopa/daloopa_company_directory` → `missing_widget`

#### `cited_research_operations_level2`

**level2** · category: platform · specification: -

> Use Daloopa Guidance Tracker governance on the open Cited Research Operations dashboard and add Bench Daloopa's Management Guidance for NVDA.

- Initial workspace: dashboard "Cited Research Operations"; 1 tab(s): research
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Daloopa/daloopa_management_guidance` with data_args ⊇ {"ticker": "NVDA"} → `missing_widget`

#### `cited_research_operations_level3`

**level3** · category: dashboard · specification: -

> For the open Cited Research Operations dashboard, use Daloopa Industry governance to place two Bench Daloopa Company Fundamentals views, one for MSFT in 2025Q4 and one for NVDA in 2025Q4.

- Initial workspace: dashboard "Cited Research Operations"; 1 tab(s): research
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "MSFT", "period": "2025Q4"} → `missing_widget`
- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "NVDA", "period": "2025Q4"} → `missing_widget`

#### `cited_research_operations_level4`

**level4** · category: dashboard · specification: -

> Combine Daloopa Capital Allocation governance with Workspace session guidance on the open Cited Research Operations dashboard. Add Bench Daloopa's Company Fundamentals for AMZN in 2026Q1 and a Citation Protocol note naming source_url and calendar_period.

- Initial workspace: dashboard "Cited Research Operations"; 1 tab(s): research
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Daloopa/daloopa_company_fundamentals` with data_args ⊇ {"ticker": "AMZN", "period": "2026Q1"} → `missing_widget`
- **Generated note** ≥1× named ~"Citation Protocol" whose content mentions "source_url", "calendar_period" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `cited_research_operations_level5`

**level5** · category: platform · specification: -

> Following Daloopa Tearsheet governance, author and add a Cited Research Backend with a Citation Review Queue, then publish and instantiate a Cited Research App with a Research tab.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Cited Research Backend/citation_review_queue` on tab `research` → `missing_widget`

#### `comps_governance_level0`

**level0** · category: platform · specification: -

> Read the Finance Comps skill and add a Comps-governance Starter Note containing valuation multiples.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Comps-governance Starter Note" whose content mentions "valuation multiples" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `comps_governance_level1`

**level1** · category: platform · specification: -

> Start from the Finance Comps skill: add a Comps-governance Discovery Note containing valuation multiples.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Comps-governance Discovery Note" whose content mentions "valuation multiples" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `comps_governance_level2`

**level2** · category: platform · specification: -

> Put the Finance Comps skill to work: add Getting Started's Plotly Chart with Theme and Toolbar using Config File for valuation multiples.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/plotly_chart_with_theme_and_toolbar_using_config_file` → `missing_widget`

#### `comps_governance_level3`

**level3** · category: platform · specification: -

> Working from the Finance Comps skill, add Getting Started's Plotly Chart with Theme and Toolbar using Config File, Widget Examples's Chains chart example Plotly with raw data to support valuation multiples.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/plotly_chart_with_theme_and_toolbar_using_config_file` → `missing_widget`
- **Widget** ≥1× `Widget Examples/chains_plotly` → `missing_widget`

#### `comps_governance_level4`

**level4** · category: platform · specification: -

> Using the Finance Comps skill, add Getting Started's Plotly Chart with Theme and Toolbar using Config File, Widget Examples's Chains chart example Plotly with raw data, and add a Comps-governance Governed Note containing valuation multiples.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/plotly_chart_with_theme_and_toolbar_using_config_file` → `missing_widget`
- **Widget** ≥1× `Widget Examples/chains_plotly` → `missing_widget`
- **Generated note** ≥1× named ~"Comps-governance Governed Note" whose content mentions "valuation multiples" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `comps_governance_level5`

**level5** · category: platform · specification: -

> Deliver Buildout Comps Governance: read the Finance Comps skill, add the backend with a Comps Governance Register table per the workspace's widgets.json spec, publish and instantiate Comps Governance App on Comparables, and add a Comps-governance Build Note containing valuation multiples.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Comps Governance/comps_governance_register` on tab `comparables` → `missing_widget`
- **Generated note** ≥1× named ~"Comps-governance Build Note" whose content mentions "valuation multiples" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `governed_earnings_brief_level0`

**level0** · category: platform · specification: -

> Read the Finance Earnings Prep skill for the open Governed Earnings Brief dashboard. Add an Earnings Prep Workflow note that records the workflow title and its first and fourth actions.

- Initial workspace: dashboard "Governed Earnings Brief"; 1 tab(s): overview
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Earnings Prep Workflow" whose content mentions "Earnings prep workflow", "internal estimates", "transcript tone" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `governed_earnings_brief_level1`

**level1** · category: platform · specification: -

> On the open Governed Earnings Brief dashboard, consult Finance Earnings Prep governance and add an Earnings Governance Actions note that names internal estimates and transcript tone.

- Initial workspace: dashboard "Governed Earnings Brief"; 1 tab(s): overview
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Earnings Governance Actions" whose content mentions "internal estimates", "transcript tone" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `governed_earnings_brief_level2`

**level2** · category: platform · specification: -

> Review the backend contract resource (openbb://workspace/contract/backend) for the open Governed Earnings Brief dashboard, then add a Backend Contract Actions note recording the two contract items listed between the manifest files and authentication.

- Initial workspace: dashboard "Governed Earnings Brief"; 1 tab(s): overview
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Backend Contract Actions" whose content mentions "endpoints", "CORS" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `governed_earnings_brief_level3`

**level3** · category: dashboard · specification: -

> Use Workspace session guidance on the open Governed Earnings Brief dashboard. Add an Actions tab and place a Session Grounding note there naming current-dashboard and current-tab.

- Initial workspace: dashboard "Governed Earnings Brief"; 1 tab(s): overview
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Session Grounding" whose content mentions "current-dashboard", "current-tab" on tab `actions` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `governed_earnings_brief_level4`

**level4** · category: dashboard · specification: -

> For the open Governed Earnings Brief dashboard, combine Finance Earnings Prep governance with Workspace session guidance. Add an Actions tab and an Earnings Session Actions note there naming action items and current-dashboard.

- Initial workspace: dashboard "Governed Earnings Brief"; 1 tab(s): overview
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Earnings Session Actions" whose content mentions "action items", "current-dashboard" on tab `actions` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `governed_earnings_brief_level5`

**level5** · category: platform · specification: -

> The desk wants a Governed Earnings Backend with an Earnings Action Register. Following the build-an-app guide, author and add it, publish a Governed Earnings App with an Actions tab, and instantiate it.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Governed Earnings Backend/earnings_action_register` on tab `actions` → `missing_widget`

#### `investment_snapshot_governance_level0`

**level0** · category: platform · specification: -

> Read the Finance Tearsheet skill and add a Investment-snapshot Starter Note containing price action.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Investment-snapshot Starter Note" whose content mentions "price action" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `investment_snapshot_governance_level1`

**level1** · category: platform · specification: -

> Start from the Finance Tearsheet skill: add a Investment-snapshot Discovery Note containing price action.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Investment-snapshot Discovery Note" whose content mentions "price action" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `investment_snapshot_governance_level2`

**level2** · category: platform · specification: -

> Put the Finance Tearsheet skill to work: add Getting Started's TradingView Chart for price action.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/udf` → `missing_widget`

#### `investment_snapshot_governance_level3`

**level3** · category: platform · specification: -

> Working from the Finance Tearsheet skill, add Getting Started's TradingView Chart, Getting Started's HTML Widget to support price action.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/udf` → `missing_widget`
- **Widget** ≥1× `Getting Started/html_widget` → `missing_widget`

#### `investment_snapshot_governance_level4`

**level4** · category: platform · specification: -

> Using the Finance Tearsheet skill, add Getting Started's TradingView Chart, Getting Started's HTML Widget, and add a Investment-snapshot Governed Note containing price action.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/udf` → `missing_widget`
- **Widget** ≥1× `Getting Started/html_widget` → `missing_widget`
- **Generated note** ≥1× named ~"Investment-snapshot Governed Note" whose content mentions "price action" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `investment_snapshot_governance_level5`

**level5** · category: platform · specification: -

> Deliver Buildout Investment Snapshot: read the Finance Tearsheet skill, add the backend with a Investment Snapshot Register table per the workspace's widgets.json spec, publish and instantiate Investment Snapshot App on Snapshot, and add a Investment-snapshot Build Note containing price action.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Investment Snapshot/investment_snapshot_register` on tab `snapshot` → `missing_widget`
- **Generated note** ≥1× named ~"Investment-snapshot Build Note" whose content mentions "price action" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### repair (24)

#### `manufacturer_details_repair_level0`

**level0** · category: repair · specification: -

> Car Manufacturer Details on the open Manufacturer Detail Repair dashboard has company set to F and year set to 2022. Set company to F and year back to 2024.

- Initial workspace: dashboard "Manufacturer Detail Repair"; 1 tab(s): details; 2 seeded widget(s): company_details({"company": "F", "year": 2022}), markdown_widget({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_details` with data_args ⊇ {"company": "F", "year": 2024} → `missing_widget`

#### `manufacturer_details_repair_level1`

**level1** · category: repair · specification: -

> On the open Manufacturer Detail Repair dashboard, restore Car Manufacturer Details to company F and year 2024. Preserve Markdown Widget and every other workspace item.

- Initial workspace: dashboard "Manufacturer Detail Repair"; 1 tab(s): details; 2 seeded widget(s): company_details({"company": "F", "year": 2022}), markdown_widget({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_details` with data_args ⊇ {"company": "F", "year": 2024} → `missing_widget`
- **Widget** ≥1× `Getting Started/markdown_widget` → `missing_widget`

#### `manufacturer_details_repair_level2`

**level2** · category: repair · specification: -

> The open Manufacturer Detail Repair dashboard has two copies of Car Manufacturer Details. Remove the one flagged as the duplicate so exactly one remains, and preserve Markdown Widget.

- Initial workspace: dashboard "Manufacturer Detail Repair"; 1 tab(s): details; 3 seeded widget(s): company_details({"company": "F", "year": 2024}), company_details({"company": "F", "year": 2024}), markdown_widget({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_details` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/markdown_widget` → `missing_widget`

#### `manufacturer_details_repair_level3`

**level3** · category: repair · specification: -

> Car Manufacturer Details overlaps Markdown Widget on the open Manufacturer Detail Repair dashboard. Move Car Manufacturer Details to x 0, y 10, width 40, height 14 on Details while preserving its parameters.

- Initial workspace: dashboard "Manufacturer Detail Repair"; 1 tab(s): details; 2 seeded widget(s): company_details({"company": "F", "year": 2024}), markdown_widget({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_details` → `missing_widget`
- **Widget** ≥1× `Getting Started/markdown_widget` → `missing_widget`

#### `manufacturer_details_repair_level4`

**level4** · category: repair · specification: -

> Clean up the open Manufacturer Detail Repair dashboard. Restore the primary Car Manufacturer Details to F and 2024, and remove the extra copy flagged as the duplicate. Move the primary to x 0, y 10, width 40, height 14 on Details, and preserve Markdown Widget.

- Initial workspace: dashboard "Manufacturer Detail Repair"; 1 tab(s): details; 3 seeded widget(s): company_details({"company": "F", "year": 2022}), company_details({"company": "F", "year": 2022}), markdown_widget({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Getting Started/company_details` with data_args ⊇ {"company": "F", "year": 2024} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Getting Started/markdown_widget` → `missing_widget`

#### `manufacturer_details_repair_level5`

**level5** · category: repair · specification: -

> Rollout Detail Repair was lost from the workspace; on the open Custom Detail Repair dashboard, rebuild it from scratch: add a custom backend Rollout Detail Repair with a Manufacturer Detail Queue table, publish Detail Repair App, and instantiate it with one non-overlapping Manufacturer Detail Queue placement on Details, keeping all other workspace content. Follow the widgets.json spec. Follow the Daloopa Industry skill and add a Detail-queue Rebuild Note recording who it lists from the company directory.

- Initial workspace: dashboard "Custom Detail Repair"; 1 tab(s): details
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Rollout Detail Repair/manufacturer_detail_queue` on tab `details` → `missing_widget`
- **Generated note** ≥1× named ~"Detail-queue Rebuild Note" whose content mentions "peers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `nav_exception_station_level0`

**level0** · category: repair · specification: -

> NAV Exceptions on the open NAV Repair Staging dashboard has fund set to Flagship Long/Short, status set to Open, and period set to QTD. Set fund to Flagship Long/Short, status to Open, and period back to YTD.

- Initial workspace: dashboard "NAV Repair Staging"; 1 tab(s): exceptions; 2 seeded widget(s): fund_operations_control_tower_pricing_nav_exceptions({"fund": "Flagship Long/Short", "status": "Open", "period": "QTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_pricing_nav_exceptions` with data_args ⊇ {"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"} → `missing_widget`

#### `nav_exception_station_level1`

**level1** · category: repair · specification: -

> On the open NAV Repair Staging dashboard, fix the NAV Exceptions parameters by restoring Flagship Long/Short, Open, and YTD. Preserve Trade Ideas and every other workspace item.

- Initial workspace: dashboard "NAV Repair Staging"; 1 tab(s): exceptions; 2 seeded widget(s): fund_operations_control_tower_pricing_nav_exceptions({"fund": "Flagship Long/Short", "status": "Closed", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_pricing_nav_exceptions` with data_args ⊇ {"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` → `missing_widget`

#### `nav_exception_station_level2`

**level2** · category: repair · specification: -

> The open NAV Repair Staging dashboard has two copies of NAV Exceptions. Remove the one flagged as the duplicate so exactly one remains, and preserve Trade Ideas and all other content.

- Initial workspace: dashboard "NAV Repair Staging"; 1 tab(s): exceptions; 3 seeded widget(s): fund_operations_control_tower_pricing_nav_exceptions({"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"}), fund_operations_control_tower_pricing_nav_exceptions({"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_pricing_nav_exceptions` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` → `missing_widget`

#### `nav_exception_station_level3`

**level3** · category: repair · specification: -

> Fix the overlap on the open NAV Repair Staging dashboard without disturbing Trade Ideas. Move NAV Exceptions to x 0, y 14, width 40, and height 14 on Exceptions, preserving all parameters and remaining workspace content.

- Initial workspace: dashboard "NAV Repair Staging"; 1 tab(s): exceptions; 2 seeded widget(s): fund_operations_control_tower_pricing_nav_exceptions({"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_pricing_nav_exceptions` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` → `missing_widget`

#### `nav_exception_station_level4`

**level4** · category: repair · specification: -

> Clean up the open NAV Repair Staging dashboard. Restore the primary NAV Exceptions view to Flagship Long/Short, Open, and YTD; remove the extra copy flagged as the duplicate. Move the primary to x 0, y 14, width 40, height 14 on Exceptions, and preserve Trade Ideas.

- Initial workspace: dashboard "NAV Repair Staging"; 1 tab(s): exceptions; 3 seeded widget(s): fund_operations_control_tower_pricing_nav_exceptions({"fund": "Flagship Long/Short", "status": "Closed", "period": "YTD"}), fund_operations_control_tower_pricing_nav_exceptions({"fund": "Flagship Long/Short", "status": "Closed", "period": "YTD"}), portfolio_command_center_actions_trade_ideas({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/fund_operations_control_tower_pricing_nav_exceptions` with data_args ⊇ {"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_trade_ideas` → `missing_widget`

#### `nav_exception_station_level5`

**level5** · category: repair · specification: -

> Pilot NAV Repair was lost from the workspace; on the open Custom NAV Repair Staging dashboard, rebuild it from scratch: add a custom backend Pilot NAV Repair with a NAV Exception Queue table, publish NAV Repair App, and instantiate it with one non-overlapping NAV Exception Queue placement on Exceptions, keeping all other workspace content. Follow the widgets.json spec. Follow the Daloopa Guidance Tracker skill and add a NAV-exception Rebuild Note recording the last of the three verdict kinds it tallies.

- Initial workspace: dashboard "Custom NAV Repair Staging"; 1 tab(s): exceptions
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Pilot NAV Repair/nav_exception_queue` on tab `exceptions` → `missing_widget`
- **Generated note** ≥1× named ~"NAV-exception Rebuild Note" whose content mentions "Missed" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `protocol_display_repair_level0`

**level0** · category: repair · specification: -

> Fix Defi Llama Protocol Details on the open Protocol Display Repair dashboard: set protocol_id to uniswap.

- Initial workspace: dashboard "Protocol Display Repair"; 1 tab(s): review; 2 seeded widget(s): defi_llama_protocol_details({"protocol_id": "aave"}), demo_data_ssrm({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/defi_llama_protocol_details` with data_args ⊇ {"protocol_id": "uniswap"} → `missing_widget`

#### `protocol_display_repair_level1`

**level1** · category: repair · specification: -

> Restore Defi Llama Protocol Details on the open Protocol Display Repair dashboard with protocol_id uniswap, and preserve Demo Financial Data (SSRM).

- Initial workspace: dashboard "Protocol Display Repair"; 1 tab(s): review; 2 seeded widget(s): defi_llama_protocol_details({"protocol_id": "aave"}), demo_data_ssrm({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/defi_llama_protocol_details` with data_args ⊇ {"protocol_id": "uniswap"} → `missing_widget`
- **Widget** ≥1× `Widget Examples/demo_data_ssrm` → `missing_widget`

#### `protocol_display_repair_level2`

**level2** · category: repair · specification: -

> The open Protocol Display Repair dashboard has two copies of Defi Llama Protocol Details. Remove the one flagged as the duplicate, and preserve Demo Financial Data (SSRM).

- Initial workspace: dashboard "Protocol Display Repair"; 1 tab(s): review; 3 seeded widget(s): defi_llama_protocol_details({"protocol_id": "uniswap"}), demo_data_ssrm({}), defi_llama_protocol_details({"protocol_id": "uniswap"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/defi_llama_protocol_details` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Widget Examples/demo_data_ssrm` → `missing_widget`

#### `protocol_display_repair_level3`

**level3** · category: repair · specification: -

> Demo Financial Data (SSRM) is overlapping on the open Protocol Display Repair dashboard: move it to x 0, y 12, width 40, height 12 on Review, and preserve Defi Llama Protocol Details.

- Initial workspace: dashboard "Protocol Display Repair"; 1 tab(s): review; 2 seeded widget(s): defi_llama_protocol_details({"protocol_id": "uniswap"}), demo_data_ssrm({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/defi_llama_protocol_details` → `missing_widget`
- **Widget** ≥1× `Widget Examples/demo_data_ssrm` → `missing_widget`

#### `protocol_display_repair_level4`

**level4** · category: repair · specification: -

> Repair the open Protocol Display Repair dashboard under the Daloopa Inflection skill: restore Defi Llama Protocol Details with protocol_id uniswap, preserve Demo Financial Data (SSRM), and add a Protocol-display Governance Note naming growth-rate reversals.

- Initial workspace: dashboard "Protocol Display Repair"; 1 tab(s): review; 2 seeded widget(s): defi_llama_protocol_details({"protocol_id": "aave"}), demo_data_ssrm({})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Widget Examples/defi_llama_protocol_details` with data_args ⊇ {"protocol_id": "uniswap"} → `missing_widget`
- **Widget** ≥1× `Widget Examples/demo_data_ssrm` → `missing_widget`
- **Generated note** ≥1× named ~"Protocol-display Governance Note" whose content mentions "growth-rate reversals" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `protocol_display_repair_level5`

**level5** · category: repair · specification: -

> Buildout Protocol Repair was lost from the workspace; on the open Protocol-display Backend Repair dashboard, rebuild it from scratch: add a custom backend Buildout Protocol Repair with a Protocol Repair Queue table, publish Protocol Repair App, and instantiate it with one non-overlapping Protocol Repair Queue placement on Protocols, keeping all other workspace content. Follow the widgets.json spec. Follow the Daloopa Inflection skill and add a Protocol-display Rebuild Note recording what it flags as inflections.

- Initial workspace: dashboard "Protocol-display Backend Repair"; 1 tab(s): protocols
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Protocol Repair/protocol_repair_queue` on tab `protocols` → `missing_widget`
- **Generated note** ≥1× named ~"Protocol-display Rebuild Note" whose content mentions "growth-rate reversals" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_freshness_repair_level0`

**level0** · category: repair · specification: -

> Fix SLA Metrics on the open Vendor Freshness Repair dashboard: set vendor to Bloomberg, status to Open, period to QTD.

- Initial workspace: dashboard "Vendor Freshness Repair"; 1 tab(s): review; 2 seeded widget(s): vendor_dataset_monitor_vendors_sla_metrics({"vendor": "FactSet", "status": "Closed", "period": "1Y"}), vendor_dataset_monitor_vendors_vendor_contract_terms({"vendor": "FactSet", "status": "Open", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_sla_metrics` with data_args ⊇ {"vendor": "Bloomberg", "status": "Open", "period": "QTD"} → `missing_widget`

#### `vendor_freshness_repair_level1`

**level1** · category: repair · specification: -

> Restore SLA Metrics on the open Vendor Freshness Repair dashboard with vendor Bloomberg, status Open, period QTD, and preserve Vendor Contract Terms.

- Initial workspace: dashboard "Vendor Freshness Repair"; 1 tab(s): review; 2 seeded widget(s): vendor_dataset_monitor_vendors_sla_metrics({"vendor": "FactSet", "status": "Closed", "period": "1Y"}), vendor_dataset_monitor_vendors_vendor_contract_terms({"vendor": "FactSet", "status": "Open", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_sla_metrics` with data_args ⊇ {"vendor": "Bloomberg", "status": "Open", "period": "QTD"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_vendor_contract_terms` → `missing_widget`

#### `vendor_freshness_repair_level2`

**level2** · category: repair · specification: -

> The open Vendor Freshness Repair dashboard has two copies of SLA Metrics. Remove the one flagged as the duplicate, and preserve Vendor Contract Terms.

- Initial workspace: dashboard "Vendor Freshness Repair"; 1 tab(s): review; 3 seeded widget(s): vendor_dataset_monitor_vendors_sla_metrics({"vendor": "Bloomberg", "status": "Open", "period": "QTD"}), vendor_dataset_monitor_vendors_vendor_contract_terms({"vendor": "FactSet", "status": "Open", "period": "YTD"}), vendor_dataset_monitor_vendors_sla_metrics({"vendor": "Bloomberg", "status": "Open", "period": "QTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_sla_metrics` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_vendor_contract_terms` → `missing_widget`

#### `vendor_freshness_repair_level3`

**level3** · category: repair · specification: -

> Vendor Contract Terms is overlapping on the open Vendor Freshness Repair dashboard: move it to x 0, y 12, width 40, height 12 on Review, and preserve SLA Metrics.

- Initial workspace: dashboard "Vendor Freshness Repair"; 1 tab(s): review; 2 seeded widget(s): vendor_dataset_monitor_vendors_sla_metrics({"vendor": "Bloomberg", "status": "Open", "period": "QTD"}), vendor_dataset_monitor_vendors_vendor_contract_terms({"vendor": "FactSet", "status": "Open", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_sla_metrics` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_vendor_contract_terms` → `missing_widget`

#### `vendor_freshness_repair_level4`

**level4** · category: repair · specification: -

> Repair the open Vendor Freshness Repair dashboard under the Finance Guidance Tracker skill: restore SLA Metrics with vendor Bloomberg, status Open, period QTD, preserve Vendor Contract Terms, and add a Vendor-freshness Governance Note naming evidence gaps.

- Initial workspace: dashboard "Vendor Freshness Repair"; 1 tab(s): review; 2 seeded widget(s): vendor_dataset_monitor_vendors_sla_metrics({"vendor": "FactSet", "status": "Closed", "period": "1Y"}), vendor_dataset_monitor_vendors_vendor_contract_terms({"vendor": "FactSet", "status": "Open", "period": "YTD"})
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_sla_metrics` with data_args ⊇ {"vendor": "Bloomberg", "status": "Open", "period": "QTD"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_vendor_contract_terms` → `missing_widget`
- **Generated note** ≥1× named ~"Vendor-freshness Governance Note" whose content mentions "evidence gaps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_freshness_repair_level5`

**level5** · category: repair · specification: -

> Buildout Vendor Repair was lost from the workspace; on the open Vendor-freshness Backend Repair dashboard, rebuild it from scratch: add a custom backend Buildout Vendor Repair with a Vendor Repair Queue table, publish Vendor Repair App, and instantiate it with one non-overlapping Vendor Repair Queue placement on Incidents, keeping all other workspace content. Follow the widgets.json spec. Follow the Finance Guidance Tracker skill and add a Vendor-freshness Rebuild Note recording the final thing its workflow lists.

- Initial workspace: dashboard "Vendor-freshness Backend Repair"; 1 tab(s): incidents
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Vendor Repair/vendor_repair_queue` on tab `incidents` → `missing_widget`
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

> On the open Closing Tape Review dashboard, read the daily OHLCV rows in Bench Daloopa's configured Stock Prices view without changing it and report the latest date, exact close, and volume.

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

> Build and add a Rollout Closing Tape backend with a Closing Tape Lookup table for NVDA, instantiate its Closing Tape App, read the result, and report the latest date and exact close. Follow the widgets.json spec. Follow the Daloopa Tearsheet skill and add a Closing Tape Build Note recording the anchor it uses for all period math.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Rollout Closing Tape/closing_tape_lookup` with data_args ⊇ {"ticker": "NVDA"} on tab `tape` → `missing_widget`
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

> On the open Earnings & Estimates Monitor dashboard, read Bench Stark Enterprise's configured Upcoming Earnings view without changing it, and report LLY's exact YTD score and change.

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

> The desk needs a Pilot Earnings Lookup backend with an Earnings Status Lookup table for LLY and YTD. Build and add it, instantiate its Earnings Lookup App, read the lookup, and report the exact score and status. Follow the widgets.json spec. Follow the Finance Earnings Prep skill and add a Earnings Lookup Build Note recording what it identifies right after the estimate comparison.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Pilot Earnings Lookup/earnings_status_lookup` with data_args ⊇ {"ticker": "LLY", "period": "YTD"} on tab `lookup` → `missing_widget`
- **Generated note** ≥1× named ~"Earnings Lookup Build Note" whose content mentions "surprise drivers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `live_quote_lookup_level0`

**level0** · category: read · specification: -

> Read Widget Examples's Live Grid with symbol AAPL, then report the exact symbol and price shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `live_quote_lookup_level1`

**level1** · category: read · specification: -

> Quick ask - read Widget Examples's Live Grid with symbol AAPL, then report the exact symbol and price shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `live_quote_lookup_level2`

**level2** · category: read · specification: -

> For the desk, read Widget Examples's Live Grid with symbol AAPL, then report the exact symbol and price shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `live_quote_lookup_level3`

**level3** · category: read · specification: -

> Before the meeting, read Widget Examples's Live Grid with symbol AAPL, then report the exact symbol and price shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `live_quote_lookup_level4`

**level4** · category: read · specification: -

> Following the Finance Tearsheet skill, read Widget Examples's Live Grid with symbol AAPL, report the exact symbol and price shown, and add a Live-quote Governance Note that records price action.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Live-quote Governance Note" whose content mentions "price action" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `live_quote_lookup_level5`

**level5** · category: platform · specification: -

> Stand up Buildout Live Quote: add it with a Live Quote Lookup table carrying symbol and last_price columns; publish and instantiate Live Quote App on Quotes, read it with symbol AAPL, and report the exact symbol and last_price values shown. Build it to the workspace's widgets.json spec. Follow the Finance Tearsheet skill and add a Live-quote Build Note recording the first input its workflow gathers.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Live Quote/live_quote_lookup` with data_args ⊇ {"symbol": "AAPL"} on tab `quotes` → `missing_widget`
- **Generated note** ≥1× named ~"Live-quote Build Note" whose content mentions "price action" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `operating_driver_lookup_level0`

**level0** · category: read · specification: -

> Read Bench Daloopa's Operating KPIs with ticker AAPL, period 2026Q1, then report the exact calendar_period and Installed Base Active Devices value shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `operating_driver_lookup_level1`

**level1** · category: read · specification: -

> Quick ask - read Bench Daloopa's Operating KPIs with ticker AAPL, period 2026Q1, then report the exact calendar_period and Installed Base Active Devices value shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `operating_driver_lookup_level2`

**level2** · category: read · specification: -

> For the desk, read Bench Daloopa's Operating KPIs with ticker AAPL, period 2026Q1, then report the exact calendar_period and Installed Base Active Devices value shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `operating_driver_lookup_level3`

**level3** · category: read · specification: -

> Before the meeting, read Bench Daloopa's Operating KPIs with ticker AAPL, period 2026Q1, then report the exact calendar_period and Installed Base Active Devices value shown.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `operating_driver_lookup_level4`

**level4** · category: read · specification: -

> Following the Daloopa Inflection skill, read Bench Daloopa's Operating KPIs with ticker AAPL, period 2026Q1, report the exact calendar_period and Installed Base Active Devices value shown, and add a Operating-driver Governance Note that records growth-rate reversals.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Operating-driver Governance Note" whose content mentions "growth-rate reversals" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `operating_driver_lookup_level5`

**level5** · category: platform · specification: -

> Stand up Buildout Operating Drivers: add it with a Operating Driver Lookup table carrying fiscal_period and driver_value columns; publish and instantiate Operating Driver App on Drivers, read it with ticker AAPL, period 2026Q1, and report the exact fiscal_period and driver_value values shown. Build it to the workspace's widgets.json spec. Follow the Daloopa Inflection skill and add a Operating-driver Build Note recording what it flags as inflections.

- Initial workspace: baseline `stark-workspace-a`; backends `stark-enterprise-x`, `support-daloopa-skills`, `getting-started`, `widget-examples`; active dashboard "Home"
- Allowed tools (21): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`, `final_answer`
- Turn budget: None · oracle reference trace: 0 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Buildout Operating Drivers/operating_driver_lookup` with data_args ⊇ {"ticker": "AAPL", "period": "2026Q1"} on tab `drivers` → `missing_widget`
- **Generated note** ≥1× named ~"Operating-driver Build Note" whose content mentions "growth-rate reversals" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`


---

Total: 410 tasks.