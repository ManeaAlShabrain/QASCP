# QASCP 2.0 — Domain, data and API contracts

Proposed P1 interface baseline; PRD-01..06, QASCP-SEC-001..005 and QASCP-AI-001. Review method P1-V02. Runtime validation and DB isolation are later-phase deliverables. The external intake request is [observation.schema.json](../../contracts/qascp-2/observation.schema.json); the trusted adapter emits [normalized-observation.schema.json](../../contracts/qascp-2/normalized-observation.schema.json); and the first-slice API is [openapi.json](../../contracts/qascp-2/openapi.json).

Versioned internal contracts are [trusted context](../../contracts/qascp-2/trusted-context.schema.json), [audit event](../../contracts/qascp-2/audit-event.schema.json), [outbox event](../../contracts/qascp-2/outbox-event.schema.json), [consumer receipt](../../contracts/qascp-2/consumer-receipt.schema.json), [delivery/retry/replay envelope](../../contracts/qascp-2/delivery-envelope.schema.json), and [approval lifecycle](../../contracts/qascp-2/approval-lifecycle.schema.json). These JSON Schemas are static P1 contracts, not claims of implemented services.

## Relational domain model

Every row below is tenant-owned with composite identity (tenant_id, id), version and created_at, unless stated otherwise. All tenant-owned references include tenant_id; UUID uniqueness alone is insufficient. Shared framework catalogs are separately administered, immutable-versioned metadata and cannot reference customer records.

| Record | Principal fields and invariant |
|---|---|
| Asset | kind, source bindings, owner reference, service criticality, classification; external IDs scoped to connector |
| Identity | human/service kind, issuer, external subject, status; tokens and secret values excluded |
| Finding | source key, affected asset, severity basis, observed status; no unsupported inference of exploitability |
| SecurityEvent | connector/source key, source digest, observed_at, received_at, normalized type; append corrections rather than replace |
| AI system | asset reference, model version, tool grants, dataset dependencies and accountable owner |
| GraphNode | typed resource reference to one of the above or control/evidence/case/risk; never orphaned |
| GraphEdge | source/target node, relation, confidence, source observation, valid_from/valid_to, recorded_at, supersedes; endpoints and provenance share tenant |
| Case / risk | linked subject/finding/event references, owner, state and versioned reasoning result; decision history append-only |
| Control mapping | source edition/clause, applicability state, reviewer and review scope; mapped does not mean compliant |
| Evidence | object reference, digest, collector, observed interval, received time, retention, expiry/revocation and classification |
| Assurance assertion | subject/control/policy version, dependency versions, source checkpoints, state, evaluated_at and expected version |
| Proposal / approval | exact action/target/parameter digest and version; human decision, authorization version, expiry, revocation and single-use consumption record |
| Audit event | tenant, actor/workload, authorization version, action, resource, outcome, time and correlation; append-only and atomically recorded for sensitive mutation |
| Outbox event | tenant, producer workload, authorization version, aggregate identity/version, payload reference/digest and correlation; committed with its domain record |
| Consumer receipt | tenant, event, consumer workload, purpose, input version, outcome and correlation; legacy 1.0 shape retained; proposed graph receipt 2.0 uses tenant/event/logical-consumer/consumer-version/purpose/input-version identity |
| Delivery envelope | tenant, producer, authorization version, purpose, input version, attempt, payload reference/digest and correlation; retry, dead-letter and replay retain lineage |

Relations initially: owns (identity→asset), runs_as (AI/application asset→identity), accesses (identity→asset), affects (finding→asset), observed_on (event→asset or identity), supports (evidence→assertion), evaluates (assertion→control), depends_on (asset→asset or assertion→evidence). Enforce this allowlist at domain entry; confidence is in [0,1] and is a source/rule association confidence, not probability of compromise. Store derivation and source reference for every inferred edge. Display names never establish identity.

## Time and replay

UTC RFC3339 instants distinguish observed_at (source-valid time), received_at (server arrival) and recorded_at (projection commit). Retain correction lineage and query historical state at both source time and knowledge cutoff. Edge valid_to may be absent; otherwise it is later than valid_from. Expired evidence is not deleted solely to change assertion status. Unknown source ordering or missing checkpoints prevents selective assurance from claiming complete dependency coverage.

