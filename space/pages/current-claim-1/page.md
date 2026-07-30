# Claim 1 — current verification

## Exact paper claim

Theorem 3.2 states that for every finite lower-semicontinuous convex
`f:R^n→R`, every `x∈R^n`, and positive `t,δ`,

`||prox^δ_tf(x) − prox_tf(x)|| ≤ sqrt(n t δ)`,

uniformly over `x`. Source: arXiv:2601.22370v4, Section 3.1, Theorem 3.2,
equation (6), restated and proved in Appendix A.

## Verdict: VERIFIED

This current result does not extrapolate from a one-dimensional grid. It uses an
independently reconstructed symbolic certificate:

1. `f(y)+||x-y||²/(2t)` is `1/t`-strongly convex.
2. Gibbs integration by parts contributes exactly `δ` in each of `n`
   coordinates.
3. Therefore `E||W||² ≤ n t δ`.
4. Jensen gives `||E W||² ≤ E||W||²`; the Gibbs mean is `prox^δ` and its mode
   is `prox`.
5. Moreau-envelope approximation plus dominated convergence covers nonsmooth
   convex `f`.

The checker replays 11 obligations and exits nonzero if any fails. A mutation
that replaces the `n` coordinate contributions with `n−1` is rejected.

## Reproduce and inspect

- Fixed command: `uv run --frozen python -m reproduction.run`
- [Claim contract](../../evidence/claim1/claim_contract.json)
- [Source audit](../../evidence/claim1/source_audit.md)
- [Proof certificate](../../evidence/claim1/proof_certificate.json)
- [Fixed cumulative runner](../../reproduction/run.py)
- [Executable checker](../../reproduction/verify_claim1.py)
- [Checker output](../../evidence/claim1/checker_output.json)
- [Negative-control certificate](../../evidence/claim1/negative_control_certificate.json)
- [Negative-control output](../../evidence/claim1/negative_control_output.json)
- [Limitations](../../evidence/claim1/limitations.md)

This page supersedes the old one-dimensional verification. The prior material
remains reachable under **Historical rejected baseline** and is not the current
verifier.
