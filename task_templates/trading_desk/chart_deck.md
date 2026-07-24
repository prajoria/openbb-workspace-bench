---
facts:
  dashboard: Chart Deck
  targets:
    - {widget: TradingView Chart, origin: Getting Started}
    - {widget: Plotly Heatmap, origin: Getting Started, params: {color_scale: Viridis}}
  find_hint: the candles chart
  policy: {phrase: the house palette policy, carries: color_scale, meaning: the Viridis scale}
  governance: {prompt: workspace_session_context}
  build: {backend: Chart Deck Service, table: Deck Register}
---
# Chart deck

The desk keeps a two-chart deck on the side screen: the candles chart for
price and a heatmap for the cross-section. TradingView Chart takes no
parameters - it earns its place by being found and placed; the heatmap takes
the house color scale.

The house palette policy carries the scale: Viridis. Workspace session
guidance governs the deeper rungs - the deck is a layout exercise, and the
session-grounding anchors that guidance describes are what a governed note
should record. Deck furniture for the lived-in levels: a sparkline table,
perhaps a tabs-and-dropdown ratio view from Widget Examples.
