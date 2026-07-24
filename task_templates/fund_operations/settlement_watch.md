---
facts:
  dashboard: Fails Watch
  targets:
    - {widget: Failed Trades, app: Fund Operations Control Tower, origin: Bench Stark Enterprise}
    - {widget: Settlement Exceptions, app: Fund Operations Control Tower, origin: Bench Stark Enterprise}
  params: {fund: Income Fund, status: Open, period: 1D}
  find_hint: the fails queue
  policy: {phrase: the same-day fails policy, carries: period, meaning: today only - the one-day window}
  governance: {skill: finance-guidance-tracker}
  build: {backend: Fails Watch Service, table: Fails Register}
---
# Settlement watch

Under T+1 a fail caught tomorrow is a fail settled late, so ops watches the
queue same-day: the failed-trades count and the settlement exceptions for the
Income Fund, open items, today only. Two views, one cut, checked before the
afternoon cutoff.

The same-day fails policy carries the period: today, the one-day window. The
finance-guidance-tracker skill governs the deeper rungs - an exceptions queue
is only clear when the evidence gaps are listed, and that is the note the
cutoff review requires.
