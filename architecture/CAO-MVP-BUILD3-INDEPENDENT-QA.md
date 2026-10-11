# CAO MVP Build 3 — independent adversarial QA

Status: CORRECTED COMPONENT/INTEGRATION QA PASS — 51 independent tests; fourteen resolved findings. Previous full local acceptance is historical; corrected-tree proof, full regression and exact-head publication gates remain pending.

Separate reviewer inspected Build 1/2A handoffs, local adapter, context resolver, document adapters, inference boundary, investigation loop, private durable Case metadata, native correction/recovery and HTTP jobs. Reviewer authored `intelligence/tests/test_independent_qa.py` without production implementation ownership. Synthetic reviewed packs are explicitly test-only and come from authored fixtures; independent tests mutate/substitute them adversarially. Production does not import test certification helpers.

## Independently reproduced findings

| ID | Defect | Permanent executable regression | Resolution |
| --- | --- | --- | --- |
| B3-IQA-01 | Two active contradictory contracts had no disambiguation conflict | `test_ambiguous_contracts_block_and_request_resolution` | Explicit active-contract ambiguity blocks; rerun PASS |
| B3-IQA-02 | Model contradiction disappeared on continuation without inference | `test_model_conflict_persists_without_new_inference` | Historical inferred conflict remains; rerun PASS |
| B3-IQA-03 | Malformed XLSX parser exception escaped safe API envelope | `test_malformed_xlsx_returns_safe_envelope` | Parser failure safely blocked; rerun PASS |
| B3-IQA-04 | Malformed PDF parser exception escaped safe API envelope | `test_malformed_pdf_returns_safe_envelope` | Parser failure safely blocked; rerun PASS |
| B3-IQA-05 | Model provider could mutate frozen scope/context through aliased objects | `test_model_provider_cannot_mutate_bound_snapshot` | Provider receives isolated copies; rerun PASS |
| B3-IQA-06 | Caller metadata mutation changed extracted document lineage after hashing | `test_document_mutable_input_cannot_change_lineage` | Metadata isolated; rerun PASS |
| B3-IQA-07 | Governed Period registry tuple/list wire mismatch blocked native revenue and hosted jobs | Native revenue and HTTP integration tests | Canonical wire scope preserves exact native qualification; rerun PASS |
| B3-IQA-08 | Explicit unknown context item applied its placeholder investigation threshold | `test_unknown_context_value_cannot_be_applied` | Unknown state remains unresolved; independent rerun PASS |
| B3-IQA-09 | Raw hidden-sheet parser warning exposed private source-note wording | `test_parser_warning_cannot_leak_private_source_notes` | Curated warning preserves limitation without arbitrary sheet title; independent rerun PASS |
| B3-IQA-10 | Post-execution inference conflict still delivered COMPLETE | `test_post_execution_inference_conflict_blocks_delivery` | Current delivery blocks unresolved conflict, native history/currentness remain exact; independent rerun PASS |
| B3-IQA-11 | Requested invoice remained missing/OPEN after exact invoice arrival | `test_received_specific_invoice_not_requested_again` | Acquisition question closes; source-referenced qualification followup remains stable and blocked; independent rerun PASS |
| B3-IQA-12 | Explicit native GROUP Scope type was unsupported, selection defaulted to legal entity | `test_explicit_group_scope_retained_in_durable_case`, `test_group_cannot_masquerade_as_legal_entity` | Existing ScopeRegistry validates true GROUP/GROUP_CASE with no legal identifier; durable restore and masquerade rejection rerun PASS |
| B3-IQA-13 | Nondefault execution dimensions bypassed framework qualification | Three selection-qualification tests | Resolve self-applicable framework then qualify execution dimensions before conflicts/scope; rerun PASS |
| B3-IQA-14 | Nondefault policy conflict rejected snapshot instead of preserving durable context alternatives | `test_nondefault_policy_conflict_preserved_in_blocked_case` | Restrict selection collector to execution dimensions; scoped policy conflict and blocked Case survive restart; rerun PASS |

