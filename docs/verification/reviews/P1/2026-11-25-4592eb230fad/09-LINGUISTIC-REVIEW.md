# المراجعة اللغوية والتحريرية — REV-08

Reviewed repository: ManeaAlShabrain/QASCP · branch: main · commit: `4592eb230fadebb828c8b7d3b7972c6bd1aec012` · date: 2026-11-25, Asia/Riyadh.

AI-assisted review only; virtual specialties do not represent actual independent people.

النتيجة: **توجد فروق معنوية تتطلب المصالحة قبل قبول خط الأساس الثنائي**. الملاحظة QAR-005؛ أخطاء وصف API في QAR-009. قورنت الالتزامات والفاعل والنطاق والشرط والفشل، وليس المعرّفات وحدها.

| الموضع | النص الأصلي | النص المقترح | السبب والأثر |
|---|---|---|---|
| [docs/governance/ENGINEERING_GOVERNANCE.md:59](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/docs/governance/ENGINEERING_GOVERNANCE.md#L59) | Reviewer assessment and applicable static, unit, integration, and regression checks are required. | Human reviewer assessment and applicable static, unit, integration, and regression checks are required. | مقترح لتوحيد معنى «تُطلب مراجعة بشرية» في العربية. يقرر صاحب الصلاحية المعنى النهائي في PR واحد للغتين؛ لا نضعف المتطلب العربي تلقائيًا. |
| [docs/governance/ENGINEERING_GOVERNANCE.ar.md:59](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/docs/governance/ENGINEERING_GOVERNANCE.ar.md#L59) | تُطلب مراجعة بشرية والفحوص الساكنة واختبارات الوحدات والتكامل والانحدار المنطبقة. | تُطلب مراجعة بشرية، إضافةً إلى الفحوص الساكنة واختبارات الوحدات والتكامل والانحدار المنطبقة. | يبقى المعنى البشري محفوظًا؛ تفصل الصياغة بين المراجعة والفحوص وتمنع اللبس النحوي. |
| [docs/architecture/QASCP_2_BANK01_BLUEPRINT.ar.md:31](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/docs/architecture/QASCP_2_BANK01_BLUEPRINT.ar.md#L31) مقابل النسخة الإنجليزية:31 | اختيار مُصدّر يمكن إعادة إنتاجه بصورة مكافئة | اختيار محدد الإصدار يمكن إعادة إنتاجه بصورة مكافئة | versioned تعني محدد الإصدار، وليست exported. المعنى متعلق بإعادة بناء لقطة ثابتة، لا تصديرها. |
| [docs/architecture/QASCP_2_BANK01_BLUEPRINT.ar.md:84](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/docs/architecture/QASCP_2_BANK01_BLUEPRINT.ar.md#L84) | لا يعد الترقية غير منطبقة إلا بسبب مراجَع صريح عند غياب إصدار سابق مدعوم. | لا تُعدّ الترقية غير منطبقة إلا بمبرر صريح خضع للمراجعة، عند عدم وجود إصدار سابق مدعوم. | تصحيح التأنيث والمبني للمجهول ووضوح معنى reviewed reason؛ يحفظ شرط المراجعة ولا يجيز تجاوز الاختبار. أثر منخفض داخل QAR-005. |
| [contracts/qascp-2/graph/openapi-0.2.json:327](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/contracts/qascp-2/graph/openapi-0.2.json#L327) و460 | New logical observation | New import command durably accepted; projection state is reported separately. | مخرجات العمليتين CommandReceipt وليست إيصال observation. QAR-009. |
| [contracts/qascp-2/graph/openapi-0.2.json:337](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/contracts/qascp-2/graph/openapi-0.2.json#L337) و470 | Identical replay; previous observation ID | Identical command replay; previous command receipt. | تصحيح نوع المعرّف والحدث المنطقي دون تغيير schema أو سلوك runtime. QAR-009. |
| [scripts/verify_foundation.py](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/scripts/verify_foundation.py) / رسالة نجاح CLI | bilingual parity | structural bilingual parity | توضيح تحريري موصى به؛ الأداة تتحقق من version/IDs/order ولا تثبت المعنى. إجراءات التحقق تشرح الحد بالفعل، لذلك لا نعد الرسالة وحدها ادعاء اعتماد لغوي رسمي. |

## المطابقة المعنوية للحوكمة

| البنود | نتيجة المقارنة |
|---|---|
| GOV-001..004 | نطاق المرحلة ومنع الانتقال، المنشأ، PR وضبط اللغتين، الأشخاص الفعليون والاستقلال متوافقة إجمالًا؛ قرار التبني البشري غير موجود. |
| SEC-001..005 | سياق المؤسسة، DB/المشتقات، workload، تصنيف/أسرار، والتدقيق الذري تحمل المعنى نفسه في النصوص المقروءة. لا يعني ذلك أن الضوابط منفذة. |
| AI-001..002 | التنفيذ والموافقة البشرية، عدم الثقة، الامتناع والتقييم متوافقة. |
| ENG-001 | human review أكثر صراحة في العربية؛ فرق QAR-005 يحتاج حسمًا، ولا يُلغى شرط GOV-004 في أي لغة. |
| ENG-002..003 | فحوص فعلية وأدلة حديثة، تثبيت المدخلات والتصحيحات والمنشأ متوافقة إجمالًا. |
| OPS-001/CMP-001/REL-001 | الأهداف التشغيلية، الانطباق وعدم ادعاء الامتثال، والموانع والاستثناءات متوافقة إجمالًا. |
| BANK-01 B01..B06 / BA01..BA11 | النطاق والمعاملات والاختبارات المخططة محفوظة؛ فرق snapshot version والتركيب النحوي في BA10 أعلاه. |

السجل البنيوي يجتاز 17 معرّفًا مرتبة وإصدار 1.0 وP1..P6. لا يُعتمد استنتاج حزمة التسليم السابق بأنها لم تجد فرق التزام جوهري قبل معالجة هذه الملاحظات وتسجيل قبول المراجع الثنائي الفعلي. هذه المقترحات لم تُطبّق على ملفات المصدر.
