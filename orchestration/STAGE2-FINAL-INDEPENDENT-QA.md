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

## Expanded release review — independent continuation

A separately delegated final reviewer inspected the current runtime, planner,
intake/preparation/semantic contracts, temporal qualification, Scope/Case/Period
registries, governed-plan loader, version publication/invalidation/receipts and
current scoped journals. Implementation and git were not edited by this reviewer.
Permanent new attacks are in `tests/test_stage2_release_independent.py`; historical
41-method and nine-method reports above remain intact.

### F8 — auxiliary reviewed source evidence bypasses temporal qualification

Independent executable reproduction: use the two-period temporal intake fixture;
attach the actual October source fingerprint and metadata to the September native
input, re-certify that reviewed native input, and supply an exact September
DocumentBinding. Before remediation `Intake.execute` completed both native owners.
Auxiliary source qualification checked Scope/framework/currency but omitted
Period/calendar/relationship and auxiliary binding target identity. The new
`test_october_document_cannot_certify_september` preserves this attack; a separate
calendar substitution attack and same-period positive control prevent acceptance
through unconditional rejection. Root remediated central auxiliary qualification;
all three independently reran PASS.

### F9 — material questions lose same-Scope temporal identity

Independent code inspection found missing-fact declarations could not carry a
Period, question deduplication used only kind/attribute/Scope, and answered-fact
selection accepted any established fact in that Scope. Root remediated these
contracts during review. New tests independently confirm September and October
confirmation questions retain separate exact Period IDs, and an established
September amount does not suppress an October missing-fact question. Both PASS.
This finding's pre-remediation evidence is inspection, not a claimed saved failing
execution; the permanent regressions were executed after concurrent remediation.

### F10 — consecutive corrections can omit still-pending consumers

Root independently found that replacing a producer again before its first rework
could make the latest plan ignore consumers still bound to an older predecessor.
The reviewer independently derived a new attack through ordinary `CAO.correct`:
correct US September twice without rerunning consumers, reject the obsolete first
plan, and require the latest plan to include/reexecute the same four actual
consumers. Root's predecessor-lineage traversal remediation independently passes.
This is root-originated finding evidence with an independent permanent regression,
not a claim that the reviewer discovered or ran the unremediated defect.

### F11 — ordinary native source manifests can substitute governed Period identity

Independent reproduction: keep October source dates and all accounting dimensions,
replace its qualified source manifest `metadata.period_id` with September's ID,
re-certify the native Revenue input, and invoke ordinary `CAO.run` directly. Both
native owners completed; the permanent fail-closed test independently FAILed.
Intake qualification had protected its own path, but ordinary native execution
checked manifest dates without the governed Period/calendar/role/relationship.
Root added central native source qualification to ordinary and versioned production
entry. The original attack independently reran PASS; a separate native correction
attack proves correction does not bypass that gate or publish a new version.

### F12 — governed temporal Scope activity qualification bypasses

Independent executable reproduction of the root's Scope-effective-date concern:
set US Scope `effective_to=2026-09-30` in the two-period ordinary request with a
September default context. October native execution still completed because Scope
activity was checked before the source's governed Period replaced default dates.
A separate independently discovered attack marks US Scope INACTIVE in the governed
plan: initial native US executions still completed. Permanent regressions cover
both paths. Their disposition and final combined rerun will be appended after
remediation; no final stable acceptance is claimed by this paragraph.

### New independent coverage beyond reproduced findings

The new module also verifies exact reviewed native receipt omission and imported
result-fingerprint substitution, equal-value replacement receipt rejection,
downstream CLOSED Period protection, bounded reopened authorization, ordinary
correction/public refresh and privacy, comparative/restatement original payload
preservation and stale receipt rejection, structural SUBGROUP Case selective
currentness and no posting authority, current journal alias/wrong-owner/version
rejection, and current restated journal economics without counting original
history. The immutable payload and posting assertions use actual native Revenue
results; bounded observations retain local currency and claim no accounting
restatement/conversion/consolidation authority.

### F12 remediation and positive journal migration control

Root moved ordinary Scope effective-date checks after actual governed Period
selection and added pre-owner governed/versioned Scope authorization. Both
original activity attacks independently reran PASS. The reviewer also independently
reproduced an adjacent false rejection: actual valid September native journals in
an October Group context, with the US Scope effective through September, failed
because scoped journal qualification still used October defaults. Root now selects
the row's actual governed Period before journal qualification; ordinary native
posting qualification uses its already qualified actual node context. The positive
`test_valid_prior_period_journals_use_actual_scope_effective_interval` independently
passes and allocates the six actual September implications exactly once. This
fix preserves prior-period economics while expired later executions fail closed.

## Final independent stable-architecture rerun

After the final demonstrated Scope/journal remediation, independently executed:

`python -m unittest orchestration.tests.test_stage2 orchestration.tests.test_stage2_independent orchestration.tests.test_stage2_final_independent orchestration.tests.test_stage2_release_independent -q`

**113 distinct methods PASS, 0 FAIL, 0 ERROR**: 41 authored Stage2, 41 historical
independent Stage2, nine checkpoint final-independent and 22 new release-independent
methods. Counts were separately verified through unittest loading. Intermediate
reruns (including 108, 110 and 112 methods while new attacks were being added) are
not additional distinct tests. `git diff --check` independently passes.

