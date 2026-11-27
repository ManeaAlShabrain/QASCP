"""Discover, download and identify candidate inputs without installing their code.

Run only on the declared Linux CPython314 x86_64 validation host. The resulting
receipt must be reviewed and frozen before any runtime/dependency installation.
Docker registry tokens are kept only in memory and never included in evidence.
"""

from email.parser import BytesParser
from email.policy import default
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.request import Request, urlopen
from zipfile import ZipFile


KNOWN = {"fastapi": "0.165.0", "PyJWT": "2.15.1", "psycopg": "3.3.9",
         "psycopg-binary": "3.3.9", "psycopg-pool": "3.3.3"}
RUNTIME = ("fastapi", "uvicorn", "PyJWT", "cryptography", "psycopg",
           "psycopg-binary", "psycopg-pool")
TEST = ("httpx", "jsonschema", "rfc3339-validator")
BUILD = ("build", "setuptools", "wheel")
PG_TAG = "18.7-alpine3.24"


def fetch(url, *, headers=None):
    with urlopen(Request(url, headers=headers or {}), timeout=20) as response:
        body = response.read(4 * 1024 * 1024 + 1)
        if len(body) > 4 * 1024 * 1024:
            raise ValueError("Oversize input metadata")
        return body, dict(response.headers)


def metadata(name, version=None):
    if not re.fullmatch(r"[A-Za-z0-9._-]+", name):
        raise ValueError("Invalid package name")
    tail = f"{name}/{version}/json" if version else f"{name}/json"
    return json.loads(fetch("https://pypi.org/pypi/" + tail)[0])


def wheel_evidence(path):
    with ZipFile(path) as archive:
        items = archive.infolist()
        if len(items) > 10000:
            raise ValueError("Oversize wheel inventory")
        # setuptools legitimately carries nested vendored dist-info directories.
        # Only the root wheel distribution defines the installed artifact.
        meta = [i for i in items if re.fullmatch(r"[^/]+\.dist-info/METADATA", i.filename)]
        if len(meta) != 1 or meta[0].file_size > 2 * 1024 * 1024:
            raise ValueError("Invalid wheel metadata")
        parsed = BytesParser(policy=default).parsebytes(archive.read(meta[0]))
        name, version = str(parsed["Name"]), str(parsed["Version"])
        release = metadata(name, version)
        if release.get("vulnerabilities"):
            raise ValueError("Reported PyPI advisory requires disposition")
        entry = next((v for v in release["urls"] if v["filename"] == path.name), None)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if not entry or entry.get("yanked") or entry["digests"]["sha256"] != digest:
            raise ValueError("Wheel source or integrity mismatch")
        licences, native = [], []
        for info in items:
            leaf = info.filename.rsplit("/", 1)[-1].upper()
            if ".dist-info/" in info.filename and any(
                    leaf.startswith(v) for v in ("LICENSE", "LICENCE", "NOTICE", "COPYING", "COPYRIGHT")):
                if info.file_size > 512 * 1024 or len(licences) >= 100:
                    raise ValueError("Oversize licence material")
                licences.append({"path": info.filename, "bytes": info.file_size,
                                 "sha256": hashlib.sha256(archive.read(info)).hexdigest()})
            if info.filename.endswith((".so", ".dll", ".dylib")) or ".so." in info.filename:
                native.append({"path": info.filename, "bytes": info.file_size})
        licence = release["info"].get("license_expression") or release["info"].get("license") or "UNKNOWN"
        return {"name": name, "version": version, "filename": path.name,
                "sha256": digest, "url": entry["url"], "requires_python": parsed.get("Requires-Python"),
                "requires_dist": parsed.get_all("Requires-Dist", []),
                "declared_license": licence[:512], "embedded_license_files": licences,
                "bundled_native_files": native, "pypi_advisories": release.get("vulnerabilities", []),
                "project_urls": release["info"].get("project_urls") or {}}


def docker_evidence():
    token = json.loads(fetch("https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/postgres:pull")[0])["token"]
    headers = {"Authorization": "Bearer " + token,
               "Accept": "application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.list.v2+json"}
    body, response_headers = fetch("https://registry-1.docker.io/v2/library/postgres/manifests/" + PG_TAG, headers=headers)
    index_digest = "sha256:" + hashlib.sha256(body).hexdigest()
    declared = next((v for k, v in response_headers.items() if k.lower() == "docker-content-digest"), None)
    if declared != index_digest:
        raise ValueError("Registry manifest digest mismatch")
    index = json.loads(body)
    matches = [m for m in index["manifests"] if m.get("platform", {}).get("os") == "linux"
               and m.get("platform", {}).get("architecture") == "amd64"]
    if len(matches) != 1 or not re.fullmatch(r"sha256:[a-f0-9]{64}", matches[0]["digest"]):
        raise ValueError("Ambiguous Docker platform")
    digest = matches[0]["digest"]
    headers["Accept"] = "application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.v2+json"
    platform_body, _ = fetch("https://registry-1.docker.io/v2/library/postgres/manifests/" + digest, headers=headers)
    if "sha256:" + hashlib.sha256(platform_body).hexdigest() != digest:
        raise ValueError("Platform image digest mismatch")
    return {"registry": "docker.io/library/postgres", "observed_tag": PG_TAG,
            "index_digest": index_digest, "linux_amd64_digest": digest,
            "image": "postgres@" + digest,
            "scope": "Manifest identity discovery only; no image execution or vulnerability clearance"}


def main():
    if not (sys.version_info[:2] == (3, 14) and sys.platform == "linux" and platform.machine() == "x86_64"):
        raise SystemExit("Input discovery requires Linux x86_64 CPython314")
    pins = {}
    for name in (*RUNTIME, *TEST, *BUILD):
        release = metadata(name, KNOWN.get(name))
        version = release["info"]["version"]
        if release.get("vulnerabilities") or not re.fullmatch(r"\d+(?:\.\d+)+", version):
            raise ValueError("Release discovery requires explicit review")
        pins[name] = version
    print("QASCP_P2_DIRECT_PINS=" + json.dumps(pins, sort_keys=True))
    with TemporaryDirectory(prefix="qascp-p2-inputs-") as work:
        for group, names in (("runtime", RUNTIME), ("test", (*RUNTIME, *TEST)), ("build", BUILD)):
            folder = Path(work) / group
            folder.mkdir()
            command = [sys.executable, "-m", "pip", "--isolated", "download", "--disable-pip-version-check",
                       "--index-url", "https://pypi.org/simple", "--only-binary=:all:", "--dest", str(folder)]
            command.extend(f"{name}=={pins[name]}" for name in names)
            result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=240)
            if result.returncode:
                print(result.stdout[-2000:])
                print(result.stderr[-2000:])
                raise ValueError("Wheel-only resolution failed")
            wheels = sorted(folder.glob("*.whl"))
            entries = [wheel_evidence(p) for p in wheels]
            if not entries or len({v["name"].lower().replace("_", "-") for v in entries}) != len(entries):
                raise ValueError("Wheel closure is not unique")
            print("QASCP_P2_" + group.upper() + "_EVIDENCE=" + json.dumps(entries, sort_keys=True))
    print("QASCP_P2_POSTGRES_EVIDENCE=" + json.dumps(docker_evidence(), sort_keys=True))
    print("QASCP_P2_DISCOVERY_LIMITS=Downloaded only; not installed; embedded notice identities are not legal clearance; PyPI advisories are bounded, not exhaustive SCA")


if __name__ == "__main__":
    main()
