# QASCP 2.0 — Consolidated P1 human-review package

Current inspection: [2026-11-25 review and resumption](QASCP_2_P1_REVIEW_2026-11-25.md)
at main f9df7a30747aba111ee7df0afe209fd613cae869. Main now has an active
ruleset with the required Actions check and no bypass actors. This supersedes
the historical disabled-protection observations below. Controlled test #37 now
records an observed blocked merge and repaired positive check. PR #36 carries
the final candidate/CI binding; human reviewer/phase decisions remain missing.
Older candidate results below retain their original scope.

Prepared 2026-11-16 (Qatar). Active phase: P1. Official decision remains Pending review in [the stage record](README.md). This is an evidence index and a review checklist, not an approval. Candidate readiness: ready for human review once the proposed consolidated package's required checks pass; P1 closure remains blocked by outstanding mandatory evidence and decisions.

## Scope and authority

The [PRD](../product/QASCP_2_PRD.md), [architecture](../architecture/QASCP_2_ARCHITECTURE.md), [authority matrix](../architecture/QASCP_2_SUPERSESSION.md), [canonical backlog](../product/QASCP_2_BACKLOG.md), [source register](../governance/REGULATORY_SOURCES.md), [threat register](../architecture/QASCP_2_THREATS.md) and [governance handbook](../governance/ENGINEERING_GOVERNANCE.md) remain authoritative for their assigned subjects.

The static graph package now connects [planning](../architecture/QASCP_2_GRAPH_PLAN.md), [G-01..G-07 proposals](../architecture/QASCP_2_GRAPH_DECISIONS.md), [import contracts](../architecture/QASCP_2_GRAPH_IMPORT_CONTRACTS.md), [receipt/history records](../architecture/QASCP_2_GRAPH_RECORD_CONTRACTS.md) and [query/page/cursor boundary](../architecture/QASCP_2_GRAPH_BOUNDARY.md). No merged PR is represented as formal acceptance of a phase or as delivered runtime functionality.

Baseline reviewed for this index: main aa8c5a24911ec911507d7c6a2c837717f14fc040, tree 81b0e72cb26b9a9b9d4586fd5800a1e82c7f6205 after merged PR #11. Its [main Actions run](https://github.com/ManeaAl-Shabrain/QASCP/actions/runs/43946683513) succeeded. The earlier [PR #11 run](https://github.com/ManeaAl-Shabrain/QASCP/actions/runs/43935824525) at 81ce4ef83abb331934bfac2ab36807bae3cbcb0d passed both full OpenAPI documents and 69 cumulative tests. New package checks must reference its own immutable candidate. This file must not invent a self-referential final commit SHA; the PR carries that binding.

## P1 evidence and remaining decision

