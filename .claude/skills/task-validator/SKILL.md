---
name: task-validator
description: Fresh-eyes feasibility judgment of workspace_tasks task.json files - could an agent given only the prompt and the tools actually satisfy the eval? Use after tasks are authored and certified, before they count.
---

# Task validation with fresh eyes

You judge finished tasks the way a test-taker meets them. You did **not** author them, and you must not read the story or persona files in `task_templates/` — your value is that you see only what the model under test will see. Input: the `task.json` files themselves.

## What you may consult

**The data folder — you can and should open `src/workspace_bench/data/` to establish whether the task is actually possible:**

- `backends/*.json` — does the graded widget exist under the named origin? Is the display name spelled the way the prompt spells it? Do the parameter's **declared options** contain every graded value? Do the served data rows contain the facts a note or answer must record?
- `skills/*.json` — when a note must record something derived from a skill, does the skill text really contain it, and does the prompt's description locate it **uniquely** (not two candidate phrases)?
- `initial_states/*.json` — does the seeded world match what the prompt assumes (the named dashboard exists, the "broken" state is actually broken)?

Also fair game: the simulator's tool behavior in `src/workspace_bench/workspace/` when a verdict hinges on it (e.g. whether a wrong name returns a helpful error). Never modify any file.

## The five questions, per task

1. **Value reachability.** Every graded argument and note content must be obtainable from the prompt, a stated policy phrase whose meaning a person could resolve (check the options!), or a read of the world. A graded value with no path to it fails the task for everyone — flag it.
2. **Target findability.** Enough words to locate each widget, backend, dashboard, and tab. If two catalog entries share a display name, the prompt must disambiguate (app or origin). Check the catalogs, not your intuition.
3. **Possibility.** The asked-for end state is achievable and self-consistent: the params exist on that widget, the layout fits, the seeded defect is really there to fix, the backend/app lifecycle the eval expects matches what the tools do.
4. **Budget sanity.** Count the calls a competent-but-not-psychic agent needs, including discovery. If `max_turns` only fits the answer key, flag it.
5. **Single ask, single route.** One coherent request — and no coin-flip: if two equally reasonable readings or two eval-equivalent trajectories exist and only one is graded, flag it.

## What each level promises — and what to check

Every story runs the same five-step ladder. Each level makes the ask harder in exactly one new way, and part of your job is confirming the task actually delivers its level — not an easier or unfairer version of it. Example prompts below all use the same story (the PM wants the Trade Ideas widget on their briefing dashboard, set to fund Flagship Long/Short and period QTD).

**Level 0 — Execute: everything is spelled out.** The prompt names the widget, where it lives, where it goes, and every value to set. The model only has to follow instructions.

> *"Add Trade Ideas from Bench Stark Enterprise's Portfolio Command Center to the open Pilot Decision Brief dashboard, with fund set to Flagship Long/Short and period set to QTD."*

Check: the prompt really does state every name and value the grader checks. If something graded is missing here, the floor level is broken.

**Level 1 — Find: one thing is described, not named.** The prompt refers to something the way a colleague would ("the PM's idea pipeline") instead of by its exact name. The model must look around the workspace to figure out what's meant.

> *"Get the PM's idea pipeline up on the open Pilot Decision Brief dashboard — it's somewhere under Bench Stark Enterprise's Portfolio Command Center — for Flagship Long/Short and QTD."*

Check: the casual description plus the other words really do point to exactly one widget. If two catalog entries fit the description equally well, the task is a guess.

**Level 2 — Derive: one value must be worked out.** The prompt hides one value behind a shorthand or house policy ("per the quarterly briefing policy" instead of "QTD"). The model must translate.

> *"Prep the open Pilot Decision Brief dashboard with Trade Ideas from Bench Stark Enterprise's Portfolio Command Center for Flagship Long/Short, per the quarterly briefing policy."*

Check two failure directions: if the hidden value *does* appear in the prompt, the level is fake (nothing to work out); if a person *couldn't* work it out — from the phrase's plain meaning or the widget's own option list (open the catalog and look) — the task is unfair.

**Level 3 — Ground: read the governing source.** A skill or document governs the outcome: the deliverable (usually a note) must contain a fact that lives only in that document. The prompt names the document and *describes* the fact without saying it.

Level 3 also runs in the ambient world: the dashboard is populated with preservation-graded content, including a decoy near-copy of the target, a stale note, and a stale-twin instance whose correction rides in the ask. The model must do the grounded work, correct the stale twin, and leave every other pre-existing item standing.

> *"On the open Pilot Decision Brief dashboard, fix the stale Trade Ideas instance for Flagship Long/Short and QTD and add a fresh one alongside it. Leave the existing views and notes untouched, then close with a note recording the final item the Finance Guidance Tracker skill's workflow lists."*

Check both parts. The knowledge fact must not appear anywhere in the prompt — otherwise the model could skip the reading — and its description must locate exactly one fact in the named source. The preservation-graded content must really be in the starting state, ALL pre-existing content must be graded as preserved, the stale-twin correction must select the intended opaque uuid, and the look-alike clutter must not make the requested change ambiguous.

**Level 4 — Compose: build it, then use it.** The full workflow stands up a backend, publishes and instantiates an app with a named tab, and then does the story's work with it. It keeps level 3's knowledge read and note, and it runs under the same ambient-world preservation contract. One coherent request, not a checklist.

> *"Stand up the Briefing Feed Service with an Idea Register table, publish and open its app on the named Briefing tab, then on the open Pilot Decision Brief dashboard fix the stale Trade Ideas instance for Flagship Long/Short and QTD and add a fresh one alongside it without disturbing the existing views or notes. Close with a note recording the final item the Finance Guidance Tracker skill's workflow lists."*

Check: the whole chain is achievable within the turn budget; the names the prompt states are enough for the model to derive the technical ids it must author (the naming convention lives in the workspace's own spec document, which the model can read); the level-3 read-and-note and ambient preservation checks remain present; and the ask still reads as one job, not a list of disconnected demands.

## What not to flag

Style, tone, or wording you'd merely phrase differently; difficulty that is honest (a hard-but-fair rung is the point); redundancy in optional reference steps. You are the feasibility gate, not an editor.

## Report

Return raw findings as your final message — one line per task:

```
<task_id>: OK
<task_id>: FLAG - <one sentence: what is unreachable/impossible and why>
```

End with `<n> flagged / <n> checked`. Modify nothing; the author fixes, then you re-check only the changed tasks.
