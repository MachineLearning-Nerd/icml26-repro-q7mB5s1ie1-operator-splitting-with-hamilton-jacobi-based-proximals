"""Prepare the exact text-only Space upload and integrity records."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPACE = ROOT / "space"
RELEASE = ROOT / ".openresearch" / "release"
JUDGED = SPACE / "historical" / "judged-revision"
TEXT_SUFFIXES = {
    "",
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".sha256",
    ".svg",
    ".txt",
}
UPLOAD_EXCLUSIONS = {
    "historical/judged-revision/MANIFEST.sha256",
}
SECRET_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "huggingface_token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "assigned_secret": re.compile(
        r"(?i)(api[_-]?key|access[_-]?token|password)\s*[:=]\s*['\"][^'\"]{8,}"
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def judged_entries() -> list[tuple[str, str]]:
    entries = []
    for line in (JUDGED / "MANIFEST.sha256").read_text().splitlines():
        digest, relative = line.split(maxsplit=1)
        entries.append((digest, relative.removeprefix("*").removeprefix("./")))
    return entries


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def text_uploads() -> list[str]:
    paths = []
    for path in SPACE.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(SPACE).as_posix()
        if relative in UPLOAD_EXCLUSIONS:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            path.read_text(encoding="utf-8")
            paths.append(relative)
    return sorted(paths)


def main() -> None:
    RELEASE.mkdir(parents=True, exist_ok=True)
    entries = judged_entries()
    candidate_files = {
        path.relative_to(SPACE).as_posix()
        for path in SPACE.rglob("*")
        if path.is_file()
    }
    old_paths = {relative for _, relative in entries}
    missing = sorted(old_paths - candidate_files)

    protected = []
    mismatched = []
    for expected, relative in entries:
        root_path = SPACE / relative
        historical_path = JUDGED / relative
        preserved_path = (
            root_path if root_path.suffix.lower() == ".png" else historical_path
        )
        actual = sha256(preserved_path)
        if actual != expected:
            mismatched.append(relative)
        protected.append(
            {
                "judged_path": relative,
                "judged_sha256": expected,
                "preserved_at": preserved_path.relative_to(SPACE).as_posix(),
                "preserved_sha256": actual,
            }
        )

    subset = {
        "candidate_file_count": len(candidate_files),
        "judged_file_count": len(old_paths),
        "missing_judged_paths": missing,
        "status": "PASS" if not missing else "FAIL",
    }
    preservation = {
        "judged_revision": "ae7327ad0ea3f7ba2e3ca2ccb8fcba3282753785",
        "entries": protected,
        "mismatched_hashes": mismatched,
        "status": "PASS" if not mismatched else "FAIL",
    }
    write_json(SPACE / "evidence" / "release" / "subset_check.json", subset)
    write_json(
        SPACE / "evidence" / "release" / "protected_revision.json",
        preservation,
    )

    scanned = text_uploads()
    findings = []
    for relative in scanned:
        if relative == "evidence/release/secret_scan.json":
            continue
        text = (SPACE / relative).read_text(encoding="utf-8")
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                findings.append({"path": relative, "pattern": name})
    secret_scan = {
        "findings": findings,
        "scanner_output_excluded_from_self_scan": (
            "evidence/release/secret_scan.json"
        ),
        "scanned_file_count": len(scanned),
        "status": "PASS" if not findings else "FAIL",
    }
    write_json(
        SPACE / "evidence" / "release" / "secret_scan.json",
        secret_scan,
    )

    uploads = text_uploads()
    allowlist = "".join(f"{relative}\n" for relative in uploads)
    manifest = "".join(
        f"{sha256(SPACE / relative)}  {relative}\n" for relative in uploads
    )
    (RELEASE / "upload-allowlist.txt").write_text(allowlist)
    (RELEASE / "upload-manifest.sha256").write_text(manifest)
    write_json(RELEASE / "historical-subset.json", subset)
    write_json(RELEASE / "protected-revision.json", preservation)
    write_json(RELEASE / "secret-scan.json", secret_scan)

    status = (
        "PASS"
        if subset["status"] == preservation["status"] == secret_scan["status"]
        else "FAIL"
    )
    print(
        json.dumps(
            {
                "allowlisted_text_files": len(uploads),
                "protected_revision": preservation["status"],
                "secret_scan": secret_scan["status"],
                "subset_check": subset["status"],
                "status": status,
            },
            sort_keys=True,
        )
    )
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
