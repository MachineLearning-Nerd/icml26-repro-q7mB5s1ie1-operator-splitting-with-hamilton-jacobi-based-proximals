# Claim 5 method

The analytical route uses `f(x)=x` and `g(x)=-x`. Both functions are convex
and have minimal global Lipschitz constant 1, while `f+g=0` has minimal
constant 0. At `t=delta=0.1`, the unsplit constant is 1 and the split total is
`2 exp(2)`. The independent control `f=g=abs(x)` reverses the comparison as
expected.

The empirical route generates five independent H.6-scale data sets. Exact
DYS, hybrid DYS with the correct population HJ l1 prox, and fully approximate
DYS with correct population HJ l1 and orthant proxes share all parameters.
All methods are evaluated with the exact DYS fixed-point residual. A paired
bootstrap interval on the log hybrid/full residual ratio quantifies the
hierarchy. An identical-arm control must not declare a hierarchy.

The fixed cumulative command is:

`uv run --frozen python -m reproduction.run`

The cumulative run is estimated at eight cores and is routed to Hugging Face
`cpu-upgrade` with image
`ghcr.io/astral-sh/uv:0.11.32-python3.12-trixie-slim`.
