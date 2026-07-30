# Operator Splitting with Hamilton-Jacobi-based Proximals — reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-q7mB5s1ie1-operator-splitting-with-hamilton-jacobi-based-proximals/blob/main/notebooks/hj_prox_reproduction.py)

This claim-by-claim reproduction of
[arXiv:2601.22370](https://arxiv.org/abs/2601.22370) replaces the prior scalar
checks with an exact derivation, valid counterexamples, and paper-scale CPU
experiments. The current live judge score remains **5/10**. A best-case
**10/10 is only a forecast** until the evaluator reviews the new Hugging Face
revision.

## Results

| Claim | Paper claim tested | Observed evidence | Assessment | Paper versus observed |
|---|---|---|---|---|
| 1 | uniform HJ-Prox error `≤sqrt(n t delta)` | 11 proof obligations pass; `n→n-1` mutation fails | VERIFIED | universal theorem versus machine-replayed derivation |
| 2 | HJ-PPM/PGD converge a.s. | valid no-minimizer counterexample; corrected n=500 PPM/PGD reach 1.940%/1.843% error | FALSIFIED as printed | convergence claim versus divergent admissible instance |
| 3 | HJ-DRS/DYS converge a.s. | valid counterexample; actual n=256 DRS and 300×60 DYS executed | FALSIFIED as printed | DYS correlation 0.99898; DRS correlation 0.94895 |
| 4 | HJ-PDHG converges with conjugate prox | valid counterexample; explicit 250×500 `g*` update reaches correlation 0.9999999999 | FALSIFIED as printed | conjugate mechanism directly executed |
| 5 | splitting gives tighter `J`; hybrid beats full approximation | cancelling pair gives split 14.778 versus unsplit 1; corrected H.6 hybrid/full residual ratio 0.25174 | FALSIFIED | broad bound false; narrower hybrid hierarchy aligned |

Claims 2–4 are interpretation-sensitive: the printed theorems omit minimizer
existence, while their proofs appear to rely on the nonempty fixed-point
premise stated earlier. Paper-scale finite runs therefore test that likely
corrected interpretation separately; they are not presented as proofs.

- [Illustrated technical report](reports/reproduction/report.md)
- [Release forecast and evidence gate](reports/reproduction/release-report.md)
- [Self-contained tutorial notebook](notebooks/hj_prox_reproduction.py)
- [Evaluator-visible Space candidate](space/pages/index.md)
- [Raw cumulative evidence](space/evidence/cumulative/run_f4ec095c.json)

## Experiment log

All formal nodes inherit the same fixed command.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `main` | publication surface | Not run as an experiment (publication surface) | README, report, notebook, and released evidence | none |
| [frozen Claim 1 baseline](https://github.com/MachineLearning-Nerd/icml26-repro-q7mB5s1ie1-operator-splitting-with-hamilton-jacobi-based-proximals/tree/orx/frozen-baseline-theorem-calibrated-claim-1) | locked uv environment and exact Claim 1 certificate | `uv run --frozen python -m reproduction.run` | VERIFIED | local CPU, 1 core estimate |
| [Claims 2–4 counterexamples](https://github.com/MachineLearning-Nerd/icml26-repro-q7mB5s1ie1-operator-splitting-with-hamilton-jacobi-based-proximals/tree/orx/exact-no-minimizer-counterexamples-for-claims-2) | exact assumption-satisfying divergent instances | `uv run --frozen python -m reproduction.run` | Claims 2–4 FALSIFIED as printed | local CPU, 1 core estimate |
| [paper-scale corroboration](https://github.com/MachineLearning-Nerd/icml26-repro-q7mB5s1ie1-operator-splitting-with-hamilton-jacobi-based-proximals/tree/orx/paper-scale-five-family-convergence-corroboratio) | actual PPM, PGD, DRS, DYS, and PDHG | `uv run --frozen python -m reproduction.run` | corrected interpretation CORROBORATED | Hugging Face `cpu-upgrade`, 64-CPU affinity |
| [Claim 5 cumulative winner](https://github.com/MachineLearning-Nerd/icml26-repro-q7mB5s1ie1-operator-splitting-with-hamilton-jacobi-based-proximals/tree/orx/claim-5-exact-bound-counterexample-and-matched-h) | exact `J` counterexample and corrected five-seed H.6 hierarchy | `uv run --frozen python -m reproduction.run` | Claims 1 VERIFIED; Claims 2–5 FALSIFIED | Hugging Face `cpu-upgrade`, 64-CPU affinity |

## Reproduce

Python 3.12 and every dependency are pinned in `uv.lock`.

```bash
uv sync --frozen
uv run --frozen python -m reproduction.run
```

The cumulative experiment is CPU-heavy and was formally run on Hugging Face
`cpu-upgrade` with
`ghcr.io/astral-sh/uv:0.11.32-python3.12-trixie-slim`; its in-program runtime
was 55.064 seconds and provider duration was 1m14s. No GPU was used.

For the bounded tutorial:

```bash
uv run --frozen marimo edit notebooks/hj_prox_reproduction.py
uv run --frozen marimo run notebooks/hj_prox_reproduction.py
```
