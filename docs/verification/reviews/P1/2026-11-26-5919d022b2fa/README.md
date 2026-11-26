# P1 separate-process re-audit — 2026-11-26

Reviewed main **5919d022b2fab819e8a74484c656a6a3f7db5fcc**, tree
**b6bda6eb698ec1c83e6b792f950190e56d750f48**. Four real delegated AI review
processes assessed this fixed source before the implementer made any corrections.
They are functionally separate, not actual independent humans or organizations.

| Report | Actual canonical process | Base disposition |
|---|---|---|
| [Security/architecture](01-security-architecture.md) | /root/p1_security_arch_review | HOLD activation; BLOCK P1; new worktree-scope guard gap |
| [Bilingual/source preparation](02-bilingual-sources.md) | /root/p1_bilingual_source_review | Changes requested: SEC-002 ambiguity, stale comparison; no legal approval |
| [Organization/requirements](03-organization-requirements.md) | /root/p1_org_requirements_review | Full36 rows/19packages/12risks/20ADs; owner/authority gaps remain |
| [Final verification/challenge](04-final-verification.md) | /root/p1_final_verification_review | Independently confirmed MEDIUM SEC-NEW-001/BR-L01 and LOW BR-L02; HOLD activation/BLOCK P1 |

Original QAR-004 include correction, QAR-008 platform hash-lock absence and QAR-009
response prose are narrowly verified by separate reviewers. QAR-006 prerequisite
documentation is verified within the supported Linux scope. Overall checkout
acceptance and bilingual acceptance remain blocked on this old base; unqualified
clearance is not inferred from107 passing tests. The actual hosted checkout
unsets the worktree extension: no credential retention/leak in that run is proven.

The original audit REJECTED/72.95 stays unchanged. Subsequent internal risk-owner
confirmation and implementation corrections belong to a later candidate, not a
retroactive rewrite of this review. No P1 exit, P2 or production authority here.

## Evidence custody

[Manifest](manifest.json) identifies actual tasks, original artifact SHA-256 and
each authoritative raw envelope. The published Markdown is a display view only,
with normalized whitespace. To verify an original, decode its envelope's content
as UTF-8 and hash those bytes; the result must equal original_utf8_sha256. This
preserves the exact reports read by the final reviewer and their input digests.
All raw probes/logs/results/source manifests/comparison evidence are retained in
the evidence envelopes; no temporary Git repositories or their metadata are copied.
The report's original evidence filenames map to the corresponding .raw.json
envelope. No author finding, judgment or test result is changed by display format.

Later correction/re-review addenda must identify their own fixed SHA and evidence.
They cannot relabel this base's HOLD/BLOCK verdict or silently change its evidence.
