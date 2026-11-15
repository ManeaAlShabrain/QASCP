# QASCP

QASCP: Unified Cybersecurity, AI Security & Continuous Assurance Platform.

Enterprise cybersecurity and AI assurance for Qatar's financial sector.

## Foundation setup

- [Engineering governance and delivery handbook — English](docs/governance/ENGINEERING_GOVERNANCE.md)
- [دليل الحوكمة والتنفيذ — العربية](docs/governance/ENGINEERING_GOVERNANCE.ar.md)
- [P1 architecture, threat model, contracts, and backlog](docs/architecture/P1_ARCHITECTURE.md)
- [Product design and independent development](docs/product/QASCP_PRODUCT_DESIGN.md)
- [Market and patent reconnaissance](docs/research/QASCP_PRIOR_ART.md)
- [Regulatory and engineering source register](docs/governance/REGULATORY_SOURCES.md)
- [Verification procedures](docs/verification/PROCEDURES.md)
- [Security reporting](SECURITY.md)
- [Stage verification record](docs/verification/README.md)
- [Codex instructions](AGENTS.md)

Run the current foundation check from the repository root.

```sh
python3 scripts/verify_foundation.py
python3 -m unittest discover -s tests -v
```

When initializing a new GitHub repository, select **Private**. Run the workflow on the default branch, then protect that branch with pull requests and the **QASCP Foundation Gate** required check on a plan that supports these rules for private repositories. Keep bypass access limited in accordance with the repository's governance. Treat workflow and gate changes as sensitive code review items.

To validate the GitHub rule once active, open a temporary PR containing a broken required documentation link, confirm the required check fails and blocks the merge, then repair the PR and confirm the check passes. Close the test PR. Record the real run links in the stage verification record.

The current gate checks foundations and documentation. Application, data-isolation, and cumulative regression jobs should be added as functioning components are delivered. The stage record requires separate review and linked evidence.
