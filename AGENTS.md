# QASCP development instructions

- Read docs/governance/ENGINEERING_GOVERNANCE.md and the active record in docs/verification/ before implementing or reviewing a stage change.
- Identify scope, acceptance criteria, and affected previously accepted paths. Run the current check with `python3 scripts/verify_foundation.py` and run the component and regression checks required by approved stage criteria as those checks become available.
- Record commands, results, commit SHA, and evidence links. Distinguish failed, unrun, missing, and inapplicable checks. Mark a stage ready for review only when evidence supports each applicable criterion. Record acceptance only after the named authorized reviewer approves the relevant version.
- Keep customer data, credentials, and production access outside this development workflow. Open scoped PRs and treat changes to acceptance criteria and CI as sensitive.
