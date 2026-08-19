# Reproduction status

## Paper

**Operator Splitting with Hamilton–Jacobi-based Proximals** by Nicholas Di,
Eric C. Chi, and Samy Wu Fung. The audited scientific source is arXiv
`2601.22370v4`, pinned by SHA-256 in the source audit.

## Overall verdict

`PARTIAL_CLAIM_1_VERIFIED_CLAIMS_2_TO_5_FALSIFIED_AS_PRINTED`

Claim 1 passes an 11-obligation symbolic HJ-Prox error certificate. Claims
2–4 are falsified as printed by exact assumption-satisfying no-minimizer
counterexamples. Claim 5's broad split-bound comparison is falsified by an
exact convex Lipschitz counterexample; the corrected H.6 hierarchy is reported
as a separate finite experiment and is not used to rescue the broad claim.

## Claim boundary

`C1_SYMBOLIC_SCOPED_VERIFIED_C2_C3_C4_PRINTED_STATEMENTS_FALSIFIED_BY_NO_MINIMIZER_COUNTEREXAMPLES_C5_BROAD_SPLIT_BOUND_FALSIFIED_H6_CORRECTED_HIERARCHY_REPORTED`

Claims 2–4 become missing-hypothesis diagnoses if the nonempty fixed-point
premise from an earlier theorem is intended implicitly. The finite paper-scale
experiments corroborate that interpretation but do not prove universal
almost-sure convergence.

| Item | Status |
| --- | --- |
| Current score claim | `false` |
| Publication gate | `false` |
| Official author endorsement | `false` |
| Last historical live judge | `5/10` |
| Projected score | `8/10–10/10`, forecast only |

## Verification

The cumulative evidence was produced with:

```bash
uv sync --frozen
uv run --frozen python -m reproduction.run
```

The exact claim contracts, raw outputs, independent checkers, controls,
source audits, and limitations are linked from
[`CLAIM_EVIDENCE.md`](CLAIM_EVIDENCE.md).

