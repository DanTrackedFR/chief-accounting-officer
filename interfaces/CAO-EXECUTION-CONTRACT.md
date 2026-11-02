# Shared CAO execution contract 1.0

Current merged-build note: the foundational operation tables below describe Build1/
Build2A. Additive Build3 investigation/document/native correction/rework operations
are authoritative in `CAO-CONTEXT-EVIDENCE-DOCUMENT-CONTRACT.md`; Build4 acceptance
and TrackedFR mapping are in architecture/CAO-MVP-BUILD4-BUILD2B-HANDOFF.md.
No memory promotion or authenticated reviewer endpoint is introduced.

`local_cao.ExecutionInterface(workspace).call(request)` accepts/returns JSON-safe
values without exposing internal classes. `python -m local_cao --workspace PATH`
is the stdin/stdout transport. The host selects PATH; it is not a wire field.
No HTTP, MCP, network, model-inference, authentication or approval adapter exists.

Input envelope: contract_version (exact string1.0), operation, explicit company_id.
Unknown fields, duplicate wire keys, future versions, nonfinite numbers, excessive
size/depth and invalid stable IDs reject. Native intake bounds apply (2MB, depth12,
10,000 entries). Request schema: local_cao/execution.schema.json. Response structure:
local_cao/response.schema.json. The public-output code remains the stricter
accounting-content authorization boundary, not JSON Schema. Operation-specific
requirements below are enforced by code; examples use docs/LOCAL-CAO.md.

| Operation | Additional input | Governed behavior |
|---|---|---|
| initialize | none | Validate workspace Markdown and bind immutable company marker; initialize native SQLiteStore |
| diagnose | none | Validate context, native storage/memory audit, metadata and public boundary |
| context | none | Return execution dimensions as user assertions; never policy narrative or approval |
| capabilities | none | Discover actual Registry metadata/executor/fact adapter dynamically; gates still apply |
| start | request_id, objective, target_family | Immutable objective/scope request; native safe preview; stable native Case ID |
| status / questions | case_id | Latest committed native Case, or native staged preview; curated open_items and minimal workplan |
| submit | case_id; exactly one of evidence or evidence_file | Stage immutable inert controlled native workpapers; do not certify |
| execute | case_id | Native run for initial supported execution, then native validated checkpoint; retries load |
| result / resume | case_id | Load current durable native checkpoint; never execute owners |
| list | none | Enumerate selected company's local staged/executed Case references |

Optional route defaults tool_output. Any accounting delivery route must be an
existing interfaces.public_output.ROUTES member, including export. There is no
raw-result route. start/execute without results remain non-durable previews.
No general live LLM planner or binary extraction is promised. target_family is a
client-declared required fact family for objective coverage, not authorization
or a second accounting planner; unrelated evidence cannot replace it. Native facts
drive actual owner selection. Claude must declare an appropriate supported family;
this bounded runtime cannot independently validate the semantics of all prose.

Evidence is the native request subset: facts, handoffs, challenge_assertions,
journal_account_mapping, journal_pack_review, reviewed_scope_packs. facts use native
FACT_ADAPTERS. No governed_plan override, company-context approval, scope override,
executable callback or arbitrary-path source retrieval can enter this facade.
Evidence retains actual native source references, inventory/population, review and
fingerprints required by the relevant owner. The adapter never creates them.
Fixture-generated synthetic review records are explicitly test-only. Real source
qualification remains a native gate, not authenticated approval infrastructure.

Result envelope: contract_version, operation, company_id, ok; case operations include
case_id, lifecycle_state (native uppercase lifecycle), execution_state (native
complete/partial/blocked), checkpoint_revision or null, durable, currentness
(NOT_EXECUTED/CURRENT/STALE), public_result, and workplan owner/state rows. A CURRENT
checkpoint may be partial/blocked; current does not mean complete. Questions are
public_result.open_items, with explicit controlled source requirements for staged
requests. No private node/result/source/reviewer record enters accounting output.
Metadata identifiers are transport references, not accounting authority.

