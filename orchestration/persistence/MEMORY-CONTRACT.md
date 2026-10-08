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
