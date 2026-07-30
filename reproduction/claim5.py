"""Exact and paper-scale checks for the splitting-efficiency claim."""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.special import log_ndtr

from reproduction.empirical import hj_l1_population, soft_threshold


SEEDS = [26051, 26052, 26053, 26054, 26055]
HORIZONS = [1, 10, 100, 500, 1000, 2000]


def fixed_point_residual(
    state: np.ndarray,
    design: np.ndarray,
    response: np.ndarray,
    lam: float,
    step: float,
) -> float:
    projected = np.maximum(state, 0)
    gradient = design.T @ (design @ projected - response)
    proximal = soft_threshold(
        2 * projected - state - step * gradient,
        step * lam,
    )
    return float(np.linalg.norm(proximal - projected))


def hj_nonnegative_population(
    x: np.ndarray,
    t: float,
    delta: float,
) -> np.ndarray:
    sigma = math.sqrt(t * delta)
    standardized = x / sigma
    log_density = (
        -0.5 * standardized * standardized - 0.5 * math.log(2 * math.pi)
    )
    correction = sigma * np.exp(
        np.clip(log_density - log_ndtr(standardized), -700, 700)
    )
    return np.maximum(x + correction, 0)


def setup(seed: int) -> tuple[np.ndarray, np.ndarray, float, float]:
    rng = np.random.default_rng(seed)
    observations, dimension, nonzeros = 250, 500, 50
    design = rng.normal(size=(observations, dimension))
    design -= design.mean(axis=0, keepdims=True)
    design /= np.linalg.norm(design, axis=0, keepdims=True) + 1e-12
    truth = np.zeros(dimension)
    support = rng.choice(dimension, size=nonzeros, replace=False)
    truth[support] = rng.uniform(1, 2, size=nonzeros) * 2.5
    response = design @ truth + rng.normal(scale=0.5, size=observations)
    response -= response.mean()
    return design, response, 0.5, 0.0025


def run_dys(
    design: np.ndarray,
    response: np.ndarray,
    lam: float,
    step: float,
    mode: str,
    iterations: int,
    delta: float,
) -> tuple[np.ndarray, list[dict[str, float | int]]]:
    state = np.zeros(design.shape[1])
    trace: list[dict[str, float | int]] = []
    horizon_set = set(HORIZONS)
    for k in range(iterations):
        if mode == "fully_approximate":
            proximal_first = hj_nonnegative_population(state, step, delta)
        else:
            proximal_first = np.maximum(state, 0)

        gradient = design.T @ (design @ proximal_first - response)
        reflected = 2 * proximal_first - state - step * gradient
        if mode == "exact":
            proximal_second = soft_threshold(reflected, step * lam)
        else:
            proximal_second = hj_l1_population(
                reflected,
                step,
                delta,
                lam,
            )
        state += proximal_second - proximal_first
        if k + 1 in horizon_set:
            trace.append(
                {
                    "iterations": k + 1,
                    "analytical_fixed_point_residual": fixed_point_residual(
                        state,
                        design,
                        response,
                        lam,
                        step,
                    ),
                }
            )
    return state, trace


def objective(
    state: np.ndarray,
    design: np.ndarray,
    response: np.ndarray,
    lam: float,
) -> float:
    beta = np.maximum(state, 0)
    residual = design @ beta - response
    return float(0.5 * residual @ residual + lam * np.sum(beta))


def bound_counterexample() -> dict[str, object]:
    t, delta = 0.1, 0.1
    component_lipschitz = 1.0
    combined_lipschitz = 0.0
    combined_j = math.exp(2 * combined_lipschitz**2 * t / delta)
    split_j = 2 * math.exp(2 * component_lipschitz**2 * t / delta)

    aligned_control_combined_j = math.exp(2 * 2.0**2 * t / delta)
    aligned_control_split_j = split_j
    return {
        "domain": "R",
        "f": "f(x)=x",
        "g": "g(x)=-x",
        "f_is_convex": True,
        "g_is_convex": True,
        "minimal_L_f": component_lipschitz,
        "minimal_L_g": component_lipschitz,
        "minimal_L_f_plus_g": combined_lipschitz,
        "t": t,
        "delta": delta,
        "J_f_plus_g": combined_j,
        "J_f_plus_J_g": split_j,
        "split_bound_is_tighter": split_j < combined_j,
        "counterexample_contradicts_broad_tighter_bound_statement": (
            split_j > combined_j
        ),
        "aligned_negative_control": {
            "f": "abs(x)",
            "g": "abs(x)",
            "minimal_L_f_plus_g": 2.0,
            "J_f_plus_g": aligned_control_combined_j,
            "J_f_plus_J_g": aligned_control_split_j,
            "split_bound_is_tighter": (
                aligned_control_split_j < aligned_control_combined_j
            ),
        },
    }


