# CAO MVP Build1 integration handoff

Baseline: ea19ee62c938dba06f3faf758a75e17a7da27e15.
Branch: mvp/local-cao-execution-contract. PR44; no merge authorization.

Install/use: docs/LOCAL-CAO.md. Python3.12+ standard library, Linux/macOS or WSL,
local durable filesystem. Clone/checkout, create ignored .cao-local, copy/edit
company-context.example.md, initialize/diagnose then open Claude Code. CLAUDE.md
instructs the client to discover capabilities, declare a supported accounting fact
family, invoke native accounting and deliver only curated public_result. Stable
company/entity/calendar/date keys and immutable request_id preserve Case identity.

The interface is local_cao.ExecutionInterface.call(JSON) or the equivalent stdin
CLI. interfaces/CAO-EXECUTION-CONTRACT.md and versioned request/response schemas
specify initialize/context/capabilities/start/status/questions/submit/execute/result/
resume/list/diagnose. Envelope IDs and workplan are operational metadata, not
accounting conclusions. Production flags alone do not establish execution capability;
actual native review/knowledge/applicability gates still decide.

A finance user provides execution dimensions in Markdown and controlled native
reviewed workpaper JSON with actual source inventory, evidence and independent
review records where the owner requires them. Claude can construct operation
envelopes, but cannot certify accounting evidence or fabricate reviewer fingerprints.
Company narrative/policy references remain user assertion, never auto-promoted
CompanyMemory truth. URLs are inert metadata. Free-text narrative conflicts need
human clarification; there is no semantic contradiction detector for all prose.

Fixed-assets depreciation EUR90,000 and AP accrual EUR9,600 are real native
calculations from existing explicitly synthetic workpapers. local_cao/examples/
cli-proof.json records fresh-process CLI execution, durable restore and retry parity,
plus revenue-without-contract and prepayment-without-reconciliation refusal. It
explicitly records Claude Code unavailable; owner must still run the documented
live-Claude prompts. Do not claim CLI proof is a live conversational-client test.

Input staging is immutable private files; existing schema3 SQLiteStore is the only
durable accounting state/memory store. Native Scope/Period/Case identity, currentness,
source validation, lifecycle, dependencies and journal ownership remain unchanged.
Retries after publication load native state without owner execution. Pending reads
never compute staged evidence. An empty execution preview may later accept first
evidence with the same identity. A partial checkpoint retains its unresolved work.
Replacement evidence cannot overwrite a reviewed version; the native sealed
CORRECT/REWORK integration is not exposed in this bounded facade. No journal
posting, approval service or CompanyMemory promotion endpoint exists.

Build2 can reuse operation envelopes, identities, context parsing, dynamic metadata,
public output, safe errors, staging and native durable resume. Add intelligent
evidence gathering/iteration using native Intake and exact qualified replacement
bindings. Do not build another planner/lifecycle/database. Real PDF/XLSX/DOCX
extraction needs a separate reviewed adapter; current normalized input is not binary
parsing. Live model inference, qualified broader scope selection and authenticated
accounting governance remain future work.

Future hosted Python service wraps the same transport-independent interface. Existing
TrackedFR Express obtains real user/company authorization, validates limits, calls
an authenticated HTTPS adapter, and consumes curated results. Hosting/authentication/
queues/remote services are not implemented here. Do not put accounting calculations
or native policy authority into Express. The requirements in architecture/
TRACKEDFR-CAO-FINANCE-CONTEXT-REQUIREMENTS.md extend existing finance_context; source
inspection must establish actual database column mappings. Preserve TrackedFR
onboarding/preferences ownership and CAO approved-position/currentness ownership.

Independent QA report: architecture/CAO-MVP-BUILD1-INDEPENDENT-QA.md. Release results
and exact tested source hashes: local_cao/release/release-regression.json.
All 3,050 distinct repository tests and seven validators passed locally; 25 authored
and 30 independent tests are included. Two deterministic fresh-process CLI proofs
are byte-identical. Completion report records the final gate status. Exact final-head and
readiness-triggered Actions are recorded on PR44; do not infer CI PASS from a local
count or from another SHA. Specialist PRs27/42/43 were neither modified nor merged.
