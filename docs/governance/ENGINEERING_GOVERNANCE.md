# QASCP Engineering Governance and Delivery Handbook

[العربية](ENGINEERING_GOVERNANCE.ar.md) · Version 1.0 · Proposed baseline for P1 review

QASCP is a unified cybersecurity, AI security, and continuous assurance platform for Qatar's financial sector. This handbook governs design, implementation, verification, and release. The English and Arabic editions carry the same requirements. MUST and MUST NOT are binding project requirements once this baseline is adopted. If a translation is ambiguous or conflicts with the other edition, block the affected acceptance decision until both texts are reconciled in one pull request.

Translation clarification candidate, 2026-11-17: SEC-004 workload terminology and ENG-003 patch terminology are aligned in both editions within proposed baseline 1.0. Independent bilingual/security review and baseline adoption remain pending; no phase decision is recorded here.

## Using this handbook

Start with the [verification record](../verification/README.md) to identify the active phase. Read the [P1 architecture](../architecture/P1_ARCHITECTURE.md) for design decisions and trust boundaries, the [source register](REGULATORY_SOURCES.md) for authority and applicability, and [verification procedures and records](../verification/PROCEDURES.md) for evidence and approvals. Every applicable requirement links to a verification ID in the [verification register](../verification/requirements.json). The verification ID identifies the evidence to collect at the named phase. Requirements spanning phases must also be tested as relevant earlier components are delivered.

### QASCP-GOV-001 — Phase scope and formal closure

Every work item MUST name the active phase, requirement IDs, affected interfaces, and acceptance criteria before implementation. A later phase MUST NOT begin until the previous phase has a recorded approval tied to an immutable revision, its evidence, and an authorized approver. Merging a pull request, closing an issue, and passing CI do not independently close a phase. Missing dependencies, unresolved applicability, and exceptions MUST be recorded explicitly.

### QASCP-GOV-002 — Clean-room implementation

Use original requirements, code, data models, workflows, and tests. Do not copy external project structures, categories, interface designs, prompts, fixtures, or source code into QASCP. Public standards may be referenced by version and identifier. Record provenance, usage rights, and the design rationale in an ADR before adoption. Review licenses for dependencies and redistributable material. If provenance or permission is uncertain, suspend that adoption until documented review resolves it.

### QASCP-GOV-003 — Change and translation control

Changes to either handbook edition, the requirement register, CI, security controls, or acceptance criteria MUST use a pull request with scope, requirement IDs, and evidence. Keep normative text, version, IDs, and order aligned across both languages in the same change. A bilingual reviewer checks substantive equivalence. The automated register check verifies structural parity. Protect the default branch with pull requests and the required GitHub Actions check on a supported plan. Validate enforcement before claiming it is active.

### QASCP-GOV-004 — Ownership and independence

The product owner approves scope and phase exit. The implementer provides reproducible evidence. A qualified reviewer independently assesses security-sensitive changes, the controls governing acceptance, and readiness for client or production deployment. The regulatory owner verifies legal and contractual applicability. The release operator deploys the accepted artifact and records the outcome. Record the actual people and decisions at approval. Author self-review does not fulfill independent review. Missing reviewers block the affected acceptance decision.

### QASCP-SEC-001 — Trusted tenant context

Every customer-plane API request and internal job MUST carry an authenticated, authorized `tenant_id` through every service boundary. Resolve membership from trusted server-side identity and validate any caller-supplied tenant selector against that identity. Reject absent, malformed, expired, or inconsistent context before data access. Noncustomer bootstrap and liveness surfaces MUST be isolated from tenant operations and MUST expose no tenant data or perform tenant queries.

### QASCP-SEC-002 — Database isolation

Every application-owned tenant-data table, join, read, write, and deletion MUST be tenant-scoped. Tenant-owned keys and references MUST prevent cross-tenant ownership links. Enforce mandatory tenant filtering in the data layer and database controls such as row-level security, with application roles that cannot bypass it. Shared infrastructure metadata MUST be isolated and unable to access tenant records. Connection reuse, background processing, maintenance, backups, and restores MUST preserve tenant boundaries and be verified independently.

### QASCP-SEC-003 — Isolation across derived data

Carry `tenant_id` into search indexes, object metadata and authorization, caches, queues, graph edges, reports, evidence exports, audit events, and AI retrieval. Scope identifiers and invalidate caches on access changes as appropriate. Enforce the same access policy on generated artifacts, retry paths, and replay. Verify that attempts to read, infer, mutate, or reference tenant B resources from tenant A are denied across each applicable surface.

### QASCP-SEC-004 — Identity and sensitive data

Enforce default-deny authorization, least privilege, separation of user roles from workload roles (including services, connectors, workers and scheduled jobs), and access reviews for privileged duties. Minimize and classify data. Encrypt sensitive data in transit and at rest, keep secrets outside code and logs, and verify rotation and revocation. Record processing purpose, storage location, retention, deletion, and authorized access. Development and CI use approved synthetic fixtures only. These fixtures are kept out of production data paths.

### QASCP-SEC-005 — Audit integrity

Record tenant scope, actor and actor type, time, affected resource, action, outcome, and correlation ID for access-control changes, evidence mutations and exports, approval decisions, and sensitive operations. Append audit events to restricted storage and verify the integrity, retention, and access of those records. Logs MUST exclude secrets and inappropriate customer payloads. If required audit evidence cannot be committed, block the sensitive mutation or apply a documented atomic delivery mechanism that preserves its audit record.

### QASCP-AI-001 — Human approval and execution boundaries

