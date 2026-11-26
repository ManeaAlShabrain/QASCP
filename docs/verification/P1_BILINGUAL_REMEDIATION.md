# Bilingual terminology and correction record — QAR-005 / Issue #41

Current-disposition note, 2026-11-26: the comparison below is preserved as the
historical baseline 1.0 correction pass, not the current baseline 1.1 comparison.
Its statements that GOV-004 is unchanged and baseline remains 1.0 apply to that
earlier pass only. The owner later approved the scoped proposal in
[GOV-DEC-001](../governance/decisions/GOV-DEC-001.md); the paired 1.1 handbook and
[process](../governance/SOLO_ASSURANCE_PROCESS.md) supersede that current-status
interpretation, with activation still pending the required dispositions.
The separate 2026-11-26 review identified an additional SEC-002 capability
ambiguity; the new candidate makes the shared-metadata service/access-path
prohibition explicit in both editions. Original reports and correction history
are preserved; a new candidate requires affected substantive re-review.

## Historical baseline 1.0 comparison and glossary

Prepared by the implementation assistant, 2026-11-25; GOV-003/004, ENG-001,
PRD-06/09; P1-V01. This is a substantive comparison and correction proposal,
not an independent linguistic or regulatory acceptance. The complete paired
documents are the two handbooks and two BANK-01 blueprints. Other Arabic
continuity notes are summaries, not substitute normative editions.

## Corrections

| Location | Earlier wording | Corrected wording | Preserved obligation / consequence |
|---|---|---|---|
| English ENG-001 | Reviewer assessment | Human reviewer assessment | Explicit human review, matching Arabic and GOV-004 actual people; no solo-policy exception applied. |
| Arabic ENG-001 | تُطلب مراجعة بشرية والفحوص… | تُطلب مراجعة بشرية، إضافةً إلى الفحوص… | Separates the human obligation from automated checks. |
| Arabic B02 snapshot | اختيار مُصدّر | اختيار محدد الإصدار | Version identity and reproducibility, not export. |
| Arabic BA10 | لا يعد الترقية غير منطبقة إلا بسبب مراجَع صريح… | لا تُعدّ الترقية غير منطبقة إلا بمبرر صريح خضع للمراجعة… | Upgrade test inapplicability still requires reviewed reason. |
| Foundation CLI | bilingual parity | structural bilingual parity | The tool cannot judge substantive meaning. |
| Earlier delivery packet comparison | No material obligation difference identified | Appended dated correction acknowledging QAR-005 | Historical wording retained, conclusion superseded as an implementer assessment; audit #43 unchanged. |

Baseline label stays proposed 1.0 because these corrections clarify the existing
human/version obligation without adopting a new policy. Both editions carry a
dated correction note. GOV-004 remains unchanged; a proposed policy revision
requires the separate ADR/change-request PR and explicit owner decision.

## Clause comparison: actors, obligation, scope and conditions

| Clause | Same substantive commitment checked in both languages | Residual reviewer task |
|---|---|---|
| GOV-001 | Implementer identifies scope/IDs/interfaces; authorized owner closes exact revision; PR/issue/CI never imply exit; dependencies/exceptions explicit. | Verify exact-candidate approval remains missing. |
| GOV-002 | Original implementation; prohibit copied external structure/code/fixtures; provenance/rights/ADR before adoption; suspend uncertain adoption. | Independent rights/adoption review pending. |
| GOV-003 | PR for sensitive changes; same meaning/version/order in paired edits; substantive bilingual reviewer separate from structural tool; verify enforcement. | Independent substantive and control disposition required. |
| GOV-004 | Product owner, implementer, qualified independent reviewer, regulatory owner and release operator have separate responsibilities; actual people/decisions recorded; self-review insufficient. | No real reviewer or decision invented; separate governance proposal does not amend this row. |
| SEC-001 | Trusted tenant context before access; membership from server; selector is not authority; bootstrap/liveness isolated. | User/customer plane and internal customer jobs share scope in both editions. |
| SEC-002 | Every tenant table/join/reference/write scoped; mandatory data filtering and DB controls; non-bypass roles; pool/worker/maintenance/restore preserve isolation. | Independently review design now; actual DB tests P2/P6. |
| SEC-003 | Tenant applies to derived stores, graph, evidence, exports, retries and AI retrieval; prevent cross-tenant read/inference/mutation/reference. | Counts/metadata cannot disclose hidden data. |
| SEC-004 | Default deny/least privilege; distinguish users from all workload roles, including services/connectors/workers/jobs; minimize/classify/encrypt/rotate; synthetic-only development. | Existing workload clarification retained, no narrower services-only reading. |
| SEC-005 | Restricted append audit, actor/type/scope/time/outcome/correlation; exclude secrets; required audit failure blocks sensitive success or atomic delivery. | Append-only is a design obligation, not a present storage claim. |
| AI-001 | AI has no production write credentials/direct executor; exact authorized human action/version/target/parameters/expiry; separate executor revalidates; deny changed/expired/revoked/reused approval. | Owner software approval cannot substitute for customer production authorization. |
| AI-002 | Model/retrieved text untrusted; tenant/data policy first; evaluation/prompt/model versions; cite/abstain/escalate; output grants no authority/compliance. | Evidence insufficiency and human escalation preserved. |
| ENG-001 | Complete supported paths/failures/concurrency; no unfinished production stubs/fake evidence/fallback; human assessment plus applicable tests; P1 only docs/verifier. | English actor now explicitly human; independent review still pending. |
| ENG-002 | Real entry points/dependencies, applicable cumulative regression, immutable revision/environment/results; failed/skipped/cancelled/missing/stale checks block; reviewed N/A and reruns. | Windows six errors are errors, not passes or skips. |
| ENG-003 | Provenance/licenses/maintenance, pinned inputs/minimal CI, deliverable SBOM, scans and exact-artifact binding; unpatched differs from merely older. | Hash verification and pip check are not exhaustive security clearance. |
| OPS-001 | Before client/production: install/upgrade where applicable/restore/recovery/audit/exact artifact; agree targets first; authorized incident channel. | No P1 runtime result asserted. |
| CMP-001 | Issuer/version/date/clause/entity/data/deployment/control/evidence/reviewer; permitted snapshots; scoped pending/assessed/insufficient/approved states; no premature external compliance claim. | Legal applicability/rights need qualified actual reviewer. |
| REL-001 | Binding unmet requirement, unverified control, high/critical issues, isolation/authorization/data loss block; limited approved deferral with owner/expiry; mandatory boundaries not waivable. | Governance proposal is not a waiver. |

