"""Trace-discipline grading for Workspace tool execution."""

from __future__ import annotations

from typing import Protocol

from workspace_bench.core.models import Task, ToolTraceEvent


class CheckBuilder(Protocol):
    def check(self, condition: bool, code: str, message: str) -> None: ...


def grade_trace(
    builder: CheckBuilder, task: Task, trace: tuple[ToolTraceEvent, ...]
) -> None:
    checks = task.success.trace
    invalid_count = sum(1 for event in trace if not event.ok)
    builder.check(
        invalid_count <= checks.max_invalid_tool_calls,
        "too_many_invalid_calls",
        (
            f"Expected <= {checks.max_invalid_tool_calls} invalid tool calls, "
            f"observed {invalid_count}."
        ),
    )

    if checks.must_call_schema_before_create:
        seen_schemas: set[tuple[str, str]] = set()
        for event in trace:
            args = event.call.args
            if event.call.name == "get_widget_schema" and event.ok:
                seen_schemas.add((str(args.get("origin")), str(args.get("widget_id"))))
            if event.call.name == "create_widget":
                origin = str(args.get("origin") or args.get("backend_name"))
                widget_id = str(args.get("widget_id"))
                builder.check(
                    (origin, widget_id) in seen_schemas,
                    "schema_not_called_before_create",
                    f"create_widget used {origin}/{widget_id} before get_widget_schema.",
                )

    if checks.forbid_invented_widget_ids:
        listed_widgets: set[tuple[str, str]] = set()
        listed_origins: set[str] = set()
        listing_required = "list_available_widgets" in task.allowed_tools
        for event in trace:
            if event.call.name == "list_available_widgets" and event.ok:
                listed_origin = str(event.call.args.get("origin", ""))
                if listed_origin:
                    listed_origins.add(listed_origin)
                for widget in (event.result.get("data") or {}).get("widgets", []):
                    listed_widgets.add((widget.get("origin"), widget.get("widget_id")))
                    # Listings addressed by backend_id (or unscoped) still show
                    # the agent every origin they return.
                    if widget.get("origin"):
                        listed_origins.add(str(widget.get("origin")))
            if event.call.name == "manage_backends" and event.ok:
                args = event.call.args
                if args.get("operation") in {"add", "refresh"} and args.get("name"):
                    # The agent authored these ids itself; no listing needed.
                    registered = str(args["name"])
                    listed_origins.add(registered)
                    for authored_id in args.get("widgets_json") or {}:
                        listed_widgets.add((registered, str(authored_id)))
            if event.call.name in {"get_widget_schema", "create_widget"}:
                used_origin = str(
                    event.call.args.get("origin") or event.call.args.get("backend_name") or ""
                )
                used_widget_id = event.call.args.get("widget_id")
                if listing_required:
                    builder.check(
                        used_origin in listed_origins,
                        "widget_list_not_called_before_use",
                        (
                            f"{event.call.name} used {used_origin}/{used_widget_id} "
                            "before list_available_widgets for that origin."
                        ),
                    )
                if used_origin in listed_origins:
                    builder.check(
                        (used_origin, used_widget_id) in listed_widgets,
                        "unlisted_widget_id",
                        f"{event.call.name} used unlisted widget {used_origin}/{used_widget_id}.",
                    )

    if checks.max_repeated_snapshots is not None:
        max_seen = max_consecutive_snapshots(trace)
        builder.check(
            max_seen <= checks.max_repeated_snapshots,
            "repeated_snapshots",
            (
                f"Expected <= {checks.max_repeated_snapshots} consecutive snapshots, "
                f"observed {max_seen}."
            ),
        )


def max_consecutive_snapshots(trace: tuple[ToolTraceEvent, ...]) -> int:
    max_seen = 0
    current = 0
    for event in trace:
        if event.call.name == "get_workspace_snapshot":
            current += 1
            max_seen = max(max_seen, current)
        else:
            current = 0
    return max_seen