Configuration entity identity is a legal entity key, calendar and start/end form
native Period identity via compatibility_period, and Case identity uses native
case_identity plus immutable request_id cycle. Company ID is not a company name.
The explicit native Scope preserves functional/presentation currencies and calendar;
calendar fiscal start remains unknown under native compatibility normalization.
Build1 local scope is one legal entity and one bounded period per request; native
multi-entity orchestration remains unchanged and is regression tested, not replaced.

Idempotency: identical start request_id reuses immutable request, a changed objective
or scope conflicts. Identical submit returns existing acknowledgement; changed
reviewed data rejects. First execute publishes native checkpoint revision1 after
native validation; subsequent execute/resume/result loads the latest head without
owner or journal execution. A process crash before SQLite commit can replay the
same pure initial native calculation; no external side effects occur. Native
SQLite transaction/CAS owns durability. Host-local flock serializes facade calls,
releases automatically on exit/crash, and rejects competing calls safely. It is
not a distributed lock. Input staging files are not accounting state.

Immutable committed accounting cannot be replaced by a new submitted workpaper.
Native sealed Intake correction/recovery and CompanyMemory promotion are outside
the exposed subset in1.0. Preserve their original authority contracts; later
operations must compose SQLiteStore.prepare/recover and actual sealed evidence.
No approval, period closure, journal posting or memory promotion endpoint exists.

Errors: runtime_installation, invalid_request, invalid_context, workspace_boundary, identity_conflict,
immutable_submission, not_found, storage_failure, public_boundary. Responses are
safe fixed messages plus curated blocked public_result, never exceptions or raw
source content. Internal/private diagnostics are separate; no response claims
SaaS authorization. Host-trusted files can be modified by the local owner; hashes
and namespace checks do not stop a privileged malicious filesystem writer.

Future hosted adapter: authenticated Express selects a company-bound workspace /
storage namespace, validates identity/roles outside this contract, translates the
same versioned requests and returns the same public boundary. Add HTTPS, request
limits, access control, service credentials and revision-aware qualified rework
without moving accounting methods into Express. Version unsupported operations
explicitly. Do not use context/user edits to rewrite accepted CAO knowledge.

## Additive profile 1.1 — bounded system preparation

The backward-compatible wire envelope remains `contract_version: "1.0"`.
`start` may explicitly request `review_mode: "prepared_unreviewed"`; omission
retains formal behavior. Trusted host construction must independently enable
`ExecutionInterface(..., allow_prepared_unreviewed=True)` (CLI host option
`--allow-prepared-unreviewed`). The boolean defaults false and cannot be enabled
by wire evidence or company Markdown. Only `machinery` / fixed-assets and
`supplier_cost` / accounts-payable are supported. Investigation operations and
other packages remain outside this profile.

The selected mode enters the immutable request and native Case cycle identity.
The same request ID with a changed mode conflicts. Later submit/execute/read
requests inherit the staged mode; an explicit mode must match. Production Case
fingerprints bind the mode, current preparation implementation and canonical
knowledge document population. Hosted acceptance also binds immutable request,
context and staged evidence. No system record refreshes a formal reviewer seal.

Prepared evidence must contain only `facts` and the one selected fact family.
Client-supplied `knowledge_review`, `applicability_review`, `reviewer_signoff`
are recursively rejected, as are imported owner Cases and journal-pack authority.
The engine derives canonical populations/hashes and machine applicability from
the qualified Case dimensions. Source-population controls, actual source row
approvals, specialist handoff evidence, policy/life/component determinations,
reconciliations and evidence sufficiency remain required. These supplied source
controls are never created or relabeled as an independent accounting sign-off.

Initial applicability is ordinary commercial for-profit work with periods wholly
within calendar 2026. UK requires `FRS_102` / `uk_standard_edition: "2026"`;
AASB requires `aasb_compilation: "2026"` and integer Tier 1 or 2; US GAAP
requires `us_entity_type: "private_company"`. Here "2026" is a bounded governed
applicability selector for this profile, not a claim that the literal standards
publication has that title. NFP/public sector, FRS 101/105, public/regulated US
entities, declared regulatory overlays and additional policy elections require
separate assessment. Supported existing owner methods are unchanged.

