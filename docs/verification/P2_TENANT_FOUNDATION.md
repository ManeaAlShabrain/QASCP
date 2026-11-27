# V2-P2-01 - Tenant foundation implementation and validation

2026-11-27. Internal synthetic development only. PR #50; active phase P2.
PRD-01/08/10; GOV-001..004; SEC-001..005; ENG-001..003; P2-V01/02.
Implementation is not package acceptance or P2 exit. P2-02..06 remain separate.

## Implemented boundary

The installable `qascp-foundation` wheel exposes process-only `/live` and
`GET /api/v2/tenancy/current`. The latter requires one Bearer access token with
`typ=at+jwt`, RS256, exact configured issuer/API audience, valid integer dates,
lifetime at most3600s, subject and trusted issuer `amr` containing `mfa`.
Clock leeway30s; key cache60s; unknown-key refresh limited5s. This is an explicit
issuer integration profile: an issuer must truthfully attest MFA for that API
access token. Browser ID tokens are rejected. TLS discovery/JWKS stays on the
configured origin, with no redirects, proxies or token-supplied URLs.

The selector is a canonical UUID. Server-owned issuer+subject membership,
active status, human actor type and `tenancy:read` permission determine access;
token role/tenant claims grant no authority. Membership is locked through
`qascp.lock_membership` until profile read and required audit commit. This
separate definer belongs to the tenant-table owner under FORCE RLS; the metadata
definer belongs to a distinct NOLOGIN metadata-only principal. Both fix their
search path and evaluate the original SESSION_USER. Runtime receives no UPDATE
grant merely to lock membership. Revocation commits before a subsequent request
and invalidates that request even if the JWT is still valid.

Per-tenant logins have no role memberships, table ownership, BYPASSRLS,
superuser, role/database creation, replication, TEMP or schema-create privileges.
FORCE RLS requires fixed SESSION_USER binding AND transaction-local tenant GUC.
Composite audit-to-membership keys prevent cross-tenant actor references.
Runtime may only read profile/membership, invoke the constrained lookup and
insert same-tenant audit. It cannot read/update/delete/truncate audit or mutate
membership. Pool count is configured (max16tenants), max4connections/tenant,
max32waiters,3s acquisition/connect timeout. Transactions bound statement/lock/
idle timeouts; rollback/reset precedes reuse. TLS database connections require
verify-full and a configured root CA.

Append-only storage is not cryptographic nonrepudiation: stolen tenant DB
credentials can fabricate same-tenant inserts/attribution. RLS limits that login
to its tenant; whole service compromise can expose all configured credentials.
The internal risk holds remain. No customer/production access, deployment,
enterprise-scale pool claim, operational backup/retention acceptance or regulatory
approval is provided by this package. Later tamper-evident custody and operational
recovery need their own tests/authorization.

## Controlled inputs

