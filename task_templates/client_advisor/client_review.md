---
facts:
  dashboard: Quarterly Client Review
  targets:
    - {widget: Company Fundamentals, origin: Bench Daloopa}
    - {widget: Segment Breakdown, origin: Bench Daloopa}
  params: {ticker: AAPL, period: 2026Q1}
  find_hint: the company financials
  policy: {phrase: the 2026 first-quarter review policy, carries: period, meaning: the 2026 first quarter - 2026Q1}
  governance: {skill: daloopa-tearsheet}
  build: {backend: Client Review Service, table: Review Register, app: Client Review App, tab: Review}
---
# Client review

The quarterly review for the client includes a clear Apple company snapshot:
Company Fundamentals for the financial picture and Segment Breakdown for where
the revenue comes from, both on the same 2026Q1 basis. The advisor wants the
review ready before the meeting and the figures presented without internal
shorthand.

The 2026 first-quarter review policy carries the period directly: 2026Q1. The
daloopa-tearsheet skill governs the deeper rungs because the two views must keep
"every number from the same clock" and preserve the skill's sourcing discipline
when the review note is prepared.
