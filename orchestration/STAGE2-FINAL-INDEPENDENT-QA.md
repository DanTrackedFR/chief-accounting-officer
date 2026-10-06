# Final Stage 2 independent audit — release gates unresolved

Audit target: live PR #35 head `29f9ae126ac1a577187d3d6c5a44bbdff315ed89`.
Independent context: dedicated final audit agent, read-only implementation inspection and new executable attacks derived from existing interfaces. Only this report and `tests/test_stage2_final_independent.py` were authored by the reviewer. No implementation remediation or release administration was performed.

This does not replace `STAGE2-INDEPENDENT-QA.md`. Its 41 intermediate independent tests and eight remediated finding classes remain historical evidence. Intermediate acceptance is not final acceptance.

## Executable review result

Command: `python -m unittest orchestration.tests.test_stage2_final_independent -v`.
Seven distinct methods: one PASS, six FAIL; eight failure assertions because one method uses three required-control subtests. These numbers are not eight distinct methods.

The existing central selective chain passes: US correction stales and reruns four actual downstream nodes and leaves UK unchanged. This working foundation should be preserved.

## Findings

### F1 — ordinary temporal Case execution is not governed by Case registry

Reproducer: `FinalRuntimeAudit.test_ordinary_case_qualifies_scope_period` and `test_ordinary_completed_nodes_bind_governed_case`.

Using the existing native US September Revenue fixture, the request supplies governed Scope records and Period registry inside `scope`, as required by `scoped_context`. `CAO.run` concludes complete; returned Case Scope, Period and Case type are empty, and completed node Case ID is empty. Existing Scope/Period qualification does not establish governed Case ownership. Required correction: normalize ordinary execution into the existing Case architecture, with deterministic objective/cycle identity and bound nodes.

### F2 — ordinary temporal execution has no version/current dependency lineage

Reproducer: `FinalRuntimeAudit.test_ordinary_complete_result_has_version_lineage`.

The same successful request has an empty `result_version_refs`; execution receipt carries a result fingerprint and nominal currentness but no result version. `CAO.run` does not use `VersionedExecution` or publish governed versions. Ordinary callers therefore cannot use its successful output as the required exact-version substrate without a separate execution path. Required correction: compose the existing ordinary native execution with the existing version/dependency registry rather than adding another runtime.

### F3 — CLOSED Period protection bypassed by ordinary native execution

Reproducer: `FinalRuntimeAudit.test_closed_period_ordinary_native_execution_fails_closed`.

Close US September through `PeriodRegistry.close`, serialize that registry into the ordinary request, and execute native Revenue. The result remains complete and the production node executes. `scoped_context` validates identity/dates but does not authorize execution; ordinary runtime never calls `authorize_execution`. This is a fail-closed governance defect, not simply missing evidence. Required correction: authorize ordinary temporal execution using the same existing close/reopen contract before invoking owners. Preserve closed history; do not invent journals.

### F4 — mandatory unaffected controls absent from controlled final proof

Reproducer: `FinalProofAudit.test_required_unaffected_controls_executable`.

The actual initial graph contains nine nodes. It includes UK and NL controls but has no unrelated Treasury result, no execution after October, and no Group node lacking dependencies. November Period records do not constitute a November execution witness. All three required control subtests fail before correction. Required correction: add bounded governed proof executions for these required controls and assert exact current versions survive US correction/rework unchanged. This finding is missing release evidence, not a demonstration that the existing engine globally invalidates these classes.

### F5 — comparative relationship represented but not executed

Reproducer: `FinalProofAudit.test_comparative_dependency_is_executed`.

The fixture registers comparative Period relationships, but no dependency edge has type COMPARATIVE and no comparative consumer executes. The final proof cannot establish original-prior/current-comparative/restated-comparative exact-version lineage merely from Period relationship validation. Required correction: add qualified non-authoritative comparative/restatement executions preserving original history, with stale/superseded receipt attacks. Do not invent accounting restatement authority.

## Disposition

Five substantive final finding classes remain unresolved at audit time. This report is an intermediate final-architecture review, not exhaustive final acceptance. Additional requested release gates (including temporal intake/ReviewedInputPack, Subgroup execution and full migration/authority regression) still require independent validation after remediation. Documentation declaring Stage 2 COMPLETE is inconsistent with these executable findings. Do not claim zero unresolved final findings or ready integration until remediation, permanent regressions and independent rerun pass.

