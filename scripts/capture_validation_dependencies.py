"""P1 wheel integrity/provenance and PyPI advisory evidence; no runtime dependencies.

Use after pip download into .validation-wheels. This is a limited PyPI advisory
lookup, not an exhaustive vulnerability/license clearance or a signed attestation.
"""

import hashlib
import json
from pathlib import Path
import platform
import sys
from urllib.request import urlopen


def main():
    root = Path(__file__).resolve().parents[1]
    wheels = list((root / ".validation-wheels").glob("*.whl"))
    pins = [line.strip() for line in (root / "requirements-contracts.txt").read_text().splitlines()
            if line.strip() and not line.startswith("#")]
    if len(wheels) != len(pins):
        raise SystemExit("Wheel closure does not match pins")
    entries = []
    for pin in pins:
        name, version = pin.split("==")
        with urlopen(f"https://pypi.org/pypi/{name}/{version}/json", timeout=30) as response:
            metadata = json.load(response)
        candidates = {artifact["filename"]: artifact for artifact in metadata["urls"]
                      if artifact["packagetype"] == "bdist_wheel"}
        matches = [wheel for wheel in wheels if wheel.name in candidates]
        if len(matches) != 1:
            raise SystemExit("Expected one official wheel per pin")
        wheel = matches[0]
        digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
        artifact = candidates[wheel.name]
        if digest != artifact["digests"]["sha256"] or artifact.get("yanked"):
            raise SystemExit("Wheel integrity or release state rejected")
        entries.append({"name": name, "version": version, "filename": wheel.name,
                        "sha256": digest, "url": artifact["url"],
                        "license": metadata["info"].get("license_expression") or metadata["info"].get("license"),
                        "advisories": metadata.get("vulnerabilities", [])})
    evidence = {"python": sys.version, "platform": platform.platform(),
                "machine": platform.machine(), "packages": entries,
                "coverage": "PyPI release JSON advisories only; not exhaustive SCA or license approval"}
    print("QASCP_DEPENDENCY_EVIDENCE=" + json.dumps(evidence, sort_keys=True))
    if any(entry["advisories"] for entry in entries):
        raise SystemExit("PyPI advisory entries require review")


if __name__ == "__main__":
    main()
