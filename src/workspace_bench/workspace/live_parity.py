"""Live-vs-mocked parity runner against the hosted Workspace MCP bridge.

Runs one bundled task twice — through the deterministic simulator and through
the hosted Workspace MCP (``https://backend.openbb.co/mcp``), whose bridge
executes tool calls inside the operator's real, logged-in Workspace session —
and grades both legs with the same ``grade_task``. The output is a per-leg
grade plus an agreement report: which checks pass in both worlds, and which
disagree.

The live leg operates on a real production workspace, so it is conservative
by construction:

- Everything it creates lands on one dedicated dashboard whose name carries a
  ``workspace-bench parity`` marker; created widget uuids are tracked and torn
  down in reverse order, and the previously active dashboard is restored.
- Only tasks whose initial state and oracle trace the live surface can
  faithfully reproduce are eligible (see ``check_eligibility``); everything
  else is refused with a reason rather than approximated.
- Task fixtures name simulator backends ("Bench Stark Enterprise") while the
  live workspace connects the real deployments ("Stark Fund"); an explicit
  origin map translates calls on the way out and snapshots on the way back,
  so both legs are graded in the task's own vocabulary.

Grading caveat recorded in every report: live data values come from the real
backend, not the bench's baked fixture data, so result-content checks can
legitimately differ; structural checks (widgets, params, layout, tabs, notes)
are the comparable core.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from workspace_bench.core.graders import grade_task
from workspace_bench.core.models import (
    GradeResult,
    JsonDict,
    Task,
    ToolCall,
    ToolTraceEvent,
)
from workspace_bench.workspace.fixtures import get_fixture_backend
from workspace_bench.workspace.naming import slugify

DEFAULT_LIVE_URL = "https://backend.openbb.co/mcp"
DEFAULT_ORIGIN_MAP = {"Bench Stark Enterprise": "Stark Fund"}
PARITY_MARKER = "workspace-bench parity"

# Tools the live replay knows how to execute faithfully. Registry-mutating and
# envelope-echo tools are excluded until they get their own parity story.
REPLAYABLE_TOOLS = frozenset(
    {
        "get_workspace_snapshot",
        "manage_dashboard",
        "manage_navigation_bar",
        "navigate_workspace",
        "list_available_widgets",
        "get_widget_schema",
        "get_params_options",
        "get_widget_data",
        "create_widget",
        "update_widget",
        "update_widget_layout",
        "delete_widget",
        "add_generative_widget",
        "read_widget",
        # Read-only knowledge surfaces are safe to replay against the live
        # bridge; registry-mutating tools (manage_backends/manage_apps) and
        # envelope echoes stay excluded.
        "get_skill_content",
        "read_workspace_resource",
        "get_workspace_prompt",
    }
)

ORIGIN_KEYS = ("origin", "backend_name")
PLACEHOLDER_KEYS = ("widget_uuid", "dashboard_id")


class LiveParityIneligible(ValueError):
    """Raised when a task cannot be faithfully replayed on the live bridge."""


def load_live_token() -> str | None:
    """Read the bearer token from the environment or a local ``.env`` file."""

    import os
    from pathlib import Path

    for key in ("WORKSPACE_MCP_TOKEN", "OPENBB_MCP_TOKEN"):
        if os.environ.get(key):
            return os.environ[key]
    env_path = Path(os.environ.get("WORKSPACE_MCP_ENV_FILE", ".env"))
    if not env_path.exists():
        return None
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip().removeprefix("export ").strip()
        if "=" not in line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        if key.strip() in ("WORKSPACE_MCP_TOKEN", "OPENBB_MCP_TOKEN"):
            return value.strip().strip("'\"")
    return None


# ---------------------------------------------------------------------------
# Pure helpers (no network) — unit-tested in tests/test_live_parity.py
# ---------------------------------------------------------------------------


def map_origin_values(payload: Any, mapping: dict[str, str]) -> Any:
    """Deep-copy ``payload`` with origin-key values translated via ``mapping``.

    Only dict values under the known origin keys are rewritten; prose and data
    payloads are never touched.
    """

    if isinstance(payload, dict):
        return {
            key: (
                mapping.get(str(value), value)
                if key in ORIGIN_KEYS and isinstance(value, str)
                else map_origin_values(value, mapping)
            )
            for key, value in payload.items()
        }
    if isinstance(payload, list):
        return [map_origin_values(item, mapping) for item in payload]
    return payload


class PlaceholderMapper:
    """Two-way map between simulator counter ids and live-assigned uuids.

    The simulator assigns ``widget_001``-style uuids in creation order (seeded
    widgets first, then episode-created ones) and ``dash_001``-style dashboard
    ids. The live workspace assigns real uuids in the same order, so tracking
    creation order is sufficient to translate oracle args outward and live
    snapshots back into simulator id-space.
    """

    def __init__(self) -> None:
        self._widget_count = 0
        self.sim_to_live: dict[str, str] = {}
        self.live_to_sim: dict[str, str] = {}

    def record_widget(self, live_uuid: str) -> str:
        self._widget_count += 1
        sim_uuid = f"widget_{self._widget_count:03d}"
        self.sim_to_live[sim_uuid] = live_uuid
        self.live_to_sim[live_uuid] = sim_uuid
        return sim_uuid

    def record_dashboard(self, live_id: str, sim_id: str = "dash_001") -> None:
        self.sim_to_live[sim_id] = live_id
        self.live_to_sim[live_id] = sim_id

    def to_live(self, payload: Any) -> Any:
        return self._translate(payload, self.sim_to_live)

    def to_sim(self, payload: Any) -> Any:
        return self._translate(payload, self.live_to_sim)

    def _translate(self, payload: Any, table: dict[str, str]) -> Any:
        if isinstance(payload, dict):
            return {
                key: (
                    table.get(str(value), value)
                    if key in PLACEHOLDER_KEYS and isinstance(value, str)
                    else self._translate(value, table)
                )
                for key, value in payload.items()
            }
        if isinstance(payload, list):
            return [self._translate(item, table) for item in payload]
        return payload


def extract_widget_uuid(payload: JsonDict) -> str | None:
    """Find the created widget uuid in a live tool result payload."""

    def visit(node: Any) -> str | None:
        if isinstance(node, dict):
            value = node.get("widget_uuid")
            if isinstance(value, str) and value:
                return value
            for child in node.values():
                found = visit(child)
                if found:
                    return found
        if isinstance(node, list):
            for child in node:
                found = visit(child)
                if found:
                    return found
        return None

    return visit(payload.get("data") if isinstance(payload.get("data"), (dict, list)) else payload)


def extract_dashboard_id(payload: JsonDict) -> str | None:
    """Find the created dashboard id in a live tool result payload."""

    data = payload.get("data")
    candidates = [data, payload]
    for node in candidates:
        if not isinstance(node, dict):
            continue
        for key in ("dashboard_id", "id", "uuid"):
            value = node.get(key)
            if isinstance(value, str) and value:
                return value
        inner = node.get("dashboard")
        if isinstance(inner, dict):
            for key in ("dashboard_id", "id", "uuid"):
                value = inner.get(key)
                if isinstance(value, str) and value:
                    return value
    return None


@dataclass(frozen=True)
class SeedStep:
    """One live setup call derived from a task's initial state."""

    call: ToolCall
    kind: str  # "dashboard" | "tabs" | "activate_tab" | "widget" | "layout"


