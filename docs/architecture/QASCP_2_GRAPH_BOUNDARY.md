# QASCP 2.0 — Graph boundary contract and consolidated conformance

Status: P1 proposal, 2026-11-16 (Qatar). Package V2-P1-02 / P1-V02. Refines G-02/G-05 and connects the merged import/receipt/history proposals into one boundary candidate. No FastAPI service, database, identity provider, signed-token executor or customer integration is delivered. Owner and independent reviewer remain pending. [Stage status](../verification/README.md) governs phase authorization.

Requirements: PRD-01, PRD-02, PRD-06, PRD-09, PRD-10; QASCP-GOV-001..004, QASCP-SEC-001..005, QASCP-ENG-001..003. Earlier paths affected: observation resolution state, import receipts, graph query/direction, edge qualifier, snapshot metadata, pagination and future historical selection.

## Scope and compatibility

| Contract | Role |
|---|---|
| [Neighborhood query 0.2](../../contracts/qascp-2/graph/neighborhood-query.schema.json) | Normalized path/query input with bounded depth, edge limit, direction and reserved historical selectors |
| [Neighborhood page 0.2](../../contracts/qascp-2/graph/neighborhood-page.schema.json) | Root, visible nodes/edges, qualifier, snapshot metadata and continuation |
| [Cursor binding payload 0.2](../../contracts/qascp-2/graph/cursor-binding.schema.json) | Internal payload bound to tenant/principal/current authority, normalized query and snapshot |
| [Successor OpenAPI 0.2](../../contracts/qascp-2/graph/openapi-0.2.json) | Existing observation intake, proposed resource/relationship imports and graph neighborhood |
| [Fixture graph](../../tests/fixtures/graph-query-examples.json) | One synthetic tenant, five nodes and a cyclic dependency graph |
| [Conformance oracle](../../scripts/verify_graph_query_fixtures.py) / [tests](../../tests/test_graph_boundary_contracts.py) | Static paging, visibility, cursor-binding, endpoint/interval and bounded-reference expectations |

The original contracts/qascp-2/openapi.json remains unchanged. The 0.2 document is a separately reviewed successor candidate, not an additional running endpoint or automatic migration. A deployed API-version negotiation, rollout and client compatibility decision is required before implementation. Fields cannot be injected into an original additionalProperties:false response in place.

## Proposed endpoint boundary

| Method / path | Required operation permission | Payload or response |
|---|---|---|
| POST /observations | observations:write plus registered connector binding | Existing external observation; successor receipt adds projection_state |
| POST /imports/resources | inventory:import plus registered connector capability | ResourceImport 0.1; CommandReceipt |
| POST /imports/relationships | graph:claims:import plus registered connector capability | RelationshipClaimImport 0.1; CommandReceipt |
| GET /graph/nodes/{node_id}/neighbors | graph:read plus resource/provenance policy | Normalized query and neighborhood page 0.2 |

All paths require X-Tenant-ID validated against active identity/registration, with global bearer authentication and no operation override. Import replays recheck current authorization. The shared import idempotency key remains tenant/connector/command_id across both import families; its digest is computed over received entity bytes. New intake/import receipts represent durable accepted work, not completed graph projection. projection_state is pending, projected or quarantined.

Successor command receipts require import_id, command_id, command_family, tenant, received time, disposition, digest, projection state and correlation. A receipt grants no access to a hidden resource. 409 covers digest/version conflicts and, on graph queries, stale/altered snapshot bindings that require restart. Errors retain the generic message/correlation convention. Size, quota and permission enforcement require runtime entry-point tests; descriptions alone do not enforce them.

## Query, snapshot and visibility

Normalize depth (default 1), limit (default 100), direction (default both), root UUID and selected times before cursor binding. Supported depth is 1..2; edge limit is 1..200. The fixture digest uses sorted compact JSON over these fixed typed fields, never over a caller-supplied tenant or trust claim. It is distinct from the raw-byte ingestion digest. Real token issuance must use one documented canonicalization on producer and verifier.

A first request selects an authorized immutable projection snapshot/generation with knowledge_cutoff, valid_at, expiry and scoped projection_state. The 0.2 response removes ambiguous as_of in favor of these explicit meanings. A projection state of current is relative to its defined source checkpoints, not a global assertion that every real-world event is known. lagging and unknown remain explicit even if no permitted edges are returned.

Explicit valid_at/known_at selectors are reserved for separately authorized P5 historical delivery and require graph:history in addition to graph:read. A P2 implementation must reject history selectors until that delivery is enabled. Schema support is not phase authorization. The synthetic oracle requires query times to match its fixed example snapshot and does not simulate arbitrary historical retrieval.

