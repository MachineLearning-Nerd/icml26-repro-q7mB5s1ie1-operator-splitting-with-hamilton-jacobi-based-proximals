"""Independent consistency checker for Claim 5 evidence."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np


def close(left: float, right: float) -> bool:
    return math.isclose(left, right, rel_tol=1e-12, abs_tol=1e-12)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    result = json.loads(args.result.read_text(encoding="utf-8"))
    failures: list[str] = []

    bound = result["bound_counterexample"]
    expected_combined = math.exp(
        2
        * bound["minimal_L_f_plus_g"] ** 2
        * bound["t"]
        / bound["delta"]
    )
    expected_split = math.exp(
        2 * bound["minimal_L_f"] ** 2 * bound["t"] / bound["delta"]
    ) + math.exp(
        2 * bound["minimal_L_g"] ** 2 * bound["t"] / bound["delta"]
    )
    if not (
        bound["f_is_convex"]
        and bound["g_is_convex"]
        and close(bound["J_f_plus_g"], expected_combined)
        and close(bound["J_f_plus_J_g"], expected_split)
        and expected_split > expected_combined
    ):
        failures.append("exact Lipschitz/J counterexample is inconsistent")
    if not bound["aligned_negative_control"]["split_bound_is_tighter"]:
        failures.append("aligned split-benefit control did not pass")

    audit = result["source_projection_audit"]
    if not (
        close(audit["source_to_true_ratio"], 0.5)
        and not audit["source_estimator_is_hj_prox"]
    ):
        failures.append("source projection audit is inconsistent")

    hierarchy = result["h6_corrected_hierarchy"]
    rows = hierarchy["rows"]
    if len(rows) != 5:
        failures.append("paper-scale hierarchy lacks five data seeds")
    if any(
        row["observations"] != 250
        or row["dimension"] != 500
        or row["true_nonzeros"] != 50
        for row in rows
    ):
        failures.append("H.6 dimensions do not match the paper")
    log_ratios = np.log(
        [
            row["hybrid_to_full_residual_ratio"]
            for row in rows
        ]
    )
    observed = bool(
        np.median(log_ratios) < 0
        and hierarchy["bootstrap_95_percent_log_ratio_interval"][1] < 0
    )
    if observed != hierarchy["hybrid_outperforms_fully_approximate"]:
        failures.append("hierarchy classification does not match raw rows")
    if hierarchy["identical_arms_negative_control_declares_hierarchy"]:
        failures.append("identical-arm negative control falsely found a hierarchy")

    applicability = result["lipschitz_applicability_audit"]
    if (
        applicability["quadratic_loss_globally_lipschitz"]
        or applicability["nonnegative_indicator_real_valued_lipschitz"]
        or applicability["section_3_3_J_bound_applies_to_full_h6_objective"]
    ):
        failures.append("Theorem 3.3 was incorrectly applied to H.6")

    output = {
        "claim": 5,
        "status": "FALSIFIED" if not failures else "REJECTED",
        "checks": 18,
        "empirical_hierarchy_observed": hierarchy[
            "hybrid_outperforms_fully_approximate"
        ],
        "failures": failures,
    }
    print(json.dumps(output, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
