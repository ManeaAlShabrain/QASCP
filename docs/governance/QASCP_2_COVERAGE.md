# QASCP 2.0 — Framework coverage and applicability

P1 design mapping for PRD-07 / QASCP-CMP-001 / P1-V01. These are proposed capability associations, not clause-level compliance assessments. No source text is redistributed. The [source register](REGULATORY_SOURCES.md) is authoritative for source identity, edition, rights, access and applicability status. This file owns only the proposed capability-to-control and evidence mapping.

| Source/version reference | Capability-to-control association | Planned evidence |
|---|---|---|
| REF-NIST-CSF / CSF 2.0 | Inventory, governance, detection, response and recovery | Resource ownership, cases, control results and recovery tests |
| REF-NIST-AI / AI RMF 1.0 | AI inventory, accountable decisions and evaluations | Model/policy versions, risk reviews and evaluation records |
| REF-NIST-SSDF / SP 800-218 v1.1 | Secure implementation and build provenance | Reviewed dependencies, CI, SBOM and artifact digest |
| REF-MITRE-ATTACK / version pending | Threat and detection context | Version-pinned technique references and authorized detection evidence |
| REF-MITRE-ATLAS / version pending | AI threat scenarios | Version-pinned scenario references and adversarial evaluation |
| REF-OWASP-ASVS / edition pending | Application and API verification | Authentication, authorization and validation test results |
| REF-OWASP-AI / publication pending | LLM and agent boundary review | Injection, disclosure and tool-permission evaluations |
| QA-QCB-AI / 2024, commencement 2024-09-04; amendments pending | Banking AI governance and evidence | AI owner, use-case review, model evaluation and decisions |
| QA-QCB-DHP / title inspected; edition/date pending | Data and evidence handling | Classification, purpose, location, retention and access tests |
| QA-QCB-CLOUD / commencement 2024-04-15; revision pending | Cloud and outsourcing boundaries | Approved deployment, vendor, access and location review |
| QA-QCB-BANK / exact instruction pending | Banking obligations discovery | Licensed-entity scope and exact instruction/circular review |
| QA-NCSA-PDP / exact texts pending | Personal-data processing | Role, purpose, minimization, retention and rights-workflow evidence |
| QA-NCSA-NIA / V2.1, May 2023; currency pending | Institutional assurance | Scoped control observations and reviewer decisions |
| QA-QFMA-RULES / exact rules pending | Regulated capital-market activities | License-specific source review |
| QA-QFC-DP / exact texts pending | QFC data-protection context | Jurisdiction and processing-role assessment |

SWIFT, payment and open-banking use cases do not establish applicability of a particular contractual scheme or regulatory requirement. Add exact authoritative source, edition, rights and clauses before making a specialized mapping.

The [2026-11-17 source review](QASCP_2_SOURCE_REVIEW_2026-11-17.md) records selected primary-text observations and remaining scope/rights questions. Improved source identity does not resolve entity applicability or approve a clause-level mapping.

## Unresolved mapping review

Exact clauses and control identifiers remain pending wherever the source/version reference says pending or unverified. SWIFT, payment and open-banking scenarios remain product contexts, not regulatory applicability decisions. The designated regulatory reviewer must first resolve the authoritative source entry, entity/license, deployment and data scope in the source register; only then may this mapping add clause-level associations. No source hashes or clause conclusions are inferred here.

Required mapping record: source ID, issuer, title, edition, clause, effective date, retrieved date, permitted snapshot/hash, usage rights, entity license, jurisdiction, deployment/data scope, mandatory/advisory basis, QASCP control, evidence IDs, assessment state, reviewer decision and next review. Unknown fields remain pending. A source outage blocks adopting an unverified source conclusion, while independent product design can continue.
