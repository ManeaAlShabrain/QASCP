# QASCP 2.0 - Qatar source review and regulatory handoff

P1 / V2-P1-03 / P1-V01, prepared 2026-11-17 (Qatar). Requirements: PRD-07, PRD-10, QASCP-CMP-001, QASCP-GOV-002..004 and QASCP-ENG-002. This implementer research note supports the [source register](REGULATORY_SOURCES.md); it is not independent regulatory review, adoption, client applicability or phase approval. [Stage authority](../verification/README.md) remains unchanged.

The change affects source metadata and review questions only. Acceptance: accurately separate retrieved source facts, retrieval limitations, proposed design associations, rights and outstanding reviewer decisions; preserve older access history and rerun cumulative candidate checks. No regulation text, PDF, private source material or new compliance obligation is incorporated.

## SR01 - Retrieval and evidence limits

Primary publisher URLs were inspected on the date above. Initial direct QCB PDF requests returned two 502 errors and a timeout; subsequent primary-URL search/open retrieval exposed PDF text for all three documents. The original NCSA assurance URL redirected to an unreadable publication page; a second official ncsa.gov.qa PDF supplied extractable text. These are primary-publication text observations through indexed/cached retrieval, not retained source binaries or evidence of a successful fresh origin download.

Selected identity, commencement, scope and review clauses were read. Search crawl/publication labels and URL directory years are not document versions, effective dates or an amendment history. No PDF hash, byte identity between alternate NCSA URLs, visual pagination verification, authoritative translation, latest-edition claim or absence-of-amendments finding is available. The immutable QASCP candidate identifies this note, not a frozen copy of its external sources.

## SR02 - Observed source identity and review pointers

