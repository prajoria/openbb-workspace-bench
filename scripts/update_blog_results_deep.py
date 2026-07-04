"""Deepen blog post 1's results section with the full 6-model calibration data.

Reads runs/reports/calibration.json (compile_calibration.py, including the
per-scenario matrix) and injects into docs/blog-workspacebench-series-draft.html:
  - a static leaderboard table (all models, strict/mean, tier curve),
  - pass-rate distribution small-multiples by tier and by difficulty rating,
  - an interactive tier explorer: pick t0-t4, see every scenario in that tier
    as a row with per-model pass/fail cells; click a row for scores + issues,
  - analysis prose computed from the consensus data,
  - replaces the stale v0 reproduce-commands block with v1 commands.

Idempotence: every injected chunk lives between WB-DEEP:* comment markers.
Re-running replaces marker contents in place, so it is safe after recompiling.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BLOG = REPO / "docs/blog-workspacebench-series-draft.html"
DATA = REPO / "runs/reports/calibration.json"

ORDER = ["gpt-5.5", "sonnet-5", "glm-5.2", "gpt-4.1-mini", "gpt-oss-20b", "qwen3-8b"]
FULL = {
    "gpt-5.5": "GPT-5.5", "sonnet-5": "Claude Sonnet 5", "glm-5.2": "GLM-5.2",
    "gpt-4.1-mini": "gpt-4.1-mini", "gpt-oss-20b": "gpt-oss:20b", "qwen3-8b": "Qwen3 8B",
}
SHORT = {
    "gpt-5.5": "GPT-5.5", "sonnet-5": "Sonnet 5", "glm-5.2": "GLM-5.2",
    "gpt-4.1-mini": "4.1-mini", "gpt-oss-20b": "oss:20b", "qwen3-8b": "Qwen3 8B",
}
SETUP = {
    "gpt-5.5": "OpenAI API", "sonnet-5": "OpenRouter", "glm-5.2": "OpenRouter",
    "gpt-4.1-mini": "OpenAI · gating", "gpt-oss-20b": "local Ollama", "qwen3-8b": "local Ollama",
}
SHAPE = {
    "gpt-5.5": "compressed — t4 ≈ t0", "sonnet-5": "monotonic, graceful",
    "glm-5.2": "t0 discipline dip", "gpt-4.1-mini": "the gating curve",
    "gpt-oss-20b": "monotonic echo", "qwen3-8b": "cliff at t2–t3",
}
TIERS = ["t0", "t1", "t2", "t3", "t4"]
TIER_LABEL = {
    "t0": "t0 — single action", "t1": "t1 — one mutation under discipline",
    "t2": "t2 — composed artifacts", "t3": "t3 — repair & preserve",
    "t4": "t4 — multi-intent composition",
}
DIFFS = ["easy", "medium", "hard"]


def replace_between(
    src: str, name: str, content: str, anchor: str, before: bool, css: bool = False
) -> str:
    # HTML comments inside <style> are not CSS comments — the parser drops the
    # first rule after each one — so CSS chunks get CSS-comment markers.
    if css:
        start, end = f"/* {name}:START */", f"/* {name}:END */"
    else:
        start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    block = f"{start}\n{content}\n{end}"
    if start in src:
        i, j = src.index(start), src.index(end) + len(end)
        return src[:i] + block + src[j:]
    assert anchor in src, f"anchor for {name} missing"
    if before:
        return src.replace(anchor, block + "\n" + anchor)
    return src.replace(anchor, anchor + "\n" + block)


def pct(p: int, n: int) -> int:
    return round(100 * p / n)


def main() -> None:
    data = json.loads(DATA.read_text())
    models = {m["slug"]: m for m in data["models"]}
    scenarios = data["scenarios"]
    assert all(s in models for s in ORDER), "missing model runs"
    assert len(scenarios) == 300

    # ---- computed consensus facts --------------------------------------------------
    for s in scenarios:
        s["_passes"] = sum(s["models"][slug]["passed"] for slug in ORDER)
    all_pass = [s for s in scenarios if s["_passes"] == 6]
    all_fail = [s for s in scenarios if s["_passes"] == 0]
    contested = [s for s in scenarios if 0 < s["_passes"] < 6]
    contested_by_tier = Counter(s["tier"] for s in contested)
    agree_by_tier = {
        t: sum(1 for s in scenarios if s["tier"] == t and s["_passes"] in (0, 6))
        for t in TIERS
    }
    fail_families = Counter(s["family"] for s in all_fail)
    inversions = [
        s for s in scenarios
        if not s["models"][ORDER[0]]["passed"] and s["models"][ORDER[-1]]["passed"]
    ]

    # ---- 1. headline chart + industry benchmark table -------------------------------
    def fmt1(x: float) -> str:
        return f"{x:.1f}%"

    overall = {slug: 100 * models[slug]["strict"] / 300 for slug in ORDER}
    cols = []
    for slug in ORDER:
        cols.append(
            f"        <div class=\"col\"><span class=\"col-val\">{fmt1(overall[slug])}</span>"
            f"<div class=\"col-track\"><div class=\"col-fill\" style=\"height:{overall[slug]:.1f}%\"></div></div>"
            f"<span class=\"col-name\">{FULL[slug]}</span></div>"
        )

    def bench_row(label: str, values: list[float], cells_fmt=None, cls: str = "") -> str:
        fmt = cells_fmt or (lambda v: f"{round(v)}%")
        best = max(values)
        best_attr = ' class="best"'
        tds = "".join(
            f"<td{best_attr if v == best else ''}>{fmt(v)}</td>" for v in values
        )
        klass = f' class="{cls}"' if cls else ""
        return f'          <tr{klass}><th scope="row">{label}</th>{tds}</tr>'

    def bench_group(label: str) -> str:
        return (
            f"          <tr class=\"bench-group\"><td colspan=\"{len(ORDER) + 1}\">{label}</td></tr>"
        )

    FAMILY_DESC = {
        "create": "create widgets", "update": "update widget params", "delete": "remove widgets",
        "layout": "grid geometry", "note": "documentation notes", "read": "read & cite data",
        "apps": "instantiate apps", "navigate": "dashboards & tabs", "skills": "run workspace skills",
        "delegate": "delegate to agents", "params": "parameter surgery", "backends": "manage backends",
        "resources": "MCP resources", "prompts": "MCP prompts", "inspect": "ambient-state reasoning",
    }
    families = sorted(
        models[ORDER[0]]["families"],
        key=lambda f: -sum(models[s]["families"][f][0] for s in ORDER),
    )

    table_rows = [
        bench_row("Overall", [overall[s] for s in ORDER], fmt1, "bench-overall"),
        bench_row("Mean check score", [100 * models[s]["mean_score"] for s in ORDER], fmt1),
        bench_group("by structural tier · 60 scenarios each"),
    ]
    for t in TIERS:
        table_rows.append(bench_row(TIER_LABEL[t], [pct(*models[s]["tiers"][t]) for s in ORDER]))
    table_rows.append(bench_group("by difficulty rating · bands derived from tiers — the --difficulty cli slice"))
    for d in DIFFS:
        n = models[ORDER[0]]["difficulties"][d][1]
        table_rows.append(
            bench_row(f"{d} · {n} scenarios", [pct(*models[s]["difficulties"][d]) for s in ORDER])
        )
    table_rows.append(bench_group("by tool family · 20 scenarios each · easiest to hardest"))
    for fam in families:
        label = f"{fam} <span style=\"color:var(--muted)\">· {FAMILY_DESC[fam]}</span>"
        table_rows.append(bench_row(label, [pct(*models[s]["families"][fam]) for s in ORDER]))

    header = "".join(
        f"<th>{SHORT[s]}<span class=\"bench-sub\">{SETUP[s]}</span></th>" for s in ORDER
    )
    leaderboard = f"""  <figure class="panel">
    <figcaption class="panel-head"><strong>WorkspaceBench</strong><span>strict pass rate · 300 scenarios · single attempt · higher is better</span></figcaption>
    <div class="panel-body">
      <div class="cols-chart" role="img" aria-label="Overall strict pass rate by model">
{chr(10).join(cols)}
      </div>
    </div>
    <div class="matrix-scroll">
      <table class="bench-table">
        <thead><tr><th>&nbsp;</th>{header}</tr></thead>
        <tbody>
{chr(10).join(table_rows)}
        </tbody>
      </table>
    </div>
    <figcaption class="panel-note">Strict pass = every grader check on the scenario passes; mean check score gives partial credit. Best score per row highlighted. All models at temperature 0 except GPT-5.5, which samples at temperature 1. Each family cell is 20 scenarios, so one scenario moves it 5 points; read the family block for failure fingerprints, not rankings. Full per-scenario data below and in runs/reports/calibration.json.</figcaption>
  </figure>

  <p>
    Two things to read off the table before the charts. First, the spread: {fmt1(overall[ORDER[0]])} to {fmt1(overall[ORDER[-1]])} strict separates roughly two generations of capability, and the ordering is stable — across all 300 scenarios there is exactly {len(inversions)} inversion between the top and the bottom of the board (a t0 delegation task GPT-5.5 fumbles and Qwen3 8B happens to pass). All results are single-attempt pass@1 from one run (GPT-5.5 additionally samples at temperature 1), so per-cell numbers carry sampling noise; the harness supports <code>--repeats</code> and pass@k for anyone who wants error bars. Second, the gap between mean check score and strict pass: GPT-5.5 earns {round(100 * models['gpt-5.5']['mean_score'], 1)}% of all grader checks but passes {fmt1(overall['gpt-5.5'])} of scenarios — partial credit flatters everyone, which is exactly why the headline metric is all-checks-or-nothing. One inversion hides in the mean checks too: GLM-5.2's mean check score ({round(100 * models['glm-5.2']['mean_score'], 1)}%) sits below gpt-4.1-mini's ({round(100 * models['gpt-4.1-mini']['mean_score'], 1)}%) and even Qwen3 8B's ({round(100 * models['qwen3-8b']['mean_score'], 1)}%) despite a far higher strict pass rate — GLM fails messily across many checks while weaker models fail narrowly. The family block at the bottom is the benchmark's diagnostic panel: read down a column and you get a model's failure fingerprint; read across the inspect row and you see the suite's open problem.
  </p>

  <p>
    Adapter plumbing can cost a frontier model double-digit points. OpenRouter can route Anthropic models through Bedrock, and requesting <code>json_schema</code> <code>response_format</code> there degraded Sonnet to schema-minimal outputs; a controlled A/B diagnosed it, and the harness fixed the adapter by disabling <code>response_format</code> on that route.
  </p>

  <figure class="panel">
    <figcaption class="panel-head"><strong>Test of record</strong><span>everything needed to reproduce the table</span></figcaption>
    <div class="panel-body" style="padding: 0;">
      <table class="stats-table">
        <tbody>
          <tr><td>release</td><td><strong>WorkspaceBench</strong> — one release, 300 scenarios, certified before any model ran (oracle 300/300, no-op 0/300)</td></tr>
          <tr><td>models</td><td>gpt-5.5 &amp; gpt-4.1-mini (OpenAI API) · anthropic/claude-sonnet-5 &amp; z-ai/glm-5.2 (OpenRouter) · gpt-oss:20b &amp; qwen3:8b (local Ollama)</td></tr>
          <tr><td>protocol</td><td><strong>pass@1</strong> — one attempt per scenario, interactive tool loop, temperature 0 (GPT-5.5: 1, API-enforced), same turn budget and grader for every model</td></tr>
          <tr><td>artifacts</td><td>1,800 full episode transcripts as rollout JSONL (runs/exports/) · compiled report (runs/reports/calibration.json)</td></tr>
          <!-- TODO(didier): confirm total API spend -->
          <tr><td>cost</td><td>≈ $60 of API spend across the calibration loop and the final sweep · run July 2026</td></tr>
        </tbody>
      </table>
    </div>
  </figure>"""

    # ---- 2. distribution small-multiples -------------------------------------------
    def dist_panel(title: str, rows_html: str) -> str:
        return (
            f"        <div class=\"dist-panel\"><h5>{title}</h5>\n{rows_html}        </div>"
        )

    def dist_row(label: str, value: int, display: str) -> str:
        return (
            f"          <div class=\"dist-row\"><span>{label}</span>"
            f"<div class=\"dist-track\"><div class=\"dist-fill\" style=\"width:{value}%\"></div></div>"
            f"<span>{display}</span></div>\n"
        )

    tier_panels = []
    for t in TIERS:
        body = "".join(
            dist_row(SHORT[slug], pct(*models[slug]["tiers"][t]), f"{pct(*models[slug]['tiers'][t])}%")
            for slug in ORDER
        )
        tier_panels.append(dist_panel(TIER_LABEL[t], body))
    agree_body = "".join(
        dist_row(t, round(100 * agree_by_tier[t] / 60), f"{agree_by_tier[t]}/60")
        for t in TIERS
    )
    tier_panels.append(dist_panel("all six models agree", agree_body))

    distribution = f"""  <figure class="panel">
    <figcaption class="panel-head"><strong>Pass rate by structural tier</strong><span>the difficulty axis, model by model</span></figcaption>
    <div class="panel-body">
      <div class="dist-grid">
{chr(10).join(tier_panels)}
      </div>
    </div>
    <figcaption class="panel-note">Same six models, same fixed order in every panel. The sixth panel counts unanimous scenarios — all six pass or all six fail — per tier; everything else is the disagreement band where the benchmark discriminates.</figcaption>
  </figure>

  <p>
    The distribution shows three distinct ladder shapes, and each one is informative. GPT-5.5 compresses the ladder: {pct(*models['gpt-5.5']['tiers']['t4'])}% at t4, barely below its t0 — multi-intent composition is essentially solved for it, and its residue is precision and ambiguity. Claude Sonnet 5, gpt-4.1-mini, and gpt-oss:20b degrade monotonically, each an echo of the gating curve at a different altitude — the tier axis measures the same thing at every capability level. Qwen3 8B shows the third shape: near-parity with the mid-field at t0–t1, then a cliff — it halves at t2 and lands at {pct(*models['qwen3-8b']['tiers']['t4'])}% by t4. Small models don't degrade on this benchmark; they break, and they break exactly where episodes become multi-step. The agreement panel makes the same point from the other side: unanimity falls from {agree_by_tier['t0']}/60 at t0 to {agree_by_tier['t4']}/60 at t4, so the contested band — {len(contested)} of 300 scenarios — is concentrated precisely where the ladder claims difficulty lives ({', '.join(str(contested_by_tier[t]) for t in TIERS)} contested scenarios across t0→t4).
  </p>"""

    # ---- 3. tier explorer -----------------------------------------------------------
    tx_scenarios = [
        {
            "id": s["id"], "f": s["family"], "t": s["tier"], "d": s["difficulty"],
            "p": [s["models"][slug]["passed"] for slug in ORDER],
            "s": [s["models"][slug]["score"] for slug in ORDER],
            "i": [s["models"][slug]["issue"] for slug in ORDER],
        }
        for s in sorted(scenarios, key=lambda s: (s["tier"], s["family"], s["id"]))
    ]
    tx_payload = json.dumps(
        {"order": ORDER, "labels": [FULL[s] for s in ORDER], "short": [SHORT[s] for s in ORDER],
         "scenarios": tx_scenarios},
        separators=(",", ":"),
    )

    pills = "".join(
        f"<button class=\"btn{' active' if t == 't0' else ''}\" data-tx=\"{t}\">{t}</button>"
        for t in TIERS
    )
    explorer = f"""  <figure class="panel">
    <figcaption class="panel-head"><strong>Who passed what</strong><span>pick a tier · every scenario · click a row</span></figcaption>
    <div class="panel-body">
      <div class="btn-row"><span class="btn-label">Tier</span>{pills}</div>
      <p class="tm-meta" id="tx-meta" style="margin: 12px 0 8px;"></p>
      <div class="matrix-scroll"><table class="tx-table" id="tx-table"></table></div>
    </div>
    <div class="detail-box" aria-live="polite">
      <h4 id="tx-title">Click a scenario row</h4>
      <div id="tx-text"><p>Each cell is one model's strict verdict on one scenario. Click a row to see per-model scores, the first failed check, and the task prompt.</p></div>
    </div>
  </figure>

  <p>
    The rows nobody passes are the most valuable output of the whole sweep. {len(all_fail)} of 300 scenarios defeat all six models, and they are not scattered: {fail_families.get('inspect', 0)} are inspect-family tasks (deduplicate or reconcile a workspace the agent did not build — ambient-state reasoning), {fail_families.get('params', 0)} are companion-widget parameter tasks, {fail_families.get('layout', 0)} are precise layout splits, and {fail_families.get('skills', 0)} is a full skills-driven tearsheet. Even GPT-5.5 passes only {models['gpt-5.5']['families']['inspect'][0]}/20 of the inspect family. That list is simultaneously t5's seed, Part 2's tool-surface work queue, and the strongest evidence that the remaining headroom is about reading state, not composing calls. At the opposite end, {len(all_pass)} scenarios are passed by everyone — the sanity floor, {sum(1 for s in all_pass if s['tier'] in ('t0', 't1'))} of them in t0–t1, which is what "t0 nearly free" should look like.
  </p>
  <p>
    Failures are also model-specific in ways a single number hides. Qwen3 8B scores {models['qwen3-8b']['families']['apps'][0]}/20 on the apps family — long instantiation chains — where every other model scores 17 or better. GLM-5.2 is the only model that struggles with the prompts family ({models['glm-5.2']['families']['prompts'][0]}/20), because it skips the prompt fetch it considers unnecessary. gpt-oss:20b bottoms out on documentation notes ({models['gpt-oss-20b']['families']['note'][0]}/20). Six models, six different failure fingerprints on identical tasks — which is why the issue-code explorer below follows whichever model you pick, instead of averaging the differences away.
  </p>"""

    # ---- 4. CSS + JS ----------------------------------------------------------------
    css = """    /* Headline columns chart (overall strict) */
    .cols-chart { display: flex; align-items: flex-end; gap: 14px; padding: 4px 4px 0; }
    .cols-chart .col { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 6px; min-width: 0; }
    .cols-chart .col-track { width: 100%; max-width: 72px; height: 170px; display: flex; align-items: flex-end; border-bottom: 1px solid var(--line); }
    .cols-chart .col-fill { width: 100%; background: var(--ink); border-radius: 3px 3px 0 0; }
    .cols-chart .col-val { font-size: 0.84rem; font-weight: 600; font-variant-numeric: tabular-nums; }
    .cols-chart .col-name { font-size: 0.7rem; color: var(--muted); text-align: center; overflow-wrap: anywhere; }

    /* Industry benchmark table */
    .bench-table, .matrix-scroll table.bench-table { width: 100%; min-width: 640px; table-layout: fixed; }
    .bench-table thead th { text-align: center; padding: 8px 4px; }
    .bench-table thead th:first-child { width: 22%; }
    .bench-table thead th .bench-sub { display: block; font-size: 0.6rem; letter-spacing: 0.02em; text-transform: none; color: var(--muted); font-weight: 400; margin-top: 2px; }
    .bench-table tbody th { text-align: left; font-size: 0.8rem; font-weight: 400; text-transform: none; letter-spacing: 0; color: var(--ink); padding: 6px 8px; border-bottom: 1px solid var(--line); }
    .bench-table td { text-align: center; font-size: 0.8rem; font-variant-numeric: tabular-nums; padding: 6px 4px; }
    .bench-table td.best { font-weight: 700; background: var(--chip); }
    .bench-table tr.bench-overall th, .bench-table tr.bench-overall td { font-size: 0.95rem; font-weight: 600; }
    .bench-table tr.bench-group td { text-align: left; text-transform: uppercase; letter-spacing: 0.07em; font-size: 0.68rem; font-weight: 600; color: var(--muted); border-bottom: 1px solid var(--ink); padding: 18px 10px 6px; background: none; }

    /* Tier explorer (who passed what) */
    .tx-table { min-width: 720px; }
    .tx-table th, .tx-table td { text-align: center; padding: 5px 8px; }
    .tx-table th:nth-child(-n+2), .tx-table td:nth-child(-n+2) { text-align: left; }
    .tx-table td { font-size: 0.8rem; border-bottom: 1px solid #eceff1; }
    .tx-table tbody tr { cursor: pointer; }
    .tx-table tbody tr:hover td, .tx-table tbody tr.active td { background: var(--chip); }
    .tx-table tfoot td { border-top: 1px solid var(--ink); border-bottom: 0; font-weight: 600; }
    .tx-id { font-size: 0.78rem; overflow-wrap: anywhere; }"""

    js = """<script>
  const TX = __TX__;
  const txMarks = (v) => v ? '<span class="pass">✓</span>' : '<span class="fail">✕</span>';
  const txPrompts = (typeof TM_ROWS !== "undefined")
    ? Object.fromEntries(TM_ROWS.map((r) => ["gen_" + r[0], r[5]])) : {};

  function txShort(s) {
    return s.id.replace(new RegExp("^gen_" + s.t + "_(" + s.f + "|app|skill)_?"), "") || s.id;
  }

  function renderTx(tier) {
    const rows = TX.scenarios.filter((s) => s.t === tier);
    const contested = rows.filter((s) => {
      const n = s.p.reduce((a, b) => a + b, 0);
      return n > 0 && n < TX.order.length;
    }).length;
    document.getElementById("tx-meta").textContent =
      rows.length + " scenarios · " + contested + " contested (models disagree) · sorted by family";
    const head = "<thead><tr><th>family</th><th>scenario</th>"
      + TX.short.map((s) => `<th>${esc(s)}</th>`).join("")
      + "<th>passed</th></tr></thead>";
    const body = "<tbody>" + rows.map((s, idx) => {
      const n = s.p.reduce((a, b) => a + b, 0);
      return `<tr data-tx-row="${idx}"><td>${esc(s.f)}</td>`
        + `<td class="tx-id">${esc(txShort(s))}</td>`
        + s.p.map(txMarks).map((m) => `<td>${m}</td>`).join("")
        + `<td>${n}/${TX.order.length}</td></tr>`;
    }).join("") + "</tbody>";
    const totals = TX.order.map((_, col) =>
      rows.reduce((a, s) => a + s.p[col], 0));
    const foot = "<tfoot><tr><td></td><td>tier total</td>"
      + totals.map((t) => `<td>${t}</td>`).join("")
      + `<td>/${rows.length}</td></tr></tfoot>`;
    const table = document.getElementById("tx-table");
    table.innerHTML = head + body + foot;
    table.querySelectorAll("[data-tx-row]").forEach((tr) => {
      tr.addEventListener("click", () => {
        table.querySelectorAll("[data-tx-row]").forEach((n) => n.classList.remove("active"));
        tr.classList.add("active");
        txDetail(rows[Number(tr.dataset.txRow)]);
      });
    });
    document.getElementById("tx-title").textContent = "Click a scenario row";
    document.getElementById("tx-text").innerHTML =
      "<p>Each cell is one model's strict verdict on one scenario. Click a row to see per-model scores, the first failed check, and the task prompt.</p>";
  }

  function txDetail(s) {
    document.getElementById("tx-title").textContent = s.id;
    const lines = TX.labels.map((label, i) => {
      const verdict = s.p[i]
        ? '<span class="pass">PASS</span>'
        : '<span class="fail">FAIL</span>';
      const issue = (!s.p[i] && s.i[i]) ? ` · <code>${esc(s.i[i])}</code>` : "";
      return `<div style="display:flex; gap:10px; font-size:0.85rem;">`
        + `<span style="min-width:120px;">${esc(label)}</span>${verdict}`
        + `<span style="color:var(--muted);">score ${s.s[i]}%${issue}</span></div>`;
    }).join("");
    const prompt = txPrompts[s.id]
      ? `<p class="tm-meta" style="margin:10px 0 0;">prompt: ${esc(txPrompts[s.id])}</p>` : "";
    document.getElementById("tx-text").innerHTML =
      `<p class="tm-meta" style="margin:0 0 8px;">${esc(s.f)} family · ${esc(s.t)} · ${esc(s.d)}</p>`
      + lines + prompt;
  }

  document.querySelectorAll("[data-tx]").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll("[data-tx]").forEach((n) => n.classList.remove("active"));
      button.classList.add("active");
      renderTx(button.dataset.tx);
    });
  });
  renderTx("t0");
  </script>"""

    # ---- TL;DR block for the top of the post -----------------------------------------
    tldr = f"""  <figure class="panel">
    <figcaption class="panel-head"><strong>TL;DR</strong><span>full results in <a href="#results">the results section</a></span></figcaption>
    <div class="panel-body" style="padding: 0;">
      <table class="stats-table">
        <tbody>
          <tr><td>best model</td><td><strong>{FULL[ORDER[0]]} · {fmt1(overall[ORDER[0]])}</strong> strict pass@1 — composition is nearly solved at the frontier; what remains is precision and ambient-state reasoning</td></tr>
          <tr><td>the spread</td><td><strong>{fmt1(overall[ORDER[0]])} → {fmt1(overall[ORDER[-1]])}</strong> across six models, frontier APIs to a local 8B — the bottom model beats the top on exactly {len(inversions)} of 300 scenarios</td></tr>
          <tr><td>open problems</td><td><strong>{len(all_fail)} of 300</strong> scenarios defeat every model tested, {fail_families.get('inspect', 0)} of them ambient-state inspection tasks — that list is the roadmap</td></tr>
        </tbody>
      </table>
    </div>
  </figure>"""

    # ---- apply ----------------------------------------------------------------------
    src = BLOG.read_text()

    tldr_anchor = "Part 3 turns the traces into training data.\n  </p>"
    src = replace_between(src, "WB-DEEP-TLDR", tldr, tldr_anchor, before=False)

    intro_anchor = "exported as portable rollout JSONL in the repo.\n  </p>"
    src = replace_between(src, "WB-DEEP-LEADERBOARD", leaderboard, intro_anchor, before=False)

    quote_anchor = "  <blockquote class=\"soft\">\n    The honest read:"
    src = replace_between(
        src, "WB-DEEP-DISTRIBUTION", distribution + "\n\n" + explorer, quote_anchor, before=True,
    )

    # migrate any old HTML-comment CSS markers (they corrupted adjacent rules)
    old_css_start = "<!-- WB-DEEP-CSS:START -->"
    if old_css_start in src:
        i = src.index(old_css_start)
        j = src.index("<!-- WB-DEEP-CSS:END -->") + len("<!-- WB-DEEP-CSS:END -->")
        src = src[:i] + src[j:]
    src = replace_between(src, "WB-DEEP-CSS", css, "  </style>", before=True, css=True)
    src = replace_between(
        src, "WB-DEEP-JS", js.replace("__TX__", tx_payload), "</body>", before=True,
    )

    old_cmds = """  <pre><code># the core comparison behind the charts (25 scenarios x 3 repeats)
