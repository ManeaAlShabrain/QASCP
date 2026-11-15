"""Validate QASCP foundation documents and requirement traceability."""

import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
HANDBOOKS = (
    "docs/governance/ENGINEERING_GOVERNANCE.md",
    "docs/governance/ENGINEERING_GOVERNANCE.ar.md",
)
PROCEDURES = "docs/verification/PROCEDURES.md"
REGISTER = "docs/verification/requirements.json"
PRODUCT_REQUIREMENTS = "docs/product/QASCP_2_PRD.md"
PRODUCT_BACKLOG = "docs/product/QASCP_2_BACKLOG.md"
REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "SECURITY.md",
    *HANDBOOKS,
    "docs/governance/REGULATORY_SOURCES.md",
    "docs/architecture/P1_ARCHITECTURE.md",
    "docs/product/QASCP_PRODUCT_DESIGN.md",
    PRODUCT_REQUIREMENTS,
    PRODUCT_BACKLOG,
    "docs/architecture/QASCP_2_ARCHITECTURE.md",
    "docs/architecture/QASCP_2_CONTRACTS.md",
    "docs/architecture/QASCP_2_THREATS.md",
    "docs/architecture/QASCP_2_SUPERSESSION.md",
    "docs/governance/QASCP_2_COVERAGE.md",
    "docs/verification/QASCP_2_P1_LOCAL.md",
    "contracts/qascp-2/observation.schema.json",
    "contracts/qascp-2/normalized-observation.schema.json",
    "contracts/qascp-2/openapi.json",
    "contracts/qascp-2/trusted-context.schema.json",
    "contracts/qascp-2/audit-event.schema.json",
    "contracts/qascp-2/outbox-event.schema.json",
    "contracts/qascp-2/consumer-receipt.schema.json",
    "contracts/qascp-2/delivery-envelope.schema.json",
    "contracts/qascp-2/approval-lifecycle.schema.json",
    "docs/research/QASCP_PRIOR_ART.md",
    "docs/verification/README.md",
    PROCEDURES,
    REGISTER,
    ".github/pull_request_template.md",
    ".github/workflows/ci.yml",
    "tests/test_verify_foundation.py",
)
MARKDOWN_LINK = re.compile(r"\[[^\]\n]+\]\(([^\s)]+)\)")
STAGE_ROW = re.compile(r"(?m)^\| (P\d+) —")
REQUIREMENT_ID = re.compile(r"QASCP-[A-Z]+-\d{3}")
REQUIREMENT_HEADING = re.compile(r"(?m)^### (QASCP-[A-Z]+-\d{3}) — \S[^\n]*\n\n[^\s#]")
PRODUCT_REQUIREMENT_ID = re.compile(r"PRD-\d{2}")
PRODUCT_REQUIREMENT_ROW = re.compile(r"(?m)^\| (PRD-\d{2}) \|")
BACKLOG_ITEM = re.compile(r"(?m)^\| (V2-(P[1-6])-\d{2}) / (P[1-6]) \|")
VERIFICATION_HEADING = re.compile(r"(?m)^### (P[1-6]-V\d{2}) — \S")
VERSION = re.compile(r"(?m)^\[[^\]\n]+\]\([^)]+\) · (?:Version|الإصدار) (\d+\.\d+) · ")
PHASES = [f"P{number}" for number in range(1, 7)]


