"""Operator-only transactional migration; never invoked by application startup."""

import hashlib
from importlib.resources import files
import os

import psycopg


def migrate(dsn):
    migrations = sorted(files("qascp").joinpath("migrations").iterdir(), key=lambda p: p.name)
    with psycopg.connect(dsn, autocommit=True, prepare_threshold=None) as conn:
        with conn.transaction():
            conn.execute("SELECT pg_advisory_xact_lock(51783021)")
            role = conn.execute("SELECT session_user").fetchone()[0]
            if role != "qascp_migrator":
                raise ValueError("Dedicated migrator identity required")
            conn.execute("CREATE TABLE IF NOT EXISTS public.qascp_migrations "
                         "(version text PRIMARY KEY, sha256 text NOT NULL, applied_at timestamptz NOT NULL DEFAULT now())")
            conn.execute("REVOKE ALL ON public.qascp_migrations FROM PUBLIC")
            applied = dict(conn.execute("SELECT version, sha256 FROM public.qascp_migrations").fetchall())
            expected = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in migrations}
            if set(applied) - set(expected) or any(expected[k] != v for k, v in applied.items()):
                raise ValueError("Migration history drift")
            for migration in migrations:
                if migration.name not in applied:
                    conn.execute(migration.read_text(encoding="utf-8"), prepare=False)
                    conn.execute("INSERT INTO public.qascp_migrations(version,sha256) VALUES (%s,%s)",
                                 (migration.name, expected[migration.name]))
    return expected


def main():
    try:
        migrate(os.environ["QASCP_MIGRATION_DSN"])
    except Exception:
        raise SystemExit("Migration failed; inspect through the restricted operator channel") from None
    print("QASCP migrations verified/applied")
