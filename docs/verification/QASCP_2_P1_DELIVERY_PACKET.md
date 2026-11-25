# QASCP — حزمة تسليم P1 وقرارات القبول المتبقية

Prepared 2026-11-25. Phase: **P1 — Product and architecture foundation**.
Readiness: **Ready for human review after this packet's candidate CI passes**.
Formal phase exit: **Blocked / Pending review**.

هذه حزمة تسليم لما هو موجود فعليًا، وربط كل مهمة P1 بمعيار قبولها ودليلها.
ليست اعتمادًا للمرحلة ولا تعيينًا لمراجعين أو قبولًا للمخاطر. تبقى
[الحوكمة](../governance/ENGINEERING_GOVERNANCE.md) و[سجل المرحلة](README.md)
و[خطة العمل](../product/QASCP_2_BACKLOG.md) مراجع السلطة.

Requirements: PRD-01..10; QASCP-GOV-001..004, QASCP-SEC-001..005,
QASCP-AI-001/002, QASCP-ENG-001..003, QASCP-CMP-001 and QASCP-REL-001.
Canonical scope: V2-P1-01..05 / P1-V01..04. Affected interfaces: documentation
navigation, acceptance handoff and foundation required-file inventory only.

## 1. النسخة التي روجعت والأدلة الفعلية

