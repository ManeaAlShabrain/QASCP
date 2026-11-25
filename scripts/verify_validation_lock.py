"""Fail if version pins, wheel hashes and retained provenance disagree."""

from pathlib import Path
import re

if __package__:
    from .verify_foundation import strict_json_loads
else:
    from verify_foundation import strict_json_loads


ROOT = Path(__file__).resolve().parents[1]


def verify_lock(root=ROOT):
    pins = {}
    for line in (root / "requirements-contracts.txt").read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            match = re.fullmatch(r"([A-Za-z0-9_-]+)==([0-9][A-Za-z0-9.]*)", line.strip())
            if not match or match[1].lower() in pins:
                raise ValueError("Invalid or duplicate dependency pin")
            pins[match[1].lower()] = match[2]
    entries = {}
    for line in (root / "requirements-contracts-linux-cp314.lock").read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            match = re.fullmatch(r"([A-Za-z0-9_-]+)==([0-9][A-Za-z0-9.]*) --hash=sha256:([a-f0-9]{64})", line.strip())
            if not match or match[1].lower() in entries:
                raise ValueError("Invalid or duplicate wheel lock")
            entries[match[1].lower()] = (match[2], match[3])
    evidence = strict_json_loads((root / "docs/verification/remediation/P1-2026-11-25/dependency-evidence.json").read_text(encoding="utf-8"))
    packages = evidence["packages"]
    expected = {p["name"].lower(): (p["version"], p["sha256"]) for p in packages}
    if len(expected) != len(packages) or not pins or entries != expected or pins != {k: v[0] for k, v in entries.items()}:
        raise ValueError("Dependency pins, wheel lock and provenance disagree")
    return len(entries)


if __name__ == "__main__":
    print(f"Validation wheel lock matches all {verify_lock()} pins and retained artifact hashes")
