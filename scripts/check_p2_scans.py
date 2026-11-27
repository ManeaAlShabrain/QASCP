"""Retain actual scanner results and fail on unresolved High/Critical findings."""

import hashlib
import json
from pathlib import Path


def main():
    blockers = []
    for name in (".p2-python-scan.json", ".p2-image-scan.json"):
        path = Path(name)
        raw = path.read_bytes()
        report = json.loads(raw)
        results = report.get("Results", [])
        if not results:
            raise SystemExit("Scanner returned no evaluated components")
        print("QASCP_P2_SCAN="+json.dumps({"file": name, "sha256": hashlib.sha256(raw).hexdigest(),
              "targets": [r.get("Target") for r in results], "scanner": report.get("Metadata", {}),
              "vulnerabilities": [v for r in results for v in r.get("Vulnerabilities") or []]}, sort_keys=True))
        for result in results:
            for finding in result.get("Vulnerabilities") or []:
                if finding.get("Severity") in ("HIGH", "CRITICAL"):
                    blockers.append((finding.get("VulnerabilityID"), finding.get("PkgName"), finding.get("Severity")))
    sbom = Path(".p2-image.cdx.json").read_bytes()
    print("QASCP_P2_IMAGE_SBOM="+json.dumps({"sha256": hashlib.sha256(sbom).hexdigest(),
          "components": len(json.loads(sbom).get("components", []))}, sort_keys=True))
    if blockers:
        raise SystemExit("High/Critical findings block acceptance: "+json.dumps(blockers))


if __name__ == "__main__":
    main()
