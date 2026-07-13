# Task-Suite Quality Report

Date: 2026-07-13. Author: the benchmark's orchestrating agent, after the
five-suite restructure and the answer-judge calibration. Every claim below is
backed by an artifact in this repository or a run performed on 2026-07-12/13.
Verification model: local `ollama gpt-oss:20b` only (no hosted models were
used while testing). All certification gates were green at writing time:
256 tests, five suite validations (637/637 oracle-pass / noop-fail), three
audits at zero findings.

## How to read the confidence grades

- **A** — I would publish results on this suite today.
- **B** — sound construction, but one named piece of evidence is still
  missing before I would publish.
- **C** — experimental; useful signal, not a claim.

---

## smoke — 20 tasks · confidence A−

**Created:** `ai-authored-direct`. Every task written directly in
`scripts/generators/generate_smoke_suite.py`, one per Workspace MCP
tool/surface, certified in-process (oracle passes, no-op fails, ≤4 graded
checks each) on the default-workspace-v1 baseline.

**Quality evidence.** 17/20 tasks are live-parity-eligible by construction
(the three exclusions — manage_backends, manage_apps, assign_tasks_to_agents
— are inherently non-replayable against a production workspace); a live
spot-check fully agreed 3/3 with clean teardown against the real hosted
bridge. A gpt-oss:20b verification run scored 8/20, which exposed a real
design flaw — prompts named widgets colloquially ("the Stark Alert Trend
widget") while checks demanded verbatim identifiers, forcing identifier
guessing. All 20 prompts were rewritten to carry exact identifiers (a smoke
test measures the pipe, not discovery), and the rerun scored **17/20**, with
the three residues being ordinary small-model slips on fully-specified asks.

**Caveats.** Reads are graded by trace (required call + args) rather than
state, because reads leave no state; this is the only suite where that is
accepted, and its README says so. A frontier model should be ~20/20; that
expectation is falsifiable and worth checking on the first paid run.

## enterprise-apps-default — 69 tasks · confidence B+

**Created:** `product-verbatim-prompts + reviewed-derived-rubrics + judged
exemplars`. One task per bundled product prompt of each of the 23 enterprise
apps — prompts byte-verbatim, never edited (enforced by the generator's
certifier). Grading is two-key: (1) deterministic grounding — the note
artifact must contain exact fact values from the app's served data — and
(2) a binary LLM judge verdict on whether the right data was consulted (the
judge sees the full trace), the reasoning fits the ask, and the question was
answered. Rubric widget/anchor derivation was reviewed per prompt (56
overrides), and every oracle exemplar answer was iterated against the judge
until it passed.

**Quality evidence.** Judge calibration against pinned `gpt-oss:20b`
(template `workspace-bench-answer-judge/v2`, sha recorded per verdict): the
full sweep ran 69 exemplars plus three mutant classes per task (shallow
fact-stub, off-topic, prompt-injection). Mutants fail 100%, including the
injection attack. After a boundary-hardening round, **all 69 exemplars pass,
with every reworked case verified at three repeats**. The judge repeatedly
demonstrated real discrimination: it rejected fact-stub answers, silently
incomplete multi-part answers, claims about data outside its context, and a
fabricated-funds briefing from the verification model — that last one was
independently rejected by both keys, which is the design working. The
gpt-oss verification subset scored 0/3 honestly (it fabricated funds and
missed graded facts).

**Caveats — why not A.** (1) Difficulty labels are placeholders ("medium")
pending measured runs; the suite has never been calibrated against a model
gate the way the build suite was. (2) The judge is a grader with a pinned
model dependency: cross-judge agreement and a human audit of early
transcripts are still unmeasured. (3) Exemplars may only cite figures
visible in the judge's fund-filtered data previews — a fair constraint (the
evaluated model faces the same context) but one that narrows what "complete"
means. (4) Three prompts are answerable only with explicit
data-cannot-show hedges; the judge accepts those, and the README records them.

## enterprise-apps-usage — 300 tasks · confidence A

**Created:** `template-scaled-from-basis`. Fifteen tool-anchored families ×
five rungs × four tasks, scaled by `scripts/generators/generate_usage_suite.py`
from per-family bases; renamed from `core` in this restructure. Gates:
suite-wide quotas (families, difficulty distribution, distinct widget pairs,
per-check coverage floors), in-process certification, and the adversarial
mutation matrix (zero survivors across all families at last full run).

**Quality evidence.** This is the most battle-tested suite: six published
model boards were run on its predecessor; five simulator-fidelity defects
found by live-parity testing (widget-id echo, dashboard_id contract,
data_args create/update asymmetry, tab-id stability, grid compaction) were
fixed at the simulator and generator level with all 300 tasks re-certified.
54 tasks are live-parity-eligible today; the last full sweep had **zero
structural disagreements** against the real product. The gpt-oss
verification subset (read family, 20 tasks) scored 12/20 — consistent with
that model's historical ~70% on this suite, i.e. the difficulty transfer
survived the restructure.

