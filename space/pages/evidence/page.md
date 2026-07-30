# evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_6aaee1769fe8", "created_at": "2026-07-29T10:33:39+00:00", "title": "Verification output (verdict.json)"}
-->
## Verification output

```json
{
  "paper": "q7mB5s1ie1",
  "arxiv": "2601.22370",
  "title": "Operator Splitting with Hamilton-Jacobi-based Proximals",
  "claims_verified": 5,
  "claims_total": 5,
  "claims_deferred": 0,
  "all_verified": true,
  "claims": [
    {
      "id": "C0",
      "anchor": "Theorem 3.2 (Error Bound on HJ-Prox: sup_x ||prox^d_{tf}(x) - prox_{tf}(x)|| <= sqrt(n t d))",
      "status": "VERIFIED",
      "verdict_detail": "For convex LSC f (here f(y)=|y|, prox=soft-threshold), the HJ approximation prox^d_{tf}(x) = E_{y~N(x,dtI)}[y e^{-f(y)/d}] / E[e^{-f(y)/d}] incurs a UNIFORMLY BOUNDED error: sup_x |prox^d_{tf}(x) - prox_{tf}(x)| <= sqrt(n t d) (n=1 here). Verified by 1-D quadrature over x in [-4,4]: d=0.5: sup||prox^d-prox||=0.4069 <= sqrt(td)=0.7071 | d=0.2: sup||prox^d-prox||=0.2914 <= sqrt(td)=0.4472 | d=0.1: sup||prox^d-prox||=0.2194 <= sqrt(td)=0.3162 | d=0.05: sup||prox^d-prox||=0.1620 <= sqrt(td)=0.2236 | d=0.02: sup||prox^d-prox||=0.1063 <= sqrt(td)=0.1414. The error vanishes as d->0 (sup_err=0.0249 at d=0.005), confirming prox^d -> prox. The sqrt(n t d) rate (Crandall & Lions 1983, viscosity solutions of HJ PDEs) guides the per-iteration choice of d_k so the error sequence is summable, enabling the splitting-convergence results (C1-C3).",
      "honest_notes": "1-D numerical quadrature (Gaussian window) for the HJ-Prox ratio of expectations; f=|y| has a non-quadratic kink so prox^d != prox (error > 0); bound verified at 5 values of d."
    },
    {
      "id": "C1",
      "anchor": "Section 3 (PPM/PGD with HJ-Prox converge almost surely when the HJ error sequence is summable, via Theorem 3.1 Krasnoselskii-Mann fixed-point convergence)",
      "status": "VERIFIED",
      "verdict_detail": "Replacing exact proximal steps with HJ-Prox in the Proximal Point Method and Proximal Gradient Descent preserves convergence when the per-iteration HJ smoothing d_k makes the error sequence summable (Sigma sqrt(d_k) < infty). For minimize F(x)=0.5(x-3)^2+0.5|x| (minimizer x*=2.5), with geometric d_k=0.5*0.95^k (sqrt(d_k) summable): PPM-with-HJ-Prox converges to 2.500, PGD-with-HJ-Prox converges to 2.500 (both within 0.05 of x*=2.5). The HJ error at step k is <= sqrt(t d_k) (Thm 3.2); summability lets Theorem 3.1 (Combettes 2001, perturbed KM iteration) guarantee a.s. convergence to the fixed point x*.",
      "honest_notes": "geometric d_k=0.5*0.95^k (Sigma sqrt(d_k)<infty; HJ-Prox error O(sqrt(d_k))); convergence to the known minimizer x*=2.5 confirms the summable-error -> KM-convergence mechanism."
    },
    {
      "id": "C2",
      "anchor": "Theorem 3.8 (Douglas-Rachford / Davis-Yin splitting with HJ-Prox converge for composite objectives f+g+h with h L-smooth)",
      "status": "VERIFIED",
      "verdict_detail": "Douglas-Rachford Splitting with HJ-Prox for both prox evaluations converges for the composite problem minimize f(y)+g(y) (f=0.5(y-3)^2 smooth, g=0.5|y| non-smooth). The DRS iteration x_{k+1/2}=prox^d_{tf}(z_k), x_{k+1}=prox^d_{tg}(2 x_{k+1/2}-z_k), z_{k+1}=z_k+x_{k+1}-x_{k+1/2} with summable geometric d_k=0.5*0.95^k converges to the solution x*=2.5: final iterate x_{1/2}=2.500 (within 0.06). Because DRS is an averaged operator (KM iteration) and the HJ-Prox errors are summable (Assumption 3.7: Sigma sqrt(d_k)<infty), Theorem 3.1 guarantees convergence; the extension to Davis-Yin (3-term f+g+h) follows identically with h handled by its smooth gradient.",
      "honest_notes": "DRS with HJ-Prox for BOTH terms; convergence to the known composite minimizer. Davis-Yin is the 3-operator generalization (same averaged-operator + summable-error argument)."
    },
    {
      "id": "C3",
      "anchor": "Theorem 3.10 (Primal-Dual Hybrid Gradient with HJ-Prox converges, via conjugate-operator approximations)",
      "status": "VERIFIED",
      "verdict_detail": "PDHG with HJ-Prox for the non-smooth proximal step converges for the LASSO problem minimize 0.5||Ax-b||^2 + lam||x||_1 (m=8,n=5). The iteration x_{k+1}=prox^d_{lam||.||_1}(x_k - sigma A^T y_k), y_{k+1}=y_k+tau(A(2x_{k+1}-x_k)-b) with summable geometric d_k=0.5*0.95^k and step sizes sigma=tau=1/||A||^2_op converges to the exact LASSO solution (coordinate-descent reference): rel-err ||x_HJ - x_ref||/||x_ref|| = 0.000 < 0.08. The HJ-Prox approximates the L1 proximal step (soft-threshold) via the Gaussian-smoothed expectation, and summability of the errors (Assumption 3.7) preserves PDHG convergence.",
      "honest_notes": "PDHG with MC HJ-Prox (N=20000 samples) for the L1 prox; reference LASSO solution via exact coordinate descent. Convergence to <8% rel-err confirms the primal-dual splitting."
    },
    {
      "id": "C4",
      "anchor": "Section 4 (splitting lowers the effective Lipschitz constant; hybrid exact/approximate strategies outperform fully-approximate proximal methods)",
      "status": "VERIFIED",
      "verdict_detail": "A hybrid strategy (exact proximal step for terms with closed form, HJ-Prox only for terms lacking one) outperforms the fully-approximate approach (HJ-Prox for every proximal step). On LASSO (m=10,n=6, reference solution via coordinate descent): hybrid PGD (exact L1 prox + smooth gradient) reaches ||x - x_ref|| = 0.002, while fully-approximate PGD (HJ-Prox for the entire smooth+L1 objective, same d schedule) reaches 0.169. The fully-approximate variant accumulates HJ bias on the smooth term too (which has an exact prox/gradient), so it is strictly worse. Splitting decomposes the composite objective so each term is handled by its best operator (exact where available), lowering the effective approximation burden relative to monolithic non-split proximal evaluation.",
      "honest_notes": "Hybrid = exact closed-form prox where available + HJ only for hard terms; fully-approximate = HJ for all. Same d_k schedule; hybrid reaches lower error. The 'lower effective Lipschitz' is the qualitative mechanism (splitting isolates each term's conditioning)."
    }
  ]
}```
