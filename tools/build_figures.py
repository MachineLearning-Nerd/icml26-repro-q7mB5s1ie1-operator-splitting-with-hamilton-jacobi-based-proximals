"""Build deterministic report figures from the cumulative run evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


COLORS = {
    "exact": "#334155",
    "hybrid": "#059669",
    "full": "#dc2626",
    "ppm": "#2563eb",
    "pgd": "#7c3aed",
}


def save(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path, format="svg", metadata={"Date": None})
    plt.close()
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    empirical = evidence["empirical_raw"]
    claim5 = evidence["claim5_raw"]

    bound = claim5["bound_counterexample"]
    labels = ["cancelling pair\nf=x, g=-x", "aligned pair\nf=g=|x|"]
    unsplit = [
        bound["J_f_plus_g"],
        bound["aligned_negative_control"]["J_f_plus_g"],
    ]
    split = [
        bound["J_f_plus_J_g"],
        bound["aligned_negative_control"]["J_f_plus_J_g"],
    ]
    x = np.arange(2)
    width = 0.35
    plt.figure(figsize=(7.2, 4.2))
    plt.bar(x - width / 2, unsplit, width, label="unsplit $J_{f+g}$", color="#2563eb")
    plt.bar(x + width / 2, split, width, label="split $J_f+J_g$", color="#f97316")
    plt.yscale("log")
    plt.xticks(x, labels)
    plt.ylabel("theoretical constant (log scale)")
    plt.title("Splitting is not uniformly tighter")
    plt.legend(frameon=False)
    save(args.output / "headline_bound.svg")

    claim2 = empirical["claim2"]
    horizons = [row["iterations"] for row in claim2["horizon_results"]]
    ppm = [row["ppm_relative_solution_error"] for row in claim2["horizon_results"]]
    pgd = [row["pgd_relative_solution_error"] for row in claim2["horizon_results"]]
    plt.figure(figsize=(7.2, 4.2))
    plt.loglog(horizons, ppm, marker="o", label="HJ-PPM", color=COLORS["ppm"])
    plt.loglog(horizons, pgd, marker="s", label="HJ-PGD", color=COLORS["pgd"])
    plt.axhline(0.08, color=COLORS["ppm"], linestyle=":", alpha=0.7)
    plt.axhline(0.03, color=COLORS["pgd"], linestyle=":", alpha=0.7)
    plt.xlabel("iterations")
    plt.ylabel("relative solution error")
    plt.title("Claim 2: calibrated paper-scale convergence")
    plt.legend(frameon=False)
    plt.grid(alpha=0.2, which="both")
    save(args.output / "claim2_horizons.svg")

    agreement_labels = ["DRS\nn=256", "DYS\n300×60", "PDHG\n250×500"]
    correlations = [
        empirical["claim3_drs"]["reference_correlation"],
        empirical["claim3_dys"]["reference_correlation"],
        empirical["claim4"]["reference_correlation"],
    ]
    plt.figure(figsize=(7.2, 4.2))
    bars = plt.bar(agreement_labels, correlations, color=["#64748b", "#0d9488", "#7c3aed"])
    plt.ylim(0.9, 1.005)
    plt.ylabel("correlation with exact reference")
    plt.title("Intended splitting behavior at paper scale")
    for bar, value in zip(bars, correlations):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.002,
            f"{value:.4f}",
            ha="center",
            fontsize=9,
        )
    save(args.output / "splitting_agreement.svg")

    rows = claim5["h6_corrected_hierarchy"]["rows"]
    horizons5 = [point["iterations"] for point in rows[0]["hybrid_trace"]]
    for key, label, color in (
        ("exact_trace", "exact DYS", COLORS["exact"]),
        ("hybrid_trace", "hybrid HJ", COLORS["hybrid"]),
        ("fully_approximate_trace", "fully approximate HJ", COLORS["full"]),
    ):
        values = np.array(
            [
                [point["analytical_fixed_point_residual"] for point in row[key]]
                for row in rows
            ]
        )
        mean = np.mean(values, axis=0)
        low = np.min(values, axis=0)
        high = np.max(values, axis=0)
        plt.plot(horizons5, mean, marker="o", label=label, color=color)
        plt.fill_between(horizons5, low, high, color=color, alpha=0.12)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("iterations")
    plt.ylabel("exact DYS fixed-point residual")
    plt.title("Claim 5: hybrid beats fully approximate")
    plt.legend(frameon=False)
    plt.grid(alpha=0.2, which="both")
    save(args.output / "claim5_residuals.svg")

    seeds = [str(row["seed"]) for row in rows]
    hybrid_gap = [
        row["hybrid_objective"] - row["exact_objective"] for row in rows
    ]
    full_gap = [
        row["fully_approximate_objective"] - row["exact_objective"]
        for row in rows
    ]
    x = np.arange(len(rows))
    plt.figure(figsize=(7.2, 4.2))
    plt.bar(x - width / 2, hybrid_gap, width, label="hybrid", color=COLORS["hybrid"])
    plt.bar(x + width / 2, full_gap, width, label="fully approximate", color=COLORS["full"])
    plt.xticks(x, seeds)
    plt.xlabel("data seed")
    plt.ylabel("objective gap from exact DYS")
    plt.title("Matched H.6 objective gaps")
    plt.legend(frameon=False)
    save(args.output / "claim5_objective_gaps.svg")


if __name__ == "__main__":
    main()
