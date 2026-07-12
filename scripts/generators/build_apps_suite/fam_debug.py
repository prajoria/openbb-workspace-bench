"""Long, diagnosis-first repair tasks for seeded custom backends."""

from __future__ import annotations

import copy

from build_apps_suite import common as c
from workspace_bench.workspace.tool_surface import WORKSPACE_TOOL_NAMES


DESKS = (
    {
        "slug": "execution",
        "role": "execution analysts",
        "subject": "orders and exceptions",
        "backend": "Execution Repair Data",
        "app": "Execution Recovery Room",
        "entity": "order",
    },
    {
        "slug": "surveillance",
        "role": "surveillance analysts",
        "subject": "cases and alert review",
        "backend": "Surveillance Repair Data",
        "app": "Surveillance Recovery Room",
        "entity": "case",
    },
    {
        "slug": "vendor",
        "role": "vendor operations analysts",
        "subject": "vendor intake and service review",
        "backend": "Vendor Repair Data",
        "app": "Vendor Recovery Room",
        "entity": "record",
    },
)

ARCHETYPES = (
    ("invalid_widget", "medium"),
    ("data_mismatch", "medium"),
    ("dangling_app", "medium"),
    ("duplicate_backend", "medium"),
    ("broken_group", "hard"),
    ("wrong_form_endpoint", "hard"),
    ("wrong_live_row_id", "hard"),
    ("silent_second_tab", "hard"),
)


def _columns(*fields: str) -> dict:
    return {
        "table": {
            "columnsDefs": [
                {
                    "field": field,
                    "headerName": field.replace("_", " ").title(),
                    "cellDataType": (
                        "number" if field in {"value", "price", "age_days"} else "text"
                    ),
                }
                for field in fields
            ]
        }
    }


def _base_widgets(desk: dict, archetype: str) -> dict[str, dict]:
    entity_id = f"{desk['entity']}_id"
    shared = {
        "paramName": "scope",
        "type": "text",
        "label": "Review scope",
        "value": "Open",
    }
    if archetype == "wrong_form_endpoint":
        primary = {
            "name": "Intake Review",
            "description": f"Submit and review one {desk['entity']} intake request.",
            "endpoint": "/intake-review",
            "type": "table",
            "gridData": {"w": 20, "h": 10},
            "params": [
                {
                    "paramName": "intake",
                    "type": "form",
                    "label": "Intake request",
                    "endpoint": "/intake-submit",
                    "method": "POST",
                    "inputParams": [
                        {"paramName": entity_id, "type": "text", "label": "Identifier"},
                        {"paramName": "owner", "type": "text", "label": "Owner"},
                        {"paramName": "submit", "type": "button", "label": "Submit"},
                    ],
                },
                shared,
            ],
            "data": _columns(entity_id, "status", "owner"),
        }
    elif archetype == "wrong_live_row_id":
        primary = {
            "name": "Live Review Queue",
            "description": f"Live updates for active {desk['entity']} reviews.",
            "endpoint": "/live-review",
            "type": "live_grid",
            "wsEndpoint": "live-review-ws",
            "gridData": {"w": 24, "h": 11},
            "params": [shared],
            "data": {
                "wsRowIdColumn": entity_id,
                **_columns(entity_id, "status", "price"),
            },
        }
    else:
        primary = {
            "name": "Review Queue",
            "description": f"Active {desk['entity']} review ownership and status.",
            "endpoint": "/review-queue",
            "type": "table",
            "gridData": {"w": 20, "h": 9},
            "params": [shared],
            "data": _columns(entity_id, "status", "owner"),
        }
    return {
        "review_queue": primary,
        "review_detail": {
            "name": "Review Detail",
            "description": f"Detail and aging for each {desk['entity']} review.",
            "endpoint": "/review-detail",
            "type": "table",
            "gridData": {"w": 20, "h": 9},
            "params": [shared],
            "data": _columns(entity_id, "updated_at", "age_days"),
        },
        "health_metric": {
            "name": "Service Health",
            "description": "A stable health indicator used by the operations handbook.",
            "endpoint": "/service-health",
            "type": "metric",
            "gridData": {"w": 8, "h": 4},
        },
    }


