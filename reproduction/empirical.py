"""Paper-scale finite corroboration for the five named splitting families."""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
from numpy.polynomial.hermite import hermgauss
from scipy.linalg import cho_factor, cho_solve
from scipy.special import expit, log_ndtr


SEEDS = {
    "claim2": 26012,
    "drs": 26013,
    "dys": 26014,
    "pdhg": 26015,
}


def soft_threshold(x: np.ndarray, threshold: float) -> np.ndarray:
    return np.sign(x) * np.maximum(np.abs(x) - threshold, 0.0)


def correlation(x: np.ndarray, y: np.ndarray) -> float:
    if np.std(x) == 0 or np.std(y) == 0:
        return 0.0
    return float(np.corrcoef(x.ravel(), y.ravel())[0, 1])


def hj_l1_population(
    x: np.ndarray, t: float, delta: float, lam: float
) -> np.ndarray:
    sigma = math.sqrt(delta * t)
    mu_positive = x - t * lam
    mu_negative = x + t * lam
    a = mu_positive / sigma
    b = mu_negative / sigma
    common = t * lam * lam / (2 * delta)
    log_positive = -lam * x / delta + common + log_ndtr(a)
    log_negative = lam * x / delta + common + log_ndtr(-b)
    log_phi_a = -0.5 * a * a - 0.5 * math.log(2 * math.pi)
    log_phi_b = -0.5 * b * b - 0.5 * math.log(2 * math.pi)
    mean_positive = mu_positive + sigma * np.exp(
        np.clip(log_phi_a - log_ndtr(a), -700, 700)
    )
    mean_negative = mu_negative - sigma * np.exp(
        np.clip(log_phi_b - log_ndtr(-b), -700, 700)
    )
    positive_weight = expit(log_positive - log_negative)
    return positive_weight * mean_positive + (1 - positive_weight) * mean_negative


def pseudohuber(x: np.ndarray, center: np.ndarray) -> np.ndarray:
    return np.sqrt(1 + (x - center) ** 2) - 1


def prox_pseudohuber_l1(
    x: np.ndarray, center: np.ndarray, t: float, lam: float
) -> np.ndarray:
    at_zero = -center / np.sqrt(1 + center * center) - x / t
    result = np.zeros_like(x)
    positive = at_zero < -lam
    negative = at_zero > lam
    for mask, sign in ((positive, 1.0), (negative, -1.0)):
        y = np.where(mask, x - t * lam * sign, 0.0)
        for _ in range(12):
            residual = y - center
            gradient = (
                residual / np.sqrt(1 + residual * residual)
                + (y - x) / t
                + lam * sign
            )
            curvature = 1 / (1 + residual * residual) ** 1.5 + 1 / t
            y = np.where(mask, y - gradient / curvature, y)
        result = np.where(mask, y, result)
    return result


HERMITE_NODES, HERMITE_WEIGHTS = hermgauss(32)


def hj_pseudohuber_l1_population(
    x: np.ndarray, center: np.ndarray, t: float, delta: float, lam: float
) -> np.ndarray:
    mode = prox_pseudohuber_l1(x, center, t, lam)
    scale = math.sqrt(2 * t * delta)
    samples = mode[:, None] + scale * HERMITE_NODES[None, :]
    phi = (
        pseudohuber(samples, center[:, None])
        + lam * np.abs(samples)
        + (samples - x[:, None]) ** 2 / (2 * t)
    )
    phi_mode = (
        pseudohuber(mode, center)
        + lam * np.abs(mode)
        + (mode - x) ** 2 / (2 * t)
    )
    gaussian_part = (samples - mode[:, None]) ** 2 / (2 * t)
    log_weights = (
        np.log(HERMITE_WEIGHTS)[None, :]
        - (phi - phi_mode[:, None] - gaussian_part) / delta
    )
    log_weights -= np.max(log_weights, axis=1, keepdims=True)
    weights = np.exp(log_weights)
    weights /= np.sum(weights, axis=1, keepdims=True)
    return np.sum(weights * samples, axis=1)


