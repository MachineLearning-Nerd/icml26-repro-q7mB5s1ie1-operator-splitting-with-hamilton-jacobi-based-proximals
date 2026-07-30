# Operator Splitting with Hamilton-Jacobi-based Proximals — current reproduction

Current verification is presented first. The exact judged 5/10 baseline remains
reachable under **Historical rejected baseline**.

## Current status

| Claim | Status | Current evidence |
|---|---|---|
| 1, uniform HJ-Prox error bound | VERIFIED | machine-replayed symbolic derivation and a failing coefficient mutation |
| 2, PPM and PGD convergence | FALSIFIED as printed | valid no-minimizer construction; corrected n=500 PPM/PGD reach 1.940%/1.843% error |
| 3, DRS and DYS convergence | FALSIFIED as printed | divergent construction; actual n=256 DRS and 300×60 DYS executed |
| 4, PDHG conjugate approximation | FALSIFIED as printed | divergent construction; explicit 250×500 HJ `g*` run reaches correlation 0.9999999999 |
| 5, splitting and hybrid advantage | FALSIFIED | split `J=14.778` exceeds unsplit `J=1` for a valid cancelling pair; corrected H.6 hybrid/full residual ratio 0.25174 |

- [Current Claim 1 verification](current-claim-1/page.md)
- [Current Claim 2 verification](current-claim-2/page.md)
- [Current Claim 3 verification](current-claim-3/page.md)
- [Current Claim 4 verification](current-claim-4/page.md)
- [Current Claim 5 verification](current-claim-5/page.md)
- [Illustrated reproduction report](../reports/reproduction/report.md)
- [Visibility matrix](visibility/page.md)
- [Release forecast and evidence gate](release-report/page.md)
- [Historical rejected baseline](historical-baseline/page.md)

## Pages

| Page |
| --- |
| [overview](#/overview) |
| [claims](#/claims) |
| [evidence](#/evidence) |
| [conclusion](#/conclusion) |
| [verification-run](#/verification-run) |

The complete passing run record, including inline raw outputs, CPU allocation,
seeds, checkers, and controls, is
[downloadable here](../evidence/cumulative/run_108d9cac.json).