Zero unresolved substantive findings in the reviewed paths. This does not substitute for complete repository regression or exact-head Actions.

## Actual independent rerun

Command: `python -m unittest intelligence.tests.test_independent_qa -q`.

51 distinct independently authored tests; exit 0; all PASS; elapsed 66.636 seconds. The strengthened post-execution conflict regression additionally passed a targeted independent rerun (1 test, exit 0), without double counting. Reruns are not added to this count.

Coverage includes untrusted APPROVED context, other-entity exclusion, conflicting currencies, effective dates, wrong-company/currency source rejection, CSV population completeness, duplicate headers, formula refusal, hidden row retention, forged XLSX dimensions, scanned/active PDF refusal, inert prompt injection, fabricated inference references, retry bounds, missing evidence refusal, request deduplication, immutable event retry, frozen Case snapshots after onboarding edits, cross-company isolation, document supersession identity, native source bindings, altered contract amounts, altered reviewer-certified economics and wrong Case packs.

## Actual accounting and investigation results

Unfamiliar prepayments: opening 200, additions 4500, consumption 400, closing 4300. Native investigation observation reports increase 4100, residual 0, and identifies supporting invoice ORION-573 from the movement row. Missing completeness returns no calculation and a population conflict. These are observational investigation calculations, not certified accounting economics.

Unfamiliar DOCX customer contract and separately reviewed native intake invoke the real Revenue Recognition owner. Actual revenue is EUR11,494.38. Changing extracted contract price to EUR90,000 while reviewed facts retain EUR17,350 rejects. Omitting document bindings, changing certified economics and substituting Case identity also reject. Restore/execute retries with native CAO execution forced to fail retain exact public result and revision, proving retries do not run economics again.

A real local HTTP server accepts the same native execution through durable jobs, refuses direct synchronous execute, returns exact local public-result parity, preserves checkpoint on a new-key retry and rejects another-company job access.

## Correction and recovery

Qualified contract successor v2 changes fixed price to EUR18,000. Upload immediately returns STALE and refuses ordinary execute. Native CORRECT and REWORK refresh governed synthesis. Original ResultVersion fields remain byte-equivalent except legitimate state/superseded_by transitions; both document versions remain; one rework plan is retained. Retrying the immutable correction preserves checkpoint and journals.

Deterministic fault injection interrupts immediately after native prepare and immediately after native recovery commit. A fresh ExecutionInterface restores the same Case and finishes correction/rework. Both variants retain exactly two operations (one correction, one rework), one rework plan, and a complete governed result. These are deterministic exception-at-commit-boundary tests; final proof should separately describe any real-process kill tests rather than conflating them.

## Remaining release review

The prior complete local regression is retained historical evidence below. Corrected-tree full local regression, validators/source hashes and exact-head publication gates are pending. Current corrected proof and component/integration tests are independently accepted. No live-model evaluation has been verified by this reviewer. DOCX body-only extraction warning and PDF reading-order uncertainty must remain visible. Specialist PRs and historical artifacts were not modified by this reviewer. No commit, push or merge performed.

## Final proof and release-gate review

Final integrated proof SHA256: `51cb8df87c36d6b64995594b54c1196a28e1ed6d8d4e3e922600224849832920`. The seed manifest records PYTHONHASHSEED 19 and 941 with exit statuses 0/0 and byte-identical output. Reviewer independently checked that manifest hash equals the actual final proof hash, all six retained original sources decode to the stated bytes/length/hash/format and match the separate committed originals under intelligence/release/sources/, both context snapshot hashes verify, and original immutable native version hashes survive correction. There are two revenue DOCX versions, three reconciliation/movement CSVs and one supporting invoice text source.

Final proof preserves source lineage, context/history, requests, calculations and exact Case/version identities. Native corrected revenue is COMPLETE; prepayment increase is 8100 and its invoice request is derived from movement QX-7826. Prepayment accounting remains explicitly BLOCKED because no independent native accounting pack was supplied. Live model evaluation is false, with absent credentials accurately stated. Synthetic fixture review is not represented as production authenticated reviewer approval.

