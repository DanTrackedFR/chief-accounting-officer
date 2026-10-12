# Durable Case Stage 2 → Stage 3

Start only after owner integration of Stage2 PR39. Verify actual live main and all
committed handoffs; do not use a historical quoted head if main has advanced.
Stage3 Company Accounting Memory & Controlled Promotion is NOT implemented here.

## Interfaces to preserve

`SQLiteStore.save/load` retain Stage1 expected-revision, exact native restoration,
complete immutable history, strict corruption/schema/type checks and namespace
boundaries. `prepare(case, company_id, company_context, expected_revision, intent)`
records exact native CORRECT/REWORK/REOPEN/CLOSE_PERIOD/SELECT_JOURNALS semantics.
`recover(company_id, case_id, operation_id)` returns latest native Case plus private
operation record, head revision and `outcome_current`. `operation(...)` reads private
status from one read snapshot; `abandon(..., reason)` only withdraws uncommitted pure
native operations. BLOCKED needs separately qualified evidence; UNCERTAIN needs
external reconciliation and cannot automatically repost. See persistence/CONTRACT.md.

Schema2 registers transactional exact schema1 migration. Checkpoint wire contract1
is unchanged. Original checkpoint bytes, sealed source inventories, reviewed packs,
result IDs, version/source fingerprints, receipt bindings and temporal identities
must never be rewritten. Native successor publications require complete rework
history. Checkpoint reverse operation bindings, append-only event transitions and
native outcome provenance prevent hidden or contradictory recovery state.

Preparation permits only retained sealed evidence additions, not new uncommitted
accounting. Every committing correction/rework source must match an actual archived
native qualification in that same prepared session. Preview execution is neither
review authority nor transferable evidence unless its exact original bundle is
explicitly retained through existing intake/evidence boundaries.

Internal native journal inventory is idempotently selected for exact current
versions; committed retry never reruns allocation. Historical outcomes are explicitly
distinguished from latest state and must not authorize current release. Legal/Group,
conversion/reassessment, superseded versions and different entities/Periods retain
native economic boundaries. No external ERP posting or exactly-once guarantee exists.
Closed Periods require exact native reopening; reclosure requires current ordinary
Case/receipt prerequisites, not a retained historical CLOSED label.

## Company-memory seam and constraints

Company Context records remain governed supplied records, not approved reusable
company truths. Existing Context Observer candidates and exact per-version evidence
archives provide future candidate provenance. Stage3 must define proposal/review/
promotion/supersession/retrieval separately; restoration, successful native execution,
synthetic reviewer labels or COMPLETE/CLOSED alone never promote company memory.
Bind any future reusable knowledge to Company/Scope/Case/Period/effective interval,
framework/currency, original reviewed evidence and immutable result-version lineage.
Currentness and source/temporal qualification must be rechecked on reuse.

Native accounting owners remain sole recognition, measurement, FX, conversion,
consolidation and statements authority. Do not add a second graph/version registry,
parallel Case/Period lifecycle, journal engine or hidden balancing logic. Preserve
unrelated cases and exact topological selective work. Company-memory candidates may
inform work only through appropriately qualified governed intake and native owners.

Mandatory regressions: all Manufacturing, Diagnostic, Semantic/Data Intake, SaaS,
Treasury, Group and four multi-entity stages; distinct OPENING/COMPARATIVE lineage;
historical16/18 and current18/18; public native profit3/cash490; eight native journals;
Stage1 persistence attacks and read-only restart; Stage2 prepared/crash/lost-ack/
concurrency/history/uncertainty/closed-period proof; independent permanent defects;
seed19/941 deterministic audit views; full live-workflow suite and authority validators.

Trusted runtime and synthetic review are explicit assumptions. Native owners must
stay pure for deterministic replay. Authentication, encryption, external posting,
distributed guarantees and a product UI remain outside delivered scope. Full native
validation may be expensive; optimization needs permanent equivalence attacks and
must not weaken corruption/currentness/evidence checks. Stage4 full durable/company-
memory flagship remains a later stage, not this bounded continuation proof.
