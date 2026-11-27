"""Verify the installed closure and emit a CycloneDX input SBOM for actual scanning."""

import hashlib
from importlib import metadata
import json
from pathlib import Path
import platform
import sys
from uuid import uuid4


def main():
    root = Path(__file__).resolve().parents[1]
    receipt = json.loads((root/"docs/verification/p2-input-receipt.json").read_text())
    if not (sys.version_info[:2] == (3, 14) and sys.platform == "linux" and platform.machine() == "x86_64"):
        raise SystemExit("Unsupported P2 validation platform")
    components = []
    for entry in receipt["test"]:
        if metadata.version(entry["name"]) != entry["version"]:
            raise SystemExit("Installed dependency differs from reviewed closure")
        name = entry["name"].lower().replace("_", "-")
        components.append({"type": "library", "name": name, "version": entry["version"],
                           "purl": f"pkg:pypi/{name}@{entry['version']}",
                           "hashes": [{"alg": "SHA-256", "content": entry["sha256"]}]})
    sbom = {"bomFormat": "CycloneDX", "specVersion": "1.6", "serialNumber": "urn:uuid:"+str(uuid4()),
            "version": 1, "metadata": {"component": {"type": "application", "name": "qascp-foundation-validation", "version": "0.1.0"}},
            "components": components}
    Path(".p2-inputs.cdx.json").write_text(json.dumps(sbom, indent=2))
    wheel = next(Path(".p2-dist").glob("*.whl"))
    print("QASCP_P2_ARTIFACT="+json.dumps({"filename": wheel.name, "sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(),
          "installed_location": str(metadata.distribution("qascp-foundation").locate_file("qascp")),
          "input_sbom": sbom, "limits": "Python distribution inventory, not exhaustive bundled native library discovery"}, sort_keys=True))


if __name__ == "__main__":
    main()
