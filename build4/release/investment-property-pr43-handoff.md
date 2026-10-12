# Investment Property #37 — PR #43 release handoff

Release readiness is conditional on the accepted full-regression receipt and exact published-head GitHub Actions. This document does not authorize merge or ERP posting.

## Architecture and integration

The existing CAO runtime, orchestration, durable Case store, Company Accounting Memory, local/hosted contracts and MVP Build 4 remain the execution architecture. Investment Property is dispatched through `production.assess_case("investment-property", case)`. The original implementation brief is preserved unchanged (SHA256 `773c1c175c336ad6f9437dc69676a29793e14967b36dd65dcc3ecfb0dd7c2748`).

Main baseline `e75375b84813b9d584db12aa692b2f4d16baf052` contains owner-authorized Borrowing Costs PR #42 and Government Grants PR #27. Both were integrated non-destructively into this branch. The exact dispatcher witness and strict additive fingerprint bridge preserve all existing owner-scoped fingerprints while binding new Investment Property cases to their actual implementation. Independent reconciliation checks compare eight Borrowing/Grants whole-result hashes and fingerprints with real main Git objects, preserve 49 other production contracts, and challenge shared code tampering. See `skills/investment-property/ARCHITECTURE-RECONSTRUCTION.md`, `INDEPENDENT-MAIN-RECONCILIATION.md` and the external `ip-roadmap-final` review.

The canonical baseline remains 157 approved topics, 347 capability mappings and 1,598 claims. Main has 49 bounded production skills; this candidate adds the fiftieth. No canonical topic, capability mapping, prior specialist accounting method or historical artifact is regenerated.

## Accounting authority and bounded support

The separately governed 96-claim supplement is independently AI-reviewed, not human-certified. Its approved claim hashes and source assurance remain explicit: **MODEL_DERIVED_AUDIT_REQUIRED / TRAINING_DATA_CHECKED**, with no claim of comprehensive directly verified licensed-standard authority. Public primary-source checks and limitations are recorded in `knowledge/investment-property/independent-source-challenge.md` and the knowledge QA report. A valuation certificate alone cannot authorize a missing governed method.

Execution is deliberately limited to calendar 2026, one owned property, one entity, one currency and one reporting-date event, with actual captured source records and current independent certification. IFRS and Australian Tier-1 for-profit AASB support supplied fair value or cost, defined initial/holding/disposal routes and bounded cost transfers/FV transfers out. UK FRS 102 September 2024 ordinary investment property uses fair value; the specific group-lessor cost option remains PPE-presented. US ordinary held-and-used real estate remains historical-cost PPE; universal investment-property fair value and **all US transfer methods are blocked**. Mixed-use separable portions are explicitly identified; insignificant inseparable owner use is not imported into UK GAAP.

Construction, right-of-use assets, finance lessor accounting, inventory/development property, held-for-sale, combinations, sale-and-leaseback, midyear events, into-fair-value transfers, prior impairments/estimate changes, gifts/nonexchange and zero-price/fee-only acquisitions, other periods and industry/entity-specific US exceptions remain blocked. See the framework/method and source-assurance matrices for exact gates.

Supplied independent valuation evidence is checked, never generated. Cost depreciation is independently recalculated from actual straight-line inputs but its recognition remains with Fixed Assets; impairment recognition remains with Impairment. All offsets, original source identities, property-class rollforwards, presentation and disclosure amounts reconcile. Fair-value movements are journaled once. Transfers do not usurp PPE revaluation. Native duplicate owner scopes and ambiguous same-scope sources block before execution. There is no global external cross-Case posting ledger, no ERP posting and no authenticated-human approval claim.

## Independent findings and dispositions

Knowledge review corrected UK effective-period cost exceptions, group-lessor presentation/disclosures, actual-use transfer requirements and paragraph references; source assurance was not upgraded. Frozen approval hashes and executable independent knowledge checks record the disposition.

Runtime R1: midyear acquisition could omit later annual owner accounting. Corrected by reporting-date-only event and acquisition chronology gates; independently reproduced and rerun.

Author-discovered transfer-in rollforward error: PPE source opening was counted twice in the Investment Property class. Corrected to zero class opening plus transferred carrying basis; independently rerun over 27 supported routes.

