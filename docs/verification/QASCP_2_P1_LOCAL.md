# QASCP 2.0 — Local P1 working-tree evidence

Date: 2026-11-15. Active phase: P1. Decision: Pending review. Branch: `foundation/qascp-2-product-architecture`. Full HEAD: `55b731b6585ee7e3e6c80883ce393941295aaa74`.

This is local working-tree evidence, not evidence for an immutable candidate revision and not P1 approval. The commands below included uncommitted content as described. No customer data, production access, external connector, production mutation, Git staging, commit, push, pull request, rule change or phase decision was involved.

## Scope and working-tree inputs

Requirements: PRD-01..10; QASCP-GOV-001..004, QASCP-SEC-001..005, QASCP-AI-001..002, QASCP-ENG-002, QASCP-CMP-001. Affected proposed interfaces: external observation request, trusted normalized observation, trusted request/worker context, audit, outbox, consumer receipt, delivery/retry/replay, graph neighborhood, proposal/decision and constrained execution lifecycle. The handbooks and their P4 gate were not changed.

Tracked modified files included in the working-tree review:

```text
README.md
docs/architecture/P1_ARCHITECTURE.md
docs/governance/REGULATORY_SOURCES.md
docs/product/QASCP_PRODUCT_DESIGN.md
docs/verification/requirements.json
scripts/verify_foundation.py
tests/test_verify_foundation.py
```

Untracked non-cache files included in the working-tree review:

```text
contracts/qascp-2/approval-lifecycle.schema.json
contracts/qascp-2/audit-event.schema.json
contracts/qascp-2/consumer-receipt.schema.json
contracts/qascp-2/delivery-envelope.schema.json
contracts/qascp-2/normalized-observation.schema.json
contracts/qascp-2/observation.schema.json
contracts/qascp-2/openapi.json
contracts/qascp-2/outbox-event.schema.json
contracts/qascp-2/trusted-context.schema.json
docs/architecture/QASCP_2_ARCHITECTURE.md
docs/architecture/QASCP_2_CONTRACTS.md
docs/architecture/QASCP_2_SUPERSESSION.md
docs/architecture/QASCP_2_THREATS.md
docs/governance/QASCP_2_COVERAGE.md
docs/product/QASCP_2_BACKLOG.md
docs/product/QASCP_2_PRD.md
docs/verification/QASCP_2_P1_LOCAL.md
```

Existing untracked generated caches were present but excluded from the proposed change and explicit source-file review:

```text
scripts/__pycache__/verify_foundation.cpython-314.pyc
tests/__pycache__/test_verify_foundation.cpython-314.pyc
```

## Environment and actual results

Environment: Windows PowerShell 5.1.22621.6133; Python 3.14.4 through `py -3`; Git 2.54.0.windows.1.

| Command or check | Exit | Actual result and coverage |
|---|---:|---|
| `git diff --check` | 0 | No tracked-diff whitespace errors. This Git command included tracked unstaged changes but does not inspect untracked files. |
| `py -3 -B scripts/verify_foundation.py` | 0 | Required files and local Markdown links passed; bilingual handbook phase/requirement parity passed; QASCP governance and PRD-01..10 mappings, canonical backlog references and verification evidence references passed. It read the current tracked and untracked working-tree files required by the verifier. |
| `py -3 -B -m unittest discover -s tests -v` | 0 | 17 tests passed, 0 failed, 0 errors, 0 skipped. The suite includes missing/duplicate PRD IDs, invalid phase/evidence references and broken backlog mapping regressions. It exercised the current modified verifier and required working-tree artifacts. |
| Explicit modified/untracked source check using Python 3.14.4 | 0 | Checked 24 modified or untracked non-cache files for UTF-8 decoding, final newline, trailing whitespace and conflict markers. |
| Contract parse/reference/structure check using Python standard library | 0 | Parsed all 9 JSON files under `contracts/qascp-2`, resolved 23 local `$ref` values including JSON Pointers, and asserted OpenAPI 3.1.0, the two expected paths, global bearer security and the external observation request reference. |
| Validator availability check | 0 | `jsonschema` and `openapi_spec_validator` are not installed. Full JSON Schema meta-schema and full OpenAPI specification validation were therefore not run. Successful JSON parsing/reference resolution is not represented as full schema validation. |

The exact three required commands were rerun after the evidence record was refreshed. Bytecode generation was disabled with `-B`; the two pre-existing cache files remained untouched.

## Remediation disposition

- P4/P5 alignment: the binding P4 governance gate is preserved. P4 now owns exact human approval and the constrained executor boundary using synthetic operations; P5 owns full assurance workflows, evidence custody, remote reconciliation and separately authorized operational integrations.
- Product traceability: `requirements.json` now contains a distinct machine-checked `product_requirements` section for PRD-01..10 with phases, canonical backlog items and verification IDs. The verifier and regression suite fail closed on missing, duplicate or invalid mappings.
- Authority: `QASCP_2_SUPERSESSION.md` is the sole retained/refined/replaced/deprecated map. The engineering handbooks remain binding, and `QASCP_2_BACKLOG.md` is canonical for 2.0 work.
- Tenant contracts: versioned static context, audit, outbox, receipt and delivery schemas identify the service that establishes trust and carry tenant, authorization and correlation across internal boundaries. P2 acceptance cases are design-only in this change.
- Intake digest: the trusted adapter computes SHA-256 over the exact received HTTP entity octets before parsing. Original-evidence verification is a separate authorized retrieval and digest decision.
- Approval lifecycle: proposal, human decision, execution request, atomic consumption, result, revocation and reconciliation records and denial cases are specified for P4 synthetic testing.
- Regulatory status: source identity, edition, rights, access and applicability are consolidated in `REGULATORY_SOURCES.md`; the 2.0 coverage document contains mappings only.

## Historical local result retained for context

Earlier on 2026-11-15, `python -m unittest discover -s tests -v` and a later direct `C:/Python314/python.exe` run each reported 13 tests with 12 passed and one `WinError 1314` error because that invocation could not create the out-of-scope symbolic-link fixture. That was a local host/launch-context limitation, not a skipped test. The current required `py -3 -B` invocation completes the symlink test and all 17 tests successfully. The earlier result is historical and does not replace the current command evidence.

## P1 evidence still outstanding

- P1-V01: automated structural parity and source-register consolidation pass locally. Substantive Arabic–English equivalence review and designated regulatory review of editions, rights and applicability remain pending.
- P1-V02: the local architecture, static contract and threat remediation is complete and locally checked. Actual accountable people, independent security/architecture review, likelihood/impact/residual-risk disposition and reviewer record remain pending. Static contracts do not prove runtime authorization, RLS, audit durability or executor behavior.
- P1-V03: local verifier and tests pass. A fresh GitHub Actions result on an immutable candidate, active default-branch rule inspection and evidence that a deliberately failing PR is blocked remain pending. Historical Actions runs are not current-candidate enforcement evidence.
- P1-V04: no immutable final candidate or authorized human phase-exit decision is recorded. P1 remains Pending review, and P2 has not begun.
