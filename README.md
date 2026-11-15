# QASCP

QASCP: Unified Cybersecurity, AI Security & Continuous Assurance Platform.

Enterprise cybersecurity and AI assurance for Qatar's financial sector.

## QASCP 2.0 product and architecture proposal

**One Platform. Every Security Domain. Continuous Assurance.**

The proposed enterprise-banking scope connects 24 security domains through a security knowledge graph, contextual reasoning, continuous assurance and human-controlled response orchestration. P1 remains active and pending review; the documents and contracts below do not represent delivered runtime features.

- [Product requirements, domain coverage and banking scenarios](docs/product/QASCP_2_PRD.md)
- [Architecture and proposed ADRs](docs/architecture/QASCP_2_ARCHITECTURE.md)
- [Domain, data and API contracts](docs/architecture/QASCP_2_CONTRACTS.md)
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

Run the current foundation check from the repository root.

```sh
python3 scripts/verify_foundation.py
python3 -m unittest discover -s tests -v
```

When initializing a new GitHub repository, select **Private**. Run the workflow on the default branch, then protect that branch with pull requests and the **QASCP Foundation Gate** required check on a plan that supports these rules for private repositories. Keep bypass access limited in accordance with the repository's governance. Treat workflow and gate changes as sensitive code review items.

To validate the GitHub rule once active, open a temporary PR containing a broken required documentation link, confirm the required check fails and blocks the merge, then repair the PR and confirm the check passes. Close the test PR. Record the real run links in the stage verification record.

The current gate checks foundations and documentation. Application, data-isolation, and cumulative regression jobs should be added as functioning components are delivered. The stage record requires separate review and linked evidence.
