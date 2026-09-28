# Technical accounting — Phase 2D QA remediation self-review

Checked 27 September 2026 against AGENTS.md, canonical manifest/matrix, existing packs, and PR #1 QA comment. This report is a worker proposal; the shared manifest remains unchanged. Source materials remain REFERENCE_ONLY; no standards text/PDF is copied.

## Scope, outcome and limitations

- 63 canonical topics and 126 capability mappings across Domains 03, 05, 06, 07, 08 and 13 have been audited and have substantive packs. The manifest lists 34 duplicate/retry folder references, counted under canonical IDs once.
- Batch reports 01–22 preserve prior work and record additions; batches 10–22 respond to QA with decision forks, cross-framework routing, workpapers, controls, source links, adverse cases and explicit unresolved limits.
- Nine operational/method topics below are **candidates for independent REVIEWED assessment**, not self-promoted. The other 54 remain **PARTIAL** because full source-depth and applicable framework checks have not all been independently completed. Exact US Codification paragraph verification remains incomplete: the Basic View landing page was located, but a live paragraph session did not return content on 28 September 2026. This is a source-access/verification gap, not a restriction on citing paragraph identifiers or a need to reproduce copyrighted text; it does not excuse available FRC/AASB/IFRS checks.
- Existing README labels “REVIEWED / production-candidate” and scenario PASS text are not canonical status; arithmetic and structural checks do not prove the full factory contract.

## Source/effective-period gates

| Domain | Primary route to check in each case |
|---|---|
| 03 | IFRS 15/9; ASC 606/326/340-40; FRS 102 §§23/11; AASB 15/9 |
| 05 | IAS 19/37, IFRS 2/15; ASC 450/710/715/718/420; FRS 102 §§21/23/26/28; AASB 119/137/2/15 |
| 06 | IAS 7/21/32, IFRS 7/9/13; ASC 230/470/815/820/830/326; FRS 102 §§7/11/12/22/30/2A; AASB 107/121/132/7/9/13 |
| 07 | IFRS 3/10/11/12, IAS 21/28; ASC 805/810/323/830; FRS 102 §§9/14/15/19/30; AASB 3/10/11/121/128 |
| 08 | IAS 1/7/8/10/24/33, IFRS 8/18; ASC 205/230/260/280/850; FRS 102 §§1A/3–8/32/33; AASB 101/107/110/124/133/8/18 |
| 13 | IFRS 3/5/9/10/11, IAS 21/24/29/32/37; ASC 805/852/830/470/815/850; FRS 102 §§19/22/30/31/33; AASB counterparts |

Period gates verified on official overview/register pages: revised FRS 102 Sections 20/23 principally annual periods beginning 1 January 2026 (check transitional choices); IFRS 9/7 classification amendments 1 January 2026; IAS 21 lack-of-exchangeability 1 January 2025; November 2025 IAS 21 hyperinflationary-presentation amendment 1 January 2027 with early application; IFRS 18 annual periods from 1 January 2027 with early application; FASB ASU 2025-05 eligible trade-AR/contract-asset expedient annual periods beginning after 15 December 2025. AASB compilation commencement varies by Standard and entity type: select the actual operative version, especially at 1 July 2026 and 1 January 2027. Do not use a dated AASB link as blanket current authority.

## Topic-by-topic disposition

“Source gate” means exact current US ASC paragraph applicability has not been independently verified in Basic View where the topic relies on US GAAP; IFRS/FRC/AASB section and effective version must still be checked against the particular reporting period. This is a precise source-access limitation, not a claim that every other subquestion is solved.

