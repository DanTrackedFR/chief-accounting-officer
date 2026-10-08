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
