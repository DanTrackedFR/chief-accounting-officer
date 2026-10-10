# Shared CAO execution contract 1.0

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
