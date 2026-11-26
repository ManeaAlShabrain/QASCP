# QASCP 2.0 — Proposed graph import contracts and validation

Current2026-11-27: [ADR-P1-ACCEPTANCE-001](ADR-P1-ACCEPTANCE-001.md)
and P1_CONTRACT_SELECTION.json define the concrete review candidate. The dated
proposal/rationale below is preserved; no earlier pending state is relabeled as
a later approval. Owner ratification and P1 exit remain separate.

Status: P1 proposal, 2026-11-15 (Qatar). Canonical package V2-P1-02 / P1-V02. This refines G-01/G-02 in [the graph decisions](QASCP_2_GRAPH_DECISIONS.md), with static payload rules supporting G-03/G-04. No application endpoint, authorization service, migration or production integration is implemented. Owner/independent reviewer: assignment pending.

Requirements: PRD-01, PRD-02, PRD-06, PRD-10; QASCP-GOV-002/003/004, QASCP-SEC-001..005, QASCP-ENG-001..003. Affected paths: future inventory/relationship import, source identity, version conflicts and contract validation in the existing foundation job. Acceptance: both schemas pass Draft 2020-12 meta-schema checks, accepted synthetic commands validate with UUID/date-time checks enabled, and invalid type pairs, qualifiers, versions, fields and selectors fail. P1-V02 independent review remains required.

## Delivered static contracts

| Artifact | Meaning |
|---|---|
| [resource-import.schema.json](../../contracts/qascp-2/graph/resource-import.schema.json) | Strict create/update union for asset and identity source records |
| [relationship-import.schema.json](../../contracts/qascp-2/graph/relationship-import.schema.json) | P2 assert/correct/retract commands for owns, runs_as and accesses |
| [Synthetic examples](../../tests/fixtures/graph-import-examples.json) | Nine schema-valid examples: two assets, one identity, four claims, correction and retraction |
| [Validator regressions](../../tests/test_graph_import_contracts.py) | Actual Draft 2020-12 meta-schema and instance validation, including rejection cases |
| [Validation dependencies](../../requirements-contracts.txt) | Exact versions for the validation-only dependency closure |

المخططان يحددان شكل الأمر المسموح وحقوله، لكنهما لا يثبتان أن المرسل مخوّل أو أن الأصل موجود. اختبار JSON Schema لا يُغني عن اختبارات العزل وقاعدة البيانات والتفويض في P2.

## Version and command rules

Command version is 0.1. Existing observation/internal contracts retain their current versions and content; neither observation 1.0 nor current OpenAPI is silently changed. Commands are proposed domain operations, not advertised new HTTP endpoints. OpenAPI adoption and evidence-registration/pending-resolution behavior require a separately reviewed interface change before runtime delivery.

ResourceImport now makes operation explicit as create or update, a refinement of the earlier expected_version convention. Create forbids expected_version; update requires a positive integer. Relationship assert forbids expected_version; correct/retract require it to identify the expected prior claim version. Boolean values are not integers for these constraints.

All commands require command_id, connector_id, observed_at and evidence_event_id. Strings have declared length limits and must contain nonwhitespace. UUID syntax and date-time are validated using an explicit FormatChecker. This command version chooses UTC timestamps ending in uppercase Z; offsets are rejected even if otherwise valid RFC3339. The domain additionally requires a sensible observed interval and clock policy.

Source endpoints carry resource_kind and source_id inside the authenticated connector registration, with no tenant_id, arbitrary canonical UUID or cross-source connector selector. The service resolves the tenant and validates connector binding; schema validity cannot authenticate it. Resource records exclude secret/token fields and arbitrary metadata. AI systems, findings and later-phase relation authoring are outside this P2 command version.

owns is identity-to-asset; runs_as is asset-to-identity; accesses is identity-to-asset. accesses requires entitlement or observed_use. A qualifier is prohibited on the other two relations. The domain restricts runs_as to applicable application/service asset subtypes after resolving the resource; an endpoint reference alone does not carry that subtype.

Correction and retraction retain the full typed claim envelope for audit comparison. The domain must verify that endpoints, relation, qualifier and source_claim_id match the expected lineage, or reject the operation. Retraction is not permission to delete another source's claim.

## What schemas deliberately cannot prove

| Rule | Required runtime evidence |
|---|---|
| Tenant and connector authorization, provenance access | Authenticated API/domain negative tests with two tenants |
| Source/evidence existence and permitted unresolved bootstrap intake | Real intake/import integration and resolution-state tests |
| Immutable binding/reassignment and expected-version match | Transaction/concurrency tests against PostgreSQL |
| valid_to strictly later than valid_from | Domain timestamp comparison; JSON Schema does not compare two field values |
| Relation truth, excessive permissions, compromise or exfiltration | Source evidence plus deterministic assessment or attributed review |
| Idempotency across command families and event-specific receipts | Real replay/digest/conflict/crash tests |
| Atomic domain/audit/outbox commit and projection receipt | Database failure injection |
| Cursor/historical semantics or approved workload thresholds | Separate G-04/G-05/G-07 contract and acceptance work |

The nine examples are syntactic fixtures, not an operational event stream: evidence_event_id references are synthetic and do not establish a preexisting snapshot. Runs_as/accesses claims cannot be derived just because resources co-occur. BANK-01 case correlation, AI review and assurance remain P3/P4/P5 work respectively.

