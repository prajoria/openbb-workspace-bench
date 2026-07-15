"""Systematic invalid-candidate generation for grader sensitivity gates."""

from __future__ import annotations

import copy
from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, replace
from functools import partial
from typing import Literal

from workspace_bench.core.grading.state import lookup_path, widget_definitions
from workspace_bench.core.graders import grade_task
from workspace_bench.core.models import (
    GradeResult,
    JsonDict,
    RunResult,
    RuntimeDataset,
    Task,
    ToolCall,
    ToolTraceEvent,
)
from workspace_bench.workspace.runtime import bind_dataset, declared_fields
from workspace_bench.workspace.default_setup import apply_workspace_baseline
from workspace_bench.workspace.simulated_workspace import SimulatedWorkspace
from workspace_bench.workspace.widget_params import flatten_params


WRONG_ENDPOINT_DATA = "wrong_endpoint_data"
NEVER_INSTANTIATED = "never_instantiated"
ONE_WIDGET_MISSING = "one_widget_missing"
INCOMPATIBLE_VALUES = "incompatible_values"
BROKEN_FORM_SUBMISSION = "broken_form_submission"
SEVERED_SHARED_INTERACTION = "severed_shared_interaction"
INVALID_SETTING = "invalid_setting"
COLLAPSED_CONNECTED_PAIR = "collapsed_connected_pair"
FIELDLESS_CONTRIBUTOR = "fieldless_contributor"
SELF_SATISFIED_CONNECTION = "self_satisfied_connection"
NOTE_ONLY_PROOF = "note_only_proof"
STRIPPED_APP_PROMPTS = "stripped_app_prompts"

ADVERSARIAL_ARCHETYPES = (
    WRONG_ENDPOINT_DATA,
    NEVER_INSTANTIATED,
    ONE_WIDGET_MISSING,
    INCOMPATIBLE_VALUES,
    BROKEN_FORM_SUBMISSION,
    SEVERED_SHARED_INTERACTION,
    INVALID_SETTING,
    COLLAPSED_CONNECTED_PAIR,
    FIELDLESS_CONTRIBUTOR,
    SELF_SATISFIED_CONNECTION,
    NOTE_ONLY_PROOF,
    STRIPPED_APP_PROMPTS,
)
RUNTIME_ARCHETYPES = frozenset(
    {WRONG_ENDPOINT_DATA, INCOMPATIBLE_VALUES, BROKEN_FORM_SUBMISSION}
)


@dataclass(frozen=True)
class AdversarialContext:
    """Complete grading input that one candidate mutation may transform."""

    task: Task
    final_snapshot: JsonDict
    trace: tuple[ToolTraceEvent, ...]
    initial_snapshot: JsonDict


Mutation = Callable[[AdversarialContext], AdversarialContext]


@dataclass(frozen=True)
class AdversarialCandidate:
    """One plausible invalid solution with its intended grader signal."""

    name: str
    archetype: str
    mutate: Mutation
    primary_code: str
    expected_codes: tuple[str, ...]
    mutation_level: Literal["trace", "state", "runtime-data"]
    description: str


@dataclass(frozen=True)
class AdversarialResult:
    """Isolated oracle/candidate grades for one adversarial check."""

    task_id: str
    family: str
    candidate: AdversarialCandidate
    oracle_grade: GradeResult
    candidate_grade: GradeResult

    @property
    def observed_codes(self) -> tuple[str, ...]:
        return tuple(sorted({issue.code for issue in self.candidate_grade.issues}))

    @property
    def oracle_clean(self) -> bool:
        return self.oracle_grade.passed and not self.oracle_grade.issues

    @property
    def rejected(self) -> bool:
        return not self.candidate_grade.passed

    @property
    def expected_code_observed(self) -> bool:
        return self.candidate.primary_code in self.observed_codes

    @property
    def passed(self) -> bool:
        return self.oracle_clean and self.rejected and self.expected_code_observed


