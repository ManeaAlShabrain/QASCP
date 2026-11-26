# P1 second-review corrective candidate — 2026-11-26

Reviewed base: main **5919d022b2fab819e8a74484c656a6a3f7db5fcc**, tree
**b6bda6eb698ec1c83e6b792f950190e56d750f48**. Four separately delegated AI
processes completed read-only reviews before these implementation changes.
These are functional AI reviews, not human/organizational independence.
Original REJECTED/72.95 and all earlier failures remain unchanged.

| Review finding | Implementer correction | Verification / remaining condition |
|---|---|---|
| SEC-NEW-001 / #40 | Inspect both Git --local and --worktree scopes with includes disabled/enabled; all include/auth keys and inspection failures retain fail-closed/no-values handling | 15 actual/injected-error regression methods pass locally, including active worktree helper/header/SSH, scoped variants, includes/conditional includes, benign worktree, malformed worktree and late inspection failures. Fresh supported CI and separate re-review required. |
| BR-L01 / #41 | Both SEC-002 editions now name shared-metadata services/access paths and explicitly prohibit their permission to access tenant records | Clarifies the existing no-access obligation; no tenant/control exception, new deployment authority or weaker policy. Affected substantive bilingual/security review required. |
| BR-L02 / #41 | Add dated historical/current-status wrapper to P1_BILINGUAL_REMEDIATION; keep original baseline 1.0 comparison verbatim below it | Current baseline 1.1/owner-decision/process references replace interpretation of the old comparison as current acceptance. |
| BR-O01 | Keep policy-activation findings distinct from phase-exit findings in the eventual activation record | Clarification observation, not proof of circularity. Risk/residual/AD/phase decisions cannot be closed by policy activation. |
| Subsequent T01–T12 confirmation / #14 | Record [RISK-DEC-001](../governance/decisions/RISK-DEC-001.md) and populate confirmed internal owners | Residual ratings, risk-acceptance references and review dates remain unset; no bank/regulator/client authority, AD adoption or P1 exit inferred. |

Official semantics: [Git config scope documentation](https://git-scm.com/docs/git-config#Documentation/git-config.txt---worktree).
Worktree configuration is a repository-resident scope that --local alone omits.
The exact old hosted checkout unsets extensions.worktreeConfig, so the independent
probe proves a reusable-checker completeness defect, not surviving credentials,
a leak or a compromised runner in that run. Global/system/command configuration
and arbitrary runner compromise remain outside this check's assertion.

Reports/evidence are published under
`docs/verification/reviews/P1/2026-11-26-5919d022b2fa/` with actual task IDs,
fixed inputs and preserved original-content digests. They assess the old base;
later re-review addenda must name the new candidate and must not relabel the
old rejection or old 12-null-owner observation as assessing these corrections.
Display Markdown may normalize whitespace; authoritative original UTF-8 content
and SHA-256 remain in the corresponding raw JSON envelopes.

Requirements: GOV-001/003/004, SEC-002/004, ENG-001/002/003, REL-001;
P1-V01..04. Changes remain P1 design/verification/governance only. No workflow,
dependency, API/schema version or runtime component is changed. No P2.

Implementer status: **READY FOR RE-REVIEW**, not VERIFIED FIXED. Baseline 1.1
activation remains pending the corrected candidate's separate dispositions.
P1 exit separately remains blocked by reviewed residual-risk dispositions,
unadopted AD01–AD20 and the owner's exact-candidate phase decision.
