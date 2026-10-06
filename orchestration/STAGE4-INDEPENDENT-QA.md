# Stage 4 independent QA history — intermediate only

Review date: 2026-10-06. Branch: `orchestration/multi-entity-multi-period-flagship`; Draft PR #37. This review is independent of the authored checklist and is not final acceptance. Stage 4 remains INCOMPLETE. No commit, push, PR modification, production edit, knowledge edit or delegation was performed by this reviewer.

## Contract reconstruction

The inspected implementation is the ordinary `CAO.run` / Graph / production boundary with ScopeRegistry, CaseRegistry, PeriodRegistry and VersionedExecution. Stage 1 separates legal and Group scopes and posting layers. Stage 2 binds Cases to objective/cycle/scope/period; dependencies and immutable result versions carry exact dimensional identities. Scope or Case parentage never supplies consumption edges. Correction invalidation follows actually consumed version bindings, including blocked records, rather than organizational membership. Closed periods need governed reopening.

Stage 3 adds exact original transaction sides, reviewed relationship classification, native translation and narrowly bounded ordinary-loan IFRS reassessment. Matching is lineage without accounting authority. General framework conversion remains unresolved. Consolidation and Financial Statements own accounting; translations enter Group TB populations rather than duplicated legal postings. Public delivery is curated through `interfaces/public_output.py`.

Stage 4 fixture adds the UK translation/reassessment chain, material reciprocal conflict, blocked downstream accounting/reporting/analytics, corrected clean branch, source-qualified intake snapshots and ordinary selective rework. Original principal/rate facts and independently supplied JSON native snapshots are distinct evidence populations. This synthetic review does not establish authentic approval, full source inventory completeness or a complete realistic Group close.

## S4-IQA01 — incomplete declared intake snapshot population

**Demonstrated generic defect; remediated and independently rerun.** The reviewer removed the complete native workpaper's source ID from both `source_population` and `qualified_scope_sources`, retaining `qualified_input_snapshot`. Initially governed intake accepted the pack: a valid pointer to an inventoried snapshot bypassed inclusion in the supposedly complete declared source population. Expected behavior is rejection of this omitted population.

Permanent reproducer: `IndependentStage4.test_iqa01_complete_snapshot_is_in_declared_source_population`. The primary author added explicit declaration/fingerprint checks in `intake/governed.py`. Fresh independent test now PASS. Initial acceptance history is retained here rather than replacing the finding with a clean checklist.

## S4-IQA02 — unsupported service recharge entered ordinary-loan framework reassessment

**Demonstrated generic runtime defect; remediated and independently rerun.** On a current corrected `uk-conversion`, the reviewer supplied a separately certified native pack with opening principals/books changed from 10 to 9, recharge 1, closing principals/GL retained at 10, and a complete approved services recharge allocation. `CAO.correct` initially accepted it. The current GROUP-EUR result published COMPLETE, `calculations.recharges='1.00'`, and journal entities ENTITY-UK/ENTITY-NL. The economic substitution therefore passed exact closing-value bindings while broadening the ordinary-loan conversion into service recognition and legal-book journals.

`cross_layer_receipts.py` already rejected nonempty recharge populations, but the ordinary runtime `stage3.validate_native_bindings` path did not enforce the same bound. Expected behavior is rejection before publication, without creating service recognition or legal-book journals under a Group conversion node. Permanent reproducer: `test_iqa02_recharge_cannot_enter_ordinary_framework_conversion`.

The primary author added runtime recharge and journal-layer guards. Fresh independent test now PASS. This remediation does not supply a general conversion contract.

## S4-IQA03 — current legal relationship inventory omitted from a CLOSED full-Group conclusion

**OPEN: demonstrated false completeness on an incomplete Stage 4 population implementation.** This is not a finding that timing/FX residuals must be forced to zero. They must enter the actual Group source population or receive an independently reviewed, evidence-backed exclusion/disposition that supports the objective's completeness.

Reconstruction from current native versions after the fixture's correction:

| Current legal relationship | Native source population | Group coverage |
| --- | --- | --- |
| clean | NL/US October ordinary loan | included |
| mismatch | NL/UK October corrected ordinary loan | included |
| timing | UK October principal 30; NL September principal 30 is historical lineage | October UK balance absent; no reviewed exclusion/disposition |
| fx | UK October GBP16 and US October USD20 local carrying amounts for transaction principal 20 | absent from both foreign-operation TBs and Group relationship population; no reviewed exclusion/disposition |

The Group source's `intercompany` contains only clean and mismatch. The UK translated TB has only cash, mismatch loan and equity. The US translated TB has only cash, clean loan, equity and FX income. No `relationship_dispositions` or equivalent independently reviewed exclusion population accounts for timing/fx. The corrected fixture nevertheless reaches `case.outcome='complete'`, `case.status='CLOSED'`, and a current complete public result for the objective requesting the final Group accounting/reporting conclusion.

Permanent reproducers: `test_iqa03_current_relationships_have_group_population_dispositions` and `test_iqa03_uncovered_current_relationships_cannot_close_full_group_objective`. The former independently reconstructs current legal relationship identities, without assuming September is an October closing balance. Expected behavior: a complete evidence-backed inventory flow through translation, Group books, elimination and reporting, or retained partial/blocked full-Group conclusion while coverage is unresolved. An INTERMEDIATE label on generated files does not by itself repair runtime false closure.

