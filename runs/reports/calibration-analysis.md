# Build-suite calibration — 2026-07

The empirical difficulty labels use only the three complete guided-track runs below (236 tasks × 2 repeats). Process failures caused by malformed model output remain strict failures. Provider-credit failures are excluded.

## Clean-run summary

| Model | Strict | State | Runtime | Invalid calls | Median turns | Recovery | Flip | Cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| OpenAI GPT-5.1 | 47/472 (10.0%) | 20.8% | 58.3% | 10.5% | 4.0 | 11.0% | 5.5% | $9.48 |
| OpenAI GPT-5.4 mini | 15/472 (3.2%) | 7.6% | 35.0% | 6.2% | 6.0 | 7.6% | 5.5% | $5.12 |
| OpenAI GPT-5.5 | 128/472 (27.1%) | 31.1% | 48.9% | 2.9% | 6.0 | 32.9% | 5.1% | $61.23 |

## Family × measured difficulty

### OpenAI GPT-5.1

| Family | Easy | Medium | Hard |
| --- | ---: | ---: | ---: |
| advanced | 2/12 (17%) | — | 0/28 (0%) |
| aggrid | 0/12 (0%) | 0/4 (0%) | 0/24 (0%) |
| apps | 8/12 (67%) | 0/4 (0%) | 0/24 (0%) |
| charts | 2/6 (33%) | — | 0/34 (0%) |
| debug | 18/18 (100%) | 3/10 (30%) | 4/20 (20%) |
| e2e | — | — | 0/24 (0%) |
| extend | 1/10 (10%) | — | 0/30 (0%) |
| forms | 0/2 (0%) | — | 0/38 (0%) |
| grouping | 2/2 (100%) | 1/2 (50%) | 0/36 (0%) |
| params | 0/12 (0%) | 1/2 (50%) | 0/26 (0%) |
| settings | 3/12 (25%) | — | 0/28 (0%) |
| types | 2/12 (17%) | — | 0/28 (0%) |

### OpenAI GPT-5.4 mini

| Family | Easy | Medium | Hard |
| --- | ---: | ---: | ---: |
| advanced | 3/12 (25%) | — | 0/28 (0%) |
| aggrid | 1/12 (8%) | 0/4 (0%) | 0/24 (0%) |
| apps | 3/12 (25%) | 0/4 (0%) | 0/24 (0%) |
| charts | 1/6 (17%) | — | 0/34 (0%) |
| debug | 0/18 (0%) | 0/10 (0%) | 0/20 (0%) |
| e2e | — | — | 0/24 (0%) |
| extend | 2/10 (20%) | — | 0/30 (0%) |
| forms | 0/2 (0%) | — | 0/38 (0%) |
| grouping | 1/2 (50%) | 0/2 (0%) | 0/36 (0%) |
| params | 1/12 (8%) | 0/2 (0%) | 0/26 (0%) |
| settings | 3/12 (25%) | — | 0/28 (0%) |
| types | 0/12 (0%) | — | 0/28 (0%) |

### OpenAI GPT-5.5

| Family | Easy | Medium | Hard |
| --- | ---: | ---: | ---: |
| advanced | 11/12 (92%) | — | 0/28 (0%) |
| aggrid | 10/12 (83%) | 2/4 (50%) | 0/24 (0%) |
| apps | 12/12 (100%) | 2/4 (50%) | 0/24 (0%) |
| charts | 5/6 (83%) | — | 0/34 (0%) |
| debug | 18/18 (100%) | 9/10 (90%) | 14/20 (70%) |
| e2e | — | — | 0/24 (0%) |
| extend | 7/10 (70%) | — | 0/30 (0%) |
| forms | 2/2 (100%) | — | 0/38 (0%) |
| grouping | 0/2 (0%) | 0/2 (0%) | 0/36 (0%) |
| params | 12/12 (100%) | 2/2 (100%) | 0/26 (0%) |
| settings | 11/12 (92%) | — | 0/28 (0%) |
| types | 11/12 (92%) | — | 0/28 (0%) |

## Excluded OpenRouter incidents

These slices are supplementary only and never feed labels; valid attempts cover an alphabet-biased prefix of the suite.

| Model | Process failures | HTTP 402 | Valid attempts | Strict | State | Runtime |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| OpenRouter Claude Sonnet 5 | 362/472 | 356 | 110 | 30/110 (27.3%) | 38.2% | 52.7% |
| OpenRouter GLM-5.2 | 357/472 | 349 | 115 | 17/115 (14.8%) | 29.6% | 48.7% |

Once credits are restored, rerun exactly:

```bash
uv run workspace-bench --models-file runs/comparison/build-calibration-202607/models.json --models openrouter-claude-sonnet-5 openrouter-glm-5.2 --suite build-openbb-apps --runner interactive --track guided --repeats 2 --episode-timeout 420 --concurrency 3 --output-dir runs/comparison/build-calibration-openrouter-rerun-202607
```
