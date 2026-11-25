# GRC and compliance — REV-06

Reviewed repository: ManeaAlShabrain/QASCP · branch: main · commit: `4592eb230fadebb828c8b7d3b7972c6bd1aec012` · date: 2026-11-25, Asia/Riyadh.

AI-assisted review only; virtual specialties do not represent actual independent people.

Result: **Blocked for formal P1 acceptance**. QAR-001/002/003/005; QAR-008 improvement. No formal regulatory compliance or certification conclusion is issued.

The 17-governance-ID register is structurally linked to verification procedures and product mappings. The 15-entry source register distinguishes authority, edition, rights, access and applicability. Coverage tables explicitly describe capability associations rather than adopted clause-level controls. This separation is appropriate for P1.

| Topic | Assessed evidence | Disposition |
|---|---|---|
| Accountability | GOV-004 requires actual people and separation of implementer/reviewer/owner/regulatory authority | AI roles and owner account do not fulfill it; QAR-001 |
| Risk management | T01–T12 define impacts, mitigations and planned evidence | Actual owners and residual-risk decisions missing; QAR-002 |
| Clean-room/provenance | ADRs and notes attribute original choices to project requirements; dependencies have proposed provenance/license tables | No external proprietary implementation found in inspected source; original-design assertions are not an exhaustive originality proof. Independent adoption/license/advisory review remains unverified. |
| Regulatory source identity | 15 entries, including NIST editions and selected QCB/NCSA observations | Several editions/amendments/rights are pending. P1 backlog permits explicit pending gaps; their existence alone is not a legal-compliance failure. Qualified reviewer disposition is still missing. |
| Privacy | Purpose/minimization/classification, encrypted storage, scoped access, retention/deletion/legal hold/restore are planned | Actual entity/data/deployment context is not provided. No universal retention timer or Qatar applicability ruling is inferred. |
| Evidence management | Exact-SHA CI, source manifest, historical negative controls, stage record and immutable links | Strong technical traceability; approval is distinct and absent. |
| Exceptions | REL-001 forbids waiver of mandatory checks/isolation/audit/obligations | No risk acceptance or exception was issued by this review. |

## Fresh external sample and limits

On 2026-11-25, the official [NIST CSF 2.0 page](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20) and [SP 800-218 v1.1 page](https://csrc.nist.gov/pubs/sp/800/218/final) were reachable and supported their source identity/edition labels. The official QCB AI PDF request returned 502 and the QCB cloud PDF timed out. These access errors do not prove missing or withdrawn regulation and do not validate the prior cached PDF observations. No fresh origin binary/hash, amendment completeness or legal applicability was established. Detailed observations are E08.

ISO/IEC 27001/27002/42001, NIST AI RMF/SP 800-53, OWASP ASVS/SAMM, PCI DSS, CIS and SOC 2 can inform later scoped checks only where adopted and relevant. This repository does not provide evidence of certification to those schemes, nor does P1 require inventing an implementation/control matrix for every named standard.

Required next decisions: assign actual qualified security/architecture/bilingual/regulatory reviewers, review permitted pending-source gaps against exact scope, assign risk owners, resolve findings, and obtain authorized phase exit on a fresh reviewed revision. Repository-only AI assessment cannot replace these acts.