@dataclass(frozen=True)
class SeedPlan:
    """Faithful live reproduction of a task's ``initial_state.dashboard``."""

    steps: tuple[SeedStep, ...]
    dashboard_name: str
    tab_ids: tuple[str, ...]
    seeded_widget_count: int


def check_eligibility(task: Task, origin_map: dict[str, str]) -> None:
    """Refuse tasks the live replay cannot reproduce faithfully."""

    if task.code_task is not None:
        raise LiveParityIneligible("real-code tasks have no live-bridge replay")
    initial = task.initial_state or {}
    unsupported = sorted(set(initial) - {"dashboard"})
    if unsupported:
        raise LiveParityIneligible(
            f"initial_state keys not yet supported live: {', '.join(unsupported)}"
        )
    dashboard = initial.get("dashboard") or {}
    for widget_spec in dashboard.get("generated_widgets") or []:
        raise LiveParityIneligible(
            f"seeded generated widgets not yet supported live: {widget_spec!r}"
        )
    for tab in dashboard.get("tabs") or []:
        tab_id = str(tab.get("id", ""))
        tab_name = str(tab.get("name", tab_id))
        if not tab_id and not tab_name:
            # The simulator's unnamed default tab; the live dashboard's own
            # default tab plays this role, so nothing is created for it.
            continue
        if tab_id and tab_id != slugify(tab_name, fallback=tab_id):
            raise LiveParityIneligible(
                f"tab id {tab_id!r} is not the slug of its name {tab_name!r}; "
                "the live navigation bar derives tab ids from names"
            )
    origins: set[str] = set()
    for widget_spec in dashboard.get("widgets") or []:
        origins.add(str(widget_spec.get("origin", "")))
    for call in task.oracle_tool_calls:
        if call.name not in REPLAYABLE_TOOLS:
            raise LiveParityIneligible(f"oracle uses non-replayable tool {call.name!r}")
        for key in ORIGIN_KEYS:
            value = call.args.get(key)
            if isinstance(value, str):
                origins.add(value)
    unmapped = sorted(origin for origin in origins if origin and origin not in origin_map)
    if unmapped:
        raise LiveParityIneligible(
            f"origins without a live mapping: {', '.join(unmapped)}"
        )


