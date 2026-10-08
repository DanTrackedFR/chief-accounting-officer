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

## Remediation progression (additive evidence)

Partial author-remediation rerun: 17 methods in 337.534 seconds, 16 passed and
only the expected P2QA02 duplicate-middle PREPARED/plain-load reproducer failed
because that process loaded the earlier store copy. The unchanged reproducer then
passed against the full ordinary-load validation fix (1 method, 28.839 seconds).
No original finding status or original failing run is erased by these later runs.

AUTH01 was discovered by the author’s permanent missing-rework-history test, then
independently reproduced by this reviewer: erase all native rework plans, omit one
plan, or duplicate a plan in the accepted native baseline. All three restore-boundary
refusal tests failed on the original state.py (3 methods, 14.312 seconds). The
reviewer copied the author's generic Counter validation of every immutable
successor `(predecessor, version)` against the exact native rework-plan population.
No production implementation was edited by the reviewer. Unchanged independent
reproducers plus prior Stage 1 independent and compatibility controls all passed:
41 methods in 45.742 seconds (3 new + 25 prior independent + 13 compatibility).
AUTH01 is therefore independently verified remediated; the author retains credit
for its original discovery and permanent authored reproducer.

The reviewer permanent Stage 2 suite now has 21 distinct methods. Beyond the
original three findings it includes meaningful interruption after the first
selected native consumer really publishes: discarded partial state must restore
exact prepared snapshot/revision, then replay the native unit in exact dependency
order with unrelated versions unchanged and ordinary CLOSED/public complete.
Final 18-method frozen production rerun and updated complete Period generator
remain running; the three new history tests have already passed as above.

The final frozen production rerun completed successfully: **18 independent methods
in 468.227 seconds, OK**, against exact store/recovery/generator/fixture bytes from
`3ec38ca580cdb948e7b47c15af9565f2d26c248b`. P2QA01, P2QA02 and P2QA03 permanent
reproducers all pass; meaningful first-consumer publication interruption also passes.
The subsequently added state.py history-population validation passed the 41-method
follow-up above, including its three new independent methods. Independent Stage 2
coverage comprises **21 distinct methods**; reruns and prior Stage 1 controls are
not counted as additional new methods. P2QA01–03 and AUTH01 are remediated with
permanent executable coverage; no unresolved substantive finding is known.
The complete updated eleven-process reopened/reclosed generator is still pending.

## Final independent disposition

The updated complete eleven-process generator finished successfully (exit 0).
The reviewer verified its actual generated summary and Period artifacts: actual
controlled process death 73 after native execution/before outcome commit; fresh
resume with ordinary CLOSED Case and complete public answer; eight selected native
journals; original/unaffected immutable history; original unresolved control still
partial; CLOSED → explicitly synthetic reviewed REOPENED → reviewed correction in
a fresh process → native selective rework → ordinary CLOSED Period; repeated
COMMITTED reclosure recovery with identical checkpoint/public output. No accounting
owner or completion override supplied any of these outcomes.

Final delivered production persistence bytes reviewed and exercised:

- store.py: `fd9f6f640f03d1966ac657393e7065f9dcfbd53fa57fbc423b3dfd1050e45bea`
- recovery.py: `271501c24e3084e3445ce5fc34bf4ba021a63aedce9781281d646376566bcc93`
- state.py: `d8c175ce0595840d90213bfc9f07211b0eccb6569f01cb4718917fa5007d00d1`

Store/recovery and native generator flow match frozen production
`3ec38ca580cdb948e7b47c15af9565f2d26c248b`; later state.py validation was independently
reproduced and passed with the three new attacks plus all prior independent and
compatibility persistence controls. Author head observed after these changes was
`5472c00f493d8614b2631f91e9bcabb0796cf623` with the same production bytes above.
Later generator output-envelope additions were inspected as format-only:
deterministic gzip (`mtime=0`, canonical OS header), base64 and exact canonical
checkpoint SHA retain full native original/resumed payloads. Native proof execution
and qualification did not change. Full envelope restoration/reference-artifact
validation is also part of the author's final repository release suite.

| Finding | Final independent disposition |
| --- | --- |
| P2QA01 | Remediated; all three marker-deletion boundary reproducers pass. |
| P2QA02 | Remediated; missing events and impossible duplicate transition refuse on ordinary load. |
| P2QA03 | Remediated; returned journal/correction outcomes must agree with immutable native authority. |
| AUTH01 (author discovery, independently challenged) | Remediated; erased/omitted/duplicated native rework population rejects; prior persistence compatibility passes. |

**Independent Stage 2 acceptance PASS: 21 distinct permanent methods, all substantive
findings remediated, zero unresolved substantive findings.** The separate 18-method
full run and three-new-method follow-up must not be double-counted with reruns or
prior Stage 1 methods. Recovery coordinates pure native work and idempotent internal
selection; it does not establish exactly-once external ERP posting, authenticated
approvals, encryption or protection against a privileged coherent full-state rewrite.
Final whole-repository regression, deterministic two-seed artifact comparison and
required exact-head GitHub Actions/PR readiness remain the implementation author's
release responsibilities; this independent report does not fabricate those gates.
