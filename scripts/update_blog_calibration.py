"""Inject the v1 calibration results into blog post 1.

Reads runs/reports/v1-calibration.json (produced by compile_calibration.py)
and rewrites the results + failure sections of
docs/blog-workspacebench-series-draft.html:
  - replaces the v0-alpha results explorer with the six-model v1 explorer
    (per-model tier curves, strict/mean, per-model notes),
  - replaces the v0 issue-code data with v1 per-model issue data,
  - adds the "calibration caught our own bugs" narrative,
  - retires all "v1 baselines queued" copy.

Idempotence: the script replaces between stable HTML markers, so it can be
re-run after recompiling calibration data.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BLOG = REPO / "docs/blog-workspacebench-series-draft.html"
DATA = REPO / "runs/reports/v1-calibration.json"

LABELS = {
    "gpt-5.5": ("GPT-5.5", "frontier · OpenAI API"),
    "sonnet-5": ("Claude Sonnet 5", "frontier · via OpenRouter"),
    "glm-5.2": ("GLM-5.2", "open frontier · via OpenRouter"),
    "gpt-4.1-mini": ("gpt-4.1-mini", "gating model · tier bands defined here"),
    "gpt-oss-20b": ("gpt-oss:20b", "open 20B · local Ollama"),
    "qwen3-8b": ("Qwen3 8B", "small floor · local Ollama"),
}

NOTES = {
    "gpt-4.1-mini": "The gating model. Strictly monotonic — this curve defines the tier bands. Its #1 issue is schema-before-create discipline, the exact behavior Part 2's tool experiments target.",
    "gpt-5.5": "Frontier compression: composition (t4) barely slows it down; what remains are precision failures (exact layout coordinates) and ambient-state reasoning (the inspect family). v1's headroom warning, quantified.",
    "sonnet-5": "Run at temperature 0 via OpenRouter after a structured-output incompatibility was diagnosed and fixed in the harness (OpenRouter can route Anthropic models through Bedrock, where json_schema response_format degrades them to schema-minimal outputs).",
    "glm-5.2": "Strong mid-frontier. Its t0 dip is a discipline trait — invalid tool calls and skipped prompt fetches on tasks it treats as beneath deliberation — not a ladder fault.",
    "gpt-oss-20b": "Open-weights mid model. Independently reproduces the monotonic ladder — the cross-validation that the tier structure is real, not tuned to one vendor.",
    "qwen3-8b": "The small-model floor: what an 8B can and cannot do against a real tool surface. Every failure here is headroom for distillation and fine-tuning (Part 3).",
}


def main() -> None:
    data = json.loads(DATA.read_text())
    models = {m["slug"]: m for m in data["models"]}
    order = [s for s in LABELS if s in models]
    if len(order) < len(LABELS):
        missing = [s for s in LABELS if s not in models]
        print(f"WARNING: missing runs for {missing}; proceeding with {len(order)} models")

    blob = []
    for slug in order:
        m = models[slug]
        label, role = LABELS[slug]
        tiers = [round(100 * p / n) for p, n in m["tiers"].values()]
        blob.append({
            "slug": slug, "label": label, "role": role,
            "strict": m["strict"], "mean": round(100 * m["mean_score"], 1),
            "tiers": tiers,
            "issues": [[k, v] for k, v in m["top_issues"].items()][:5],
            "note": NOTES.get(slug, ""),
        })
    payload = json.dumps(blob, separators=(",", ":"))

    src = BLOG.read_text()

    # ---- 1. results section copy -------------------------------------------------
    old_intro = """    These are real runs from the interactive comparison harness: each model chooses one tool call, receives the simulated workspace result, then chooses the next call. They ran on the 40-scenario v0 alpha that seeded this benchmark — GPT-4.1 against a local 20B open-weights model (gpt-oss:20b via Ollama) on 25 scenarios, three attempts each, plus GPT-4.1 alone on the 15 enterprise scenarios. Full v1 baselines over all 300 are queued; these numbers are the reason the suite got harder."""
    new_intro = """    These are real runs from the interactive comparison harness: each model chooses one tool call, receives the simulated workspace result, then chooses the next call — all __NMODELS__ models against the same 300 certified scenarios, same grader, same logs. Two run locally through Ollama for free; the rest go through vendor APIs and OpenRouter. Every episode's full transcript is exported as portable rollout JSONL in the repo."""
    assert old_intro in src, "results intro anchor missing"
    src = src.replace(old_intro, new_intro.replace("__NMODELS__", str(len(order))))

    # ---- 2. swap the explorer data + JS -------------------------------------------
    # HTML: replace pack/metric button rows with model pills
    old_controls = """      <div class="btn-row"><span class="btn-label">Pack</span>
        <button class="btn active" data-pack="core">v0 core · 25 × 3</button>
        <button class="btn" data-pack="stark">v0 enterprise · 15 × 1</button>
      </div>
      <div class="btn-row"><span class="btn-label">Metric</span>
        <button class="btn active" data-metric="strict">strict pass</button>
        <button class="btn" data-metric="mean">mean score</button>
        <button class="btn" data-metric="passk">pass@3</button>
        <button class="btn" data-metric="passhatk">pass^3</button>
        <button class="btn" data-metric="levels">by level</button>
      </div>
      <div class="bars" id="results-bars" style="margin-top: 18px;" aria-live="polite"></div>"""
    new_controls = """      <div class="btn-row" id="calib-pills"><span class="btn-label">Model</span></div>
      <div id="calib-summary" style="margin-top: 16px;"></div>
      <div class="bars" id="results-bars" style="margin-top: 12px;" aria-live="polite"></div>"""
    assert old_controls in src, "explorer controls anchor missing"
    src = src.replace(old_controls, new_controls)

    old_caption = """<figcaption class="panel-head"><strong>Results explorer</strong><span>switch pack and metric</span></figcaption>"""
    new_caption = """<figcaption class="panel-head"><strong>v1 calibration results</strong><span>__NMODELS__ models · 300 scenarios each · pick one</span></figcaption>"""
    assert old_caption in src
    src = src.replace(old_caption, new_caption.replace("__NMODELS__", str(len(order))))

    # honest-read quote
    old_quote_start = src.index("  <blockquote class=\"soft\">\n    The honest read:")
    old_quote_end = src.index("</blockquote>", old_quote_start) + len("</blockquote>")
    mini = models.get("gpt-4.1-mini")
    mini_curve = " → ".join(f"{round(100*p/n)}%" for p, n in mini["tiers"].values()) if mini else ""
    top = max(order, key=lambda s: models[s]["strict"])
    top_label = LABELS[top][0]
    top_pct = round(models[top]["strict"] / 3)
    new_quote = f"""  <blockquote class="soft">
    The honest read: the gating model's ladder is strictly monotonic ({mini_curve}) and an independent open model reproduces the shape — the tiers are real. At the top, {top_label} passes {top_pct}% of the suite: v1 discriminates the mid-field sharply but the frontier is already close to the ceiling, and its remaining failures are precision and ambiguity, not composition. That is the roadmap for t5.
  </blockquote>"""
    src = src[:old_quote_start] + new_quote + src[old_quote_end:]

    # ---- 3. JS: replace runData block with calibration explorer -------------------
    js_start = src.index("  // ------------------------------------------------------------------\n  // Results explorer — real runs:")
    js_end = src.index("  // ------------------------------------------------------------------\n  // Issue-code explorer")
    new_js = """  // ------------------------------------------------------------------
  // v1 calibration explorer — data from scripts/compile_calibration.py
  // ------------------------------------------------------------------
  const CALIB = __CALIB__;
  const CALIB_TIERS = ["t0", "t1", "t2", "t3", "t4"];

  const calibPills = document.getElementById("calib-pills");
  calibPills.innerHTML = '<span class="btn-label">Model</span>' + CALIB.map((m, i) =>
    `<button class="btn${i === 0 ? " active" : ""}" data-calib="${i}">${esc(m.label)} · ${Math.round(m.strict / 3)}%</button>`
  ).join("");

  function renderCalib(index) {
    const m = CALIB[index];
    document.getElementById("calib-summary").innerHTML =
      `<p class="tm-meta" style="margin: 0 0 4px;">${esc(m.role)}</p>`
      + `<p style="margin: 0 0 10px; font-size: 0.92rem;"><strong>strict ${m.strict}/300</strong>`
      + ` · mean score ${m.mean}% · ${esc(m.note)}</p>`;
    document.getElementById("results-bars").innerHTML =
      "<div>" + CALIB_TIERS.map((tier, i) =>
        `<div class="bar-row"><span class="series-name">${tier}</span>`
        + `<div class="bar-track"><div class="bar-fill" data-width="${m.tiers[i]}"></div></div>`
        + `<span class="bar-value">${m.tiers[i]}%</span></div>`).join("") + "</div>";
    requestAnimationFrame(() => {
      document.querySelectorAll("#results-bars .bar-fill").forEach((fill) => {
        fill.style.width = fill.dataset.width + "%";
      });
    });
    renderIssues(index);
  }
  calibPills.querySelectorAll("[data-calib]").forEach((button) => {
    button.addEventListener("click", () => {
      calibPills.querySelectorAll("[data-calib]").forEach((node) => node.classList.remove("active"));
      button.classList.add("active");
      renderCalib(Number(button.dataset.calib));
    });
  });

"""
    src = src[:js_start] + new_js.replace("__CALIB__", payload) + src[js_end:]

    # ---- 4. issue explorer: feed from CALIB ---------------------------------------
    js_i_start = src.index("  const issueRuns = {")
    js_i_end = src.index("  renderIssues(\"ollama\");") + len("  renderIssues(\"ollama\");")
    new_issue_js = """  function renderIssues(modelIndex) {
    const m = CALIB[modelIndex];
    const rows = m.issues;
    const max = Math.max(...rows.map((row) => row[1]), 1);
    const container = document.getElementById("issue-rows");
    container.innerHTML = rows.map(([code, count]) => `
      <button class="issue-row" data-issue="${esc(code)}">
        <code>${esc(code)}</code>
        <div class="issue-track"><div class="issue-fill" data-width="${(count / max) * 100}"></div></div>
        <span class="issue-count">${count}</span>
      </button>`).join("");
    requestAnimationFrame(() => {
      container.querySelectorAll(".issue-fill").forEach((fill) => {
        fill.style.width = fill.dataset.width + "%";
      });
    });
    container.querySelectorAll("[data-issue]").forEach((row) => {
      row.addEventListener("click", () => {
        container.querySelectorAll("[data-issue]").forEach((node) => node.classList.remove("active"));
        row.classList.add("active");
        document.getElementById("issue-title").textContent = row.dataset.issue;
        document.getElementById("issue-text").textContent =
          issueMeaning[row.dataset.issue] || "Grader check failure — see docs/scenario-catalog.md for the check semantics.";
      });
    });
  }
  renderCalib(0);"""
    src = src[:js_i_start] + new_issue_js + src[js_i_end:]

    # issue section: retarget copy + controls
    old_issue_controls = """      <div class="btn-row">
        <button class="btn active" data-issuerun="ollama">gpt-oss:20b · core · 75 attempts</button>
        <button class="btn" data-issuerun="gpt">GPT-4.1 · core · 75</button>
        <button class="btn" data-issuerun="gptstark">GPT-4.1 · Stark · 15</button>
      </div>
      <div id="issue-rows" style="margin-top: 14px; display: grid; gap: 4px;" aria-live="polite"></div>"""
    new_issue_controls = """      <div id="issue-rows" style="display: grid; gap: 4px;" aria-live="polite"></div>"""
    assert old_issue_controls in src
    src = src.replace(old_issue_controls, new_issue_controls)

    old_issue_caption = """<figcaption class="panel-head"><strong>Issue codes across full runs</strong><span>click a row</span></figcaption>"""
    new_issue_caption = """<figcaption class="panel-head"><strong>Issue codes — selected model's v1 run</strong><span>follows the model picked above · click a row</span></figcaption>"""
    assert old_issue_caption in src
    src = src.replace(old_issue_caption, new_issue_caption)

    old_issue_intro = """    Every failed check maps to a stable issue code, and issue codes aggregate across a run. That turns "the small model is worse" into something specific: gpt-oss:20b mostly fails on tool discipline — malformed calls, mutating before schema lookup — while GPT-4.1's Stark failures are mostly wrong widget or missing artifact choices on multi-widget dashboards."""
    new_issue_intro = """    Every failed check maps to a stable issue code, and issue codes aggregate across a run. That turns "model X is worse" into something specific: the gating model's #1 failure is schema-before-create discipline, GLM-5.2 burns attempts on invalid calls, and GPT-5.5's residue is exact-layout precision. Same benchmark, different failure fingerprints — that specificity is what Part 2 builds on."""
    assert old_issue_intro in src
    src = src.replace(old_issue_intro, new_issue_intro)

    # ---- 5. calibration story section (insert before results section h2) ----------
    story_anchor = "  <h2>Same benchmark, different agents</h2>"
    assert story_anchor in src
    story = """  <h2>Calibration caught our own bugs</h2>
  <p>
    Before trusting any of the numbers below, the tiers had to earn them. The protocol: run a mid-strength gating model (gpt-4.1-mini) over all 300 scenarios and check that measured pass rates fall monotonically from t0 to t4 — if difficulty is structural, the curve must show it.
  </p>
  <p>
    The first gating run did something better than confirm the ladder: it exposed three defects in our own benchmark. Two brand-new families scored 0/20 — because the harness never documented the two new tools' schemas to models (they invented argument shapes), and because several prompts demanded facts the grader checked but the instructions never requested. A third pass caught an inconsistency in when schema-discipline was instructed versus silently expected. All three were fixed at the generator level, the pack re-certified (oracle 300/300, no-op 0/300), and the sweep re-run from scratch.
  </p>
  <p>
    The before/after tells the story: the gating curve went from 83–67–48–47–30 (with two broken families and a suspicious t2/t3 tie) to <strong>98–92–77–52–33</strong> — monotonic, well-spaced, t0 nearly-free, t4 unfloored. That loop — design structurally, certify, calibrate empirically, let calibration expose your own bugs, fix, recalibrate — is the discipline this whole series argues for. It cost about three days of compute babysitting, and it is the difference between a benchmark and a demo.
  </p>

""" + story_anchor
    src = src.replace(story_anchor, story)

    BLOG.write_text(src)
    print(f"Blog updated with {len(order)} models: {', '.join(order)}")


if __name__ == "__main__":
    main()
