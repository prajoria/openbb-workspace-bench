---
facts:
  dashboard: Guidance Watch
  targets:
    - {widget: Management Guidance, origin: Bench Daloopa}
  params: {ticker: NFLX}
  find_hint: management's promises
  policy: {phrase: the streaming coverage policy, carries: ticker, meaning: the streaming name - Netflix}
  governance: {skill: daloopa-guidance-tracker}
  build: {backend: Guidance Watch Service, table: Guidance Register}
---
# Guidance tracker

The analyst tracks what management promised versus what they delivered, and
Netflix is the name under review this cycle. Management Guidance from the
covered dataset is the source of truth - "management's promises" in the
analyst's own words, the natural colloquial handle.

The streaming coverage policy resolves to the one streaming name on the
coverage list: Netflix, NFLX. The daloopa-guidance-tracker skill governs -
comparing claims with guidance and flagging changed assumptions is exactly
this workflow, so its concepts belong in the notes the deeper levels require.
