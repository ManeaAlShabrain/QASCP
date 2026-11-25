# Reproduce P1 validation — QAR-006 / QAR-008

Requirements: ENG-001/002/003, GOV-003; P1-V01/03; Issue #42.
P1 checks static design and verification tooling; no application installation exists.

## Supported full-check environment

Linux x86_64, CPython **3.14** with venv/pip, Git, UTF-8 filesystem and symbolic
links. The actual baseline hosted environment is Ubuntu 26.04.1 / Python 3.14.4;
the runner image/kernel/compiler vary and must be retained from each run. Only
that platform/ABI's 19 wheel artifacts are in the hash lock. Other Python/CPU/OS
combinations require their own reviewed lock and full evidence. No Python 3.12,
3.13, Windows or ARM full-suite success is asserted. Hosted ubuntu-latest changes;
the version/platform assertion intentionally fails if it no longer matches.

Use a new checkout of the immutable candidate and an absent .venv-contracts.
Do not reuse a populated environment as proof of a clean install. Run from the
repository root in a POSIX shell:

```sh
python3 --version
git --version
python3 -c 'import platform, sys; assert sys.version_info[:2] == (3, 14) and sys.platform == "linux" and platform.machine() == "x86_64", "Unsupported validation lock platform"'
python3 scripts/verify_checkout_auth.py
python3 scripts/verify_foundation.py
python3 scripts/verify_validation_lock.py
python3 -m venv .venv-contracts
.venv-contracts/bin/python -m pip install --disable-pip-version-check --no-input --index-url https://pypi.org/simple --no-deps --only-binary=:all: --require-hashes -r requirements-contracts-linux-cp314.lock
.venv-contracts/bin/python -m pip check
.venv-contracts/bin/python scripts/verify_openapi_contracts.py
.venv-contracts/bin/python -m unittest discover -s tests -v
```

JSON Schema meta-schema/instance validation with explicit format checks is in
the full suite. The dedicated OpenAPI command validates both complete documents
and their bounded local references plus QASCP policy; no network resolution is
allowed for specification references. Foundation checks structure/local paths,
not substantive bilingual equivalence or human approval. pip check checks
dependency consistency; it does not scan vulnerabilities.

CI additionally runs this actual integrity/advisory lookup:

```sh
.venv-contracts/bin/python -m pip download --disable-pip-version-check --no-input --index-url https://pypi.org/simple --no-deps --only-binary=:all: --require-hashes -r requirements-contracts-linux-cp314.lock --dest .validation-wheels
.venv-contracts/bin/python scripts/capture_validation_dependencies.py
```

This requires PyPI network access; it compares downloaded SHA-256 to official
release JSON and reports that source's advisory entries. It is a bounded SCA
input, not complete vulnerability, license or supply-chain certification. Network
failure fails the step; do not replace it with an empty result. See
[captured artifact provenance](remediation/P1-2026-11-25/dependency-evidence.json).

## Windows investigation

The original audit recorded five missing dependency test-module imports and one
WinError 1314 creating a symbolic link, not six application assertion failures.
The 31 discovery entries were not the full 96-test denominator. Those original
[outputs](https://github.com/ManeaAlShabrain/QASCP/blob/cc04fa6e82f0b53d75fd5d08e1a36f11fba5c4d2/docs/verification/reviews/P1/2026-11-25-4592eb230fad/evidence/local-results.json) remain intact.
Native Windows needs both the pinned validators and permission to create symbolic
links (Developer Mode or an appropriately permitted process, according to local
policy). This task does not alter machine privileges. The Linux wheel lock
intentionally cannot install Windows native wheels. Use matching Linux/WSL or a
separately reviewed Windows wheel lock and preserve the actual result. No test
has been disabled or skipped to obtain a pass.

For dependency-free Windows preparation:

```powershell
python -B scripts/verify_foundation.py
python -B -m unittest discover -s tests -p test_checkout_auth.py -v
```

These commands are a subset, not full P1 validation. A guard run on a developer
checkout can legitimately reject a local include/helper; do not remove personal
authentication settings automatically. The CI checkout has a stricter ephemeral
local-authentication boundary. For full local discovery, retain all errors and
skips. Fresh candidate Linux results must be linked separately from local failures.
