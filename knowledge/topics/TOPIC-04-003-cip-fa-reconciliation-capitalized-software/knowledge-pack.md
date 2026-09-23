# TOPIC-04-003 — Construction in Progress / Fixed Asset Reconciliation / Capitalized Software

Status: REVIEWED / US SOURCE-DEPTH PARTIAL
Capabilities: CAO-04-007, CAO-04-008, CAO-04-009
Knowledge types: PRINCIPLES, STANDARDS, PRACTICE, DIFFERENCES
Source checked: 2026-09-22

## Authoritative source map
IFRS: IAS 16 for constructed PPE; IAS 38 for software/intangibles; IAS 23 where borrowing costs qualify; IAS 36 impairment. IFRS Foundation confirms IAS 16 recognition/cost architecture and IAS 38 internal-generation model.
AASB: AASB 116 / 138 (plus AASB 123 / 136 where applicable), independently verified against AASB portal.
UK GAAP: FRS 102 Sections 17 and 18, with current/effective-period routing; Section 18 treatment must not be assumed identical to IAS 38.
US GAAP: ASC 360 for long-lived tangible assets and ASC 350-40 for internal-use software. ASU 2025-06 materially updates internal-use software guidance and is effective for annual periods beginning after 15 December 2027, including interim periods, with early adoption permitted. Reporting period and early adoption are mandatory routing inputs.

## CIP / constructed PPE
Capitalize directly attributable costs only when the applicable asset-recognition criteria are met. Track projects from authorization through ready-for-use. Depreciation starts when the asset is available for its intended use, not simply when invoices stop or project is administratively closed. Costs incurred after ready-for-use require separate analysis rather than remaining in CIP by default.

CIP controls: approved project/capital budget; project-to-asset mapping; invoice/payroll allocation evidence; capitalization policy; monthly aging; stalled-project review; available-for-use trigger; transfer to asset register; impairment/abandonment review; physical/project-manager confirmation.

## Fixed-asset register to GL
Reconcile opening gross cost and accumulated depreciation plus additions, disposals, transfers, depreciation, impairment, revaluation/FX where applicable to closing balances. Tie asset register by entity/account/class to GL. Investigate unmatched assets, negative NBV, fully depreciated assets still in service, assets in GL but absent register, disposed assets still depreciating and CIP aged beyond expected project dates.

## Capitalized software — CAO routing
1. Establish purpose: internal-use, software to be sold/licensed/marketed, embedded in hardware, cloud/SaaS implementation, acquired software, or other intangible.
2. Resolve framework/reporting period and US early-adoption status.
3. Identify project phases and when recognition/capitalization threshold is met.
4. Classify cost population: employee time, third parties, hosting, data conversion, training, maintenance, overhead, testing, upgrades/enhancements, interest where relevant.
5. Establish control/identifiability for intangible recognition.
6. Determine capitalization start/stop dates and available-for-use date.
7. Build cost rollforward and allocation evidence.
8. Set useful life/amortization/depreciation policy and impairment monitoring.
9. Reconcile project ledger/software schedule to GL.

## Framework differences
IFRS/AASB: IAS/AASB 38 distinguishes research from development; research is expensed and qualifying development is capitalized when all recognition criteria are demonstrated. Internally generated brands/customer-list-like items are not recognized. Software integral to hardware may be PPE rather than intangible.

UK GAAP: route through FRS 102 Section 18 and applicable accounting policy/effective-period requirements; do not copy IAS 38 criteria mechanically.

US GAAP: software model depends on software's nature/use. Internal-use software is governed by ASC 350-40 rather than IAS 38 research/development architecture. ASU 2025-06 removes the old project-stage model and uses updated capitalization thresholds for periods in its effective scope; 2026 cases normally remain under pre-amendment guidance unless facts/effective adoption say otherwise. Full current Codification paragraph-body verification remains PARTIAL under the programme's public-source limitation.

## Journal patterns
During qualifying build: Dr CIP/software asset; Cr AP/payroll/other source. At ready-for-use: Dr final asset class; Cr CIP. Subsequent depreciation/amortization follows applicable useful-life method. Abandoned/impaired projects route to impairment/abandonment analysis, not automatic capitalization continuation.

## Controls / audit evidence
Project approval; technical/business feasibility evidence where framework requires; time-writing/allocation support; vendor invoices/contracts; capitalization start/stop memo; available-for-use evidence; project aging; impairment indicators; reconciliation; useful-life approval; policy consistency; change/upgrade assessment.

## Systems / data
Project ID, entity, asset class, cost category, employee/vendor, service date, capitalization eligibility, allocation rule, approval, phase/status, ready-for-use date, asset ID, useful life, impairment status and source-document lineage.

## Scenarios
1. ERP implementation has licenses, configuration, training and data conversion: classify each cost; do not capitalize whole project.
2. SaaS product developed for customers: do not route automatically to internal-use software.
3. CIP project has no activity for nine months: trigger status/impairment/abandonment review.
4. Asset is operational but still in CIP: transfer and start depreciation from actual available-for-use date; assess catch-up/error.
5. US internal-use project in 2028: test ASU 2025-06 effective/adoption status before using legacy project-stage logic.
6. Register agrees GL total but class-level balances differ: reconciliation fails at appropriate assertion/detail level.

## QA
PASS for factory coverage. US paragraph-depth remains PARTIAL, recorded as non-blocking. No standards text reproduced.