@dataclass(frozen=True)
class AdversarialMatrix:
    """Full family/archetype result matrix for one selected task collection."""

    applicable: dict[tuple[str, str], int]
    results: tuple[AdversarialResult, ...]
    runtime_sample_per_family: int

    @property
    def survivors(self) -> tuple[AdversarialResult, ...]:
        return tuple(result for result in self.results if not result.rejected)

    @property
    def wrong_reason(self) -> tuple[AdversarialResult, ...]:
        return tuple(
            result
            for result in self.results
            if result.rejected and not result.expected_code_observed
        )

    @property
    def dirty_oracles(self) -> tuple[AdversarialResult, ...]:
        return tuple(result for result in self.results if not result.oracle_clean)

    @property
    def passed(self) -> bool:
        return not (self.survivors or self.wrong_reason or self.dirty_oracles)

    def rows(self) -> list[JsonDict]:
        rows: list[JsonDict] = []
        keys = sorted(self.applicable)
        for family, archetype in keys:
            selected = [
                result
                for result in self.results
                if result.family == family and result.candidate.archetype == archetype
            ]
            rows.append(
                {
                    "family": family,
                    "archetype": archetype,
                    "applicable": self.applicable[(family, archetype)],
                    "exercised": len(selected),
                    "rejected": sum(result.rejected for result in selected),
                    "expected_code_observed": sum(
                        result.expected_code_observed for result in selected
                    ),
                    "survivors": sum(not result.rejected for result in selected),
                    "wrong_reason": sum(
                        result.rejected and not result.expected_code_observed
                        for result in selected
                    ),
                }
            )
        return rows

    def examples(self) -> list[JsonDict]:
        examples: list[JsonDict] = []
        for archetype in ADVERSARIAL_ARCHETYPES:
            result = next(
                (
                    candidate_result
                    for candidate_result in self.results
                    if candidate_result.candidate.archetype == archetype
                ),
                None,
            )
            if result is None:
                continue
            examples.append(
                {
                    "archetype": archetype,
                    "task_id": result.task_id,
                    "candidate": result.candidate.name,
                    "mutation_level": result.candidate.mutation_level,
                    "expected_codes": list(result.candidate.expected_codes),
                    "primary_code": result.candidate.primary_code,
                    "observed_codes": list(result.observed_codes),
                    "passed": result.passed,
                }
            )
        return examples


def run_adversarial_matrix(
    tasks: Sequence[Task],
    *,
    runtime_sample_per_family: int = 3,
) -> AdversarialMatrix:
    """Run suite-wide in-memory mutants and bounded runtime-probe mutants."""

    if runtime_sample_per_family < 1:
        raise ValueError("runtime_sample_per_family must be positive")
    from workspace_bench.core.runner import TaskRunner

    runner = TaskRunner()
    applicable: Counter[tuple[str, str]] = Counter()
    runtime_selected: Counter[tuple[str, str]] = Counter()
    selected: list[tuple[Task, RunResult, AdversarialCandidate]] = []
    for task in sorted(tasks, key=lambda item: (item.family, item.id)):
        oracle = runner.run(task, "oracle")
        for candidate in generate_adversarial_candidates(task, oracle):
            key = (task.family, candidate.archetype)
            applicable[key] += 1
            if candidate.archetype in RUNTIME_ARCHETYPES:
                if runtime_selected[key] >= runtime_sample_per_family:
                    continue
                runtime_selected[key] += 1
            selected.append((task, oracle, candidate))
    results = tuple(
        evaluate_adversarial_candidate(task, oracle, candidate)
        for task, oracle, candidate in selected
    )
    return AdversarialMatrix(
        applicable=dict(applicable),
        results=results,
        runtime_sample_per_family=runtime_sample_per_family,
    )


def adversarial_context(task: Task, oracle: RunResult) -> AdversarialContext:
    """Build the isolated grader input shared by oracle and mutant checks."""

    fixtures, initial_state = apply_workspace_baseline(
        task.suite,
        task.fixtures,
        task.initial_state,
        baseline_override=task.workspace_baseline,
        backends_override=task.workspace_backends,
    )
    workspace = SimulatedWorkspace()
    workspace.reset(
        backends=fixtures,
        initial_state=initial_state,
        runtime_checks=task.success.runtime,
    )
    return AdversarialContext(
        task=task,
        final_snapshot=copy.deepcopy(oracle.final_snapshot),
        trace=oracle.trace,
        initial_snapshot=workspace.snapshot(),
    )


def evaluate_adversarial_candidate(
    task: Task,
    oracle: RunResult,
    candidate: AdversarialCandidate,
) -> AdversarialResult:
    """Grade the clean oracle immediately before its isolated mutation."""

    context = adversarial_context(task, oracle)
    oracle_grade = grade_task(
        context.task,
        context.final_snapshot,
        context.trace,
        initial_snapshot=context.initial_snapshot,
    )
    mutated = candidate.mutate(context)
    candidate_grade = grade_task(
        mutated.task,
        mutated.final_snapshot,
        mutated.trace,
        initial_snapshot=mutated.initial_snapshot,
    )
    return AdversarialResult(
        task_id=task.qualified_id,
        family=task.family,
        candidate=candidate,
        oracle_grade=oracle_grade,
        candidate_grade=candidate_grade,
    )


