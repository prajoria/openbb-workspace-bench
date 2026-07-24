---
facts:
  dashboard: Best-Ex Review
  targets:
    - {widget: Live Orders, app: Execution Desk, origin: Bench Stark Enterprise}
    - {widget: Broker Scorecard, app: Execution Desk, origin: Bench Stark Enterprise}
  params: {desk: US Equity, period: QTD}
  find_hint: the blotter
  policy: {phrase: the US desk review policy, carries: desk, meaning: the US Equity desk}
  governance: {skill: finance-comps}
  build: {backend: Best-Ex File Service, table: Best-Ex Register}
---
# Best-execution file

The best-ex committee meets quarterly and the desk owns the pack: the blotter
and the broker scorecard, both cut to the US Equity desk, quarter-to-date.
Note that Broker Scorecard also exists in the Liquidity & TCA Workbench - the
Execution Desk copy is the one the committee reviews, so the app matters.

The US desk review policy is the committee's scope: the US Equity desk. The
finance-comps skill governs the deeper rungs - ranking brokers is a comparison
exercise, and the skill's language about what deserves premium or discount is
the vocabulary of a scorecard review.
