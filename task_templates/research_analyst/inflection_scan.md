---
facts:
  dashboard: Inflection Scan
  targets:
    - {widget: Operating KPIs, origin: Bench Daloopa}
  params: {ticker: TSLA, period: 2025Q3}
  find_hint: the KPI trends
  policy: {phrase: the fresh-quarter scan policy, carries: period, meaning: the newest covered quarter - 2025Q3}
  governance: {skill: daloopa-inflection}
  build: {backend: Inflection Scan Service, table: Reversal Register}
---
# Inflection scan

Once the new quarter lands in the dataset, the analyst scans the operating KPIs
for turning points - growth that flipped sign, cadence that broke. Tesla is
this cycle's scan. Operating KPIs from the covered set is the input; the
deliverable at deeper levels is a note recording what the scan method demands.

The fresh-quarter scan policy carries the period: the newest covered quarter in
the options, 2025Q3. The daloopa-inflection skill governs - quarter-over-quarter
cadence first, reversals flagged as inflections - which is the entire point of
this dashboard.
