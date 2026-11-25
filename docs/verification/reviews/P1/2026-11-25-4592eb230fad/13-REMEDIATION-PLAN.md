# Corrective action and re-review plan

Reviewed repository: ManeaAlShabrain/QASCP · branch: main · commit: `4592eb230fadebb828c8b7d3b7972c6bd1aec012` · date: 2026-11-25, Asia/Riyadh.

AI-assisted review only; virtual specialties do not represent actual independent people.

The reviewer made no implementation fixes. Role names below are requested responsibilities, not actual assigned people or accepted risks.

| Order | Findings | Action and accountable role needed | Acceptance evidence |
|---|---|---|---|
| 1 | QAR-004 | CI implementer corrects effective local include handling without logging values; qualified independent security reviewer assesses correction | Clean/direct/include/matching-includeIf real-Git matrix, error-path checks, fresh cumulative candidate CI; [#40](https://github.com/ManeaAlShabrain/QASCP/issues/40) |
| 2 | QAR-005 | Policy owner + substantive bilingual reviewer reconcile human obligation and snapshot-version translation in both editions | Paired text, corrected historical comparison note, foundation/contract checks and actual bilingual disposition; [#41](https://github.com/ManeaAlShabrain/QASCP/issues/41) |
| 3 | QAR-003 | Architecture/database/API owners select exact P2 contract/receipt/compatibility and source-field authority decisions | B06/G decision table, no silent original-contract mutation or source rebinding, expected denial/conflict examples; existing [#14](https://github.com/ManeaAlShabrain/QASCP/issues/14) |
| 4 | QAR-002 | Actual security/domain/integration/AI/workflow/assurance/build/platform/operations/regulatory owners review T01–T12 | Names, dated scopes, likelihood/impact/residual-risk decisions and evidence links; existing #14 and appropriate owner record |
| 5 | QAR-006/009 | Documentation implementer repairs primary verification recipe and import receipt prose | Fresh supported-environment recipe result, full API/policy validation and regression; [#42](https://github.com/ManeaAlShabrain/QASCP/issues/42) |
| 6 | QAR-007 | Product/project owner restores an active representation of remaining package acceptance | Existing issues reopened by authorized decision or explicit active tracker with owners/dependencies; [#32](https://github.com/ManeaAlShabrain/QASCP/issues/32) |
| 7 | QAR-008 | Build/security owner evaluates wheel hash lock and real advisory/provenance review at applicable gate | Artifact/platform provenance and install/build evidence; no arbitrary P1 hash-lock requirement added |
| 8 | QAR-001 | Actual qualified independent, bilingual and regulatory reviewers record dispositions; authorized product owner decides P1 exit | Exact immutable candidate, identities, qualification/independence, all P1-V01..04, no unresolved mandatory blockers; existing [#15](https://github.com/ManeaAlShabrain/QASCP/issues/15), [#16](https://github.com/ManeaAlShabrain/QASCP/issues/16), [#17](https://github.com/ManeaAlShabrain/QASCP/issues/17) |

Steps that do not depend on one another may be implemented independently; reviewer re-verification remains separate. No calendar deadline, person or legal applicability is fabricated.

## Re-review protocol

1. Preserve this dated baseline and findings. Obtain the new candidate SHA and bounded diff; never overwrite this report to imply it assessed later fixes.
2. Require the implementer to identify each finding addressed, affected requirements/interfaces and acceptance proof. A comment saying fixed is insufficient.
3. Re-run the effective-local-config probe against the exact revised guard, substantive paired-text review, both full OpenAPI/policy checks and complete P1 foundation/schema/oracle regressions. Retain local failures, skips and stale checks explicitly.
4. Verify source/adoption/risk/reviewer/owner records and current rule configuration; require new enforcement evidence if relevant policy/gate behavior changes.
5. Record OPEN → IN PROGRESS → READY FOR RE-REVIEW → VERIFIED FIXED with actual closure evidence. Regressions become REOPENED. CLOSED requires the governed disposition. ACCEPTED RISK requires the actual authorized risk authority; this plan grants no exception.
6. Authorized P1 exit is a separate record tied to the accepted candidate; only then can P2 begin. Do not merge this review PR automatically.
