# Independent Government Grants implementation QA

Reviewer: `/root/implementation_qa`, an independent Codex agent delegated by the release agent. This reviewer did not author or change substantive accounting methods. This is an actual agent identity, not an authenticated human reviewer, management approval or external audit opinion. Synthetic case approvals exist only to exercise software controls.

## Review method

Reviewed the applicable repository AGENTS controls, current workflow, grant knowledge gate, production boundary, framework methods and shared accounting helpers. Shared fixture code supplies only the document/control shape. The independent numerical constructor overwrites the authored fixture's amounts, schedules, disclosure amounts and GL; it never calls the authored arithmetic oracle or derives expected accounting amounts from production results.

Independent numerical facts: agreement 137.03, actual eligible cost basis 913, current income expenses 271.11, or asset expense 91.3. Independently calculated income matching is 137.03 × 271.11 / 913 = 40.69 after half-up cents rounding, closing deferral 96.34; asset matching is 13.70, closing deferral 123.33. UK performance recognizes 137.03 when specified conditions are met; the accrual route recognizes 40.69. Supported basis methods adjust 137.03 with no grant-income release. Repayment70 consumes opening deferral30 and creates current expense40.

The test suite independently challenges four-framework arithmetic, UK model distinction, asset basis routes, nonmonetary clearing, advances, clawback, source mutation, source-to-GL stocks, cumulative award entitlement, income expense denominator, US intangible scope, compliance, adoption, framework/period editions, AASB Tier2, UK netting, scope exclusions, duplicate receipts/ownership, entity/currency/framework/period mismatch, valuation, prior-error repayment, disposed assets, disclosure accuracy, stale/incomplete certification and public-source privacy.

Local workflow probes isolate accounting methods using the supplemental namespace; they are not a replacement for production qualification. Separate tests call `production.assess_case` to exercise certification and public rendering. Local arithmetic tests do not claim to authenticate grantor records or source evidence.

## Findings and permanent reproductions

| ID | Finding | Permanent reproduction | Retest status |
|---|---|---|---|
| IQA-GRANT-01 | Income expense denominator could diverge from independently supported eligible-cost population, accelerating income. | `test_income_pattern_not_supported_by_cost_population` | Corrected; independently passed. Initial defect was identified from code and corrected before its first test execution. |
| IQA-GRANT-02 | Opening receivable could exceed award entitlement. | `test_opening_receivable_cannot_exceed_total_award` | Corrected; independently passed. Initial defect was identified from code and corrected before its first test execution. |
| IQA-GRANT-03 | Deferred grant stock could coexist with a basis presentation. | `test_prior_deferral_in_basis_route_excluded` | Corrected; independently passed. |
| IQA-GRANT-04 | US nonmonetary intangible transfer was accepted despite the documented Topic832 exclusion. | `test_us_nonmonetary_intangible_excluded` | Corrected; independently passed. Initial defect was identified from code and corrected before its first test execution. |
| IQA-GRANT-05 | Equal offsets to opening/closing/statement GL stock could pass journal-delta reconciliation while contradicting actual grant stocks. | `test_gl_parallel_stock_shift_is_not_reconciliation` | Reproduced as acceptance before correction, then independently passed after aggregate source-stock checks. |
| IQA-GRANT-06 | Opening unpaid prior recognition100 plus new recognition137.03 could exceed award137.03 without blocking. | `test_opening_unpaid_prior_grant_plus_addition_exceeds_entitlement` | Reproduced, corrected using reviewed cumulative recognized/cash/income/basis history, then independently passed. |

| IQA-GRANT-07 | A fully recognized and fully paid award could receive a second full award as a new advance, bypassing current-only cash ceilings. | `test_advance_cannot_receive_previously_paid_award_again` | Reproduced, corrected with all-time cash ceiling and new-advance prior-recognition guard, then independently passed. |

Initial execution: 30 tests, 29 passed, IQA-GRANT-05 failed (exit1). After source-stock/disclosure fixes and three additional adversarial tests: 33 tests, 32 passed, IQA-GRANT-06 failed (exit1). Disclosures in the independent numerical fixture were updated to match its independently calculated amounts after the release agent added actual quantitative disclosure controls.

