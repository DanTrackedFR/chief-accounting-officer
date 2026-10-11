# TrackedFR → CAO Finance Context requirements (Build1 handoff)

This is a requirements specification for a separate Replit implementation agent.
No TrackedFR source or database was inspected and no website/database/API was
modified. Verified owner-provided infrastructure: React19/TypeScript, Express/Node,
PostgreSQL/Drizzle, Supabase authentication/private storage, company-owned
finance_context, accounts/roles, workflow/run models, Anthropic/streaming chat,
financial workflows/reporting and Stripe. Exact existing columns, foreign keys,
constraints and API semantics require source inspection before implementation.
Do not replace finance_context with a competing onboarding database.

Native verified requirements are Scope/Period identities, framework/currency/date
qualification, immutable source/result versions, explicit company namespaces,
CompanyMemory states and authority/currentness boundaries. Fields below are proposed
extensions/mappings, not claims about existing TrackedFR schema names. Build1's
Markdown configuration supports one selected entity/period; richer hosted mapping
will require explicit native dimensional qualification, not arbitrary string labels.

## Ownership and synchronization

| Owner | Records | Authority |
|---|---|---|
| TrackedFR | Authenticated users, accounts, team association, roles, billing, preferences | Real identity and application access |
| TrackedFR | Editable onboarding, finance configuration, registered locations | Proposed/asserted configuration; not reviewed accounting truth |
| CAO | Governed Cases, source qualification, immutable result versions, judgments, reviewed positions, Case/Artifact Library, decision history | Native accounting evidence/lifecycle authority |
| CAO | Company Accounting Memory, accepted knowledge currentness/supersession | Governed institutional accounting knowledge |

Map an immutable TrackedFR company key to one explicit CAO company_id; preserve a
mapping version and never rename the key when legal/display names change. Derive
membership and authorization server-side from actual authenticated identity, not
client-selected company_id. Team/workspace identity must not come from an LLM.
User role/preference updates may change presentation, never approved policy.
Company configuration edits create a new context version/proposal; approved CAO
positions change only through native evidence-qualified successor governance.
Conflicts retain both alternatives and block only affected context/operations.

Synchronization is explicit, versioned and directional: TrackedFR sends asserted
context + original source refs; CAO returns public results and opaque Case references.
Qualified contextual reuse references exact native memory versions. CAO memory
projection back to TrackedFR is read-only with status/currentness/effective scope;
editing it creates a proposed change, not an update-in-place. Store proposed context
version, mapping version, consuming Case/checkpoint reference and native acceptance
or refusal reason. Do not claim distributed atomicity between PostgreSQL and SQLite.
Use a transactional TrackedFR outbox and idempotent eventual delivery in a future
hosted build; do not implement queues/HTTP/auth in Build1. If delivery is uncertain,
query existing Case before retrying economics. Never use a new request identity to
hide an ambiguous old execution.

## Field requirements

Every company context item should support field key, typed value or explicit unknown,
company owner key, scope/entity IDs, source state, original source reference/version,
attribution, effective_from/to, learned_at, recorded_at, supersedes and context_version.
Dates with unknown precision remain explicit; do not infer historical effect from
upload/edit time. Retain author identity from TrackedFR, with no implication that
editing authority is accounting review approval. Store evidence/document references
separately from mutable display URLs. A metadata URL is not retrieved evidence.

