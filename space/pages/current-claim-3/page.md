# Claim 3 — current verification

## Exact paper claim

Theorems 3.8 and 3.9 state that the displayed HJ-Prox Douglas–Rachford and
Davis–Yin iterates converge almost surely to minimizers of `f+g` and `f+g+h`
under the printed assumptions.

## Verdict: FALSIFIED as printed

Use `f=0`, `g(x)=x`, `h=0`, `t=0.5`, and take `L'=1` as a valid
smoothness upper bound for `h`. All three functions are proper, LSC, convex,
and globally Lipschitz; `h` is smooth and `0<t<2/L'`. The Assumption 3.7
sequences use `delta_k=(k+1)^-4`, `alpha_k=(k+1)^-2`, a summable Monte Carlo
target, and the explicit sample-size witness linked below.

Both the displayed DRS and three-term DYS maps reduce to
`state_(k+1)=state_k-t`, up to almost-sure summable HJ errors. They diverge,
and `F(x)=x` has no minimizer. A single dimension is decisive for falsifying
a universal theorem; it is not described as full-scale empirical evidence.

The negative control changes `t` to 3 and is rejected because
`0<t<2/L'` no longer holds.

## Reproduce and inspect

- [Contract](../../evidence/claim3/claim_contract.json)
- [Source audit](../../evidence/claim3/source_audit.md)
- [Raw counterexample](../../evidence/claim3/counterexample.json)
- [Independent checker](../../reproduction/verify_claims234.py)
- [Checker output](../../evidence/claim3/checker_output.json)
- [Step-violating control](../../evidence/claim3/negative_control.json)
- [Control output](../../evidence/claim3/negative_control_output.json)
- [Limitations](../../evidence/claim3/limitations.md)