Structural contract review of ten proof investigation outputs and nested evidence requests passed. Readiness caching explicitly requires the Build 3 intelligence and deterministic proof step; a legacy green run lacking that step cannot satisfy the final gate. No unresolved substantive findings remain in independently reviewed component/integration/proof paths; the prior complete local release regression is historical; corrected-tree local and exact-head Actions/readiness gates remain pending.

## Exhaustive orchestration sharding review

Reviewer inspected the seven-worker module runner and CI invocation. The runner discovers the original `test_*.py` population independently, then requires sorted aggregate test IDs to equal that full discovery exactly and forbids duplicate IDs. Every isolated module must return exit 0 and a successful unittest result. Missing recursive tests, failed imports, duplicate populations or failed subprocesses cannot produce PASS. Each module's result, log path, exit status and log hash is retained. No test selection narrower than the original discovery is accepted; this changes execution isolation/concurrency, not accounting acceptance expectations.

The interrupted original sequential orchestration attempt has no successful full-suite result and is not credited. The complete final sharded manifest has been independently accepted. The runner now also requires shard result modification time to be at or after attempt start; a failed attempt cannot credit stale prior result IDs. Nonzero shard exits independently prevent PASS. Final accepted suite0 contains all fresh successful shard results and exact discovery equality.

## Supporting document continuation and final guard

Distinct supporting invoices do not falsely make the three reconciliation populations ambiguous; independent regression retains increase4100, no false conflict and legitimate BLOCKED. Exact received invoice replaces its acquisition request with a targeted dates/allocation qualification request referencing actual invoice fields. Continuation preserves request IDs and does not certify source observations.

Reviewer also inspected the no-native-rework-plan guard and independently executed an original native COMPLETE Case followed by rework without a plan: safe blocked envelope, unchanged checkpoint and exact public result. This one-off check is not counted as a new unittest or a duplicated test. Final frozen proof/source/followup review verifies the regenerated hash recorded above, all six retained original files and a source-referenced QX-7826 qualification request replacing acquisition. Independent47/twelve-resolved status remains current; the prior full local regression is historical; corrected-tree local and exact-head CI/readiness gates remain pending.

## Group Scope qualification

Reviewer reproduced the original explicit GROUP item rejection against the prior committed resolver. The corrected resolver consumes typed scope assertions through the existing native Scope/ScopeRegistry, not a separate scope authority. Independent tests verify GROUP/no legal entity ID, actual native GROUP_CASE and GROUP Scope registry binding, exact durable snapshot restoration and rejection of a group masquerading as a legal entity. Whole47 independent suite passes after this final context extension. Final regenerated proof independently verifies explicit GROUP_CASE, native GROUP/no legal identifier and exact group snapshot hash while the subsidiary retains UK_GAAP/GBP. The fresh-process proof script asserts durable GROUP_CASE binding and restart parity. Final hash above matches the actual regenerated proof and seed manifest; all six original retained sources remain exact. The prior full local regression is historical; corrected-tree local and exact-head CI/readiness gates remain pending.

## Full orchestration release evidence review

Reviewer independently verified completed suite0: 1,344 distinct tests, 61 isolated modules, every module exit0/PASS, no duplicate IDs, and aggregate IDs equal fresh full `test_*.py` discovery exactly. All 61 retained module log hashes match actual bytes. The original full-company fresh-process artifact test passed (1 test, 2,646.822 seconds) rather than being replaced or regenerated.

Interrupted sequential attempt is retained separately: exit130, complete=false, credited_as_pass=false, credited_distinct_tests=0. Reviewer verified both compressed and original decompressed log hashes. It is not counted as a successful run. This preliminary review was followed by the complete final local acceptance below; exact-head CI/readiness remain external gates.

## Superseded prior local release acceptance (historical)

