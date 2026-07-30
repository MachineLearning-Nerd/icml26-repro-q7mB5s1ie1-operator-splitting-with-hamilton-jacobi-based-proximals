# Claim 5 limitations and deviations

- The analytical verdict targets the broad Section 3.3 tighter-bound
  statement. Splitting can still help in aligned, non-cancelling cases, as the
  negative control demonstrates.
- The corrected H.6 comparison uses population HJ operators rather than
  `N=1000`; this isolates finite-delta bias from Monte Carlo variance.
- Approximate arms run 2,000 iterations rather than the paper source's 10,000.
  The exact reference runs 10,000, and precommitted horizons expose the
  trajectory.
- HJ-PPM is not included in the formal hierarchy because the public source
  projects samples before weighting and therefore does not implement Equation
  (4). The tested empirical subclaim is specifically hybrid DYS-HJ-1 versus
  fully approximate DYS-HJ-2.
- The H.6 experiment cannot measure a finite Theorem 3.3 full-objective
  Lipschitz constant because its quadratic and indicator violate that
  theorem's global real-valued Lipschitz premise.
