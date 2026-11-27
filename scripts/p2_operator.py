"""Explicit DBA bootstrap/provisioning, outside the installed runtime artifact.

Credentials come from a private JSON file named by QASCP_OPERATOR_FILE.
No migration/provisioning operation is reachable through the HTTP application.
"""

import os
from pathlib import Path
from uuid import UUID

import psycopg
from psycopg import sql

from qascp.config import strict_json, uuid_text


def bootstrap(admin_dsn, migrator_password):
    with psycopg.connect(admin_dsn) as conn:
        database = conn.execute("SELECT current_database()").fetchone()[0]
        for role in ("qascp_owner", "qascp_metadata"):
            conn.execute(sql.SQL("CREATE ROLE {} NOLOGIN NOINHERIT NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE NOREPLICATION").format(sql.Identifier(role)))
        conn.execute(sql.SQL("CREATE ROLE qascp_migrator LOGIN INHERIT NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE NOREPLICATION PASSWORD {}").format(sql.Literal(migrator_password)))
        conn.execute("GRANT qascp_owner, qascp_metadata TO qascp_migrator")
        conn.execute(sql.SQL("REVOKE ALL ON DATABASE {} FROM PUBLIC").format(sql.Identifier(database)))
        conn.execute(sql.SQL("GRANT CONNECT, CREATE ON DATABASE {} TO qascp_migrator").format(sql.Identifier(database)))
        conn.execute("REVOKE CREATE ON SCHEMA public FROM PUBLIC")
        conn.execute("GRANT USAGE, CREATE ON SCHEMA public TO qascp_migrator")


def provision(admin_dsn, tenant, password, display_name, issuer, subject, actor):
    uuid_text(tenant)
    uuid_text(actor)
    role = "qascp_t_" + tenant.replace("-", "")
    with psycopg.connect(admin_dsn) as conn:
        database = conn.execute("SELECT current_database()").fetchone()[0]
        conn.execute(sql.SQL("CREATE ROLE {} LOGIN NOINHERIT NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE NOREPLICATION PASSWORD {}").format(sql.Identifier(role), sql.Literal(password)))
        conn.execute(sql.SQL("GRANT CONNECT ON DATABASE {} TO {}").format(sql.Identifier(database), sql.Identifier(role)))
        conn.execute(sql.SQL("GRANT USAGE ON SCHEMA qascp, qascp_meta TO {}").format(sql.Identifier(role)))
        conn.execute(sql.SQL("GRANT EXECUTE ON FUNCTION qascp_meta.bound_tenant() TO {}").format(sql.Identifier(role)))
        conn.execute(sql.SQL("GRANT EXECUTE ON FUNCTION qascp.lock_membership(uuid,text,text) TO {}").format(sql.Identifier(role)))
        conn.execute(sql.SQL("GRANT SELECT ON qascp.tenant_profile, qascp.membership TO {}").format(sql.Identifier(role)))
        conn.execute(sql.SQL("GRANT INSERT ON qascp.access_audit TO {}").format(sql.Identifier(role)))
        conn.execute("INSERT INTO qascp_meta.role_tenant VALUES (%s,%s)", (role, tenant))
        conn.execute("INSERT INTO qascp.tenant_profile VALUES (%s,%s)", (tenant, display_name))
        conn.execute("INSERT INTO qascp.membership VALUES (%s,%s,%s,%s,'user',true,1,ARRAY['tenancy:read'])",
                     (tenant, actor, issuer, subject))


def main():
    import sys
    try:
        path = Path(os.environ["QASCP_OPERATOR_FILE"])
        if path.stat().st_size > 65536 or path.is_symlink() or (os.name == "posix" and path.stat().st_mode & 0o077):
            raise ValueError("Invalid operator file")
        value = strict_json(path.read_bytes())
        if sys.argv[1:] == ["bootstrap"]:
            bootstrap(value["admin_dsn"], value["migrator_password"])
        elif sys.argv[1:] == ["provision"]:
            provision(value["admin_dsn"], **value["tenant"])
        else:
            raise ValueError("Choose bootstrap or provision")
    except Exception:
        raise SystemExit("Operator action failed; inspect through restricted operator channel") from None
    print("QASCP operator action committed")


if __name__ == "__main__":
    main()