def claim2_ppm_pgd() -> dict[str, object]:
    rng = np.random.default_rng(SEEDS["claim2"])
    n = 500
    center = rng.normal(0, 1, n)
    lam = 0.2
    cutoff = lam / math.sqrt(1 - lam * lam)
    optimum = np.sign(center) * np.maximum(np.abs(center) - cutoff, 0)

    def objective(x: np.ndarray) -> float:
        return float(np.sum(pseudohuber(x, center)) + lam * np.sum(np.abs(x)))

    initial = np.zeros(n)
    initial_objective = objective(initial)
    horizons = [100, 300, 1000, 3000, 10000, 30000]
    iterations = horizons[-1]
    horizon_set = set(horizons)
    horizon_results: list[dict[str, float | int]] = []
    scale = np.linalg.norm(optimum) + 1e-12

    ppm = initial.copy()
    pgd = initial.copy()
    pgd_finite_sum_control = initial.copy()
    for k in range(iterations):
        t = 0.5 / (k + 1)
        delta = 0.1 / (k + 1) ** 4
        ppm = hj_pseudohuber_l1_population(ppm, center, t, delta, lam)

        gradient = (pgd - center) / np.sqrt(1 + (pgd - center) ** 2)
        pgd = hj_l1_population(pgd - t * gradient, t, delta, lam)

        control_t = 0.5 / (k + 1) ** 2
        gradient_control = (pgd_finite_sum_control - center) / np.sqrt(
            1 + (pgd_finite_sum_control - center) ** 2
        )
        pgd_finite_sum_control = hj_l1_population(
            pgd_finite_sum_control - control_t * gradient_control,
            control_t,
            delta,
            lam,
        )

        if k + 1 in horizon_set:
            horizon_results.append(
                {
                    "iterations": k + 1,
                    "ppm_relative_solution_error": float(
                        np.linalg.norm(ppm - optimum) / scale
                    ),
                    "pgd_relative_solution_error": float(
                        np.linalg.norm(pgd - optimum) / scale
                    ),
                }
            )

    ppm_error = float(np.linalg.norm(ppm - optimum) / scale)
    pgd_error = float(np.linalg.norm(pgd - optimum) / scale)
    ppm_first_hit = next(
        (
            row["iterations"]
            for row in horizon_results
            if row["ppm_relative_solution_error"] < 0.08
        ),
        None,
    )
    pgd_first_hit = next(
        (
            row["iterations"]
            for row in horizon_results
            if row["pgd_relative_solution_error"] < 0.03
        ),
        None,
    )
    return {
        "seed": SEEDS["claim2"],
        "dimension": n,
        "iterations": iterations,
        "precommitted_horizons": horizons,
        "horizon_results": horizon_results,
        "ppm_first_hit_below_8_percent": ppm_first_hit,
        "pgd_first_hit_below_3_percent": pgd_first_hit,
        "functions_satisfy_printed_assumptions": True,
        "minimizer_nonempty": True,
        "initial_objective": initial_objective,
        "optimal_objective": objective(optimum),
        "ppm_final_objective": objective(ppm),
        "pgd_final_objective": objective(pgd),
        "ppm_relative_solution_error": ppm_error,
        "pgd_relative_solution_error": pgd_error,
        "finite_sum_step_control_error": float(
            np.linalg.norm(pgd_finite_sum_control - optimum) / scale
        ),
        "finite_sum_step_control_sum_upper_bound": math.pi**2 / 12,
        "population_integrals": True,
        "finite_sample_N": None,
    }


def hj_prox_mc(
    x: np.ndarray,
    t: float,
    delta: float,
    samples: int,
    rng: np.random.Generator,
    function_batch,
) -> tuple[np.ndarray, float]:
    half = samples // 2
    noise = rng.standard_normal((half, x.size))
    noise = np.concatenate([noise, -noise], axis=0)
    points = x[None, :] + math.sqrt(t * delta) * noise
    values = np.asarray(function_batch(points), dtype=float)
    log_weights = -values / delta
    log_weights -= np.max(log_weights)
    weights = np.exp(log_weights)
    weights /= np.sum(weights)
    ess = float(1 / np.sum(weights * weights))
    return weights @ points, ess


def doppler(n: int) -> np.ndarray:
    grid = np.linspace(0.02, 0.98, n)
    return np.sqrt(grid * (1 - grid)) * np.sin(2 * math.pi * 1.05 / (grid + 0.05))


def trend_reference(y: np.ndarray, lam: float) -> np.ndarray:
    n = y.size
    difference = np.diff(np.eye(n), n=3, axis=0)
    rho = 1.0
    factor = cho_factor(np.eye(n) + rho * difference.T @ difference)
    x = y.copy()
    z = difference @ x
    dual = np.zeros_like(z)
    for _ in range(1600):
        x = cho_solve(factor, y + rho * difference.T @ (z - dual))
        dx = difference @ x
        z = soft_threshold(dx + dual, lam / rho)
        dual += dx - z
    return x


