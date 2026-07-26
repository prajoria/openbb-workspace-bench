---
facts:
  dashboard: Shock Watch
  targets:
    - {widget: VaR Trend, app: Risk & Exposure Monitor, origin: Bench Stark Enterprise}
  params: {portfolio: Long/Short Equity, scenario: Rates +100bp, period: YTD}
  find_hint: the value-at-risk trend
  policy: {phrase: the rates-shock policy, carries: scenario, meaning: the plus-100-basis-points rates scenario}
  governance: {skill: daloopa-inflection}
  build: {backend: Shock Watch Service, table: Shock Register}
---
# VaR monitor

Risk reviews the long/short book against the rates shock every cycle: VaR
Trend for the Long/Short Equity portfolio, year-to-date, under the rates
scenario. The scenario names are a fixed menu - equity down ten, rates up a
hundred, credit wider - and the policy picks one of them.

The rates-shock policy carries the scenario: rates up one hundred basis
points, exactly as the option spells it. The daloopa-inflection skill governs
the deeper rungs - a risk trend review is a hunt for reversals, and the
skill's cadence-and-turning-point language is what belongs in the note.
