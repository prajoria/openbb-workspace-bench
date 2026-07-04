# WorkspaceBench v1 TODO — one benchmark, 300 scenarios, full surface coverage

Owner: Didier · Drafted: 2026-07-03 · Status: planning

## North star

Ship **workspace-bench-v1**: a single, uniformly-weighted benchmark of **300
scenarios** that measures whether an agent can operate OpenBB Workspace through
its **entire MCP surface — 18 tools, 2 prompts, and its resources** — with a
task distribution that is designed, measured, and defensible in public. No
provenance castes: every scenario is generated, certified the same way, and
carries the same weight. Splits exist for ML hygiene, not for status.

Definition of done: `workspace-bench validate --min-scenarios 300` passes with
oracle 300/300 / no-op 0/300, every tool/prompt/resource is exercised by ≥8
scenarios, no two scenarios share a novelty fingerprint, and Part 1 of the blog
presents the distribution visually with media slots for real Workspace footage.

Current state (facts, 2026-07-03): 240 scenarios across three packs
(workspace-core-v0 25 + stark-enterprise-v0 15 + workspace-gen-v0 200).
Distribution skews to fix: L1 = 125/240 (52%) vs L2 = 18 (7.5%); backends
stark 104 / equities 89 / macro 36 / portfolio 21; medium difficulty is the
smallest band (57); 66 distinct required widgets out of ~358 available; MCP
prompts and resources: **0 scenarios**.

---

## A. Code level

### A1. Unify the packs (kill the 40/200 split)

- [ ] Create one release: `workspace-bench-v1`, one manifest, one release id.
      Migrate `workspace-core-v0`, `stark-enterprise-v0`, and
      `workspace-gen-v0` scenarios into a single generated pack; retire the
      three pack names from the public story (keep them only as git history).
- [ ] Same schema, same certification, same weight for all 300. The generator
      (`scripts/generate_gen_pack.py`) becomes the single source of truth;
      the 40 formerly "hand-written" scenarios get absorbed as template
      instances (they were AI-generated too — the distinction was never real).
- [ ] Assign splits **stratified, not by provenance**: 60/20/20
      train/validation/test sampled per (family × tier) cell so every slice of
      the distribution appears in every split. Hold out whole workflows in
      test where possible to catch family shortcuts.
- [ ] Update `RELEASE_CHECKLIST.md`, `docs/benchmark-card.md`, and README
      numbers (300, one release id, split table).
- Acceptance: `workspace-bench list` shows one pack; `validate --pack all
  --min-scenarios 300` green; no doc references "40 hand-audited" anywhere.

### A2. Model MCP prompts and resources in the simulator (the missing surface)

The live server exposes `workspace_tool_usage` + `workspace_session_context`
prompts and `openbb://workspace/app-builder/index` as an MCP resource
(`EXPECTED_MCP_PROMPTS` / `EXPECTED_MCP_RESOURCES` in
`src/workspace_bench/workspace/live_mcp.py`). No scenario touches any of them.

- [ ] Add `read_workspace_resource` to `SimulatedWorkspace`: takes a resource
      URI, returns deterministic content. Back `app-builder/index` with the
      fixture app catalog; expose the 4 workspace skills additionally as
      resources (`openbb://workspace/skills/<slug>`) so the same content is
      reachable both ways, mirroring how the real server dual-publishes.
- [ ] Add `get_workspace_prompt` to the simulator returning the two prompt
      payloads with deterministic text (fixture versions of tool-usage
      guidance and session context).
- [ ] Grader support: `required_resource_reads` (URI + `data_contains`) and
      reuse `required_tool_calls` for prompt fetches. New issue codes:
      `missing_resource_read`, stable and documented.
- [ ] Live bridge mapping: in `live_mcp.py`, translate the two new tools to
      real MCP `resources/read` / `prompts/get` calls so the smoke path stays
      honest. Extend `--check-surface` to assert the skills resources too.
- [ ] Update `docs/agent-command.md` + task envelope: document the two new
      tools in `allowed_tools` vocabulary.
- Acceptance: a scenario can require "agent read the app-builder index
  resource and cited an app from it in a note", oracle passes it via the
  simulator AND via `smoke-workspace-mcp` against a live sidecar.

### A3. Grow 240 → 300 with designed diversity (no filler)

Target lattice: **15 families × 5 tiers × 4 scenarios = 300.** Keep the 10
tool-anchored families; add 5 new anchors that are currently support-only or
missing entirely:

- [ ] `params` family — anchor `get_params_options` (t0 read options → t4
      options-constrained multi-widget build).
- [ ] `backends` family — anchor `manage_backends` (list/read backends →
      cross-backend orchestration under discovery).
- [ ] `resources` family — anchor `read_workspace_resource` (t0 read index →
      t4 read index, pick an app, instantiate it, brief it). Requires A2.
