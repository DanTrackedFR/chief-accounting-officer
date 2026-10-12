# Durable dependency, rework and recovery: verified reconstruction

Verified live main: `d202e910e17de559d908df478939ce10042e41db`.
PR38 is merged as `2f79018b7f9a0a8ff39fb7ebfebf9dfdbafaafd3`.
No existing durable Stage2 branch/PR was found. Government Grants draft PR27
(`phase-3/government-grants-assistance`) is separate protected work.

## Actual boundaries

`runtime.CAO.run`, `correct`, `selective_reexecute`, `_refresh_versioned` and
`public` are the ordinary execution, correction, rework and delivery routes.
`versions.VersionedExecution` owns typed Dependency edges, exact receipts,
topological execution, invalidation and current journal selection. Its native
`VersionRegistry` owns immutable ResultVersions, per-version source snapshots,
currentness and supersession. `cases.CaseRegistry` refreshes qualified Case state;
`periods.PeriodRegistry` authorizes execution and synthetic reviewed reopening.
`scoped_journals.allocate_scoped` delegates gross-line economic allocation to the
existing CAO allocator. None of these authorities will be replaced.

`persistence.state.snapshot/restore`, `evidence.retain/validate`, and
`store.CheckpointStore/SQLiteStore.save/load` preserve the entire native session.
Schema1 uses immutable checkpoint/object rows, transactional head update and
optimistic expected revisions. Restoration is read-only: no accounting,
invalidation, closure or journal selection is executed.

## Missing continuation contract and integration seams

Stage1 recovers the last committed snapshot only. Native publication includes its
predecessor in version identity, so blindly repeating correction can create new
history. Correction publication/invalidation and selective rework are in-memory
operations until save. There is no prepared operation identity, durable outcome,
lost-ack deduplication, uncertain external-action marker, or durable journal
selection receipt. Partial rework cannot reuse the original native plan blindly.

Stage2 will coordinate native operations as deterministic units beginning from an
exact durable prepared checkpoint. Crash recovery discards uncommitted in-memory
work and replays the whole authorized native unit, including original reviewed
sources and seals. Upstream correction and downstream selective rework remain
separate durable units. A transaction will couple outcome checkpoint and operation
commit; lost acknowledgement will load that outcome instead of rerunning it.
Optimistic revision checks prevent obsolete workers publishing over newer work.
Schema2 will add narrowly scoped operation records/events with transactional
schema1 migration, preserving all original historical checkpoint bytes.

## Protected boundaries and proposed proof

Recognition, measurement, FX, conversion, elimination and statements remain native
production-owner authority. Evidence qualification uses actual retained sealed
intake in the committing session; a preview is not an approval substitute. Exact
Scope/Case/Period/calendar/framework/currency/version/source and OPENING versus
COMPARATIVE contracts remain authoritative. Native closed-period authorization is
required. Closure requires current ordinary Case prerequisites. Internal journal
selection is durable and idempotent; no external posting connector or external
exactly-once claim is introduced. Unknown external outcomes fail closed for
explicit reconciliation.

Executable acceptance will reuse accepted Stage4 native accounting: separate
processes establish a qualified baseline, restore, commit reviewed upstream
revision and exact selective invalidation, interrupt rework, restore and replay
only its graph-selected consumers, retain unaffected identities and historical
conflicts, requalify journals and ordinary public COMPLETE/CLOSED. A separate
unresolved control remains partial. Permanent fault, evidence, identity, currentness,
concurrency, migration, journal and public privacy attacks plus fresh independent
review, deterministic seeds19/941 and the full live-workflow regression gate are
required before readiness. Stages3/4 memory promotion/integration remain future.
