---
facts:
  dashboard: Alert Sweep
  targets:
    - {widget: Open Alert Metrics, app: Compliance Surveillance Hub, origin: Bench Stark Enterprise}
    - {widget: Alert Trend, app: Compliance Surveillance Hub, origin: Bench Stark Enterprise}
  params: {severity: High, status: Open, period: MTD}
  find_hint: the alert queue
  policy: {phrase: the open-items sweep policy, carries: status, meaning: everything still open}
  governance: {skill: finance-guidance-tracker}
  build: {backend: Sweep File Service, table: Sweep Register}
---
# Alert sweep

The monthly surveillance sweep: high-severity items still open, this month,
counted and trended. Open Alert Metrics gives the headline number; Alert Trend
shows whether the queue is growing. Both come from the Compliance Surveillance
Hub and both get cut the same way - severity High, status Open, month-to-date.

The open-items sweep policy carries the status: everything still open. The
finance-guidance-tracker skill governs the deeper rungs - its workflow ends by
listing evidence gaps, which is exactly what a surveillance sweep must record
before anyone signs it off.
