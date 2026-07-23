---
name: prompt-validator
description: Quick per-task feasibility test - flag prompts that ask something impossible or unreachable given the visible world, data, and budget. Use after prompt rewrites, after generator changes, or when a task's fairness is in doubt.
---

# Prompt feasibility check

You are the skeptic, not the author: never fix prompts, tasks, or assertions here — report flags. Rewriting belongs to `/prompt-realism`. This is a **quick heuristic test**, seconds per task, not a full solve: the one question is *could a competent agent actually do this, given only the prompt and the visible world?*

## Heuristics (per task, in order — stop at the first flag)

1. **Value reachability.** Every graded value must be reachable: stated in the prompt, derivable from a stated policy phrase, or actually present in the world — the answer figure exists in the fixture rows the graded read returns (check the backend JSON under `src/workspace_bench/data/backends/` with the graded `data_args`); the note phrase exists in the named skill/resource/prompt text; an authored id derives from a prompt-stated name via the convention in the widgets.json spec resource.
2. **Target findability.** Every named widget, dashboard, skill, resource, and app exists and matches exactly one thing in the mounted world. A display name matching zero or several targets is a flag.
3. **Possibility.** Nothing asked is something the workspace would refuse: parameter values are inside the widget's declared options (the product silently drops out-of-options values); the tool a step needs is in `allowed_tools`; anything to "preserve" or "restore" actually exists in the seeded state; layout coordinates fit the 40-column grid.
4. **Budget sanity.** `max_turns` covers the minimum call count the ask implies, with discovery headroom on rungs where the prompt withholds identifiers.
5. **Single ask.** The prompt is one coherent ask a person could hold in their head — not several unrelated workflows fused into a sentence (the crypto six-dimensions lesson).

## Output

One line per task: `OK` or `FLAG: <task_id>: <one-sentence reason naming the exact value/name involved>` — e.g. `FLAG: segment_mix_handoff_level3: graded value 52365.6 not present in daloopa_segment_breakdown served rows for AAPL 2026Q1`. Finish with `N flagged / M checked`. No essays, no fixes — findings go to the user or the rewriting session to action.

## When suspicion is high

Only for a task already under suspicion (a model fails it every run, or the user flagged it): do one careful pass — read prompt + setup, write down the calls you would make and the values you would produce, then open the eval and check that each graded item was plausibly implied. Report the mismatch precisely. This deep mode is the exception, not the loop.
