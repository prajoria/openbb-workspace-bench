from __future__ import annotations

from workspace_bench.exports import RolloutRecord, build_preference_pairs
from workspace_bench.exports.schema import ROLLOUT_SCHEMA_VERSION
from workspace_bench.exports.sft import format_sft_record


def test_build_preference_pairs_prefers_passing_or_higher_score_attempt() -> None:
    failed = _record("scenario_1", passed=False, score=0.5, repeat=1)
    passed = _record("scenario_1", passed=True, score=1.0, repeat=2)

    pairs = build_preference_pairs([failed, passed])

    assert len(pairs) == 1
    assert pairs[0]["chosen"]["metadata"]["passed"] is True
    assert pairs[0]["rejected"]["metadata"]["passed"] is False


def test_rollout_schema_version_is_stable() -> None:
    record = _record("scenario_1", passed=True, score=1.0, repeat=1)

    assert record.to_dict()["schema_version"] == ROLLOUT_SCHEMA_VERSION


def test_format_sft_record_supports_openai_messages() -> None:
    record = _record("scenario_1", passed=True, score=1.0, repeat=1)
    record.messages.append({"role": "user", "content": "hello"})

    payload = format_sft_record(record, fmt="openai_messages")

    assert payload["messages"] == [{"role": "user", "content": "hello"}]
    assert payload["metadata"]["scenario_id"] == "scenario_1"


def _record(
    scenario_id: str,
    *,
    passed: bool,
    score: float,
    repeat: int,
) -> RolloutRecord:
    metadata = {
        "scenario_id": scenario_id,
        "model_slug": "model-a",
        "passed": passed,
        "score": score,
        "repeat": repeat,
    }
    return RolloutRecord(
        task={"scenario": {"id": scenario_id}},
        messages=[],
        tool_calls=[],
        tool_results=[],
        final_snapshot={},
        grade={"passed": passed, "score": score},
        metadata=metadata,
    )
