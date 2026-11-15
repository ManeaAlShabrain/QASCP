# QASCP P1 architecture and product definition

This document proposes decisions for P1 review. Implementation choices and numerical performance targets require approval and evidence at the phase stated in the handbook. The first tenanted pilot focuses on financial-sector security assurance in Qatar. Product coverage grows through P6. QASCP will initially consume findings and events only from authorized defensive sources or synthetic test environments.

See the [product design](../product/QASCP_PRODUCT_DESIGN.md) for the proposed workflow and measurable differentiation, and the [prior-art search record](../research/QASCP_PRIOR_ART.md) for public comparisons.

## Product scope and prioritized scenarios

| Priority | Actor and outcome | Observable acceptance | Phase |
|---|---|---|---|
| 1 | SOC analyst registers an asset, imports a security event, and sees its audit trail within the institution. | The event resolves to the correct tenant asset, duplicate ingestion has one logical effect, and another tenant cannot observe it. | P2 |
| 2 | SOC analyst groups authorized findings and identities into a case suitable for triage. | Use a labeled dataset with reproducible precision and recall, preserve ambiguous matches for review, and compare against the existing workflow. | P3 |
| 3 | Model-risk reviewer evaluates a model recommendation with evidence and explicit uncertainty. | Retrieval stays within an authorized tenant and the result abstains when the evidence is insufficient. | P4 |
| 4 | Control owner sees an expired security artifact, reviews a remedial proposal, and verifies the outcome. | A versioned case links the evidence, decision, result, and independent verification. | P5 |
| 5 | Operational and compliance owners review release and client readiness. | Restore and upgrade evidence, operational measurements, and scoped regulatory decisions are reproducible and approved. | P6 |

Product domains are tenants and membership, assets and ownership, event intake, identities and findings, cases and risk, AI governance, controls and approvals, evidence and audit, reporting, resilience, and regulated deployment. Reporting and compliance reviews consume evidence with provenance. No use case permits automatic changes to customer production systems by a model.

## Scope boundaries and pilot success

The authorized banking pilot uses one scoped security data connector after P1 acceptance. Core banking, payment, SWIFT, ATMs, digital channels, open-banking APIs, and fraud platforms may become separately approved source domains. Connecting each domain requires its own data classification, access and operational review. The product does not assume control of transactions or customer operations.

Pilot success is evaluated by time to triage, proportion of correctly linked assets, and completeness of case evidence against a versioned dataset and an agreed baseline. A pilot is eligible for review after the client and project owner agree on scope, permission boundaries, expected outcomes, and thresholds. Each measurement records the denominator, failed cases, limitations, and the tested revision.

## Domain coverage register

The table records design coverage and the earliest planned delivery phases. P1 reviews boundaries and dependencies. The specific implementations and acceptance criteria are established within the authorized phase.

| Area | Domains in the product roadmap | First intended evidence |
|---|---|---|
| Security operations and defense | SOC operations and alert triage, detection and hunting, incident response and forensics, threat intelligence and correlation | P3 for triage, correlation, and authorized defensive inputs. P5–P6 for evidence-based incident coordination and operational assurance. |
| Infrastructure and exposure | Asset discovery and inventory, vulnerability and exposure management, network and endpoint security, cloud and container security | P2 for scoped inventory. P3 for ingesting and correlating authorized findings and telemetry. |
| AI and application security | AI system security, application and API security, software supply chain security, AI model governance and MLOps security | P2 onward for application and dependency assurance. P4 for AI inventory, model evaluation, and policy boundaries. |
| Identity, data, and trust | IAM, zero trust, data privacy, cryptography and secrets management | P2 for identity and tenant isolation. P4–P6 for AI data boundaries, lifecycle evidence, and operational assurance. |
| Governance and financial security | Regulatory compliance and GRC, enterprise risk, third-party risk, banking, payment, and fraud security | P1 for source discovery. P3–P6 for risk linkage, evidence, and scoped review. Payment and fraud data integrations require distinct scope approval. |
| Resilience and assurance | Business continuity and disaster recovery, posture and control validation, audit and evidence, security orchestration | P2 for audit events. P5 for lifecycle and human-approved coordination. P6 for measured restore and release readiness. |

## Boundaries and data flow

1. **Identity boundary.** An identity provider and authenticated workload identities establish a principal. A service authorizes the institution and operation before constructing an immutable tenant context. The incoming tenant selector is a request parameter until verified against membership.
2. **Integration boundary.** Approved connectors deliver tenant-bound events. Validate schema, source identity, tenant binding, event size, and replay semantics before storage. Capture source references and minimize original payloads.
3. **Persistence boundary.** Relational data, indexes and object metadata enforce tenant scoping. Read models and background jobs use the same context. Administrative operations use distinct identities, channels, and audit controls.
4. **AI boundary.** An approved model endpoint receives only permitted context. Its outputs enter a proposal record. The path from proposal to a system change crosses human decision, authorization revalidation, and a separate constrained executor.
5. **Evidence boundary.** Case evidence and audit records identify producer, time, tenant, integrity reference, and decision. Exports and restore operations retain scoped access and retention policy. Telemetry excludes restricted payloads.

## Domain contracts

