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

## Optional review execution profile 1.1

TrackedFR may expose an explicit system-preparation selection only where its CAO
host enables `allow_prepared_unreviewed`. Send `review_mode: prepared_unreviewed`
at start, retain the returned Case ID, submit qualified evidence without the
three top-level accounting review records, then use the existing `/v1/jobs`
flow. Scope is ordinary fixed-assets machinery and supplier-cost AP only; see
interfaces/CAO-EXECUTION-CONTRACT.md for 2026 framework/entity boundaries.

Render the accounting treatment and supported numbers first. Native partial
status is retained separately from accounting_determination, evidence_sufficiency
and review_provenance. Show precise material open items. A user may separately
attest Finalised in TrackedFR; store that attestation in TrackedFR with its own
identity/time and never mutate native accounting review authority. Journals are
proposals, and the native posting implication list remains empty in this mode.
Canonical packages are labeled background guidance; no source-verification or
applied-claim assertion is inferred. Private provenance remains in the Case.

## Profile 1.2 — corrected integration-probe contract

After explicit user selection, TrackedFR may send the Profile1.1 review mode plus
`source_assurance: presumed_user_provided`, only if the CAO host enables both
switches. Keep the same Case/job mapping and exact Idempotency-Key. Supply one
Case-level source_attestation with session-authenticated user reference, timestamp,
statement version and affirmative company-record assertion. CAO stores the fields
as client assertions; TrackedFR session authentication is not independent source
or accounting review. Preserve source id/version/hash and source Case identity.

Do not manufacture row approvers, independent population certificates, eligibility/
consumption memos or specialist handoffs. Supply real class accounting assumptions
with qualified entity/framework/effective window/policy version. policy_elections
may be omitted in Profile1.2; CAO discloses no elections assumed. Ordinary invoice
PO/receipt-amount matching fields are optional. Their absence is NOT_PERFORMED;
receipt evidence still matters for unbilled/receipt-dependent accounting routes.

Use validation_requirements (identifier/field_path/explanation/category) for Nally
needs. Preserve all aggregated requirements and anomaly findings. A malformed
wire Case binding is HTTP400 invalid_request; a malformed source Case binding
returns safe native422 invalid_request with error.requirements. Correct these
before job acceptance instead of treating them as infrastructure outages.

Render supported calculations, treatment, applied assumptions, proposed journal
implications and concise review/source status. Keep SYSTEM_PREPARED separate from
USER_PROVIDED_SOURCES. Native partial remains partial. Population restrictions
must remain visible alongside supported row calculations. No control/GL comparison
or qualified norm means NOT_PERFORMED; mismatches cannot become reconciliation
claims. Avoid serializing private source/user/approval metadata into findings.

The owner clarified that the original27-row register/10-invoice probe files belong
to TrackedFR and are not required engine release inputs. This engine release uses
explicitly synthetic representative fixtures through actual HTTP/jobs/restart/
idempotent retries. TrackedFR separately retests its original files and owns
application authentication, uploads/mapping, UI and commercial deployment acceptance.
See PRESUMED-SOURCES-DESIGN.md and the current execution/HTTP contracts for the
bounded ordinary machinery/invoice/accrual fields and unavailable specialist routes.

Render supplied class defaults separately from actual per-row applied assumptions,
including explicit user assumptions. An unusable optional outlier norm leaves the
check NOT_PERFORMED while supported calculation inputs remain effective. Do not
replace absent populations or wholly excluded rows with zero balance cards. An
invoice-only upload cannot establish zero accrued liabilities.
