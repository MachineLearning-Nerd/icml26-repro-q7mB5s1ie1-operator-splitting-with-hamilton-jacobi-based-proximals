# Source audit

Theorems 3.5 and 3.6, equations (8) and (9), require proper LSC convex
Lipschitz `f,g`; PGD additionally requires smooth `f`, `0<t_k<1/L'`, and both
use Assumption 3.4. Neither printed theorem assumes `argmin(f+g)` is nonempty,
although the upstream perturbed fixed-point Theorem 3.1 does require a nonempty
common fixed-point set.

The counterexample uses `f(x)=0`, `g(x)=x`, and
`t_k=0.5/(k+1)`. Both functions satisfy the printed assumptions, but
`F(x-1)=F(x)-1`, so `argmin F` is empty. Exact PPM and PGD both have
`x_(k+1)=x_k-t_k`; summable HJ errors cannot cancel the divergent harmonic
drift.