Baseline main: **ea2fd32c9f3d21f6635ea3b17a02ae74cfe160d3**.
Tree: **be21e4ea712f1705c5dc41517082aced077e9e1a**, after merged
[#38](https://github.com/ManeaAlShabrain/QASCP/pull/38).

[Main Actions 45677821487](https://github.com/ManeaAlShabrain/QASCP/actions/runs/45677821487)
passed. Its [foundation log](https://github.com/ManeaAlShabrain/QASCP/actions/runs/45677821487/job/139429969139)
shows dependency consistency, the post-checkout local-auth check, both full
OpenAPI documents with security-policy operation counts 2/4, and **96/96 tests
passing, zero skips**. The [required gate](https://github.com/ManeaAlShabrain/QASCP/actions/runs/45677821487/job/139430120767)
passed. These are inspected baseline results. This packet's PR must bind its
own exact SHA and fresh cumulative result; baseline CI does not cover new files.

The isolated local tree matches that baseline tree. Existing edits in the
older checkout remain excluded. Counts below describe the 72-file baseline;
this packet adds one document. Local environment failures remain in the
[review record](QASCP_2_P1_REVIEW_2026-11-25.md) and the candidate PR.

## 2. المخرجات الثمانية المطلوبة — موجودة، واعتمادها منفصل

| المخرج المطلوب | الموجود والدليل | حدود الجاهزية |
|---|---|---|
| PRD شامل | [PRD 2.0](../product/QASCP_2_PRD.md): 10 متطلبات PRD-01..10، و24 مجالًا في ست مجموعات، ومستخدمون وحدود وتسلسل تسليم | موافقة النطاق في #13 تخص سجلها المحدد؛ لا تعني تنفيذ المجالات |
| معمارية وADRs | [المعمارية](../architecture/QASCP_2_ARCHITECTURE.md)، [سلطة الوثائق](../architecture/QASCP_2_SUPERSESSION.md)، [قرارات الرسم](../architecture/QASCP_2_GRAPH_DECISIONS.md)، [قرار CI](../architecture/QASCP_2_CI_CHECKOUT_DECISION.md) | قرارات مقترحة تحتاج حسمًا مستقلًا للتبني والمخاطر |
| Domain Model وData/API Contracts | [عقود المجالات](../architecture/QASCP_2_CONTRACTS.md)، 16 JSON Schemas، وعقدا OpenAPI 0.1/0.2 مع فحص كامل وسياسة مشتركة | عقود ساكنة؛ لا API أو PostgreSQL أو OIDC تشغيلي |
| حالات مصرفية مرتبة | BANK-01 أولًا، BANK-02 تاليًا، BANK-03..06 لاحقًا؛ [مخطط BANK-01](../architecture/QASCP_2_BANK01_BLUEPRINT.md) و[العربية](../architecture/QASCP_2_BANK01_BLUEPRINT.ar.md)، وستة أقسام B01..B06 و11 سيناريو BA01..BA11 | اختبارات BA التشغيلية مخططة في P2؛ لم تُنفذ هنا |
| Threat Model للمنصة | [T01..T12](../architecture/QASCP_2_THREATS.md): حدود المؤسسات والمصادر وAI والتدقيق والتوافر والاستعادة | الأدوار محددة، والأشخاص الفعليون وقبول المخاطر غير مسجلين |
| مصفوفة أطر ومصادر | [التغطية](../governance/QASCP_2_COVERAGE.md)، [سجل المصادر](../governance/REGULATORY_SOURCES.md)، [مراجعة قطرية](../governance/QASCP_2_SOURCE_REVIEW_2026-11-17.md) | ربط قدرات مقترح وفجوات صريحة؛ لا حكم امتثال أو اعتماد قانوني |
| مقاييس الأداء والدقة والاعتمادية | ملف LAB-GRAPH-01 المقترح في PRD، ومقاييس الربط والتدقيق وعدم تسرب البيانات والتحقق الانتقائي | الحدود العددية غير معتمدة وغير مقاسة؛ SLO/RTO/RPO للنشر تحتاج ملاكًا واتفاقًا |
| Backlog على GitHub | [19 حزمة V2-P*](../product/QASCP_2_BACKLOG.md)، مهام #13..#31، و[المتابعة #32](https://github.com/ManeaAlShabrain/QASCP/issues/32) | إغلاق Issues لا يثبت قبولها؛ خمس حزم P1 مقيمة أدناه |

وجود الفئات الثماني لا يعني اجتياز ثمانية اعتمادات. هذه مراجعة لتوفر
المخرجات وحدودها؛ شروط المراجعة والقرار في خطة العمل تبقى واجبة.

## 3. كل مهام P1 الخمس ومعاييرها

| الحزمة / GitHub | معيار القبول من الخطة | حالة الدليل والإجراء المطلوب |
|---|---|---|
| V2-P1-01 / [#13](https://github.com/ManeaAlShabrain/QASCP/issues/13) | PRD-01..10 وكل المجالات الـ24 محددة، مع قرار مالك النطاق | قرار نطاق وأولوية BANK-01 موجود على ac501e9ef2b80980ccfff9745f293d4e8fbd5ada. لا يعاد نسبه تلقائيًا لكل مراجعة أحدث أو لقرار الخروج |
| V2-P1-02 / [#14](https://github.com/ManeaAlShabrain/QASCP/issues/14) | تتبع المؤسسة والمنشأ عبر الواجهات، ومراجعة أمن مستقلة | التصميم والعقود والاختبارات الساكنة ومراجعات المنفّذ موجودة؛ يلزم مراجع مستقل فعلي، وحسم G-01..G-07 وB06 وتوافق العقود وملاك T01..T12 |
| V2-P1-03 / [#15](https://github.com/ManeaAlShabrain/QASCP/issues/15) | إصدارات وحقوق دقيقة أو فجوات معلنة، ومراجعة معنوية للترجمة | سجل المصادر يفصل المعلوم والمعلق؛ المقارنة التحضيرية أدناه مكتملة. يبقى قرار مراجع ثنائي/تنظيمي مؤهل على النسخة المحددة |
| V2-P1-04 / [#16](https://github.com/ManeaAlShabrain/QASCP/issues/16) | CI سليم، وPR سلبي محجوب بقاعدة فعّالة، ودليل المراجع | الأدلة التقنية موجودة: main ناجح، وقاعدة فعالة واختبار #37 محجوب وإصلاح ناجح. يبقى قبول المراجع المستقل لضوابط القبول الحساسة |
| V2-P1-05 / [#17](https://github.com/ManeaAlShabrain/QASCP/issues/17) | اعتماد مالك مخول ومراجعة مستقلة مرتبطة، دون مانع إلزامي | **Blocked**: لا قرار خروج رسمي ولا سجلات المراجعين والمخاطر المطلوبة. تجهيز نموذج القرار لا يصدره |

At inspection, #13..#17 and #32 were closed with no assignees. The latest
comments endpoints for #14..#17 were empty. Reviews endpoints for PRs
3, 5..12, 33..36 and 38 returned empty lists. These are inspected evidence
locations, not proof about every possible off-platform record. No qualified
independent acceptance record was supplied for this candidate. Existing issue
state is preserved; closure is not counted as acceptance.

## 4. مراجعة المعنى العربي والإنجليزي — تهيئة من المنفّذ

Method: compare actor, obligation/prohibition, scope, authority, evidence and
failure/exception behavior, not only heading counts. Both current handbooks
were read clause by clause at the baseline. No material obligation difference
was identified in this implementer comparison; a qualified reviewer must
still record their own substantive disposition. No translation approval is
claimed.

| ID | المعنى الذي تمت مقارنته |
|---|---|
| QASCP-GOV-001 | نطاق المهمة والنسخة والدليل والمعتمِد، ومنع انتقال المرحلة بمجرد الدمج |
| QASCP-GOV-002 | التصميم المستقل والمنشأ والحقوق ووقف التبني غير المحسوم |
| QASCP-GOV-003 | PR للتغيير الحساس، ضبط اللغتين، وفصل الفحص البنيوي عن المراجع المعنوي وفرض الحماية |
| QASCP-GOV-004 | مسؤولية المالك والمنفّذ والمراجع المستقل والمسؤول التنظيمي، ومنع اعتبار المراجعة الذاتية مستقلة |
| QASCP-SEC-001 | سياق المؤسسة الموثوق قبل البيانات وعزل واجهات التهيئة والحياة |
| QASCP-SEC-002 | عزل الجداول والربط والمراجع والأدوار والاتصالات والصيانة والاستعادة |
| QASCP-SEC-003 | العزل عبر المشتقات والطوابير والرسوم والتقارير والاسترجاع ومنع الاستنتاج |
| QASCP-SEC-004 | أقل الصلاحيات وفصل المستخدم عن أحمال العمل والبيانات والأسرار والاختبارات الاصطناعية |
| QASCP-SEC-005 | حقول التدقيق والتخزين المقيد ومنع الحمولة الحساسة والفشل الذري |
| QASCP-AI-001 | منع كتابة AI في الإنتاج، وربط القرار البشري الدقيق بمنفّذ مستقل وإعادة التحقق |
| QASCP-AI-002 | عدم الثقة بالمحتوى المسترجع والمخرجات، والتقييم والامتناع وعدم منح التفويض |
| QASCP-ENG-001 | اكتمال مسارات التشغيل ومعالجة الفشل ومنع المسارات الصورية؛ فحص P1 ساكن |
| QASCP-ENG-002 | نقاط دخول وتبعيات فعلية حيث تنطبق، وانحدار تراكمي ودليل حديث وإظهار الفشل |
| QASCP-ENG-003 | منشأ وتراخيص وتثبيت المدخلات وسلامة الحزمة، وفصل التصحيحات عن حداثة الإصدار |
| QASCP-OPS-001 | التثبيت والترقية والاستعادة والاستجابة والأهداف المتفق عليها قبل النشر |
| QASCP-CMP-001 | هوية المصدر والنطاق والانطباق والدليل والمراجع، ومنع ادعاء الامتثال قبل التحقق |
| QASCP-REL-001 | موانع القبول، وضوابط التأجيل المحدود دون تجاوز الالتزامات الإلزامية |

Automated structural cross-check: 17 identical ordered IDs, handbook version
1.0 and P1..P6 order. The BANK-01 editions retain B01..B06 and BA01..BA11,
including the same unassigned-owner/independent-review boundaries in B06.
SEC-004 workload terminology and ENG-003 patch terminology from #33 remain
aligned. Matching identifiers alone is not semantic acceptance.

## 5. الأمن والمعمارية: أسئلة القبول المتبقية

The original [threat register](../architecture/QASCP_2_THREATS.md) remains
authoritative. This table does not assign people, accept residual risk or
change its initial likelihood/impact ratings.

| Threats | المطلوب من المراجع / المالك الفعلي |
|---|---|
| T01 / T02 | تتبع السياق وRLS والمفاتيح المركبة وإعادة استخدام الاتصال؛ تعيين الأمن والخلفية |
| T03 / T04 | سلطة المصدر ومنع التكرار والنسخ والتصادم وإعادة التعيين؛ تعيين التكامل والكشف |
| T05 / T06 | حدود الاسترجاع وAI والموافقة الدقيقة والتنفيذ وإعادة المطابقة؛ تعيين أمن AI وسير العمل |
| T07 / T08 | الزمن والتبعيات والتدقيق والحيازة والتصدير؛ تعيين الضمان والأمن |
| T09 / T10 | الاعتماديات وCI والحزم والحدود والإنصاف؛ تعيين البناء والمنصة |
| T11 / T12 | الاستعادة والأدلة وادعاءات الانطباق؛ تعيين العمليات والمسؤول التنظيمي |

قبل قبول التصميم يلزم حسم استراتيجية تكامل سجل المورد والمجال، وسلطة
حقول المصادر، وترتيب تعادل الزمن، وأجيال الإسقاط واللقطات والاحتفاظ،
وتوافق العقد الأصلي واللاحق. توجد خيارات وآثار وفحوص مخططة في G-01..G-07
ومخطط BANK-01؛ لا نحول أسئلة المراجعة إلى قرارات معتمدة من المنفّذ.

## 6. المصادر والحقوق والمقاييس

The source/coverage registers contain **15 source entries**. The NIST CSF,
AI RMF and SSDF entries state specific editions; ATT&CK/ATLAS/OWASP version
adoption remains pending. Selected QCB/NCSA source identity observations were
recorded on 2026-11-17 with retrieval/amendment/rights limits. Other entries
remain discovery or pending. This packet rechecks the repository's source
traceability, not external publication currency or legal applicability.

حقوق إعادة الاستخدام والتعديلات والنطاق لكل جهة وبيانات ونشر يراجعها
المسؤول التنظيمي. لا نصدر استنتاجًا قانونيًا أو اعتماد امتثال، ولا ننسخ
نصوص المعايير أو ملفاتها. تبقى فجوات الإصدارات والحقوق صريحة، وفق معيار
V2-P1-03، ويحتاج قبولها إلى قرار المراجع.

LAB-GRAPH-01 is proposed: two synthetic tenants, 10,000 nodes/50,000 edges
each; 10 events/s for 30 minutes and a 100 events/s 60-second burst.
Proposed p95 targets: bounded graph <=500 ms, intake <=1 s, projection lag
<=10 s. These are unapproved and unmeasured. Correlation precision/recall,
missing context, audit completeness and selective/full assurance equivalence
must retain denominators and failure cases. Client availability/RTO/RPO and
load acceptance remain deployment decisions, not invented P1 measurements.

## 7. ما ينفذ ويختبر الآن وما يبقى للمرحلة التالية

| الموجود القابل للتشغيل في P1 | الاختبار المنفذ |
|---|---|
| Foundation verifier | ملفات وروابط وUTF-8 وJSON صارم وتطابق بنيوي وتتبع PRD/backlog/evidence |
| Full OpenAPI verifier + shared policy | العقدان الفعليان، حدود المراجع المحلية ورفض الإضعاف الأمني |
| Synthetic graph record/query oracles | اتساق السلاسل والتكرار والزمن والصفحات والحدود والمنشأ في fixtures |
| CI and repository rule | 96 اختبارًا، CodeQL، أقل الصلاحيات، checkout مثبت وفحص إعدادات المصادقة المحلية، بوابة إلزامية |

[Enforcement snapshot](evidence/main-enforcement-2026-11-25.json) captures the
active main rule, required check/App 15368, strict updates and empty bypasses.
[Negative #37](https://github.com/ManeaAlShabrain/QASCP/pull/37) was open/non-draft
at its failed head and reported mergeable_state=blocked. Its repaired positive
control passed and it closed without merge. No merge endpoint or override was
attempted. #38 changes preserve the required gate contract; its fresh healthy
CI is separate from the earlier negative observation.

A source path or fixture schema is not runtime delivery. No FastAPI service,
real PostgreSQL/RLS, operational OIDC, signed cursor/key service, customer
connector, AI server, executor or command-center UI is present. No runtime
isolation, performance, recovery, certification or banking-production readiness
is claimed. Those real-entry-point checks belong to the component phases and
are not reported as skipped P1 application tests.

P1 is the first phase, so there is no earlier approved phase to regress.
Its cumulative foundation/contract/oracle/security regressions remain required.

## 8. سجل القرار المطلوب لإغلاق P1

The authorized participants must supply actual decisions in an access-controlled
review source; this checklist does not fill them in.

| Required field | Current status / next action |
|---|---|
| Reviewed candidate and scope | Baseline above; final packet candidate/CI bound by its PR |
| Actual qualified independent security/architecture reviewer | Not assigned/recorded; include identity, qualification, independence, findings and disposition |
| Actual substantive bilingual and regulatory/rights reviewers | Not assigned/recorded; include source/edition/scope and accepted remaining gaps |
| Actual owners and risk dispositions for T01..T12 | Missing; names, scope and residual-risk decisions required |
| Complete candidate checks and enforcement evidence | Baseline available; retain fresh packet candidate run and snapshot limits |
| Authorized product-owner phase decision | Missing; accept/request changes/reject with exact SHA, date/time, evidence and conditions |
| Official stage-record update | Pending actual approvals; keep P1 / Pending review until then |

تكتمل خطوة المنفّذ بإعداد المخرجات والأدلة والملخص وتقديم حزمة واحدة
قابلة للمراجعة. لا نستطيع إكمال واجب المراجع المستقل أو قبول المخاطر
أو إصدار قرار المالك نيابة عنه. لا تُنشأ استثناءات لتجاوز هذه المدخلات.

After those records exist, a governed stage-record PR can link the actual
reviewed revision and exit decision. Notify the owner that P1 is complete and
review its evidence **before** beginning V2-P2-01. This packet does not start P2.

## English handoff summary

All eight requested artifact categories are present. The 72-file baseline has
24 target domains, 10 product requirements, six banking scenarios, 16 JSON
Schemas, two API proposals, 17 bilingual governance requirements, twelve design
threats, 19 backlog packages and 96 passing static/tool tests. P1's five work
packages have the individual dispositions above. **Documentation/tool readiness
is distinct from formal P1 completion, which remains blocked by actual human
review, ownership and phase-exit records.**


## Correction following independent audit #43 — 2026-11-25

The preceding implementer comparison is retained as history, not current acceptance.
QAR-005 disproved its no-material-obligation-difference conclusion: ENG-001 lacked
explicit human reviewer wording in English and Arabic BANK-01 mistranslated versioned
selection as exported selection. The corrected candidate retains human review in
both editions and uses اختيار محدد الإصدار. See the [clause comparison and glossary](P1_BILINGUAL_REMEDIATION.md).
This implementation pass cannot accept its own translation or replace the still
missing independent human/regulatory disposition. #43's original rejection and
72.95 score remain unchanged. P1 remains pending; no P2 authorization is supplied.
