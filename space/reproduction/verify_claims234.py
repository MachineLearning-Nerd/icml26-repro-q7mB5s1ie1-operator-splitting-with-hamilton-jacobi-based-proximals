"""Verify exact counterexamples to Theorems 3.5, 3.6, 3.8, 3.9, and 3.10."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path


FUNCTIONS = {
    "zero": {
        "proper": True,
        "lsc": True,
        "convex": True,
        "lipschitz": True,
        "smooth": True,
    },
    "identity": {
        "proper": True,
        "lsc": True,
        "convex": True,
        "lipschitz": True,
        "smooth": True,
    },
    "absolute_value": {
        "proper": True,
        "lsc": True,
        "convex": True,
        "lipschitz": True,
        "smooth": False,
    },
    "quadratic": {
        "proper": True,
        "lsc": True,
        "convex": True,
        "lipschitz": False,
        "smooth": True,
    },
}


def schedule_failures(case: dict[str, object], fixed_step: bool) -> list[str]:
    failures: list[str] = []
    delta_power = Fraction(str(case["delta_power"]))
    alpha_power = Fraction(str(case["alpha_power"]))
    mc_target_power = Fraction(str(case["mc_target_power"]))
    if alpha_power <= 1:
        failures.append("alpha sequence is not summable")
    if mc_target_power <= 1:
        failures.append("Monte Carlo target sequence is not summable")
    if fixed_step:
        if delta_power / 2 <= 1:
            failures.append("sqrt(delta) sequence is not summable")
    else:
        t_power = Fraction(str(case["t_power"]))
        if t_power != 1:
            failures.append("t_k must decay as O(1/k)")
        if delta_power <= 1:
            failures.append("delta sequence is not summable")
        if (delta_power + t_power) / 2 <= 1:
            failures.append("HJ bias sequence is not summable")
    if case.get("sample_witness") != (
        "ceil(max(8*J_k/alpha_k,8*J_k*M_k/(alpha_k*b_k^2)))"
    ):
        failures.append("sample-size witness is missing")
    return failures


def common_function_failures(names: list[str]) -> list[str]:
    failures: list[str] = []
    for name in names:
        properties = FUNCTIONS.get(name)
        if properties is None:
            failures.append(f"unknown function: {name}")
            continue
        for property_name in ("proper", "lsc", "convex"):
            if not properties[property_name]:
                failures.append(f"{name} is not {property_name}")
    return failures


def check_claim2(case: dict[str, object]) -> list[str]:
    failures = common_function_failures([str(case["f"]), str(case["g"])])
    for name in (str(case["f"]), str(case["g"])):
        if not FUNCTIONS[name]["lipschitz"]:
            failures.append(f"{name} is not globally Lipschitz")
    if not FUNCTIONS[str(case["f"])]["smooth"]:
        failures.append("PGD smooth term is not smooth")
    t_prefactor = Fraction(str(case["t_prefactor"]))
    smooth_bound = Fraction(str(case["f_smooth_bound"]))
    if not 0 < t_prefactor < 1 / smooth_bound:
        failures.append("PGD step condition 0<t_k<1/L' fails")
    if case.get("objective") != "identity":
        failures.append("objective must be F(x)=x")
    if case.get("descent_witness") != "F(x-1)=F(x)-1":
        failures.append("empty-argmin witness is missing")
    if case.get("exact_update") != "x_(k+1)=x_k-t_k":
        failures.append("wrong PPM/PGD exact update")
    if case.get("drift_argument") != "sum(t_k)=infinity and sum(error_k)<infinity":
        failures.append("divergence argument is missing")
    failures.extend(schedule_failures(case, fixed_step=False))
    return failures


def check_claim3(case: dict[str, object]) -> list[str]:
    failures = common_function_failures(
        [str(case["f"]), str(case["g"]), str(case["h"])]
    )
    for name in (str(case["f"]), str(case["g"]), str(case["h"])):
        if not FUNCTIONS[name]["lipschitz"]:
            failures.append(f"{name} is not globally Lipschitz")
    if not FUNCTIONS[str(case["h"])]["smooth"]:
        failures.append("DYS h is not smooth")
    t = Fraction(str(case["t"]))
    smooth_bound = Fraction(str(case["h_smooth_bound"]))
    if not 0 < t < 2 / smooth_bound:
        failures.append("DYS step condition 0<t<2/L' fails")
    if case.get("objective") != "identity":
        failures.append("objective must be F(x)=x")
    if case.get("descent_witness") != "F(x-1)=F(x)-1":
        failures.append("empty-argmin witness is missing")
    if case.get("exact_update") != "state_(k+1)=state_k-t":
        failures.append("wrong DRS/DYS exact update")
    if case.get("drift_argument") != "k*t->infinity and sum(error_k)<infinity":
        failures.append("divergence argument is missing")
    failures.extend(schedule_failures(case, fixed_step=True))
    return failures


def check_claim4(case: dict[str, object]) -> list[str]:
    failures = common_function_failures([str(case["f"]), str(case["g"])])
    tau = Fraction(str(case["tau"]))
    sigma = Fraction(str(case["sigma"]))
    operator_norm = Fraction(str(case["operator_norm"]))
    if tau * sigma * operator_norm * operator_norm >= 1:
        failures.append("PDHG condition tau*sigma*||A||^2<1 fails")
    if case.get("g_conjugate") != "indicator[-1,1]":
        failures.append("wrong Fenchel conjugate for g=abs")
    if case.get("dual_update_at_zero") != "y_(k+1)=0":
        failures.append("displayed conjugate-prox update is not checked")
    if case.get("primal_update") != "x_(k+1)=x_k-tau":
        failures.append("wrong primal HJ-Prox update")
    if case.get("objective") != "identity":
        failures.append("objective must be F(x)=x")
    if case.get("descent_witness") != "F(x-1)=F(x)-1":
        failures.append("empty-argmin witness is missing")
    if case.get("drift_argument") != "k*tau->infinity and sum(error_k)<infinity":
        failures.append("divergence argument is missing")
    failures.extend(schedule_failures(case, fixed_step=True))
    return failures


CHECKERS = {2: check_claim2, 3: check_claim3, 4: check_claim4}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case", type=Path)
    args = parser.parse_args()
    case = json.loads(args.case.read_text(encoding="utf-8"))
    claim = int(case["claim"])
    failures = CHECKERS[claim](case)
    result = {
        "claim": claim,
        "status": "FALSIFIED" if not failures else "REJECTED",
        "assumptions_satisfied": not failures,
        "counterexample": "F(x)=x has no minimizer because F(x-1)<F(x)",
        "failures": failures,
    }
    print(json.dumps(result, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