| Evidence | Demonstrated / available evidence | Required reviewer or next action |
|---|---|---|
| P1-V01 | Foundation structural parity and governance/product traceability; authoritative source register exists. Baseline main [Actions 43930109029](https://github.com/ManeaAl-Shabrain/QASCP/actions/runs/43930109029) succeeded. | Named bilingual reviewer records substantive equivalence; regulatory owner verifies exact editions, rights, applicability, relevant clauses and unresolved source gaps. Structural parity is not that review. |
| P1-V02 | Domain/architecture/contracts, typed relationships, synthetic conformance cases, threat register and backlog; merged PR #11 full OpenAPI and 69-test evidence linked above. The bilingual BANK-01 blueprint adds planned storage/transaction acceptance. | Qualified independent architecture/security reviewer assesses the full candidate and sensitive verifier inputs; assign actual threat owners; record likelihood/impact/residual-risk dispositions and compatibility decisions. Tool adoption and the new blueprint still need independent review and fresh candidate CI. |
| P1-V03 | Earlier positive/negative workflow evidence exists; the new candidate must pass its full required jobs. On this inspection [main branch metadata](https://api.github.com/repos/ManeaAl-Shabrain/QASCP/branches/main) reports protected:false, enforcement off, empty required check lists. | Repository administrator enables and verifies required PR/check enforcement on an eligible configuration. Retain rule scope/check identity/bypass evidence and a controlled failing PR targeting main that was demonstrably blocked. |
| P1-V04 | The official phase decision is Pending review. No authorized phase-exit decision is claimed by this package. | Authorized owner records approval against the exact candidate with complete evidence, actual reviewer/approver identities and timestamp. Missing mandatory review or enforcement evidence blocks closure. |

P1 is the first phase; there is no earlier approved phase to regress. Cumulative P1 checks include the original foundation-verifier regressions, import schema tests, receipt/history fixtures and the added boundary tests. Runtime API/DB/RLS, executor, model, performance and recovery tests belong to the phases that deliver those components; their absence is not a claim that P1 tests proved them.

## Repository enforcement inspection limits

Inspection on 2026-11-16 obtained main branch metadata showing protection disabled and no required status contexts/checks. The detailed branch-protection endpoint returned 403 Resource not accessible by integration. Ruleset listing returned 403 with GitHub's message that this private-repository feature needs an eligible upgrade or public visibility. Detailed bypass/check-source/rule conditions could not be inspected. No setting was changed.

[Controlled PR #2](https://github.com/ManeaAl-Shabrain/QASCP/pull/2) and [failing run 43739146166](https://github.com/ManeaAl-Shabrain/QASCP/actions/runs/43739146166) are historical workflow-failure evidence. The earlier inspected test targeted foundation/engineering-governance, not main; do not promote it to proof that a main merge was blocked. Fresh enforcement evidence must name the target, protected rule, failed check and observed merge block.

## Source review added 2026-11-17

[Qatar source review and regulatory handoff](../governance/QASCP_2_SOURCE_REVIEW_2026-11-17.md) records selected QCB/NCSA primary-publication text observations, commencement/version findings, initial retrieval failures and the absence of retained binary hashes or amendment verification. It supplies review pointers, not adopted clause mappings. Regulatory approval, bank decisions and QASCP operator decisions remain distinct. Actual entity applicability, rights, substantive bilingual review and independent reviewer decisions remain pending. The expanded PR must pass fresh checks for its own SHA.

## Concrete P1 review agenda

The bilingual [BANK-01 storage and transaction blueprint](../architecture/QASCP_2_BANK01_BLUEPRINT.md) ([العربية](../architecture/QASCP_2_BANK01_BLUEPRINT.ar.md)) now maps G-06 canonical ownership, T1..T3 crash boundaries and BA01..BA11 planned two-tenant acceptance to the existing backlog/threats. This is implementer preparation for independent review; none of the planned runtime cases is reported executed. Review both editions substantively and resolve source-field authority, equal-time ordering, role constraints and generation/retention decisions before implementation.

1. Confirm the 24-domain scope, BANK-01 first slice, original design provenance and all retained/refined/replaced authority decisions.
2. Review P2 inventory/identity/bootstrap/source claim contracts, shared import idempotency key, event-specific receipt identity and current-authorization retry behavior.
3. Review full-replacement claim correction, terminal withdrawal and half-open source/knowledge-time behavior; decide whether the restricted 0.1 semantics are sufficient.
4. Review the 0.2 API successor, accesses qualifier, pending/projected/quarantined intake, resource/provenance filtering before expansion and hidden-hop denial.
5. Review snapshot/cursor/key boundaries, expiry/revocation, independent node/edge budgets, incomplete-source metadata and historical-phase gates.
6. Review validation-tool versions/provenance/licenses, CI/gate inputs and the bounded full OpenAPI validation evidence, with no assumption of runtime assurance.
7. Assign people and record required bilingual/regulatory/security dispositions, then obtain branch-enforcement evidence and the authorized phase decision.

No approval template is prefilled with an approver, acceptance timestamp or Approved status. Actual people and evidence links must be entered by authorized participants in an access-controlled review record.

## Consolidated delivery sequence

Finish and review one coherent P1 package rather than issuing a PR per small step. Keep security-sensitive and phase boundaries explicit. After P1 exit is recorded, the next implementation bundle follows V2-P2-01..06: authenticated tenant context and real PostgreSQL roles first, then authoritative inventory/identity, intake/audit/outbox, typed graph/receipts, BANK-01 integration and an authorized bilingual shell. Approval/AI/historical operations stay in their P4/P5 phases.

هذه الحزمة تجمع العمل القابل للمراجعة في طلب واحد. نجاح الاختبارات ودمج الطلب لا يغنيان عن مراجعة المعنى والمصادر والأمان وقرار اعتماد المرحلة، ولا ننسب إلى الأمثلة الاصطناعية حماية فعلية لبيانات بنك.

Full OpenAPI assurance is consolidated in [the verifier/adoption record](../architecture/QASCP_2_OPENAPI_ASSURANCE.md). This resolves the prior missing-tool capability when the candidate check passes; it does not replace substantive architecture/security review, runtime evidence or a phase-exit decision.
