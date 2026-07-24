---
name: task-level-fairness
description: Judge a completed story ladder as a set - the six task.json files of one story compared side by side, verifying each level genuinely differentiates according to the ladder rules. Triggered once all six levels of a story exist and pass per-task validation.
---

# Ladder fairness with fresh eyes

You receive the **six task.json files of one story** and judge them as a set. The task-validator already checked each task alone; your job is what only a side-by-side view can catch: do the levels actually differ in the way the ladder promises, with the same story underneath? Like the validator, you must not read `task_templates/` — the tasks speak for themselves. You may open `src/workspace_bench/data/` to check any fact.

## The ladder contract

**The graded story facts stay constant — this is the hard rule.** Diff the six evals: the same target widget(s), origin, dashboard name, and parameter values must appear at every level. If level 3 grades a different fund than level 0, or a level quietly swaps widgets, the ladder is broken — a drop in pass rates between those levels would measure a content change, not a difficulty step.

**The furniture may vary — this is not a hard rule.** The populated worlds of levels 3-5 need the preservation demand *present and of roughly comparable weight*, but not the same props: level 3's duplicate widget and level 4's stale chart are both fine clutter. Flag a world only when its burden is clearly out of step (level 4 nearly empty while level 3 is crowded), never for different-but-comparable furniture. Likewise levels 0-2 aren't required to be sterile — just simple enough that nothing competes with the level's one demand.

**Each level adds one new demand — its signature:**

| level | its signature — present here, and checkably absent below |
|---|---|
| 0 | none: everything stated, minimal world, the floor |
| 1 | the target is *not named exactly* in the prompt — only described colloquially (the only level where this happens) |
| 2 | exactly one graded value is absent from the prompt, carried by a stated policy phrase (the only level where a value is hidden this way) |
| 3 | the starting dashboard is populated, including a decoy near-duplicate of the target itself (same widget, different configuration), and the eval grades ALL pre-existing content as preserved, the decoy included |
| 4 | a knowledge read is required, and a note is graded on a fact derivable only from that source — the fact never appears in the prompt |
| 5 | a real platform build is graded: authored backend (`required_widget_defs`) AND a published, instantiated app with a named tab and the built widget required ON that tab (`required_app_defs` with `widgets_on_tab`), its widget then used - alongside level 4's read-and-note; story-shape extras like delegation ride HERE (orchestration), never at level 4 |

**World demands accumulate; prompt dials do not.** A populated, preservation-graded world is present from level 3 through 5 (same demand, not necessarily the same furniture); level 5 keeps level 4's read-and-note demand alongside its build. But prompt-side signatures are one level each: level 3 may name the widget plainly again (finding was level 1's exam) and may print the value that level 2 hid (deriving was level 2's exam). This is deliberate — each level's failure should have one interpretation.

## What to check, in order

1. **Constant core** — diff the evals; flag any *graded* fact (target, origin, values, dashboard name) that changes between levels. Ungraded furniture differences are fine.
2. **Signatures present** — each level's new demand actually exists in that task, in both the eval and the prompt. A "level 3" whose starting dashboard is empty, or a "level 4" whose note content also appears in its prompt, is wearing the wrong label.
3. **Signatures absent where they should be** — the level-1 colloquialism doesn't leak into level 0; the level-2 hidden value is plainly stated at levels 0 and 1; no level below 4 requires a knowledge read.
4. **Difficulty direction** — walking 0→5, each task should have more to do or more to figure out than the last. Flag any level that is plausibly *easier* than its predecessor (fewer demands, a more generous budget for the same work, a prompt that hands over more).
5. **Budgets track the growth** — `max_turns` should grow (or hold) as the reference traces grow; a level whose demands grew while its budget shrank starves honest solves.
6. **Rung weight** — a "level 3" whose furniture contains no near-duplicate of the target, or a "level 5" that registers a bare backend without publishing and instantiating an app, is wearing the wrong label: its demand is too light to cost more than the level below. Flag underweight rungs even when everything else checks out.
7. **Six asks, not one ask six times** — the prompts should read like the same person raising the same matter with rising demands, not one sentence photocopied with a word swapped. Flag copy-paste ladders; they train pattern-matching, not capability.

## What not to flag

Intentional repetition of the world dials (levels 3-5 sharing the same clutter is correct); values restated at level 3+ that level 2 hid (correct by design); stylistic differences between prompts (that's the point); a hard-but-honest top rung.

## Report

One line per finding, story-scoped:

```
<story>: LADDER OK
<story>: FLAG level<N> - <one sentence: which rule is violated and how>
```

End with `<n> flags`. Modify nothing; flags go back to the story's author agent.
