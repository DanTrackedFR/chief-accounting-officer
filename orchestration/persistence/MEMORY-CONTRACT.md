# Company Accounting Memory contract 1

CompanyMemory is accessed through `SQLiteStore.memory()`. SQLite schema3 adds only
memory_events and memory_heads to the existing store. Exact schema1 migrates through
schema2, exact schema2 migrates transactionally to schema3. Checkpoint contract1,
all historical checkpoint/object bytes and Stage2 operation events remain untouched.
Mixed and future schemas fail closed. No second database, CaseRegistry, version
registry, accounting owner, or posting engine exists.

Each Company owns an append-only canonical event chain and revision CAS. CAPTURE
retains the exact existing Context Observer/Intake candidate, source Case checkpoint
revision/hash, sealed bundle IDs and exact same-Case/Scope immutable result versions.
Stable identity includes evidence lineage, never display names. Sources and native
currentness are rechecked inside one SQLite snapshot. Material/reusable intent is
required; observations remain PROPOSED. Missing/changed original evidence rejects.
Original semantic assertion cannot be relabeled. Inferred, assumed, disputed and
unresolved records cannot qualify reusable truth or approved policies.
Record attribute/value and observer context bind to the original candidate through
the canonical closed codec. Python-equal but differently typed values (for example
integer 1 and boolean true) cannot substitute. Immutable transitions, identities
and retry comparisons also preserve exact typed encoding. Contract/revision fields
require actual integers rather than boolean aliases.

TRANSITION requires explicit intent, exact prior state, subject/record/applicability,
current qualified evidence, reason, time precision and TRUSTED_CALLER_ASSERTION.
DOCUMENTARY and SYNTHETIC remain explicit; authenticated must be false. Documentary
APPROVED needs an exact canonical `memory_governance` source JSON column envelope
with subject/attribute/value/status/Scope/framework/Period/currency/jurisdiction and
DOCUMENTARY_ASSERTION convention. Negative/quoted/model text is not this envelope.
This is documentary assertion representation, not authenticated human governance.
Synthetic transition tests remain synthetic even when exercising APPROVED.

Knowledge statuses and current qualification are distinct. Historical approved
records may become stale, superseded or retracted. Effective bounds are inclusive;
unknown or approximate dates remain explicit. Exact fully covering effective bounds
are required for current reuse. Learned dates do not establish historical effect.
Exact registered Scope, entity, calendar, Period IDs, framework, jurisdiction,
currency and relationship IDs qualify. Group membership conveys no implicit policy
inheritance; explicit broad entity coverage is not yet supported. OPENING and
COMPARATIVE identities remain separate. Equal values never transfer provenance.
The source Case calendar and declared Scope reporting calendar must agree with
selected registered Periods. A relationship must bind its exact source Case
Period and selected target Period; merely supplying an existing relationship ID
does not establish the accounting role.

Overlapping incompatible candidates preserve both alternatives and block only the
affected subject/attribute. Confidence/newness never resolves conflict. Consecutive
nonoverlapping intervals and distinct dimensions remain separate. Duplicate current
APPROVED positions refuse. `resolve_conflict` requires exact successor provenance
and every superseded alternative's explicit intent, performs all transitions in
one transaction, preserves reciprocal lineage and permits exact lost-ack retry.
Retraction and ordinary transitions are also idempotent and revision-guarded.

Decision Register is distinct linked why-data: material proposed rationale, previous
and new position, decision date and implications. Capture cannot assert an approved
or implemented decision. `decide` records explicit governed documented/approved/
implemented/reversed/superseded history separately from Company Context status.
An implemented process decision supplies no accounting-standard authority.
The linked decision's new position must equal its Company Context typed value.
Material candidate wording such as "we decided", "going forward", "from next
month", "we changed", "instead of", "management approved", "audit asked" or
"implemented" produces only an unresolved proposed decision when none was supplied.
Its decision date stays unknown and a qualification question blocks promotion.
These phrases cannot establish rationale, implementation or approval by themselves.

Five stores are projections over one ledger: Company Context records; exact native
Case Library references; Artifact Library references to sealed bundles/checkpoints;
append-preserving provenance events; linked Decision Register. No blob upload or
independently editable Case truth. `history` returns all retained record events;
current `retrieve` separates qualified/refused/conflict/limitations from historical
lookup. `audit` is private. Hashes are integrity witnesses, not signatures.

`Intake.prepare_with_memory` feeds qualified contextual records into the existing
semantic preparation boundary. It requires exact native dimensional and date
qualification and returns exact version references. It never creates owner inputs
or ReviewedInputPacks. After the new Case is saved, `consume_context` atomically
binds exact memory version to exact consuming Case revision/hash, source revision/
hash and CONTEXT_ONLY use. Ledger restoration validates as-of-use governance,
provenance, currentness, conflicts and temporal applicability. Later invalidation
preserves historical consumption and current retrieval refuses stale support.
Exact inherited context references also travel through the sealed native context.
An observer cannot recapture an inherited attribute as independent USER_STATED
truth using unrelated evidence; a new candidate requires independent extracted
source evidence. Context reuse therefore cannot launder its original dependency.
No actual native execution dependency is manufactured by contextual reuse; any
financial input still needs the existing native reviewed source/owner/dependency
boundary. Thus context invalidation does not indiscriminately rerun accounting.

Company Memory publication is atomic in one local file. Native Case checkpoint
publication precedes referencing memory publication; a crash may retain a Case
without memory but never grants memory authority without its already committed
Case/evidence. No cross-service atomicity is claimed. Compound memory resolution
commits fully or rolls back. Reads/restoration never execute owners or promote.

Stored text is inert data. Ordinary public answers remain CAO.public and existing
allowlisted public DTOs; no private ledger/bundle/source/governance route is public.
Trusted runtime, local durable fsync/locking, file/backup protection remain host
assumptions. Authentication, authorization, encryption, external posting and full
Stage4 integration are outside this Stage3 foundation.

Stage4 bounds repeated native reconstruction with a transaction-local cache.
Its key includes Company, root Case, exact resolved checkpoint revision and
current head inside the same SQLite snapshot. The first encounter performs full
native restore and operation integrity validation. The cache is cleared before
final memory-write ledger validation and on commit or rollback; later retrieval
or correction always validates native state afresh. It is neither persistent
memory authority nor a substitute for source, receipt or currentness checks.
