# Claim 4 — current verification

## Exact paper claim

Theorem 3.10 displays PDHG with HJ-Prox applied to the dual
`prox_(sigma g*)` and primal `prox_(tau f)` updates and claims almost-sure
convergence to a minimizer of `f(x)+g(Ax)`.

## Verdict: FALSIFIED as printed

Let `f(x)=x`, `g(y)=|y|`, and `A=0`, with `tau=sigma=0.5`. Both functions
are proper, convex, and LSC, and the strict step product is
`tau sigma ||A||²=0<1`. Here `g*` is the indicator of `[-1,1]`; at dual
input zero, its HJ-Prox is zero by symmetry. The primal HJ-Prox population
update is `x_(k+1)=x_k-tau`, and summable Monte Carlo errors cannot cancel
the fixed drift. The objective is `x`, so no minimizer exists.

This directly audits the conjugate mechanism missing from the historical
LASSO proxy. The negative control sets `A=1` and `tau=sigma=2`; the checker
rejects its step product of 4.

## Corrected-interpretation corroboration

The paper-scale run used 250 observations and 500 variables. Its dual
HJ-population update is explicitly
`prox^delta_(sigma g*)(v)=(v-sigma b)/(1+sigma)` for
`g*(y)=0.5||y||²+<b,y>`, followed by an HJ l1 primal update. The result reached
reference correlation **0.9999999999** and relative solution error
**1.258e-5**. The valid step product was 0.25; the product-4 control was
rejected.

## Reproduce and inspect

- [Contract](../../evidence/claim4/claim_contract.json)
- [Source audit](../../evidence/claim4/source_audit.md)
- [Raw counterexample](../../evidence/claim4/counterexample.json)
- [Independent checker](../../reproduction/verify_claims234.py)
- [Checker output](../../evidence/claim4/checker_output.json)
- [Step-product control](../../evidence/claim4/negative_control.json)
- [Control output](../../evidence/claim4/negative_control_output.json)
- [Limitations](../../evidence/claim4/limitations.md)
- [Raw PDHG result and checker output](../../evidence/cumulative/run_f4ec095c.json)
- [Executed PDHG source](../../reproduction/empirical.py)
- [Paper-scale independent checker](../../reproduction/verify_empirical.py)
