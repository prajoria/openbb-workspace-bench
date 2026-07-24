---
facts:
  dashboard: Breach Review
  targets:
    - {widget: Policy Breaches, app: Compliance Surveillance Hub, origin: Bench Stark Enterprise}
  params: {severity: High, status: Open, period: QTD}
  seeded_wrong: {status: Closed, period: 1Y}
  find_hint: the personal-trading breaches
  policy: {phrase: the quarter-under-review policy, carries: period, meaning: quarter-to-date}
  governance: {skill: finance-guidance-tracker}
  build: {backend: Breach Watch Service, table: Breach Register}
---
# Breach repair

Someone left the personal-trading breaches view filtered to closed items over a
year - useless for the review that starts this afternoon. This is a repair
story: the view exists but is misconfigured (status Closed, period 1Y where the
review needs Open and quarter-to-date), and the fix must not disturb whatever
else the review dashboard carries.

The quarter-under-review policy carries the period: quarter-to-date. The
finance-guidance-tracker skill governs the deeper rungs, for the same reason as
the sweep: the review closes by evidencing what is still missing.
