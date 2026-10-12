# Stage 2 independent QA

Reviewer: separate `/root/stage2_independent_qa` agent context. Independently read live Period, Case, Scope/node identity, Graph, VersionRegistry, VersionedExecution, native owner fixture, public adapter and scoped journal allocator implementation before deriving attacks. No implementation edits or Git mutations performed by reviewer. Tests use actual production Revenue and bounded non-authoritative downstream observations. They are permanent in `orchestration/tests/test_stage2_independent.py`.

## Findings with executable reproducers

| Finding | Reproducer | Remediation required |
|---|---|---|
| F1 Case accepts US Scope with Group calendar | `test_scope_calendar_case_substitution_rejected` | Validate Scope calendar when registering Case. |
| F2 Blocked required producer retains CURRENT version; parent remains complete | `test_required_blocked_node_with_current_version_blocks_parent` | Check producing node lifecycle as well as version currentness. |
| F3 Publishing can bind UK version to US dependency / omit required binding | `test_bound_result_must_belong_to_declared_producer`, `test_required_binding_cannot_be_omitted_on_publish` | Validate exact declared edge/producer/version binding at registry publication. |
| F4 Reopened period cannot close | `test_reopened_period_can_close_preserving_identity` | Allow governed reclose, preserve reopening history. |
| F5 Bounded executor accepts wrong Scope/Period source | `test_bounded_executor_wrong_scope_source_rejected`, `test_bounded_executor_wrong_period_source_rejected` | Validate source dimensions before any execution/version mutation. |
| F6 Effective interval accepts incompatible Scope fiscal calendar | `test_effective_interval_wrong_scope_calendar_rejected` | Validate Scope/calendar binding. |
| F7 Registry serialization cannot reconstruct periods with status or relationships with ID | `test_current_journals_complete_population`, `test_new_journals_once_history_not_extra_postings` | Round-trip serialized registry records through generic normalization, retaining status. |
| F8 Adding dependency after publication leaves consumer CURRENT without consumed binding | `test_new_dependency_cannot_leave_already_current_consumer_unbound` | Fail closed or invalidate existing consumer, never silently authorize retroactive binding. |

Initial 16-method independent run reproduced F1–F6 (7 failing/error methods), while nine other controls passed. Expanded 32-method run after initial remediation reproduced F7 and F8; earlier seven methods passed. Subsequent final rerun and disposition are recorded below when completed.

## Attack coverage

Cases: objective/period identity distinction; wrong Scope/Period registration; wrong parent; undeclared child consumption; independent Case lifecycle history; required blocked producer propagation. Scope, Case and dependency graphs are challenged independently by unrelated UK controls and explicit edge mutation.

Periods: deterministic identity independent of evidence; calendar identity separation; partial acquisition and disposal interval contamination; outside-source interval; wrong opening Scope; future comparative; relationship cycle; reopening identity/history and reclose. Authored suite supplies additional malformed dates, end-before-start and opening-date controls.

Versions: wrong producer and omitted binding; equal-value superseded/stale receipt rejection; exact-period receipt substitution; defensive historical payload copy; broken supersession; repeated production owner across Scope and Period. Selective chain verifies direct/transitive invalidation and unaffected UK/US October identities.

Rework: wrong execution order, unrelated appended rerun, closed-period unauthorized execution, reopening without global invalidation or reversal, stale completed Case entering rework with history.

Journals: actual complete native implication population; superseded event rejection; wrong-period event; duplicate alias allocation; current corrected economics counted once alongside preserved historical versions. Opening/Group/analytics observations carry no journal authority; supersession introduces no reversal.

Privacy/determinism: public serialization excludes internal result/dependency/Case/version/fingerprint/reviewer state; fresh executions produce identical registries and dependency identities. Stage 1 and earlier flagship migration tests remain separate release gates, not assumed green from Stage 2 attacks.

No generalized intercompany, conversion, authentication, persistence or new accounting authority was added by this QA work.

## Independent remediation rerun

41 distinct independent methods PASS (`python -m unittest orchestration.tests.test_stage2_independent -q`, 22.654 seconds). All F1–F8 executable reproducers pass after remediation. Wrong Scope/calendar and source dimensions fail closed; registry publication validates complete exact producer-version bindings; blocked producers affect required parent status; reopened periods retain history and can close; registry records round-trip through canonical validation; published consumers reject retroactive dependency insertion. Findings are retained as permanent regressions, without expected-failure exemptions.

Independent generator runs call `artifacts()` without altering generated files, under `PYTHONHASHSEED=19` and `PYTHONHASHSEED=941`. Both produce 31 artifacts and identical SHA256 of canonical JSON: `a7a8a915b062aa5e62965f01f0b3a4ea268ee91dba26e3a4f26a733a74985b9c`. Actual native journal population is 18 implications across US September, US October and UK September. Corrected supersession preserves that current population, rather than adding historical versions.

Unresolved substantive independent findings: **0** for the inspected implementation. This is intermediate QA acceptance only: compatibility integration, repository-wide regression, final handoffs/roadmap and immutable-head CI remain separate release gates. Changes after this reviewed state require their appropriate regression and independent review.

Independent Stage 1 regression: `python -m unittest orchestration.tests.test_scopes orchestration.tests.test_scope_independent -q` — **96 distinct methods PASS**, 49.459 seconds. This preserves repeated-owner Scope identity/current-result and adversarial Stage 1 behavior; reruns are not counted as additional methods.

## Context-reliability checkpoint rerun

After the final intermediate boundary additions (native production-owner dispatch, rejection of journal postings from non-authoritative observation consumers, and current-upstream enforcement when selecting current payloads), independently reran the existing suite without implementation changes or new functionality: **41 distinct Stage 2 methods PASS**, 21.304 seconds. Command: `python -m unittest orchestration.tests.test_stage2_independent -q`. The repeated run does not increase the distinct method count.

F1–F8 remain permanently covered and passing. Unresolved substantive findings are **0 within this reviewed intermediate scope**. This does not assert the complete Stage 2 assignment has passed or that later unreviewed additions are covered.

Outstanding release gates at checkpoint: finish all generalized compatibility/migration integration and corresponding authored coverage; complete controlled proof/artifact deliverables and final deterministic regeneration; review any subsequent implementation changes independently; run every required previous flagship and full repository/authority regression; commit the actual Stage 3 and final integration handoffs; advance roadmap only after substantive gates pass; freeze and push the immutable candidate; obtain required exact-head Actions; update and mark the existing PR ready for review. These gates belong to continuation on the same branch/PR, not to this intermediate QA acceptance.
