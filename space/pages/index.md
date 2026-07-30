# Operator Splitting with Hamilton-Jacobi-based Proximals — current reproduction

Current verification is presented first. The exact judged 5/10 baseline remains
reachable under **Historical rejected baseline**.

## Current status

| Claim | Status | Current evidence |
|---|---|---|
| 1, uniform HJ-Prox error bound | VERIFIED | machine-replayed symbolic derivation and a failing coefficient mutation |
| 2, PPM and PGD convergence | FALSIFIED as printed | valid no-minimizer construction; intended corrected theorem still receives a paper-scale sibling test |
| 3, DRS and DYS convergence | FALSIFIED as printed | both displayed maps have a valid divergent construction; paper-scale sibling pending |
| 4, PDHG conjugate approximation | FALSIFIED as printed | displayed `g*` and `f` updates checked in a valid divergent construction; paper-scale sibling pending |
| 5, splitting and hybrid advantage | BLOCKED | pending matched paper-scale experiment and measured constants |

- [Current Claim 1 verification](current-claim-1/page.md)
- [Current Claim 2 verification](current-claim-2/page.md)
- [Current Claim 3 verification](current-claim-3/page.md)
- [Current Claim 4 verification](current-claim-4/page.md)
- [Visibility matrix](visibility/page.md)
- [Historical rejected baseline](historical-baseline/page.md)

## Pages

| Page |
| --- |
| [overview](#/overview) |
| [claims](#/claims) |
| [evidence](#/evidence) |
| [conclusion](#/conclusion) |
| [verification-run](#/verification-run) |
