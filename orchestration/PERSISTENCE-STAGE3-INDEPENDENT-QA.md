# Stage 3 independent adversarial QA

Status: ACTIVE — implementation attacks currently PASS; final isolated committed-tree proof is still pending. No authenticated approval infrastructure is claimed.

A separate reviewer agent examined production read-only and created detached worktree `stage3-review` at local checkpoint `5a4254e`. The implementer supplied publication equivalence to remote `74a2903969a4d41d543363a0a6619d0b38541f9a`. Reviewer changed only independent tests, this register and execution evidence; production fixes belong to the implementation agent.

The reviewer reconstructed native Context Observer, Intake/ReviewedInputPack, Scope/Period, immutable result and SQLite checkpoint contracts. Attacks use actual sealed-source/native execution and SQLite publication/reconstruction boundaries. Patches in tests either supply hostile raw fixture data or forbid accounting reruns; refusal is never mocked. Concurrent promotion uses real simultaneous threads with independent SQLite connections. Atomicity uses an actual SQLite trigger abort on the second compound event.

## Original findings and final current disposition

Original inspected memory implementation SHA256: `679432f237560eea2cd2ab24a2f98b59b497b798e6665c3dcb79f03da7e8a779`. Original findings are retained below, including failed/error outcomes. Original execution logs are committed under `orchestration/tests/evidence/company-memory-independent/`. Later PASS results do not erase original failures.

| ID | Severity | Original finding/result | Generic remediation and permanent coverage | Current independent disposition |
|---|---|---|---|---|
| IQA01 | High | Unknown coherent USE memory version survived audit; actual FAIL. | Exact historical memory-version binding; `test_unknown_historical_consumption_version_rejected`. | PASS, remediated |
| IQA02 | High | DOCUMENTED position could supersede itself; actual FAIL. | Self/cycle/backlink refusal; `test_supersession_cannot_use_self_as_successor`. | PASS, remediated |
| IQA03 | High | Read-only original approval accepted substring wording, including negative/quoted text. | Exact documentary envelope with explicit trusted intent; `test_negative_documentary_wording_never_approves` plus inferred-claim tests. | PASS, remediated |
| IQA04 | High | Read-only original support accepted any existing result without producer Case/Scope binding. | Exact producer Case/Scope lineage; `test_existing_current_result_of_other_native_case_cannot_support_memory` executes accepted Stage4 fixture and native Context Observer. | PASS, remediated |
| IQA05 | Limitation | Exact-Scope memory has no legitimate declared broad-policy coverage/inheritance. No invalid authority was demonstrated. | Group membership must not invent applicability; exact-Scope refusal documented in MEMORY-CONTRACT. | Accepted bounded limitation, not substantive defect |
| IQA06 | High | Unknown consuming root Case/Case survived coherent USE audit; actual FAIL. | Bind exact native consumer namespace/revision/hash and applicability; `test_unknown_consuming_case_in_history_rejected`. | PASS, remediated |
| IQA07 | High | Candidate could assert approved Decision Register entry without governance; actual FAIL. | Capture requires proposed decision; explicit separate decision lifecycle; `test_candidate_cannot_assert_approved_decision_without_governance`. | PASS, remediated |
| IQA08 | High | Coherently hashed historical supersession referenced itself; detached-worktree FAIL. | Restored successor/backlink/state validation; `test_restored_supersession_must_validate_successor_lineage`. | PASS, remediated |
| IQA09 | High | Historical DECISION event approved decision on merely DOCUMENTED position; detached-worktree FAIL. | Same decision authority gate on reconstruction/publication; `test_restored_decision_cannot_claim_approval_on_documented_position`. | PASS, remediated |
| IQA10 | High | Legitimate USE followed by audit ERROR because consumer checkpoint checksum shadowed event-chain checksum. | Distinct checksum variables; `test_valid_context_consumption_remains_readable`. | PASS, remediated |
| IQA11 | High | Historical USE bypassed effective bounds (Dec15 policy consumed for full Dec1–31 Case); actual FAIL after IQA10 fixed. | Exact event-time effective/uncertainty/semantic qualification; `test_restored_use_cannot_bypass_effective_period`. | PASS, remediated |
| IQA12 | High | Compound resolution succeeded, then identical lost-ack retry ERROR RevisionConflict. | Exact retained successor/alternative governance replay returns original result; `test_compound_resolution_is_idempotent_after_lost_ack`. | PASS, remediated |

## Execution chronology without double counting

