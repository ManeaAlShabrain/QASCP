# Project governance and organization — REV-09

Reviewed repository: ManeaAlShabrain/QASCP · branch: main · commit: `4592eb230fadebb828c8b7d3b7972c6bd1aec012` · date: 2026-11-25, Asia/Riyadh.

AI-assisted review only; virtual specialties do not represent actual independent people.

Result: **Blocked for P1 exit**. Findings QAR-001/002/003/007.

The canonical backlog defines 19 packages with phase/dependency/acceptance references: five P1, six P2, two P3, two P4, three P5 and one P6. The stage record remains P1. There is no source evidence that a P2 application was started; future phases are not scored as prematurely required deliverables.

| Control | Observed state | Assessment |
|---|---|---|
| Phase prerequisites | Approved-P1 dependency before V2-P2-01; formal state Pending review | Transition is prohibited until P1-V04; passing CI/issue closure is insufficient. |
| Requirements and DoD | 17 governance IDs, 10 PRD IDs, P1-V01..04 and package criteria | Structurally traced; actual acceptance inputs remain missing. |
| Repository branching | Main protected, scoped foundation/test branches and PR history | Current source points to 30 recent commits inspected. This audit creates a separate report-only review branch. |
| Branch rule | Active Protect main; default branch; strict gate from GitHub Actions App 15368; no bypass actors | Required PR/check enforcement exists. Required approving review count is 0: workflow policy does not mechanically supply independent human approval. The handbook does not explicitly mandate a count of 1, so this fact is not separately invented as a ruleset violation. |
| Controlled negative | #37 failed gate, recorded blocked merge state; repaired positive; closed without merge | Historical evidence supports enforcement at that configuration. No new negative merge experiment or merge-endpoint rejection was performed by this auditor. |
| Issues | Existing #13–31 and #32 closed, no assignees/labels at initial inspection | QAR-007 tracking ambiguity. Bodies already warn that closure is not approval; actual closure motivation is unknown. |
| Human decisions | #13 contains a transcribed scope-only decision on an earlier SHA | Original chat not independently available. No scope/exit approval for the current candidate is inferred. |
| Release | P1 has no operational release artifact | Install/recovery/SBOM/customer release approval belong to their applicable later gates. |

Existing acceptance issues #14/#15/#16/#17 and tracker #32 were reused as references rather than duplicated or silently reopened. Novel validated findings are in #40/#41/#42, with severity/status in titles and bodies. The labels listing endpoint was not supported by the GitHub connector; no unverified label names were applied. No assignee or qualified human reviewer was fabricated.

The new inline COMMENT on merged #38 identifies QAR-004 at its actual changed source line and is explicitly an AI follow-up via the owner's account. It is not REQUEST_CHANGES from a human account, not an approval, not a phase decision and not a merge. Existing branch rules are unchanged.
