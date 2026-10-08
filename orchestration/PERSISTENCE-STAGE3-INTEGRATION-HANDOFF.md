# Durable Case Stage 3 integration handoff

Repository DanTrackedFR/chief-accounting-officer; branch
persistence/company-accounting-memory-promotion; existing PR40. Verified starting
main 92cbc713e4723ac4a14b73b3dd1f4835db1cab08, owner-authorized Stage2 PR39 merge.
The final release manifest and PR metadata identify immutable release SHA/Actions.
Owner integration only; do not merge or enable auto-merge. Stage4 remains FUTURE.

## Delivered architecture and five stores

`SQLiteStore.memory()` returns CompanyMemory in the SAME SQLite file. Schema3 adds
only a Company-scoped immutable memory_events chain and revision/hash memory_heads.
Exact schema1→2→3 and schema2→3 migrations run inside initialization transaction,
preserving original checkpoint/object bytes and all Stage2 operations. Checkpoint
contract remains1. CAS, integrity manifests, native read-only restoration, namespace,
closed-period, prepared-operation and recovery behavior remain authoritative.

One event/record contract supports five linked projections: Company Context describes
what is asserted and applicable; Case Library indexes exact native Cases/results;
Artifact Library references retained sealed bundles and checkpoint fingerprints;
Provenance preserves candidate, transition, decision and consumption history;
Decision Register separately preserves why, previous/new positions, rationale,
implications and explicit lifecycle. No duplicate lifecycle/version registry, general
blob store, semantic planner, accounting owner or journal engine was introduced.
See persistence/MEMORY-CONTRACT.md for exact interface and trust contract.

## Candidate, evidence and governance

Capture selects an EXACT existing native Context Observer or Intake candidate,
retains its original assertion/uncertainty/questions and source lineage, and requires
explicit material/reusable classification. Candidate identity includes Company,
Case, exact supporting source/result provenance, subject/category/dimensions and
effective interval. It is never derived from display name. All candidates start
PROPOSED; even a closed native Case or successful result confers no policy approval.
EXTRACTED candidates must match retained source field values; caller cannot relabel
inferred/model assertions as source facts. Supporting results must belong to the
exact native producer Case/Scope. Missing or rewritten sealed evidence fails closed.

Every governance transition requires explicit exact record/applicability/prior-state
intent, current native evidence qualification, trusted caller authority assertion,
reason and nonfabricated date precision. Documentary approval is a narrow canonical
source envelope; model prose, confidence, negative wording and reviewer names cannot
approve. SYNTHETIC and DOCUMENTARY remain visibly distinct; authenticated is always
false. This delivers documentary assertion representation, NOT authenticated human
governance, tenant authorization, accounts or role enforcement.

Material source wording such as "we decided", "going forward", "from next month",
"we changed", "instead of", "management approved", "audit asked" or "implemented"
triggers only a proposed linked decision when no qualified decision was supplied.
The decision date remains unknown and an unresolved rationale/authority/applicability
question blocks promotion. Source wording never proves approval or implementation.

## Currentness, applicability and conflicts

Record status is independent of current qualified reuse. Exact Company/Scope/type/
entity/calendar/Period/framework/jurisdiction/currency/relationship and covering
effective interval are checked. Learned date does not backdate effect. Unknown dates
remain unknown. OPENING and COMPARATIVE are distinct. This foundation is deliberately
exact-Scope and enumerated-Period: no implicit Group inheritance, broad entity
coverage, vector retrieval or fuzzy dimension substitution exists.

Incompatible overlapping candidates preserve alternatives and block only affected
subject/attribute context. Highest confidence/newest source never wins silently.
Nonoverlapping intervals and distinct applicable dimensions remain separate.
Explicit resolution requires a successor's complete predecessor links and each
alternative's exact governed supersession intent. The entire compound transition
is one SQLite transaction, with reciprocal lineage and exact lost-ack retry.
Retraction disqualifies reuse; superseded versions remain historical. Decision
states cannot be asserted approved/implemented on capture, and a Decision's new
position must agree with linked Company Context.

## Native intake and cross-Case consumption