Initial 4-test review: 2 PASS, IQA01/IQA02 FAIL. After fixes those four PASS.
Expanded intermediate 17-test run PASS before further restoration attacks.
Detached checkpoint `5a4254e`: 23 tests, 22 PASS / IQA08 FAIL.
Later WIP 27-test run: 26 PASS / IQA11 FAIL; IQA12 separately ERROR.
Current WIP full run: **31 distinct independent tests PASS**, 66.121 seconds, `current-31-pass.log`. Reruns and subprocess phases are not additional distinct tests. No unresolved substantive reproduced finding remains at this WIP checkpoint.

Reviewer fixture mistakes were corrected without production credit: RawSource uses `format`, not `kind`; the accepted Stage4 fixture did not pre-run Context Observer, so reviewer explicitly invoked the existing native observer before the supporting-Case attack. A pre-IQA10 temporal attack initially refused only because of the checksum bug; it was not credited as temporal protection and was rerun to expose IQA11.

The independent fresh-process cross-Case test runs Cases A/B separately, persists documentary assertion, forbids CAO/native reruns in the first new process, retrieves and consumes exact original memory/source Case identity, then verifies intact USE history in another fresh process. It PASS. This is documentary assertion, not human authentication.

## Outstanding final reviewer gates

Refresh detached worktree to the complete committed implementation; independently execute full seven-process positive generator and decode/hash-check its lossless checkpoint envelopes; run the 31-test independent suite on that same immutable tree; verify generated public output and current/historical qualification after correction and unresolved conflict. Only then may this register state final independent QA PASS.

## Frozen checkpoint generator review

At detached local checkpoint `e1d1c12`, reviewer independently executed the complete seven-process proof under seed19: PASS, all eight files byte-identical to committed checkpoint artifacts. Six nested lossless envelopes decoded with exact SHA256 checks; all three embedded native checkpoints restored CLOSED with 1, 2 and 1 immutable result versions respectively. This checkpoint's earlier 32-test run had 31 PASS plus a reviewer-only canonical PeriodRegistry construction error; sorting native registry rows fixed that fixture and the alternate valid-calendar planning refusal then independently PASS.

A final artifact-linked finding was identified: fixture Decision Register `new_position=NetSuite` was hardcoded even for Xero context successors. Frozen production also allowed a proposed linked decision whose new position contradicted its context value.

| ID | Severity | Original actual result | Generic remediation | Permanent regression | Current disposition |
|---|---|---|---|---|---|
| IQA13 | Medium | Frozen e1d1c12 capture accepted conflicting linked Decision new_position; FAIL retained in `decision-value-calendar-e1d1c12.log`. | Bind linked new position to exact context typed value; generate actual candidate positions and preserve known previous positions. | `test_linked_decision_new_position_cannot_contradict_context_value` | Fix in progress; independent corrected-tree rerun pending |

Independent permanent test count now 33. Final corrected immutable checkpoint suite/proof remain outstanding.

## Final temporal and inherited-context review

| ID | Severity | Original actual result | Generic remediation | Permanent regression | Latest independent disposition |
|---|---|---|---|---|---|
| IQA14 | High | Frozen e1d1c12 accepted real registered relationship whose endpoints exclude selected memory Period; FAIL. | Bind selected target/endpoints and original native source Case role. | `test_registered_relationship_of_other_period_cannot_qualify_memory` | Targeted WIP PASS |
| IQA15 | High | Frozen e1d1c12 accepted real registered Period belonging to another Scope calendar; FAIL. | Enforce Scope reporting calendar and original native source Case calendar. | `test_registered_period_of_wrong_scope_calendar_cannot_qualify_memory` | Targeted WIP PASS |
| IQA16 | High | Case B inherited systems only from memory A, with sealed raw archive containing AP evidence but no system-policy; recapture as USER_STATED then DOCUMENTARY DOCUMENTED succeeded, laundering inherited knowledge into independent truth; FAIL. | Preserve exact memory dependencies in sealed native context and refuse derived observer recertification without independent extraction. | `test_memory_derived_context_cannot_launder_into_independent_documented_truth` | Targeted WIP PASS |
| IQA17 | Preventive review | Read-only concern: consumed version could differ from sealed planning origin despite equal values. Guard landed before execution; no original FAIL claimed. | Exact planned record/version/sourceCase/use binding in publication and restoration. | `test_planning_memory_use_cannot_substitute_equal_value_wrong_provenance` | WIP PASS |

Targeted IQA14/15/16 rerun: 3 PASS in20.276s. Planning provenance attack after preventive guard: PASS in10.189s. Original failures and rerun logs committed with this register. Independent permanent suite count is now **37**, including the separate real other-calendar planning boundary test. Final immutable complete suite/generator still required.