- [ ] `prompts` family — anchor `get_workspace_prompt` (t0 fetch guidance →
      t4 follow the fetched session-context instructions in a build).
- [ ] `inspect` family — anchor `read_widget`/`get_workspace_snapshot`
      (currently only support tools; give ambient-state reasoning its own
      ladder: find the misconfigured widget among N without being told which).
- [ ] Rebalance the secondary axes while filling the lattice, with quotas
      enforced at generation time:
      - L2 dashboard-construction ≥ 15% of suite (currently 7.5%),
      - each fixture backend ≥ 15% (portfolio currently 9%),
      - difficulty bands within 30/40/30 ± 5 (medium currently starved),
      - ≥ 120 distinct required widgets (currently 66 of ~358),
      - every grader check type used ≥ 10× (incl. new resource checks).
- Acceptance: generator prints the 15×5 matrix (all 4s) plus the quota report;
  all quotas green.

### A4. Novelty enforcement ("every scenario brings something new")

- [ ] Define a **novelty fingerprint** per scenario:
      `(family, tier, oracle-toolset mask, check-type set, backend set,
      pathology type, artifact type)`. Parameter swaps (AAPL→MSFT) share a
      fingerprint; structural differences don't.
- [ ] Enforce at generation: max 1 scenario per fingerprint in v1 (hard
      assert in `generate_gen_pack.py` `main()`), so 300 scenarios = 300
      distinct structural situations. Where today's pack has 3–4 param-swap
      siblings, replace the siblings with new structures instead of dropping
      count.
