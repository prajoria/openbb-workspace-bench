"""Shared traversal for widget parameter definitions."""

from __future__ import annotations

from workspace_bench.core.models import JsonDict


def flatten_params(definition: JsonDict, *, recurse: bool = True) -> list[JsonDict]:
    """Return widget params in declaration order, optionally including nested inputs.

    Widget ``params`` may contain parameter objects directly or row-layout lists of
    parameter objects. When ``recurse`` is true, each parameter's ``inputParams`` are
    traversed recursively using the same declaration order.
    """

    params = definition.get("params")
    if not isinstance(params, list):
        return []

    flattened: list[JsonDict] = []

    def append_nested(param: JsonDict) -> None:
        nested = param.get("inputParams")
        if not isinstance(nested, list):
            return
        children = [item for item in nested if isinstance(item, dict)]
        flattened.extend(children)
        for child in children:
            append_nested(child)

    for entry in params:
        entries = [item for item in entry if isinstance(item, dict)] if isinstance(
            entry, list
        ) else ([entry] if isinstance(entry, dict) else [])
        flattened.extend(entries)
        if recurse:
            for param in entries:
                append_nested(param)
    return flattened
