# CAO MVP Build 2A integration handoff

Baseline b3b6d3c7a57682985f66dc76985f99fe42b4dbd2; branch
mvp/hosted-cao-service; existing PR45. DO NOT MERGE. Specialist PR27/42/43 are
excluded. One Python engine now supports the local Claude Code interface and
server-side HTTP callers. No TrackedFR code or production deployment is changed.

Start independently with `python -m hosted_cao` and host-selected CAO_SERVICE_CONFIG,
CAO_HOST/CAO_PORT. See docs/HOSTED-CAO.md and hosted_cao/config.example.json,
env.example. Protected config maps caller credentials to allowed company IDs and
unique provisioned workspaces. Express must verify Supabase users and company
membership before selecting the scoped service credential. TLS/private network,
proxy limits, protected durable POSIX storage and backups remain host responsibilities.
Rotation supports overlapping scoped keys during explicit graceful restarts.

interfaces/CAO-HTTP-API-CONTRACT.md, hosted_cao/request.schema.json/job.schema.json
and local_cao/response.schema.json define the exact API. GET health/readiness/version;
POST operations initialize/capabilities/context/diagnose/start/status/questions/submit/
result/resume/list; POST jobs execute with immutable company-scoped Idempotency-Key;
GET jobs/ID polls. Do not add a direct synchronous execute bypass. Native safe errors
and curated accounting responses are unchanged. A202 acceptance or SUCCEEDED job
never implies COMPLETE/CLOSED/current accounting. Show BLOCKED/PARTIAL/STALE accurately.

Operational journal jobs.sqlite3 retains request/fingerprint/input binding/state/
attempts and native Case references. It is not a second accounting database. The
worker first restores the authoritative native checkpoint on every unresolved attempt;
only absent checkpoints permit the same pure initial execute. Actual process-death
proof before/after native commit preserves one revision and no duplicate journal
amounts. No external posting/side effects are supported. Native corrupted checkpoints
fail closed. New keys do not override committed native accounting or immutable evidence.
Different inputs after acceptance require diagnosis and a new separately bound job.

Evidence is native bounded structured JSON or a host-provisioned opaque staged_file_id
within that company's staged directory. No paths, fetching, extraction or URLs.
Native review/qualification remains mandatory; credentials do not authenticate
accounting approvals. Public_result and Case/revision/currentness are the artifact
contract. TrackedFR owns rendering/chat/navigation and private storage; no new memo,
source citation, calculation or CompanyMemory position is authored by HTTP handlers.

Fresh-process HTTP proof: hosted_cao/release/http-proof.json. Synthetic fixed-assets
EUR90,000 depreciation and AP EUR9,600 accrual execute real native owners with exact
local public parity. Hard service restart and identical retry preserve checkpoint1.
Missing revenue evidence returns BLOCKED with no journals/checkpoint. Authored tests
cover actual kill boundaries and actual PARTIAL; independent QA persists genuine
STALE native state and verifies safe polling.44 distinct new tests (24 authored
service,12 independent service,8 independent release gate), counted once. Full
local regression passes3,094 distinct tests and seven validators. Independent report:
architecture/CAO-MVP-BUILD2A-INDEPENDENT-QA.md. Full repository release evidence and
exact tested Python hashes: hosted_cao/release/release-regression.json. Exact final
remote SHA/Actions and unchanged-head readiness must be verified in PR45 before
owner integration. A partial/in-progress evidence file is not a PASS.

Separate Replit agent specification:
architecture/TRACKEDFR-CAO-BUILD2B-INTEGRATION-REQUIREMENTS.md. Inspect actual TrackedFR
routes, membership guard, tables/components before edits; this repo has no verified
TrackedFR source paths. Reuse existing UI and context/workflow records; do not rebuild
accounting. Build2B/full MVP remain incomplete. One legal entity/period per workspace,
controlled supported workpapers only. No authenticated reviewer workflow, sealed
replacement-evidence rework/memory-promotion endpoint, binary extraction, live model,
connectors, distributed queue or multi-host deployment. Local standard-library HTTP
requires a production proxy. Preserve historical accounting and native history.