**Caveats.** Boards from before the schema slim-down and baseline work are
historical and not comparable; fresh boards are needed. Bench Equities /
Macro / Portfolio families still run on invented fixture catalogs rather
than transcriptions (the Stark and reference-repo families are
transcription-grade).

## build-openbb-apps — 236 tasks · confidence A−

**Created:** `agent-authored-certified`. Family modules authored by agents
against the real widgets.json/apps.json contract (transcribed from the
product's zod validation), never scaled; certified in-process with check
caps, quota-enforced type/param ownership, and a long documented calibration
history (thirteen gating rounds; five task-defect classes caught by
multi-model sweeps; strictly-decreasing official gate curve on the previous
schema).

**Quality evidence.** 236/236 certify; the adversarial matrix and release
audits pass; prompt distribution quotas (60/92/84 specification levels)
hold. The gpt-oss verification subset (4 easy tasks) scored 0/4 with
coherent, domain-specific failure codes (schema-before-create discipline,
def mismatches, capability coverage) — the pipeline works; the model is
simply weak under the hardened grading, and n=4 is anecdote, not signal.

**Caveats.** The hardening pass restored workflow-discipline gates whose
score impact against the prior outcome-only interlude is unmeasured — the
next full board defines the new baseline. Its live-parity story (authoring
against the real backend registry) does not exist yet; the live surface
cannot replay manage_backends.

## build-openbb-backends — 12 tasks · confidence C (by design)

**Created:** `agent-authored-certified`, experimental v0 real-code track:
pinned FastAPI starter repos, graded by launching the agent's own server
with typed probes; oracle overlays and starter tests certified (starters
fail before implementation, oracle green, garbage-server rejection).

**Quality evidence.** 12/12 certify and the code-track tests pass. No model
has ever been run through it in this cycle, it executes agent code without a
security sandbox, and it is excluded from the MCP tool matrix on purpose.
Treat any number from it as exploratory.

---

## Cross-suite infrastructure the grades rest on

- **default-workspace-v1**: versioned, hashed baseline (Home + all 23
  enterprise apps instantiated; stark-enterprise, daloopa, getting-started,
  widget-examples backends connected) applied via suite manifests; smoke and
  enterprise-apps-default run on it, usage/build remain minimal-baseline as
  a documented ablation axis.
- **Live-shape agent snapshot**: the model-visible snapshot matches the
  hosted server (dashboard summaries + active composition only), verified
  against the production bridge.
- **Judge infrastructure**: pluggable OpenAI-compatible judge, pinned model +
  template sha recorded per verdict, verdicts cached in result rows (replay
  never re-calls a model), CI deterministic-only, judge calibration as a
  local release gate.
- **Provenance READMEs**: every suite carries a same-skeleton README whose
  task counts are enforced by the release-consistency audit.

## Addendum: gpt-4.1-mini spot test (2026-07-13, post-report)

A small paid-model probe (full smoke, six judged enterprise-apps-default
tasks) ran after the report above. It caught five defects no oracle run
could, each fixed and re-verified:

1. Smoke prompts withheld exact identifiers while checks demanded them —
   all 20 prompts now carry identifiers verbatim (mini: 8/20 → 18/20).
2. The read_widget check required an `origin` argument the tool does not
   need — relaxed (mini then passed it).
3. The assign_tasks_to_agents check contradicted the tool's own documented
   `description` field, and exposed that the args matcher compares lists by
   exact equality — the check now proves the round trip without a fragile
   nested list (mini then passed it; smoke is now effectively 20/20 for
   mini).
4. Product prompts read as chat asks, so models answered in chat instead of
   a durable note — judged tasks now carry a completion rule in the
   recency position of every turn (documented harness assistance).
5. **The interactive parser silently discarded a final tool call sent
   together with `{"done": true}`** — a pattern mini uses consistently, so
   its finished notes never executed. Fixed in the parser and loop; this
   affects every suite and every model that ends episodes this way.

With the pipeline fixed, mini scored 0/6 on the judged tasks with
substantive verdicts on real notes: fabricated funds and figures not
present in the served data, a claimed "escalated" status where the data
says "Open", and omitted ask components — independently confirmed by the
deterministic fact key. That is a genuine capability signal, not harness
noise: the suite is hard but honest, and the fabrication failure mode is
exactly what the two-key design exists to catch. The open question for the
full mini gate remains where stronger models land.

## What I would do next, in order

1. A real gpt-4.1-mini gate run on smoke + enterprise-apps-default (89
   tasks) to measure difficulty and set the first judged board.
2. Cross-judge agreement (a second open-weight judge on the same 69
   exemplars + mutants) and a ~50-episode human audit of judge verdicts.
3. Migrate usage/build onto default-workspace-v1 and re-certify (the
   distractor-sensitivity comparison is a publishable result on its own).
4. Retire the invented Bench fixtures in favor of transcription-grade
   catalogs, extending live-parity eligibility beyond Stark.