def derive_seed_plan(task: Task) -> SeedPlan:
    """Translate ``initial_state.dashboard`` into ordinary live tool calls.

    The simulator seeds this state directly; the live workspace only offers the
    public tool surface, so the seed becomes a prefix of tool calls executed
    before the oracle replay begins. Seed calls are setup, not agent behavior,
    and are excluded from the graded trace.
    """

    dashboard = (task.initial_state or {}).get("dashboard") or {}
    name = str(dashboard.get("name", "Workspace Bench"))
    steps: list[SeedStep] = [
        SeedStep(
            ToolCall(
                "manage_dashboard",
                {
                    "operation": "create",
                    "name": f"{name} · {PARITY_MARKER}",
                    "activate": True,
                },
            ),
            kind="dashboard",
        )
    ]
    tabs = dashboard.get("tabs") or []
    tab_ids = tuple(
        str(tab.get("id", slugify(str(tab.get("name", "")), fallback="tab"))) for tab in tabs
    )
    named_tabs = [
        tab for tab in tabs if str(tab.get("id", "")) or str(tab.get("name", ""))
    ]
    if named_tabs:
        steps.append(
            SeedStep(
                ToolCall(
                    "manage_navigation_bar",
                    {
                        "operation": "create",
                        "tabs": [
                            {"name": str(tab.get("name", tab.get("id", "")))}
                            for tab in named_tabs
                        ],
                    },
                ),
                kind="tabs",
            )
        )
        first_tab = named_tabs[0]
        first_tab_id = str(
            first_tab.get("id", slugify(str(first_tab.get("name", "")), fallback="tab"))
        )
        steps.append(
            SeedStep(
                ToolCall(
                    "navigate_workspace",
                    {"operation": "tab", "tab_id": first_tab_id},
                ),
                kind="activate_tab",
            )
        )
    widget_specs = list(dashboard.get("widgets") or [])
    for spec in widget_specs:
        target_tab = str(spec.get("tab_id", tab_ids[0] if tab_ids else ""))
        if target_tab and tab_ids and target_tab != tab_ids[0]:
            steps.append(
                SeedStep(
                    ToolCall(
                        "navigate_workspace",
                        {"operation": "tab", "tab_id": target_tab},
                    ),
                    kind="activate_tab",
                )
            )
        steps.append(
            SeedStep(
                ToolCall(
                    "create_widget",
                    {
                        "origin": str(spec["origin"]),
                        "widget_id": str(spec["widget_id"]),
                        "data_args": spec.get("data_args") or {},
                    },
                ),
                kind="widget",
            )
        )
        layout = spec.get("layout") or {}
        if layout:
            steps.append(
                SeedStep(
                    ToolCall(
                        "update_widget_layout",
                        {
                            # widget_uuid is patched in at execution time from
                            # the create_widget response.
                            "widget_uuid": "",
                            **{k: layout[k] for k in ("x", "y", "w", "h") if k in layout},
                        },
                    ),
                    kind="layout",
                )
            )
    return SeedPlan(
        steps=tuple(steps),
        dashboard_name=name,
        tab_ids=tab_ids,
        seeded_widget_count=len(widget_specs),
    )


