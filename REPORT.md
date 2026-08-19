# Audit report

This repository is an independent reproduction and claim audit for
**Operator Splitting with Hamilton–Jacobi-based Proximals**.

The uniform HJ-Prox error bound passes a replayed symbolic certificate. The
printed convergence statements for PPM/PGD, DRS/DYS, and PDHG are falsified by
exact no-minimizer counterexamples under their displayed assumptions. The
broad Claim 5 split-bound comparison is independently falsified by a convex
Lipschitz cancelling pair, while the corrected H.6 hierarchy is reported as a
separate finite experiment with its source deviations disclosed.

Read the detailed report at
[`reports/reproduction/report.md`](reports/reproduction/report.md), the
release report at
[`reports/reproduction/release-report.md`](reports/reproduction/release-report.md),
and the evaluator-facing pages under [`space/pages`](space/pages).

The branch roles and historical `orx/` to clean-name mapping are documented
in [`branch-audit.md`](branch-audit.md). Branch names describe evidence role;
they are not separate paper versions or author statements.

