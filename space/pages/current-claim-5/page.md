# Claim 5 — current verification

## Exact paper claim

Section 3.3 defines `J(L)=exp(2L²t/delta)`, gives split approximation cost
`J_f+J_g`, and says splitting substantially reduces `J_(f+g)` and yields a
tighter theoretical bound. Section 4.3 says hybrid DYS-HJ-1 significantly
outperforms fully approximate DYS-HJ-2 on Appendix H.6's 250×500
nonnegative-LASSO experiment.

## Verdict: FALSIFIED

Let `f(x)=x` and `g(x)=-x`. Both are convex and have minimal global Lipschitz
constant 1, while `f+g=0` has minimal constant 0. At `t=delta=0.1`,

| quantity | exact value |
|---|---:|
| unsplit `J_(f+g)` | 1.000000 |
| split `J_f+J_g` | 14.778112 |

Thus the split bound is larger, contradicting the broad tighter-bound
statement. The aligned control `f=g=|x|` behaves in the intended direction:
split 14.778112 versus unsplit 2980.957987.

The H.6 full objective cannot supply the requested finite Lipschitz
measurement: its quadratic loss is not globally Lipschitz on `R^500`, and its
extended-valued orthant indicator has no finite real-valued Lipschitz
constant. Applying Theorem 3.3's `J` there would violate its premise.

## Corrected H.6 hierarchy

Using correct population HJ operators, five matched 250×500 data sets with 50
positive nonzeros support the narrower empirical statement. The geometric
mean hybrid/full analytical-residual ratio was **0.251737**; the paired
bootstrap 95% log-ratio interval was **[-1.40152, -1.35715]**. Hybrid objective
gaps were smaller for all five seeds. An identical-arm control found no
hierarchy.

The public paper source at commit
`895067559f4786c471a763811d949b3ae1f7377b` is not used as ground truth. Its
orthant routine is exactly half the true HJ value at `z=0` because it divides
by all samples rather than feasible mass.

## Reproduce and inspect

- Fixed command: `uv run --frozen python -m reproduction.run`
- [Claim contract](../../evidence/claim5/claim_contract.json)
- [Source and implementation audit](../../evidence/claim5/source_audit.md)
- [Method](../../evidence/claim5/method.md)
- [Raw five-seed traces](../../evidence/cumulative/run_f4ec095c.json)
- [Executable source](../../reproduction/claim5.py)
- [Independent checker](../../reproduction/verify_claim5.py)
- [Limitations and deviations](../../evidence/claim5/limitations.md)

The corrected experiment uses population HJ and 2,000 approximate iterations
rather than `N=1000` and 10,000. HJ-PPM is excluded because the public source
projects samples before weighting and does not implement Equation (4). These
deviations do not affect the exact counterexample.