Command: `PYTHONPATH=skills:skills/tests python -m unittest skills/tests/test_independent_government_grants.py`.

## Boundaries and release conclusion

Loans/forgiveness, basis repayments, prior errors, changed assets and prior-advance conversion intentionally remain blocked. This review does not authorize those routes, alter historical reference artifacts, authenticate management judgments, or provide automatic ERP posting. Full repository regression and exact-head CI remain the release agent's separate obligations.

After the cumulative-history correction, 34 tests passed (exit0), including a positive follow-on release with opening deferral82.22, independently calculated income40.69, closing deferral41.53 and no current recognition. An additional prior-paid-award advance challenge produced 35 tests, 34 passed, IQA-GRANT-07 failed (exit1).

Final original independent retest: **36 tests passed, zero failures/errors/skips, exit0**, using the command above with `-v`. IQA-GRANT-07 is independently resolved. An additional production test asserts complete execution, repeat-result equality and exact net account movements (cash137.03; receivable0; deferred credit96.34; income credit40.69). Public privacy testing now explicitly requires complete production status before checking the allowlisted output, avoiding vacuous success through a blocked result.

Independent implementation acceptance for the documented bounded routes: **PASS**, subject to unchanged reviewed files and the separate full release gates. No skipped test has been represented as passing.

## Final alias and native integration challenge

The release agent independently identified a duplicate agreement alias route and added a unique source-agreement guard. This reviewer then constructed a permanent test with a second distinct grant/economic identity, distinct cost/asset/bank identities, correctly doubled source population/GL, and the same original agreement ID. The test requires an agreement-specific failure, proving that another duplicate-identity guard cannot produce a vacuous pass. `test_duplicate_agreement_cannot_alias_distinct_economic_records` independently passes. This finding was first reported by the release agent; this reviewer does not claim its discovery or pre-correction execution.

An independent native orchestration test supplies the separately calculated137.03/913/271.11 case through `CAO.run`, requires complete grant-only execution and income40.69, then supplies independently missing compliance and requires blocked owner status with no executable journals. The native boundary legitimately retains a structured blocked result, so the initial test's expectation of an absent result was corrected after inspection; this was a test-assumption correction, not an accounting fix. Local SQLite/HTTP authored integration tests were read but are not represented as independently authored QA tests.

Final expanded independent execution: **38 tests passed, zero failures/errors/skips, exit0**, using the command recorded above. Bounded independent acceptance remains **PASS**.

## Condition due-date contradiction challenge

The release agent identified the additional distinction between supported future compliance assurance and an already-due failed condition. The reviewer independently challenged the resulting due-date/current-cutoff control without reopening standards research. Permanent tests cover unmet conditions due before or exactly on reporting cutoff across IFRS/AASB/US/UK accrual, and positively assured future conditions across the same frameworks. UK performance's independent unmet-condition test continues to block regardless of future due date.

Separate tests require actual current cutoff for recognition, advance and repayment, verify that a failed due condition can retain actual cash as an unrecognized advance with zero income, and verify supported clawback consumes deferral before expense without recognizing new income. Missing due dates produce a production blocked result with no executable journals.

Final expanded independent execution after this correction: **44 tests passed, zero failures/errors/skips, exit0**, command `PYTHONPATH=skills:skills/tests python -m unittest skills/tests/test_independent_government_grants.py`; elapsed12.272 seconds. The reviewer did not author the underlying correction and does not claim discovery or pre-correction reproduction of this release-agent finding. Bounded independent acceptance remains **PASS**.

## Final source timing, asset and expense-pattern challenge

The independent numerical fixtures now supply actual remaining owner expense basis641.89 (income) or821.7 (asset), without deriving it from production grant amounts. The independently constructed prior-release case uses actual remaining expense276.69 after prior365.2 and current271.11 of the913 total basis. Resulting cent-rounded grants continue to reconcile to96.34,123.33 and41.53 respectively.

Eight additional permanent challenges verify: US costs incurred after grant recognition block; asset expense before availability blocks; zero owner useful life blocks; residual-value/depreciable-basis contradiction blocks; non-US ordinary inventory cannot alias a long-term asset; future grant schedule needs supported owner expense; an early future row cannot accelerate grant release despite aggregate closing balance tie; and partial repayment retaining deferral requires the separately revised owner expense route. This review consumes the asset owner's supplied expense pattern; it does not reperform depreciation or choose useful lives.

