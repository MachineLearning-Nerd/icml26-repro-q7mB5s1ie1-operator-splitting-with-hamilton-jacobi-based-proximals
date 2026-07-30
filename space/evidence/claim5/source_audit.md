# Claim 5 source audit

Paper source: arXiv 2601.22370v4 HTML, retrieved 2026-07-30 with an
explicit browser user agent. SHA-256:
`8e673443dd09f2952988fb9348c43f2b52d78442665d7b764e01586a8a7c5205`.

Section 3.3 defines `J(L)=exp(2 L^2 t/delta)`, gives the split cost as
`J_f+J_g`, then says splitting "substantially reduces" the unsplit cost and
"yields a tighter theoretical bound." The stated assumptions for this
comparison are convexity and global Lipschitz constants `L_f,L_g`.

Section 4.3 and Figure 4 compare exact DYS, DYS-HJ-1 (exact nonnegative
projection and HJ l1), DYS-HJ-2 (both proxes approximated), and HJ-PPM. The
asserted hierarchy is that DYS-HJ-1 significantly outperforms DYS-HJ-2 and
HJ-PPM is worst. Appendix H.6 fixes 250 observations, 500 variables, 50
positive nonzeros, and fixed delta.

The linked public source repository was inspected at commit
`895067559f4786c471a763811d949b3ae1f7377b`. In
`dys_constrained_lasso.ipynb`, `compute_prox_projection` divides
`sum(y * 1[y>=0])` by all samples. In one dimension at `z=0`, its expectation
is `sigma/sqrt(2 pi)`, while the HJ-Prox conditional mean is
`sigma sqrt(2/pi)`: the source estimator is exactly one half of the named
operator. The source HJ-PPM also projects Gaussian samples before weighting,
which is not Equation (4). Neither implementation is used as ground truth.

The H.6 quadratic loss is not globally Lipschitz on R^500, and the
extended-valued orthant indicator has no finite real-valued Lipschitz
constant. Thus Theorem 3.3 cannot supply a finite full-objective `J` for H.6.
