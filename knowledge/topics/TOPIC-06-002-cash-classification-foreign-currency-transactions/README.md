# TOPIC-06-002 — Cash Classification & Presentation / Foreign Currency Transaction Accounting

Status: **REVIEWED / production-candidate**  
Capabilities: `CAO-06-004`, `CAO-06-005`  
Sensitivity: H  
Source check: 2026-09-23

## Objective
Enable the CAO to determine what is cash/cash equivalent, present it correctly, and account for transactions denominated in currencies other than an entity's functional currency from initial recognition through settlement/reporting date.

## Required facts
Framework/entity/period; functional and presentation currencies; bank/deposit/investment terms; maturity from acquisition; accessibility/restrictions; overdraft terms/cash-management practice; transaction currency; transaction and settlement dates; monetary/non-monetary nature; historical/spot/average rates and source; prepayments/advances; fair-value measurement dates; hedging relationships if any.

## PRINCIPLES
- Cash classification is based on contractual/economic characteristics and purpose, not account name.
- Foreign-currency accounting starts with **functional currency**. Transaction currency and presentation currency are separate concepts.
- A foreign-currency transaction is initially recorded using the applicable transaction-date rate (or a permitted reasonable approximation). At reporting date, monetary and non-monetary items follow different subsequent translation rules.
- FX differences must be traceable to the underlying monetary exposure, rate movement and settlement/remeasurement event; unexplained FX plugs are not acceptable.

## STANDARDS routing
### IFRS
IAS 7 governs cash/cash equivalents and IAS 21 governs foreign-currency transactions and foreign operations. IAS 7 describes cash as cash on hand/demand deposits and cash equivalents as short-term, highly liquid investments readily convertible to known amounts with insignificant value-change risk. IAS 21 defines functional currency as the currency of the primary economic environment. For production work use current IAS 21 transaction-date, reporting-date, non-monetary and exchange-difference requirements, plus IAS 7/IFRS 18 presentation and IFRS 7 disclosures where relevant.

### AASB
AASB 107 and AASB 121 are IFRS-aligned core routes. Current AASB 107 material confirms the cash-equivalent architecture and foreign-currency cash-flow translation principles; AASB 121 governs transaction accounting. Independently verify current Australian compilation, reporting tier and period.

### US GAAP
Route foreign currency to ASC 830 and cash-flow/presentation to ASC 230 plus applicable presentation Topics. US terminology and remeasurement/translation mechanics are not assumed identical to IAS 21. Determine functional currency under current ASC 830, then apply transaction gains/losses and settlement rules. Full paragraph-level status remains PARTIAL without authorised current Codification access.

### UK GAAP
Route to FRS 102 Sections 7 and 30 and relevant financial-instrument/presentation sections using the period-effective edition. Maintain 1 Jan 2026 Periodic Review gate and 1 Jan 2027 adapted-format presentation gate where relevant. Do not assume IAS 21 paragraph mechanics apply unchanged.

## CAO decision workflow
1. Resolve framework/entity/period and functional currency.
2. Classify cash, demand deposits, short-term investments, overdrafts and restrictions.
3. For each foreign-currency transaction, identify transaction currency, recognition date and item type.
4. Record initial amount using framework-permitted transaction-date rate/approximation and controlled rate source.
5. At reporting date classify item as monetary/non-monetary and determine required rate basis.
6. Calculate remeasurement/translation difference and determine P&L/OCI/asset treatment under applicable topic.
7. On settlement, clear monetary item and isolate realised/settlement FX.
8. Reconcile FX subledger/exposure schedule to GL and cash-flow/FS presentation.
9. Document rate source, approximations, judgments, exceptions and disclosures.

## Calculation architecture
For a monetary item: functional-currency carrying amount at each required measurement date = foreign-currency units × applicable rate. FX movement is the change attributable to rate movement after considering additions/settlements and any framework-specific treatment. Preserve rate convention (FC per functional or functional per FC) and never mix quote direction. For average-rate approximations, validate that rates did not fluctuate so materially that an average ceases to approximate actual transaction-date rates.

## Controls / audit
Approved FX-rate source and quote convention; interface-rate completeness; transaction-date/cut-off control; monetary/non-monetary mapping; bank/AR/AP/subledger-to-GL reconciliation; review of large FX gains/losses; settlement clearing; restricted-cash classification review; disclosure tie-out; functional-currency review trigger after business-model changes.

## Systems / data
Store transaction currency, functional currency, original FC amount, recognition rate/date, carrying FC amount, closing/settlement rate, functional amount, FX movement, source and rate type. ERP configuration must not overwrite original transaction currency/rate evidence.

## TrackedFR applicability
Useful for recurring reconciliation of ERP transactions, bank/settlement data and controlled FX-rate datasets across systems. Not recommended for a one-off currency calculation.

## Scenario tests
1. Three-month treasury deposit acquired to meet near-term cash commitments → test cash-equivalent criteria rather than label.
2. Six-month investment with same liquidity → do not assume cash equivalent solely because liquid.
3. Foreign supplier invoice unpaid at period end → initial recognition then monetary-item remeasurement and settlement bridge.
4. Foreign-currency prepayment → identify non-monetary nature and route subsequent accounting correctly.
5. Bank overdraft integral to cash management under IFRS/AASB → test IAS 7/AASB 107 conditions; do not generalise to US GAAP.
6. Average monthly FX rate during volatile month → challenge whether approximation is acceptable.
7. UK period beginning 2027 → route current FRS 102 plus adapted-format presentation amendments.
8. Large unexplained FX account → reconcile exposure-by-currency and rate bridge rather than plug.

Expected routing: **8/8 PASS**.

## Completion assessment
Principles PASS; framework routing PASS subject to US paragraph-depth limitation; decision/calculation logic PASS; documentation/controls/audit/systems PASS; capability integration PASS; scenarios 8/8 PASS. **REVIEWED / production-candidate.**

## Authoritative sources
IFRS Foundation: IAS 7 and IAS 21; FASB Codification ASC 230/830 and issued ASUs; FRC current FRS 102 Sections 7/30; AASB current AASB 107/AASB 121. Rights: REFERENCE_ONLY.