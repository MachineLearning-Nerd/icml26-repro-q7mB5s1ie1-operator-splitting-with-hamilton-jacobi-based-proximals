"""Fixed cumulative reproduction entrypoint."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAIM1 = ROOT / ".openresearch" / "artifacts" / "claim1"


def cpu_allocation() -> int:
    if hasattr(os, "sched_getaffinity"):
        return len(os.sched_getaffinity(0))
    return os.cpu_count() or 1


def run_checker(certificate: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "reproduction.verify_claim1", str(certificate)],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )


def git_sha() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> int:
    started = time.perf_counter()
    metadata = {
        "fixed_command": "uv run --frozen python -m reproduction.run",
        "estimated_cores": 4,
        "selected_compute": "huggingface",
        "selected_flavor": "cpu-upgrade",
        "container_image": "ghcr.io/astral-sh/uv:0.11.32-python3.12-trixie-slim",
        "actual_cpu_allocation": cpu_allocation(),
        "process_max_threads": "uncapped within cpu-upgrade allocation",
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "seed": None,
    }
    print("RUN_METADATA " + json.dumps(metadata, sort_keys=True))

    accepted = run_checker(CLAIM1 / "proof_certificate.json")
    print("CLAIM1_CHECKER " + accepted.stdout.strip())
    if accepted.returncode != 0:
        print(accepted.stderr, file=sys.stderr)
        return 1

    rejected = run_checker(CLAIM1 / "negative_control_certificate.json")
    print("CLAIM1_NEGATIVE_CONTROL " + rejected.stdout.strip())
    if rejected.returncode == 0:
        print("negative control unexpectedly passed", file=sys.stderr)
        return 1

    from reproduction.empirical import write_result

    result_path = Path(tempfile.gettempdir()) / "hj_prox_empirical.json"
    result = write_result(result_path)
    print("EMPIRICAL_RAW " + json.dumps(result, sort_keys=True))
    empirical_check = subprocess.run(
        [sys.executable, "-m", "reproduction.verify_empirical", str(result_path)],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    print("EMPIRICAL_CHECKER " + empirical_check.stdout.strip())
    if empirical_check.returncode != 0:
        print(empirical_check.stderr, file=sys.stderr)
        return 1

    summary = {
        "claim_1": "VERIFIED",
        "claims_2_4_intended_interpretation": "CORROBORATED",
        "control": "EXPECTED_FAILURE",
        "runtime_seconds": round(time.perf_counter() - started, 6),
    }
    print("FINAL_SUMMARY " + json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
