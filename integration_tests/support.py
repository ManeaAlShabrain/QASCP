"""Synthetic-only disposable PostgreSQL and TLS issuer/server harness."""

from datetime import datetime, timedelta, timezone
import functools
import http.server
import importlib.util
import json
import os
from pathlib import Path
import secrets
import re
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
import time
from uuid import uuid4

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import jwt
from jwt.algorithms import RSAAlgorithm
import httpx
import psycopg
from psycopg.conninfo import make_conninfo

from qascp.migrate import migrate


ROOT = Path(__file__).resolve().parents[1]
TENANTS = ("11111111-1111-4111-8111-111111111111", "22222222-2222-4222-8222-222222222222")
ACTOR = "33333333-3333-4333-8333-333333333333"


def port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def material(folder):
    now = datetime.now(timezone.utc)
    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "QASCP ephemeral test CA")])
    ca = (x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(ca_key.public_key())
          .serial_number(x509.random_serial_number()).not_valid_before(now-timedelta(minutes=1))
          .not_valid_after(now+timedelta(days=1)).add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
          .sign(ca_key, hashes.SHA256()))
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    cert = (x509.CertificateBuilder().subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")]))
            .issuer_name(name).public_key(key.public_key()).serial_number(x509.random_serial_number())
            .not_valid_before(now-timedelta(minutes=1)).not_valid_after(now+timedelta(days=1))
            .add_extension(x509.SubjectAlternativeName([x509.DNSName("localhost")]), critical=False)
            .sign(ca_key, hashes.SHA256()))
    for filename, data in (("ca.crt", ca.public_bytes(serialization.Encoding.PEM)),
                           ("server.crt", cert.public_bytes(serialization.Encoding.PEM)),
                           ("server.key", key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                                            serialization.NoEncryption()))):
        (folder/filename).write_bytes(data)
    (folder/"server.key").chmod(0o600)


class Issuer:
    def __init__(self, folder):
        self.key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.kid = "initial"
        self.outage = False
        self.document_override = None
        owner = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if owner.outage:
                    self.send_response(503)
                    self.end_headers()
                    return
                if self.path.endswith("/.well-known/openid-configuration"):
                    data = owner.document_override or {"issuer": owner.url, "jwks_uri": owner.url+"/jwks"}
                elif self.path == "/jwks":
                    value = RSAAlgorithm.to_jwk(owner.key.public_key(), as_dict=True)
                    value.update(kid=owner.kid, use="sig", alg="RS256")
                    data = {"keys": [value]}
                else:
                    self.send_response(404)
                    self.end_headers()
                    return
                body = json.dumps(data).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                return None

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = "https://localhost:" + str(self.server.server_port)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(folder/"server.crt", folder/"server.key")
        self.server.socket = context.wrap_socket(self.server.socket, server_side=True)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def token(self, **overrides):
        now = int(time.time())
        claims = {"iss": self.url, "aud": "qascp-api", "sub": "same-subject", "iat": now,
                  "exp": now+300, "amr": ["pwd", "mfa"]}
        claims.update(overrides)
        return jwt.encode(claims, self.key, algorithm="RS256", headers={"kid": self.kid, "typ": "at+jwt"})

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)


