CREATE SCHEMA qascp AUTHORIZATION qascp_owner;
CREATE SCHEMA qascp_meta AUTHORIZATION qascp_metadata;
REVOKE ALL ON SCHEMA qascp, qascp_meta FROM PUBLIC;

CREATE TABLE qascp_meta.role_tenant (
    login_name name PRIMARY KEY,
    tenant_id uuid NOT NULL UNIQUE
);
ALTER TABLE qascp_meta.role_tenant OWNER TO qascp_metadata;
REVOKE ALL ON qascp_meta.role_tenant FROM PUBLIC;

CREATE FUNCTION qascp_meta.bound_tenant() RETURNS uuid
LANGUAGE sql STABLE SECURITY DEFINER
SET search_path = pg_catalog, pg_temp
AS 'SELECT tenant_id FROM qascp_meta.role_tenant WHERE login_name = SESSION_USER';
ALTER FUNCTION qascp_meta.bound_tenant() OWNER TO qascp_metadata;
REVOKE ALL ON FUNCTION qascp_meta.bound_tenant() FROM PUBLIC;
GRANT USAGE ON SCHEMA qascp_meta TO qascp_owner;
GRANT EXECUTE ON FUNCTION qascp_meta.bound_tenant() TO qascp_owner;

CREATE TABLE qascp.tenant_profile (
    tenant_id uuid PRIMARY KEY,
    display_name text NOT NULL CHECK (length(display_name) BETWEEN 1 AND 200)
);
CREATE TABLE qascp.membership (
    tenant_id uuid NOT NULL REFERENCES qascp.tenant_profile(tenant_id),
    actor_id uuid NOT NULL,
    issuer text NOT NULL CHECK (length(issuer) BETWEEN 1 AND 2048),
    subject text NOT NULL CHECK (length(subject) BETWEEN 1 AND 256),
    actor_type text NOT NULL CHECK (actor_type IN ('user', 'workload', 'connector', 'system')),
    active boolean NOT NULL,
    authorization_version bigint NOT NULL CHECK (authorization_version > 0),
    permissions text[] NOT NULL,
    PRIMARY KEY (tenant_id, actor_id),
    UNIQUE (tenant_id, issuer, subject)
);
CREATE TABLE qascp.access_audit (
    tenant_id uuid NOT NULL,
    audit_event_id uuid NOT NULL,
    schema_version text NOT NULL CHECK (schema_version = '1.0'),
    actor_id uuid NOT NULL,
    actor_type text NOT NULL CHECK (actor_type IN ('user', 'workload', 'connector', 'system')),
    authorization_version text NOT NULL CHECK (length(authorization_version) BETWEEN 1 AND 128),
    action text NOT NULL CHECK (action = 'tenancy.read'),
    resource_type text NOT NULL CHECK (resource_type = 'tenant'),
    resource_id uuid NOT NULL,
    outcome text NOT NULL CHECK (outcome IN ('succeeded', 'denied')),
    occurred_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    correlation_id uuid NOT NULL,
    PRIMARY KEY (tenant_id, audit_event_id),
    FOREIGN KEY (tenant_id, actor_id) REFERENCES qascp.membership(tenant_id, actor_id),
    FOREIGN KEY (resource_id) REFERENCES qascp.tenant_profile(tenant_id),
    CHECK (resource_id = tenant_id)
);

ALTER TABLE qascp.tenant_profile OWNER TO qascp_owner;
ALTER TABLE qascp.membership OWNER TO qascp_owner;
ALTER TABLE qascp.access_audit OWNER TO qascp_owner;
ALTER TABLE qascp.tenant_profile ENABLE ROW LEVEL SECURITY;
ALTER TABLE qascp.tenant_profile FORCE ROW LEVEL SECURITY;
ALTER TABLE qascp.membership ENABLE ROW LEVEL SECURITY;
ALTER TABLE qascp.membership FORCE ROW LEVEL SECURITY;
ALTER TABLE qascp.access_audit ENABLE ROW LEVEL SECURITY;
ALTER TABLE qascp.access_audit FORCE ROW LEVEL SECURITY;

CREATE POLICY tenant_boundary ON qascp.tenant_profile
USING (tenant_id = qascp_meta.bound_tenant()
       AND tenant_id = NULLIF(current_setting('qascp.tenant_id', true), '')::uuid)
WITH CHECK (tenant_id = qascp_meta.bound_tenant()
       AND tenant_id = NULLIF(current_setting('qascp.tenant_id', true), '')::uuid);
CREATE POLICY tenant_boundary ON qascp.membership
USING (tenant_id = qascp_meta.bound_tenant()
       AND tenant_id = NULLIF(current_setting('qascp.tenant_id', true), '')::uuid)
WITH CHECK (tenant_id = qascp_meta.bound_tenant()
       AND tenant_id = NULLIF(current_setting('qascp.tenant_id', true), '')::uuid);
CREATE POLICY tenant_boundary ON qascp.access_audit
USING (tenant_id = qascp_meta.bound_tenant()
       AND tenant_id = NULLIF(current_setting('qascp.tenant_id', true), '')::uuid)
WITH CHECK (tenant_id = qascp_meta.bound_tenant()
       AND tenant_id = NULLIF(current_setting('qascp.tenant_id', true), '')::uuid);
REVOKE ALL ON ALL TABLES IN SCHEMA qascp FROM PUBLIC;

-- Separate from the metadata definer. FORCE RLS still evaluates SESSION_USER.
-- Runtime receives no UPDATE privilege merely to take a revocation-safe lock.
CREATE FUNCTION qascp.lock_membership(p_tenant uuid, p_issuer text, p_subject text)
RETURNS TABLE(actor_id uuid, actor_type text, active boolean, authorization_version bigint, permissions text[])
LANGUAGE sql VOLATILE SECURITY DEFINER SET search_path = pg_catalog, pg_temp
AS 'SELECT m.actor_id, m.actor_type, m.active, m.authorization_version, m.permissions
    FROM qascp.membership m WHERE m.tenant_id=p_tenant AND m.issuer=p_issuer AND m.subject=p_subject FOR SHARE';
ALTER FUNCTION qascp.lock_membership(uuid,text,text) OWNER TO qascp_owner;
REVOKE ALL ON FUNCTION qascp.lock_membership(uuid,text,text) FROM PUBLIC;
