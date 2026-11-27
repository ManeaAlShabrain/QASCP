# Solo Developer & AI-Assisted Assurance Governance Model — effective baseline 1.1

Status: **EFFECTIVE FOR INTERNAL DEVELOPMENT ONLY** under GOV-DEC-002's conditions
satisfied by merged #48, recorded in [GOV-DEC-003](decisions/GOV-DEC-003.md).
Existing [GOV-DEC-001](decisions/GOV-DEC-001.md) supplies proposal authority.
Policy effectiveness does not close P1 or generate phase acceptance; its
criteria and separate decision still require documentation.
QASCP-GOV-001/003/004, ENG-001/002, CMP-001, REL-001; P1-V01..04.

## Readiness classes and authority

| Class | Evidence and authority | Prohibited inference |
|---|---|---|
| Internal Development Readiness | Synthetic-only research/design/local development; named project owner; separate reviews below; exact candidate/phase scope, no unresolved mandatory blockers; authorized scoped phase-exit record after effective-policy review | No bank data, customer deployment or production connection; owner cannot accept another party's obligations |
| Enterprise Production Readiness | Actual qualified independent human security/architecture review, substantive human bilingual review where applicable, qualified regulatory/rights review and actual runtime/operational/tenant/recovery/artifact evidence at applicable gates; customer/operator authorization | Internal AI process is not independent human assurance or permission to deploy |
| Regulatory Approval | Actual competent regulatory/customer authority for the entity, use and deployment where applicable | Owner, AI, CI, grade and enterprise readiness cannot issue regulatory approval |

The owner remains the actual human authority for internal decisions. Approval of
this governance proposal does not assign every risk to the owner or accept any
residual risk. T01–T12 and AD01–AD20 need their own scoped attributable decisions.
No waiver can override isolation, default-deny authorization, auditability,
applicable obligations or AI-001's exact authorized human production decision.

## Separate review process

| Step | Separate review scope | Current actual reviewer / evidence |
|---|---|---|
| Implementation | Prepare changes, provenance, manifest, actual tests and failures; no independent verdict on own changes | This Codex implementation conversation; not a review slot |
| Security and architecture | Challenge changed trust boundaries, contracts, risk treatment, compatibility, CI and acceptance controls | /root/p1_security_arch_review; https://github.com/ManeaAlShabrain/QASCP/pull/48; 05-security-corrected-candidate.md; b5702fd09083 |
| Linguistic and source preparation | Read both full editions for actors/obligations/conditions/versions; inspect authoritative source/rights/applicability gaps without legal approval claims | /root/p1_bilingual_source_review; https://github.com/ManeaAlShabrain/QASCP/pull/48; 06-bilingual-corrected-candidate.md; b5702fd09083 |
| Organization and requirements | Cross-check all 36 requirement rows, 19 packages, dependencies, authority, actual owners and decision records | /root/p1_org_requirements_review; https://github.com/ManeaAlShabrain/QASCP/pull/48; 07-organization-corrected-candidate.md; b5702fd09083 |
| Final verification audit | Independently reproduce applicable checks and challenge preceding review conclusions on the fixed candidate | /root/p1_final_verification_review; https://github.com/ManeaAlShabrain/QASCP/pull/48; 08-final-corrected-candidate.md; b5702fd09083 |
| Owner decision | Review reports, technical blockers, risk/architecture decisions and exact candidate; separately record scoped internal phase exit | Policy proposal approved only; phase exit pending |

The four review slots MUST use separate conversations/review processes from the
implementation and from each other. A reviewer MUST assess a fixed SHA/diff and
MUST NOT repair it during that audit. Corrections return to implementation,
produce a new candidate and require affected checks and reviewer dispositions.
An old report is not relabeled as reviewing a later SHA or a different policy.
No role names, template files or numbered AI specialties count as completed reviews.

Each review MUST record: actual reviewer type and name/account or session
reference, qualification where human authority is required, independence and
shared-provider/context/tool/account limitations, input SHA/tree/manifest/diff,
policy baseline and readiness class, scope/requirements/interfaces, source
evidence, commands/environment/dataset/artifact where applicable, actual results
including failures/skips/missing evidence, findings/disposition/date and publisher.
If a shareable session URL is unavailable, record that limit and retain the actual
attributable report/reference; never invent a conversation identifier.

AI separation is functional only. Shared provider, model, account or inherited
context can cause correlated errors. This process makes no human-independence,
professional accreditation or multi-person-panel claim. Actual human and
regulatory gates remain mandatory for enterprise/customer/production acceptance.

## Activation and phase decision

1. Retain owner proposal approval and exact scoped baseline 1.1 diff.
2. Collect separate security/architecture, substantive bilingual/source,
   organization and final verification dispositions against the exact candidate.
3. Require healthy cumulative CI and effective branch rules, preserve all earlier
   failures, and resolve mandatory findings; only a separate reviewer marks
   VERIFIED FIXED. Preserve the historical #43 rejection unchanged.
4. Record activation against the reviewed baseline revision and existing owner
   approval. Missing required review evidence leaves activation pending; do not
   request or fabricate a second approval of the identical proposal.
5. Separately evaluate P1-V01..04, actual risk/architecture decisions and all
   mandatory criteria; obtain the owner's scoped phase-exit decision before P2.

Record policy activation with baseline version/SHA, this owner decision,
readiness class, reviewer evidence and date. Record phase decisions separately
with phase, prior approved phase, exact candidate, applicable requirements,
checks/results, reviewers, risk/exception decisions, authority, scope and date.
CI only checks the repository/tooling; it cannot generate either decision.

Provenance/records: preserve reports, evidence and history append-only; no
customer data/secrets in this public repository. Deployment-sensitive evidence
stays in authorized restricted storage. Revisit before client/production work
and on material ownership/obligation changes. A rollback or broader scope needs
a governed superseding decision; it never rewrites historical decisions.