Final method-freeze independent execution: **52 tests passed, zero failures/errors/skips, exit0**, command `PYTHONPATH=skills:skills/tests python -m unittest skills/tests/test_independent_government_grants.py`; elapsed9.068 seconds. **PASS** applies to the bounded methods and source hashes below, subject to separate repository regression and exact-head release gates.

## All grant-owned stock and posted-component retest

The release agent extended IQA-GRANT-05 source-stock reconciliation to current-period grant income/repayment expense, contra-basis, repayment payable and nonmonetary clearing. A new independent permanent test shifts each account's opening, closing and statement by17.37 together while leaving the actual grant history/component amounts unchanged; it specifically requires a source-stock/GL failure. It covers normal income, clawback expense/payable, asset deduction basis and nonmonetary clearing, preventing journal-delta reconciliation from masking a stock contradiction.

A separate independent test marks an otherwise complete and independently captured grant economic component already posted, and specifically requires a posted-component reconciliation blocker. This verifies the bounded unposted journal route does not reexecute an already-owned posted component.

Final immutable-freeze independent execution: **54 tests passed, zero failures/errors/skips, exit0**, same command above; elapsed12.556 seconds. Bounded independent implementation acceptance remains **PASS** for the reviewed hashes below.

## US nonmonetary cost-accumulation withdrawal

The release agent withdrew US nonmonetary cost accumulation after distinguishing cost-to-entity original-asset-owner accounting from an additional grant benefit/contra-basis deduction. This reviewer independently constructs both attempted cost-to-entity and fair-value variants with matching measurement election, separate owner clearing balance and no cash. Permanent production tests specifically require the qualified original asset-owner adapter blocker and no executable journals for both attempts.

A positive production test retains the supported US tangible nonmonetary fair-value/deferred route and independently verifies grant income13.70, remaining deferral123.33 and zero basis adjustment. US monetary cost accumulation remains covered by the independently calculated positive basis-route test.

| US route | Independent acceptance |
|---|---|
| Monetary cost accumulation | Supported bounded PASS |
| Tangible nonmonetary fair-value/deferred | Supported bounded PASS |
| Nonmonetary cost accumulation, either FV or cost-to-entity election | BLOCKED pending qualified original-cost owner adapter |
| Nonmonetary intangible | BLOCKED scope exclusion |

Final independently executed suite: **56 tests passed, zero failures/errors/skips, exit0**, same command above; elapsed15.795 seconds. Bounded implementation acceptance remains **PASS**, with the withdrawn route expressly excluded. No standards claims or source-assurance classifications were altered by this reviewer.

## Nonmonetary valuation-date binding

A final permanent independent production test uses each supported framework's nonmonetary fair-value/deferred route. Valuations dated one day earlier or one day later than recognition remain within the reporting year but must produce a blocked date conclusion and no executable journals. Same-day valuation positively retains complete production execution and independently calculated grant income13.70 across IFRS/AASB/UK/US. This closes the distinction between merely in-period valuation and the actual matched recognition measurement date; no valuation is generated by the engine.

Final independent suite after this source binding: **57 tests passed, zero failures/errors/skips, exit0**, same command above; elapsed14.620 seconds. Bounded acceptance remains **PASS** for the reviewed hashes below and the explicit unsupported-route exclusions in this report.

## Reviewed source hashes

- `skills/government-grants/workflow.py` SHA256 `316b7baa8577821633431b655de324f771d26b4065effeb5b6a0488b9a07e627`
- `skills/grant_knowledge.py` SHA256 `1c1b0c8844a75f064e2ed5b499102033990badb29ee6c8748778381e35150c3d`
- `skills/production.py` SHA256 `10a34f9fcbe28bb291373fe9c640470ee8bd1202b46590ec66a2a2105d28dfb4`
- `orchestration/planning.py` SHA256 `07a195645f0611eb07eebc2c06d43b37b24cf657d892a9123db5f1e129edfbf8`
- `skills/tests/test_independent_government_grants.py` SHA256 `26492c81af1497e0eb41723e24e5b1b7d512c1d4bf5a13b452b1cfc98b5ab20f`
