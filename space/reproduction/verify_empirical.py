"""Independent acceptance checks for the paper-scale finite corroboration."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    result = json.loads(args.result.read_text(encoding="utf-8"))
    failures: list[str] = []

    claim2 = result["claim2"]
    if claim2["dimension"] != 500:
        failures.append("Claim 2 dimension is not paper-scale 500")
    if not (
        claim2["ppm_final_objective"] < claim2["initial_objective"]
        and claim2["pgd_final_objective"] < claim2["initial_objective"]
    ):
        failures.append("PPM/PGD did not improve the objective")
    if claim2["ppm_relative_solution_error"] >= 0.08:
        failures.append("PPM solution error exceeds 8%")
    if claim2["pgd_relative_solution_error"] >= 0.03:
        failures.append("PGD solution error exceeds 3%")
    if claim2["ppm_first_hit_below_8_percent"] is None:
        failures.append("PPM never crossed the precommitted 8% threshold")
    if claim2["pgd_first_hit_below_3_percent"] is None:
        failures.append("PGD never crossed the precommitted 3% threshold")
    if (
        claim2["finite_sum_step_control_error"]
        <= claim2["pgd_relative_solution_error"] + 0.05
    ):
        failures.append("finite-sum step control did not materially degrade")

    drs = result["claim3_drs"]
    if drs["dimension"] != 256:
        failures.append("DRS does not match paper trend-filtering dimension")
    if not (
        drs["final_objective"] < drs["initial_objective"]
        and drs["reference_correlation"] > 0.9
    ):
        failures.append("DRS lacks objective improvement or reference agreement")

    dys = result["claim3_dys"]
    if not dys["smooth_h_is_nonzero"]:
        failures.append("DYS smooth h term is missing")
    if not (dys["valid_step_product"] < 2 and dys["invalid_step_control_rejected"]):
        failures.append("DYS step boundary control failed")
    if not (
        dys["final_objective"] < dys["initial_objective"]
        and dys["reference_correlation"] > 0.95
        and dys["analytic_fixed_point_residual"] < 0.08
    ):
        failures.append("DYS lacks convergence/reference evidence")

    pdhg = result["claim4"]
    if "g*" not in pdhg["dual_function"]:
        failures.append("PDHG conjugate update is not explicit")
    if not (
        pdhg["valid_step_product"] < 1
        and pdhg["invalid_step_control_rejected"]
        and pdhg["reference_correlation"] > 0.98
        and pdhg["final_objective"] < pdhg["initial_objective"]
    ):
        failures.append("PDHG mechanism, step control, or convergence check failed")

    output = {
        "status": "CORROBORATED" if not failures else "REJECTED",
        "checks": 16,
        "failures": failures,
    }
    print(json.dumps(output, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
