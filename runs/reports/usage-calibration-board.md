# `enterprise-apps-usage` calibration board

Certified 2026-07-17 on suite content `d6ca1439c8ca` at harness `0c2250f`;
gpt-4.1-mini re-measured 2026-07-19 with a uniform three-run protocol (see notes).
Strict-pass rates; local reference models run free-form (`OLLAMA_FORMAT=none`).

| level | driver | gpt-oss:20b | qwen3:8b | gpt-4.1-mini | GLM-5.2 | GPT-5.5 |
| --- | --- | --- | --- | --- | --- | --- |
| level0 | execute | 53% | 59% | 91% | 100% | 100% |
| level1 | discover | 39% | 42% | 75% | 95% | 100% |
| level2 | translate policy | 41% | 55% | 70% | 92% | 94% |
| level3 | ambient state | 12% | 28% | 47% | 72% | 97% |
| level4 | knowledge-governed | 9% | 3% | 17% | 59% | 81% |
| level5 | governed build | 0% | 0% | 7% | 22% | 56% |
| **overall** | | **25.8%** | **31.3%** | **51.0%** | **73.4%** | **88.0%** |

Serving and profile notes live in the JSON alongside per-cell attempt,
process-failure, and clean-rate detail.
