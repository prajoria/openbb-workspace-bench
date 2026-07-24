---
facts:
  dashboard: PM Morning Briefing
  targets:
    - {widget: Trade Ideas, app: Portfolio Command Center, origin: Bench Stark Enterprise}
  params: {fund: Flagship Long/Short, period: QTD}
  find_hint: the idea pipeline
  policy: {phrase: the quarterly briefing policy, carries: period, meaning: quarter-to-date}
  governance: {skill: daloopa-capital-allocation}
  build: {backend: Briefing Feed Service, table: Idea Register}
---
# Morning briefing

The PM starts every day with the 9am call and wants the Flagship Long/Short idea
pipeline on screen before it begins. Trade Ideas is the actions view inside the
Portfolio Command Center - and note the same display name also exists in the
Strategy Health Monitor, so the app name matters when precision is needed.

The quarterly briefing policy is house shorthand: briefing views run
quarter-to-date. For the lived-in levels, this dashboard plausibly carries other
morning furniture - a Top Alerts view from the same app, an old briefing note
from last week - things the PM expects to survive untouched.
