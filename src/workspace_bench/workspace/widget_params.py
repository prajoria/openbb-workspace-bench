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


def sanitize_data_args(
    definition: JsonDict, data_args: JsonDict, *, mode: str = "update"
) -> JsonDict:
    """Apply the real Workspace frontend's data_args handling.

    Verified against the live Workspace MCP bridge (2026-07-12), which is
    asymmetric between the two paths:

    - ``mode="create"``: keys that do not name a declared widget parameter are
      silently dropped; declared keys keep whatever value was sent; missing
      declared parameters are backfilled with their declared default value.
    - ``mode="update"``: undeclared keys are dropped, and a parameter with a
      declared options list only accepts values from that list.
    """

    declared: dict[str, JsonDict] = {}
    for param in flatten_params(definition):
        name = param.get("paramName")
        if name:
            declared.setdefault(str(name), param)
    sanitized: JsonDict = {}
    for key, value in data_args.items():
        spec = declared.get(key)
        if spec is None:
            continue
        if mode == "update":
            options = spec.get("options")
            if isinstance(options, list) and options:
                values = {
                    str(option.get("value") if isinstance(option, dict) else option)
                    for option in options
                }
                if str(value) not in values:
                    continue
        sanitized[key] = value
    if mode == "create":
        for name, param in declared.items():
            if name not in sanitized and param.get("value") is not None:
                sanitized[name] = param.get("value")
    return sanitized
