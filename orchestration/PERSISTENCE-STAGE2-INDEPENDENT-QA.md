# Durable Case Stage 2 independent adversarial QA

Reviewer: fresh separate agent context and detached worktree `stage2-review`,
initial reviewed implementation `67f28624681e010b1e42e81dbfb06c3b6280d1ee`.
Production files are never edited by this reviewer. Author remediation is copied
verbatim only after reproducing original defects. Reviewer permanent tests use
accepted native temporal fixture execution directly, independent correction and
journal intent construction, actual SQLite files, and separate worker processes.
No authored recovery-test helper supplies the reviewer baseline or attack results.

## Architecture reconstructed

The reviewer read native CAO correction/selective execution and public refresh,
VersionedExecution publication/invalidation/topology/receipts/current journals,
PeriodRegistry reopening/execution authorization/history, scoped gross-line journal
allocation, Case lifecycle, Stage 1 state/store/evidence contracts and accepted
Stage 4 temporal controls before implementation review. Actual new production
changes are `persistence/recovery.py` and `persistence/store.py`; native accounting
recognition, measurement, FX, consolidation and statement authority remain native.

Recovery replays a pure native unit from its exact prepared committed checkpoint.
The prepared intent includes reviewed source population and namespace/base hashes.
Execution and outcome checkpoint/event publication occur under SQLite's writer
transaction; interruption leaves prepared state and EXECUTING for deterministic
replay. This is atomic internal selection and checkpoint consistency, not external
posting. Uncertain external outcomes remain explicitly blocked; synthetic reviews
remain synthetic and checksums are not authenticated approvals.

## Finding register (historical entries preserved)

| ID | Severity and authority boundary | Original reproducer/result | Remediation and permanent coverage | Disposition |
| --- | --- | --- | --- | --- |
| P2QA01 | Substantive: durable operation identity and unresolved-economics exclusion | On initial head, prepare CORRECT at revision 2; delete operation_events then operations with valid foreign keys; load accepts revision 2 and save succeeds at revision 3. No hashes or checkpoint payloads rewritten. The same deletion can erase UNCERTAIN_EXTERNAL exclusion. | Independent `test_prepared_operation_cannot_disappear_from_durable_history`, `test_uncertain_external_marker_cannot_disappear`, `test_deleted_marker_detected_even_with_foreign_keys_disabled`. Author proposes checkpoint reverse binding with deferred FK plus exact prepared/outcome revision membership. | Original defect reproduced; remediation rerun pending. |
| P2QA02 | Substantive: complete durable transition history at read boundary | Delete PREPARED events, or delete COMMITTED outcome event while retaining operation/checkpoints. Plain store.load accepts inconsistent history. Initial targeted run: 2 methods, 35.284 seconds, both fail because IntegrityError is absent. | Independent `test_committed_outcome_event_cannot_disappear_on_plain_load`, `test_prepared_event_cannot_disappear_on_plain_load`. Author must validate operation event history and matching committed outcome on ordinary load without executing accounting. | Original defect reproduced; remediation rerun pending. |

Additional original reproduction evidence: the initial independent full suite ran
12 methods in 263.578 seconds: three expected P2QA01 failures and nine passes,
including competing real processes. P2QA02's duplicate-middle PREPARED transition
also reproduced (one method, 24.900 seconds, expected refusal absent).

| ID | Severity and authority boundary | Original reproducer/result | Remediation and permanent coverage | Disposition |
| --- | --- | --- | --- | --- |
| P2QA03 | Substantive: committed recovery receipt versus native accounting authority | Change only COMMITTED event result plus its redundant SHA: native selected journal amount becomes `999999999999`, or correction plan refers to `version:missing-authority`; immutable native checkpoints/results/sources remain unchanged. Both committed recover calls accepted inconsistent outcomes. Initial targeted run: 2 methods, 50.703 seconds, two expected failures. | Independent `test_committed_journal_receipt_must_match_native_outcome_checkpoint`, `test_committed_correction_plan_must_match_native_rework_history`. Author binds prepared native journal-selection digest into operation identity and validates correction/rework/Period receipts against exact outcome checkpoint history, without accounting execution during reads. | Original defect reproduced; remediated rerun pending. |

A coherent privileged rewrite of the entire governed state remains the documented
trust limitation. P2QA03 changed one redundant event payload/hash while leaving its
referenced governed authority unchanged, so it was an inconsistent authority claim,
not a coherent full-state rewrite.

## Independently executed positive control

The reviewer executed `python -m
orchestration.tests.generate_persistence_stage2_examples` on frozen initial head.
It completed successfully using real SQLite and distinct producer/consumer
processes, actual OS exit 73 after native selective rework and before durable
outcome commit, then fresh-process recovery. Native Case reached CLOSED, public
answer complete, immutable history/unaffected versions retained, exact selected
native journal population eight, repeat recovery unchanged. The unresolved original
conflict control remained partial. This original generator stopped its Period
proof after reopening; the reviewer requested actual correction/rework/reclosure
and repeat recovery after reclosure before final acceptance.

## Permanent independent attacks

`orchestration/tests/test_persistence_stage2_independent.py` additionally attacks
same-value historical receipt reuse, changed prepared source payload, lost commit
acknowledgement with owner execution disabled on retry, two genuinely separate
simultaneous recovery worker processes, repeated selection operation with identical
qualified journal economics, Group-to-legal relabeling, read-only restoration with
native owner disabled, blocked closure retry, and every public route's exclusion
of private evidence/journals/recovery metadata.

Final remediated rerun and final generator verification remain pending. This file
records findings; it does not yet grant independent acceptance or release readiness.
