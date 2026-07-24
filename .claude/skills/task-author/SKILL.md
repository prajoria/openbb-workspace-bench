---
name: task-author
description: Author complete workspace_tasks task.json files (setup, eval, reference trace, prompt) from a persona README and a story markdown. Use when creating or revising tasks for the workspace_tasks suite.
---

# Task authoring from stories

You write **complete tasks** — setup, eval, reference trace, and prompt in one sitting — for the `workspace_tasks` suite. There is no generator: you are the generator. Two gates stand behind you (certification replay and a fresh-eyes validator), so your job is to compose tasks that are *right*, not merely plausible.

## Your place in the pipeline

You are a dedicated story agent, spawned by an orchestrator (see the `workspace-bench-tasks-orchestrator` skill) with one assignment: **one story — all six levels, in this one session**. Holding the story's canonical facts (widget, values, dashboard, governing skill) in a single working session is what keeps the six tasks consistent; never hand parts of a ladder to anyone else.

Validation is pipelined: **as soon as a level certifies, you dispatch a task-validator subagent on that one task in the background and keep writing the next level.** Each validator is a fresh session — give it only the task file path and point it at the `task-validator` skill; never paste story or persona content into its brief (its value is that it meets the task cold). Fix FLAG lines as they arrive — an early flag often reveals a mistake you'd otherwise repeat at every later level.

When all six levels are authored and validator-quiet, run the full-family certification and report. The orchestrator then triggers the `task-level-fairness` check across your six files; its per-level flags come back to you in this same session. You are done when certification is green and both checkers are quiet. Certify with the `--family <persona>` filter (add `--difficulty level<N>` for a single level): other stories may be in flight in other folders, and their work-in-progress is not your concern.

## Ground truth: the data folder

You have full access to `src/workspace_bench/data/` and you **must** use it. Every fact in a task traces to it — nothing is invented:

- `backends/*.json` — the four catalogs (`stark_enterprise_x`, `getting_started`, `widget_examples`, `support_daloopa_skills`): every widget's id, display name, endpoint, parameters with their **declared options and defaults**, and the data rows it serves.
- `skills/*.json` — the ten skill documents. If a note must record something "the skill says", open the skill and confirm the exact phrase exists.
- `initial_states/*.json` — the seeded workspace states, including `stark_workspace_a.json` (the standard lived-in baseline: Home + the Stark apps as dashboards).

Before writing any task: locate the story's widgets in the catalogs, confirm the display names and origins **letter for letter**, confirm every graded parameter value appears in that parameter's declared options, and read any governing skill end to end. If the story's facts block contradicts the data folder, the data folder wins — flag the discrepancy instead of writing a lie.

## Inputs and output

- **In:** `task_templates/<persona>/README.md` (who is asking: voice, priorities, vocabulary) and `task_templates/<persona>/<story>.md` — short prose context plus a `facts:` block carrying the canonical ingredients: the working dashboard name, the target widget(s) with app and origin, the parameter values, a find-hint (how the persona says it colloquially, for level 1), the level-2 policy phrase and which value it carries, the governing knowledge source for level 4, and the level-5 build names (backend, table, app/tab if used). Furniture for levels 3-5 is yours to invent; the facts block is the graded canon. The story's name must be unique across **all** personas — task ids carry no persona prefix.
- **Out:** six files in `src/workspace_bench/task_suites/workspace_tasks/<persona>/` named `<story>_level0.json` … `<story>_level5.json`. The persona directory doubles as the task family. Tasks are committed source — self-contained, no external references beyond the standard baselines and catalogs.

## The task.json schema

Exactly five top-level keys — the existing bench schema, so every tool (validate, runner, model harness) works unchanged:

```json
{
  "id": "<story>_level<N>",
  "difficulty": "level0 ... level5",
  "prompt": "<the persona's ask - written last>",
  "setup": {
    "workspace_baseline": "stark-workspace-a",
    "workspace_backends": ["stark-enterprise-x", "support-daloopa-skills", "getting-started", "widget-examples"],
    "workspace_skills": ["<all ten skill slugs>"],
    "default_selected_dashboard": "<a dashboard name from this task's initial_state, or one of the baseline's dashboard names>",
    "allowed_tools": ["<the standard twenty>"],
    "initial_state": { "dashboard": { "name": ..., "tabs": [...], "widgets": [...] } }
  },
  "eval": {
    "required_tools": [ {"tool": ..., "args": {...}, "graded_args": [...], "optional": true|false} ],
    "required_widgets": [ {"origin": ..., "widget_id": ..., "data_args": {...}} ],
    "required_generated_widgets": [ {"widget_type": "note", "name_contains": ..., "data_contains": [...]} ],
    "max_turns": <reference call count + 3>
  }
}
```

Do not write a `category` field — the suite's `task_suite.json` manifest supplies it for every task.

Other eval keys available when the story needs them: `required_tabs`, `required_dashboard_name_contains`, `required_values_in_answer`, `required_widget_defs` / `required_app_defs` (for built backends). Copy field shapes from certified tasks in `task_suites/enterprise_apps_usage/` when unsure — they are the precedent library.