## Independent intermediate remediation rerun

Reviewed current local `runtime_governance.py`, `governed_plan.py` and controlled fixture after initial findings. The original seven audit methods independently reran PASS. F1–F4 are remediated for the inspected contracts. F5 now has an executable comparative consumer and exact-version receipt; this closes the represented-versus-executed comparative gap but does not yet establish all required comparative/restatement attack coverage.

The proof now runs its initial graph through ordinary `CAO.run(governed_plan=...)`, includes Treasury/future/non-consuming Group observation controls and comparative execution, and preserves existing native accounting authority boundaries. Ordinary normalization binds Cases and publishes versions and blocks CLOSED initial execution. Remaining intake/ReviewedInputPack/Subgroup/restatement gates are not accepted by this rerun.

### F6 — bounded consumer can relabel exact producer amount into another currency

Reproducer: `FinalRemediationAttackAudit.test_local_observation_cannot_relabel_producer_currency`.

Change `US-REPORT` source `observation_currency` from USD to EUR before initial governed-plan execution. Native US Revenue still produces 800 USD. The bounded consumer completes with `observed_amount=800.00`, `currency=EUR` without a conversion. Generic current-result receipt supplies no framework/currency qualification. The public output adapter can subsequently display this relabelled result. A non-authoritative limitation does not make a wrong currency valid. Require retained producer currency/framework dimensions and qualified consumer observation context; leave unavailable conversion fail closed. Finding remains unresolved at this rerun.

### F7 — serialized node dimensions can disagree with its registered identity

Reproducer: `FinalRemediationAttackAudit.test_governed_node_cannot_substitute_registered_dimensions`.

Initially reproduced by changing `GROUP-CONTROL` node framework to US_GAAP, functional currency to JPY and jurisdiction to JP while retaining its legitimate execution ID. Governed-plan validation recomputed the ID from registered Scope metadata but did not compare supplied node dimensions; the contaminated graph concluded complete. The implementation was updated concurrently after reviewer notification; this permanent attack now passes. Preserve this finding and regression rather than erasing its history. Final acceptance requires independent stable-candidate rerun.

Latest expanded audit: nine distinct methods, eight PASS and one FAIL (F6). Original five finding classes remain documented and their intermediate remediation status is recorded above. One newly reproduced substantive finding remains unresolved in this audit scope; no full final acceptance is claimed.

## Checkpoint independent rerun — nine methods PASS, release incomplete

After F6 remediation, independently reran the same nine distinct methods against current local code: **9 PASS, 0 FAIL**. This is a rerun of existing methods, not nine additional methods. F6 now rejects USD→EUR observation relabelling; current-version receipts bind semantic metric path, framework/currency dimensions and observed value currency. F7 still rejects serialized node dimensional substitution. No additional review scope was introduced for this checkpoint.

Current dispositions:

- F1/F2: demonstrated ordinary Case/Period binding and version publication reproducers PASS. Partial final-runtime integration acceptance only: complete migration and unresolved temporal input/source/ReviewedInputPack handling remain unreviewed release gates.
- F3: ordinary CLOSED-period execution attack PASS; reopening/history/full ordinary rework release controls still require final regression.
- F4: required unaffected observation controls execute and survive correction unchanged; this does not claim a new Treasury accounting flagship.
- F5: executed comparative dependency and current receipt PASS; restatement preservation, superseding comparative versions and complete comparative adversarial coverage remain open.
- F6/F7: permanent currency and node metadata attacks independently rerun PASS; original finding history preserved.

There are zero failing assertions in the nine-method checkpoint audit. This is **intermediate acceptance only**, not zero unresolved substantive findings across the complete requested Stage 2 architecture. Remaining gates include temporal semantic/intake ambiguity and material questions, period-aware source and ReviewedInputPack certification, structural Subgroup execution/governance, comparative/restatement lineage, full native receipt/rework contracts, final deterministic artifacts, complete migration/authority regression, final independent expanded review, accurate final handoff/roadmap and immutable exact-head CI. Stage 2 must remain INCOMPLETE until those gates pass.