def source_projection_audit() -> dict[str, object]:
    step, delta = 0.0025, 0.1
    sigma = math.sqrt(step * delta)
    true_hj = sigma * math.sqrt(2 / math.pi)
    source_estimator_expectation = sigma / math.sqrt(2 * math.pi)
    return {
        "source_repository_commit": "895067559f4786c471a763811d949b3ae1f7377b",
        "source_file": "dys_constrained_lasso.ipynb",
        "audit_point": "one dimension, z=0",
        "true_hj_nonnegative_value": true_hj,
        "source_estimator_expectation": source_estimator_expectation,
        "source_to_true_ratio": source_estimator_expectation / true_hj,
        "source_estimator_is_hj_prox": False,
        "reason": "source divides feasible numerator by N instead of feasible mass",
    }


def hierarchy() -> dict[str, object]:
    delta = 0.1
    rows = []
    for seed in SEEDS:
        design, response, lam, step = setup(seed)
        exact_state, exact_trace = run_dys(
            design,
            response,
            lam,
            step,
            "exact",
            10000,
            delta,
        )
        hybrid_state, hybrid_trace = run_dys(
            design,
            response,
            lam,
            step,
            "hybrid",
            HORIZONS[-1],
            delta,
        )
        full_state, full_trace = run_dys(
            design,
            response,
            lam,
            step,
            "fully_approximate",
            HORIZONS[-1],
            delta,
        )
        exact_objective = objective(
            exact_state,
            design,
            response,
            lam,
        )
        hybrid_residual = fixed_point_residual(
            hybrid_state,
            design,
            response,
            lam,
            step,
        )
        full_residual = fixed_point_residual(
            full_state,
            design,
            response,
            lam,
            step,
        )
        rows.append(
            {
                "seed": seed,
                "observations": 250,
                "dimension": 500,
                "true_nonzeros": 50,
                "lambda": lam,
                "step": step,
                "delta": delta,
                "exact_reference_iterations": 10000,
                "approximate_iterations": HORIZONS[-1],
                "exact_objective": exact_objective,
                "hybrid_objective": objective(
                    hybrid_state,
                    design,
                    response,
                    lam,
                ),
                "fully_approximate_objective": objective(
                    full_state,
                    design,
                    response,
                    lam,
                ),
                "hybrid_analytical_fixed_point_residual": hybrid_residual,
                "fully_approximate_analytical_fixed_point_residual": full_residual,
                "hybrid_to_full_residual_ratio": (
                    hybrid_residual / (full_residual + 1e-300)
                ),
                "exact_trace": exact_trace,
                "hybrid_trace": hybrid_trace,
                "fully_approximate_trace": full_trace,
            }
        )

    paired_log_ratios = np.log(
        [
            row["hybrid_to_full_residual_ratio"]
            for row in rows
        ]
    )
    bootstrap_rng = np.random.default_rng(26050)
    draws = bootstrap_rng.choice(
        paired_log_ratios,
        size=(10000, len(paired_log_ratios)),
        replace=True,
    )
    bootstrap_means = np.mean(draws, axis=1)
    confidence_interval = np.quantile(bootstrap_means, [0.025, 0.975])
    hierarchy_observed = bool(
        np.median(paired_log_ratios) < 0 and confidence_interval[1] < 0
    )
    identical_control = np.zeros(len(rows))
    return {
        "paper_scale": "250 observations x 500 variables, 50 positive nonzeros",
        "fixed_delta": delta,
        "population_hj_used": True,
        "finite_sample_N": None,
        "deviation": (
            "correct population HJ operators replace the paper source's "
            "non-normalized projection estimator; 2000 approximate iterations "
            "replace the paper's 10000"
        ),
        "rows": rows,
        "geometric_mean_hybrid_to_full_residual_ratio": float(
            np.exp(np.mean(paired_log_ratios))
        ),
        "bootstrap_95_percent_log_ratio_interval": [
            float(confidence_interval[0]),
            float(confidence_interval[1]),
        ],
        "hybrid_outperforms_fully_approximate": hierarchy_observed,
        "identical_arms_negative_control_declares_hierarchy": bool(
            np.median(identical_control) < 0
        ),
    }


def run_all() -> dict[str, object]:
    started = time.perf_counter()
    result = {
        "claim": 5,
        "verdict": "FALSIFIED",
        "bound_counterexample": bound_counterexample(),
        "source_projection_audit": source_projection_audit(),
        "h6_corrected_hierarchy": hierarchy(),
        "lipschitz_applicability_audit": {
            "quadratic_loss_globally_lipschitz": False,
            "nonnegative_indicator_real_valued_lipschitz": False,
            "section_3_3_J_bound_applies_to_full_h6_objective": False,
            "l1_component_L": 0.5 * math.sqrt(500),
            "conclusion": (
                "No finite full-objective J constant exists under Theorem 3.3 "
                "for H.6, so a numerical finite Lipschitz reduction there "
                "would be invalid."
            ),
        },
    }
    result["runtime_seconds"] = time.perf_counter() - started
    return result


def write_result(path: Path) -> dict[str, object]:
    result = run_all()
    path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result
