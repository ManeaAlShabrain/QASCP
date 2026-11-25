# Verification procedures and acceptance records

## P1 check and enforcement

First follow the [supported clean environment and dependency installation recipe](P1_VALIDATION_SETUP.md).
Use Linux x86_64 / CPython 3.14 with the hash-locked wheels-only closure and pip check;
the full validators are mandatory dependencies. From the repository root:

```sh
.venv-contracts/bin/python scripts/verify_foundation.py
.venv-contracts/bin/python scripts/verify_openapi_contracts.py
.venv-contracts/bin/python -m unittest discover -s tests -v
```

The first command checks required files, local document paths, phase order, and IDs in both handbooks against the register. It checks that every requirement points to a defined verification method and vice versa. The tests verify representative failure cases. Reviewers examine substantive translation equivalence and design evidence. Store CI links against the tested revision.

During P1, review the plans and trust boundary controls without connecting to customer systems. GitHub Actions evaluates the changed branch. Verify separately that the repository protects the default branch and makes **QASCP Foundation Gate** mandatory. Inspect the rule scope, enforcement state, check source and bypasses; run an isolated PR targeting the protected branch with a deliberate documentation failure and check its merge state, then close the test PR without merging. Check that the healthy candidate passes CI. A successful or failed workflow alone provides no evidence of merge enforcement.

## Verification IDs

### P1-V01 — Handbook and source traceability

Run the foundation check and unit tests. Review translated statements side by side. Sample requirement-to-evidence references and each regulatory source entry. Verify duplicate or missing IDs, reordered phases, missing sources, and broken file pointers are detected. Record unresolved translation, provenance, legal applicability, and review items.

### P1-V02 — Architecture and boundary review

Review use cases, ADRs, trust boundaries, data and API contracts, independent design provenance, domain invariants, threat controls, and backlog. For each architecture risk, describe a testable mitigation and assign ownership before recording closure. Trace tenant context, model inputs, and audit records across the documented components.

### P1-V03 — CI and repository enforcement

Retain passing and failing Actions runs from a controlled test, capture the active branch rule and expected Actions check identity, and record whether the test PR became blocked. Keep a reviewer record for security-sensitive changes to the policy or gate.

### P1-V04 — Phase closure and blockers

Identify the effective policy baseline and readiness class first; a candidate baseline cannot silently replace the prior acceptance boundary. Verify all applicable P1 criteria, qualified review under that effective baseline, open risk disposition, and all P1 evidence linked to an immutable revision. Record acceptance with the actual approving identity and time. An unresolved required check or reviewer decision leaves the phase pending. Review the prerequisite again before starting P2.

### P2-V01 — Tenant and audit integration

Using two isolated synthetic tenants and a real deployed test database, test authorized and denied calls, malicious tenant selectors, joins, same-tenant references, connection reuse, queues, retries, clipping of logs, and audit persistence. Test every implemented tenant surface on allow and deny cases. Record service role and migrator privileges separately.

### P2-V02 — Build, dependencies, and migration

Verify dependency provenance and supported build environment, test clean install and prior supported database upgrade where applicable, and capture build output and regression results. Check that deployed packages contain no unfinished implementation or synthetic fallback paths.

### P3-V01 — Correlation and replay

Run a versioned labeled fixture set via the real authorized event path. Evaluate precision, recall, duplicate handling, out-of-order delivery, and audit linkage. Report dataset version, class balance, denominators and failure cases. Repeat relevant P2 tests.

### P4-V01 — AI policy and authorization

Verify tenant-scoped retrieval, prohibited production credentials, recommendation provenance, correct abstention, and the independent approval/execution boundary. Test absent, revoked, expired, altered, cross-tenant, and replayed approvals using synthetic identities. Repeat relevant prior checks.

### P5-V01 — Evidence lifecycle and audit

Use a synthetic case to collect an artifact, resolve ownership, record approval, reverify and age out evidence. Verify expiry and deduplication behavior, gated actions and export scope. Retain audit evidence and earlier-stage regression results.

### P6-V01 — Enterprise release readiness

Verify independent security review, performance against approved workload, recovery against approved RTO/RPO, installation, upgrade, rollback or forward recovery, incident procedures, evidence integrity, and the identified build artifact and component inventory. Review regulated deployment scope with its owner. Record open findings and actual release authorization.

## Stage decision record

Each candidate record contains policy baseline/effectiveness evidence, readiness class, phase, prior approved phase or first-phase status, immutable revision, scope, applicable requirements, evidence IDs, workflow or command results, test environment and dataset versions, artifact digest where applicable, risks and exceptions, and the decision with reviewer and timestamp. The approver records the decision in a PR or other access-controlled audit source after reviewing the cited revision, and the repository record links that decision.

## Decision and exception handling

Use Pending, Ready for review, Approved, or Blocked as recorded states. A documented approval from the assigned approver and all mandatory evidence are required for Approved. A decision requiring independent review remains blocked until that reviewer provides evidence. If an accepted control regresses, block the affected release, identify impacted phases and consumers, and record a new decision after remediation and verification.

For a permitted lower-risk deferral use a time-bound record with requirement, evidence, severity, impact, compensating control, owner, expiry, and approver. Revisit on expiry or when exposure changes. Required missing evidence and failures in tenant isolation, authorization, audit integrity, and applicable obligations cannot be waived through this process.


## Baseline 1.1 candidate and separate-process review

The owner [approved the proposal](../governance/decisions/GOV-DEC-001.md), not
P1 exit. Follow the paired [English](../governance/SOLO_ASSURANCE_PROCESS.md) /
[Arabic](../governance/SOLO_ASSURANCE_PROCESS.ar.md) process for candidate review
and activation evidence. Four separate review conversations/processes must
cover security/architecture, substantive bilingual/source preparation,
organization/requirements and final verification; this implementer cannot fill
them. Record actual reviewer type/session/independence limits, exact candidate,
policy/readiness scope, evidence and disposition. Until governed activation is
recorded the prior conservative human-review boundary remains applicable.
Enterprise/client/production and applicable regulatory decisions always retain
their actual human/competent-authority gates. A reviewer verifies findings;
the owner separately decides phase exit after all mandatory criteria.