A supported native result remains `status: "partial"`, with separate
`accounting_determination: "SUPPORTED"`, `evidence_sufficiency: "SUFFICIENT"`,
`review_provenance: "SYSTEM_PREPARED"`. Material accounting gaps block affected
calculations and produce UNRESOLVED/INSUFFICIENT. Wider unresolved objective
requirements remain visible even when an owner calculation is supported.
The existing SQLite Case checkpoint retains the partial result and original
source workpaper; there is no complete result version, formal approval, memory
promotion or authorized posting. Current means current checkpoint, not reviewed.

Public guidance leads with treatment, calculations, assumptions and proposed
journal implications. Machine provenance does not imply standards uncertainty.
Canonical claim sets are background guidance unless actual claim applicability
is established; this profile publishes no fabricated paragraph citations or
claim-by-claim application. Hashes, reviewer identities and raw source state
remain private. A machine-only compatibility sentinel is categorically rejected
in formal mode. TrackedFR user Finalised attestations must remain separate from
native accounting review authority.

Historical formal request IDs and fingerprints are retained through an exact
byte-checked additive dispatch/allowlist witness. Any non-enumerated common-code
change invalidates normalization; historical reference results are unchanged.

## Additive profile 1.2 — presumed user-provided sources

Requires both trusted host switches `allow_prepared_unreviewed=True` and
`allow_presumed_user_sources=True` (CLI `--allow-presumed-user-sources`). Both
default off and require actual booleans. Explicit start fields are
`review_mode: prepared_unreviewed` and `source_assurance: presumed_user_provided`.
Later operations inherit assurance; explicit fields must match the immutable
Case descriptor. No other owner or investigation route is opted in.

Submit only `facts` with the selected `machinery` or `supplier_cost` Case. Each
Case supplies `case_id`, exact entity/framework/jurisdiction/2026 period/currency,
`assumptions`, `source: {id, version, hash}` and `source_attestation` with
`authenticated_user_reference`, timezone ISO `timestamp`, `statement_version`
and literal true `represents_company_records`. This is a client assertion, not
engine-authenticated independent certification. No controls certificate, row
approver or specialist review memo is required or generated. All three accounting
review-record keys remain recursively forbidden.

Profile1.2 alone makes `policy_elections` optional, defaulting to no elections;
outputs disclose that none were assumed. Unsupported elections remain blocked.
Class assumptions are keyed by row `class`; each policy has exact `entity`,
`framework`, `effective_from`, `effective_to`, `policy_version` plus supported
accounting values. Explicit row values override applicable class defaults.
No company assumptions come from generic industry norms or unqualified memory.
Current Company Memory is not automatically converted into source authority.

See architecture/PRESUMED-SOURCES-DESIGN.md for exact numerical fields and
unsupported movement routes; interfaces/source-case.schema.json records shared
source/attestation prerequisites. Ordinary AP po_amount/received_amount matching
fields are optional. Missing checks explicitly report NOT_PERFORMED. Receipt
support remains essential for unbilled receipts and receipt-dependent recognition.

Every deterministic requirement has identifier, field_path, explanation, category
in `validation_requirements`. Anomaly findings include stable check_id, severity,
source_reference, row_references, explanation, optional observed/expected,
blocks_calculation and resolution. Table/row references are1-based. Missing or
blocked prerequisites aggregate without inventing dependent findings. Supported
individual calculations survive unrelated invalid rows/optional comparisons;
population status never claims independent completeness/reconciliation. Qualified
norms absent means outlier screening NOT_PERFORMED.

Results remain partial with SYSTEM_PREPARED and USER_PROVIDED_SOURCES provenance.
Private attestation, source hashes and optional approval records stay in the
native Case. Journals remain proposals and journal_entry_implications stays empty.
Nally needs and structured anomalies are curated through the same public boundary.
Malformed client submissions return invalid_request with safe field requirements,
including missing wire/source Case bindings, before numerical job acceptance.
Formal and Profile1.1 retain their original contracts and historical seals.