def generate_adversarial_candidates(
    task: Task,
    oracle: RunResult,
) -> tuple[AdversarialCandidate, ...]:
    """Generate every archetype that is meaningful for this task/oracle."""

    context = adversarial_context(task, oracle)
    candidates: list[AdversarialCandidate] = []
    candidates.extend(_runtime_data_candidates(context))

    if _has_instantiate_call(context.trace) and _instantiated_custom_widgets(
        context.final_snapshot
    ):
        if task.success.required_capabilities:
            expected_codes: tuple[str, ...] = ("missing_capability",)
        elif task.success.required_widgets:
            expected_codes = ("missing_widget",)
        else:
            expected_codes = ("missing_tool_call",)
        candidates.append(
            AdversarialCandidate(
                name="published-app-never-opened",
                archetype=NEVER_INSTANTIATED,
                mutate=_never_instantiate,
                primary_code=expected_codes[0],
                expected_codes=expected_codes,
                mutation_level="trace",
                description="Keep widgets.json/apps.json but omit every app instantiation call.",
            )
        )

    missing_widget_id = _critical_app_widget(context)
    if missing_widget_id is not None:
        expected_codes = (
            (
                "capability_fields_uncovered",
                "missing_capability",
                "capability_param_missing",
                "capability_config_missing",
            )
            if task.success.required_capabilities
            else ("missing_widget",)
        )
        candidates.append(
            AdversarialCandidate(
                name=f"instantiated-app-missing-{missing_widget_id}",
                archetype=ONE_WIDGET_MISSING,
                mutate=partial(_remove_app_widget, widget_id=missing_widget_id),
                primary_code=expected_codes[0],
                expected_codes=expected_codes,
                mutation_level="state",
                description=(
                    f"Publish and instantiate the app after deleting {missing_widget_id!r} "
                    "from its layout."
                ),
            )
        )

    form_target = _form_target(context)
    if form_target is not None:
        backend_name, widget_id = form_target
        candidates.append(
            AdversarialCandidate(
                name=f"broken-form-submit-{widget_id}",
                archetype=BROKEN_FORM_SUBMISSION,
                mutate=partial(
                    _mutate_widget_trace,
                    backend_name=backend_name,
                    widget_id=widget_id,
                    mutate_definition=_break_form_contract,
                ),
                primary_code="form_submission_incompatible",
                expected_codes=("form_submission_incompatible",),
                mutation_level="trace",
                description="Keep the form UI but change its POST submission route and method.",
            )
        )

    if task.success.capability_connections:
        candidates.append(
            AdversarialCandidate(
                name="sever-shared-parameter-graph",
                archetype=SEVERED_SHARED_INTERACTION,
                mutate=_sever_groups,
                primary_code="capability_unconnected",
                expected_codes=("capability_unconnected",),
                mutation_level="trace",
                description="Keep every widget valid but delete apps.json shared-param groups.",
            )
        )

    setting_target = _setting_target(context)
    if setting_target is not None:
        backend_name, widget_id, path, expected_code = setting_target
        candidates.append(
            AdversarialCandidate(
                name=f"invalid-setting-{widget_id}-{path.replace('.', '-')}",
                archetype=INVALID_SETTING,
                mutate=_setting_mutation(
                    backend_name,
                    widget_id,
                    path,
                ),
                primary_code=expected_code,
                expected_codes=(expected_code,),
                mutation_level="trace",
                description=f"Flip the business-significant {path!r} setting on {widget_id!r}.",
            )
        )

    collapsed_target = _connected_pair_target(context)
    if collapsed_target is not None:
        backend_name, source_id, target_id = collapsed_target
        candidates.extend(
            [
                AdversarialCandidate(
                    name=f"wide-widget-collapses-{source_id}-{target_id}",
                    archetype=COLLAPSED_CONNECTED_PAIR,
                    mutate=partial(
                        _collapse_connected_pair,
                        backend_name=backend_name,
                        source_id=source_id,
                        target_id=target_id,
                        keep_self_group=False,
                    ),
                    primary_code="capability_unconnected",
                    expected_codes=(
                        "capability_unconnected",
                        "missing_capability",
                        "capability_fields_uncovered",
                    ),
                    mutation_level="trace",
                    description="Collapse a connected pair into one wide widget and no link.",
                ),
                AdversarialCandidate(
                    name=f"single-widget-self-links-{source_id}-{target_id}",
                    archetype=SELF_SATISFIED_CONNECTION,
                    mutate=partial(
                        _collapse_connected_pair,
                        backend_name=backend_name,
                        source_id=source_id,
                        target_id=target_id,
                        keep_self_group=True,
                    ),
                    primary_code="capability_unconnected",
                    expected_codes=(
                        "capability_unconnected",
                        "missing_capability",
                        "capability_fields_uncovered",
                    ),
                    mutation_level="trace",
                    description="Use one widget as both endpoints of its own parameter group.",
                ),
            ]
        )

    fieldless_target = _fieldless_target(context)
    if fieldless_target is not None:
        backend_name, widget_id = fieldless_target
        candidates.append(
            AdversarialCandidate(
                name=f"fieldless-capability-widget-{widget_id}",
                archetype=FIELDLESS_CONTRIBUTOR,
                mutate=partial(
                    _make_widget_fieldless,
                    backend_name=backend_name,
                    widget_id=widget_id,
                ),
                primary_code="capability_fields_uncovered",
                expected_codes=("capability_fields_uncovered", "missing_capability"),
                mutation_level="trace",
                description="Keep a runtime-valid shell after removing every consumed field.",
            )
        )

    if task.success.required_generated_widgets and task.success.required_capabilities:
        candidates.append(
            AdversarialCandidate(
                name="perfect-note-with-deployment-missing",
                archetype=NOTE_ONLY_PROOF,
                mutate=_never_instantiate,
                primary_code="missing_capability",
                expected_codes=("missing_capability", "capability_fields_uncovered"),
                mutation_level="trace",
                description=(
                    "Keep every required note fragment while omitting the live app deployment."
                ),
            )
        )

    if any(
        required.prompts_min_count is not None
        for required in task.success.required_app_defs
    ):
        candidates.append(
            AdversarialCandidate(
                name="published-app-with-prompts-stripped",
                archetype=STRIPPED_APP_PROMPTS,
                mutate=_strip_app_prompts,
                primary_code="app_prompts_missing",
                expected_codes=("app_prompts_missing",),
                mutation_level="state",
                description="Keep the app and layout but remove its shipped starter prompts.",
            )
        )

    return tuple(candidates)


