# TOPIC-04-003 — Construction in Progress, Fixed-Asset Reconciliation & Capitalized Software Routing

Status: REVIEWED / production-candidate
Built: 2026-09-23
Primary capabilities: CAO-04-007, CAO-04-008, CAO-04-009

## Scope
This topic governs CIP/AUC accounting and the fixed-asset-register-to-GL control. Capitalized software is included as a routing capability here but detailed recognition/cost analysis is deliberately delegated to TOPIC-04-004 because framework divergence is substantial.

## Principles
CIP accumulates qualifying costs for an asset being constructed/developed before it reaches the condition/location necessary for intended use. CIP is not a parking account for uncertain spend. Costs must be attributable to a defined asset/project and supported by capitalization criteria. When ready for intended use, qualifying balance transfers to the appropriate depreciable/amortizable asset class and depreciation/amortization starts under the applicable framework.

## Framework routing
IFRS/AASB: IAS 16/AASB 116 for tangible self-constructed assets, IAS 23/AASB 123 for qualifying borrowing costs, IAS 38/AASB 138 for qualifying intangible/software development, plus impairment guidance. IAS 16's current model requires proceeds from items sold before intended use to be recognized in profit/loss with related cost rather than netted from PPE cost.

UK GAAP: FRS 102 Sections 17/18 and applicable financing-cost requirements. US GAAP: route based on asset nature to ASC 360 and specialized internal-use/software/interest guidance; do not apply IAS 38 development recognition by analogy.

## CIP workflow
1. Define project/asset and framework route.
2. Establish approved budget, capitalization start criteria and cost categories.
3. Map source costs from AP, payroll, procurement/project systems and allocations.
4. Exclude nonqualifying start-up, training, abnormal waste, general admin and post-ready-for-use spend unless separate authoritative criteria are met.
5. Review aged/stalled projects and impairment/abandonment indicators.
6. Obtain ready-for-use/placed-in-service evidence.
7. Transfer qualifying balance to final asset class; assign component/useful-life/master data.
8. Start depreciation/amortization at the correct date.
9. Close project and investigate residual CIP.

## Fixed-asset reconciliation
Required rollforward: opening gross cost + additions + transfers/reclasses + business-combination/other movements - disposals +/- FX/revaluation where applicable = closing gross cost. Reconcile accumulated depreciation/impairment separately. Register totals must tie to GL by entity/account/class; reconciling items require owner, cause, amount, age and resolution date.

## Capitalized-software route
Determine whether software is purchased, internal-use, to be sold/marketed, embedded in hardware, cloud/SaaS implementation, or part of another asset. Then invoke TOPIC-04-004. Do not decide capitalization from project label or management budget alone.

## Controls
Project creation/approval; capitalization-category rules; payroll/time allocation approval; invoice coding; monthly aged-CIP review; ready-for-use certification; timely transfer; residual project closure; FA register-to-GL reconciliation; additions/disposals rollforward; suspense/unmapped asset review; change control over asset master data.

## Evidence
Business case/project approval; contracts/POs/invoices; time records/allocation methodology; project ledger; engineering/product/IT milestone evidence; ready-for-use acceptance; transfer form; FA master record; depreciation start; GL reconciliation.

## TrackedFR fit
Strong fit when monthly CIP/FA reconciliation repeatedly combines ERP GL, AP invoices, project data, payroll/time data and fixed-asset register in Excel. The CAO should recommend it only when that recurring cross-system data problem exists.

## Scenarios
1. Project technically ready but business launch delayed: assess whether asset is already capable of intended operation; commercial launch alone does not necessarily delay depreciation.
2. Abandoned project: stop capitalization, assess write-off/impairment and evidence approval.
3. Payroll allocated to software project: route recognition/eligible-cost analysis to TOPIC-04-004 before capitalizing.
4. Register exceeds GL: reconcile additions/transfers/disposals by source and prevent plug entries.

## QA
PASS for operational factory use. Detailed software accounting is intentionally not duplicated; TOPIC-04-004 is a required dependency.