class Lab:
    def __init__(self):
        self.temp = tempfile.TemporaryDirectory(prefix="qascp-p2-")
        self.folder = Path(self.temp.name)
        self.folder.chmod(0o755)  # Only test TLS public material is mounted; secrets remain 0600.
        material(self.folder)
        self.issuer = Issuer(self.folder)
        self.name = "qascp-p2-" + uuid4().hex
        self.process = None
        self.dbport = port()
        image = json.loads((ROOT/"docs/verification/p2-input-receipt.json").read_text())["postgres"]["image"]
        admin_password, migrator_password = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
        self.passwords = [secrets.token_urlsafe(32), secrets.token_urlsafe(32)]
        envfile = self.folder/"db.env"
        envfile.write_text("POSTGRES_PASSWORD="+admin_password+"\nPOSTGRES_DB=qascp_test\nPOSTGRES_INITDB_ARGS=--auth-host=scram-sha-256\n")
        envfile.chmod(0o600)
        # Key is copied from a read-only mount by root, then restricted to postgres.
        command = ["docker", "run", "--detach", "--name", self.name, "--env-file", str(envfile),
                   "--publish", "127.0.0.1:"+str(self.dbport)+":5432", "--mount",
                   "type=bind,src="+str(self.folder)+",dst=/qascp-test-tls,readonly", image,
                   "sh", "-c", "cp /qascp-test-tls/server.crt /tmp/server.crt && cp /qascp-test-tls/server.key /tmp/server.key && chown postgres:postgres /tmp/server.* && chmod 600 /tmp/server.key && exec docker-entrypoint.sh postgres -c ssl=on -c ssl_cert_file=/tmp/server.crt -c ssl_key_file=/tmp/server.key -c log_statement=none -c log_min_error_statement=panic"]
        subprocess.run(command, check=True, capture_output=True, timeout=180)
        self.admin = self.dsn("postgres", admin_password)
        self.migrator = self.dsn("qascp_migrator", migrator_password)
        for attempt in range(80):
            try:
                with psycopg.connect(self.admin):
                    break
            except psycopg.OperationalError:
                if attempt == 79:
                    raise RuntimeError("Test PostgreSQL did not become available") from None
                time.sleep(0.25)
        spec = importlib.util.spec_from_file_location("p2_operator", ROOT/"scripts/p2_operator.py")
        operator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(operator)
        operator.bootstrap(self.admin, migrator_password)
        migrate(self.migrator)
        self.connections = {}
        for index, tenant in enumerate(TENANTS):
            operator.provision(self.admin, tenant, self.passwords[index], "Synthetic Tenant "+str(index), self.issuer.url, "same-subject", ACTOR)
            self.connections[tenant] = self.dsn("qascp_t_"+tenant.replace("-", ""), self.passwords[index])
        secretfile = self.folder/"connections.json"
        secretfile.write_text(json.dumps(self.connections))
        secretfile.chmod(0o600)
        appport = port()
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        env.update(QASCP_OIDC_ISSUER=self.issuer.url, QASCP_OIDC_AUDIENCE="qascp-api",
                   QASCP_OIDC_CA_FILE=str(self.folder/"ca.crt"), QASCP_TENANT_CONNECTIONS_FILE=str(secretfile),
                   QASCP_TLS_CERT=str(self.folder/"server.crt"), QASCP_TLS_KEY=str(self.folder/"server.key"), QASCP_PORT=str(appport))
        self.log = open(self.folder/"service.log", "wb")
        self.process = subprocess.Popen([sys.executable, "-I", "-c", "from qascp.server import main; main()"],
                                        cwd=self.folder, env=env, stdout=self.log, stderr=self.log)
        self.client = httpx.Client(base_url="https://localhost:"+str(appport),
                                   verify=ssl.create_default_context(cafile=str(self.folder/"ca.crt")), trust_env=False, timeout=8)
        for attempt in range(80):
            try:
                if self.client.get("/live").status_code == 200:
                    break
            except httpx.HTTPError:
                if self.process.poll() is not None or attempt == 79:
                    self.log.flush()
                    diagnostic = (self.folder/"service.log").read_text(errors="replace")[-8000:]
                    for sensitive in [admin_password, migrator_password, *self.passwords,
                                      self.admin, self.migrator, *self.connections.values()]:
                        diagnostic = diagnostic.replace(sensitive, "[REDACTED]")
                    diagnostic = re.sub(r"[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", "[REDACTED_TOKEN]", diagnostic)
                    raise RuntimeError("Installed HTTPS service did not start; sanitized test-process diagnostic: "+diagnostic) from None
                time.sleep(0.1)

    def dsn(self, user, password):
        return make_conninfo(host="localhost", port=str(self.dbport), dbname="qascp_test", user=user,
                             password=password, sslmode="verify-full", sslrootcert=str(self.folder/"ca.crt"), connect_timeout="3")

    def request(self, tenant=TENANTS[0], token=None, **kwargs):
        headers = {"Authorization": "Bearer "+(token or self.issuer.token()), "X-Tenant-ID": tenant}
        headers.update(kwargs.pop("headers", {}))
        return self.client.get("/api/v2/tenancy/current", headers=headers, **kwargs)

    def close(self):
        if getattr(self, "process", None):
            self.process.terminate()
            self.process.wait(timeout=10)
            self.log.close()
        if hasattr(self, "client"):
            self.client.close()
        if hasattr(self, "issuer"):
            self.issuer.close()
        if hasattr(self, "name"):
            subprocess.run(["docker", "rm", "--force", self.name], capture_output=True, timeout=20, check=False)
        if hasattr(self, "temp"):
            self.temp.cleanup()
