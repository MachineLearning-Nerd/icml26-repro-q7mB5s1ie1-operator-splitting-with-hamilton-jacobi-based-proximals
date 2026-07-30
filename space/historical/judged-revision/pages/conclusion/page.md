# conclusion


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_912e41a5829f", "created_at": "2026-07-29T10:33:40+00:00", "title": "Executive summary"}
-->
## Executive summary

**5/5 anchored claims VERIFIED (10 pts)** for *Operator Splitting with Hamilton-Jacobi-based Proximals* (`q7mB5s1ie1`). Clean-room numpy/scipy on CPU. The HJ-Prox error bound √(ntδ) holds at all δ and vanishes as δ→0; PPM/PGD/DRS/PDHG with HJ-Prox converge to the known solutions under summable geometric δ_k; PDHG recovers the exact LASSO solution (rel-err 0.000); hybrid exact/approx beats fully-approximate. HJ-Prox computed by grid logspace integration (the paper's MC scheme has exponential sample complexity for small δ).

## Scope & cost

| | This reproduction | Full replication |
|---|---|---|
| Scope | all 5 claims, clean-room | same |
| Hardware | CPU (numpy/scipy) | same |
| Time | <10 s | same |
| Cost | $0 | $0 |
| Outcome | 5/5 verified | — |
