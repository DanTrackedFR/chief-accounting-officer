# PPE Recognition & Capitalization — Knowledge Pack

Status: REVIEWED
Checked: 2026-09-22

## Authoritative sources
IFRS Foundation IAS 16 official page/supporting material; FRC FRS 102 Section 17 current edition; AASB 116 current compilation (annual periods beginning on/after 1 January 2023); FASB ASC 360 source family plus applicable US cost-specific guidance. Restricted standards text is not reproduced.

## IFRS / IAS 16
IAS 16 covers tangible items held for production/supply, rental or administration and expected to be used beyond one period. Recognition requires probable future economic benefits and reliably measurable cost. Initial cost includes purchase price net of discounts/rebates, directly attributable costs to bring the asset to necessary location/condition, and qualifying dismantling/removal/restoration estimates. Subsequent measurement can use cost or revaluation model by class when requirements are met.

Important current rule: proceeds from selling items produced while preparing PPE for intended use are not netted against asset cost under the 2020 amendment; sales proceeds and related costs go through profit or loss under applicable guidance.

## AASB / AASB 116
Core recognition/measurement is closely aligned to IAS 16. Current AASB compilation applies from 1 January 2023. Australian entity type/tier and any Aus paragraphs remain mandatory context; do not infer compliance solely from IFRS record.

## UK GAAP / FRS 102 Section 17
Section 17 is the primary PPE model. Current FRC materials retain a cost/revaluation architecture and include UK-specific scope/presentation details. The September 2024 edition is current; Periodic Review 2024 has principal effective date 1 January 2026. Version-route the reporting period and early-adoption status before final conclusion.

## US GAAP
US GAAP PPE accounting is distributed across ASC 360 and transaction/cost-specific topics rather than mirroring IAS 16 paragraph architecture. General practice capitalizes acquisition/construction costs necessary to ready the asset for intended use, then depreciates systematically; impairment is routed to ASC 360. Revaluation upward of ordinary PPE is generally not an IAS-16-style policy option. Full paragraph-level Codification support remains PARTIAL where public FASB access does not expose current body text; do not fabricate paragraph citations.

## Differences
- IFRS/AASB permit a revaluation model by class subject to requirements; ordinary US GAAP does not offer the same broad upward-revaluation policy.
- FRS 102 has its own Section 17 scope and UK legal/presentation environment; never label it identical to IAS 16.
- Detailed directly-attributable-cost conclusions can diverge, especially for interest, asset acquisitions, software, start-up/reorganization, environmental obligations and industry-specific costs. Route those facts to linked topics.

## Decision logic — eligible cost
CAPITALIZE when the cost creates/acquires the qualifying asset or is necessary to bring it to the location and condition for intended operation under the applicable framework. EXPENSE costs of abnormal waste, general administration not directly attributable, training, initial operating losses and costs incurred after the asset is capable of intended operation unless a separate recognition basis exists. ESCALATE mixed contracts and internally constructed assets for component/cost-pool analysis.

## Additions workpaper
Required fields: asset ID; entity; vendor/project; invoice/PO; description; asset class; location; acquisition date; available-for-use date; gross cost; cost categories; excluded expense; restoration obligation link; componentization; useful life; method; residual value; GL; cost center/dimensions; approver; evidence; policy threshold; framework conclusion.

## Journal pattern
At qualifying recognition: Dr PPE / Cr cash, AP or relevant liability. Restoration/decommissioning element may credit a provision under the applicable framework. Depreciation begins under the linked depreciation topic when the asset reaches the framework-specific ready/available-for-use point.

## Controls / audit / systems
Controls: capex authorization is not accounting recognition approval; invoice/project-cost validation; expense-v-capex review; threshold policy; available-for-use approval; component review; duplicate-asset detection; additions-to-GL reconciliation; project-to-fixed-asset transfer; asset master-data approval.

Audit evidence: invoice/contract, approval, proof of receipt/construction, project ledger, cost-allocation support, in-service evidence, physical existence where relevant, restoration estimate, policy and register/GL reconciliation.

Systems: preserve project/CIP ID to final asset IDs and source transactions. A recurring ERP/project/AP-to-fixed-asset reconciliation is a genuine TrackedFR candidate when cross-system and Excel-heavy; simple one-off capitalization is not.

## Scenarios / QA
1. Machine purchase + freight + installation + operator training: capitalize qualifying acquisition/freight/installation; training normally expense. PASS.
2. Factory trial production sold before intended use: do not net sale proceeds against PPE under current IAS 16/AASB logic. PASS.
3. Individually immaterial laptops below approved threshold: distinguish technical asset eligibility from materiality policy. PASS.
4. Major inspection/replacement: assess component recognition/derecognition rather than automatic repair expense. PASS.
5. Internally constructed asset with abnormal waste: exclude abnormal waste. PASS.
6. US entity asks for annual PPE upward revaluation: flag framework difference; do not apply IAS 16 election. PASS.
7. Asset not yet capable of intended operation at close: remain CIP/no ordinary depreciation; verify impairment and costs. PASS.
8. Asset physically installed but waiting for ceremonial launch/customer ramp: assess actual readiness, not management's preferred depreciation date. PASS.

Result: 8/8 routing scenarios PASS. US paragraph-level source depth remains PARTIAL; not a blocker to production-candidate architecture.
