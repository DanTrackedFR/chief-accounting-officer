# CAO MVP Build 3 — independent adversarial QA

Status: IN PROGRESS. Separate reviewer; no production changes, no certification of final release yet.

Reviewer inspected Build 1/2A integration handoffs, local adapter, context resolver, document adapters, model boundary, investigation loop and persistence private Case metadata. Independent tests are `intelligence/tests/test_independent_qa.py`, authored without implementation ownership.

## Initial executable challenge

Command: `python -m unittest intelligence.tests.test_independent_qa -q`.
Initial expanded run: 25 distinct tests; exit 1; 23 passed, 2 substantive failures.

1. **B3-IQA-01 — ambiguous active contracts.** Two active contracts with different observed prices generated no conflict or specific disambiguation request. Regression: `test_ambiguous_contracts_block_and_request_resolution`. Status: RESOLVED; independent expanded 28-test rerun passes this regression.
2. **B3-IQA-02 — inferred contradiction erased on continuation.** Two different model price interpretations sharing actual source lineage produced `inferred-price`, then a continuation without model output removed the unresolved conflict. Regression: `test_model_conflict_persists_without_new_inference`. Status: RESOLVED; independent expanded 28-test rerun passes this regression.

Passing challenges include untrusted APPROVED context, other-entity exclusion, conflicting currencies, future effective dates, wrong-company/currency document rejection, incomplete CSV population, duplicate headers, XLSX formula refusal and retained hidden rows, scanned/active PDF refusal, prompt-injection observation status, fabricated model citations, bounded retry, missing evidence, immutable event retries, durable restart request parity, frozen context after onboarding edits, cross-company denial and mismatched document supersession refusal.

Unfamiliar prepayments example uses opening 200, additions 4500, consumption 400 and closing 4300. Observational increase is 4100, residual 0, and request identifies supporting invoice ORION-573 from the actual movement row. Incomplete-population variant returns no calculation and records reconciliation population conflict. These are investigation observations, not certified accounting outputs.

## Remaining review

Qualified actual native owner execution, journal duplication/correction, recovery at accounting commit boundaries, hosted Build 3 authorization/job coverage, final deterministic proof and complete release regression remain to be independently reviewed. No live-model result has been verified. Do not represent this interim report as acceptance.

## Expanded parser review

Expanded run: 28 distinct tests, exit 1; 26 passed and 2 parser-boundary errors. B3-IQA-03: malformed XLSX leaks `zipfile.BadZipFile` through local API; B3-IQA-04: malformed PDF leaks `pypdf.errors.PdfReadError`. Both must return a safe blocked envelope without changing the Case. Reproductions: `test_malformed_xlsx_returns_safe_envelope`, `test_malformed_pdf_returns_safe_envelope`. Status: OPEN pending remediation/rerun. Forged XLSX dimensions regression passes: actual XML rows are retained despite smaller declared dimensions.

## Inference and source immutability

Expanded 30-test run: exit 1, 26 pass; previous parser findings remain OPEN.

B3-IQA-05: `Boundary.infer` passes bound snapshot scope/context objects directly to model provider. A provider can mutate framework/currency without changing context snapshot identity. `test_model_provider_cannot_mutate_bound_snapshot` reproduces. Status OPEN.

B3-IQA-06: `ingest` result metadata aliases caller document metadata. Mutating the caller input after extraction changes source metadata without updating the extraction hash. `test_document_mutable_input_cannot_change_lineage` reproduces. Status OPEN.

Independent parser-remediation rerun: 30 distinct tests, exit 1; 28 pass, only B3-IQA-05/06 fail. B3-IQA-03/04 are RESOLVED by actual reviewer rerun: malformed binary sources now return blocked envelopes. Final acceptance remains pending.

## Current independent rerun

`python -m unittest intelligence.tests.test_independent_qa -q`: 30 distinct tests, exit 0, all PASS (3.033 seconds). B3-IQA-01 through B3-IQA-06 all RESOLVED by actual separate-reviewer rerun. This is scoped component/interface acceptance; remaining qualified native execution, hosted integration, correction and full release gates listed above are not yet accepted.

## Qualified native execution challenge

Five further independent tests initially passed: actual unfamiliar revenue native owner EUR11,494.38; restored execution retry with `CAO.run` forced to fail preserves journals/revision; altered source contract price, removed bindings, changed reviewed economics and wrong Case pack reject.

The expanded 36-test run after concurrent scope changes has 34 pass and 2 failures: successful native revenue and HTTP durable job. Isolated traceback identifies `scoped_context` rejecting missing governed temporal registry. This is an in-progress integration finding, B3-IQA-07, OPEN pending normalization and reviewer rerun. True HTTP test confirms direct synchronous execute refusal and durable job acceptance; native accounting completion is not yet reaccepted on current tree.
