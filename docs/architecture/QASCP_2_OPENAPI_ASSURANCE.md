# QASCP 2.0 — Full OpenAPI assurance and bounded reference policy

Status: proposed P1 verification/adoption package, 2026-11-16 (Qatar). Canonical V2-P1-02 / P1-V02 with P1-V03 CI evidence. No application feature, database, customer connector or production authority is delivered. Independent reviewer and tool-adoption approval remain pending.

Requirements: PRD-01, PRD-02, PRD-10; QASCP-GOV-002..004, QASCP-SEC-004, QASCP-ENG-001..003. Affected earlier paths: both versioned OpenAPI contracts, existing JSON Schema validators, dependency closure, full unit suite and CI acceptance. Acceptance: both actual OpenAPI documents pass the dedicated OpenAPI 3.1 validator, representative invalid specifications fail, local reference policy rejects remote/out-of-root retrieval, and the full cumulative suite passes against the candidate.

## What is added

[verify_openapi_contracts.py](../../scripts/verify_openapi_contracts.py) invokes OpenAPIV31SpecValidator from openapi-spec-validator 0.7.2 on:
- contracts/qascp-2/openapi.json (the preserved original proposal).
- contracts/qascp-2/graph/openapi-0.2.json (the graph-boundary successor proposal).

This is dedicated OpenAPI document/schema/semantic validation implemented by that pinned library, not only JSON parsing, local-pointer resolution or QASCP's custom structural assertions. Its exact library coverage and version remain part of the evidence; it is not a proof that an API implementation conforms to the contract.

The existing JSON Schema and graph conformance checks remain in place. New [OpenAPI regressions](../../tests/test_openapi_contracts.py) test both specifications, missing info, invalid response status, unresolved path parameters, duplicate operation IDs and explicit version selection, plus reference boundary failures. Required checks fail rather than skip when a validator is missing.

## Local JSON reference boundary

Before invoking the library, the verifier recursively checks all $ref, $dynamicRef and $recursiveRef values across referenced JSON documents. It permits only relative/local JSON Pointer references, resolves symlinks/encoded paths, and keeps every loaded file under the resolved contracts directory. Non-string references, remote/absolute URI references, query strings, invalid JSON Pointer escapes, unsupported named anchors and missing files/pointers fail.

The validator's resolver_handlers are replaced with a bounded file-only handler, not augmented with default network handlers. The reader accepts only file URIs with no host/query, a resolved path inside contracts and a .json extension. It uses JSON parsing, not an arbitrary YAML deserializer. No HTTP(S), UNC/network host, all-URL fallback or outside-root file reader is provided.

The two contract versions currently use relative files and JSON Pointers; introducing named/dynamic anchors or another reference format requires an explicit verifier-policy review rather than silently enabling retrieval. This restriction governs static repository verification, not customer evidence retrieval.

The tests prohibit socket connection creation and urllib URL opening during full validation, in addition to malformed-reference cases. This covers the exercised validator paths; it is not an operating-system egress firewall or a universal proof about all third-party code.

## Proposed adoption record: ADR-2-OPENAPI-VALIDATION-001

Problem: the project previously had JSON Schema meta-schema tests and custom API structural/reference tests but no dedicated full OpenAPI validation result. Choose an isolated development/CI validator rather than claiming those narrower checks cover the whole specification.

