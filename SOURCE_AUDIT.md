# Source audit

The scientific evidence is pinned to **Operator Splitting with
Hamilton–Jacobi-based Proximals**, arXiv `2601.22370v4`.

| Field | Value |
| --- | --- |
| Retrieved | `2026-07-30` |
| Source URL | https://arxiv.org/abs/2601.22370v4 |
| Source SHA-256 | `8e673443dd09f2952988fb9348c43f2b52d78442665d7b764e01586a8a7c5205` |
| Claims | 1 through 5 |
| Main interpretation boundary | Printed Claims 2–4 omit or rely on a nonempty minimizer/fixed-point premise |

Claim 1's checker records the exact theorem obligations and the trusted
specialized mathematical steps. Claims 2–4 use `F(x)=x` or its displayed
PDHG analogue, which satisfies the printed assumptions but has no minimizer;
the resulting divergent iterates expose the missing-hypothesis boundary.

Claim 5's source audit also records that the paper's H.6 quadratic loss and
extended-valued orthant indicator do not satisfy the global real-valued
Lipschitz premise needed for a finite full objective `J`. The broad split
comparison is therefore tested with the independent convex Lipschitz pair
`f(x)=x`, `g(x)=-x`, while the corrected H.6 hierarchy is reported separately.

Detailed per-claim source records are under
[`space/evidence`](space/evidence) and `.openresearch/artifacts`.

