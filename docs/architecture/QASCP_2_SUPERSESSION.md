# QASCP 2.0 — Document authority and supersession matrix

Current2026-11-27: [ADR-P1-ACCEPTANCE-001](ADR-P1-ACCEPTANCE-001.md)
and P1_CONTRACT_SELECTION.json define the concrete review candidate. The dated
proposal/rationale below is preserved; no earlier pending state is relabeled as
a later approval. Owner ratification and P1 exit remain separate.

This P1 record is the authoritative map between the earlier P1 design package and the QASCP 2.0 proposal. The English and Arabic engineering governance handbooks remain the binding authority for governance requirements and phase gates. The verification register remains the machine-readable requirement-to-evidence authority. [QASCP_2_BACKLOG.md](../product/QASCP_2_BACKLOG.md) is the canonical QASCP 2.0 backlog.

The states below mean: **retained** remains applicable without changing its authority; **refined** remains applicable with the linked 2.0 detail controlling where the two differ; **replaced** is no longer the active product or component definition; **deprecated** remains only as a historical identifier and must not be opened as new work.

## Architecture, product and component authority

| Earlier source | State | QASCP 2.0 authority and effect |
|---|---|---|
| P1 architecture — product scope and prioritized scenarios | Refined | [QASCP 2.0 PRD](../product/QASCP_2_PRD.md) controls the 24-domain target scope and BANK-01..06 sequencing. The defensive-source, tenant-isolation and no-model-execution boundaries are retained. |
| P1 architecture — scope boundaries and pilot success | Retained | Separate approval for banking source domains, agreed measurement denominators and no control of bank transactions remain binding design constraints. The 2.0 PRD adds an unapproved laboratory profile. |
| P1 architecture — domain coverage register | Replaced | The coverage and sequencing tables in the 2.0 PRD are the active product roadmap. [QASCP_2_COVERAGE.md](../governance/QASCP_2_COVERAGE.md) controls capability-to-source/evidence mapping without making compliance claims. |
| P1 architecture — identity, integration, persistence, AI and evidence boundaries | Refined | [QASCP_2_ARCHITECTURE.md](QASCP_2_ARCHITECTURE.md) and [QASCP_2_CONTRACTS.md](QASCP_2_CONTRACTS.md) add trusted internal contexts, delivery contracts, digest ownership and the approval/execution lifecycle. The original boundary invariants remain applicable. |
| P1 architecture — domain contracts | Refined | The 2.0 contracts document and versioned JSON contracts are the active static contract definitions. Earlier entity invariants remain minimum requirements. |
| P1 architecture — interface contracts | Refined | The 2.0 contracts document, OpenAPI and JSON Schemas control the first-slice interface. Interfaces absent from the static contract package are not authorized for implementation. |
| P1 architecture — defensive threat model | Refined | [QASCP_2_THREATS.md](QASCP_2_THREATS.md) is the active threat and design-risk register. Earlier threats remain applicable when their surface is delivered. |
| Product design — investigate, assess impact, reverify and review history | Retained | The workflow, evidence lineage, historical cutoff and conservative selective re-verification semantics remain applicable. The 2.0 PRD refines navigation and bilingual acceptance. |
| Product design — proposed technical mechanism | Retained | Dual time, complete-dependency preconditions, broader reconciliation and version conflict handling remain design invariants for P5. |
| Product design — earlier product identity/navigation | Refined | The 2.0 PRD controls command-center navigation and the explicit RTL/LTR, accessibility, authorization, export and historical-view acceptance criteria. |

## ADR and component decision authority

| Earlier decision | State | QASCP 2.0 decision |
|---|---|---|
| ADR-001 modular monolith and PostgreSQL | Refined | ADR-2-001 selects a FastAPI modular monolith and preserves the measured split criterion. |
| ADR-002 tenant-scoped relational keys and row-level controls | Retained | The 2.0 reliability invariants add composite foreign keys, non-bypass application roles and transaction-scoped context reset. |
| ADR-003 evidence object storage | Refined | ADR-2-004 selects S3-compatible encrypted storage and adds orphan, retention, authorization and restore evidence. |
| ADR-004 separate AI recommendation, decision and execution | Refined | ADR-2-005 plus the P4 approval lifecycle contracts add exact approval binding, single-use consumption, synthetic executor denial tests and audit behavior. Full assurance orchestration remains P5. |
| ADR-005 defer specialized search, graph and queue infrastructure | Refined | ADR-2-002, ADR-2-003 and ADR-2-007 use PostgreSQL graph/search first and introduce broker/workers only when asynchronous delivery begins. |
| Generic model endpoint component | Replaced | ADR-2-005 selects a local model plus tenant-scoped retrieval for the proposed design; authorization, provenance, injection controls and abstention remain mandatory regardless of deployment. |
| Generic event intake contract | Replaced | The external connector request, trusted normalized envelope, adapter-computed received-payload digest and delivery contracts in the 2.0 package are authoritative. |

## Backlog identifier migration

The earlier backlog rows are replaced by the canonical 2.0 backlog. Their identifiers are deprecated after this mapping; they remain searchable history, not parallel work queues.

| Earlier item | State | Canonical successor |
|---|---|---|
| B-P1-01 architecture, scenarios and contracts | Deprecated | V2-P1-01 and V2-P1-02 |
| B-P1-02 bilingual equivalence and applicability | Deprecated | V2-P1-03 |
| B-P1-03 GitHub gate failure and enforcement | Deprecated | V2-P1-04 |
| B-P1-04 P1 decision | Deprecated | V2-P1-05 |
| B-P2-01 scoped asset and event integration | Deprecated | V2-P2-01 through V2-P2-06 |
| B-P3-01 correlation and replay | Deprecated | V2-P3-01 and V2-P3-02 |
| B-P4-01 AI and approval boundaries | Deprecated | V2-P4-01 and V2-P4-02 |
| B-P5-01 evidence lifecycle | Deprecated | V2-P5-01 through V2-P5-03 |
| B-P6-01 release evaluation | Deprecated | V2-P6-01 |

## Change control

A later document may change this authority map only through the governed P1/P-stage change process, with requirement IDs, affected interfaces, evidence and review. An ambiguity is resolved in favor of the binding handbooks and the more restrictive tenant, authorization, audit and human-approval boundary until an authorized change reconciles the documents.
