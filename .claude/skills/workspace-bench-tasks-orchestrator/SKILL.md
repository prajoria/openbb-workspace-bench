---
name: workspace-bench-tasks-orchestrator
description: Coordinate the authoring of workspace_tasks stories - spawn one task-author subagent per story (each pipelines its own per-level validators), trigger the ladder fairness check, relay flags, and stop for the user's review after each completed persona. Use when asked to author or extend the workspace_tasks suite.
---

# Orchestrating story authoring

You are the coordinator, not the author. You never write task files yourself — you spawn agents that do, and you run the loop between them.

## The unit of work: one story = one author subagent

For each story, spawn **one** subagent with the `task-author` skill and this brief: the persona folder (`task_templates/<persona>/README.md`), the story file, and full access to `src/workspace_bench/data/`. That agent writes all five levels **in its one session** — never split a story across agents; the story's facts staying in one working memory is what keeps the five tasks consistent.

## Sequencing rule

Personas are delivered one at a time (each ends at the user's review), and **stories run sequentially within the persona** — one author in flight. Authors certify with `--family <persona>` (and `--difficulty level<N>` per level), so a validation run never sees half-written sibling files.

## The loop per story

1. Spawn the author. It writes the five levels sequentially in one session — and **pipelines validation itself**: after each level certifies (`--family <persona> --difficulty level<N>`), it dispatches a background `task-validator` subagent on that one task and keeps writing. It fixes validator flags as they arrive and finishes with a full-family certification. You do not manage the per-level validators — the author does.
2. When the author reports green and validator-quiet, trigger the **`task-level-fairness`** check — a fresh subagent judging the five files side by side: graded facts constant across levels, each level's signature present (and absent below it), difficulty pointing upward, five distinct asks. This is the check that only fires when a full level-per-task ladder exists.
3. Relay fairness FLAG lines back to the **same author agent** (continue its session — it still holds the story context) rather than spawning a new fixer. It repairs, re-certifies, and re-runs any per-task validation its fixes require.
4. Re-run fairness on the changed ladder. The story is done when certification is green and both checkers are quiet.

## The persona calibration gate

When a persona's **last** story goes green (all 4 stories × 5 levels = 20 tasks), run the calibration gate before counting the persona done:

```
uv run python scripts/audits/calibrate_workspace_tasks.py --persona <persona>
```

It runs gpt-4.1-mini over the persona's tasks with 3 repeats (12 attempts per level - the sample is small, hence the repeats), checks the staircase `level0 >= level1 >= ... >= level4` (ties allowed), and records the curve in `runs/reports/workspace-tasks-calibration.json`. A non-zero exit is a gate failure: diagnose before proceeding — a task failing level0 on **every** repeat is a defect fingerprint (route it back to its story's author), while a single mid-ladder wobble at this sample size may be noise (note it for the persona review, don't tune content toward the curve). Once all five personas are recorded, `--aggregate` writes the pooled per-level comparison across personas to `runs/reports/workspace-tasks-calibration.md`.

## Dead levels: a 0% rung is a question, not a result

A gate can PASS with levels at 0% (ties at the floor are allowed) — but a dead level must be explained before the persona is called done. The gating model's zero tells you nothing by itself: it cannot distinguish "honestly hard" from "impossible". Investigate every 0% level:

1. **Transcript diagnosis first.** Pull the failing episodes' tool calls and failure codes. Failures scattering across distinct modes per story lean honest; identical near-miss failures (high checks-passed, one repeated missing check) are the over-pinning fingerprint.
2. **Frontier probe.** Run one or two of the dead level's tasks as single live episodes with a strong model (the suite's arbiter, e.g. GPT-5.5 — single episodes, never a full run). A frontier pass proves the level is reachable and honestly hard. A frontier failure by one or two checks almost always means a task defect — read the transcript and find which valid route the eval refuses to credit.
3. **Close the loop with validation.** Task feasibility validation exists precisely to answer "could this be solved?" — so when calibration contradicts it, re-run the task-validator on the dead tasks WITH the probe transcript attached as evidence: fresh eyes plus what actually happened. Fix the task (never the grader, never the level labels), add the lesson to the task-author skill, re-certify, and re-run the calibration so the staircase claim holds on the shipped content.

Precedent from the pilot: level 4 sat at 0% for the gating model; the frontier probe passed level 3 outright and missed level 4 by exactly one check — an instantiate call pinned to `app_name` when the model used an equally valid `template_id` it had discovered. Task fixed, rule recorded, re-probe passed 74/74. The zero was half honest difficulty, half a defect only a live run could expose.

## Persona review gates

The unit of delivery is the **persona**: four stories, the calibration gate, done. When a persona completes: run certification over the whole suite dir, tally coverage (origins, skills, parameter types, widget types touched), and **stop for the user's review** — sample tasks, the persona's staircase, coverage tally, anything that fought the gates. Never start the next persona without their go. The first persona (portfolio_manager) is the pilot: it proves the whole pipeline before any other persona begins.

## What you watch for

- An author burning multiple fix rounds on the same task — read the failures yourself; it may be a story problem (facts wrong) rather than an authoring problem, which means fixing the story file, not the tasks.
- Validator flags that indict the *guidelines* (a rule two authors both got wrong) — fix the skill, not just the task, and note it for the persona review.
- Scope creep: authors edit only their own story's files; nothing outside `task_suites/workspace_tasks/` and never the live suites.
- Name collisions: task ids are `<story>_level<N>` with no persona in them, so **story names must be unique across all personas**, not just within one. Check before spawning an author; at each persona review also scan for duplicate ids and duplicate prompts across the whole suite.
- Commits: a story is committed only after it is fully green (certification + validator + fairness), one commit per story or per persona — never mid-loop.
