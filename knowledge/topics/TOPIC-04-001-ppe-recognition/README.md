# TOPIC-04-001 — Fixed Asset Recognition, Capitalization Policy & Additions

Status: REVIEWED / production-candidate
Built: 2026-09-23
Primary capabilities: CAO-04-001, CAO-04-002, CAO-04-003

## Objective
Enable the CAO to decide whether tangible expenditure is PPE, expense, inventory, investment property or another asset; determine initial cost; apply capitalization policy without replacing standards recognition; produce entries, asset-register data, controls and evidence.

## Authoritative source map
- IFRS: IAS 16 Property, Plant and Equipment; IAS 23 where borrowing costs apply; IAS 36 for impairment; IFRIC 1 for restoration-liability changes. Official IAS 16 page verified 2026-09-23.
- US GAAP: ASC 360 Property, Plant, and Equipment is the core long-lived-asset topic; other specialized guidance may govern capitalization (including interest and industry-specific assets). FASB source family verified 2026-09-23.
- UK GAAP: FRS 102 Section 17 Property, Plant and Equipment, September 2024 edition; Periodic Review 2024 principal effective date 1 January 2026. FRC source verified 2026-09-23.
- AASB: AASB 116 Property, Plant and Equipment, December 2022 compilation, operative for periods beginning on/after 1 January 2023 and before 1 January 2027. AASB source verified 2026-09-23.

No standards-body text is reproduced. Paragraph identifiers are pointers only.

## Principles
A tangible item belongs in PPE when it is held for production/supply, rental or administration and expected to be used beyond one period, subject to the applicable framework. Recognition is assessed when costs are incurred, including later additions/replacements. A capitalization threshold is a practical materiality/control policy; it cannot make an expenditure an asset when the framework requires expense, nor justify expensing individually material assets.

## IFRS / AASB decision logic
IAS 16/AASB 116 recognition centers on probable future economic benefits and reliable measurement. Initial cost includes purchase price net of discounts/rebates; directly attributable costs necessary to bring the asset to the location and condition required for intended operation; and qualifying initial dismantling/removal/site-restoration estimates. Day-to-day servicing is expensed. Replacement/major-inspection costs are capitalized when recognition criteria are met and the replaced/previous-inspection carrying amount is derecognized. Proceeds from selling items produced before intended use are not netted against PPE cost; related proceeds/costs go through profit or loss under the applicable guidance.

Relevant IFRS pointers: IAS 16.7–17, 20–22, 43 onward for component depreciation; IAS 16 derecognition requirements. AASB 116 follows the IAS 16 core architecture but current Australian compilation/entity overlays must be checked independently.

## US GAAP decision logic
US GAAP does not use IAS 16 as its PPE model. Route to ASC 360 plus applicable specialized capitalization literature and entity policy. Establish asset nature, useful life, directly attributable acquisition/construction costs, repairs-versus-betterments and applicable interest-capitalization requirements. Do not import IFRS componentization or revaluation conclusions into US GAAP. Revaluation of ordinary PPE upward to fair value is not a general US GAAP model; component depreciation is not generally mandatory in the IAS 16 sense.

## UK GAAP decision logic
Use FRS 102 Section 17. Establish scope, recognition and initial cost, subsequent model, depreciation/components, impairment and derecognition. The September 2024 FRS 102 edition is current; Periodic Review 2024 has a principal effective date of 1 January 2026. Section 17 contains UK-specific scope/presentation details and revaluation fair-value guidance; do not assume it is word-for-word IAS 16.

## Framework differences that change execution
1. Revaluation: IFRS/AASB and FRS 102 permit a revaluation model subject to their conditions; ordinary US GAAP generally does not permit upward PPE revaluation.
2. Component depreciation: IFRS/AASB require significant components with different useful lives/patterns to be depreciated separately; US GAAP does not impose the same general requirement. FRS 102 has component accounting requirements for significant components.
3. Borrowing costs: route to the applicable borrowing-cost guidance; framework differences exist and are not resolved merely by PPE policy.
4. Thresholds: company thresholds are practice/materiality controls across frameworks, not authoritative recognition criteria.
5. Specialized assets: bearer plants, investment property, held-for-sale assets, biological/extractive assets and regulated/industry assets can leave the ordinary PPE route.

## CAO workflow
1. Resolve entity, framework, reporting period, asset class and materiality.
2. Obtain invoice/PO/contract, receiving/in-service evidence and project/addition support.
3. Determine correct accounting scope.
4. Identify unit of account/components and whether expenditure creates/acquires/enhances an asset versus maintains existing condition.
5. Build cost pool: purchase price; taxes/duties; direct costs; restoration obligation; borrowing costs if separately applicable; exclude abnormal/start-up/training/general overhead unless authoritative criteria are met.
6. Determine date available for use / placed in service.
7. Apply capitalization threshold only after accounting eligibility/materiality analysis.
8. Assign asset class, owner/location, useful life, residual value, depreciation method and GL mapping.
9. Record addition and any related liability/cash/AP entry.
10. Update fixed-asset register; reconcile addition to GL/AP/project source.
11. Capture judgments, approvals and evidence.

## Typical entries
Simple acquisition: Dr PPE / Cr AP or Cash. Restoration obligation at initial recognition, where applicable: Dr PPE / Cr Provision or ARO liability. Subsequent depreciation is handled in TOPIC-04-002.

## Required Company Context
Framework; reporting period; capitalization policy/threshold; asset classes; useful-life matrix; COA; entity/tax book architecture; ERP/fixed-asset system; approval matrix; project/CIP process; materiality.

## Controls and audit evidence
Controls: approved capitalization policy; PO/project coding; capex approval; invoice/receiving validation; in-service-date evidence; threshold exception review; repairs-and-maintenance analytics; project-to-FA transfer review; duplicate asset prevention; register-to-GL reconciliation; physical existence/ownership controls where material.

Evidence: contracts/invoices; payment/receiving; project ledger; engineering/operations confirmation; location/serial; placed-in-service evidence; restoration estimate; policy and approval; useful-life support; JE; FA register; reconciliation.

## Systems/data
Minimum master data: asset ID, entity, class, description, vendor, invoice/PO/project, acquisition and in-service dates, gross cost, component/parent ID, location/custodian, useful life, residual value, method, GL accounts, status and evidence link.

## Scenario tests
1. Laptop below threshold but bulk purchase material — assess aggregation/materiality and policy; do not blindly expense.
2. Production-line replacement — test component/replacement recognition and derecognition of replaced component.
3. Routine annual maintenance — expense unless it creates a separately recognizable asset/major inspection under framework.
4. Factory commissioning with saleable test output — do not net proceeds against PPE under current IAS 16/AASB treatment.
5. US subsidiary asks to revalue machinery — block IFRS revaluation import; apply US GAAP.
6. Safety equipment required for operations — can qualify even without standalone incremental cash flows when necessary to obtain benefits from related assets.

## QA
PASS for topic-factory use: four-framework routing, differences, execution, entries, controls, evidence, systems and scenarios are present. Specialized capitalization (borrowing costs, software, cloud, CIP) routes to linked topics and is not duplicated here.
