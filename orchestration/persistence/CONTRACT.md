# Durable Case checkpoint contract v1

Stage 1 persists the accepted governed runtime. It has no accounting, approval,
conversion, memory promotion, journal release or owner execution authority.
`CheckpointStore` separates the runtime contract from `SQLiteStore`.

## State and identity

A caller supplies its existing stable Company identity and governed Company Context
record population. No identity is derived from a display name. One checkpoint
contains a root Case and its entire native session: Scope hierarchy, fiscal
calendars and Period history, all Cases, Graph nodes, exact Dependency contracts,
immutable ResultVersions and complete versioned source snapshots, CURRENT/STALE/
SUPERSEDED registries, publication/invalidation/restatement history, historical
receipts, selective-rework records, runtime context/request and retained intake.
All Case dataclass fields and the registered private provenance fields are
included. Unknown runtime fields/types reject, rather than being silently dropped.

The native runtime previously retained only the latest node source. Publication
now additionally copies each source into `VersionRegistry.source_snapshots`.
Accounting outputs and version identity formulas are unchanged. Old live sessions
created without those historical payloads cannot be saved by guessing evidence.

Native legacy and governed-plan intake/replacement qualification retains original RawSource wire
order, sealed proposal/context/candidates/qualifications, complete ReviewedInputPack
and lineage, linked by exact private Case qualification references. Raw member order is preserved because native extraction uses it for
field identity; all other dictionaries use deterministic sorted encoding. Restored
bundles verify original payloads/extractions, seals, exact node bindings and full
source populations. Synthetic reviews remain synthetic. Missing qualified evidence
rejects. A caller qualifying in a preview session must retain those same qualified
bundles in the actual session before checkpointing; source declarations alone do
not substitute for evidence. `evidence.retain` copies an already sealed native
qualification and supplies no review/certification.

## Transactions and concurrency

SQLite schema version 1 has immutable checkpoint revisions, separately indexed
object payloads/hashes, foreign keys and an atomic head pointer per Company/root
Case. A complete checkpoint is written inside BEGIN IMMEDIATE / COMMIT with
synchronous FULL. Any failure rolls back all rows and the pointer. The caller must
supply an integer expected revision (zero for first publication). Interleaved
writers serialize at SQLite's file boundary; an obsolete expected revision rejects.
Readers use one deferred transaction and see committed state only. This is local
single-file consistency, not distributed or cross-service atomicity.

Readers verify exact SQL schema, user_version, quick_check, foreign keys, payload
SHA256, object manifest and checkpoint predecessor hash. Revision hashes detect
accidental damage; they are not signatures or authenticated approvals. A privileged
writer who can rewrite coherent data/hashes remains inside the trusted boundary.

## Encoding and restoration

The closed value codec supports JSON primitives, finite floats/Decimal, ISO date/
datetime and tuples. No pickle, eval, dynamic class loading or stored executable
callbacks. Duplicate JSON keys, noncanonical encodings, unknown types/fields and
future contract/schema versions fail closed. Native public calculation row order is explicit private provenance, so sorted
encoding does not reorder the final public response. Lists retaining historical/event or
native input order are never guessed/reordered. Registry populations are sorted
by exact identity during construction and canonical checkpoint generation.

Restoration uses native ScopeRegistry, PeriodRegistry.from_record, CaseRegistry,
Case, Graph/Node, Dependency, VersionedExecution and ResultVersion constructors.
It validates lifecycle history, dimensions, exact identity formulas, version
publication and stale/supersession history, original source/result fingerprints,
exact receipt bindings and completed-Case prerequisites. It does not call CAO.run,
accounting owners, journal allocation or Case closure. Stored statuses are retained;
invalid COMPLETE/CLOSED checkpoints reject rather than being silently demoted.
Historical receipts retain their original serialized qualification labels and remain
historical. The existing native validate_receipt still disqualifies a stale or
superseded producer version; equal values never refresh an old receipt.

Public delivery still uses CAO.public and interfaces.public_output. Internal
checkpoint data is private; no checkpoint object is a public response DTO. Stored
synthesis currentness and private provenance are retained, not regenerated.

## Schema evolution and recovery

Version 1 is the initial and only registered compatible schema. `migrate` is the
transactional compatibility entrypoint; current version is a no-op, unknown older
or future versions reject. Future stages must register explicitly reviewed steps,
run them transactionally and retain original checkpoint bytes/results/history.
No speculative future migration is implemented. Migration/init failure rolls back.
Repeated loads produce independent object graphs with the same canonical state.
Prior committed revisions remain readable; corruption is never silently repaired.
Recovery means reopening the last committed valid checkpoint, not finishing an
interrupted accounting operation. Stage 2 owns coordinated restart/rework and
interrupted journal-release recovery; Stages 3/4 own company memory/integration.

## Trust, confidentiality and operations

