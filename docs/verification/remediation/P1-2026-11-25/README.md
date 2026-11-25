# P1 corrective action and independent re-audit handoff

Date: 2026-11-25. Remediation base main **cc04fa6e82f0b53d75fd5d08e1a36f11fba5c4d2**,
tree **66aeb9277ea7a1cf3e4e84e12d6d6782dbeb2e85**. No newer repairs existed at intake.
The [historical audit](https://github.com/ManeaAlShabrain/QASCP/blob/cc04fa6e82f0b53d75fd5d08e1a36f11fba5c4d2/docs/verification/reviews/P1/2026-11-25-4592eb230fad/01-EXECUTIVE-SUMMARY.md)
assessed 4592eb230fadebb828c8b7d3b7972c6bd1aec012: **REJECTED**, 72.95/100.
PR #43 merged reports only. All 17 reports and 17 retained evidence files were
retrieved at the immutable merged main and Git-blob verified; none is edited.

## Delivery boundaries

[Technical correction PR #44](https://github.com/ManeaAlShabrain/QASCP/pull/44)
groups CI security, bilingual/API/verification corrections and risk/architecture/
tracking records because they share the same P1 review candidate and cumulative
checks. A single corrective register/36-row recheck avoids nine drifting acceptance
branches. [Governance proposal PR #45](https://github.com/ManeaAlShabrain/QASCP/pull/45)
is separate: owner approval is explicitly required; no effective GOV-004 change.
No PR is merged automatically, no branch protection changed and no P2 begun.

| Finding | Implementer disposition | Remaining action |
|---|---|---|
| QAR-001 | Proposal and handoff prepared; PARTIALLY REMEDIATED | Owner decision on #45; effective-policy reviews and formal exit remain missing. |
| QAR-002 | Complete 12-risk register; PARTIALLY REMEDIATED | Confirm actual owners; assess/decide residual risk; no acceptance recorded. |
| QAR-003 | Complete 20-decision options/register; PARTIALLY REMEDIATED | Decide exact version/source/registry/transaction choices; independent review. |
| QAR-004 | READY FOR RE-REVIEW | Independent security assessment of direct/include/conditional/error regressions and fresh candidate checks. |
| QAR-005 | READY FOR RE-REVIEW | Independent substantive bilingual and source/regulatory disposition, actual human where current policy requires. |
| QAR-006 | READY FOR RE-REVIEW | Reproduce documented clean Linux recipe; native Windows limitations retained. |
| QAR-007 | READY FOR RE-REVIEW | Inspect active #32/19-package register; confirm actual owners; closed packages remain historical. |
| QAR-008 | READY FOR RE-REVIEW | Review lock/provenance/PyPI advisory result/scoped inventory; independent tool/license adoption pending. |
| QAR-009 | READY FOR RE-REVIEW | Inspect all response identities, full OpenAPI/policy result; architecture adoption is separate. |

## Evidence and reviewer instructions

- [Corrective action register: all requested fields](CORRECTIVE_ACTION_REGISTER.json).
- [All 36 requirement rows rechecked within P1 scope](REQUIREMENTS_RECHECK.md).
- [Bilingual comparison, correction log and glossary](../../P1_BILINGUAL_REMEDIATION.md).
- [Risk ownership and residual-risk record](../../../governance/P1_RISK_OWNERSHIP.md).
- [Architecture options, recommendations and pending decisions](../../../architecture/P1_ARCHITECTURE_DECISION_REGISTER.md).
- [Active 19-package acceptance view](../../../product/P1_ACTIVE_ACCEPTANCE_REGISTER.md).
- [Clean supported validation setup](../../P1_VALIDATION_SETUP.md).
- [Supply-chain scope and deferred measures](../../P1_SUPPLY_CHAIN_REMEDIATION.md),
  [actual 19-wheel/advisory capture](dependency-evidence.json) and
  [scoped CycloneDX inventory](validation-wheels.cdx.json).

The final exact candidate and fresh run links are bound in the PR body and
candidate-evidence.json after publication. Never put a self-referential commit
SHA in the commit that defines it. Initial checkout candidate 1d6c14375e10581241919d71372469c0d16b3fa8
passed Actions 45690090809: 106 tests/no skips, both full API/policy validators,
dependency consistency, gate and actual PyPI lookup. That bootstrap run predates
later corrections/lock installation; it is not final-candidate evidence.
The original Windows errors and independent negative probe remain in the audit;
new local command outputs are retained separately without changing their result.
The initial corrective discovery had one additional fixture failure because the
isolated foundation fixture copies required current files, not historical audit
assets newly linked by them. Those three historical references now use immutable
GitHub anchors. The initial 42-entry/one-failure/six-error output is preserved in
local-results-initial.json and unittest-local-initial.txt; a corrected rerun is
retained separately. No assertion or test was disabled.

Re-audit: fetch the immutable final SHA and diff, verify preserved audit blobs,
reproduce the guard using temporary nonsecret Git repos, examine both paired
documents substantively, inspect command/observation/projection distinctions,
run all full validators and regressions, inspect current rule plus retained #37
negative-control limits, then assess all 36 rows, 12 owner decisions and 20
architecture choices. Record actual reviewer identity/type/qualification or AI
session/independence limits, scope, SHA, date, findings and evidence.

Only a separate reviewer can mark VERIFIED FIXED. This implementation conversation
cannot supply independent re-audit results. No actual reviewer is currently
assigned; the handoff requests one and does not fabricate a completed review.
Formal P1 exit remains pending and distinct from remediation/re-audit completion.


## Complete implementation candidate: actual retained result

Candidate **5b9106b8a01fe05e77533c5e93993e682cfcc313**, tree
**d529fa2759ee0fb223035170a70ed2980dffb9f7**, passed
[Actions 45692520028](https://github.com/ManeaAlShabrain/QASCP/actions/runs/45692520028):
107/107 tests, zero skips/errors/failures, clean hash-required wheels-only install,
pip check, 19 official artifact hashes and zero returned PyPI advisory entries,
both complete OpenAPI/shared-policy validations and the required gate.
[Machine evidence](candidate-evidence.json) and [actual job log](candidate-foundation.log)
retain exact jobs/steps/environment.
The display log normalizes line endings and strips trailing whitespace; the
unaltered tool-returned content is retained in candidate-foundation-raw.json,
with its UTF-8 SHA-256 in candidate-evidence.json. New evidence formatting fixes
do not modify historical audit logs or any test outcome.

The final evidence-only candidate receives
fresh checks, bound in PR #44 and the re-audit request; this avoids claiming a
commit contains its own SHA or transferring old results to a changed tree.

Local corrected discovery: 42 entries, 36 successful and six errors, no skips;
OpenAPI command fails for missing validator. These results are preserved in
[local-results.json](local-results.json); initial fixture failure remains in
[local-results-initial.json](local-results-initial.json). Linux success does not
relabel local errors. All 34 original audit blobs remain byte-identical.

Governance proposal #45 at 7e9b11528f8250caefccd41ec6d554d0e9c81c02 passed
[its own unchanged-baseline 96-test run](https://github.com/ManeaAlShabrain/QASCP/actions/runs/45691253061).
Those checks do not assess this 107-test technical candidate or adopt the policy.
The only changes outside #44 are three proposal files in #45 and reopening the
existing #32 acceptance tracker; original package issue history is retained.
