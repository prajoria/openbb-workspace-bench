# WorkspaceBench Task Catalog

Auto-generated from the bundled task JSON files — regenerate with
`python scripts/generators/generate_task_catalog.py` after editing tasks.
The four deterministic simulator suites are included. The 12 experimental
`build-openbb-backends` code tasks are excluded; their
filesystem/process criteria are documented in the README task schema and generated
by `scripts/generators/generate_backend_code_suite.py`.

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

## Suite: smoke (20 tasks)

### add_generative_widget (1)

#### `smoke_add_generative_widget`

**easy** · category: single-widget · specification: explicit

> Add a minimal generated note to Home.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (1): `add_generative_widget`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Smoke Note" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### assign_tasks_to_agents (1)

#### `smoke_assign_tasks_to_agents`

**easy** · category: platform · specification: explicit

> Round-trip one bounded task request through the agent envelope.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (1): `assign_tasks_to_agents`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `assign_tasks_to_agents` with args ⊇ {"task_requests": [{"id": "smoke-envelope", "task": "Return the Workspace smoke envelope."}]} must appear in the trace → `missing_tool_call`

### create_widget (1)

#### `smoke_create_widget`

**easy** · category: single-widget · specification: explicit

> Create the Stark Alert Trend widget on Home.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (1): `create_widget`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_alert_trend` with data_args ⊇ {"severity": "High", "status": "Open", "period": "YTD"} → `missing_widget`

### delete_widget (1)

#### `smoke_delete_widget`

**easy** · category: single-widget · specification: explicit

> Delete the seeded Stark Alert Trend widget.

- Initial workspace: dashboard "Smoke delete_widget"; 1 tab(s): overview; 1 seeded widget(s): compliance_surveillance_hub_alerts_alert_trend({"severity": "High", "status": "Open", "period": "YTD"})
- Allowed tools (1): `delete_widget`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥0× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_alert_trend` → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

### get_params_options (1)

#### `smoke_get_params_options`

**easy** · category: read · specification: explicit

> Read valid period options for the Stark Alert Trend widget.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (1): `get_params_options`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `get_params_options` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "compliance_surveillance_hub_alerts_alert_trend", "param_name": "period"} must appear in the trace → `missing_tool_call`

### get_skill_content (1)

#### `smoke_get_skill_content`

**easy** · category: read · specification: explicit

> Read the Finance Tearsheet skill content once.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (1): `get_skill_content`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-tearsheet"} must appear in the trace → `missing_tool_call`

### get_widget_data (1)

#### `smoke_get_widget_data`

**easy** · category: read · specification: explicit

> Fetch open high-severity YTD data from the Stark Alert Trend widget.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (1): `get_widget_data`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "compliance_surveillance_hub_alerts_alert_trend", "data_args": {"severity": "High", "status": "Open", "period": "YTD"}} must appear in the trace → `missing_tool_call`

### get_widget_schema (1)

#### `smoke_get_widget_schema`

**easy** · category: read · specification: explicit

> Read the schema for the Stark Alert Trend widget.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (1): `get_widget_schema`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `get_widget_schema` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "compliance_surveillance_hub_alerts_alert_trend"} must appear in the trace → `missing_tool_call`

### get_workspace_prompt (1)

#### `smoke_get_workspace_prompt`

**easy** · category: read · specification: explicit

> Read the Workspace tool-usage prompt once.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (1): `get_workspace_prompt`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_tool_usage"} must appear in the trace → `missing_tool_call`

### get_workspace_snapshot (1)

#### `smoke_get_workspace_snapshot`

**easy** · category: read · specification: explicit

> Read the current Workspace snapshot once.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (1): `get_workspace_snapshot`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `get_workspace_snapshot` must appear in the trace → `missing_tool_call`

### list_available_widgets (1)

#### `smoke_list_available_widgets`

**easy** · category: read · specification: explicit

> List the widgets available from Bench Stark Enterprise.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (1): `list_available_widgets`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `list_available_widgets` with args ⊇ {"origin": "Bench Stark Enterprise"} must appear in the trace → `missing_tool_call`

### manage_apps (1)

#### `smoke_manage_apps`

**easy** · category: dashboard · specification: explicit

> Instantiate the Stark Portfolio Command Center as Smoke Instantiated App.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (1): `manage_apps`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Smoke Instantiated App" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`

### manage_backends (1)

#### `smoke_manage_backends`

**easy** · category: platform · specification: explicit

> List connected Workspace backends once.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (1): `manage_backends`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "list"} must appear in the trace → `missing_tool_call`

### manage_dashboard (1)

#### `smoke_manage_dashboard`

**easy** · category: dashboard · specification: explicit

> Rename the Home dashboard to Smoke Home Dashboard.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (1): `manage_dashboard`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Smoke Home Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`

### manage_navigation_bar (1)

#### `smoke_manage_navigation_bar`

**easy** · category: dashboard · specification: explicit

> Create Overview and Details tabs on Home.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (1): `manage_navigation_bar`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `details` must exist (matched by tab id) → `missing_tab`

### navigate_workspace (1)

#### `smoke_navigate_workspace`

**easy** · category: dashboard · specification: explicit

> Navigate to Details and leave a small marker there.

- Initial workspace: dashboard "Smoke navigate_workspace"; 2 tab(s): overview, details
- Allowed tools (2): `navigate_workspace`, `add_generative_widget`
- Turn budget: 2 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Navigation Marker" on tab `details` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### read_widget (1)

#### `smoke_read_widget`

**easy** · category: read · specification: explicit

> Read the seeded Stark Alert Trend widget once.

- Initial workspace: dashboard "Smoke read_widget"; 1 tab(s): overview; 1 seeded widget(s): compliance_surveillance_hub_alerts_alert_trend({"severity": "High", "status": "Open", "period": "YTD"})
- Allowed tools (1): `read_widget`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `read_widget` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "compliance_surveillance_hub_alerts_alert_trend"} must appear in the trace → `missing_tool_call`

### read_workspace_resource (1)

#### `smoke_read_workspace_resource`

**easy** · category: read · specification: explicit

> Read the Workspace widget-types resource once.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (1): `read_workspace_resource`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `read_workspace_resource` with args ⊇ {"uri": "openbb://workspace/specs/widget-types"} must appear in the trace → `missing_tool_call`

### update_widget (1)

#### `smoke_update_widget`

**easy** · category: single-widget · specification: explicit

> Change the seeded Stark Alert Trend widget period to MTD.

- Initial workspace: dashboard "Smoke update_widget"; 1 tab(s): overview; 1 seeded widget(s): compliance_surveillance_hub_alerts_alert_trend({"severity": "High", "status": "Open", "period": "YTD"})
- Allowed tools (1): `update_widget`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_alerts_alert_trend` with data_args ⊇ {"period": "MTD"} → `missing_widget`

### update_widget_layout (1)

#### `smoke_update_widget_layout`

**easy** · category: single-widget · specification: explicit

> Resize the seeded Stark Alert Trend widget to 20 by 10.

- Initial workspace: dashboard "Smoke update_widget_layout"; 1 tab(s): overview; 1 seeded widget(s): compliance_surveillance_hub_alerts_alert_trend({"severity": "High", "status": "Open", "period": "YTD"})
- Allowed tools (1): `update_widget_layout`
- Turn budget: 1 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `compliance_surveillance_hub_alerts_alert_trend` must sit at exactly x=0, y=0, w=20, h=10 on tab `overview` → `layout_mismatch`


## Suite: enterprise-apps-default (69 tasks)

### cio_investment_committee_pack (3)

#### `cio_investment_committee_pack_p1`

**medium** · category: read · specification: -

> Create the investment committee packet summary with decisions required, allocation changes, capacity, research, and follow-ups.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "investment", "allocation", "52.01", "40.63", "6.21" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `cio_investment_committee_pack_p2`

**medium** · category: read · specification: -

> Identify recommendations where risk, liquidity, or research evidence conflicts with the proposed allocation.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "recommendations", "allocation", "50.48", "37.8", "97.02" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `cio_investment_committee_pack_p3`

**medium** · category: read · specification: -

> Draft the decision log update after committee review.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "committee", "decision", "61.24", "88.24", "52.01" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### client_360 (3)

#### `client_360_p1`

**medium** · category: read · specification: -

> Prepare an investor meeting brief with mandate context, performance, exposure, flows, requests, and approved talking points.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "performance", "investor", "0.0157", "0.0811", "11.13" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `client_360_p2`

**medium** · category: read · specification: -

> Identify client accounts with redemption risk or unresolved service issues.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "redemption", "unresolved", "11.13", "16.22", "77.48" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `client_360_p3`

**medium** · category: read · specification: -

> Draft a concise response to the client using only approved commentary and current portfolio context.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "commentary", "portfolio", "85.23", "0.0157" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### compliance_surveillance_hub (3)

#### `compliance_surveillance_hub_p1`

**medium** · category: read · specification: -

> Triage open surveillance alerts by severity, age, restricted-list overlap, and audit evidence.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "surveillance", "severity", "119", "18.98", "64.75" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `compliance_surveillance_hub_p2`

**medium** · category: read · specification: -

> Identify employee trades or research activity that should be escalated to compliance leadership.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "compliance", "leadership", "29.14", "19", "119" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `compliance_surveillance_hub_p3`

**medium** · category: read · specification: -

> Draft the investigation summary with evidence, next owner, and remediation status.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "investigation", "remediation", "64.75", "19" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### corporate_access_meeting_notes (3)

#### `corporate_access_meeting_notes_p1`

**medium** · category: read · specification: -

> Create a pre-meeting brief with prior claims, open follow-ups, expert-call context, and MNPI controls.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "MNPI", "follow-ups", "21.22", "4.24", "20.04" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `corporate_access_meeting_notes_p2`

**medium** · category: read · specification: -

> Flag meetings or notes that require compliance review before research can be distributed.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "meetings", "compliance", "20.04", "26.71", "57.19" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `corporate_access_meeting_notes_p3`

**medium** · category: read · specification: -

> Summarize management claims that changed the investment thesis and list the evidence still required.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "management", "evidence", "21.22", "49.26", "45.91" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### crypto_research_dashboard (3)

#### `crypto_research_dashboard_p1`

**medium** · category: read · specification: -

> Summarize crypto market structure: price action, liquidity, on-chain activity, funding, basis, and liquidation risk.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "liquidity", "liquidation", "40.83", "172896", "67.84" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `crypto_research_dashboard_p2`

**medium** · category: read · specification: -

> Identify assets where derivatives positioning conflicts with on-chain flow or spot market behavior.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "derivatives", "positioning", "40.83", "67.84", "172896" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `crypto_research_dashboard_p3`

**medium** · category: read · specification: -

> Draft the token thesis update using market, on-chain, derivatives, and research-document context.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "thesis", "on-chain", "172896", "67.84", "40.83" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### earnings_estimates_monitor (3)

#### `earnings_estimates_monitor_p1`

**medium** · category: read · specification: -

> Prepare the earnings preview: internal versus street estimates, expected surprise drivers, and trade setup.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "estimates", "earnings", "63.14", "8.82", "27.63" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_estimates_monitor_p2`

**medium** · category: read · specification: -

> Summarize post-earnings action items from price reaction, transcript tone, rating changes, and checklist status.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "transcript", "checklist", "55747.2", "81.37", "54.14" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `earnings_estimates_monitor_p3`

**medium** · category: read · specification: -

> Identify companies where estimate revisions and management commentary create a material thesis change.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "management", "commentary", "4.89", "33.55", "81.37" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### equity_research_workbench (3)

#### `equity_research_workbench_p1`

**medium** · category: read · specification: -

> Summarize what changed in coverage, estimates, valuation, ownership, and thesis since the last review.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "estimates", "valuation", "97.51", "8.1" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `equity_research_workbench_p2`

**medium** · category: read · specification: -

> Compare internal target price, street range, upside, and valuation sensitivity for the selected ticker.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "sensitivity", "valuation", "249629", "80700.4", "27.29" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `equity_research_workbench_p3`

**medium** · category: read · specification: -

> Draft the analyst call prep note with catalysts, risks, research approvals, and open evidence gaps.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "catalysts", "approvals", "39.25", "81.07", "7.98" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### execution_desk (3)

#### `execution_desk_p1`

**medium** · category: read · specification: -

> Prioritize the live blotter by liquidity, rejection risk, restricted-list status, and expected slippage.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "liquidity", "slippage", "14", "202", "41.08" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_desk_p2`

**medium** · category: read · specification: -

> Explain which fills underperformed arrival price and whether broker, venue, or algo choice drove the outcome.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "fills", "arrival", "41.08", "68.41", "9.92" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_desk_p3`

**medium** · category: read · specification: -

> Draft an end-of-day execution exception report for the PM and COO.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "execution", "exception", "167", "202", "215" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### executive_investment_dashboard (3)

#### `executive_investment_dashboard_p1`

**medium** · category: read · specification: -

> Write the executive briefing: firm AUM, flows, strategy returns, drawdown, stress risk, and major open issues.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "AUM", "stress", "90111.5", "83.06", "54.46" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `executive_investment_dashboard_p2`

**medium** · category: read · specification: -

> Identify which issues require CEO, CIO, COO, or CRO attention this week.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "issues", "CIO", "54.46", "45.63" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `executive_investment_dashboard_p3`

**medium** · category: read · specification: -

> Explain whether performance, flows, and risk are moving consistently across strategies.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "performance", "flows", "83.06", "0.0405", "-7000" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### fund_operations_control_tower (3)

#### `fund_operations_control_tower_p1`

**medium** · category: read · specification: -

> Create the operations morning checklist: failed trades, recon breaks, corporate actions, pricing exceptions, and owners.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "operations", "exceptions", "50.74", "1.67", "67" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `fund_operations_control_tower_p2`

**medium** · category: read · specification: -

> Prioritize breaks by age, dollar impact, settlement risk, and downstream NAV impact.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "breaks", "settlement", "1.67", "30.55", "61" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `fund_operations_control_tower_p3`

**medium** · category: read · specification: -

> Explain which operational issues need escalation before market open or NAV strike.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "operational", "escalation", "61", "67", "79.97" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### healthcare_research_dashboard (3)

#### `healthcare_research_dashboard_p1`

**medium** · category: read · specification: -

> Prepare the healthcare analyst brief: coverage, clinical catalysts, probability funnel, TAM, prescriptions, and research documents.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "prescriptions", "probability", "68.96", "7.43", "40.91" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `healthcare_research_dashboard_p2`

**medium** · category: read · specification: -

> Identify names where clinical probability and commercial revenue scenarios imply a thesis change.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "probability", "commercial", "68.96", "93.24", "7.43" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `healthcare_research_dashboard_p3`

**medium** · category: read · specification: -

> Draft the KOL follow-up plan with open questions and evidence needed for the investment committee.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "KOL", "follow-up", "22.38", "44.47", "68.96" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### liquidity_tca_workbench (3)

#### `liquidity_tca_workbench_p1`

**medium** · category: read · specification: -

> Recommend execution tactics by order size, volume profile, venue flow, and expected implementation shortfall.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "execution", "shortfall", "21", "40.06", "31.3" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `liquidity_tca_workbench_p2`

**medium** · category: read · specification: -

> Rank brokers by fill quality, commission, latency, and slippage for the selected desk.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "commission", "slippage", "16.9", "27.81", "53.77" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `liquidity_tca_workbench_p3`

**medium** · category: read · specification: -

> Summarize post-trade review items that require broker follow-up or algo parameter changes.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "broker", "parameter", "24.1", "119", "53.77" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### mnpi_research_review (3)

#### `mnpi_research_review_p1`

**medium** · category: read · specification: -

> Review the MNPI case file: wall crossings, meetings, research drafts, target changes, and sign-off history.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "crossings", "meetings", "99.08", "74.8", "31.85" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `mnpi_research_review_p2`

**medium** · category: read · specification: -

> Identify research items that cannot be published until compliance evidence is complete.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "research", "evidence", "31.85", "5.45", "64.44" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `mnpi_research_review_p3`

**medium** · category: read · specification: -

> Create the approval narrative for legal review with unresolved risks and required attestations.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "attestations", "unresolved", "5.45", "97.4", "64.44" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### nav_fees_close_dashboard (3)

#### `nav_fees_close_dashboard_p1`

**medium** · category: read · specification: -

> Prepare the close package: NAV bridge, tolerance exceptions, fee accruals, cash breaks, and unresolved dependencies.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "dependencies", "exceptions", "29.76", "93.49", "45.09" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `nav_fees_close_dashboard_p2`

**medium** · category: read · specification: -

> Identify items that could delay the daily or monthly NAV sign-off.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "NAV", "sign-off", "12.67", "225", "45.09" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `nav_fees_close_dashboard_p3`

**medium** · category: read · specification: -

> Summarize fee, cash, and pricing exceptions that require fund controller approval.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "exceptions", "controller", "93.49", "51.07", "225" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### portfolio_command_center (3)

#### `portfolio_command_center_p1`

**medium** · category: read · specification: -

> Prepare the PM morning note: overnight P&L, largest active exposures, limit pressure, and trade actions by urgency.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "overnight", "exposures", "0.0389", "85.25", "62.35" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `portfolio_command_center_p2`

**medium** · category: read · specification: -

> Find holdings where conviction, liquidity, and risk contribution disagree with the current portfolio weight.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "contribution", "conviction", "85.65", "29.38", "20.59" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `portfolio_command_center_p3`

**medium** · category: read · specification: -

> Explain which alerts should be escalated to the CIO before the opening risk meeting.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "alerts", "escalated", "193", "85.25", "86.16" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### quant_research_backtest_lab (3)

#### `quant_research_backtest_lab_p1`

**medium** · category: read · specification: -

> Evaluate whether the selected model is production-ready using signal quality, backtest path, risk exposures, and capacity.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "signal", "exposures", "83.92", "35.41", "0.0342" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `quant_research_backtest_lab_p2`

**medium** · category: read · specification: -

> Identify signals with attractive IC but unacceptable turnover, crowding, or liquidity cost.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "signals", "turnover", "83.92", "55.65", "26.45" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `quant_research_backtest_lab_p3`

**medium** · category: read · specification: -

> Draft the model review memo for PM and risk approval.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "approval", "model", "83.92", "35.41", "0.0342" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### rebalance_scenario_lab (3)

#### `rebalance_scenario_lab_p1`

**medium** · category: read · specification: -

> Draft a rebalance recommendation that balances target drift, liquidity cost, restricted-list checks, and scenario downside.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "rebalance", "drift", "0.0471", "10.55", "31.12" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `rebalance_scenario_lab_p2`

**medium** · category: read · specification: -

> Identify proposed trades that should be resized or delayed because of ADV usage, constraints, or compliance blockers.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "constraints", "compliance", "13.46", "10.55", "22.35" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `rebalance_scenario_lab_p3`

**medium** · category: read · specification: -

> Create an approval memo with implementation risk, residual drift, and the decision needed from the PM.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "implementation", "approval", "36.17", "22.05", "19.65" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### reporting_factsheet_studio (3)

#### `reporting_factsheet_studio_p1`

**medium** · category: read · specification: -

> Build the monthly reporting checklist: performance, attribution, risk stats, commentary, disclosures, and DDQ blockers.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "performance", "attribution", "0.1015", "36.9", "1.39" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `reporting_factsheet_studio_p2`

**medium** · category: read · specification: -

> Find factsheet language that needs approval before external distribution.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "distribution", "factsheet", "26.04", "8.82" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `reporting_factsheet_studio_p3`

**medium** · category: read · specification: -

> Summarize what changed in returns, attribution, risk, and client-facing commentary for the selected period.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "attribution", "commentary", "0.1015", "36.9", "8.82" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### risk_exposure_monitor (3)

#### `risk_exposure_monitor_p1`

**medium** · category: read · specification: -

> Prepare the risk officer briefing: VaR drivers, stress losses, concentration, breaches, and recommended actions.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "concentration", "breaches", "-103000", "0.0359", "0.0137" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `risk_exposure_monitor_p2`

**medium** · category: read · specification: -

> Identify positions contributing disproportionate marginal VaR or stress P&L relative to their portfolio weight.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "positions", "VaR", "0.0187", "-56000", "0.0833" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `risk_exposure_monitor_p3`

**medium** · category: read · specification: -

> Explain which limits are closest to escalation and what portfolio changes would reduce utilization.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "utilization", "escalation", "0.0339", "0.0137", "0.0732" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### strategy_health_monitor (3)

#### `strategy_health_monitor_p1`

**medium** · category: read · specification: -

> Rank strategy sleeves by return quality, drawdown behavior, crowding, and remaining capacity.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "drawdown", "capacity", "15.3", "43.5", "92.83" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `strategy_health_monitor_p2`

**medium** · category: read · specification: -

> Highlight themes where factor tilt or liquidity capacity is inconsistent with PM conviction.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "conviction", "capacity", "29.82", "82.47", "92.83" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `strategy_health_monitor_p3`

**medium** · category: read · specification: -

> Build the weekly strategy-health brief for the CIO with watchlist names and catalyst risk.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "watchlist", "catalyst", "14.24", "62.05", "43.5" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### stress_liquidity_lab (3)

#### `stress_liquidity_lab_p1`

**medium** · category: read · specification: -

> Summarize the selected stress scenario with portfolio loss, liquidation days, crowded names, and redemption impact.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "liquidation", "redemption", "-49500", "62.96", "54.69" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `stress_liquidity_lab_p2`

**medium** · category: read · specification: -

> Find assumptions that should be challenged before the risk committee signs off.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "assumptions", "committee", "87.8", "62.96" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `stress_liquidity_lab_p3`

**medium** · category: read · specification: -

> Create the committee sign-off note with unresolved actions and owners.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "unresolved", "committee", "76.26", "8.67" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### vendor_dataset_monitor (3)

#### `vendor_dataset_monitor_p1`

**medium** · category: read · specification: -

> Prepare the vendor SLA report by latency, freshness, validation failures, incidents, and affected fund apps.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "validation", "freshness", "727", "124", "59.16" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_dataset_monitor_p2`

**medium** · category: read · specification: -

> Identify data quality issues that create trading, risk, reporting, or compliance impact.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "compliance", "reporting", "59.16", "188", "94.16" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_dataset_monitor_p3`

**medium** · category: read · specification: -

> Draft the vendor escalation note with affected datasets, app impact, and owner actions.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "escalation", "affected", "94.16", "18.67", "24.33" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### workspace_data_control_center (3)

#### `workspace_data_control_center_p1`

**medium** · category: read · specification: -

> Audit data platform readiness: failed jobs, stale feeds, entitlements, exports, and Copilot visibility flags.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "entitlements", "visibility", "96.33", "99.15", "61.17" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `workspace_data_control_center_p2`

**medium** · category: read · specification: -

> Identify apps or widgets whose data or AI access should be restricted before a fund demo or production rollout.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "restricted", "production", "3.14", "61.17", "96.33" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `workspace_data_control_center_p3`

**medium** · category: read · specification: -

> Summarize usage, export, and prompt-audit activity for the platform owner.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (5): `get_workspace_snapshot`, `navigate_workspace`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "usage", "prompt-audit", "58.09", "86.66", "34.77" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`


## Suite: enterprise-apps-usage (300 tasks)

### apps (20)

#### `client_360`

**easy** · category: platform · specification: - · no-op baseline score: 0.000

> From the Bench Stark Enterprise backend, instantiate the Client 360 app as a new dashboard named Client Review Workspace.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `get_workspace_snapshot`, `manage_backends`, `manage_apps`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Review Workspace" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`

#### `compliance_surveillance_hub`

**easy** · category: platform · specification: - · no-op baseline score: 0.000

> Instantiate the Compliance Surveillance Hub app from the Bench Stark Enterprise backend as a new dashboard named Daily Surveillance Board.

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

#### `earnings_estimates_monitor`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> From the Bench Stark Enterprise backend, instantiate the Earnings & Estimates Monitor app as a new dashboard named Earnings Season Monitor.

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

#### `equity_research_workbench`

**easy** · category: platform · specification: - · no-op baseline score: 0.000

> From the Bench Stark Enterprise backend, instantiate the Equity Research Workbench app as a new dashboard named Coverage Workbench.

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

#### `execution_desk`

**easy** · category: platform · specification: - · no-op baseline score: 0.000

> Create a new dashboard named AM Execution Desk by instantiating the Execution Desk app from the Bench Stark Enterprise backend.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `get_workspace_snapshot`, `manage_backends`, `manage_apps`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "AM Execution Desk" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`

#### `executive_investment_dashboard`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> From the Bench Stark Enterprise backend, instantiate the Executive Investment Dashboard app as a new dashboard named Executive Morning Brief.

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

#### `extend_fund_operations_control_tower`

**hard** · category: platform · specification: - · no-op baseline score: 0.000

> Instantiate the Fund Operations Control Tower app from the Bench Stark Enterprise backend as a new dashboard named Ops Control Room. Then add the Break Aging widget (id fund_operations_control_tower_recons_break_aging) to the Recons tab of the new dashboard.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (7): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

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

#### `extend_portfolio_command_center`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> From the Bench Stark Enterprise backend, instantiate the Portfolio Command Center app as a new dashboard named PM Command Post. Then add the Sector Exposure widget (id portfolio_command_center_holdings_sector_exposure) to the Holdings tab of the new dashboard.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (7): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

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

#### `extend_rebalance_scenario_lab`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> Instantiate the Rebalance & Scenario Lab app from the Bench Stark Enterprise backend as a new dashboard named Rebalance Studio. Then add the Drift by Sleeve widget (id Drift by Sleeve) to the Drift tab of the new dashboard.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (7): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Rebalance Studio" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `approval` must exist (matched by tab id) → `missing_tab`
- **Tab** `drift` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/rebalance_scenario_lab_approval_approval_checklist` on tab `approval` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/rebalance_scenario_lab_drift_current_vs_target_weights` on tab `drift` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/rebalance_scenario_lab_drift_drift_by_sleeve` on tab `drift` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`

#### `extend_strategy_health_monitor`

**hard** · category: platform · specification: - · no-op baseline score: 0.000

> From the Bench Stark Enterprise backend, instantiate the Strategy Health Monitor app as a new dashboard named Strategy Health Desk. Then add the Catalyst Calendar widget (id strategy_health_monitor_watchlist_catalyst_calendar) to the Watchlist tab of the new dashboard.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (7): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

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

#### `full_corporate_access_meeting_notes`

**hard** · category: platform · specification: - · no-op baseline score: 0.000

> From the Bench Stark Enterprise backend, instantiate the Corporate Access & Meeting Notes app as a new dashboard named Corporate Access Log. Then add the Expert Calls widget (id corporate_access_meeting_notes_meetings_expert_calls) to the Meetings tab, and add a note on the same tab mentioning expert calls and meeting calendar.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (8): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

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

#### `full_crypto_research_dashboard`

**hard** · category: platform · specification: - · no-op baseline score: 0.000

> From the Bench Stark Enterprise backend, instantiate the Crypto Research Dashboard app as a new dashboard named Digital Assets Desk. Then add the Crypto Market Metrics widget (id crypto_research_dashboard_market_crypto_market_metrics) to the Market tab, and add a note on the same tab mentioning market metrics and token.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (8): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

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

#### `full_healthcare_research_dashboard`

**hard** · category: platform · specification: - · no-op baseline score: 0.000

> Instantiate the Healthcare Research Dashboard app from the Bench Stark Enterprise backend as a new dashboard named Biotech Catalyst Desk. Then add the Regulatory Timeline widget (id healthcare_research_dashboard_clinical_regulatory_timeline) to the Clinical tab, and add a note on the same tab mentioning regulatory timeline and catalysts.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (8): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

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

#### `full_mnpi_research_review`

**hard** · category: platform · specification: - · no-op baseline score: 0.000

> Instantiate the MNPI & Research Review app from the Bench Stark Enterprise backend as a new dashboard named MNPI Control Desk. Then add the Reviewer Comments widget (id mnpi_research_review_research_reviewer_comments) to the Research tab, and add a note on the same tab mentioning reviewer comments and sign off.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (8): `get_workspace_snapshot`, `manage_backends`, `manage_apps`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

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

#### `note_nav_fees_close_dashboard`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> Create a new dashboard named Monthly Close Control by instantiating the NAV, Fees & Close Dashboard app from the Bench Stark Enterprise backend, then add a note on the Close tab mentioning close checklist and exceptions.

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

#### `note_quant_research_backtest_lab`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> Instantiate the Quant Research & Backtest Lab app from the Bench Stark Enterprise backend as a new dashboard named Signal Research Lab, then add a note on the Signals tab mentioning signal and decay.

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

#### `note_reporting_factsheet_studio`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> Create a new dashboard named Factsheet Control by instantiating the Reporting & Factsheet Studio app from the Bench Stark Enterprise backend, then add a note on the Factsheets tab mentioning factsheet and distribution.

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

#### `note_stress_liquidity_lab`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> Create a new dashboard named Quarterly Stress Review by instantiating the Stress & Liquidity Lab app from the Bench Stark Enterprise backend, then add a HTML card on the Sign Off tab mentioning sign off and residual risk.

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
- **Generated html** ≥1× whose content mentions "sign off", "residual risk" on tab `sign_off` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`