def normalize_live_snapshot(
    *,
    task: Task,
    dashboard_info: JsonDict,
    dashboard_name: str,
    widget_details: dict[str, JsonDict],
    generated_uuids: set[str],
    generated_meta: dict[str, JsonDict],
    mapper: PlaceholderMapper,
    reverse_origin_map: dict[str, str],
    tab_id_map: dict[str, str] | None = None,
) -> JsonDict:
    """Rebuild a simulator-shaped snapshot from live workspace responses.

    ``dashboard_info`` is ``workspace_state.current_dashboard_info`` from the
    live snapshot; ``widget_details`` maps live widget uuids to ``read_widget``
    payloads. Widget ``type`` is filled from the bundled fixture schema (static
    catalog data, not runtime state). Live uuids are translated back into
    simulator placeholder ids so both legs share one id-space; ``tab_id_map``
    does the same for tab ids (the live default tab stands in for the
    simulator's unnamed seed tab).
    """

    tab_ids = dict(tab_id_map or {})
    tabs_payload: list[JsonDict] = []
    widgets_payload: list[JsonDict] = []
    for tab in dashboard_info.get("tabs") or []:
        live_tab_id = str(tab.get("tab_id", tab.get("id", "")))
        tab_id = tab_ids.get(live_tab_id, live_tab_id)
        tab_name = str(tab.get("tab_name", tab.get("name", tab_id)))
        layout_by_uuid = {
            str(item.get("widget_uuid", "")): item for item in tab.get("layout") or []
        }
        tab_layout: list[JsonDict] = []
        for widget_ref in tab.get("widgets") or []:
            live_uuid = str(widget_ref.get("widget_uuid", ""))
            sim_uuid = mapper.live_to_sim.get(live_uuid, live_uuid)
            detail = widget_details.get(live_uuid) or {}
            origin = str(detail.get("origin", ""))
            origin = reverse_origin_map.get(origin, origin)
            widget_id = str(detail.get("widget_id", ""))
            layout_item = layout_by_uuid.get(live_uuid) or {}
            layout_payload: JsonDict = {
                "widget_uuid": sim_uuid,
                "widget_id": widget_id,
                "origin": origin,
                "tab_id": tab_id,
                "x": float(layout_item.get("x", 0)),
                "y": float(layout_item.get("y", 0)),
                "w": float(layout_item.get("w", 20)),
                "h": float(layout_item.get("h", 10)),
            }
            tab_layout.append(layout_payload)
            generated = live_uuid in generated_uuids
            meta = generated_meta.get(live_uuid) or {}
            widgets_payload.append(
                {
                    "widget_uuid": sim_uuid,
                    "widget_id": widget_id,
                    "origin": origin,
                    "name": str(detail.get("name", widget_ref.get("name", ""))),
                    "type": (
                        str(meta.get("widget_type", ""))
                        if generated
                        else _fixture_widget_type(origin, widget_id)
                    ),
                    "data_args": detail.get("data_args") or {},
                    "ui_args": detail.get("ui_args") or {},
                    "generated": generated,
                    "generated_data": detail.get("data") if generated else None,
                    "chart_params": meta.get("chart_params") if generated else None,
                    "description": detail.get("description"),
                    "layout": layout_payload,
                }
            )
        tabs_payload.append({"id": tab_id, "name": tab_name, "layout": tab_layout})
    composition: JsonDict = {
        "dashboard_id": mapper.live_to_sim.get(
            str(dashboard_info.get("id", "")), str(dashboard_info.get("id", ""))
        ),
        "name": dashboard_name,
        "navigation_bar": len(tabs_payload) > 1,
        "tabs": tabs_payload,
        "widgets": widgets_payload,
    }
    return {
        "generated_at": 0,
        "dashboard_composition": composition,
        "dashboards": {composition["dashboard_id"]: composition},
        "artifacts": [],
        "files": [],
        "context": {},
        "source": "live-workspace-mcp",
        "task_id": task.id,
    }


def _fixture_widget_type(origin: str, widget_id: str) -> str:
    """Look up the static widget type from the bundled fixture catalog."""

    try:
        backend = get_fixture_backend("stark-enterprise")
    except Exception:  # noqa: BLE001 - type stays best-effort for non-Stark origins.
        return ""
    if backend.name != origin:
        return ""
    widget = backend.widgets.get(widget_id) or {}
    return str(widget.get("type", ""))


# Issue codes that grade returned data content. The live backend serves its
# own data, not the bench fixture's, so these can disagree without indicating
# a simulator-fidelity defect; every other disagreement is structural.
DATA_CONTENT_ISSUE_CODES = frozenset({"missing_tool_result"})


