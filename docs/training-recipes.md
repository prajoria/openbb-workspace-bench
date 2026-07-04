# Training Data Recipes

WorkspaceBench is not a trainer. It produces reliable benchmark traces and
export files that trainers can consume.

The benchmark should stay usable without GPU, RL, or fine-tuning dependencies.
Training workflows begin by exporting data explicitly.

## Dataset Versioning

Every rollout export includes metadata for:

- benchmark name
- benchmark version
- benchmark release id
- export schema version
- export timestamp
- scenario id, level, capability, workflow, domain, subdomain, difficulty, and split
- model or runner metadata when available
- task-pack metadata for private or hidden packs

This metadata lets you trace a training row back to the benchmark release and
scenario pack that produced it.

## SFT From Passing Traces

Use oracle traces as a small bootstrap dataset:

```bash
uv run --extra dev workspace-bench export-sft \
  --oracle \
  --format openai_messages \
  --output runs/exports/oracle-sft.jsonl
```

Use passing model attempts from a comparison run:

```bash
uv run --extra dev workspace-bench export-sft \
  --comparison-dir runs/comparison/<run-id> \
  --format openai_messages \
  --output runs/exports/model-sft.jsonl
```

Failed attempts are excluded by default. Add `--include-failures` only when the
trainer needs negative examples with grade metadata.

## Preference Pairs From Repeated Attempts

Run repeated attempts first:

```bash
uv run --extra dev workspace-bench compare-models \
  --difficulty all \
  --repeats 3 \
  --metric pass-at-k \
  --timeout 240
```

Then export chosen/rejected pairs:

```bash
uv run --extra dev workspace-bench export-preferences \
  --comparison-dir runs/comparison/<run-id> \
  --output runs/exports/preferences.jsonl
```

The chosen attempt is the passing or higher-scoring attempt for the same model
and scenario. The rejected attempt is the failing or lower-scoring attempt.

## RL Rollout Collection

Use the Gym-style adapter for policy loops:

```python
from workspace_bench.rl.env import WorkspaceGymEnv
from workspace_bench.rl import collect_rollout
from workspace_bench.core.runner import find_scenario

scenario = find_scenario("gen_t0_create_price_performance_aapl")
env = WorkspaceGymEnv(scenario=scenario, process_rewards=True)

transitions = collect_rollout(
    env,
    [{"tool": "get_workspace_snapshot", "args": {}}],
    seed=1,
)
```

The environment uses the same simulator and graders as normal benchmark runs.
Sparse reward is the final grade score. Optional process rewards can shape tool
discipline, but they should not replace final deterministic grading.

## Quality Rules

- Export data only from a known benchmark release.
- Keep train/dev/test scenario splits separate.
- Do not train on hidden benchmark answers if the same hidden pack will be used
  for held-out evaluation.
- Prefer passing traces for SFT.
- Keep failed traces only when their grade metadata is preserved.
- Keep raw comparison outputs so exported rows can be audited later.
