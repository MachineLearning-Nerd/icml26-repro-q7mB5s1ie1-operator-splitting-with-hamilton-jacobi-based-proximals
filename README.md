# Operator Splitting with Hamilton–Jacobi-based Proximals — independent reproduction

[![Open in Molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-operator-splitting-hamilton-jacobi-proximals/blob/main/notebooks/hj_prox_reproduction.py)

Independent reproduction and claim audit for **Operator Splitting with
Hamilton-Jacobi-based Proximals** by Nicholas Di, Eric C. Chi, and Samy Wu
Fung.

- Paper: [arXiv:2601.22370](https://arxiv.org/abs/2601.22370)
- Audited source: [arXiv:2601.22370v4](https://arxiv.org/abs/2601.22370v4)
- Clean repository: [MachineLearning-Nerd/icml26-operator-splitting-hamilton-jacobi-proximals](https://github.com/MachineLearning-Nerd/icml26-operator-splitting-hamilton-jacobi-proximals)
- Evaluator-visible candidate: [`space/pages`](space/pages/index.md)
- Reproduction command: `uv run --frozen python -m reproduction.run`

## What the paper does

The paper develops a unified operator-splitting framework that replaces exact
proximal operators with derivative-free Monte Carlo Hamilton–Jacobi proximal
(HJ-Prox) approximations. It analyzes HJ-Prox versions of proximal point,
proximal gradient, Douglas–Rachford, Davis–Yin, and primal-dual hybrid
gradient methods, and evaluates them on statistical learning problems.

## Reproduction status

The release evaluates five claim contracts. Claim 1 is supported by a
machine-replayed symbolic derivation. Claims 2–5 are **FALSIFIED as printed**
by exact assumption-satisfying counterexamples or an exact analytical
counterexample. The paper's likely intended nonempty-solution interpretation
is tested separately with finite experiments and is not confused with a proof
of the universal theorems.

| Release result | Meaning |
| --- | --- |
| Claim 1: **VERIFIED** | Eleven proof obligations pass and the `n→n-1` coefficient mutation is rejected. |
| Claims 2–4: **FALSIFIED as printed** | Each printed convergence statement admits an objective with no minimizer and a divergent admissible update. |
| Claim 5: **FALSIFIED** | The broad split-bound comparison has an exact convex Lipschitz counterexample; the corrected H.6 hierarchy is reported separately. |
| Blocked claims: none | Every contract has a terminal verdict. |
| Historical live judge: `5/10` | This remains the recorded score. |
| Projected score: `8–10/10` | Forecast only; a new score requires live evaluator review. |

The source audit pins the scientific claims to arXiv v4 retrieved on
2026-07-30 with SHA-256
`8e673443dd09f2952988fb9348c43f2b52d78442665d7b764e01586a8a7c5205`.
The current arXiv page is linked above for discovery; the repository does
not silently mix revisions.

## Claim-to-evidence map

The cumulative runner is [`reproduction/run.py`](reproduction/run.py). Each
claim has a contract, source audit, method, limitations, executable checker,
raw result, and negative control under
[`.openresearch/artifacts`](.openresearch/artifacts). The evaluator-facing
copies are under [`space/evidence`](space/evidence).

| Claim | Paper statement | How the result is produced | Verdict |
| --- | --- | --- | --- |
| 1. Uniform HJ-Prox error bound | For finite lower-semicontinuous convex `f:R^n→R`, `||prox^δ_t f(x)−prox_t f(x)|| ≤ √(n t δ)`. | [`verify_claim1.py`](reproduction/verify_claim1.py) independently replays 11 obligations: strong convexity, coordinatewise Gibbs integration by parts, the exact sum over `n` coordinates, Jensen, the prox translation, and the nonsmooth Moreau-envelope limit. | **VERIFIED** |
| 2. HJ-Prox PPM and PGD convergence | Theorems 3.5–3.6 claim almost-sure convergence to a minimizer under the printed convexity, Lipschitz, smoothness, step, and schedule assumptions. | [`verify_claims234.py`](reproduction/verify_claims234.py) uses `f(x)=0`, `g(x)=x`, `t_k=0.5/(k+1)`, summable HJ errors, and an explicit sample witness. The objective `F(x)=x` has no minimizer and the exact iterates drift by `x_(k+1)=x_k−t_k`. | **FALSIFIED as printed** |
| 3. HJ-Prox DRS and DYS convergence | Theorems 3.8–3.9 claim almost-sure convergence to minimizers of `f+g` or `f+g+h`. | The same checker uses `f=0`, `g(x)=x`, `h=0`, `t=0.5`, and valid `L'=1`; both displayed maps reduce to `state_(k+1)=state_k−t` with summable errors, while `F(x)=x` has no minimizer. | **FALSIFIED as printed** |
| 4. HJ-Prox PDHG convergence | Theorem 3.10 claims convergence of the conjugate-prox dual and primal updates when `τ σ ||A||²<1` and the printed schedules hold. | The checker uses `f(x)=x`, `g(y)=|y|`, `A=0`, and `τ=σ=0.5`. Since `g*` is the indicator of `[-1,1]`, the dual stays at zero while the primal drifts by `x_(k+1)=x_k−τ`; the objective has no minimizer. | **FALSIFIED as printed** |
| 5. Splitting bound and H.6 hierarchy | Section 3.3 says splitting substantially reduces `J`; Section 4.3 says hybrid DYS-HJ-1 outperforms fully approximate DYS-HJ-2. | [`claim5.py`](reproduction/claim5.py) checks `f(x)=x`, `g(x)=−x`: unsplit `J=1`, split `J_f+J_g=14.778112`, so the broad statement is false. It separately runs five matched `250×500` H.6-scale data sets using corrected population HJ operators and a paired bootstrap. | **FALSIFIED** |

### How verdicts are produced

1. Each contract fixes the paper version, theorem or section, assumptions,
   quantifiers, target, and verdict rule.
2. The source audit records the exact statement, omitted hypotheses, and
   any interpretation boundary.
3. The checker executes either a symbolic certificate, an exact
   counterexample, or a matched finite experiment.
4. Independent checker outputs and negative controls are stored beside the
   raw result. Invalid controls must be rejected; they are not optional
   demonstrations.
5. `reproduction.run` executes the cumulative suite and exits nonzero if any
   contract or control fails.

The word **“as printed”** is deliberate for Claims 2–4. The counterexamples
use the stated assumptions and show that the target set can be empty. The
source proof appears to rely on the nonempty fixed-point premise from an
earlier theorem; if that premise is intended implicitly, the result diagnoses
an omitted hypothesis rather than refuting the corrected theorem.

## Branches

`main` is the publication surface. The full historical-to-clean mapping is
in [branch-audit.md](branch-audit.md).

| Clean branch | Purpose |
| --- | --- |
| `audit/frozen-claim-1-baseline` | Freeze the locked environment and Claim 1 certificate. |
| `audit/no-minimizer-counterexamples` | Produce exact counterexamples for Claims 2–4. |
| `experiment/paper-scale-convergence` | Run PPM, PGD, DRS, DYS, and PDHG under the intended nonempty-solution interpretation. |
| `release/cumulative-theorem-verdicts` | Combine Claims 1–4 with paper-scale corroboration. |
| `audit/claim-5-bound-and-hybrid` | Audit the Claim 5 analytical counterexample and corrected H.6 hierarchy. |
| `release/publication-candidate` | Assemble evaluator-visible cumulative evidence. |
| `release/post-publication-evidence` | Record the published artifact, post-run evidence, and judge-waiting state. |

Branch names describe provenance and purpose; they do not determine a claim
verdict. Historical `orx/` names remain only in the branch audit.

## Repository map

| Path | Role |
| --- | --- |
| `reproduction/run.py` | Cumulative runner and result writer. |
| `reproduction/verify_claim1.py` | Symbolic Claim 1 certificate checker. |
| `reproduction/verify_claims234.py` | Exact Claims 2–4 assumption and recurrence checker. |
| `reproduction/empirical.py` | Paper-scale PPM, PGD, DRS, DYS, and PDHG implementations. |
| `reproduction/claim5.py` | Claim 5 `J` counterexample and corrected H.6 hierarchy. |
| `.openresearch/artifacts/claim1..claim5` | Contracts, source audits, methods, raw outputs, controls, and runtime records. |
| `.openresearch/artifacts/cumulative` | Cumulative runs and repeated red-team reviews. |
| `reports/reproduction` | Illustrated technical report and release forecast. |
| `space` | Evaluator-facing pages, evidence mirror, historical baseline, and visibility audit. |
| `notebooks/hj_prox_reproduction.py` | Self-contained marimo tutorial surface. |

## Reproduce locally

```bash
uv sync --frozen
uv run --frozen python -m reproduction.run
```

The accepted cumulative run used Python 3.12 with the locked dependencies,
Hugging Face `cpu-upgrade`, and no GPU. It reported `55.064` seconds of
in-program runtime and `1m14s` provider duration, with 64 CPUs visible to the
process and an estimate of eight useful cores. The cumulative raw run is
[`run_f4ec095c.json`](.openresearch/artifacts/cumulative/run_f4ec095c.json).

For the tutorial:

```bash
uv run --frozen marimo edit notebooks/hj_prox_reproduction.py
uv run --frozen marimo run notebooks/hj_prox_reproduction.py
```

## Scope and limitations

- Claim 1 uses a transparent specialized proof checker, not a general proof
  assistant kernel; trusted mathematical rules are documented in its source
  audit.
- Claims 2–4 are counterexamples to the printed universal statements. They
  become missing-hypothesis diagnoses if the nonempty fixed-point premise is
  intended implicitly.
- Paper-scale finite experiments corroborate the corrected interpretation;
  they do not prove almost-sure universal convergence.
- Claim 5's broad `J` comparison is falsified independently of the H.6
  experiment. The corrected H.6 run uses population HJ operators and 2,000
  approximate iterations rather than the paper's flawed finite-sample
  projection and 10,000 iterations.
- The paper's H.6 quadratic loss and extended-valued orthant indicator do not
  satisfy the global real-valued Lipschitz premise needed for a finite full
  objective `J`.
- This repository is an independent reproduction and is not author-endorsed.

## Citation

```bibtex
@article{di2026operator,
  title={Operator Splitting with Hamilton-Jacobi-based Proximals},
  author={Di, Nicholas and Chi, Eric C. and Wu Fung, Samy},
  journal={arXiv preprint arXiv:2601.22370},
  year={2026},
  doi={10.48550/arXiv.2601.22370}
}
```

## Thank you

Thank you to Nicholas Di, Eric C. Chi, and Samy Wu Fung for developing and
sharing this work. The paper's unified HJ-Prox perspective and public
artifacts made it possible to separate a symbolic approximation bound,
printed-theorem hypotheses, intended algorithm behavior, and practical
splitting experiments in a single reproducible audit.

Documentation, cleanup, and independent verification in this repository are
maintained by [MachineLearning-Nerd](https://github.com/MachineLearning-Nerd).
That attribution applies to this reproduction work and does not change the
provenance of the paper or the authors' artifacts.