| Canonical ID | Capabilities | Worker proposal | Remaining gate / QA focus |
|---|---|---|---|
| TOPIC-03-001 | CAO-03-001, CAO-03-002, CAO-03-003 | PARTIAL | Linked-contract/material-right terms and duplicate routing; source gate and effective-period verification. Preserve/canonicalize 4 manifest duplicate paths. |
| TOPIC-03-002 | CAO-03-004, CAO-03-005 | PARTIAL | Constraint/specific allocation evidence and US 606 body; source gate and effective-period verification. |
| TOPIC-03-003 | CAO-03-006, CAO-03-007 | PARTIAL | Right-to-payment and input-method paragraph mapping; source gate and effective-period verification. |
| TOPIC-03-004 | CAO-03-008, CAO-03-009 | PARTIAL | Specified-promise control and contract-balance rules; source gate and effective-period verification. |
| TOPIC-03-005 | CAO-03-010, CAO-03-011 | PARTIAL | Acceptance-versus-control and refund/credit interplay; source gate and effective-period verification. |
| TOPIC-03-006 | CAO-03-012, CAO-03-013 | PARTIAL | Cost asset impairment sequence and UK transition; source gate and effective-period verification. |
| TOPIC-03-007 | CAO-03-014, CAO-03-015 | PARTIAL | Return asset and price concession versus credit loss; source gate and effective-period verification. |
| TOPIC-03-008 | CAO-03-016, CAO-03-017 | PARTIAL | UK Section 11 impairment and US ASU election scope; source gate and effective-period verification. |
| TOPIC-03-009 | CAO-03-018, CAO-03-019 | PARTIAL | Write-off/recovery presentation and duplicate routing; source gate and effective-period verification. Preserve/canonicalize 2 manifest duplicate paths. |
| TOPIC-03-010 | CAO-03-020, CAO-03-021 | PARTIAL | Customer-credit legal expiry and duplicate routing; source gate and effective-period verification. Preserve/canonicalize 2 manifest duplicate paths. |
| TOPIC-03-011 | CAO-03-022, CAO-03-023 | REVIEWED candidate — method | Independent event population and control precision; independent QA of control evidence and source handoffs. Preserve/canonicalize 2 manifest duplicate paths. |
| TOPIC-03-012 | CAO-03-024, CAO-03-025 | PARTIAL | RPO expedients and acquired-system completeness; source gate and effective-period verification. |
| TOPIC-05-001 | CAO-05-001, CAO-05-002 | REVIEWED candidate — method | AP source-to-GL exception ownership; independent QA of control evidence and source handoffs. |
| TOPIC-05-002 | CAO-05-003, CAO-05-004 | REVIEWED candidate — method | Service accrual backtest and reversal controls; independent QA of control evidence and source handoffs. |
| TOPIC-05-003 | CAO-05-005, CAO-05-006 | PARTIAL | ASC 450/FRS 21/AASB 137 reimbursement thresholds; source gate and effective-period verification. |
| TOPIC-05-004 | CAO-05-007, CAO-05-008 | PARTIAL | US contract-specific loss rules, impairment waterfall; source gate and effective-period verification. |
| TOPIC-05-005 | CAO-05-009, CAO-05-010 | PARTIAL | ASC 715/FRS 28/AASB 119 plan-measurement mapping; source gate and effective-period verification. |
| TOPIC-05-006 | CAO-05-011, CAO-05-012 | PARTIAL | Bonus obligation and commission capitalization differences; source gate and effective-period verification. |
| TOPIC-05-007 | CAO-05-013, CAO-05-014 | PARTIAL | ASC 718/FRS 26/AASB 2 cash/equity classification; source gate and effective-period verification. |
| TOPIC-05-008 | CAO-05-015, CAO-05-016 | PARTIAL | Cancellation/replacement guidance and duplicate routing; source gate and effective-period verification. Preserve/canonicalize 2 manifest duplicate paths. |
| TOPIC-05-009 | CAO-05-017, CAO-05-018 | PARTIAL | US termination trigger, UK/AA leave, duplicate routing; source gate and effective-period verification. Preserve/canonicalize 2 manifest duplicate paths. |
| TOPIC-05-010 | CAO-05-019, CAO-05-020 | REVIEWED candidate — method | Payroll interface/capitalization exception proof; independent QA of control evidence and source handoffs. Preserve/canonicalize 2 manifest duplicate paths. |
| TOPIC-06-001 | CAO-06-001, CAO-06-002, CAO-06-003 | PARTIAL | Cash restriction and US cash-flow reconciliation; duplicate routing; source gate and effective-period verification. Preserve/canonicalize 2 manifest duplicate paths. |
| TOPIC-06-002 | CAO-06-004, CAO-06-005 | PARTIAL | Cash-equivalent and advance-FX model; duplicate routing; source gate and effective-period verification. Preserve/canonicalize 2 manifest duplicate paths. |
| TOPIC-06-003 | CAO-06-006, CAO-06-007 | PARTIAL | Net-investment FX and disposal reserve; duplicate routing; source gate and effective-period verification. Preserve/canonicalize 2 manifest duplicate paths. |
| TOPIC-06-004 | CAO-06-008, CAO-06-009 | PARTIAL | Functional-currency mixed indicators and change date; source gate and effective-period verification. |
| TOPIC-06-005 | CAO-06-010, CAO-06-011 | PARTIAL | Revolver fee/US presentation and EIR exactness; source gate and effective-period verification. |
| TOPIC-06-006 | CAO-06-012, CAO-06-013 | PARTIAL | Lender fee test and reporting-date waiver rights; source gate and effective-period verification. |
| TOPIC-06-007 | CAO-06-014, CAO-06-015 | PARTIAL | 2026 contingent SPPI amendment and duplicate routing; source gate and effective-period verification. Preserve/canonicalize 2 manifest duplicate paths. |
| TOPIC-06-008 | CAO-06-016, CAO-06-017 | PARTIAL | Independent derivative valuation/hierarchy sensitivity; source gate and effective-period verification. |
| TOPIC-06-009 | CAO-06-018, CAO-06-019 | PARTIAL | Hedge discontinuation and associate scope; duplicate routing; source gate and effective-period verification. Preserve/canonicalize 2 manifest duplicate paths. |
| TOPIC-06-010 | CAO-06-020, CAO-06-021 | PARTIAL | Stage versus CECL loan disclosure and allowance exception; source gate and effective-period verification. |
| TOPIC-07-001 | CAO-07-001, CAO-07-002 | PARTIAL | Substantive rights, US VIE, acquisition-date cutover; source gate and effective-period verification. |
| TOPIC-07-002 | CAO-07-003, CAO-07-004 | PARTIAL | NCI rights/allocation and duplicate routing; source gate and effective-period verification. Preserve/canonicalize 2 manifest duplicate paths. |
| TOPIC-07-003 | CAO-07-005, CAO-07-006 | REVIEWED candidate — method | Bilateral FX/payment timing control; independent QA of control evidence and source handoffs. |
| TOPIC-07-004 | CAO-07-007, CAO-07-008 | PARTIAL | Upstream/NCI and deferred-tax fixed-asset transfer; source gate and effective-period verification. |
| TOPIC-07-005 | CAO-07-009, CAO-07-010 | REVIEWED candidate — method | Consolidation source-version and re-run controls; independent QA of control evidence and source handoffs. |
| TOPIC-07-006 | CAO-07-011, CAO-07-012 | PARTIAL | Group rate/mapping and CTA attribution; source gate and effective-period verification. |
| TOPIC-07-007 | CAO-07-013, CAO-07-014 | PARTIAL | Associate basis, loss-limit, IAS 28 project boundary; source gate and effective-period verification. |
| TOPIC-07-008 | CAO-07-015, CAO-07-016 | PARTIAL | Joint operation rights and US/UK models; source gate and effective-period verification. |
| TOPIC-07-009 | CAO-07-017, CAO-07-018 | PARTIAL | OCI/remainder valuation on loss of control; source gate and effective-period verification. |
| TOPIC-08-001 | CAO-08-001, CAO-08-002 | PARTIAL | Debt covenant classification and 2027 IFRS 18 transition; source gate and effective-period verification. |
| TOPIC-08-002 | CAO-08-003, CAO-08-004 | PARTIAL | Cash-flow category/indirect mismatch and IFRS 18; source gate and effective-period verification. |
| TOPIC-08-003 | CAO-08-005, CAO-08-006 | PARTIAL | Equity/NCI and disclosure population by tier; source gate and effective-period verification. |
| TOPIC-08-004 | CAO-08-007, CAO-08-008 | PARTIAL | Prior-period error, comparative and transition; source gate and effective-period verification. |
| TOPIC-08-005 | CAO-08-009, CAO-08-010 | PARTIAL | Going-concern horizon/event cutoff cross-framework; source gate and effective-period verification. |
| TOPIC-08-006 | CAO-08-011, CAO-08-012 | PARTIAL | CODM/ASC 280 and UK/AASB related-party scope; source gate and effective-period verification. |
| TOPIC-08-007 | CAO-08-013, CAO-08-014 | PARTIAL | EPS scope/anti-dilution and regulator APM rules; source gate and effective-period verification. |
| TOPIC-08-008 | CAO-08-015, CAO-08-016 | PARTIAL | Entity-specific filing law/size/tier, statutory mapping; source gate and effective-period verification. |
| TOPIC-08-009 | CAO-08-017, CAO-08-018 | REVIEWED candidate — method | Assertion source and late-change recertification; independent QA of control evidence and source handoffs. |
| TOPIC-08-010 | CAO-08-019, CAO-08-020 | REVIEWED candidate — method | Dependency critical path and source-version certification; independent QA of control evidence and source handoffs. |
| TOPIC-13-001 | CAO-13-001, CAO-13-002 | PARTIAL | PPA intangible/tax/NCI and US ASU current body; source gate and effective-period verification. |
| TOPIC-13-002 | CAO-13-003, CAO-13-004 | PARTIAL | Earn-out/service split and FRS Section 19 difference; source gate and effective-period verification. |
| TOPIC-13-003 | CAO-13-005, CAO-13-006 | PARTIAL | Measurement-period cost/tax and ASC current body; source gate and effective-period verification. |
| TOPIC-13-004 | CAO-13-007, CAO-13-008 | PARTIAL | US discontinued strategic-shift and UK disposal model; source gate and effective-period verification. |
| TOPIC-13-005 | CAO-13-009, CAO-13-010 | PARTIAL | Asset-versus-business and restructuring recognition; source gate and effective-period verification. |
| TOPIC-13-006 | CAO-13-011, CAO-13-012 | PARTIAL | Debt modification/equity classification US/UK differences; source gate and effective-period verification. |
| TOPIC-13-007 | CAO-13-013, CAO-13-014 | PARTIAL | Warrant fixed-for-fixed and ASC own-equity exceptions; source gate and effective-period verification. |
| TOPIC-13-008 | CAO-13-015, CAO-13-016 | PARTIAL | Off-market related-party transaction-specific models; source gate and effective-period verification. |
| TOPIC-13-009 | CAO-13-017, CAO-13-018 | PARTIAL | Common-control policy and UK group reconstruction; source gate and effective-period verification. |
| TOPIC-13-010 | CAO-13-019, CAO-13-020 | PARTIAL | ASC 852 qualification/filing context; duplicate routing; source gate and effective-period verification. Preserve/canonicalize 2 manifest duplicate paths. |
| TOPIC-13-011 | CAO-13-021 | PARTIAL | IAS 21 issued 2027 gate, ASC 830; duplicate routing; source gate and effective-period verification. Preserve/canonicalize 4 manifest duplicate paths. |
| TOPIC-13-012 | CAO-13-022 | REVIEWED candidate — method | Multi-topic issue ownership and close evidence; independent QA of control evidence and source handoffs. |