## The reference trace and the budget

`eval.required_tools` is both the grading contract and the oracle replay:

- It must model an **honest solve path from the prompt** — include the discovery calls a competent agent would need (`get_workspace_snapshot`, `list_available_widgets`, `get_params_options`) marked `"optional": true`; grade only the calls that matter, and only the arguments that matter (`graded_args`).
- `max_turns` = number of entries in `required_tools` + 3. Never budget for the answer key; budget for the solve.
- The replayed trace must pass the grader (oracle) and a do-nothing agent must fail (no-op). If nothing would fail a do-nothing agent, the task grades nothing — add an outcome check.
- **Instantiate calls: grade the operation only.** `manage_apps instantiate` accepts equally valid addressings (`app_name`, or `template_id` discovered via `manage_apps list`); pinning one fails grounded agents that chose the other. Grade `graded_args: ["operation"]` and let `required_app_defs` (name_contains, widgets_on_tab) plus state checks carry which app was built and instantiated.
- **Read calls: grade the args — they are load-bearing.** An unfiltered `get_widget_data` returns the widget's ENTIRE fixture (all tickers, all periods), so a graded note's values never prove the correct read on their own — a lazy bare read dumps everything and the note can quote it. Keep `data_args` in the read's `graded_args` for every read-and-report task. At the Execute and Find rungs this is also the point: "read X with ticker AAPL" graded as stated measures faithful execution; an agent that detours (create-then-bare-read) and skips the stated call fails honestly.

## The six levels

