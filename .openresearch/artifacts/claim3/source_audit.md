# Source audit

Theorem 3.8 requires proper convex LSC Lipschitz `f,g` and Assumption 3.7.
Theorem 3.9 requires proper LSC convex Lipschitz `f,g,h`, smooth `h`,
`0<t<2/L'`, and Assumption 3.7. Neither printed theorem assumes the relevant
argmin is nonempty.

Take `f=0`, `g(x)=x`, `h=0`, `t=0.5`, and use `L'=1` as a valid smoothness
upper bound for `h`. DRS and the displayed three-operator DYS update both
reduce to `state_(k+1)=state_k-t`. The objective is `F(x)=x`, which has no
minimizer. The fixed drift dominates the almost-sure summable HJ errors.