## Regression and contract self-review

- Local scan: 63/63 canonical IDs have artifacts; 126/126 assigned capability mappings represented in the manifest inventory; all 63 topic packs scanned for relative Markdown links and none broken. A final independent cross-domain arithmetic regression re-performed 24 examples spanning revenue, credit loss, compensation, treasury, consolidation, reporting and special transactions; all passed. Scenario negatives are documented in each pack; they remain narrative tests pending independent QA.
- Source provenance uses official IFRS Foundation, FASB, FRC, AASB and SEC locations. A source URL is not proof of every paragraph body; do not claim US paragraph verification from an ASU or FASB project summary. One stale IAS 21 pipeline assertion was corrected in 13-011. AASB 8 and 10 links were corrected to identifiable compilations with period gates.
- Factory contract check: every topic has decision method and applicable standards/practice routing, with worked cases, adverse conditions, evidence and controls; further depth is required where the table says PARTIAL. Operational packs use source handoffs rather than artificial four-framework standards. Duplicates are preserved and counted once. No shared manifest, progress, roadmap, Master Build Map or other worker domain was edited.
- Independent QA owns status promotion and integration. This report does not assert all 63 are REVIEWED-ready. The remaining source-depth queue, especially current US Codification access, must be resolved before such a claim; per-topic gates above identify what to recheck.

## 28 September 2026 continuation checkpoint

The latest **main** manifest (generated 28 September 2026) independently classified nine assigned topics REVIEWED and the 54 IDs in this ledger PARTIAL. The worker-branch manifest is an older snapshot and was not edited. PR #1 was merged at 04:37 UTC on 28 September; it cannot receive new commits, though the same `worker/technical-accounting` workstream remains available. TOPIC-03-001 received `practice/period-and-authority-check-2026.md`, preserving existing content and adding verified IFRS/AASB/FRC period routing, an option SSP allocation, adverse cases and exact residual sign-off conditions. The file's calculations reconcile to 180; this topic **remains PARTIAL** pending live ASC Basic View and the later AASB operative compilation for periods commencing 1 July 2026. No other PARTIAL topic is promoted by this checkpoint. This is not a five-topic completion batch.
