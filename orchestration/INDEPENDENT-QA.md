# Independent orchestration QA

Reviewer: independent review context delegated by the integration agent at the owner's request. Review began with existing architecture and native production/import contracts before implementation was available. The reviewer did not implement orchestration or author its fixture. Tests were independently derived from architecture and callable runtime APIs; synthetic native cases reuse repository test-data builders solely as inputs.

## Initial candidate assessment

The candidate genuinely executes multiple governed owners for the factory fixture, preserves certification gates, constructs dependency edges, propagates challenge invalidation, retains internal evidence, produces a separately curated public representation and handles material/nonmaterial unavailable dependencies differently. It does not call private accounting workflows. Native assessment supplies accounting authority, rather than the planner.

Initial 18-test run: 13 passed, five substantive failures. Additional independent controls have subsequently been added; final rerun is required after remediation.

| ID | Finding and reproduction | Required remediation | Executable regression |
|---|---|---|---|
| IQA-01 | A valid planner node `ap-issue-1` selecting `accounts-payable` executes AP, then challenge reads `inputs[n.id]` and blocks the otherwise valid case. Node identity is incorrectly coupled to package identity. Handoff lookup has the same assumption. | Resolve source by selected skill while retaining graph node ID independently; map imports to unambiguous owner node; preserve node IDs in dependency references. | `test_custom_node_identity_not_skill_identity` |
| IQA-02 | Broad review includes malformed `inventory` facts as a list plus complete AP facts. Unsupported shape is silently discarded, and the case closes COMPLETE without surfacing inventory. | Surface malformed supported families as governed blocking questions; distinguish absent/inapplicable populations from supplied malformed material facts. | `test_malformed_supplied_known_family_is_visible` |
| IQA-03 | Structured planner sets `material=1`. Python equality accepts this in `(None, True, False)`, and the case completes. The governed materiality flag requires evidenced boolean/null. | Require exact bool type or null, with fail-closed structured response. | `test_materiality_flag_rejects_integer` |
| IQA-04 | AP actual imports contain Payroll, whose source case imports FX. Planner adds Payroll but inspects no source inputs for the newly added dependency; FX and the Payroll → FX edge are absent. | Recursively inspect actual dependency cases, retaining conflicts/cycle detection and dependency dimensions. | `test_nested_owner_imports_are_planned_transitively` |
| IQA-05 | Duplicate factory labour handoff copies the same producer metric, consumer target and amount, changing only caller-provided economic ID. Both receipts are accepted and the case closes COMPLETE. | Bind handoff identity to actual producer metric/source and consumer target, beyond freely supplied economic ID; reject alias duplicates. Preserve legitimate evidence-only downstream reporting. | `test_duplicate_handoff_economic_alias_is_rejected` |

## Independent controls

Tests also attack wrong entity/framework/jurisdiction/period/currency, missing native reviewer certification, material unavailable Grants, explicitly immaterial independent Grants, actual altered imported owner output, cycles/unknown dependencies/duplicate dependencies, parallel-ready nodes, transitive challenge invalidation, context scope/expiry/proposal/conflict, company-context dimension reuse without mutation, memory candidate nonpromotion, runtime public/private separation, training attribution contamination, native supplier-confirmation contradiction, manufacturing selection/negative selection/margin arithmetic and simple-question scaling.

The test suite checks real `production.assess_case` results for executable cases; no mocking supplies production accounting approvals or replaces the production execution boundary. A custom planner tests the bounded planner interface, and direct graph tests independently exercise scheduling/rework.

## Architectural limits identified

This is a bounded source-workpaper adapter foundation. It does not extract arbitrary business documents or understand every free-form natural-language objective. Only one execution scope is currently supplied per Case. Parallel-ready nodes are scheduled as a batch and executed deterministically; this is not concurrent execution infrastructure. Persistence and an application UI remain deferred. Serialisable artifact metadata identifies required workpapers; it is not external artifact storage. These should remain explicit integration limitations rather than completion claims.

## Remediation and independent rerun

IQA-01–05 were remediated by the implementation author. The independent reviewer inspected source lookup separation, exact boolean checks, recursive actual import traversal, malformed-fact questions and semantic metric/target uniqueness. Independent rerun: all original 23 tests PASS.

A further native execution review found two integration defects, both reproduced using actual certified owner outputs without accounting mocks:

| ID | Finding and reproduction | Required remediation | Executable regression |
|---|---|---|---|
| IQA-06 | Removing all request handoffs from the complete factory fixture still produces COMPLETE/CLOSED, zero handoff receipts and no Financial Statements → Inventory/Revenue dependency. Source-to-reporting graph coverage is optional caller input rather than a governed completion gate. | Infer or require the relevant cross-owner mappings; missing bridges must surface structured incomplete work, preserving unaffected native owner outputs. | `test_reporting_owner_handoffs_cannot_be_omitted` |
| IQA-07 | Setting `journal_account_mapping['accounts payable']='Revenue'` changes AP journal liability credits into Revenue credits and still yields COMPLETE/CLOSED. The plain input dict is applied after the challenge, outside native owner certification, without a reporting source movement tie. | Validate governed account mapping and whole mapped journal movement against reviewed source/reporting balances; unauthorized classification changes must fail closed. | `test_journal_account_remapping_cannot_change_accounting` |

