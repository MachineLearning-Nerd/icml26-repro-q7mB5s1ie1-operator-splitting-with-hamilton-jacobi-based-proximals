# Method

The checker independently audits the convex/Lipschitz/smooth function
properties, the DYS step inequality, the `sqrt(delta_k)` and `alpha_k`
summability exponents, and the explicit sample-size witness. It replays the
displayed DRS and DYS algebra for this construction.

The negative control changes `t` from `0.5` to `3` while retaining `L'=1`; it
must fail the printed `0<t<2/L'` condition.