Idempotency key: (trusted tenant, registered connector, source_event_id). The external connector sends a UTF-8 `application/json` request and does not supply the replay digest. The trusted intake adapter computes SHA-256 over the exact HTTP entity-body octets delivered after transfer/content decoding and before character decoding, JSON parsing, whitespace normalization or field reordering. No JSON canonicalization is applied; byte-distinct payloads have distinct digests even when they parse to equivalent objects. The adapter records the lowercase hex digest as `received_payload_digest` in the trusted normalized envelope and receipt.

An optional original-evidence claim is separate from the received-payload digest. It becomes `verified` only when the adapter is authorized to retrieve the referenced source bytes and independently computes the claimed SHA-256 over those source bytes without transformation. If the bytes are unavailable, access is denied or the digest differs, record `unavailable`, `unauthorized` or `mismatch`; do not describe the original evidence as verified and do not silently substitute the request-body digest. Retain the request digest and authorized source reference for at least the configured replay window; original bytes follow the evidence classification, minimization, retention and deletion policy.

The registered adapter and schema version define normalization. An identical idempotency key and received-payload digest returns the previous ID without duplicate audit/domain effects; a changed digest yields 409 and a conflict audit. A correction uses a new source event ID with explicit correction lineage. Idempotency receipt retention covers the authorized replay window; replay older than that window requires a reviewed reconciliation path.

## Customer and connector API boundary

Base path /api/v1. OIDC bearer token validation and operation permission are mandatory. `X-Tenant-ID` is a selector checked against active membership; it never grants membership. Connector principals additionally bind to one tenant and connector registration. The connector_id in the observation must equal that registration. No tenant_id is accepted in the observation body. Server responses may include tenant_id after authorization.

| Operation | Authorization | Result / bounds |
|---|---|---|
| POST /observations | observations:write and bound connector | Adapter hashes the received entity bytes; 201 new; 200 identical replay; 409 same key with changed received-payload digest; 400 bad tenant selector; 401 invalid identity; 403 denied; 413 >1 MiB; 422 schema; 429 quota; 503 unavailable |
| GET /graph/nodes/{node_id}/neighbors | graph:read and resource policy | 200 authorized neighborhood; 404 absent or invisible resource; depth 1..2, limit 1..200 |

Graph returns typed node IDs and provenance-bearing edges, excluding inaccessible endpoints and derived metadata. Traversal must apply resource policy before expansion, counts and pagination. Opaque continuation cursors are signed, expire, and bind tenant, subject/authorization version, node, query and as-of cutoff. Reauthorize each page. A truncated result requires a nonempty next_cursor; a complete result omits next_cursor. The OpenAPI schema encodes this conditional. A truncated result never implies no additional exposure.

Errors contain stable code, generic message and correlation_id, without stack traces or evidence payloads. Per-tenant and per-connector quotas are configured and recorded at deployment. Sensitive audit failure blocks intake; 503 acknowledges no successful mutation. No API in the P1 first-slice contract executes production actions. Proposal, approval, evidence export and case write endpoints require separate phase-scoped contracts before implementation.

## Trusted context and internal delivery contracts

The API authorization service establishes trusted context for user requests after validating OIDC issuer, audience, signature and expiry, resolving active server-side membership and permission, and comparing the tenant selector. The connector authorization service establishes it for intake after validating the workload credential and binding the connector registration to one tenant. The worker authorization service reconstructs a fresh context from signed/scoped job metadata and current workload permission; workers never trust a tenant field merely because it arrived in a message. Domain code accepts only the versioned trusted-context contract.

