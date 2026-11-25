# QA and verification — REV-05

Reviewed repository: ManeaAlShabrain/QASCP · branch: main · commit: `4592eb230fadebb828c8b7d3b7972c6bd1aec012` · date: 2026-11-25, Asia/Riyadh.

AI-assisted review only. REV-01..10 are virtual specialties exercised sequentially by one AI process, not ten people or independent human approvals.

Result: **Blocked for P1 acceptance**, even though exact-SHA Linux CI passed. The additional independent guard probe found a case omitted from the passing suite.

| Evidence | Executed/inspected command | Actual result |
|---|---|---|
| E01 | Git blob SHA-1 over all 73 retrieved source files | 73 match; zero mismatches |
| E03 | Local Python 3.14.4 AST parse of scripts/tests | 12 files parsed |
| E03 | `python -B scripts/verify_foundation.py` | Exit 0; required files/local links/structural bilingual and mappings pass |
| E03 | `python -B -m unittest discover -s tests -v` | Exit 1; 31 discovered entries, 25 successful, 6 errors; zero skips |
| E03 | `python -B scripts/verify_openapi_contracts.py` | Exit 1; missing openapi_spec_validator |
| E03 | Isolated venv + pinned --no-deps --only-binary PyPI install | Exit 1; no matching attrs==25.4.0 in this environment; no full local validator success |
| E04 | Exact workflow guard, four actual temporary Git repos | Clean pass; direct helper denied; include/includeIf helper incorrectly pass |
| E05 | Existing main Actions 45680438066 / job 139439242217 | Exact SHA, Python 3.14.4/Ubuntu 26.04.1; dependency consistency, both full validators/shared policy and 96/96 tests pass; no skipped tests observed |
| E05 | Existing gate job 139439425433 | Success for exact SHA |
| E06 | Historical negative run 45674710740 | Foundation/gate fail at 5c8b52d606f25d807e97029f0c80d48762af165c; later install/validator/unit steps skipped |
| E06 | Historical repaired control 45674930080 | Foundation and gate pass at 2ffc0a864c3d7cf9b43041dadfaffa1bf2438438; #37 closed without merge |

The local six errors comprise five missing-validator test-module imports and one WinError 1314 symlink privilege error. These are actual errors, not six failed application assertions and not six skips. The 31 discovery entries are not the complete 96-test denominator. The supported Linux result is separately evidenced; local errors are retained rather than relabeled.

Full OpenAPI output: original API has 2 local documents/22 references/2 policy operations; successor has 5 documents/51 references/4 operations. This is static specification/policy validation, not deployed API conformance.

## Test adequacy

Positive/negative tests cover missing/invalid documents, JSON ambiguity, mapping/order parity, OpenAPI policy weakening, bounded references, graph visibility and hidden-hop behavior, 201-node/200-edge paging, replay identities, source lineage, dual-time correction and stage-specific approval outcomes. These are substantive P1 tests. Permission lists and unsigned cursor payloads are fixture inputs, so they cannot prove real authorization or token cryptography. There is no independent numerical line/branch coverage measurement; do not infer one from test count.

The prior auth guard preparation covered direct keys and an inspection failure but not included local config. E04 demonstrates why a green suite is insufficient for mandatory control completeness. The corrective implementation must add meaningful include regressions and be independently reviewed.

## Inapplicable and unavailable checks

| Check family | P1 status | Reason |
|---|---|---|
| Real tenant API/DB/RLS/OIDC/connection pool integration | NOT APPLICABLE | First delivered in P2; no application/DB in reviewed tree |
| Broker correlation/replay and labeled precision/recall | NOT APPLICABLE | P3 implementation gate |
| AI injection/retrieval and executor E2E | NOT APPLICABLE | P4, with P5 operational integration |
| Assurance/custody/history/export E2E | NOT APPLICABLE | P5 |
| Performance, restore, install/upgrade release artifact | NOT APPLICABLE | Deployment/P6 evidence; P1 numeric profile remains proposed |
| Full local dependency-enabled tests | NOT VERIFIED | Dependency install and Windows privileges prevent completion; Linux exact-SHA evidence retained separately |
| Current dependency vulnerability/license clearance | NOT VERIFIED | No complete advisory/license audit executed; pip check is only dependency consistency |

P1 is the first phase: no earlier approved phase exists. Required cumulative paths are all current foundation, schema, OpenAPI/policy and graph-oracle regressions. Corrections to CI, translation and contracts require fresh candidate checks and affected cumulative tests; old success cannot be transferred to a new commit.
