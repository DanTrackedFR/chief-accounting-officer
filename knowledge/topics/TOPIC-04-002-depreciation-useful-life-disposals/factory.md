# TOPIC-04-002 — Depreciation / Useful Life & Residual Value / Asset Transfer, Disposal & Retirement

Status: REVIEWED / production-candidate
Capabilities: CAO-04-004, CAO-04-005, CAO-04-006
Sensitivity: HIGH
Source checked: 2026-09-22

## Sources
IFRS: IAS 16 Property, Plant and Equipment, official IFRS Foundation source. AASB: AASB 116 current applicable compilation, official AASB source. UK: FRS 102 Section 17, September 2024 edition/current amendments. US: ASC 360 PP&E/depreciation architecture; public FASB material confirms key US/IFRS differences, but complete current Codification paragraph-body verification remains PARTIAL under the programme's existing source limitation.

## Principles
Depreciation allocates depreciable amount systematically over the period/pattern of expected consumption; it is not a valuation adjustment. Useful life is entity-specific expected utility, not necessarily physical/economic life. Residual value is estimated disposal value at the end of useful life under the framework definition. Changes in useful life, residual value or method are generally estimate changes applied prospectively under the relevant framework, not prior-period errors absent an earlier error.

## IFRS / AASB
IAS 16/AASB 116 require significant components with different useful lives/patterns to be depreciated separately. Depreciation begins when the asset is available for use. Depreciable amount is allocated systematically over useful life. Residual value/useful life are reviewed at least annually under IAS 16/AASB 116; method reflects consumption pattern and is reviewed for significant change. AASB 116 paragraph family 43–62 provides the component/depreciation architecture. Held-for-sale classification can change when depreciation ceases under IFRS/AASB; route to disposal/held-for-sale topic as applicable.

## UK GAAP
FRS 102 Section 17.16–17.21 requires component depreciation where major components have significantly different consumption patterns; systematic allocation over useful life; depreciation begins when available for use; indicators of changed residual value/useful life/method trigger estimate reassessment. Section 17 uses an indicator-based review approach rather than blindly assuming every IFRS review mechanic is identical.

## US GAAP
US PP&E is generally carried at historical cost less accumulated depreciation/impairment; upward revaluation is not the ordinary US model. Component depreciation is permitted but, unlike IFRS, is not generally required. Determine depreciation method/life/residual value based on expected consumption/use and entity policy; current detailed Codification references must be verified before APPROVED paragraph-level status.

## CAO workflow
1. Confirm asset exists/is capitalized and available-for-use date.
2. Determine depreciable base: recorded cost/other basis less residual value as applicable.
3. Identify significant components and framework requirement/policy.
4. Establish useful life using expected usage/capacity, wear, maintenance, obsolescence, strategy, demand and legal/contractual limits.
5. Select method reflecting consumption pattern: straight-line, diminishing balance, units-of-production or other supportable method.
6. Reassess life/residual/method at required cadence or when indicators arise.
7. Distinguish estimate change from correction of error.
8. For transfer, preserve asset identity/cost/accumulated depreciation and assess whether entity/book/classification changes create accounting consequences.
9. For disposal/retirement, determine derecognition date, proceeds/receivable, carrying amount and resulting gain/loss under applicable framework.
10. Reconcile fixed-asset register to GL and reporting/disclosure population.

## Calculation
Straight-line annual depreciation = (depreciable basis - residual value, where residual not already embedded in basis) / useful life, adjusted for available-for-use timing and framework/entity convention. Production calculations must use actual dates/policy and cannot assume a full-month convention merely because the fixed-asset system does.

Disposal gain/loss = consideration/proceeds recognized under applicable guidance less carrying amount derecognized, with transaction-specific adjustments where relevant.

## Journals
Depreciation: Dr depreciation expense or qualifying asset/inventory cost / Cr accumulated depreciation. Disposal: Dr cash/receivable; Dr accumulated depreciation; Cr asset cost; balancing gain/loss. Exact presentation/classification follows facts/framework.

## Controls
Capitalization-to-available-for-use approval; useful-life/residual-value policy by asset class; component review; annual/indicator reassessment; asset-register change approval; disposal authorization; physical existence/retirement feed; depreciation recalculation; FA-to-GL reconciliation; gain/loss review.

## Systems/data
asset_id, entity, class, component, cost/basis, in-service date, method, useful_life, residual_value, accumulated_depreciation, location/custodian, impairment, transfer history, disposal date/proceeds, policy version, reviewer.

## Artifacts
Useful-life study; depreciation policy; component assessment; change-in-estimate memo; disposal calculation; transfer form; asset rollforward/reconciliation.

## Scenarios
1. Server expected life drops from five to three years due to technology: prospective estimate change if prior estimate was reasonable; assess impairment separately.
2. Building roof and structure have materially different lives: IFRS/AASB componentization required; US conclusion may differ.
3. Asset is idle but still available for use: do not automatically stop depreciation under IFRS/AASB/FRS 102.
4. Machine sold mid-period: calculate depreciation through appropriate derecognition/held-for-sale point and disposal gain/loss.
5. Asset transferred between cost centers only: usually classification/master-data move, not disposal; preserve cost/accumulated depreciation lineage.

## QA
PASS for factory build. IFRS/AASB and FRS 102 official depreciation architecture verified; material US difference captured. US paragraph-level Codification depth remains PARTIAL, documented and non-blocking.