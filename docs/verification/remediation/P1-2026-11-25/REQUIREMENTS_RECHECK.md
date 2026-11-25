# All 36 requirements: implementer corrective recheck

Base main cc04fa6e82f0b53d75fd5d08e1a36f11fba5c4d2, 2026-11-25; P1 only.
This is an updated scope/evidence map, not an independent audit or new grade.
Original RTM and finding states remain unchanged. Every ID and historical state
below was retained from the original 36 rows, then assessed for changed scope.
Fresh full candidate test links are in this package/PR; bootstrap results do not
stand in for later commits. All acceptance/reviewer decisions remain pending.

Evidence keys: C=CI guard/code regression; L=bilingual correction/glossary;
V=clean validation recipe and full candidate checks; S=wheel lock/provenance/SBOM;
A=20-row architecture register; R=12-risk ownership/residual register;
G=proposal-only #45/current effective human gate; T=19-package active tracker.

| Requirement | Historical audit status | Corrective evidence / scope rechecked | Remaining acceptance action |
|---|---|---|---|
| QASCP-GOV-001 | PARTIALLY VERIFIED | G/T: P1 Pending review; no P2, merge/closure not acceptance | Record actual exact-SHA exit after prerequisites |
| QASCP-GOV-002 | PARTIALLY VERIFIED | A/S/G: original decision provenance, wheel origin/limits; rights not adopted | Complete scoped provenance/license/adoption review |
| QASCP-GOV-003 | FAILED | C/L/V: guarded checkout, paired correction and protected PR process | Correct acceptance inputs and obtain actual bilingual/control review |
| QASCP-GOV-004 | MISSING | G/R/A: actual people/authority still absent; proposal not adopted | Assign actual people and record their decisions |
| QASCP-SEC-001 | PARTIALLY VERIFIED | A/R: trusted tenant context retained; runtime auth later P2 | Adopt design; P2 actual API/auth tests remain later |
| QASCP-SEC-002 | PARTIALLY VERIFIED | A/R: composite registry/RLS/non-bypass/pool invariants retained | Resolve registry/role disposition before P2 migrations |
| QASCP-SEC-003 | PARTIALLY VERIFIED | A/L/R: snapshot/provenance/query policy; no operational proof | Adopt boundaries and retain planned P2/P4/P5 regressions |
| QASCP-SEC-004 | PARTIALLY VERIFIED | C/S: include/header/helper/SSH failures now denied; values not logged | Fix exact guard and complete tool/security review |
| QASCP-SEC-005 | PARTIALLY VERIFIED | A: T1–T3 audit/outbox ownership proposal; actual DB tests later | Adopt transaction ownership; actual audit DB tests in P2/P5 |
| QASCP-AI-001 | PARTIALLY VERIFIED | G/A/R: production human/executor boundary unchanged; P4/P5 future | Review/adopt P1 design; test execution boundary only at P4/P5 |
| QASCP-AI-002 | PARTIALLY VERIFIED | G/R: untrusted AI and insufficient-evidence scope unchanged | Assign AI risk owner; retain exact future evaluation gate |
| QASCP-ENG-001 | PARTIALLY VERIFIED | C/L/V: human wording retained, full tool/setup failures explicit | Correct guard and documentation; rerun relevant cumulative checks |
| QASCP-ENG-002 | PARTIALLY VERIFIED | C/V: expanded real-Git and cumulative validation; old failures preserved | Retain expanded negative regression and fresh fixed-candidate evidence |
| QASCP-ENG-003 | PARTIALLY VERIFIED | C/S/V: byte lock, provenance, bounded advisory query and scoped inventory | Review adoption; fix guard; plan exact-artifact evidence at release gate |
| QASCP-OPS-001 | NOT APPLICABLE | NOT APPLICABLE to P1 execution: no release; P6 install/recovery gate retained | Retain P6 gate; no fabricated P1 operational test |
| QASCP-CMP-001 | PARTIALLY VERIFIED | G/L/R: 15-source pending rights/entity/edition gaps remain explicit | Regulatory owner reviews exact scope/rights and permitted pending gaps |
| QASCP-REL-001 | VERIFIED | G/T: no mandatory waiver, no self-acceptance or phase transition | Keep phase blocked; fresh approval only after remediation |
| PRD-01 | PARTIALLY VERIFIED | A: exact graph/registry/contract target decisions proposed, not adopted | Choose exact contract/ownership disposition; P2/P3 runtime later |
| PRD-02 | PARTIALLY VERIFIED | A/V: CommandReceipt prose corrected; observation receipt unchanged; T2 distinct from T3 | Adopt intake/import semantics; correct receipt descriptions |
| PRD-03 | VERIFIED | R/A: deterministic/contextual plan retained; no runtime score/model claim | P1 design requirement only verified; P3/P4 implementation later |
| PRD-04 | VERIFIED | A/R: dual time and selective/full assurance plan retained; P5 runtime | Retain P5 dependency-completeness and labeled-fixture gate |
| PRD-05 | PARTIALLY VERIFIED | G/R/A: exact production human approval unchanged; P4/P5 gated | Obtain design adoption; no operational execution authorized |
| PRD-06 | PARTIALLY VERIFIED | A/L: versioned snapshot wording corrected; historical service remains P5 | Resolve version adoption/translation; P3/P5 actual history later |
| PRD-07 | PARTIALLY VERIFIED | G/L: source/coverage remain design mappings, no certification | Actual regulatory source review, not invented certification |
| PRD-08 | VERIFIED | A: private/on-prem and proposed unmeasured targets retained; P6 later | P1 planning only; deployment testing at P6 |
| PRD-09 | PARTIALLY VERIFIED | L/A: paired blueprint/snapshot semantics; UI still P2/P5 | Correct technical translation; UI delivery remains P2–P6 |
| PRD-10 | PARTIALLY VERIFIED | A/S: original choices and dependency origin; independent rights/adoption pending | Complete actual provenance/adoption disposition |
| V2-P1-01 | PARTIALLY VERIFIED | T/G: earlier scope-only decision retained; no transfer to corrected exit | Do not transfer old decision to current exit; exact candidate disposition needed |
| V2-P1-02 | PARTIALLY VERIFIED | A/R/C/V: design and tools prepared; actual adoption/reviewer pending | Resolve adoption and record actual independent acceptance |
| V2-P1-03 | FAILED | L/G: paired full meaning comparison; source/regulatory gaps pending | Reconcile text and obtain real source/bilingual disposition |
| V2-P1-04 | PARTIALLY VERIFIED | C/S/V: fresh candidate checks; current rule and historical controlled block retained | Correct guard and independently accept exact candidate controls |
| V2-P1-05 | MISSING | G/T: authorized P1 exit NOT RECORDED | Obtain formal decision after evidence and fixes |
| P1-V01 | FAILED | L/V/G: structural check and semantic correction; substantive acceptance pending | Correct paired baseline and retain actual disposition |
| P1-V02 | PARTIALLY VERIFIED | A/R/G: 20 decisions/12 risks prepared; approval and ownership unresolved | Resolve exact target and actual review |
| P1-V03 | PARTIALLY VERIFIED | C/V/S: corrected acceptance input, full CI and rule evidence; independent control review pending | Fix and reverify changed guard; independent acceptance |
| P1-V04 | MISSING | G/T: Pending review; no formal exact-candidate exit or P2 | No P2 before authorized closure |

No row is promoted to independent VERIFIED FIXED. Applicable automated criteria
are checked by final CI; future API/DB/RLS/AI/executor/recovery/performance tests
remain explicitly out of P1 execution. Mandatory human/owner/source/adoption
decisions cannot be manufactured by tests or this recheck matrix.
