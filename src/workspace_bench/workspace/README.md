# Workspace

`workspace_bench.workspace` contains the Workspace runtime adapters used by the
benchmark.

It owns deterministic fixture backends, the in-process Workspace MCP-like
simulator, and the live `workspace-mcp` smoke bridge. This package should expose
Workspace tool behavior to the benchmark core without knowing about model
providers, export formats, or RL policies.

Use this package when you need to:

- serve deterministic fixture backends over HTTP
- reset and mutate simulated Workspace dashboard state
- call Workspace-like tools in-process
- smoke-test a real `workspace-mcp` sidecar path
- inspect fixture widget/app definitions

Module responsibilities:

- `fixtures.py`: deterministic backend data, widget schemas, app templates, and fixture HTTP server.
- `widget_params.py`: canonical flat traversal of row-grouped and recursively nested widget params.
- `simulated_workspace.py`: in-process Workspace state machine and tool dispatcher.
- `live_mcp.py`: smoke bridge for the real streamable HTTP MCP sidecar.

The simulator is the default benchmark runtime because it is deterministic and
fast. The live MCP path is a compatibility smoke test, not the default
high-throughput evaluator.