One story, six tasks, same canonical facts throughout. Each level adds one new demand — its signature. **World demands accumulate** (levels 3-5 each run in a populated, preservation-graded world — comparable burden, same furniture recommended but not required; level 5 keeps level 4's read-and-note), but **prompt dials are one level each**: level 3 may name the widget plainly again and print the value level 2 hid — finding and deriving were already examined, and each level's failure should have one interpretation.

| level | dial | setup | eval | prompt |
|---|---|---|---|---|
| 0 **Execute** | none | minimal | grade the stated action | everything stated: display names, every parameter key and value |
| 1 **Find** | discovery | minimal | same | one thing named only colloquially (the story's find-hint); enough other words to disambiguate |
| 2 **Derive** | inference | minimal | grades the derived value | a named policy phrase carries one graded value; do **not** also print that value |
| 3 **Care** | preservation | populated dashboard whose distractors include a **decoy near-duplicate of the target itself** (same widget, different configuration) plus at least one more piece of furniture | ALL pre-existing content graded as preserved, the decoy included - byte-for-byte | names the open dashboard; asks only for the change; the decoy is never mentioned |
| 4 **Ground** | reading | as 3 | a required knowledge read + a note whose graded content is derivable **only from the source** | names the source; **describes** the graded fact ("recording what the skill lists last") — never prints it |
| 5 **Compose** | orchestration | as 3 or fresh | a **real platform build**: authored backend (`required_widget_defs`) AND a published app with at least one named tab (`required_app_defs`), instantiated, its widget then used - plus level 4's read-and-note | one coherent build-publish-instantiate-use ask |

The level-2 rule in full: the policy phrase must make the value humanly derivable — via its meaning, common knowledge ("quarterly" → QTD), or the parameter's declared options — and the value must be inside those options. The level-4 rule in full: if the prompt printed the fact, reading the source would be optional and the level would be a lie.

**Rung weight — each level's new demand must actually cost something.** The pilot measured what happens otherwise. A Care world of polite, unrelated furniture doesn't bind: the decoy near-duplicate (same widget as the target, different parameter values, preservation-graded, never mentioned in the prompt) is what makes carelessness expensive — an agent that "fixes", reuses, or updates the decoy instead of placing the fresh one fails. A Compose rung that only registers one table is *lighter than its own ceremony* — models follow long structured asks more diligently than short ones, so a cheap build makes level 5 easier than level 4. The build must include publishing and instantiating an app with a named tab, so the manifest surface (widgets_json AND apps_json with layout refs) carries real failure modes. Never compensate the other way: do not pad prompts, budgets, or grading to force the staircase — weight lives in the world and the eval, not in wording tricks.

## Story shapes beyond place-and-read

- **Repair stories** (the facts block carries `seeded_wrong`): the target starts on the working dashboard **misconfigured with the seeded_wrong values**, and the ask is to restore the correct configuration (graded via `update_widget` and/or the corrected end state). The six dials apply unchanged — level 0 states the correct values, level 2's policy carries one of them, level 3 adds the decoy and preservation ("repair the target, leave everything else"), level 5 still builds. Old-suite precedent: the repair-family tasks in `task_suites/enterprise_apps_usage/`.
- **Resource- and prompt-governed rungs**: when the story's governance names a workspace resource or prompt instead of a skill, the level-4 read is `read_workspace_resource` / `get_workspace_prompt` (graded on `uri` / `name`), and the note fact must live only in that source — same describe-never-print contract. Verify the source's exact text via `src/workspace_bench/workspace/simulated_workspace.py`.
- **Form widgets**: the form param type carries no options list; grade placement and end state, and verify the widget's actual schema in the catalog before inventing any interaction with it.

## The prompt

Written last, once the eval is fixed, in the persona's voice (their README is the voice contract):

- One coherent ask a real person would send — plain verbs, no tool names, no ids, no JSON. **Start with the ask itself**: no scene-setting openers ("Quarterly briefing time:", "Audit prep —"). Context earns its place only when it carries information the model needs (e.g. "the dashboard already has the morning views on it").
- Every graded display name, origin, and stated value appears **verbatim** — they are how the agent finds and knows things. Ambiguous widget names get their app named too.
- Say **dashboard** (never "board"), **parameters** (never "settings"). No personal names — say "the PM", "the desk".

## Workflow

1. Read the persona README and the story. List the canonical facts.
2. Verify every fact against the data folder. Flag conflicts; never paper over them.
3. Write level 0 first, replay it mentally call by call, then climb the ladder — each level a copy of the previous plus its one dial.
4. After each level: certify it alone (`uv run workspace-bench validate --task-dir src/workspace_bench/task_suites/workspace_tasks --family <persona> --difficulty level<N>` — oracle passes, no-op fails), then dispatch a background task-validator subagent on that task and move to the next level.
5. Fix validator FLAG lines as they land (an unreachable value, an ambiguous target, an impossible ask, a too-tight budget) — before writing later levels if the flag reveals a pattern. Re-certify and have the validator re-check anything you change.
6. When all six are authored and validator-quiet: run the full-family certification (`--family <persona>`, no difficulty filter). Report. The orchestrator then runs the task-level-fairness check across your ladder; repair its per-level flags the same way.

## Worked example — a level 2 task, annotated

Adapted from a certified task, so every field shape is proven. The story's facts: the PM's *Pilot Decision Brief* dashboard needs *Trade Ideas* (Portfolio Command Center, Bench Stark Enterprise) for fund *Flagship Long/Short*, period *QTD*.

```json
{
  "id": "morning_briefing_level2",
  "difficulty": "level2",
  "prompt": "Prep the open Pilot Decision Brief dashboard with Trade Ideas from Bench Stark Enterprise's Portfolio Command Center for Flagship Long/Short, configured per the quarterly briefing policy.",
  "setup": {
    "workspace_baseline": "stark-workspace-a",
    "workspace_backends": ["stark-enterprise-x", "support-daloopa-skills", "getting-started", "widget-examples"],
    "workspace_skills": ["<all ten slugs>"],
    "default_selected_dashboard": "Pilot Decision Brief",
    "allowed_tools": ["<the standard twenty>"],
    "initial_state": {
      "dashboard": {
        "name": "Pilot Decision Brief",
        "tabs": [{"id": "review", "name": "Review"}],
        "widgets": []
      }
    }
  },
  "eval": {
    "required_tools": [
      {
        "tool": "list_available_widgets",
        "args": {"origin": "Bench Stark Enterprise"},
        "optional": true
      },
      {
        "tool": "create_widget",
        "args": {
          "origin": "Bench Stark Enterprise",
          "widget_id": "portfolio_command_center_actions_trade_ideas",
          "data_args": {"fund": "Flagship Long/Short", "period": "QTD"}
        },
        "graded_args": ["origin", "data_args"]
      }
    ],
    "required_widgets": [
      {
        "origin": "Bench Stark Enterprise",
        "widget_id": "portfolio_command_center_actions_trade_ideas",
        "data_args": {"fund": "Flagship Long/Short", "period": "QTD"}
      }
    ],
    "max_turns": 5
  }
}
```

Why each piece is the way it is:

- **The level-2 dial is visible in the prompt**: "the quarterly briefing policy" carries `period=QTD` — the prompt never prints QTD. Everything else the eval grades ("Trade Ideas", "Bench Stark Enterprise", "Flagship Long/Short", the dashboard) is stated verbatim, and the app name disambiguates a widget name that appears more than once in the catalogs.
- **The reference trace is an honest route, narrowly graded**: the discovery call is `"optional": true` (a competent agent might list first — allowed, not required), and `graded_args` grades only `origin` and `data_args`, so the trajectory isn't over-pinned.
- **The budget follows the rule**: 2 `required_tools` entries + 3 = `max_turns: 5`.
- **Both certifications are satisfiable by construction**: replaying the trace produces the required widget (oracle passes); an agent that does nothing leaves the dashboard empty (`required_widgets` unmet — no-op fails).
- **Every fact is data-folder-verified**: the widget id and display name from the Stark catalog, and `Flagship Long/Short` / `QTD` from that widget's declared parameter options — which is also what makes "quarterly" derivable (QTD is the only quarter option).

Once the pilot's *Morning briefing* story is certified and validated, its six committed files in `task_suites/workspace_tasks/portfolio_manager/` are the canonical reference ladder — read them before your first story.
