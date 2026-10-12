# Build 4 → TrackedFR Build 2B acceptance handoff

TrackedFR implementation is not performed here. The older Build2A requirements
remain historical for transport/auth; merged Build3 and current execution contracts
supersede statements that binary intake, investigation and correction are absent.
No actual TrackedFR source or authenticated application has been evaluated.

Express must verify existing session/company membership server-side, map the stable
company ID to scoped service credentials/workspace, and send the same shared1.0
requests. React never calls Python or sees service secrets. Use current local/
HTTP/intelligence schemas and independently validate field/size/version boundaries.

Supported /v1/operations include investigate, document, continue_investigation and
investigation alongside initialize/discovery/submit/result/resume. Execute,
correct_investigation and rework_investigation use durable /v1/jobs with immutable
Idempotency-Key and exact input binding. Preserve original raw document identity,
version and metadata; private storage labels cannot qualify accounting facts.
Supported formats: bounded CSV/XLSX/DOCX/text-PDF/text. No OCR or formula recalculation.

Keep a company-scoped workflow→Case/job mapping and persist idempotency keys before
submission. Retry identical bodies/keys after uncertain acknowledgement. Poll the
existing job. SUCCEEDED means operational completion; native COMPLETE/PARTIAL/
BLOCKED and CURRENT/STALE are separate. Supply reviewed native packs explicitly.

Render curated public_result for accounting. Separately show requested evidence,
observations, warnings and unresolved qualification. Preserve generated artifact
Case/checkpoint/currentness binding. Do not expose native checkpoint/ledger/raw
source seals/internal diagnostics. Don't turn extracted prose into approved memory.
Native memory promotion/reviewer authentication is not an HTTP operation.

## Required real-application acceptance

- Execute Boreal-type unfamiliar agreement and source-linked questions, reviewed
  €31,920 original/€34,200 amended economics; preserve source/result histories.
- Run prepayments3,000→18,750; discover BC-20481 from movement, preserve −100 residual
  and blocked allocation review. Never render observational increase as a journal.
- Correct company/entity/framework/calendar/period selection; isolate Group from
  legal entity, functional USD from presentation EUR; no implicit FX conversion.
- Test wrong membership/cross-company Case/job/document IDs, source substitutions,
  prompt injection, unknown schema/limits, expired/rotated credentials and log privacy.
- Lost202/commit acknowledgement and app/server restart reuse stored keys/Case IDs;
  repeated requests cannot duplicate economics. Detect stale outputs/revisions.
- Actual authenticated preparer/reviewer roles/events and separation require their
  own implementation/acceptance; service authentication never supplies approval.

Private TLS proxy/body/header/time/rate limits, one POSIX service/worker, protected
persistent SQLite disk, backups/restore/retention/rotation/monitoring/incident response
and production load/operational acceptance remain prerequisites. No Replit deployment,
connector/MCP/external posting or distributed exactly-once is supplied. The commercial
MVP remains incomplete pending Build2B, live model/client and production acceptance.