| Domain | Required/proposed fields | Validation / mapping |
|---|---|---|
| User | Authenticated user key; company/team memberships; role; responsibilities; preferred detail; language; framework familiarity; recurring responsibilities; timezone | User-owned preference profile. Server-approved membership. Never put these into approved company policy |
| Corporate | Stable company key; legal/display names; business description; industry; operating model; products/services; revenue model; geographies/jurisdictions; ownership/funding; group structure | Minimal business profile can be unknown; name never identity |
| Entities | Stable entity/legal-entity keys; display names; LEGAL_ENTITY/GROUP/SUBGROUP; parent/group relationships; active/effective dates; legal identifiers | Explicit native Scope records. Cycle/invalid parent checks. Group membership alone grants no policy applicability or elimination authority |
| Reporting | Framework per entity/reporting layer; statutory/group requirements; regulators; audit arrangements; external auditor; consolidation requirements | IFRS/US_GAAP/UK_GAAP/AASB supported codes; local/group differences explicit; no conversion inferred |
| Currency | Functional currency per legal entity; presentation currency per reporting scope; ledger currencies where relevant | ISO currency codes; FX/translation still needs separately reviewed rates, dates and method evidence |
| Calendar | Stable calendar ID; fiscal year start; year end; reporting frequency; close calendar; deadlines/timezone; period start/end, fiscal year/label/kind | Native FiscalCalendar/Period/relationships. Dates and calendar identity required; OPENING adjacent continuity distinct from nonadjacent COMPARATIVE |
| Materiality | Amount/currency; basis; scope; effective periods; investigation threshold; relative threshold; risk/age thresholds | Finite nonnegative typed decimal; unknown stays unknown; no default zero or silent financial materiality assumption |
| Finance organization | Team roles/locations; close tasks; preparer/reviewer responsibilities; process owner keys; review/release responsibilities; external providers; due dates | Authenticated organizational attribution in app; not a synthetic native reviewer signoff |
| Systems | ERP, billing, payroll, procurement/P2P, banking, expenses, CRM, equity, fixed asset, lease, consolidation/reporting, warehouse/BI; product/provider/version; owners; entity coverage; interfaces | Configuration and mappings; no connector authorization implied; do not store secrets in context |
| Policies | Revenue; ECL/instruments; inventory; PPE; leases; capitalization; FX; accruals; provisions; other applicable policies; document ID/version/location; scope/framework/effective dates/status | Actual policy references. Proposed/free prose does not manufacture policy contents or approvals |
| Positions | Existing accounting position reference; native Case/memory/result version; decision rationale reference; dates; alternatives; review status/currentness | CAO-owned authoritative position with read-only application projection. Mutable onboarding position is only assertion |
| Processes | Close deadlines; reconciliation/journal/reporting owners; controls; SOP references; external dependencies; handoffs | Scope/period-specific responsibility records; process decisions separate from accounting requirements |
| Risks | Known problem areas; prior errors/audit findings; unresolved reconciliations; historical risks; severity; affected entity/period; owner; source refs; resolution state | Preserve disputed/unverified hypotheses; no inference becomes established anomaly |
| Locations | Stable registered-location key; company owner; provider; directory/folder URL or path metadata; category; entity coverage; owner; purpose; effective dates; connector access status | Policies/contracts/close/TB/reconciliations/audit/journal/reporting/process folders; no retrieval claim until connector proves it |

A proposed entity table and versioned context-item collection can extend existing
finance_context without replacing existing values; determine actual table layout
only after inspecting Drizzle migrations and current models. Keep group membership,
reporting relationships and currency/reporting layers distinct.

## Evidence and state model

| Input state | Meaning | Native authority |
|---|---|---|
| unknown | Not supplied | Material questions remain open |
| inferred | Model suggestion | No confirmed/approved institutional truth |
| user_asserted / unverified | Onboarding assertion | Proposed contextual configuration only |
| document_backed | Document was actually retrieved; original version linked | Still requires native source and applicability qualification |
| proposed | Candidate position/change | Cannot overwrite accepted memory |
| confirmed / documented | Explicit supported confirmation/documentation | Must satisfy native status, scope, dates and provenance for reuse |
| approved | Governed accepted accounting position | Native transition/evidence rules; app edit cannot create it |
| conflicting | Multiple incompatible items | Preserve alternatives, require explicit resolution |
| superseded / retracted / stale | Historical or no longer supported | Preserve history, refuse current reuse where invalid |

UI labels must distinguish proposed TrackedFR context from native CompanyMemory
status. confidence is not authority. A signed document/link does not automatically
resolve framework/date applicability. Personal detail preferences never set
materiality, policy elections or accepted accounting positions. Do not translate
unknown into false, zero, empty approved value or a fabricated reporting date.

## Onboarding and validation

Minimum before useful conversation: authenticated company association, stable
company key, user role/responsibilities, legal/business profile and selected entity.
Minimum before governed execution: stable company and Scope/entity/calendar keys,
framework, jurisdiction, reporting start/end, functional/presentation currencies,
objective and required evidence/review source references. Missing optional audited
statements, policies or systems descriptions need not block all use; confidence
and questions change. Request the minimum material facts progressively.

