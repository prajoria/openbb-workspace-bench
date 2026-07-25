---
facts:
  dashboard: Client Holdings Watch
  targets:
    - {widget: Live Grid, app: Onboarding App for Devs, origin: Getting Started}
  params: {symbol: AAPL}
  seeded_wrong: {symbol: TSLA}
  find_hint: the live price watch
  policy: {phrase: the Apple holding policy, carries: symbol, meaning: the client's Apple holding - AAPL}
  governance: {skill: finance-tearsheet}
  build: {backend: Holdings Watch Service, table: Holdings Register, app: Holdings Watch App, tab: Watch}
---
# Holdings watch

The client's holdings watch should be on Apple before the call, but the live
view was left on Tesla after an earlier conversation. This is a repair story:
correct the existing Live Grid from TSLA to AAPL without disturbing the other
client material on the dashboard; the lived-in levels can carry a second,
correctly configured watch as the near twin.

The Apple holding policy carries the symbol directly: Apple means AAPL. The
finance-tearsheet skill governs the deeper rungs because its workflow says to
"Gather price action first", which is the purpose of this live client watch.
