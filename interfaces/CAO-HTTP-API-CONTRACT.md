# CAO HTTP API 1.0

Current merged-build note: the foundational operation tables below describe Build1/
Build2A. Additive Build3 investigation/document/native correction/rework operations
are authoritative in `CAO-CONTEXT-EVIDENCE-DOCUMENT-CONTRACT.md`; Build4 acceptance
and TrackedFR mapping are in architecture/CAO-MVP-BUILD4-BUILD2B-HANDOFF.md.
No memory promotion or authenticated reviewer endpoint is introduced.

Python 3.12+, POSIX, standard library. Base path `/v1`. JSON request/response;
Content-Type must be `application/json`. Maximum body 2,000,000 bytes, native
maximum depth12/10,000 entries. Duplicate keys, nonfinite numbers, unknown fields,
unknown versions and unsupported operations reject. Request schema:
`hosted_cao/request.schema.json`; job schema: `hosted_cao/job.schema.json`.
Native accounting envelopes retain `local_cao/response.schema.json` and the stricter
public-output allowlist. No raw accounting or checkpoint endpoint exists.

| Method/path | Body or headers | Response |
|---|---|---|
| GET /v1/health | public | 200 process health, api_version1.0 |
| GET /v1/readiness | public | 200 usable operational store/worker; 503 unavailable |
| GET /v1/version | public | 200 service/api version |
| POST /v1/operations | shared1.0 envelope | 200 native operational response; 422 safe native refusal |
| POST /v1/jobs | execute envelope; Idempotency-Key | 202 accepted or same job on retry |
| GET /v1/jobs/{job-id} | scoped authentication | 200 job projection and terminal native accounting result |

All private endpoints require exactly one `Authorization: Bearer SECRET` and
`X-CAO-Company: STABLE_COMPANY_KEY`. Host configured credentials bind caller_id
to an explicit allowed company set and unique private workspace. The header selects
only among those permissions. Express must resolve company membership from Supabase
before choosing the credential and company header. Never forward browser credentials
or browser assertions directly. No service identity certifies reviewer approvals.

Operations: initialize, capabilities, context, diagnose, start, status, questions,
submit, result, resume, list. Execute is only asynchronous via /v1/jobs. Envelope
requires contract_version1.0, company_id matching the authorized header, operation.
Start additionally requires request_id/objective/target_family. Case operations
require case_id. Submit requires exactly one evidence object or staged_file_id.
Optional route must be an existing public_output.ROUTES member. No other fields.

Evidence uses the exact shared native workpaper subset. No automatic certification,
extraction, fetching or policy promotion. `staged_file_id` is 1–80 ASCII letters,
digits, underscore or hyphen. Host provisions COMPANY_WORKSPACE/staged/ID.json;
regular bounded JSON files only. Caller cannot supply evidence_file or any path.
File bytes remain private and are never served by this API. Symlinks at any ancestor
reject. Source qualification, fingerprints and entity/period bindings remain native.

Future source exchange metadata (TrackedFR-owned, not an implemented qualification
endpoint): company_id, provider, document_id, document_version, content_sha256,
entity_id, period_start/end, qualification_status. Values must refer to actual
private-storage object versions. Qualification status is informational until native
reviewed input evidence verifies it; service authentication never changes it.

Jobs have id/company_id/case_id/state/attempts/created/updated/api_version. State is
ACCEPTED, EXECUTING, SUCCEEDED or FAILED. SUCCEEDED means the requested operational
attempt finished. Inspect `accounting.execution_state`, lifecycle_state, durable,
currentness and public_result before displaying accounting completion. BLOCKED and
PARTIAL can legitimately accompany SUCCEEDED. A non-durable blocked preview is
retained only as the exact public operational outcome; it is not a saved Case.
Durable results are always restored from the latest native checkpoint, preserving
STALE outcomes. A failed result restoration remains a safe accounting.ok=false
response; never render it as current/complete.

Idempotency is company-scoped and immutable. Same key/exact canonical envelope
returns the same job; changed request returns409. Acceptance binds context/staged
input hash. Changing evidence before execution fails closed, requiring a new key.
Native checkpoint recovery takes precedence: a committed Case is restored without
owner calls, including lost acknowledgment. No valid checkpoint permits replay of
only the same initial pure request. Corruption/invalid storage fails rather than
replaying. Different job keys for a committed Case reuse native revision/journals.
No external journal posting or distributed exactly-once guarantee exists.

