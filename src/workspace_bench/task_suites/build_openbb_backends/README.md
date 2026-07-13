# `build-openbb-backends` task suite

Tasks: 12

## Purpose

A pass means the agent can edit a pinned FastAPI starter repository into a working OpenBB custom backend whose manifests, HTTP behavior, and evaluator-owned tests satisfy the declared real-code contract.

## Workspace baseline

The manifest declares no default-workspace version, so the baseline is minimal. Each task supplies its own starter repository, oracle repository, tests, and HTTP probes instead of seeding simulated Workspace state.

## Generation method

`agent-authored-certified`. This is the experimental v0 real-code track: agent-written definitions in `scripts/generators/generate_backend_code_suite.py` produce deterministic starter and oracle repositories, and suite validation installs, launches, probes, mutates, and tears down the resulting processes.

## Axes

All tasks belong to the `backend-code` family. Category distinguishes building or extending a backend from repairing one, and difficulty reflects the breadth of the manifest, parameter, endpoint, and test contract. This v0 suite does not use rungs or a separate specification-level field.

| Axis | File-derived counts |
| --- | --- |
| `family` | `backend-code` 12 |
| `category` | `platform` 10; `repair` 2 |
| `difficulty` | `easy` 3; `medium` 6; `hard` 3 |
| `specification_level` | omitted 12 |

## Gates

`workspace-bench validate --suite build-openbb-backends` verifies that the oracle repository installs, launches, passes its pinned tests, serves valid `widgets.json` or `apps.json` manifests, and satisfies typed HTTP probes; the starter no-op must fail, evaluator mutations must be rejected, processes must terminate cleanly, and task ids and generated content must remain deterministic.

## Limitations

This suite executes agent code and is not a security sandbox. It is an experimental v0 contract with only 12 FastAPI tasks, pinned dependencies, local HTTP probes, and evaluator-owned tests; a pass does not establish production hardening, deployment readiness, live Workspace compatibility, or complete backend-framework coverage.