def _strip_app_prompts(context: AdversarialContext) -> AdversarialContext:
    snapshot = copy.deepcopy(context.final_snapshot)
    for backend in (snapshot.get("custom_backends") or {}).values():
        if not isinstance(backend, dict):
            continue
        for app in backend.get("apps_json") or []:
            if isinstance(app, dict) and app.get("prompts"):
                app.pop("prompts", None)
                return replace(context, final_snapshot=snapshot)
    return context


def _connected_pair_target(
    context: AdversarialContext,
) -> tuple[str, str, str] | None:
    checks = context.task.success.runtime
    # The collapsed-pair mutation is isolated only for a single required edge.
    # In a three-node clique, removing one node can leave alternate edges that
    # legitimately satisfy every connection, so the archetype is inapplicable.
    if checks is None or len(context.task.success.capability_connections) != 1:
        return None
    capabilities = {
        capability.name: capability
        for capability in context.task.success.required_capabilities
    }
    dataset_widgets = {dataset.name: dataset.widget_id for dataset in checks.datasets}
    definitions = {
        (backend_name, widget_id): definition
        for backend_name, widget_id, definition in _widget_definitions(
            context.final_snapshot
        )
    }
    for connection in context.task.success.capability_connections:
        source = capabilities.get(connection.source)
        target = capabilities.get(connection.target)
        if source is None or target is None:
            continue
        source_ids = {
            dataset_widgets[name]
            for name in source.datasets
            if name in dataset_widgets
        }
        target_ids = {
            dataset_widgets[name]
            for name in target.datasets
            if name in dataset_widgets
        }
        for backend_name, source_id in sorted(definitions):
            if source_id not in source_ids:
                continue
            for candidate_backend, target_id in sorted(definitions):
                if candidate_backend != backend_name or target_id not in target_ids:
                    continue
                source_definition = definitions[(backend_name, source_id)]
                target_definition = definitions[(backend_name, target_id)]
                if (
                    source_id != target_id
                    and _table_columns(source_definition)
                    and _table_columns(target_definition)
                ):
                    return backend_name, source_id, target_id
    return None


def _table_columns(definition: JsonDict) -> list[JsonDict]:
    table = (definition.get("data") or {}).get("table") or {}
    columns = table.get("columnsDefs")
    return [column for column in columns or [] if isinstance(column, dict)]


