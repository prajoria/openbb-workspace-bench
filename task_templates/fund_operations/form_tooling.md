---
facts:
  dashboard: Intake Tools
  targets:
    - {widget: Financial Entry Form, origin: Widget Examples}
    - {widget: Example Backend Params, origin: Widget Examples, params: {daysPicker1: "5"}}
  find_hint: the intake form
  policy: {phrase: the weekly window policy, carries: daysPicker1, meaning: one trading week - five days}
  governance: {resource: the widget-parameters spec}
  build: {backend: Intake Form Service, table: Intake Register}
---
# Form tooling

Ops runs manual adjustments through a form, not through chat messages - so the
intake page gets built properly: the entry form for submissions, and the
parameters tester beside it set to the standard review window. The Financial
Entry Form carries a form-type parameter, the rarest kind on the surface.

The weekly window policy carries the day picker: one trading week, five days.
The widget-parameters spec governs the deeper rungs - it is the document that
defines the parameter kinds themselves (form sits between endpoint and button
in its list), making it the right source for the tooling note. The level-5
build is the payoff: ops publishing its own intake service.
