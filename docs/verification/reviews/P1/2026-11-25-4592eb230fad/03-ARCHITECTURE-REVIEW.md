# Architecture review — REV-02

Reviewed repository: ManeaAlShabrain/QASCP · branch: main · commit: `4592eb230fadebb828c8b7d3b7972c6bd1aec012` · date: 2026-11-25, Asia/Riyadh.

AI-assisted review only. REV-01..10 are virtual specialties exercised sequentially by one AI process, not ten people or independent human approvals.

Result: **Blocked for P1 adoption**. Findings: QAR-002/003/005.

| Boundary | Assessed design | Evidence and disposition |
|---|---|---|
| Modular monolith | FastAPI modules + PostgreSQL, domain-owned writes and explicit interfaces reduce early distributed transactions | ADR-2-001/002; reasonable P1 choice. Scalability is an unmeasured hypothesis, not a verified capability. |
| Resource ownership | Composite tenant keys/FKs, immutable kind, deferred registry/domain consistency, restricted runtime/migrator roles | BANK-01 B02 and G-06. Design reviewed; exact migration/role implementation belongs to P2. |
| Intake and source identity | Authenticated connector binding, exact received-body digest, identical replay/conflict behavior; unresolved references avoid bootstrap circularity | Contracts, G-01/B03. No implicit resource creation; source authority/reassignment policy needs disposition. |
| Atomicity | T1 intake and T2 imports commit domain/audit/outbox; T3 projection/receipt/checkpoint/audit commit together | B03/BA04/05/08. No distributed exactly-once claim; planned crash/concurrency matrix is appropriate. |
| Projection | Event-specific receipt identity independent of replicas, isolated rebuild generations, controlled activation | Receipt 2.0/G-03. Original 1.0 is explicitly insufficient; adoption is pending. |
| Graph pages | Authorization before traversal/counts, node/edge budgets, tenant/principal/query/snapshot cursor binding | Boundary 0.2. Fixture oracle is a useful executable specification; cryptography/real authorization are future work. |
| Historical semantics | Source-valid versus knowledge time; expected versions and terminal claim withdrawal | G-04, records 0.1. Equal-time position is internal; full historical API remains P5. |
| Failure and retention | Quarantine, audit failure abort, uncertain result reconciliation, generation expiry and deletion propagation | Appropriate design invariants; actual retention and deployment targets need scoped owners. |
| AI/response | Recommendation separate from facts, human decision and constrained executor | P4 synthetic boundary, P5 operational integration. No model production write authority. |

**Unresolved decisions:** select API 0.1/0.2 behavior under the shared /api/v1 server path, receipt version, client compatibility, source-field precedence/collision/reassignment and B06 registry/transaction dispositions. Proposed schemas existing is not acceptance; QAR-003 contains executable closure criteria.

**Debt:** many linked proposal layers increase interpretation cost. Preserve the authority matrix and adopt one explicit implementation target rather than treating every schema as simultaneously active. Specialized graph/search infrastructure remains justified only by measured demand. No microservice rewrite is recommended from this review.

**Next-phase readiness:** BA01..BA11 correctly plan two tenants, real entry points, DB roles/RLS, concurrency/crash and bilingual authorized views. Do not require those future results in P1. Do require the P1 design decisions and actual risk owners before authorizing their implementation.
