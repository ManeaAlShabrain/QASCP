# QASCP code and contract security review

Prepared 2026-11-17 (Qatar). Active phase P1; V2-P1-02/03, P1-V01..03. Requirements: QASCP-SEC-003/005, QASCP-AI-001, QASCP-ENG-001..003 and QASCP-GOV-002..004. This is an implementer review and remediation candidate, not independent acceptance or a phase-exit decision.

## Revision and scope

Base main: 9abbdd2619626f8faf28b91b1836d4fb267e2426. An isolated snapshot matched all 65 base Git blobs after line-ending normalization. Shared-workspace edits to the approval/normalized contracts and other files were preserved and excluded. The PR binds the final candidate SHA and actual CI results; this report does not invent its own commit identity.

Read the four Python verifier/oracle scripts, all five existing Python test modules, workflow and dependency manifest. Inspected all 18 contract JSON documents for nested constraints/references and reviewed security-sensitive approval, tenant-context, normalized intake and graph semantics against the architecture. The project has no application API server, database implementation, identity provider, production connector or executor in this revision. No deployed-service security claim can follow from this review.

## Findings and fixes

| ID | Before / impact within current P1 tooling | Remediation and regression evidence |
|---|---|---|
| CR-01 | Missing/empty/unreadable product PRD or backlog could reach traceability code without its inputs and raise KeyError instead of a useful failure report. | Require every traceability input before analysis. Real CLI regressions remove/empty/corrupt both product inputs and require exit 1 with a diagnostic and no traceback. |
| CR-02 | Standard JSON decoding accepted duplicate object keys and non-finite numbers. Different consumers could interpret an ambiguous security document differently. | Shared strict decoder rejects duplicate keys at every depth, NaN/Infinity and floating-point overflow. Foundation checks every required JSON input; all four script entry points use strict decoding. Tests include nested duplicates and 1e999 plus a valid positive control. |
| CR-03 | Full and custom OpenAPI checks had different reference policies. Custom pointers accepted negative array indices; the full document reader opened its starting path before checking containment. Encoded network-style paths could reach path resolution. | Share one bounded reference-closure checker; check lexical/resolved JSON scope before reads, reject network-style encoded paths before resolution, enforce ASCII array indices and exact empty/trailing pointer semantics. Negative tests check pre-I/O rejection and both checker paths. |
| CR-04 | Fixture dictionaries and edge de-duplication could silently collapse conflicting/duplicate input IDs; filtering could hide dangling, invalid-pair or invalid-interval edges before validation. | Validate complete synthetic input nodes/edges, identities, visibility references, endpoints/type pairs and intervals before filtering/traversal. Tests cover duplicate nodes/edges and invalid hidden edges. This is fixture integrity, not runtime authorization. |
| CR-05 | Two independent claim IDs could reuse one tenant/connector/source_claim_id, contradicting the documented source-lineage identity. | Reject aliases across claim lineages while allowing the same external identity in distinct tenant/connector namespaces. Paired negative/positive tests retain valid namespace separation. |
| CR-06 | The approval schema allowed reconciled outcomes on execution_result and initial/partial outcomes on reconciliation, contradicting the documented state meanings. | Narrow outcome enums by record_type. Tests accept all documented valid stage/outcome pairs and reject cross-stage pairs. This does not implement approval authenticity, single-use consumption or an executor. |

The findings concern acceptance reliability, local file/reference boundaries and static contract consistency. No production exploitability or independent severity rating is claimed. Correcting them does not settle tenant isolation, legal applicability or outstanding review.

## Compatibility and trust limits

The approval record remains an unadopted P1 1.0 proposal; its accepted input set is intentionally narrowed to the already documented lifecycle. No deployed consumer or migration is assumed. The reviewer must assess compatibility before adoption. Other public contracts and phase gates remain unchanged.

The strict JSON decoder also rejects numeric values that overflow Python floats; future legitimately larger numeric domains need an explicit representation decision. File resolution is a static repository policy, not an operating-system egress sandbox or protection against concurrent filesystem mutation. Network paths are rejected before resolution in the exercised cases; current authorization, workload authenticity and cross-record value equality require future real entry-point checks.

The graph code is a synthetic conformance oracle: visibility lists are fixture inputs, cursor bindings are unsigned, and no policy database or token verifier exists. Output-page bounds do not substitute for production query/time/fairness limits. P2/P3 must enforce actual database/worker concurrency and resource controls.

JSON Schema cannot establish that trusted context was server-issued, that tenant/connector references agree across separate records, that an approval is current, or that audit committed durably. These remain acceptance paths in the governed backlog, with exact human approval/constrained execution in P4 and operational integration in P5.

The existing CI uses read-only repository permission, a pinned checkout action, no persisted checkout credential, pinned validation-only packages, wheels-only installation and dependency consistency checking. Package hashes, an independent vulnerability/license assessment, release SBOM and enterprise build/recovery proof remain outstanding; this review makes no vulnerability-free dependency claim. Main protection is not changed by a source patch.

## Verification and disposition

Meaningful regressions were added to existing modules plus a dedicated approval-outcome test module. The foundation verifier includes this report and that test module in its required files. The PR records actual local and Linux commands, missing/failed/skipped checks and exact results; prior main CI is not reused as proof of this candidate. All required cumulative checks must pass before human review readiness is reported.

Independent architecture/security and bilingual/regulatory reviewers, actual threat owners and risk dispositions, verified main merge enforcement and the formal P1 decision remain pending. The owner's instruction to receive phase-completion notice and review before any successor is retained. P2 has not started.

## الخلاصة العربية

شملت المراجعة كود أدوات التحقق الأربع واختباراتها الخمسة الموجودة والعقود الساكنة وCI. عولجت ست فجوات: تشخيص المدخلات الناقصة، ورفض JSON الملتبس، وتوحيد حدود المراجع قبل القراءة، ومنع إخفاء تعارضات بيانات الرسم، وتفرد سلسلة ادعاء المصدر، وربط نتيجة التنفيذ بمرحلتها الصحيحة. أضيفت اختبارات رفض وقبول فعلية لكل إصلاح.

هذه مراجعة من المنفّذ لنسخة P1؛ لا توجد خدمة مصرفية تشغيلية في الكود لتدقيقها. نجاح الفحوص لا يثبت العزل أو المصادقة أو تنفيذ إجراءات إنتاجية، ولا يغني عن المراجعة المستقلة أو حماية الدمج أو قرار اعتماد المرحلة.

Local preparation: Windows/Python 3.14.4 foundation exited 0. Full unittest discovery exited 1: 25 entries, 19 passed, five missing-validator module imports and WinError 1314 symlink privilege error; no skips. Original-base missing-backlog KeyError and duplicate-key last-value behavior were reproduced separately. Fresh candidate Linux results are required in the PR.
