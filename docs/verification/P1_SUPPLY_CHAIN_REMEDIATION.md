# QAR-008 — P1 validation supply-chain disposition

ENG-003, GOV-002/003/004, PRD-10; P1-V02/03. Implementer evidence only,
independent adoption/license review pending. No production artifact exists.

| Measure | Implemented P1 scope | Evidence and limits |
|---|---|---|
| Exact artifact hash locking | 19 Linux x86_64 CPython 3.14 wheel hashes; --require-hashes, --only-binary and --no-deps in CI | [Lock](../../requirements-contracts-linux-cp314.lock); lock/pins/provenance consistency verifier plus tamper regression. Final candidate CI must demonstrate actual installation. |
| Artifact integrity | Downloaded wheels SHA-256 compared with official PyPI release metadata; yanked/mismatch fails | [Captured evidence](remediation/P1-2026-11-25/dependency-evidence.json), Actions 45690090809/job 139472925358. TLS metadata and downloaded artifact share publisher trust; not an independent signature. |
| Provenance | Per-artifact publisher URL, wheel filename, digest, Python/platform, license metadata, exact run/candidate | Metadata records origin, not authorization to redistribute or proof of publisher security. Qualified license/adoption disposition pending. |
| Advisory lookup / bounded SCA | Actual PyPI release-JSON vulnerability lookup for all 19 versions; no entries returned in the retained run | No exhaustive advisory database/SAST/dependency reachability conclusion. Query date and source bound result; pip check is separate. Network/parse/mismatch/advisory fails CI; no fabricated empty fallback. |
| Validation wheel SBOM | [CycloneDX 1.6 inventory](remediation/P1-2026-11-25/validation-wheels.cdx.json) with package URLs and SHA-256 | Controlled validator wheels only, not full runner or application SBOM; JSON generated from captured artifacts, not claimed externally schema-certified. Bootstrap pip, OS and Actions excluded explicitly. |
| Reproducible validation inputs | Exact wheel/action bytes, explicit ABI check, fresh venv, dependency consistency/full schema/API/regressions | ubuntu-latest runner image, base Python/pip/OS remain external mutable inputs; actual image/version in run logs. No bit-for-bit environment/build reproducibility claim. |
| CI privileges and auth | Read-only contents, no persistent checkout credentials, include/auth guard; gate success-only | QAR-004 regression and fresh CI; no branch-rule change or bypass. |

Deferred with reasons, not marked complete: a fully pinned container/OS/bootstrap
toolchain and signed build provenance need a deliverable build artifact and a
separately reviewed image/toolchain choice (P2/P6); production application/image
SBOM and full dependency/container vulnerability scanning apply when those inputs
exist (P2/P6); external human license/advisory review remains required under
current GOV-004. Windows/ARM/other Python wheel sets require separate reviewed
locks before support is claimed. More advisory sources or a new scanner dependency
requires explicit provenance/license/pin/adoption review; this patch adds none.
No pending regulatory/right gap is treated as accepted by internal owner proposal.

Historical design documents accurately described their earlier version-only
state. This dated record supersedes that current tooling limitation for the
corrected candidate only; it does not rewrite earlier reports or declare release
approval. Future pin updates must refresh lock/provenance/inventory, inspect
license/advisory changes, run clean installation and tests, and receive review.
