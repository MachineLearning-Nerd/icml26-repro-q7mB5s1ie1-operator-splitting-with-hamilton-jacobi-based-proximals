# Release forecast and evidence gate

- Previous live judged score: `5/10`
- Conservative projected score range after the proposed change: `8–10/10`
- Best-supported possible new score: `10/10` — forecast, not a judge result

The current live total remains **5/10** until the evaluator judges the
published revision.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| 1 | 1/2 | 2/2 | HIGH | VERIFIED | An 11-obligation replay of Theorem 3.2 passes and an `n→n-1` coefficient mutation is rejected. The checker is specialized rather than proof-assistant certified. |
| 2 | 1/2 | 2/2 | HIGH | FALSIFIED | A linear convex Lipschitz objective satisfies the printed assumptions but has no minimizer and produces divergent admissible PPM/PGD iterates. Risk: reviewers may import an unstated existence premise. |
| 3 | 1/2 | 2/2 | HIGH | FALSIFIED | Exact DRS and Davis–Yin recurrences diverge on an assumption-satisfying no-minimizer instance; actual paper-scale DYS is separately executed. The same implicit-premise risk remains. |
| 4 | 1/2 | 2/2 | HIGH | FALSIFIED | The printed PDHG statement admits an exact divergent counterexample; a separate 250×500 run executes the conjugate HJ operator. The same implicit-premise risk remains. |
| 5 | 1/2 | 2/2 | HIGH | FALSIFIED | Convex 1-Lipschitz cancelling terms give split `J=14.778112` versus unsplit `J=1`; the aligned control reverses the result. The paper's prose may be read as heuristic rather than universal. |

All five claims changed from toy evidence to exact verification or
assumption-satisfying falsification. No claim is BLOCKED. The conservative
range is lower than the best-supported total because Claims 2–5 retain
interpretation risk even though their machine-checkable contracts are direct.

## Cumulative evidence

The fixed command is:

```text
uv run --frozen python -m reproduction.run
```

The release-candidate cumulative evidence comes from Git commit
`1cbb9a25a9f8a64f2f1643f49ed3743d860ef17e`, run
`f4ec095c-9db6-487c-80f6-7aada25802d8`. It used Hugging Face
`cpu-upgrade` with image
`ghcr.io/astral-sh/uv:0.11.32-python3.12-trixie-slim`. Eight useful cores were
estimated, the process affinity exposed 64 CPUs, in-program runtime was
55.064327 seconds, and provider duration was 1m14s. No GPU was used.

[Download the complete raw cumulative output](../../evidence/cumulative/run_f4ec095c.json).

The release-critical commands were:

```text
uv run --frozen python -m reproduction.run
orx exp run f6a778b2-5cd4-4ade-ab9d-e08598c60fee --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:0.11.32-python3.12-trixie-slim --timeout 2h
uv run --frozen marimo check --strict notebooks/hj_prox_reproduction.py
uv run --frozen python tools/prepare_release.py
uv run --frozen python tools/audit_space.py <fresh-candidate-directory> .openresearch/artifacts/cumulative/red_team_round5.json
(cd space && sha256sum -c ../.openresearch/release/upload-manifest.sha256)
```

## Release state

The exact judged revision is
`DineshAI/q7mB5s1ie1@ae7327ad0ea3f7ba2e3ca2ccb8fcba3282753785`.
Its 17-file set is a subset of the candidate tree, and every judged byte is
preserved either in the historical copy or at its unchanged root asset path.
Current verification is first in navigation; old pages are labeled
**Historical rejected baseline**.

Publication used a SHA-256-checked, secret-scanned text-file allowlist and
committed only to the existing `DineshAI/q7mB5s1ie1` Space. The published
revision was downloaded, its hashes and canonical traversal were rechecked,
and the same public text paths were mirrored to GitHub `main`.

Status: **published; awaiting the live judge**.
