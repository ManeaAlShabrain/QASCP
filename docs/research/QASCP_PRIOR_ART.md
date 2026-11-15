# QASCP market and patent reconnaissance

Search date: 2026-11-15. Scope: public product documentation and published materials surfaced by web searches, including Google Patents records. The search focused on case correlation, evidence freshness, policy-change re-evaluation, audit history, and replayable verification. PATENTSCOPE and Espacenet are identified for follow-up. This record contains no conclusion about patentability, claim coverage, or freedom to operate.

## Initial search terms

Queries combined patent and software-security terms such as “continuous compliance stale evidence,” “policy configuration change re-evaluation,” “asset control dependency graph historical,” and “replay-verifiable conformance.” Market queries covered SOC case correlation, exposure graphs, control monitoring, and evidence renewal. Results were screened by titles and descriptions, then selected claim and disclosure passages were checked. The search did not exhaust patent families, non-English publications, or national registers.

## Product overlap

| Source | Publicly documented overlap |
|---|---|
| [Microsoft Defender XDR](https://learn.microsoft.com/en-us/defender-xdr/investigate-incident-cases) and [Google SecOps](https://docs.cloud.google.com/chronicle/docs/soar/investigate/working-with-cases/explore-entities-and-alerts-investigation) | Cases, alerts, entities, affected assets, and investigative context. |
| [Microsoft Security Exposure Management](https://learn.microsoft.com/en-us/security-exposure-management/cross-workload-attack-surfaces) and [Tenable One](https://www.tenable.com/products/tenable-one/capabilities/exposure-prioritization) | Enterprise exposure graphs, asset context, and prioritized remediation. |
| [ServiceNow IRM](https://www.servicenow.com/docs/r/governance-risk-compliance/audit-management/continuous-monitoring.html) and [Drata](https://help.drata.com/en/articles/13417542-evidence-renewal-date) | Continuous control monitoring, evidence collection, and changes in control readiness when evidence ages. |

## Patent documents surfaced

Identifier examples below distinguish published applications (A1) and U.S. grants (B1/B2). Legal status and geographic coverage were not assessed. Summaries describe selected disclosed overlaps and do not define the legal scope of any claim.

| Publication | Selected overlap | Specific comparison to make next |
|---|---|---|
| [US12166788B2](https://patents.google.com/patent/US12166788B2/en) | Real-time compliance monitoring and identification of outdated evidence for controls. See claims 8 and 16. | Determine how evidence freshness and missing-evidence behavior relate to change-specific propagation and previously approved results. |
| [US12225033B1](https://patents.google.com/patent/US12225033B1/en) | Mapping regulatory rules, enterprise policies, assets and threat information. See claim 1 and the description of change-triggered checks. | Compare asset/policy change handling, representation of dependencies and the resulting scoped re-evaluation. |
| [US20260220652A1](https://patents.google.com/patent/US20260220652A1/en) | Continuous compliance using a common data model and detection of changes to device configurations and compliance policies. | Compare technical scope, source-change detection, dependency granularity and decision reconstruction. |
| [US20260332647A1](https://patents.justia.com/patent/20260332647) | Policy evaluation with asset/control dependencies, historical configuration states and simulation. See claims 1 and 12 in the published application. | Compare graph-based failure localization, handling of late and revised evidence, and use of previously approved assertions. |
| [US12645555B1](https://patents.google.com/patent/US12645555B1/en) | Replay-verifiable conformance records, evidence and policy versions, and conformance certification. See the independent claims and disclosure. | Distinguish verified assertions about tenant state, the as-of audit view, and when an operational re-evaluation is necessary. |

Non-patent references include [NIST OSCAL assessment results](https://pages.nist.gov/OSCAL/documentation/schema/assessment-results-layer/assessment-results/) for structured evidence and [Bazel Skyframe](https://bazel.googlesource.com/bazel/%2B/d167757e358b239f261afa41c0725ae74e86aee5/site/en/reference/skyframe.md) as an example of incremental re-evaluation over dependencies in a different domain. Recording audit evidence, expiring evidence, replaying decisions, and incremental recomputation each have precedents. The proposed behavior should be described and tested as a specific technical mechanism before any stronger claim.

## Next review

1. Describe the technical problem, input and output semantics, invariants, and measurable effect in a confidential disclosure record. Record contributors, dates, and external disclosures.
2. Search [WIPO PATENTSCOPE](https://patentscope.wipo.int/) and [EPO Espacenet](https://www.epo.org/en/searching-for-patents/technical/espacenet) by synonyms, IPC/CPC categories found in close records, patent families and backward/forward citations. Search dated papers, source repositories, vendor docs and standards. Record the exact searches, criteria, dates, and findings.
3. Compare each material element with the nearest earlier publications. Read independent claims, cited passages, family dates, and the relevant official registers. Separately evaluate novelty, inventive step, eligible subject matter, and freedom to operate for intended jurisdictions.
4. Review publication plans with a patent adviser before disclosing enabling technical details. Qatar's current published patent law lists computer programs in Article 4 and sets patentability criteria in Article 2. Consult the [Qatari legal portal](https://www.almeezan.qa/LawPage.aspx?id=2708&language=ar), [MOCI's IP department](https://www.moci.gov.qa/en/departments/intellectual-property-rights-protection-department), and the [MOCI inventor support initiative](https://www.moci.gov.qa/en/news/451). For naming, check the [WIPO Global Brand Database](https://www.wipo.int/en/web/global-brand-database) and relevant national records.
