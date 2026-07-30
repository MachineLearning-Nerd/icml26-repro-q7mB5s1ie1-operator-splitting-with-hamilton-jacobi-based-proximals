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

The current cumulative evidence comes from Git commit
`1e6c16b3bc08dda235b956e09b26dfcde944c4da`, run
`108d9cac-f2d1-469e-8371-3381a2849645`. It used Hugging Face
`cpu-upgrade` with image
`ghcr.io/astral-sh/uv:0.11.32-python3.12-trixie-slim`. Eight useful cores were
estimated, the process affinity exposed 64 CPUs, in-program runtime was
53.746125 seconds, and provider duration was 11m02s. No GPU was used.

The experiment tree descends through the frozen Claim 1 baseline, exact
Claims 2–4 counterexamples, paper-scale intended-interpretation checks,
cumulative Claims 1–4, and the Claim 5 cumulative winner. Raw output is
available at `space/evidence/cumulative/run_108d9cac.json`.

## Release state

The exact judged revision is
`DineshAI/q7mB5s1ie1@ae7327ad0ea3f7ba2e3ca2ccb8fcba3282753785`.
Its 17-file set is a subset of the candidate tree, and every judged byte is
preserved either in the historical copy or at its unchanged root asset path.
Current verification is first in navigation; old pages are labeled
**Historical rejected baseline**.

Publication will use a SHA-256-checked, secret-scanned text-file allowlist to
commit only to the existing `DineshAI/q7mB5s1ie1` Space. After publication,
the exact revision will be downloaded, hashes and canonical traversal will be
rechecked, and the same public text paths will be mirrored to GitHub `main`.
The paper will then be reported as awaiting the live judge.