| Entity | Ownership and identity | Invariant |
|---|---|---|
| Tenant and membership | Tenant identifier with tenant-bound user or service subject | Active membership grants only defined actions. Revocation is effective for new authorizations. |
| Asset and identity | Tenant and stable resource ID; source identity when managed by a connector | An external ID identifies a resource only inside a tenant and source. |
| Event | Tenant, connector ID, source event ID, event time, arrival time, schema version | Unique tenant/connector/source key. Replays never create duplicate effects. Inconsistent replays raise a conflict. |
| Finding and case | Tenant and immutable identifiers, typed edges to tenant resources | Links require same-tenant endpoints and include provenance and correlation confidence. |
| Evidence and decision | Tenant, artifact digest or stable reference, collector, decision version | Expiry and retention are explicit. Approvals target exact parameters and expire. |
| Audit event | Tenant for customer-plane actions, actor, action, outcome, resource, time, correlation ID | Append-only semantics. Audit commit and retry handling preserve accountability. |

## Interface contracts

- **Customer API.** Use a versioned interface, authenticated principal and explicit tenant selector verified by the service. Writes use bounded payloads, schema validation, exact authorization, and auditable outcomes. A rejected cross-tenant reference reveals no resource details. Pagination cursors are bound to the tenant and query. Errors expose a correlation ID and stable error code with restricted payload detail.
- **Event intake.** Input includes schema version, source event identifier, connector identifier, observed time, event type, and authorized resource references. Resolve tenant from connector identity. Repeated identical events return the prior result. A repeated key with changed payload is recorded as a conflict. Document permitted reprocessing and schema compatibility before integration.
- **Worker and storage.** A worker receives scoped job metadata and rechecks context and idempotency. Storage adapters require the scoped context. Verify connection reset between workloads, key naming, encryption, and authorization on reads and exports.
- **AI proposal and approval.** Proposal fields include provenance, model and policy versions, target, normalized parameters, expiry, and risk. The separate approval references the exact proposal version and tenant. Execution revalidates principal authority, approval freshness, and idempotency before acting.

## Architecture decisions

| ADR | Proposed decision and rationale | Evidence or reconsideration |
|---|---|---|
| ADR-001 | Start with a modular monolith and PostgreSQL for a transactional tenant boundary and simpler operations. | Reassess with measured scale, failure domains, or customer deployment constraints. |
| ADR-002 | Use tenant-scoped relational keys and database row-level controls as a second boundary. | Require tenant A/B negative cases at API and database layers, including roles, joins, and pooled connections. |
| ADR-003 | Keep evidence objects in tenant-scoped storage and stable integrity references in relational records. | Show retention and restored authorization through an end-to-end test before release. |
| ADR-004 | Separate AI recommendations from decision and execution responsibilities. | Test that missing, cross-tenant, changed, expired, revoked, and replayed approvals cannot authorize changes. |
| ADR-005 | Establish module contracts and evidence provenance before adopting search, graph, or queue infrastructure. | Add specialized storage only when justified by an approved use case, performance evidence, and an ADR. |

Decision records include author, date, sources with version and usage rights, alternatives considered, risk, consequences, evidence, and approval. Provenance is reviewed for external research and dependencies. These choices derive from the product requirements and source register.

## Defensive threat model

| Threat | Design control | Verification to retain |
|---|---|---|
| Confused deputy or cross-tenant object access | Trusted membership, scoped data access, database enforcement, same-tenant keys | Matrix across API, DB, search, reports, queues, object store, and restore paths as they are delivered. |
| Tenant context leakage through cache or pooled connections | Scoped cache keys and transaction-bound database context | Execute sequential and concurrent A/B operations against the same worker and pool. |
| Ingested event tampering, replay, or resource exhaustion | Connector authentication, bounded input, schema checks, versioning, idempotency | Integrity failure, retry, ordering and load cases with controlled fixtures. |
| Unauthorized AI-assisted action or data disclosure | Tenant-aware retrieval, separate executor, human approval and output validation | Permission boundary, insufficient evidence, altered or expired approval tests. |
| Audit deletion or exposure from logs and backups | Restricted append-only records, redaction, integrity verification, encrypted backups | Access and restore tests and comparison of expected audit evidence. |
| CI or dependency compromise | Pin versions, restrict write permissions, require review of release and workflow policy | Review pinned sources, confirm read-scoped CI, and tie artifacts to approved revisions. |

Maintain risk owner, likelihood, impact, mitigation, residual risk, and review dates in a stage record. This design inventory identifies the initial review scope and does not record those risks as accepted.

## Initial backlog and quality measures

| Work item | Phase | Dependency and decision evidence |
|---|---|---|
| B-P1-01 Review the architecture, scenarios, and contracts | P1 | Confirm design rationale, scope, trust boundaries, and architecture ownership. |
| B-P1-02 Validate Arabic–English equivalence and applicability | P1 | Review both editions and applicability statuses with the designated reviewers. |
| B-P1-03 Exercise GitHub gate failure and prove branch enforcement | P1 | Validate positive and negative Actions runs, then confirm a failing PR cannot merge to protected main. |
| B-P1-04 Record P1 decision | P1 | Collect evidence for P1-V01 through P1-V04 and authorized approval at the candidate SHA. |
| B-P2-01 Deliver scoped asset and event integration | P2 | Requires recorded P1 acceptance. |
| B-P3-01 Evaluate correlation and replay | P3 | Requires recorded P2 acceptance. |
| B-P4-01 Validate AI and approval boundaries | P4 | Requires recorded P3 acceptance. |
| B-P5-01 Verify evidence lifecycle | P5 | Requires recorded P4 acceptance. |
| B-P6-01 Execute release evaluation | P6 | Requires recorded P5 acceptance. |

A confirmed cross-tenant data or authorization failure is a blocker. Measure correlation precision and recall on labeled, versioned events. Measure audit completeness against expected actions, and record model-supported claims, unsupported claims, and abstention when evidence is absent. Measure latency, throughput, RTO, and RPO using a documented environment and workload. Obtain approval for numerical targets and production profiles before using them as release thresholds. No performance results are recorded during document validation.
