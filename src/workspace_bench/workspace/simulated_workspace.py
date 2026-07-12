"""In-memory Workspace MCP simulator used by the benchmark runner."""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass, field
from typing import Any

from workspace_bench.core.models import FixtureBackendRef, JsonDict, RuntimeChecks, ToolCall
from workspace_bench.workspace import backend_validation
from workspace_bench.workspace.fixtures import FixtureBackend, default_fixture_backends
from workspace_bench.workspace.runtime import task_widget_data


WORKSPACE_SKILLS: dict[str, JsonDict] = {
    "finance-earnings-prep": {
        "slug": "finance-earnings-prep",
        "name": "Finance Earnings Prep",
        "description": "Build an earnings preview from estimates, guidance, transcript, price reaction, and thesis risks.",
        "content": (
            "Earnings prep workflow: compare internal estimates to street numbers, "
            "identify surprise drivers, review guidance, inspect transcript tone, "
            "and produce action items for the portfolio manager."
        ),
    },
    "finance-tearsheet": {
        "slug": "finance-tearsheet",
        "name": "Finance Tearsheet",
        "description": "Create a concise company or asset tear sheet with valuation, catalysts, risks, and ownership context.",
        "content": (
            "Tearsheet workflow: gather price action, fundamentals, valuation, "
            "catalysts, risks, ownership, and a short investment conclusion."
        ),
    },
    "finance-guidance-tracker": {
        "slug": "finance-guidance-tracker",
        "name": "Finance Guidance Tracker",
        "description": "Track company guidance changes, management claims, and follow-up evidence.",
        "content": (
            "Guidance tracker workflow: extract management claims, compare them "
            "with prior guidance, flag changed assumptions, and list evidence gaps."
        ),
    },
    "finance-comps": {
        "slug": "finance-comps",
        "name": "Finance Comps",
        "description": "Compare companies or assets using peer valuation and operating metrics.",
        "content": (
            "Comps workflow: define the peer set, normalize metrics, compare "
            "valuation multiples, and explain why outliers deserve premium or discount."
        ),
    },
}

WORKSPACE_PROMPTS: dict[str, str] = {
    "workspace_tool_usage": (
        "Workspace tool usage guidance: inspect current state first, discover "
        "backend catalogs before creating widgets, read schemas before mutation, "
        "and prefer deterministic Workspace MCP tools over shell or browser hacks. "
        "Stable phrase: schema-before-create workspace tool discipline."
    ),
    "workspace_session_context": (
        "Workspace session context guidance: use the current dashboard and tab "
        "from session context, create or navigate tabs deliberately, and keep "
        "generated notes tied to durable dashboard artifacts. Stable phrase: "
        "current-dashboard current-tab session grounding."
    ),
}

APP_BUILDER_INDEX_URI = "openbb://workspace/app-builder/index"


def slugify(value: str) -> str:
    """Slugify a Workspace navigation tab name."""

    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "tab"


@dataclass
class LayoutItem:
    x: float
    y: float
    w: float
    h: float
    tab_id: str = ""
    min_w: float | None = None
    min_h: float | None = None
    max_w: float | None = None
    max_h: float | None = None

    def to_dict(self, widget_uuid: str, widget_id: str, origin: str) -> JsonDict:
        payload: JsonDict = {
            "widget_uuid": widget_uuid,
            "widget_id": widget_id,
            "origin": origin,
            "tab_id": self.tab_id,
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h,
        }
        for key in ("min_w", "min_h", "max_w", "max_h"):
            value = getattr(self, key)
            if value is not None:
                payload[key] = value
        return payload


@dataclass
class WidgetInstance:
    widget_uuid: str
    widget_id: str
    origin: str
    name: str
    widget_type: str
    data_args: JsonDict = field(default_factory=dict)
    ui_args: JsonDict = field(default_factory=dict)
    generated: bool = False
    generated_data: Any = None
    chart_params: JsonDict | None = None
    description: str | None = None
    layout: LayoutItem = field(default_factory=lambda: LayoutItem(0, 0, 20, 10))

    def to_dict(self) -> JsonDict:
        return {
            "widget_uuid": self.widget_uuid,
            "widget_id": self.widget_id,
            "origin": self.origin,
            "name": self.name,
            "type": self.widget_type,
            "data_args": copy.deepcopy(self.data_args),
            "ui_args": copy.deepcopy(self.ui_args),
            "generated": self.generated,
            "generated_data": copy.deepcopy(self.generated_data),
            "chart_params": copy.deepcopy(self.chart_params),
            "description": self.description,
            "layout": self.layout.to_dict(
                self.widget_uuid, self.widget_id, self.origin
            ),
        }


@dataclass
class Tab:
    tab_id: str
    name: str

    def to_dict(self) -> JsonDict:
        return {"id": self.tab_id, "name": self.name}


@dataclass
class Dashboard:
    dashboard_id: str
    name: str
    tabs: dict[str, Tab] = field(default_factory=lambda: {"": Tab("", "")})
    widgets: dict[str, WidgetInstance] = field(default_factory=dict)
    navigation_bar: bool = False

    def ensure_tab(self, tab_id: str, name: str | None = None) -> None:
        if tab_id not in self.tabs:
            self.tabs[tab_id] = Tab(tab_id, name or tab_id)


