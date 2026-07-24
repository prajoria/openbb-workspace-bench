---
facts:
  dashboard: Close Room
  targets:
    - {widget: Close Exceptions, app: "NAV, Fees & Close Dashboard", origin: Bench Stark Enterprise}
  params: {fund: Flagship Long/Short, status: Open, period: 1D}
  seeded_wrong: {fund: Multi-Asset Fund, status: Closed, period: 1Y}
  find_hint: the close blotter
  policy: {phrase: the close-day policy, carries: period, meaning: today's close - the one-day window}
  governance: {skill: daloopa-capital-allocation}
  build: {backend: Close Watch Service, table: Close Register}
---
# NAV close repair

The close room's exceptions view is pointing at the wrong fund, the wrong
status, and a year-long window - someone's leftover from a quarter-end
investigation. Today's close needs it back on Flagship Long/Short, open items,
one-day window, and nothing else on the close dashboard may move. Beware the
app's own traps: it carries two views named NAV Exceptions, which is why this
story targets Close Exceptions by its exact name.

The close-day policy carries the period: today's close, the one-day window.
The daloopa-capital-allocation skill governs the deeper rungs - distributions
are the payout item in its comparison, and payouts land in the NAV, which is
what the close note must get right.
