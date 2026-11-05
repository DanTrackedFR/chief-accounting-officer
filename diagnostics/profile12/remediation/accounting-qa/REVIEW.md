# Independent accounting remediation QA

Reviewer: independent accounting QA agent (separate from implementation), 5 November 2026.
Candidate initially tested: `3d8458eac0defdc52f7644638d12c9fe98af4c90`.
Scope: owner-authorized Profile 1.2 remediation, not full release acceptance or new standards approval.

## Method

Fresh synthetic asset amount 24,000 / opening accumulation 6,000 / remaining life 6 years; fresh supplier invoice 360; accrual 7 × 80 less 60 with opening 90. Expected annual charge is 3,000, disposal carrying amount 15,000, credit/cash consideration 18,000, independent closing accrual 500 and adjustment 410. Existing service test harness is reused only for transport/setup. Scenarios and accounting assertions are newly authored rather than copies of implementation tests.

Every case uses authenticated production loopback HTTP, a real queued job, native persisted workpaper, reopened service job equality and idempotent retry equality. Every retained journal is independently checked for balanced debits and credits. Each compressed evidence record includes exact input, public result, native result, runtime head and production helper hashes. Historical diagnostic fixtures/evidence are unchanged.

Reviewed authoritative defect register/HANDOFF, Profile 1.2 design, AP governed factory recognition/transaction-substance rules, existing fixed-asset charge and opening/disposal workflow, source screening/execution, standards-evidence ringfence. No normative claim was promoted or represented as newly source-verified.

## Initial result

`python diagnostics/profile12/remediation/accounting-qa/test_accounting_qa.py`: **17 methods, 13 passing, 4 failing**, no errors/skips. See `initial.log` and `initial-evidence/`.

| ID | Related remediation | Reproduction | Expected behavior | Initial finding |
|---|---|---|---|---|
| AQA-01 | ENG-05 / ACC-05 evidence isolation | Valid invoice 360, opening AP 0, payments_total="invalid", no payment detail | Preserve invoice and 360 journal; qualify balance evidence | Global blocked result discards independently supported invoice |
| AQA-02 | ACC-05 overlap isolation | Malformed invoice and independently identified accrual, but accrual supplier is an object; overlap_resolved=true | Resolution of overlap must not validate malformed supplier | Closing accrual 500 and 410 adjustment are incorrectly retained |
| AQA-03 | ACC-04 legitimate affirmative screening | `This invoice is not disputed, but the supplier disputes the obligation.` plus disputed_obligation=false | Affirmative clause conflicts with negation; block/qualify | Negated `disputed` stripped and `disputes` missed; 360 invoice SUPPORTED |
| AQA-04 | ENG-05 payment evidence reconciliation | 2026 Case; matching aggregate/detail payment 120 dated 2027-02-01 | Retain invoice; qualify 2026 closing AP until date/scope contradiction resolved | Closing AP 240 is SUPPORTED despite out-of-period payment |

Other challenges passed: invalid boolean disposal variants (0/1/string/null/array/object), literal false and omission, supported cash and credit disposals, contradictory/malformed receipt facts, mixed rejected disposal, invalid opening accumulation plus linked addition with no residual journals, equal opening gross/accumulated boundary, refundable-deposit exclusion with valid service retention, simple dispute negations, structured affirmative despite negated text, matched/conflicting payment totals, independent accrual with malformed invoice, unresolved overlap rejection.

## Disposition

**Not cleared at initial candidate.** AQA-01–04 were reported to the implementation agent for narrowly scoped correction. Their final dispositions are recorded below. These are refinements of the existing defect boundaries, not additional stable owner defect IDs. Existing formal/Profile 1.1 analogous owner behavior is outside these changes and was not silently rewritten.


## Final independent review

**Cleared for the bounded remediation checkpoint:** 18 methods pass, zero failures/errors/skips; 18.662 seconds. This is not full Profile 1.2 release acceptance. `final.log` and `evidence/` retain final outputs. All 32 executed fresh scenarios retain equal results after restart and idempotent retry. Method count is 18; repeated scenarios/subtests are not counted as additional test methods.

The initial four findings were corrected by the implementation agent, not this reviewer:

- AQA-01: scoped invalid opening/payment aggregate handling now retains supported invoice work and qualifies closing AP.
- AQA-02: accrual supplier validation now occurs independently of overlap resolution.
- AQA-03: affirmative dispute inflections remain detected after stripping explicit negations. An added boundary initially found `not disputing` falsely blocked; that intermediate result is preserved in `negation-boundary.log` and `intermediate-evidence/`. The final suite also passes `no disputes` and `does not dispute`, while still blocking a separate affirmative clause and structured affirmative indicator.
- AQA-04: supplied payment `date` and `payment_date` are checked against the Case period before a supported AP roll-forward is asserted.

The prior 17-method correction rerun is preserved separately in `intermediate.log`; this precedes the additional negation boundary and is not presented as the final acceptance population. No test assertion was weakened to make it pass.

Final production source identity: `98c89f9ae3f76fae441a86edeeb6232dd5d790ef` (the production helper hashes below are identical in every final scenario and were checked against that commit):

- `skills/source_execution.py`: `771101a3f38100dd82a7a452b466f0161dc51473e901db32815c9b3d7b378ef9`
- `skills/source_screening.py`: `9ffae190a4dd8e7fbc7e185b9b1d744da9e3154b8140a81f0a5d6d3282fadb07`

No unresolved accounting remediation blocker remains in this bounded review. Qualified unsupported deposit/settlement routes remain unresolved rather than fabricated; textual screening remains deterministic and bounded, not a claim of general natural-language understanding. Formal/Profile 1.1 owner behavior, external authoritative standards-source reverification, full regression, integration with original customer uploads and deployed TrackedFR retesting are not claimed by this review. The broader compatibility/governance checks are owned by the implementation and independent engineering review.

## Independently justified compatibility test correction

The old `skills/tests/test_presumed_accounting_qa.py::test_disposal_gain_independently_reperformed` supplied sale authorization, date and proceeds of 400,000 but no settlement evidence. Its arithmetic expectation (70,000 gain after 90,000 depreciation on 600,000 gross / 180,000 opening accumulation) remains correct for a supported completed sale; it did not establish cash receipt. Following ACC-03, indexing an accepted asset on those incomplete settlement facts is no longer a valid positive-control expectation.

The correction **retains the original incomplete fixture as a negative subcase**: it must produce UNRESOLVED, no journal and specific validation requirements. The same method then adds explicit `cash_received=true` and `payment_terms=cash` before asserting all original gain and closing-balance expectations, plus a new 400,000 cash-debit assertion. No original accounting amount assertion was removed or weakened. The method count is unchanged. The targeted corrected method passes (`compatibility-fixture.log`). The independent hosted settlement-negative method also now tests omitted receipt/terms with the fresh 18,000 disposal case, including retry/reopen; its targeted rerun passes (`omitted-settlement.log`). This is a contract-driven fixture correction independently reviewed by the accounting QA agent, not acceptance of a changed accounting answer solely to turn a test green.