def _apps(desk: dict) -> list[dict]:
    return [
        {
            "name": desk["app"],
            "template_id": "incident-recovery",
            "description": f"Recovery workflow for {desk['subject']}.",
            "tabs": {
                "overview": {
                    "id": "overview",
                    "name": "Overview",
                    "layout": [
                        {"i": "review_queue", "x": 0, "y": 0, "w": 20, "h": 10}
                    ],
                },
                "detail": {
                    "id": "detail",
                    "name": "Detail",
                    "layout": [
                        {"i": "review_detail", "x": 0, "y": 0, "w": 20, "h": 9}
                    ],
                },
            },
            "groups": [
                {
                    "name": "Review Scope",
                    "type": "param",
                    "paramName": "scope",
                    "widgetIds": ["review_queue", "review_detail"],
                }
            ],
        },
        {
            "name": "Operations Handbook",
            "template_id": "operations-handbook",
            "description": "Stable operational context that must not change during repair.",
            "tabs": {
                "health": {
                    "id": "health",
                    "name": "Health",
                    "layout": [
                        {"i": "health_metric", "x": 0, "y": 0, "w": 8, "h": 4}
                    ],
                }
            },
            "groups": [],
        },
    ]


def _archive_backend(desk: dict) -> dict:
    widget = {
        "archive_status": {
            "name": "Archive Status",
            "description": "Stable archive status that is unrelated to the incident.",
            "endpoint": "/archive-status",
            "type": "table",
            "gridData": {"w": 12, "h": 6},
            "data": _columns("archive_id", "retention_state"),
        }
    }
    app = {
        "name": "Archive Console",
        "template_id": "archive-console",
        "description": "Unrelated archive controls.",
        "tabs": {
            "archive": {
                "id": "archive",
                "name": "Archive",
                "layout": [
                    {"i": "archive_status", "x": 0, "y": 0, "w": 12, "h": 6}
                ],
            }
        },
        "groups": [],
    }
    return {
        "backend_id": "debug_archive",
        "name": f"{desk['backend']} Archive",
        "url": "http://localhost:7899",
        "widgets_json": widget,
        "apps_json": [app],
    }


def _broken_payload(
    desk: dict,
    archetype: str,
    widgets: dict[str, dict],
    apps: list[dict],
) -> tuple[dict[str, dict], list[dict], list[str]]:
    broken_widgets = copy.deepcopy(widgets)
    broken_apps = copy.deepcopy(apps)
    warnings: list[str] = []
    if archetype == "invalid_widget":
        broken_widgets["review_queue"].pop("description")
        warnings.append("widgets.review_queue: 'description' is required")
    elif archetype == "data_mismatch":
        broken_widgets["review_queue"]["data"]["table"]["columnsDefs"].append(
            {"field": "retired_owner_code", "headerName": "Retired Owner Code"}
        )
    elif archetype == "dangling_app":
        broken_apps[0]["tabs"]["detail"]["layout"][0]["i"] = "removed_detail"
        warnings.append("Missing widgets used in tab `removed_detail`: removed_detail")
    elif archetype == "broken_group":
        broken_apps[0]["groups"][0]["widgetIds"] = ["review_queue"]
    elif archetype == "wrong_form_endpoint":
        broken_widgets["review_queue"]["params"][0]["endpoint"] = "/retired-intake"
    elif archetype == "wrong_live_row_id":
        broken_widgets["review_queue"]["data"]["wsRowIdColumn"] = "retired_id"
    elif archetype == "silent_second_tab":
        broken_widgets["review_detail"]["endpoint"] = "/retired-detail"
    return broken_widgets, broken_apps, warnings


def _runtime_datasets(
    desk: dict,
    widgets: dict[str, dict],
    archive: dict,
) -> list[dict]:
    datasets = [
        c.runtime_dataset(desk["backend"], widget_id, definition)
        for widget_id, definition in sorted(widgets.items())
    ]
    datasets.extend(
        c.runtime_dataset(archive["name"], widget_id, definition)
        for widget_id, definition in sorted(archive["widgets_json"].items())
    )
    return datasets


def _prompt_variants(desk: dict, archetype: str) -> list[str]:
    incident = {
        "invalid_widget": "one panel disappeared after a backend definition update",
        "data_mismatch": "the overview loads but a declared analyst field is absent",
        "dangling_app": "the detail tab opens to an empty space after a retired panel was removed",
        "duplicate_backend": "two identically named backend connections now compete for the app",
        "broken_group": "changing review scope no longer keeps the overview and detail aligned",
        "wrong_form_endpoint": "the intake form accepts input but submission does nothing",
        "wrong_live_row_id": "live updates overwrite the wrong rows and make the queue unstable",
        "silent_second_tab": "the primary view works while a secondary view silently fails to load",
    }[archetype]
    invariant = (
        "Keep the Operations Handbook, the archive workspace, and every unrelated app "
        "byte-for-byte unchanged. "
        f"Leave {desk['app']} open and add a short verification note that naturally mentions "
        f"{desk['app']}, {desk['backend']}, and repair verified."
    )
    return [
        (
            f"{desk['role'].capitalize()} report that {incident} in {desk['app']}. "
            f"Diagnose the existing {desk['backend']} connection, repair it in place, and "
            f"retest the affected workflow with live data before handing it back. {invariant}"
        ),
        (
            f"An incident in {desk['app']} means {incident}. Investigate the connected "
            f"{desk['backend']} backend, make the smallest in-place repair, and prove the "
            f"workflow against live data. {invariant}"
        ),
        (
            f"Restore {desk['app']} for {desk['role']}: {incident}. Work through the existing "
            f"{desk['backend']} connection, repair the root cause without replacing healthy "
            f"content, and run a live-data retest. {invariant}"
        ),
    ]


