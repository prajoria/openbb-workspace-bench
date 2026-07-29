"""Materialize the stark-workspace-a baseline as a reviewable data file.

stark-workspace-a is the everything-mounted lived-in workspace used as the
workspace-tasks baseline: Home plus every Stark app dashboard (as built from the
canonical catalog) plus the three personal desk dashboards from
stark-onboard-a, with all four catalog backends connected. Re-run this
script to regenerate ``data/initial_states/stark_workspace_a.json``.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))

from workspace_bench.workspace.default_setup import (  # noqa: E402
    _build_default_v1_state,
    _load_initial_state_file,
)

OUT_PATH = (
    REPO / "src" / "workspace_bench" / "data" / "initial_states" / "stark_workspace_a.json"
)

PERSONAL_DASHBOARDS = ("Morning Markets", "IC Prep - Q3 Review", "Ops Daily Checks")


def build_state() -> dict:
    state = _build_default_v1_state()
    onboard = _load_initial_state_file("stark_onboard_a.json")
    personal = [
        copy.deepcopy(dashboard)
        for dashboard in onboard["dashboards"]
        if dashboard.get("name") in PERSONAL_DASHBOARDS
    ]
    if len(personal) != len(PERSONAL_DASHBOARDS):
        raise AssertionError(
            f"expected {PERSONAL_DASHBOARDS} in stark-onboard-a, found "
            f"{[d.get('name') for d in personal]}"
        )
    for dashboard in personal:
        dashboard["activate"] = False
    return {"dashboards": [*state["dashboards"], *personal]}


def main() -> None:
    state = build_state()
    names = [dashboard["name"] for dashboard in state["dashboards"]]
    if names[0] != "Home" or len(names) != len(set(names)):
        raise AssertionError(f"unexpected dashboard composition: {names}")
    payload = {
        "source": {
            "generator": "scripts/generators/generate_workspace_states.py",
            "description": (
                "Home + all Stark Enterprise app dashboards + the "
                "stark-onboard-a personal desk dashboards; backends "
                "stark-enterprise-x, support-daloopa-skills, "
                "getting-started, widget-examples."
            ),
        },
        "initial_state": state,
    }
    OUT_PATH.write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n")
    print(f"Wrote {OUT_PATH.name}: {len(names)} dashboards ({names[0]} first)")


if __name__ == "__main__":
    main()
