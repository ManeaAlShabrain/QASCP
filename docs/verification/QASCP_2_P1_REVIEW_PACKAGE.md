# QASCP 2.0 — Consolidated P1 human-review package

Prepared 2026-11-16 (Qatar). Active phase: P1. Official decision remains Pending review in [the stage record](README.md). This is an evidence index and a review checklist, not an approval. Candidate readiness: ready for human review once the proposed consolidated package's required checks pass; P1 closure remains blocked by outstanding mandatory evidence and decisions.

## Scope and authority

The [PRD](../product/QASCP_2_PRD.md), [architecture](../architecture/QASCP_2_ARCHITECTURE.md), [authority matrix](../architecture/QASCP_2_SUPERSESSION.md), [canonical backlog](../product/QASCP_2_BACKLOG.md), [source register](../governance/REGULATORY_SOURCES.md), [threat register](../architecture/QASCP_2_THREATS.md) and [governance handbook](../governance/ENGINEERING_GOVERNANCE.md) remain authoritative for their assigned subjects.

The static graph package now connects [planning](../architecture/QASCP_2_GRAPH_PLAN.md), [G-01..G-07 proposals](../architecture/QASCP_2_GRAPH_DECISIONS.md), [import contracts](../architecture/QASCP_2_GRAPH_IMPORT_CONTRACTS.md), [receipt/history records](../architecture/QASCP_2_GRAPH_RECORD_CONTRACTS.md) and [query/page/cursor boundary](../architecture/QASCP_2_GRAPH_BOUNDARY.md). No merged PR is represented as formal acceptance of a phase or as delivered runtime functionality.

Baseline reviewed for this index: main 9c8fb2e665d25b325b4e9fa82b4c97f80d1b77cd, tree c042a9c277061d84f11406d8a2a2ff9b742e5f7e. New package checks must reference its own immutable candidate. This file must not invent a self-referential final commit SHA; the PR carries that binding.

## P1 evidence and remaining decision

| Evidence | Demonstrated / available evidence | Required reviewer or next action |
|---|---|---|
| P1-V01 | Foundation structural parity and governance/product traceability; authoritative source register exists. Baseline main [Actions 43921524606](https://github.com/ManeaAl-Shabrain/QASCP/actions/runs/43921524606) succeeded. | Named bilingual reviewer records substantive equivalence; regulatory owner verifies exact editions, rights, applicability, relevant clauses and unresolved source gaps. Structural parity is not that review. |
| P1-V02 | Original domain/architecture/contracts, scoped source history, typed relationships, synthetic conformance cases, threat register and backlog. [Merged PR #9](https://github.com/ManeaAl-Shabrain/QASCP/pull/9) and its [Actions run](https://github.com/ManeaAl-Shabrain/QASCP/actions/runs/43921148650) passed 42 tests. New boundary work requires its own fresh run. | Qualified independent architecture/security reviewer assesses the full candidate and sensitive verifier inputs; assign actual threat owners; record likelihood/impact/residual-risk dispositions and compatibility decisions. Full OpenAPI validation remains outstanding. |
| P1-V03 | Earlier positive/negative workflow evidence exists; the new candidate must pass its full required jobs. On this inspection [main branch metadata](https://api.github.com/repos/ManeaAl-Shabrain/QASCP/branches/main) reports protected:false, enforcement off, empty required check lists. | Repository administrator enables and verifies required PR/check enforcement on an eligible configuration. Retain rule scope/check identity/bypass evidence and a controlled failing PR targeting main that was demonstrably blocked. |
| P1-V04 | The official phase decision is Pending review. No authorized phase-exit decision is claimed by this package. | Authorized owner records approval against the exact candidate with complete evidence, actual reviewer/approver identities and timestamp. Missing mandatory review or enforcement evidence blocks closure. |

P1 is the first phase; there is no earlier approved phase to regress. Cumulative P1 checks include the original foundation-verifier regressions, import schema tests, receipt/history fixtures and the added boundary tests. Runtime API/DB/RLS, executor, model, performance and recovery tests belong to the phases that deliver those components; their absence is not a claim that P1 tests proved them.

## Repository enforcement inspection limits

Inspection on 2026-11-16 obtained main branch metadata showing protection disabled and no required status contexts/checks. The detailed branch-protection endpoint returned 403 Resource not accessible by integration. Ruleset listing returned 403 with GitHub's message that this private-repository feature needs an eligible upgrade or public visibility. Detailed bypass/check-source/rule conditions could not be inspected. No setting was changed.

[Controlled PR #2](https://github.com/ManeaAl-Shabrain/QASCP/pull/2) and [failing run 43739146166](https://github.com/ManeaAl-Shabrain/QASCP/actions/runs/43739146166) are historical workflow-failure evidence. The earlier inspected test targeted foundation/engineering-governance, not main; do not promote it to proof that a main merge was blocked. Fresh enforcement evidence must name the target, protected rule, failed check and observed merge block.

## Concrete P1 review agenda

1. Confirm the 24-domain scope, BANK-01 first slice, original design provenance and all retained/refined/replaced authority decisions.
2. Review P2 inventory/identity/bootstrap/source claim contracts, shared import idempotency key, event-specific receipt identity and current-authorization retry behavior.
3. Review full-replacement claim correction, terminal withdrawal and half-open source/knowledge-time behavior; decide whether the restricted 0.1 semantics are sufficient.
4. Review the 0.2 API successor, accesses qualifier, pending/projected/quarantined intake, resource/provenance filtering before expansion and hidden-hop denial.
5. Review snapshot/cursor/key boundaries, expiry/revocation, independent node/edge budgets, incomplete-source metadata and historical-phase gates.
6. Review validation-tool versions/provenance/licenses, CI/gate inputs and missing full OpenAPI validation, with no assumption of runtime assurance.
7. Assign people and record required bilingual/regulatory/security dispositions, then obtain branch-enforcement evidence and the authorized phase decision.

No approval template is prefilled with an approver, acceptance timestamp or Approved status. Actual people and evidence links must be entered by authorized participants in an access-controlled review record.

## Consolidated delivery sequence

Finish and review one coherent P1 package rather than issuing a PR per small step. Keep security-sensitive and phase boundaries explicit. After P1 exit is recorded, the next implementation bundle follows V2-P2-01..06: authenticated tenant context and real PostgreSQL roles first, then authoritative inventory/identity, intake/audit/outbox, typed graph/receipts, BANK-01 integration and an authorized bilingual shell. Approval/AI/historical operations stay in their P4/P5 phases.

هذه الحزمة تجمع العمل القابل للمراجعة في طلب واحد. نجاح الاختبارات ودمج الطلب لا يغنيان عن مراجعة المعنى والمصادر والأمان وقرار اعتماد المرحلة، ولا ننسب إلى الأمثلة الاصطناعية حماية فعلية لبيانات بنك.
