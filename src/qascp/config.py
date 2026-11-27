"""Strict operator configuration; never format supplied values in errors."""

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
from urllib.parse import urlsplit
from uuid import UUID

from psycopg.conninfo import conninfo_to_dict


def unique_object(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError("Duplicate JSON member")
        result[key] = value
    return result


def strict_json(raw):
    return json.loads(raw, object_pairs_hook=unique_object,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Nonfinite JSON")))


def https_origin(url):
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
            or parsed.query or parsed.fragment or len(url) > 2048):
        raise ValueError("Invalid HTTPS configuration")
    return parsed.hostname.lower(), parsed.port or 443


def uuid_text(value):
    if not isinstance(value, str) or str(UUID(value)) != value:
        raise ValueError("Invalid canonical UUID")
    return value


@dataclass(frozen=True)
class Settings:
    issuer: str
    audience: str
    oidc_ca: str | None
    tenants: dict

    @classmethod
    def load(cls):
        try:
            issuer = os.environ["QASCP_OIDC_ISSUER"]
            https_origin(issuer)
            if issuer.endswith("/"):
                raise ValueError("Issuer trailing slash not supported by this profile")
            audience = os.environ["QASCP_OIDC_AUDIENCE"]
            if not re.fullmatch(r"[A-Za-z0-9:._/-]{1,256}", audience):
                raise ValueError("Invalid audience")
            path = Path(os.environ["QASCP_TENANT_CONNECTIONS_FILE"])
            # Secret material is read from a mounted file, not a command line.
            if path.is_symlink() or path.stat().st_size > 65536:
                raise ValueError("Invalid connection file")
            if os.name == "posix" and path.stat().st_mode & 0o077:
                raise ValueError("Connection file permissions must be private")
            tenants = strict_json(path.read_bytes())
            if not isinstance(tenants, dict) or not 1 <= len(tenants) <= 16:
                raise ValueError("Invalid tenant connections")
            for tenant, dsn in tenants.items():
                uuid_text(tenant)
                if not isinstance(dsn, str) or len(dsn) > 8192:
                    raise ValueError("Invalid connection")
                fields = conninfo_to_dict(dsn)
                allowed = {"host", "port", "dbname", "user", "password", "sslmode", "sslrootcert", "connect_timeout"}
                if (set(fields) != allowed or fields["sslmode"] != "verify-full"
                        or fields["connect_timeout"] != "3" or not fields["password"]
                        or not re.fullmatch(r"qascp_t_[a-f0-9]{32}", fields["user"])
                        or fields["user"] != "qascp_t_" + tenant.replace("-", "")
                        or not re.fullmatch(r"[A-Za-z0-9.-]{1,253}", fields["host"])
                        or not fields["port"].isdigit() or not 1 <= int(fields["port"]) <= 65535
                        or not re.fullmatch(r"[A-Za-z0-9_]{1,63}", fields["dbname"])
                        or not Path(fields["sslrootcert"]).is_file()):
                    raise ValueError("Unsafe database configuration")
            ca = os.environ.get("QASCP_OIDC_CA_FILE")
            if ca and not Path(ca).is_file():
                raise ValueError("Missing CA file")
            return cls(issuer, audience, ca, tenants)
        except (KeyError, ValueError, TypeError, OSError):
            raise ValueError("QASCP configuration rejected") from None