Primary sources consulted: [validator 0.7.2 dependency manifest](https://github.com/python-openapi/openapi-spec-validator/blob/0.7.2/pyproject.toml), [its validator interface](https://github.com/python-openapi/openapi-spec-validator/blob/0.7.2/openapi_spec_validator/validation/validators.py), [Python usage documentation](https://openapi-spec-validator.readthedocs.io/en/latest/python.html), [schema-validator dependency manifest](https://github.com/python-openapi/openapi-schema-validator/blob/0.6.3/pyproject.toml) and [jsonschema-path dependency manifest](https://github.com/p1c2u/jsonschema-path/blob/0.3.4/pyproject.toml).

No upstream implementation is copied into QASCP. The wrapper/tests are original QASCP verification code using the documented library interface. This is a proposed development-tool adoption; independent provenance, license, maintenance and vulnerability review remains required before acceptance.

| Package/version change | Role / declared license / source |
|---|---|
| openapi-spec-validator 0.7.2 | Full OpenAPI validator; Apache-2.0; [PyPI](https://pypi.org/project/openapi-spec-validator/0.7.2/) |
| openapi-schema-validator 0.6.3 | OpenAPI Schema Object rules; BSD-3-Clause; [PyPI](https://pypi.org/project/openapi-schema-validator/0.6.3/) |
| jsonschema-path 0.3.4 | Local schema-path resolution; Apache-2.0; [manifest](https://github.com/p1c2u/jsonschema-path/blob/0.3.4/pyproject.toml) |
| pathable 0.4.4 | Path abstraction; Apache-2.0; [PyPI](https://pypi.org/project/pathable/0.4.4/) |
| PyYAML 6.0.3 | Declared upstream parser dependency; MIT; [PyPI](https://pypi.org/project/PyYAML/6.0.3/) |
| lazy-object-proxy 1.12.0 | Declared upstream proxy dependency; BSD-2-Clause; [PyPI](https://pypi.org/project/lazy-object-proxy/1.12.0/) |
| requests 2.34.2 | Published jsonschema-path wheel dependency; Apache-2.0; [manifest](https://github.com/psf/requests/blob/v2.34.2/pyproject.toml) |
| charset-normalizer 3.5.2 | requests encoding dependency; MIT; [PyPI](https://pypi.org/project/charset-normalizer/3.5.2/) |
| idna 3.20 | requests hostname dependency; BSD-3-Clause; [PyPI](https://pypi.org/project/idna/3.20/) |
| urllib3 2.8.0 | requests transport dependency; MIT; [PyPI](https://pypi.org/project/urllib3/2.8.0/) |
| certifi 2026.10.23 | requests trust-store dependency; MPL-2.0; [PyPI](https://pypi.org/project/certifi/2026.10.23/) |
| referencing 0.36.2 replaces 0.37.0 | jsonschema-path 0.3.4 requires referencing <0.37.0; [PyPI](https://pypi.org/project/referencing/0.36.2/), MIT. jsonschema 4.26.0 permits >=0.28.4, so this pin satisfies both declared constraints. |

The published jsonschema-path 0.3.4 wheel declares requests as required: the first CI attempt exposed its omission through pip check. The source-manifest optional declaration was insufficient evidence for the wheel dependency closure. requests and its four dependencies are therefore explicitly pinned; neither installing nor omitting an HTTP library enforces offline operation. The file-only resolver and reference preflight enforce the exercised boundary, with socket, urllib and requests calls prohibited in the full-document regression. The project does not use the upstream YAML parser on repository contracts. Other existing validator pins remain unchanged.

CI retains the isolated virtual environment and installs the explicit 19-package closure from requirements-contracts.txt with --no-deps and --only-binary=:all:, runs pip check, then the new standalone verifier and the complete unit suite. There is no unpinned resolver or source-build fallback. Wheel artifact hashes are not locked by this change and independent supply-chain review remains pending. Nothing here is a runtime dependency adoption or vulnerability-free claim.

## CI checkout maintenance candidate

[ADR-2-CI-001](QASCP_2_CI_CHECKOUT_DECISION.md) records the proposed full-SHA
Node24 checkout update and post-checkout local-auth configuration check.
It preserves the read-only token, all validators and the required gate identity.
Fresh candidate CI and independent review are required; older runs retain their
original action version and evidence scope.

## Limits and reviewer handoff

The [2026-11-25 review](../verification/QASCP_2_P1_REVIEW_2026-11-25.md)
adds one shared [QASCP policy checker](../../scripts/verify_openapi_policy.py)
to the standalone batch for both preserved API versions. Each decoded document
must pass the full specification validator and the shared authentication,
tenant-selector and operation policy; successor graph tests reuse that policy.
The lower-level validate_document remains specification-only so regressions can
demonstrate the difference. Six dependency-free tests do not replace the real
validator or cumulative suite. The code candidate passed both actual full
validators and 96 tests in Actions 45674623799; PR #36 binds the final evidence
update to its own fresh cumulative result.

Passing this check can close the previously missing dedicated OpenAPI-validation evidence for the exact candidate. It cannot approve the contract's security design, choose its product semantics, certify regulatory applicability, prove tenant isolation or satisfy the human phase-exit decision. Keep the custom QASCP security/structural tests, synthetic conformance tests and later real-entry-point verification.

The [consolidated P1 review package](../verification/QASCP_2_P1_REVIEW_PACKAGE.md) retains substantive bilingual/regulatory review, independent security/architecture dispositions, verified main merge enforcement and formal P1 acceptance as separate requirements. No phase decision or branch setting is changed.

## Preparation evidence

Base main 16a47ee45bbe521a04a6234ebd6304b4ec0da5c2, tree 5be7a70db3eabcfcbbc836ce42f421e3081dc54b. Prepared as one isolated package after merged PR #10, preserving unrelated shared-workspace changes. Local Windows/Python 3.14.4 lacks the validation dependencies and retains the symlink privilege limit. Local structural checks and the exact candidate's Linux full-validator/unit results are recorded in the PR; earlier candidate checks are not silently reused.

A failure in dependency compatibility, document validity or reference handling must be corrected and rerun. Do not record this verification gap as resolved until the fresh candidate check actually passes.

Initial candidate 2e9ef6c57f4131eb36ab9124ecd3ae8c463c3fd3 failed [run 43935055382](https://github.com/ManeaAl-Shabrain/QASCP/actions/runs/43935055382): installation succeeded but pip check reported missing requests. Full OpenAPI validation and unit tests were skipped, and the gate failed. The revised closure corrects the cause; fresh results must be bound to the replacement candidate in the PR.

Local preparation: nine-file UTF-8/newline/whitespace, Python AST and Markdown local-link checks passed; foundation verifier exited 0. Full Windows unittest discovery exited 1 with 21 entries: 16 passed, four missing-validator import errors and the existing WinError 1314 symlink error; no skips. New OpenAPI validation was not represented as locally passed. The candidate requires the existing isolated Linux CI flow with its updated explicit dependency closure.


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