Runtime R2: a coherently zero-valued US transfer-out bypassed an incidental GL guard. Corrected with an explicit US transfer-method block, not a nonzero numerical condition. Three permanent scope tests and eight extra US variants passed independently. At that stage, independent review ran 39 tests and reproduced all 42 examples / 211 files under seeds 19 and 941 with unchanged reviewed source hashes. See `ip-independent-final/post-r2-review.json`, `r2-disposition.json` and their actual logs. Subsequent R3/R4/R5 receipts supersede this earlier source freeze.

The first full-regression attempt is diagnostic, not acceptance. It began before the additive roadmap correction and later source changes; all failed/unfinished receipts remain retained. The roadmap correction preserves the complete main text as an immutable prefix and appends a dated status update; original protection assertions were not weakened.

The second full specialist gate exposed R3 in the additive fingerprint bridge: the original byte-mutation test changed the implementation read while a separate text read still matched the witness. The bridge now validates authoritative dispatcher/witness bytes and refuses normalization if the recorded dispatcher digest disagrees with those validated bytes. The exact helper pin was updated; original shared-boundary assertions are unchanged. Four additional independent probes reproduce byte-only dispatcher/witness mutation, captured-digest mismatch and inconsistent non-authoritative text views. All earlier full attempts remain diagnostic; final acceptance must follow this correction and an independent rerun.

Runtime R4: cost transfer-in omitted current pre-transfer PPE charges. Current owner measurements are now mandatory and independently reperformed: prior 600,000 less 20,000 depreciation gives transfer 580,000; with independently owned 10,000 impairment it gives 570,000. Only the net transfer is journaled. IP class opening and IP class depreciation/impairment are zero; pre-transfer owner charges are separate workpaper fields, not duplicate deductions. Missing current owners, wrong charges and contradictory original captures block. The reviewer corrected its own earlier 600,000 oracle explicitly; the initial failing evidence is retained.

Runtime R5: cutoff initial/cost transfer-in could complete without a qualified fair-value note and the cost-model output omitted the note amount. All closing IFRS/AASB cost-model properties now require qualified reporting-date valuation evidence and output `fair_value_disclosure` (650,000 in these synthetic cases), while `fair_value_movement` remains zero. Stale, wrong-framework, unreliable or missing evidence blocks. There is no cost-to-FV recognition election or duplicate valuation journal.

The post-R4/R5 independent runtime review passed 46 tests and read-only reproduction of 42 scenarios / 211 artifacts under both seeds. A fixture-only chronology correction documents first technical/legal readiness for intended use on 2026-01-01, explaining zero 2025 depreciation and full 2026 depreciation; readiness is not first tenancy or actual occupancy, and no prior construction/development method is asserted. `ip-independent-final/post-fixture-final-review.json` retains that stage-specific 46-test/two-seed receipt. A distinct knowledge review independently checked ten scope tests, twelve knowledge tests and six actual runtime cases against existing governed claims and public operative AASB paragraphs. `ip-knowledge-final-review.json` confirms correct mathematics/notes and unchanged knowledge hashes/assurance. The qualified independent valuation requirement is a conservative supported runtime boundary, not a claim that every jurisdiction statutorily mandates an independent valuer.

Runtime R6: an expressly gifted zero-price property could enter the initial cash-purchase route using paid legal fees alone. Initial recognition now requires explicit nongift cash-purchase qualification and strictly positive independently evidenced property-price consideration, separately identified from fees. Unsupported gifts, nonexchange acquisitions and fee-only/zero-price acquisitions are blocked for separately governed original-owner accounting; no gift valuation or new accounting method is inferred. Independent read-only before evidence and permanent adversarial tests are retained in `ip-independent-final/gift-boundary-readonly.*` and `r6-disposition.json`. Separate knowledge review `ip-knowledge-r6-final-review.json` passed thirteen scope tests and four positive initial framework cases with unchanged claims and assurance. Authored post-correction tests passed 35 tests; their receipt is separate from independent QA.

Final current-source independent implementation QA passed 49 tests under seed 19 (41.725 seconds) and seed 941 (35.143 seconds), plus exact reproduction of all 42 scenarios / 211 artifacts under each seed, with unchanged reviewed byte hashes. `ip-independent-final/post-r6-final-review.json` and its four stdout logs supersede earlier stage-specific gates. Separate final reconciliation ran 25 tests (15 independent main reconciliations and 10 unchanged original implementation-scope tests), exit zero, no skips, in 32.119 seconds. `ip-r6-final-reconciliation/review.json` records exact equality of eight merged Borrowing/Grants fingerprints and whole results, 49 other specialist contracts, historical bytes and live main `e75375b8`. No owner conflict intervention is required.

