---
facts:
  dashboard: Allocation Review
  targets:
    - {widget: Segment Breakdown, origin: Bench Daloopa}
  params: {ticker: AAPL, period: 2026Q1}
  find_hint: the segment split
  policy: {phrase: the latest covered quarter policy, carries: period, meaning: the newest quarter the dataset covers - 2026Q1}
  governance: {skill: daloopa-tearsheet}
  build: {backend: Allocation Digest Service, table: Segment Digest, app: Allocation Digest App, tab: Digest}
---
# Allocation read

Before sizing the Apple position, the PM wants the segment mix read off the
covered data and recorded exactly - top segment and its revenue figure, quoted
to the decimal in a note the desk can reuse. This is a read-and-report story:
the deliverable is the note, grounded in what Segment Breakdown actually serves.

The latest covered quarter policy means the most recent period the dataset
offers - the parameter options end at 2026Q1, which is how a careful reader
derives it. The daloopa-tearsheet skill governs: its period arithmetic anchors
on the latest calendar quarter, the same convention this policy encodes.
