# `enterprise-apps-usage` calibration board

Certified 2026-07-17 on suite content `d6ca1439c8ca` at harness `0c2250f`.
Strict-pass rates; local reference models run free-form (`OLLAMA_FORMAT=none`).

| level | driver | qwen3:8b | gpt-oss:20b | gpt-4.1-mini | GLM-5.2 | GPT-5.5 |
| --- | --- | --- | --- | --- | --- | --- |
| level0 | execute | 59% | 53% | 95% | 100% | 100% |
| level1 | discover | 42% | 39% | 79% | 95% | 100% |
| level2 | translate policy | 55% | 41% | 68% | 92% | 94% |
| level3 | ambient state | 28% | 12% | 44% | 72% | 97% |
| level4 | knowledge-governed | 3% | 9% | 19% | 59% | 81% |
| level5 | governed build | 0% | 0% | 3% | 22% | 56% |
| **overall** | | **31.3%** | **25.8%** | **51.3%** | **73.4%** | **88.0%** |

Serving and profile notes live in the JSON alongside per-cell attempt,
process-failure, and clean-rate detail.
