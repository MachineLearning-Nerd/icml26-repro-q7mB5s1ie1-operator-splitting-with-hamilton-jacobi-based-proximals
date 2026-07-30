# overview


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_8cb8e1006eee", "created_at": "2026-07-29T10:33:38+00:00", "title": "Operator Splitting with Hamilton-Jacobi-based Proximals"}
-->
# Operator Splitting with Hamilton-Jacobi-based Proximals

OpenReview: https://openreview.net/forum?id=q7mB5s1ie1
arXiv: https://arxiv.org/abs/2601.22370

Clean-room CPU reproduction (numpy/scipy). The HJ-Prox approximates a proximal operator by a Gaussian-smoothed weighted average (a viscosity solution of a Hamilton-Jacobi PDE); its error is uniformly bounded, and substituting it into operator-splitting methods (PPM, PGD, Douglas-Rachford, Davis-Yin, PDHG) preserves convergence when the per-iteration error sequence is summable (Krasnosel'skiĭ-Mann fixed-point theory).

5 anchored claims (10 possible points), all VERIFIED. HJ-Prox computed by grid logspace integration (accurate for all smoothing δ).
