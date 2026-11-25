# ADR-GOV-001 — Internal-only solo development assurance

Status: **OWNER-APPROVED PROPOSAL; BASELINE ACTIVATION PENDING REVIEW**. 2026-11-25.
QAR-001; GOV-001/003/004, ENG-001, CMP-001, REL-001; P1-V01..04.
Change request: [GCR-P1-001](../governance/proposals/GCR-P1-001.md),
[العربية](../governance/proposals/GCR-P1-001.ar.md).

Context: one project owner, no assigned independent human reviewers, design-only
P1, rejected exit at 4592eb230fadebb828c8b7d3b7972c6bd1aec012. Actual current policy
does not accept virtual roles as independent people. At proposal preparation, the owner had authorized preparing a proposal only. The later [GOV-DEC-001](../governance/decisions/GOV-DEC-001.md) approves the internal-only proposal and baseline-update preparation; activation/review and phase exit remain separate.

| Option | Benefits | Costs / risks |
|---|---|---|
| Keep current human-review gates for all phase exit | Strong actual independence expectation; no policy change | Solo internal development remains blocked until qualified people are available. |
| Narrow internal-only AI-assisted process plus actual owner decision | Traceable separation and useful progress on synthetic work; explicit enterprise/regulatory boundaries | Shared provider/account/context limits; confirmation bias; owner bears internal accountability; cannot claim human independence or enterprise readiness. |
| Treat AI as human or waive review generally | No legitimate assurance benefit | False identity and uncontrolled enterprise risk; rejected option, never authorized. |

Recommendation: consider the narrow second option only through explicit owner
approval of the paired change request, subsequent governed baseline update and
independently initiated process reviews. Preserve every mandatory technical
control and external human/client/production/regulatory gate. Until then keep
option one, P1 Pending review and no P2. No architectural/runtime contract changes
are adopted by this ADR; separate risk/source/compatibility decisions remain.

Consequences: maintain separate review sessions with immutable manifests and
declarations; owner decides exact internal readiness and scope, no implicit
transfer to production. Reassess before customer engagement or production and
on material policy/ownership changes. A future rollback requires a new governed
decision; historical audit reports and decisions remain immutable.

Provenance: original project-owner constraints and audit #43/GOV-004; no copied
external governance framework, regulatory claim or newly adopted dependency.
Proposal decision: owner APPROVE, 2026-11-25, contextual reply transcribed in [GOV-DEC-001](../governance/decisions/GOV-DEC-001.md). Chosen option: narrow internal-only model. Effective baseline revision: **activation pending review**. No risk acceptance, architecture adoption or phase exit is supplied.
