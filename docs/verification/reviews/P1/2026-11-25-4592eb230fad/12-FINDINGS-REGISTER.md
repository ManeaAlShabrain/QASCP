# Findings register

Reviewed repository: ManeaAlShabrain/QASCP · branch: main · commit: `4592eb230fadebb828c8b7d3b7972c6bd1aec012` · date: 2026-11-25, Asia/Riyadh.

AI-assisted review only; virtual specialties do not represent actual independent people.

All findings are **OPEN** at issuance. Existing closed GitHub package states do not close these findings. No ACCEPTED RISK status is used. P0..P4 below are severity priorities; P1..P6 in Affected Phase are project phases.

| ID | Severity | Category | Blocker | Tracking |
|---|---|---|---|---|
| QAR-001 | HIGH — P1 | Governance and acceptance | Yes | [Issue](https://github.com/ManeaAlShabrain/QASCP/issues/17) |
| QAR-002 | HIGH — P1 | Risk ownership | Yes | [Issue](https://github.com/ManeaAlShabrain/QASCP/issues/14) |
| QAR-003 | HIGH — P1 | Architecture and compatibility | Yes | [Issue](https://github.com/ManeaAlShabrain/QASCP/issues/14) |
| QAR-004 | MEDIUM — P2 | CI security verification | Yes | [Issue](https://github.com/ManeaAlShabrain/QASCP/issues/40) |
| QAR-005 | MEDIUM — P2 | Normative translation | Yes | [Issue](https://github.com/ManeaAlShabrain/QASCP/issues/41) |
| QAR-006 | LOW — P3 | Developer documentation | No additional | [Issue](https://github.com/ManeaAlShabrain/QASCP/issues/42) |
| QAR-007 | LOW — P3 | Project tracking | No additional | [Issue](https://github.com/ManeaAlShabrain/QASCP/issues/32) |
| QAR-008 | INFORMATIONAL — P4 | Supply-chain improvement | No additional | Not Available / informational review record |
| QAR-009 | LOW — P3 | API documentation consistency | No additional | [Issue](https://github.com/ManeaAlShabrain/QASCP/issues/42) |

## QAR-001 — Mandatory human review and phase-exit approval are not recorded

- **Finding ID:** QAR-001
- **Finding Title:** Mandatory human review and phase-exit approval are not recorded
- **Reviewer ID:** REV-01 / REV-06 / REV-09
- **Category:** Governance and acceptance
- **Severity:** HIGH — P1
- **Affected Phase:** P1
- **Requirement Reference:** QASCP-GOV-001/003/004, QASCP-CMP-001, QASCP-REL-001; P1-V01..04; V2-P1-02..05
- **Affected File:** [docs/governance/ENGINEERING_GOVERNANCE.ar.md:27](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/docs/governance/ENGINEERING_GOVERNANCE.ar.md#L27)
- **Line Number:** 27; additional references below
- **Description:** No actual qualified independent security/architecture, substantive bilingual or regulatory-owner acceptance is recorded at the reviewed revision; no authorized P1 exit exists. GOV-004 explicitly requires actual people. The inspected PR review collections and P1 issue comments contain no such decision.
- **Expected Behavior:** Attributable qualified independent review, source/rights disposition and authorized owner exit decision tied to the immutable candidate and all mandatory evidence.
- **Actual Behavior:** Stage remains Pending review; declaration would have Human Reviewer: Not Assigned. An AI panel operating via the owner's account cannot satisfy the actual-people requirement.
- **Evidence:** E01, E02, E06, E07; docs/verification/README.md:25; delivery packet:181–185; reviews for PRs #12, #33–36, #38–39 empty; comments for #13–17/#32 empty.
- **Root Cause:** Required approval records have not been supplied in the inspected acceptance sources; no individual motive is inferred.
- **Impact:** P1 cannot close and P2 is not authorized. This is an unmet mandatory acceptance input, not evidence of an exploitable production service.
- **Recommended Remediation:** Have the authorized owner assign actual reviewers, retain qualification/independence and scoped dispositions, resolve findings, then record the exact-SHA exit decision and link it from a governed stage-record PR. Do not relabel this AI review as human acceptance.
- **Acceptance Criteria for Fix:** Actual identities, scopes, findings/dispositions, candidate SHA, dates and evidence are available; all mandatory blockers resolved; owner phase decision is recorded. An AI report or merged PR alone does not meet this criterion.
- **Verification Method:** Read the new access-controlled review/decision records and verify their revision and scope against fresh checks; no closure based only on implementer assertion.
- **Blocking Status:** Yes — formal P1 exit
- **Current Status:** OPEN
- **Tracking:** [GitHub Issue](https://github.com/ManeaAlShabrain/QASCP/issues/17)

## QAR-002 — T01–T12 lack actual accountable owners and reviewed residual-risk dispositions

- **Finding ID:** QAR-002
- **Finding Title:** T01–T12 lack actual accountable owners and reviewed residual-risk dispositions
- **Reviewer ID:** REV-03 / REV-06
- **Category:** Risk ownership
- **Severity:** HIGH — P1
- **Affected Phase:** P1
- **Requirement Reference:** P1-V02, P1-V04; QASCP-GOV-004, QASCP-REL-001
- **Affected File:** [docs/architecture/QASCP_2_THREATS.md:20](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/docs/architecture/QASCP_2_THREATS.md#L20)
- **Line Number:** 20; additional references below
- **Description:** The threat register explicitly identifies role names rather than assigned people and requires actual ownership and likelihood/impact/residual-risk review before P1 closure.
- **Expected Behavior:** Every T01–T12 entry has an actual accountable owner, scoped mitigation/evidence, reviewed likelihood/impact and residual-risk disposition.
- **Actual Behavior:** All twelve entries remain role-only proposals; no residual risk acceptance is recorded.
- **Evidence:** E02, E07; threat register:3,7–18,20; BANK-01 blueprint B06; delivery packet:183.
- **Root Cause:** Risk-accountability and disposition step remains uncompleted.
- **Impact:** No person is accountable for tenant isolation, AI/executor, audit, availability or source-claim risks when implementation begins.
- **Recommended Remediation:** Populate a governed owner/disposition record for all twelve threats, link planned BA/phase evidence, and escalate unresolved risks to the authorized risk authority. Keep acceptance distinct from simple owner assignment.
- **Acceptance Criteria for Fix:** 12/12 threats have actual owners and dated review/disposition; any accepted risk has documented authorized acceptance, scope, compensating controls and expiry where required.
- **Verification Method:** Cross-check threat IDs, named owner confirmation, decisions and linked evidence; re-review affected design changes.
- **Blocking Status:** Yes — explicitly required before P1 closure
- **Current Status:** OPEN
- **Tracking:** [GitHub Issue](https://github.com/ManeaAlShabrain/QASCP/issues/14)

## QAR-003 — P1 architectural adoption and source-authority decisions remain unresolved

- **Finding ID:** QAR-003
- **Finding Title:** P1 architectural adoption and source-authority decisions remain unresolved
- **Reviewer ID:** REV-02
- **Category:** Architecture and compatibility
- **Severity:** HIGH — P1
- **Affected Phase:** P1
- **Requirement Reference:** V2-P1-02; P1-V02; PRD-01/02/10; QASCP-GOV-002/004
- **Affected File:** [docs/architecture/QASCP_2_BANK01_BLUEPRINT.md:93](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/docs/architecture/QASCP_2_BANK01_BLUEPRINT.md#L93)
- **Line Number:** 93; additional references below
- **Description:** Concrete proposals exist, but B06/G-01..G-07 have no recorded adoption disposition. Both API proposals use /api/v1; the successor changes responses and original receipt 1.0 is insufficient for graph deduplication. Source-field precedence/collision rules are deferred to a separately reviewed policy.
- **Expected Behavior:** An exact-version P2 target and compatibility strategy are selected; required source-authority, registry/role and transaction/snapshot decisions are explicitly adopted, rejected or bounded with safe default-deny behavior.
- **Actual Behavior:** API-version negotiation/client compatibility and B06 source/constraint dispositions are pending. Source precedence is referenced but not defined as an accepted policy.
- **Evidence:** E02; BANK-01 blueprint:31,53,93–94; graph boundary:18; graph decisions:5,11–17; graph record contracts receipt compatibility sections.
- **Root Cause:** Design preparation has reached proposals but not authorized decision closure.
- **Impact:** Implementers could choose incompatible receipts/API shapes or invent canonical source precedence. No runtime data loss is asserted.
- **Recommended Remediation:** Record a coherent P1 decision table selecting exact API/receipt/schema versions, original-contract disposition, source conflict/reassignment behavior, registry constraint strategy and T1–T3 ownership. For future-only history/performance inputs, record their later gate rather than demand their implementation now.
- **Acceptance Criteria for Fix:** No conflicting P2 authority remains; incompatible additions cannot be injected into original additionalProperties:false responses; ordinary import cannot rebind sources or apply last-writer precedence; later-phase items remain gated.
- **Verification Method:** Independent trace from decision to schema, prose and canonical backlog; check denial/conflict examples and rerun affected static checks on the resulting candidate.
- **Blocking Status:** Yes — unresolved P1 adoption; future P5 implementation itself is not a blocker
- **Current Status:** OPEN
- **Tracking:** [GitHub Issue](https://github.com/ManeaAlShabrain/QASCP/issues/14)

## QAR-004 — CI checkout-auth guard misses active credentials configuration in local includes

- **Finding ID:** QAR-004
- **Finding Title:** CI checkout-auth guard misses active credentials configuration in local includes
- **Reviewer ID:** REV-03 / REV-05
- **Category:** CI security verification
- **Severity:** MEDIUM — P2
- **Affected Phase:** P1 tooling
- **Requirement Reference:** QASCP-GOV-003, QASCP-SEC-004, QASCP-ENG-002/003; P1-V03; ADR-2-CI-001
- **Affected File:** [.github/workflows/ci.yml:30](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/.github/workflows/ci.yml#L30)
- **Line Number:** 30; additional references below
- **Description:** The guard queries git config --local without --includes. Local include.path and a matching includeIf can supply credential.helper while the exact guard exits 0 and prints its clean message.
- **Expected Behavior:** The claimed local checkout authentication check fails closed when prohibited effective local authentication configuration remains, including configuration imported from local includes.
- **Actual Behavior:** Independent disposable-repository probe: clean=0, direct credential.helper=1, include.path credential.helper=0, matching includeIf credential.helper=0. The last two have effective included prohibited key names.
- **Evidence:** E04; evidence/checkout-probe.json and checkout_probe.py; exact workflow:30–37; local Git 2.54.0.windows.1. Official Git config documentation describes scoped include defaults: https://git-scm.com/docs/git-config#Documentation/git-config.txt---includes.
- **Root Cause:** The scoped Git config query does not traverse include directives by default; original six-case preparation did not cover includes.
- **Impact:** False assurance from a security-sensitive acceptance check. The inspected hosted run removed its temporary include directives, so this finding does not demonstrate retained secrets, credential theft or a compromised checkout.
- **Recommended Remediation:** Either explicitly reject remaining local include/includeIf authentication paths or inspect the effective included local configuration with fail-closed handling; preserve the no-values logging boundary. Add retained direct/include/matching-includeIf negative regressions using nonsecret markers.
- **Acceptance Criteria for Fix:** Clean config passes; direct and included helper/HTTP auth header/SSH-command cases fail; inspection errors fail; logs expose no configuration values. Fresh candidate checks and independent disposition are retained.
- **Verification Method:** Rerun the exact extracted guard against disposable Git repositories, then fresh hosted CI on the fixed candidate. Repeat earlier P1 regression paths.
- **Blocking Status:** Yes — affected P1-V03 acceptance-control verification until corrected/reviewed; medium severity is not a production exploit rating
- **Current Status:** OPEN
- **Tracking:** [GitHub Issue](https://github.com/ManeaAlShabrain/QASCP/issues/40)

## QAR-005 — Bilingual governance and snapshot wording have substantive mismatches

- **Finding ID:** QAR-005
- **Finding Title:** Bilingual governance and snapshot wording have substantive mismatches
- **Reviewer ID:** REV-07 / REV-08
- **Category:** Normative translation
- **Severity:** MEDIUM — P2
- **Affected Phase:** P1
- **Requirement Reference:** QASCP-GOV-003; P1-V01; V2-P1-03
- **Affected File:** [docs/governance/ENGINEERING_GOVERNANCE.ar.md:59](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/docs/governance/ENGINEERING_GOVERNANCE.ar.md#L59)
- **Line Number:** 59; additional references below
- **Description:** ENG-001 explicitly requires a human review in Arabic, whereas English only requires reviewer assessment. BANK-01 translates versioned selection as اختيار مُصدّر (exported selection), which omits version semantics. The delivery packet's no-material-obligation-difference statement therefore needs reconciliation.
- **Expected Behavior:** Both governed editions preserve actor type, obligation and version/snapshot meaning; ambiguous normative translation blocks the affected acceptance.
- **Actual Behavior:** Human versus unspecified reviewer language differs; versioning is mistranslated as export.
- **Evidence:** E02; English/Arabic handbook:59; English/Arabic BANK-01 blueprint:31; delivery packet:73–75.
- **Root Cause:** Structural parity and earlier implementer comparison did not catch these semantic differences.
- **Impact:** Different acceptance interpretations and an incorrect Arabic description of reproducible snapshots. The English omission does not waive GOV-004's actual-people requirement.
- **Recommended Remediation:** Reconcile the intended human-review obligation in both handbooks in one scoped PR, replace اختيار مُصدّر with اختيار محدد الإصدار (or equivalent reviewed text), and append a correction to the previous equivalence conclusion without erasing history.
- **Acceptance Criteria for Fix:** A substantive bilingual reviewer accepts the same obligation and versioning semantics on the exact revised candidate; structure/version/order checks pass.
- **Verification Method:** Clause-by-clause comparison of actors, obligations, conditions and technical terms, plus foundation/contract regressions.
- **Blocking Status:** Yes — affected bilingual baseline acceptance under handbook:5
- **Current Status:** OPEN
- **Tracking:** [GitHub Issue](https://github.com/ManeaAlShabrain/QASCP/issues/41)

## QAR-006 — Foundation quick-start omits validator installation prerequisites

- **Finding ID:** QAR-006
- **Finding Title:** Foundation quick-start omits validator installation prerequisites
- **Reviewer ID:** REV-07
- **Category:** Developer documentation
- **Severity:** LOW — P3
- **Affected Phase:** P1
- **Requirement Reference:** QASCP-ENG-001/002; P1-V01/03
- **Affected File:** [README.md:44](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/README.md#L44)
- **Line Number:** 44; additional references below
- **Description:** The README and primary procedure instruct users to run unittest directly but do not put the required isolated dependency installation before those commands. Detailed setup exists only deeper in architecture documentation.
- **Expected Behavior:** The main verification path states supported environment and installs the same pinned wheels-only closure as CI before full checks.
- **Actual Behavior:** Documented direct commands in this Windows environment produce five import errors; additionally the symlink case requires an OS privilege unavailable here. The attempted isolated pinned install failed to resolve attrs in this environment.
- **Evidence:** E03; README:44–48; PROCEDURES:5–10; graph import contracts:77–83; evidence/local-results.json.
- **Root Cause:** Quick-start was not updated as validator dependencies were introduced; local OS limitations are documented elsewhere.
- **Impact:** New reviewers cannot reproduce the full suite from the primary instructions without searching historical design records. This is not a failure of the exact-SHA Linux suite.
- **Recommended Remediation:** Add a supported Linux/CI-equivalent verification recipe, venv creation, pinned --no-deps --only-binary installation, pip check and both full validators/tests. Explain the Windows symlink prerequisite or clearly state the supported full-check platform.
- **Acceptance Criteria for Fix:** A fresh supported environment follows the primary instructions to the complete suite; failures and platform limits remain explicit; no weakening or skipping required checks.
- **Verification Method:** Execute the documented recipe on a fresh supported environment and record exact outputs; preserve the current local failures as history.
- **Blocking Status:** No by itself; no risk deferral approval is inferred
- **Current Status:** OPEN
- **Tracking:** [GitHub Issue](https://github.com/ManeaAlShabrain/QASCP/issues/42)

## QAR-007 — All work-package issues are closed although their acceptance remains pending

- **Finding ID:** QAR-007
- **Finding Title:** All work-package issues are closed although their acceptance remains pending
- **Reviewer ID:** REV-09
- **Category:** Project tracking
- **Severity:** LOW — P3
- **Affected Phase:** P1–P6 tracking
- **Requirement Reference:** QASCP-GOV-001; canonical V2-P* backlog
- **Affected File:** [docs/product/QASCP_2_BACKLOG.md:7](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/docs/product/QASCP_2_BACKLOG.md#L7)
- **Line Number:** 7; additional references below
- **Description:** Live #13–31 and tracker #32 are closed without assignees or labels. P1 acceptance remains pending and P2–P6 functionality is not implemented. Bodies preserve these limits, but the default issue-state view cannot represent remaining work.
- **Expected Behavior:** The active tracker exposes unresolved work and acceptance state while preserving historical closures and decisions.
- **Actual Behavior:** Every canonical package appears closed in GitHub; no independent acceptance is inferred from that state.
- **Evidence:** E07; evidence/issues-snapshot.json; stage record; delivery packet:61–67.
- **Root Cause:** Issue lifecycle and acceptance lifecycle are disconnected; original closure intent is not independently established.
- **Impact:** Planning/search/default dashboard views can hide uncompleted packages and owners.
- **Recommended Remediation:** Have the project owner choose reopening the appropriate existing issues or an explicit active acceptance tracker with owners and states. Link findings to existing issues to avoid duplicates.
- **Acceptance Criteria for Fix:** Pending packages and dependencies are visible with accountable owners; closed history is preserved; closure is not represented as phase approval.
- **Verification Method:** Inspect active tracker against the canonical 19 packages and phase record.
- **Blocking Status:** No additional blocker beyond the mandatory acceptance gaps
- **Current Status:** OPEN
- **Tracking:** [GitHub Issue](https://github.com/ManeaAlShabrain/QASCP/issues/32)

## QAR-008 — Validator packages are version-pinned without artifact hashes

- **Finding ID:** QAR-008
- **Finding Title:** Validator packages are version-pinned without artifact hashes
- **Reviewer ID:** REV-03 / REV-06
- **Category:** Supply-chain improvement
- **Severity:** INFORMATIONAL — P4
- **Affected Phase:** P1 tooling; later release
- **Requirement Reference:** QASCP-ENG-003; PRD-10
- **Affected File:** [requirements-contracts.txt:1](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/requirements-contracts.txt#L1)
- **Line Number:** 1; additional references below
- **Description:** The validation-only closure pins 19 versions and uses wheels-only --no-deps installation, but does not lock wheel hashes. This limitation is accurately disclosed by the existing adoption records.
- **Expected Behavior:** Retain the current explicit limitation and assess artifact-hash locking for the supported build platform as part of supply-chain adoption/release work.
- **Actual Behavior:** Version pins, pip check and the checkout full SHA are present; wheel hash lock, independent current vulnerability assessment and release artifact SBOM are not established by this review.
- **Evidence:** E02, E05; graph import contracts:67; OpenAPI assurance dependency/adoption sections; requirements-contracts.txt.
- **Root Cause:** Hash-locked artifact adoption is intentionally deferred, not falsely claimed complete.
- **Impact:** Version identity alone does not freeze exact package bytes. No malicious package or vulnerable pin is established.
- **Recommended Remediation:** Evaluate a platform-specific reviewed wheel lock with hashes and retain provenance/advisory evidence before applicable release adoption; do not call pip check a vulnerability scanner.
- **Acceptance Criteria for Fix:** If adopted, exact hashes and platform/ABI provenance are recorded and verified; release SBOM requirements are satisfied when a release artifact exists.
- **Verification Method:** Review artifact lock and build/install evidence on the target platform; run an actual advisory scan when available.
- **Blocking Status:** No new P1 blocker from hash absence alone; independent tool review remains QAR-001
- **Current Status:** OPEN
- **Tracking:** Not Available; informational improvement retained in this review

## QAR-009 — Import API response descriptions refer to observation receipts

- **Finding ID:** QAR-009
- **Finding Title:** Import API response descriptions refer to observation receipts
- **Reviewer ID:** REV-04 / REV-07
- **Category:** API documentation consistency
- **Severity:** LOW — P3
- **Affected Phase:** P1 static API
- **Requirement Reference:** PRD-01/02; P1-V02; V2-P1-02
- **Affected File:** [contracts/qascp-2/graph/openapi-0.2.json:327](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/contracts/qascp-2/graph/openapi-0.2.json#L327)
- **Line Number:** 327; additional references below
- **Description:** Both import endpoints describe 201 as New logical observation and 200 as previous observation ID, but their response schema is CommandReceipt with import/command identity.
- **Expected Behavior:** Import responses describe durable command acceptance/replay and the previous import/command receipt, keeping graph completion separate.
- **Actual Behavior:** Observation-specific descriptions were reused on /imports/resources and /imports/relationships.
- **Evidence:** E02; successor API:327,337,460,470; CommandReceipt schema; graph boundary command-receipt description.
- **Root Cause:** Copied response prose was not adapted to the import domain.
- **Impact:** Generated API docs can mislead clients about identifier type and which transaction completed; no incorrect runtime response has been observed.
- **Recommended Remediation:** Use New import command durably accepted; projection state is reported separately and Identical command replay; previous command receipt on both import operations.
- **Acceptance Criteria for Fix:** All four affected descriptions match CommandReceipt and durable-acceptance semantics; observation endpoint retains its own correct description.
- **Verification Method:** Read the rendered/parsed operation descriptions, validate both full documents and shared policy, run existing regressions.
- **Blocking Status:** No by itself
- **Current Status:** OPEN
- **Tracking:** [GitHub Issue](https://github.com/ManeaAlShabrain/QASCP/issues/42)
