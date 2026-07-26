---
facts:
  dashboard: Desk Shelf
  targets:
    - {widget: HTML Widget, origin: Getting Started}
    - {widget: Video Library, origin: Getting Started, params: {video_name: OpenBB Workspace Demo}}
  find_hint: the internal tools page
  policy: {phrase: the interactive-dashboard widget policy, carries: target widget, meaning: the Getting Started widget described as an interactive dashboard}
  governance: {resource: the build-an-app guide}
  build: {backend: Shelf Service, table: Shelf Register}
---
# Embed shelf

New joiners on the desk get pointed at the shelf: an embedded internal tools
page and the onboarding walkthrough video, both parked on one dashboard. The
HTML Widget is the embedded page; Video Library plays the explicitly named
clip.

The interactive-dashboard widget policy calls for the Getting Started
component whose catalog description says it is an interactive dashboard: HTML
Widget. The video selection is stated plainly because Video Library does not
expose a discoverable options list. The build-an-app guide governs the deeper
rungs - the shelf is where the desk's own tooling starts, and the guide is the
document that says how an app comes to exist, which makes it the natural source
for a governed note here.
