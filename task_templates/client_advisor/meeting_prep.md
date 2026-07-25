---
facts:
  dashboard: Client Call Prep
  targets:
    - {widget: Client Returns, app: Client 360, origin: Bench Stark Enterprise}
  params: {client: Northstar Endowment, period: QTD}
  find_hint: the client's performance view
  policy: {phrase: the quarterly call policy, carries: period, meaning: quarter-to-date}
  governance: {skill: finance-tearsheet}
  build: {backend: Call Prep Service, table: Call Notes Register, app: Client Call Prep App, tab: Call Prep}
---
# Meeting prep

Before the call, the advisor needs the Northstar Endowment performance view cut
quarter-to-date and a short note with the client, fund, return, change, and
review status recorded exactly as served. This is a read-and-note story: the
figures come from Client Returns in Client 360, not from memory or a previous
pack.

The quarterly call policy carries the period: quarter-to-date. The
finance-tearsheet skill governs the deeper rungs because the note should lead to
the skill's "short investment conclusion a reader could act on" while keeping
the language suitable for the client.
