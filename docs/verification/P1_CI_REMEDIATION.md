# QAR-004 / QAR-008: checkout and validation-input correction

Base: main cc04fa6e82f0b53d75fd5d08e1a36f11fba5c4d2; P1 only.
Requirements: QASCP-GOV-003, QASCP-SEC-004, QASCP-ENG-002/003;
P1-V03; Issue #40. Implementer correction, independent review pending.

The earlier inline guard omitted --includes. Its six-case preparation was
insufficient; the independent audit's two false-clean results remain preserved.
The retained script now inspects names only, explicitly checks both direct and
effective included local configuration, rejects all local include/includeIf paths
(including inactive and missing ones), and rejects credentials, HTTP extraheaders
and SSH commands. Inspection/parsing/timeout failures deny success. Captured stderr
and configuration values never enter diagnostics. This conservative checkout
policy avoids later activation of a local authentication include. Global/system
configuration, environment credentials and a compromised runner remain outside
this repository-local claim. The script is a reviewed acceptance input, not a
sandbox against arbitrary malicious Python in a PR.

Primary reference: [Git config includes](https://git-scm.com/docs/git-config#_includes).
No external implementation was copied; behavior derives from QASCP's boundary and
the independently demonstrated Git behavior. Real temporary-repository regressions
cover direct helper/header/SSH keys, included keys, matching gitdir and gitdir/i,
inactive/missing includes, malformed config, nonrepository and inspection failure.
Ten local test methods passed on Windows/Python 3.14.4, zero skips. An initial test
used a nonmatching trailing-slash conditional pattern and failed six assertions;
the pattern was corrected and each conditional case now proves effective key
presence before checking denial. This was a test-fixture defect, not a passing
security result. Hosted full-suite evidence must bind the final candidate.

QAR-008 preparation downloads the exact pinned wheel closure, compares SHA-256 to
official PyPI release metadata over TLS, retains artifact URLs/license metadata
and performs an actual release-advisory lookup. Bootstrap output is evidence for
a reviewed platform-specific hash lock; it is not an independent trust root,
signed provenance, exhaustive SCA or permission to use every license. A later
candidate must install with --require-hashes before claiming hash enforcement.
The pinned checkout SHA, read-only workflow permissions and success-only gate
propagation are preserved. No ruleset or bypass setting is changed.
