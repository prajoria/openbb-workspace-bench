---
name: prompt-realism
description: Author enterprise-apps-usage task prompts from their machine-emitted specs - realistic analyst/PM asks that satisfy every graded invariant. Use when authoring or re-authoring prompts after generator changes, or when the user asks to make task prompts more realistic.
---

# Prompt authoring from specs

You author the **prompt field only**, from each task's spec. Setup, traces, and evals are generator-owned and never touched. Every prompt must survive the generator's full assertion battery — the checks are the editor-in-chief; you are the voice.

## Inputs and output

1. Specs: `src/workspace_bench/task_suites/enterprise_apps_usage/prompt_specs.json` — per task: `must_contain` literals (each with its reason), `must_describe_never_print` tokens with their registered descriptions, `grounded_from_read` facts, the level directive, forbidden fragments, the word cap, and the reference flow. **The spec is law.** If a good prompt and a spec entry conflict, the spec wins and the conflict gets flagged to the user — never argue for weakening a check.
2. Output: `src/workspace_bench/task_suites/enterprise_apps_usage/prompt_overlay.json` — `{task_id: {"prompt": ..., "spec_sha256": <copied from the task's spec>}}`. Committed; the sha is the provenance: when a spec changes, its overlay entry goes stale and is re-authored.

## Voice contract

Write like an analyst or PM asking a colleague, not like a test case:

- **Forbidden:** everything in the spec's `forbidden_fragments`; taxonomy or label-colon openers; the word "board" for a dashboard (say **dashboard**); "settings" for widget parameters (say **parameters**).
- **Wanted:** a reason where it fits naturally ("before the client call…", "the desk needs…"); plain verbs (set, restore, add, read, stand up); catalog names woven into natural word order, never inventory rows; varied sentence shapes across a family — no two rungs should read like the same sentence with swapped nouns.
- Display names in `must_contain` stay **exactly as spelled** — they are disambiguation tokens, not prose to improve.
- The opening five words (casefolded) must be unique across all 192 prompts: place a spine-distinctive token early. Collisions come back from the checker; fix them there.
- Respect the `level_directive`: never state what the level withholds, never withhold what it states.

## Procedure

1. Work one family at a time (~24 prompts). Before writing anything, read the whole family's specs side by side, plus the last approved family's prompts, so variety is deliberate.
2. Skip tasks whose overlay entry is fresh (matching `spec_sha256`) unless asked.
3. After each family, run the inner loop: `uv run python scripts/generators/check_prompt_overlay.py` — it applies the overlay and runs the full battery, printing precise per-task failures. Fix and re-run until green.
4. Before committing a batch, run the full generator once (`uv run python scripts/generators/generate_usage_suite.py`) — it additionally writes files and replays oracle/no-op certification.
5. Have a fresh subagent run `/prompt-validator` over the family — a feasibility pass by eyes that did not author.
6. End each family with a before→after sample of 3–4 prompts for the user's read before starting the next family.

## Gold examples

(Empty until the first family is approved. Then paste 3–4 approved before→after pairs here — they outrank every rule above when in tension, because they carry the user's actual taste.)

## Done means

Overlay entries for the batch, checker fully green, a clean full generator run, the validator pass reported, and the user has seen the sample.
