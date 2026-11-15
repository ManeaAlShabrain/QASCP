# QASCP 2.0 — Product requirements

Status: proposed P1 baseline, 2026-11-15. Product owner and independent reviewer: assignment pending. Active phase and approval remain in the [stage record](../verification/README.md). Product version 2.0 does not change handbook baseline 1.0.

**One Platform. Every Security Domain. Continuous Assurance.**

منصة موحدة للأمن السيبراني وأمن الذكاء الاصطناعي والضمان المستمر في القطاع المالي القطري. تجمع السياق والأدلة والقرارات في قضية قابلة للتتبع، مع إبقاء صلاحيات التنفيذ منفصلة عن توصيات الذكاء الاصطناعي.

## Problem, users, and value

Financial institutions have separate asset inventories, identity systems, security alerts, exposure findings and assessment evidence. Analysts cannot reliably determine which business service is affected, which evidence remains current, or why a prior decision should be revisited. QASCP connects these records with attributable relationships and a versioned decision history.

| User | Job | Observable result |
|---|---|---|
| SOC analyst | Triage an alert in its business context | One case exposes asset, identity, finding, evidence and association reasons |
| Security engineer | Prioritize exposure | Versioned deterministic rationale includes criticality, exposure and missing context |
| AI security reviewer | Investigate a model or agent dependency | AI system, service identity, dataset and retrieval permissions are linked |
| Control owner | Maintain assurance | Changed or expired evidence creates an attributable re-verification task |
| Auditor | Reconstruct a decision | Authorized as-of view exposes evidence and rule versions known at the cutoff |
| Banking security lead | Review institutional posture | Coverage, unresolved gaps and source freshness appear separately |

QASCP is an integration, reasoning and assurance layer. Its initial scope does not replace SIEM, EDR, IAM, scanners, payment processing or specialist fraud engines. The 24 domains below describe target coverage; none is represented as a delivered module by this document.

## Requirements and acceptance

Product IDs below supplement, and do not replace, the binding [governance requirements](../verification/requirements.json). All are proposed until P1 review. Acceptance refers to future delivery unless explicitly marked P1.

| ID | Requirement | Acceptance | Phase / governance |
|---|---|---|---|
| PRD-01 | Unified, tenant-scoped security graph | Asset, identity, finding and event connect with source, confidence and time; cross-tenant edges fail | P2-P3 / QASCP-SEC-001..003 |
| PRD-02 | Authenticated normalized intake | Same source key and digest has one logical effect; changed digest conflicts; missing scope fails | P2 / QASCP-SEC-001, QASCP-SEC-005 |
| PRD-03 | Contextual reasoning | Rule version and input versions explain ranking; unknown context is visible and AI cannot assign authorization | P3-P4 / QASCP-AI-002 |
| PRD-04 | Continuous assurance | Expiry, correction and source gaps invalidate support; incomplete dependencies trigger broader reconciliation | P5 / QASCP-ENG-002 |
| PRD-05 | Human-controlled response | P4 defines and tests exact human approval plus a constrained synthetic executor that rejects absent, altered, cross-tenant, expired, revoked, reused or stale-authority approvals; P5 adds full assurance workflow, evidence custody, remote reconciliation and operational integrations | P4-P5 / QASCP-AI-001 |
| PRD-06 | Reconstructable case | Timeline links observations, rule output, reviewer, decision and re-verification without overwriting prior decisions | P3-P5 / QASCP-SEC-005 |
| PRD-07 | Scoped framework mapping | Source/version/clause/applicability/evidence/reviewer are separate; unknown applicability prevents a compliance claim | P1 design, P5-P6 / QASCP-CMP-001 |
| PRD-08 | Enterprise deployment | Private-cloud/on-prem installation, recovery and tenant isolation meet agreed profiles | P6 / QASCP-OPS-001 |
| PRD-09 | Bilingual command center | Arabic RTL and English LTR expose consistent IDs, timestamps and state labels; access policies apply to every view | P2-P6 / QASCP-SEC-003 |
| PRD-10 | Independent development | ADRs explain original choices and source rights; no external proprietary schemas or interfaces copied | P1-P6 / QASCP-GOV-002 |

