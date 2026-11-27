# QASCP 2.0 — Proposed graph receipt and claim-history records

Current2026-11-27: [ADR-P1-ACCEPTANCE-001](ADR-P1-ACCEPTANCE-001.md)
and P1_CONTRACT_SELECTION.json define the concrete review candidate. The dated
proposal/rationale below is preserved; no earlier pending state is relabeled as
a later approval. Owner ratification and P1 exit remain separate.

Status: P1 proposal, 2026-11-16 (Qatar). Package V2-P1-02 / P1-V02. Refines G-03 and G-04 in [the graph decisions](QASCP_2_GRAPH_DECISIONS.md). No database, queue consumer, graph service or operational action is implemented. Independent security/architecture reviewer and accountable owners remain unassigned.

Requirements: PRD-01, PRD-02, PRD-04, PRD-06, PRD-10; QASCP-GOV-001..004, QASCP-SEC-001..005, QASCP-ENG-001..003. Earlier paths affected: receipt identity, graph projection, claim provenance/lineage, correction/retraction and future historical queries. P1 acceptance covers schema/meta-schema validation, static fixture consistency, rejection cases, compatibility review and recorded limitations.

## Artifacts and version boundaries

| Artifact | Proposed role |
|---|---|
| [consumer-receipt-v2.schema.json](../../contracts/qascp-2/graph/consumer-receipt-v2.schema.json) | Internal graph receipt 2.0 with event-specific logical identity and duplicate reference |
| [claim-version.schema.json](../../contracts/qascp-2/graph/claim-version.schema.json) | Immutable P2 source-claim snapshot 0.1 |
| [claim-transition.schema.json](../../contracts/qascp-2/graph/claim-transition.schema.json) | Assert/correct/retract transition 0.1 with expected/prior/new versions |
| [Synthetic records](../../tests/fixtures/graph-record-examples.json) | Four receipts, three claim versions and three transitions |
| [Fixture consistency oracle](../../scripts/verify_graph_record_fixtures.py) | P1 executable specification over fixed synthetic records only |
| [Regression tests](../../tests/test_graph_record_contracts.py) | Schema rejection, duplicate identities, lineage, source time and knowledge cutoff |

Receipt 1.0 remains unchanged at its original path and identifier. Receipt 2.0 is a new candidate, not an in-place reinterpretation or automatic migration. Existing external import commands 0.1 and observation 1.0 are unchanged. Public OpenAPI/history/cursor adoption is separate work. Canonical prose is updated to prevent an unsafe tenant/purpose/input-version-only projection identity from appearing sufficient.

## Receipt 2.0

Logical processing key is (tenant_id, event_id, logical_consumer_id, consumer_version, purpose, input_version). Worker replica identity is recorded in consumer_workload_id but does not change this logical key. A different event at the same schema version is not a duplicate. A new consumer algorithm version creates a different key only through an authorized reprocessing decision.

Each receipt requires a UUID receipt_id, tenant/event scope, logical consumer and version, workload identity, authorization version, purpose, input version, outcome, audit_event_id, recorded_at and correlation_id. Outcomes are processed, duplicate, quarantined or failed. Duplicate requires duplicate_of_receipt_id; that field is forbidden for other outcomes. Failed/quarantined receipts require a reason_code. Trusted services establish these fields after authorization; their presence in JSON is not proof of trust.

The fixture oracle rejects two processed effects for the same logical key. A duplicate must reference an earlier listed processed receipt with the same tenant/key and cannot have an earlier recorded time. Failed/quarantined attempts are not successful processing effects. The actual database must implement atomic uniqueness, retry/concurrency policy and projection/receipt/audit commit behavior; a set in a fixture verifier does not prove those controls.

The receipt's audit reference is required, but the fixture does not contain the actual audit store or prove durability. Consumer-version changes cannot execute a production response again or consume an approval. Rebuild generation activation, retention/replay windows and obsolete-version handling remain controlled operational decisions.

## Claim version 0.1 and transition 0.1

Claim versions carry tenant, stable claim UUID/version, connector/source-claim identity, typed endpoints, relation/qualifier, evidence observation UUID, adapter version, source-valid interval, server recorded_at and payload digest. This first candidate supports only the P2 owns, runs_as and accesses pairs. accesses retains its mandatory entitlement/observed_use qualifier. It excludes later-phase arbitrary relations and model-authored facts.

Transitions carry tenant/connector/claim scope, transition UUID, operation, expected_version/new_version, optional prior_version, reason, actor/type, authorization version, audit reference, server recorded time and correlation. Assert requires expected_version 0, new_version 1 and no prior_version. Correct/retract require positive expected_version and prior_version, and new_version at least 2. The cross-record verifier additionally enforces new_version = expected_version + 1 and prior_version = expected_version.