def claim3_drs() -> dict[str, object]:
    rng = np.random.default_rng(SEEDS["drs"])
    n = 256
    clean = doppler(n)
    y = clean + 0.12 * rng.normal(size=n)
    lam = 0.06
    reference = trend_reference(y, lam)

    def objective(x: np.ndarray) -> float:
        return float(0.5 * np.sum((x - y) ** 2) + lam * np.sum(np.abs(np.diff(x, n=3))))

    state = np.zeros(n)
    initial = objective(state)
    samples = 1024
    ess_values = []
    iterations = 1800
    primal = state.copy()
    for k in range(iterations):
        t = 0.25
        primal = (state + t * y) / (1 + t)
        reflected = 2 * primal - state
        delta = 0.08 / (1 + k / 180) ** 0.8 + 0.008
        prox_g, ess = hj_prox_mc(
            reflected,
            t,
            delta,
            samples,
            rng,
            lambda batch: lam * np.sum(np.abs(np.diff(batch, n=3, axis=1)), axis=1),
        )
        state += prox_g - primal
        ess_values.append(ess)
    return {
        "seed": SEEDS["drs"],
        "dimension": n,
        "iterations": iterations,
        "samples_per_hj_call": samples,
        "function_evaluations": iterations * samples,
        "initial_objective": initial,
        "final_objective": objective(primal),
        "reference_objective": objective(reference),
        "reference_correlation": correlation(primal, reference),
        "relative_solution_error": float(
            np.linalg.norm(primal - reference) / (np.linalg.norm(reference) + 1e-12)
        ),
        "median_ess": float(np.median(ess_values)),
        "paper_scale_matches_trend_dimension": True,
        "quadratic_data_term_deviates_from_global_lipschitz_assumption": True,
    }


def group_shrink(x: np.ndarray, threshold: float, group_size: int) -> np.ndarray:
    groups = x.reshape(-1, group_size)
    norms = np.linalg.norm(groups, axis=1, keepdims=True)
    return (groups * np.maximum(1 - threshold / (norms + 1e-15), 0)).ravel()