def _collapse_connected_pair(
    context: AdversarialContext,
    *,
    backend_name: str,
    source_id: str,
    target_id: str,
    keep_self_group: bool,
) -> AdversarialContext:
    def mutate(args: JsonDict) -> None:
        widgets = args.get("widgets_json")
        if not isinstance(widgets, dict):
            return
        source = widgets.get(source_id)
        target = widgets.get(target_id)
        if not isinstance(source, dict) or not isinstance(target, dict):
            return
        if args.get("name") not in {None, backend_name} and not args.get("backend_id"):
            return
        columns = _table_columns(source)
        seen = {str(column.get("field", "")) for column in columns}
        columns.extend(
            copy.deepcopy(column)
            for column in _table_columns(target)
            if str(column.get("field", "")) not in seen
        )
        source.setdefault("data", {}).setdefault("table", {})["columnsDefs"] = columns
        source_params = source.setdefault("params", [])
        source_param_names = {
            str(param.get("paramName", ""))
            for param in flatten_params(source, recurse=True)
        }
        source_params.extend(
            copy.deepcopy(param)
            for param in target.get("params", []) or []
            if isinstance(param, dict)
            and str(param.get("paramName", "")) not in source_param_names
        )
        widgets.pop(target_id)
        for app in args.get("apps_json") or []:
            if not isinstance(app, dict):
                continue
            for tab in (app.get("tabs") or {}).values():
                if not isinstance(tab, dict):
                    continue
                rewritten: list[JsonDict] = []
                seen_layout: set[str] = set()
                for item in tab.get("layout", []) or []:
                    if not isinstance(item, dict):
                        continue
                    item = copy.deepcopy(item)
                    if str(item.get("i")) == target_id:
                        item["i"] = source_id
                    item_id = str(item.get("i", ""))
                    if item_id not in seen_layout:
                        seen_layout.add(item_id)
                        rewritten.append(item)
                tab["layout"] = rewritten
            groups: list[JsonDict] = []
            for group in app.get("groups", []) or []:
                if not isinstance(group, dict):
                    continue
                ids = [str(widget_id) for widget_id in group.get("widgetIds", []) or []]
                if source_id in ids and target_id in ids and not keep_self_group:
                    continue
                group = copy.deepcopy(group)
                group["widgetIds"] = list(
                    dict.fromkeys(source_id if widget_id == target_id else widget_id for widget_id in ids)
                )
                groups.append(group)
            app["groups"] = groups

    return _mutate_backend_calls(context, mutate)


def _fieldless_target(context: AdversarialContext) -> tuple[str, str] | None:
    checks = context.task.success.runtime
    if checks is None:
        return None
    dataset_widgets = {dataset.name: dataset.widget_id for dataset in checks.datasets}
    definitions = _widget_definitions(context.final_snapshot)
    for capability in context.task.success.required_capabilities:
        if not capability.must_cover_fields:
            continue
        widget_ids = {
            dataset_widgets[name]
            for name in capability.datasets
            if name in dataset_widgets
        }
        for backend_name, widget_id, definition in definitions:
            if widget_id in widget_ids and declared_fields(definition):
                return backend_name, widget_id
    return None


def _remove_declared_fields(definition: JsonDict) -> None:
    data = definition.get("data")
    if not isinstance(data, dict):
        return
    data.pop("table", None)
    for key in (
        "categoryField",
        "categoryKey",
        "xField",
        "xKey",
        "yField",
        "yKey",
        "valueField",
        "valueKey",
        "series",
    ):
        data.pop(key, None)


def _make_widget_fieldless(
    context: AdversarialContext,
    *,
    backend_name: str,
    widget_id: str,
) -> AdversarialContext:
    replayed = _mutate_widget_trace(
        context,
        backend_name,
        widget_id,
        _remove_declared_fields,
    )
    snapshot = copy.deepcopy(replayed.final_snapshot)
    for backend in (snapshot.get("custom_backends") or {}).values():
        if not isinstance(backend, dict) or str(backend.get("name", "")) != backend_name:
            continue
        definition = (backend.get("widgets_json") or {}).get(widget_id)
        if isinstance(definition, dict):
            _remove_declared_fields(definition)
    return replace(replayed, final_snapshot=snapshot)


