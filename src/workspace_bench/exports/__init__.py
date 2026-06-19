"""Rollout and training-data export helpers."""

from workspace_bench.exports.loaders import (
    load_comparison_rollouts,
    load_trace_dir_rollouts,
    replay_tool_calls,
    rollouts_from_oracle,
    run_result_to_rollout,
    synthesize_messages,
)
from workspace_bench.exports.metadata import annotate_rollouts, base_export_metadata
from workspace_bench.exports.preferences import (
    build_preference_pairs,
    write_preferences_jsonl,
)
from workspace_bench.exports.rollouts import write_rollouts_jsonl
from workspace_bench.exports.schema import RolloutRecord, SFTFormat
from workspace_bench.exports.sft import format_sft_record, write_sft_jsonl

__all__ = [
    "RolloutRecord",
    "SFTFormat",
    "annotate_rollouts",
    "base_export_metadata",
    "build_preference_pairs",
    "format_sft_record",
    "load_comparison_rollouts",
    "load_trace_dir_rollouts",
    "replay_tool_calls",
    "rollouts_from_oracle",
    "run_result_to_rollout",
    "synthesize_messages",
    "write_preferences_jsonl",
    "write_rollouts_jsonl",
    "write_sft_jsonl",
]
