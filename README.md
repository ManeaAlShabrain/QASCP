# QASCP

QASCP: Unified Cybersecurity, AI Security & Continuous Assurance Platform.

Enterprise cybersecurity and AI assurance for Qatar's financial sector.

## QASCP 2.0 product and architecture proposal

**One Platform. Every Security Domain. Continuous Assurance.**

The proposed enterprise-banking scope connects 24 security domains through a security knowledge graph, contextual reasoning, continuous assurance and human-controlled response orchestration. P1 remains active and pending review; the documents and contracts below do not represent delivered runtime features.

- [Product requirements, domain coverage and banking scenarios](docs/product/QASCP_2_PRD.md)
- [Architecture and proposed ADRs](docs/architecture/QASCP_2_ARCHITECTURE.md)
- [Domain, data and API contracts](docs/architecture/QASCP_2_CONTRACTS.md)
- [Security Knowledge Graph plan and diagrams](docs/architecture/QASCP_2_GRAPH_PLAN.md)
- [Graph boundary contracts and validation](docs/architecture/QASCP_2_GRAPH_BOUNDARY.md)
- [Consolidated P1 human-review package](docs/verification/QASCP_2_P1_REVIEW_PACKAGE.md)
- [P1 deliverables, all five work packages and remaining acceptance decisions](docs/verification/QASCP_2_P1_DELIVERY_PACKET.md)
- [P1 corrective actions, all nine audit findings and re-audit evidence](docs/verification/remediation/P1-2026-11-25/README.md)
- [Current repository review and resumption — 2026-11-25](docs/verification/QASCP_2_P1_REVIEW_2026-11-25.md)
- [Arabic continuity record and next steps](docs/product/QASCP_2_CONTINUITY_AR.md)
- [Threat and design-risk register](docs/architecture/QASCP_2_THREATS.md)
- [Document authority and supersession matrix](docs/architecture/QASCP_2_SUPERSESSION.md)
- [Framework coverage and pending applicability](docs/governance/QASCP_2_COVERAGE.md)
- [Phase-scoped implementation backlog](docs/product/QASCP_2_BACKLOG.md)
- [Observation JSON Schema](contracts/qascp-2/observation.schema.json) and [first-slice OpenAPI](contracts/qascp-2/openapi.json)

The [document authority and supersession matrix](docs/architecture/QASCP_2_SUPERSESSION.md) identifies every affected earlier section, ADR, scenario, component decision and backlog item as retained, refined, replaced or deprecated. The engineering governance handbooks remain binding, and [QASCP_2_BACKLOG.md](docs/product/QASCP_2_BACKLOG.md) is the canonical 2.0 backlog. See the [local change evidence](docs/verification/QASCP_2_P1_LOCAL.md) for actual checks and remaining review gaps.

## Foundation setup

- [Engineering governance and delivery handbook — English](docs/governance/ENGINEERING_GOVERNANCE.md)
- [دليل الحوكمة والتنفيذ — العربية](docs/governance/ENGINEERING_GOVERNANCE.ar.md)
- [P1 architecture, threat model, contracts, and backlog](docs/architecture/P1_ARCHITECTURE.md)
- [Product design and independent development](docs/product/QASCP_PRODUCT_DESIGN.md)
- [Market and patent reconnaissance](docs/research/QASCP_PRIOR_ART.md)
- [Regulatory and engineering source register](docs/governance/REGULATORY_SOURCES.md)
- [Verification procedures](docs/verification/PROCEDURES.md)
- [Security reporting](SECURITY.md)
- [Stage verification record](docs/verification/README.md)
- [Codex instructions](AGENTS.md)

Use the [supported clean verification setup](docs/verification/P1_VALIDATION_SETUP.md)
before running the complete suite. Linux x86_64 / CPython 3.14 is the full-check
target; install the hash-locked, wheels-only validator closure in a new venv first.
Native Windows also needs symbolic-link permission and a separate platform lock.

```sh
python3 -m venv .venv-contracts
.venv-contracts/bin/python -m pip install --disable-pip-version-check --no-input --index-url https://pypi.org/simple --no-deps --only-binary=:all: --require-hashes -r requirements-contracts-linux-cp314.lock
.venv-contracts/bin/python -m pip check
.venv-contracts/bin/python scripts/verify_foundation.py
.venv-contracts/bin/python scripts/verify_openapi_contracts.py
.venv-contracts/bin/python -m unittest discover -s tests -v
```

The current repository is public under **ManeaAlShabrain/QASCP**, following the owner's visibility and organization changes. The latest [review and resumption record](docs/verification/QASCP_2_P1_REVIEW_2026-11-25.md) records the active main ruleset and the controlled main-targeted failed/blocked and repaired-positive test. Required PRs and the **QASCP Foundation Gate** from GitHub Actions remain mandatory. Keep customer data and secrets outside public history, discussions, logs and fixtures. Before any later visibility or ownership change, assess disclosure, plan support, integration access and effective rules. Treat workflow and gate changes as sensitive code review items.

To validate the GitHub rule once active, open a temporary PR containing a broken required documentation link, confirm the required check fails and blocks the merge, then repair the PR and confirm the check passes. Close the test PR. Record the real run links in the stage verification record.

The current gate checks foundations and documentation. Application, data-isolation, and cumulative regression jobs should be added as functioning components are delivered. The stage record requires separate review and linked evidence.
