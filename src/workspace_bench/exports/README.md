# Exports

`workspace_bench.exports` converts benchmark runs into portable data.

It sits after evaluation. The benchmark first runs an agent, captures tool
calls and tool results, grades the final Workspace state, and only then exports
the attempt as rollout, SFT, or preference data.

Use this package when you need to:

- export canonical rollout JSONL
- convert passing traces into SFT message formats
- include failed attempts with grade metadata
- create chosen/rejected preference pairs from repeated attempts
- replay saved tool calls through the normal grader

Module responsibilities:

- `schema.py`: canonical rollout and preference schema constants.
- `metadata.py`: benchmark release, export timestamp, and task-suite annotations.
- `loaders.py`: oracle, comparison-directory, trace-directory, and replay loaders.
- `rollouts.py`: canonical rollout JSONL writer.
- `sft.py`: SFT format conversion and JSONL writer.
- `preferences.py`: chosen/rejected preference-pair builder and writer.
- `jsonl.py`: shared JSONL writer utility.

Exports should stay separate from benchmark publishing. Public tasks, hidden
tasks, oracle traces, and model traces should only become training data through
an explicit export command.
