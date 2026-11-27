"""Bounded OIDC discovery and RS256 verification against one configured issuer."""

import base64
from dataclasses import dataclass
import re
import ssl
from threading import Lock
import time
from urllib.request import HTTPSHandler, HTTPRedirectHandler, ProxyHandler, Request, build_opener

import jwt
from jwt.algorithms import RSAAlgorithm

from .config import https_origin, strict_json


class IdentityError(Exception):
    """Untrusted or unavailable identity evidence; no token values retained."""


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise IdentityError("Redirect denied")


@dataclass(frozen=True)
class Identity:
    issuer: str
    subject: str


class OIDC:
    def __init__(self, issuer, audience, ca=None):
        self.issuer, self.audience = issuer, audience
        self.origin = https_origin(issuer)
        self.opener = build_opener(ProxyHandler({}), NoRedirect(),
                                   HTTPSHandler(context=ssl.create_default_context(cafile=ca)))
        self.lock, self.keys = Lock(), {}
        self.expires, self.last_refresh = 0.0, float("-inf")

    def document(self, url):
        if https_origin(url) != self.origin:
            raise IdentityError("Issuer origin mismatch")
        with self.opener.open(Request(url, headers={"Accept": "application/json"}), timeout=3) as response:
            body = response.read(262145)
            if response.status != 200 or len(body) > 262144:
                raise IdentityError("Identity response rejected")
        value = strict_json(body)
        if not isinstance(value, dict):
            raise IdentityError("Identity document rejected")
        return value

    def refresh(self):
        self.last_refresh = time.monotonic()
        discovery = self.document(self.issuer + "/.well-known/openid-configuration")
        if discovery.get("issuer") != self.issuer:
            raise IdentityError("Issuer mismatch")
        jwks = self.document(discovery["jwks_uri"]).get("keys")
        if not isinstance(jwks, list) or not 1 <= len(jwks) <= 32:
            raise IdentityError("Key set rejected")
        keys = {}
        for item in jwks:
            if not isinstance(item, dict):
                raise IdentityError("Key rejected")
            # This profile intentionally requires unambiguous RSA signing keys.
            kid = item.get("kid")
            if (not isinstance(kid, str) or not re.fullmatch(r"[A-Za-z0-9._-]{1,128}", kid)
                    or kid in keys or item.get("kty") != "RSA" or item.get("use", "sig") != "sig"
                    or item.get("alg", "RS256") != "RS256"
                    or item.get("key_ops", ["verify"]) != ["verify"]
                    or not isinstance(item.get("n"), str) or not 342 <= len(item["n"]) <= 684
                    or not isinstance(item.get("e"), str) or len(item["e"]) > 8
                    or any(k in item for k in ("d", "p", "q", "dp", "dq", "qi", "oth", "jku", "x5u"))):
                raise IdentityError("Signing key rejected")
            key = RSAAlgorithm.from_jwk(item)
            if not 2048 <= key.key_size <= 4096 or key.public_numbers().e != 65537:
                raise IdentityError("RSA profile rejected")
            keys[kid] = key
        self.keys, self.expires = keys, time.monotonic() + 60

    def verify(self, token):
        try:
            if not isinstance(token, str) or len(token) > 16384:
                raise IdentityError("Token size rejected")
            parts = token.split(".")
            if len(parts) != 3 or any(not re.fullmatch(r"[A-Za-z0-9_-]+", p) for p in parts):
                raise IdentityError("Token encoding rejected")
            header, claims = [strict_json(base64.urlsafe_b64decode(p + "=" * (-len(p) % 4))) for p in parts[:2]]
            if (not isinstance(header, dict) or not isinstance(claims, dict)
                    or set(header) - {"alg", "typ", "kid"}
                    or header.get("alg") != "RS256" or header.get("typ") != "at+jwt"
                    or not isinstance(header.get("kid"), str)
                    or not re.fullmatch(r"[A-Za-z0-9._-]{1,128}", header["kid"])):
                raise IdentityError("Token header rejected")
            for field in ("exp", "iat"):
                if type(claims.get(field)) is not int:
                    raise IdentityError("NumericDate rejected")
            if "nbf" in claims and type(claims["nbf"]) is not int:
                raise IdentityError("NumericDate rejected")
            subject = claims.get("sub")
            if (not isinstance(subject, str) or not 1 <= len(subject) <= 256
                    or any(ord(c) < 32 for c in subject)
                    or claims["exp"] <= claims["iat"] or claims["exp"] - claims["iat"] > 3600
                    or not isinstance(claims.get("amr"), list) or "mfa" not in claims["amr"]):
                raise IdentityError("Identity claims rejected")
            kid = header["kid"]
            with self.lock:
                now = time.monotonic()
                if now >= self.expires or kid not in self.keys:
                    if now - self.last_refresh < 5:
                        raise IdentityError("Identity refresh limited")
                    self.refresh()
                key = self.keys.get(kid)
            if key is None:
                raise IdentityError("Unknown signing key")
            jwt.decode(token, key, algorithms=["RS256"], issuer=self.issuer,
                       audience=self.audience, leeway=30,
                       options={"require": ["iss", "aud", "sub", "exp", "iat"]})
            return Identity(self.issuer, subject)
        except Exception:
            # Network, parser, TLS and cryptographic failures share a closed boundary.
            # The original exception/token is never exposed or logged.
            raise IdentityError("Identity verification failed") from None