| Contract | Trust owner | Required binding and failure rule |
|---|---|---|
| Trusted request/worker context | API, connector or worker authorization service | Tenant, principal type/ID, current authorization version, permissions, authentication/expiry, correlation and establishing service. Reject absent, expired or inconsistent context before data access. |
| Audit event | Domain transaction and restricted audit writer | Tenant, actor/workload, authorization version, action, resource, outcome, time and correlation. A required audit write failure aborts the sensitive mutation or uses the documented atomic delivery mechanism. |
| Outbox event | Domain transaction | Tenant, producer workload, authorization version, aggregate/version, payload digest/reference and correlation. Commit with the domain record; never dual-write directly to a broker. |
| Consumer receipt | Authorized consumer | Tenant, event, workload, purpose, input version, outcome and correlation. A tenant mismatch quarantines the delivery without reading its payload. |
| Retry/dead-letter/replay envelope | Delivery service; replay additionally requires an authorized operator decision | Preserve tenant, producer, authorization version, purpose, input version, payload digest, original delivery lineage, attempt and correlation. Reauthorize the current workload scope on every attempt and replay. |

P2 acceptance uses two synthetic tenants and a real test PostgreSQL. It must show same-tenant success and A→B denial at API, domain, composite-FK and raw application-role/RLS layers; reset transaction tenant context across sequential and concurrent pooled-connection reuse; preserve tenant and correlation through outbox, retry, dead-letter and authorized replay; deduplicate graph receipts by tenant/event/logical-consumer/consumer-version/purpose/input-version under the proposed 2.0 contract; abort a sensitive mutation when its required audit record cannot commit; and prove that replay under revoked or changed workload authorization is denied. These cases belong to V2-P2-01, V2-P2-04 and the cumulative V2-P2-05 slice.

## P4 proposal, approval and constrained execution lifecycle

P4 implements this boundary only with synthetic operations. The proposal is untrusted and begins in `proposed`. An authorized human decision bound to tenant, proposal ID/version, exact action, target, canonical parameter digest, authorization version and expiry moves it to `approved` or `rejected`. Revocation moves an unconsumed approval to `revoked`. The constrained executor revalidates tenant, current entitlement, proposal version, action, target, parameters, approval freshness and nonconsumption immediately before creating an `execution_requested` record. In the same protected transaction it writes the required audit event and consumes the approval exactly once, producing `consumed`.

The executor uses an execution ID and downstream idempotency key. A definitive result becomes `succeeded` or `failed`. A partial result or ambiguous timeout becomes `indeterminate` and `reconciliation_required`; it must not retry the mutation until separately authorized reconciliation establishes remote state. Reconciliation records `reconciled_succeeded` or `reconciled_failed` without rewriting the original result. Rejection, revocation, consumption, execution and reconciliation remain append-only case/audit history. If required proposal, decision, consumption or execution audit cannot commit, the boundary fails closed and no successful mutation is acknowledged.

P4 acceptance covers absent approval; altered proposal version, action, target or parameters; cross-tenant approval; expired, revoked, reused and stale-authority approval; concurrent double consumption; model or recommender credentials attempting execution; ambiguous timeout; partial execution; reconciliation before retry; and audit failure at decision, consumption and result recording. V2-P4-02 verifies all cases with synthetic identities and operations. P5 may then add full assurance workflows, evidence custody, remote reconciliation adapters and separately authorized operational integrations without weakening the accepted P4 boundary.

## BANK-01 acceptance trace

Synthetic application asset assistant-01 runs_as service identity svc-01, which accesses database db-01 (restricted). Finding f-01 affects db-01; event e-01 references svc-01. Each source binding is unique within its registered synthetic connector. P2 stores observations and authorized neighborhood; P3 links them into one case with explicit correlation reasons. P4 may summarize the evidence without inventing customer access or confirmed exfiltration, then records an exact human decision and exercises access-reduction only through the constrained synthetic executor boundary. P5 connects that accepted boundary to the full assurance workflow, evidence custody, remote reconciliation and any separately authorized operational adapter, then independently verifies fresh permissions. A second synthetic tenant using identical display names and source IDs remains isolated throughout. Source gaps, ambiguous identity, replay, conflicting digest, late evidence and revoked permissions are required negative cases.

Proposed graph-specific receipt version 2.0 and claim lifecycle version 0.1 are defined in [Graph record contracts](QASCP_2_GRAPH_RECORD_CONTRACTS.md). They require explicit adoption before runtime use. Receipt 1.0 is not a sufficient identity for graph projection deduplication and is not silently migrated.
