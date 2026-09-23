# TOPIC-04-002 — Depreciation, Useful Lives, Residual Values, Transfers & Disposals

Status: REVIEWED / production-candidate
Built: 2026-09-23
Primary capabilities: CAO-04-004, CAO-04-005, CAO-04-006

## Source map
IFRS: IAS 16, with IAS 36 interaction. IFRS official IAS 16 material verified 2026-09-23. AASB: AASB 116 December 2022 compilation, current for periods beginning 1 Jan 2023 to before 1 Jan 2027. UK GAAP: FRS 102 Section 17, September 2024 edition. US GAAP: ASC 360 core PPE/long-lived-asset literature plus specialized guidance where applicable.

## Core accounting model
Depreciation systematically allocates depreciable amount over useful life using a method reflecting consumption of economic benefits. Useful life, residual value and method are accounting estimates requiring periodic review under the applicable framework. Depreciation begins when the asset is available for use/placed in service under the framework, not merely when cash is paid. It stops on derecognition or other framework-specified classification/event; idle assets are not automatically non-depreciating.

## IFRS / AASB
Significant components of an item with different useful lives/patterns are depreciated separately. Useful life and residual value are reviewed at least each financial year-end; changes are prospective estimate changes under IAS 8/AASB 108. Depreciation method reflects expected consumption; revenue-based depreciation is prohibited for PPE. Land and buildings are accounted for separately where appropriate. Derecognition occurs on disposal or when no future economic benefits are expected from use/disposal; resulting gain/loss is based on net disposal proceeds versus carrying amount and is generally recognized in profit or loss rather than revenue.

## FRS 102
Section 17 requires systematic depreciation over useful life, componentization where significant parts have materially different consumption patterns, and review when indicators suggest significant change in useful life, residual value or depreciation method. Paragraphs 17.22–17.23 identify straight-line, diminishing-balance and usage methods and require method reassessment when consumption pattern changes. Apply Section 27 for impairment.

## US GAAP
Depreciate cost less residual/salvage value over estimated useful life using a systematic/rational method. Component depreciation may be used but is not generally mandatory in the IAS 16 sense. Changes in useful life/salvage/method can be estimate-related and require US-GAAP-specific analysis. Do not import IFRS revaluation/component conclusions. Long-lived asset impairment/disposal classification routes to ASC 360 and TOPIC-04-006 where relevant.

## CAO workflow
1. Resolve framework, asset/component and status.
2. Confirm in-service/available-for-use date.
3. Determine depreciable base, residual value, useful life and method with evidence.
4. Check componentization requirements.
5. Calculate current-period depreciation including additions/disposals/transfers.
6. Review estimate-change indicators: usage, maintenance, obsolescence, legal limits, strategy, condition, technology.
7. Apply estimate changes prospectively unless authoritative guidance says otherwise.
8. For transfer, preserve cost/accumulated depreciation/history and reassess class/accounting model.
9. For disposal/retirement, remove gross cost and accumulated depreciation; recognize proceeds/receivable and gain/loss; consider held-for-sale/abandonment/impairment guidance first.
10. Reconcile FA rollforward to GL and disclosure population.

## Calculation
Straight-line annual depreciation = (cost or revalued amount - residual value) / useful life, adjusted for time in service. Other methods must reflect consumption. Production method uses output/usage denominator supported by expected total capacity.

## Evidence
Useful-life policy and asset-specific overrides; engineering/vendor data; maintenance history; obsolescence/technology analysis; legal/contractual limits; residual-value market support; in-service evidence; disposal authorization; sale invoice/proceeds; scrapping certificate; transfer documentation; FA register and GL reconciliation.

## Controls
Useful-life/method master-data approval; in-service-date review; depreciation-run completeness/accuracy; negative/fully depreciated asset analytics; annual estimate review; disposal authorization; proceeds-to-derecognition matching; idle/obsolete asset review; FA-to-GL reconciliation.

## Scenarios
1. Major component has 5-year life within 20-year machine: separate under IFRS/AASB and generally FRS 102; US GAAP conclusion may differ.
2. Asset idle for six months: do not automatically stop depreciation.
3. Useful life changes from 5 to 8 years after new evidence: prospective estimate treatment, subject to framework.
4. Asset sold: remove carrying amount and recognize gain/loss, with held-for-sale route considered where applicable.
5. Revenue-based method proposed: reject for IAS 16/AASB PPE.

## QA
PASS for factory use. Impairment is delegated to TOPIC-04-006; revaluation mechanics remain linked to PPE framework records rather than duplicated here.
