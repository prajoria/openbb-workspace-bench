# Agents

`workspace_bench.agents` contains the agent-facing interfaces.

There are two paths:

- built-in benchmark agents such as `oracle` and `noop`
- external command agents that read a task JSON file and write JSONL tool calls

The JSONL command protocol is the universal bring-your-own-agent contract. It
lets local scripts, hosted model wrappers, Claude Code-style agents, OpenAI
models, Ollama models, or other processes participate without importing the
benchmark internals.

The benchmark remains responsible for executing the emitted tool calls,
capturing the final Workspace state, and grading the result.