def _runtime_data_candidates(
    context: AdversarialContext,
) -> list[AdversarialCandidate]:
    target = _runtime_row_target(context)
    if target is None:
        return []
    dataset_index, field = target
    return [
        AdversarialCandidate(
            name=f"served-dataset-shifted-{field}",
            archetype=WRONG_ENDPOINT_DATA,
            mutate=partial(
                _mutate_runtime_payload,
                dataset_index=dataset_index,
                mutate_rows=_shift_rows,
            ),
            primary_code="endpoint_response_incompatible",
            expected_codes=("endpoint_response_incompatible",),
            mutation_level="runtime-data",
            description="Serve a shifted dataset whose rows do not match the declared fields.",
        ),
        AdversarialCandidate(
            name=f"served-column-all-null-{field}",
            archetype=INCOMPATIBLE_VALUES,
            mutate=_null_field_mutation(dataset_index, field),
            primary_code="endpoint_response_incompatible",
            expected_codes=("endpoint_response_incompatible",),
            mutation_level="runtime-data",
            description=f"Keep response keys intact but serve only null values for {field!r}.",
        ),
    ]


def _runtime_row_target(context: AdversarialContext) -> tuple[int, str] | None:
    checks = context.task.success.runtime
    if checks is None:
        return None
    for _, widget_id, definition in _widget_definitions(context.final_snapshot):
        fields = sorted(declared_fields(definition))
        if not fields:
            continue
        dataset = bind_dataset(
            definition,
            widget_id,
            checks.datasets,
            pinned_paths=checks.pinned_paths,
        )
        if dataset is None:
            continue
        rows = _payload_rows(definition, dataset.payload)
        if not rows or not all(isinstance(row, dict) for row in rows):
            continue
        field = next(
            (
                candidate
                for candidate in fields
                if all(candidate in row for row in rows)
            ),
            None,
        )
        if field is not None:
            return checks.datasets.index(dataset), field
    return None


def _mutate_runtime_payload(
    context: AdversarialContext,
    dataset_index: int,
    mutate_rows: Callable[[list[JsonDict]], list[JsonDict]],
) -> AdversarialContext:
    checks = context.task.success.runtime
    if checks is None:
        return context
    datasets = list(checks.datasets)
    dataset = datasets[dataset_index]
    definition = _definition_for_dataset(context.final_snapshot, dataset, checks.datasets)
    if definition is None:
        return context
    payload = copy.deepcopy(dataset.payload)
    rows = _payload_rows(definition, payload)
    if not isinstance(rows, list):
        return context
    mutated_rows = mutate_rows(copy.deepcopy(rows))
    mutated_payload = _replace_payload_rows(definition, payload, mutated_rows)
    datasets[dataset_index] = replace(dataset, payload=mutated_payload)
    task = replace(
        context.task,
        success=replace(
            context.task.success,
            runtime=replace(checks, datasets=tuple(datasets)),
        ),
    )
    return replace(context, task=task)


def _definition_for_dataset(
    snapshot: JsonDict,
    dataset: RuntimeDataset,
    datasets: tuple[RuntimeDataset, ...],
) -> JsonDict | None:
    for _, widget_id, definition in _widget_definitions(snapshot):
        if bind_dataset(definition, widget_id, datasets) == dataset:
            return definition
    return None


def _shift_rows(rows: list[JsonDict]) -> list[JsonDict]:
    return [{"shifted_value": index + 1} for index, _ in enumerate(rows)]


def _null_field(rows: list[JsonDict], field: str) -> list[JsonDict]:
    for row in rows:
        row[field] = None
    return rows


def _null_field_mutation(dataset_index: int, field: str) -> Mutation:
    def mutate(context: AdversarialContext) -> AdversarialContext:
        return _mutate_runtime_payload(
            context,
            dataset_index,
            lambda rows: _null_field(rows, field),
        )

    return mutate


def _payload_rows(definition: JsonDict, payload: object) -> list[JsonDict] | None:
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return None
    data = definition.get("data")
    data_key = data.get("dataKey") if isinstance(data, dict) else None
    if isinstance(data_key, str) and isinstance(payload.get(data_key), list):
        return payload[data_key]
    rows = payload.get("rows")
    return rows if isinstance(rows, list) else None


def _replace_payload_rows(
    definition: JsonDict,
    payload: object,
    rows: list[JsonDict],
) -> object:
    if isinstance(payload, list):
        return rows
    if not isinstance(payload, dict):
        return payload
    data = definition.get("data")
    data_key = data.get("dataKey") if isinstance(data, dict) else None
    if isinstance(data_key, str) and isinstance(payload.get(data_key), list):
        payload[data_key] = rows
    elif isinstance(payload.get("rows"), list):
        payload["rows"] = rows
    return payload


def _has_instantiate_call(trace: tuple[ToolTraceEvent, ...]) -> bool:
    return any(
        event.call.name == "manage_apps"
        and event.call.args.get("operation") == "instantiate"
        for event in trace
    )


def _instantiated_custom_widgets(snapshot: JsonDict) -> list[JsonDict]:
    composition = snapshot.get("dashboard_composition") or {}
    return [
        widget
        for widget in composition.get("widgets", []) or []
        if isinstance(widget, dict) and not widget.get("generated")
    ]