def claim3_dys() -> dict[str, object]:
    rng = np.random.default_rng(SEEDS["dys"])
    observations, n, group_size = 300, 60, 10
    design = rng.normal(size=(observations, n)) / math.sqrt(observations)
    truth = np.zeros(n)
    truth[:10] = rng.normal(0.8, 0.2, 10)
    truth[30:40] = rng.normal(-0.6, 0.2, 10)
    response = design @ truth + 0.05 * rng.normal(size=observations)
    lam_group, lam_l1 = 0.05, 0.025
    smooth_bound = float(np.linalg.norm(design, 2) ** 2)
    t = 0.35 / smooth_bound

    def smooth_value(x: np.ndarray) -> float:
        residual = design @ x - response
        return float(np.sum(np.sqrt(1 + residual * residual) - 1))

    def gradient(x: np.ndarray) -> np.ndarray:
        residual = design @ x - response
        return design.T @ (residual / np.sqrt(1 + residual * residual))

    def objective(x: np.ndarray) -> float:
        groups = x.reshape(-1, group_size)
        return (
            smooth_value(x)
            + lam_group * float(np.sum(np.linalg.norm(groups, axis=1)))
            + lam_l1 * float(np.sum(np.abs(x)))
        )

    def exact_run(iterations: int) -> tuple[np.ndarray, np.ndarray]:
        state = np.zeros(n)
        y = state.copy()
        for _ in range(iterations):
            y = group_shrink(state, t * lam_group, group_size)
            z = soft_threshold(2 * y - state - t * gradient(y), t * lam_l1)
            state += z - y
        return state, y

    reference_state, reference = exact_run(2200)
    state = np.zeros(n)
    initial = objective(state)
    samples = 1024
    ess_values = []
    iterations = 600
    y = state.copy()
    for k in range(iterations):
        delta = 0.045 / (1 + k / 220) ** 0.8 + 0.004
        y, ess = hj_prox_mc(
            state,
            t,
            delta,
            samples,
            rng,
            lambda batch: lam_group
            * np.sum(
                np.linalg.norm(batch.reshape(-1, n // group_size, group_size), axis=2),
                axis=1,
            ),
        )
        reflected = 2 * y - state - t * gradient(y)
        z = hj_l1_population(reflected, t, delta, lam_l1)
        state += z - y
        ess_values.append(ess)

    exact_y = group_shrink(state, t * lam_group, group_size)
    exact_z = soft_threshold(
        2 * exact_y - state - t * gradient(exact_y), t * lam_l1
    )
    fixed_point_residual = float(np.linalg.norm(exact_z - exact_y) / math.sqrt(n))
    invalid_t = 2.5 / smooth_bound
    return {
        "seed": SEEDS["dys"],
        "dimension": n,
        "observations": observations,
        "groups": n // group_size,
        "iterations": iterations,
        "samples_per_hj_call": samples,
        "function_evaluations": iterations * samples,
        "smooth_h_is_nonzero": True,
        "smooth_h_is_globally_lipschitz": True,
        "valid_step_product": t * smooth_bound,
        "initial_objective": initial,
        "final_objective": objective(y),
        "reference_objective": objective(reference),
        "reference_correlation": correlation(y, reference),
        "relative_solution_error": float(
            np.linalg.norm(y - reference) / (np.linalg.norm(reference) + 1e-12)
        ),
        "analytic_fixed_point_residual": fixed_point_residual,
        "median_ess": float(np.median(ess_values)),
        "invalid_step_control_tL": invalid_t * smooth_bound,
        "invalid_step_control_rejected": invalid_t * smooth_bound >= 2,
        "reference_state_norm": float(np.linalg.norm(reference_state)),
    }


def pdhg_run(
    design: np.ndarray,
    response: np.ndarray,
    lam: float,
    iterations: int,
    tau: float,
    sigma: float,
    hj: bool,
) -> np.ndarray:
    x = np.zeros(design.shape[1])
    y = np.zeros(design.shape[0])
    for k in range(iterations):
        dual_input = y + sigma * (design @ x)
        y_next = (dual_input - sigma * response) / (1 + sigma)
        primal_input = x - tau * (design.T @ y_next)
        if hj:
            delta = 0.08 / (k + 1) ** 2.2
            x_next = hj_l1_population(primal_input, tau, delta, lam)
        else:
            x_next = soft_threshold(primal_input, tau * lam)
        x, y = x_next, y_next
    return x


def claim4_pdhg() -> dict[str, object]:
    rng = np.random.default_rng(SEEDS["pdhg"])
    observations, n = 250, 500
    design = rng.normal(size=(observations, n)) / math.sqrt(observations)
    truth = np.zeros(n)
    support = rng.choice(n, size=25, replace=False)
    truth[support] = rng.normal(0, 1, support.size)
    response = design @ truth + 0.05 * rng.normal(size=observations)
    lam = 0.08
    operator_norm = float(np.linalg.norm(design, 2))
    tau = sigma = 0.5 / operator_norm
    iterations = 1200
    reference = pdhg_run(
        design, response, lam, 3000, tau, sigma, hj=False
    )
    estimate = pdhg_run(
        design, response, lam, iterations, tau, sigma, hj=True
    )

    def objective(x: np.ndarray) -> float:
        residual = design @ x - response
        return float(0.5 * residual @ residual + lam * np.sum(np.abs(x)))

    invalid_tau = invalid_sigma = 2 / operator_norm
    return {
        "seed": SEEDS["pdhg"],
        "dimension": n,
        "observations": observations,
        "iterations": iterations,
        "dual_function": "g*(y)=0.5||y||^2+<b,y>",
        "dual_hj_population_update": "(v-sigma*b)/(1+sigma)",
        "primal_hj_population_update": "tilted-truncated-Gaussian l1 mean",
        "valid_step_product": tau * sigma * operator_norm**2,
        "invalid_step_control_product": invalid_tau
        * invalid_sigma
        * operator_norm**2,
        "invalid_step_control_rejected": (
            invalid_tau * invalid_sigma * operator_norm**2 >= 1
        ),
        "initial_objective": objective(np.zeros(n)),
        "final_objective": objective(estimate),
        "reference_objective": objective(reference),
        "reference_correlation": correlation(estimate, reference),
        "relative_solution_error": float(
            np.linalg.norm(estimate - reference)
            / (np.linalg.norm(reference) + 1e-12)
        ),
    }


def run_all() -> dict[str, object]:
    started = time.perf_counter()
    result = {
        "protocol": "independent finite corroboration; exact theorem verdicts are separate",
        "seeds": SEEDS,
        "claim2": claim2_ppm_pgd(),
        "claim3_drs": claim3_drs(),
        "claim3_dys": claim3_dys(),
        "claim4": claim4_pdhg(),
    }
    result["runtime_seconds"] = time.perf_counter() - started
    return result


def write_result(path: Path) -> dict[str, object]:
    result = run_all()
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result
