# P2 — Core security data platform entry

Active2026-11-27 after actual [P1 approval](../governance/decisions/P1-EXIT-001-APPROVAL.md)
on4ece34ef1400068333e42bc34fd1c9fd887688de/treecbc8a3f69b20d387dbbabd42febb9024f0cced6f,
merged separately in #49. P2 exit is **NOT APPROVED**.

First package: V2-P2-01/#18, PRD-01/08/10, SEC-001..005, ENG-001..003,
P2-V01/02. [ADR-P2-001](../architecture/ADR-P2-001_TENANT_FOUNDATION.md)
defines scope, provenance/alternatives, trusted tenant context, actual database
roles, new foundation interface and mandatory tests before implementation.

Current work: verify exact dependency/image candidates before installing them,
then implement FastAPI/OIDC/PostgreSQL migrations and actual two-tenant integration
tests. Discovery downloads/inspects candidate wheels and registry manifests; it
is not a successful application build or a security/licence clearance. Every
result must bind its actual candidate SHA and environment.

P1 source/risk/architecture ratification and all nineteen internal package
assignments are actual owner decisions now, not missing preparation. Operational
High/Critical exposures remain unaccepted and feature-gated. Enterprise/production
human/competent-authority and external source rights holds remain intact.

## الحزمة الأولى

تبدأ P2 بحزمة V2-P2-01 بعد اعتماد P1 الحقيقي. يُتحقق أولًا من الإصدارات
والبصمات والتراخيص، ثم تُبنى الخدمة والتحقق من الهوية والترحيلات والعزل
وتُختبر بقاعدة بيانات فعلية ومؤسستين اصطناعيتين. لا يمثل تنزيل الاعتماديات
بناءً ناجحًا للتطبيق، ولا يُدعى تنفيذ اختبار لم يحدث. قبول هذه الحزمة وخروج
P2 ليسا حاصلين بمجرد بدء المرحلة.
