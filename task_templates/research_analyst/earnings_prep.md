---
facts:
  dashboard: Earnings Prep Desk
  targets:
    - {widget: Upcoming Earnings, app: Earnings & Estimates Monitor, origin: Bench Stark Enterprise}
  params: {sector: Technology, ticker: NVDA, period: QTD}
  find_hint: the earnings calendar
  policy: {phrase: the current-quarter prep policy, carries: period, meaning: quarter-to-date}
  governance: {skill: finance-earnings-prep}
  build: {backend: Prep Sheet Service, table: Prep Register}
---
# Earnings prep

Nvidia reports soon and the analyst is building the preview. First move every
cycle: the earnings calendar filtered to the name - sector Technology, ticker
NVDA - and the facts it shows recorded precisely for the prep sheet.

The current-quarter prep policy is the team convention that previews run
quarter-to-date. The finance-earnings-prep skill governs the deeper rungs -
it is literally the checklist this persona works from in earnings season
(estimates versus street, guidance review, transcript tone). Lived-in levels
can carry the rest of a prep desk: a Consensus Revisions view, half-finished
prep notes from another name.