Reviewer independently audited `intelligence/release/release-regression.json` (SHA256 `0857ff56bee6f7a2f143cc7bc056e966d8a3a5fc3cc2c9e33e53a1f2df4fc156`): complete=true; **3,160 distinct tests**, counted once; 13 suites with actual populations 1344/1180/17/53/10/83/35/4/7/262/55/44/66; every suite exit0/PASS; zero failures, errors or skipped tests. All 21 successful execution logs (13 suites, seven validators and whitespace check) match retained byte counts/SHA256. Seven validator outputs show no errors; `git diff --check` log is empty and exit0. All 298 recorded Python file hashes match current source and exactly cover the six declared engine/interface source namespaces. Independent Build3 tests (47) and authored tests (19) are included in the 66-test suite, not added again to the total.

The sole protected metadata change in the merged insurance `LIVE-BASELINE.json` is its exact roadmap SHA witness. Reviewer normalized only that entry and independently compared current metadata to user baseline `0523543fb1da0e8b8d05f05e93148ffc3b29cd70`: all other metadata and all 1,101 protected entries match. The current roadmap witness equals actual roadmap bytes; the permanent protected-roadmap regression rerun passes. This is authorized roadmap metadata maintenance, not regeneration of historical accounting sources, examples or economic results. The historical full-company artifact suite passed unchanged.

The previously accepted twelve findings remain resolved. Subsequent B3-IQA-13 reopened final local acceptance; its three permanent regressions and the full50 independent rerun now pass. Previous local acceptance must not be treated as approval of the forthcoming corrected tree. Exact immutable remote-head Actions and readiness-triggered checks must still be verified externally before publication acceptance; local results do not imply those remote gates passed. Specialist PRs were not modified by the reviewer, and no merge occurred in this review.

## B3-IQA-13 — framework-qualified execution dimensions

RESOLVED by independent targeted3 and whole50 reruns. Nondefault entity selection constructed native scope before applying optional item.framework qualification. Three independent permanent regressions reproduce: wrong-framework-only currencies/calendar are accepted; valid UK_GAAP/GBP plus irrelevant IFRS/USD falsely conflicts; a framework value UK_GAAP itself qualified only IFRS is accepted. Targeted old-source run:3 tests, exit1,2 failures/1error. Tests: `test_selection_rejects_wrong_framework_only_dimensions`, `test_selection_ignores_inapplicable_framework_dimension_conflict`, `test_selection_rejects_self_inapplicable_framework_item`.

Superseded/retracted/unknown/inferred and future-dated dimension variants reject correctly in standalone review. Fix must establish a self-applicable framework then qualify dimensions before constructing scope or detecting conflicts. Whole50 distinct independent methods pass, exit0,53.275 seconds. Final regression/source/proof/CI evidence must bind the new corrected immutable tree, not the superseded freeze.

Current corrected-source independent component/integration acceptance:50 distinct tests, zero failures/errors, exit0. New complete local release and remote publication gates are not yet accepted.

## Corrected context release review

B3-IQA-14 is RESOLVED. Reviewer reproduced the old committed resolver rejecting applicable UK policy alternatives as an execution-selection error. Permanent regression now verifies retained alternatives, omitted conflicted policy value, native UK_GAAP/GBP scope, durable BLOCKED Case, targeted context-policies request and exact restart parity. Whole51 independent suite passes (exit0,66.636 seconds), including all three framework-qualification regressions.

Corrected proof SHA256 `51cb8df87c36d6b64995594b54c1196a28e1ed6d8d4e3e922600224849832920` matches actual bytes and seed manifest (19/941, exit0/0, byte-identical). Reviewer verifies all six exact retained original source files, snapshots and immutable historical version hashes. Applicable per-entity framework-qualified inputs select UK_GAAP/GBP while an IFRS-only USD item is retained in history and excluded from selected items without false conflict. GROUP remains a native GROUP_CASE.

Fourteen findings are now resolved; zero unresolved substantive findings remain in corrected component/integration/proof review. The previously complete3,160-test manifest and prior remote-head checks are preserved historical evidence; final corrected-tree full13-suite regression, validators, source hashes and exact-head/readiness checks remain pending. They must not be inferred from the superseded accepted tree.
