"""Live HTTPS/OIDC/PostgreSQL tests against the installed QASCP wheel."""

import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
from importlib.resources import files
import json
import os
from pathlib import Path
import subprocess
import time
import unittest
from uuid import uuid4

import jwt
from jwt.algorithms import RSAAlgorithm
from cryptography.hazmat.primitives.asymmetric import rsa
import jsonschema
import psycopg
from psycopg import sql

import qascp
from qascp.config import Settings
from qascp.database import Tenancy
from qascp.identity import IdentityError, OIDC
from qascp.migrate import migrate
from support import ACTOR, Lab, ROOT, TENANTS


class TenantFoundation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lab = Lab.__new__(Lab)
        cls.addClassCleanup(cls.lab.close)
        cls.lab.__init__()
        cls.schema = json.loads((ROOT/"contracts/p2/foundation-openapi-0.1.json").read_text())

    def admin(self, statement, params=()):
        with psycopg.connect(self.lab.admin) as conn:
            cursor = conn.execute(statement, params)
            return cursor.fetchall() if cursor.description else []

    def oidc(self):
        return OIDC(self.lab.issuer.url, "qascp-api", str(self.lab.folder/"ca.crt"))

    def test_01_real_https_two_tenants_and_persisted_contract_audit(self):
        for index, tenant in enumerate(TENANTS):
            response = self.lab.request(tenant)
            self.assertEqual(response.status_code, 200, response.text)
            body = response.json()
            jsonschema.Draft202012Validator(self.schema["components"]["schemas"]["CurrentTenant"],
                                            format_checker=jsonschema.FormatChecker()).validate(body)
            self.assertEqual(body["tenant_id"], tenant)
            self.assertEqual(body["display_name"], "Synthetic Tenant "+str(index))
            self.assertEqual(body["actor_id"], ACTOR)
            self.assertEqual(response.headers["cache-control"], "no-store")
            row = self.admin("SELECT tenant_id::text, actor_id::text, outcome, schema_version FROM qascp.access_audit WHERE correlation_id=%s", (body["correlation_id"],))
            self.assertEqual(row, [(tenant, ACTOR, "succeeded", "1.0")])

    def test_02_authentication_invalid_tokens_leave_no_audit(self):
        before = self.admin("SELECT count(*) FROM qascp.access_audit")[0][0]
        now = int(time.time())
        cases = ["invalid", self.lab.issuer.token(iss="https://other.invalid"), self.lab.issuer.token(aud="other"),
                 self.lab.issuer.token(exp=now-60, iat=now-360), self.lab.issuer.token(iat=now+100, exp=now+400),
                 self.lab.issuer.token(nbf=now+100), self.lab.issuer.token(amr=["pwd"]),
                 self.lab.issuer.token(exp=True), self.lab.issuer.token(exp=now+7200), self.lab.issuer.token(sub=""),
                 self.lab.issuer.token(nbf="tomorrow"), "x"*16385]
        claims = {"iss": self.lab.issuer.url, "aud": "qascp-api", "sub": "same-subject", "iat": now, "exp": now+300, "amr": ["mfa"]}
        cases += [jwt.encode(claims, "synthetic-nonsecret-hmac-input-32-bytes", algorithm="HS256", headers={"kid": "initial", "typ": "at+jwt"}),
                  jwt.encode(claims, self.lab.issuer.key, algorithm="RS256", headers={"kid": "initial", "typ": "JWT"}),
                  jwt.encode(claims, self.lab.issuer.key, algorithm="RS256", headers={"kid": "initial", "typ": "at+jwt", "jku": self.lab.issuer.url+"/jwks"})]
        for token in cases:
            with self.subTest(length=len(token)):
                result = self.lab.request(token=token)
                self.assertEqual(result.status_code, 401)
                self.assertNotIn(token[:40], result.text)
        self.assertEqual(self.admin("SELECT count(*) FROM qascp.access_audit")[0][0], before)
        self.assertEqual(self.lab.client.get("/api/v2/tenancy/current").status_code, 401)

    def test_03_selectors_and_identity_not_token_roles(self):
        self.assertEqual(self.lab.request(str(uuid4())).status_code, 403)
        self.assertEqual(self.lab.request("malformed").status_code, 400)
        self.assertEqual(self.lab.request(headers={"X-Tenant-ID": ""}).status_code, 400)
        self.assertEqual(self.lab.request(params={"tenant_id": TENANTS[1]}).status_code, 400)
        # Tenant and role claims cannot override current server-owned membership.
        self.assertEqual(self.lab.request(token=self.lab.issuer.token(sub="unregistered", roles=["admin"], tenant_id=TENANTS[0])).status_code, 403)
        self.assertEqual(self.lab.request(token=self.lab.issuer.token(roles=["admin"], tenant_id=TENANTS[1])).json()["tenant_id"], TENANTS[0])

    def test_04_revocation_permission_and_workload_separation(self):
        token = self.lab.issuer.token()
        for updates in ("active=false", "permissions=ARRAY[]::text[]", "actor_type='workload'"):
            try:
                self.admin("UPDATE qascp.membership SET "+updates+", authorization_version=authorization_version+1 WHERE tenant_id=%s", (TENANTS[0],))
                self.assertEqual(self.lab.request(token=token).status_code, 403)
            finally:
                self.admin("UPDATE qascp.membership SET active=true, permissions=ARRAY['tenancy:read'], actor_type='user', authorization_version=authorization_version+1 WHERE tenant_id=%s", (TENANTS[0],))
        self.assertEqual(self.lab.request(token=token).status_code, 200)

    def test_05_rls_missing_and_forged_context_joins_same_actor(self):
        with psycopg.connect(self.lab.connections[TENANTS[0]], autocommit=True) as conn:
            self.assertEqual(conn.execute("SELECT count(*) FROM qascp.tenant_profile").fetchone()[0], 0)
            for tenant, expected in ((TENANTS[1], 0), (TENANTS[0], 1)):
                with conn.transaction():
                    conn.execute("SELECT set_config('qascp.tenant_id',%s,true)", (tenant,))
                    self.assertEqual(conn.execute("SELECT count(*) FROM qascp.tenant_profile").fetchone()[0], expected)
                    rows = conn.execute("SELECT p.tenant_id::text,m.actor_id::text FROM qascp.tenant_profile p JOIN qascp.membership m USING(tenant_id)").fetchall()
                    self.assertEqual(rows, [(TENANTS[0], ACTOR)] if expected else [])

    def test_06_no_role_escalation_ddl_temporary_shadow_or_audit_mutation(self):
        with psycopg.connect(self.lab.connections[TENANTS[0]], autocommit=True) as conn:
            prohibited = ["SET ROLE qascp_owner", "SET ROLE qascp_metadata", "SET ROLE qascp_migrator",
                          "SET ROLE qascp_t_"+TENANTS[1].replace("-", ""), "SET SESSION AUTHORIZATION postgres",
                          "CREATE TEMP TABLE role_tenant(x int)", "CREATE TABLE public.unauthorized(x int)",
                          "SELECT * FROM qascp_meta.role_tenant", "SELECT * FROM qascp.access_audit",
                          "UPDATE qascp.membership SET active=true", "DELETE FROM qascp.access_audit",
                          "TRUNCATE qascp.access_audit", "ALTER TABLE qascp.membership DISABLE ROW LEVEL SECURITY",
                          "CREATE ROLE unauthorized"]
            for statement in prohibited:
                with self.subTest(statement=statement), self.assertRaises(psycopg.Error):
                    conn.execute(statement)

    def test_07_cross_tenant_composite_foreign_key_and_audit_insert_policy(self):
        actor_b = str(uuid4())
        self.admin("INSERT INTO qascp.membership VALUES (%s,%s,%s,'only-b','user',true,1,ARRAY['tenancy:read'])", (TENANTS[1], actor_b, self.lab.issuer.url))
        try:
            with psycopg.connect(self.lab.connections[TENANTS[0]], autocommit=True) as conn:
                for target, actor in ((TENANTS[1], ACTOR), (TENANTS[0], actor_b)):
                    with self.subTest(target=target, actor=actor), self.assertRaises(psycopg.Error):
                        with conn.transaction():
                            conn.execute("SELECT set_config('qascp.tenant_id',%s,true)", (TENANTS[0],))
                            conn.execute("INSERT INTO qascp.access_audit VALUES (%s,%s,'1.0',%s,'user','1','tenancy.read','tenant',%s,'succeeded',now(),%s)", (target, str(uuid4()), actor, target, str(uuid4())))
        finally:
            self.admin("DELETE FROM qascp.membership WHERE tenant_id=%s AND actor_id=%s", (TENANTS[1], actor_b))

    def test_08_sequential_concurrent_pool_reuse_and_reset(self):
        for index in range(12):
            tenant = TENANTS[index%2]
            self.assertEqual(self.lab.request(tenant).json()["tenant_id"], tenant)
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(lambda i: (TENANTS[i%2], self.lab.request(TENANTS[i%2])), range(24)))
        for tenant, response in results:
            self.assertEqual(response.status_code, 200, response.text)
            self.assertEqual(response.json()["tenant_id"], tenant)
        tenancy = Tenancy(self.lab.connections)
        tenancy.open()
        try:
            pool = tenancy.pools[TENANTS[0]]
            with pool.connection() as conn:
                conn.execute("SELECT set_config('qascp.tenant_id',%s,false)", (TENANTS[1],))
                conn.execute("SET application_name='changed-by-test'")
            with pool.connection() as conn:
                self.assertIn(conn.execute("SELECT current_setting('qascp.tenant_id',true)").fetchone()[0], (None, ""))
                self.assertNotEqual(conn.execute("SHOW application_name").fetchone()[0], "changed-by-test")
        finally:
            tenancy.close()

    def test_09_audit_insert_outage_and_commit_failure_block_success(self):
        role = sql.Identifier("qascp_t_"+TENANTS[0].replace("-", ""))
        before = self.admin("SELECT count(*) FROM qascp.access_audit")[0][0]
        try:
            self.admin(sql.SQL("REVOKE INSERT ON qascp.access_audit FROM {}").format(role))
            self.assertEqual(self.lab.request().status_code, 503)
            self.assertEqual(self.admin("SELECT count(*) FROM qascp.access_audit")[0][0], before)
        finally:
            self.admin(sql.SQL("GRANT INSERT ON qascp.access_audit TO {}").format(role))
        self.admin("CREATE FUNCTION qascp.test_commit_failure() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'synthetic commit failure'; END $$")
        self.admin("CREATE CONSTRAINT TRIGGER test_commit_failure AFTER INSERT ON qascp.access_audit DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION qascp.test_commit_failure()")
        try:
            self.assertEqual(self.lab.request().status_code, 503)
            self.assertEqual(self.admin("SELECT count(*) FROM qascp.access_audit")[0][0], before)
        finally:
            self.admin("DROP TRIGGER test_commit_failure ON qascp.access_audit")
            self.admin("DROP FUNCTION qascp.test_commit_failure()")
        self.assertEqual(self.lab.request().status_code, 200)

    def test_10_migration_idempotence_drift_and_separate_roles(self):
        first = self.admin("SELECT version,sha256,applied_at FROM public.qascp_migrations")
        migrate(self.lab.migrator)
        self.assertEqual(first, self.admin("SELECT version,sha256,applied_at FROM public.qascp_migrations"))
        try:
            self.admin("UPDATE public.qascp_migrations SET sha256=%s", ("0"*64,))
            with self.assertRaises(ValueError):
                migrate(self.lab.migrator)
        finally:
            self.admin("UPDATE public.qascp_migrations SET sha256=%s", (first[0][1],))
        with self.assertRaises(ValueError):
            migrate(self.lab.connections[TENANTS[0]])
        with psycopg.connect(self.lab.migrator) as conn:
            self.assertEqual(conn.execute("SELECT count(*) FROM qascp.tenant_profile").fetchone()[0], 0)
        with psycopg.connect(self.lab.admin) as conn:
            conn.execute("SET ROLE qascp_metadata")
            with self.assertRaises(psycopg.errors.InsufficientPrivilege):
                conn.execute("SELECT * FROM qascp.tenant_profile")

    def test_11_installed_artifact_without_fixtures(self):
        self.assertNotIn(str(ROOT/"src"), str(Path(qascp.__file__).resolve()))
        package = files("qascp")
        self.assertTrue(package.joinpath("migrations/001_tenancy.sql").is_file())
        self.assertFalse(package.joinpath("integration_tests").is_dir())
        for url in ("/docs", "/redoc", "/openapi.json", "/config", "/api/v2/assets"):
            self.assertEqual(self.lab.client.get(url).status_code, 404)

    def test_12_identity_tls_origin_issuer_and_refresh_fail_closed(self):
        with self.assertRaises(IdentityError):
            OIDC(self.lab.issuer.url, "qascp-api").verify(self.lab.issuer.token())
        try:
            for document in ({"issuer": "https://other.invalid", "jwks_uri": self.lab.issuer.url+"/jwks"},
                             {"issuer": self.lab.issuer.url, "jwks_uri": "https://other.invalid/jwks"}):
                self.lab.issuer.document_override = document
                with self.assertRaises(IdentityError):
                    self.oidc().verify(self.lab.issuer.token())
        finally:
            self.lab.issuer.document_override = None
        verifier = self.oidc()
        verifier.verify(self.lab.issuer.token())
        self.lab.issuer.outage = True
        try:
            # Valid cached key is bounded; after expiry there is no stale-key fallback.
            verifier.verify(self.lab.issuer.token())
            verifier.expires, verifier.last_refresh = 0, float("-inf")
            with self.assertRaises(IdentityError):
                verifier.verify(self.lab.issuer.token())
        finally:
            self.lab.issuer.outage = False

    def test_13_key_rotation_unknown_key_throttle_and_duplicate_json(self):
        verifier = self.oidc()
        verifier.verify(self.lab.issuer.token())
        old_key, old_kid = self.lab.issuer.key, self.lab.issuer.kid
        try:
            self.lab.issuer.key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            self.lab.issuer.kid = "rotated"
            token = self.lab.issuer.token()
            with self.assertRaises(IdentityError):
                verifier.verify(token)
            verifier.last_refresh = float("-inf")
            verifier.verify(token)
            malformed = base64.urlsafe_b64encode(b'{"alg":"RS256","alg":"none"}').rstrip(b'=').decode()+".e30.AA"
            with self.assertRaises(IdentityError):
                verifier.verify(malformed)
        finally:
            self.lab.issuer.key, self.lab.issuer.kid = old_key, old_kid

    def test_14_failure_responses_never_contain_secret_or_request_values(self):
        response = self.lab.request(token="sensitive-token-sentinel")
        self.assertEqual(set(response.json()), {"error", "correlation_id"})
        self.assertNotIn("sensitive-token-sentinel", response.text)
        self.assertTrue(response.headers.get("www-authenticate"))
        self.lab.log.flush()
        logs = (self.lab.folder/"service.log").read_text(errors="replace")
        for secret in [*self.lab.passwords, "sensitive-token-sentinel"]:
            self.assertNotIn(secret, logs)

    def test_99_liveness_and_invalid_auth_work_during_database_outage(self):
        subprocess.run(["docker", "pause", self.lab.name], check=True, capture_output=True, timeout=10)
        try:
            self.assertEqual(self.lab.client.get("/live").json(), {"status": "alive"})
            self.assertEqual(self.lab.request(token="invalid").status_code, 401)
            self.assertEqual(self.lab.request().status_code, 503)
        finally:
            subprocess.run(["docker", "unpause", self.lab.name], check=True, capture_output=True, timeout=10)


if __name__ == "__main__":
    unittest.main()