Apply resource, edge and provenance policy before each hop, counts, ordering or pagination. Invisible intermediate nodes cannot connect visible endpoints. Use the earliest authorized hop per edge, order by hop then stable edge ID, and prevent frontier cycles with visited IDs. Direction is incoming, outgoing or both; it does not create inverse facts or inherit permission.

Every page includes its root and all returned edge endpoints. Enforce at most 201 nodes independently of 200 edges. Later pages may contain disjoint depth-two edges, so they may need fewer edges to preserve endpoint closure. The 400-edge fanout fixture expects pages of 200, 100 and 100 edges. Truncated pages require next_cursor; complete pages forbid it.

The fixtures accept predeclared allowed-node/edge/provenance sets as example inputs. They do not evaluate actual membership, ABAC or RLS. Public node/edge identifiers and text-independent state codes support shared RTL/LTR semantics, but no frontend or accessibility acceptance is delivered here.

## Cursor authority and cryptography boundary

The internal binding payload includes tenant_id, principal_id, authorization_version, root, snapshot/generation IDs, normalized query digest, valid/knowledge times, issuance/expiry, final hop/edge ordering key and key_id. Revalidate current authorization and snapshot status on every page; changes invalidate continuation rather than return a partially privileged snapshot.

The external API carries an opaque signed token. The internal payload schema is not a signature or a key-management design. Production implementation must verify signature/MAC, algorithm allowlist, active key identity/rotation/revocation, expiry and exact bindings before using an ordering key. Merely decoding a token or passing schema validation is insufficient.

The fixture oracle deliberately returns an explicit synthetic-unsigned marker plus a separate unsigned payload for conformance tests. It refuses an opaque cursor without a supplied fixture binding. It does not implement cryptography and must never be wired into an application route. The marker cannot be used as evidence that tamper-resistant tokens, authorization or tenant isolation have been implemented.

## Conformance coverage

The added regressions cover cycles; hidden intermediates; concealed edge/provenance filtering; uniform absent/invisible root error; direction/depth and invalid query bounds; complete nonduplicated page coverage; tenant/principal/authorization/snapshot/query binding changes; expiry/future-issued bindings; refusal to treat opaque text as verified; truncation/cursor coupling; missing endpoints/duplicate IDs/type pairs; accesses qualifier; unknown secret metadata; future/expired claims; explicit lag; independent edge/node budgets; and local OpenAPI contract regressions.

The QASCP-specific API checker verifies version/security shape, path parameters, unique operation IDs, required documented response categories, POST body bindings, component JSON Schema structure and local JSON Pointer references. Referenced files must stay under contracts; remote reference retrieval is refused. It does not constitute full OpenAPI specification or semantic validation. A dedicated bounded full OpenAPI verifier is now specified in [OpenAPI assurance](QASCP_2_OPENAPI_ASSURANCE.md); its fresh candidate CI result is separate from these QASCP-specific checks.

Existing pinned dependencies and CI setup are reused; no new package or workflow change is introduced. All new *.schema.json files are included in the existing Draft 2020-12 meta-schema tests. Missing checker dependencies fail rather than skip. No runtime DB, concurrency, cryptographic, performance or recovery result is claimed.

## Delivery and original design

This is one consolidated P1 review package linked from the canonical graph decisions and README. Runtime implementation follows the existing V2-P2 packages after formal P1 approval; historical/export paths remain P5. The package does not create a parallel backlog or modify the bilingual handbook. Independently review compatibility, policy-before-traversal semantics, cursor/key boundaries, pending resolution, retention, source minimization and verifier acceptance changes.

Design provenance is the owner's vision and the QASCP PRD, graph decisions and merged static contracts. No external product implementation or proprietary schema is copied. Existing validation-tool adoption remains governed by its recorded review; this change adds no legal, compliance or novelty conclusion.

## Preparation evidence

Base main 9c8fb2e665d25b325b4e9fa82b4c97f80d1b77cd, tree c042a9c277061d84f11406d8a2a2ff9b742e5f7e. Prepared in an isolated snapshot of merged PR #9, excluding unrelated shared-workspace changes. Local Windows/Python 3.14.4 lacks the installed jsonschema closure and has the known symlink restriction. Exact local checks and the fresh candidate Linux Actions result are recorded in the consolidated PR; previous candidate CI is not reused as new evidence.

For remaining review and authorized phase exit, use [the consolidated review package](../verification/QASCP_2_P1_REVIEW_PACKAGE.md).

Local preparation results: twelve-file UTF-8/newline/whitespace, JSON parsing, Python AST and Markdown local-link checks passed; foundation verification returned exit 0. Full Windows unittest discovery returned exit 1 with 20 discovered entries: 16 passed, three missing-jsonschema import errors and one existing WinError 1314 symlink error, no skips. The 19 newly added boundary tests require the existing pinned CI environment. Fresh Linux CI is required for this candidate.