def grade_agreement(mocked: GradeResult, live: GradeResult) -> JsonDict:
    """Summarize where the two legs agree and disagree, by issue code."""

    mocked_issues = {(issue.code, issue.message) for issue in mocked.issues}
    live_issues = {(issue.code, issue.message) for issue in live.issues}
    live_only = live_issues - mocked_issues
    structural = {
        (c, m) for c, m in live_only if c not in DATA_CONTENT_ISSUE_CODES
    }
    data_content = live_only - structural
    return {
        "verdict_agree": mocked.passed == live.passed,
        "structural_agree": mocked.passed == live.passed or not structural,
        "mocked_passed": mocked.passed,
        "live_passed": live.passed,
        "issues_in_both": sorted(f"{c}: {m}" for c, m in mocked_issues & live_issues),
        "live_only_structural": sorted(f"{c}: {m}" for c, m in structural),
        "live_only_data_content": sorted(f"{c}: {m}" for c, m in data_content),
        "mocked_only_issues": sorted(f"{c}: {m}" for c, m in mocked_issues - live_issues),
        "note": (
            "Live data values come from the real backend, not bench fixture "
            "data; data-content differences are expected, structural "
            "differences are findings."
        ),
    }


# ---------------------------------------------------------------------------
# Live session
# ---------------------------------------------------------------------------


@dataclass
class LiveLegRecord:
    """Everything the live leg observed, for the report and for teardown."""

    trace: list[ToolTraceEvent] = field(default_factory=list)
    created_widget_uuids: list[str] = field(default_factory=list)
    generated_widget_uuids: set[str] = field(default_factory=set)
    generated_meta: dict[str, JsonDict] = field(default_factory=dict)
    dashboard_live_id: str = ""
    prior_dashboard_id: str = ""
    teardown_log: list[str] = field(default_factory=list)
    seed_log: list[str] = field(default_factory=list)


async def run_live_parity(
    task: Task,
    *,
    url: str = DEFAULT_LIVE_URL,
    token: str,
    origin_map: dict[str, str] | None = None,
    keep: bool = False,
) -> JsonDict:
    """Run one task mocked and live, grade both, and report agreement.

    The mocked leg runs first and is authoritative for oracle correctness; the
    live leg then seeds, replays, grades, and — unless ``keep`` — tears down
    everything it created and restores the previously active dashboard.
    """

    from workspace_bench.agents import build_agent
    from workspace_bench.core.runner import TaskRunner

    origins = dict(origin_map or DEFAULT_ORIGIN_MAP)
    reverse_origins = {live: sim for sim, live in origins.items()}
    check_eligibility(task, origins)
    seed_plan = derive_seed_plan(task)

    mocked = TaskRunner().run(task, build_agent("oracle"))

    record = LiveLegRecord()
    mapper = PlaceholderMapper()
    session_cm = _open_session(url, token)
    async with session_cm as session:
        before = await _call(session, "get_workspace_snapshot", {})
        before_state = (before.get("data") or {}).get("workspace_state") or {}
        record.prior_dashboard_id = str(
            before_state.get("current_dashboard_uuid")
            or (before_state.get("current_dashboard_info") or {}).get("id")
            or ""
        )
        if not record.prior_dashboard_id:
            record.seed_log.append(
                "prior dashboard unknown; it will not be restored after teardown"
            )
        reusable_id = _find_parked_dashboard(before)
        try:
            await _seed(session, seed_plan, origins, mapper, record, reuse_id=reusable_id)
            await _replay(session, task, origins, reverse_origins, mapper, record)
            live_grade, live_snapshot = await _collect_and_grade(
                session, task, seed_plan, mapper, reverse_origins, record
            )
        finally:
            if keep:
                record.teardown_log.append("kept: teardown skipped by request")
            else:
                await _teardown(session, record)

    report: JsonDict = {
        "task_id": task.qualified_id,
        "live_url": url,
        "origin_map": origins,
        "eligible": True,
        "mocked": _grade_payload(mocked.grade),
        "live": _grade_payload(live_grade),
        "agreement": grade_agreement(mocked.grade, live_grade),
        "live_seed": record.seed_log,
        "live_teardown": record.teardown_log,
        "live_snapshot": live_snapshot,
        "live_trace": [
            {
                "index": event.index,
                "tool": event.call.name,
                "args": event.call.args,
                "ok": event.ok,
                **(
                    {"error": (event.result.get("error") or {}).get("message")}
                    if not event.ok
                    else {}
                ),
            }
            for event in record.trace
        ],
    }
    return report


