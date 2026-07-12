from workspace_bench.core import adversarial, graders
from workspace_bench.core.grading.state import (
    declared_backend_widgets,
    lookup_path,
    widget_definitions,
)
from workspace_bench.core.grading.matching import subset_matches
from workspace_bench.workspace import backend_validation
from workspace_bench.workspace.geometry import rects_overlap
from workspace_bench.workspace.live_mcp import EXPECTED_MCP_TOOLS
from workspace_bench.workspace.naming import slugify
from workspace_bench.workspace.tool_surface import WORKSPACE_TOOL_NAMES


def test_all_layout_paths_share_numeric_rectangle_overlap() -> None:
    left = {"x": "0", "y": 0, "w": 10, "h": 10}
    touching = {"x": 10, "y": 0, "w": 5, "h": 5}
    overlapping = {"x": 9, "y": 9, "w": 5, "h": 5}

    assert not rects_overlap(left, touching)
    assert rects_overlap(left, overlapping)
    assert graders._find_overlaps(
        [
            {"widget_uuid": "left", "layout": left},
            {"widget_uuid": "right", "layout": overlapping},
        ]
    ) == [("left", "right")]

    errors, warnings, _ = backend_validation.validate_apps_json(
        [
            {
                "name": "Overlap",
                "tabs": {
                    "main": {
                        "id": "main",
                        "name": "Main",
                        "layout": [
                            {"i": "left", "x": 0, "y": 0, "w": 10, "h": 10},
                            {"i": "right", "x": 9, "y": 9, "w": 5, "h": 5},
                        ],
                    }
                },
            }
        ],
        {"left", "right"},
    )
    assert errors == []
    assert any("overlap" in warning for warning in warnings)


def test_backend_widget_adapters_share_one_ordered_walker() -> None:
    first = {"name": "First"}
    second = {"name": "Second"}
    snapshot = {
        "custom_backends": {
            "backend-1": {
                "name": "Research",
                "widgets_json": {"first": first, "ignored": "not-a-definition"},
            },
            "backend-2": {
                "name": "Risk",
                "widgets_json": {"second": second},
            },
        }
    }

    expected = [("Research", "first", first), ("Risk", "second", second)]
    assert widget_definitions(snapshot) == expected
    assert adversarial._widget_definitions(snapshot) == expected
    assert declared_backend_widgets(snapshot) == {
        ("Research", "first"): first,
        ("Risk", "second"): second,
    }
    assert graders._declared_backend_widgets(snapshot) == declared_backend_widgets(snapshot)


def test_path_exists_is_a_boolean_adapter_over_shared_lookup() -> None:
    payload = {"data": {"table": {"columnsDefs": []}, "value": None}}

    assert lookup_path(payload, "data.table.columnsDefs") == (True, [])
    assert graders._lookup_path(payload, "data.value") == (True, None)
    assert adversarial._path_exists(payload, "data.value")
    assert lookup_path(payload, "data.missing") == (False, None)
    assert not adversarial._path_exists(payload, "data.missing")


def test_subset_matchers_keep_their_intentionally_different_contracts() -> None:
    assert graders._dict_contains(
        {"filters": {"region": "US", "period": "annual"}},
        {"filters": {"region": "US"}},
    )
    assert not subset_matches(
        {"filters": {"region": "US"}},
        {"filters": {"region": "US", "period": "annual"}},
    )
    assert subset_matches(
        {"field": "price", "renderFn": ["greenRed"]},
        {"field": "price", "renderFn": "titleCase, greenRed"},
    )


def test_slugify_has_explicit_entity_fallbacks() -> None:
    assert slugify("Risk & Return") == "risk-return"
    assert slugify("!!!") == "app"
    assert slugify("!!!", fallback="tab") == "tab"


def test_live_mcp_tools_are_derived_from_the_canonical_surface() -> None:
    assert EXPECTED_MCP_TOOLS == set(WORKSPACE_TOOL_NAMES) - {
        "read_workspace_resource",
        "get_workspace_prompt",
    }