def _never_instantiate(context: AdversarialContext) -> AdversarialContext:
    calls: list[ToolCall] = []
    for event in context.trace:
        call = event.call
        if call.name == "manage_apps" and call.args.get("operation") == "instantiate":
            # Preserve the dashboard side effect and requested name so this
            # mutant injects exactly one semantic defect: the app itself was
            # never instantiated. Without this replacement the active
            # dashboard falls back to the seed and ``dashboard_name`` masks
            # the intended missing-widget/capability/tool-call attribution.
            calls.append(
                ToolCall(
                    name="manage_dashboard",
                    args={
                        "operation": "create",
                        "name": str(
                            call.args.get("dashboard_name")
                            or call.args.get("app_name")
                            or call.args.get("template_id")
                            or "Adversarial uninstantiated app"
                        ),
                        "activate": bool(call.args.get("activate", True)),
                    },
                )
            )
        else:
            calls.append(call)
    return _replay(context, calls)


def _critical_app_widget(context: AdversarialContext) -> str | None:
    widgets = _instantiated_custom_widgets(context.final_snapshot)
    if len(widgets) < 2 or not _has_instantiate_call(context.trace):
        return None
    instantiated = {str(widget.get("widget_id", "")) for widget in widgets}
    preferred: list[str] = []
    preferred.extend(required.widget_id for required in context.task.success.required_widgets)
    checks = context.task.success.runtime
    if checks is not None:
        capabilities = sorted(
            context.task.success.required_capabilities,
            key=lambda capability: not bool(capability.must_cover_fields),
        )
        for capability in capabilities:
            preferred.extend(
                dataset.widget_id
                for dataset in checks.datasets
                if dataset.name in capability.datasets
            )
    return next((widget_id for widget_id in preferred if widget_id in instantiated), None)


def _remove_app_widget(
    context: AdversarialContext,
    widget_id: str,
) -> AdversarialContext:
    def mutate(args: JsonDict) -> None:
        for app in args.get("apps_json") or []:
            if not isinstance(app, dict):
                continue
            for tab in (app.get("tabs") or {}).values():
                if isinstance(tab, dict):
                    tab["layout"] = [
                        item
                        for item in tab.get("layout", []) or []
                        if not isinstance(item, dict) or str(item.get("i")) != widget_id
                    ]

    replayed = _mutate_backend_calls(context, mutate)
    snapshot = copy.deepcopy(replayed.final_snapshot)
    for composition in (snapshot.get("dashboard_compositions") or {}).values():
        if isinstance(composition, dict):
            composition["widgets"] = [
                widget
                for widget in composition.get("widgets", []) or []
                if not isinstance(widget, dict)
                or widget.get("generated")
                or str(widget.get("widget_id")) != widget_id
            ]
    active_id = str((snapshot.get("workspace_state") or {}).get("current_dashboard_uuid", ""))
    active = (snapshot.get("dashboard_compositions") or {}).get(active_id)
    if isinstance(active, dict):
        snapshot["dashboard_composition"] = copy.deepcopy(active)
    return replace(replayed, final_snapshot=snapshot)


def _form_target(context: AdversarialContext) -> tuple[str, str] | None:
    checks = context.task.success.runtime
    if checks is None:
        return None
    for backend_name, widget_id, definition in _widget_definitions(context.final_snapshot):
        dataset = bind_dataset(
            definition,
            widget_id,
            checks.datasets,
            pinned_paths=checks.pinned_paths,
        )
        if dataset is not None and dataset.form_endpoint is not None:
            return backend_name, widget_id
    return None


def _break_form_contract(definition: JsonDict) -> None:
    for param in flatten_params(definition, recurse=True):
        if str(param.get("method", "GET")).upper() == "POST":
            param["endpoint"] = "/adversarial-wrong-submit"


def _sever_groups(context: AdversarialContext) -> AdversarialContext:
    def mutate(args: JsonDict) -> None:
        for app in args.get("apps_json") or []:
            if isinstance(app, dict):
                app["groups"] = []

    return _mutate_backend_calls(context, mutate)