def _grade_payload(grade: GradeResult) -> JsonDict:
    return {
        "passed": grade.passed,
        "score": grade.score,
        "checks_passed": grade.checks_passed,
        "checks_total": grade.checks_total,
        "state": f"{grade.state_checks_passed}/{grade.state_checks_total}",
        "trace": f"{grade.trace_checks_passed}/{grade.trace_checks_total}",
        "runtime": f"{grade.runtime_checks_passed}/{grade.runtime_checks_total}",
        "issues": [f"{issue.code}: {issue.message}" for issue in grade.issues],
    }


def _open_session(url: str, token: str) -> Any:
    """Return an async context manager yielding a connected MCP session."""

    try:
        from contextlib import asynccontextmanager

        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client
    except ImportError as error:  # pragma: no cover - exercised via CLI only.
        raise RuntimeError(
            "live-parity requires optional dependencies; run via "
            "`uv run --extra live workspace-bench live-parity ...`"
        ) from error

    @asynccontextmanager
    async def connect() -> Any:
        headers = {"Authorization": f"Bearer {token}"}
        async with streamablehttp_client(url, headers=headers) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                yield session

    return connect()


async def _call(session: Any, name: str, args: JsonDict, *, timeout: float = 90) -> JsonDict:
    import asyncio

    result = await asyncio.wait_for(session.call_tool(name, args), timeout=timeout)
    for item in result.content or []:
        text = getattr(item, "text", None)
        if not text:
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    return {"ok": not result.isError, "command": name, "data": None}


def _find_parked_dashboard(before_snapshot: JsonDict) -> str:
    """Find an empty cleanup dashboard from a previous run to reuse.

    The live surface cannot delete dashboards, so teardown parks the emptied
    dashboard under a cleanup name; reusing it keeps the operator's workspace
    at a single parked dashboard no matter how many parity runs execute. Only
    a parked dashboard with no widgets and at most one tab is safe to reuse.
    """

    parked_name = f"[cleanup] {PARITY_MARKER} — delete me"
    for entry in (before_snapshot.get("data") or {}).get("dashboards") or []:
        if not isinstance(entry, dict) or str(entry.get("name", "")) != parked_name:
            continue
        if int(entry.get("widget_count") or 0) == 0 and int(entry.get("tab_count") or 0) <= 1:
            return str(entry.get("dashboard_id", ""))
    return ""


async def _seed(
    session: Any,
    plan: SeedPlan,
    origins: dict[str, str],
    mapper: PlaceholderMapper,
    record: LiveLegRecord,
    *,
    reuse_id: str = "",
) -> None:
    pending_layout_uuid = ""
    for step in plan.steps:
        if step.kind == "dashboard" and reuse_id:
            rename = await _call(
                session,
                "manage_dashboard",
                {
                    "operation": "update",
                    "dashboard_id": reuse_id,
                    "name": str(step.call.args["name"]),
                },
            )
            navigate = await _call(
                session,
                "navigate_workspace",
                {"operation": "dashboard", "dashboard_id": reuse_id},
            )
            if rename.get("ok") and navigate.get("ok"):
                record.dashboard_live_id = reuse_id
                mapper.record_dashboard(reuse_id)
                record.seed_log.append(f"reused parked cleanup dashboard: {reuse_id}")
                await _wait_for_active_dashboard(session, reuse_id)
                record.seed_log.append("dashboard activation confirmed")
                # The parked widget_count can be stale (bridge writes apply
                # asynchronously), so sweep any orphans before seeding.
                removed = await _delete_all_widgets(session, reuse_id)
                if removed:
                    record.seed_log.append(f"swept {removed} orphan widget(s) before seeding")
                continue
            record.seed_log.append("parked dashboard reuse failed; creating fresh")
        args = map_origin_values(dict(step.call.args), origins)
        if step.kind == "layout":
            args["widget_uuid"] = pending_layout_uuid
        payload = await _call(session, step.call.name, args)
        if (
            not payload.get("ok")
            and "error" not in payload
            and step.kind in {"activate_tab", "layout"}
        ):
            # The bridge occasionally drops the envelope on write operations;
            # retry only steps that are safe to repeat (never creations).
            payload = await _call(session, step.call.name, args)
        if not payload.get("ok"):
            raise RuntimeError(
                f"live seed failed at {step.call.name} ({step.kind}): "
                f"{json.dumps(payload)[:500]}"
            )
        if step.kind == "dashboard":
            live_id = extract_dashboard_id(payload) or ""
            if not live_id:
                raise RuntimeError(
                    "live seed could not identify the created dashboard id in "
                    f"{json.dumps(payload)[:500]}"
                )
            record.dashboard_live_id = live_id
            mapper.record_dashboard(live_id)
            record.seed_log.append(f"dashboard created: {live_id}")
            # Bridge writes apply asynchronously in the browser; wait for the
            # activation before creating widgets so nothing can land on the
            # operator's real dashboard.
            await _wait_for_active_dashboard(session, live_id)
            record.seed_log.append("dashboard activation confirmed")
        if step.kind == "widget":
            live_uuid = extract_widget_uuid(payload) or ""
            if not live_uuid:
                raise RuntimeError("live seed could not identify a created widget uuid")
            sim_uuid = mapper.record_widget(live_uuid)
            record.created_widget_uuids.append(live_uuid)
            pending_layout_uuid = live_uuid
            record.seed_log.append(f"seeded {sim_uuid} -> {live_uuid}")
            continue
        record.seed_log.append(f"{step.call.name}:{step.kind} ok")