#### `risk_exposure_monitor`

**easy** · category: platform · specification: - · no-op baseline score: 0.000

> From the Bench Stark Enterprise backend, instantiate the Risk & Exposure Monitor app as a new dashboard named Risk Watch.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `get_workspace_snapshot`, `manage_backends`, `manage_apps`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Risk Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`

#### `vendor_dataset_monitor`

**easy** · category: platform · specification: - · no-op baseline score: 0.000

> Create a new dashboard named Data Vendor Watch by instantiating the Vendor & Dataset Monitor app from the Bench Stark Enterprise backend.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `get_workspace_snapshot`, `manage_backends`, `manage_apps`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Data Vendor Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`

### backends (20)

#### `add_equities`

**easy** · category: dashboard · specification: - · no-op baseline score: 0.000

> With manage_backends, use operation add and name equities to register Bench Equities, then list it with operation list.

- Initial workspace: dashboard "Backend Registration"
- Allowed tools (1): `manage_backends`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "list"} must appear in the trace → `missing_tool_call`
- **Tool result** of `manage_backends` must contain "Bench Equities" (agent must actually retrieve the data) → `missing_tool_result`

#### `add_macro`

**easy** · category: dashboard · specification: - · no-op baseline score: 0.000

> Call manage_backends with operation add and name macro to register Bench Macro, then call manage_backends with operation list.

- Initial workspace: dashboard "Backend Registration"
- Allowed tools (1): `manage_backends`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "list"} must appear in the trace → `missing_tool_call`
- **Tool result** of `manage_backends` must contain "Bench Macro" (agent must actually retrieve the data) → `missing_tool_result`

#### `add_portfolio`

**easy** · category: dashboard · specification: - · no-op baseline score: 0.000

> With manage_backends, use operation add and name portfolio to register Bench Portfolio, then list it with operation list.

- Initial workspace: dashboard "Backend Registration"
- Allowed tools (1): `manage_backends`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "list"} must appear in the trace → `missing_tool_call`
- **Tool result** of `manage_backends` must contain "Bench Portfolio" (agent must actually retrieve the data) → `missing_tool_result`

#### `add_stark_enterprise`

**easy** · category: dashboard · specification: - · no-op baseline score: 0.000

> With manage_backends, use operation add and name stark-enterprise to register Bench Stark Enterprise, then list it with operation list.

- Initial workspace: dashboard "Backend Registration"
- Allowed tools (1): `manage_backends`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "list"} must appear in the trace → `missing_tool_call`
- **Tool result** of `manage_backends` must contain "Bench Stark Enterprise" (agent must actually retrieve the data) → `missing_tool_result`

#### `multi_equities_macro`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Register the needed backends by exact name (equities, macro); then build a dashboard with Bench Equities/price_performance with data_args {"symbol": "AAPL"} and Bench Macro/macro_timeseries with data_args {"series": "DGS10"}, and add a HTML card mentioning AAPL and DGS10.

- Initial workspace: dashboard "Multi Backend Build"
- Allowed tools (6): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Generated html** ≥1× whose content mentions "AAPL", "DGS10" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥2× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `multi_equities_portfolio`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> After registering backend names equities, portfolio, build a dashboard with Bench Equities/latest_news with data_args {"limit": 5, "symbol": "NVDA"} and Bench Portfolio/holdings_table, and add a note mentioning NVDA and holdings.

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

#### `multi_portfolio_macro`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Register backend names portfolio, macro, build a dashboard with Bench Portfolio/risk_metrics and Bench Macro/yield_curve, and add a HTML card mentioning portfolio and yield curve.

- Initial workspace: dashboard "Multi Backend Build"
- Allowed tools (6): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Widget** ≥1× `Bench Macro/yield_curve` → `missing_widget`
- **Generated html** ≥1× whose content mentions "portfolio", "yield curve" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥2× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `multi_stark_portfolio`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Register the needed backends by exact name (stark-enterprise, portfolio); then build a dashboard with Bench Stark Enterprise/equity_research_workbench_valuation_football_field and Bench Portfolio/sector_exposure, and add a HTML card mentioning stark and sector exposure.

- Initial workspace: dashboard "Multi Backend Build"
- Allowed tools (6): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/equity_research_workbench_valuation_football_field` → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`
- **Generated html** ≥1× whose content mentions "stark", "sector exposure" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥2× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `refresh_backend_before_building_holdings_table`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> After registering backend name portfolio and refreshing Bench Portfolio, add Bench Portfolio/holdings_table and document that the backend was refreshed.

- Initial workspace: dashboard "Backend Refresh Build"
- Allowed tools (6): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`
- **Generated note** ≥1× whose content mentions "refreshed", "Bench Portfolio" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "refresh"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `refresh_backend_before_building_macro_timeseries`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Register Bench Macro with backend name macro, refresh it, then add Bench Macro/macro_timeseries with data_args {"series": "DGS10"} and document that the backend was refreshed.

- Initial workspace: dashboard "Backend Refresh Build"
- Allowed tools (6): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "refreshed", "Bench Macro" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "refresh"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `refresh_backend_before_building_post_earnings_checklist`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> After registering backend name stark-enterprise and refreshing Bench Stark Enterprise, add Bench Stark Enterprise/Post-Earnings Checklist and document that the backend was refreshed.

- Initial workspace: dashboard "Backend Refresh Build"
- Allowed tools (6): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_post_earnings_post_earnings_checklist` → `missing_widget`
- **Generated note** ≥1× whose content mentions "refreshed", "Bench Stark Enterprise" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "refresh"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `refresh_backend_before_building_price_performance`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> After registering backend name equities and refreshing Bench Equities, add Bench Equities/price_performance with data_args {"symbol": "AAPL"} and document that the backend was refreshed.

- Initial workspace: dashboard "Backend Refresh Build"
- Allowed tools (6): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Generated html** ≥1× whose content mentions "refreshed", "Bench Equities" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "refresh"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `register_backend_and_add_holdings_table`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Call manage_backends with operation add and name portfolio to register Bench Portfolio; then discover holdings_table, fetch its schema, and add Bench Portfolio/holdings_table to the active dashboard.

- Initial workspace: dashboard "Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `register_backend_and_add_macro_timeseries`

**easy** · category: dashboard · specification: - · no-op baseline score: 0.000

> After calling manage_backends with operation add and name macro for Bench Macro, discover macro_timeseries, fetch its schema, and add Bench Macro/macro_timeseries with data_args {"series": "DGS10"} to the active dashboard.

- Initial workspace: dashboard "Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `register_backend_and_add_post_earnings_checklist`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Call manage_backends with operation add and name stark-enterprise to register Bench Stark Enterprise; then discover Post-Earnings Checklist, fetch its schema, and add Bench Stark Enterprise/Post-Earnings Checklist to the active dashboard.

- Initial workspace: dashboard "Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_post_earnings_post_earnings_checklist` → `missing_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `register_backend_and_add_price_performance`

**easy** · category: dashboard · specification: - · no-op baseline score: 0.000

> After calling manage_backends with operation add and name equities for Bench Equities, discover price_performance, fetch its schema, and add Bench Equities/price_performance with data_args {"symbol": "AAPL"} to the active dashboard.

- Initial workspace: dashboard "Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `register_two_backends_fundamental_metrics_and_holdings_table`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Register both backends by name (equities, portfolio); then fetch each widget's schema and add Bench Equities/fundamental_metrics with data_args {"symbol": "NVDA"} and Bench Portfolio/holdings_table to the active dashboard.

- Initial workspace: dashboard "Cross Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 12 · oracle reference trace: 9 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`
- **Tool call** ≥2× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `register_two_backends_latest_news_and_yield_curve`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Register both backends by name (equities, macro); then fetch each widget's schema and add Bench Equities/latest_news with data_args {"limit": 5, "symbol": "MSFT"} and Bench Macro/yield_curve to the active dashboard.

- Initial workspace: dashboard "Cross Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 12 · oracle reference trace: 9 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "MSFT", "limit": 5} → `missing_widget`
- **Widget** ≥1× `Bench Macro/yield_curve` → `missing_widget`
- **Tool call** ≥2× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `register_two_backends_ownership_snapshot_and_risk_metrics`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Register backend names stark-enterprise and portfolio; then fetch each widget's schema and add Bench Stark Enterprise/equity_research_workbench_company_ownership_snapshot and Bench Portfolio/risk_metrics to the active dashboard.

- Initial workspace: dashboard "Cross Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 12 · oracle reference trace: 9 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/equity_research_workbench_company_ownership_snapshot` → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Tool call** ≥2× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `register_two_backends_sector_exposure_and_macro_timeseries`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Register backend names portfolio and macro; then fetch each widget's schema and add Bench Portfolio/sector_exposure and Bench Macro/macro_timeseries with data_args {"series": "FEDFUNDS"} to the active dashboard.

- Initial workspace: dashboard "Cross Backend Build"
- Allowed tools (5): `manage_backends`, `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 12 · oracle reference trace: 9 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "FEDFUNDS"} → `missing_widget`
- **Tool call** ≥2× `manage_backends` with args ⊇ {"operation": "add"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

### create (20)

#### `cross_aapl_rates`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> On the active dashboard, add these two widgets: the Price Performance widget from Bench Equities for AAPL and the Macro Timeseries widget from Bench Macro for DGS10. Then add a HTML card mentioning AAPL and DGS10.

- Fixture backends: equities, macro
- Initial workspace: dashboard "Cross-Backend Task"
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 8 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Generated html** ≥1× whose content mentions "AAPL", "DGS10" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `cross_book_inflation`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Build the active dashboard with these two widgets: the Holdings Table widget from Bench Portfolio and the Macro Timeseries widget from Bench Macro for CPIAUCSL. Add a note mentioning holdings and CPIAUCSL.

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

#### `cross_msft_exposure`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Add these two widgets to the active dashboard: the Latest News widget from Bench Equities for MSFT and the Sector Exposure widget from Bench Portfolio. Then add a note mentioning MSFT and sector exposure.

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

#### `cross_nvda_curve`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> On the active dashboard, add these two widgets: the Price Performance widget from Bench Equities for NVDA and the Yield Curve widget from Bench Macro. Then add a note mentioning NVDA and yield curve.

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

#### `estimate_history_nvda`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Add the Estimate History widget for NVDA to the active dashboard. Discover the widget catalog and its schema before creating.

- Fixture backends: equities
- Initial workspace: dashboard "Creation Task"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `read_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `latest_news_aapl`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> On the active dashboard, create a Latest News widget (widget_id latest_news) from the Bench Equities backend with data_args {"symbol": "AAPL", "limit": 5}.

- Fixture backends: equities
- Initial workspace: dashboard "Creation Task"
- Allowed tools (3): `get_workspace_snapshot`, `create_widget`, `read_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL", "limit": 5} → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `macro_timeseries_dgs10`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> To the active dashboard, add the Macro Timeseries widget for DGS10. Discover the widget catalog and its schema before creating.

- Fixture backends: macro
- Initial workspace: dashboard "Creation Task"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `read_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `place_fundamental_metrics_aapl`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Place a Fundamental Metrics widget for AAPL at exactly x=0, y=0, width 10, height 8. Fetch the widget schema and confirm the symbol value through the parameter options before creating.

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

#### `place_latest_news_msft`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Add the Latest News widget for MSFT and place it at exactly x=20, y=0, width 20, height 10. Fetch the widget schema and confirm the symbol value through the parameter options before creating.

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

#### `place_macro_timeseries_fedfunds`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Fetch the widget schema and confirm the series value through the parameter options before creating the Macro Timeseries widget for FEDFUNDS, then place it at exactly x=0, y=2, width 20, height 10.

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

#### `place_price_performance_nvda`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Fetch the widget schema and confirm the symbol value through the parameter options before creating the Price Performance widget for NVDA, then place it at exactly x=0, y=2, width 20, height 12.

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

#### `preserve_fundamental_metrics_msft`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> Keep the existing Estimate History widget undisturbed and non-overlapped while adding the Fundamental Metrics widget for MSFT next to it.

- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): estimate_history({"symbol": "MSFT"})
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `read_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `preserve_latest_news_aapl`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Keep the existing Price Performance widget undisturbed and non-overlapped while adding the Latest News widget for AAPL next to it.

- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): price_performance({"symbol": "AAPL"})
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `read_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL", "limit": 5} → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `preserve_risk_metrics_plain`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> This dashboard already has a Holdings Table widget. Add the Risk Metrics widget next to it without disturbing the existing widget or overlapping it.

- Fixture backends: portfolio
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): holdings_table({})
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `read_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `preserve_yield_curve_plain`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Keep the existing Macro Timeseries widget undisturbed and non-overlapped while adding the Yield Curve widget next to it.

- Fixture backends: macro
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): macro_timeseries({"series": "DGS10"})
- Allowed tools (7): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`, `read_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Macro/yield_curve` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `price_performance_aapl`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> On the active dashboard, create a Price Performance widget (widget_id price_performance) from the Bench Equities backend with data_args {"symbol": "AAPL"}.

- Fixture backends: equities
- Initial workspace: dashboard "Creation Task"
- Allowed tools (3): `get_workspace_snapshot`, `create_widget`, `read_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `price_performance_msft`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> To the active dashboard, add the Price Performance widget for MSFT. Discover the widget catalog and its schema before creating.

- Fixture backends: equities
- Initial workspace: dashboard "Creation Task"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `read_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `risk_metrics_plain`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Create a Risk Metrics widget (widget_id risk_metrics) from the Bench Portfolio backend on the active dashboard.

- Fixture backends: portfolio
- Initial workspace: dashboard "Creation Task"
- Allowed tools (3): `get_workspace_snapshot`, `create_widget`, `read_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `sector_exposure_plain`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> To the active dashboard, add the Sector Exposure widget. Discover the widget catalog and its schema before creating.

- Fixture backends: portfolio
- Initial workspace: dashboard "Creation Task"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `read_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `yield_curve_plain`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Create a Yield Curve widget (widget_id yield_curve) from the Bench Macro backend on the active dashboard.

- Fixture backends: macro
- Initial workspace: dashboard "Creation Task"
- Allowed tools (3): `get_workspace_snapshot`, `create_widget`, `read_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/yield_curve` → `missing_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

### delegate (20)

#### `build_earnings_build`

**hard** · category: platform · specification: - · no-op baseline score: 0.000

> Use assign_tasks_to_agents with two task_requests using ids revisions-analyst and reaction-analyst. Then add the Consensus Revisions widget (id earnings_estimates_monitor_estimates_consensus_revisions) from the Bench Stark Enterprise backend so the workstreams have their data, and add a coordinator note naming both workstreams. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_themes_crowded_names({})
- Allowed tools (6): `get_workspace_snapshot`, `assign_tasks_to_agents`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/earnings_estimates_monitor_estimates_consensus_revisions` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_themes_crowded_names` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "revisions analyst", "reaction analyst", "consensus revisions" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "revisions-analyst", "reaction-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `build_exec_build`

**hard** · category: platform · specification: - · no-op baseline score: 0.000

> Use assign_tasks_to_agents with two task_requests using ids rejects-analyst and restricted-analyst. Then add the Rejected Orders widget (id execution_desk_exceptions_rejected_orders) from the Bench Stark Enterprise backend so the workstreams have their data, and add a coordinator note naming both workstreams. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_themes_factor_tilts({})
- Allowed tools (6): `get_workspace_snapshot`, `assign_tasks_to_agents`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_exceptions_rejected_orders` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_themes_factor_tilts` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "rejects analyst", "restricted analyst", "rejected orders" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "rejects-analyst", "restricted-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `build_risk_build`

**hard** · category: platform · specification: - · no-op baseline score: 0.000

> Use assign_tasks_to_agents with two task_requests using ids var-analyst and stress-analyst. Then add the VaR Trend widget (id risk_exposure_monitor_dashboard_var_trend) from the Bench Stark Enterprise backend so the workstreams have their data, and add a coordinator note naming both workstreams. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_themes_thematic_baskets({})
- Allowed tools (6): `get_workspace_snapshot`, `assign_tasks_to_agents`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_var_trend` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_themes_thematic_baskets` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "var analyst", "stress analyst", "var trend" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "var-analyst", "stress-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `build_vendor_build`

**hard** · category: platform · specification: - · no-op baseline score: 0.000

> Call assign_tasks_to_agents with two task_requests using ids triage-analyst and sla-analyst. Then add the Incident Log widget (id vendor_dataset_monitor_incidents_incident_log) from the Bench Stark Enterprise backend so the workstreams have their data, and add a coordinator HTML card naming both workstreams. Omit dashboard_id when adding the HTML card.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_watchlist_names_near_action_levels({})
- Allowed tools (6): `get_workspace_snapshot`, `assign_tasks_to_agents`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_incidents_incident_log` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_watchlist_names_near_action_levels` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated html** ≥1× whose content mentions "triage analyst", "sla analyst", "incident log" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "triage-analyst", "sla-analyst" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `client_note`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> Call assign_tasks_to_agents with two task_requests using ids ir-analyst and portfolio-analyst for client meeting prep work. Then add a coordinator note naming both workstreams on the active dashboard; omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_watchlist_trade_ideas({})
- Allowed tools (3): `get_workspace_snapshot`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_watchlist_trade_ideas` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "ir analyst", "portfolio analyst", "client meeting" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "ir-analyst", "portfolio-analyst" (agent must actually retrieve the data) → `missing_tool_result`

#### `client_pair`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> Use assign_tasks_to_agents with two task_requests using ids ir-analyst and portfolio-analyst for client meeting prep work.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_liquidity_crowded_names({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_liquidity_crowded_names` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "ir-analyst", "portfolio-analyst" (agent must actually retrieve the data) → `missing_tool_result`

#### `client_single`

**easy** · category: platform · specification: - · no-op baseline score: 0.000