## Additional verification and honest limits

Independent tests verify blocked publication contains no accounting authority or journals; material correction invalidates exactly the six consumed downstream nodes; unaffected versions remain current; stale public delivery is partial with no previous totals; wrong legal posting scope, duplicate and wrong-entity translation dispositions, substituted conversion adjustment and invented original transaction source IDs fail; arbitrary provenance objects are excluded from all public routes; dynamic private reviewer names fail closed.

Two exploratory expectations were corrected, not reported as defects. Stale public delivery now safely returns partial/no calculations instead of throwing. Both parity translations have zero journal implications, so omitting their optional posting dispositions creates no duplicate posting and is accepted. Actual duplicate dispositions still fail. These corrections preserve the evidence distinction between unsafe acceptance and a harmless zero-implication case.

The intake-backed correction/rework path still supplies new certified native packs directly through CAO APIs, without a fresh sealed intake inventory for correction confirmations, replacement exports and all subsequent reviewed inputs. That is an incomplete Stage 4 provenance integration gate; the runtime's supported independently reviewed native correction contract alone does not demonstrate a generic regression. Complete source-to-Group economics, non-parity translation/CTA realism, realistic source coverage, all prior flagship migrations, deterministic artifact generation, full repository regression and immutable-head CI acceptance remain outside this intermediate acceptance claim.

## Execution history

Command: `python -m unittest orchestration.tests.test_stage4_independent -v`.

- Initial exploratory probes demonstrated IQA01 and IQA02 acceptance before the primary author's fixes.
- First 14-method executable run after those fixes: IQA01/IQA02 PASS; three failures included one substantive IQA03 and two overstrong trial expectations described above.
- Corrected 14-method independent rerun: 13 PASS, IQA03 population coverage FAIL.
- Final 15-method run: 13 PASS, 2 FAIL, exit 1. Both failures reproduce the same OPEN IQA03 finding: missing timing/fx population disposition and false complete closure. Reruns are not distinct test additions.

No Stage 4 completion, merge approval or final release acceptance is granted.

## Follow-up checkpoint — explicit full-Group population rejection

The primary author added `current_legal_loan_versions` and `validate_group_loan_population` to `stage3.py`. The Stage 4 Consolidation source now declares `group_population_coverage.mode='ALL_CURRENT_LOAN_SIDES'` with exact current legal result versions. Inspection confirms the opt-in gate independently reconstructs current legal loan versions inside the supplied legal perimeter and compares the matching receipt side population against that roster. Missing/duplicated current sides and substituted roster identities reject before native Consolidation publication. Legacy bounded chains deliberately remain outside the opt-in contract; this review does not infer that an absent declaration proves a full close.

Independent executable verification now includes `test_iqa03_generic_gate_rejects_omitted_and_forged_roster` and `test_iqa03_real_flagship_missing_population_fails_safely`. Both PASS: real fixture rework rejects with `Full Group accounting omits or duplicates current legal loan economics`, retains partial/non-CLOSED Case state and emits partial public delivery without accounting totals. Thus the previously demonstrated false-closure behavior is guarded for the declared flagship path. IQA03 remains OPEN because the actual timing/FX books, translation and Group accounting coverage are not integrated and no qualified positive complete control exists.

To keep all other independent attacks runnable, the suite now constructs an explicitly named **test-local legacy bounded attack control**. It removes only this new opt-in declaration from an isolated Consolidation input and recertifies that test input; it edits no runtime or fixture files. Its apparent complete state is never used as acceptance of the full objective. The actual flagship must still satisfy permanent positive accounting integration and population coverage tests, which remain hard failures rather than skipped or expected failures. Reproducing the safe failure alone cannot turn these acceptance failures into passes.

Follow-up command remains `python -m unittest orchestration.tests.test_stage4_independent -v`. The first adapted 17-method run executed all attacks: 15 PASS, one coverage assertion FAIL and one positive integration ERROR caused by the expected safe rejection. The positive requirement was subsequently expressed as an explicit assertion failure for clearer reporting; latest rerun counts follow below. All earlier finding and run history above is retained.

Latest follow-up rerun: **17 methods, 15 PASS, 2 FAIL, exit 1**. Both outstanding failures are intentional hard positive-acceptance requirements for OPEN IQA03; generic omission/roster rejection and real safe failure PASS. IQA01/IQA02 remain PASS. Stage 4 remains INCOMPLETE.

## Fresh continuation separate-context review

A fresh independent reviewer reconstructed current population and native owner contracts and reproduced S4-IQA04 (self-shortened legal perimeter). See `STAGE4-POPULATION-INDEPENDENT-QA.md` for original reproducers, generic remediation, four permanent attacks, seven fresh sealed replacement attacks, and independent rerun: 11 distinct tests PASS. This preserves prior IQA01/IQA02/IQA03 history. IQA03 and final Stage4 acceptance remain OPEN; this is not a zero-unresolved-final-findings claim.
