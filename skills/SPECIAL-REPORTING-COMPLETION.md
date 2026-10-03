# Fixed Phase 3 batch 36 / 37 / 40 / 41 / 42

Baseline: current live main `c813f16fb6abcaf9a2169e1d9be0f34f5a8d0b22`, merged PR19, 30 production skills. One branch `phase-3/disposals-property-hyperinflation-apm-sec`, PR20. No merge authorized.

## Individually bounded outcomes

| Skill | Final outcome | Executable scope / knowledge boundary |
|---|---|---|
|36 Assets Held for Sale & Discontinued Operations|1.0.0 / production, supported-scope QA PASS|IFRS/AASB dated classification and discontinued-presentation workpaper. No disposal-group measurement, allocation/reversal, disposal/OCI accounting or journals. US/UK block.|
|37 Investment Property|NONPRODUCTION, all four routes fail closed|PPE knowledge is only a classification boundary. No substantive governed definition, mixed-use/model, transfers or framework-specific engine. No calculations/journals; certification cannot bypass the blocker.|
|40 Hyperinflation Accounting|1.0.0 / production, supported-scope QA PASS|IFRS/AASB economic-assessment and isolated index workpaper. No complete restatement, net monetary gain/loss, tax, FX/consolidation or journals. US/UK block.|
|41 Non-GAAP / Alternative Performance Measures|1.0.0 / production, supported-scope QA PASS|Actual source-backed journal/statement reconciliation, cross-period dictionary/recurrence and qualified jurisdictional publication controls. No invented measures/adjustments, underlying accounting or regulatory clearance.|
|42 SEC / Public Company Reporting & Filing Accounting|1.0.0 / production, supported-scope QA PASS|US registrant source-to-filing, actual domestic/FPI/form/calendar, tag accounting and release controls. No autonomous law/deadlines, EDGAR submission, compliance/officer/audit or XBRL-validity certification.|

The immutable SPECIAL-REPORTING-KNOWLEDGE-MAP.json contains exact 9-topic/19-capability/42-claim mappings, actual proposition/framework/evidence/reference/audit/approval/effective-period/entity limitations and source hashes. TOPIC16-005 has approved operational documents and no normative claims. TOPIC16-006/007 were inspected and excluded. No new standards knowledge or supplemental namespace was created.

## QA and regeneration

SPECIAL-REPORTING-INDEPENDENT-QA.md records genuinely separate review, 13 substantive independently discovered failures, implementation remediation and successful independent rerun. The independent regression includes 16 test methods, 100 broader assertions and an actual completed Financial Statements import/contradiction pair. Additional integration tests consume a completed APM owner in SEC support, reject duplicates/alteration/journal reposting and exercise FPI US GAAP and actual interim spans.

`python skills/tests/generate_special_reporting_examples.py` generates 20 framework/case examples: 10 supported complete+unsigned partial pairs and 10 unsupported blocked outputs. All example data and approvals are explicitly synthetic. No real economy/index/issuer/deadline conclusion is asserted. No raw source/reviewer/hash internals are in public outputs. The existing normal presentation generator refreshes only four Subsequent Events adjusting-case embedded owner certificates, required by the shared global implementation fingerprint; their accounting and expected public output remain unchanged.

## Regression and promotion

Full skill suite: 449 tests; lease:17; repository:53; supplemental tax:10. All 529 tests PASS after promotion. Canonical/evidence and supplemental validators PASS; git diff --check PASS. Candidate exact-head CI PASS:46cd18909ae8a0695e0577a263c0c79f0b444679, run37148978590. Only four individually passed bounded packages were promoted to1.0.0/production after that gate. Production metadata changes regenerate every fingerprint-sensitive example and four older embedded adjusting cases. Full regression PASS after promotion; final exact-head CI remains a required integration gate. CI results and final SHA are recorded in PR20 because embedding the current commit's own SHA in committed files is recursive.

Projected production count if PR20 is merged:34 (previous30 plus36/40/41/42). Investment Property is excluded. PR20 is not merged in this task.

## Immutable project boundaries

The entire canonical knowledge, supplemental-tax knowledge, architecture and jurisdictions remain byte-identical to baseline. 157/157 APPROVED topics,347 capability mappings,1598 claims and64 tax claims are preserved. Actual evidence_status/reference_confidence/audit_required/approval-track/limitations remain intact; APPROVED never means SOURCE_VERIFIED. Production owners retain their contracts and journal ownership. Government Grants and Borrowing Costs are untouched NONPRODUCTION/fail-closed. Reserved #24/#29/#30/#38/#39 artifacts and queue remain untouched.