async def _replay(
    session: Any,
    task: Task,
    origins: dict[str, str],
    reverse_origins: dict[str, str],
    mapper: PlaceholderMapper,
    record: LiveLegRecord,
) -> None:
    for call in task.oracle_tool_calls:
        live_args = map_origin_values(mapper.to_live(dict(call.args)), origins)
        payload = await _call(session, call.name, live_args)
        if call.name in {"create_widget", "add_generative_widget"} and payload.get("ok"):
            live_uuid = extract_widget_uuid(payload) or ""
            if live_uuid:
                mapper.record_widget(live_uuid)
                record.created_widget_uuids.append(live_uuid)
                if call.name == "add_generative_widget":
                    record.generated_widget_uuids.add(live_uuid)
                    record.generated_meta[live_uuid] = {
                        "widget_type": call.args.get("widget_type"),
                        "chart_params": call.args.get("chart_params"),
                    }
        graded_result = map_origin_values(mapper.to_sim(payload), reverse_origins)
        record.trace.append(
            ToolTraceEvent(
                index=len(record.trace) + 1,
                call=call,
                ok=bool(payload.get("ok")),
                result=graded_result,
            )
        )


async def _collect_and_grade(
    session: Any,
    task: Task,
    plan: SeedPlan,
    mapper: PlaceholderMapper,
    reverse_origins: dict[str, str],
    record: LiveLegRecord,
) -> tuple[GradeResult, JsonDict]:
    # The bridge acknowledges write commands before the browser applies them
    # (verified: an update_widget reads stale immediately and correct ~3s
    # later), so poll until two consecutive collections are identical.
    import asyncio

    info, widget_details = await _collect_once(session, record)
    for _ in range(10):
        await asyncio.sleep(1.5)
        next_info, next_details = await _collect_once(session, record)
        if next_info == info and next_details == widget_details:
            break
        info, widget_details = next_info, next_details
    live_tabs = info.get("tabs") or []
    tab_id_map: dict[str, str] = {}
    if len(live_tabs) == len(plan.tab_ids):
        for live_tab, sim_tab_id in zip(live_tabs, plan.tab_ids):
            live_tab_id = str(live_tab.get("tab_id", live_tab.get("id", "")))
            if live_tab_id != sim_tab_id:
                tab_id_map[live_tab_id] = sim_tab_id
    snapshot = normalize_live_snapshot(
        task=task,
        dashboard_info=info,
        # The oracle may rename the dashboard mid-episode, so the graded name
        # is the live one (the seed name carries the parity marker as a
        # suffix, which contains-style name checks tolerate).
        dashboard_name=str(info.get("name") or plan.dashboard_name),
        widget_details=widget_details,
        generated_uuids=record.generated_widget_uuids,
        generated_meta=record.generated_meta,
        mapper=mapper,
        reverse_origin_map=reverse_origins,
        tab_id_map=tab_id_map,
    )
    grade = grade_task(task, snapshot, tuple(record.trace))
    return grade, snapshot


