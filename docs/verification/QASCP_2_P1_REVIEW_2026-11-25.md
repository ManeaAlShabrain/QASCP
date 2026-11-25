# QASCP P1 review and resumption — 2026-11-25

Active phase: **P1**. Official decision: **Pending review**.
Human-review bundle: [PR #36](https://github.com/ManeaAlShabrain/QASCP/pull/36).
Work packages: V2-P1-02/04/05; P1-V01..04.
Requirements: PRD-01/02/10, QASCP-GOV-001..004, QASCP-SEC-001/003,
QASCP-ENG-001..003. This is implementer preparation, not independent acceptance.

## Revision and complete repository inventory

Repository: public organization [ManeaAlShabrain/QASCP](https://github.com/ManeaAlShabrain/QASCP).
Baseline main: **f9df7a30747aba111ee7df0afe209fd613cae869**.
Tree: **2c21d99bdeb0a1773a35c9fe53dbf4969854b5b7**.

All 67 tracked files were retrieved at that immutable revision into an isolated
workspace; every file's UTF-8 bytes matched its Git blob SHA-1. Existing edits
in the older local checkout were preserved and excluded. The isolated local
Git root is a verified snapshot, not the upstream commit. Publication instead
created a real upstream descendant, **bd310dfa4a9522f3a70555eeae5bb1c6b83a0ac3**.

| Inventory | Files | Review subject |
|---|---:|---|
| Root | 5 | README, instructions, security reporting, license and validation dependencies |
| GitHub | 2 | PR template and pinned-checkout/read-only foundation workflow |
| Documents | 29 | Both handbooks, PRD/backlog, architecture/ADRs, graph decisions/plans, bilingual BANK-01 blueprint, threats, sources/coverage/research and evidence |
| Contracts | 18 | Sixteen JSON Schemas and two preserved OpenAPI proposals |
| Scripts | 4 | Foundation, bounded OpenAPI reader and graph fixture oracles |
| Tests | 6 | Foundation, import, record, boundary, OpenAPI and approval-outcome modules |
| Synthetic fixtures | 3 | Import, query and receipt/claim examples |

Reading repository content does not revalidate external standards, regulations,
patent records or untracked historical PDF attachments. Edition, rights and
entity-applicability gaps remain in their source records. No customer system,
banking dataset or production credential was used.

## Current design and implementation boundary

The 24 domains are target coverage. [Scope decision #13](https://github.com/ManeaAlShabrain/QASCP/issues/13)
accepts BANK-01 first on its earlier revision; it is not acceptance of this newer
code or P1 exit. The graph already specifies typed resources/source identity,
entitlement versus observed use, attributable lineages, source/knowledge time,
T1..T3 transactions, authorization before expansion, bounded snapshots and
planned BA01..BA11 tests. The [authority matrix](../architecture/QASCP_2_SUPERSESSION.md)
and [canonical backlog](../product/QASCP_2_BACKLOG.md) retain precedence.

No FastAPI server, actual PostgreSQL/RLS, OIDC service, signed cursor, operational
connector, model or executor exists in the baseline. Fixture oracles must stay
outside production routes. After recorded P1 exit, start V2-P2-01 with trusted
authentication/tenant context, isolated membership resolution, PostgreSQL roles
and migrations, and real A/B allow-deny tests. Inventory, intake/audit/outbox,
graph and bilingual BANK-01 views follow their existing dependencies.
P3 correlation, P4 AI/synthetic execution and P5 assurance/history stay gated.

## CR-08 — Apply one security policy to both API proposals

The standalone full OpenAPI batch checked both documents, but the custom
security policy was only exercised for successor 0.2 in the graph fixture
module. The preserved 0.1 lacked the same mandatory policy path.

- Extract the existing policy to [verify_openapi_policy.py](../../scripts/verify_openapi_policy.py).
  It uses the standard library and retains all eight HTTP methods, global and
  inherited bearer/tenant checks, alias/override rejection and unsupported
  callback/webhook/referenced-path denial.
- Apply full specification validation and shared policy to the same decoded
  snapshot for both documents. Report policy_operations=2 and 4 respectively.
  The graph wrapper retains its successor version/schema/reference checks.
- Keep lower-level validate_document specification-only. Tests use the real
  full validator to accept six standards-valid weakened examples before the
  shared policy rejects them. This distinction must remain testable.
- Add six dependency-free policy/batch regressions. Two isolate the unavailable
  full validator with mocks; they do not claim full specification validation.
  Make the new policy, tests, review and evidence snapshot required inputs.

This is original QASCP acceptance-tool maintenance derived from its own prior
checker. No public contract bytes, dependency pins, workflow/check identity,
normative handbook or phase gate changes. No runtime authentication is claimed.
Independent review of changed acceptance controls remains required.

## Effective ruleset and controlled main test

[Main metadata](https://api.github.com/repos/ManeaAlShabrain/QASCP/branches/main)
reports protected:true. The [Protect main rule 27321554](https://github.com/ManeaAlShabrain/QASCP/rules/27321554)
is active for ~DEFAULT_BRANCH, currently main, with no exclusions or bypass
actors; connected-actor bypass is never. It requires PRs, strict up-to-date
checks and **QASCP Foundation Gate** from GitHub Actions/App **15368**.
Deletion and force push are restricted. Required approving review count is
**0**; this setting does not establish an independent review. Classic
protection's legacy disabled/off summary is not the separate ruleset.
The detailed classic protection endpoint remains unavailable to this integration;
no inaccessible setting is inferred.

The initial create-tree write returned 403 before creating anything. The owner
then enabled organization application access; publication succeeded.
The earlier [PR #2](https://github.com/ManeaAlShabrain/QASCP/pull/2) targets a different
branch and remains historical workflow evidence.

A separate, non-draft [PR #37](https://github.com/ManeaAlShabrain/QASCP/pull/37)
targeted main with exactly one broken README link at
**5c8b52d606f25d807e97029f0c80d48762af165c**.

| Control | Observed evidence |
|---|---|
| Deliberate failure | [Run 45674710740](https://github.com/ManeaAlShabrain/QASCP/actions/runs/45674710740): foundation and required gate failed; later installation/validator/unit steps skipped |
| Failure cause | README.md: unresolved local link missing-controlled-main-enforcement-probe.md |
| Merge block after gate failure | PR open, draft=false, base=main, negative head unchanged; mergeable_state=blocked, mergeable=true, merged=false |
| Other observed check | CodeQL succeeded at the negative head |
| Repair | **2ffc0a864c3d7cf9b43041dadfaffa1bf2438438** restores exact main tree **2c21d99bdeb0a1773a35c9fe53dbf4969854b5b7** |
| Positive control | [Run 45674930080](https://github.com/ManeaAlShabrain/QASCP/actions/runs/45674930080) passed foundation/full validators/tests and gate; PR net diff was zero |
| Cleanup | #37 closed without merging |

[Captured API evidence](evidence/main-enforcement-2026-11-25.json) retains rule
parameters, check IDs/producer, negative PR state and positive/closure data.
mergeable=true describes conflict feasibility, not permission to bypass the
blocked policy state. No merge endpoint or override was attempted. The last
positive merge-state sample was unstable during asynchronous processing; it is
not represented as a successful merge-capability test. The observed negative
block is not a guarantee about future settings or other privileged actors.

## Actual verification and candidate binding

| Environment / command | Result |
|---|---|
| Baseline content verification | 67/67 Git blobs matched |
| Windows / Python 3.14.4 foundation | Exit 0 |
| Windows new policy tests | 6/6 passed |
| Windows complete discovery | Exit 1: 31 entries, 25 passed, 6 errors, zero skipped |
| Windows errors | Five missing-validator module imports; existing WinError 1314 symlink privilege error |
| Windows standalone full validator | Exit 1; openapi_spec_validator unavailable |
| Original local candidate text/AST checks | All 70 files passed; final evidence update checked again before publication |
| Code candidate bd310dfa4a9522f3a70555eeae5bb1c6b83a0ac3 | [Run 45674623799](https://github.com/ManeaAlShabrain/QASCP/actions/runs/45674623799): foundation, pinned dependency consistency, both full APIs with policy counts 2/4, **96/96 tests**, zero skips, gate success |
| Final evidence-only update | Its exact SHA and fresh cumulative run are bound in PR #36; earlier code CI is not final-candidate CI |

The fresh code job [139418731480](https://github.com/ManeaAlShabrain/QASCP/actions/runs/45674623799/job/139418731480)
logs the real full validators, 96 tests and OK; the [gate](https://github.com/ManeaAlShabrain/QASCP/actions/runs/45674623799/job/139418892616)
passed. Linux image: ubuntu-26.04. CI warned that the pinned checkout action
declares Node.js 20 and is forced onto Node.js 24 by the runner. Record this
maintenance input under QASCP-ENG-003; no action pin was silently changed.

The shell clone could not connect to github.com:443 in this environment;
authorized GitHub reads provided the verified snapshot. No substitute
validator, local skipped test, production fallback or sandbox elevation was
used. Local failures remain distinct from the fresh Linux pass.

## P1 evidence and remaining acceptance

| Evidence | Available | Remaining action / reviewer |
|---|---|---|
| P1-V01 | Both handbooks/source records inspected; structural/foundation checks and source handoff | Named qualified bilingual reviewer and regulatory/rights owner for exact sources, amendments, entity/deployment and permissions |
| P1-V02 | Full inventory, architecture/graph/BA planning, CR-08 fix and real static regressions | Independent qualified security/architecture reviewer; actual T01..T12 owners; risk, compatibility and adoption dispositions |
| P1-V03 | Active rule/source/bypasses captured; #37 blocked while required gate failed; repaired positive passed and test closed; 96-test code CI | Retain final #36 SHA/run and independent acceptance-control review; reverify after relevant changes |
| P1-V04 | No phase-exit approval supplied | Authorized owner records exact candidate, complete evidence, actual reviewers, conditions and timestamp |

Report Ready for human review only after the final #36 candidate's complete
checks pass. **P1 exit remains Blocked by missing mandatory reviewer/owner
decisions.** No identity, independence, qualification, risk acceptance or phase
approval is inferred from role names, issue closure, PR merge or this report.
P1 completion must be reported to the owner before transition. P2 has not begun.

## خلاصة الاستئناف

رُوجعت ملفات المستودع الـ67 على النسخة المحددة، وحُفظت التعديلات المحلية
القائمة. استعيدت صلاحية الكتابة للمنظمة، وأُنشئ طلب المراجعة #36. وُحّد
فحص سياسة المصادقة ومحدد المؤسسة للعقدين، ونجحت 96/96 من الاختبارات في
Linux مع العقدين والبوابة؛ وتبقى أخطاء البيئة المحلية مسجلة منفصلة.

في طلب الاختبار #37 ثبتت حالة blocked عند فشل الفحص المطلوب على main،
ثم أعيد المحتوى السليم ونجح فحصه وأغلق الطلب دون دمج. حُفظت بيانات API
المقروءة، ولم تُجرّب عملية دمج أو تجاوز. يرتبط تحديث الأدلة النهائي بنسخته
وفحصه داخل #36. تبقى المراجعات المستقلة والثنائية والتنظيمية وتعيين
ملاك المخاطر وقرار الخروج الرسمي؛ لم يبدأ P2.
