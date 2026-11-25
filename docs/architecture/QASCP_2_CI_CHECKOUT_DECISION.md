# ADR-2-CI-001 — Explicit Node.js 24 checkout adoption

Status: proposed P1 CI maintenance, 2026-11-25. V2-P1-02/04;
P1-V02/03; QASCP-GOV-002..004, QASCP-SEC-004, QASCP-ENG-002/003,
PRD-10. Author: implementation assistant. Independent security reviewer and
adoption decision: pending. [Stage record](../verification/README.md) remains
P1 / Pending review.

## Problem and inspected baseline

Main **4ea6f575aef0781491daf2137d3ba127e5ae0671** merged #36.
[Main run 45676415089](https://github.com/ManeaAlShabrain/QASCP/actions/runs/45676415089)
reports success. The preceding
[CI review](../verification/QASCP_2_P1_REVIEW_2026-11-25.md) recorded the runner
warning: pinned checkout 4.2.2 declares Node.js 20 and was forced onto Node.js 24.
A successful forced-runtime run is not an explicit reviewed action upgrade.

The baseline requires a read-only token, no persisted checkout credentials and
an always-evaluated QASCP Foundation Gate that fails unless foundation succeeds.

## Proposed decision and original provenance

Use official actions/checkout **v7.0.1**, pinned to full commit
**3d3c42e5aac5ba805825da76410c181273ba90b1**. Its tagged action manifest declares node24,
its package declares version 7.0.1 and Node >=24, and its source LICENSE
declares MIT. The release tag resolved directly to that commit. These primary
upstream records were read; no external implementation was copied into QASCP.

| Primary record | Reviewed fact |
|---|---|
| [Release](https://github.com/actions/checkout/releases/tag/v7.0.1) | Published 2026-07-20; current release API returned v7.0.1 at inspection |
| [Resolved tag](https://api.github.com/repos/actions/checkout/git/ref/tags/v7.0.1) | Direct commit 3d3c42e5aac5ba805825da76410c181273ba90b1 |
| [Action manifest](https://github.com/actions/checkout/blob/3d3c42e5aac5ba805825da76410c181273ba90b1/action.yml) | node24; existing persist-credentials input; allow-unsafe-pr-checkout defaults false |
| [Package manifest](https://github.com/actions/checkout/blob/3d3c42e5aac5ba805825da76410c181273ba90b1/package.json) | ESM, version 7.0.1, Node >=24 |
| [README](https://github.com/actions/checkout/blob/3d3c42e5aac5ba805825da76410c181273ba90b1/README.md) | Node24 runner minimum v2.327.1; v6 container-auth scenario needs v2.329.0; v7 fork/trusted-trigger restrictions |
| [License](https://github.com/actions/checkout/blob/3d3c42e5aac5ba805825da76410c181273ba90b1/LICENSE) | Upstream MIT declaration; no bundled upstream source redistributed here |

The choice follows the project's own controlled-input and least-privilege
requirements. Using the action is a development dependency, not application
runtime adoption. This source/compatibility inspection is not an independent
license opinion, exhaustive upstream/transitive audit or vulnerability-free claim.

Alternatives: retain v4 and runner coercion (leaves the recorded maintenance
gap); pin a Node24 v5/v6 release (possible, but not the current official release);
implement manual authenticated Git checkout (adds custom token handling without
a project need). Revisit if the hosted runner or reviewed upstream behavior
changes. Self-hosted/container deployment support is not added by this PR.

## Preserved boundaries and additional runtime check

- Keep pull_request and main push triggers, contents:read, and
  persist-credentials:false. No alternate token, write grant, explicit PR-head
  override or privileged pull_request_target/workflow_run trigger is added.
- Explicitly set allow-unsafe-pr-checkout:false; do not opt into the new upstream
  escape hatch. This workflow's existing pull_request trigger does not require it.
- Keep foundation/gate names, dependencies, timeouts, required-check identity,
  always() and the success-only gate command unchanged. Branch rules remain
  separately configured; this source change does not edit them.
- Immediately after checkout, record Python/Git versions and inspect only
  names of local Git authentication configuration keys. Fail before project
  scripts if a checkout HTTP extraheader, credential setting or SSH command
  remains, or if Git cannot inspect its config. Capture output internally and
  never print config values.
- This checks the exercised local Git configuration boundary. It is not a
  complete scan of runner files, environment secrets, global configuration,
  arbitrary remote URLs or every upstream behavior.
- Keep all pinned Python validation dependencies, full validators and cumulative
  tests. A required failure still prevents foundation/gate success.

New acceptance inputs are this decision record and the workflow behavior;
the foundation inventory includes the record so copied-repository tests retain
its linked evidence. This is governed CI maintenance, not a phase-gate waiver.

## Verification and review requirements

Before review readiness, inspect the exact candidate's fresh Linux run:
checkout resolves to the pinned v7.0.1 commit, the post-checkout auth check
passes without printing values, both full API/policy checks and all cumulative
tests pass, and QASCP Foundation Gate succeeds. Record actual runner/Python/Git
versions and any remaining action/runtime warnings. Older #36 checks are
baseline evidence only. The PR binds final SHA and run after publication.

Local Windows preparation retains the known missing-validator imports and
symlink privilege limitation; no local full pass is assumed. No synthetic
credentials are added to the project. No customer data or production access is
involved.

Local preparation: foundation and diff whitespace checks passed. The exact
embedded Python auth check was extracted and executed against actual temporary
Git repositories: empty auth config passed; unscoped/scoped HTTP extraheaders,
credential.helper and core.sshCommand were rejected; inability to inspect a
nonrepository directory also failed closed. These six cases used a nonsecret
marker, printed no configuration values and exercised Git rather than mocking
its output. They are local preparation, not the hosted-checkout result.

Complete Windows discovery was actually rerun: exit 1, 31 entries, 25 passed,
six errors (five missing-validator imports and WinError 1314), zero skips.
The candidate requires a fresh dependency-enabled Linux cumulative run; these
local failures are not relabeled as passes.

Independent review must assess the new action pin, upstream runtime/input and
credential changes, minimal permissions, event trust and the added CI check.
Wheel artifact hashes, transitive supply-chain review and release SBOM evidence
remain separate tracked gaps. P1-V01/V02 reviewer decisions, actual risk owners
and the authorized P1-V04 exit remain outstanding; merging this PR does not
start P2.

Rollback: revert the checkout pin/input, auth-check step, decision link and
required-file entry together. No database, API or operational migration exists.

## خلاصة القرار

يقترح هذا التغيير تثبيت checkout الرسمي على إصدار يعمل صراحةً عبر Node.js
24، مع إبقاء رمز CI للقراءة ومنع حفظ بيانات الاعتماد أو استخدام مسار PR
غير الآمن. يضاف فحص فعلي لإعدادات مصادقة Git المحلية بعد checkout دون طباعة
قيمها، مع تسجيل إصدارات البيئة. تلزم فحوص المرشح الجديد ومراجعة مستقلة؛
ولا يمثل تحديث CI اعتمادًا لـP1 أو بدءًا لـP2.


## Current P1 corrective tooling addendum — 2026-11-25

QAR-004/006/008 supersede the earlier tooling limitations for the corrected
candidate only: [checkout boundary correction](../verification/P1_CI_REMEDIATION.md),
[supported clean setup](../verification/P1_VALIDATION_SETUP.md),
[hash-lock/provenance/advisory disposition](../verification/P1_SUPPLY_CHAIN_REMEDIATION.md)
and [exact candidate evidence](../verification/remediation/P1-2026-11-25/README.md).
The inline guard's earlier six-case preparation did not cover include/includeIf;
the replacement rejects those paths and retains real-Git regressions. Nineteen
platform wheel hashes are now enforced in CI; earlier version-only statements
describe their dated baseline. Historical reports/failed results are preserved.
No contract/ADR adoption, independent review, legal applicability or P1 exit is
granted by this tooling correction. P2 remains blocked under the current policy.
