# Borrowing Costs independent implementation QA

Reviewer: `/root/implementation_review`, an independent model agent; no human identity or actual human certification is asserted. All case identities, source approvals and reviewer signatures in fixtures are explicitly synthetic. This review does not promote knowledge claims or source assurance.

Scope: 2026 ordinary domestic single tangible construction project; IFRS, AASB Tier 1 for-profit, ordinary US GAAP and full commercial FRS 102. Knowledge approval, canonical baseline and exact-head release remain separately controlled.

## Observed original defect and remediation

IQA01: original local workflow accepted a +37 contradiction in construction GL and separately in finance GL while capitalization remained 11032.88. Reproducer: use the author's original mixed IFRS fixture, increment opening/closing/statement of either GL row by 37, call workflow.assess with the supplemental namespace sentinel. Both calls returned an allocation. This was an isolated algorithm probe bypassing the pending knowledge gate, not a production acceptance claim.

Generic remediation: bind opening/closing construction and finance GL to independently derived source balances, then verify journal movement. Require a separately captured original source population, retain it when recomputing calculations or renewing synthetic certification, and reject any contradictory or missing finance/expenditure/chronology source. Permanent tests `test_iqa01_asset_gl_shift`, `test_iqa01_finance_gl_shift`, expenditure and financing recompute contradictions reject the observed defects after author fixes.

IQA02: review identified the original daily incurred-interest ceiling as narrower than the period-level ceiling. A permanent fresh US general-debt example uses 1,000,000 opening cash expenditure and a 995,000 July refund; the correct annual weighted avoidable amount is 39872.88, within actual annual interest. The remediated annual ceiling passes. No false claim that this new test was executed against the deleted original is made.

Method challenges also led the author to compute a period-weighted general borrowing rate, include prior-day capitalized cost in UK carrying expenditure, and ringfence nonzero prior capitalized IFRS/AASB/US cost outside the selected actual-cash route. Exact source snapshots supplement approvals and inventories. Source capture remains a supplied evidence assertion, not cryptographic proof of external originals.

## Independently checked accounting and evidence

The independent numerical expectations use fresh 137-percent money populations and closed-form formulas: mixed IFRS/AASB/US 15115.04; general IFRS/AASB/US 16485.04; specific IFRS/AASB/UK 20550 versus US 12363.78. UK carrying-cost general/mixed expectations use a closed geometric series rather than the production daily loop: mixed15620.23/general17046.36. Positive UK expense returns no journal and retains58910 incurred expense. Positive extended suspension/resumption, necessary delays and readiness cessation establish temporal behavior. Allocation journals debit construction and credit previously recognized expense; no second lender liability is created.

Primary sources independently inspected on2026-10-09: AASB current portal https://standards.aasb.gov.au/aasb-123-mar-2020 (Tier1 comparison,14,17–23 and18 carrying approximation); FRC September2024 https://www.frc.org.uk/documents/7668/FRS_102_September_2024_tmKYWO6.pdf p266 Section25. The AASB portal identifies operative periods beginning on/after2021-07-01. FRC25.2 permits class-consistent policy/expense,25.2B deducts temporary specific investment income,25.2C uses average carrying amount including prior capitalized costs and weighted general rates with period ceiling,25.2D identifies commencement/suspension/cessation. This implementation review does not imply independently inspected current ASC text or IFRS licensed text; their exact source assurance remains with separate knowledge QA.

## Execution ledger

Initial full run:37 methods were not yet present;31 methods produced3 expectation failures and4 gate errors. Two expectation failures were deliberate UK methodology changes requiring an independently derived geometric oracle; the US specific expectation had a reviewer arithmetic error corrected from12375.04 to12363.78. Four production errors reflected the pending supplemental knowledge map. These are not omitted or reported as passing.

Latest local run:33 local methods passed in0.636s after source/GL and method remediation. Four production/certification/public-route methods remain pending the validly approved supplemental map. The permanent suite contains37 test methods at this checkpoint. Command: `PYTHONPATH=skills:skills/tests python -m unittest skills.tests.test_independent_borrowing_costs -q`.

IQA03: the expanded41-method run actually failed1 test after map refreeze: missing original-source input emitted raw `original_source_snapshot` in public guidance, limitations and uncertainties. Generic remediation: narrowly curate the required input name to an accounting evidence description in all public fields, retaining the substantive requirement. Root fixed the curation; the permanent seven-route test now passes with both named-source and training-data notes excluded.

