# Training Data Recipes

WorkspaceBench is not a trainer. It produces reliable benchmark traces and
export files that trainers can consume.

The benchmark should stay usable without GPU or fine-tuning dependencies.
Training workflows begin by exporting data explicitly.

## Dataset Versioning

Every rollout export includes metadata for:

- benchmark name
- benchmark version
- benchmark release id
- export schema version
- export timestamp
- task id, level, capability, workflow, domain, subdomain, difficulty, and split
- model or runner metadata when available
- task-suite metadata for private or hidden suites

This metadata lets you trace a training row back to the benchmark release and
task suite that produced it.

## SFT From Passing Traces

Use oracle traces as a small bootstrap dataset:

```bash
uv run workspace-bench export-sft \
  --oracle \
  --format openai_messages \
  --output runs/exports/oracle-sft.jsonl
```

Use passing model attempts from a comparison run:

```bash
uv run workspace-bench export-sft \
  --comparison-dir runs/comparison/<run-id> \
  --format openai_messages \
  --output runs/exports/model-sft.jsonl
```

Failed attempts are excluded by default. Add `--include-failures` only when the
trainer needs negative examples with grade metadata.

## Preference Pairs From Repeated Attempts

Run repeated attempts first:

```bash
uv run workspace-bench \
  --difficulty all \
  --repeats 3 \
  --metric pass-at-k \
  --timeout 240
```

Then export chosen/rejected pairs:

```bash
uv run workspace-bench export-preferences \
  --comparison-dir runs/comparison/<run-id> \
  --output runs/exports/preferences.jsonl
```

The chosen attempt is the passing or higher-scoring attempt for the same model
and task. The rejected attempt is the failing or lower-scoring attempt.

## Quality Rules

- Export data only from a known benchmark release.
- Keep train/dev/test task splits separate.
- Do not train on hidden benchmark answers if the same hidden pack will be used
  for held-out evaluation.
- Prefer passing traces for SFT.
- Keep failed traces only when their grade metadata is preserved.
- Keep raw comparison outputs so exported rows can be audited later.
