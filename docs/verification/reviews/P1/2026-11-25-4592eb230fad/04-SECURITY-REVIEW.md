# Cybersecurity and AI security review — REV-03

Reviewed repository: ManeaAlShabrain/QASCP · branch: main · commit: `4592eb230fadebb828c8b7d3b7972c6bd1aec012` · date: 2026-11-25, Asia/Riyadh.

AI-assisted review only. REV-01..10 are virtual specialties exercised sequentially by one AI process, not ten people or independent human approvals.

Result: **Blocked for acceptance**. Findings QAR-001/002/004; QAR-008 is informational. No CRITICAL/P0 finding or deployed-service exploit was established.

| Area | P1 assessment | Required future evidence |
|---|---|---|
| Authentication/RBAC/ABAC | Trusted server identity, current membership, user/workload separation and fail-closed context are documented | P2 OIDC issuer/audience/signature/expiry, operation/resource policy and two-tenant entry-point tests |
| Database/derived data | Composite tenant references, RLS without bypass, connection reset, scoped objects/cache/jobs/graph/export/retrieval | Real DB/application roles, A/B joins/FK/pool/worker denial and restored access tests |
| Intake/API | Client cannot supply tenant authority; body bound, registration binding, exact received-byte replay digest and generic errors | Real content decoding/body bounds, quotas, revoked source replay, audit failures |
| Audit and data protection | Atomic sensitive domain/audit/outbox, append-only restricted storage; minimization, retention and encryption defined as requirements | P2/P5/P6 persistence, integrity, rotation, custody/deletion/recovery tests |
| AI | Retrieved text/model output untrusted; source citations/abstention; deterministic facts separate; no AI execution credentials | P4 adversarial prompt injection/disclosure/permission evaluations and exact-human-approval lifecycle; P5 operational reconciliation |
| Supply chain | Pinned checkout SHA, read-only CI, no persisted checkout credential; 19 pinned validation packages, wheels-only/no-deps, pip check | Qualified adoption/license/advisory assessment still pending; pip check is not vulnerability scanning; wheel hashes are a separate improvement |
| Acceptance controls | Required gate, always()/needs/success-only propagation, active default-branch rules and no bypass actors observed | Correct/review the local-auth guard blind spot QAR-004; fresh candidate evidence |

## Reproduced CI guard failure

Exact source [.github/workflows/ci.yml:30](https://github.com/ManeaAlShabrain/QASCP/blob/4592eb230fadebb828c8b7d3b7972c6bd1aec012/.github/workflows/ci.yml#L30). The independent script extracts the workflow's embedded Python unchanged and runs it in four fresh Git repositories with nonsecret markers. No helper is invoked and no credential is used.

| Case | Exact guard exit | Effective included prohibited key | Assessment |
|---|---:|---|---|
| Clean local config | 0 | None | Expected pass |
| Direct credential.helper | 1 | credential.helper | Expected fail |
| include.path imports helper | 0 | credential.helper | False clean result |
| Matching includeIf imports helper | 0 | credential.helper | False clean result |

Evidence: [probe output](evidence/checkout-probe.json), [reproduction script](evidence/checkout_probe.py), [Issue #40](https://github.com/ManeaAlShabrain/QASCP/issues/40), [inline source comment](https://github.com/ManeaAlShabrain/QASCP/pull/38#discussion_r4699827512). Official [Git config documentation](https://git-scm.com/docs/git-config) describes include processing and its scoped-query default. The actual hosted log removes temporary includeIf entries before the guard; this demonstrates a checker blind spot, not a leaked hosted token.

Rerun from a repository root: `python docs/verification/reviews/P1/2026-11-25-4592eb230fad/evidence/checkout_probe.py .`. The script writes checkout-probe.json beside itself; use a disposable copy for reproducibility without changing the retained evidence. Windows/Python 3.14.4/Git 2.54.0.windows.1 was the executed environment. Linux behavior must be confirmed with the corrective implementation rather than silently claimed here.

## Threat dispositions

T01/T02 tenant and context; T03/T04 source identity/replay/conflation; T05/T06 AI injection/approval; T07/T08 stale assurance/audit; T09/T10 build compromise/resource exhaustion; T11/T12 restore/claims are covered as design risks. Their likelihood/impact are proposals and all actual owners remain missing. This AI process accepts no residual risk.

No ISO/PCI/SOC2/OWASP certification, production tenant-isolation test, full dependency advisory clearance or universal no-secrets claim is made. Standards can inform future tests only after exact source/version and scope decisions.
