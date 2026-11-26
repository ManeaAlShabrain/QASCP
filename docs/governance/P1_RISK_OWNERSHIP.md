# Risk Ownership & Residual Risk Register — QAR-002

P1-V02/04, GOV-004, REL-001; existing Issue #14. Prepared 2026-11-25.
The [machine-readable register](P1_RISK_OWNERSHIP.json) contains every requested
field for T01–T12. It supplements, and does not rewrite, the threat register.

Confirmed internal accountable owner (RISK-DEC-001, 2026-11-26): **Manea Mohammed Saleh Al-Shabrain**, GitHub
**ManeaAl-Shabrain** (the organization is ManeaAlShabrain). Identity is a project
attribution, not a verified legal identity, professional qualification or a
banking/regulatory delegation. The [owner decision](decisions/RISK-DEC-001.md) confirms internal responsibility only; no residual risk is accepted.
All residual ratings remain unassessed and no risk is accepted. No production
mitigation is credited as implemented. Internal ownership cannot accept a bank's,
customer's, licensor's or regulator's obligations. T12 needs qualified regulatory
authority before any deployment applicability or external compliance statement.

| Risk | Asset | Likelihood / impact (inherited, needs review) | Confirmed internal owner / residual decision |
|---|---|---|---|
| T01 | Tenant API, registry and graph | Medium / critical | Manea, internal project only; confirmed under RISK-DEC-001 / unassessed, not accepted |
| T02 | Pooled DB sessions, caches, jobs | Medium / critical | Manea, internal project only; confirmed under RISK-DEC-001 / unassessed, not accepted |
| T03 | Observation/import boundary | High / high | Manea, internal project only; confirmed under RISK-DEC-001 / unassessed, not accepted |
| T04 | Resource identity and source bindings | Medium / high | Manea, internal project only; confirmed under RISK-DEC-001 / unassessed, not accepted |
| T05 | AI retrieval/evidence | High / high | Manea, internal project only; confirmed under RISK-DEC-001 / unassessed, not accepted |
| T06 | Proposal/approval/executor | Medium / critical | Manea, internal project only; confirmed under RISK-DEC-001 / unassessed, not accepted |
| T07 | Assurance dependencies/history | Medium / high | Manea, internal project only; confirmed under RISK-DEC-001 / unassessed, not accepted |
| T08 | Audit, objects and exports | Medium / high | Manea, internal project only; confirmed under RISK-DEC-001 / unassessed, not accepted |
| T09 | CI and validation wheels | Medium / critical | Manea, internal project only; confirmed under RISK-DEC-001 / unassessed, not accepted |
| T10 | Graph query and queues | High / high | Manea, internal project only; confirmed under RISK-DEC-001 / unassessed, not accepted |
| T11 | Backups, roles and evidence | Medium / critical | Manea, internal project only; confirmed under RISK-DEC-001 / unassessed, not accepted |
| T12 | Applicability reports and UI | Medium / high | Manea, internal project only; confirmed under RISK-DEC-001 / unassessed, not accepted |

Assignment is confirmed for internal scope only. Remaining owner review must scope
the applicable asset and mitigation, review likelihood/impact and residual evidence, name
acceptance authority and record a dated decision tied to the exact candidate.
For a permitted lower-risk deferral, include compensating control, owner, expiry
and explicit approval under REL-001. Mandatory isolation, audit and applicable
obligations cannot be waived. No expiry or approval date is invented here.
Owner assignment is now confirmed. Unassessed residual risk and missing reviewed risk dispositions remain P1 blockers; this assignment does not close QAR-002.
