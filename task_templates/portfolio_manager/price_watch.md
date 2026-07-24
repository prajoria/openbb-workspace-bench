---
facts:
  dashboard: Price Watch
  targets:
    - {widget: Live Grid, origin: Getting Started}
  params: {symbol: TSLA}
  find_hint: the live-updating price grid
  policy: {phrase: the EV watch policy, carries: symbol, meaning: the desk's EV name - Tesla}
  governance: {skill: finance-tearsheet}
  build: {backend: Watch Feed Service, table: Watch Register}
---
# Price watch

The PM wants one always-on price view for the name they are most nervous about.
The Live Grid from Getting Started updates in place - that streaming behaviour is
how the PM refers to it ("the live-updating price grid"), which is the natural
level-1 handle since they never remember its catalog title.

The EV watch policy pins the symbol: the desk's electric-vehicle name, Tesla,
so TSLA. The finance-tearsheet skill governs here naturally - its workflow
starts from price action, which is exactly what this dashboard exists to show.
Sensible furniture for the lived-in levels: a sparkline view of other tickers,
a stale watch note from a previous session.
