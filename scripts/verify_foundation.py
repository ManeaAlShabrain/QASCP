"""Validate the QASCP foundation files from any working directory."""

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE = "docs/governance/ENGINEERING_GOVERNANCE.md"
REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    GOVERNANCE,
    "docs/verification/README.md",
    ".github/pull_request_template.md",
    ".github/workflows/ci.yml",
)
MARKDOWN_LINK = re.compile(r"\[[^\]\n]+\]\(([^\s)]+)\)")
STAGE_ROW = re.compile(r"(?m)^\| (P[1-6]) —")


def main():
    problems = []
    for relative_path in REQUIRED_FILES:
        path = ROOT / relative_path
        if not path.is_file():
            problems.append(f"Missing {relative_path}")
            continue

        content = path.read_text(encoding="utf-8")
        if not content.strip():
            problems.append(f"Empty {relative_path}")
        if relative_path == GOVERNANCE:
            expected = [f"P{number}" for number in range(1, 7)]
            if STAGE_ROW.findall(content) != expected:
                problems.append("Governance must list P1 through P6 once in order.")
        if path.suffix != ".md":
            continue

        for link in MARKDOWN_LINK.findall(content):
            target = urlsplit(link)
            if target.scheme or target.netloc or not target.path:
                continue
            resolved = (path.parent / unquote(target.path)).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                problems.append(f"{relative_path}: unresolved local link {link}")

    if problems:
        print("\n".join(problems))
        return 1

    print("Foundation verified: required files, ordered stage records, and local document links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