class SimulatedWorkspace:
    """A deterministic subset of the Workspace MCP command surface."""

    def __init__(self, fixtures: dict[str, FixtureBackend] | None = None):
        self._fixture_registry = fixtures or default_fixture_backends()
        self.reset()

    def reset(
        self,
        backends: tuple[FixtureBackendRef, ...] | list[FixtureBackendRef] = (),
        initial_state: JsonDict | None = None,
        runtime_checks: RuntimeChecks | None = None,
    ) -> None:
        self._dash_counter = 0
        self._widget_counter = 0
        self._snapshot_counter = 0
        self._backend_counter = 0
        self.dashboards: dict[str, Dashboard] = {}
        self.active_dashboard_id: str | None = None
        self.active_tab_id: str = ""
        self.backends: dict[str, FixtureBackend] = {}
        self.backend_ids_by_name: dict[str, str] = {}
        self.custom_backends: dict[str, JsonDict] = {}
        self.declared_backends: dict[str, JsonDict] = {}
        self.runtime_checks = runtime_checks

        for backend_ref in backends:
            self.register_backend(backend_ref.name, backend_ref.backend_id, backend_ref.url)

        initial_state = initial_state or {}
        for custom_spec in initial_state.get("custom_backends", []) or []:
            self._seed_custom_backend(custom_spec)
        dashboard_specs = initial_state.get("dashboards")
        if isinstance(dashboard_specs, list) and dashboard_specs:
            for dashboard_spec in dashboard_specs:
                if isinstance(dashboard_spec, dict):
                    self.seed_dashboard(dashboard_spec)
        elif dashboard_spec := initial_state.get("dashboard"):
            self.seed_dashboard(dashboard_spec)
        else:
            dashboard = self.create_dashboard("Workspace Bench", activate=True)
            self.active_dashboard_id = dashboard.dashboard_id

    def register_backend(
        self, name: str, backend_id: str | None = None, url: str | None = None
    ) -> str:
        backend = self._fixture_registry.get(name)
        if backend is None:
            raise KeyError(f"Unknown fixture backend {name!r}")
        self._backend_counter += 1
        resolved_id = backend_id or f"backend_{self._backend_counter:03d}"
        if url:
            backend = FixtureBackend(
                slug=backend.slug,
                name=backend.name,
                widgets=backend.widgets,
                apps=backend.apps,
                default_url=url,
            )
        self.backends[resolved_id] = backend
        self.backend_ids_by_name[backend.name] = resolved_id
        return resolved_id

    def _register_custom_backend(
        self,
        name: str,
        url: str,
        widgets: dict[str, JsonDict],
        apps: list[JsonDict],
        warnings: list[str],
        backend_id: str | None = None,
    ) -> str:
        """Register an authored (custom) backend from validated payloads."""

        self._backend_counter += 1
        resolved_id = backend_id or f"backend_{self._backend_counter:03d}"
        backend = FixtureBackend(
            slug=f"custom-{backend_validation.slugify(name)}",
            name=name,
            widgets=copy.deepcopy(widgets),
            apps=copy.deepcopy(apps),
            default_url=url,
        )
        self.backends[resolved_id] = backend
        self.backend_ids_by_name[name] = resolved_id
        self.custom_backends[resolved_id] = {
            "name": name,
            "url": url,
            "warnings": list(warnings),
        }
        return resolved_id

    def _seed_custom_backend(self, spec: JsonDict) -> str:
        """Seed a custom backend from task initial_state, bypassing validation.

        Seeded state represents "whatever the author's backend currently serves" —
        including broken payloads a repair task expects the agent to fix via
        ``manage_backends operation='refresh'``.
        """

        widgets: dict[str, JsonDict] = {}
        for widget_id, definition in (spec.get("widgets_json") or {}).items():
            stored = dict(definition)
            stored.setdefault(
                "type",
                stored.get("defaultViz") if isinstance(stored.get("defaultViz"), str) else "table",
            )
            widgets[str(widget_id)] = stored
        apps: list[JsonDict] = []
        for app in spec.get("apps_json") or []:
            stored = dict(app)
            stored.setdefault(
                "template_id",
                stored.get("templateId")
                or backend_validation.slugify(str(stored.get("name", "app"))),
            )
            apps.append(stored)
        return self._register_custom_backend(
            name=str(spec.get("name", "Custom Backend")),
            url=str(spec.get("url", "http://127.0.0.1:7779")),
            widgets=widgets,
            apps=apps,
            warnings=list(spec.get("warnings", [])),
            backend_id=spec.get("backend_id"),
        )

    def seed_dashboard(self, spec: JsonDict) -> Dashboard:
        dashboard = self.create_dashboard(
            str(spec.get("name", "Workspace Bench")),
            dashboard_id=spec.get("dashboard_id"),
            activate=bool(spec.get("activate", True)),
        )
        tabs = spec.get("tabs", [])
        if tabs:
            dashboard.tabs.clear()
            for tab in tabs:
                tab_id = str(tab.get("id", slugify(str(tab.get("name", "")))))
                dashboard.ensure_tab(tab_id, str(tab.get("name", tab_id)))
            self.active_tab_id = str(tabs[0].get("id", ""))
        for widget_spec in spec.get("widgets", []):
            self._seed_regular_widget(dashboard, widget_spec)
        for widget_spec in spec.get("generated_widgets", []):
            self._seed_generated_widget(dashboard, widget_spec)
        return dashboard

    def create_dashboard(
        self,
        name: str,
        dashboard_id: str | None = None,
        activate: bool = True,
    ) -> Dashboard:
        self._dash_counter += 1
        resolved_id = dashboard_id or f"dash_{self._dash_counter:03d}"
        dashboard = Dashboard(dashboard_id=resolved_id, name=name)
        self.dashboards[resolved_id] = dashboard
        if activate:
            self.active_dashboard_id = resolved_id
            self.active_tab_id = ""
        return dashboard

    def call_tool(self, call: ToolCall | str, args: JsonDict | None = None) -> JsonDict:
        """Execute a Workspace MCP-like tool call."""

        if isinstance(call, ToolCall):
            name = call.name
            args = call.args
        else:
            name = call
            args = args or {}
        handler = getattr(self, f"_tool_{name}", None)
        if handler is None:
            return self._error(name, "invalid_request", f"Unknown tool {name!r}")
        try:
            return handler(copy.deepcopy(args or {}))
        except Exception as error:  # noqa: BLE001 - simulator returns tool errors.
            return self._error(name, "command_failed", str(error))

    def snapshot(self) -> JsonDict:
        return self._workspace_snapshot()

    def _seed_regular_widget(self, dashboard: Dashboard, spec: JsonDict) -> None:
        origin = str(spec["origin"])
        widget_id = str(spec["widget_id"])
        tab_id = str(spec.get("tab_id", self.active_tab_id))
        dashboard.ensure_tab(tab_id, tab_id)
        backend = self._backend_by_origin(origin)
        schema = backend.get_widget_schema(widget_id)
        grid = schema.get("gridData") or {"w": 20, "h": 10}
        layout_spec = spec.get("layout", {})
        self._add_widget_instance(
            dashboard=dashboard,
            origin=origin,
            widget_id=widget_id,
            name=schema["name"],
            widget_type=schema["type"],
            data_args=spec.get("data_args", {}),
            ui_args=spec.get("ui_args", {}),
            layout=LayoutItem(
                x=float(layout_spec.get("x", 0)),
                y=float(layout_spec.get("y", self._next_y(dashboard, tab_id))),
                w=float(layout_spec.get("w", grid.get("w", 20))),
                h=float(layout_spec.get("h", grid.get("h", 10))),
                tab_id=tab_id,
            ),
        )

    def _seed_generated_widget(self, dashboard: Dashboard, spec: JsonDict) -> None:
        tab_id = str(spec.get("tab_id", self.active_tab_id))
        dashboard.ensure_tab(tab_id, tab_id)
        layout_spec = spec.get("layout", {})
        self._add_widget_instance(
            dashboard=dashboard,
            origin="generated",
            widget_id=f"generated_{spec.get('widget_type', 'note')}",
            name=str(spec.get("name", spec.get("widget_type", "Generated"))),
            widget_type=str(spec.get("widget_type", "note")),
            generated=True,
            generated_data=spec.get("data"),
            chart_params=spec.get("chart_params"),
            description=spec.get("description"),
            layout=LayoutItem(
                x=float(layout_spec.get("x", 0)),
                y=float(layout_spec.get("y", self._next_y(dashboard, tab_id))),
                w=float(layout_spec.get("w", 20)),
                h=float(layout_spec.get("h", 8)),
                tab_id=tab_id,
            ),
        )

    def _tool_get_workspace_snapshot(self, args: JsonDict) -> JsonDict:
        return self._ok("get_workspace_snapshot", self._workspace_snapshot())

    def _tool_manage_backends(self, args: JsonDict) -> JsonDict:
        operation = args.get("operation")
        if operation == "list":
            return self._ok("manage_backends", {"backends": self._backend_list()})
        if operation == "add":
            name = args.get("name")
            if not isinstance(name, str) or not name:
                return self._error(
                    "manage_backends",
                    "invalid_request",
                    "manage_backends operation='add' requires name.",
                )
            if "widgets_json" in args or "apps_json" in args:
                return self._add_custom_backend(args, name)
            backend_id = self.register_backend(name, args.get("backend_id"), args.get("url"))
            backend = self.backends[backend_id]
            self.declared_backends[backend_id] = {
                "name": backend.name,
                "url": backend.default_url,
                "warnings": [],
            }
            return self._ok(
                "manage_backends",
                {"backend_id": backend_id, "backends": self._backend_list()},
            )
        if operation == "refresh":
            refresh_backend_id = args.get("backend_id")
            if refresh_backend_id not in self.backends:
                return self._error("manage_backends", "invalid_request", "Unknown backend_id.")
            if "widgets_json" in args or "apps_json" in args:
                return self._refresh_custom_backend(args, str(refresh_backend_id))
            return self._ok("manage_backends", {"backend_id": refresh_backend_id})
        if operation == "delete":
            delete_backend_id = args.get("backend_id")
            if delete_backend_id not in self.custom_backends:
                return self._error(
                    "manage_backends",
                    "invalid_request",
                    "manage_backends delete requires a custom backend_id.",
                )
            deleted = self.backends.pop(str(delete_backend_id))
            self.custom_backends.pop(str(delete_backend_id), None)
            self.declared_backends.pop(str(delete_backend_id), None)
            remaining = [
                candidate_id
                for candidate_id, backend in self.backends.items()
                if backend.name == deleted.name
            ]
            if remaining:
                self.backend_ids_by_name[deleted.name] = remaining[-1]
            else:
                self.backend_ids_by_name.pop(deleted.name, None)
            return self._ok(
                "manage_backends",
                {"message": "Backend deleted.", "backend_id": delete_backend_id},
            )
        return self._error(
            "manage_backends",
            "invalid_request",
            "manage_backends supports list, add, refresh, and delete in the simulator.",
        )

    @staticmethod
    def _validation_message(prefix: str, errors: list[str]) -> str:
        shown = errors[:3]
        suffix = f" (+{len(errors) - 3} more)" if len(errors) > 3 else ""
        return f"{prefix}: " + " | ".join(shown) + suffix

    def _add_custom_backend(self, args: JsonDict, name: str) -> JsonDict:
        url = args.get("url")
        if not isinstance(url, str) or not url:
            return self._error(
                "manage_backends",
                "invalid_request",
                "manage_backends operation='add' requires name and url.",
            )
        if name in self.backend_ids_by_name:
            return self._error(
                "manage_backends",
                "invalid_request",
                f'A backend with the name "{name}" already exists.',
            )
        widgets_payload = args.get("widgets_json")
        if widgets_payload is None:
            return self._error(
                "manage_backends",
                "invalid_request",
                "manage_backends operation='add' with apps_json also requires "
                "widgets_json (the widgets.json content your backend serves).",
            )
        errors, warnings, widgets = backend_validation.validate_widgets_json(
            widgets_payload
        )
        if errors:
            return self._error(
                "manage_backends",
                "command_failed",
                self._validation_message("Widget validation failed", errors),
            )
        app_errors, app_warnings, apps = backend_validation.validate_apps_json(
            args.get("apps_json"), set(widgets)
        )
        if app_errors:
            return self._error(
                "manage_backends",
                "command_failed",
                self._validation_message("App validation failed", app_errors),
            )
        all_warnings = warnings + app_warnings
        backend_id = self._register_custom_backend(
            name=name,
            url=url.strip().rstrip("/"),
            widgets=widgets,
            apps=apps,
            warnings=all_warnings,
            backend_id=args.get("backend_id"),
        )
        return self._ok(
            "manage_backends",
            {
                "message": "Backend added.",
                "backend_id": backend_id,
                "backend": {
                    "id": backend_id,
                    "name": name,
                    "url": self.backends[backend_id].default_url,
                    "widget_count": len(widgets),
                    "app_count": len(apps),
                },
                "validation_warnings": all_warnings,
            },
        )

    def _refresh_custom_backend(self, args: JsonDict, backend_id: str) -> JsonDict:
        if backend_id not in self.custom_backends:
            return self._error(
                "manage_backends",
                "invalid_request",
                "refresh with widgets_json/apps_json is only supported for custom "
                "backends added with widgets_json.",
            )
        current = self.backends[backend_id]
        widgets_payload = args.get("widgets_json")
        if widgets_payload is not None:
            errors, warnings, widgets = backend_validation.validate_widgets_json(
                widgets_payload
            )
            if errors:
                return self._error(
                    "manage_backends",
                    "command_failed",
                    self._validation_message("Backend refresh failed", errors),
                )
        else:
            warnings, widgets = [], copy.deepcopy(current.widgets)
        apps_payload = args.get("apps_json")
        if apps_payload is not None:
            app_errors, app_warnings, apps = backend_validation.validate_apps_json(
                apps_payload, set(widgets)
            )
        else:
            app_errors, app_warnings, apps = backend_validation.validate_apps_json(
                current.apps_json(), set(widgets)
            )
        if app_errors:
            return self._error(
                "manage_backends",
                "command_failed",
                self._validation_message("Backend refresh failed", app_errors),
            )
        all_warnings = warnings + app_warnings
        name = current.name
        self.backends[backend_id] = FixtureBackend(
            slug=current.slug,
            name=name,
            widgets=copy.deepcopy(widgets),
            apps=copy.deepcopy(apps),
            default_url=current.default_url,
        )
        self.custom_backends[backend_id] = {
            "name": name,
            "url": current.default_url,
            "warnings": all_warnings,
        }
        return self._ok(
            "manage_backends",
            {
                "message": "Backend refreshed.",
                "backend_id": backend_id,
                "backend": {
                    "id": backend_id,
                    "name": name,
                    "url": current.default_url,
                    "widget_count": len(widgets),
                    "app_count": len(apps),
                },
                "validation_warnings": all_warnings,
            },
        )

    def _tool_list_available_widgets(self, args: JsonDict) -> JsonDict:
        origin = args.get("origin")
        backend_id = args.get("backend_id")
        backends = self._select_backends(origin=origin, backend_id=backend_id)
        widgets: list[JsonDict] = []
        for resolved_backend_id, backend in backends:
            for widget in backend.list_available_widgets():
                widget["backend_id"] = resolved_backend_id
                widgets.append(widget)
        return self._ok("list_available_widgets", {"widgets": widgets})

    def _tool_get_widget_schema(self, args: JsonDict) -> JsonDict:
        origin = args.get("origin")
        widget_id = args.get("widget_id")
        if not origin or not widget_id:
            return self._error(
                "get_widget_schema",
                "invalid_request",
                "get_widget_schema requires origin and widget_id.",
            )
        backend = self._backend_by_origin(str(origin))
        schema = backend.get_widget_schema(str(widget_id))
        return self._ok("get_widget_schema", {"schema": schema})

    def _tool_get_params_options(self, args: JsonDict) -> JsonDict:
        origin = args.get("origin")
        widget_id = args.get("widget_id")
        param_name = args.get("param_name")
        if not origin or not widget_id or not param_name:
            return self._error(
                "get_params_options",
                "invalid_request",
                "get_params_options requires origin, widget_id, and param_name.",
            )
        backend = self._backend_by_origin(str(origin))
        options = backend.get_param_options(
            str(widget_id), str(param_name), args.get("data_args", {})
        )
        return self._ok("get_params_options", {"options": options})

    def _tool_get_widget_data(self, args: JsonDict) -> JsonDict:
        origin = args.get("origin")
        widget_id = args.get("widget_id")
        if not origin or not widget_id:
            return self._error(
                "get_widget_data",
                "invalid_request",
                "get_widget_data requires origin and widget_id.",
            )
        data_args = args.get("data_args", {})
        if not isinstance(data_args, dict):
            return self._error(
                "get_widget_data", "invalid_request", "data_args must be an object."
            )
        backend = self._backend_by_origin(str(origin))
        resolved_widget_id = str(widget_id)
        backend_id = self.backend_ids_by_name.get(str(origin))
        if (
            backend_id in self.custom_backends
            and self.runtime_checks is not None
        ):
            definition = backend.widgets.get(resolved_widget_id)
            if definition is None:
                return self._error(
                    "get_widget_data",
                    "invalid_request",
                    f"Unknown widget_id {resolved_widget_id!r}.",
                )
            data, error = task_widget_data(
                definition,
                resolved_widget_id,
                self.runtime_checks,
            )
            if error is not None:
                return self._error(
                    "get_widget_data",
                    "backend_response_invalid",
                    error,
                )
        else:
            data = backend.fetch_widget_data(resolved_widget_id, data_args)
        return self._ok("get_widget_data", {"data": data})

    def _tool_manage_dashboard(self, args: JsonDict) -> JsonDict:
        operation = args.get("operation")
        if operation == "create":
            name = args.get("name")
            if not isinstance(name, str) or not name:
                return self._error(
                    "manage_dashboard",
                    "invalid_request",
                    "manage_dashboard operation='create' requires name.",
                )
            dashboard = self.create_dashboard(
                name=name,
                dashboard_id=args.get("dashboard_id"),
                activate=bool(args.get("activate", True)),
            )
            return self._ok("manage_dashboard", self._dashboard_payload(dashboard))
        if operation == "read":
            dashboard = self._dashboard(args.get("dashboard_id"))
            return self._ok("manage_dashboard", self._dashboard_payload(dashboard))
        if operation == "update":
            dashboard = self._dashboard(args.get("dashboard_id"))
            name = args.get("name")
            if not isinstance(name, str):
                return self._error(
                    "manage_dashboard",
                    "invalid_request",
                    "manage_dashboard operation='update' requires name.",
                )
            dashboard.name = name
            return self._ok("manage_dashboard", self._dashboard_payload(dashboard))
        return self._error(
            "manage_dashboard",
            "invalid_request",
            "manage_dashboard requires operation from {create, read, update}.",
        )

    def _tool_manage_navigation_bar(self, args: JsonDict) -> JsonDict:
        dashboard = self._dashboard(args.get("dashboard_id"))
        operation = args.get("operation")
        tabs_payload = args.get("tabs", [])
        if operation in {"create", "add_tabs", "remove_tabs"}:
            if not isinstance(tabs_payload, list) or not tabs_payload:
                return self._error(
                    "manage_navigation_bar",
                    "invalid_request",
                    f"manage_navigation_bar operation={operation!r} requires tabs.",
                )
            for tab in tabs_payload:
                if not isinstance(tab, dict) or set(tab) != {"name"}:
                    return self._error(
                        "manage_navigation_bar",
                        "invalid_request",
                        "tabs must be objects with only the key name.",
                    )
        if operation == "create":
            dashboard.navigation_bar = True
            dashboard.tabs.clear()
            for tab in tabs_payload:
                dashboard.ensure_tab(slugify(str(tab["name"])), str(tab["name"]))
            self.active_tab_id = next(iter(dashboard.tabs), "")
            return self._ok("manage_navigation_bar", self._dashboard_payload(dashboard))
        if operation == "add_tabs":
            dashboard.navigation_bar = True
            for tab in tabs_payload:
                dashboard.ensure_tab(slugify(str(tab["name"])), str(tab["name"]))
            return self._ok("manage_navigation_bar", self._dashboard_payload(dashboard))
        if operation == "remove_tabs":
            for tab in tabs_payload:
                dashboard.tabs.pop(slugify(str(tab["name"])), None)
            if self.active_tab_id not in dashboard.tabs:
                self.active_tab_id = next(iter(dashboard.tabs), "")
            return self._ok("manage_navigation_bar", self._dashboard_payload(dashboard))
        if operation == "rename_tabs":
            rename_map = args.get("rename_map", {})
            if not isinstance(rename_map, dict) or not rename_map:
                return self._error(
                    "manage_navigation_bar",
                    "invalid_request",
                    "rename_tabs requires rename_map.",
                )
            for old_tab_id, new_name in rename_map.items():
                if old_tab_id in dashboard.tabs:
                    tab = dashboard.tabs.pop(old_tab_id)
                    tab.name = str(new_name)
                    tab.tab_id = slugify(str(new_name))
                    dashboard.tabs[tab.tab_id] = tab
            return self._ok("manage_navigation_bar", self._dashboard_payload(dashboard))
        return self._error(
            "manage_navigation_bar",
            "invalid_request",
            "manage_navigation_bar requires operation from {create, add_tabs, remove_tabs, rename_tabs}.",
        )

    def _tool_navigate_workspace(self, args: JsonDict) -> JsonDict:
        operation = args.get("operation")
        if operation == "dashboard":
            dashboard_id = args.get("dashboard_id")
            if dashboard_id not in self.dashboards:
                return self._error("navigate_workspace", "invalid_request", "Unknown dashboard_id.")
            self.active_dashboard_id = str(dashboard_id)
            tab_id = args.get("tab_id")
            if tab_id is not None:
                return self._tool_navigate_workspace(
                    {"operation": "tab", "dashboard_id": dashboard_id, "tab_id": tab_id}
                )
            return self._ok("navigate_workspace", self._workspace_snapshot())
        if operation == "tab":
            dashboard = self._dashboard(args.get("dashboard_id"))
            tab_id = args.get("tab_id")
            if tab_id not in dashboard.tabs:
                return self._error("navigate_workspace", "invalid_request", "Unknown tab_id.")
            self.active_dashboard_id = dashboard.dashboard_id
            self.active_tab_id = str(tab_id)
            return self._ok("navigate_workspace", self._workspace_snapshot())
        return self._error(
            "navigate_workspace",
            "invalid_request",
            "navigate_workspace requires operation from {dashboard, tab}.",
        )

    def _tool_create_widget(self, args: JsonDict) -> JsonDict:
        origin = args.get("origin") or args.get("backend_name")
        widget_id = args.get("widget_id")
        if not origin or not widget_id:
            return self._error(
                "create_widget",
                "invalid_request",
                "create_widget requires origin and widget_id.",
            )
        dashboard = self._dashboard(args.get("dashboard_id"))
        backend = self._backend_by_origin(str(origin))
        schema = backend.get_widget_schema(str(widget_id))
        config = args.get("config") or {}
        data_args = args.get("data_args")
        ui_args = args.get("ui_args")
        if data_args is None and isinstance(config, dict):
            data_args = config.get("data_args", {})
        if ui_args is None and isinstance(config, dict):
            ui_args = config.get("ui_args", {})
        if not isinstance(data_args or {}, dict) or not isinstance(ui_args or {}, dict):
            return self._error(
                "create_widget",
                "invalid_request",
                "data_args and ui_args must be objects.",
            )
        tab_id = self.active_tab_id if self.active_tab_id in dashboard.tabs else ""
        grid = schema.get("gridData") or {"w": 20, "h": 10}
        instance = self._add_widget_instance(
            dashboard=dashboard,
            origin=str(origin),
            widget_id=str(widget_id),
            name=schema["name"],
            widget_type=schema["type"],
            data_args=data_args or {},
            ui_args=ui_args or {},
            layout=LayoutItem(
                x=0,
                y=self._next_y(dashboard, tab_id),
                w=float(grid.get("w", 20)),
                h=float(grid.get("h", 10)),
                tab_id=tab_id,
            ),
        )
        return self._ok("create_widget", {"widget": instance.to_dict()})

    def _tool_update_widget(self, args: JsonDict) -> JsonDict:
        config = args.get("config") or {}
        data_args = args.get("data_args")
        if data_args is None and isinstance(config, dict):
            data_args = config.get("data_args")
        ui_args = args.get("ui_args")
        if ui_args is None and isinstance(config, dict):
            ui_args = config.get("ui_args")
        for key in ("x", "y", "w", "h", "gridData", "tab_id"):
            if key in args or key in (ui_args or {}):
                return self._error(
                    "update_widget",
                    "invalid_request",
                    "Use update_widget_layout for layout fields.",
                )
        widget = self._find_widget(args)
        if isinstance(data_args, dict):
            widget.data_args.update(data_args)
        if isinstance(ui_args, dict):
            widget.ui_args.update(ui_args)
        return self._ok("update_widget", {"widget": widget.to_dict()})

    def _tool_read_widget(self, args: JsonDict) -> JsonDict:
        widget = self._find_widget(args)
        payload = widget.to_dict()
        backend_id = self.backend_ids_by_name.get(widget.origin)
        if backend_id in self.custom_backends and self.runtime_checks is not None:
            response = self._tool_get_widget_data(
                {
                    "origin": widget.origin,
                    "widget_id": widget.widget_id,
                    "data_args": widget.data_args,
                }
            )
            if response.get("ok"):
                payload["data_preview"] = (response.get("data") or {}).get("data")
            else:
                payload["data_error"] = (response.get("error") or {}).get("message")
        return self._ok("read_widget", {"widget": payload})

    def _tool_delete_widget(self, args: JsonDict) -> JsonDict:
        dashboard = self._dashboard(args.get("dashboard_id"))
        widget = self._find_widget(args)
        dashboard.widgets.pop(widget.widget_uuid, None)
        return self._ok("delete_widget", {"deleted_widget_uuid": widget.widget_uuid})

    def _tool_update_widget_layout(self, args: JsonDict) -> JsonDict:
        widget = self._find_widget(args)
        for key in ("x", "y", "w", "h"):
            if key not in args:
                return self._error(
                    "update_widget_layout",
                    "invalid_request",
                    "update_widget_layout requires x, y, w, and h.",
                )
        dashboard = self._dashboard(args.get("dashboard_id"))
        tab_id = str(args.get("tab_id", widget.layout.tab_id))
        dashboard.ensure_tab(tab_id, tab_id)
        widget.layout = LayoutItem(
            x=float(args["x"]),
            y=float(args["y"]),
            w=float(args["w"]),
            h=float(args["h"]),
            tab_id=tab_id,
            min_w=args.get("min_w"),
            min_h=args.get("min_h"),
            max_w=args.get("max_w"),
            max_h=args.get("max_h"),
        )
        return self._ok("update_widget_layout", {"widget": widget.to_dict()})

    def _tool_add_generative_widget(self, args: JsonDict) -> JsonDict:
        widget_type = args.get("widget_type")
        if widget_type not in {"note", "table", "chart", "html"}:
            return self._error(
                "add_generative_widget",
                "invalid_request",
                "widget_type must be one of note, table, chart, html.",
            )
        if widget_type in {"note", "html"} and not isinstance(args.get("data"), str):
            return self._error(
                "add_generative_widget",
                "invalid_request",
                "note and html widgets require string data.",
            )
        if widget_type in {"table", "chart"} and not isinstance(args.get("data"), list):
            return self._error(
                "add_generative_widget",
                "invalid_request",
                "table and chart widgets require array data.",
            )
        if widget_type == "chart":
            chart_params = args.get("chart_params")
            if not isinstance(chart_params, dict) or not {
                "chartType",
                "xKey",
                "yKey",
            }.issubset(chart_params):
                return self._error(
                    "add_generative_widget",
                    "invalid_request",
                    "chart_params must include chartType, xKey, and yKey.",
                )
        dashboard = self._dashboard(args.get("dashboard_id"))
        tab_id = str(args.get("inner_tab") or self.active_tab_id or "")
        dashboard.ensure_tab(tab_id, tab_id)
        instance = self._add_widget_instance(
            dashboard=dashboard,
            origin="generated",
            widget_id=f"generated_{widget_type}",
            name=str(args.get("name") or widget_type.title()),
            widget_type=str(widget_type),
            generated=True,
            generated_data=args.get("data"),
            chart_params=args.get("chart_params"),
            description=args.get("description"),
            layout=LayoutItem(
                x=0,
                y=self._next_y(dashboard, tab_id),
                w=20 if widget_type != "chart" else 24,
                h=8 if widget_type != "chart" else 12,
                tab_id=tab_id,
            ),
        )
        return self._ok("add_generative_widget", {"widget": instance.to_dict()})

    def _tool_manage_apps(self, args: JsonDict) -> JsonDict:
        operation = args.get("operation")
        if "apps_json" in args or "widgets_json" in args:
            return self._error(
                "manage_apps",
                "invalid_request",
                "manage_apps does not publish apps or widgets. Your backend serves "
                "them: use manage_backends operation='add' (new custom backend) or "
                "operation='refresh' (existing backend_id) with widgets_json and/or "
                "apps_json, then manage_apps can list/read/instantiate them.",
            )
        backend = self._backend_by_id(str(args.get("backend_id", "")))
        if operation == "list":
            apps = [
                {
                    "name": app["name"],
                    "template_id": app.get("template_id"),
                    "description": app.get("description"),
                    "tab_count": len(app.get("tabs", {})),
                    "prompt_count": len(app.get("prompts", [])),
                    "allow_customization": app.get("allowCustomization"),
                }
                for app in backend.apps_json()
            ]
            return self._ok("manage_apps", {"apps": apps})
        app = self._find_app(backend, args.get("app_name"), args.get("template_id"))
        if operation == "read":
            return self._ok("manage_apps", {"app": app})
        if operation == "instantiate":
            unavailable = sorted({
                str(layout.get("i"))
                for tab_payload in app.get("tabs", {}).values()
                for layout in tab_payload.get("layout", [])
                if str(layout.get("i")) not in backend.widgets
                and str(layout.get("i")) != "navigation_bar"
            })
            if unavailable:
                return self._error(
                    "manage_apps",
                    "command_failed",
                    "Unable to create app because these widgets are unavailable: "
                    + ", ".join(unavailable),
                )
            dashboard = self.create_dashboard(
                name=str(args.get("dashboard_name") or app["name"]),
                activate=bool(args.get("activate", True)),
            )
            dashboard.tabs.clear()
            for tab_id, tab_payload in app.get("tabs", {}).items():
                dashboard.ensure_tab(tab_id, tab_payload.get("name", tab_id))
            self.active_tab_id = next(iter(dashboard.tabs), "")
            origin = backend.name
            for tab_id, tab_payload in app.get("tabs", {}).items():
                for layout in tab_payload.get("layout", []):
                    widget_id = str(layout["i"])
                    schema = backend.get_widget_schema(widget_id)
                    state = layout.get("state", {})
                    self._add_widget_instance(
                        dashboard=dashboard,
                        origin=origin,
                        widget_id=widget_id,
                        name=schema["name"],
                        widget_type=schema["type"],
                        data_args=state.get("params", {}),
                        layout=LayoutItem(
                            x=float(layout.get("x", 0)),
                            y=float(layout.get("y", 0)),
                            w=float(layout.get("w", schema.get("gridData", {}).get("w", 20))),
                            h=float(layout.get("h", schema.get("gridData", {}).get("h", 10))),
                            tab_id=tab_id,
                        ),
                    )
            return self._ok("manage_apps", self._dashboard_payload(dashboard))
        return self._error(
            "manage_apps",
            "invalid_request",
            "manage_apps requires operation from {list, read, instantiate}.",
        )

    def _tool_get_skill_content(self, args: JsonDict) -> JsonDict:
        slug = str(args.get("slug", ""))
        skill = WORKSPACE_SKILLS.get(slug)
        if skill is None:
            return self._error(
                "get_skill_content",
                "invalid_request",
                f"Unknown skill slug {slug!r}.",
            )
        return self._ok(
            "get_skill_content",
            {
                "slug": slug,
                "name": skill["name"],
                "description": skill["description"],
                "content": skill["content"],
            },
        )

    def _tool_read_workspace_resource(self, args: JsonDict) -> JsonDict:
        uri = str(args.get("uri", ""))
        if uri == APP_BUILDER_INDEX_URI:
            return self._ok(
                "read_workspace_resource",
                {
                    "uri": uri,
                    "mime_type": "application/json",
                    "text": self._app_builder_index_text(),
                    "apps": self._app_builder_index(),
                },
            )
        skill_prefix = "openbb://workspace/skills/"
        if uri.startswith(skill_prefix):
            slug = uri.removeprefix(skill_prefix)
            skill = WORKSPACE_SKILLS.get(slug)
            if skill is not None:
                return self._ok(
                    "read_workspace_resource",
                    {
                        "uri": uri,
                        "mime_type": "application/json",
                        "slug": slug,
                        "name": skill["name"],
                        "description": skill["description"],
                        "content": skill["content"],
                        "text": (
                            f"{skill['name']}: {skill['description']} "
                            f"{skill['content']}"
                        ),
                    },
                )
        valid = ", ".join(self._valid_resource_uris())
        return self._error(
            "read_workspace_resource",
            "invalid_request",
            f"Unknown workspace resource URI {uri!r}. Valid URIs: {valid}.",
        )

    def _tool_get_workspace_prompt(self, args: JsonDict) -> JsonDict:
        name = str(args.get("name", ""))
        text = WORKSPACE_PROMPTS.get(name)
        if text is None:
            valid = ", ".join(sorted(WORKSPACE_PROMPTS))
            return self._error(
                "get_workspace_prompt",
                "invalid_request",
                f"Unknown workspace prompt {name!r}. Valid prompts: {valid}.",
            )
        return self._ok(
            "get_workspace_prompt",
            {
                "name": name,
                "description": f"Deterministic fixture prompt for {name}.",
                "messages": [{"role": "user", "content": text}],
                "text": text,
            },
        )

    def _tool_assign_tasks_to_agents(self, args: JsonDict) -> JsonDict:
        return self._ok(
            "assign_tasks_to_agents",
            {"task_requests": copy.deepcopy(args.get("task_requests", []))},
        )

    def _add_widget_instance(
        self,
        *,
        dashboard: Dashboard,
        origin: str,
        widget_id: str,
        name: str,
        widget_type: str,
        data_args: JsonDict | None = None,
        ui_args: JsonDict | None = None,
        generated: bool = False,
        generated_data: Any = None,
        chart_params: JsonDict | None = None,
        description: str | None = None,
        layout: LayoutItem | None = None,
    ) -> WidgetInstance:
        self._widget_counter += 1
        widget_uuid = f"widget_{self._widget_counter:03d}"
        instance = WidgetInstance(
            widget_uuid=widget_uuid,
            widget_id=widget_id,
            origin=origin,
            name=name,
            widget_type=widget_type,
            data_args=copy.deepcopy(data_args or {}),
            ui_args=copy.deepcopy(ui_args or {}),
            generated=generated,
            generated_data=copy.deepcopy(generated_data),
            chart_params=copy.deepcopy(chart_params),
            description=description,
            layout=layout or LayoutItem(0, self._next_y(dashboard, ""), 20, 10),
        )
        dashboard.ensure_tab(instance.layout.tab_id, instance.layout.tab_id)
        dashboard.widgets[widget_uuid] = instance
        return instance

    def _workspace_snapshot(self) -> JsonDict:
        self._snapshot_counter += 1
        active = self._dashboard(self.active_dashboard_id)
        return {
            "generated_at": self._snapshot_counter,
            "workspace_state": {
                "current_dashboard_uuid": active.dashboard_id,
                "current_tab_id": self.active_tab_id,
            },
            "dashboards": [
                {"dashboard_id": dash.dashboard_id, "name": dash.name}
                for dash in self.dashboards.values()
            ],
            # Full compositions make collateral workspace mutations observable
            # to deterministic graders; dashboard_composition remains the
            # backwards-compatible active-dashboard view.
            "dashboard_compositions": {
                dashboard_id: self._dashboard_composition(dashboard)
                for dashboard_id, dashboard in self.dashboards.items()
            },
            "dashboard_composition": self._dashboard_composition(active),
            "backends": self._backend_list(),
            "custom_backends": {
                backend_id: {
                    "name": meta["name"],
                    "url": meta["url"],
                    "widgets_json": self.backends[backend_id].widgets_json(),
                    "apps_json": self.backends[backend_id].apps_json(),
                    "warnings": list(meta.get("warnings", [])),
                }
                for backend_id, meta in {
                    **self.declared_backends,
                    **self.custom_backends,
                }.items()
                if backend_id in self.backends
            },
            "skills": [
                {
                    "slug": skill["slug"],
                    "name": skill["name"],
                    "description": skill["description"],
                }
                for skill in WORKSPACE_SKILLS.values()
            ],
        }

    def _dashboard_payload(self, dashboard: Dashboard) -> JsonDict:
        return {
            "dashboard_id": dashboard.dashboard_id,
            "name": dashboard.name,
            "dashboard_composition": self._dashboard_composition(dashboard),
            "session_context": {
                "current_dashboard_uuid": self.active_dashboard_id,
                "current_tab_id": self.active_tab_id,
            },
        }

    def _dashboard_composition(self, dashboard: Dashboard) -> JsonDict:
        tabs = []
        for tab_id, tab in dashboard.tabs.items():
            layout = [
                widget.layout.to_dict(
                    widget.widget_uuid, widget.widget_id, widget.origin
                )
                for widget in dashboard.widgets.values()
                if widget.layout.tab_id == tab_id
            ]
            tabs.append({"id": tab_id, "name": tab.name, "layout": layout})
        return {
            "dashboard_id": dashboard.dashboard_id,
            "name": dashboard.name,
            "navigation_bar": dashboard.navigation_bar,
            "tabs": tabs,
            "widgets": [widget.to_dict() for widget in dashboard.widgets.values()],
        }

    def _backend_list(self) -> list[JsonDict]:
        return [
            {
                "id": backend_id,
                "name": backend.name,
                "url": backend.default_url,
                "status": "connected",
                "widget_count": len(backend.widgets),
                "app_count": len(backend.apps),
            }
            for backend_id, backend in self.backends.items()
        ]

    def _app_builder_index(self) -> list[JsonDict]:
        apps: list[JsonDict] = []
        for backend_id, backend in self.backends.items():
            for app in backend.apps_json():
                tabs = app.get("tabs", {})
                tab_ids = sorted(tabs) if isinstance(tabs, dict) else []
                apps.append(
                    {
                        "backend_id": backend_id,
                        "backend_name": backend.name,
                        "backend_slug": backend.slug,
                        "name": app.get("name"),
                        "template_id": app.get("template_id"),
                        "description": app.get("description"),
                        "tab_ids": tab_ids,
                    }
                )
        return apps

    def _app_builder_index_text(self) -> str:
        lines = ["Workspace app builder index"]
        for app in self._app_builder_index():
            lines.append(
                " | ".join(
                    [
                        str(app["backend_name"]),
                        str(app["name"]),
                        str(app["template_id"]),
                        str(app.get("description") or ""),
                        f"tabs={','.join(app['tab_ids'])}",
                    ]
                )
            )
        return "\n".join(lines)

    def _valid_resource_uris(self) -> list[str]:
        return [
            APP_BUILDER_INDEX_URI,
            *[
                f"openbb://workspace/skills/{slug}"
                for slug in sorted(WORKSPACE_SKILLS)
            ],
        ]

    def _select_backends(
        self, *, origin: str | None = None, backend_id: str | None = None
    ) -> list[tuple[str, FixtureBackend]]:
        selected = list(self.backends.items())
        if backend_id:
            selected = [(backend_id, self._backend_by_id(backend_id))]
        if origin:
            selected = [(bid, backend) for bid, backend in selected if backend.name == origin]
        return selected

    def _backend_by_origin(self, origin: str) -> FixtureBackend:
        backend_id = self.backend_ids_by_name.get(origin)
        if backend_id is None:
            raise KeyError(f"Unknown backend origin {origin!r}")
        return self.backends[backend_id]

    def _backend_by_id(self, backend_id: str) -> FixtureBackend:
        try:
            return self.backends[backend_id]
        except KeyError as error:
            raise KeyError(f"Unknown backend_id {backend_id!r}") from error

    def _dashboard(self, dashboard_id: str | None) -> Dashboard:
        resolved_id = dashboard_id or self.active_dashboard_id
        if resolved_id is None:
            raise KeyError("No active dashboard")
        try:
            return self.dashboards[str(resolved_id)]
        except KeyError as error:
            raise KeyError(f"Unknown dashboard_id {resolved_id!r}") from error

    def _find_widget(self, args: JsonDict) -> WidgetInstance:
        dashboard = self._dashboard(args.get("dashboard_id"))
        widget_uuid = args.get("widget_uuid")
        if widget_uuid:
            try:
                return dashboard.widgets[str(widget_uuid)]
            except KeyError as error:
                raise KeyError(f"Unknown widget_uuid {widget_uuid!r}") from error
        widget_id = args.get("widget_id")
        matches = [
            widget
            for widget in dashboard.widgets.values()
            if widget.widget_id == widget_id
        ]
        if len(matches) != 1:
            raise KeyError(
                f"widget_id {widget_id!r} matched {len(matches)} widgets; use widget_uuid"
            )
        return matches[0]

    def _find_app(
        self,
        backend: FixtureBackend,
        app_name: str | None,
        template_id: str | None,
    ) -> JsonDict:
        for app in backend.apps_json():
            if app_name and app.get("name") == app_name:
                return app
            if template_id and app.get("template_id") == template_id:
                return app
        served = ", ".join(
            f"{app.get('name')} (template_id {app.get('template_id')})"
            for app in backend.apps_json()
        ) or "none"
        raise KeyError(
            f"App {app_name or template_id!r} not found. Apps served by this "
            f"backend: {served}. Pass the app's name as app_name (or its "
            "template_id), and the new dashboard's name as dashboard_name."
        )

    def _next_y(self, dashboard: Dashboard, tab_id: str) -> float:
        max_bottom = 2.0 if dashboard.navigation_bar else 0.0
        for widget in dashboard.widgets.values():
            if widget.layout.tab_id == tab_id:
                max_bottom = max(max_bottom, widget.layout.y + widget.layout.h)
        return max_bottom

    def _ok(self, command: str, data: Any | None = None) -> JsonDict:
        return {
            "ok": True,
            "command": command,
            "request_id": None,
            "message": "ok",
            "data": data,
            "error": None,
        }

    def _error(self, command: str, code: str, message: str) -> JsonDict:
        return {
            "ok": False,
            "command": command,
            "request_id": None,
            "message": message,
            "data": None,
            "error": {"code": code, "message": message, "retryable": False},
        }
