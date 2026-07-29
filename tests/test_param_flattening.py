"""Regression coverage for canonical widget-parameter traversal."""

from workspace_bench.core import adversarial, graders
from workspace_bench.core.models import JsonDict
from workspace_bench.workspace import runtime
from workspace_bench.workspace.widget_params import flatten_params


DEFINITION: JsonDict = {
    "params": [
        [
            {
                "paramName": "outer_form",
                "type": "form",
                "inputParams": [
                    {
                        "paramName": "middle_tabs",
                        "type": "tabs",
                        "inputParams": [
                            {"paramName": "deep_parameter", "type": "date"},
                        ],
                    }
                ],
            }
        ]
    ]
}


def _param_names(params: list[JsonDict]) -> set[str]:
    return {str(param.get("paramName")) for param in params}


def test_flatten_params_controls_recursive_input_traversal() -> None:
    assert _param_names(flatten_params(DEFINITION, recurse=True)) == {
        "outer_form",
        "middle_tabs",
        "deep_parameter",
    }
    assert _param_names(flatten_params(DEFINITION, recurse=False)) == {"outer_form"}


def test_gate_lint_grader_and_runtime_share_recursive_param_visibility() -> None:
    recursive_consumers = (
        adversarial,
        graders,
        runtime,
    )
    expected_names = _param_names(flatten_params(DEFINITION, recurse=True))

    for consumer in recursive_consumers:
        assert consumer.flatten_params is flatten_params
        assert _param_names(consumer.flatten_params(DEFINITION, recurse=True)) == expected_names

    assert set(runtime.synthesize_params(DEFINITION)) == expected_names
    assert graders._definition_param_kinds(DEFINITION) == {"form", "tabs", "date"}
