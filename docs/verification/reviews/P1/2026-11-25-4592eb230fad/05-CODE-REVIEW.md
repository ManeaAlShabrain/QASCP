# Software engineering and code review — REV-04

Reviewed repository: ManeaAlShabrain/QASCP · branch: main · commit: `4592eb230fadebb828c8b7d3b7972c6bd1aec012` · date: 2026-11-25, Asia/Riyadh.

AI-assisted review only. REV-01..10 are virtual specialties exercised sequentially by one AI process, not ten people or independent human approvals.

Result: **Tooling reviewed with a confirmed correction required**. Findings QAR-004/009. Code score applies to P1 verification tools, not an absent application.

The five scripts separate foundation/traceability, bounded OpenAPI validation, shared API policy, query fixtures and receipt/history fixtures. Twelve script/test Python files passed local AST parsing. Actual Linux execution is E05; local dependency errors are E03.

| Subject | Finding/evidence |
|---|---|
| Strict JSON | Duplicate object keys, NaN/Infinity and overflowing floats are rejected by the shared decoder; current regressions include nested invalid cases. |
| File/reference boundaries | Contract containment is checked before reading; local-only JSON pointers and explicit remote/query/UNC restrictions are present. Resolver restrictions and positive full-validator tests are complementary. Concurrent filesystem mutation is outside the claimed boundary. |
| OpenAPI policy | Shared function is called on the same decoded documents as full validation; bearer/tenant definitions, all eight operation methods, overrides/aliases/cycles and required response categories are checked. These checks do not implement runtime OIDC or permission enforcement. |
| Fixture integrity | Complete synthetic graphs are validated before visibility filtering; duplicates/dangling/type/interval failures cannot be silently collapsed. Receipt logical keys and immutable claim lineage are explicit. |
| Error handling | Invalid required inputs fail rather than silently skip tests; missing validators fail imports. Some malformed programmer-controlled inputs raise exceptions, which fail CI; no customer API error handler is claimed. |
| Performance | Fixture traversal iterates in-memory data and validates repeatedly. This is acceptable for bounded synthetic conformance tests; do not connect it to production routes or interpret it as a scale benchmark. |
| Incomplete/fake implementation | No application route, database or executor is claimed delivered; fixture unsigned cursors and visibility allowlists are clearly marked. No runtime stub is counted as completed functionality. |
| Maintainability | Shared decoder/policy reduce divergent security assertions. The auth guard remains embedded workflow code without retained include regressions; QAR-004 specifies a meaningful real-Git regression rather than an implementation-mirroring assertion. |
| API prose | Import operations use CommandReceipt but observation-specific descriptions; QAR-009. |

Prior implementer CR-01..07 reports were checked against present code and tests; they are historical remediation claims, not independent approvals. The current suite meaningfully exercises those boundaries, but does not prove all unknown negative cases. No source changes were made by this reviewer.
