"""Role-bound tenant pools. Membership, authorized read and audit share one transaction."""

from uuid import uuid4

from psycopg_pool import ConnectionPool


class AccessDenied(Exception):
    """No currently authorized human membership."""


def reset_connection(conn):
    conn.rollback()
    conn.execute("RESET ROLE")
    conn.execute("RESET ALL")


def configure_connection(conn, tenant):
    identity = conn.execute("SELECT session_user, current_user, qascp_meta.bound_tenant()::text").fetchone()
    role = conn.execute("SELECT rolsuper, rolbypassrls, rolcreaterole, rolcreatedb, rolreplication "
                        "FROM pg_roles WHERE rolname = session_user").fetchone()
    memberships = conn.execute("SELECT 1 FROM pg_auth_members m JOIN pg_roles r ON r.oid=m.member "
                               "WHERE r.rolname=session_user").fetchone()
    owned = conn.execute("SELECT 1 FROM pg_class c JOIN pg_roles r ON r.oid=c.relowner "
                         "WHERE r.rolname=session_user LIMIT 1").fetchone()
    if (identity != ("qascp_t_" + tenant.replace("-", ""),) * 2 + (tenant,)
            or role != (False,) * 5 or memberships or owned):
        raise ValueError("Unsafe runtime database identity")


class Tenancy:
    def __init__(self, connections):
        self.pools = {tenant: ConnectionPool(dsn, min_size=0, max_size=4, max_waiting=32,
                      timeout=3, open=False, kwargs={"autocommit": True, "prepare_threshold": None},
                      configure=lambda c, t=tenant: configure_connection(c, t), reset=reset_connection,
                      reconnect_timeout=3, name="qascp-tenant") for tenant, dsn in connections.items()}

    def open(self):
        for pool in self.pools.values():
            pool.open()

    def close(self):
        for pool in self.pools.values():
            pool.close(timeout=3)

    def current(self, tenant, identity, correlation):
        pool = self.pools.get(tenant)
        if pool is None:
            raise AccessDenied()
        denied = False
        with pool.connection(timeout=3) as conn:
            with conn.transaction():
                conn.execute("SET LOCAL statement_timeout = '2500ms'")
                conn.execute("SET LOCAL lock_timeout = '1000ms'")
                conn.execute("SET LOCAL idle_in_transaction_session_timeout = '3000ms'")
                conn.execute("SELECT set_config('qascp.tenant_id', %s, true)", (tenant,))
                # The selected pool is server configured; user token tenant/roles are ignored.
                row = conn.execute("SELECT actor_id::text, actor_type, active, authorization_version, permissions "
                                   "FROM qascp.lock_membership(%s,%s,%s)",
                                   (tenant, identity.issuer, identity.subject)).fetchone()
                if row is None:
                    raise AccessDenied()
                actor, actor_type, active, version, permissions = row
                denied = actor_type != "user" or not active or "tenancy:read" not in permissions
                result = None
                if not denied:
                    profile = conn.execute("SELECT display_name FROM qascp.tenant_profile WHERE tenant_id=%s", (tenant,)).fetchone()
                    if profile is None:
                        raise AccessDenied()
                    result = {"schema_version": "0.1", "tenant_id": tenant, "display_name": profile[0],
                              "actor_id": actor, "authorization_version": str(version), "correlation_id": correlation}
                conn.execute("INSERT INTO qascp.access_audit(tenant_id,audit_event_id,schema_version,actor_id,actor_type,"
                             "authorization_version,action,resource_type,resource_id,outcome,correlation_id) "
                             "VALUES (%s,%s,'1.0',%s,%s,%s,'tenancy.read','tenant',%s,%s,%s)",
                             (tenant, str(uuid4()), actor, actor_type, str(version), tenant,
                              "denied" if denied else "succeeded", correlation))
            # Commit completes before any success or audited denial leaves the data layer.
        if denied:
            raise AccessDenied()
        return result
