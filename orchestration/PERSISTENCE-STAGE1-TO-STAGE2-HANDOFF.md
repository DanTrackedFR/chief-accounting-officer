# Durable Case Stage 1 → Stage 2 handoff

Stage 2 starts from the owner-integrated Stage 1 main, after PR38 review/merge.
Do not build a parallel accounting or lifecycle engine. Start from actual live
main and the native runtime contracts, not a quoted historical SHA.

Read persistence/CONTRACT.md, PERSISTENCE-STAGE1-INTEGRATION-HANDOFF.md,
PERSISTENCE-STAGE1-INDEPENDENT-QA.md, PERSISTENCE-STAGE1-RELEASE-REGRESSION.json,
DURABLE-CASE-COMPANY-ACCOUNTING-MEMORY-HANDOFF.md and accepted Stage4 handoffs.

Stage1 gives CheckpointStore/SQLiteStore schema1, exact immutable checkpoint
revisions, per-version source snapshots, native sealed intake archives linked to
Cases, complete private governed state, optimistic revision conflicts, atomic
transactions and deterministic new-runtime restoration without accounting/journal
execution. Historical receipt labels remain original observations; native version
currentness still determines qualification. Restoring never issues journals.

Future Stage2 must complete restart-safe invalidation, selective re-execution,
closed/reopened Period governance, legitimate correction workflows, exact-once
journal selection and interruption recovery. Stage1 persists the native state and
validates its references; it does not coordinate interrupted owner execution or
posting release. A committed checkpoint cannot recover external economic actions
without explicit evidence and appropriately governed transaction boundaries.

Use existing CAO.correct/selective_reexecute, VersionedExecution/VersionRegistry,
CaseRegistry/PeriodRegistry, native receipt qualification and scoped journals.
Qualified preview evidence must remain durably linked to the actual committing
session. Preserve committed immutable histories when extending a checkpoint.
Do not interpret a successfully loaded CLOSED status as permission to release
journals after dependencies have changed. Native owners retain all accounting
recognition/measurement/FX/consolidation/framework/statement authority.

Schema changes need explicit registered transactional compatibility steps and
permanent migration/failure tests, retaining historical source/result bytes.
No speculative schema migration exists in Stage1. Checksums are not signatures;
Company namespaces are not authentication or authorization. Synthetic approvals
remain synthetic. No encryption-at-rest or distributed transaction claim exists.

Company-memory candidate proposal/approval/promotion/retrieval belongs to Stage3;
full durable integration flagship belongs to Stage4. Neither starts in Stage2.
