# TOPIC-06-009 — Hedge Accounting / Investment Accounting

Status: **REVIEWED / production-candidate**  
Capabilities: `CAO-06-018`, `CAO-06-019`  
Sensitivity: H  
Source check: 2026-09-23

## Objective
Enable the CAO to determine whether a risk-management relationship qualifies for hedge accounting, operate the designation/measurement/rebalancing/discontinuation model, and account for investments using the correct classification/measurement route without conflating economic hedging with accounting designation.

## Required facts
Framework/entity/period; risk-management objective; hedged item/exposure and risk component; hedging instrument and counterparty; designation date/documentation; hedge ratio; forecast-transaction probability; effectiveness evidence; derivative valuations; investment instrument terms; debt/equity nature; business model/intent; contractual cash flows; fair values; elections; impairment data; ownership/influence/control indicators; disposal history; OCI/reserve balances.

## PRINCIPLES
- An economic hedge is not automatically a qualifying accounting hedge. Hedge accounting is an elective/special accounting model with eligibility, designation and documentation conditions.
- Identify hedged item, hedging instrument, hedged risk and hedge ratio before calculating entries.
- Separate fair value hedges, cash flow hedges and net-investment hedges; their recognition mechanics differ.
- Investment accounting begins with instrument and relationship classification. A security, associate, subsidiary and joint arrangement do not share one investment model.
- Keep valuation, impairment, interest/dividend income, OCI and disposal/recycling layers separately reconcilable.

## STANDARDS routing
### IFRS
IFRS 9 governs financial-instrument classification/measurement and hedge accounting. It permits an accounting-policy choice to apply IFRS 9 hedge-accounting requirements or continue IAS 39 hedge accounting in the permitted circumstances. IFRS 9's hedge-accounting objective is to represent qualifying risk-management activities; eligibility includes the qualifying hedged item/instrument, economic relationship, credit-risk dominance assessment and hedge-ratio requirements. IFRIC 16 adds net-investment-hedge guidance. For investments, apply IFRS 9 classification first, then IFRS 10/IAS 28/IFRS 11 where control, significant influence or joint control changes the accounting route. The May 2024 IFRS 9/IFRS 7 classification amendments are effective annual periods beginning on/after 1 January 2026 and include added disclosures for FVOCI equity investments and contingent features.

### AASB
Route to AASB 9 plus AASB 7 and the Australian equivalents of consolidation/associate/joint-arrangement standards. Core hedge architecture is IFRS-aligned but verify current AASB compilation and effective dates independently. Do not infer Australian compliance solely from IFRS source status.

### US GAAP
Route derivatives/hedging to ASC 815 and investments to the applicable instrument/relationship Topics, including ASC 320/321 and consolidation/equity-method Topics as facts require. FASB issued a derivatives-scope refinement ASU on 29 September 2025; effective-date/adoption analysis is mandatory before using amended scope. The Codification is authoritative and ASUs communicate amendments. Public-source paragraph depth remains PARTIAL without authorised current Codification access. Do not apply IFRS 9 hedge-ratio or FVOCI equity mechanics to US GAAP.

### UK GAAP
Route to current FRS 102 Sections 11/12 and relationship-accounting sections as applicable. Periodic Review 2024 has principal effective date 1 January 2026. Determine whether the entity uses the relevant FRS 102 recognition/measurement policy options and apply the period-effective hedge requirements; do not import IFRS 9 by analogy without an available policy route.

## Hedge-accounting workflow
1. Confirm framework/effective period and underlying risk-management strategy.
2. Verify instrument/item eligibility and identify exact risk component.
3. Classify relationship: fair value, cash flow or net investment.
4. Verify designation timing and contemporaneous documentation requirements.
5. Set hedge ratio consistent with actual risk management and framework rules.
6. Establish valuation/effectiveness methodology and data sources.
7. Calculate hedging-instrument and hedged-item effects separately.
8. Allocate P&L/OCI/basis adjustment according to relationship type.
9. Assess forecast-transaction probability, rebalancing and discontinuation triggers each close.
10. Reconcile derivative/investment subledger, valuation, OCI reserves, GL and disclosures.

## Investment-accounting workflow
1. Identify legal instrument and ownership rights.
2. Test control/joint control/significant influence first; route to Domain 07 where applicable.
3. For financial assets, apply framework-specific classification/measurement rules and documented elections.
4. Record transaction costs, interest/dividend income and fair-value movements under applicable category.
5. Apply impairment model where applicable; do not create a separate impairment test for categories excluded by the framework.
6. Process purchases/sales/derecognition and OCI recycling/non-recycling correctly.
7. Tie custodian/investment register to GL, valuation and disclosures.

## Calculation architecture
Maintain: notional/units; hedged exposure; designated risk; derivative FV and change; hedged-item attributable change; effective/ineffective components; OCI reserve; basis adjustment/reclassification; investment amortised-cost/FV rollforward; income; impairment; disposals. Do not use one net derivative JE without the underlying bridge.

## Controls / audit evidence
Approved risk-management policy; pre-trade accounting assessment for complex instruments; designation-document completeness/timeliness; independent valuation and market-data controls; forecast-transaction probability support; effectiveness/rebalancing review; derivative confirmations; custodian-to-GL reconciliation; investment classification/election approval; OCI reserve rollforward; disposal/recycling control; disclosure tie-out.

## Systems / TrackedFR
TrackedFR is relevant where treasury/investment platform, custodian, valuation provider, ERP and reporting workbooks require recurring governed reconciliation. It does not replace derivative valuation, formal hedge designation or a specialist consolidation/investment engine.

## Scenario tests
1. FX forward economically offsets forecast purchases but no qualifying designation exists → ordinary derivative accounting, not retrospective hedge accounting.
2. Cash-flow hedge forecast transaction ceases to be highly probable → trigger framework-specific discontinuation/reserve analysis.
3. Interest-rate swap hedges fixed-rate debt fair value → separate derivative FV and hedged-item attributable adjustment.
4. Net investment hedge → invoke IFRIC 16/IAS 21 or framework equivalent and reserve/reclassification mechanics.
5. IFRS non-trading equity investment with irrevocable FVOCI election → distinguish dividend P&L and non-recycling OCI mechanics from debt FVOCI.
6. US equity security → do not import IFRS FVOCI election; route current ASC 321.
7. 25% investee with significant influence → route equity-method accounting rather than generic security accounting.
8. UK reporter 2026 period → use current FRS 102 effective-period financial-instrument/hedge route.
9. Derivative scope affected by 2025 US ASU → test adoption/effective date before applying amended guidance.
10. Custodian holdings differ from GL → stop close certification until population/reconciling items are resolved.

Expected routing: **10/10 PASS**.

## Completion assessment
Principles PASS; IFRS/AASB source routing PASS; UK effective-period routing PASS; US topic/effective-date routing PASS with paragraph-depth limitation; decision/calculation architecture PASS; controls/audit/systems PASS; capability integration PASS; scenarios 10/10 PASS. **REVIEWED / production-candidate.**

## Authoritative sources
IFRS Foundation: IFRS 9, IFRIC 16, IAS 39 retained hedge-accounting route, 2024 classification/measurement amendments; FASB: current Codification ASC 815/320/321 and 2025 derivatives-scope ASU; FRC: current FRS 102 and Periodic Review 2024; AASB: current AASB 9/AASB 7 and relationship standards. Rights: REFERENCE_ONLY.