## Coverage and sequencing

| Group | Domain | Initial QASCP responsibility | Earliest intended phase |
|---|---|---|---|
| A | SOC operations & alert triage | Case and alert context | P3 |
| A | Detection & hunting | Authorized detection results and coverage links | P3 |
| A | Incident response & forensics | Evidence custody and investigation coordination | P5 |
| A | Threat intelligence & correlation | Source-qualified indicators and associations | P3 |
| B | Asset discovery & inventory | Authorized inventory import and resolution | P2 |
| B | Vulnerability & exposure | Finding-to-business-service prioritization | P3 |
| B | Network & endpoint | Consume existing defensive telemetry | P3 |
| B | Cloud, containers & Kubernetes | Resource and configuration finding imports | P3 |
| C | AI/LLM/agent security | Agent tools, retrieval boundaries and evaluation evidence | P4 |
| C | Application & API security | Application inventory and authorized findings | P3 |
| C | Software supply chain | Component/SBOM finding relationships | P3 |
| C | AI governance & MLOps | Model, dataset and policy version records | P4 |
| D | Identity & access | Human/workload identities and entitlements | P2 |
| D | Zero trust | Evidence of identity/resource policy decisions | P3 |
| D | Data security & privacy | Classification and processing-scope relationships | P2 |
| D | Cryptography, PKI & secrets | Metadata, ownership and expiry; no secret values in graph | P3 |
| E | Regulatory compliance & GRC | Applicability review and control/evidence mapping | P1 design, P5 delivery |
| E | Enterprise risk | Evidence-linked risk decisions | P3 |
| E | Third-party & supply chain risk | Supplier/service dependency and evidence freshness | P5 |
| E | Banking, payment & fraud | Approved source integration and case context | P3-P6, separate source scope |
| F | Business continuity & disaster recovery | Service dependencies and recovery-test evidence | P6 |
| F | Posture & control validation | Versioned assertions and re-verification | P5 |
| F | Audit & evidence management | Scoped custody, integrity and decision history | P2 audit, P5 lifecycle |
| F | Automation & orchestration | P4 approval and constrained synthetic executor boundary; P5 full assurance and operational workflow | P4 boundary, P5 integration |

## Prioritized banking scenarios

| ID / priority | Scenario | Acceptance and boundary |
|---|---|---|
| BANK-01 / first slice | AI assistant service identity has excessive access to a sensitive database and unusual activity | Authorized event resolves to identity, assistant, database and finding; one case shows provenance and missing evidence; recommendation has no execution authority |
| BANK-02 / next | Exposed digital banking API has a finding and privileged workload identity | Link exposure to service importance without treating a severity score alone as business risk |
| BANK-03 / later | Core banking configuration evidence changes | Mark affected assertions for re-verification; unchanged assertions remain current only with complete dependencies |
| BANK-04 / later | Payment/SWIFT infrastructure alert | Read-only authorized metadata supports triage; no message signing, transaction blocking or payment manipulation |
| BANK-05 / later | ATM endpoint alert or supplier outage | Link endpoint/vendor to service owner and recovery evidence |
| BANK-06 / later | Open banking API and fraud signal | Consume permitted findings; fraud adjudication stays with authorized bank processes |

BANK-01 uses synthetic records during repository development. It spans P2 intake/graph, P3 correlation, P4 AI evaluation plus exact human approval and a constrained synthetic executor boundary, and P5 full assurance workflow, evidence custody, remote reconciliation and any separately authorized operational integration. Describing its full flow does not authorize later phases.

## Command center design

