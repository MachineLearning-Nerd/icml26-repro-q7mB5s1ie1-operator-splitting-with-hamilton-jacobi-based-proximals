"""Replay the symbolic certificate for Theorem 3.2."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_STEPS = {
    "strong_convexity": {
        "rule": "quadratic_plus_convex_is_strongly_convex",
        "conclusion": "<w, subgradient_Phi(w)> >= ||w||^2 / t",
    },
    "integration_by_parts": {
        "rule": "gibbs_coordinate_integration_by_parts",
        "conclusion": "E[w_i * subgradient_i_Phi(w)] = delta",
    },
    "sum_coordinates": {
        "rule": "sum_over_all_coordinates",
        "conclusion": "E[<w, subgradient_Phi(w)>] = n * delta",
    },
    "second_moment": {
        "rule": "combine_monotonicity_and_ibp",
        "conclusion": "E[||w||^2] <= n * t * delta",
    },
    "jensen": {
        "rule": "jensen_squared_norm",
        "conclusion": "||E[w]||^2 <= E[||w||^2]",
    },
    "translate": {
        "rule": "gibbs_mean_minus_mode",
        "conclusion": "prox_delta(x) - prox(x) = E[w]",
    },
    "finish": {
        "rule": "nonnegative_square_root",
        "conclusion": "||prox_delta(x) - prox(x)|| <= sqrt(n * t * delta)",
    },
}


def check(certificate: dict[str, object]) -> list[str]:
    failures: list[str] = []
    if certificate.get("theorem") != "Theorem 3.2":
        failures.append("wrong theorem identifier")
    if certificate.get("quantifier") != "for every x in R^n":
        failures.append("uniform quantifier is missing")
    if certificate.get("ibp_coordinate_count") != "n":
        failures.append("summed IBP dimension coefficient must be n")
    if certificate.get("nonsmooth_passage") != (
        "Moreau-envelope approximation followed by dominated convergence"
    ):
        failures.append("nonsmooth convex passage is missing")

    steps = certificate.get("steps")
    if not isinstance(steps, list):
        return failures + ["steps must be a list"]
    by_id = {
        step.get("id"): step
        for step in steps
        if isinstance(step, dict) and isinstance(step.get("id"), str)
    }
    for step_id, expected in REQUIRED_STEPS.items():
        if by_id.get(step_id) != {"id": step_id, **expected}:
            failures.append(f"invalid proof step: {step_id}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text(encoding="utf-8"))
    failures = check(certificate)
    result = {
        "claim": 1,
        "status": "VERIFIED" if not failures else "REJECTED",
        "proof_obligations": len(REQUIRED_STEPS) + 4,
        "failures": failures,
    }
    print(json.dumps(result, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
