# Source audit

Retrieved 2026-07-30 from `https://arxiv.org/html/2601.22370v4` with the
explicit User-Agent `OpenResearch-Reproduction/1.0 (contact: DineshAI; paper
2601.22370)`. SHA-256:
`8e673443dd09f2952988fb9348c43f2b52d78442665d7b764e01586a8a7c5205`.

Anchors: Section 3.1, Theorem 3.2, equation (6), and Appendix A, equation (18).
The printed statement quantifies over finite LSC convex `f:R^n->R`; `x` is
inside a supremum, so the bound is uniform on all of `R^n`. Positive `t` and
`delta` are inherited from the proximal and viscous HJ definitions.

The certificate does not infer universality from a finite grid. It reconstructs
the strong-log-concavity argument: center the Gibbs density at the unique mode,
use the `1/t` quadratic curvature, apply coordinatewise Gibbs integration by
parts, sum all `n` coordinates, apply Jensen, and take a nonnegative square
root. The nonsmooth case is reached through Moreau envelopes and dominated
convergence.
