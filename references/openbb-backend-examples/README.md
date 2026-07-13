# OpenBB backend-examples (vendored snapshot)

Curated, source-only snapshot of OpenBB's official
[backend-examples-for-openbb-workspace](https://github.com/OpenBB-finance/backend-examples-for-openbb-workspace)
repository (MIT, see `LICENSE`). These are the canonical reference
implementations for OpenBB Workspace custom backends — kept in-repo as ground
truth for authoring widget-creation and backend-building tasks, so task
generators and oracle overlays never depend on a sibling checkout.

Pinned upstream commit: `729f1fd706b549776ea120e1e3f33fe465a823f5` (2026-07-07).
To refresh, re-copy from upstream and update this pin.

## Contents

| Directory | What it is |
| --- | --- |
| `reference-backend/` | The "getting started" onboarding backend: one module per feature (widget types, plotly/highcharts/vega-lite charts, sparklines, ag-grid tables, live grid, omni SQL, input params, forms, grouping, TradingView, YouTube, settings) plus its `apps.json`. |
| `widget-types/` | Twelve minimal one-widget-type backends (table, chart, metric, markdown, pdf, omni, live_grid, news, html, advanced_charting, multi_file_viewer, live_feed) — each just `main.py` + `widgets.json`. The canonical "create a widget of type X" ground truth. |
| `parameters-types/` | Five parameter-feature examples: parameters, forms, tabs, grouping, column/cell rendering. |
| `ssrm_mode/` | Server-side row model (`ssrm_table`) backend over SQLite/MySQL/Snowflake. |
| `matching-widget-mcp-tool/` | Backend pairing a widget with a matching MCP tool. |

## What was intentionally excluded

- Dependency/build junk: `.venv/`, `__pycache__/`, `node_modules/`.
- `ssrm_mode/demo_data.db` (11M binary). Upstream ships it pre-built with no
  generator script — copy it from the upstream repo if you want to actually
  run `ssrm_mode`.
- `widget-examples/streamlit/`, `widget-examples/database-connectors/`,
  `widget-examples/market-data-react-app/`, `apps/`, `scripts/` — integration
  demos unrelated to widget authoring (and ~650M of vendored environments).

These are references, not bench fixtures: nothing imports them at runtime, and
they carry no bench-side tests. When a code task needs one as a starter or
oracle, copy the relevant files into that task's fixture directory under
`src/workspace_bench/task_suites/` rather than importing from here.