AI components MUST have no production write credentials or direct execution path. They may produce a recommendation with sources and uncertainty. A production mutation requires an authorized human decision bound to tenant, exact action and target, parameters, expiry, and the proposal version. A separate constrained executor must revalidate authorization and approval immediately before the action. Expired, revoked, altered, or reused approvals MUST be denied. Audit the proposal, decision, execution outcome, and correlation.

### QASCP-AI-002 — Model and data assurance

Treat model output and retrieved content as untrusted. Enforce tenant and data policy before retrieval, redact sensitive inputs and outputs where required, and record model, prompt-policy, and evaluation dataset versions. Evaluate unsupported claims, missing evidence, policy limits, and permission boundaries on versioned fixtures. Abstain or route to human review when evidence is insufficient. No model response is an authorization or compliance decision.

### QASCP-ENG-001 — Complete and maintainable code

Production paths MUST handle errors and supported inputs, including validation failures, partial failures, retries, and concurrent requests. Do not ship stub bodies, standalone `pass` in unfinished functions, unfinished markers such as `TODO`, sample credentials, fake evidence, or synthetic production fallback data. Document supported interfaces, invariant ownership, and operational failure handling. Human reviewer assessment and applicable static, unit, integration, and regression checks are required. CI at P1 assesses the repository documentation and the verifier itself.

### QASCP-ENG-002 — Integration, regression, and evidence

Test at the real entry point and with real component dependencies when the behavior depends on them. Stage evidence MUST include applicable earlier-phase regression checks. Record the commit, tested environment, commands or workflow run, artifact digest where relevant, and outcomes. A failed, skipped, cancelled, missing, or stale required check blocks the affected decision. A genuinely inapplicable check needs a reason recorded and accepted before closure. Re-run checks after an affected commit, interface, dataset, or deployment change.

### QASCP-ENG-003 — Software supply chain and build integrity

Review dependency provenance, licenses, and maintenance risks. Pin controlled build and CI inputs, protect secrets, restrict CI privileges, and retain the software bill of materials for deliverable artifacts. Scan dependencies and images where present. Bind release review to an immutable, identifiable artifact built from the tested commit. A different artifact requires its own verification. Record risks from unpatched dependencies and the mitigation owner; patch status is distinct from release recency.

### QASCP-OPS-001 — Release, recovery, and incident handling

Before client or production deployment, verify install, upgrade from the prior supported version where applicable, backup restoration, rollback or forward recovery, audit continuity, and deployment of the exact approved artifact. Agree and record availability, RTO, RPO, load profile, and alert thresholds before testing against them. Maintain an incident procedure that covers triage, containment approval, evidence custody, notification ownership, recovery, and lessons learned. Suspected incidents are handled through the authorized operational channel.

### QASCP-CMP-001 — Regulatory applicability and claims

Record the issuing authority, source version, effective date, clause, license or entity scope, data and deployment context, mapped control, evidence, and regulatory reviewer. Preserve applicable source provenance and any permitted snapshot hash. Use review states such as applicability pending, assessed, insufficient evidence, and approved. No external compliance claim may be made before applicability and its supporting evidence are reviewed. Framework mappings inform design. Regulatory applicability is determined per entity and deployment.

### QASCP-REL-001 — Release blockers and exceptions

An unmet binding requirement, an unverified required control, confirmed unresolved high or critical findings, tenant isolation failure, authorization failure, or data loss blocks phase closure or release wherever applicable. Correct the cause, record an issue, and rerun impacted checks and dependency paths. A lower-risk deferral requires impact, a compensating control, named owner, expiry, and explicit approval. A deferral cannot override mandatory checks, tenant isolation, auditability, or applicable obligations.

## Phase gates

| Phase | Exit evidence |
|---|---|
| P1 — Product and architecture foundation | Bilingual governed baseline, architecture and ADRs, trust boundaries and threat model, domain and interface contracts, prioritized banking scenarios and backlog, requirements-to-evidence register, source and applicability register, and formal P1 decision. |
| P2 — Core security data platform | Reproducible installation and upgrade where applicable, authenticated tenant context, actual database and service isolation, seedless acceptance paths with test fixtures outside runtime, and an asset-to-event-to-audit integration test. |
| P3 — Detection, exposure, and risk | Authorized event-to-asset-to-identity-to-finding flow, measured correlation precision and recall on a versioned set, replay and ordering evidence, and cumulative regression. |
| P4 — AI security and governance | Human approval and executor boundary tests, tenant-scoped retrieval, versioned model-policy evaluations, insufficient-evidence abstention, and cumulative regression. |
| P5 — Assurance and orchestration | Evidence-to-case-to-approval-to-reverification flow, expiry and duplicate handling, factual claim review, and cumulative regression. |
| P6 — Enterprise validation | Independent security review, approved operational targets with recovery and performance evidence, versioned deployment and support package, customer applicability review where relevant, and release acceptance tied to the exact artifact. |

## Working sequence

1. Read the active phase record, both editions when editing policy, and the relevant architecture or source record.
2. Open a scoped branch and link the requirement IDs. Document new decisions and affected earlier paths.
3. Run the commands and tests in the verification procedure. Capture failures and correct the cause before retest.
4. Submit a pull request with release-impact, security, provenance, and evidence links. Record review against the current revision.
5. Record the phase decision only after the authorized approver provides evidence. Use a repository record that points to the reviewed revision rather than a self-referential commit SHA.


Translation correction candidate, 2026-11-25 (QAR-005): ENG-001 explicitly retains human review in both editions. GOV-004 is unchanged. The separate solo-governance proposal is not adopted. Substantive independent review and baseline adoption remain pending.