def _task(desk: dict, archetype: str, difficulty: str) -> dict:
    task_id = f"{desk['slug']}_{archetype}"
    structural_difficulty = difficulty
    task_ref = f"build-openbb-apps/debug/{task_id}"
    difficulty = c.MEASURED_DIFFICULTY_OVERRIDES.get(task_ref, difficulty)
    widgets = _base_widgets(desk, archetype)
    apps = _apps(desk)
    archive = _archive_backend(desk)
    broken_widgets, broken_apps, warnings = _broken_payload(
        desk, archetype, widgets, apps
    )
    target_backend = {
        "backend_id": "debug_target",
        "name": desk["backend"],
        "url": "http://localhost:7898",
        "widgets_json": broken_widgets,
        "apps_json": broken_apps,
        "warnings": warnings,
    }
    custom_backends = [target_backend]
    if archetype == "duplicate_backend":
        custom_backends.append(
            {
                **copy.deepcopy(target_backend),
                "backend_id": "debug_duplicate",
            }
        )
    custom_backends.append(archive)
    datasets = _runtime_datasets(desk, widgets, archive)
    by_widget = {dataset["widget_id"]: dataset["name"] for dataset in datasets}
    if archetype == "wrong_live_row_id":
        primary_kind = "server-side-grid"
    elif archetype == "wrong_form_endpoint":
        primary_kind = "form"
    else:
        primary_kind = "table-like"
    primary_fields = list(c.declared_fields(widgets["review_queue"]))
    detail_fields = list(c.declared_fields(widgets["review_detail"]))
    if archetype == "wrong_live_row_id":
        required_config = {"data.wsRowIdColumn": f"{desk['entity']}_id"}
    elif archetype == "invalid_widget":
        # The broken payload drops the required description; repairing it is
        # only outcome-visible through the restored configuration value.
        required_config = {"description": widgets["review_queue"]["description"]}
    else:
        required_config = {}
    capabilities = [
        {
            "name": f"incident-overview-{archetype}",
            "datasets": [by_widget["review_queue"]],
            "widget_kind": primary_kind,
            "must_cover_fields": sorted(primary_fields),
            "required_param_kinds": (
                ["form"] if archetype == "wrong_form_endpoint" else ["text"]
            ),
            "required_config": required_config,
        },
        {
            "name": f"incident-detail-{archetype}",
            "datasets": [by_widget["review_detail"]],
            "widget_kind": "table-like",
            "must_cover_fields": sorted(detail_fields),
            "required_param_kinds": ["text"],
        },
    ]
    connections = (
        [
            {
                "source": f"incident-overview-{archetype}",
                "target": f"incident-detail-{archetype}",
                "param_kind": "text",
            }
        ]
        if archetype == "broken_group"
        else []
    )
    repair_args = (
        {"operation": "delete", "backend_id": "debug_duplicate"}
        if archetype == "duplicate_backend"
        else {
            "operation": "refresh",
            "backend_id": "debug_target",
            "widgets_json": widgets,
            "apps_json": apps,
        }
    )
    oracle = [
        {"tool": "get_workspace_snapshot", "args": {}},
        {"tool": "manage_backends", "args": {"operation": "list"}},
        {
            "tool": "read_workspace_resource",
            "args": {"uri": "openbb://workspace/app-builder/index"},
        },
        {"tool": "list_available_widgets", "args": {"origin": desk["backend"]}},
        {
            "tool": "get_widget_schema",
            "args": {"origin": desk["backend"], "widget_id": "review_queue"},
        },
        {
            "tool": "get_widget_data",
            "args": {"origin": desk["backend"], "widget_id": "review_queue"},
        },
    ]
    if archetype == "silent_second_tab":
        oracle.append(
            {
                "tool": "get_widget_data",
                "args": {"origin": desk["backend"], "widget_id": "review_detail"},
            }
        )
    oracle.extend(
        [
            {"tool": "manage_backends", "args": repair_args},
            {"tool": "manage_backends", "args": {"operation": "list"}},
            {"tool": "list_available_widgets", "args": {"origin": desk["backend"]}},
            {
                "tool": "get_widget_schema",
                "args": {"origin": desk["backend"], "widget_id": "review_queue"},
            },
            {
                "tool": "get_widget_data",
                "args": {"origin": desk["backend"], "widget_id": "review_queue"},
            },
            {
                "tool": "get_widget_data",
                "args": {"origin": desk["backend"], "widget_id": "review_detail"},
            },
            {
                "tool": "manage_apps",
                "args": {
                    "operation": "instantiate",
                    "backend_id": "debug_target",
                    "template_id": "incident-recovery",
                },
            },
            {"tool": "read_widget", "args": {"widget_id": "review_queue"}},
            {
                "tool": "add_generative_widget",
                "args": {
                    "widget_type": "note",
                    "name": f"{desk['app']} Verification",
                    "data": (
                        f"{desk['app']} on {desk['backend']}: repair verified with "
                        "a successful data retest."
                    ),
                },
            },
            {"tool": "get_workspace_snapshot", "args": {}},
        ]
    )
    task = {
        "id": task_id,
        "title": f"Repair {desk['app']} {archetype.replace('_', ' ')} incident",
        "category": "repair",
        "family": "debug",
        "capability": "backend-repair",
        "workflow": "diagnose-repair-retest",
        "domain": "finance",
        "subdomain": desk["slug"],
        "specification_level": (
            "partially-specified"
            if structural_difficulty == "medium"
            else "open-brief"
        ),
        "difficulty": difficulty,
        "tags": [
            "build-openbb-apps",
            "debug",
            "repair",
            archetype,
            "long-oracle",
        ],
        "source": "workspace-bench-build-apps-gen",
        "novelty": "assigned after generation",
        "prompt": c.phrased(task_id, _prompt_variants(desk, archetype)),
        "business_terms": [
            desk["app"],
            desk["backend"],
            "repair verified",
            "Operations Handbook",
            "Archive Workspace",
        ],
        "fixtures": {},
        "initial_state": {
            "custom_backends": custom_backends,
            "dashboards": [
                {
                    "dashboard_id": "incident_triage",
                    "name": "Incident Triage",
                    "activate": True,
                },
                {
                    "dashboard_id": "archive_workspace",
                    "name": "Archive Workspace",
                    "activate": False,
                    "widgets": [
                        {
                            "origin": archive["name"],
                            "widget_id": "archive_status",
                            "layout": {"x": 0, "y": 0, "w": 12, "h": 6},
                        }
                    ],
                },
            ],
        },
        "allowed_tools": list(WORKSPACE_TOOL_NAMES),
        "success": {
            "required_capabilities": capabilities,
            "capability_connections": connections,
            # The duplicate-backend repair leaves no state-level trace once
            # whole-workspace checks are out of scope; require the repair
            # delete call itself.
            "required_tool_calls": (
                [{"tool": "manage_backends", "args_contains": {"operation": "delete"}}]
                if archetype == "duplicate_backend"
                else []
            ),
            "business_names": [{"scope": "app", "contains": desk["app"]}],
            "app_structure": {
                "required": True,
                "layout_refs_valid": True,
                "no_overlaps": True,
            },
            "required_generated_widgets": [
                {
                    "widget_type": "note",
                    "name_contains": "Verification",
                    "data_contains": [desk["app"], desk["backend"], "repair verified"],
                }
            ],
            "workspace_checks": {
                "preserve_other_dashboards": True,
                "preserve_other_apps": True,
                "mutable_app_ids": ["incident-recovery"],
                "preserve_custom_backend_ids": archetype != "duplicate_backend",
                "required_custom_backend_ids": (
                    ["debug_target", "debug_archive"]
                    if archetype == "duplicate_backend"
                    else []
                ),
                "unique_custom_backend_names": True,
                "require_no_backend_warnings": True,
                "max_dashboard_delta": 1,
                "max_custom_backend_delta": 0,
            },
            "runtime_checks": {
                "datasets": datasets,
                "pinned_paths": True,
            },
            "trace_checks": {
                "max_invalid_tool_calls": 3,
                "max_repeated_snapshots": 4,
            },
        },
        "oracle_tool_calls": oracle,
        "limits": {"max_turns": len(oracle) * 5 // 2},
        "_family": "debug",
        "_rung": "debug",
    }
    c.diversify_generated_widget_proof(task, share=20, selected_buckets=7)
    return task


def build() -> None:
    for desk in DESKS:
        for archetype, difficulty in ARCHETYPES:
            c.SCENARIOS.append(_task(desk, archetype, difficulty))
