# QASCP P1 review and resumption — 2026-11-25

Active phase: **P1**. Official decision: **Pending review**.
Work packages: V2-P1-02/04/05; P1-V01..04.
Requirements: PRD-01/02/10, QASCP-GOV-001..004, QASCP-SEC-001/003,
QASCP-ENG-001..003. This is implementer review and preparation; no
independent review or phase approval is recorded here.

## Reviewed baseline and inventory

Repository: [ManeaAlShabrain/QASCP](https://github.com/ManeaAlShabrain/QASCP).
GitHub reports public visibility and organization ownership.
Baseline main: **f9df7a30747aba111ee7df0afe209fd613cae869**.
Tree: **2c21d99bdeb0a1773a35c9fe53dbf4969854b5b7**.

All 67 tracked files were retrieved at that immutable revision into an isolated
workspace. Each file's UTF-8 bytes matched its Git blob SHA-1, with no mismatches.
Existing changes in the older local checkout were preserved and excluded.
The isolated local Git root commit is a snapshot, not the upstream commit or
a branch that can be pushed as an upstream descendant without reconstruction.
A patch against the verified snapshot is the portable handoff.

| Inventory group | Files | Review subject |
|---|---:|---|
| Root | 5 | README, instructions, security reporting, license, pinned validation dependencies |
| GitHub | 2 | Pull request template; read-only pinned-checkout foundation workflow |
| Documents | 29 | Both governance editions, product and backlog, architecture/ADRs, graph plans/decisions, bilingual BANK-01 blueprint, contracts, threats, source/coverage/research and evidence |
| Contracts | 18 | Sixteen JSON Schemas and two preserved OpenAPI proposals |
| Scripts | 4 | Foundation, bounded OpenAPI reader, graph record/query fixture oracles |
| Test modules | 6 | Foundation, import, record, graph boundary, OpenAPI and approval outcomes |
| Synthetic fixtures | 3 | Import commands, graph query and receipt/claim histories |

Reading these repository documents does not revalidate their external standards,
regulations, patent records or historical PDF attachments that are not tracked
here. Their recorded edition/rights/applicability gaps remain. No external
customer system, banking dataset or production credential was used.

## Existing product and delivery decisions

The 24 domains remain target coverage, not delivered modules. BANK-01 remains
the first scenario, under the [scope decision in #13](https://github.com/ManeaAlShabrain/QASCP/issues/13).
That decision is tied to its earlier reviewed revision and does not approve
the newer code or P1 exit.

The graph design already includes typed resources, source identities,
entitlement/observed-use qualifiers, attributable claim lineages, separate
source/knowledge time, transaction boundaries T1..T3, resource-filtered
traversal, bounded snapshot pages and BA01..BA11 planned acceptance.
The [authority matrix](../architecture/QASCP_2_SUPERSESSION.md) and
[canonical backlog](../product/QASCP_2_BACKLOG.md) still control implementation.

No FastAPI server, PostgreSQL schema/RLS implementation, OIDC service, signed
cursor implementation, operational connector, model or executor exists in the
reviewed revision. Fixture oracles must stay outside production paths.

After recorded P1 exit, implement V2-P2-01 first: authenticated trusted context,
isolated membership resolution, PostgreSQL roles/migrations and actual A/B
tenant tests. Inventory/source binding, durable intake/audit/outbox, graph
projection/query and bilingual BANK-01 views follow the existing dependencies.
P3 correlation, P4 AI/synthetic execution and P5 assurance/history are not moved
into P2 by this review.

## Confirmed repository rule configuration

The [main metadata](https://api.github.com/repos/ManeaAlShabrain/QASCP/branches/main)
now reports protected:true. This supersedes the older private-plan observation.
Classic protection's legacy summary still reports disabled/off; it must not be
used as the complete account of the separate repository ruleset.

The independently retrieved [Protect main ruleset 27321554](https://github.com/ManeaAlShabrain/QASCP/rules/27321554)
has the following configuration at this inspection:

| Setting | Observed value |
|---|---|
| Target and status | Branch; active |
| Included refs | ~DEFAULT_BRANCH; main is the current default |
| Excluded refs | None |
| Required PR | Enabled |
| Required approving reviews | 0; automated review approval is not required by this setting |
| Required check | QASCP Foundation Gate |
| Check integration | GitHub Actions, integration_id 15368 |
| Require updated branch | true |
| Enforce on branch creation | true; do_not_enforce_on_create=false |
| Prevent deletion / force push | Both rules present |
| Bypass actors | Empty |
| Current connected actor bypass | never |

This verifies configuration, not the result of a controlled denied merge.
The detailed classic branch-protection endpoint previously denied integration
access; no unavailable administrative setting is inferred here.

Existing baseline [Actions run 44151885270](https://github.com/ManeaAlShabrain/QASCP/actions/runs/44151885270)
and its [foundation](https://github.com/ManeaAlShabrain/QASCP/actions/runs/44151885270/job/134282136692)
and [gate](https://github.com/ManeaAlShabrain/QASCP/actions/runs/44151885270/job/134282276391)
checks report success for the baseline SHA. The earlier inspected foundation
logs reported 89 tests. These are existing baseline results, not new execution
of this local change.

[Historical negative PR #2](https://github.com/ManeaAlShabrain/QASCP/pull/2)
targets foundation/engineering-governance. Its failed workflow does not prove
that a main-targeted PR was blocked. Do not merge its deliberate broken link.

A new single-file negative test tree was attempted through the connected GitHub
integration. GitHub rejected creation with HTTP 403, Resource not accessible by
integration, before a branch or PR was created. No new negative run, blocked
merge, repaired positive control or repository mutation is claimed.

## CR-08 — Share API security acceptance across both proposals

Finding: the standalone full OpenAPI batch validates both documents, while the
custom security policy previously lived in the graph fixture module and was
exercised for successor 0.2 only. Standards-valid weakening of the preserved
0.1 authentication/tenant contract lacked the same mandatory policy path.

Remediation in this local candidate:

- Extract the existing security/operation policy into
  [verify_openapi_policy.py](../../scripts/verify_openapi_policy.py), using only
  the standard library. Keep the successor-specific version/schema/reference
  checks in its graph wrapper.
- Apply the shared policy after full specification validation to **both**
  documents in the standalone batch, using the same decoded input snapshot.
  Report policy_operations alongside reference counts.
- Retain the lower-level validate_document as specification-only validation;
  existing tests deliberately use it to distinguish standards validity from
  QASCP policy. CI still invokes the batch and complete suite.
- Add six standard-library regressions over both real documents: healthy
  operations, global/operation overrides, bearer/tenant weakening, all eight
  HTTP methods, aliased tenant overrides and the actual batch path. Two batch
  unit cases mock only the unavailable full validator; they do not claim a
  standards-validation result.
- Add a dependency-enabled regression requiring the real full validator to
  accept six weakened examples (three per version) before the shared policy
  rejects them. This regression remains unexecuted locally until dependencies
  are available.
- Make the new policy and regression module required foundation inputs, and
  update the current public-repository setup/evidence pointers.

No public contract bytes, workflow job/check identity, pinned dependency,
binding governance text or phase gate is changed. This is original QASCP
acceptance-tool maintenance derived from its existing checker; no new external
implementation is adopted. It implements no runtime authentication or tenancy.

## Local verification and publication limits

Environment: Windows, Python 3.14.4. Working candidate based on the verified
67-file snapshot. Bytecode generation disabled for test commands.

| Command/check | Actual result |
|---|---|
| Base Git blob verification | 67/67 matched before editing |
| python -B scripts/verify_foundation.py | Exit 0 |
| python -B -m unittest tests.test_openapi_policy -v | Exit 0; 6/6 passed |
| python -B -m unittest discover -s tests -v | Exit 1; 31 discovered entries: 25 passed, 6 errors, zero skipped |
| Full-suite errors | Five missing-validator module imports, plus existing WinError 1314 symlink privilege failure |
| python -B scripts/verify_openapi_contracts.py | Exit 1; openapi_spec_validator is unavailable |
| git diff --check | Exit 0 on tracked changes |
| Candidate-wide text and Python AST checks | Passed for all 70 candidate files, including new files; no trailing whitespace or missing final newline |
| GitHub publication | Blocked: create-tree HTTP 403 from organization repository |
| Fresh candidate Actions | Missing; no PR or new run created |

The public-repository shell clone also failed because this execution environment
could not connect to github.com:443. Authorized GitHub reads supplied and
verified the snapshot. No sandbox elevation, substitute validator, skipped
test or production dependency fallback was used. A missing package is a failed
check here, not a passing structural-only substitute.

## P1 review disposition

| Evidence | Supported by this review | Remaining action / actual reviewer |
|---|---|---|
| P1-V01 | Both handbooks/source records inspected; existing structural checks and present foundation pass | Named qualified bilingual reviewer; regulatory/rights owner for exact sources, amendments, applicable entity/deployment and permissions |
| P1-V02 | Full repository inventory, graph/contract/BA planning and implementer CR-08 fix | Independent qualified security/architecture reviewer, actual T01..T12 owners, risk and compatibility/adoption dispositions |
| P1-V03 | Baseline passing checks; active main ruleset, check producer, strict updates and empty bypass list verified | Restore organization integration write access; run isolated negative PR from current main, observe merge block while failed, repair and verify positive checks, close without merge; fresh complete candidate CI |
| P1-V04 | No exit approval supplied | Authorized product owner records exact candidate, complete evidence, actual reviewers, conditions and timestamp |

Baseline material can be read by human reviewers using its existing passing
evidence. **This changed candidate is Blocked pending complete verification
and publication; P1 exit remains Blocked.** No reviewer identity, qualification,
independence, acceptance or risk ownership is inferred from role names or issue
closure.

The owner requested phase-completion notification and review before transition.
P1 has not completed and P2 has not begun.

## خلاصة الاستئناف

رُوجعت ملفات المستودع الـ67 على نسخة main المحددة، وحُفظت تعديلات النسخة
المحلية القديمة. أصبح المستودع عامًا داخل المنظمة، وثبت إعداد قاعدة main
الفعّالة مع الفحص المطلوب ومصدره وعدم وجود استثناءات تجاوز. لم يثبت بعد
حجب دمج طلب فاشل يستهدف main؛ رفض اتصال GitHub إنشاء الاختبار بخطأ 403.

وُحّد فحص سياسة المصادقة ومحدد المؤسسة للعقدين 0.1 و0.2. نجحت الاختبارات
الستة الجديدة وفحص الأساس محليًا، لكن المجموعة الكاملة لم تنجح بسبب
الاعتماديات الناقصة وصلاحية الروابط الرمزية. لا ننسب إلى هذه التغييرات CI
قديمًا، ولا نعدها مراجعة مستقلة أو اعتمادًا للمرحلة.

تُستكمل صلاحية الكتابة للمنظمة ثم طلب مراجعة واحد مترابط وفحوصه، واختبار
فرض الحماية، والمراجعات المستقلة والثنائية والتنظيمية، وقرار صاحب الصلاحية.
يبقى التنفيذ التشغيلي لـP2 خلف قرار الخروج الرسمي من P1.
