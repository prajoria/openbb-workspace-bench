"""Shared readers for nested Workspace state used by graders and mutations."""

from __future__ import annotations

from collections.abc import Iterator

from workspace_bench.core.models import JsonDict


def lookup_path(payload: object, dotted: str) -> tuple[bool, object | None]:
    """Resolve a dotted path inside nested dictionaries as ``(found, value)``."""

    current = payload
    for part in dotted.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False, None
    return True, current


def iter_backend_widget_definitions(
    snapshot: JsonDict,
) -> Iterator[tuple[str, str, JsonDict]]:
    """Yield every declared custom-backend widget through one canonical lens."""

    for backend in (snapshot.get("custom_backends") or {}).values():
        if not isinstance(backend, dict):
            continue
        backend_name = str(backend.get("name", ""))
        for widget_id, definition in (backend.get("widgets_json") or {}).items():
            if isinstance(definition, dict):
                yield backend_name, str(widget_id), definition


def declared_backend_widgets(snapshot: JsonDict) -> dict[tuple[str, str], JsonDict]:
    """Adapt the shared widget walk to the grader's keyed lookup."""

    return {
        (backend_name, widget_id): definition
        for backend_name, widget_id, definition in iter_backend_widget_definitions(snapshot)
    }


def widget_definitions(snapshot: JsonDict) -> list[tuple[str, str, JsonDict]]:
    """Adapt the shared widget walk to the adversarial mutator's ordered list."""

    return list(iter_backend_widget_definitions(snapshot))