Navigation: Overview, Investigations, Assets & Relationships, Exposure, AI Systems, Assurance, Governance, Integrations, Administration. Each screen indicates tenant, freshness, permission scope and unresolved gaps. The primary case view retains the existing Investigate → Assess impact → Reverify → Review history workflow. Use a timeline plus a bounded relationship view, an evidence drawer and an explanation panel. A user can inspect a relationship's source and confidence rather than infer certainty from a graph line. Distinguish observed facts, rule conclusions, model suggestions and human decisions using text as well as visual cues.

The overview aggregates current findings and source health, not an unsupported universal security score. Production actions expose exact target and parameters at approval. Export and historical views retain authorization. Keyboard access, readable contrast, RTL review and localization checks form UI acceptance.

PRD-09 acceptance is phase-specific. P2 establishes an authenticated shell with Arabic RTL and English LTR layout, keyboard operation, readable contrast, consistent identifiers/timestamps/state labels and tenant/permission indicators on every delivered view. P3 and P4 apply the same checks to investigation, graph, reasoning and AI-review views, including authorization before counts, traversal and evidence display. P5 adds separately authorized export and historical views, reauthorizes every export and historical request, preserves the as-of cutoff and prevents hidden records from affecting visible counts. P6 repeats bilingual accessibility and authorization checks in the accepted deployment and release regression. Missing localization must not change identifiers or authorization semantics.

PRD-10 acceptance recurs at every phase. Each adopted design, dependency, schema or interface records its original requirement, author, alternatives, provenance, usage or license terms, affected ADR and review disposition before acceptance. Each phase reruns the applicable provenance and license review and updates an ADR when a component, trust boundary or external source changes. An unresolved right or copied proprietary structure blocks adoption.

## Measures and release limits

P1 deliverables: this PRD, [architecture and ADRs](../architecture/QASCP_2_ARCHITECTURE.md), [domain/contracts](../architecture/QASCP_2_CONTRACTS.md), [threat register](../architecture/QASCP_2_THREATS.md), [authority/supersession matrix](../architecture/QASCP_2_SUPERSESSION.md), [coverage mapping](../governance/QASCP_2_COVERAGE.md), machine-checked requirement mappings, static JSON contracts and the canonical [backlog](QASCP_2_BACKLOG.md). P1-V01..04 remain the review gates.

Proposed laboratory profile for owner review: two synthetic tenants, 10,000 nodes and 50,000 edges per tenant, 10 events/second for 30 minutes plus a 100 events/second 60-second burst. Candidate targets: graph lookup p95 ≤500 ms for depth ≤2 and ≤200 returned edges; intake acknowledgement p95 ≤1 s; projection lag p95 ≤10 s. Measure on a recorded deployment with authentication, audit and RLS enabled; include overload and failures. These are unapproved targets, not measured capabilities or bank SLAs.

Correctness gates: zero unauthorized cross-tenant results in the versioned negative suite; all expected sensitive operations have durable audit events; identical ingestion has one logical effect; conflicting ingestion never silently replaces evidence. For BANK-01 report precision, recall, ambiguous matches, dataset balance and triage time against an agreed baseline. For assurance compare selective evaluation to full evaluation and require zero missed affected assertions in the approved fixtures. Runtime availability, RTO/RPO and correlation thresholds require named owners and approved workloads before P6 testing. Model output must cite permitted evidence or abstain; measure unsupported claims and abstentions separately.

## Migration from existing P1

The [document authority and supersession matrix](../architecture/QASCP_2_SUPERSESSION.md) is the sole record of which earlier architecture, product, ADR, scenario, component and backlog material is retained, refined, replaced or deprecated. The engineering governance handbooks remain binding, and [QASCP_2_BACKLOG.md](QASCP_2_BACKLOG.md) is the canonical 2.0 backlog. No prior phase approval, benchmark, connector readiness or compliance claim transfers automatically. No application runtime or migrations are delivered in P1.
