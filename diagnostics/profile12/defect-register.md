# Profile 1.2 — authoritative diagnostic defect register

Baseline `36acb611142bc8bedd214622f1ecac539c290056`. All 13 findings were independently reproduced. All 13 are now VERIFIED_FIXED_FOCUSED on published source `33704a4cfecf8d54f4333fe8b836033d8c5ee826`; full release acceptance remains pending. The original reproduction descriptions below remain historical evidence, not current behavior.

The original engineering review was retrieved from [the standalone report](https://chatgpt.com/library?file_id=libfile_959431e279908191b9b85d14e4490708&account_id=personal). E1–E6 map to ENG-01–ENG-06; G1/G2 map to GOV-01/GOV-02. Original accounting reviewer name/full requests were unavailable; owner-supplied observations were independently reconstructed. Existing implementation QA reports predate these adversarial findings and are preserved unchanged.

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| ENG-01 | High | False-string disposal authorization | Verified fixed; focused QA pass |
| ENG-02 | High | Rejected-row journal leakage | Verified fixed; focused QA pass |
| ENG-03 | High | Malformed source Case identifier | Verified fixed; focused QA pass |
| ENG-04 | High | Diagnostic response amplification | Verified fixed; focused QA pass |
| ENG-05 | High | Contradictory AP payment evidence | Verified fixed; focused QA pass |
| GOV-01 | Medium | Release receipt sidecar tampering | Verified fixed; focused QA pass |
| GOV-02 | Medium | Optimized Python governance bypass | Verified fixed; focused QA pass |
| ENG-06 | Medium | Malformed operation returns HTTP 503 | Verified fixed; focused QA pass |
| ACC-01 | High | Opening accumulation validated after additions | Verified fixed; focused QA pass |
| ACC-02 | High | Refundable deposit inherits expense default | Verified fixed; focused QA pass |
| ACC-03 | High | Credit disposal debited to cash | Verified fixed; focused QA pass |
| ACC-04 | Medium | Negated dispute interpreted as affirmative | Verified fixed; focused QA pass |
| ACC-05 | High | Malformed invoice blocks independently supported accrual | Verified fixed; focused QA pass |

## Evidence method

Real authenticated loopback HTTP service with both Profile 1.2 switches enabled; actual production owner execution, public job responses and reopened durable native results. Trace records contain exact request bodies and parsed HTTP response/status; bearer token is synthetic and supplied by the reusable fixture helper. Financial workpapers remain proposals, never posting authority. Runtime records test idempotent retrieval and service restart equality except ENG-03/ENG-06 preacceptance probes. Decimal values in captured JSON are strings. Gzip evidence is lossless (`gzip -dc file.json.gz`).

Runtime baseline: 19 test methods, 7 passing controls and 12 failing defect methods; 15 failure records because malformed-operation variants are subtests. Governance: 4 methods, 2 passing controls and 2 failing defect methods; 5 failure records across four sidecars and optimization. No errors or skips in final runs. Subtests and repeated executions are not additional distinct findings or tests.

## Individual findings

### ENG-01 — False-string disposal authorization

**Severity:** High

**Accounting/control impact:** incorrect journal construction; insufficient evidence

**Original reviewer:** Independent final engineering/governance review (E/G identifiers)

**Reported observation:** String false enabled disposal with cash 12000 and gain 2100.

**Reproduction status:** independently_reproduced

**Minimal input:** fixtures/ENG-01.json

**Actual output and persistence:** SUPPORTED; cost derecognized; persisted Dr cash 12000, Dr accumulation 1100, Cr PPE 11000, Cr gain 2100. Same result after retry/restart.

**Expected behavior:** Require a literal boolean at disposal input boundaries. A string is invalid, never disposal authorization. Reject or exclude affected row with specific requirement and no disposal journal. Literal false/omission retain asset; legitimate true disposal remains supported.

**Production entry point:** Authenticated loopback HTTP /v1/operations → submit → /v1/jobs → worker → production source execution → persisted owner workpaper

**Confirmed mechanism / code reference:** skills/source_execution.py:fixed_assets.calculate lines 282/313 and cost_row line 246 use truthiness of disposal.enabled; no disposal boolean validator precedes them. Existing owner workflow uses flag().

**Executable regression:** regressions.py:Regressions.test_ENG_01

**Actual evidence:** evidence/ENG-01.json.gz

**Dependencies and overlap:** ACC-03 shares disposal branch but concerns consideration account, not flag type.; ENG-02 shares disposal ordering, but rejected-row atomicity is separate.

**Remediation boundary:** Validate the whole disposal object at adapter and direct production entry; maintain row/dependency isolation.

**Evidence limits:** Synthetic IFRS 2026 fixture; no customer upload or deployed TrackedFR endpoint tested.

### ENG-02 — Rejected-row journal leakage

**Severity:** High

**Accounting/control impact:** incorrect journal construction; incorrect persistence

**Original reviewer:** Independent final engineering/governance review (E/G identifiers)

**Reported observation:** Invalid disposal proceeds exclude row but leave depreciation 545.48.

**Reproduction status:** independently_reproduced

**Minimal input:** fixtures/ENG-02.json

**Actual output and persistence:** UNRESOLVED with empty public calculations and assets:1 excluded, yet durable Dr depreciation/Cr accumulation 545.48. Mixed fixture retains public depreciation 1100 but persisted depreciation totals 1645.48. Retry/restart preserve leakage.

**Expected behavior:** An excluded row contributes no journals. Mixed valid row must retain exactly 1100 depreciation and its balanced proposal. Validate dependency groups before publishing financial side effects.

**Production entry point:** Authenticated loopback HTTP /v1/operations → submit → /v1/jobs → worker → production source execution → persisted owner workpaper

**Confirmed mechanism / code reference:** skills/source_execution.py:fixed_assets.calculate line 312 appends to outer entries before number(disposal.proceeds) at line 314; source_screening.py:Screening.row catches failure and returns None without rolling back entries.

**Executable regression:** regressions.py:Regressions.test_ENG_02

**Actual evidence:** evidence/ENG-02.json.gz

**Dependencies and overlap:** Same mechanism as accountant rejected-row depreciation observation; retained as ENG-02 with separate mixed reproduction ENG-02-mixed.; ACC-01 also involves linked cost state, but temporal balance validation is distinct.

**Remediation boundary:** Stage row/dependency results and journal entries privately; commit together only after all validation; preserve retry/checkpoint consistency.

**Evidence limits:** Synthetic IFRS 2026 fixture; no customer upload or deployed TrackedFR endpoint tested.

### ENG-03 — Malformed source Case identifier

**Severity:** High

**Accounting/control impact:** incorrect persistence; audit lineage integrity

**Original reviewer:** Independent final engineering/governance review (E/G identifiers)

**Reported observation:** Object accepted as source Case ID and persisted with supported depreciation.

**Reproduction status:** independently_reproduced

**Minimal input:** fixtures/ENG-03.json

**Actual output and persistence:** Submit HTTP 200; job SUCCEEDED; SUPPORTED depreciation 1100; native source_lineage.case is {"not":"a case identifier"}. Outer durable Case ID remains a separate valid ID.

**Expected behavior:** Nonblank bounded string required before accepting inline or staged source evidence and at owner entry. Return field-specific client requirements; never persist an object as source Case lineage.

**Production entry point:** Authenticated loopback HTTP /v1/operations → submit → /v1/jobs → worker → production source execution → persisted owner workpaper

**Confirmed mechanism / code reference:** local_cao/adapter.py:ExecutionInterface._evidence lines 381–385 uses truthiness; source_execution.py:requirements checks presence only; execute line 480 copies case_id verbatim. interfaces/source-case.schema.json string contract is not enforced here.

**Executable regression:** regressions.py:Regressions.test_ENG_03

**Actual evidence:** evidence/ENG-03.json.gz

**Dependencies and overlap:** ENG-04 shares missing identifier constraints but concerns source.id size and output multiplication.

**Remediation boundary:** Central validated source-ID contract across inline, staged, preacceptance and direct owner paths; do not require equality to outer durable Case ID.

**Evidence limits:** Synthetic IFRS 2026 fixture; no customer upload or deployed TrackedFR endpoint tested.

### ENG-04 — Diagnostic response amplification

**Severity:** High

**Accounting/control impact:** resource exhaustion risk; public source identity exposure

**Original reviewer:** Independent final engineering/governance review (E/G identifiers)

**Reported observation:** 10264-byte Case yields 907290-byte public JSON through repeated source identifier.

**Reproduction status:** independently_reproduced

**Minimal input:** fixtures/ENG-04.json

**Actual output and persistence:** Exactly 10264 source bytes and 907290 public JSON bytes; 8192-character source.id appears in all 107 findings. SUPPORTED depreciation 15500. Native result and cached job also retain repeated findings.

**Expected behavior:** Bound identifiers and diagnostic work/output. Use bounded display references without repeated raw oversized identifiers; reject invalid bounds with specific requirements, or preserve findings through a bounded representation. Do not silently discard substantive findings.

**Production entry point:** Authenticated loopback HTTP /v1/operations → submit → /v1/jobs → worker → production source execution → persisted owner workpaper

**Confirmed mechanism / code reference:** source_screening.py:source/text validate nonblank only; Screening.add line 71 copies source.id into every finding; interfaces/public_output.py:curate_anomalies line 99 preserves each copy. Hosted inbound cap does not bound output product.

**Executable regression:** regressions.py:Regressions.test_ENG_04

**Actual evidence:** evidence/ENG-04.json.gz

**Dependencies and overlap:** ENG-03 related identifier validation; distinct field and failure mode.

**Remediation boundary:** Shared identifier contract plus anomaly representation/public serialization and service output budget.

**Evidence limits:** Exact size reproduced with json.dumps UTF-8 sizing; no destructive load test. Resource exhaustion at maximum input is inferred, not tested. Regression uses a duplicate-count contract rather than inventing a maximum ID length.

### ENG-05 — Contradictory AP payment evidence

**Severity:** High

**Accounting/control impact:** insufficient evidence; incorrect blocking or qualification

**Original reviewer:** Independent final engineering/governance review (E/G identifiers)

**Reported observation:** 110 payment detail conflicts with zero declared payments but closing AP 110 is SUPPORTED.

**Reproduction status:** independently_reproduced

**Minimal input:** fixtures/ENG-05.json

**Actual output and persistence:** SUPPORTED invoices 110, opening AP 0, payments 0, closing AP 110; no requirements. Payment detail is retained in facts_used but ignored. Invoice expense/AP proposal persists.

**Expected behavior:** Preserve independently supported invoice 110, identify detail/aggregate contradiction, and withhold supported closing AP pending resolution. Do not silently choose either payment total or treat incomplete detail as bank-confirmed.

**Production entry point:** Authenticated loopback HTTP /v1/operations → submit → /v1/jobs → worker → production source execution → persisted owner workpaper

**Confirmed mechanism / code reference:** source_execution.py:accounts_payable lines 423–427 reads payments_total only; never screens case.payments. Existing accounts-payable/workflow.py:assess handles a payments population.

**Executable regression:** regressions.py:Regressions.test_ENG_05

**Actual evidence:** evidence/ENG-05.json.gz

**Dependencies and overlap:** ACC-05 both AP evidence handling, but ignored conflicting detail versus malformed cross-row overlap scan are independent root causes.

**Remediation boundary:** Reconcile supplied detail with summary where supported; otherwise explicitly qualify unsupported payment evidence. Keep invoice recognition separate from complete-balance assertions.

**Evidence limits:** Synthetic IFRS 2026 fixture; no customer upload or deployed TrackedFR endpoint tested.

### GOV-01 — Release receipt sidecar tampering

**Severity:** Medium

**Accounting/control impact:** release evidence integrity

**Original reviewer:** Independent final engineering/governance review (E/G identifiers)

**Reported observation:** Modified sidecars accepted by normal Python verifier.

**Reproduction status:** independently_reproduced

**Minimal input:** governance.py:SIDECARS

**Actual output and persistence:** Each of four individual sidecars replaced with {} plus newline in a disposable frozen clone. All four actual verify_release.py invocations exit 0 with PASS, 3844 tests, 8912 preserved files. Untouched verifier passes; tampered bound command log fails.

**Expected behavior:** Bind imported evidence inventory and post-run attestations to authoritative digests; reject every altered evidence class. Preserve original receipt identities and bytes; no historical receipt backfill.

**Production entry point:** Actual frozen verifier in a disposable local Git clone

**Confirmed mechanism / code reference:** skills/presumed-sources/verify_release.py:verify binds main receipt and listed command/shard logs, but does not validate start-source-hashes.json, suite-1.json, outer full-regression log or receipt-review.md. build4/run_release.py:input_hashes excludes /release/ paths.

**Executable regression:** governance.py:Governance.test_GOV_01

**Actual evidence:** evidence/GOV-01-0.json; evidence/GOV-01-1.json; evidence/GOV-01-2.json; evidence/GOV-01-3.json

**Dependencies and overlap:** GOV-02 can suppress checks that do exist; GOV-01 omits checks in ordinary Python.

**Remediation boundary:** Add explicit complete inventory/attestation verification and negative cases; retain independent baseline valid-control prerequisite.

**Evidence limits:** Four reported evidence classes tested independently, not every sidecar. No allegation that the actual frozen receipt was tampered with. Full verifier performs discovery and receipt checks, not a full accounting regression.

### GOV-02 — Optimized Python governance bypass

**Severity:** Medium

**Accounting/control impact:** historical preservation integrity

**Original reviewer:** Independent final engineering/governance review (E/G identifiers)

**Reported observation:** Unauthorized workflow accepted under python -O.

**Reproduction status:** independently_reproduced

**Minimal input:** governance.py:test_GOV_02

**Actual output and persistence:** Actual workflow bytes modified only in disposable clone. verify_historical() under ordinary Python rejects Active successor workflow changed; identical invocation under -O exits 0 and returns 8912.

**Expected behavior:** Mandatory integrity checks must remain enforced under optimization, or verifier must explicitly refuse optimized execution before reporting success.

**Production entry point:** Actual frozen verifier in a disposable local Git clone

**Confirmed mechanism / code reference:** skills/presumed-sources/verify_release.py:verify_workflow_migration, verify_historical, validate_population, _counted_pass and verify use assert for mandatory controls. Python -O removes these expressions, including hash checks.

**Executable regression:** governance.py:Governance.test_GOV_02

**Actual evidence:** evidence/GOV-02-normal.json; evidence/GOV-02-optimized.json

**Dependencies and overlap:** GOV-01 omitted coverage remains a separate ordinary-mode gap.

**Remediation boundary:** Replace optimization-sensitive governance checks or explicitly reject optimized interpreter; assess adjacent receipt/population/namespace checks without altering historical contracts.

**Evidence limits:** Exact historical-verifier bypass reproduced with real filesystem mutation, stronger than original read_bytes injection. Whole verify() under -O not separately executed. Existing reviewed CI uses ordinary Python.

### ENG-06 — Malformed operation returns HTTP 503

**Severity:** Medium

**Accounting/control impact:** incorrect client error boundary

**Original reviewer:** Independent final engineering/governance review (E/G identifiers)

**Reported observation:** Array/object operation causes unavailable response instead of structured client error.

**Reproduction status:** independently_reproduced

**Minimal input:** regressions.py:test_ENG_06

**Actual output and persistence:** Both [] and {} at both /v1/operations and /v1/jobs return 503 unavailable with no field requirements; four trace variants retained.

**Expected behavior:** Malformed operation is a deterministic 4xx invalid_request with operation requirement; no job acceptance or accounting work.

**Production entry point:** Authenticated HTTP /v1/operations and /v1/jobs → Service.validate

**Confirmed mechanism / code reference:** local_cao/validation.py:requirements line 15 performs set membership on unhashable operation before validating type. Service.validate lines 77–80 calls it before structured try handler; outer service maps exception to unavailable.

**Executable regression:** regressions.py:Regressions.test_ENG_06

**Actual evidence:** evidence/ENG-06-operations-array.json.gz; evidence/ENG-06-operations-object.json.gz; evidence/ENG-06-jobs-array.json.gz; evidence/ENG-06-jobs-object.json.gz

**Dependencies and overlap:** ENG-03 is also preacceptance validation, but independent type and exception-boundary failure.

**Remediation boundary:** Type-check before membership; contain validation exceptions inside client boundary; cover both hosted endpoints and local entry.

**Evidence limits:** Synthetic IFRS 2026 fixture; no customer upload or deployed TrackedFR endpoint tested.

### ACC-01 — Opening accumulation validated after additions

**Severity:** High

**Accounting/control impact:** incorrect accounting calculation; insufficient evidence

**Original reviewer:** Independent accounting review, observations supplied by repository owner; original standalone report not recovered

**Reported observation:** Impossible opening accumulation becomes accepted after current additions.

**Reproduction status:** independently_reproduced

**Minimal input:** fixtures/ACC-01.json

**Actual output and persistence:** Opening cost 100 and accumulation 150 plus current purchase 100 are SUPPORTED with cost 200, depreciation 4.58, closing accumulation 154.58 and carrying 45.42. Without addition the control rejects the impossible opening balance.

**Expected behavior:** Validate opening cost and accumulation at opening date before current-period movements. Current additions cannot cure invalid opening balance. Require correction/qualified error analysis, retaining independently supportable movements only with sound dependency treatment.

**Production entry point:** Authenticated loopback HTTP /v1/operations → submit → /v1/jobs → worker → production source execution → persisted owner workpaper

**Confirmed mechanism / code reference:** source_execution.py:fixed_assets.calculate lines 277–278 compares accumulation to opening_cost + additions, not opening_cost. Existing fixed-assets/workflow.py:assess lines 51–52 has analogous ordering (scope expansion requires owner decision).

**Executable regression:** regressions.py:Regressions.test_ACC_01

**Actual evidence:** evidence/ACC-01.json.gz

**Dependencies and overlap:** ENG-02 linked movement/journal side effects require coordinated tests, but do not merge temporal validation into atomicity.

**Remediation boundary:** Opening-state invariants before movement assembly; examine shared historical owner behavior separately without rewriting proofs.

**Evidence limits:** Synthetic IFRS 2026 fixture; no customer upload or deployed TrackedFR endpoint tested.

### ACC-02 — Refundable deposit inherits expense default

**Severity:** High

**Accounting/control impact:** incorrect classification; incorrect journal construction; insufficient evidence

**Original reviewer:** Independent accounting review, observations supplied by repository owner; original standalone report not recovered

**Reported observation:** Class expense default applied despite refundable-deposit text.

**Reproduction status:** independently_reproduced

**Minimal input:** fixtures/ACC-02.json

**Actual output and persistence:** SUPPORTED 110 invoice and durable Dr administrative expense / Cr AP 110 despite refundable security deposit description.

**Expected behavior:** Transaction-specific refundable-deposit evidence conflicts with services_received/expense defaults. Do not propose expense automatically. Seek terms/classification resolution; a supported refundable right belongs in its applicable asset model, without inventing a new account or policy.

**Production entry point:** Authenticated loopback HTTP /v1/operations → submit → /v1/jobs → worker → production source execution → persisted owner workpaper

**Confirmed mechanism / code reference:** source_execution.py:resolved_row copies class account/recognition_basis; specialist only screens limited indicator words; accounts_payable.invoice accepts inherited expense/basis without testing transaction-specific deposit conflict.

**Executable regression:** regressions.py:Regressions.test_ACC_02

**Actual evidence:** evidence/ACC-02.json.gz

**Dependencies and overlap:** ACC-04 also text/structured evidence reconciliation, but missed deposit conflict differs from false affirmative dispute.

**Remediation boundary:** Resolve policy defaults against transaction facts before recognition and journal construction; qualified conflict rather than keyword-only forced asset posting.

**Evidence limits:** Synthetic IFRS 2026 fixture; no customer upload or deployed TrackedFR endpoint tested.

### ACC-03 — Credit disposal debited to cash

**Severity:** High

**Accounting/control impact:** incorrect classification; incorrect journal construction; insufficient evidence

**Original reviewer:** Independent accounting review, observations supplied by repository owner; original standalone report not recovered

**Reported observation:** Credit sale recognized as cash without receipt evidence.

**Reproduction status:** independently_reproduced

**Minimal input:** fixtures/ACC-03.json

**Actual output and persistence:** SUPPORTED; explicit description says credit/no cash received and disposal cash_received=false; nevertheless persisted Dr cash 12000 and gain 2100. Cash-sale positive control also passes.

**Expected behavior:** Derecognition and gain are separate from settlement classification. No cash debit without supported cash receipt. If consideration is an established unpaid receivable, use supported receivable treatment; otherwise qualify the settlement journal, without inventing payment.

**Production entry point:** Authenticated loopback HTTP /v1/operations → submit → /v1/jobs → worker → production source execution → persisted owner workpaper

**Confirmed mechanism / code reference:** source_execution.py:fixed_assets.calculate line 315 hard-codes Dr cash from proceeds; ignores credit terms/receipt facts. Analogous hard-coded cash appears in existing fixed-assets/workflow.py:assess line 74.

**Executable regression:** regressions.py:Regressions.test_ACC_03

**Actual evidence:** evidence/ACC-03.json.gz

**Dependencies and overlap:** ENG-01 is authorization type; a literal true sale still exhibits ACC-03.; ENG-02 is atomicity after rejection; ACC-03 persists an accepted but misclassified journal.

**Remediation boundary:** Disposal consideration/settlement contract and journal construction; preserve asset derecognition math where sufficiently supported.

**Evidence limits:** Credit facts are supplied through description plus explicit synthetic payment_terms/cash_received fields; those fields are not claimed as documented Profile 1.2 supported schema. Even unsupported credit evidence must not silently justify cash. Original accountant request not recovered.

### ACC-04 — Negated dispute interpreted as affirmative

**Severity:** Medium

**Accounting/control impact:** incorrect blocking or qualification

**Original reviewer:** Independent accounting review, observations supplied by repository owner; original standalone report not recovered

**Reported observation:** Negated dispute text blocks invoice.

**Reproduction status:** independently_reproduced

**Minimal input:** fixtures/ACC-04.json

**Actual output and persistence:** Description This invoice is not disputed. with disputed_obligation=false yields UNRESOLVED, invoice excluded, no 110 obligation. Affirmative disputed control correctly blocks.

**Expected behavior:** Do not assert dispute solely from a token inside explicit negation. Reconcile textual/structured evidence with confidence; preserve supported invoice when no genuine conflict remains. Ambiguous text may warrant a scoped clarification.

**Production entry point:** Authenticated loopback HTTP /v1/operations → submit → /v1/jobs → worker → production source execution → persisted owner workpaper

**Confirmed mechanism / code reference:** source_execution.py:specialist line 146 detects dispute/disputed regex tokens without negation and ORs with structured indicator, so literal false cannot override false-positive textual evidence.

**Executable regression:** regressions.py:Regressions.test_ACC_04

**Actual evidence:** evidence/ACC-04.json.gz

**Dependencies and overlap:** ACC-02 concerns unrecognized conflict; separate regression and classification impact.

**Remediation boundary:** Negation/context-aware indicator interpretation; keep affirmative dispute controls and avoid globally disabling screening.

**Evidence limits:** Synthetic IFRS 2026 fixture; no customer upload or deployed TrackedFR endpoint tested.

### ACC-05 — Malformed invoice blocks independently supported accrual

**Severity:** High

**Accounting/control impact:** incorrect blocking or qualification; loss of valid-row calculations

**Original reviewer:** Independent accounting review, observations supplied by repository owner; original standalone report not recovered

**Reported observation:** Unrelated malformed invoice blocks supportable work.

**Reproduction status:** independently_reproduced

**Minimal input:** fixtures/ACC-05.json

**Actual output and persistence:** Malformed invoice supplier is excluded. Independent 200 accrual has explicit invoice_overlap_resolved=true but is also excluded because normalized(None) raises while scanning invoice supplier. Standalone accrual control produces 200.

**Expected behavior:** Preserve 200 closing accrual and its supported adjustment when explicit overlap assessment resolves dependency; retain invoice-specific requirement. If overlap is genuinely unresolved, qualify it instead of inventing independence.

**Production entry point:** Authenticated loopback HTTP /v1/operations → submit → /v1/jobs → worker → production source execution → persisted owner workpaper

**Confirmed mechanism / code reference:** source_execution.py:accounts_payable.accrual line 401 evaluates any(normalized(invoice.supplier) ...) before checking whether invoice_overlap_resolved exists. ReviewRequired from unrelated invalid supplier is caught as an accrual-row defect by Screening.row.

**Executable regression:** regressions.py:Regressions.test_ACC_05

**Actual evidence:** evidence/ACC-05.json.gz

**Dependencies and overlap:** ENG-05 ignored payment contradictions is independent, not the same blocking defect.

**Remediation boundary:** Validate/scope overlap population and honor supported overlap evidence before traversing invalid suppliers; retain genuine duplicate-liability controls.

**Evidence limits:** Reconstructed minimal fixture, not recovered original accountant request. Early exploratory fixture lacked explicit overlap assessment; retained separately and superseded for definitive reproduction by explicit true assessment.


## Remediation verification — 5 November 2026

Published tested source: `33704a4cfecf8d54f4333fe8b836033d8c5ee826`. Original suites: 19 runtime + 4 governance methods pass, no errors/skips. Governance uses `CAO_GOV_REF=33704a4cfecf8d54f4333fe8b836033d8c5ee826 CAO_GOV_FOCUSED=1` and verifies a newly executed, separately versioned positive receipt BEFORE tampering. Independent QA and compatibility are in [completion report](remediation/COMPLETION.md). Machine-readable register binds per-ID evidence digests. Original diagnostic artifact-sha256.json remains the inventory for its original diagnostic commit; it is not relabeled for these updated register files.

- **ENG-01 — verified fixed:** Literal disposal booleans validated; invalid flags cannot authorize journals.
- **ENG-02 — verified fixed:** Asset journals staged atomically; rejected dependent capital movements withheld; valid mixed rows retained.
- **ENG-03 — verified fixed:** Bounded nonblank source Case IDs checked inline, staged, preacceptance and direct owner.
- **ENG-04 — verified fixed:** Bounded identifiers/populations and hashed public display reference retain substantive anomalies.
- **ENG-05 — verified fixed:** Payment detail, aggregate and supplied period/scope reconciled; invalid balance evidence preserves invoices.
- **ENG-06 — verified fixed:** Operation type validated before set membership; structured client requirements returned.
- **ACC-01 — verified fixed:** Opening accumulated depreciation checked against opening gross before additions.
- **ACC-02 — verified fixed:** Refundable-deposit evidence cannot inherit generic expense recognition without classification resolution.
- **ACC-03 — verified fixed:** Cash requires explicit consistent receipt; supported credit consideration uses receivable; uncertain settlement qualified.
- **ACC-04 — verified fixed:** Scoped negation recognizes dispute verb forms while preserving affirmative/conflicting dispute screening.
- **ACC-05 — verified fixed:** Explicit overlap assessment isolates valid accrual; malformed invoice cannot erase it; accrual supplier independently validated.
- **GOV-01 — verified fixed:** Versioned inventory binds required sidecars, maps, logs and review; required-role omissions/redirection fail closed.
- **GOV-02 — verified fixed:** Verifier refuses optimized interpreter at import before any mandatory assertion can be bypassed.