For the inspected completed Stage2 architecture, there are **zero unresolved
substantive findings**: F1–F12 are remediated in their documented scopes, with
permanent regressions and independent reruns. The new review covers ordinary and
serialized governed execution, exact owner/Scope/Period selection, temporal intake
and reviewed/native source qualification, material questions, comparative/restated
history, structural SUBGROUP execution, immutable versions and native/bounded
receipts, ordinary correction including pending repeated corrections, selective
rework/public currentness/privacy, Scope activity, closed/reopened Periods and
current exact-once scoped journal economics. Bounded observations remain explicit
local non-authoritative observations; production owners retain accounting authority.

This is final independent **architecture acceptance**, not a claim that this
reviewer executed every repository/production/knowledge validator, independently
regenerated every flagship artifact, verified an immutable pushed SHA or observed
all required exact-head workflows. Those separate release gates remain the
integrator's responsibility and must be evidenced before readiness. No Stage3/4,
general conversion/intercompany authority, durable persistence or authenticated
governance is certified by this review.

## F13 — migration residual bridge lost at public currentness boundary

The integrator's full migration regression found the permanent existing
`test_diagnostic_independent.IndependentResidualRuntimeQA.test_material_residual_keeps_valid_bridge_and_limits_publicly`
failed: a global stale-result public guard removed a correctly qualified partial
diagnostic bridge, including its unexplained residual and limitations. A partial
conclusion synthesized against the current challenged view must retain qualified
work and unresolved residuals rather than disappear.

Root remediated synthesis/public integration: ordinary synthesis captures the
exact active version/currentness view; public delivery rejects a changed view but
retains a qualified partial synthesis against its unchanged challenged view.
Governed no-conclusion stale delivery still blocks. This is integrator-originated
finding evidence, not a claimed independent discovery or pre-remediation rerun.

The reviewer independently reran the existing permanent migration test PASS on
all public routes. A new independent permanent adversarial test,
`test_low_level_native_rework_cannot_republish_old_ordinary_synthesis`, also PASSes:
initial ordinary native synthesis contains 800; direct versioned native correction
and reexecution leave all active versions CURRENT, but the old ordinary conclusion
is refused because its captured version view changed. This protects against
allowing a historical synthesis merely because downstream currentness has recovered.
The two focused methods independently passed; final combined rerun follows below.

### Final post-F13 independent rerun

Independently reran the same four Stage2 modules after F13 remediation and the
new synthesis attack: **114 distinct methods PASS, 0 FAIL, 0 ERROR** (41 authored,
41 intermediate independent, nine checkpoint independent, 23 release independent).
The separately executed existing diagnostic residual migration method also PASSes;
the new focused synthesis method is already included in 114 and is not counted
twice. `git diff --check` PASSes.

There are **zero unresolved substantive findings F1–F13 in the inspected completed
Stage2 architecture and this demonstrated migration scope**. This supersedes the
113-method architecture rerun above for the additional F13 change; original finding
history remains intact. The same boundaries apply: broader repository validators,
flagship artifact reproduction, immutable commit and exact-head workflows remain
separate integrator release evidence, not claims made by this independent reviewer.

## F14 — fiscal-label/as-of aliases create duplicate actual Period identities

Root's final alias inspection identified a possible duplicate-period identity
attack. The reviewer independently reproduced both variants before remediation:
create a second Period for the same calendar/start/end/type with a new fiscal label,
or with an altered evidence as-of date. Both produced distinct IDs and both were
accepted together by `PeriodRegistry`. This could treat one actual governed
interval as separate execution/economic identities; the saved pre-remediation
reproduction establishes registry acceptance, not a claimed end-to-end duplicate
posting execution.

Root added a narrow registry uniqueness gate over calendar/start/end/period_type.
It rejects distinct IDs for the same actual interval/type; it does not introduce
generalized overlapping-period restrictions. Four new permanent independent
methods PASS: fiscal-label alias rejection, as-of alias rejection, direct ordinary
native request alias rejection, and positive preservation of cross-calendar
Periods plus REPORTING/OPENING/PARTIAL_INCLUDED_PERIOD type distinctions. The native
alias request is independently blocked before any completed owner execution.

Final combined post-F14 rerun follows; root-originated concern, independent
reproduction, remediation and positive controls are all preserved here.

### Final post-F14 independent rerun

Independently reran all four Stage2 modules after the alias gate: **118 distinct
methods PASS, 0 FAIL, 0 ERROR** (41 authored, 41 intermediate independent, nine
checkpoint independent, 27 release independent). The four focused alias methods
are included in 118, not additional distinct tests. `git diff --check` PASSes.

There are **zero unresolved substantive findings F1–F14 in the independently
inspected completed Stage2 architecture and demonstrated migration scope**. This
post-F14 result supersedes the earlier combined method counts while retaining their
history. Broader repository validation, deterministic flagship reproduction,
immutable final publication and exact-head workflows remain separate integrator
release gates; this reviewer makes no independent claim to have executed them.