- [ ] Add a `novelty` one-liner field to scenario JSON ("what this test adds
      that no other test does") — generated from the fingerprint diff, shown
      in the blog matrix detail and `docs/scenario-catalog.md`.
- [ ] Extend `workspace-bench validate` with a `fingerprint_unique` release
      check so regressions fail CI.
- Acceptance: `validate` reports 300 unique fingerprints; catalog shows a
  novelty line per scenario.

### A5. Certification & measurement (unchanged gates, new evidence)

- [ ] Re-certify: oracle 300/300 pass, no-op 300/300 fail.
- [ ] Regenerate `docs/scenario-catalog.md`, `docs/tool-coverage-matrix.md`,
      `docs/tool-matrix-data.json` (now 300 rows + prompts/resources columns
      → 20 columns).
- [ ] Empirical tier calibration run: `compare-models --scenario-dir <v1>`
      with gpt-oss:20b (free, local), 3 repeats — verify measured pass rates
      fall monotonically t0→t4 and produce the per-tier pass-rate chart the
      blog needs. Re-tier any family whose ladder inverts.
- [ ] Repeat the Stark-equivalent slice with GPT-4.1, 3 repeats, so the blog's
      strongest claim stops resting on a single repeat.
- Acceptance: a `runs/comparison/<id>` directory with per-tier pass rates for
  both models; monotonic or explained.

### A6. Repo hygiene for outside users (it's a public benchmark now)

- [ ] Decide + publish the public repo URL (blog has a TODO comment waiting).
- [ ] Media pipeline: `docs/media/` with a manifest (`media.json`: slot id →
      filename, caption, which tool/resource it demonstrates) so blog
      placeholders resolve by id. Record real Workspace screen captures per
      tool family (see B3 list).
- [ ] CI: add `validate --min-scenarios 300` + fingerprint check + pytest to
      the GitHub workflow; fail on any quota regression.
- [ ] Baseline docs: one page "evaluate your agent in 10 minutes" (exists in
      README — verify all commands against v1 names).

---

## B. Blog level (Part 1)

### B1. Unify the numbers and the story

- [ ] Stats table: one headline — **300 scenarios, one release, all generated,
      all certified** — kill the "40 hand-audited + 200 generated" row.
      Splits shown as a stratification detail, not a hierarchy.
- [ ] Generation section copy: reframe from "hand-written eval + generated
      train" to "one generated, certified distribution; splits are sampled,
      not blessed". Keep the TMax framing.
- [ ] Update every count that changes (families 10→15, tools 18→18+2+N
      resources, tier ladder examples, escalation averages).

### B2. An "MCP surface reference" section — every tool AND resource

- [ ] New section after the eval-loop: a compact reference of the full
      surface: 18 tools + 2 prompts + resources. For each: one-line "what it
      does", scenario count exercising it (live from matrix data), and a
      link/scroll to a media slot showing it used in the real Workspace.
      Format: the same minimal mono table (name · role · #tests · media) —
      interactive: click a row → description + its media placeholder +
      example scenario ids.
- [ ] Resources get equal billing to tools — including a sentence on why
      resource-reading is part of workspace competence (agents that ignore
      the app-builder index rebuild dashboards from scratch).

### B3. Make it visual (replace prose with graphs; add media slots)

- [ ] **Distribution dashboard figure** (one panel, monochrome bars): four
      small-multiple histograms — scenarios by level, by tier, by backend, by
      difficulty — rendered from embedded data, replacing the current prose
      recitation of counts.
- [ ] **Coverage heatmap**: families × tiers with avg-tools-per-episode as
      cell intensity — the 2.1→4.6 escalation as a picture instead of a
      sentence.
- [ ] **Per-tier pass-rate chart** (needs A5 calibration run): measured
      difficulty monotonicity — the money chart for "tiers are structural".
- [ ] **Media placeholders**: a styled `figure.media-slot` component (dashed
      border, uppercase caption, slot id) at these points minimum:
      1. hero: 30s video, agent building the earnings dashboard end-to-end;
      2. durable-artifact section: screenshot of the real graded dashboard;
      3. one per tool-family row in the MCP reference (18+ slots, short
         clips: create_widget firing, delete removing a duplicate, app
         instantiation, resource read in the client…);
      4. failure section: clip of the hallucinated `container.exec` moment.
      Each slot renders its caption + "media pending" until `docs/media/`
      provides the asset (resolved via media.json id).
- [ ] Trim prose: target ≤ 60% of current word count in the generation and
      results sections once the graphs land (graphs carry the numbers; text
      carries the argument).

### B4. Publish checklist (Part 1 → series)

- [ ] Fill the repo URL (removes the HTML TODO comment).
- [ ] Byline/date/canonical URL per didierlopes.com conventions; port to
      Docusaurus MDX (fonts already on-site; strip the Google Fonts link).
- [ ] Restyle Parts 2 and 3 into the same mono design system (they still wear
      the old cream/green style).
- [ ] Part 2 experiments (E1–E3 tool-surface A/Bs) get run for real before
      Part 2 ships — its "results pending" badges must resolve.
- [ ] Cross-check every number in all three posts against the v1 catalog and
      the calibration runs (no stale 240/40/200 references anywhere).

---

## Sequencing (dependency order)

1. A2 (simulator prompts/resources) — unblocks A3's new families.
2. A3 + A4 together (regenerate 300 with quotas + fingerprints).
3. A1 (unify packs/splits) once the 300 exist.
4. A5 (certify + calibrate) — produces the blog's charts.
5. A6 media recording (parallel with 4).
6. B1–B3 blog rebuild from the new data; B4 publish gate.

Estimated effort: A2 ~1 day; A3+A4 ~2 days; A1 ~half day; A5 ~half day compute
+ review; media ~1 day of recording; blog ~1 day. ~1 week of focused work to a
publishable v1.

---

## Post-implementation status & v1.1 queue (2026-07-04)

Code-level A1–A4 and A5-docs are DONE (codex --yolo run, gates re-verified):
one bundled `workspace-bench-v1`, 300 scenarios, 15 families × t0–t4, quotas +
fingerprints in CI, resources/prompts modeled end-to-end. Media slots trimmed
from 23 to 6 shared clips by decision (per-tool clips were overkill).

In flight:
- [ ] A5 calibration: gpt-oss:20b over all 300 (1 repeat), running in
      `runs/comparison/v1-calibration-gptoss20b` — produces the per-tier
      pass-rate chart for the blog. GPT-4.1 frontier line: pending approval
      (API spend).

Promoted into v1 (in flight):
- [ ] Prompt phrasing pools — codex implementing now: >=3 deterministic
      phrasings per template site, selected by stable hash of scenario id,
      semantics/oracles/fingerprints unchanged, full re-certification.
      Calibration restarts only after this lands (measure the final artifact).
- [ ] Calibration protocol locked: three-point — gpt-oss:20b (floor, free),
      gpt-4.1-mini (GATING model: tier bands defined against it, ~$10-15 for
      300 episodes, needs approval), GPT-4.1 (frontier ceiling, subset ok).

v1.1 queue (deliberately deferred, none block blog post 1):
- [ ] Held-out-family split variant: add `--split-strategy family-heldout` for
      training users (blog carries the honest caveat meanwhile).
- [ ] Stark data layer upgrade (keep the catalog — 349 widgets/23 apps of
      realistic structure is the asset; the DATA behind them is the weak
      part): replace the id-derived value formula and the one-shape-fits-all
      3-row payload with type-appropriate seeded synthetic tables baked into
      stark_enterprise.json at build time — tables get 5-10 domain-plausible
      rows, metrics get value+change, charts get series, markdown gets prose;
      values from a seeded RNG (not derivable from the id), plausible ranges
      (negative VaR, weights summing to ~1). Kills the memorize-the-hash
      backdoor AND makes data-reading tasks test real schema diversity.
      Requires regenerating value-citing scenarios + re-certify. Never live
      data (determinism + canary).
- [ ] Ambiguity axis: realistic messy phrasing (typos, implicit constraints,
      conflicting wording) as a tagged scenario property.
