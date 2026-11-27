# ADR-P1-ACCEPTANCE-001 — Concrete P1 architecture selection

Date2026-11-27. Status: **RATIFIED FOR INTERNAL DEVELOPMENT ONLY** under
[P1-EXIT-001 approval](../governance/decisions/P1-EXIT-001-APPROVAL.md).
The original prepared text and approval request below retain their historical
context; the accepted exact source and scope are recorded separately.
Authority to prepare: [P1-PREP-001](../governance/decisions/P1-PREP-001.md).
Requirements PRD-01/02/06/09/10; GOV-002/004,SEC-001..005;P1-V02.
These exact choices resolve the earlier20row proposal index into one coherent
candidate. They do not self-adopt architecture or authorize P2 before owner
ratification and separate review. Tradeoffs remain in the
[historical decision index](P1_ARCHITECTURE_DECISION_REGISTER.md).

| Decision | Selected candidate | Rationale / constraint | Implementation / acceptance boundary |
|---|---|---|---|
| AD01 | Successor0.2 at /api/v2; original0.1 /api/v1 is historical/unimplemented, never co-mounted | Distinct incompatible route; no supported original clients or implicit migration | Change successor server and canonical prose; preserve original bytes |
| AD02 | First runtime implements successor only; no additive mutation of strict original shapes | No claimed backwards compatibility with original candidate; later client support requires explicit adapter/deprecation/testing | No deployed client migration represented |
| AD03 | Freeze exact18-file contract manifest;16schemaIDs/versions retained; approval1.0 narrowing is unreleased selection, not backwards-compatible update | No deployed consumers; future incompatible adopted changes require new version/ID and migration disposition | Manifest hashes exact bytes; legacy consumer receipt excluded from graph dedup |
| AD04 | CommandReceipt after T2:201new/200authorized identical replay; ObservationReceipt remains distinct; neither proves graph completion | Domain acceptance and projection are separate durable states | Existing receipt contracts/prose retained |
| AD05 | Graph processing identity tenant/event/logical-consumer/consumer-version/purpose/input-version; atomic effect/receipt/checkpoint/audit | Replica identity does not suppress distinct events; no exactly-once transport claim | Real concurrent receipt uniqueness and replay tests requiredP2/P3 |
| AD06 | Preserve per-source claims; canonical values default unresolved without explicit eligible field grant | No globally trusted connector or vendor ranking; no inference from timestamp | Source-policy candidate v1 below; no production source enabled |
| AD07 | Eligible current registration and field grant, then explicit policy priority; equal priority conflict stays unresolved | Unmapped/expired/revoked grants contribute no canonical conclusion | Empty default grants; source onboarding must supply reviewed tenant/kind/field grants |
| AD08 | Scoped immutable source bindings with generation; mismatched resource rebind conflicts/quarantines | Never merge by display name; ordinary import cannot repair ownership | Separate audited authorized resolution needed before actual source enablement |
| AD09 | Retain accesses entitlement/observed_use qualifier and per-source provenance; filter before expansion/counts | Entitlement/use does not by itself establish compromise or excessive permission | P2subset owns/runs_as/accesses only |
| AD10 | Immutable claim0.1 versions/full-interval correction/terminal withdrawal; valid-time distinct from knowledge-time | No partial retraction/resurrection; historical service staysP5 | New identity required after withdrawal; retain lineage |
| AD11 | Immutable authorized snapshot selection with commit position+cutoff; reauthorize every page; no generation switch | P2history selectors denied; expiry/revocation force restart | Lab cursor MAC HMAC-SHA256, server-only256bit key,key_id allowlist,TTL300s,rotation24h,old key verify <=300s,immediate revoke; design only |
| AD12 | Composite tenant/id/kind registry FKs and deferred exactly-one domain-row check; immutable kind | Domain writers only; projector cannot create canonical resources | Registry+domain row commit or roll back together; actual PostgreSQL enforcementP2 |
| AD13 | Trusted membership/workload context, composite references, FORCE RLS and nonowner/non-BYPASSRLS runtime roles | Application filtering alone rejected; metadata-admin cannot access tenant rows | Separate migrator;transaction-local context;sequential/concurrent pool reuse testsP2 |
| AD14 | T1 intake owns observation/event registration+audit+outbox atomically | Unresolved references never auto-create asset/identity | Accountable internal package owner proposedManea; module invariant owner intake |
| AD15 | T2 inventory/identity owns resource import; claim domain owns relationship import; shared command key across families | Domain/binding/receipt/audit/outbox one commit; no nested independent commit | Crash/retry/digest-conflict/expected-version testsP2 |
| AD16 | T3 restricted projector owns projection/processed receipt/checkpoint/audit one commit, then acknowledgement | Fresh current authority before payload access; retry reads durable receipt | P2controlled outbox projector; durable broker/worker deliveryP3 |
| AD17 | LAB-GRAPH-01 experimental profile:two synthetic tenants,10k nodes/50k claims each; no production SLO | No measured latency/rate or accepted operational RTO/RPO claim | Lab query budgets depth<=2,edges<=200,nodes<=201,DB timeout2s,max20snapshots/tenant; benchmarks later |
| AD18 | ADR-2-001..008 selected in existing phase scope:modular monolith/PostgreSQL first,versioned outbox,OIDC,object evidence,localAI,observability | Conceptual architecture selection does not install/adopt dependency versions; split/search/graph stores need measured case | P2runtime dependency/license/security adoption separate;P3broker;P4AI;P5evidence;P6production |
| AD19 | This explicit review candidate + exact manifest supersedes unresolved choice index for owner ratification | Merge/old supersession prose alone never counts as a phase decision | Owner P1-EXIT-001 and four exact-candidate reviews required |
| AD20 | Internal reference metadata and original design only; all15external sources have bounded use dispositions | No banking applicability, certification, commercial reproduction or regulator authority adopted | Per-source holds remain before actual regulated/deployment/rights-dependent use |

