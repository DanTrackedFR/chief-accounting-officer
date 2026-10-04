# Independent Agriculture knowledge QA — internal

Reviewer: independent-agriculture-knowledge-reviewer; separate from author context, on 2026-10-04. All 66 material claims individually challenged. No implementation approval. Initial register and author tests were not written by this reviewer.

Official inspection: AASB141 https://standards.aasb.gov.au/aasb-141-jun-2020 (operative2022–before2027); FRC Section34 https://www.frc.org.uk/documents/7668/FRS_102_September_2024_tmKYWO6.pdf and current-edition page; IFRS overview https://www.ifrs.org/issued-standards/list-of-standards/ias-41-agriculture/; historical FASB https://storage.fasb.org/ASU%202015-11.pdf. Independently tried operative2026 IAS41 PDF (retrieval error) and https://asc.fasb.org/ (no operative body). Corroboration does not establish operative IAS/ASC verification. No standard text/PDF stored.

Findings and remediation:

1. Multi-period bearer condition missing explicitly: corrected IFRS002/AASB002; single-period challenge added.
2. Exception disclosure incomplete: corrected IFRS019/AASB019, separately controlled exception bridge, depreciation/impairment reversals and conditional feasible FV range; corresponding challenge added.
3. Privacy leak: raw evidence limitations were allowlisted. Retrieval now emits substantive public_limitations only; fresh tests inspect all four framework retrieval paths for leaked provenance. Implementation privacy remains separate.
4. Evidence summary miscount: actual US5 primary/5 model. Corrected internal narrative. Overall35 SOURCE_VERIFIED,13 PRIMARY_CORROBORATED,18 MODEL_DERIVED_AUDIT_REQUIRED;35 direct-source approvals/31 training approvals. No evidence ratings elevated.
5. Selling-cost transport assurance: author narrowed proposition to independently verified selling-cost definition. Fair-value owner's input and operational nonduplication control remain separate from valuation authority; no extra paragraph verification invented.

UK cost routes require qualified owners and do not silently assign all biological assets to ordinary PPE. US current-source audit remains open; IFRS/AASB are not assumed interchangeable for entity/tier/period. Grants remain blocked. Postharvest inventory, cost exceptions and specialized sector cases stay bounded dependencies. Mandatory disclosures distinguished from encouragement.

Fresh numerical challenge: opening900 + invoice300 + Agriculture gain125 - harvest125 = closing1200; purchase FV270 causes initial loss30, birth80 and residual75 total125. Harvest prevalue100 to125 contributes25 within residual75, not another inventory entry. Quantity20+3+2-4-1=20. Milk/fruit yield does not remove surviving parents. A residual is not invented price/physical attribution.

Individual claim dispositions; each includes 2026 entity/period, framework distinction and source-locator assurance review:

| Claim | Counterexample | Result | Track |
|---|---|---|---|
| AGR-IFRS-001 | unmanaged ocean fishing / ordinary farm tractor | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-002 | single-period plant / milk cow as bearer plant | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-003 | fruit+lumber tree / annual maize automatically PPE | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-004 | orchard land or land lease included in FV biological balance | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-005 | unowned cattle physically present | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-006 | invoice price silently substituted for FVCTS | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-007 | last-year value reused for current year | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-008 | finance/tax deduction; duplicate transport deduction | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-009 | fixed forward price overrides qualified market FV | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-010 | birth gain credited OCI | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-011 | postharvest NRV computed inside Agriculture | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-012 | milking removes cow; slaughter retains live animal | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-013 | IAS initial-only restriction imported into UK | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-014 | FV asset reverted to cost at inconvenient date | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-015 | grant silently completed using IAS41 for every framework | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-016 | encouraged splits treated mandatory; omit output | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-017 | pledged restricted carrying omitted | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-018 | invent price/physical split from residual | PASS | TRAINING_DATA_CHECKED |
| AGR-IFRS-019 | omit depreciation / force unavailable FV range | PASS | TRAINING_DATA_CHECKED |
| AGR-AASB-001 | unmanaged ocean fishing / ordinary farm tractor | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-002 | single-period plant / milk cow as bearer plant | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-003 | fruit+lumber tree / annual maize automatically PPE | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-004 | orchard land or land lease included in FV biological balance | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-005 | unowned cattle physically present | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-006 | invoice price silently substituted for FVCTS | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-007 | last-year value reused for current year | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-008 | finance/tax deduction; duplicate transport deduction | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-009 | fixed forward price overrides qualified market FV | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-010 | birth gain credited OCI | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-011 | postharvest NRV computed inside Agriculture | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-012 | milking removes cow; slaughter retains live animal | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-013 | IAS initial-only restriction imported into UK | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-014 | FV asset reverted to cost at inconvenient date | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-015 | grant silently completed using IAS41 for every framework | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-016 | encouraged splits treated mandatory; omit output | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-017 | pledged restricted carrying omitted | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-018 | invent price/physical split from residual | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-019 | omit depreciation / force unavailable FV range | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-020 | Tier2 claimed IFRS compliant | PASS | DIRECT_SOURCE_CHECKED |
| AGR-AASB-021 | AASB for-profit grant rule on NFP | PASS | DIRECT_SOURCE_CHECKED |
| AGR-UK_GAAP-001 | unowned cattle physically present | PASS | DIRECT_SOURCE_CHECKED |
| AGR-UK_GAAP-002 | UK class elected FV switched to cost at will | PASS | DIRECT_SOURCE_CHECKED |
| AGR-UK_GAAP-003 | UK fruit recognized separately from parent | PASS | DIRECT_SOURCE_CHECKED |
| AGR-UK_GAAP-004 | UK FV gain sent OCI | PASS | DIRECT_SOURCE_CHECKED |
| AGR-UK_GAAP-005 | UK FV harvest carried historical cost | PASS | DIRECT_SOURCE_CHECKED |
| AGR-UK_GAAP-006 | agricultural engine invents orchard benchmark valuation | PASS | DIRECT_SOURCE_CHECKED |
| AGR-UK_GAAP-007 | IAS initial-only restriction imported into UK | PASS | DIRECT_SOURCE_CHECKED |
| AGR-UK_GAAP-008 | UK elected cost forced IAS FV | PASS | DIRECT_SOURCE_CHECKED |
| AGR-UK_GAAP-009 | UK cost harvest FV alternative forbidden | PASS | DIRECT_SOURCE_CHECKED |
| AGR-UK_GAAP-010 | unsupported borrowing capitalization completed | PASS | DIRECT_SOURCE_CHECKED |
| AGR-UK_GAAP-011 | omit current bridge; force comparative bridge | PASS | DIRECT_SOURCE_CHECKED |
| AGR-UK_GAAP-012 | UK FV harvested produce assumption omitted | PASS | DIRECT_SOURCE_CHECKED |
| AGR-UK_GAAP-013 | copy IFRS quantities into UK requirement | PASS | DIRECT_SOURCE_CHECKED |
| AGR-UK_GAAP-014 | grant silently completed using IAS41 for every framework | PASS | TRAINING_DATA_CHECKED |
| AGR-UK_GAAP-015 | UK tractor placed into Agriculture fair-value class | PASS | TRAINING_DATA_CHECKED |
| AGR-UK_GAAP-016 | 2025 edition assumptions or early2027 adopted | PASS | DIRECT_SOURCE_CHECKED |
| AGR-US_GAAP-001 | unmanaged ocean fishing / ordinary farm tractor | PASS | TRAINING_DATA_CHECKED |
| AGR-US_GAAP-002 | US growth gain replacing inventory cost | PASS | TRAINING_DATA_CHECKED |
| AGR-US_GAAP-003 | US developing sale livestock as IAS41 FV | PASS | TRAINING_DATA_CHECKED |
| AGR-US_GAAP-004 | US NRV alternative without immediate delivery | PASS | TRAINING_DATA_CHECKED |
| AGR-US_GAAP-005 | postharvest NRV computed inside Agriculture | PASS | TRAINING_DATA_CHECKED |
| AGR-US_GAAP-006 | US dairy animals default FVCTS | PASS | TRAINING_DATA_CHECKED |
| AGR-US_GAAP-007 | US vineyard default IAS41 classification | PASS | TRAINING_DATA_CHECKED |
| AGR-US_GAAP-008 | unowned cattle physically present | PASS | TRAINING_DATA_CHECKED |
| AGR-US_GAAP-009 | IAS41 disclosure mandates automatically US | PASS | TRAINING_DATA_CHECKED |
| AGR-US_GAAP-010 | grant silently completed using IAS41 for every framework | PASS | TRAINING_DATA_CHECKED |

Regression: 66 independently named claim challenges plus four fresh governance/privacy/arithmetic tests; author tests counted separately. Approval is this actual second-context challenge process, not a PASS label shortcut. Knowledge approval does not certify production implementation or public renderer privacy.

Executed: `python -m unittest discover -s knowledge/agriculture -p "test*.py" -v` —82 PASS (12 authored,70 independent); `python knowledge/agriculture/validate_supplement.py` —66 claims APPROVED, zero errors.

## AGR-IQA07 harvest valuation follow-up — independently challenged

Root and independent implementation reviewer identified operational prose that conflated preharvest biological carrying and harvested-produce measurement. Re-inspected AASB141 paragraphs13 and28 and FRS10234.5/34.4 on2026-10-04. Existing atomic harvest claims correctly require produce FVCTS and remain unchanged; all66 approvals/evidence statuses/counts preserved. Corrected method to require separate qualified produce valuation on actual produce quantity/unit, derecognize controlled biological carrying once and recognize the conversion difference in P&L. Distinct preharvest and produce populations may differ; neither equality nor conversion yield is inferred. Missing produce evidence blocks. Synthetic journal: Dr inventory65, Dr Agriculture loss5, Cr biological assets70. The unequal example is supported IFRS/AASB; UK unequal conversion execution requires separately governed support and remains blocked unless that support is supplied. Section34.5 alone must not be presented as directly verifying a terminal conversion P&L rule. Fresh independent executable knowledge regression test includes this journal, non-equality, units/evidence method constraints and biological33,000 versus conversion2,000 gain decomposition. This is knowledge remediation only, not production implementation sign-off.

Final follow-up knowledge regression:83 PASS (12 authored,71 independent); supplemental validator66 APPROVED, zero errors; diff check PASS.
