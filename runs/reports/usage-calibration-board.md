# `enterprise-apps-usage` calibration board

Certified 2026-07-17 on suite content `2fe31c92315c` at harness `5b77b82`.
Strict-pass rates; local reference models run free-form (`OLLAMA_FORMAT=none`).

| level | driver | qwen3:8b | gpt-oss:20b | gpt-4.1-mini | GLM-5.2 | GPT-5.5 |
| --- | --- | --- | --- | --- | --- | --- |
| level0 | execute | 59% | 53% | 95% | 100% | 100% |
| level1 | discover | 38% | 44% | 76% | 95% | 100% |
| level2 | translate policy | 53% | 38% | 74% | 92% | 94% |
| level3 | ambient state | 25% | 12% | 44% | 72% | 97% |
| level4 | knowledge-governed | 3% | 9% | 19% | 59% | 81% |
| level5 | governed build | 0% | 0% | 3% | 22% | 56% |
| **overall** | | **29.7%** | **26.0%** | **51.8%** | **73.4%** | **88.0%** |