`Intake.prepare_with_memory` uses current qualified records through existing
Company Context/Semantic Intake, checking exact supplied Scope/Period/calendar and
dates before context preparation. It returns exact record/version references.
It does not construct ReviewedInputPacks, financial source values, certifications,
owner overrides or journals. Missing/conflicted/inapplicable requested memory refuses.

After saving Case B, `consume_context` appends an exact memory-version consumption
bound to B's immutable checkpoint revision/hash and the supporting source checkpoint
revision/hash. Each event also retains its exact native qualification snapshot.
Restoration validates event-time governance, effective interval, native currentness,
consuming Case identity, conflicts and version history. Later correction does not
rewrite previous completed Cases or their historical consumption. Current retrieval
rechecks native result states and refuses stale/superseded support. There is no
actual native execution dependency created by contextual reuse; any later financial
input dependency must use native reviewed-source/owner/receipt qualification and
selective rework. Context invalidation does not rerun unrelated owners.

## Atomicity and safe output

Case checkpoint commits BEFORE a referencing memory event. A crash can preserve a
Case with no promoted memory; it cannot create authority without a committed Case
and valid evidence. Memory event/head and compound resolution publish atomically.
There is no cross-service transaction claim. Competing SQLite connections serialize
and obsolete Company revisions reject. Read snapshots/restore never run owners,
allocate journals, approve or promote. Historical events are immutable and validated;
unknown schemas/types, corrupt hashes, missing events and inconsistent links refuse.

Public delivery remains ordinary CAO.public and existing allowlisted DTOs. Ledger,
raw bodies, workpapers, private governance/provenance and operation payloads stay
internal. Text remains inert data. Host protection of local files/backups, fsync/
locking, trusted runtime and synthetic testing are explicit limits; authentication,
encryption, distributed consistency and ERP posting remain absent.

## Deterministic native proof and validation

`tests/generate_persistence_stage3_examples.py` uses seven distinct processes against
real SQLite. A native AP Case and sealed source produce an EXTRACTED systems
candidate. Fresh restart proves PROPOSED is not APPROVED. An exact documented
source assertion promotes it; Case B's intake consumes memory context and suppresses
a systems question, without rerunning Case A. Exact original provenance/version is
retained, unrelated Company reuse refuses, and owner/journal economics remain native.

A contradictory source blocks reuse/promotion until explicit atomic resolution.
Fresh Stage2 prepare/recover CORRECT retains reviewed replacement source, creates a
new immutable native accounting version, disqualifies the old supporting memory,
then native prepare/recover REWORK completes ordinary CLOSED/public complete. Old
memory is explicitly retracted and a proposed successor separately documented.
A separate unresolved conflict remains refused; unrelated subject context survives.
Final fresh restoration retains identical institutional history and exact past USE.

Eight references under examples/company-accounting-memory include full canonical
native checkpoints and lossless audit envelopes with SHA256. Decoder/reproduction
test verifies all hashes, restores complete native snapshots and exact roundtrips.
Fresh seed19/941 execution and byte comparison are recorded in the release manifest.
Original reviewer and authored failures are retained in tests/evidence/. No lost
execution is credited PASS. Independent QA disposition and distinct full-workflow
counts are recorded separately; intermediate reruns/subtests are never added.

Protected prior Manufacturing, Diagnostics, Intake, SaaS, Treasury, Group, four
multi-entity stages, ordinary accounting, durable Stages1/2, knowledge and public
boundaries are covered by unchanged full workflow regression. One native replacement
node comparator now uses the existing strict closed codec so a legacy native Decimal
node can be compared exactly; it changes no accounting output or authority. Historical
schema tests construct exact old tables and unsupported future version4 correctly.
Government Grants PR27 and unrelated accounting packages/approvals/mappings remain
unchanged; only the authorized roadmap witness is refreshed.

## Additional independent lineage controls

The linked Decision Register new position must match the Company Context typed value. Registered temporal relationships must bind the source Case Period and selected target; the source Case calendar, selected Period calendar and declared Scope reporting calendar agree. Intake seals inherited exact memory record/version/source Case/attribute references in native context. Observer recapture cannot convert inherited context into independent user-stated documentary truth. Context consumption and restoration reject substitution of equal-value memory with different planned provenance. These are authority controls, not authenticated identity checks.