def _setting_target(
    context: AdversarialContext,
) -> tuple[str, str, str, str] | None:
    definitions = {
        (backend_name, widget_id): definition
        for backend_name, widget_id, definition in _widget_definitions(
            context.final_snapshot
        )
    }
    checks = context.task.success.runtime
    if checks is not None:
        for capability in context.task.success.required_capabilities:
            for path in _preferred_paths(capability.required_config):
                for dataset in checks.datasets:
                    if dataset.name not in capability.datasets:
                        continue
                    for (backend_name, widget_id), definition in definitions.items():
                        if dataset.widget_id != widget_id or not _path_exists(definition, path):
                            continue
                        return backend_name, widget_id, path, "capability_config_missing"
    for required in context.task.success.required_widget_defs:
        exact_definition: JsonDict | None = definitions.get(
            (required.backend_name, required.widget_id)
        )
        if exact_definition is None:
            continue
        for path in _preferred_paths(required.expect):
            if path in {"type", "endpoint"}:
                continue
            if _path_exists(exact_definition, path):
                return (
                    required.backend_name,
                    required.widget_id,
                    path,
                    "widget_def_mismatch",
                )
    return None


def _preferred_paths(values: JsonDict) -> list[str]:
    priority = {
        "runButton": 0,
        "raw": 1,
        "data.wsRowIdColumn": 2,
        "data.dataKey": 3,
        "data.updateFrequency": 4,
        "wsEndpoint": 5,
        "data.defaultSymbol": 6,
        "staleTime": 7,
        "refetchInterval": 8,
        "type": 9,
        "endpoint": 10,
    }
    return sorted(values, key=lambda path: (priority.get(path, 50), path))


def _path_exists(payload: JsonDict, dotted: str) -> bool:
    found, _ = lookup_path(payload, dotted)
    return found


def _flip_path(payload: JsonDict, dotted: str) -> None:
    current = payload
    parts = dotted.split(".")
    for part in parts[:-1]:
        child = current.get(part)
        if not isinstance(child, dict):
            return
        current = child
    key = parts[-1]
    if key in current:
        current[key] = _invalid_value(current[key])


def _invalid_value(value: object) -> object:
    if isinstance(value, bool):
        return not value
    if isinstance(value, (int, float)):
        return value + 1
    if isinstance(value, str):
        return f"{value}-adversarial"
    if isinstance(value, list):
        return [] if value else ["adversarial"]
    if isinstance(value, dict):
        return {"adversarial": True}
    return "adversarial"


def _setting_mutation(
    backend_name: str,
    widget_id: str,
    path: str,
) -> Mutation:
    def mutate(context: AdversarialContext) -> AdversarialContext:
        return _mutate_widget_trace(
            context,
            backend_name,
            widget_id,
            lambda definition: _flip_path(definition, path),
        )

    return mutate


def _mutate_widget_trace(
    context: AdversarialContext,
    backend_name: str,
    widget_id: str,
    mutate_definition: Callable[[JsonDict], None],
) -> AdversarialContext:
    def mutate(args: JsonDict) -> None:
        name = args.get("name")
        widgets = args.get("widgets_json")
        if isinstance(widgets, dict) and widget_id in widgets:
            if name is None or str(name) == backend_name or args.get("backend_id"):
                definition = widgets[widget_id]
                if isinstance(definition, dict):
                    mutate_definition(definition)

    return _mutate_backend_calls(context, mutate)


def _mutate_backend_calls(
    context: AdversarialContext,
    mutate_args: Callable[[JsonDict], None],
) -> AdversarialContext:
    calls: list[ToolCall] = []
    for event in context.trace:
        args = copy.deepcopy(event.call.args)
        if event.call.name == "manage_backends":
            mutate_args(args)
        calls.append(ToolCall(name=event.call.name, args=args))
    return _replay(context, calls)


def _replay(
    context: AdversarialContext,
    calls: Iterable[ToolCall],
) -> AdversarialContext:
    fixtures, initial_state = apply_workspace_baseline(
        context.task.suite,
        context.task.fixtures,
        context.task.initial_state,
        baseline_override=context.task.workspace_baseline,
        backends_override=context.task.workspace_backends,
    )
    workspace = SimulatedWorkspace()
    workspace.reset(
        backends=fixtures,
        initial_state=initial_state,
        runtime_checks=context.task.success.runtime,
    )
    initial_snapshot = workspace.snapshot()
    trace: list[ToolTraceEvent] = []
    for index, call in enumerate(calls, start=1):
        result = workspace.call_tool(call)
        trace.append(
            ToolTraceEvent(
                index=index,
                call=call,
                ok=bool(result.get("ok")),
                result=result,
            )
        )
    return replace(
        context,
        final_snapshot=workspace.snapshot(),
        trace=tuple(trace),
        initial_snapshot=initial_snapshot,
    )


def _widget_definitions(snapshot: JsonDict) -> list[tuple[str, str, JsonDict]]:
    return widget_definitions(snapshot)