Full attempts 001–004 remain explicitly diagnostic, with cancellation exit 130 and all completed receipts preserved. Attempt 004 had sixteen complete suites and sixty-three orchestration modules pass before the remaining durable-history proof was interrupted for R6; its unfinished proof and final validators are not reported as passed. Frozen attempt 005 is the required fresh full acceptance run.

## Reproduction and release receipts

Run from repository root:

```sh
PYTHONPATH=skills:skills/tests PYTHONHASHSEED=19 python skills/tests/generate_investment_property_examples.py --verify
PYTHONPATH=skills:skills/tests PYTHONHASHSEED=941 python skills/tests/generate_investment_property_examples.py --verify
python knowledge/investment-property/validate_supplement.py
python -m unittest discover -s knowledge/investment-property -p 'test_*.py'
CAO_IP_ATTEMPT=investment-property-pr43-attempt-NEW python skills/investment-property/run_release.py
python -m build4.verify_release
```

The supervisor refuses to overwrite prior attempts. Acceptance requires exact discovered test IDs, no errors/failures/skips, unchanged Python and execution inputs, all validator/log checksums and historical integrity. Only new synthetic IP examples may be regenerated; historical examples and prior accepted logs must never be rewritten.

`ip-proofs/manifest.json` records independent-seed local, hosted, intelligence, Build 4 and Company Memory proof commands and exact comparisons with main-approved layered historical references. `investment-property-historical-preservation.json` checks 5,926 original main files. These proofs complement, and do not replace, full repository regression.

## Commit preservation and publication

Local checkpoints and both main integrations are preserved in ordinary local Git history. Because direct Git push has no configured authentication, the configured GitHub writer is used to upload exact Git blobs and a SHA-verified identical tree, fast-forwarding only the existing PR branch with a checked expected remote head. There is no force push and no new PR. `ip-local-checkpoints.bundle` preserves the earlier exact local checkpoint chain. Verified final archive `ip-final-local-checkpoints.bundle` preserves exact local implementation/QA/full-acceptance head `30bbc9e54e2ed76f5fe71b26efd08d434c4925af`, SHA256 `2a093a63a0cd491495ddfa4ae0819fe566c70b8562da346e23f441126cb9ef84`; the subsequent archive-containing commit cannot archive itself. Bundle prerequisites are the original PR head and integrated main commits; use `git bundle verify` before recovery. API publication metadata produces a different commit SHA from local checkpoints; tree equivalence and preserved bundles make that distinction explicit. See the release completion report and recovery instructions.

## Final release status

Frozen attempt 005 passed all 3,632 distinct tests across seventeen suites, with no failures, errors or skips; all ten validators and the whitespace gate exited zero. The orchestration suite passed 1,361 tests in 3,566.185 seconds; specialist tests passed 1,499 tests in 732.908 seconds. All 415 Python hashes and 2,673 execution-input hashes remained unchanged. The accepted manifest SHA256 is `61fa3e76e195f69876cf78466454e89c23623616803182551cda21f1cbdf07d8`; the accepted pointer and verifier enforce every receipt/log hash, exact discovered test IDs and 5,926 protected historical files.

Exact published-head and unchanged-head readiness-triggered GitHub Actions results are recorded in the PR #43 release completion comment, avoiding a self-referential commit hash in this commit's report. PR #43 remains Draft until every external gate passes; marking Ready for Review does not authorize merge. Merge remains exclusively owner-authorized.

Final receipt sealing detected two truncated new-release stdout files. Both damaged prefixes and both failed verifier logs are preserved. Independent forensic review recovered bytes matching the **original preexisting recorded SHA256 values exactly**, without changing expected hashes, receipts, test outcomes, source, Case evidence or any historical main artifacts. Separate fresh reruns passed five native-opening tests and thirty-five insurance knowledge tests; those transcripts are not substituted for the original run. The causal actor is not established. `ip-receipt-integrity-review/final-recovery-acceptance.json` records the actual AI roles, authenticated restorations, all ninety-two matching stdout hashes and unchanged frozen inputs. Independent and primary unchanged acceptance verifiers then exited zero, verifying 3,632 tests and 5,926 protected files. Failed gates are not retroactively labelled passed.
