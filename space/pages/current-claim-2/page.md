# Claim 2 — current verification

## Exact paper claim

Theorems 3.5 and 3.6 state that HJ-Prox PPM and PGD converge almost surely to a
minimizer under their printed convexity, Lipschitz/smoothness, step, and
Assumption 3.4 schedule conditions.

## Verdict: FALSIFIED as printed

Set `f(x)=0`, `g(x)=x`, and `t_k=0.5/(k+1)`. Both functions are finite,
proper, LSC, convex, and globally Lipschitz; `f` is 1-smooth and
`0<t_k<1`. Choose `delta_k=(k+1)^-4`, `alpha_k=(k+1)^-2`, a summable
Monte Carlo target `b_k=(k+1)^-2`, and

`N_k=ceil(max(8J_k/alpha_k, 8J_kM_k/(alpha_k b_k²)))`.

All printed conditions hold. But `F(x)=x` has no minimizer because
`F(x-1)=F(x)-1`. Both exact algorithm maps reduce to
`x_(k+1)=x_k-t_k`; the harmonic drift diverges to negative infinity and
almost-sure summable HJ errors cannot cancel it.

The paper's proof appears to intend the nonempty fixed-point condition from
Theorem 3.1. If treated as implicit, this result is a missing-hypothesis
diagnosis; a separate paper-scale route tests that corrected interpretation.

## Reproduce and inspect

- Fixed command: `uv run --frozen python -m reproduction.run`
- [Contract](../../evidence/claim2/claim_contract.json)
- [Source audit](../../evidence/claim2/source_audit.md)
- [Raw counterexample](../../evidence/claim2/counterexample.json)
- [Independent checker](../../reproduction/verify_claims234.py)
- [Checker output](../../evidence/claim2/checker_output.json)
- [Lipschitz-violating control](../../evidence/claim2/negative_control.json)
- [Control output](../../evidence/claim2/negative_control_output.json)
- [Limitations](../../evidence/claim2/limitations.md)