Artifact contract: Case ID, checkpoint_revision/currentness and native curated
public_result are references for TrackedFR rendering. The API does not invent memo,
workpaper, citation or downloadable source files. TrackedFR may render the returned
allowed calculations/journals/guidance/open_items into documents and retain the
reference binding; it must not treat those files as new accounting authority.

Errors:400 invalid_request;401 unauthorized;403 forbidden;404 not_found;409
conflict;413 payload_limit;422 native safe error;503 unavailable. Messages are fixed,
never exception strings, paths, source content or credentials. HTTP200/202 alone
never means complete accounting. Responses include Cache-Control:no-store and
X-Correlation-ID. Logs contain generated correlation/job IDs, status and durations;
no bodies, headers, objectives, evidence, company narrative or exceptions.

Single host/one service process/one worker; durable local POSIX disk and fsync.
Global worker lock rejects a second live worker using the same job root. Native
workspace flock/CAS protects accounting. Thread locks serialize company API access.
A reverse proxy must supply TLS, header/request time limits and rate limits. Direct
Python HTTP is for trusted local development/private network behind that proxy.
No CORS/browser API, public internet exposure or production deployment supplied.
Graceful SIGINT/SIGTERM stops acceptance, drains HTTP then finishes active work.
Hard process kill leaves EXECUTING jobs recoverable on next startup.

## Additive profile 1.1 — optional review mode

The 1.0 wire version remains supported. Host JSON configuration may explicitly set
`"allow_prepared_unreviewed": true`; defaults false and requires a real boolean.
This enables the shared local profile documented in CAO-EXECUTION-CONTRACT.md.
`start` accepts `review_mode: "prepared_unreviewed"` only for `machinery` and
`supplier_cost`. Subsequent operations inherit immutable mode, and any supplied
mode must match. `/v1/jobs` still executes the same native Case path. Mode changes
cannot reuse a formal Case, immutable request or idempotency binding.

A SUCCEEDED operational job may deliver a durable partial native result with
SUPPORTED accounting, SUFFICIENT evidence and SYSTEM_PREPARED provenance.
Consumers must read all three dimensions and retain specific unresolved issues;
never equate job success, currentness, user Finalised or supported arithmetic
with formal review or posting authorization. No named independent accounting
reviewer is required for this bounded profile. Actual source controls and all
substantive accounting/evidence restrictions still apply. Reviewer records in
submitted/staged evidence reject. Host-disabled reads/execution reject safely.

## Profile 1.2 HTTP integration

Trusted host configuration adds `allow_presumed_user_sources: false` by default.
Enabling it requires `allow_prepared_unreviewed: true`. Start with explicit
`source_assurance: presumed_user_provided` and `review_mode: prepared_unreviewed`,
submit the source Case under the selected facts family, then use existing /v1/jobs.
The Case-level source assertion, optional policy_elections and ordinary AP matching
rules follow CAO-EXECUTION-CONTRACT.md and source-case.schema.json. Transport,
authentication, persistent Case and job ownership remain unchanged.

Assurance is immutable and included in the structured Case cycle. Full descriptor,
source rows, source attestation, source versions/hashes and class assumptions are
bound at job acceptance. Explicit request/row assurance changes reject. Restart
and exact-key retries restore the same checkpoint without repeating accounting.
A missing case_id produces HTTP400 invalid_request with error.requirements naming
case_id. Malformed source Case bindings return the native HTTP422 invalid_request
and an actionable field requirement. Such deterministic errors are checked before
acceptance, not reported as “Service temporarily unavailable” job failures.

Render public_result.validation_requirements as Nally needs and
public_result.anomaly_report.findings as checks/exceptions; never render raw native
facts, policy metadata or source assertions. Supported rows may coexist with
UNRESOLVED population issues and native PARTIAL. NOT_PERFORMED is an unperformed
check, not a pass. No generic accountant referral, automatic posting, independent
source verification or review approval is inferred. The independent synthetic
27-row/10-invoice HTTP proof covers the corrected four addendum requirements;
TrackedFR owns its separate original-file acceptance.
