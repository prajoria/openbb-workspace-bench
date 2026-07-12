"""Collateral-state preservation grading."""

from __future__ import annotations

from typing import Protocol

from workspace_bench.core.models import JsonDict, Task


class CheckBuilder(Protocol):
    def check(self, condition: bool, code: str, message: str) -> None: ...


def grade_workspace_preservation(
    builder: CheckBuilder,
    task: Task,
    *,
    initial_snapshot: JsonDict | None,
    final_snapshot: JsonDict,
) -> None:
    checks = task.success.workspace
    if initial_snapshot is None:
        return

    initial_dashboards = initial_snapshot.get("dashboard_compositions") or {}
    final_dashboards = final_snapshot.get("dashboard_compositions") or {}
    if not isinstance(initial_dashboards, dict) or not isinstance(final_dashboards, dict):
        return

    if checks.preserve_other_dashboards:
        initial_active = str(
            (initial_snapshot.get("workspace_state") or {}).get("current_dashboard_uuid", "")
        )
        for dashboard_id, composition in initial_dashboards.items():
            if str(dashboard_id) == initial_active:
                continue
            builder.check(
                final_dashboards.get(dashboard_id) == composition,
                "collateral_dashboard_change",
                f"Unrelated dashboard {dashboard_id!r} changed or was deleted.",
            )

    initial_backends = initial_snapshot.get("custom_backends") or {}
    final_backends = final_snapshot.get("custom_backends") or {}
    if not isinstance(initial_backends, dict):
        initial_backends = {}
    if not isinstance(final_backends, dict):
        final_backends = {}

    if checks.preserve_custom_backend_ids:
        for backend_id, initial_backend in initial_backends.items():
            builder.check(
                backend_id in final_backends,
                "custom_backend_replaced",
                (
                    f"Existing custom backend {backend_id!r} "
                    f"({initial_backend.get('name')!r}) was replaced or deleted."
                ),
            )

    for backend_id in checks.required_custom_backend_ids:
        initial_backend = initial_backends.get(backend_id)
        builder.check(
            initial_backend is not None and backend_id in final_backends,
            "custom_backend_replaced",
            f"Required custom backend {backend_id!r} was replaced or deleted.",
        )

    if checks.unique_custom_backend_names:
        names = [
            str(backend.get("name", ""))
            for backend in final_backends.values()
            if isinstance(backend, dict)
        ]
        builder.check(
            len(names) == len(set(names)),
            "duplicate_custom_backend_name",
            "Custom backend names must be unique.",
        )

    if checks.require_no_backend_warnings:
        for backend_id, backend in final_backends.items():
            warnings = backend.get("warnings") or [] if isinstance(backend, dict) else []
            builder.check(
                not warnings,
                "backend_validation_warnings",
                f"Custom backend {backend_id!r} still has validation warnings: {warnings}.",
            )

    if checks.preserve_other_apps:
        mutable = set(checks.mutable_app_ids)
        for backend_id, initial_backend in initial_backends.items():
            if not isinstance(initial_backend, dict):
                continue
            final_backend = final_backends.get(backend_id)
            if not isinstance(final_backend, dict) and checks.unique_custom_backend_names:
                initial_name = str(initial_backend.get("name", ""))
                final_backend = next(
                    (
                        backend
                        for backend in final_backends.values()
                        if isinstance(backend, dict)
                        and str(backend.get("name", "")) == initial_name
                    ),
                    None,
                )
            initial_apps = initial_backend.get("apps_json") or []
            final_apps = (
                final_backend.get("apps_json") or []
                if isinstance(final_backend, dict)
                else []
            )
            final_by_id = {
                str(app.get("template_id") or app.get("id") or app.get("name")): app
                for app in final_apps
                if isinstance(app, dict)
            }
            for initial_app in initial_apps:
                if not isinstance(initial_app, dict):
                    continue
                app_id = str(
                    initial_app.get("template_id")
                    or initial_app.get("id")
                    or initial_app.get("name")
                )
                if app_id in mutable:
                    continue
                builder.check(
                    final_by_id.get(app_id) == initial_app,
                    "collateral_app_change",
                    f"Unrelated app {app_id!r} changed or was deleted.",
                )

    if checks.max_dashboard_delta is not None:
        delta = len(final_dashboards) - len(initial_dashboards)
        builder.check(
            delta <= checks.max_dashboard_delta,
            "unexpected_dashboard_created",
            (
                f"Expected at most {checks.max_dashboard_delta} new dashboard(s), "
                f"observed delta {delta}."
            ),
        )

    if checks.max_custom_backend_delta is not None:
        initial_count = len(initial_backends)
        final_count = len(final_backends)
        delta = final_count - initial_count
        builder.check(
            delta <= checks.max_custom_backend_delta,
            "unexpected_backend_created",
            (
                f"Expected at most {checks.max_custom_backend_delta} new custom "
                f"backend(s), observed delta {delta}."
            ),
        )
