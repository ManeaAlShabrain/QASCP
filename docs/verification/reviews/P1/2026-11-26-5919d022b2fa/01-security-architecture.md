# QASCP P1 — Separate AI Security and Architecture Review

**Assessment date:** 2026-11-26, Asia/Riyadh
**Actual reviewer:** `/root/p1_security_arch_review`
**Reviewer type:** AI; separate security/architecture review process
**Repository:** [ManeaAlShabrain/QASCP](https://github.com/ManeaAlShabrain/QASCP)
**Reviewed candidate:** `5919d022b2fab819e8a74484c656a6a3f7db5fcc`
**Verified tree:** `b6bda6eb698ec1c83e6b792f950190e56d750f48`

**Disposition: BLOCKED for P1 exit. Baseline 1.1 policy design is supportable within its stated internal-only limits, but activation should remain pending.** The original checkout include defect is narrowly verified fixed. A new, reproducible worktree-configuration blind spot prevents acceptance of the broader checkout authentication boundary.

## 1. Reviewer declaration and review boundary

This report represents one actual AI process, identified by the canonical task ID above. It was conducted separately from implementation, using supplied review context without the implementation conversation history. Separation is functional only: the processes share the AI service, available tools and the project owner’s connected publishing account. Correlated errors remain possible.

This reviewer has no human professional qualification, independent organizational authority, regulatory authority or authority to accept residual risk. No shareable conversation URL is available; none is invented. This report is returned to the coordinator for attributable publication. I did not publish a GitHub review, grant an approval, edit repository content, change issue states, create a branch or authorize P2.

The review addresses:

- QAR-001’s replacement-policy design and security boundaries.
- QAR-002 risk ownership and residual-risk records.
- QAR-003 architectural adoption, contract compatibility and source authority.
- QAR-004 checkout authentication verification.
- QAR-008 artifact hashing and the bounded supply-chain evidence.
- QAR-009 import response semantics.
- P1 design treatment of tenant context, T1–T3, source binding, projection receipts and snapshots.

Substantive bilingual/source clearance, all-requirement organizational reconciliation and the final verification audit remain separate review responsibilities. Their completion is not inferred from this report.

## 2. Candidate identity, policy state and historical audit

GitHub’s [commit object](https://api.github.com/repos/ManeaAlShabrain/QASCP/git/commits/5919d022b2fab819e8a74484c656a6a3f7db5fcc) identifies the candidate tree as `b6bda6eb698ec1c83e6b792f950190e56d750f48`. The isolated checkout’s `git rev-parse 'HEAD^{tree}'` returned that same tree. Local commit history differs from GitHub; it was not used to claim GitHub ancestry.

The [comparison with the original audited revision](https://github.com/ManeaAlShabrain/QASCP/compare/4592eb230fadebb828c8b7d3b7972c6bd1aec012...5919d022b2fab819e8a74484c656a6a3f7db5fcc) was inspected, including the checkout guard, workflow, hash lock, governance additions, risk/decision registers and API prose changes.

The [stage record](https://github.com/ManeaAlShabrain/QASCP/blob/5919d022b2fab819e8a74484c656a6a3f7db5fcc/docs/verification/README.md) still records:

| Item | Actual state |
|---|---|
| Active phase | P1 — Product and architecture foundation |
| Phase decision | Pending review |
| GCR-P1-001 | Owner-approved proposal |
| Governance baseline 1.1 | Candidate; activation pending review |
| Risk and architecture decisions | Outstanding |
| P1-V04 | Outstanding |
| P2 authorization | Not granted |

The original audit reviewed `4592eb230fadebb828c8b7d3b7972c6bd1aec012` and issued **REJECTED / 72.95**. Its [findings register](https://github.com/ManeaAlShabrain/QASCP/blob/5919d022b2fab819e8a74484c656a6a3f7db5fcc/docs/verification/reviews/P1/2026-11-25-4592eb230fad/12-FINDINGS-REGISTER.md), security/architecture reports, checkout probe and phase decision were read as historical evidence. This review does not revise their conclusions or relabel them as assessments of the current candidate.

## 3. Evidence and executed verification

Local commands ran in:

`C:\Users\manem\Desktop\QASCP\public-review-20261125`

Environment: Windows 11, Python **3.14.4**, Git **2.54.0.windows.1**. Bytecode generation was disabled for test execution.

| Command or inspection | Actual result |
|---|---|
| `git rev-parse 'HEAD^{tree}'` | Matched the candidate tree |
| `python -B scripts/verify_foundation.py` | Passed |
| `python -B scripts/verify_validation_lock.py` | Passed; all 19 pins matched retained artifact hashes |
| `python -B -m unittest discover -s tests -p test_checkout_auth.py -v` | Exit 0; 10 test methods passed; zero skips |
| `python -B scripts/verify_openapi_contracts.py` | Failed: missing `openapi_spec_validator` |
| `python -B -m unittest discover -s tests -v` | Exit 1; 42 discovered entries, 36 passed, six errors; zero skips |
| Independent worktree-scope probe against the actual guard | Three prohibited-key cases incorrectly returned exit 0 |
| `git diff --exit-code` after review | Exit 0; tracked content unchanged |

The full local discovery errors were four missing-`jsonschema` module imports, one missing-`openapi_spec_validator` module import and the existing Windows symbolic-link privilege error, **WinError 1314**. These are recorded as failures, not passes or skipped checks. The 42 local discovery entries are not equivalent to successful execution of the 107-test dependency-enabled suite.

### Exact-candidate hosted evidence

I retrieved the run metadata, job summaries and decoded logs rather than relying on a badge.

The [foundation job](https://github.com/ManeaAlShabrain/QASCP/actions/runs/45698686089/job/139502739842) explicitly checked out `5919d022b2fab819e8a74484c656a6a3f7db5fcc`. Its logs showed:

- Ubuntu runner image version `20261116.202.1`, Python 3.14.4 and Git 2.56.1.
- Checkout authentication guard success.
- Matching 19-package wheel lock.
- Installation and download using `--require-hashes`, `--only-binary=:all:` and `--no-deps`.
- Successful `pip check`.
- Actual per-release PyPI advisory evidence.
- Both full OpenAPI documents validated with the shared policy: two operations in the preserved document and four in the successor.
- **107 tests, OK; zero skips.**

The [gate job](https://github.com/ManeaAlShabrain/QASCP/actions/runs/45698686089/job/139502909409) succeeded with `FOUNDATION_RESULT=success`.

The [CodeQL job](https://github.com/ManeaAlShabrain/QASCP/actions/runs/45698686380/job/139502750949) also checked out the exact candidate and completed successfully. Its logs identify the analysis kind as **code-quality**. This is useful corroboration, not evidence of exhaustive security analysis or absence of vulnerabilities.

### Repository enforcement

A fresh read of [ruleset 27321554](https://github.com/ManeaAlShabrain/QASCP/rules/27321554) showed active default-branch enforcement, required pull requests, strict `QASCP Foundation Gate` checking from GitHub Actions App **15368**, no bypass actors and `current_user_can_bypass=never`.

Required approving review count remains **0**. Consequently, the ruleset enforces PR/check mechanics; it does not itself enforce completion of the separate assurance reports or an authorized phase decision.

Historical negative/positive enforcement evidence and closed PR #37 were inspected. I did not create a new enforcement-test PR or attempt a merge. Historical blocked-state evidence is not represented as a fresh merge rejection.

## 4. Finding-by-finding dispositions

| Finding | This reviewer’s disposition | Remaining boundary |
|---|---|---|
| **QAR-001** | **OPEN for acceptance.** Baseline 1.1’s policy design preserves essential security boundaries and accurately limits AI assurance. | Activation, remaining separate reviews, risk/architecture decisions and exact-candidate owner phase exit remain pending. |
| **QAR-002** | **OPEN / BLOCKER.** The new register improves completeness and honesty but does not assign accountability. | All 12 actual owners and risk-acceptance references remain null; residual risk is unassessed. |
| **QAR-003** | **OPEN / BLOCKER.** The 20-row decision register supplies meaningful options and recommendations. | AD01–AD20 remain proposed; incompatible API/source-authority choices have not been adopted. |
| **QAR-004** | **VERIFIED FIXED narrowly:** the original direct/include/matching-conditional-include defect and tested error/output handling. | Broader checkout authentication acceptance remains blocked by **SEC-NEW-001** below. |
| **QAR-008** | **VERIFIED FIXED narrowly:** absence of an enforced platform-specific artifact hash lock. | Qualified adoption/license decisions, exhaustive vulnerability assessment and future release-artifact obligations are not completed by this correction. |
| **QAR-009** | **VERIFIED FIXED** for the four incorrect import response descriptions and associated T2 prose. | This does not adopt the successor API or resolve QAR-003. |
| **QAR-005/006/007** | No closure determination in this report. | Separate reviewers retain their applicable scopes. |

These dispositions are this reviewer’s assessment of the fixed candidate. They do not mutate the historical register or imply that the implementing assistant independently verified its own changes.

## 5. New finding — SEC-NEW-001

**Title:** Checkout authentication guard ignores active worktree authentication configuration
**Severity:** **MEDIUM**
**Affected scope:** P1 tooling and P1-V03 acceptance-control assurance
**Status:** **OPEN / BLOCKER for acceptance of the affected control**
**Tracking:** Coordinator identifier not yet assigned
**Requirements:** QASCP-GOV-003, SEC-004, ENG-002/003; P1-V03
**Source:** [verify_checkout_auth.py, line 21](https://github.com/ManeaAlShabrain/QASCP/blob/5919d022b2fab819e8a74484c656a6a3f7db5fcc/scripts/verify_checkout_auth.py#L21)

### Observed defect

Both inspections use `git config --local`. Enabling `extensions.worktreeConfig` allows active authentication settings to reside in the repository’s `config.worktree`. The current guard does not examine that scope or reject the enabling extension.

Official Git documentation distinguishes `--local`, which reads `.git/config`, from `--worktree`, which reads `config.worktree` when the extension is enabled. Worktree settings participate in effective configuration and can override other settings. [Git configuration documentation](https://git-scm.com/docs/git-config).

The reproduction used ordinary fresh temporary repositories. No linked worktree, remote, real credential or helper execution was required.

| Effective setting in worktree scope | Expected guard result | Actual result |
|---|---:|---:|
| `credential.helper` | Reject | Exit 0 |
| `http.extraheader` | Reject | Exit 0 |
| `core.sshCommand` | Reject | Exit 0 |

For all three cases, `git config --show-scope --name-only --list` confirmed the prohibited key in **worktree** scope. The guard printed its clean result. The nonsecret marker was absent from its stdout/stderr.

### Reproduction

Run this from the reviewed repository root. It changes only disposable temporary repositories and prints key names/results, never configuration values.

```python
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

script = Path("scripts/verify_checkout_auth.py").resolve()
env = {k: v for k, v in os.environ.items()
       if not k.startswith("GIT_")}
env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
marker = "QASCP-NONSECRET-WORKTREE-PROBE"

for key in ("credential.helper", "http.extraheader", "core.sshCommand"):
    with tempfile.TemporaryDirectory() as temporary:
        repo = Path(temporary)

        def git(*args):
            return subprocess.run(
                ["git", *args], cwd=repo, env=env,
                capture_output=True, check=True
            )

        git("init", "--quiet")
        git("config", "--local", "extensions.worktreeConfig", "true")
        git("config", "--worktree", key, marker)

        effective = git(
            "config", "--show-scope", "--name-only", "--list"
        )
        result = subprocess.run(
            [sys.executable, "-B", str(script)],
            cwd=repo, env=env, capture_output=True
        )
        print(json.dumps({
            "case": key,
            "effective_scope_line": [
                line.decode()
                for line in effective.stdout.splitlines()
                if key.lower().encode() in line.lower()
            ],
            "guard_exit": result.returncode,
            "marker_exposed":
                marker.encode() in result.stdout + result.stderr,
        }))
```

Actual output:

```json
{"case":"credential.helper","effective_scope_line":["worktree\tcredential.helper"],"guard_exit":0,"marker_exposed":false}
{"case":"http.extraheader","effective_scope_line":["worktree\thttp.extraheader"],"guard_exit":0,"marker_exposed":false}
{"case":"core.sshCommand","effective_scope_line":["worktree\tcore.sshcommand"],"guard_exit":0,"marker_exposed":false}
```

### Impact and limits

This is a false-clean result for a repository-resident authentication configuration path. It undermines the broader repository-local checkout authentication assertion.

It does **not** establish that the inspected hosted run retained credentials, that a token leaked or that a runner was compromised. A party able to alter arbitrary runner files already has capabilities beyond this checker. The finding concerns the correctness of a claimed acceptance check, consistent with the scope of original QAR-004.

### Required correction and verification

Either conservatively reject the repository’s worktree-configuration extension, or inspect applicable worktree configuration and include paths with the same fail-closed and no-values-output rules. Add real-Git regressions for all three prohibited key families and any supported worktree include handling.

A correction requires a new candidate, fresh applicable checks and a separate reviewer disposition. No correction was made during this audit.

## 6. Original checkout correction: what was actually verified

The [retained checkout tests](https://github.com/ManeaAlShabrain/QASCP/blob/5919d022b2fab819e8a74484c656a6a3f7db5fcc/tests/test_checkout_auth.py) invoke the actual CLI against temporary Git repositories. The independently executed suite confirmed:

| Case | Result |
|---|---|
| Clean repository | Pass |
| Direct helper, scoped helper, unscoped/scoped HTTP header and SSH command | Reject |
| `include.path` supplying helper/header/SSH command | Reject |
| Matching `gitdir` and case-insensitive `gitdir/i` includes | Reject; tests first confirmed effective prohibited-key presence |
| Inactive conditional include and missing include target | Reject |
| Malformed local configuration | Reject without exposing captured Git stderr |
| Nonrepository inspection | Reject |
| Invalid output, second-inspection error, unavailable Git and timeout | Reject in injected-failure tests |
| Nonsecret marker in guard stdout/stderr | Absent in asserted cases |

The distinction between actual-Git cases and injected subprocess failures matters: unavailable-Git/timeout/output-corruption tests exercise exception handling through mocks; they are not described as independently occurring runner failures.

The original include defect is corrected. Passing these tests did not cover the newly demonstrated worktree scope.

## 7. Architecture and contract assessment

The design provides a coherent PostgreSQL-first modular architecture and appropriately distinguishes static contracts from implemented security controls. Its principal unresolved problem is adoption and accountability, rather than a need for additional architectural machinery.

| Boundary | Assessment and required disposition |
|---|---|
| **Tenant context** | Caller selectors remain untrusted until validated against server-side membership or registered workload identity. Worker replay requires fresh authority. This is a suitable design invariant; schema presence cannot establish authentication. |
| **Database isolation** | Composite tenant references, nonowner/non-BYPASSRLS runtime roles, `USING`/`WITH CHECK`, transaction-local context and pool reset are explicitly required. Real role, connection-reuse and A/B denial evidence belongs to P2. |
| **Registry integrity** | Immutable resource kind, composite references and deferred exactly-one authoritative-domain-row checks address polymorphic-reference hazards. Migration/runtime privilege design still needs adoption under AD12/13. |
| **Source identity** | Binding is scoped by tenant, connector, kind, source ID and generation. Ordinary import cannot rebind it; collisions require quarantine or separate attributed resolution. No display-name merge is authorized. |
| **Source authority** | AD06/07 propose retaining conflicting claims and leaving canonical conclusions unresolved until approved field-specific authority exists. This is safer than timestamp or connector-order precedence, but remains unadopted. |
| **T1** | Intake owns observation/event persistence, digest, audit and outbox. Unresolved source references must not manufacture assets or identities. |
| **T2** | Domain effects, source binding/claim changes, command receipt, audit and outbox form one transaction. Shared idempotency across both import families prevents duplicate effects through family switching. |
| **T3** | Projection effects, processed receipt, checkpoint and audit commit together; acknowledgment follows commit. Replays must not bypass current authority. |
| **Receipt identity** | Receipt 2.0 correctly includes event identity and logical consumer/version, independent of worker replica. Preserved receipt 1.0 is explicitly insufficient for this purpose. Adoption and uniqueness implementation remain pending. |
| **Snapshots and cursors** | Tenant/principal/current-authority/query/generation binding, immutable selection, expiry, revocation and reauthorization per page are appropriate. Authorization precedes traversal, counts and pagination. The unsigned fixture cursor is correctly excluded from application use. |
| **AI execution** | Recommendations remain untrusted; AI has no production write credentials. Exact human approval, revalidation, atomic consumption, downstream idempotency and reconciliation remain required at their applicable gates. |

Evidence: [architecture](https://github.com/ManeaAlShabrain/QASCP/blob/5919d022b2fab819e8a74484c656a6a3f7db5fcc/docs/architecture/QASCP_2_ARCHITECTURE.md), [BANK-01 blueprint](https://github.com/ManeaAlShabrain/QASCP/blob/5919d022b2fab819e8a74484c656a6a3f7db5fcc/docs/architecture/QASCP_2_BANK01_BLUEPRINT.md), [graph boundary](https://github.com/ManeaAlShabrain/QASCP/blob/5919d022b2fab819e8a74484c656a6a3f7db5fcc/docs/architecture/QASCP_2_GRAPH_BOUNDARY.md), [decision register](https://github.com/ManeaAlShabrain/QASCP/blob/5919d022b2fab819e8a74484c656a6a3f7db5fcc/docs/architecture/P1_ARCHITECTURE_DECISION_REGISTER.md).

### Compatibility remains unresolved — QAR-003

Both OpenAPI documents still declare `/api/v1`, while their versions and response shapes differ. The original strict response schemas do not permit arbitrary successor fields to be inserted in place.

AD01/02 recommend a separate successor path and successor-only first implementation, preserving the original as historical and requiring an adapter before supporting an original client. That is a reasonable recommendation, not an adopted decision. Exact API path/version, schema/receipt set and supported-client policy must be selected and reconciled before implementation.

The [supersession matrix](https://github.com/ManeaAlShabrain/QASCP/blob/5919d022b2fab819e8a74484c656a6a3f7db5fcc/docs/architecture/QASCP_2_SUPERSESSION.md) resolves document precedence; it cannot substitute for owner adoption.

### Import prose correction — QAR-009

Both import operations now correctly describe:

- 201 as durable import-command acceptance with projection state reported separately.
- 200 as identical command replay returning the previous command receipt.
- T2 as committing the authorized domain mutation, command receipt, audit and outbox.

Their response schema remains `CommandReceipt`; the observation endpoint retains observation-specific wording. The inspected diff changes prose rather than response structure. This narrow correction is verified fixed.

## 8. Risk ownership and source authority

The [risk JSON](https://github.com/ManeaAlShabrain/QASCP/blob/5919d022b2fab819e8a74484c656a6a3f7db5fcc/docs/governance/P1_RISK_OWNERSHIP.json) contains 12 risk records. All **12 accountable owners are null** and all **12 risk-acceptance references are null**. Residual ratings remain unassessed. Proposed owner attribution is not confirmed delegation or acceptance.

The register properly avoids crediting unimplemented operational mitigations as reduced residual risk. That improves evidence quality but leaves QAR-002 open.

The [source register](https://github.com/ManeaAlShabrain/QASCP/blob/5919d022b2fab819e8a74484c656a6a3f7db5fcc/docs/governance/REGULATORY_SOURCES.md) and source-review handoff distinguish identity/discovery, rights, currency and entity applicability. This report does not independently establish current regulatory provisions, legal applicability, commercial reproduction permission or certification.

Technical source-field precedence and legal/regulatory source applicability are different decisions. Neither may be inferred from the existence of an imported claim or a reference link.

## 9. Supply-chain correction — QAR-008

The [lock](https://github.com/ManeaAlShabrain/QASCP/blob/5919d022b2fab819e8a74484c656a6a3f7db5fcc/requirements-contracts-linux-cp314.lock), consistency verifier and actual hosted installation establish an enforced **19-wheel Linux x86_64/CPython 3.14 hash lock**. This corrects the original absence-of-artifact-hashes finding within that platform scope.

The [supply-chain disposition](https://github.com/ManeaAlShabrain/QASCP/blob/5919d022b2fab819e8a74484c656a6a3f7db5fcc/docs/verification/P1_SUPPLY_CHAIN_REMEDIATION.md) accurately limits its claims:

- PyPI release-JSON advisory lookup is an actual but bounded check.
- Empty returned advisory lists do not establish exhaustive vulnerability clearance.
- `pip check` checks dependency consistency.
- Publisher metadata and downloaded bytes share a publisher trust relationship; the comparison is not an independent signature.
- The CycloneDX inventory covers validation wheels, excluding the OS, bootstrap pip, Actions and future application artifacts.
- `ubuntu-latest`, the base interpreter and bootstrap tools remain external mutable inputs.

The pinned checkout manifest was independently read at commit `3d3c42e5aac5ba805825da76410c181273ba90b1`; it declares Node 24 and the unsafe-PR-checkout input. The workflow retains read-only contents permission, `persist-credentials:false`, `allow-unsafe-pr-checkout:false` and success-only gate propagation. No exhaustive upstream dependency audit is claimed.

## 10. Governance design and separate recommendations

The paired handbooks, paired assurance-process documents, ADR-GOV-001, GCR-P1-001 and [GOV-DEC-001](https://github.com/ManeaAlShabrain/QASCP/blob/5919d022b2fab819e8a74484c656a6a3f7db5fcc/docs/governance/decisions/GOV-DEC-001.md) were read.

The proposed model is defensible for **Internal Development Readiness only** because it:

- Requires four separate review processes on a fixed candidate and prohibits repair during audit.
- Discloses shared-service and account limitations.
- Preserves synthetic-only, no-customer-data and no-production-connection restrictions.
- Retains qualified human and competent-authority gates for enterprise/customer/production and regulatory acceptance.
- Separates policy activation from risk acceptance, architecture adoption and phase exit.
- Preserves nonwaivable tenant isolation, default-deny authorization, auditability and exact human production authorization.

The owner’s **«موافق»** is recorded as a contextual proposal approval associated with PR #45 head `19610e8f690d69b5b408e5b61d909ebea6aec6a8`. The record correctly explains that the message did not literally restate the SHA/scope and is an assistant transcription, not a digital signature or independently authenticated legal identity. This review does not expand its authority.

| Decision | Recommendation |
|---|---|
| **Baseline 1.1 security/architecture policy design** | Favorable within the documented internal-only scope; no separate policy-design defect established here. |
| **Baseline 1.1 activation now** | **HOLD / PENDING.** Complete the other required dispositions and final challenge; resolve the new mandatory acceptance-control finding and re-review the resulting candidate. This report does not activate policy. |
| **P1 exit on this candidate** | **BLOCKED.** SEC-NEW-001, QAR-002/003, remaining required review evidence and P1-V04 remain unresolved. |
| **P2 authorization** | **Not granted.** Requires effective-policy evidence and a separate authorized exact-candidate phase decision. |
| **Enterprise/customer/production readiness** | Not established; the required actual human, runtime and external-authority gates remain. |

Real PostgreSQL isolation, runtime authentication, concurrency/crash recovery, signed cursors, load, deployment and production recovery were not required to be implemented during this design-only P1 review. Their later gates remain binding. P1’s present blockers are the demonstrated tooling defect and outstanding review/ownership/adoption/approval decisions, not the absence of future application runtime.