[Exact receipt](p2-input-receipt.json) records official PyPI URLs, downloaded
wheel hashes, transitive versions, licence-file hashes, native library filenames,
advisory state and PostgreSQL linux/amd64 manifest digest. Discovery initially
[failed](https://github.com/ManeaAlShabrain/QASCP/actions/runs/46029667723)
on setuptools' legitimate nested vendored METADATA; the parser now selects only
the root distribution. The subsequent receipt run46030614878 succeeded without
installing/executing the downloaded wheels. Receipt review precedes installation.

Declared families reviewed for unmodified internal installation: MIT/MIT-0,
BSD-2/3, Apache2, PSF2, test-only certifiMPL2, Psycopg/poolLGPL3. Retain upstream
notices. No library is modified/rebundled in the QASCP wheel; no customer binary
redistribution or legal clearance is asserted. Bundled native components are
identified but their full component/NOTICE/patch provenance is not exhaustively
established by Python package metadata. That limitation remains explicit before
any deployment/distribution acceptance.

Build backend setuptools84.2.1/wheel0.48.0 and build1.6.1 closure are hash locked.
Trivy0.76.2 is an unmodified Apache2-licensed CI tool from the official release,
archive SHA256bc0fc726e017b8927a62b2d3531d7a84ee01769daf5c99ed866dced54089fdbf
as reported by GitHub release metadata. The official upload-artifactv7.0.2 action
is pinnedcf430e030ddbb5b0abf93d22962f4752f3646cd9; checkout pin is retained.
Runner image, scanner vulnerability DB and external advisory state are observed
dynamic inputs, not falsely claimed frozen/reproducible across dates.

## Supported clean validation

Linux x86_64, CPython3.14, Docker daemon and HTTPS egress to official PyPI,
GitHub/Docker registries and scanner advisory databases. Windows is not a
supported runtime validation host; local checks cannot replace this job.

```sh
python3 -m venv .venv-p2-build
.venv-p2-build/bin/python -m pip install --isolated --no-deps --only-binary=:all: --require-hashes -r requirements-p2-build-linux-cp314.lock
.venv-p2-build/bin/python -m pip check
python3 -m venv .venv-p2
.venv-p2/bin/python -m pip install --isolated --no-deps --only-binary=:all: --require-hashes -r requirements-p2-test-linux-cp314.lock
export SOURCE_DATE_EPOCH=1795737600
.venv-p2-build/bin/python -m build --wheel --no-isolation --outdir .p2-dist
.venv-p2-build/bin/python -m build --wheel --no-isolation --outdir .p2-dist-repeat
cmp .p2-dist/*.whl .p2-dist-repeat/*.whl
.venv-p2/bin/python -m pip install --isolated --no-deps --no-index .p2-dist/*.whl
.venv-p2/bin/python -m pip check
.venv-p2/bin/python scripts/verify_p2_inputs.py
.venv-p2/bin/python -m unittest discover -s integration_tests -v
```

The harness generates ephemeral CA/TLS/signing keys and random credentials,
starts the exact PostgreSQL image in a disposable loopback-only container,
bootstraps distinct roles, applies migrations, provisions two synthetic tenants
with repeated subject/actor IDs, and starts the installed wheel's HTTPS entry
point in isolated Python outside the source directory. Fixtures never enter the
installed artifact. Initial-schema installation/idempotence/drift rejection are
tested; no upgrade from a nonexistent prior runtime release is claimed.

CI additionally runs all P1 validators/regressions, full foundation OpenAPI
validation, two builds/byte comparison, installed-version checks, CycloneDX SBOM,
actual Python-SBOM and image vulnerability scans. High/Critical scan findings or
scanner errors block the gate. Retained wheel/SBOM/scan artifacts expire after
30days on GitHub; download/retain the acceptance candidate before expiry.
No scanner's coverage is exhaustive. Unexecuted checks remain pending, and
failed iterations remain in Actions history.

## Explicit operator paths

Bootstrap is a one-time DBA action on a new authorized database, through
`scripts/p2_operator.py bootstrap` with a private0600JSON file selected by
QASCP_OPERATOR_FILE containing `admin_dsn` and `migrator_password`. Bootstrap
creates NOLOGIN owners and a dedicated non-superuser migrator, revokes public
database CONNECT/TEMP/CREATE and schema CREATE; it deliberately fails on a
preexisting conflicting role/database state. It is not an idempotent upgrade.

Run `qascp-migrate` with QASCP_MIGRATION_DSN for qascp_migrator only. The migrator
can alter schema through owner membership; it has no tenant login binding, so
FORCE RLS denies tenant reads. This DDL authority is operator-only and must never
be mounted in the service. Migrations use one transaction/advisory lock and
refuse checksum/history drift. Restore from backup is outside this first package.

Provision through `scripts/p2_operator.py provision`, using that private operator
file with `admin_dsn` and a `tenant` object containing canonical `tenant`, random
`password`, `display_name`, exact `issuer`, `subject` and canonical `actor`.
It atomically creates a new role, immutable tenant binding, profile and initial
human membership. Existing/conflicting identities fail; no runtime seed path.
The privileged operator must validate authorized owner identity/MFA issuer profile
before provisioning. No sample credentials or automatic admin membership exist.

Runtime configuration: QASCP_OIDC_ISSUER, QASCP_OIDC_AUDIENCE, optional
QASCP_OIDC_CA_FILE; private0600QASCP_TENANT_CONNECTIONS_FILE mapping tenant UUID
to DSN. Every DSN must explicitly supply only host,port,dbname,user,password,
sslmode=verify-full,sslrootcert,connect_timeout=3. The login must equal
qascp_t_ followed by the tenant's32hex digits. No PG service/options injection.
Set QASCP_TLS_CERT, QASCP_TLS_KEY, optional QASCP_PORT(default8443); qascp-serve
binds127.0.0.1, disables request access logs/proxy-header trust/docs/debug.
External exposure/load balancing and deployment topology are not accepted here.

## ملخص التنفيذ وحدوده

بدأت P2 بموافقة موثقة على P1 للتطوير الداخلي فقط. تتطلب قراءة المؤسسة الحالية
رمز وصول موقّعًا لجمهور API المحدد، وإثبات MFA من مُصدر الهوية الموثوق، وعضوية
بشرية نشطة وصلاحية محفوظة في الخادم. تُربط هوية دخول قاعدة البيانات بمؤسسة ثابتة
وسياق المعاملة معًا؛ تغيير محدد المؤسسة وحده لا يمنح الوصول. يكتمل تسجيل التدقيق
قبل إعادة النجاح، وفشله يمنع النجاح. مفاتيح الاختبار والبيانات الاصطناعية تبقى
خارج الحزمة المثبتة. صلاحية DDL منفصلة عن حسابات التشغيل. لا يثبت التخزين الإلحاقي
وحده صحة الإسناد عند سرقة بيانات دخول المؤسسة. قبول هذه الحزمة وخروج P2 وموافقة
الإنتاج والجهة التنظيمية قرارات مستقلة؛ ولا يُدعى نجاح أي اختبار قبل تنفيذه.
