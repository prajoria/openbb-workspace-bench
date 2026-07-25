---
facts:
  dashboard: Proposal Pack
  targets:
    - {widget: Company Fundamentals, origin: Bench Daloopa, params: {ticker: MSFT, period: 2025Q4}}
    - {widget: Omni Widget with Citations, origin: Widget Examples, params: {type: markdown}}
  find_hint: the cited written summary
  policy: {phrase: the written-summary pack policy, carries: type, meaning: written narrative rather than a chart or table - markdown}
  governance: {skill: daloopa-tearsheet}
  build: {backend: Client Pack Service, table: Pack Register, app: Client Pack App, tab: Pack}
---
# Proposal pack

The proposal pack pairs Microsoft fundamentals for 2025Q4 with a cited written
summary that explains the figures in client-safe language. At the Compose rung,
the advisor needs a Client Pack Service with a Pack Register table, published
and instantiated as the Client Pack App so the Pack tab is ready to use before
the meeting.

The written-summary pack policy carries the content type directly: among
markdown, chart, and table, a written narrative means markdown. The
daloopa-tearsheet skill governs the deeper rungs because it requires the pack to
"Cite every Daloopa-sourced figure with its source_url", which is essential
when the firm's view is being presented to the client.
