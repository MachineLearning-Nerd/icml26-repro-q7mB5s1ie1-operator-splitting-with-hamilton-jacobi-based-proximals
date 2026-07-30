# Source audit

Theorem 3.10, equation (12), explicitly applies HJ-Prox to `g*` in the dual
update and to `f` in the primal update. It requires proper convex LSC `f,g`,
`tau*sigma*||A||^2<1`, and the Assumption 3.7 schedules, but does not assume a
minimizer exists.

Use `f(x)=x`, `g(y)=|y|`, and the zero linear operator `A`. Then
`g*` is the indicator of `[-1,1]`; at dual input zero its HJ-Prox is zero by
symmetry. The HJ-Prox of linear `f` has population update `x-tau`, and summable
Monte Carlo errors cannot cancel the fixed drift. The objective
`f(x)+g(0)=x` has no minimizer, while the step product is exactly zero.
