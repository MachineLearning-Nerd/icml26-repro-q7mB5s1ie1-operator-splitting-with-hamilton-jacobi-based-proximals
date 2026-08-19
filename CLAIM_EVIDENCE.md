# Claim-to-evidence ledger

Each verdict is produced by a claim contract, source audit, executable
checker, saved raw result, and negative control. The evaluator-facing pages
are under [`space/pages`](space/pages), with mirrored evidence under
[`space/evidence`](space/evidence).

| Claim | Verdict | How the verdict is produced | Primary evidence |
| --- | --- | --- | --- |
| C1. Uniform HJ-Prox error bound | `VERIFIED_SCOPED` | Replay 11 symbolic obligations covering strong convexity, Gibbs integration by parts, the exact sum over coordinates, Jensen, prox translation, and the nonsmooth limit; reject an `n→n-1` coefficient mutation. | [`reproduction/verify_claim1.py`](reproduction/verify_claim1.py) · [`space/pages/current-claim-1/page.md`](space/pages/current-claim-1/page.md) |
| C2. HJ-Prox PPM and PGD convergence | `FALSIFIED_AS_PRINTED` | Use `f=0`, `g(x)=x`, summable HJ errors, and `t_k=0.5/(k+1)`; the admissible iterates drift while `F(x)=x` has no minimizer. | [`reproduction/verify_claims234.py`](reproduction/verify_claims234.py) · [`space/pages/current-claim-2/page.md`](space/pages/current-claim-2/page.md) |
| C3. HJ-Prox DRS and DYS convergence | `FALSIFIED_AS_PRINTED` | Use `f=0`, `g(x)=x`, `h=0`, constant `t=0.5`, and valid `L'=1`; both displayed maps reduce to a divergent translation with no minimizer. | [`reproduction/verify_claims234.py`](reproduction/verify_claims234.py) · [`space/pages/current-claim-3/page.md`](space/pages/current-claim-3/page.md) |
| C4. HJ-Prox PDHG convergence | `FALSIFIED_AS_PRINTED` | Use `f(x)=x`, `g(y)=|y|`, `A=0`, and `tau=sigma=0.5`; the conjugate-prox dual stays at zero while the primal drifts on an objective with no minimizer. | [`reproduction/verify_claims234.py`](reproduction/verify_claims234.py) · [`space/pages/current-claim-4/page.md`](space/pages/current-claim-4/page.md) |
| C5. Splitting bound and H.6 hierarchy | `FALSIFIED_SCOPED` | Check `f(x)=x`, `g(x)=-x`: unsplit `J=1` but split `J_f+J_g=14.778112`; run the corrected H.6 hierarchy separately with matched finite data. | [`reproduction/claim5.py`](reproduction/claim5.py) · [`space/pages/current-claim-5/page.md`](space/pages/current-claim-5/page.md) |

The counterexamples for Claims 2–4 are exact and assumption-satisfying under
the printed statements. The H.6 finite experiment is evidence for the
corrected interpretation only; it does not reverse the broad Claim 5 verdict.