## Versioned source authority policy1 — empty-default configuration

Grant identity: tenant_id, resource_kind, field_name, connector registration,
capability, binding_generation, effective_from/to, policy_version and approving
authority/evidence. A policy revision is immutable after activation; no editing
an old priority entry. Initially grants=[] and priorities=[] for every tenant.
Thus all unconfigured canonical fields remain unresolved, while attributable
source claims may be retained. P2 may implement this deny-by-default boundary;
populating an actual source's field grant requires current scoped authority.

For each field: authenticate/currently authorize source and capability; match
tenant/kind/field/current binding interval; discard ineligible claims from
canonical selection without erasing history; apply only explicitly configured
field priorities. Identical top-ranked values may agree; differing values at
equal authority remain conflicting, retaining evidence. A newer timestamp,
connector order, display name or AI output never resolves a tie. Resolution
is separately authorized and audited. No request can supply its own trust rank.

## Lab bounds and invalidation

The cursor algorithm/key/TTL/rotation and query budgets above are proposed
engineering limits for synthetic development, not benchmark results or an
enterprise cryptographic certification. Key bytes are generated/held outside
the repository; no actual key or token service exists in P1. Revocation and
current authorization take precedence over remaining token TTL. Snapshot
materialization may not hold a DB transaction across requests. A per-snapshot
cutoff and internal commit position bind membership, policy and graph generation;
restarts never silently switch those bindings. A reached quota returns a bounded
error, not an incomplete result labeled complete. Actual stress/concurrency/key
tests are mandatory before P2 acceptance.

## Compatibility and immutability

[Exact contract selection](P1_CONTRACT_SELECTION.json) records18file digests,
IDs and versions. Original API0.1 and receipt1.0 remain immutable history and are
not used for successor graph responses/dedup. No supported API existed, so this
is a first unreleased baseline selection; it does not assert semantic
compatibility with earlier strict candidate shapes. Approval1.0's prior narrowing
is explicitly frozen as the unreleased selected bytes, not described as a
compatible patch. A future incompatible change to an adopted contract requires
a new version/ID plus consumer migration decision and tests.

## Bilingual technical terms — 2026-11-27 correction

| English term | المصطلح العربي | Meaning in this decision |
|---|---|---|
| Canonical field value | القيمة المرجعية الموحّدة للحقل | Policy-selected field value; unresolved without an eligible grant or on conflicting equal-authority claims. This is separate from legal applicability. |
| Worker replica identity | هوية مثيل عامل التنفيذ | Identity of the executing instance; not part of the logical processing key. |
| Logical consumer version | إصدار المستهلك المنطقي | Version of the logical processing algorithm; included in the processing key. |

## القرار العربي

هذه اختيارات فنية محددة لمرشح المراجعة، وليست موافقة مالك أو تنفيذًا تشغيليًا.
يُختار عقد0.2 على /api/v2، وتبقى النسخة الأصلية0.1 على /api/v1 تاريخية غير
منفذة. تُثبت بصمات العقود وإصداراتها؛ لا يُدعى توافق الأشكال المختلفة أو
ترحيل عملاء لم يوجدوا. تبقى صلاحيات المؤسسة والموارد والصفوف والتدقيق ذرية.
تُقيد هوية المعالجة بالمؤسسة والحدث والمستهلك المنطقي وإصداره والغرض وإصدار
المدخل؛ ولا تشمل هوية مثيل عامل التنفيذ. وتُفصل إيصالات أوامر
الاستيراد عن استلام الملاحظة واكتمال الإسقاط.

تبدأ سياسة مصادر الحقول بإعداد فارغ يترك القيمة المرجعية الموحّدة للحقل غير محسومة؛
لا ثقة تلقائية بمورد أو موصل ولا أولوية زمنية لحسم التعارض. تُحدد مسؤوليات
T1وT2وT3 كما في الجدول، وتُمنع الواجهات التاريخية حتى P5. حدود اللقطة والمفاتيح
والحمل المذكورة مرشحة لمختبر اصطناعي، لا نتائج أداء أو موافقة إنتاجية.
تبقى حقوق المصادر وانطباقها الخارجي محجوبة وفق السجل؛ ويحتاج اعتماد التصميم
وخروج P1 قرار المالك على نسخة مراجعة محددة، بعد المراجعات الأربع والفحوص.
