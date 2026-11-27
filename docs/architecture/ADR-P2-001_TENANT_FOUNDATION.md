# ADR-P2-001 — Authenticated tenant foundation and controlled input adoption

Date2026-11-27. PhaseP2/V2-P2-01; P2-V01/02; PRD-01/08/10,
GOV-001..004, SEC-001..005, ENG-001..003. Prior approval:
[P1-EXIT-001](../governance/decisions/P1-EXIT-001-APPROVAL.md).
Status: IMPLEMENTATION DECISION / CURRENT-INPUT DISCOVERY BEFORE INSTALLATION.
No package or P2 phase acceptance is claimed by preparing this ADR.

## Scope and interfaces

Build the first modular FastAPI service and tenant PostgreSQL foundation.
The accepted P1 four-operation business contract stays byte-preserved until
its dependent packages are implemented. Add a separately versioned foundation
contract for GET /api/v2/tenancy/current and isolated GET /live; no asset,
observation, graph or production-action endpoint is stubbed or falsely shipped.
The former returns the currently authorized tenant profile, and records actual
access audit evidence. Liveness returns process state without any tenant query.
No public auto-doc/config/debug surface or synthetic runtime fallback is enabled.

## Security choices

- OIDC discovery/JWKS only from operator-configured HTTPS issuer and its exact
  allowed origin, TLS verified; no token-supplied URL or redirect. RS256-only
  bounded RSA keys, explicit issuer/audience/expiry/issuance/subject validation,
  human MFA claim and current server-owned membership/permission required.
  Bounded cached keys and rate-limited unknown-key refresh are explicit; key
  revocation lag is bounded by cache expiry, not falsely claimed instantaneous.
- Per-tenant nonowner/non-superuser/non-BYPASSRLS database login and bounded
  connection pool for the two-tenant lab. A SECURITY DEFINER metadata function
  derives the fixed tenant binding from SESSION_USER, has a fixed search path
  and no tenant-table grants. Policies require BOTH role binding and transaction
  tenant context. Forging SET qascp.tenant_id alone cannot switch tenants.
- Shared application role plus freely writable tenant GUC was rejected as the
  sole database authority because stolen/raw SQL access could forge that GUC.
  Per-tenant roles add credentials/pool management overhead; no enterprise
  scale claim. A later pooled-capability design needs separate review/tests.
- Tenant profile, membership, composite references and append-only access audit
  use FORCE RLS. Sensitive required audit failure rolls back the operation;
  runtime roles cannot update/delete audit, migrate, create roles or assume
  another tenant role. Metadata management has no tenant-record access.
- Schema migrations are checksum-versioned, transactionally applied under an
  advisory lock, using distinct operator/migrator credentials. Runtime startup
  does not migrate, seed users or create tenant roles. Synthetic identities,
  TLS/signing keys and fixtures belong only in the integration test harness.

## Dependency alternatives, provenance and adoption boundary

FastAPI and PostgreSQL are already conceptually selected by the accepted P1
design. Psycopg3/pool is selected over a new ORM or handwritten database driver:
parameter binding, transactions and pool lifecycle are explicit, with fewer
layers to obscure role/context tests. PyJWT plus cryptography is selected over
handwritten JWT/RSA verification. Uvicorn serves ASGI; HTTPX is test-only.
No external application source or example keys are copied.

Current direct-version candidates are discovered from official PyPI metadata;
known reference releases include FastAPI0.165.0, PyJWT2.15.1, psycopg3.3.9 and
pool3.3.3. PostgreSQL18.7 is the supported18minor observed at the official
versioning table. Discovery resolves exact LinuxCP314 wheels, transitive versions,
published hashes, yanked/advisory state and embedded licence-file identities
WITHOUT installing or executing those wheels. Official Docker manifests resolve
the exact linux/amd64 PostgreSQL image digest. Only after reviewing that receipt
are exact locks/image adopted and installed for synthetic validation.

Licence families are not flattened: Psycopg/pool LGPL-3.0-only; crypto
Apache-2.0 OR BSD-3-Clause; API/JWT/server/test tools use their declared licences.
Unmodified separately installed libraries retain upstream licence material.
No third-party binary bundle, modification, customer redistribution or legal
clearance is authorized. Unknown/conflicting rights or active advisories block
the affected adoption. Actual deployment/distribution licence/NOTICE/source
duties require their own rights review and artifact inventory before that use.

## Primary references actually consulted

- https://pypi.org/project/fastapi/ — observed0.165.0/CPython3.14.
- https://pypi.org/project/PyJWT/ and https://pyjwt.readthedocs.io/en/stable/api.html
- https://pypi.org/project/psycopg/ and https://pypi.org/project/psycopg-pool/
- https://github.com/psycopg/psycopg/blob/3.3.9/LICENSE.txt
- https://www.psycopg.org/psycopg3/docs/advanced/pool.html — versioned release
  behavior must be checked; live docs currently identify a development version.
- https://www.postgresql.org/support/versioning/
- https://www.postgresql.org/docs/18/ddl-rowsecurity.html
- https://openid.net/specs/openid-connect-discovery-1_0.html
- https://github.com/docker-library/official-images/blob/master/library/postgres

Local Windows has no docker/psql and direct PyPI egress failed with URLError.
Supported hosted Linux validation will run the actual database/network tests;
no local DB or dependency-enabled execution is fabricated.

## Acceptance

Verify real signed-token/discovery/TLS allow/deny cases; live HTTP/ASGI entry
points with real PostgreSQL; two tenants with repeated identifiers; non-bypass
roles, forged GUC/SET ROLE/ownership/FK denial; sequential/concurrent pool reuse;
current membership revocation; audit tamper/outage; clean/idempotent/drift-rejected
migration and actual installed artifact without test fallback. Run all115P1
regressions and current full contract checks. Retain all failures/limits and
separate security/architecture review before accepting the package. P2 exit
still requires the later packages and actual phase decision.

## ملخص القرار

بدأت P2 بعد اعتماد P1 الحقيقي. تُبنى مؤسسة التطبيق والتحقق الفعلي من OIDC
وقاعدة PostgreSQL بأدوار منفصلة لكل مؤسسة في المختبر، وسياسات صفوف تربط
صلاحية الاتصال بالمؤسسة وسياق المعاملة معًا. لا تكفي قيمة GUC قابلة للتغيير
وحدها لمنح الوصول. تبقى فحوص الحياة معزولة، والهويات والمفاتيح الاصطناعية
داخل الاختبارات، وأدلة التدقيق ذرية ومحمية من تعديل دور التشغيل.
تُراجع الإصدارات والبصمات والتراخيص قبل التثبيت، ولا يُدعى نشر إنتاجي أو
فحص لم يُنفّذ. قبول الحزمة وقرار خروج P2 يظلان منفصلين عن بدء تنفيذها.
