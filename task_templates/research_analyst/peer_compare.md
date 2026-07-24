---
facts:
  dashboard: Peer Compare
  targets:
    - {widget: Company Fundamentals, origin: Bench Daloopa, params: {ticker: MSFT, period: 2025Q2}}
    - {widget: Company Fundamentals, origin: Bench Daloopa, params: {ticker: AMZN, period: 2025Q2}}
  find_hint: the fundamentals table
  policy: {phrase: the cloud pair policy, carries: ticker, meaning: the two covered cloud names - Microsoft and Amazon}
  governance: {skill: daloopa-industry}
  build: {backend: Peer Compare Service, table: Peer Register}
---
# Peer compare

Two names, same quarter, side by side - the analyst's standard peer read.
Company Fundamentals goes up twice, once for Microsoft and once for Amazon,
both pinned to 2025Q2 so the comparison is apples to apples. The two-view
placement is the story's heart: same widget, different tickers, deliberate.

The cloud pair policy names the pair by franchise - the two covered cloud
names, Azure's and AWS's owners - so MSFT and AMZN. The daloopa-industry skill
governs: peers come from the company directory, which is the method being
exercised here.
