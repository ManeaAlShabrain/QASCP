# QASCP 2.0 — Threat and design-risk register

P1 proposed assessment scope; PRD-01..08, QASCP-SEC-001..005, QASCP-AI-001..002, QASCP-ENG-003. P1-V02 reviews design; later phases test implemented boundaries. Owners below are required roles, not assigned people. No residual risk is accepted. Likelihood/impact are initial qualitative estimates requiring independent review before closure.

| ID | Threat / boundary | Likelihood / impact | Mitigation and required evidence | Accountable role / verification |
|---|---|---|---|---|
| T01 | Forged tenant selector or graph edge | Medium / critical | Trusted context, composite FKs, RLS; API/DB A→B negative tests, raw role tests | Security lead / P1-V02, P2-V01, P3-V01 |
| T02 | Cache, worker or pooled connection leaks context | Medium / critical | Transaction-scoped context and scoped keys; sequential/concurrent A/B reuse tests | Backend lead / P1-V02, P2-V01 |
| T03 | Connector spoofing, malicious payload or replay | High / high | Workload binding, size/schema/quota checks, adapter-owned digest conflicts, quarantine; retry/out-of-order tests | Integration lead / P1-V02, P2-V01, P3-V01 |
| T04 | Entity conflation causes false banking impact | Medium / high | Scoped stable source IDs, explicit ambiguity and confidence; labeled collision fixtures | Detection lead / P1-V02, P3-V01 |
| T05 | Poisoned evidence or prompt injection | High / high | Treat retrieved text as data, enforce tool/data allowlists, cite sources/abstain; adversarial tenant-scoped evaluations | AI security lead / P1-V02, P4-V01 |
| T06 | Approval altered or reused; remote timeout repeats mutation | Medium / critical | Exact digest/version approval, atomic consumption, downstream idempotency and reconciliation; adversarial synthetic executor tests in P4 and operational integration tests in P5 | Workflow lead / P1-V02, P4-V01, P5-V01 |
| T07 | Late/corrected evidence leaves stale assurance supported | Medium / high | Dual time, dependency lineage, version checks and conservative reconciliation; compare full/selective evaluation | Assurance lead / P1-V02, P5-V01 |
| T08 | Audit tampering, sensitive log or export disclosure | Medium / high | Restricted append-only audit, redaction, per-resource export checks and custody; audit outage/restore tests | Security lead / P1-V02, P2-V01, P5-V01, P6-V01 |
| T09 | Dependency/CI artifact compromise | Medium / critical | Pinned reviewed inputs, minimal CI privileges, SBOM and immutable build/review binding | Build lead / P1-V02, P2-V02, P6-V01 |
| T10 | Expensive traversal, queue flooding or tenant starvation | High / high | Depth/edge limits, timeouts, per-tenant budgets, backpressure and dead letters; overload fairness tests | Platform lead / P1-V02, P3-V01, P6-V01 |
| T11 | Backup/restore loses authorization or evidence | Medium / critical | Encrypted scoped restore and audit continuity checks against agreed RTO/RPO | Operations lead / P1-V02, P6-V01 |
| T12 | Mapping shown as certification | Medium / high | Separate applicability/evidence/reviewer states; UI/report negative tests for unreviewed claims | Regulatory owner / P1-V01, P1-V02, P5-V01, P6-V01 |

Review date: 2026-11-15. Next review: P1 candidate review, and after changed interfaces or trust boundaries. Before P1 closure assign actual owners, review likelihood/impact/residual risk and link reviewer disposition. Unresolved ownership and review remain explicit blockers, rather than implied approval of this table.
