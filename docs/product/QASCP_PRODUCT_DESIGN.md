# QASCP product design and independent development

Proposed P1 design. Implementation and acceptance follow the active phase in the [verification record](../verification/README.md). See the [P1 architecture](../architecture/P1_ARCHITECTURE.md) and the [prior-art search record](../research/QASCP_PRIOR_ART.md).

## Product identity

**Primary users:** The SOC analyst investigates a security event. A control owner decides what needs to be rechecked. An independent reviewer reconstructs why a result was accepted or rejected.

**Product promise:** Trace each assurance decision to its evidence, and show what must be verified again when that evidence or its context changes.

**Arabic:** اعرف لماذا اعتُمدت نتيجة الضمان، وما الذي يجب التحقق منه عند تغيّر دليلها أو سياقها.

QASCP uses a case workspace with four task views: **investigate · assess impact · reverify · review history**. The workspace emphasizes the case timeline, ownership, evidence, and current assurance state. Arabic and English use the same decision identifiers, with appropriate direction and labels. The design relies on outcomes from authorized sources and human decisions.

## ملخص التصميم بالعربية

تبدأ تجربة المستخدم من قضية واحدة، ينتقل فيها محلل الأمن من الحدث إلى الأصل ومالكه وسبب الربط. يرى مسؤول الضابط النتائج التي تحتاج إلى إعادة تحقق، ويتولى المراجع المخوّل تقييم الدليل الجديد. يرى المدقق الحالة الحالية، وما كان متاحًا لحظة اتخاذ القرار السابق.

يحتفظ كل تقييم بإصدار الضابط والأدلة التي استند إليها ونطاق المؤسسة. نسجل وقت حدوث الملاحظة ووقت وصولها إلى المنصة، حتى يظهر أثر الدليل المتأخر دون تعديل السجل التاريخي. يُعاد فحص النتائج المتأثرة، مع توسيع الفحص عند نقص بيانات التبعيات أو عدم اكتمال تدفق الأحداث. نقص الدليل يضع النتيجة في حالة «تحتاج إلى تحقق». وتُسجل حالة الفشل عندما يثبتها اختبار أو تقييم مخوّل.

نقيس التصميم بمقارنته بإعادة تقييم كامل على السيناريوهات نفسها. نتابع الحالات المتأثرة التي فاتت النظام، وعدد الفحوص المطلوبة، والزمن، والقرارات التي يستطيع المدقق إعادة تفسيرها بالأدلة التي يحق له الوصول إليها.

## The workflow

| Step | What the user sees | Linked record | Phase |
|---|---|---|---|
| Investigate | A source event, related asset, owner, and the basis of the association | Tenant-scoped event and source references | P2–P3 |
| Assess impact | Which assurance assertions may need review and the first supporting fact that changed | Versioned assurance assertions and their evidence dependencies | P5 |
| Reverify | Assigned follow-up with required observations and acceptance criteria | New evidence, verifier, policy version and decision | P5 |
| Review history | What the reviewer could see at the earlier decision time and what is known now | Immutable decision history and scoped evidence access | P5–P6 |

The platform derives status for each scoped assurance assertion separately. An assertion records the tenant, subject, control version, supporting observations, and approval context. Record both when an observation applied in the source and when QASCP learned about it. A late report or correction can invalidate a current result and qualify a historical view without silently overwriting the earlier decision. The prior view is bounded by information available at its recorded cutoff.

### Proposed technical mechanism for evaluation

Changes include source configuration version, evidence expiry or revocation, and a superseded policy version. For the tenant and authorized subject scope, identify assertions whose recorded dependencies could be affected. Limit re-verification to that set only if the system can confirm that dependency records are complete and identify which source events have been processed. If a required source, dependency or timeframe is uncertain, mark the affected scope as needing verification and use a broader reconciliation. Preserve the reason for each transition. Protect concurrent updates against decisions from superseded snapshots. The state **needs verification** indicates insufficient current support. A controlled test or authorized assessment can establish **failed**.

A reviewer reproduces the rules-based evaluation using retained input versions and an authorized historical view. A human decision is retrieved as an attributed record. AI suggestions are retained with provenance when used. Reconstructing an assertion does not require reproducing a model response or rerunning an operational action. New tests and human decisions follow the existing governance requirements.

## Banking walkthrough

An authorized configuration source reports that a service account changed scope. An earlier assurance assertion relied on a permissions observation for that account. QASCP links the event to the account, its accountable owner and the affected assertion, records why the assertion needs verification, and assigns re-verification. An unrelated backup assertion remains current when its dependencies are verified and unchanged. A reviewer can inspect what supported the earlier decision and when the change was observed. After an authorized reviewer evaluates fresh evidence, the system records the new decision separately.

## How to measure the design

Compare selective re-verification with full re-evaluation on the same versioned synthetic dataset and event sequence. The full evaluation is the reference for candidate output, and hand-reviewed scenarios validate the expected behavior of both methods.

- **Correctness:** Compare affected assertion IDs, final states, and stated reasons. Require zero missed affected assertions in the approved test set. Report denominators and every mismatch. Cover parallel updates, late and duplicate events, expiry, source gaps, and fallback reconciliation.
- **Cost:** Compare evaluations per change, processing time, and p95 latency under the same workload. Report the number of unnecessary checks and the fraction of cases requiring broad reconciliation. Establish numerical performance thresholds after the pilot profile is agreed.
- **Audit:** Measure the fraction of decisions that can be reconstructed with the retained evidence and permitted access. Verify that access revocation and retention rules are respected in historical review.
- **Tenant isolation:** Test that evidence, dependencies, background evaluations, logs and exports never cross the tenant boundary in the approved scenarios.

## Independent design record

Capture requirements and their owners before implementation. Record design options, rationale, source provenance, document versions, license terms, author and dated approval in the relevant ADRs. Link implementation commits and tests to those decisions. Treat external product documentation and patent publications as comparison evidence. Preserve an access-controlled record of comparisons, design revisions, contributors and experiments. Review the name and branding separately before external launch.
