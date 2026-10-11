# CAO Context, Evidence and Document Contract — Build 3

Additive contract1.0 operations are shared by local JSON and Build2A HTTP. Runtime
validation remains authoritative; intelligence/*.schema.json describes structured
context, document, inference, evidence-request and investigation records.

| Operation | Required fields | Effect |
|---|---|---|
| investigate | request_id, objective | Create/retrieve one native durable Case; target_family or validated interpretation/provider selects existing owner |
| document | case_id, event_id, document | Bounded ingestion; append immutable original/extraction; observations only |
| continue_investigation | case_id, event_id | Re-examine; optional validated interpretation; stable requests |
| investigation | case_id | Current operational view; no owner execution |
| submit | case_id, evidence | Existing immutable staging; Build3 evidence is proposal/pack/optional sources |
| execute | case_id | Existing native intake and accounting owner; no adapter approval |
| correct_investigation | case_id,event_id,node_id,reason,evidence | Existing native CORRECT; independently qualified replacement |
| rework_investigation | case_id,event_id,evidence | Existing native selective REWORK; empty evidence only for empty downstream execution order |

HTTP execute/correct/rework use POST /v1/jobs and existing Idempotency-Key. Other
operations use POST /v1/operations. Company authorization/workspace ownership and
job input binding remain Build2A controls. Poll the durable job; accounting COMPLETE
is distinct from job SUCCEEDED. Clients never decide qualification or post journals.

Context is versioned {version,company_id,items,selection?}. Every item names exact
entity, effective interval, key/value, source_ref/version/state. Selection names
entity_id and period_start/end. Non-default entities require their own framework,
jurisdiction, currencies and calendar; Group is no fallback. UK FRS102 uses existing
UK_GAAP owner contract. Markdown and editable APPROVED labels remain assertions.
Document references alone remain unqualified; only existing CompanyMemory governance
can supply approved accounting positions. Conflicts, unknowns and historical entries
are retained in the immutable Case snapshot. Materiality/threshold assertions are
visible inputs, not approved accounting policy. Framework selection conflicts block.

Document envelope names id/version/format/role/content_base64/metadata and optional
supersedes=id:version. Metadata binds company/entity/period/currency; optional native
scope/calendar/period identifiers, row_count, control_total, complete_population.
Formats: UTF8 CSV/text, XLSX, DOCX, text PDF. Full bytes/source SHA256 and extraction
SHA256 remain private in the existing Case checkpoint; sheet/row/page/paragraph refs
are native inventory fields. Public operational descriptors include parser warnings.
No parser output is reviewed accounting evidence. Supported bounds:1MB input,8MB
expanded archive,1000 archive entries,5000 rows,20000 cells,100 pages,1.5MB aggregate
Case investigation. Exceeding limits refuses the entire input, never truncates it.
Formula/error workbooks require independently recalculated controlled exports;
hidden populations remain included. Scanned/encrypted/unreadable PDFs, active PDF
payloads, embedded/macro Office payloads and unresolved DOCX revisions refuse safely.
DOCX body-only extraction warns that headers/notes/textboxes need reviewed exports.
PDF text warns about reading order. Neither active content nor document instructions
execute. Spreadsheet control totals/completeness assertions remain unreviewed.

Interpretation={family,claims,questions}; claims require real source_fields and
uncertainty; questions carry key/needed/why/source_fields. No approval or accounting
execution fields are accepted. Injected provider receives copied untrusted observations
and context, at most3 attempts; deterministic doubles are supported. No live model
provider, credentials, connector or identity system is shipped. Claude/TrackedFR
supplies its existing model response or a server-owned provider through the boundary.
The supplied response is validated again by CAO and remains INFERRED.

Evidence requests have stable Case/key IDs, needed/why/owner/scope/period,
source_status/blocking/source_fields/role/status. Repeated calls do not duplicate
requests or economics. All investigated active documents must bind in the separately
reviewed native pack. Arbitrary price claims or synthetic approval labels cannot
replace native evidence checks. Test certificates are explicitly synthetic fixtures.

Original documents and result versions remain after correction. New active evidence
makes prior economics STALE until native correction/rework completes. Replacement
legacy owner packs require a complete exact input snapshot and source manifest;
existing governed plans use native qualification. General downstream governed rework
requires each replacement's native source qualification; unsupported replacement
shapes fail rather than invent evidence. Resume replays neither owners nor journals.
Opaque operational references remain outside curated public_result; raw bytes and
private review packs never enter public output. Existing privacy boundary governs
accounting results and user-controlled request/observation strings.