Recommended optional enrichment: two years audited statements, chart of accounts,
group structure, systems architecture, current TB/management accounts, policies,
close checklist, audit findings, controls and organization chart. Keep their
original retrieval/qualification status. Do not imply generic binary extraction
exists in CAO; a later document adapter must generate controlled source envelopes.

Validate duplicate IDs, dates, intervals, inactive entities, invalid parent/cycles,
framework codes, explicit country/currency, finite decimals, materiality currency,
source/version existence and ownership. Group scope needs presentation currency;
legal entity needs functional currency. Require explicit framework conversion and
translation evidence before reporting a local result as Group economics. Validate
supersession is reciprocal and evidence-qualified, not just newest edit wins.
Context conflicts across same attribute/scope/effective window remain explicit.
Use independent tests for user/company isolation, missing values, typed equality
(bool versus1), narrative approval injection, expired/current mappings and conflict.

## Versioned CAO mapping

Proposed mapping identity: trackedfr-finance-context/v1 to cao-execution/1.0.
Map company key to company_id, legal entity to native Scope, selected calendar and
period to native identity, framework/jurisdiction/currency to scope. User assertions
stay outside approved native company_context records. Build1 accepts Markdown with
company/execution keys; later Express can map typed database records directly into
the same public contract. Do not transmit internal Python classes. Rich multi-entity/
period/memory context requires native structured Intake with exact scope and reviewed
bindings; Build1 does not claim that local operation exists. Do not serialize
unreviewed arbitrary finance_context fields as status APPROVED native records.

Each execution should record input context version and native checkpoint revision;
new context edits do not mutate that immutable historical accounting request.
If context conflicts with accepted memory, return actionable refusal/qualification
needs; do not silently choose the preferred UI value. Existing approved memory
remains governed by its original source and effective dimensions.

## Future source connectors

Google Drive/ERP connectors consume location metadata only after authenticated,
company-scoped access consent and source-level permission checks. Record actual
retrieval time, immutable provider document/export key/version, content fingerprint,
entity/period and original evidence reference, then invoke native inert extraction/
qualification. A Drive URL in onboarding establishes no access or examination.
ERP mappings must identify actual accounts/entities/periods and read scope; no
journal write authority is provided. Native reviewed source inventory and handoffs
must bind exact source versions. Keep credentials in secure connector storage,
not Company Context or model prompts.

## Backward-compatible migration acceptance

Inspect existing finance_context columns, ownership rules, Supabase/Express access
boundaries, workflow/run foreign keys and existing populated records first. Add
nullable/versioned fields or companion records; retain old IDs and original values.
Backfill only known attributes with legacy_user_assertion provenance; never bulk
promote approved states. Preserve unknowns. Migrate per company transaction with
revision check, audit entry and rollback route. Keep existing workflow/chat/reporting
reads functioning during rollout. New validation may ask for missing execution
fields without preventing existing non-CAO application use. Test duplicate legal
names, multi-company users, deleted memberships, stale onboarding edits and older
clients. Owners should review a real schema-to-requirement mapping before deployment.

Build2 can reuse stable mapping, operation envelope, public output and context
status distinction; hosted transport, real connector/document extraction, iterative
evidence gathering, authorization and authenticated accounting reviews remain future.

## Build3 implemented server contract

Map future finance_context to intelligence/context.schema.json. Entity-specific
framework/currency/calendar/Period must be explicit; IFRS Group context cannot override
UK_GAAP subsidiary context. Source_state APPROVED in editable onboarding remains a
user assertion; approved positions require existing native CompanyMemory governance.
Bind the immutable resolved snapshot to each Case; later onboarding edits apply to
new Cases. Expose conflicts/unknowns without client-side authority upgrades.

Use document.schema.json, inference.schema.json and evidence-request.schema.json;
interfaces/CAO-CONTEXT-EVIDENCE-DOCUMENT-CONTRACT.md defines additive local/HTTP routes.
Document originals/versions/dimensions remain server-bound observations; frontend
must display warnings and BLOCKED/PARTIAL states. Existing Anthropic integration may
produce structured interpretation, but CAO validates it and executes accounting only
through separately qualified native contracts. Execute/correction/rework use existing
Build2A durable jobs. Build2B/UI/connectors and authenticated accounting approval are
not included. See Build3 integration handoff for exact synthetic proof and limits.
