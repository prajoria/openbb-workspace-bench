---
facts:
  dashboard: Case Review
  targets:
    - {widget: Expert Calls, app: MNPI & Research Review, origin: Bench Stark Enterprise}
  params: {status: In Review, severity: High, period: MTD}
  find_hint: the expert-network log
  policy: {phrase: the escalation policy, carries: severity, meaning: high severity}
  governance: {skill: finance-earnings-prep}
  build: {backend: Case File Service, table: Case Register}
---
# Case handoff

An expert-network call has been sitting in review and the officer is packaging
the case for the surveillance team: read the expert-calls log cut to the items
under review this month, record the facts in a case note, and at the deeper
levels hand the follow-up to the reviewing team. The paper trail is the point.

The escalation policy carries the severity: escalation means high. The
finance-earnings-prep skill governs - its workflow inspects transcript tone,
and an expert-call review is exactly a transcript-tone exercise, which is why
its concepts belong in the case note.
