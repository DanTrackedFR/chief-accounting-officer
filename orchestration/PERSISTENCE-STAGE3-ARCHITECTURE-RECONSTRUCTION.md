# Stage 3 architecture reconstruction

Verified 2026-10-08: live main `92cbc713e4723ac4a14b73b3dd1f4835db1cab08`,
Stage 2 PR39 merged at that SHA; Stage 1 PR38 already merged. No Stage3 branch
or PR existed. Government Grants PR27 remains open and protected.

Read Stage2 release/independent QA/integration/continuation, Stage1 integration,
durable-memory, intake and multi-entity Stage4 handoffs; persistence contract;
architecture memory/context/onboarding/case/roadmap and all seven memory schemas.
Historical structural schemas express semantics; actual merged runtime owns APIs.

Native CAO._observe appends PROPOSED supplied-context or OBSERVED request records.
Intake.prepare appends semantic PROPOSED context candidates with original assertion
status and evidence references; Intake qualification copies them into native Cases.
Neither path grants company policy approval. Sealed evidence bundles retain raw
sources, proposals, candidate populations, reviewed packs and exact lineage.
VersionRegistry owns immutable source/result snapshots and currentness; CaseRegistry,
ScopeRegistry and PeriodRegistry retain authoritative identity/lifecycle/temporality.
CAO.public and existing allowlisted DTOs remain the sole ordinary public boundary.

SQLiteStore currently schema2/checkpoint contract1: save/load expected revision;
prepare/recover bounded native operations; one atomic local transaction; exact
read snapshots; complete immutable checkpoint and operation history. Cross-Case
company memory is absent. Supplied Company Context is checkpointed input, not an
approved independently reusable institutional record.

Implementation direction: registered transactional schema3 extension in the SAME
SQLiteStore, Company-scoped immutable candidate/record/event history and revision
CAS. Five stores are projections over one memory ledger: context, native Case
references, retained artifact references, provenance events, distinct linked decisions.
Evidence qualification reads exact native checkpoints in the same transaction;
no duplicate Case/version registry, owners, posting, approval or semantic engine.
Explicit documentary/synthetic governance remains distinguishable; no authenticated
human governance. Promotion and retrieval recheck scope/time/framework/currency,
source/result currentness and contradictions. Historical consumption must retain
exact memory versions. Unknown dates remain unknown; effective and learned dates
remain separate. Stored text is data, never instructions or native financial input.

Release gates remain outstanding: implementation, permanent authored attacks,
separate independent reviewer, fresh-process cross-Case proof, deterministic seed
19/941 artifacts, full live workflow regression, validators and final unchanged-head
Actions/readiness. Stage4 remains FUTURE. Do not merge.