def verify_traceability(documents, problems):
    """Check agreement among the handbooks, verification procedures, and register."""
    try:
        register = json.loads(documents[REGISTER])
    except json.JSONDecodeError as error:
        problems.append(f"{REGISTER}: invalid JSON: {error.msg}")
        return

    if not isinstance(register, dict):
        problems.append(f"{REGISTER}: expected a JSON object")
        return
    version = register.get("baseline_version")
    entries = register.get("requirements")
    product_entries = register.get("product_requirements")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+", version):
        problems.append(f"{REGISTER}: invalid baseline_version")
        return
    if not isinstance(entries, list) or not entries:
        problems.append(f"{REGISTER}: expected a nonempty requirements list")
        return
    if not isinstance(product_entries, list) or not product_entries:
        problems.append(f"{REGISTER}: expected a nonempty product_requirements list")
        return

    verification_ids = VERIFICATION_HEADING.findall(documents[PROCEDURES])
    defined = set(verification_ids)
    if len(defined) != len(verification_ids):
        problems.append(f"{PROCEDURES}: duplicate verification IDs")
    if {identifier.split("-")[0] for identifier in defined} != set(PHASES):
        problems.append(f"{PROCEDURES}: verification methods must cover P1 through P6")

    requirement_ids = []
    referenced = set()
    for entry in entries:
        if not isinstance(entry, dict):
            problems.append(f"{REGISTER}: expected a requirement object")
            continue
        identifier = entry.get("id")
        if not isinstance(identifier, str) or not REQUIREMENT_ID.fullmatch(identifier):
            problems.append(f"{REGISTER}: invalid requirement ID {identifier!r}")
            continue
        requirement_ids.append(identifier)
        methods = entry.get("verification")
        if not isinstance(methods, list) or not methods or not all(
            isinstance(method, str) for method in methods
        ):
            problems.append(f"{identifier}: expected nonempty verification IDs")
            continue
        if len(set(methods)) != len(methods):
            problems.append(f"{identifier}: duplicate verification references")
        for method in methods:
            if method not in defined:
                problems.append(f"{identifier}: unknown verification ID {method}")
            referenced.add(method)

    if len(requirement_ids) != len(set(requirement_ids)):
        problems.append(f"{REGISTER}: duplicate requirement IDs")
    backlog_matches = BACKLOG_ITEM.findall(documents[PRODUCT_BACKLOG])
    backlog_phases = {}
    for identifier, id_phase, declared_phase in backlog_matches:
        if identifier in backlog_phases:
            problems.append(f"{PRODUCT_BACKLOG}: duplicate backlog ID {identifier}")
        backlog_phases[identifier] = declared_phase
        if id_phase != declared_phase:
            problems.append(f"{PRODUCT_BACKLOG}: phase mismatch for {identifier}")

    product_ids = []
    for entry in product_entries:
        if not isinstance(entry, dict):
            problems.append(f"{REGISTER}: expected a product requirement object")
            continue
        identifier = entry.get("id")
        if not isinstance(identifier, str) or not PRODUCT_REQUIREMENT_ID.fullmatch(identifier):
            problems.append(f"{REGISTER}: invalid product requirement ID {identifier!r}")
            continue
        product_ids.append(identifier)

        phases = entry.get("phases")
        if (
            not isinstance(phases, list)
            or not phases
            or not all(isinstance(phase, str) and phase in PHASES for phase in phases)
            or len(set(phases)) != len(phases)
            or phases != sorted(phases, key=PHASES.index)
        ):
            problems.append(f"{identifier}: invalid or unordered phase references")
            phases = []

        backlog = entry.get("backlog")
        if not isinstance(backlog, list) or not backlog or not all(
            isinstance(item, str) for item in backlog
        ):
            problems.append(f"{identifier}: expected nonempty backlog references")
            backlog = []
        elif len(set(backlog)) != len(backlog):
            problems.append(f"{identifier}: duplicate backlog references")
        for item in backlog:
            if item not in backlog_phases:
                problems.append(f"{identifier}: unknown backlog ID {item}")
            elif backlog_phases[item] not in phases:
                problems.append(
                    f"{identifier}: backlog ID {item} is outside mapped phases"
                )

        methods = entry.get("verification")
        if not isinstance(methods, list) or not methods or not all(
            isinstance(method, str) for method in methods
        ):
            problems.append(f"{identifier}: expected nonempty verification IDs")
            methods = []
        elif len(set(methods)) != len(methods):
            problems.append(f"{identifier}: duplicate verification references")
        for method in methods:
            if method not in defined:
                problems.append(f"{identifier}: unknown verification ID {method}")
            referenced.add(method)

    expected_product_ids = [f"PRD-{number:02d}" for number in range(1, 11)]
    if len(product_ids) != len(set(product_ids)):
        problems.append(f"{REGISTER}: duplicate product requirement IDs")
    if product_ids != expected_product_ids:
        problems.append(f"{REGISTER}: expected PRD-01 through PRD-10 once in order")
    if PRODUCT_REQUIREMENT_ROW.findall(documents[PRODUCT_REQUIREMENTS]) != product_ids:
        problems.append(
            f"{PRODUCT_REQUIREMENTS}: product requirement IDs or order differ from the register"
        )

    if unreferenced := sorted(defined - referenced):
        problems.append(f"{PROCEDURES}: unreferenced verification IDs: {', '.join(unreferenced)}")

    for handbook in HANDBOOKS:
        content = documents[handbook]
        if REQUIREMENT_HEADING.findall(content) != requirement_ids:
            problems.append(f"{handbook}: requirement IDs or order differ from the register")
        if STAGE_ROW.findall(content) != PHASES:
            problems.append(f"{handbook}: expected P1 through P6 once in order")
        if VERSION.findall(content) != [version]:
            problems.append(f"{handbook}: baseline version differs from the register")


def verify_foundation(root):
    """Return all detected validation problems for a repository checkout."""
    root = root.resolve()
    problems = []
    documents = {}
    for relative_path in REQUIRED_FILES:
        path = root / relative_path
        if not path.is_file() or not path.resolve().is_relative_to(root):
            problems.append(f"Missing or out-of-scope file: {relative_path}")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            problems.append(f"Unreadable file: {relative_path}: {error}")
            continue
        if not content.strip():
            problems.append(f"Empty file: {relative_path}")
            continue
        documents[relative_path] = content
        if path.suffix != ".md":
            continue
        for link in MARKDOWN_LINK.findall(content):
            try:
                target = urlsplit(link)
            except ValueError:
                problems.append(f"{relative_path}: invalid link {link}")
                continue
            if target.scheme or target.netloc or not target.path:
                continue
            resolved = (path.parent / unquote(target.path)).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                problems.append(f"{relative_path}: unresolved local link {link}")

    if all(path in documents for path in (*HANDBOOKS, PROCEDURES, REGISTER)):
        verify_traceability(documents, problems)
    return problems


def main():
    problems = verify_foundation(ROOT)
    if problems:
        print("\n".join(problems))
        return 1
    print("Foundation verified: required files, links, bilingual parity, governance and product requirement mappings, backlog references, and evidence references.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
