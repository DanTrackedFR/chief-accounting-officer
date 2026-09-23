# TOPIC-04-004 — R&D / Internal Software Cost Allocation / Cloud Implementation

Status: REVIEWED / production-candidate; US paragraph-depth PARTIAL
Capabilities: CAO-04-010, CAO-04-011, CAO-04-012
Knowledge: PRINCIPLES + STANDARDS + PRACTICE + DIFFERENCES
Source check: 2026-09-22

## Objective
Determine whether internal project expenditure is research, development, internal-use software, externally marketed software, implementation/configuration of a cloud service, another asset cost, or period expense; establish when capitalization starts/stops and which directly attributable costs enter the asset.

## IFRS
IAS 38 is the primary source. Research-phase expenditure is expensed. Development expenditure is capitalized only after the entity can demonstrate the IAS 38 development recognition criteria; if research and development phases cannot be distinguished, treat the expenditure as research. Internally generated software follows IAS 38 unless it is integral to related hardware. Capitalization is prospective from the date criteria are first met; prior expense is not reinstated merely because the project later qualifies.

For SaaS/cloud arrangements, first determine whether the customer receives a software intangible asset. The April 2021 IFRIC agenda decision on configuration/customisation costs confirms that access to supplier-hosted application software can be a service rather than a software asset. Configuration/customisation then requires analysis of whether a separate intangible asset arises, whether the supplier provides a distinct service, and the timing of expense/prepayment recognition. The CAO must not automatically capitalize implementation spend because a project is large or multi-year.

The IASB has an active Intangible Assets project intended to update IAS 38 for newer intangible items/new ways of use. This is update-monitoring, not current GAAP replacement.

## AASB
AASB 138 follows the IAS 38 core model. Current official AASB material confirms research expense and the six-part development recognition test, plus software classification based on whether software is integral to hardware. Australian entity-type overlays must be checked where applicable. AASB/SIC-32-style website guidance also routes internally developed websites through AASB 138 recognition criteria.

## UK GAAP
Route to current FRS 102 Section 18 and reporting-period version. UK GAAP must be researched independently rather than inferred from IAS 38. Development-cost policy choices/recognition and useful-life rules can differ from full IFRS. For 2026 periods use the September 2024 edition plus subsequent effective amendments. Detailed paragraph-level Section 18/cloud implementation verification remains required before an APPROVED UK conclusion for unusual SaaS configurations.

## US GAAP
Classification is critical because US GAAP uses different literature for internal-use software, software to be sold/marketed and R&D. ASC 350-40 governs internal-use software. FASB ASU 2025-06 changes internal-use software capitalization and is effective for annual periods beginning after 15 December 2027, including interim periods, with early adoption permitted. The CAO must therefore resolve reporting period and early-adoption status before applying the revised model. Training and most data-conversion costs remain expense categories under the amended guidance; detailed current Codification verification is required for production conclusions. Cloud-hosting implementation also requires determining whether the arrangement includes a software licence versus a service and applying the applicable US guidance.

## CAO workflow
1. Identify project/product, intended use and contractual architecture.
2. Determine applicable accounting model: tangible-integral software; internal-use software; external-sale software; R&D; SaaS/service implementation; acquired intangible.
3. Establish project timeline and accounting gates.
4. For IFRS/AASB, separate research from development and date when every development criterion is demonstrable.
5. For US GAAP, resolve effective version of ASC 350-40 and relevant project model.
6. For SaaS, determine whether customer controls software/intangible or receives access/service.
7. Build cost population by employee/vendor/time period/activity.
8. Classify each cost: directly attributable/capitalizable, expense, training, data conversion, maintenance/support, abnormal/rework, general overhead or mixed.
9. Allocate employee costs using supportable time/activity evidence; avoid arbitrary percentages.
10. Stop capitalization when asset is available for intended use / applicable framework gate is reached.
11. Set useful life/amortization and impairment routing.
12. Reconcile project ledger/subledger to GL and preserve evidence.

## Internal cost allocation
Eligible payroll cost requires employee/activity/time evidence tied to qualifying development. Use actual time or a controlled allocation methodology with rational driver and periodic validation. Executive/general admin time, training, maintenance and unsupported estimates are not capitalized merely because staff worked near the project.

## Cloud implementation decision tree
A. Is there controlled software/intangible? If yes, route asset costs to applicable software/intangible model.
B. If service/SaaS, does configuration/customisation create a separate controlled intangible? If yes, assess IAS 38/AASB 138 or relevant framework.
C. If no asset, is implementation service distinct from hosting/access? Determine provider and timing; expense when received or recognize prepayment when payment precedes service.
D. Third-party provider status matters; do not assume payments to a third party are automatically separate from the SaaS supplier's service.

## Journal patterns
Qualifying capitalization: Dr software/intangible asset or CIP; Cr payroll/AP/cash/accrual. Nonqualifying: Dr R&D/implementation/training expense; Cr payroll/AP/cash. Prepaid service: Dr prepayment; Cr cash/AP, then expense over service receipt. When available for use: transfer CIP and commence amortization under applicable framework.

## Controls / audit
Project approval and accounting classification; capitalization-start memo; technical-feasibility/development-criteria evidence; employee time/allocation control; vendor invoice coding; cloud contract analysis; capitalization cut-off; available-for-use approval; asset register reconciliation; useful-life review; impairment indicators; policy consistency.

## Artifacts
Project accounting memo; research/development gate assessment; software model decision; SaaS/cloud assessment; cost eligibility matrix; employee allocation schedule; capitalization rollforward; available-for-use certificate; amortization schedule; reconciliation; impairment trigger log.

## Systems / data
Project ID and stage; cost center; employee/time source; vendor/PO/invoice; capitalization eligibility; gate date; asset ID; available-for-use date; useful life; GL mapping. Cross-system payroll/AP/project/GL reconciliation is a potential TrackedFR fit when recurring and Excel-heavy.

## Framework differences
IFRS/AASB use a development-criteria model under IAS/AASB 38. US GAAP is model-specific and includes ASC 350-40 internal-use software with a significant future effective-date change from ASU 2025-06. FRS 102 is a separate UK model and cannot be assumed identical to IFRS. Cloud service implementation can therefore produce different capitalization/timing outcomes even for similar economics.

## Scenario tests
1. Product discovery/prototypes before feasibility: expense research under IFRS/AASB.
2. Development criteria all evidenced mid-quarter: capitalize qualifying costs prospectively from supported gate date.
3. Engineers split new functionality/maintenance: require activity/time evidence; capitalize only qualifying development.
4. SaaS implementation with no controlled software: do not automatically create software asset; analyze configuration/customisation services/prepayment.
5. Training during ERP implementation: expense unless a framework-specific rule demonstrably says otherwise.
6. US internal-use project in 2028: check ASU 2025-06 effective/adoption status before applying capitalization gate.
7. Website mainly promotional: route through website/intangible guidance; advertising purpose can prevent asset recognition.
8. Project abandoned before available for use: stop capitalization and assess impairment/write-off.

## QA
PASS for IFRS/AASB architecture and official cloud agenda-decision routing. US status remains PARTIAL at complete current Codification paragraph-body depth; UK unusual cloud/detail conclusions remain PARTIAL pending direct Section 18 verification. These are recorded source-depth limitations, not programme blockers.