> Use assign_tasks_to_agents with one task_request using id ir-analyst for client meeting prep work: Prepare talking points and open requests for the client meeting.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_liquidity_redemption_stress({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_liquidity_redemption_stress` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "ir-analyst" (agent must actually retrieve the data) → `missing_tool_result`

#### `compliance_pair`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> Use assign_tasks_to_agents with two task_requests using ids alerts-analyst and restricted-analyst for compliance surveillance work.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_overview_workflow_overview({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_overview_workflow_overview` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "alerts-analyst", "restricted-analyst" (agent must actually retrieve the data) → `missing_tool_result`

#### `earnings_note`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> Call assign_tasks_to_agents with two task_requests using ids coverage-analyst and model-analyst for earnings prep work. Then add a coordinator note naming both workstreams on the active dashboard; omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_sign_off_approval_checklist({})
- Allowed tools (3): `get_workspace_snapshot`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_sign_off_approval_checklist` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "coverage analyst", "model analyst", "earnings prep" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "coverage-analyst", "model-analyst" (agent must actually retrieve the data) → `missing_tool_result`

#### `earnings_pair`

**easy** · category: platform · specification: - · no-op baseline score: 0.000

> For earnings prep work, call assign_tasks_to_agents with two task_requests using ids coverage-analyst and model-analyst.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_sign_off_residual_risk_actions({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_sign_off_residual_risk_actions` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "coverage-analyst", "model-analyst" (agent must actually retrieve the data) → `missing_tool_result`

#### `earnings_single`

**easy** · category: platform · specification: - · no-op baseline score: 0.000

> Use assign_tasks_to_agents with one task_request using id coverage-analyst for earnings prep work: Review estimate revisions and transcript tone for earnings prep.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_sign_off_risk_committee_comments({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_sign_off_risk_committee_comments` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "coverage-analyst" (agent must actually retrieve the data) → `missing_tool_result`

#### `ops_note`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> For vendor sla monitoring work, call assign_tasks_to_agents with two task_requests using ids triage-analyst and sla-analyst. Then add a coordinator note naming both workstreams on the active dashboard; omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_slas_latency_by_feed({})
- Allowed tools (3): `get_workspace_snapshot`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_slas_latency_by_feed` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "triage analyst", "sla analyst", "vendor" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "triage-analyst", "sla-analyst" (agent must actually retrieve the data) → `missing_tool_result`

#### `risk_note`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> Use assign_tasks_to_agents with two task_requests using ids stress-analyst and limits-analyst for risk review work. Then add a coordinator note naming both workstreams on the active dashboard; omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_data_health_feed_status({})
- Allowed tools (3): `get_workspace_snapshot`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_data_health_feed_status` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "stress analyst", "limits analyst", "risk review" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "stress-analyst", "limits-analyst" (agent must actually retrieve the data) → `missing_tool_result`

#### `risk_pair`

**easy** · category: platform · specification: - · no-op baseline score: 0.000

> Call assign_tasks_to_agents with two task_requests using ids stress-analyst and limits-analyst for risk review work.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_data_health_latency_and_freshness({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_data_health_latency_and_freshness` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "stress-analyst", "limits-analyst" (agent must actually retrieve the data) → `missing_tool_result`

#### `risk_single`

**easy** · category: platform · specification: - · no-op baseline score: 0.000

> Call assign_tasks_to_agents with one task_request using id stress-analyst for risk review work: Run the historical stress scenarios and summarize losses.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_entitlements_app_and_widget_permissions({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_entitlements_app_and_widget_permissions` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "stress-analyst" (agent must actually retrieve the data) → `missing_tool_result`

#### `skill_comps_skill`

**hard** · category: platform · specification: - · no-op baseline score: 0.000

> After calling get_skill_content with slug finance-comps to understand the workflow, call assign_tasks_to_agents with two task_requests using ids peers-analyst and multiples-analyst covering that workflow, and add a coordinator note naming both workstreams. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_entitlements_sensitive_dataset_flags({})
- Allowed tools (4): `get_workspace_snapshot`, `get_skill_content`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_entitlements_sensitive_dataset_flags` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "peers analyst", "multiples analyst", "comps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-comps"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Comps workflow", "peer set", "valuation multiples" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `assign_tasks_to_agents` must contain "peers-analyst", "multiples-analyst" (agent must actually retrieve the data) → `missing_tool_result`

#### `skill_earnings_skill`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> Call get_skill_content with slug finance-earnings-prep to understand the workflow. Then call assign_tasks_to_agents with two task_requests using ids coverage-analyst and model-analyst covering that workflow, and add a coordinator note naming both workstreams. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_overview_workflow_overview({})
- Allowed tools (4): `get_workspace_snapshot`, `get_skill_content`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_overview_workflow_overview` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "coverage analyst", "model analyst", "earnings prep" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-earnings-prep"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Earnings prep workflow", "surprise drivers", "portfolio manager" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `assign_tasks_to_agents` must contain "coverage-analyst", "model-analyst" (agent must actually retrieve the data) → `missing_tool_result`

#### `skill_guidance_skill`

**hard** · category: platform · specification: - · no-op baseline score: 0.000

> After calling get_skill_content with slug finance-guidance-tracker to understand the workflow, call assign_tasks_to_agents with two task_requests using ids claims-analyst and evidence-analyst covering that workflow, and add a coordinator note naming both workstreams. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_usage_app_usage({})
- Allowed tools (4): `get_workspace_snapshot`, `get_skill_content`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_usage_app_usage` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "claims analyst", "evidence analyst", "guidance" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-guidance-tracker"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Guidance tracker workflow", "management claims", "evidence gaps" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `assign_tasks_to_agents` must contain "claims-analyst", "evidence-analyst" (agent must actually retrieve the data) → `missing_tool_result`

#### `skill_tearsheet_skill`

**medium** · category: platform · specification: - · no-op baseline score: 0.000

> After calling get_skill_content with slug finance-tearsheet to understand the workflow, call assign_tasks_to_agents with two task_requests using ids valuation-analyst and catalyst-analyst covering that workflow, and add a coordinator note naming both workstreams. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_usage_export_activity({})
- Allowed tools (4): `get_workspace_snapshot`, `get_skill_content`, `assign_tasks_to_agents`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_usage_export_activity` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "valuation analyst", "catalyst analyst", "tearsheet" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-tearsheet"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Tearsheet workflow", "valuation", "investment conclusion" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `assign_tasks_to_agents` must contain "valuation-analyst", "catalyst-analyst" (agent must actually retrieve the data) → `missing_tool_result`

#### `vendor_single`

**easy** · category: platform · specification: - · no-op baseline score: 0.000

> Call assign_tasks_to_agents with one task_request using id triage-analyst for vendor sla monitoring work: Triage the open vendor incident log by severity.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Delegation Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_usage_prompt_audit({})
- Allowed tools (2): `get_workspace_snapshot`, `assign_tasks_to_agents`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_usage_prompt_audit` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `assign_tasks_to_agents` must appear in the trace → `missing_tool_call`
- **Tool result** of `assign_tasks_to_agents` must contain "triage-analyst" (agent must actually retrieve the data) → `missing_tool_result`

### delete (20)

#### `deduplicate_and_fix_latest_news`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> This dashboard has two identical Latest News widgets for NVDA, and the desk actually needs AAPL. Remove exactly one duplicate, update the remaining widget to AAPL, and add a note mentioning AAPL and the word repaired.

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

#### `deduplicate_and_fix_macro_timeseries`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> This dashboard has two identical Macro Timeseries widgets for DGS10, and the desk actually needs DGS2. Remove exactly one duplicate, update the remaining widget to DGS2, and add a note mentioning DGS2 and the word repaired.

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

#### `deduplicate_and_fix_price_performance`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> Remove exactly one duplicate from the two identical Price Performance widgets for AAPL; then update the remaining widget to NVDA and add a note mentioning NVDA and the word repaired.

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

#### `deduplicate_and_fix_vendor_sla_status`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> The dashboard contains two identical Vendor SLA Status widgets for YTD, but the desk actually needs MTD. Remove exactly one duplicate, update the remaining widget to MTD, and add a note mentioning MTD and the word repaired.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Dedup And Fix"; 2 seeded widget(s): vendor_dataset_monitor_slas_vendor_sla_status({"period": "YTD"}), vendor_dataset_monitor_slas_vendor_sla_status({"period": "YTD"})
- Allowed tools (5): `get_workspace_snapshot`, `read_widget`, `delete_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"period": "MTD"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥0× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"period": "YTD"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "MTD", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `remove_duplicate_estimate_history_and_document`

**medium** · category: repair · specification: - · no-op baseline score: 0.000

> Two identical Estimate History widgets are on this dashboard. Remove exactly one duplicate, then add a HTML card saying the duplicate was removed.

- Fixture backends: equities
- Initial workspace: dashboard "Duplicate Repair"; 2 seeded widget(s): estimate_history({"symbol": "AAPL"}), estimate_history({"symbol": "AAPL"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `delete_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated html** ≥1× whose content mentions "duplicate", "removed" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `remove_duplicate_fundamental_metrics_and_document`

**medium** · category: repair · specification: - · no-op baseline score: 0.000

> Remove exactly one duplicate from the two identical Fundamental Metrics widgets, then add a note saying the duplicate was removed.

- Fixture backends: equities
- Initial workspace: dashboard "Duplicate Repair"; 2 seeded widget(s): fundamental_metrics({"symbol": "NVDA"}), fundamental_metrics({"symbol": "NVDA"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `delete_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "duplicate", "removed" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `remove_duplicate_latest_news`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> The dashboard has two identical Latest News widgets. Remove exactly one so a single copy remains; do not change the one that stays.

- Fixture backends: equities
- Initial workspace: dashboard "Duplicate Cleanup"; 2 seeded widget(s): latest_news({"symbol": "MSFT", "limit": 5}), latest_news({"symbol": "MSFT", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "MSFT", "limit": 5} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `remove_duplicate_live_orders_and_document`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> Remove exactly one duplicate from the two identical Live Orders widgets, then add a note saying the duplicate was removed.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Duplicate Repair"; 2 seeded widget(s): execution_desk_blotter_live_orders({"desk": "US Equity"}), execution_desk_blotter_live_orders({"desk": "US Equity"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `delete_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_blotter_live_orders` with data_args ⊇ {"desk": "US Equity"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "duplicate", "removed" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `remove_duplicate_macro_timeseries`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> There are two identical Macro Timeseries widgets on the dashboard. Remove exactly one so a single copy remains; do not change the one that stays.

- Fixture backends: macro
- Initial workspace: dashboard "Duplicate Cleanup"; 2 seeded widget(s): macro_timeseries({"series": "DGS10"}), macro_timeseries({"series": "DGS10"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `remove_duplicate_price_performance`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> There are two identical Price Performance widgets on the dashboard. Remove exactly one so a single copy remains; do not change the one that stays.

- Fixture backends: equities
- Initial workspace: dashboard "Duplicate Cleanup"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), price_performance({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `remove_duplicate_sector_exposure_and_document`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> Remove exactly one duplicate from the two identical Sector Exposure widgets, then add a note saying the duplicate was removed.

- Fixture backends: portfolio
- Initial workspace: dashboard "Duplicate Repair"; 2 seeded widget(s): sector_exposure({}), sector_exposure({})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `delete_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "duplicate", "removed" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `remove_duplicate_vendor_sla_status`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> The dashboard has two identical Vendor SLA Status widgets. Remove exactly one so a single copy remains; do not change the one that stays.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Duplicate Cleanup"; 2 seeded widget(s): vendor_dataset_monitor_slas_vendor_sla_status({"vendor": "FactSet"}), vendor_dataset_monitor_slas_vendor_sla_status({"vendor": "FactSet"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"vendor": "FactSet"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `remove_latest_news`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> This dashboard no longer needs the Latest News widget; remove it.

- Fixture backends: equities
- Initial workspace: dashboard "Removal Task"; 1 seeded widget(s): latest_news({"symbol": "AAPL", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥0× `Bench Equities/latest_news` → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

#### `remove_macro_timeseries`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> The Macro Timeseries widget is no longer needed on this dashboard. Remove it.

- Fixture backends: macro
- Initial workspace: dashboard "Removal Task"; 1 seeded widget(s): macro_timeseries({"series": "DGS2"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥0× `Bench Macro/macro_timeseries` → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

#### `remove_price_performance`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> This dashboard no longer needs the Price Performance widget; remove it.

- Fixture backends: equities
- Initial workspace: dashboard "Removal Task"; 1 seeded widget(s): price_performance({"symbol": "NVDA"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥0× `Bench Equities/price_performance` → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

#### `remove_top_alerts`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> This dashboard no longer needs the Top Alerts widget; remove it.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Removal Task"; 1 seeded widget(s): portfolio_command_center_overview_top_alerts({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥0× `Bench Stark Enterprise/portfolio_command_center_overview_top_alerts` → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

#### `similar_estimate_history_msft`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Remove exactly one duplicate MSFT Estimate History widget from the two identical MSFT copies, while keeping the other duplicate and the NVDA widget untouched.

- Fixture backends: equities
- Initial workspace: dashboard "Similar Cleanup"; 3 seeded widget(s): estimate_history({"symbol": "MSFT"}), estimate_history({"symbol": "MSFT"}), estimate_history({"symbol": "NVDA"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `similar_latest_news_nvda`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Remove exactly one duplicate NVDA Latest News widget from the two identical NVDA copies, while keeping the other duplicate and the AAPL widget untouched.

- Fixture backends: equities
- Initial workspace: dashboard "Similar Cleanup"; 3 seeded widget(s): latest_news({"symbol": "NVDA", "limit": 5}), latest_news({"symbol": "NVDA", "limit": 5}), latest_news({"symbol": "AAPL", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `similar_macro_timeseries_dgs10`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> This dashboard has three Macro Timeseries widgets: two identical ones for DGS10 and one for DGS2. Remove exactly one duplicate DGS10 widget; keep the other and keep the DGS2 widget untouched.

- Fixture backends: macro
- Initial workspace: dashboard "Similar Cleanup"; 3 seeded widget(s): macro_timeseries({"series": "DGS10"}), macro_timeseries({"series": "DGS10"}), macro_timeseries({"series": "DGS2"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS2"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `similar_price_performance_aapl`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> This dashboard has three Price Performance widgets: two identical ones for AAPL and one for MSFT. Remove exactly one duplicate AAPL widget; keep the other and keep the MSFT widget untouched.

- Fixture backends: equities
- Initial workspace: dashboard "Similar Cleanup"; 3 seeded widget(s): price_performance({"symbol": "AAPL"}), price_performance({"symbol": "AAPL"}), price_performance({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `delete_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

### inspect (20)

#### `ambient_repair_and_brief_macro_timeseries`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> After inspecting the dashboard, find the widget with series=DGS2, repair it to DGS10, keep the companion widget, and add a note mentioning the repair.

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

#### `ambient_repair_and_brief_price_performance`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> Keep the companion widget while finding the widget with symbol=MSFT, repairing it to AAPL, and adding a note mentioning the repair after inspecting the dashboard.

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

#### `ambient_repair_and_brief_risk_stats`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> After inspecting the dashboard, find the widget with client=Northstar Endowment, repair it to Atlas Pension, keep the companion widget, and add a HTML card mentioning the repair.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Inspect Full Repair"; 2 seeded widget(s): reporting_factsheet_studio_overview_workflow_overview({}), reporting_factsheet_studio_factsheets_risk_stats({"client": "Northstar Endowment"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/reporting_factsheet_studio_overview_workflow_overview` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/reporting_factsheet_studio_factsheets_risk_stats` with data_args ⊇ {"client": "Atlas Pension"} → `missing_widget`
- **Widget** ≥0× `Bench Stark Enterprise/reporting_factsheet_studio_factsheets_risk_stats` with data_args ⊇ {"client": "Northstar Endowment"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated html** ≥1× whose content mentions "Northstar Endowment", "Atlas Pension", "repair" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `ambient_repair_and_brief_sector_exposure`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> Inspect the dashboard, find the widget with sector=Consumer Staples, repair it to Technology, keep the companion widget, and add a note mentioning the repair.

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

#### `find_and_fix_misconfigured_estimate_history`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use read_widget with widget_id estimate_history to inspect the widget configured with symbol=AAPL, then update_widget so symbol=NVDA.

- Fixture backends: equities
- Initial workspace: dashboard "Inspect Repair"; 1 seeded widget(s): estimate_history({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`

#### `find_and_fix_misconfigured_factor_exposure_table`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use read_widget with widget_id quant_research_backtest_lab_risk_model_factor_exposure_table to inspect the widget configured with universe=Liquid Crypto, then update_widget so universe=US Large Cap.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Inspect Repair"; 1 seeded widget(s): quant_research_backtest_lab_risk_model_factor_exposure_table({"universe": "Liquid Crypto"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/quant_research_backtest_lab_risk_model_factor_exposure_table` with data_args ⊇ {"universe": "US Large Cap"} → `missing_widget`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`

#### `find_and_fix_misconfigured_macro_timeseries`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> After calling read_widget with widget_id macro_timeseries, update the widget configured with series=FEDFUNDS so series=DGS10.

- Fixture backends: macro
- Initial workspace: dashboard "Inspect Repair"; 1 seeded widget(s): macro_timeseries({"series": "FEDFUNDS"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`

#### `find_and_fix_misconfigured_price_performance`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> After calling read_widget with widget_id price_performance, update the widget configured with symbol=MSFT so symbol=AAPL.

- Fixture backends: equities
- Initial workspace: dashboard "Inspect Repair"; 1 seeded widget(s): price_performance({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Tool call** ≥1× `read_widget` must appear in the trace → `missing_tool_call`

#### `find_duplicate_drift_by_sleeve`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Inspect the dashboard, identify the duplicate Drift by Sleeve among the seeded widgets, and remove exactly one duplicate while preserving the Workflow Overview widget.

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

#### `find_duplicate_latest_news`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Preserve the price_performance widget while inspecting the dashboard, identifying the duplicate latest_news among the seeded widgets, and removing exactly one duplicate.

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

#### `find_duplicate_macro_timeseries`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> After inspecting the dashboard, identify the duplicate macro_timeseries among the seeded widgets and remove exactly one duplicate while preserving the yield_curve widget.

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

#### `find_duplicate_risk_metrics`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Preserve the holdings_table widget while inspecting the dashboard, identifying the duplicate risk_metrics among the seeded widgets, and removing exactly one duplicate.

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

#### `inspect_and_repair_overlap_disclosure_checklist`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> Move the overlapping reporting_factsheet_studio_commentary_pm_quote_bank widget to x=24, y=0, w=16, h=10 after inspecting the dashboard and finding it.

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

#### `inspect_and_repair_overlap_holdings_table`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> Inspect the dashboard, find the overlapping sector_exposure widget, and move it to x=24, y=0, w=16, h=10.

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

#### `inspect_and_repair_overlap_macro_timeseries`

**medium** · category: repair · specification: - · no-op baseline score: 0.000

> Find the overlapping yield_curve widget after inspecting the dashboard, and move it to x=24, y=0, w=16, h=10.

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

#### `inspect_and_repair_overlap_price_performance`

**medium** · category: repair · specification: - · no-op baseline score: 0.000

> Inspect the dashboard, find the overlapping latest_news widget, and move it to x=24, y=0, w=16, h=10.

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

#### `inspect_holdings_table`

**easy** · category: read · specification: - · no-op baseline score: 0.000

> After calling read_widget with widget_id holdings_table for the existing Bench Portfolio/holdings_table widget, add a note mentioning holdings.

- Fixture backends: portfolio
- Initial workspace: dashboard "Inspect Board"; 1 seeded widget(s): holdings_table({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "holdings" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `read_widget` with args ⊇ {"widget_id": "holdings_table"} must appear in the trace → `missing_tool_call`

#### `inspect_macro_timeseries`

**easy** · category: read · specification: - · no-op baseline score: 0.000

> Call read_widget with widget_id macro_timeseries for the existing Bench Macro/macro_timeseries widget, then add a note mentioning DGS10.

- Fixture backends: macro
- Initial workspace: dashboard "Inspect Board"; 1 seeded widget(s): macro_timeseries({"series": "DGS10"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "DGS10" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `read_widget` with args ⊇ {"widget_id": "macro_timeseries"} must appear in the trace → `missing_tool_call`

#### `inspect_price_performance`

**easy** · category: read · specification: - · no-op baseline score: 0.000

> After calling read_widget with widget_id price_performance for the existing Bench Equities/price_performance widget, add a note mentioning AAPL.

- Fixture backends: equities
- Initial workspace: dashboard "Inspect Board"; 1 seeded widget(s): price_performance({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "AAPL" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `read_widget` with args ⊇ {"widget_id": "price_performance"} must appear in the trace → `missing_tool_call`

#### `inspect_workflow_overview`

**easy** · category: read · specification: - · no-op baseline score: 0.000

> Call read_widget with widget_id portfolio_command_center_overview_workflow_overview for the existing Bench Stark Enterprise/portfolio_command_center_overview_workflow_overview widget, then add a note mentioning stark.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Inspect Board"; 2 seeded widget(s): portfolio_command_center_overview_workflow_overview({}), vendor_dataset_monitor_slas_freshness_exceptions({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_slas_freshness_exceptions` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "stark" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `read_widget` with args ⊇ {"widget_id": "portfolio_command_center_overview_workflow_overview"} must appear in the trace → `missing_tool_call`

### layout (20)

#### `arrange_split_macro`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Set the macro widgets side by side with the 10Y series on the left half and the yield curve on the right half; both should be 10 rows tall starting at row 0.

- Fixture backends: macro
- Initial workspace: dashboard "Arrangement Task"; 2 seeded widget(s): macro_timeseries({"series": "DGS10"}), yield_curve({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `macro_timeseries` must sit at exactly x=0, y=0, w=20, h=10 → `layout_mismatch`
- **Layout** `yield_curve` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `arrange_split_portfolio`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Arrange the portfolio widgets: holdings on the left with width 24 and sector exposure to its right with width 16, both 12 rows tall starting at row 0.

- Fixture backends: portfolio
- Initial workspace: dashboard "Arrangement Task"; 2 seeded widget(s): holdings_table({}), sector_exposure({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `holdings_table` must sit at exactly x=0, y=0, w=24, h=12 → `layout_mismatch`
- **Layout** `sector_exposure` must sit at exactly x=24, y=0, w=16, h=12 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `arrange_split_price_news_aapl`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Place the AAPL price widget on the left half and the AAPL news widget on the right half, side by side, both 12 rows tall starting at row 0.

- Fixture backends: equities
- Initial workspace: dashboard "Arrangement Task"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), latest_news({"symbol": "AAPL", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `price_performance` must sit at exactly x=0, y=0, w=20, h=12 → `layout_mismatch`
- **Layout** `latest_news` must sit at exactly x=20, y=0, w=20, h=12 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `arrange_stack_price_news_nvda`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Arrange the NVDA widgets full-width with price on top (rows 0-12, 40 columns) and news below it (10 rows tall starting at row 12, 40 columns).

- Fixture backends: equities
- Initial workspace: dashboard "Arrangement Task"; 2 seeded widget(s): price_performance({"symbol": "NVDA"}), latest_news({"symbol": "NVDA", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `price_performance` must sit at exactly x=0, y=0, w=40, h=12 → `layout_mismatch`
- **Layout** `latest_news` must sit at exactly x=0, y=12, w=40, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `equity_three_widget_grid`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> Arrange the three AAPL widgets into a grid: price at columns 0-20 rows 0-12, news at columns 20-40 rows 0-12, and estimates full-width below them (40 columns, 8 rows, starting at row 12).

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

#### `halve_price_msft`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Resize the MSFT price widget to half width (20 columns). Keep its position.

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

#### `macro_three_widget_grid`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> Arrange the three macro widgets into a grid: the 2Y series at columns 0-20 rows 0-10, the 10Y series at columns 20-40 rows 0-10, and the yield curve full-width below them (40 columns, 10 rows, starting at row 10).

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

#### `mixed_equity_three_widget_grid`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> Arrange the three MSFT widgets: price full-width on top (40 columns, 10 rows), then estimates at columns 0-20 and fundamentals at columns 20-40, both 10 rows starting at row 10.

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

#### `move_news_right`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Keep the AAPL news widget's size and move it to start at column 20.

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

#### `portfolio_three_widget_grid`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> Arrange the three portfolio widgets into a grid: holdings at columns 0-24 rows 0-12, sector exposure at columns 24-40 rows 0-12, and risk metrics full-width below them (40 columns, 8 rows, starting at row 12).

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

#### `preserve_estimates_fundamentals_msft`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Do not move the estimates widget; move the MSFT fundamentals widget beside it so it starts at column 24, row 0, keeping its size.

- Fixture backends: equities
- Initial workspace: dashboard "Preserve Layout Task"; 2 seeded widget(s): estimate_history({"symbol": "MSFT"}), fundamental_metrics({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `estimate_history` must sit at exactly x=0, y=0, w=24, h=12 → `layout_mismatch`
- **Layout** `fundamental_metrics` must sit at exactly x=24, y=0, w=16, h=8 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `preserve_macro_pair`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Move the yield curve widget beside the 10Y series widget: it should start at column 20, row 0, keeping its size. Do not move the series widget.

- Fixture backends: macro
- Initial workspace: dashboard "Preserve Layout Task"; 2 seeded widget(s): macro_timeseries({"series": "DGS10"}), yield_curve({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `macro_timeseries` must sit at exactly x=0, y=0, w=20, h=10 → `layout_mismatch`
- **Layout** `yield_curve` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `preserve_portfolio_pair`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Move the sector exposure widget beside the holdings widget: it should start at column 24, row 0, keeping its size. Do not move the holdings widget.

- Fixture backends: portfolio
- Initial workspace: dashboard "Preserve Layout Task"; 2 seeded widget(s): holdings_table({}), sector_exposure({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `holdings_table` must sit at exactly x=0, y=0, w=24, h=12 → `layout_mismatch`
- **Layout** `sector_exposure` must sit at exactly x=24, y=0, w=16, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `preserve_price_news_aapl`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Keeping its size, move the AAPL news widget up beside the price widget at column 20, row 0. Do not move the price widget.

- Fixture backends: equities
- Initial workspace: dashboard "Preserve Layout Task"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), latest_news({"symbol": "AAPL", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `price_performance` must sit at exactly x=0, y=0, w=20, h=12 → `layout_mismatch`
- **Layout** `latest_news` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `repair_aapl_price_news_overlap`

**medium** · category: repair · specification: - · no-op baseline score: 0.000

> The AAPL news widget overlaps the price widget. Move the news widget to start at column 20 with its current size. Do not move the price widget.

- Fixture backends: equities
- Initial workspace: dashboard "Overlap Repair"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), latest_news({"symbol": "AAPL", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `price_performance` must sit at exactly x=0, y=0, w=20, h=12 → `layout_mismatch`
- **Layout** `latest_news` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `repair_macro_overlap`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> Do not move the 10Y series widget; resolve the overlap by moving the yield curve widget to start at column 20 with its current size.

- Fixture backends: macro
- Initial workspace: dashboard "Overlap Repair"; 2 seeded widget(s): macro_timeseries({"series": "DGS10"}), yield_curve({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `macro_timeseries` must sit at exactly x=0, y=0, w=20, h=10 → `layout_mismatch`
- **Layout** `yield_curve` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `repair_msft_estimates_overlap`

**medium** · category: repair · specification: - · no-op baseline score: 0.000

> The MSFT fundamentals widget overlaps the estimates widget. Move the fundamentals widget to start at column 24 with its current size. Do not move the estimates widget.

- Fixture backends: equities
- Initial workspace: dashboard "Overlap Repair"; 2 seeded widget(s): estimate_history({"symbol": "MSFT"}), fundamental_metrics({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `estimate_history` must sit at exactly x=0, y=0, w=24, h=12 → `layout_mismatch`
- **Layout** `fundamental_metrics` must sit at exactly x=24, y=0, w=16, h=8 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `repair_portfolio_overlap`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> The sector exposure widget overlaps the holdings widget. Move the sector exposure widget to start at column 24 with its current size. Do not move the holdings widget.

- Fixture backends: portfolio
- Initial workspace: dashboard "Overlap Repair"; 2 seeded widget(s): holdings_table({}), sector_exposure({})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget_layout`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Layout** `holdings_table` must sit at exactly x=0, y=0, w=24, h=12 → `layout_mismatch`
- **Layout** `sector_exposure` must sit at exactly x=24, y=0, w=16, h=10 → `layout_mismatch`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `shorten_estimates_nvda`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Keep the NVDA estimates widget's position and width, but reduce its height to 8 rows.

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

#### `widen_fundamentals_aapl`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Widen the AAPL fundamentals widget to 20 columns. Keep its position and height.

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

### navigate (20)

#### `addtab_curve`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> Add the missing Curve tab to this dashboard and put the Yield Curve widget on it. Keep the existing Overview tab intact.

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

#### `addtab_estimates_msft`

**medium** · category: repair · specification: - · no-op baseline score: 0.000

> Keep the existing Overview tab intact while adding a tab named Estimates and placing the Estimate History widget for MSFT on it.

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

#### `addtab_fundamentals_aapl`

**medium** · category: repair · specification: - · no-op baseline score: 0.000

> This dashboard is missing its Fundamentals tab. Add a tab named Fundamentals and put the Fundamental Metrics widget for AAPL on it. Keep the existing Overview tab intact.

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

#### `addtab_risk`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> This dashboard is missing its Risk tab. Add a tab named Risk and put the Risk Metrics widget on it. Keep the existing Overview tab intact.

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

#### `expand_client_expansion`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Set the active dashboard name to Client Command Center, add a new tab named Open Requests, and add a HTML card on the new tab that mentions open requests and says items are pending.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Client Board"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_sign_off_sign_off_tracker({})
- Allowed tools (5): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Command Center" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `open-requests` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_sign_off_sign_off_tracker` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated html** ≥1× whose content mentions "open requests", "pending" on tab `open-requests` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "add_tabs"} must appear in the trace → `missing_tool_call`

#### `expand_research_expansion`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Rename the active dashboard to Research Command Center, add a new tab named Draft Reviews, and add a HTML card on the new tab that mentions draft reviews and says items are pending.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Research Board"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_stress_tests_historical_shocks({})
- Allowed tools (5): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Research Command Center" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `draft-reviews` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_stress_tests_historical_shocks` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated html** ≥1× whose content mentions "draft reviews", "pending" on tab `draft-reviews` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "add_tabs"} must appear in the trace → `missing_tool_call`

#### `expand_risk_expansion`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Change the active dashboard's name to Risk Command Center; add a new tab named Stress Results; then add a HTML card on the new tab that mentions stress results and says items are pending.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Risk Board"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_stress_tests_risk_snapshot({})
- Allowed tools (5): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Risk Command Center" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `stress-results` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_stress_tests_risk_snapshot` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated html** ≥1× whose content mentions "stress results", "pending" on tab `stress-results` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "add_tabs"} must appear in the trace → `missing_tool_call`

#### `expand_vendor_expansion`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Set the active dashboard name to Vendor Control Center, add a new tab named Incident Log, and add a note on the new tab that mentions incident log and says items are pending.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Vendor Board"; 1 tab(s): overview; 1 seeded widget(s): stress_liquidity_lab_stress_tests_scenario_loss_waterfall({})
- Allowed tools (5): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vendor Control Center" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `incident-log` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_stress_tests_scenario_loss_waterfall` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "incident log", "pending" on tab `incident-log` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "add_tabs"} must appear in the trace → `missing_tool_call`

#### `hub_book_hub`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Set the active dashboard name to Book Hub, add a new tab named Exposure, put the Sector Exposure widget on it, and add a note on the same tab mentioning exposure and book hub.

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

#### `hub_desk_hub`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Rename the active dashboard to Desk Hub, add a new tab named News, put the Latest News widget for NVDA on it, and add a note on the same tab mentioning news and desk hub.

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

#### `hub_earnings_hub`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Set the active dashboard name to Earnings Hub, add a new tab named Estimates, put the Estimate History widget for AAPL on it, and add a note on the same tab mentioning estimates and earnings hub.

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

#### `hub_rates_hub`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Set the active dashboard name to Rates Hub, add a new tab named Curve, put the Yield Curve widget on it, and add a note on the same tab mentioning curve and rates hub.

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

#### `rename_both_client_review`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Change the active dashboard's name to Client Review Agenda; also rename the Overview tab to Talking Points.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Client Prep"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_ai_access_app_usage({})
- Allowed tools (4): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Client Review Agenda" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_ai_access_app_usage` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "Client Review Agenda"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "rename_tabs"} must appear in the trace → `missing_tool_call`

#### `rename_both_earnings_week`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Rename the active dashboard to Earnings Week Planner and rename the Overview tab to Calendar.

- Fixture backends: equities
- Initial workspace: dashboard "Earnings Board"; 1 tab(s): overview
- Allowed tools (4): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Earnings Week Planner" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "Earnings Week Planner"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "rename_tabs"} must appear in the trace → `missing_tool_call`

#### `rename_both_ops_close`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Change the active dashboard's name to Fund Close Control; also rename the Overview tab to Close Checklist.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Ops Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_ai_access_copilot_visibility_flags({})
- Allowed tools (4): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Fund Close Control" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_ai_access_copilot_visibility_flags` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "Fund Close Control"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "rename_tabs"} must appear in the trace → `missing_tool_call`

#### `rename_both_pm_morning`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Set the active dashboard name to PM Morning Review and rename the Overview tab to Holdings View.

- Fixture backends: portfolio
- Initial workspace: dashboard "PM Board"; 1 tab(s): overview
- Allowed tools (4): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "PM Morning Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "PM Morning Review"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `manage_navigation_bar` with args ⊇ {"operation": "rename_tabs"} must appear in the trace → `missing_tool_call`

#### `rename_compliance_day`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Set the active dashboard name to Daily Compliance Control.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Alert Triage"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_ai_access_prompt_audit({})
- Allowed tools (2): `get_workspace_snapshot`, `manage_dashboard`
- Turn budget: 4 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Daily Compliance Control" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_ai_access_prompt_audit` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "Daily Compliance Control"} must appear in the trace → `missing_tool_call`

#### `rename_equity_desk`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Set the active dashboard name to Equity Desk Monitor.

- Fixture backends: equities
- Initial workspace: dashboard "Desk View"; 1 tab(s): overview
- Allowed tools (2): `get_workspace_snapshot`, `manage_dashboard`
- Turn budget: 4 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Equity Desk Monitor" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "Equity Desk Monitor"} must appear in the trace → `missing_tool_call`

#### `rename_execution_open`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Set the active dashboard name to Execution Morning Board.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Desk Board"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_data_health_failed_jobs_trend({})
- Allowed tools (2): `get_workspace_snapshot`, `manage_dashboard`
- Turn budget: 4 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Execution Morning Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_data_health_failed_jobs_trend` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "Execution Morning Board"} must appear in the trace → `missing_tool_call`

#### `rename_macro_watch`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Rename the active dashboard to Rates Watch.

- Fixture backends: macro
- Initial workspace: dashboard "Macro Board"; 1 tab(s): overview
- Allowed tools (2): `get_workspace_snapshot`, `manage_dashboard`
- Turn budget: 4 · oracle reference trace: 1 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Rates Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_dashboard` with args ⊇ {"operation": "update", "name": "Rates Watch"} must appear in the trace → `missing_tool_call`

### note (20)

#### `crossbackend_aapl_vs_rates`

**hard** · category: read · specification: - · no-op baseline score: 0.000

> Add a note with the latest close and the latest 10Y value from the data after reviewing the AAPL price and 10Y Treasury widgets.

- Fixture backends: equities, macro
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), macro_timeseries({"series": "DGS10"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "AAPL", "196.10", "4.16" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `crossbackend_book_vs_fed`

**hard** · category: read · specification: - · no-op baseline score: 0.000

> Add a note with the portfolio beta and the latest FEDFUNDS value from the data after reviewing the risk metrics and Fed Funds widgets.

- Fixture backends: macro, portfolio
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): risk_metrics({}), macro_timeseries({"series": "FEDFUNDS"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "FEDFUNDS"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "1.18", "4.12" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `crossbackend_exposure_cpi`

**hard** · category: read · specification: - · no-op baseline score: 0.000

> Review the sector exposure and CPI widgets and add a note with the largest sector weight and the latest CPI value from the data.

- Fixture backends: macro, portfolio
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): sector_exposure({}), macro_timeseries({"series": "CPIAUCSL"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "CPIAUCSL"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "Technology", "0.86", "322.4" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `crossbackend_msft_vs_curve`

**hard** · category: read · specification: - · no-op baseline score: 0.000

> Review the MSFT fundamentals and yield curve widgets and add a note with the gross margin and the 30Y yield from the data.

- Fixture backends: equities, macro
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): fundamental_metrics({"symbol": "MSFT"}), yield_curve({})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/yield_curve` → `missing_widget`
- **Generated note** ≥1× whose content mentions "MSFT", "0.694", "4.48" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `fact_close_aapl`

**easy** · category: read · specification: - · no-op baseline score: 0.000

> Review the existing AAPL price widget and add a note with the latest close from the data.

- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): price_performance({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "AAPL", "196.10" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `fact_close_msft`

**easy** · category: read · specification: - · no-op baseline score: 0.000

> Add a note with the latest close from the data after reviewing the existing MSFT price widget.

- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): price_performance({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "MSFT", "451.25" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `fact_macro_10y`

**medium** · category: read · specification: - · no-op baseline score: 0.000

> Add a note with the series id and its latest value from the data after reviewing the existing 10Y series widget.

- Fixture backends: macro
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): macro_timeseries({"series": "DGS10"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "DGS10", "4.16" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `fact_top_holding`

**medium** · category: read · specification: - · no-op baseline score: 0.000

> Use the existing holdings widget data to add a note naming the largest position and its exact weight from the data.

- Fixture backends: portfolio
- Initial workspace: dashboard "Existing Review"; 1 seeded widget(s): holdings_table({})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`
- **Generated note** ≥1× whose content mentions "MSFT", "0.34" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `handover`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Add a note named Desk Handover saying the EU book is flat and the US open checklist is complete.

- Fixture backends: equities
- Initial workspace: dashboard "Notes Board"
- Allowed tools (2): `get_workspace_snapshot`, `add_generative_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Desk Handover" whose content mentions "EU book", "checklist" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `outage`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> On the dashboard, add a HTML card named Vendor Outage stating that the FactSet feed is degraded and fallback pricing is active.

- Fixture backends: equities
- Initial workspace: dashboard "Notes Board"
- Allowed tools (2): `get_workspace_snapshot`, `add_generative_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Vendor Outage" whose content mentions "FactSet", "fallback" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `reminder`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> On the dashboard, add a note named Compliance Reminder stating that attestations are due Friday and trading in restricted names is blocked.

- Fixture backends: equities
- Initial workspace: dashboard "Notes Board"
- Allowed tools (2): `get_workspace_snapshot`, `add_generative_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Compliance Reminder" whose content mentions "attestations", "restricted" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `standup`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> On the dashboard, add a note named Morning Standup stating that the desk meeting moved to 9am and the risk review is at noon.

- Fixture backends: equities
- Initial workspace: dashboard "Notes Board"
- Allowed tools (2): `get_workspace_snapshot`, `add_generative_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Morning Standup" whose content mentions "9am", "noon" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `synthesis_aapl_msft_closes`

**medium** · category: read · specification: - · no-op baseline score: 0.000

> Compare the existing AAPL and MSFT price widgets and add a note with each latest close from the data.

- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), price_performance({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "AAPL", "196.10", "MSFT", "451.25" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `synthesis_fed_vs_10y`

**hard** · category: read · specification: - · no-op baseline score: 0.000

> Add a note with both latest values from the data after reviewing the Fed Funds and 10Y Treasury widgets.

- Fixture backends: macro
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): macro_timeseries({"series": "FEDFUNDS"}), macro_timeseries({"series": "DGS10"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "FEDFUNDS"} → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "FEDFUNDS", "4.12", "DGS10", "4.16" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `synthesis_holdings_beta`

**hard** · category: read · specification: - · no-op baseline score: 0.000

> Use the holdings and risk metrics widget data to add a note with the largest position weight and the portfolio beta from the data.

- Fixture backends: portfolio
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): holdings_table({}), risk_metrics({})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Generated note** ≥1× whose content mentions "MSFT", "0.34", "1.18" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `synthesis_nvda_close_eps`

**medium** · category: read · specification: - · no-op baseline score: 0.000

> Add a note with the latest close and the 2026Q1 EPS estimate from the data after reviewing the NVDA price and estimates widgets.

- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 2 seeded widget(s): price_performance({"symbol": "NVDA"}), estimate_history({"symbol": "NVDA"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "NVDA", "179.45", "1.18" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `twofacts_estimates_aapl`

**medium** · category: read · specification: - · no-op baseline score: 0.000

> Add a HTML card on the overview tab with the 2026Q1 EPS estimate and the revenue estimate from the data after reviewing the existing AAPL estimates widget.

- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 tab(s): overview; 1 seeded widget(s): estimate_history({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "AAPL"} on tab `overview` → `missing_widget`
- **Generated html** ≥1× whose content mentions "AAPL", "2.31", "94.8" on tab `overview` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `twofacts_estimates_msft`

**medium** · category: read · specification: - · no-op baseline score: 0.000

> Add a note on the overview tab with the 2026Q1 EPS estimate and the revenue estimate from the data after reviewing the existing MSFT estimates widget.

- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 tab(s): overview; 1 seeded widget(s): estimate_history({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "MSFT"} on tab `overview` → `missing_widget`
- **Generated note** ≥1× whose content mentions "MSFT", "3.42", "71.2" on tab `overview` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `twofacts_fundamentals_aapl`

**medium** · category: read · specification: - · no-op baseline score: 0.000

> Use the existing AAPL fundamentals widget data to add a note on the overview tab with the gross margin and the net cash from the data.

- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 tab(s): overview; 1 seeded widget(s): fundamental_metrics({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "AAPL"} on tab `overview` → `missing_widget`
- **Generated note** ≥1× whose content mentions "AAPL", "0.462", "54.0" on tab `overview` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `twofacts_fundamentals_nvda`

**medium** · category: read · specification: - · no-op baseline score: 0.000

> Add a note on the overview tab with the gross margin and the buyback yield from the data after reviewing the existing NVDA fundamentals widget.

- Fixture backends: equities
- Initial workspace: dashboard "Existing Review"; 1 tab(s): overview; 1 seeded widget(s): fundamental_metrics({"symbol": "NVDA"})
- Allowed tools (3): `get_workspace_snapshot`, `get_widget_data`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "NVDA"} on tab `overview` → `missing_widget`
- **Generated note** ≥1× whose content mentions "NVDA", "0.742", "0.004" on tab `overview` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### params (20)

#### `cross_aapl_macro`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Build a dashboard with these two widgets after using parameter options for both: Bench Equities/price_performance symbol=AAPL; Bench Macro/macro_timeseries series=DGS10. Add a note mentioning AAPL and DGS10.

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

#### `cross_nvda_rates`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Build a dashboard with these two widgets after using parameter options for both: Bench Equities/estimate_history symbol=NVDA; Bench Macro/macro_timeseries series=FEDFUNDS. Add a note mentioning NVDA and FEDFUNDS.

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

#### `cross_portfolio_sector`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Build a two-widget dashboard using parameter options for both widgets: Bench Portfolio/sector_exposure sector=Technology; Bench Macro/macro_timeseries series=CPIAUCSL. Add a note mentioning Technology and CPIAUCSL.

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

#### `cross_stark_crypto`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Build a dashboard with these two widgets after using parameter options for both: Bench Stark Enterprise/crypto_research_dashboard_derivatives_liquidation_heatmap crypto_asset=ETH; Bench Portfolio/risk_metrics sector=Consumer Staples. Add a note mentioning ETH and options.

- Fixture backends: portfolio, stark-enterprise
- Initial workspace: dashboard "Cross Options"; 1 seeded widget(s): stress_liquidity_lab_scenarios_portfolio_impact({})
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/crypto_research_dashboard_derivatives_liquidation_heatmap` with data_args ⊇ {"crypto_asset": "ETH"} → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/risk_metrics` with data_args ⊇ {"sector": "Consumer Staples"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_scenarios_portfolio_impact` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "ETH", "options" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "crypto_research_dashboard_derivatives_liquidation_heatmap", "param_name": "crypto_asset"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "risk_metrics", "param_name": "sector"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `discover_schema_then_options_for_exposure_summary`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Discover the catalog and schema for Bench Stark Enterprise/client_360_portfolio_view_exposure_summary, call get_params_options for client, then create it with client=Northstar Endowment.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Parameter Options"; 1 seeded widget(s): stress_liquidity_lab_scenarios_position_impact_table({})
- Allowed tools (5): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/client_360_portfolio_view_exposure_summary` with data_args ⊇ {"client": "Northstar Endowment"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/stress_liquidity_lab_scenarios_position_impact_table` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "client_360_portfolio_view_exposure_summary", "param_name": "client"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_params_options` must contain "Northstar Endowment" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `discover_schema_then_options_for_macro_timeseries`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Discover the catalog and schema for Bench Macro/macro_timeseries, call get_params_options for series, then create it with series=DGS10.

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

#### `discover_schema_then_options_for_price_performance`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> For Bench Equities/price_performance, discover the catalog and schema, call get_params_options for symbol, then create it with symbol=AAPL.

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

#### `discover_schema_then_options_for_sector_exposure`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Before creating Bench Portfolio/sector_exposure with sector=Technology, discover the catalog and schema and call get_params_options for sector.

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

#### `options_constrained_pair_for_evidence_and_sign_off_history`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> After using get_params_options for Bench Stark Enterprise/corporate_access_meeting_notes_claims_evidence_and_sign_off_history sector=Technology, add companion widget corporate_access_meeting_notes_claims_management_claims_tracker and arrange both without overlap.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Parameter Pair"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`
- Turn budget: 13 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/corporate_access_meeting_notes_claims_evidence_and_sign_off_history` with data_args ⊇ {"sector": "Technology"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/corporate_access_meeting_notes_claims_management_claims_tracker` → `missing_widget`
- **Layout** `corporate_access_meeting_notes_claims_evidence_and_sign_off_history` must sit at exactly x=0, y=0, w=20, h=10 → `layout_mismatch`
- **Layout** `corporate_access_meeting_notes_claims_management_claims_tracker` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Tool result** of `get_params_options` must contain "Technology" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `options_constrained_pair_for_macro_timeseries`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Set Bench Macro/macro_timeseries series=DGS2 using get_params_options, then add companion widget yield_curve. Arrange both without overlap.

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

#### `options_constrained_pair_for_price_performance`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Set Bench Equities/price_performance symbol=AAPL using get_params_options, then add companion widget latest_news. Arrange both without overlap.

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

#### `options_constrained_pair_for_sector_exposure`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> After using get_params_options for Bench Portfolio/sector_exposure sector=Technology, add companion widget risk_metrics and arrange both without overlap.

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

#### `options_constrained_placement_for_access_and_export_logs`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Create Bench Stark Enterprise/compliance_surveillance_hub_audit_access_and_export_logs after fetching the widget schema and using get_params_options to choose Medium for severity, then place it at x=20, y=0, width 20, height 10.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Parameter Placement"
- Allowed tools (6): `get_workspace_snapshot`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `create_widget`, `update_widget_layout`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/compliance_surveillance_hub_audit_access_and_export_logs` with data_args ⊇ {"severity": "Medium"} → `missing_widget`
- **Layout** `compliance_surveillance_hub_audit_access_and_export_logs` must sit at exactly x=20, y=0, w=20, h=10 → `layout_mismatch`
- **Tool result** of `get_params_options` must contain "Medium" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `options_constrained_placement_for_macro_timeseries`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Use get_params_options to choose DGS10 for series, fetch the widget schema, create Bench Macro/macro_timeseries, and place it at x=20, y=0, width 20, height 10.

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

#### `options_constrained_placement_for_price_performance`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Choose AAPL for symbol with get_params_options, fetch the widget schema, create Bench Equities/price_performance, and place it at x=0, y=0, width 20, height 10.

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

#### `options_constrained_placement_for_sector_exposure`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Use get_params_options to choose Technology for sector, fetch the widget schema, create Bench Portfolio/sector_exposure, and place it at x=0, y=0, width 20, height 10.

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

#### `use_client_options_for_relationship_metrics`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_params_options for Bench Stark Enterprise/client_360_meeting_prep_relationship_metrics parameter client, choose Northstar Endowment, and create that widget with client=Northstar Endowment.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Parameter Options"; 1 seeded widget(s): workspace_data_control_center_usage_export_review_queue({})
- Allowed tools (3): `get_workspace_snapshot`, `get_params_options`, `create_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/client_360_meeting_prep_relationship_metrics` with data_args ⊇ {"client": "Northstar Endowment"} → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_usage_export_review_queue` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "client_360_meeting_prep_relationship_metrics", "param_name": "client"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_params_options` must contain "Northstar Endowment" (agent must actually retrieve the data) → `missing_tool_result`

#### `use_sector_options_for_sector_exposure`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Call get_params_options for Bench Portfolio/sector_exposure parameter sector, choose Technology, and create that widget with sector=Technology.

- Fixture backends: portfolio
- Initial workspace: dashboard "Parameter Options"
- Allowed tools (3): `get_workspace_snapshot`, `get_params_options`, `create_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` with data_args ⊇ {"sector": "Technology"} → `missing_widget`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "sector_exposure", "param_name": "sector"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_params_options` must contain "Technology" (agent must actually retrieve the data) → `missing_tool_result`

#### `use_series_options_for_macro_timeseries`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> For Bench Macro/macro_timeseries, call get_params_options on parameter series, choose DGS10, and create that widget with series=DGS10.

- Fixture backends: macro
- Initial workspace: dashboard "Parameter Options"
- Allowed tools (3): `get_workspace_snapshot`, `get_params_options`, `create_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "macro_timeseries", "param_name": "series"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_params_options` must contain "DGS10" (agent must actually retrieve the data) → `missing_tool_result`

#### `use_symbol_options_for_price_performance`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> For Bench Equities/price_performance, call get_params_options on parameter symbol, choose AAPL, and create that widget with symbol=AAPL.

- Fixture backends: equities
- Initial workspace: dashboard "Parameter Options"
- Allowed tools (3): `get_workspace_snapshot`, `get_params_options`, `create_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Tool call** ≥1× `get_params_options` with args ⊇ {"widget_id": "price_performance", "param_name": "symbol"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_params_options` must contain "AAPL" (agent must actually retrieve the data) → `missing_tool_result`

### prompts (20)

#### `cross_prompt_cross_aapl_rates`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Get workspace_tool_usage and workspace_session_context, create Prompt Cross AAPL Rates, build the cross-backend dashboard with Bench Equities/price_performance with data_args {"symbol": "AAPL"} and Bench Macro/macro_timeseries with data_args {"series": "DGS10"}, and add a note mentioning AAPL and DGS10 and current-dashboard.

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

#### `cross_prompt_cross_book_cpi`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Get workspace_tool_usage and workspace_session_context, create Prompt Cross Book CPI, build the cross-backend dashboard with Bench Portfolio/sector_exposure and Bench Macro/macro_timeseries with data_args {"series": "CPIAUCSL"}, and add a HTML card mentioning sector and CPIAUCSL and current-dashboard.

- Fixture backends: macro, portfolio
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (6): `get_workspace_prompt`, `manage_dashboard`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Prompt Cross Book CPI" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "CPIAUCSL"} → `missing_widget`
- **Generated html** ≥1× whose content mentions "sector", "CPIAUCSL", "current-dashboard" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_tool_usage"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_session_context"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `cross_prompt_cross_nvda_holdings`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Get workspace_tool_usage and workspace_session_context, create Prompt Cross NVDA Holdings, build the cross-backend dashboard with Bench Equities/estimate_history with data_args {"symbol": "NVDA"} and Bench Portfolio/holdings_table, and add a note mentioning NVDA and holdings and current-dashboard.

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

#### `cross_prompt_cross_stark_risk`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Fetch workspace_tool_usage and workspace_session_context, create Prompt Cross Stark Risk, build the cross-backend dashboard with Bench Stark Enterprise/portfolio_command_center_actions_analyst_conviction and Bench Portfolio/risk_metrics, and add a HTML card mentioning stark and risk and current-dashboard.

- Fixture backends: portfolio, stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (6): `get_workspace_prompt`, `manage_dashboard`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 12 · oracle reference trace: 10 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Prompt Cross Stark Risk" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_actions_analyst_conviction` → `missing_widget`
- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Generated html** ≥1× whose content mentions "stark", "risk", "current-dashboard" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_tool_usage"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_session_context"} must appear in the trace → `missing_tool_call`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `dashboard_aapl_prompt_dashboard`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Get workspace_tool_usage, create dashboard AAPL Prompt Dashboard, add Bench Equities/price_performance with data_args {"symbol": "AAPL"} and Bench Equities/latest_news with data_args {"limit": 5, "symbol": "AAPL"} with schema-first discipline, and add a note mentioning AAPL and schema.

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

#### `dashboard_macro_prompt_dashboard`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> After fetching workspace_tool_usage, create dashboard Macro Prompt Dashboard, add Bench Macro/macro_timeseries with data_args {"series": "DGS2"} and Bench Macro/yield_curve with schema-first discipline, and add a note mentioning DGS2 and schema.

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

#### `dashboard_portfolio_prompt_dashboard`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> After fetching workspace_tool_usage, create dashboard Portfolio Prompt Dashboard, add Bench Portfolio/holdings_table and Bench Portfolio/risk_metrics with schema-first discipline, and add a note mentioning holdings and schema.

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

#### `dashboard_stark_prompt_dashboard`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Get workspace_tool_usage, create dashboard Stark Prompt Dashboard, add Bench Stark Enterprise/mnpi_research_review_research_draft_research_review and Bench Stark Enterprise/mnpi_research_review_research_evidence_and_sign_off_history with schema-first discipline, and add a note mentioning stark and schema.

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

#### `follow_tool_usage_prompt_for_healthcare_thesis_note`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Use get_workspace_prompt with name workspace_tool_usage, then follow it by discovering schema before creating Bench Stark Enterprise/healthcare_research_dashboard_documents_healthcare_thesis_note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Prompt Build"; 1 seeded widget(s): vendor_dataset_monitor_overview_workflow_overview({})
- Allowed tools (5): `get_workspace_snapshot`, `get_workspace_prompt`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/healthcare_research_dashboard_documents_healthcare_thesis_note` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_overview_workflow_overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `follow_tool_usage_prompt_for_macro_timeseries`

**easy** · category: dashboard · specification: - · no-op baseline score: 0.000

> Before creating Bench Macro/macro_timeseries with data_args {"series": "DGS10"}, call get_workspace_prompt with name workspace_tool_usage and follow it by discovering schema.

- Fixture backends: macro
- Initial workspace: dashboard "Prompt Build"
- Allowed tools (5): `get_workspace_snapshot`, `get_workspace_prompt`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `follow_tool_usage_prompt_for_price_performance`

**easy** · category: dashboard · specification: - · no-op baseline score: 0.000

> Call get_workspace_prompt with name workspace_tool_usage, then follow it by discovering schema before creating Bench Equities/price_performance with data_args {"symbol": "AAPL"}.

- Fixture backends: equities
- Initial workspace: dashboard "Prompt Build"
- Allowed tools (5): `get_workspace_snapshot`, `get_workspace_prompt`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `follow_tool_usage_prompt_for_risk_metrics`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Use get_workspace_prompt with name workspace_tool_usage, then follow it by discovering schema before creating Bench Portfolio/risk_metrics.

- Fixture backends: portfolio
- Initial workspace: dashboard "Prompt Build"
- Allowed tools (5): `get_workspace_snapshot`, `get_workspace_prompt`, `list_available_widgets`, `get_widget_schema`, `create_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `session_context_grounding_note`

**easy** · category: read · specification: - · no-op baseline score: 0.000

> Call get_workspace_prompt with name workspace_session_context and add a note mentioning current-dashboard current-tab session grounding.

- Fixture backends: equities, portfolio
- Initial workspace: dashboard "Prompt Review"; 1 seeded widget(s): holdings_table({})
- Allowed tools (3): `get_workspace_snapshot`, `get_workspace_prompt`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "current-dashboard" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_session_context"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_workspace_prompt` must contain "current-dashboard current-tab session grounding" (agent must actually retrieve the data) → `missing_tool_result`

#### `session_context_grounding_review`

**easy** · category: read · specification: - · no-op baseline score: 0.000

> After calling get_workspace_prompt with name workspace_session_context, add a note mentioning current-dashboard current-tab session grounding.

- Fixture backends: equities, portfolio
- Initial workspace: dashboard "Prompt Review"; 1 seeded widget(s): sector_exposure({})
- Allowed tools (3): `get_workspace_snapshot`, `get_workspace_prompt`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "current-dashboard" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_session_context"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_workspace_prompt` must contain "current-dashboard current-tab session grounding" (agent must actually retrieve the data) → `missing_tool_result`

#### `session_prompt_ops_slippage`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Fetch workspace_session_context, add a Ops tab, navigate to it, fetch the widget schema, create Bench Stark Enterprise/liquidity_tca_workbench_tca_slippage_by_algo there, and add a HTML card mentioning Ops on that tab.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Prompt Session"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_entitlements_copilot_visibility_flags({})
- Allowed tools (7): `get_workspace_prompt`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 10 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `ops` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/liquidity_tca_workbench_tca_slippage_by_algo` on tab `ops` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_entitlements_copilot_visibility_flags` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated html** ≥1× whose content mentions "Ops" on tab `ops` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool result** of `get_workspace_prompt` must contain "current-dashboard current-tab session grounding" (agent must actually retrieve the data) → `missing_tool_result`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `session_tab_estimates_estimate_history`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Get workspace_session_context, add a Estimates tab, navigate to it, fetch the widget schema, create Bench Equities/estimate_history with data_args {"symbol": "MSFT"} there, and add a note mentioning Estimates on that tab.

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

#### `session_tab_exposure_sector_exposure`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Fetch workspace_session_context, add a Exposure tab, navigate to it, fetch the widget schema, create Bench Portfolio/sector_exposure there, and add a note mentioning Exposure on that tab.

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

#### `session_tab_rates_yield_curve`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> After fetching workspace_session_context, add a Rates tab, navigate to it, fetch the widget schema, create Bench Macro/yield_curve there, and add a note mentioning Rates on that tab.

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

#### `tool_usage_schema_note`

**easy** · category: read · specification: - · no-op baseline score: 0.000

> Call get_workspace_prompt with name workspace_tool_usage and add a HTML card mentioning schema-before-create workspace tool discipline.

- Fixture backends: equities, portfolio
- Initial workspace: dashboard "Prompt Review"; 1 seeded widget(s): risk_metrics({})
- Allowed tools (3): `get_workspace_snapshot`, `get_workspace_prompt`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/risk_metrics` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated html** ≥1× whose content mentions "schema-before-create" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_tool_usage"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`

#### `tool_usage_schema_summary`

**easy** · category: read · specification: - · no-op baseline score: 0.000

> Use get_workspace_prompt with name workspace_tool_usage, then add a HTML card mentioning schema-before-create workspace tool discipline.

- Fixture backends: equities, portfolio
- Initial workspace: dashboard "Prompt Review"; 1 seeded widget(s): holdings_table({})
- Allowed tools (3): `get_workspace_snapshot`, `get_workspace_prompt`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/holdings_table` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated html** ≥1× whose content mentions "schema-before-create" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_workspace_prompt` with args ⊇ {"name": "workspace_tool_usage"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_workspace_prompt` must contain "schema-before-create workspace tool discipline" (agent must actually retrieve the data) → `missing_tool_result`

### read (20)

#### `alert_trend`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_widget_data for the Bench Stark Enterprise Alert Trend widget; then add a short note that cites compliance_surveillance_hub_alerts_alert_trend and says you reviewed the data.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): compliance_surveillance_hub_alerts_alert_trend({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "compliance_surveillance_hub_alerts_alert_trend", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "compliance_surveillance_hub_alerts_alert_trend"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "alert_count" (agent must actually retrieve the data) → `missing_tool_result`

#### `attribution`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_widget_data on the Bench Stark Enterprise Attribution Summary widget, then add a short HTML card that cites Attribution Summary and says you reviewed the data.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): portfolio_command_center_attribution_attribution_summary({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "portfolio_command_center_attribution_attribution_summary", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "portfolio_command_center_attribution_attribution_summary"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "score" (agent must actually retrieve the data) → `missing_tool_result`

#### `break_aging`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_widget_data on the Bench Stark Enterprise Break Aging widget, then add a short HTML card that cites fund_operations_control_tower_recons_break_aging and says you reviewed the data.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): fund_operations_control_tower_recons_break_aging({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "fund_operations_control_tower_recons_break_aging", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "fund_operations_control_tower_recons_break_aging"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "score" (agent must actually retrieve the data) → `missing_tool_result`

#### `broker_scorecard`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> On the Bench Stark Enterprise Broker Scorecard widget, use get_widget_data, find the exact score for execution_desk_fills_broker_scorecard, then add a HTML card that cites each widget id, the field name, and the exact value.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): execution_desk_fills_broker_scorecard({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "execution_desk_fills_broker_scorecard", "score", "68.41" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "execution_desk_fills_broker_scorecard"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "score", "68.41" (agent must actually retrieve the data) → `missing_tool_result`

#### `client_pair`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> On the Bench Stark Enterprise Client Accounts and Relationship Metrics widgets, use get_widget_data, then add a short note that cites client_360_client_book_client_accounts and client_360_client_book_relationship_metrics and says you reviewed the data.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): client_360_client_book_client_accounts({"fund": "Flagship Long/Short", "period": "YTD"}), client_360_client_book_relationship_metrics({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "client_360_client_book_client_accounts", "client_360_client_book_relationship_metrics", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "client_360_client_book_client_accounts"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "client_360_client_book_relationship_metrics"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "count" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "value" (agent must actually retrieve the data) → `missing_tool_result`

#### `exec_pair`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_widget_data for the Bench Stark Enterprise Fills Table and Broker Scorecard widgets; then add a short note that cites Fills Table and execution_desk_fills_broker_scorecard and says you reviewed the data.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): execution_desk_fills_fills_table({"fund": "Flagship Long/Short", "period": "YTD"}), execution_desk_fills_broker_scorecard({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "execution_desk_fills_fills_table", "execution_desk_fills_broker_scorecard", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "execution_desk_fills_fills_table"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "execution_desk_fills_broker_scorecard"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "score" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "score" (agent must actually retrieve the data) → `missing_tool_result`

#### `issuer_conc`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_widget_data on the Bench Stark Enterprise Issuer Concentration widget, find the exact score for portfolio_command_center_holdings_issuer_concentration, then add a note that cites each widget id, the field name, and the exact value.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): portfolio_command_center_holdings_issuer_concentration({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "portfolio_command_center_holdings_issuer_concentration", "score", "94.45" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "portfolio_command_center_holdings_issuer_concentration"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "score", "94.45" (agent must actually retrieve the data) → `missing_tool_result`

#### `latency`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_widget_data for the Bench Stark Enterprise Latency by Feed widget; then add a short note that cites vendor_dataset_monitor_slas_latency_by_feed and says you reviewed the data.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): vendor_dataset_monitor_slas_latency_by_feed({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "vendor_dataset_monitor_slas_latency_by_feed", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "vendor_dataset_monitor_slas_latency_by_feed"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "latency_ms" (agent must actually retrieve the data) → `missing_tool_result`

#### `limits`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> On the Bench Stark Enterprise Limit Utilization widget, use get_widget_data, then add a short HTML card that cites risk_exposure_monitor_limits_limit_utilization and says you reviewed the data.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): risk_exposure_monitor_limits_limit_utilization({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "risk_exposure_monitor_limits_limit_utilization", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "risk_exposure_monitor_limits_limit_utilization"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "exposure" (agent must actually retrieve the data) → `missing_tool_result`

#### `order_status`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> On the Bench Stark Enterprise Order Status Metrics widget, use get_widget_data, then add a short note that cites execution_desk_blotter_order_status_metrics and says you reviewed the data.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): execution_desk_blotter_order_status_metrics({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "execution_desk_blotter_order_status_metrics", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "execution_desk_blotter_order_status_metrics"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "value" (agent must actually retrieve the data) → `missing_tool_result`

#### `pipeline`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> On the Bench Stark Enterprise Pipeline by Stage widget, use get_widget_data, then add a short HTML card that cites client_360_flows_pipeline_by_stage and says you reviewed the data.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): client_360_flows_pipeline_by_stage({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "client_360_flows_pipeline_by_stage", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "client_360_flows_pipeline_by_stage"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "score" (agent must actually retrieve the data) → `missing_tool_result`

#### `pm_values`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_widget_data for the Bench Stark Enterprise Portfolio Snapshot and Top Alerts widgets; find the exact value for portfolio_command_center_overview_portfolio_snapshot and alert_count for portfolio_command_center_overview_top_alerts, then add a note that cites each widget id, the field name, and the exact value.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): portfolio_command_center_overview_portfolio_snapshot({"fund": "Flagship Long/Short", "period": "YTD"}), portfolio_command_center_overview_top_alerts({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "portfolio_command_center_overview_portfolio_snapshot", "value", "87.94", "portfolio_command_center_overview_top_alerts", "alert_count", "193" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "portfolio_command_center_overview_portfolio_snapshot"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "portfolio_command_center_overview_top_alerts"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "value", "87.94" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "alert_count", "193" (agent must actually retrieve the data) → `missing_tool_result`

#### `quant_values`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_widget_data on the Bench Stark Enterprise Signal Metrics and Backtest Performance widgets, find the exact value for quant_research_backtest_lab_signals_signal_metrics and score for Backtest Performance, then add a note that cites each widget id, the field name, and the exact value.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): quant_research_backtest_lab_signals_signal_metrics({"fund": "Flagship Long/Short", "period": "YTD"}), quant_research_backtest_lab_backtest_backtest_performance({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "quant_research_backtest_lab_signals_signal_metrics", "value", "83.92", "quant_research_backtest_lab_backtest_backtest_performance", "score", "35.41" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "quant_research_backtest_lab_signals_signal_metrics"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "quant_research_backtest_lab_backtest_backtest_performance"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "value", "83.92" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "score", "35.41" (agent must actually retrieve the data) → `missing_tool_result`

#### `risk_pair`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_widget_data on the Bench Stark Enterprise VaR Trend and Drawdown widgets, then add a short HTML card that cites risk_exposure_monitor_dashboard_var_trend and risk_exposure_monitor_dashboard_drawdown and says you reviewed the data.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): risk_exposure_monitor_dashboard_var_trend({"fund": "Flagship Long/Short", "period": "YTD"}), risk_exposure_monitor_dashboard_drawdown({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "risk_exposure_monitor_dashboard_var_trend", "risk_exposure_monitor_dashboard_drawdown", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "risk_exposure_monitor_dashboard_var_trend"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "risk_exposure_monitor_dashboard_drawdown"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "var_usd" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "drawdown_usd" (agent must actually retrieve the data) → `missing_tool_result`

#### `risk_values`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_widget_data for the Bench Stark Enterprise Risk Snapshot and Limit Utilization widgets; find the exact value for risk_exposure_monitor_dashboard_risk_snapshot and exposure for risk_exposure_monitor_limits_limit_utilization, then add a note that cites each widget id, the field name, and the exact value.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): risk_exposure_monitor_dashboard_risk_snapshot({"fund": "Flagship Long/Short", "period": "YTD"}), risk_exposure_monitor_limits_limit_utilization({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "risk_exposure_monitor_dashboard_risk_snapshot", "value", "0.2878", "risk_exposure_monitor_limits_limit_utilization", "exposure", "0.0339" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "risk_exposure_monitor_dashboard_risk_snapshot"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "risk_exposure_monitor_limits_limit_utilization"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "value", "0.2878" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "exposure", "0.0339" (agent must actually retrieve the data) → `missing_tool_result`

#### `sla_metrics`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> On the Bench Stark Enterprise SLA Metrics widget, use get_widget_data, find the exact value for vendor_dataset_monitor_vendors_sla_metrics, then add a HTML card that cites each widget id, the field name, and the exact value.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): vendor_dataset_monitor_vendors_sla_metrics({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "vendor_dataset_monitor_vendors_sla_metrics", "value", "63.73" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "vendor_dataset_monitor_vendors_sla_metrics"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "value", "63.73" (agent must actually retrieve the data) → `missing_tool_result`

#### `strategy_health`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_widget_data for the Bench Stark Enterprise Strategy Health Metrics widget; then add a short note that cites strategy_health_monitor_performance_strategy_health_metrics and says you reviewed the data.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): strategy_health_monitor_performance_strategy_health_metrics({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "strategy_health_monitor_performance_strategy_health_metrics", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "strategy_health_monitor_performance_strategy_health_metrics"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "value" (agent must actually retrieve the data) → `missing_tool_result`

#### `stress_values`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_widget_data for the Bench Stark Enterprise Days to Liquidate and Risk Snapshot widgets; find the exact score for stress_liquidity_lab_liquidity_days_to_liquidate and value for stress_liquidity_lab_stress_tests_risk_snapshot, then add a HTML card that cites each widget id, the field name, and the exact value.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): stress_liquidity_lab_liquidity_days_to_liquidate({"fund": "Flagship Long/Short", "period": "YTD"}), stress_liquidity_lab_stress_tests_risk_snapshot({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "stress_liquidity_lab_liquidity_days_to_liquidate", "score", "62.96", "stress_liquidity_lab_stress_tests_risk_snapshot", "value", "83.56" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "stress_liquidity_lab_liquidity_days_to_liquidate"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "stress_liquidity_lab_stress_tests_risk_snapshot"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "score", "62.96" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "value", "83.56" (agent must actually retrieve the data) → `missing_tool_result`

#### `var_trend`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_widget_data for the Bench Stark Enterprise VaR Trend widget; find the exact var_usd for risk_exposure_monitor_dashboard_var_trend, then add a HTML card that cites each widget id, the field name, and the exact value.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 1 seeded widget(s): risk_exposure_monitor_dashboard_var_trend({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "risk_exposure_monitor_dashboard_var_trend", "var_usd", "-222500" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "risk_exposure_monitor_dashboard_var_trend"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "var_usd", "-222500" (agent must actually retrieve the data) → `missing_tool_result`

#### `vendor_pair`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_widget_data for the Bench Stark Enterprise Vendor SLA Status and Latency by Feed widgets; then add a short note that cites vendor_dataset_monitor_slas_vendor_sla_status and vendor_dataset_monitor_slas_latency_by_feed and says you reviewed the data.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Data Review"; 1 tab(s): main; 2 seeded widget(s): vendor_dataset_monitor_slas_vendor_sla_status({"fund": "Flagship Long/Short", "period": "YTD"}), vendor_dataset_monitor_slas_latency_by_feed({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `get_widget_data`, `read_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "vendor_dataset_monitor_slas_vendor_sla_status", "vendor_dataset_monitor_slas_latency_by_feed", "data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "vendor_dataset_monitor_slas_vendor_sla_status"} must appear in the trace → `missing_tool_call`
- **Tool call** ≥1× `get_widget_data` with args ⊇ {"origin": "Bench Stark Enterprise", "widget_id": "vendor_dataset_monitor_slas_latency_by_feed"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_widget_data` must contain "score" (agent must actually retrieve the data) → `missing_tool_result`
- **Tool result** of `get_widget_data` must contain "latency_ms" (agent must actually retrieve the data) → `missing_tool_result`

### resources (20)

#### `full_client_360`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Read the app-builder index resource at openbb://workspace/app-builder/index, instantiate client-360 as Client Resource Command, navigate to flows, add widget client_360_flows_pipeline_by_stage, and add a note mentioning pipeline and resource.

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

#### `full_portfolio_command_center`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Read the app-builder index resource at openbb://workspace/app-builder/index, instantiate portfolio-command-center as PM Resource Command, navigate to holdings, add widget portfolio_command_center_holdings_sector_exposure, and add a note mentioning sector exposure and resource.

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

#### `full_risk_exposure_monitor`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Use the app-builder index resource openbb://workspace/app-builder/index, instantiate risk-exposure-monitor as Risk Resource Command, navigate to limits, add widget risk_exposure_monitor_limits_limit_utilization, and add a note mentioning limit utilization and resource.

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

#### `full_vendor_dataset_monitor`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Read the app-builder index resource at openbb://workspace/app-builder/index, instantiate vendor-dataset-monitor as Vendor Resource Command, navigate to incidents, add widget vendor_dataset_monitor_incidents_incident_log, and add a HTML card mentioning incident log and resource.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (7): `read_workspace_resource`, `manage_backends`, `manage_apps`, `navigate_workspace`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 7 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vendor Resource Command" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_incidents_incident_log` on tab `incidents` → `missing_widget`
- **Generated html** ≥1× whose content mentions "incident log", "resource" on tab `incidents` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "vendor-dataset-monitor" (agent must actually retrieve the resource) → `missing_resource_read`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`

#### `index_client_360`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> After calling read_workspace_resource with uri openbb://workspace/app-builder/index, add a HTML card naming the Client 360 template id client-360.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "App Index Review"; 1 seeded widget(s): vendor_dataset_monitor_quality_affected_apps({})
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_quality_affected_apps` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated html** ≥1× whose content mentions "Client 360", "client-360" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "Client 360", "client-360" (agent must actually retrieve the resource) → `missing_resource_read`

#### `index_equity_earnings_review`

**easy** · category: dashboard · specification: - · no-op baseline score: 0.000

> After calling read_workspace_resource with uri openbb://workspace/app-builder/index, add a note naming the Equity Earnings Review template id equity-earnings-review.

- Fixture backends: equities
- Initial workspace: dashboard "App Index Review"
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Equity Earnings Review", "equity-earnings-review" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "Equity Earnings Review", "equity-earnings-review" (agent must actually retrieve the resource) → `missing_resource_read`

#### `index_portfolio_command_center`

**easy** · category: dashboard · specification: - · no-op baseline score: 0.000

> After calling read_workspace_resource with uri openbb://workspace/app-builder/index, add a note naming the Portfolio Command Center template id portfolio-command-center.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "App Index Review"; 1 seeded widget(s): vendor_dataset_monitor_quality_row_count_drift({})
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_quality_row_count_drift` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Portfolio Command Center", "portfolio-command-center" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "Portfolio Command Center", "portfolio-command-center" (agent must actually retrieve the resource) → `missing_resource_read`

#### `index_risk_exposure_monitor`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Call read_workspace_resource with uri openbb://workspace/app-builder/index and add a note naming the Risk Exposure Monitor template id risk-exposure-monitor.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "App Index Review"; 1 seeded widget(s): vendor_dataset_monitor_quality_validation_errors({})
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_quality_validation_errors` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Risk Exposure Monitor", "risk-exposure-monitor" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "Risk Exposure Monitor", "risk-exposure-monitor" (agent must actually retrieve the resource) → `missing_resource_read`

#### `instantiate_compliance_surveillance_hub`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Use the app-builder index resource openbb://workspace/app-builder/index, then instantiate template compliance-surveillance-hub as a dashboard named Compliance Resource Dashboard.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `read_workspace_resource`, `manage_backends`, `manage_apps`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Compliance Resource Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "compliance-surveillance-hub" (agent must actually retrieve the resource) → `missing_resource_read`

#### `instantiate_equity_earnings_review`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Read the app-builder index resource at openbb://workspace/app-builder/index, then instantiate template equity-earnings-review as a dashboard named Equity Resource Dashboard.

- Fixture backends: equities
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `read_workspace_resource`, `manage_backends`, `manage_apps`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Equity Resource Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "equity-earnings-review" (agent must actually retrieve the resource) → `missing_resource_read`

#### `instantiate_execution_desk`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Read the app-builder index resource at openbb://workspace/app-builder/index, then instantiate template execution-desk as a dashboard named Execution Resource Dashboard.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `read_workspace_resource`, `manage_backends`, `manage_apps`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Execution Resource Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "execution-desk" (agent must actually retrieve the resource) → `missing_resource_read`

#### `instantiate_vendor_dataset_monitor`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> After reading the app-builder index resource openbb://workspace/app-builder/index, instantiate template vendor-dataset-monitor as a dashboard named Vendor Resource Dashboard.

- Fixture backends: stark-enterprise
- Initial workspace: empty (no seeded dashboard)
- Allowed tools (3): `read_workspace_resource`, `manage_backends`, `manage_apps`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vendor Resource Dashboard" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Tool call** ≥1× `manage_apps` with args ⊇ {"operation": "instantiate"} must appear in the trace → `missing_tool_call`
- **Resource read** of `openbb://workspace/app-builder/index` must contain "vendor-dataset-monitor" (agent must actually retrieve the resource) → `missing_resource_read`

#### `skill_build_finance_comps`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> Read resource openbb://workspace/specs/widget-parameters, add Bench Portfolio/sector_exposure, and add a note that mentions peer set.

- Fixture backends: portfolio
- Initial workspace: dashboard "Resource Build"
- Allowed tools (6): `get_workspace_snapshot`, `read_workspace_resource`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Portfolio/sector_exposure` → `missing_widget`
- **Generated note** ≥1× whose content mentions "peer set" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/specs/widget-parameters` must contain "Widget Parameters" (agent must actually retrieve the resource) → `missing_resource_read`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `skill_build_finance_earnings_prep`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Read resource openbb://workspace/specs/widgets-json, add Bench Equities/estimate_history with data_args {"symbol": "AAPL"}, and add a note that mentions surprise drivers.

- Fixture backends: equities
- Initial workspace: dashboard "Resource Build"
- Allowed tools (6): `get_workspace_snapshot`, `read_workspace_resource`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "surprise drivers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/specs/widgets-json` must contain "widgets.json" (agent must actually retrieve the resource) → `missing_resource_read`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `skill_build_finance_guidance_tracker`

**hard** · category: dashboard · specification: - · no-op baseline score: 0.000

> After reading resource openbb://workspace/guides/build-an-app, add Bench Stark Enterprise/executive_investment_dashboard_risk_limit_utilization and add a note that mentions evidence gaps.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Resource Build"; 1 seeded widget(s): workspace_data_control_center_entitlements_role_coverage({})
- Allowed tools (6): `get_workspace_snapshot`, `read_workspace_resource`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/executive_investment_dashboard_risk_limit_utilization` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_entitlements_role_coverage` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "evidence gaps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/guides/build-an-app` must contain "Build an App" (agent must actually retrieve the resource) → `missing_resource_read`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `skill_build_finance_tearsheet`

**medium** · category: dashboard · specification: - · no-op baseline score: 0.000

> Read resource openbb://workspace/specs/widget-types, add Bench Equities/fundamental_metrics with data_args {"symbol": "MSFT"}, and add a note that mentions valuation.

- Fixture backends: equities
- Initial workspace: dashboard "Resource Build"
- Allowed tools (6): `get_workspace_snapshot`, `read_workspace_resource`, `list_available_widgets`, `get_widget_schema`, `create_widget`, `add_generative_widget`
- Turn budget: 9 · oracle reference trace: 6 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Generated note** ≥1× whose content mentions "valuation" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/specs/widget-types` must contain "table" (agent must actually retrieve the resource) → `missing_resource_read`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `skill_finance_comps`

**easy** · category: read · specification: - · no-op baseline score: 0.000

> Call read_workspace_resource with uri openbb://workspace/skills/finance-comps, then add a note mentioning peer set.

- Fixture backends: equities
- Initial workspace: dashboard "Resource Review"
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "peer set" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/skills/finance-comps` must contain "Comps workflow" (agent must actually retrieve the resource) → `missing_resource_read`

#### `skill_finance_earnings_prep`

**easy** · category: read · specification: - · no-op baseline score: 0.000

> Call read_workspace_resource with uri openbb://workspace/skills/finance-earnings-prep, then add a note mentioning surprise drivers.

- Fixture backends: equities
- Initial workspace: dashboard "Resource Review"
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "surprise drivers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/skills/finance-earnings-prep` must contain "Earnings prep workflow" (agent must actually retrieve the resource) → `missing_resource_read`

#### `skill_finance_guidance_tracker`

**easy** · category: read · specification: - · no-op baseline score: 0.000

> Call read_workspace_resource with uri openbb://workspace/skills/finance-guidance-tracker, then add a note mentioning management claims.

- Fixture backends: equities
- Initial workspace: dashboard "Resource Review"
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "management claims" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/skills/finance-guidance-tracker` must contain "Guidance tracker workflow" (agent must actually retrieve the resource) → `missing_resource_read`

#### `skill_finance_tearsheet`

**easy** · category: read · specification: - · no-op baseline score: 0.000

> Use read_workspace_resource with uri openbb://workspace/skills/finance-tearsheet and add a note mentioning valuation.

- Fixture backends: equities
- Initial workspace: dashboard "Resource Review"
- Allowed tools (3): `get_workspace_snapshot`, `read_workspace_resource`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "valuation" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Resource read** of `openbb://workspace/skills/finance-tearsheet` must contain "Tearsheet workflow" (agent must actually retrieve the resource) → `missing_resource_read`

### skills (20)

#### `apply_finance_comps_with_aapl`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_skill_content with slug finance-comps. Following that workflow, add the Fundamental Metrics widget for AAPL to the active dashboard, then add a note that applies the skill's workflow steps to this widget. Omit dashboard_id when adding the note.

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

#### `apply_finance_comps_workflow_notes`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_skill_content with slug finance-comps, then add a note on the active dashboard that captures the workflow steps for an analyst. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_capacity_liquidity_capacity_curve({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_capacity_liquidity_capacity_curve` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "comps", "peer set" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-comps"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Comps workflow", "peer set", "valuation multiples" (agent must actually retrieve the data) → `missing_tool_result`

#### `apply_finance_earnings_prep_with_aapl`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> After calling get_skill_content with slug finance-earnings-prep, follow that workflow by adding the Estimate History widget for AAPL to the active dashboard, then add a note that applies the skill's workflow steps to this widget. Omit dashboard_id when adding the note.

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

#### `apply_finance_earnings_prep_workflow_notes`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> After calling get_skill_content with slug finance-earnings-prep, add a note on the active dashboard that captures the workflow steps for an analyst. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_overview_workflow_overview({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_overview_workflow_overview` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "earnings prep", "surprise drivers" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-earnings-prep"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Earnings prep workflow", "surprise drivers", "portfolio manager" (agent must actually retrieve the data) → `missing_tool_result`

#### `apply_finance_guidance_tracker_with_aapl`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> Call get_skill_content with slug finance-guidance-tracker. Following that workflow, add the Latest News widget for AAPL to the active dashboard, then add a note that applies the skill's workflow steps to this widget. Omit dashboard_id when adding the note.

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

#### `apply_finance_guidance_tracker_workflow_notes`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Call get_skill_content with slug finance-guidance-tracker, then add a note on the active dashboard that captures the workflow steps for an analyst. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_performance_gross_and_net_exposure({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_performance_gross_and_net_exposure` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "guidance", "claims" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-guidance-tracker"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Guidance tracker workflow", "management claims", "evidence gaps" (agent must actually retrieve the data) → `missing_tool_result`

#### `apply_finance_tearsheet_with_msft`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Call get_skill_content with slug finance-tearsheet. Following that workflow, add the Price Performance widget for MSFT to the active dashboard, then add a note that applies the skill's workflow steps to this widget. Omit dashboard_id when adding the note.

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

#### `apply_finance_tearsheet_workflow_notes`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Call get_skill_content with slug finance-tearsheet, then add a note on the active dashboard that captures the workflow steps for an analyst. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): strategy_health_monitor_performance_sleeve_performance({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/strategy_health_monitor_performance_sleeve_performance` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "tearsheet", "valuation" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-tearsheet"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Tearsheet workflow", "valuation", "investment conclusion" (agent must actually retrieve the data) → `missing_tool_result`

#### `file_finance_comps_under_its_own_tab`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_skill_content with slug finance-comps. Add a new tab named Comps and put a note on that tab capturing the workflow steps. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_incidents_affected_apps({})
- Allowed tools (5): `get_workspace_snapshot`, `get_skill_content`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `comps` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_incidents_affected_apps` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "comps", "peer set" on tab `comps` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-comps"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Comps workflow", "peer set", "valuation multiples" (agent must actually retrieve the data) → `missing_tool_result`

#### `file_finance_earnings_prep_under_its_own_tab`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> After calling get_skill_content with slug finance-earnings-prep, add a new tab named Earnings Prep and put a note on that tab capturing the workflow steps. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_incidents_blast_radius_summary({})
- Allowed tools (5): `get_workspace_snapshot`, `get_skill_content`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `earnings-prep` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_incidents_blast_radius_summary` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "earnings prep", "surprise drivers" on tab `earnings-prep` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-earnings-prep"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Earnings prep workflow", "surprise drivers", "portfolio manager" (agent must actually retrieve the data) → `missing_tool_result`

#### `file_finance_guidance_tracker_under_its_own_tab`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Call get_skill_content with slug finance-guidance-tracker. Add a new tab named Guidance and put a note on that tab capturing the workflow steps. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_incidents_freshness_exceptions({})
- Allowed tools (5): `get_workspace_snapshot`, `get_skill_content`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `guidance` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_incidents_freshness_exceptions` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "guidance", "claims" on tab `guidance` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-guidance-tracker"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Guidance tracker workflow", "management claims", "evidence gaps" (agent must actually retrieve the data) → `missing_tool_result`

#### `file_finance_tearsheet_under_its_own_tab`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Call get_skill_content with slug finance-tearsheet. Add a new tab named Tearsheet and put a note on that tab capturing the workflow steps. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_incidents_incident_timeline({})
- Allowed tools (5): `get_workspace_snapshot`, `get_skill_content`, `manage_navigation_bar`, `navigate_workspace`, `add_generative_widget`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Tab** `overview` must exist (matched by tab id) → `missing_tab`
- **Tab** `tearsheet` must exist (matched by tab id) → `missing_tab`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_incidents_incident_timeline` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "tearsheet", "valuation" on tab `tearsheet` (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-tearsheet"} must appear in the trace → `missing_tool_call`
- **Tool result** of `get_skill_content` must contain "Tearsheet workflow", "valuation", "investment conclusion" (agent must actually retrieve the data) → `missing_tool_result`

#### `grounded_finance_comps_for_nvda`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_skill_content with slug finance-comps. Following that workflow, add the Fundamental Metrics widget for NVDA, read its data, and add a note that cites the exact key value from the data. Omit dashboard_id when adding the note.

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

#### `grounded_finance_earnings_prep_for_msft`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> After calling get_skill_content with slug finance-earnings-prep, follow that workflow by adding the Estimate History widget for MSFT, reading its data, and adding a note that cites the exact key value from the data. Omit dashboard_id when adding the note.

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

#### `grounded_finance_guidance_tracker_for_nvda`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> Call get_skill_content with slug finance-guidance-tracker. Following that workflow, add the Estimate History widget for NVDA, read its data, and add a note that cites the exact key value from the data. Omit dashboard_id when adding the note.

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

#### `grounded_finance_tearsheet_for_aapl`

**hard** · category: single-widget · specification: - · no-op baseline score: 0.000

> Call get_skill_content with slug finance-tearsheet. Following that workflow, add the Price Performance widget for AAPL, read its data, and add a note that cites the exact key value from the data. Omit dashboard_id when adding the note.

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

#### `read_the_finance_comps_skill`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Use get_skill_content with slug finance-comps, then add a note on the active dashboard naming the Finance Comps skill. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_vendors_sla_metrics({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_sla_metrics` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Finance Comps" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-comps"} must appear in the trace → `missing_tool_call`

#### `read_the_finance_earnings_prep_skill`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> After calling get_skill_content with slug finance-earnings-prep, add a note on the active dashboard naming the Finance Earnings Prep skill. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_vendors_vendor_contract_terms({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_vendor_contract_terms` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Finance Earnings Prep" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-earnings-prep"} must appear in the trace → `missing_tool_call`

#### `read_the_finance_guidance_tracker_skill`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Call get_skill_content with slug finance-guidance-tracker, then add a note on the active dashboard naming the Finance Guidance Tracker skill. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): vendor_dataset_monitor_vendors_vendor_sla_status({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_vendors_vendor_sla_status` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Finance Guidance Tracker" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-guidance-tracker"} must appear in the trace → `missing_tool_call`

#### `read_the_finance_tearsheet_skill`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Call get_skill_content with slug finance-tearsheet, then add a note on the active dashboard naming the Finance Tearsheet skill. Omit dashboard_id when adding the note.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Skill Review"; 1 tab(s): overview; 1 seeded widget(s): workspace_data_control_center_ai_access_ai_usage_by_role({})
- Allowed tools (3): `get_workspace_snapshot`, `get_skill_content`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/workspace_data_control_center_ai_access_ai_usage_by_role` on tab `overview` → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "Finance Tearsheet" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `get_skill_content` with args ⊇ {"slug": "finance-tearsheet"} must appear in the trace → `missing_tool_call`

### update (20)

#### `double_aapl_desk`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> This AAPL desk dashboard needs two repairs: the price widget should show AAPL, not MSFT, and the news widget should show 5 articles, not only 1. Repair both existing widgets and add a HTML card mentioning AAPL and the word repaired.

- Fixture backends: equities
- Initial workspace: dashboard "Double Repair Task"; 2 seeded widget(s): price_performance({"symbol": "MSFT"}), latest_news({"symbol": "AAPL", "limit": 1})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥0× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL", "limit": 5} → `missing_widget`
- **Widget** ≥0× `Bench Equities/latest_news` with data_args ⊇ {"limit": 1} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated html** ≥1× whose content mentions "AAPL", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `double_nvda_switch`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> Repair the existing widgets on this NVDA dashboard: change the price widget from AAPL to NVDA and the estimates widget from MSFT to NVDA, then add a note mentioning NVDA and the word repaired.

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

#### `double_rates_switch`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> On this dashboard, repair two macro series: the first widget should show DGS10 (not DGS2), and the second should show CPIAUCSL (not FEDFUNDS). Repair both existing widgets and add a note mentioning DGS10, CPIAUCSL, and the word repaired.

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

#### `double_stark_ops`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> The ops dashboard has two wrong settings: Vendor SLA Status is Open but should be In Review, and Portfolio Snapshot is YTD but should be MTD. Repair both existing widgets and add a note mentioning In Review, MTD, and the word repaired.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Double Repair Task"; 2 seeded widget(s): vendor_dataset_monitor_slas_vendor_sla_status({"vendor": "FactSet", "status": "Open"}), portfolio_command_center_overview_portfolio_snapshot({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 6 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"vendor": "FactSet", "status": "In Review"} → `missing_widget`
- **Widget** ≥0× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"status": "Open"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_overview_portfolio_snapshot` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "MTD"} → `missing_widget`
- **Widget** ≥0× `Bench Stark Enterprise/portfolio_command_center_overview_portfolio_snapshot` with data_args ⊇ {"period": "YTD"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "In Review", "MTD", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `repair_news_msft_aapl`

**medium** · category: repair · specification: - · no-op baseline score: 0.000

> This AAPL desk dashboard mistakenly shows MSFT news. Repair the widget to AAPL and add a note saying what was repaired, mentioning both values.

- Fixture backends: equities
- Initial workspace: dashboard "Repair Task"; 1 seeded widget(s): latest_news({"symbol": "MSFT"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`
- **Widget** ≥0× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "MSFT", "AAPL", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `repair_risk_portfolio`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> This Long/Short Equity risk dashboard has its snapshot configured for Macro Multi-Asset. Repair the widget to Long/Short Equity and add a HTML card saying what was repaired, mentioning both values.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Repair Task"; 1 seeded widget(s): risk_exposure_monitor_dashboard_risk_snapshot({"portfolio": "Macro Multi-Asset"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_risk_snapshot` with data_args ⊇ {"portfolio": "Long/Short Equity"} → `missing_widget`
- **Widget** ≥0× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_risk_snapshot` with data_args ⊇ {"portfolio": "Macro Multi-Asset"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated html** ≥1× whose content mentions "Macro Multi-Asset", "Long/Short Equity", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `repair_series_fedfunds_cpi`

**hard** · category: repair · specification: - · no-op baseline score: 0.000

> This inflation dashboard mistakenly shows the FEDFUNDS series. Add a HTML card saying what was repaired and mentioning both values after you repair the widget to CPIAUCSL.

- Fixture backends: macro
- Initial workspace: dashboard "Repair Task"; 1 seeded widget(s): macro_timeseries({"series": "FEDFUNDS"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "CPIAUCSL"} → `missing_widget`
- **Widget** ≥0× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "FEDFUNDS"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated html** ≥1× whose content mentions "FEDFUNDS", "CPIAUCSL", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `repair_ticker_nvda_msft`

**medium** · category: repair · specification: - · no-op baseline score: 0.000

> This MSFT review dashboard mistakenly shows NVDA in the price widget. Repair the widget to MSFT; then add a note saying what was repaired and mentioning both values.

- Fixture backends: equities
- Initial workspace: dashboard "Repair Task"; 1 seeded widget(s): price_performance({"symbol": "NVDA"})
- Allowed tools (4): `get_workspace_snapshot`, `read_widget`, `update_widget`, `add_generative_widget`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`
- **Widget** ≥0× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`
- **Generated note** ≥1× whose content mentions "NVDA", "MSFT", "repaired" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `set_latest_news_symbol_to_msft`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> For the existing Latest News widget, set symbol to MSFT.

- Fixture backends: equities
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): latest_news({"symbol": "NVDA", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "MSFT", "limit": 5} → `missing_widget`

#### `set_macro_timeseries_series_to_dgs10`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> For the existing Macro Timeseries widget, set series to DGS10.

- Fixture backends: macro
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): macro_timeseries({"series": "DGS2"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`

#### `set_portfolio_snapshot_period_to_mtd`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> For the existing Portfolio Snapshot widget, set period to MTD.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): portfolio_command_center_overview_portfolio_snapshot({"fund": "Flagship Long/Short", "period": "YTD"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_overview_portfolio_snapshot` with data_args ⊇ {"fund": "Flagship Long/Short", "period": "MTD"} → `missing_widget`

#### `set_price_performance_symbol_to_aapl`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> For the existing Price Performance widget, set symbol to AAPL.

- Fixture backends: equities
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): price_performance({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`

#### `update_estimate_history_aapl_to_nvda`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> Update the existing Estimate History widget from AAPL to NVDA; do not create a new one and leave no widget showing the old value.

- Fixture backends: equities
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): estimate_history({"symbol": "AAPL"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Widget** ≥0× `Bench Equities/estimate_history` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

#### `update_fundamental_metrics_msft_to_nvda`

**easy** · category: single-widget · specification: - · no-op baseline score: 0.000

> The Fundamental Metrics widget currently shows MSFT. Update the existing widget to NVDA; do not create a new one and leave no widget showing the old value.

- Fixture backends: equities
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): fundamental_metrics({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`
- **Widget** ≥0× `Bench Equities/fundamental_metrics` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

#### `update_macro_timeseries_cpiaucsl_to_fedfunds`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> The existing Macro Timeseries widget currently shows CPIAUCSL. Update that widget to FEDFUNDS; do not create a new one and leave no widget showing the old value.

- Fixture backends: macro
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): macro_timeseries({"series": "CPIAUCSL"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "FEDFUNDS"} → `missing_widget`
- **Widget** ≥0× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "CPIAUCSL"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

#### `update_only_the_dgs2_macro_timeseries`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Two Macro Timeseries widgets are on this dashboard: one for DGS10 and one for DGS2. Only update the DGS2 one to FEDFUNDS; leave the DGS10 widget untouched.

- Fixture backends: macro
- Initial workspace: dashboard "Selective Update Task"; 2 seeded widget(s): macro_timeseries({"series": "DGS10"}), macro_timeseries({"series": "DGS2"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS10"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "FEDFUNDS"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥0× `Bench Macro/macro_timeseries` with data_args ⊇ {"series": "DGS2"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

#### `update_only_the_factset_vendor_sla_status`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Leave the Bloomberg Vendor SLA Status widget untouched, and update only the FactSet Vendor SLA Status widget to S&P Global.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Selective Update Task"; 2 seeded widget(s): vendor_dataset_monitor_slas_vendor_sla_status({"vendor": "Bloomberg"}), vendor_dataset_monitor_slas_vendor_sla_status({"vendor": "FactSet"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"vendor": "Bloomberg"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"vendor": "S&P Global"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥0× `Bench Stark Enterprise/vendor_dataset_monitor_slas_vendor_sla_status` with data_args ⊇ {"vendor": "FactSet"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

#### `update_only_the_msft_price_performance`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Two Price Performance widgets are on this dashboard: one for AAPL and one for MSFT. Only update the MSFT one to NVDA; leave the AAPL widget untouched.

- Fixture backends: equities
- Initial workspace: dashboard "Selective Update Task"; 2 seeded widget(s): price_performance({"symbol": "AAPL"}), price_performance({"symbol": "MSFT"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥0× `Bench Equities/price_performance` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

#### `update_only_the_nvda_latest_news`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> Leave the AAPL Latest News widget untouched, and update only the NVDA Latest News widget to MSFT.

- Fixture backends: equities
- Initial workspace: dashboard "Selective Update Task"; 2 seeded widget(s): latest_news({"symbol": "AAPL", "limit": 5}), latest_news({"symbol": "NVDA", "limit": 5})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 5 · oracle reference trace: 2 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "AAPL"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥1× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "MSFT"} → `missing_widget`; and ≤1 such widget(s) → `too_many_widgets`
- **Widget** ≥0× `Bench Equities/latest_news` with data_args ⊇ {"symbol": "NVDA"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`

#### `update_rejected_orders_desk_to_credit`

**medium** · category: single-widget · specification: - · no-op baseline score: 0.000

> The existing Rejected Orders widget currently shows US Equity. Update that widget to Credit; do not create a new one and leave no widget showing the old value.

- Fixture backends: stark-enterprise
- Initial workspace: dashboard "Update Task"; 1 seeded widget(s): execution_desk_exceptions_rejected_orders({"desk": "US Equity", "period": "YTD"})
- Allowed tools (3): `get_workspace_snapshot`, `read_widget`, `update_widget`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Bench Stark Enterprise/execution_desk_exceptions_rejected_orders` with data_args ⊇ {"desk": "Credit", "period": "YTD"} → `missing_widget`
- **Widget** ≥0× `Bench Stark Enterprise/execution_desk_exceptions_rejected_orders` with data_args ⊇ {"desk": "US Equity"} → `missing_widget`; and ≤0 such widget(s) → `too_many_widgets`


## Suite: build-openbb-apps (236 tasks)

### advanced (20)

#### `case_prompt_omni`

**hard** · category: platform · specification: partially-specified

> Create a usable cases and compliance alerts workflow for a surveillance analyst. The workspace must cover hidden-prompt question answering over case evidence. The source contract must retain `prompt`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `case_qa_omni`

**medium** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Surveillance Data' at http://localhost:7807. Implement the live or advanced interaction correctly. The experience needs Case Q&A (`case_qa_omni`, omni) using `/case-qa` for ask questions over the surveillance case corpus; user controls: Prompt (`prompt`, text). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Surveillance Data/case_qa_omni` → `missing_widget`

#### `case_qa_omni_app`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for cases and compliance alerts. The workspace must cover ask questions over the surveillance case corpus. Leave the complete working workspace open for review. Use `prompt` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `case_qa_omni_ship`

**hard** · category: platform · specification: -

> Build a surveillance analyst a dependable cases and compliance alerts workspace. The workspace must cover ask questions over the surveillance case corpus. The workspace must cover open surveillance alerts. The workspace must cover open alert count. Analysts need to inspect alert ID, desk, severity, age days. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Surveillance QA', 'case QA', 'Surveillance Data', 'Show high severity cases'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Surveillance QA", "case QA", "Surveillance Data", "Show high severity cases" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `case_room_omni_room`

**hard** · category: platform · specification: -

> The desk needs a production-ready cases and compliance alerts workflow for a surveillance analyst. The workspace must cover question answering over surveillance cases. The workspace must cover open surveillance alerts. The workspace must cover open alert count. Analysts need to inspect alert ID, desk, severity, age days. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `live_orders_grid`

**easy** · category: platform · specification: -

> Connect the backend and make its first widget usable on the current dashboard. Use 'Execution Desk Data' at http://localhost:7806. Implement the live or advanced interaction correctly. The experience needs Live Orders Grid (`live_orders_grid`, live_grid) using `/live-orders` for streaming order blotter over websocket; stream updates from `live-orders-ws`; stream row id `order_id`; columns: order_id (text), px (number, showCellChange). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Execution Desk Data/live_orders_grid` → `missing_widget`

#### `live_orders_grid_app`

**medium** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Execution Desk Data' at http://localhost:7806. Implement the live or advanced interaction correctly. The experience needs Live Orders Grid (`live_orders_grid`, live_grid) using `/live-orders` for streaming order blotter over websocket; stream updates from `live-orders-ws`; stream row id `order_id`; columns: order_id (text), px (number, showCellChange). Organize it as app 'Live Order Tape' with tabs Orders (live_orders_grid). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Live Order Tape" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Execution Desk Data/live_orders_grid` on tab `orders` → `missing_widget`

#### `live_orders_grid_ship`

**hard** · category: platform · specification: -

> Build an execution analyst a dependable orders and venue quality workspace. The workspace must cover live order activity. The workspace must cover open execution exceptions. The workspace must cover live open orders blotter. Analysts need to inspect order ID, price, symbol, quantity, status. Large result sets must stay responsive while analysts filter and page through them. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Execution Live Grid', 'live stream', 'Execution Desk Data', 'EDGX'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Execution Live Grid", "live stream", "Execution Desk Data", "EDGX" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `macro_advanced_chart_room`

**hard** · category: platform · specification: -

> Build a rates strategist a dependable rates and Treasury markets workspace. The workspace must cover market history for treasury futures. The workspace must cover the Treasury yield curve. The workspace must cover current 2s10s spread in bps. Leave the complete working workspace open for review. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `orders_ops_stream_room`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for orders and venue quality. The workspace must cover streaming order tape for the ops room. The workspace must cover open execution exceptions. Analysts need to inspect order ID, price. Large result sets must stay responsive while analysts filter and page through them. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use `venue_scope` and `order_id` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `orders_stream`

**hard** · category: platform · specification: partially-specified

> Create a usable orders and venue quality workflow for an execution analyst. The workspace must cover streaming orders with a stable row id. Analysts need to inspect order ID, price. Large result sets must stay responsive while analysts filter and page through them. The source contract must retain `venue` and `order_id`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `rates_advanced_chart`

**medium** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Rates Watch Data' at http://localhost:7803. Implement the live or advanced interaction correctly. The experience needs Rates Advanced Chart (`rates_advanced_chart`, advanced_charting) using `/rates-udf` for tradingView advanced charting for the 10Y yield future; default symbol `US10Y`; update frequency `30000`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Rates Watch Data/rates_advanced_chart` → `missing_widget`

#### `rates_advanced_chart_app`

**hard** · category: platform · specification: partially-specified

> Create a usable rates and Treasury markets workflow for a rates strategist. The workspace must cover market history for the 10Y yield future. Leave the complete working workspace open for review. The source contract must retain `Rates Watch Data`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `rates_live_chart_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover market history for treasury futures. The workspace must cover the Treasury yield curve. The workspace must cover current 2s10s spread in bps. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Rates Advanced Live', 'Treasury futures', 'Rates Watch Data', 'ZB'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Rates Advanced Live", "Treasury futures", "Rates Watch Data", "ZB" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `rates_symbol_chart`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a rates strategist covering rates and Treasury markets. The workspace must cover tradingView analysis with a selectable symbol. An analyst can filter the analysis by ticker. Keep these source-contract anchors: `symbol`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vix_advanced`

**medium** · category: platform · specification: explicit

> Make the requested backend widget available and working in the current view. Use 'Vol Desk Data' at http://localhost:7801. Implement the live or advanced interaction correctly. The experience needs VIX Advanced Chart (`vix_advanced`, advanced_charting) using `/udf` for tradingView advanced charting for VIX futures; default symbol `VIX`; update frequency `60000`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vol Desk Data/vix_advanced` → `missing_widget`

#### `vix_advanced_app`

**easy** · category: platform · specification: -

> Publish the requested app and open it in Workspace to verify it works. Use 'Vol Desk Data' at http://localhost:7801. Implement the live or advanced interaction correctly. The experience needs VIX Advanced Chart (`vix_advanced`, advanced_charting) using `/udf` for tradingView advanced charting for VIX futures; default symbol `VIX`; update frequency `60000`. Organize it as app 'Vol Advanced' with tabs Chart (vix_advanced). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vol Advanced" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Vol Desk Data/vix_advanced` on tab `chart` → `missing_widget`

#### `vix_advanced_ship`

**hard** · category: platform · specification: -

> Build a volatility analyst a dependable volatility and derivatives workspace. The workspace must cover market history for VIX futures. The workspace must cover current volatility regime score. The workspace must cover daily CBOE VIX closes with returns. Analysts need to inspect date, close, return percentage. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Vol Advanced Live', 'VIX futures', 'Vol Desk Data', 'VX2', 'ticker'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Vol Advanced Live", "VIX futures", "Vol Desk Data", "VX2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `vix_room_chart_room`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for volatility and derivatives. The workspace must cover market history for VIX futures. The workspace must cover daily CBOE VIX closes with returns. Analysts need to inspect date, close, return percentage. An analyst can adjust the relevant numeric scope. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use `window_days` and `window` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vol_symbol_chart`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a volatility analyst covering volatility and derivatives. The workspace must cover market history for volatility futures. Keep these source-contract anchors: `venue`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### aggrid (20)

#### `alert_queue_app`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for cases and compliance alerts. The workspace must cover open surveillance alerts. Analysts need to inspect alert ID, desk, severity, age days. Leave the complete working workspace open for review. Use `severity` and `alert_id` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `auction_calendar`

**medium** · category: platform · specification: explicit

> Make the requested backend widget available and working in the current view. Use 'Rates Watch Data' at http://localhost:7803. Make the data grid behavior and columns usable. The experience needs Auction Calendar (`auction_calendar`, table) using `/auction-calendar` for upcoming treasury auctions; columns: date (dateString), security (text), size_bn (number). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Rates Watch Data/auction_calendar` → `missing_widget`

#### `auction_watch`

**hard** · category: platform · specification: partially-specified

> Create a usable rates and Treasury markets workflow for a rates strategist. The workspace must cover upcoming treasury auctions. Analysts need to inspect auction date, security, size billions, bid to cover. The source contract must retain `auction_date` and `security`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `case_aging`

**hard** · category: platform · specification: -

> The desk needs a production-ready cases and compliance alerts workflow for a surveillance analyst. The workspace must cover open surveillance cases by age bucket. The workspace must cover open surveillance alerts. The workspace must cover open alert count. Analysts need to inspect case ID, desk, age days, alert ID, severity. Leave the complete working workspace open for review. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `chain_flows`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a digital-assets analyst covering chain activity and liquidity. The workspace must cover net flows by chain. The workspace must cover current gas price snapshot. Analysts need to inspect chain, inflow USD, outflow USD, net percentage. Leave the complete working workspace open for review. Keep these source-contract anchors: `chain` and `inflow_usd`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `chains_table_app`

**medium** · category: platform · specification: explicit

> Publish the requested app and open it in Workspace to verify it works. Use 'Chain TVL Data' at http://localhost:7802. Make the data grid behavior and columns usable. The experience needs Top Chains by TVL (`chains_table`, table) using `/chains-table` for current TVL of all chains from the desk aggregator; columns: name (text), tvl_usd (number, int), change_1d (number, percent, greenRed). Organize it as app 'Chains Board' with tabs Overview (chains_table). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Chains Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Chain TVL Data/chains_table` on tab `overview` → `missing_widget`

#### `earnings_ship`

**hard** · category: platform · specification: -

> An equity-research analyst needs a decision-ready Workspace for earnings and estimates. The workspace must cover beat/miss by ticker this season. The workspace must cover average EPS surprise last 4 quarters. The workspace must cover preview note for the earnings call. Analysts need to inspect ticker, EPS surprise percentage, revenue beat. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Season Tracker', 'season', 'Earnings Prep Data', 'MSFT', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Season Tracker", "season", "Earnings Prep Data", "MSFT" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `estimates_ssrm`

**hard** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Earnings Prep Data' at http://localhost:7805. Make the data grid behavior and columns usable. The experience needs Estimates Explorer (SSRM) (`estimates_ssrm`, table_ssrm) using `/estimates-ssrm` for server-side sorted and filtered estimates dataset; user controls: Symbol (`symbol`, endpoint) from `/symbols`; data key `rows`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Earnings Prep Data/estimates_ssrm` → `missing_widget`

#### `execution_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready orders and venue quality workflow for an execution analyst. The workspace must cover execution quality by venue. The workspace must cover open execution exceptions. The workspace must cover slippage distribution by venue. Analysts need to inspect venue, fills, slippage percentage. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Execution Room', 'venues', 'Execution Desk Data', 'EDGX'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Execution Room", "venues", "Execution Desk Data", "EDGX" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `fill_quality`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an execution analyst covering orders and venue quality. The workspace must cover fill quality by venue. Analysts need to inspect venue, fills, slippage percentage, as of. Keep these source-contract anchors: `venue` and `fills`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `healthcare_ship`

**hard** · category: platform · specification: -

> A healthcare-research analyst needs a decision-ready Workspace for clinical catalysts and pipelines. The workspace must cover upcoming trial readouts. The workspace must cover catalysts in the next 30 days. The workspace must cover FDA decision and notice feed. Analysts need to inspect ticker, phase, readout. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Readout Desk', 'readouts', 'Healthcare Research Data', 'II'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Readout Desk", "readouts", "Healthcare Research Data", "II" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `latency_history`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for vendor service levels. The workspace must cover vendor latency history. The workspace must cover count of open SLA breaches. Analysts need to inspect vendor, day, latency milliseconds, breach. Leave the complete working workspace open for review. Use `vendor` and `day` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `open_orders`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Execution Desk Data' at http://localhost:7806. Make the data grid behavior and columns usable. The experience needs Open Orders (`open_orders`, table) using `/open-orders` for live open orders blotter; columns: order_id (text), symbol (text), qty (number, int), status (text, titleCase). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Execution Desk Data/open_orders` → `missing_widget`

#### `rates_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover upcoming treasury auctions. The workspace must cover current 2s10s spread in bps. The workspace must cover desk commentary on the rates day. Analysts need to inspect auction date, security, size billions. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Auction Desk', 'auctions', 'Rates Watch Data', '30Y Bond'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Auction Desk", "auctions", "Rates Watch Data", "30Y Bond" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `realized_screen`

**medium** · category: platform · specification: -

> Deliver an analyst-ready Workspace solution for volatility and derivatives. The workspace must cover realized volatility by tenor. Analysts need to inspect tenor, realized percentage, as of. Use `tenor` and `realized_pct` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `realized_vol_grid`

**hard** · category: platform · specification: -

> Build a volatility analyst a dependable volatility and derivatives workspace. The workspace must cover realized volatility by tenor. The workspace must cover term structure for VIX futures by expiry. The workspace must cover current volatility regime score. Analysts need to inspect tenor, realized percentage, as of. Leave the complete working workspace open for review. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `revision_grid`

**medium** · category: platform · specification: -

> Create a usable earnings and estimates workflow for an equity-research analyst. The workspace must cover street revision momentum by ticker. Analysts need to inspect ticker, revised up, revised down, momentum percentage. Large result sets must stay responsive while analysts filter and page through them. The source contract must retain `ticker` and `revised_up`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `trial_catalysts_app`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for clinical catalysts and pipelines. The workspace must cover upcoming clinical trial readouts. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Use `ticker` and `phase` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vendor_sla_table_app`

**medium** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Vendor SLA Data' at http://localhost:7804. Make the data grid behavior and columns usable. The experience needs Vendor SLA Status (`vendor_sla_table`, table) using `/vendor-sla` for vendor SLA state with breach flags; user controls: Status (`status`, text); columns: vendor (text), status (text, titleCase), latency_ms (number), breach (boolean). Organize it as app 'Vendor Ops' with tabs Vendors (vendor_sla_table). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vendor Ops" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Vendor SLA Data/vendor_sla_table` on tab `vendors` → `missing_widget`

#### `vix_history`

**medium** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Vol Desk Data' at http://localhost:7801. Make the data grid behavior and columns usable. The experience needs VIX History (`vix_history`, table) using `/vix-history` for daily CBOE VIX closes with returns; user controls: Window (`window`, number); columns: date (dateString), close (number), return_pct (number, percent, greenRed). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vol Desk Data/vix_history` → `missing_widget`

### apps (20)

#### `alert_metric_wrap`

**easy** · category: platform · specification: -

> Implement the requested app and confirm it by opening it in Workspace. Use 'Surveillance Data' at http://localhost:7807. Treat the app layout and navigation as the product outcome. The experience needs Open Alerts (`alert_metric`, metric) using `/alert-count` for open alert count. Organize it as app 'Alert Board' with tabs Alerts (alert_metric). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Alert Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Surveillance Data/alert_metric` on tab `alerts` → `missing_widget`

#### `case_command`

**hard** · category: platform · specification: -

> A surveillance analyst needs a decision-ready Workspace for cases and compliance alerts. The workspace must cover notes for one surveillance case. The workspace must cover open surveillance alerts. The workspace must cover open alert count. Analysts need to inspect alert ID, desk, severity, age days. Leave the complete working workspace open for review. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `catalyst_metric_wrap`

**hard** · category: platform · specification: partially-specified

> Create a usable clinical catalysts and pipelines workflow for a healthcare-research analyst. The workspace must cover catalysts in the next 30 days. Leave the complete working workspace open for review. The source contract must retain `Healthcare Research Data`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `chain_deck`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a digital-assets analyst covering chain activity and liquidity. The workspace must cover current TVL of all chains from the desk aggregator. The workspace must cover comparison of chain TVL. Analysts need to inspect name, TVL USD, change one-day. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `chain` and `name`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_command`

**hard** · category: platform · specification: partially-specified

> Create a usable the requested financial dataset workflow for an investment analyst. The workspace must cover holdings dataset for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. The workspace must cover sector Exposure for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. The workspace must cover portfolio Snapshot for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. Analysts need to inspect ticker, company, sector, weight, active weight, pnl, rating, bucket, value. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. The source contract must retain `fund` and `period`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_desk`

**hard** · category: platform · specification: -

> An equity-research analyst needs a decision-ready Workspace for earnings and estimates. The workspace must cover EPS beat and miss history. The workspace must cover street estimate revisions by quarter. The workspace must cover average EPS surprise last 4 quarters. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `gas_metric_wrap`

**hard** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Bench Stark Enterprise' at http://localhost:7809. Treat the app layout and navigation as the product outcome. The experience needs Risk Snapshot (`risk_exposure_monitor_dashboard_risk_snapshot`, metric) using `/risk_exposure_monitor_dashboard_risk_snapshot` for risk & Exposure Monitor (Risk User). Institutional demo view modeled on fund operating workflows; user controls: Portfolio (`portfolio`, text), Scenario (`scenario`, text), Period (`period`, text). Organize it as app 'Enterprise Risk Board' with tabs Risk (risk_exposure_monitor_dashboard_risk_snapshot). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Enterprise Risk Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/risk_exposure_monitor_dashboard_risk_snapshot` on tab `risk` → `missing_widget`

#### `healthcare_ship`

**hard** · category: platform · specification: -

> A healthcare-research analyst needs a decision-ready Workspace for clinical catalysts and pipelines. The workspace must cover upcoming clinical trial readouts. The workspace must cover catalysts in the next 30 days. The workspace must cover pipeline distribution by phase. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Trial Desk', 'catalysts', 'Healthcare Research Data', 'MRNA', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Trial Desk", "catalysts", "Healthcare Research Data", "MRNA" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `order_watch`

**hard** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Execution Desk Data' at http://localhost:7806. Treat the app layout and navigation as the product outcome. The experience needs Open Orders (`open_orders`, table) using `/open-orders` for live open orders blotter; columns: order_id (text), symbol (text), qty (number, int), status (text, titleCase); Exceptions (`exception_metric`, metric) using `/exception-count` for open execution exceptions. Organize it as app 'Order Watch' with tabs Orders (open_orders, exception_metric) with 2 starter prompt(s). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Order Watch" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Execution Desk Data/open_orders` on tab `orders` → `missing_widget`
- **Widget** ≥1× `Execution Desk Data/exception_metric` on tab `orders` → `missing_widget`

#### `rates_desk`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for the requested financial dataset. The workspace must cover holdings dataset for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. The workspace must cover exposure Treemap for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. Analysts need to inspect ticker, company, sector, weight, active weight, pnl, rating. An analyst can toggle the relevant screening constraint. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use `fund` and `period` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `rates_morning`

**hard** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Rates Watch Data' at http://localhost:7803. Treat the app layout and navigation as the product outcome. The experience needs Yield Curve (`yield_curve`, chart) using `/yield-curve` for plotly treasury yield curve snapshot; consume the raw backend payload; 2s10s Spread (`curve_spread_metric`, metric) using `/curve-spread` for current 2s10s spread in bps. Organize it as app 'Rates Morning' with tabs Morning (yield_curve, curve_spread_metric) with 2 starter prompt(s). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Rates Morning" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Rates Watch Data/yield_curve` on tab `morning` → `missing_widget`
- **Widget** ≥1× `Rates Watch Data/curve_spread_metric` on tab `morning` → `missing_widget`

#### `sla_ship`

**hard** · category: platform · specification: -

> Build a vendor-operations manager a dependable vendor service levels workspace. The workspace must cover count of open SLA breaches. The workspace must cover vendor SLA state with breach flags. The workspace must cover vendor incident notices feed. Analysts need to inspect vendor, status, latency milliseconds, breach. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Vendor Live', 'vendors', 'Vendor SLA Data', 'detail'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Vendor Live", "vendors", "Vendor SLA Data", "detail" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `surprise_metric_wrap`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for earnings and estimates. The workspace must cover average EPS surprise last 4 quarters. Leave the complete working workspace open for review. Use `Earnings Prep Data` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `surveillance_morning`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a surveillance analyst covering cases and compliance alerts. The workspace must cover open surveillance alerts. The workspace must cover notes for one surveillance case. The workspace must cover open alert count. Analysts need to inspect alert ID, desk, severity, age days. Leave the complete working workspace open for review. Keep these source-contract anchors: `severity` and `case_id`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `tvl_ship`

**hard** · category: platform · specification: -

> A digital-assets analyst needs a decision-ready Workspace for chain activity and liquidity. The workspace must cover current TVL of all chains from the desk aggregator. The workspace must cover current gas price snapshot. The workspace must cover comparison of chain TVL. Analysts need to inspect name, TVL USD, change one-day. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Chain Live', 'chains', 'Chain TVL Data', 'Solana'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Chain Live", "chains", "Chain TVL Data", "Solana" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `vendor_board`

**medium** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Vendor SLA Data' at http://localhost:7804. Treat the app layout and navigation as the product outcome. The experience needs Vendor SLA Status (`vendor_sla_table`, table) using `/vendor-sla` for vendor SLA state with breach flags; user controls: Status (`status`, text); columns: vendor (text), status (text, titleCase), latency_ms (number), breach (boolean); Open Breaches (`breach_metric`, metric) using `/breach-count` for count of open SLA breaches. Organize it as app 'Vendor Board' with tabs Vendors (vendor_sla_table, breach_metric). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vendor Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Vendor SLA Data/vendor_sla_table` on tab `vendors` → `missing_widget`
- **Widget** ≥1× `Vendor SLA Data/breach_metric` on tab `vendors` → `missing_widget`

#### `vendor_command`

**medium** · category: platform · specification: -

> Build a working Workspace experience for a vendor-operations manager covering vendor service levels. The workspace must cover vendor SLA state with breach flags. The workspace must cover count of open SLA breaches. The workspace must cover vendor incident notices feed. Analysts need to inspect vendor, status, latency milliseconds, breach. Leave the complete working workspace open for review. Keep these source-contract anchors: `status` and `vendor`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vol_morning`

**medium** · category: platform · specification: -

> Deliver an analyst-ready Workspace solution for volatility and derivatives. The workspace must cover daily CBOE VIX closes with returns. The workspace must cover term structure for VIX futures by expiry. The workspace must cover current volatility regime score. Analysts need to inspect date, close, return percentage. An analyst can adjust the relevant numeric scope. Leave the complete working workspace open for review. Use `window` and `date` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vol_overview`

**hard** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Bench Stark Enterprise' at http://localhost:7809. Treat the app layout and navigation as the product outcome. The experience needs Holdings Table (`portfolio_command_center_holdings_holdings_table`, table) using `/portfolio_command_center_holdings_holdings_table` for portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows; user controls: Fund (`fund`, text), Period (`period`, text); columns: ticker (number, int), company (text), sector (text), weight (number, percent), active_weight (number, percent), pnl (number, int, greenRed), rating (text); Portfolio Snapshot (`portfolio_command_center_overview_portfolio_snapshot`, metric) using `/portfolio_command_center_overview_portfolio_snapshot` for portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows; user controls: Fund (`fund`, text), Period (`period`, text). Organize it as app 'Enterprise Portfolio Control' with tabs Overview (portfolio_command_center_holdings_holdings_table, portfolio_command_center_overview_portfolio_snapshot) with 2 starter prompt(s). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Enterprise Portfolio Control" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_holdings_holdings_table` on tab `overview` → `missing_widget`
- **Widget** ≥1× `Bench Stark Enterprise/portfolio_command_center_overview_portfolio_snapshot` on tab `overview` → `missing_widget`

#### `vol_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready the requested financial dataset workflow for an investment analyst. The workspace must cover holdings dataset for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. The workspace must cover portfolio Snapshot for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. The workspace must cover exposure Treemap for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. Analysts need to inspect ticker, company, sector, weight, active weight, pnl, rating. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Enterprise Portfolio Live', 'enterprise portfolio', 'Bench Stark Enterprise', 'Flagship Long/Short'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

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
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `chains_highchart`

**medium** · category: platform · specification: explicit

> Make the requested backend widget available and working in the current view. Use 'Chain TVL Data' at http://localhost:7802. Choose a working chart representation for the data. The experience needs TVL by Chain (Highcharts) (`chains_highchart`, chart-highcharts) using `/chains-highchart` for highcharts rendering of chain TVL; cache for 15 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Chain TVL Data/chains_highchart` → `missing_widget`

#### `chains_highchart_app`

**medium** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Chain TVL Data' at http://localhost:7802. Choose a working chart representation for the data. The experience needs TVL by Chain (Highcharts) (`chains_highchart`, chart-highcharts) using `/chains-highchart` for highcharts rendering of chain TVL. Organize it as app 'Chain Highchart' with tabs Chains (chains_highchart). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Chain Highchart" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Chain TVL Data/chains_highchart` on tab `chains` → `missing_widget`

#### `chains_highchart_room`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for chain activity and liquidity. The workspace must cover comparisons of chain TVL. The workspace must cover current TVL of all chains from the desk aggregator. Analysts need to inspect name, TVL USD, change one-day. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use `chain_scope` and `name` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_chart`

**hard** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Earnings Prep Data' at http://localhost:7805. Choose a working chart representation for the data. The experience needs EPS History (`earnings_chart`, chart) using `/eps-history` for plotly EPS beat/miss history; user controls: Symbol (`symbol`, endpoint) from `/symbols`; cache for 15 minutes; consume the raw backend payload. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Earnings Prep Data/earnings_chart` → `missing_widget`

#### `earnings_chart_app`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover EPS beat and miss history. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Keep these source-contract anchors: `symbol`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_chart_room`

**hard** · category: platform · specification: -

> The desk needs a production-ready earnings and estimates workflow for an equity-research analyst. The workspace must cover EPS beat and miss history. The workspace must cover street estimate revisions by quarter. The workspace must cover average EPS surprise last 4 quarters. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_ship`

**hard** · category: platform · specification: -

> An equity-research analyst needs a decision-ready Workspace for earnings and estimates. The workspace must cover EPS beat and miss history. The workspace must cover average EPS surprise last 4 quarters. The workspace must cover street estimate revisions by quarter. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Earnings Chart Live', 'earnings history', 'Earnings Prep Data', 'MSFT', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Earnings Chart Live", "earnings history", "Earnings Prep Data", "MSFT" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `healthcare_ship`

**hard** · category: platform · specification: -

> A healthcare-research analyst needs a decision-ready Workspace for clinical catalysts and pipelines. The workspace must cover distribution of pipeline phase mix. The workspace must cover catalysts in the next 30 days. The workspace must cover upcoming clinical trial readouts. Analysts need to inspect ticker, phase, readout date. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Pipeline Chart Live', 'pipeline phases', 'Healthcare Research Data', 'III', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Pipeline Chart Live", "pipeline phases", "Healthcare Research Data", "III" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `phase_mix_vegalite`

**hard** · category: platform · specification: partially-specified

> Create a usable clinical catalysts and pipelines workflow for a healthcare-research analyst. The workspace must cover vega-Lite phase mix analysis. The source contract must retain `phase`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `pipeline_vegalite`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Healthcare Research Data' at http://localhost:7808. Choose a working chart representation for the data. The experience needs Pipeline Mix (Vega-Lite) (`pipeline_vegalite`, chart-vegalite) using `/pipeline-vegalite` for vega-Lite bar spec of pipeline phase mix; cache for 30 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Healthcare Research Data/pipeline_vegalite` → `missing_widget`

#### `pipeline_vegalite_app`

**hard** · category: platform · specification: partially-specified

> Create a usable clinical catalysts and pipelines workflow for a healthcare-research analyst. The workspace must cover distribution of pipeline phase mix. Leave the complete working workspace open for review. The source contract must retain `phase`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `pipeline_vegalite_room`

**hard** · category: platform · specification: -

> The desk needs a production-ready clinical catalysts and pipelines workflow for a healthcare-research analyst. The workspace must cover distribution of pipeline phase mix. The workspace must cover upcoming clinical trial readouts. The workspace must cover catalysts in the next 30 days. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `rates_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover the Treasury yield curve. The workspace must cover current 2s10s spread in bps. The workspace must cover desk commentary on the rates day. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Rates Chart Live', 'yield curve', 'Rates Watch Data', '5s30s'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Rates Chart Live", "yield curve", "Rates Watch Data", "5s30s" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `symbol_momentum_chart`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for earnings and estimates. The workspace must cover plotly momentum analysis by symbol. An analyst can filter the analysis by ticker. Use `symbol` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `tvl_ship`

**hard** · category: platform · specification: -

> A digital-assets analyst needs a decision-ready Workspace for chain activity and liquidity. The workspace must cover comparisons of chain TVL. The workspace must cover current gas price snapshot. The workspace must cover current TVL of all chains from the desk aggregator. Analysts need to inspect name, TVL USD, change one-day. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Chain Chart Live', 'chain TVL', 'Chain TVL Data', 'Solana'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Chain Chart Live", "chain TVL", "Chain TVL Data", "Solana" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `venue_slippage_chart`

**hard** · category: platform · specification: partially-specified

> Create a usable orders and venue quality workflow for an execution analyst. The workspace must cover plotly slippage analysis by venue. The source contract must retain `venue`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `yield_curve`

**hard** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Rates Watch Data' at http://localhost:7803. Choose a working chart representation for the data. The experience needs Yield Curve (`yield_curve`, chart) using `/yield-curve` for plotly treasury yield curve snapshot; cache for 15 minutes; consume the raw backend payload. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Rates Watch Data/yield_curve` → `missing_widget`

#### `yield_curve_app`

**hard** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Rates Watch Data' at http://localhost:7803. Choose a working chart representation for the data. The experience needs Yield Curve (`yield_curve`, chart) using `/yield-curve` for plotly treasury yield curve snapshot; consume the raw backend payload. Organize it as app 'Yield Curve App' with tabs Curve (yield_curve). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Yield Curve App" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Rates Watch Data/yield_curve` on tab `curve` → `missing_widget`

#### `yield_curve_room`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for rates and Treasury markets. The workspace must cover the Treasury yield curve. The workspace must cover current 2s10s spread in bps. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use `curve_scope` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### debug (24)

#### `execution_broken_group`

**medium** · category: repair · specification: open-brief

> Execution analysts report that changing review scope no longer keeps the overview and detail aligned in Execution Recovery Room. Diagnose the existing Execution Repair Data connection, repair it in place, and retest the affected workflow with live data before handing it back. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification note that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_dangling_app`

**easy** · category: repair · specification: partially-specified

> An incident in Execution Recovery Room means the detail tab opens to an empty space after a retired panel was removed. Investigate the connected Execution Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification note that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_data_mismatch`

**hard** · category: repair · specification: partially-specified

> An incident in Execution Recovery Room means the overview loads but a declared analyst field is absent. Investigate the connected Execution Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification HTML card that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_duplicate_backend`

**hard** · category: repair · specification: partially-specified

> An incident in Execution Recovery Room means two identically named backend connections now compete for the app. Investigate the connected Execution Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification note that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "delete"} must appear in the trace → `missing_tool_call`

#### `execution_invalid_widget`

**hard** · category: repair · specification: partially-specified

> Restore Execution Recovery Room for execution analysts: one panel disappeared after a backend definition update. Work through the existing Execution Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification note that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_silent_second_tab`

**easy** · category: repair · specification: open-brief

> An incident in Execution Recovery Room means the primary view works while a secondary view silently fails to load. Investigate the connected Execution Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification note that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 42 · oracle reference trace: 17 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_wrong_form_endpoint`

**easy** · category: repair · specification: open-brief

> An incident in Execution Recovery Room means the intake form accepts input but submission does nothing. Investigate the connected Execution Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification note that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `execution_wrong_live_row_id`

**hard** · category: repair · specification: -

> Restore Execution Recovery Room for execution analysts: live updates overwrite the wrong rows and make the queue unstable. Work through the existing Execution Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Execution Recovery Room open and add a short verification HTML card that naturally mentions Execution Recovery Room, Execution Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Execution Recovery Room", "Execution Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `surveillance_broken_group`

**easy** · category: repair · specification: open-brief

> An incident in Surveillance Recovery Room means changing review scope no longer keeps the overview and detail aligned. Investigate the connected Surveillance Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification note that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `surveillance_dangling_app`

**easy** · category: repair · specification: partially-specified

> An incident in Surveillance Recovery Room means the detail tab opens to an empty space after a retired panel was removed. Investigate the connected Surveillance Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification note that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `surveillance_data_mismatch`

**medium** · category: repair · specification: -

> Surveillance analysts report that the overview loads but a declared analyst field is absent in Surveillance Recovery Room. Diagnose the existing Surveillance Repair Data connection, repair it in place, and retest the affected workflow with live data before handing it back. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification note that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `surveillance_duplicate_backend`

**hard** · category: repair · specification: partially-specified

> An incident in Surveillance Recovery Room means two identically named backend connections now compete for the app. Investigate the connected Surveillance Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification note that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "delete"} must appear in the trace → `missing_tool_call`

#### `surveillance_invalid_widget`

**hard** · category: repair · specification: partially-specified

> An incident in Surveillance Recovery Room means one panel disappeared after a backend definition update. Investigate the connected Surveillance Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification HTML card that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `surveillance_silent_second_tab`

**hard** · category: repair · specification: -

> Restore Surveillance Recovery Room for surveillance analysts: the primary view works while a secondary view silently fails to load. Work through the existing Surveillance Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification HTML card that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 42 · oracle reference trace: 17 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `surveillance_wrong_form_endpoint`

**medium** · category: repair · specification: open-brief

> Restore Surveillance Recovery Room for surveillance analysts: the intake form accepts input but submission does nothing. Work through the existing Surveillance Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification note that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `surveillance_wrong_live_row_id`

**easy** · category: repair · specification: open-brief

> Restore Surveillance Recovery Room for surveillance analysts: live updates overwrite the wrong rows and make the queue unstable. Work through the existing Surveillance Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Surveillance Recovery Room open and add a short verification note that naturally mentions Surveillance Recovery Room, Surveillance Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Surveillance Recovery Room", "Surveillance Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_broken_group`

**hard** · category: repair · specification: -

> An incident in Vendor Recovery Room means changing review scope no longer keeps the overview and detail aligned. Investigate the connected Vendor Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification HTML card that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_dangling_app`

**easy** · category: repair · specification: partially-specified

> Restore Vendor Recovery Room for vendor operations analysts: the detail tab opens to an empty space after a retired panel was removed. Work through the existing Vendor Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification note that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_data_mismatch`

**medium** · category: repair · specification: -

> Restore Vendor Recovery Room for vendor operations analysts: the overview loads but a declared analyst field is absent. Work through the existing Vendor Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification note that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_duplicate_backend`

**hard** · category: repair · specification: partially-specified

> Restore Vendor Recovery Room for vendor operations analysts: two identically named backend connections now compete for the app. Work through the existing Vendor Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification HTML card that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Tool call** ≥1× `manage_backends` with args ⊇ {"operation": "delete"} must appear in the trace → `missing_tool_call`

#### `vendor_invalid_widget`

**hard** · category: repair · specification: partially-specified

> Vendor operations analysts report that one panel disappeared after a backend definition update in Vendor Recovery Room. Diagnose the existing Vendor Repair Data connection, repair it in place, and retest the affected workflow with live data before handing it back. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification HTML card that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_silent_second_tab`

**easy** · category: repair · specification: open-brief

> An incident in Vendor Recovery Room means the primary view works while a secondary view silently fails to load. Investigate the connected Vendor Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification note that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 42 · oracle reference trace: 17 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_wrong_form_endpoint`

**medium** · category: repair · specification: open-brief

> An incident in Vendor Recovery Room means the intake form accepts input but submission does nothing. Investigate the connected Vendor Repair Data backend, make the smallest in-place repair, and prove the workflow against live data. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification note that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

#### `vendor_wrong_live_row_id`

**hard** · category: repair · specification: -

> Restore Vendor Recovery Room for vendor operations analysts: live updates overwrite the wrong rows and make the queue unstable. Work through the existing Vendor Repair Data connection, repair the root cause without replacing healthy content, and run a live-data retest. Keep the Operations Handbook, the archive workspace, and every unrelated app byte-for-byte unchanged. Leave Vendor Recovery Room open and add a short verification HTML card that naturally mentions Vendor Recovery Room, Vendor Repair Data, and repair verified.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 40 · oracle reference trace: 16 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× named ~"Verification" whose content mentions "Vendor Recovery Room", "Vendor Repair Data", "repair verified" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`

### e2e (12)

#### `case_triage`

**hard** · category: platform · specification: -

> A surveillance analyst needs a decision-ready Workspace for cases and compliance alerts. The workspace must cover case owners, priorities, and SLA days. The workspace must cover notes for one surveillance case. Analysts need to inspect case ID, owner, priority, SLA days. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Case Triage', 'Surveillance Data', 'C-1048'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Case Triage", "case triage", "Surveillance Data", "C-1048" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `catalyst_calendar`

**hard** · category: platform · specification: -

> Build a healthcare-research analyst a dependable clinical catalysts and pipelines workspace. The workspace must cover healthcare catalysts and impact scores. The workspace must cover catalysts in the next 30 days. Analysts need to inspect ticker, event, event date, impact score. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Catalyst Calendar', 'Healthcare Research Data', 'PFE', 'ticker'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Catalyst Calendar", "catalyst calendar", "Healthcare Research Data", "PFE" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `chain_flows`

**hard** · category: platform · specification: -

> A digital-assets analyst needs a decision-ready Workspace for chain activity and liquidity. The workspace must cover net chain flows and fee share. The workspace must cover current gas price snapshot. Analysts need to inspect chain, net flow USD, fee percentage, as of. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Chain Flows', 'Chain TVL Data', 'Solana'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Chain Flows", "chain flows", "Chain TVL Data", "Solana" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `compliance_surveillance`

**hard** · category: platform · specification: -

> The desk needs a production-ready cases and compliance alerts workflow for a surveillance analyst. The workspace must cover open surveillance cases by severity. The workspace must cover open alert count. Analysts need to inspect case ID, desk, severity, age days. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Compliance Surveillance', 'surveillance', 'Surveillance Data', 'C-1044'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Compliance Surveillance", "surveillance", "Surveillance Data", "C-1044" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `earnings_season`

**hard** · category: platform · specification: -

> An equity-research analyst needs a decision-ready Workspace for earnings and estimates. The workspace must cover earnings surprises and report dates. The workspace must cover average EPS surprise last 4 quarters. Analysts need to inspect ticker, EPS surprise percentage, revenue beat, report date. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Earnings Season', 'Earnings Prep Data', 'MSFT', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Earnings Season", "earnings season", "Earnings Prep Data", "MSFT" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `execution_monitor`

**hard** · category: platform · specification: -

> An execution analyst needs a decision-ready Workspace for orders and venue quality. The workspace must cover venue execution quality and rejects. The workspace must cover open execution exceptions. Analysts need to inspect venue, orders, reject rate percentage, as of. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Execution Monitor', 'Execution Desk Data', 'EDGX'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Execution Monitor", "execution monitor", "Execution Desk Data", "EDGX" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `healthcare_pipeline`

**hard** · category: platform · specification: -

> Build a healthcare-research analyst a dependable clinical catalysts and pipelines workspace. The workspace must cover healthcare pipeline programs by phase. The workspace must cover pipeline distribution by phase. Analysts need to inspect ticker, phase, programs, readout date. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Healthcare Pipeline', 'pipeline', 'Healthcare Research Data', 'MRNA', 'ticker'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Healthcare Pipeline", "pipeline", "Healthcare Research Data", "MRNA" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `macro_morning`

**hard** · category: platform · specification: -

> Build a rates strategist a dependable rates and Treasury markets workspace. The workspace must cover rates morning levels and changes. The workspace must cover the Treasury yield curve. Analysts need to inspect series, level, change bp, as of. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Macro Morning', 'Rates Watch Data', 'DGS2'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Macro Morning", "macro morning", "Rates Watch Data", "DGS2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `rates_auctions`

**hard** · category: platform · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover upcoming auctions and demand metrics. The workspace must cover current 2s10s spread in bps. Analysts need to inspect auction date, security, size billions, bid to cover. An analyst can choose the relevant business date. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Rates Auctions', 'Rates Watch Data', '2026-07-15', 'date'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Rates Auctions", "rates auctions", "Rates Watch Data", "2026-07-15" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `research_room`

**hard** · category: platform · specification: -

> Build an investment analyst a dependable the requested financial dataset workspace. The workspace must cover analyst research actions by ticker. The workspace must cover sector Exposure for Portfolio Command Center (Portfolio Manager). Institutional demo view modeled on fund operating workflows. Analysts need to inspect ticker, analyst, rating, upside percentage, bucket, value. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Research Room', 'Bench Stark Enterprise', 'MSFT', 'ticker'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Research Room", "research room", "Bench Stark Enterprise", "MSFT" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `vendor_ops`

**hard** · category: platform · specification: -

> The desk needs a production-ready vendor service levels workflow for a vendor-operations manager. The workspace must cover vendor uptime and latency posture. The workspace must cover count of open SLA breaches. Analysts need to inspect vendor, uptime percentage, latency milliseconds, status. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Vendor Ops', 'Vendor SLA Data', 'QuoteStream'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Vendor Ops", "vendor ops", "Vendor SLA Data", "QuoteStream" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `vol_cockpit`

**hard** · category: platform · specification: -

> A volatility analyst needs a decision-ready Workspace for volatility and derivatives. The workspace must cover implied and realized volatility by tenor. The workspace must cover market history for VIX futures. Analysts need to inspect tenor, iv percentage, realized percentage, as of. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Vol Cockpit', 'Vol Desk Data', '3M'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

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
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Healthcare Research Data/pipeline_chart` → `missing_widget`

#### `add_curve_spread_metric`

**easy** · category: repair · specification: -

> Make the requested backend widget available and working in the current view. Use 'Rates Watch Data' at http://localhost:7803. Repair the existing backend without regressing working content. The experience needs Yield Curve (`yield_curve`, chart) using `/yield-curve` for plotly treasury yield curve snapshot; consume the raw backend payload; 2s10s Spread (`curve_spread_metric`, metric) using `/curve-spread` for current 2s10s spread in bps; cache for 15 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Rates Watch Data/yield_curve` → `missing_widget`

#### `add_exception_metric`

**easy** · category: repair · specification: -

> Make the requested backend widget available and working in the current view. Use 'Execution Desk Data' at http://localhost:7806. Repair the existing backend without regressing working content. The experience needs Open Orders (`open_orders`, table) using `/open-orders` for live open orders blotter; columns: order_id (text), symbol (text), qty (number, int), status (text, titleCase); Exceptions (`exception_metric`, metric) using `/exception-count` for open execution exceptions; cache for 15 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Execution Desk Data/open_orders` → `missing_widget`

#### `add_vol_regime_metric`

**hard** · category: repair · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Vol Desk Data' at http://localhost:7801. Repair the existing backend without regressing working content. The experience needs VIX Term Structure (`vix_term_structure`, chart) using `/vix-term-structure` for plotly curve of VIX futures by expiry; consume the raw backend payload; Vol Regime (`vol_regime_metric`, metric) using `/vol-regime` for current volatility regime score; cache for 15 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 8 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vol Desk Data/vix_term_structure` → `missing_widget`

#### `diagnose_earnings`

**hard** · category: repair · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. The workspace must cover average EPS surprise last 4 quarters. The workspace must cover preview note for the earnings call. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. Keep these source-contract anchors: `symbol` and `quarter`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `diagnose_healthcare`

**hard** · category: repair · specification: partially-specified

> Deliver an analyst-ready Workspace solution for clinical catalysts and pipelines. The workspace must cover upcoming clinical trial readouts. The workspace must cover distribution of pipeline phase mix. The workspace must cover FDA decision and notice feed. The workspace must cover catalysts in the next 30 days. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. Use `ticker` and `phase` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `diagnose_rates`

**hard** · category: repair · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover upcoming treasury auctions. The workspace must cover desk commentary on the rates day. The workspace must cover current 2s10s spread in bps. The workspace must cover the Treasury yield curve. Analysts need to inspect date, security, size billions. Preserve all working content while correcting the requested workflow. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `diagnose_sla`

**hard** · category: repair · specification: -

> Build a vendor-operations manager a dependable vendor service levels workspace. The workspace must cover vendor SLA state with breach flags. The workspace must cover count of open SLA breaches. The workspace must cover vendor incident notices feed. The workspace must cover runbook for SLA escalations. Analysts need to inspect vendor, status, latency milliseconds, breach. Preserve all working content while correcting the requested workflow. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `modify_case_notes`

**hard** · category: repair · specification: partially-specified

> Create a usable cases and compliance alerts workflow for a surveillance analyst. The workspace must cover notes for one surveillance case. The workspace must cover open alert count. The source contract must retain `case_id`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `modify_rates_commentary`

**hard** · category: repair · specification: partially-specified

> Create a usable rates and Treasury markets workflow for a rates strategist. The workspace must cover desk commentary on the rates day. The workspace must cover current 2s10s spread in bps. The source contract must retain `series`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `modify_trial_catalysts`

**hard** · category: repair · specification: partially-specified

> Deliver an analyst-ready Workspace solution for clinical catalysts and pipelines. The workspace must cover upcoming clinical trial readouts. The workspace must cover catalysts in the next 30 days. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. Use `ticker` and `phase` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `modify_vol_screener`

**hard** · category: repair · specification: partially-specified

> Deliver an analyst-ready Workspace solution for volatility and derivatives. The workspace must cover screen names by implied-vol criteria. The workspace must cover current volatility regime score. An analyst can filter the analysis by ticker. An analyst can choose the relevant business date. An analyst can toggle the relevant screening constraint. Use `ticker` and `as_of` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `place_alert_metric`

**hard** · category: repair · specification: partially-specified

> Create a usable cases and compliance alerts workflow for a surveillance analyst. The workspace must cover open surveillance alerts. The workspace must cover open alert count. Analysts need to inspect alert ID, desk, severity, age days. Leave the complete working workspace open for review. The source contract must retain `severity` and `alert_id`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `place_breach_metric`

**hard** · category: repair · specification: partially-specified

> Create a usable vendor service levels workflow for a vendor-operations manager. The workspace must cover vendor SLA state with breach flags. The workspace must cover count of open SLA breaches. Analysts need to inspect vendor, status, latency milliseconds, breach. Leave the complete working workspace open for review. The source contract must retain `status` and `vendor`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `place_curve_spread_metric`

**medium** · category: repair · specification: explicit

> Publish the requested app and open it in Workspace to verify it works. Use 'Rates Watch Data' at http://localhost:7803. Repair the existing backend without regressing working content. The experience needs Auction Calendar (`auction_calendar`, table) using `/auction-calendar` for upcoming treasury auctions; columns: date (dateString), security (text), size_bn (number); 2s10s Spread (`curve_spread_metric`, metric) using `/curve-spread` for current 2s10s spread in bps. Organize it as app 'Auction Review' with tabs Auctions (auction_calendar, curve_spread_metric). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Auction Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Rates Watch Data/auction_calendar` on tab `auctions` → `missing_widget`
- **Widget** ≥1× `Rates Watch Data/curve_spread_metric` on tab `auctions` → `missing_widget`

#### `place_vol_regime_metric`

**medium** · category: repair · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Vol Desk Data' at http://localhost:7801. Repair the existing backend without regressing working content. The experience needs VIX History (`vix_history`, table) using `/vix-history` for daily CBOE VIX closes with returns; user controls: Window (`window`, number); columns: date (dateString), close (number), return_pct (number, percent, greenRed); Vol Regime (`vol_regime_metric`, metric) using `/vol-regime` for current volatility regime score. Organize it as app 'Vol Review' with tabs Overview (vix_history, vol_regime_metric). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vol Review" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Vol Desk Data/vix_history` on tab `overview` → `missing_widget`
- **Widget** ≥1× `Vol Desk Data/vol_regime_metric` on tab `overview` → `missing_widget`

#### `repair_compliance`

**hard** · category: repair · specification: -

> The desk needs a production-ready cases and compliance alerts workflow for a surveillance analyst. The workspace must cover ask questions over the surveillance case corpus. The workspace must cover open alert count. Leave the complete working workspace open for review. Preserve all working content while correcting the requested workflow. Add a short completion note that naturally includes the desk-required terms 'Case Repair Live', 'case repair', 'Surveillance Data', 'Show high severity cases'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Case Repair Live", "case repair", "Surveillance Data", "Show high severity cases" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `repair_execution`

**hard** · category: repair · specification: -

> The desk needs a production-ready orders and venue quality workflow for an execution analyst. The workspace must cover live order activity. The workspace must cover open execution exceptions. Analysts need to inspect order ID, price. Large result sets must stay responsive while analysts filter and page through them. Leave the complete working workspace open for review. Preserve all working content while correcting the requested workflow. Add a short completion HTML card that naturally includes the desk-required terms 'Execution Repair Live', 'execution repair', 'Execution Desk Data', 'EDGX'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Execution Repair Live", "execution repair", "Execution Desk Data", "EDGX" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `repair_rates`

**hard** · category: repair · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover desk commentary on the rates day. The workspace must cover current 2s10s spread in bps. Leave the complete working workspace open for review. Preserve all working content while correcting the requested workflow. Add a short completion HTML card that naturally includes the desk-required terms 'Rates Repair Live', 'rates repair', 'Rates Watch Data', 'DGS2'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Rates Repair Live", "rates repair", "Rates Watch Data", "DGS2" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `repair_vol`

**hard** · category: repair · specification: -

> A volatility analyst needs a decision-ready Workspace for volatility and derivatives. The workspace must cover market history for VIX futures. The workspace must cover current volatility regime score. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Preserve all working content while correcting the requested workflow. Add a short completion note that naturally includes the desk-required terms 'Vol Repair Live', 'vol regime', 'Vol Desk Data', 'VX2', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 5 calls

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
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Surveillance Data/access_review_form` → `missing_widget`

#### `case_escalation_form_app`

**hard** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Surveillance Data' at http://localhost:7807. Make the submission workflow functional. The experience needs Case Escalation Form (`case_escalation_form`, table) using `/case-escalation` for escalate a surveillance case to a reviewer; user controls: Escalation (`escalation`, form) with Case, Due date, Escalate. Organize it as app 'Case Escalation' with tabs Cases (case_escalation_form). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Case Escalation" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Surveillance Data/case_escalation_form` on tab `cases` → `missing_widget`

#### `case_intake_room`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a surveillance analyst covering cases and compliance alerts. The workspace must cover escalate a surveillance case to a reviewer. The workspace must cover open surveillance alerts. Analysts need to inspect alert ID, desk, severity, age days. An analyst can choose the relevant business date. The user can enter the required details and submit the workflow. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `escalation` and `case_id`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `compliance_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready cases and compliance alerts workflow for a surveillance analyst. The workspace must cover escalate a surveillance case to a reviewer. The workspace must cover open alert count. The workspace must cover open surveillance alerts. Analysts need to inspect alert ID, desk, severity, age days. An analyst can choose the relevant business date. The user can enter the required details and submit the workflow. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Case Intake Live', 'case intake', 'Surveillance Data', 'C-1044', 'date'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Case Intake Live", "case intake", "Surveillance Data", "C-1044" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `curve_comment_form_app`

**hard** · category: platform · specification: partially-specified

> Create a usable rates and Treasury markets workflow for a rates strategist. The workspace must cover submit a curve desk comment. The user can enter the required details and submit the workflow. Leave the complete working workspace open for review. The source contract must retain `comment` and `series`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `exception_intake_room`

**hard** · category: platform · specification: -

> An execution analyst needs a decision-ready Workspace for orders and venue quality. The workspace must cover record an execution venue exception. The workspace must cover live open orders blotter. The workspace must cover open execution exceptions. Analysts need to inspect order ID, symbol, quantity, status. An analyst can adjust the relevant numeric scope. The user can enter the required details and submit the workflow. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `execution_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready orders and venue quality workflow for an execution analyst. The workspace must cover record an execution venue exception. The workspace must cover open execution exceptions. The workspace must cover live open orders blotter. Analysts need to inspect order ID, symbol, quantity, status. An analyst can adjust the relevant numeric scope. The user can enter the required details and submit the workflow. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Exception Intake Live', 'exception intake', 'Execution Desk Data', 'EDGX'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Exception Intake Live", "exception intake", "Execution Desk Data", "EDGX" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `healthcare_ship`

**hard** · category: platform · specification: -

> A healthcare-research analyst needs a decision-ready Workspace for clinical catalysts and pipelines. The workspace must cover capture a clinical trial readout note. The workspace must cover catalysts in the next 30 days. The workspace must cover upcoming clinical trial readouts. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. An analyst can choose the relevant business date. The user can enter the required details and submit the workflow. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Trial Intake Live', 'trial intake', 'Healthcare Research Data', 'MRNA', 'ticker', 'date'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Trial Intake Live", "trial intake", "Healthcare Research Data", "MRNA" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `incident_triage_form`

**hard** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Vendor SLA Data' at http://localhost:7804. Make the submission workflow functional. The experience needs Incident Triage Form (`incident_triage_form`, table) using `/incident-triage` for submit an incident triage record for review; user controls: Triage (`triage`, form) with Incident, Review date, Submit. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vendor SLA Data/incident_triage_form` → `missing_widget`

#### `policy_exception_form`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a surveillance analyst covering cases and compliance alerts. The workspace must cover submit a policy exception request. The user can enter the required details and submit the workflow. Keep these source-contract anchors: `exception` and `policy_id`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `sla_ship`

**hard** · category: platform · specification: -

> Build a vendor-operations manager a dependable vendor service levels workspace. The workspace must cover submit a new vendor record into the SLA register. The workspace must cover count of open SLA breaches. The workspace must cover vendor SLA state with breach flags. Analysts need to inspect vendor, status, latency milliseconds, breach. An analyst can adjust the relevant numeric scope. The user can enter the required details and submit the workflow. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Vendor Intake Live', 'vendor intake', 'Vendor SLA Data', 'QuoteStream'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Vendor Intake Live", "vendor intake", "Vendor SLA Data", "QuoteStream" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `threshold_update_form`

**hard** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Execution Desk Data' at http://localhost:7806. Make the submission workflow functional. The experience needs Threshold Update Form (`threshold_update_form`, table) using `/threshold-update` for submit a threshold change for operations; user controls: Threshold (`threshold`, form) with Limit, Owner, Apply. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Execution Desk Data/threshold_update_form` → `missing_widget`

#### `trade_break_form`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for orders and venue quality. The workspace must cover record a trade break for operations review. An analyst can adjust the relevant numeric scope. The user can enter the required details and submit the workflow. Use `break_item` and `trade_id` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `trial_intake_room`

**hard** · category: platform · specification: -

> Build a healthcare-research analyst a dependable clinical catalysts and pipelines workspace. The workspace must cover capture a clinical trial readout note. The workspace must cover upcoming clinical trial readouts. The workspace must cover catalysts in the next 30 days. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. An analyst can choose the relevant business date. The user can enter the required details and submit the workflow. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `trial_readout_form`

**hard** · category: platform · specification: partially-specified

> Create a usable clinical catalysts and pipelines workflow for a healthcare-research analyst. The workspace must cover capture a clinical trial readout note. An analyst can filter the analysis by ticker. An analyst can choose the relevant business date. The user can enter the required details and submit the workflow. The source contract must retain `readout` and `ticker`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vendor_intake_form`

**hard** · category: platform · specification: explicit

> Make the requested backend widget available and working in the current view. Use 'Vendor SLA Data' at http://localhost:7804. Make the submission workflow functional. The experience needs Vendor Intake Form (`vendor_intake_form`, table) using `/vendor-intake` for submit a new vendor record into the SLA register; user controls: New Vendor (`intake`, form) with Vendor, Tier, Add Vendor. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vendor SLA Data/vendor_intake_form` → `missing_widget`

#### `vendor_intake_form_app`

**hard** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Vendor SLA Data' at http://localhost:7804. Make the submission workflow functional. The experience needs Vendor Intake Form (`vendor_intake_form`, table) using `/vendor-intake` for submit a new vendor record into the SLA register; user controls: New Vendor (`intake`, form) with Vendor, Tier, Add Vendor. Organize it as app 'Vendor Intake' with tabs Intake (vendor_intake_form). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vendor Intake" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Vendor SLA Data/vendor_intake_form` on tab `intake` → `missing_widget`

#### `vendor_intake_room`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a vendor-operations manager covering vendor service levels. The workspace must cover submit a new vendor record into the SLA register. The workspace must cover vendor SLA state with breach flags. Analysts need to inspect vendor, status, latency milliseconds, breach. An analyst can adjust the relevant numeric scope. The user can enter the required details and submit the workflow. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `intake` and `vendor`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vendor_review_form`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a vendor-operations manager covering vendor service levels. The workspace must cover create a vendor review item. An analyst can choose the relevant business date. The user can enter the required details and submit the workflow. Keep these source-contract anchors: `review` and `vendor_name`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `venue_exception_form_app`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an execution analyst covering orders and venue quality. The workspace must cover record an execution venue exception. An analyst can adjust the relevant numeric scope. The user can enter the required details and submit the workflow. Leave the complete working workspace open for review. Keep these source-contract anchors: `exception` and `venue`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### grouping (20)

#### `chart_note_board`

**medium** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Earnings Prep Data' at http://localhost:7805. Make the cross-widget interaction work. The experience needs EPS History (`earnings_chart`, chart) using `/eps-history` for plotly EPS beat/miss history; user controls: Symbol (`symbol`, endpoint) from `/symbols`; consume the raw backend payload; Earnings Preview (`earnings_note`, markdown) using `/earnings-preview` for preview note for the earnings call; user controls: Symbol (`symbol`, endpoint) from `/symbols`. Organize it as app 'Chart Note Board' with tabs Preview (earnings_chart, earnings_note) with shared interactions Preview Symbol Sync across earnings_chart, earnings_note via `symbol`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Chart Note Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Earnings Prep Data/earnings_chart` on tab `preview` → `missing_widget`
- **Widget** ≥1× `Earnings Prep Data/earnings_note` on tab `preview` → `missing_widget`

#### `chart_preview_sync`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover EPS beat and miss history. The workspace must cover preview note for the earnings call. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `symbol`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `chart_sync_live`

**hard** · category: platform · specification: -

> Build an equity-research analyst a dependable earnings and estimates workspace. The workspace must cover EPS beat and miss history. The workspace must cover preview note for the earnings call. The workspace must cover street estimate revisions by quarter. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Chart Sync Live', 'linked earnings selection', 'Earnings Prep Data', 'MSFT', 'ticker'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Chart Sync Live", "linked earnings selection", "Earnings Prep Data", "MSFT" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `click_preview_desk`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover preview rows whose symbol cell syncs the app. The workspace must cover preview note for the earnings call. Analysts need to inspect symbol, revision percentage. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `symbol` and `revision_pct`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `click_revision_desk`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for earnings and estimates. The workspace must cover revision rows whose symbol cell syncs the app. The workspace must cover EPS beat and miss history. Analysts need to inspect symbol, revision percentage. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use `symbol` and `revision_pct` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `click_season_desk`

**hard** · category: platform · specification: -

> The desk needs a production-ready earnings and estimates workflow for an equity-research analyst. The workspace must cover season rows whose ticker selection links to revisions. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. Analysts need to inspect symbol, revision percentage, quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `click_summary_desk`

**hard** · category: platform · specification: -

> The desk needs a production-ready earnings and estimates workflow for an equity-research analyst. The workspace must cover summary rows whose ticker selection stays linked across analysis. The workspace must cover EPS beat and miss history. The workspace must cover preview note for the earnings call. Analysts need to inspect symbol, revision percentage. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `click_sync_live`

**hard** · category: platform · specification: -

> Build an equity-research analyst a dependable earnings and estimates workspace. The workspace must cover clickable live symbol rows for grouped review. The workspace must cover EPS beat and miss history. The workspace must cover preview HTML card for the earnings call. Analysts need to inspect symbol, revision percentage. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Click Sync Live', 'click sync', 'Earnings Prep Data', 'AAPL', 'ticker'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Click Sync Live", "click sync", "Earnings Prep Data", "AAPL" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `earnings_chart_app`

**hard** · category: platform · specification: explicit

> Publish the requested app and open it in Workspace to verify it works. Use 'Earnings Prep Data' at http://localhost:7805. Make the cross-widget interaction work. The experience needs EPS History (`earnings_chart`, chart) using `/eps-history` for plotly EPS beat/miss history; user controls: Symbol (`symbol`, endpoint) from `/symbols`; consume the raw backend payload. Organize it as app 'Chart Group App' with tabs Chart (earnings_chart) with shared interactions Chart Symbol Group across earnings_chart via `symbol`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Chart Group App" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Earnings Prep Data/earnings_chart` on tab `chart` → `missing_widget`

#### `earnings_note_app`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover preview note for the earnings call. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Keep these source-contract anchors: `symbol`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_review_sync`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `symbol` and `quarter`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_symbol_board`

**hard** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Earnings Prep Data' at http://localhost:7805. Make the cross-widget interaction work. The experience needs Estimate Revisions (`estimate_revisions`, table) using `/estimate-revisions` for street estimate revisions by quarter; user controls: Symbol (`symbol`, endpoint) from `/symbols`; columns: quarter (text), eps_estimate (number), revenue_estimate_b (number); EPS History (`earnings_chart`, chart) using `/eps-history` for plotly EPS beat/miss history; user controls: Symbol (`symbol`, endpoint) from `/symbols`; consume the raw backend payload. Organize it as app 'Earnings Symbol Board' with tabs Review (estimate_revisions, earnings_chart) with shared interactions Symbol Sync across estimate_revisions, earnings_chart via `symbol`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Earnings Symbol Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Earnings Prep Data/estimate_revisions` on tab `review` → `missing_widget`
- **Widget** ≥1× `Earnings Prep Data/earnings_chart` on tab `review` → `missing_widget`

#### `earnings_sync_live`

**hard** · category: platform · specification: -

> Build an equity-research analyst a dependable earnings and estimates workspace. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. The workspace must cover preview note for the earnings call. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Earnings Sync Live', 'symbol sync', 'Earnings Prep Data', 'MSFT', 'ticker'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Earnings Sync Live", "symbol sync", "Earnings Prep Data", "MSFT" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `estimate_revisions_app`

**hard** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Earnings Prep Data' at http://localhost:7805. Make the cross-widget interaction work. The experience needs Estimate Revisions (`estimate_revisions`, table) using `/estimate-revisions` for street estimate revisions by quarter; user controls: Symbol (`symbol`, endpoint) from `/symbols`; columns: quarter (text), eps_estimate (number), revenue_estimate_b (number). Organize it as app 'Revision Group App' with tabs Revisions (estimate_revisions) with shared interactions Revision Symbol Group across estimate_revisions via `symbol`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Revision Group App" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Earnings Prep Data/estimate_revisions` on tab `revisions` → `missing_widget`

#### `full_earnings_sync`

**hard** · category: platform · specification: partially-specified

> Create a usable earnings and estimates workflow for an equity-research analyst. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. The workspace must cover preview note for the earnings call. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. The source contract must retain `symbol` and `quarter`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `nvda_review_board`

**hard** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Earnings Prep Data' at http://localhost:7805. Make the cross-widget interaction work. The experience needs Estimate Revisions (`estimate_revisions`, table) using `/estimate-revisions` for street estimate revisions by quarter; user controls: Symbol (`symbol`, endpoint) from `/symbols`; columns: quarter (text), eps_estimate (number), revenue_estimate_b (number); EPS History (`earnings_chart`, chart) using `/eps-history` for plotly EPS beat/miss history; user controls: Symbol (`symbol`, endpoint) from `/symbols`; consume the raw backend payload. Organize it as app 'NVDA Review Board' with tabs NVDA (estimate_revisions, earnings_chart) with shared interactions NVDA Symbol Sync across estimate_revisions, earnings_chart via `symbol`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "NVDA Review Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Earnings Prep Data/estimate_revisions` on tab `nvda` → `missing_widget`
- **Widget** ≥1× `Earnings Prep Data/earnings_chart` on tab `nvda` → `missing_widget`

#### `preview_sync_live`

**hard** · category: platform · specification: -

> The desk needs a production-ready earnings and estimates workflow for an equity-research analyst. The workspace must cover preview HTML card for the earnings call. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Preview Sync Live', 'preview sync', 'Earnings Prep Data', 'AAPL', 'ticker'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Preview Sync Live", "preview sync", "Earnings Prep Data", "AAPL" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `revision_note_board`

**hard** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Earnings Prep Data' at http://localhost:7805. Make the cross-widget interaction work. The experience needs Estimate Revisions (`estimate_revisions`, table) using `/estimate-revisions` for street estimate revisions by quarter; user controls: Symbol (`symbol`, endpoint) from `/symbols`; columns: quarter (text), eps_estimate (number), revenue_estimate_b (number); Earnings Preview (`earnings_note`, markdown) using `/earnings-preview` for preview note for the earnings call; user controls: Symbol (`symbol`, endpoint) from `/symbols`. Organize it as app 'Revision Note Board' with tabs Notes (estimate_revisions, earnings_note) with shared interactions Revision Symbol Sync across estimate_revisions, earnings_note via `symbol`. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Revision Note Board" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Earnings Prep Data/estimate_revisions` on tab `notes` → `missing_widget`
- **Widget** ≥1× `Earnings Prep Data/earnings_note` on tab `notes` → `missing_widget`

#### `revision_preview_sync`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover street estimate revisions by quarter. The workspace must cover preview note for the earnings call. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `symbol` and `quarter`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `symbol_click_summary_app`

**medium** · category: platform · specification: -

> Deliver an analyst-ready Workspace solution for earnings and estimates. The workspace must cover symbol rows that can drive a grouped app. Analysts need to inspect symbol, revision percentage. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Use `symbol` and `revision_pct` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### params (20)

#### `case_notes`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Surveillance Data' at http://localhost:7807. Make the user controls functional. The experience needs Case Notes (`case_notes`, markdown) using `/case-notes` for notes for one surveillance case; user controls: Case (`case_id`, text). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Surveillance Data/case_notes` → `missing_widget`

#### `case_notes_app`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for cases and compliance alerts. The workspace must cover notes for one surveillance case. Leave the complete working workspace open for review. Use `case_id` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_param_review`

**hard** · category: platform · specification: partially-specified

> Create a usable earnings and estimates workflow for an equity-research analyst. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. The source contract must retain `symbol` and `quarter`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_ship`

**hard** · category: platform · specification: -

> An equity-research analyst needs a decision-ready Workspace for earnings and estimates. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. The workspace must cover average EPS surprise last 4 quarters. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Earnings Symbol Live', 'symbol sync', 'Earnings Prep Data', 'MSFT', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Earnings Symbol Live", "symbol sync", "Earnings Prep Data", "MSFT" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `healthcare_ship`

**hard** · category: platform · specification: -

> A healthcare-research analyst needs a decision-ready Workspace for clinical catalysts and pipelines. The workspace must cover trial review filtered by symbol. The workspace must cover catalysts in the next 30 days. The workspace must cover upcoming clinical trial readouts. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Trial Symbol Live', 'trial symbol', 'Healthcare Research Data', 'PFE', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Trial Symbol Live", "trial symbol", "Healthcare Research Data", "PFE" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `kpi_param_tabs`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for earnings and estimates. The workspace must cover KPI dataset switched between growth and margin views. Use `view` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `kpi_tabs_table`

**medium** · category: platform · specification: explicit

> Make the requested backend widget available and working in the current view. Use 'Earnings Prep Data' at http://localhost:7805. Make the user controls functional. The experience needs KPI Tabs (`kpi_tabs_table`, table) using `/kpi-tabs` for kPI table with static and dynamic tab views; user controls: View (`view`, tabs). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Earnings Prep Data/kpi_tabs_table` → `missing_widget`

#### `rates_commentary_app`

**medium** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Rates Watch Data' at http://localhost:7803. Make the user controls functional. The experience needs Rates Commentary (`rates_commentary`, markdown) using `/rates-commentary` for desk commentary on the rates day; user controls: Series (`series`, endpoint) from `/series-options`. Organize it as app 'Series Commentary' with tabs Commentary (rates_commentary). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Series Commentary" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Rates Watch Data/rates_commentary` on tab `commentary` → `missing_widget`

#### `rates_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover rates commentary filtered by selected series. The workspace must cover current 2s10s spread in bps. The workspace must cover desk commentary on the rates day. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Rates Series Live', 'series preset', 'Rates Watch Data', 'DGS10'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Rates Series Live", "series preset", "Rates Watch Data", "DGS10" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `series_markdown`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a rates strategist covering rates and Treasury markets. The workspace must cover rates note for the selected time series. Keep these source-contract anchors: `series`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `symbol_param_desk`

**hard** · category: platform · specification: -

> An equity-research analyst needs a decision-ready Workspace for earnings and estimates. The workspace must cover preview note for the earnings call. The workspace must cover street estimate revisions by quarter. The workspace must cover EPS beat and miss history. Analysts need to inspect quarter, EPS estimate, revenue estimate billions. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `trial_catalysts`

**medium** · category: platform · specification: explicit

> Make the requested backend widget available and working in the current view. Use 'Healthcare Research Data' at http://localhost:7808. Make the user controls functional. The experience needs Trial Catalysts (`trial_catalysts`, table) using `/trial-catalysts` for upcoming clinical trial readouts; user controls: Ticker (`ticker`, endpoint) from `/tickers`; columns: ticker (text), phase (text), readout_date (dateString). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Healthcare Research Data/trial_catalysts` → `missing_widget`

#### `trial_catalysts_app`

**medium** · category: platform · specification: explicit

> Implement the requested app and confirm it by opening it in Workspace. Use 'Healthcare Research Data' at http://localhost:7808. Make the user controls functional. The experience needs Trial Catalysts (`trial_catalysts`, table) using `/trial-catalysts` for upcoming clinical trial readouts; user controls: Ticker (`ticker`, endpoint) from `/tickers`; columns: ticker (text), phase (text), readout_date (dateString). Organize it as app 'Catalyst Filter' with tabs Catalysts (trial_catalysts). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Catalyst Filter" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Healthcare Research Data/trial_catalysts` on tab `catalysts` → `missing_widget`

#### `trial_param_review`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a healthcare-research analyst covering clinical catalysts and pipelines. The workspace must cover upcoming clinical trial readouts. The workspace must cover pipeline distribution by phase. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Keep these source-contract anchors: `ticker` and `phase`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vendor_sla_table_app`

**medium** · category: platform · specification: -

> Create a usable vendor service levels workflow for a vendor-operations manager. The workspace must cover vendor SLA state with breach flags. Analysts need to inspect vendor, status, latency milliseconds, breach. Leave the complete working workspace open for review. The source contract must retain `status` and `vendor`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vix_history`

**medium** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Vol Desk Data' at http://localhost:7801. Make the user controls functional. The experience needs VIX History (`vix_history`, table) using `/vix-history` for daily CBOE VIX closes with returns; user controls: Window (`window`, number); columns: date (dateString), close (number), return_pct (number, percent, greenRed). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vol Desk Data/vix_history` → `missing_widget`

#### `vol_param_cockpit`

**hard** · category: platform · specification: -

> Build a volatility analyst a dependable volatility and derivatives workspace. The workspace must cover screen names by implied-vol criteria. The workspace must cover daily CBOE VIX closes with returns. The workspace must cover morning volatility commentary. Analysts need to inspect date, close, return percentage. An analyst can filter the analysis by ticker. An analyst can choose the relevant business date. An analyst can adjust the relevant numeric scope. An analyst can toggle the relevant screening constraint. Leave the complete working workspace open for review. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vol_screener`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for volatility and derivatives. The workspace must cover screen names by implied-vol criteria. An analyst can filter the analysis by ticker. An analyst can choose the relevant business date. An analyst can toggle the relevant screening constraint. Use `ticker` and `as_of` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vol_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready volatility and derivatives workflow for a volatility analyst. The workspace must cover volatility review filtered by symbol. The workspace must cover current volatility regime score. The workspace must cover daily CBOE VIX closes with returns. Analysts need to inspect date, close, return percentage. An analyst can filter the analysis by ticker. An analyst can toggle the relevant screening constraint. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Vol Symbol Live', 'vol symbol', 'Vol Desk Data', 'AAPL', 'ticker'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Vol Symbol Live", "vol symbol", "Vol Desk Data", "AAPL" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `windowed_vix_slice`

**hard** · category: platform · specification: partially-specified

> Create a usable volatility and derivatives workflow for a volatility analyst. The workspace must cover VIX analysis for a selected window and as-of date. An analyst can choose the relevant business date. An analyst can adjust the relevant numeric scope. The source contract must retain `window` and `as_of`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


### settings (20)

#### `alert_metric_app`

**easy** · category: platform · specification: -

> Publish the requested app and open it in Workspace to verify it works. Use 'Surveillance Data' at http://localhost:7807. Implement the requested runtime and refresh behavior. The experience needs Open Alerts (`alert_metric`, metric) using `/alert-count` for open alert count; cache for 15 minutes. Organize it as app 'Alert Settings' with tabs Alerts (alert_metric). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Alert Settings" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Surveillance Data/alert_metric` on tab `alerts` → `missing_widget`

#### `alert_metric_room`

**hard** · category: platform · specification: -

> Build a surveillance analyst a dependable cases and compliance alerts workspace. The workspace must cover open alert count. The workspace must cover notes for one surveillance case. The workspace must cover latest surveillance policy digest. Leave the complete working workspace open for review. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `auction_cache_grid`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for rates and Treasury markets. The workspace must cover cached auction watchlist. Analysts need to inspect auction date, security, size billions. Use `auction_date` and `security` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `catalyst_metric_app`

**medium** · category: platform · specification: explicit

> Publish the requested app and open it in Workspace to verify it works. Use 'Healthcare Research Data' at http://localhost:7808. Implement the requested runtime and refresh behavior. The experience needs Catalysts 30d (`catalyst_metric`, metric) using `/catalyst-count` for catalysts in the next 30 days; refresh every 30 seconds; run on demand. Organize it as app 'Catalyst Settings' with tabs Catalysts (catalyst_metric). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Catalyst Settings" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Healthcare Research Data/catalyst_metric` on tab `catalysts` → `missing_widget`

#### `exception_metric`

**medium** · category: platform · specification: explicit

> Register the backend and place the specified widget on the active dashboard. Use 'Execution Desk Data' at http://localhost:7806. Implement the requested runtime and refresh behavior. The experience needs Exceptions (`exception_metric`, metric) using `/exception-count` for open execution exceptions; refresh every 45 seconds; run on demand. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Execution Desk Data/exception_metric` → `missing_widget`

#### `exception_refresh_grid`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for orders and venue quality. The workspace must cover execution exceptions with manual refresh. Analysts need to inspect order ID, symbol, age min. Use `order_id` and `symbol` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `execution_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready orders and venue quality workflow for an execution analyst. The workspace must cover open execution exceptions. The workspace must cover live open orders blotter. The workspace must cover monthly venue scorecard document. Analysts need to inspect order ID, symbol, quantity, status. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Execution Config Live', 'on-demand updates', 'Execution Desk Data', 'urgent'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Execution Config Live", "on-demand updates", "Execution Desk Data", "urgent" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `gas_metric`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Chain TVL Data' at http://localhost:7802. Implement the requested runtime and refresh behavior. The experience needs Gas Now (`gas_metric`, metric) using `/gas-now` for current gas price snapshot; refresh every 30 seconds. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Chain TVL Data/gas_metric` → `missing_widget`

#### `gas_metric_room`

**hard** · category: platform · specification: partially-specified

> Create a usable chain activity and liquidity workflow for a digital-assets analyst. The workspace must cover current gas price snapshot. The workspace must cover written details for one protocol. Leave the complete working workspace open for review. The source contract must retain `protocol`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `gas_refresh_metric`

**hard** · category: platform · specification: partially-specified

> Create a usable chain activity and liquidity workflow for a digital-assets analyst. The workspace must cover auto-refreshing gas snapshot. The source contract must retain `Chain TVL Data`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `healthcare_ship`

**hard** · category: platform · specification: -

> A healthcare-research analyst needs a decision-ready Workspace for clinical catalysts and pipelines. The workspace must cover catalysts in the next 30 days. The workspace must cover upcoming clinical trial readouts. The workspace must cover pipeline distribution by phase. Analysts need to inspect ticker, phase, readout date. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Catalyst Config Live', 'Catalysts category', 'Healthcare Research Data', '60d', 'ticker'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Catalyst Config Live", "Catalysts category", "Healthcare Research Data", "60d" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `rates_commentary`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Rates Watch Data' at http://localhost:7803. Implement the requested runtime and refresh behavior. The experience needs Rates Commentary (`rates_commentary`, markdown) using `/rates-commentary` for desk commentary on the rates day; user controls: Series (`series`, endpoint) from `/series-options`; cache for 30 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Rates Watch Data/rates_commentary` → `missing_widget`

#### `rates_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready rates and Treasury markets workflow for a rates strategist. The workspace must cover current 2s10s spread in bps. The workspace must cover desk commentary on the rates day. The workspace must cover the Treasury yield curve. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Rates Config Live', 'Macro category', 'Rates Watch Data', '5s30s'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Rates Config Live", "Macro category", "Rates Watch Data", "5s30s" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `runbook_markdown`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for vendor service levels. The workspace must cover configured SLA runbook note. Use `Vendor SLA Data` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `sla_runbook_app`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for vendor service levels. The workspace must cover runbook for SLA escalations. Leave the complete working workspace open for review. Use `Vendor SLA Data` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `surprise_metric_app`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover average EPS surprise last 4 quarters. Leave the complete working workspace open for review. Keep these source-contract anchors: `Earnings Prep Data`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `surprise_metric_room`

**hard** · category: platform · specification: -

> The desk needs a production-ready earnings and estimates workflow for an equity-research analyst. The workspace must cover average EPS surprise last 4 quarters. The workspace must cover preview note for the earnings call. The workspace must cover EPS beat and miss history. An analyst can filter the analysis by ticker. Leave the complete working workspace open for review. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vol_commentary_room`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a volatility analyst covering volatility and derivatives. The workspace must cover morning volatility commentary. The workspace must cover current volatility regime score. Leave the complete working workspace open for review. Keep these source-contract anchors: `desk`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `vol_regime_metric`

**easy** · category: platform · specification: -

> Make the requested backend widget available and working in the current view. Use 'Vol Desk Data' at http://localhost:7801. Implement the requested runtime and refresh behavior. The experience needs Vol Regime (`vol_regime_metric`, metric) using `/vol-regime` for current volatility regime score; cache for 15 minutes; run on demand. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vol Desk Data/vol_regime_metric` → `missing_widget`

#### `vol_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready volatility and derivatives workflow for a volatility analyst. The workspace must cover current volatility regime score. The workspace must cover morning volatility commentary. The workspace must cover daily CBOE VIX closes with returns. Analysts need to inspect date, close, return percentage. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Vol Config Live', '15-minute cache', 'Vol Desk Data', 'stress'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

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
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `case_notes_room`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a surveillance analyst covering cases and compliance alerts. The workspace must cover notes for one surveillance case. The workspace must cover latest surveillance policy digest. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `case_id` and `case_scope`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `chains_heatmap_html`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Chain TVL Data' at http://localhost:7802. Choose the native widget type that fits the content. The experience needs Chain Heatmap (`chains_heatmap_html`, html) using `/chains-heatmap` for raw HTML heatmap of chain flows; cache for 15 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Chain TVL Data/chains_heatmap_html` → `missing_widget`

#### `curve_monitor_iframe_app`

**medium** · category: platform · specification: explicit

> Build the specified app, publish it, and leave a working instance open. Use 'Rates Watch Data' at http://localhost:7803. Choose the native widget type that fits the content. The experience needs Curve Monitor App (`curve_monitor_iframe`, iframe) using `http://localhost:5173` for embedded standalone curve monitor application. Organize it as app 'Curve Monitor' with tabs Monitor (curve_monitor_iframe). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Curve Monitor" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Rates Watch Data/curve_monitor_iframe` on tab `monitor` → `missing_widget`

#### `earnings_calls_video_app`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for an equity-research analyst covering earnings and estimates. The workspace must cover replay library of earnings calls. Leave the complete working workspace open for review. Keep these source-contract anchors: `video`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `earnings_calls_video_room`

**hard** · category: platform · specification: -

> Build an equity-research analyst a dependable earnings and estimates workspace. The workspace must cover replay library of earnings calls. The workspace must cover preview note for the earnings call. The workspace must cover average EPS surprise last 4 quarters. An analyst can filter the analysis by ticker. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `evidence_files_app`

**hard** · category: platform · specification: partially-specified

> Create a usable cases and compliance alerts workflow for a surveillance analyst. The workspace must cover browse case evidence documents. Leave the complete working workspace open for review. The source contract must retain `file`; decide the remaining implementation and preserve unrelated workspace state.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `evidence_files_room`

**hard** · category: platform · specification: -

> Build a surveillance analyst a dependable cases and compliance alerts workspace. The workspace must cover browse case evidence documents. The workspace must cover notes for one surveillance case. The workspace must cover open alert count. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `evidence_files_ship`

**hard** · category: platform · specification: -

> Build a surveillance analyst a dependable cases and compliance alerts workspace. The workspace must cover browse case evidence documents. The workspace must cover open alert count. The workspace must cover notes for one surveillance case. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Evidence Live', 'evidence', 'Surveillance Data'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Evidence Live", "evidence", "Surveillance Data" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `fda_newsfeed_room`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a healthcare-research analyst covering clinical catalysts and pipelines. The workspace must cover FDA decision and notice feed. The workspace must cover catalysts in the next 30 days. A selection in one part of the analysis stays linked to related results. Leave the complete working workspace open for review. Keep these source-contract anchors: `therapy_area`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `gas_metric`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Chain TVL Data' at http://localhost:7802. Choose the native widget type that fits the content. The experience needs Gas Now (`gas_metric`, metric) using `/gas-now` for current gas price snapshot; cache for 15 minutes; run on demand. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Chain TVL Data/gas_metric` → `missing_widget`

#### `gas_priority_metric`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a digital-assets analyst covering chain activity and liquidity. The workspace must cover priority gas fee monitor. Keep these source-contract anchors: `Chain TVL Data`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `policy_digest_pdf`

**hard** · category: platform · specification: partially-specified

> Deliver an analyst-ready Workspace solution for cases and compliance alerts. The workspace must cover current surveillance policy digest. Use `Surveillance Data` as the only fixed contract anchors, and make the other implementation choices yourself without collateral changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):


#### `policy_digest_pdf_ship`

**hard** · category: platform · specification: -

> A surveillance analyst needs a decision-ready Workspace for cases and compliance alerts. The workspace must cover current surveillance policy digest. The workspace must cover open surveillance alerts. The workspace must cover notes for one surveillance case. Analysts need to inspect alert ID, desk, severity, age days. Leave the complete working workspace open for review. Add a short completion note that naturally includes the desk-required terms 'Policy Digest Live', 'policy digest', 'Surveillance Data', 'C-2099'. Choose an effective architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated note** ≥1× whose content mentions "Policy Digest Live", "policy digest", "Surveillance Data", "C-2099" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `sla_newsfeed_app`

**easy** · category: platform · specification: -

> Implement the requested app and confirm it by opening it in Workspace. Use 'Vendor SLA Data' at http://localhost:7804. Choose the native widget type that fits the content. The experience needs Vendor Notices (`sla_newsfeed`, newsfeed) using `/vendor-notices` for vendor incident notices feed. Organize it as app 'Vendor Notices' with tabs Notices (sla_newsfeed). Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 6 · oracle reference trace: 3 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Dashboard name** must contain "Vendor Notices" (case-insensitive phrase or in-order word match, stopwords ignored) → `dashboard_name`
- **Widget** ≥1× `Vendor SLA Data/sla_newsfeed` on tab `notices` → `missing_widget`

#### `sla_newsfeed_ship`

**hard** · category: platform · specification: -

> Build a vendor-operations manager a dependable vendor service levels workspace. The workspace must cover vendor incident notices feed. The workspace must cover count of open SLA breaches. The workspace must cover vendor SLA state with breach flags. Analysts need to inspect vendor, status, latency milliseconds, breach. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Vendor Notice Room', 'notices', 'Vendor SLA Data', 'QuoteStream'. Decide how best to organize the experience and preserve unrelated work.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Vendor Notice Room", "notices", "Vendor SLA Data", "QuoteStream" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `venue_packet_pdf_ship`

**hard** · category: platform · specification: -

> The desk needs a production-ready orders and venue quality workflow for an execution analyst. The workspace must cover monthly venue scorecard packet. The workspace must cover open execution exceptions. The workspace must cover live open orders blotter. Analysts need to inspect order ID, symbol, quantity, status. Leave the complete working workspace open for review. Add a short completion HTML card that naturally includes the desk-required terms 'Venue Packet Live', 'venue packet', 'Execution Desk Data', 'EDGX'. Use your judgment on the architecture and leave other work intact.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 14 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Generated html** ≥1× whose content mentions "Venue Packet Live", "venue packet", "Execution Desk Data", "EDGX" (case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) → `missing_generated_widget`
- **Grid bounds**: every widget inside the 40-column grid (x≥0, y≥0, w>0, h>0, x+w≤40) → `layout_out_of_grid`
- **No overlaps**: no two widgets on the same tab intersect → `layout_overlap`

#### `venue_pdf`

**medium** · category: platform · specification: explicit

> Connect the backend and make its first widget usable on the current dashboard. Use 'Execution Desk Data' at http://localhost:7806. Choose the native widget type that fits the content. The experience needs Venue Scorecard (`venue_pdf`, pdf) using `/venue-scorecard` for monthly venue scorecard PDF; cache for 30 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Execution Desk Data/venue_pdf` → `missing_widget`

#### `vol_commentary`

**easy** · category: platform · specification: -

> Register the backend and place the specified widget on the active dashboard. Use 'Vol Desk Data' at http://localhost:7801. Choose the native widget type that fits the content. The experience needs Vol Commentary (`vol_commentary`, markdown) using `/vol-commentary` for morning volatility commentary; user controls: Desk (`desk`, text); cache for 15 minutes. Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 7 · oracle reference trace: 4 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):

- **Widget** ≥1× `Vol Desk Data/vol_commentary` → `missing_widget`

#### `vol_playbook_note`

**hard** · category: platform · specification: partially-specified

> Build a working Workspace experience for a volatility analyst covering volatility and derivatives. The workspace must cover written playbook for the vol desk. Keep these source-contract anchors: `section`. Choose the rest of the architecture and avoid unrelated changes.

- Initial workspace: empty (no seeded dashboard)
- Allowed tools (20): `get_workspace_snapshot`, `manage_dashboard`, `manage_navigation_bar`, `navigate_workspace`, `list_available_widgets`, `get_widget_schema`, `get_params_options`, `get_widget_data`, `create_widget`, `update_widget`, `update_widget_layout`, `delete_widget`, `add_generative_widget`, `read_widget`, `manage_backends`, `manage_apps`, `get_skill_content`, `read_workspace_resource`, `get_workspace_prompt`, `assign_tasks_to_agents`
- Turn budget: 13 · oracle reference trace: 5 calls

**Passes only if all of these checks hold** (each failure emits the issue code shown):



---

Total: 625 tasks.