| Source ID / primary publication | Identity facts observed | Selected review pointers and remaining action |
|---|---|---|
| QA-QCB-AI / [QCB AI guideline](https://www.qcb.gov.qa/Services/Financial%20Technology/QCB_Artificial_Intelligence_Guideline.pdf) | Section 1 identifies 2024 and commencement 2024-09-04. | Scope: section 5; inventory: 10.1; regulator approvals: 11.1-11.2; human oversight: 13.1. Reviewer must distinguish regulatory approval from a QASCP operator approval. |
| QA-QCB-DHP / [QCB data regulation](https://www.qcb.gov.qa/Documents/InformationSecurity/Data%20Handling%20and%20Protection%20Regulation.pdf) | Title confirmed; no explicit numbered edition or commencement date established in the inspected text. | Section 3 and Appendix 1 require scope/exemption review. Sections 11.1-11.4, 14.4.5 and 15.1 identify retention/deletion and foreign-transfer review. Do not turn a table value into a universal product timer. |
| QA-QCB-CLOUD / [QCB cloud regulation](https://www.qcb.gov.qa/Documents/InformationSecurity/Cloud%20Computing%20Regulation.pdf) | Section 1 states commencement 2024-04-15; no separate numbered revision established. | Section 5.1 is the scope pointer; 19.1-19.3 and 21.1 guide exit/access review. Deployment labels alone do not settle applicability. |
| QA-NCSA-NIA / [NCSA NIA standard](https://ncsa.gov.qa/sites/default/files/2024-01/NCSA_CSGA_%20National_Information_Assurance_Standard_En_V2.1.pdf) | V2.1, May 2023; section 6.2.2 addresses commencement. | Review sections 2.2-2.3 with the classification policy; AM 1 and SM 1 are access/monitoring pointers. Front-matter legal rights distinguish attribution from written permission for commercial reproduction. |

These are discovery pointers for the regulatory reviewer, not adopted clause-to-control compliance mappings. The [coverage matrix](QASCP_2_COVERAGE.md) remains a capability proposal. Bank/license, jurisdiction, deployment, processing role, data classification, exemptions, amendments and actual evidence must be reviewed before clause-level applicability is accepted.

## SR03 - Concrete P1 decisions and affected design

| Review item | Existing work / evidence needed | Actual reviewer and state |
|---|---|---|
| Separate source validity from entity applicability | V2-P1-03: obtain controlled authoritative editions, amendments, scope and any permission required; record the licensed entity, data/deployment context and interpretation. | Regulatory owner: unassigned; pending. |
| Keep approvals attributable to their actual authority | V2-P1-02/03: review how regulator, bank governance and QASCP action decisions are separately identified. A QASCP approval cannot be represented as approval from QCB. No new approval endpoint is adopted here. | Regulatory owner plus independent architecture/security reviewer: unassigned; pending. |
| Resolve retention, deletion and foreign access together | V2-P1-02/03: review B04/B06 in the [BANK-01 blueprint](../architecture/QASCP_2_BANK01_BLUEPRINT.md), with source classification, legal hold, backups, transfer/access paths and approved per-entity policy. No deployment default is chosen here. | Regulatory owner plus data/operations owners: unassigned; pending. |
| Resolve source reuse rights before adoption | V2-P1-03: QCB reuse permissions remain unverified; NCSA commercial reproduction needs rights review and any required written authorization. This repository stores original notes and identifiers, not copied controls/PDFs or a commercial reproduction permission. | Rights/regulatory reviewer: unassigned; pending. |
| Approve exact candidate only after required evidence | V2-P1-04/05: fresh checks, independent bilingual/security dispositions, verified main merge enforcement and authorized P1-V04 decision. | Authorized owner: decision pending. |

No role above is an assigned person, a grant of authority or an approval. Product architecture may be prepared independently while source adoption remains pending. No runtime test, legal conclusion, retained snapshot or certification is supplied by this review.

## SR04 - خلاصة عربية للمراجعة

هذه مراجعة بحثية من المنفّذ ضمن P1 وليست اعتمادًا تنظيميًا مستقلًا. تعذر الجلب المباشر أولًا، ثم أمكن فحص نصوص منشورة على روابط رسمية عبر الاسترجاع المفهرس أو المخزن. لم نحفظ ملفات المصدر أو نحسب بصماتها، ولم نثبت أنها أحدث النسخ أو أنها خالية من التعديلات اللاحقة.

| المصدر | ما رُصد وما يبقى للمراجع |
|---|---|
| QA-QCB-AI | يذكر البند 1 إصدار 2024 وبدء النفاذ في 4 سبتمبر 2024. تُراجع بنود النطاق والسجل والموافقات والرقابة البشرية؛ موافقة المنصة لا تمثل موافقة المصرف المركزي. |
| QA-QCB-DHP | ثبت العنوان، ولم يُحسم رقم إصدار أو تاريخ نفاذ. تُراجع الاستثناءات والاحتفاظ والحذف والنقل الخارجي؛ لا نعتمد مدة موحدة للمنتج من جدول المصدر. |
| QA-QCB-CLOUD | يذكر البند 1 بدء النفاذ في 15 أبريل 2024. تبقى مراجعة نطاق الترتيب السحابي والخروج والوصول، دون افتراض الانطباق من اسم بيئة النشر. |
| QA-NCSA-NIA | رُصد الإصدار 2.1، مايو 2023. تُراجع سياسة التصنيف والنطاق، وحقوق إعادة الإنتاج التجاري والموافقة الكتابية المطلوبة؛ ذكر المصدر وحده ليس إذنًا تجاريًا. |

يلزم تعيين مراجع تنظيمي ومراجع ثنائي اللغة ومراجعين مستقلين للأمن والمعمارية. تُراجع النسخة الرسمية والتعديلات وحقوق الاستخدام والجهة المرخصة والبيانات والنشر، ثم يسجل قرار الانطباق والأدلة. تبقى قرارات الجهة التنظيمية والبنك والمنصة منفصلة، وتُحسم سياسة الاحتفاظ والحذف والوصول الخارجي لكل جهة. لا يُسجل اعتماد المرحلة أو قبول مخاطر أو تنفيذ اختبارات مستقبلية في هذه المذكرة.