For this 0.1 candidate each correction fully replaces that source claim's validity interval in the current known view. Endpoint, relation, qualifier, connector and source_claim_id identity are immutable within the lineage; changing any of them needs a separate attributable claim. A correction may change valid_from/valid_to, its evidence and digest. Unknown external source evidence is not invented by the fixture.

Retraction is a terminal withdrawal of the entire claim in the current known view, retaining a full typed tombstone envelope and append-only transition. It does not erase earlier knowledge. To describe legitimate access that ended, correct valid_to rather than withdraw the whole fact. Partial-interval retraction, resurrection and overlapping segments in one lineage are outside this candidate. A new factual assertion after withdrawal requires a new claim identity and explicit provenance. This narrows the earlier general G-04 proposal and requires review.

The oracle rejects missing/orphan versions, duplicate version/transition IDs, cross-tenant targets, source/endpoint identity changes, stale expected versions, noncontiguous versions, backward knowledge timestamps and mismatched version/transition provenance. A source-valid end must be later than its start.

## Historical expectation and limits

For source time V and knowledge cutoff K, the fixture oracle selects transitions known by K, resolves their latest lineage version, then checks that version's half-open source interval [valid_from, valid_to). A later correction cannot hide an older fact from an earlier known-at view. A withdrawn claim has no current visible version, while earlier known views still have their prior version.

The example initially learns a grant at 10:00, learns a correction at 11:00 effective from 08:50, and withdraws it at 12:00. Its earlier known view does not learn the 11:00 correction. The fixture tests source-time boundaries and the withdrawal separately. Timestamps are synthetic, not incident evidence.

الدالة التجريبية تختبر اتساق أمثلة اصطناعية فقط؛ ليست واجهة لعرض تاريخ العميل ولا تمنح صلاحية للاطلاع. عند بناء الخدمة الفعلية يجب تطبيق صلاحيات المستخدم الحالية على كل عقدة وعلاقة ومصدر، حتى عند عرض تاريخ قديم.

The oracle has no identity provider, policy engine, database, locks, clock service, network client or executor. Its synthetic flag is a fixture guard, not a security boundary. It cannot establish real tenancy isolation, source authenticity, concurrent delivery correctness, audit durability, retention compliance or production performance. Runtime history must bind a real authorized snapshot/cutoff and handle equal-time commits and projection completeness under G-05; fixture timestamps alone are insufficient.

## Verification and compatibility

The existing pinned validation-only dependency closure and CI environment from [graph import contracts](QASCP_2_GRAPH_IMPORT_CONTRACTS.md) are reused unchanged. All *.schema.json files are meta-schema checked by the existing suite, and these three are also instance-validated with UUID/date-time checking. The new tests fail on missing dependencies; they do not silently skip. No new external package or CI workflow change is introduced.

Planned P2 verification still needs a real PostgreSQL database and actual application roles: A/B tenant deny cases, simultaneous workers processing one event, two events sharing a schema version, crash/retry at each commit boundary, revoked workload replay, exact source binding and audit failure. Historical access and assurance invalidation remain P5 runtime verification with earlier-phase regression. These are not satisfied by the P1 fixture oracle.

Original design provenance: QASCP requirements, the existing graph decision proposals and static contracts. No outside schemas, proprietary taxonomies or source code were copied. This proposal adopts no regulatory applicability or novelty claim.

## Preparation evidence

Base main: 660eb0b253b8f2fd463927004ae2049f58613731, tree c894387fc68951aacb90a15485049143e83c974b. Prepared as an isolated follow-up to merged PR #8, excluding unrelated local contract/test edits. Local Windows/Python 3.14.4 lacks the pinned jsonschema dependencies and restricts symlink creation; those limitations remain explicit in the PR. Local text/JSON/Python syntax/link/foundation results and fresh GitHub Actions results must be recorded against the candidate.

The phase remains P1 / Pending review in [the stage record](../verification/README.md). Independent review, source/bilingual review, verified main branch enforcement and an authorized phase-exit decision remain separate requirements.

Local preparation results: eleven-file UTF-8/newline/whitespace, JSON parsing, Python AST and Markdown local-link checks passed. The foundation verifier returned exit 0. Full unittest discovery returned exit 1 with 19 discovered entries: 16 passed, two missing-jsonschema module-import errors and the existing WinError 1314 symlink error; no skips. New schema/fixture tests require the existing pinned CI environment. These local limits do not establish a full pass.
