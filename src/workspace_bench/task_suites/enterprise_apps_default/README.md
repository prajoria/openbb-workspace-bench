# `enterprise-apps-default` task suite

Tasks: 138

## Purpose

These tasks measure whether an agent can answer each bundled enterprise-app
product prompt from the active dashboard and deliver a data-grounded reply.

## Two data worlds

Each of the 69 product prompts appears twice with identical wording and
reference read calls. The matching `_x` and `_y` ids run on
`stark-enterprise-x` and `stark-enterprise-y`, respectively. Both backends
expose the same apps, widgets, parameters, and display name, while their served
rows differ in entities, values, and row counts. Each task selects
`all-stark-enterprise-apps`, its data world, and its starting dashboard in
`setup`.

## Tools and turns

Every task exposes all 20 canonical Workspace tools in canonical order, plus
the harness-level `final_answer` action appended last in `allowed_tools`. That
action delivers the reply and completes the episode; subsequent calls are
refused. It does not create a note widget. The turn budget is the number of
calls in that task's reference plus two. Agents see only the prompt and the
setup block: grading criteria, the reference trajectory, and the turn budget
live in the sealed `eval` block and are never exported — the harness enforces
the budget and refuses calls past it.

## Provenance

Prompts remain byte-verbatim from the Stark product catalog. Read paths for
each product prompt were selected and reviewed during the July exemplar round
over the app catalogs. Each reference trace consists of a workspace snapshot,
the reviewed `get_widget_data` reads only; the reply lives in
`reference_answer`, and the reference replay synthesizes its `final_answer`
submission from that field. Matching X/Y
pairs share identical reads and differ only in the data world serving those
reads.

Each of the 138 reference answers was written by gpt-5.6sol via codex from that
task's prompt and the exact rows returned by its reference reads in its data
world. Generation machine-certifies numeric groundedness: every cited figure
must appear literally in those served rows. Category `read` and difficulty
`medium` are declared once in the suite manifest; family is derived from each
task directory.

## Grading

`judge.md` compares an agent's retrieved data and reply with one
known-good reference trajectory for the same prompt and data world. The judge
accepts other valid analyses when their reads, figures, and conclusions support
the ask.

The deterministic grader requires a submitted `final_answer` in the trace.
This `missing_final_answer` gate makes a no-op fail and the reference pass even
when no judge is configured. Generation certifies reference success, no-op
failure, product-verbatim prompts, unique ids, identical X/Y read calls,
different X/Y reference-answer text for every pair, reference-answer equality
with the final reply, and numeric groundedness.

## Limitations

Fixture data makes replay deterministic but does not establish live-data or
browser parity. The uniform medium label is not an empirically calibrated
difficulty measurement.
