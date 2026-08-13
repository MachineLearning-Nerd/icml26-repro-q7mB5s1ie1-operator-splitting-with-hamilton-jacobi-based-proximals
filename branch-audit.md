# Branch audit

This repository began with OpenResearch-style `orx/` branch names. The clean
names below preserve the original branch lineage while making the evidence
role readable. `main` is the publication surface.

| Historical branch | Clean branch | Purpose and evidence scope |
| --- | --- | --- |
| `main` | `main` | Publication README, reports, tutorial, and cumulative evidence surface. |
| `orx/frozen-baseline-theorem-calibrated-claim-1` | `audit/frozen-claim-1-baseline` | Locked environment and exact Claim 1 proof certificate. |
| `orx/exact-no-minimizer-counterexamples-for-claims-2` | `audit/no-minimizer-counterexamples` | Exact no-minimizer counterexamples for the printed Claims 2–4 convergence theorems. |
| `orx/paper-scale-five-family-convergence-corroboratio` | `experiment/paper-scale-convergence` | Paper-scale PPM, PGD, DRS, DYS, and PDHG runs for the intended corrected interpretation. |
| `orx/cumulative-theorem-verdicts-and-paper-scale-corr` | `release/cumulative-theorem-verdicts` | Cumulative Claims 1–4 verdicts plus paper-scale corroboration. |
| `orx/claim-5-exact-bound-counterexample-and-matched-h` | `audit/claim-5-bound-and-hybrid` | Exact splitting-bound counterexample, source projection audit, and corrected H.6 hierarchy. |
| `orx/publication-candidate-with-cumulative-evidence` | `release/publication-candidate` | Evaluator-visible release candidate and cumulative evidence packaging. |
| `orx/final-publication-artifact-and-post-run-evidence` | `release/post-publication-evidence` | Published artifact verification, post-run evidence, and judge-waiting state. |

## Branch hygiene

- No historical `orx/` branch remains in the cleaned public namespace.
- Branch names identify audit, experiment, or release role; they do not
  establish a scientific result.
- Claims 2–4 remain labeled **FALSIFIED as printed**, preserving the
  missing-minimizer-hypothesis boundary documented in their source audits.
- The audited paper version is recorded in each claim contract and source
  audit; branch names do not imply a paper-version change.