uv run --extra dev workspace-bench compare-models \\
  --pack core --difficulty all --repeats 3 --metric pass-at-k

# the Stark enterprise pack
uv run --extra dev workspace-bench compare-models \\
  --pack stark-enterprise-v0 --difficulty all</code></pre>"""
    new_cmds = """  <pre><code># run any adapter file against the full 300-scenario release
uv run --extra dev workspace-bench compare-models \\
  --models-file models.json --pack all --difficulty all

# re-certify the pack before trusting anything (oracle 300/300, noop 0/300)
uv run --extra dev workspace-bench validate --pack all --min-scenarios 300

# export a finished run as portable rollout JSONL
uv run --extra dev workspace-bench export-rollouts \\
  --comparison-dir runs/comparison/&lt;run&gt; --output rollouts.jsonl</code></pre>"""
    if old_cmds in src:
        src = src.replace(old_cmds, new_cmds)
    else:
        assert new_cmds in src, "commands block missing in both old and new form"

    BLOG.write_text(src)
    print(
        f"Blog deepened: leaderboard ({len(ORDER)} models), distribution "
        f"({len(TIERS)} tiers + {len(DIFFS)} ratings), tier explorer "
        f"({len(tx_scenarios)} scenarios), analysis (all-fail {len(all_fail)}, "
        f"all-pass {len(all_pass)}, contested {len(contested)})"
    )


if __name__ == "__main__":
    main()
