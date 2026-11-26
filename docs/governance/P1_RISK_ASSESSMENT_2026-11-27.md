# P1 risk assessment and treatment disposition — 2026-11-27

Status: **ASSESSMENT PREPARED / READY FOR RE-REVIEW**. Prepared by implementation
engineer under P1-PREP-001, not an independent auditor or owner approval.
QAR-002; GOV-004,SEC-001..005,AI-001/002,ENG-002,REL-001;P1-V01/02.

## Method and scope

Evaluate the documented future threat/vulnerability and available evidence for
all12risks. Likelihood is a qualitative exposure judgment (Medium: credible
conditional path; High: expected hostile input or routine repetition), not a
frequency/probability measurement. High impact means major confidentiality,
integrity or availability harm; Critical includes tenant-wide compromise,
uncontrolled production mutation or loss of recoverable evidence. Existing
High/Critical inherent bands are retained conservatively; no numeric product,
calibrated score, zero-risk claim or automatic probability multiplication is used.

P1 delivers designs/tooling, not a banking service. Runtime residuals retain the
inherent band because planned operational controls cannot justify reduction.
This is an assessed conservative disposition, not a null rating or a claim
that future High/Critical operation is acceptable. The current permitted work
is synthetic internal design/development without customer data or production
connections. No affected feature may pass its named gate with an unverified
isolation/auth/audit control. Design progress does not waive an applicable gate.

| Risk | Likelihood | Impact | Inherent | Current potential-runtime residual | Verification gate | Evidence-based rationale |
|---|---|---|---|---|---|---|
| T01 | Medium | critical | Critical | Critical; not operationally accepted | P1-V02, P2-V01, P3-V01 | A forged selector can expose another tenant; P1 schemas cannot establish RLS or trusted membership. Critical impact retained. |
| T02 | Medium | critical | Critical | Critical; not operationally accepted | P1-V02, P2-V01 | Connection reuse is a credible cross-tenant path when context outlives its transaction; no real pool exists yet. |
| T03 | High | high | High | High; not operationally accepted | P1-V02, P2-V01, P3-V01 | External observations are hostile inputs and retries are routine; no authenticated deployed adapter or concurrency proof exists. |
| T04 | Medium | high | High | High; not operationally accepted | P1-V02, P3-V01 | Repeated names and source identifiers are plausible; incorrect conflation changes banking impact. Source-binding invariants are design evidence only. |
| T05 | High | high | High | High; not operationally accepted | P1-V02, P4-V01 | Retrieved adversarial text is expected at the future AI boundary; no model/tool path exists in P1, so no reduced runtime likelihood is inferred. |
| T06 | Medium | critical | Critical | Critical; not operationally accepted | P1-V02, P4-V01, P5-V01 | An incorrect or repeated approval may mutate a critical target; no executor exists. Future ambiguous remote results remain unsafe to retry. |
| T07 | Medium | high | High | High; not operationally accepted | P1-V02, P5-V01 | Late/corrected evidence is ordinary; incomplete dependency coverage could retain an unsupported assertion. Assurance runtime is not built. |
| T08 | Medium | high | High | High; not operationally accepted | P1-V02, P2-V01, P5-V01, P6-V01 | Audit/log/export exposure can reveal sensitive evidence or hide actions. Runtime append-only storage and export authorization remain untested. |
| T09 | Medium | critical | Critical | Critical; not operationally accepted | P1-V02, P2-V02, P6-V01 | Real reviewed guard/hash-lock/least-privilege checks reduce specific paths, but hosted-runner, upstream and advisory gaps remain; no quantified reduction justified. |
| T10 | High | high | High | High; not operationally accepted | P1-V02, P3-V01, P6-V01 | A cyclic or high-fanout graph can amplify resource work; static bounded fixtures are not measured service quotas or queue fairness. |
| T11 | Medium | critical | Critical | Critical; not operationally accepted | P1-V02, P6-V01 | Restoring stale grants or losing evidence has critical effect; no backup or recovery service is delivered, so no recovery claim is possible. |
| T12 | Medium | high | High | High; not operationally accepted | P1-V01, P1-V02, P5-V01, P6-V01 | A reader can mistake a framework mapping for certification; explicit pending labels are current design controls, not legal or UI acceptance. |

## Ownership, treatment and review

All12actual internal owners remain confirmed in RISK-DEC-001; this does not
assign a bank's or regulator's obligations. The full [machine-readable register](P1_RISK_OWNERSHIP.json)
retains asset/threat/vulnerability, controls, treatment, authority, evidence and
target phase. Review dates and risk-acceptance references remain unset until a
real attributable review/decision occurs. No acceptance reference is required
merely to document a treatment plan that explicitly does not accept operation.

Owner endorsement requested: accept the P1 design/treatment plan and continue
only controlled synthetic development, keeping runtime acceptance blocked until
each applicable test passes. This is not acceptance of High/Critical operational
risk, a mandatory-control deferral, or approval of an incomplete production path.
Separate reviewers must challenge every rationale, control attribution and
phase boundary. If a High/Critical defect in the currently delivered P1 tooling
is found, it blocks this candidate; it cannot be reclassified as future risk.

Review again before affected feature acceptance, on any exposure/control/data
change, or2026-12-27, whichever occurs first. Unaccepted runtime risks stay open
with owner and tests at P2–P6. A future risk acceptance must identify scope,
authority, compensating controls, rationale and expiry; an owner cannot accept
another party's legal obligations.

## الخلاصة العربية

قُيّمت المخاطر الاثنا عشر نوعيًا مع مبرر لكل احتمال وأثر وخطة معالجة وبوابة
اختبار. تبقى التقديرات المتبقية العالية والحرجة محافظة دون تخفيض؛ فالتصميم
والاختبارات الساكنة لا تثبت ضوابط تشغيلية لم تُبنَ. المقترح اعتماد خطة التصميم
والمعالجة للتطوير الداخلي الاصطناعي فقط، لا قبول تشغيل معرض لتلك المخاطر.
تظل اختبارات العزل والتفويض والتدقيق وبوابات كل ميزة إلزامية، وتبقى المخاطر
مفتوحة حتى التحقق الفعلي. أي عيب عالٍ أو حرج في أدوات P1 الحالية يحجب القبول.
لا تُختلق مراجعة مستقلة أو موافقة مالك؛ تسجلان منفصلتين بعد حدوثهما.
