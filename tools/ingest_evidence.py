"""Copy structured evidence from an orx run log into evaluator-visible JSON."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


PREFIXES = (
    "RUN_METADATA",
    "CLAIM1_CHECKER",
    "CLAIM1_NEGATIVE_CONTROL",
    "CLAIM2_CHECKER",
    "CLAIM2_NEGATIVE_CONTROL",
    "CLAIM3_CHECKER",
    "CLAIM3_NEGATIVE_CONTROL",
    "CLAIM4_CHECKER",
    "CLAIM4_NEGATIVE_CONTROL",
    "EMPIRICAL_RAW",
    "EMPIRICAL_CHECKER",
    "CLAIM5_RAW",
    "CLAIM5_CHECKER",
    "FINAL_SUMMARY",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_id")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    completed = subprocess.run(
        ["orx", "logs", args.run_id, "--bytes", "300000"],
        check=True,
        capture_output=True,
        text=True,
    )
    evidence: dict[str, object] = {"run_id": args.run_id}
    for line in completed.stdout.splitlines():
        for prefix in PREFIXES:
            marker = prefix + " "
            if line.startswith(marker):
                evidence[prefix.lower()] = json.loads(line[len(marker) :])
                break

    missing = [prefix.lower() for prefix in PREFIXES if prefix.lower() not in evidence]
    if missing:
        raise SystemExit(f"missing log records: {', '.join(missing)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