The final scope challenge found purpose `sale` could silently admit inventory owner accounting. Author restricted to own-use construction. The permanent sale test refreshes the synthetic original capture so rejection exercises the substantive scope gate rather than only stale-source detection. Another permanent test likewise recaptures synthetic original evidence for11 adverse route combinations (fee, FX, tax-exempt, complex, currency, asset type, abandonment, shared components, expense election, Tier2 and prior capitalized cost), confirming their explicit substantive gates.

Final independent command above:44 methods passed in1.257s, including actual production fresh four-framework release, source contradiction after synthetic recertification, stale knowledge/document selection, exact-case and changed-implementation certification with journals withheld, both provenance notes and all seven public routes. Independent44-method suite is separate from the author's suite. Source/GL original reproducers now reject. Imported debt results without an exact economic loan crosswalk are explicitly blocked and tested; independently supplied original financing evidence remains the supported route. No unresolved substantive finding within the documented bounded scope at this reviewed working-tree checkpoint.

Status: ACCEPTED for the bounded implementation at this checkpoint; exact-head release and any subsequent substantive change require rerun. Acceptance is independent model QA, not a human signoff and not direct-source assurance for model-derived knowledge. No commit or push performed by this reviewer.


## Final promoted implementation acceptance — 2026-10-09

Version1.0.0 production was independently rerun: own44 methods PASS in1.224s. Root-authored six narrow integration methods were independently inspected and executed, PASS in0.518s. The latter exercise actual scope/period/CaseRegistry binding, production owner selection, complete native CAO result, SQLite save/load with native snapshot/result equality, and public output on all seven routes. They are not counted as independently authored44 methods. Total reviewer execution50 methods. No unresolved substantive finding in the final bounded own-use/direct-source scope; imported-debt results remain blocked without economic crosswalk.

Final commands:

```sh
PYTHONPATH=skills:skills/tests python -m unittest skills.tests.test_independent_borrowing_costs -q
PYTHONPATH=.:skills:skills/tests python -m unittest orchestration.tests.test_borrowing_costs_integration -q
```

Accepted exact implementation/support SHA-256 values (subsequent change requires review/rerun):

| Path | SHA-256 |
|---|---|
| skills/borrowing-costs/workflow.py | 4baf791e57264c69d400c68758469f751000f4302fd1d678ae7cc04e85774818 |
| skills/borrowing-costs/SKILL.md | e697df638b0ee19116b50e82aaa1465d7d5dfe2110c97395382e5612c4a8e074 |
| skills/borrowing-costs/methods.md | cae1c5b539d04ea4980107e0e8d80de67fb48de07c42e29017bdc659a632204e |
| skills/borrowing-costs/SUPPLEMENTAL-KNOWLEDGE-MAP.json | 80cb9f31461e221f76d70d9580bcf3a9834939f58330ba37e3cd4394a0d3f67b |
| skills/borrowing_knowledge.py | ecaa5694ff96601bcb4bcb994dc0f09fcf4251c62fe3b5eff8a253eb9f8a49ca |
| skills/production.py | 4570a618c7d998d9e9ed05d98d04317a824e70dc38922bd25634f4c299e3bfed |
| skills/financing_accounting.py | 72717ca1da5c60e9b8cf23a522e64cfee81819006e3c616155b56a4abca3979b |
| skills/core_accounting.py | c668a8c5b334c0f8cb98da27e14fe764972c28d7f8b0a875600e1e51fd6589ae |
| interfaces/public_output.py | 240aead226b7913712c13dc2af8b0f22dc8d5a6c17e8f7fb26f5f343539ad35b |
| knowledge/borrowing-costs/retrieval.py | 99c142387743285c0f8bf2889b053c454adcba005ef1dfa3238c42d0233bb512 |
| knowledge/borrowing-costs/validate_supplement.py | 6cb46a78d46456bde7e39559411fb8a10b8a6769ecae6ebbc96d85e157ced1dd |
| knowledge/borrowing-costs/standards-claims.json | 2dd59bb6f95aa726165e063c25b9f112d7645b7d39eecbbb65ffd6c1ac07392d |
| orchestration/registry.py | 9b0f355c5c8313a20b56ab0711c2af2f4518a28e4e555555fec96bd9b7c45d65 |
| orchestration/planning.py | 0424f84ed12e34208b40410949a383c97daaa7acdc2752d03a2f494169adb264 |
| orchestration/tests/test_borrowing_costs_integration.py | 97c871aaa79d9e987302ee5ec13ea51a8b336c41269de04a1e691f0644e9fe04 |
| skills/tests/test_independent_borrowing_costs.py | 658df5b0baab39b1059f04887801d25591880c1dee779625750352e48fa1eeec |
