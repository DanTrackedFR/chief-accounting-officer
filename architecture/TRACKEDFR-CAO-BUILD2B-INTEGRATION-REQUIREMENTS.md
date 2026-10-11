# TrackedFR Build 2B integration requirements

Build2A is the CAO backend; Build2B and the full MVP remain incomplete.
This repository does not contain TrackedFR source. The supplied March2026 setup
pack is background. React/Express/Supabase/private storage/PostgreSQL/Drizzle/chat/
company financial workflows are assignment-provided infrastructure, not code-inspected
paths. The Replit agent must inspect actual modules/tables/components before edits.
Do not invent column names or introduce a parallel accounting engine.

## Exact backend contract
Use interfaces/CAO-HTTP-API-CONTRACT.md and hosted_cao/request.schema.json,
job.schema.json plus local_cao/response.schema.json. Health/readiness/version are
GET/v1 endpoints; POST/v1/operations handles shared initialize/capabilities/context/
diagnose/start/status/questions/submit/result/resume/list; POST/v1/jobs accepts execute
with Idempotency-Key; GET/v1/jobs/{id} polls. All private calls require Bearer service
credential and X-CAO-Company. No browser calls Python directly. Native payload field
contract_version must be1.0. Authentication is not accounting approval.

## Minimal Express implementation
1. Reuse Supabase session verification and existing company membership/role guard.
Resolve canonical stable company UUID/key from server-side membership, never from
an unchecked request header/body. Map that key to the host-provisioned CAO workspace
and credential scope. Use dedicated server-only credential(s), scoped per company
or a narrowly configured group. A group credential trusts Express to perform its
membership check; compromise exposes its whole permitted set, so prefer narrow keys.
2. Add one server-side CAO client with timeout, size limits, fixed error translation,
correlation propagation and schemas. Keep base URL and credential secret server-only.
No API key in React, chat prompt, logs or Supabase public environment.
3. Add company-scoped Express routes for discovery/start/evidence/job submission/
polling/result. Persist operational CAO Case/job IDs and idempotency keys using the
existing PostgreSQL workflow record/migration conventions. Store native checkpoint
revision/currentness with rendered artifacts, but never reproduce Case lifecycle,
journal ledger, CompanyMemory approvals or calculations in Drizzle.
4. Start uses a stable request_id per accounting workflow, a declared supported fact
family and exact objective. Explicitly collect company/entity/calendar/framework/
jurisdiction/period/currency; host context provisioning remains an operator step in
2A. No HTTP context upload endpoint exists. Reuse prior finance-context requirements
at architecture/TRACKEDFR-CAO-FINANCE-CONTEXT-REQUIREMENTS.md.
5. Validate native workpaper evidence before forwarding but do not manufacture review
records. Structured JSON submit is the simplest implemented exchange. Private storage
raw PDFs/XLSX/DOCX are not extracted by2A. For staged exchange an operator-controlled
transfer writes bounded regular JSON at company workspace staged/ID.json; only opaque
ID crosses HTTP. No URL fetch or arbitrary path. A future automated private-storage
transfer needs its own reviewed adapter, and is not already implemented here.
6. Submit evidence before submitting execute. Persist Idempotency-Key before send.
On connection timeout/lost202 resend exactly the same canonical request/key;409 means
conflicting request, never randomize the key to conceal it. On restart resume polling
stored job IDs. ACCEPTED/EXECUTING are pending; SUCCEEDED is operational only. Read
accounting.ok, execution_state, lifecycle_state, durable and currentness. Show blocked
questions, partial work and stale warnings accurately. FAILED demands explicit safe
operator retry after diagnosis. New evidence after job acceptance is not that job's
input;2A refuses if its original staged-input binding changed.
7. Render only curated public_result. Use allowed calculations/journals/guidance/
open_items/limitations and public artifact references. Do not expose checkpoint,
reviewer seals, source bytes, internal source notes or native memory ledger. Persist
rendered document provenance to company/Case/revision/currentness. TrackedFR owns
PDF/document rendering, navigation/chat and presentation, not accounting substance.
Anthropic chat must quote/interpret governed output without inventing a completed
accounting response or new source citation.

## Existing UI reuse targets
Inspect and reuse the current company selector/membership guard, finance-context
onboarding/editor, financial workflow detail, private file picker/upload, chat
message/result cards, calculation/journal tables, document renderer and background
status/error components where present. These are semantic reuse targets; exact
component paths are unverified. Extend existing screens instead of creating another
accounting workbench. Present service progress separately from Case outcome.

## Source metadata
Keep actual company_id/provider/document_id/document_version/content_sha256/entity/
period/qualification_status in the existing private-document/workflow model or a
minimal migration. Verify actual schema mapping. This metadata is future source
exchange context, not a new2A API field or a native ReviewedInputPack. A label
qualified/reviewed in PostgreSQL cannot replace native evidence qualification.

## Required acceptance
Run Express-to-real-Python tests: unauthorized user; wrong membership/company;
credential expiry/rotation; cross-company known Case/job/file IDs; valid limits and
malformed requests; fixed-assets EUR90,000/AP EUR9,600 real synthetic outcomes;
exact local native public parity; missing contract/reconciliation refusal; timeout
before/after202 and lost commit acknowledgment; restart with stored jobs; simultaneous
same-key retries and changed-key conflict; no duplicate journals/revision; blocked/
partial/stale distinction; staged traversal/symlink rejection; source/private-note
redaction; no credentials/body leaks in both app logs; rendered artifact revision
binding. Test with synthetic workpapers only, never fake real approvals.

## Deployment assumptions
Private HTTPS between Express and a single Python service behind TLS/rate/body/header
limits; Linux/POSIX host, persistent protected local disk, one process/worker/job root,
exclusive service-owned company workspaces, backup/retention and credential rotation.
Replit frontend/Express deployment does not imply Python SQLite state is durable.
No distributed queue/multi-host support, live inference, binary extraction, ERP/Drive
connector, MCP, posting, authenticated accounting approvals, native replacement rework
or memory promotion API. One legal entity/period per provisioned workspace. Preserve
native history. Do not delete or regenerate historical accounting to repair integration.
