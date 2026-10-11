# CAO MVP Build 2A completion report

Branch mvp/hosted-cao-service; PR https://github.com/DanTrackedFR/chief-accounting-officer/pull/45.
Baseline b3b6d3c7a57682985f66dc76985f99fe42b4dbd2. Implementation and targeted acceptance
are complete. Full local regression passes; exact-final-head Actions remain the final
release gate.
PR remains Draft until every gate passes. No merge or production deployment.

The separately runnable Python /v1 HTTP service wraps the unchanged shared1.0
ExecutionInterface. Operations, schemas, credentials/company isolation, durable jobs,
evidence staging and safe errors are documented in interfaces/CAO-HTTP-API-CONTRACT.md.
HTTP handlers contain no accounting methods. Native SQLiteStore remains the only
accounting Case/history/CompanyMemory authority; jobs.sqlite3 is operational only.

Company credentials use constant-time comparison, explicit caller identity and
host-configured company scopes. Express must authenticate users/resolve membership;
no browser credentials/company assertions or service-generated accounting approval.
Workspace selection is host-only; staged-file IDs cannot select arbitrary paths.
No URL fetch, binary extraction or raw private-output route is added. Logs carry
operational IDs/status/duration without request bodies, secrets or accounting data.

24 authored service,12 independent service and8 independent release-gate tests pass
(44 new distinct methods). Full repository regression:3,094 distinct tests,12 suites,
seven validators and git diff --check PASS; zero failures/errors/skips. Independent
review reports zero unresolved substantive findings. The missing blocked-job outcome
was reproduced/repaired/retested; company polling is serialized. Actual process crash
before and after native commit, concurrent duplicate acceptance, idempotent distinct
job retries, genuine native PARTIAL/STALE and fixed error/output boundaries pass.

Real supported synthetic fixed-assets depreciation EUR90,000 and AP accrual EUR9,600
execute through HTTP. Native public results match local delivery exactly; restart/
retry preserves revision1 and journal economics. Missing contract evidence refuses.
Fresh HTTP service processes under hash seeds19/941 produce byte-identical canonical
proof (timestamps excluded), SHA256 d34769d24cea1dd384ccda256e4010e87656263e903552ee0537f9d947f77d45.
Proof and acceptance records: hosted_cao/release/. Historical accounting artifacts
are not regenerated. Required roadmap update is append-only; the existing authorized
witness tool changes only its documentation SHA, independently verified.

Full regression actual distinct IDs/results/log hashes/exit codes are recorded in
hosted_cao/release/release-regression.json. Do not credit incomplete suites or reruns
as new tests. Source-controlled reports cannot self-reference their containing SHA;
final exact-head checks/readiness are recorded on PR45.
The original3,086-test full run is preserved as pre-readiness-full-regression.json.
Eight subsequently added independent CI-gate tests pass in an expanded44-test hosted
suite; all original Python sources match the full-run hashes. Reruns count once.
Readiness may reuse only a successful full orchestration run of the same workflow
and exact unchanged SHA with every required full regression step successful. API
errors, missing proof and cached-readiness chaining require a full rerun. Final gate results must be
confirmed there, not inferred from earlier checkpoint Actions.

TrackedFR Build2B handoff:
architecture/TRACKEDFR-CAO-BUILD2B-INTEGRATION-REQUIREMENTS.md. Build2B and the full MVP
are incomplete. No TrackedFR frontend/Express modifications are made here.

Single host/one worker, protected persistent POSIX disk, host-provisioned company
context, exclusive workspaces, TLS/reverse-proxy limits and backup/credential rotation
are deployment assumptions. No distributed queue, external exactly-once posting,
real authenticated accounting governance, native replacement rework/memory-promotion
API, live LLM, binary extraction, connectors, MCP or production deployment is supplied.
All specialist PR27/42/43 remain untouched and excluded. No merge occurred.