## Blueprint comparison

| Paired section | Meaning checked | Remaining independent decision |
|---|---|---|
| B01 | Same candidate contract family; originals retained; no P2 until exit; later finding/AI/assurance phases separate. | Adopt exact version/compatibility. |
| B02 | Tenant registry/domain/binding/observation/command/claim/audit/projection/receipt/snapshot owners; immutable kind and same-tenant keys; no name conflation; snapshot reproducibly versioned. | Constraint/source authority/snapshot strategy review. |
| B03 | T1/T2/T3 separate atomic units; audit failure rollback; timeout replay; outbox dispatch is not completion; policy before graph expansion. | Human/domain ownership and planned crash matrix. |
| B04 | Source-valid vs server knowledge time; internal monotonic position; isolated rebuild generation and explicit activation; deletion/revocation across stores. | Retention and equal-time historical contract remain scoped decisions. |
| B05 | Two synthetic tenants, real API/DB roles later; static oracles are no runtime substitute. | Execute BA criteria at their authorized phases. |
| B06 | Actual reviewers unassigned; ownership/compatibility/translation/source/exit decisions required. | No approval inferred from role labels. |
| BA01 | Import/observe/project/read trace, no invented finding. | P2 execution. |
| BA02 | Cross-tenant selector/reference/read/write/join/FK denial without disclosure. | P2 execution. |
| BA03 | Pool reuse/rollback/missing or expired context isolation. | P2 execution. |
| BA04 | Identical replay once, digest conflicts, distinct events processed, replica logical effect once. | P2 execution. |
| BA05 | Crash around each commit/ack; audit outage; no lost accepted work or duplicate effect. | P2 execution. |
| BA06 | Current source/workload permission before replay/projection; ambiguous mapping quarantined. | P2 execution. |
| BA07 | Hidden-hop/count/provenance denial; tamper/revocation/expiry/budgets; no fabricated empty completion. | P2 execution. |
| BA08 | Shared command-key scope, expected versions, type constraints, terminal withdrawal and attributable history. | P2 execution. |
| BA09 | Equal timestamps/interleaved commits/lag/revocation and no mixed-generation pages. | P2 execution. |
| BA10 | Separate migration/runtime roles, RLS/registry rollback, reviewed upgrade N/A reason. | P2 execution; Arabic grammar corrected. |
| BA11 | Same authorized IDs/qualifiers/state/UTC meaning, Arabic RTL/English LTR, keyboard/contrast; no concealed-count leak. | P2 execution. |

## Terminology glossary

| English | العربية | Intended boundary |
|---|---|---|
| Qualified independent human reviewer | مراجع بشري مستقل مؤهل | Actual attributable person; AI session is not this role. |
| Functionally separate AI review | مراجعة ذكاء اصطناعي منفصلة وظيفيًا | Separate session with immutable input and declaration; shared service/account limits remain. |
| Authorized approval | موافقة مخوّلة | Attributable scoped decision; never model output or inferred merge approval. |
| Versioned selection | اختيار محدد الإصدار | Reproducible selection tied to versions; not exported selection. |
| Snapshot / generation | لقطة / جيل إسقاط | Stable authorized selection / distinct read-model build. |
| Source-valid time | وقت سريان حقيقة المصدر | Half-open source interval. |
| Knowledge cutoff | حدّ وقت المعرفة | Server-committed known set, not global completeness. |
| Projection / completion | إسقاط / اكتمال الإسقاط | Derived graph update / verified relevant checkpoint result, not command receipt. |
| Command receipt / observation receipt | إيصال أمر / إيصال ملاحظة | Separate logical identities and durable transactions. |
| Entitlement / observed use | صلاحية ممنوحة / استخدام مرصود | Distinct source assertions; neither establishes compromise. |
| Workload | حمل عمل آلي | Includes services, connectors, workers and scheduled jobs. |
| Residual risk | مخاطر متبقية | Evidence-based assessed remainder; no acceptance by assigning an owner. |
| Applicability / compliance / certification | انطباق / امتثال / تصديق | Separate source scope, evidence assessment and authorized external claim. |
| Backward compatibility | التوافق مع الإصدارات السابقة | Preserve documented supported client behavior; strict schemas can make added fields breaking. |

Disposition requested: an independently initiated linguistic/regulatory review of
the immutable corrected candidate and this table; record identity/session, sources,
findings, actual edits, qualifications/independence limits and decision. No reviewer
is assigned and no acceptance is issued in this implementer document.
