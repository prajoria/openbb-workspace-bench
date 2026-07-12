# Model comparison boards — index by era

This directory holds model-vs-model evaluation runs. They span **three eras** that must not
be pooled. Read this before citing any number from here.

> **Size warning.** These directories contain full per-episode transcripts
> (`conversation.json`, `tool_calls.jsonl`, `model_responses.jsonl` for every task × repeat).
> They total ~440 MB and ~13.6k files — the bulk of the repository. Whether the per-episode
> trees belong in git (versus only the summary/`*.json` board files) is an open cleanup
> decision; see the repo evaluation. Nothing here is deleted yet.

## Current era — 2026-07, runtime-aware graders

Measured on the guided interactive track, `build-openbb-apps` (236 tasks) × 2 repeats.
Strict pass = state ∧ trace ∧ runtime. These feed `runs/reports/*` and the README board.

| Directory | What it is | Status |
|---|---|---|
| `build-calibration-202607-regraded/` | **Canonical current board.** The three clean OpenAI runs re-graded under the post-loophole-fix graders (Phase 12), replayed from recorded episodes at zero API cost. Strict: GPT-5.5 128/472, GPT-5.1 47/472, GPT-5.4-mini 15/472. | **Authoritative** — source for `runs/reports/{calibration,suites,significance}.json`. |
| `build-calibration-202607/` | The same runs graded under the *pre-fix* graders (GPT-5.5 150/472, GPT-5.1 50/472). Retained only to show what the loophole fix retracted (−22 GPT-5.5 passes). | Superseded by `-regraded`; keep as provenance. |
| `phase9a-smoke/` | A 10-task cost/latency smoke that sized the full run. Superseded the moment the full calibration completed. | **Removal candidate** — no longer cited. |

The two OpenRouter legs (Claude Sonnet 5, GLM-5.2) hit `HTTP 402` mid-run and are **excluded
from all labels**; the rerun command is in `runs/reports/calibration-analysis.md`.

## Historical era — pre-reorganization boards

Recorded before the suite reorg and before the runtime dimension existed. Their task ids are
the retired `auth_t0_*` / `gen_t0_*` slugs, so they **cannot be joined to current task ids**
and are **excluded from current pooling and significance**. Kept for reproducibility of the
earlier published numbers only.

- Core suite: `core-gpt-4.1-mini/`, `core-gpt-5.5/`, `core-sonnet-5/`, `core-glm-5.2/`,
  `core-qwen3-8b/`, `core-gpt-oss-20b/`
- Build suite: `build-gpt-4.1-mini/`, `build-gpt-5.5/`, `build-sonnet-5/`, `build-glm-5.2/`,
  `build-qwen3-8b/`, `build-gpt-oss-20b/`

A current, runtime-aware **core** re-baseline has not been run; core is "pending re-run"
wherever it appears in reports.

## Proposed physical layout (not yet applied)

Once the git-hygiene decision is made, the intended structure is:

```
comparison/
  current/     build-calibration-202607-regraded/  (+ the pre-fix run as provenance)
  historical/  core-*  build-*        (the 12 pre-reorg boards)
  (phase9a-smoke removed)
```

with the per-episode transcript trees either kept only under `current/` or moved out of git
entirely (summaries stay). Applying this touches example paths in `README.md`,
`docs/private-task-suites.md`, `runs/README.md`, `scripts/compile_calibration.py`, and
`scripts/compile_suites_report.py`.
