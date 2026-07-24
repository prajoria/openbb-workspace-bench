---
facts:
  dashboard: Filing Room
  targets:
    - {widget: Document Search, origin: Bench Daloopa, params: {ticker: AAPL, doc_type: 10-K}}
    - {widget: Multi PDF Viewer - URL, origin: Getting Started}
  find_hint: the filings search
  policy: {phrase: the annual-report pull policy, carries: doc_type, meaning: the annual report - the 10-K}
  governance: {skill: daloopa-tearsheet}
  build: {backend: Filing Room Service, table: Filing Register}
---
# Document room

Audit season: ops assembles the filing room - the filings search cut to
Apple's annual report, and the PDF viewer beside it for whatever gets pulled.
Document Search comes from the covered dataset; the viewer is the Getting
Started multi-file viewer, URL flavor.

The annual-report pull policy carries the document type: the annual report is
the 10-K. The daloopa-tearsheet skill governs the deeper rungs - the covered
dataset's citation discipline is the whole reason the filing room exists, and
the skill's sourcing conventions are what the room's note should record.