The application/runtime supplying Company IDs, qualified sources and approvals
is trusted. Namespace checks prevent substitution, not unauthorized access.
Authorization and authenticated preparer/reviewer separation are future work.
New database files use mode 0600; symlinks and in-memory databases reject. The
application must protect existing database files, parent directories and backups.
Source evidence can contain confidential accounting data. This adapter provides
no encryption at rest, secret management, remote database or background service.
Do not put credentials in runtime source payloads. SQLite rollback-journal recovery
assumes a durable local filesystem honoring fsync and locking. Back up a closed
store or use SQLite's consistent backup mechanism; do not copy a live file without
its transaction state. Backup scheduling, retention and external disaster recovery
remain the host application's responsibility.

## Stage 2 durable operation extension (schema2, checkpoint contract1)

The checkpoint wire contract remains1. SQLite schema2 adds immutable `operations`
plus append-only `operation_events` and a nullable deferred checkpoint foreign-key
binding back to its operation. Plain checkpoint reads validate marker populations,
event transitions and committed outcomes against native history; operation deletion
or contradictory returned plans/selections reject. Prepared selection hashes bind
the already-qualified native allocation into immutable operation identity. A registered transactional migration from
exact schema1 creates only those tables; original checkpoint/object payloads,
hashes and identities are untouched. Unknown/mixed schemas reject. Initialization,
migration and outcome failures roll back. Existing expected-revision semantics
remain authoritative.

`SQLiteStore.prepare(case, company_id, context, expected_revision, intent)` binds
an operation identity to Company/root Case, exact committed base revision/hash,
prepared state hash and complete native intent. Preparation may retain already
sealed reviewed evidence, but cannot smuggle uncommitted accounting state. Every
replacement source must occur in the actual prepared session's sealed evidence.
An identical preparation retry returns the original operation identity. Human
display labels are never sufficient identities.

`recover(company_id, case_id, operation_id)` loads a fresh prepared native runtime
for each uncommitted attempt. States are PREPARED, EXECUTING, COMMITTED, BLOCKED,
ABORTED and UNCERTAIN. No operation record means not begun. PREPARED has not executed;
EXECUTING is unresolved but safely replayable for the supported pure native units.
Native correction and full selected rework each form an atomic unit: intermediate
owner versions/invalidation are never a committed checkpoint. An upstream correction
commits before its separate downstream rework unit. Replay uses the exact original
reviewed inputs and deterministic native graph order. No arbitrary callback or
execution code is stored. The trusted host must not add side effects to native
owners while relying on this replay guarantee.

Native CORRECT/REWORK/REOPEN/CLOSE_PERIOD/SELECT_JOURNALS remain the sole authorities.
A writer lock spans outcome execution/publication; checkpoint head and COMMITTED
outcome publish in the same transaction. Competing recovery workers serialize.
An obsolete revision rejects. COMMITTED retries load the durable outcome and latest
head without executing owners or journal selection again. Returned `outcome_current`
distinguishes historical operation outcomes from the latest checkpoint; old
selection receipts are historical, never permission to release superseded journals.
Reads/deserialization do not resume accounting. `operation` exposes private durable
status; the prepared checkpoint still describes the previously committed accounting,
not an assertion that a pending correction completed.

Native qualification failure produces BLOCKED with no outcome checkpoint. The
caller may explicitly `abandon` a pure uncommitted operation and prepare separately
qualified evidence. Abandonment is durable; it is not an approval or accounting
result. Pending operations block uncoordinated saves and competing intents.
Native closure requires current ordinary CLOSED/complete Cases and current exact
receipt/version prerequisites, in addition to PeriodRegistry's native close route.
Reopening uses its existing exact synthetic reviewed Case/node authorization.
Historical closure and reopening records must extend, never replace, prior history.

SELECT_JOURNALS durably records the native gross-line allocation with exact immutable
versions. It is internal idempotent selection, not a posting ledger or an external
ERP call. Legal/Group, translation/reassessment and current/superseded boundaries
remain native. An UNCERTAIN_EXTERNAL marker binds the exact latest committed
selection and supplied uncertainty evidence. Recovery fails closed and blocks further
publication; explicit external reconciliation is required. No automatic repost,
external acknowledgement fabrication or external exactly-once guarantee exists.
This stage deliberately provides no posting/reconciliation connector.

Crash boundaries: before preparation leaves the original checkpoint; preparation
transaction failure leaves no intent/head; after preparation permits exact replay;
during owner execution, invalidation, selected rework, closure or journal selection
leaves EXECUTING and the complete prepared checkpoint; before/during outcome
transaction publication rolls back the whole outcome; after COMMIT/lost caller
confirmation returns the same committed operation on retry. Ordinary lifecycle
completion within selective rework is part of that same atomic unit.

All operation payloads, receipts, reviewed sources, selections and status histories
are private. Public delivery remains CAO.public; no operation DTO is a public answer.
The existing trusted-runtime, synthetic-review, local-file, confidentiality and
security limits remain unchanged. Stage3 approved company-memory reuse is absent.
