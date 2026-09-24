# TOPIC-06-009 — Hedge Accounting / Investment Accounting

Status: **REVIEWED / production-candidate**  
Primary capabilities: **CAO-06-018, CAO-06-019**  
Sensitivity: **H**  
Source check: **2026-09-23**

## Objective
Enable the CAO to account for investment portfolios under the applicable classification model and, where an entity elects hedge accounting, determine eligibility, designation, effectiveness/rebalancing, P&L/OCI treatment, discontinuation and disclosure with an auditable link to the entity's documented risk-management activity.

## Mandatory intake
Framework/period/entity; investment agreements and custody statements; instrument terms; classification/election history; acquisition cost and fair values; dividends/interest/disposals; impairment data; derivative confirmations; hedging instrument and hedged item; risk being hedged; risk-management objective; designation date; hedge ratio; forecast-transaction probability support; effectiveness evidence; rebalancing/discontinuation events; group versus separate-entity perspective.

## Core principles
- Investment accounting begins with TOPIC-06-007 classification and measurement and TOPIC-06-010 impairment; “investment” is not a measurement category.
- A derivative used economically to reduce risk does not automatically qualify for hedge accounting.
- Hedge accounting is elective/special accounting. Eligibility and contemporaneous documentation are gates, not close-period cleanup steps.
- Keep fair-value hedge, cash-flow hedge and net-investment hedge mechanics separate.
- The accounting designation must reflect the entity's actual risk-management objective; do not manufacture a designation solely to smooth earnings.

## IFRS / AASB
IFRS 9/AASB 9 Chapter 6 aims to represent the effect of risk-management activities in the financial statements. A qualifying relationship requires eligible hedging instruments and hedged items, formal designation/documentation at inception and satisfaction of the framework's qualifying/effectiveness criteria. Risk components can qualify when separately identifiable and reliably measurable. Fair-value, cash-flow and net-investment hedges have different P&L/OCI mechanics.

For group reporting, only exposures involving an external party generally qualify as hedged items, subject to specified foreign-currency exceptions for intragroup monetary items/forecast transactions. AASB 9 also preserves the policy choice on initial application to continue IAS 39/AASB 139 hedge-accounting requirements, so Company Context must retain the entity's elected hedge-accounting model.

**Current-status gate:** IASB's 2026 Post-implementation Review of IFRS 9 Hedge Accounting and the proposed Risk Mitigation Accounting model are active standard-setting/review activity. They do **not** replace current IFRS 9 hedge accounting until final amendments become effective. Do not turn proposals or tentative decisions into current accounting.

Investment accounting under IFRS/AASB follows the classification model in TOPIC-06-007: debt instruments may route to amortised cost, FVOCI or FVTPL based on the applicable tests; equity investments are generally FVPL subject to the qualifying irrevocable OCI presentation election. Apply ECL to in-scope debt assets through TOPIC-06-010.

## US GAAP
Route investment accounting by instrument type: ASC 320 debt securities, ASC 321 equity securities, ASC 323 equity method, ASC 325 and other specialized routes as applicable; credit losses route through ASC 326. Hedge accounting routes through ASC 815 and differs materially from IFRS 9 in designation, eligible components, effectiveness mechanics, elections and presentation. Do not import IFRS hedge criteria or investment categories.

FASB issued derivatives-scope refinements in September 2025 affecting Topic 815; effective-date applicability must be checked for the reporting entity. The Codification remains the authoritative source. Public official materials do not expose every current paragraph body, so paragraph-level US conclusions remain **PARTIAL** unless directly verified from authorized current Codification access.

## UK GAAP
Apply the period-effective FRS 102. Investment classification/measurement routes through Sections 11/12 and other specific sections (for example associates/JVs where relevant), not IFRS 9 categories. Hedge accounting under FRS 102 Section 12 must be assessed using its own qualifying relationships, documentation and accounting requirements. Periodic Review 2024 amendments are generally effective from 1 January 2026; do not assume IFRS 9 hedge mechanics where FRS 102 differs.

## CAO hedge workflow
1. Confirm actual risk-management strategy and exposure before accounting designation.
2. Identify eligible hedging instrument, hedged item/risk component and reporting-entity perspective.
3. Select applicable hedge type under the framework.
4. Verify designation timing and required documentation.
5. Establish hedge ratio and effectiveness/qualifying evidence under the framework.
6. Calculate instrument fair-value change and hedged-item/risk-component change.
7. Route fair-value hedge effects, cash-flow hedge reserve/OCI and net-investment effects correctly.
8. Assess cost-of-hedging components, excluded components and basis adjustments where applicable.
9. Reassess effectiveness/qualifying criteria and rebalance where the framework requires/allows.
10. On discontinuation, determine treatment of accumulated OCI/basis adjustments and forecast transactions.
11. Reconcile derivative/investment confirmations, valuation, GL, OCI/equity and disclosures.
12. Preserve designation paper, effectiveness evidence, calculations, entries and reviewer sign-off.

## Investment workflow
Inventory investments from custody/bank/legal records; classify under TOPIC-06-007; determine interest/dividend income and transaction-cost treatment; obtain independent fair values; invoke impairment; process acquisitions/disposals; reconcile realized/unrealized gains and OCI; assess equity-method/consolidation dependencies; tie investment register to GL and disclosures.

## Controls / evidence
Approved investment register; independent custodian/broker confirmations; new-instrument technical review; fair-value price validation; impairment linkage; approved hedge designation before/at required inception point; forecast-transaction support; independent effectiveness/model review; derivative confirmation reconciliation; OCI reserve rollforward; discontinuation trigger; disclosure tie-out; quarterly completeness scan across treasury/legal/bank sources.

## Scenario tests
1. FX forward economically offsets forecast purchases but no qualifying designation documentation -> derivative accounting without retroactive hedge accounting.
2. IFRS cash-flow hedge of highly probable forecast purchase -> test eligibility/effectiveness and OCI mechanics.
3. IFRS fair-value hedge of eligible fixed-rate exposure -> route hedging-instrument and hedged-item attributable changes under fair-value-hedge mechanics.
4. Net investment hedge -> confirm qualifying foreign operation/net investment and group perspective.
5. Intragroup forecast transaction in consolidation -> do not assume eligibility; apply specific FX exception tests.
6. Entity has retained IAS 39/AASB 139 hedge policy -> do not silently switch to IFRS/AASB 9 Chapter 6.
7. US hedge -> apply ASC 815, not IFRS 9 effectiveness/designation rules.
8. UK FRS 102 entity -> apply Section 12, not IFRS 9 by analogy.
9. Equity investment sold -> apply its framework-specific classification/recycling rules; do not assume all OCI recycles.
10. Hedge forecast transaction no longer expected -> trigger discontinuation and accumulated-balance assessment.

Expected routing: **10/10 PASS**.

## Source register / rights
Official sources checked 2026-09-23: IFRS Foundation IFRS 9 hedge-accounting/IFRIC materials and 2026 PIR/Risk Mitigation Accounting project status; AASB 9 Chapter 6 and AASB 139 transition option; FRC FRS 102 current standard/Factsheet 4 materials; FASB Topic 815 public standards/2025 derivatives-scope update. Authoritative standards text remains REFERENCE_ONLY.

## Completion assessment
Framework routing: PASS. IFRS/AASB hedge architecture/current-project separation: PASS. UK routing: PASS. US routing: PASS with Codification-depth limitation. Investment integration: PASS. Controls/documentation: PASS. Scenarios: 10/10 PASS. **Factory status: REVIEWED / production-candidate.**