Initial independent remediation of five findings is accepted; integration approval remains pending IQA-06–07 fixes and rerun.

Second remediation review: IQA-06 now requires relevant owner-reporting bridge coverage and adds actual dependency edges before execution. IQA-07 now checks an independently labelled exact pack payload and separately compares mapped signed native journal movements with reviewed statement current-minus-comparative balances during CHALLENGE. The reviewer added a new regression recalculating the synthetic pack-review fingerprint after a malicious AP→Revenue mapping; numerical GL checks still reject it. This proves the gate is substantive rather than only a stale-label check.

An omission bypass remains within IQA-07: remove both `journal_account_mapping` and `journal_pack_review`. The native factory case again closes COMPLETE, exposing its unaligned native owner journal pack without the combined GL movement challenge. `test_combined_journal_validation_cannot_be_omitted` is the executable regression. A combined reporting/journal case must either provide a validated pack mapping or surface the missing integrated journal bridge; omission cannot waive the accounting check. Independent rerun after the initial two fixes: 27 tests, 26 PASS, this one bypass FAIL.


## Final independent disposition

The integrated-pack omission bypass was remediated by requiring journal validation whenever completed Financial Statements and multiple native journal owners are present, independent of whether the caller supplies a mapping field. Missing review/mapping now produces a challenged unresolved reporting node. Fixture-only pack review is generated from actual completed native owners directly; it no longer obtains candidate approval by skipping integrated validation.

Final independent rerun command: `python -m unittest orchestration.tests.test_independent_qa -v`. Result: **27 tests PASS** (15.332 seconds). This includes all seven substantive findings, the omission bypass within IQA-07, the recalculated-fingerprint semantic remap attack, real manufacturing completion and negative routing, actual changed imported owner outputs, all public routes, context/observer nonmutation, lifecycle and simple-question controls. Every documented substantive finding now has executable passing regression and has been independently rerun.

Independent disposition: **PASS for the bounded orchestration foundation and synthetic manufacturing integration scope**, conditional on the integration owner's remaining complete repository regression, generated-artifact verification and immutable exact-head CI. This review does not claim arbitrary natural-language coverage, every skill combination, multi-entity execution, persistence readiness or a complete product interface. No substantive accounting changes were made by this independent reviewer.

## IQA-08 — gross-margin presentation basis

The integration author identified a further material synthesis defect during final review: factory gross margin had been labelled as Revenue less Inventory relief alone, while excluding 45,000 of actual unallocated manufacturing expense. The independent reviewer inspected the remediation and authored separate basis/gate regressions.

Remediation keeps the native Inventory owner figures unchanged and retrieves the supplied governed `gross_margin_basis` presentation policy. An approved inclusive basis adds actual `manufacturing_expense` to inventory relief once; an approved relief-only basis leaves that expense separately visible. Missing, unsupported or merely PROPOSED context does not establish the policy: the combined case remains PARTIAL and asks a material presentation question, retains completed accounting and the separately labelled revenue-minus-relief figure, and does not fabricate gross margin.

Independent checks confirm the inclusive factory basis: Revenue 40,000, Inventory relief 11,304, manufacturing expense 45,000, cost of sales 56,304 and gross margin −16,304. The separate revenue-less-relief amount is 28,696. Changing only the approved presentation basis to relief-only yields gross margin 28,696 and keeps the 45,000 factory expense visible. This is a governed presentation alternative rather than a recalculation of specialist accounting.

Executable regressions: amended `test_flagship_quantities_synthesis_and_negative_routes`, `test_missing_margin_basis_asks_material_question`, `test_alternate_approved_margin_basis_preserves_factory_expense`, and `test_proposed_margin_policy_cannot_be_established`.

Final independent rerun after IQA-08: `python -m unittest orchestration.tests.test_independent_qa -q` — **30 tests PASS**, 22.741 seconds. All eight substantive findings and the IQA-07 omission bypass have executable passing coverage. Final bounded-scope independent disposition remains **PASS**, subject to full repository regression and immutable exact-head CI.

## IQA-09 — deterministic cross-process artifact export

Integration artifact comparison identified ordering differences across fresh interpreter processes: native inventory class dictionaries had been iterated into ordered fixture stock/interface populations, and public calculation arrays followed that incidental class order. The integration author remediated this by sorting inventory classes when preparing controlled stock/interface inputs and sorting class metrics during synthesis. This changes deterministic ordering, without changing owner amounts or accounting.

The independent reviewer inspected the ordering changes and executed artifact reproduction in two fresh processes with deliberately different hash seeds: `PYTHONHASHSEED=17 python -m unittest orchestration.tests.test_artifacts -v` and `PYTHONHASHSEED=31 python -m unittest orchestration.tests.test_artifacts -v`. Both **3-test runs PASS** (7.338 and 7.319 seconds), including exact generated-reference reproduction, safe CLI failure output and complete internal record serialization. This verifies generated public/internal/workplan/handoff/journal/challenge artifacts reproduce across independently randomized interpreter ordering.

Final executable-state independent rerun after deterministic ordering remediation: **30 independent tests PASS**, 22.829 seconds. Independent final disposition: **PASS** for the bounded foundation/manufacturing scope. IQA-01–09 and the integrated-pack omission bypass are remediated with executable coverage; artifact reproduction also passes under two fresh-process hash seeds. Complete repository regression and immutable exact-head CI remain the integration owner's final gates.
