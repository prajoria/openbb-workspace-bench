# Reconcile a trade table manifest and payload

This is the starter repository for `repair_trade_column_contract`.

## Commands

```bash
uv sync
uv run uvicorn app:app --host 127.0.0.1 --port 8000
uv run pytest -q
```

The evaluator injects its own ephemeral port and requires CORS-compatible JSON responses.
Read `TASK_BRIEF.md` in an instantiated run for the business brief.
