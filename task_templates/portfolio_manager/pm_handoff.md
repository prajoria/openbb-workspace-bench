---
facts:
  dashboard: PM Handoff Log
  targets:
    - {widget: Consensus Estimates, origin: Bench Daloopa}
  params: {ticker: MSFT}
  find_hint: the street numbers
  policy: {phrase: the mega-cap coverage policy, carries: ticker, meaning: the Microsoft line}
  governance: {skill: daloopa-earnings-review}
  build: {backend: Handoff Log Service, table: Handoff Register}
---
# PM handoff

End of day, the PM logs what the overnight desk needs to know: read the street
numbers for Microsoft, record the figures that matter in a handoff note, and at
the deeper levels delegate the follow-up to the coverage analyst. The handoff
note is the artifact - exact numbers from the read, never from memory.

The mega-cap coverage policy names the line by company, not ticker: the
Microsoft line, so MSFT. The daloopa-earnings-review skill governs the close-out
- it is the house method for checking estimates against guidance, which is
precisely what the overnight desk will do with this handoff.