async def _delete_all_widgets(session: Any, dashboard_id: str) -> int:
    """Remove every widget on a dashboard, waiting until a snapshot confirms."""

    import asyncio

    removed = 0
    for _ in range(5):
        payload = await _call(session, "get_workspace_snapshot", {})
        workspace_state = (payload.get("data") or {}).get("workspace_state") or {}
        info = workspace_state.get("current_dashboard_info") or {}
        if str(info.get("id", "")) != dashboard_id:
            break
        uuids = [
            str(ref.get("widget_uuid", ""))
            for tab in info.get("tabs") or []
            for ref in tab.get("widgets") or []
            if ref.get("widget_uuid")
        ]
        if not uuids:
            break
        for widget_uuid in uuids:
            await _call(session, "delete_widget", {"widget_uuid": widget_uuid})
            removed += 1
        await asyncio.sleep(1.5)
    return removed


async def _wait_for_active_dashboard(
    session: Any, dashboard_id: str, *, tries: int = 10, delay: float = 1.5
) -> None:
    import asyncio

    for attempt in range(tries):
        payload = await _call(session, "get_workspace_snapshot", {})
        workspace_state = (payload.get("data") or {}).get("workspace_state") or {}
        info = workspace_state.get("current_dashboard_info") or {}
        active_id = str(
            info.get("id") or workspace_state.get("current_dashboard_uuid") or ""
        )
        if active_id == dashboard_id:
            return
        if attempt < tries - 1:
            await asyncio.sleep(delay)
    raise RuntimeError(
        f"created dashboard {dashboard_id} never became active; aborting seed"
    )


async def _collect_once(
    session: Any, record: LiveLegRecord
) -> tuple[JsonDict, dict[str, JsonDict]]:
    """Fetch the active dashboard info and per-widget details once."""

    snapshot_payload = await _call(session, "get_workspace_snapshot", {})
    data = snapshot_payload.get("data") or {}
    workspace_state = data.get("workspace_state") or {}
    info = workspace_state.get("current_dashboard_info") or {}
    active_id = str(
        info.get("id") or workspace_state.get("current_dashboard_uuid") or ""
    )
    if active_id != record.dashboard_live_id:
        raise RuntimeError(
            "live workspace is no longer on the parity dashboard; refusing to "
            f"grade (active={active_id!r}, parity={record.dashboard_live_id!r})"
        )
    widget_details: dict[str, JsonDict] = {}
    for tab in info.get("tabs") or []:
        for widget_ref in tab.get("widgets") or []:
            live_uuid = str(widget_ref.get("widget_uuid", ""))
            if not live_uuid or live_uuid in widget_details:
                continue
            detail_payload = await _call(session, "read_widget", {"widget_uuid": live_uuid})
            detail_data = detail_payload.get("data")
            detail = detail_data.get("widget") if isinstance(detail_data, dict) else None
            if isinstance(detail, dict):
                widget_details[live_uuid] = detail
            elif isinstance(detail_data, dict):
                widget_details[live_uuid] = detail_data
            else:
                widget_details[live_uuid] = {}
    return info, widget_details


async def _teardown(session: Any, record: LiveLegRecord) -> None:
    for live_uuid in reversed(record.created_widget_uuids):
        payload = await _call(session, "delete_widget", {"widget_uuid": live_uuid})
        if payload.get("ok"):
            outcome = "ok"
        elif "not found" in str((payload.get("error") or {}).get("message", "")).lower():
            outcome = "already deleted during the episode"
        else:
            outcome = "FAILED"
        record.teardown_log.append(f"delete_widget {live_uuid}: {outcome}")
    if record.dashboard_live_id:
        # The live surface has no dashboard-delete operation ({create, read,
        # update} only), so the emptied dashboard is renamed for one-click
        # manual deletion in the Workspace UI.
        rename = await _call(
            session,
            "manage_dashboard",
            {
                "operation": "update",
                "dashboard_id": record.dashboard_live_id,
                "name": f"[cleanup] {PARITY_MARKER} — delete me",
            },
        )
        record.teardown_log.append(
            "dashboard delete is not in the live surface; "
            + (
                "emptied and renamed '[cleanup] … — delete me' for manual removal"
                if rename.get("ok")
                else f"rename FAILED for {record.dashboard_live_id}"
            )
        )
    if record.prior_dashboard_id:
        payload = await _call(
            session,
            "navigate_workspace",
            {"operation": "dashboard", "dashboard_id": record.prior_dashboard_id},
        )
        record.teardown_log.append(
            f"restore prior dashboard: {'ok' if payload.get('ok') else 'FAILED'}"
        )
