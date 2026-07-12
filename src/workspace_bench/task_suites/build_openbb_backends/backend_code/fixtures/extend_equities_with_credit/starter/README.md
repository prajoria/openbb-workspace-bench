# Extend an equities backend with credit data

This is the starter repository for `extend_equities_with_credit`.

## Commands

```bash
uv sync
uv run uvicorn app:app --host 127.0.0.1 --port 8000
uv run pytest -q
```

The evaluator injects its own ephemeral port and requires CORS-compatible JSON responses.
Read `TASK_BRIEF.md` in an instantiated run for the business brief.
