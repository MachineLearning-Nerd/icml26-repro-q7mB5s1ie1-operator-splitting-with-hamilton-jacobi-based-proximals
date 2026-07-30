"""Evaluator-blind traversal of a candidate logbook tree."""

from __future__ import annotations

import argparse
import json
import re
from collections import deque
from pathlib import Path


LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def logbook_files(node: dict[str, object]) -> list[str]:
    files = [str(node["file"])]
    for child in node.get("children", []):
        files.extend(logbook_files(child))
    return files


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    root = args.candidate.resolve()
    logbook = json.loads((root / "logbook.json").read_text(encoding="utf-8"))
    queue = deque(["README.md", "logbook.json", *logbook_files(logbook["root"])])
    opened: list[str] = []
    missing: list[str] = []
    seen: set[str] = set()

    while queue:
        relative = queue.popleft()
        if relative in seen:
            continue
        seen.add(relative)
        path = (root / relative).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            missing.append(relative + " (escapes candidate)")
            continue
        if not path.is_file():
            missing.append(relative)
            continue
        opened.append(relative)
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            clean = target.split("#", 1)[0]
            linked = (path.parent / clean).resolve()
            try:
                queue.append(str(linked.relative_to(root)))
            except ValueError:
                missing.append(target + " (escapes candidate)")

    claim_checks: dict[str, list[str]] = {}
    required = (
        "Exact paper claim",
        "Verdict:",
        "checker",
        "control",
        "Limitations",
    )
    for claim in range(1, 6):
        relative = f"pages/current-claim-{claim}/page.md"
        text = (root / relative).read_text(encoding="utf-8")
        claim_checks[str(claim)] = [
            item for item in required if item.lower() not in text.lower()
        ]

    visibility = (root / "pages/visibility/page.md").read_text(encoding="utf-8")
    forbidden_visibility = [
        marker
        for marker in ("| no |", "pending", "BLOCKED")
        if marker.lower() in visibility.lower()
    ]

    result = {
        "candidate": str(root),
        "entrypoints": ["README.md", "logbook.json", logbook["root"]["file"]],
        "opened_files": sorted(opened),
        "missing_links": sorted(set(missing)),
        "claim_page_missing_fields": claim_checks,
        "visibility_forbidden_markers": forbidden_visibility,
        "status": "PASS"
        if not missing
        and not any(claim_checks.values())
        and not forbidden_visibility
        else "FAIL",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