## Validation design and proposed dependency adoption

Proposed ADR: ADR-2-GRAPH-VALIDATION-001. Choose python-jsonschema for validation-only tests rather than writing a partial JSON Schema interpreter or mistaking JSON parsing for validation. Use Draft202012Validator.check_schema for every *.schema.json document, and validators with explicit UUID/date-time checks for the two new command types. No runtime application dependency is introduced. Full OpenAPI document validation is covered by the separately proposed [OpenAPI assurance verifier](QASCP_2_OPENAPI_ASSURANCE.md); JSON Schema meta-schema validation alone is not OpenAPI validation.

Primary references: [JSON Schema core](https://json-schema.org/draft/2020-12/json-schema-core), [validator documentation](https://python-jsonschema.readthedocs.io/en/stable/validate/). Original QASCP schemas and tests were written from the product requirements; no external implementation or proprietary taxonomy was copied.

| Validation package / version | Source / declared license context |
|---|---|
| jsonschema 4.26.0 | [PyPI](https://pypi.org/project/jsonschema/4.26.0/), MIT |
| attrs 25.4.0 | [PyPI](https://pypi.org/project/attrs/25.4.0/), MIT |
| jsonschema-specifications 2025.9.1 | [PyPI](https://pypi.org/project/jsonschema-specifications/2025.9.1/), MIT |
| referencing 0.36.2 | [PyPI](https://pypi.org/project/referencing/0.36.2/), MIT |
| rpds-py 0.30.0 | [PyPI](https://pypi.org/project/rpds-py/0.30.0/), MIT |
| typing-extensions 4.15.0 | [PyPI](https://pypi.org/project/typing-extensions/4.15.0/), PSF-2.0 |
| rfc3339-validator 0.1.4 | [PyPI](https://pypi.org/project/rfc3339-validator/0.1.4/), MIT |
| six 1.17.0 | [PyPI](https://pypi.org/project/six/1.17.0/), MIT |

Source/version pages were consulted during preparation. These are proposed development-tool adoptions; independent provenance/license/security review and current vulnerability assessment remain pending. rfc3339-validator is an older small dependency and should be reviewed accordingly; it is chosen explicitly to make date-time assertions active. Do not interpret package presence as regulatory evidence.

CI creates an isolated virtual environment, installs exactly the listed closure from PyPI using --no-deps and --only-binary=:all:, runs pip check and then the entire unittest suite. No fallback to an unpinned dependency resolver or source build is allowed. Packages are version-pinned, not artifact-hash locked; a hash-locked, platform-specific wheel set is a separate supply-chain improvement requiring review. The existing checkout action pin, read-only workflow permissions, foundation job and gate failure propagation remain in place. Changed CI/test acceptance controls require independent security review.

## Commands and current evidence

Base main: 782f625673ff9d4b8c8c76bf1d15705a804fc9a2, tree e4b385468d1c97d0fab7a3db18360592fc9e80d3. Prepared in an isolated copy, excluding unrelated shared-workspace contract/test changes. Local Windows Python 3.14.4 could parse/compile the source, but installing the validator failed with WinError 10013 because outbound sockets were unavailable. No local full-validator success is claimed. Missing validator imports fail the suite rather than skip its tests. The earlier host symlink restriction also remains relevant to local foundation tests.

CI setup, dependency resolution, meta-schema checks and instance tests must run on the published candidate. The PR records the exact SHA, Actions result and any remediation. Schema tests do not establish runtime isolation or authorize P2. Active phase and formal approval remain in [the stage record](../verification/README.md).

Local checks: nine-file UTF-8/newline/whitespace, JSON parse, Python AST and local Markdown link checks passed; foundation verifier passed (exit 0). Full unittest discovery returned exit 1: 18 discovered entries, 16 passed, one missing-jsonschema import error and one existing WinError 1314 symlink error. No tests were skipped. These failures are retained as local environment evidence and are not replaced by a structural-only success claim.

For a dependency-enabled local environment, create a Python virtual environment, install requirements-contracts.txt with the same --no-deps --only-binary=:all: policy as CI, run pip check, then run scripts/verify_foundation.py and the full unittest discovery with that environment's Python. A failed installation or checker import must remain a failed check.


## Current P1 corrective tooling addendum — 2026-11-25

QAR-004/006/008 supersede the earlier tooling limitations for the corrected
candidate only: [checkout boundary correction](../verification/P1_CI_REMEDIATION.md),
[supported clean setup](../verification/P1_VALIDATION_SETUP.md),
[hash-lock/provenance/advisory disposition](../verification/P1_SUPPLY_CHAIN_REMEDIATION.md)
and [exact candidate evidence](../verification/remediation/P1-2026-11-25/README.md).
The inline guard's earlier six-case preparation did not cover include/includeIf;
the replacement rejects those paths and retains real-Git regressions. Nineteen
platform wheel hashes are now enforced in CI; earlier version-only statements
describe their dated baseline. Historical reports/failed results are preserved.
No contract/ADR adoption, independent review, legal applicability or P1 exit is
granted by this tooling correction. P2 remains blocked under the current policy.
