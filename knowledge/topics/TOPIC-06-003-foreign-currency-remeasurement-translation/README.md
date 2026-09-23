# TOPIC-06-003 — Foreign Currency Remeasurement / Foreign Currency Translation

Status: **REVIEWED / production-candidate**  
Capabilities: `CAO-06-006`, `CAO-06-007`  
Sensitivity: H  
Source check: 2026-09-23

## Objective
Enable the CAO to distinguish transaction remeasurement into functional currency from translation of a foreign operation into presentation currency, calculate both without double counting, reconcile currency translation reserves, and route hyperinflation/net-investment issues correctly.

## Required facts
Framework/entity/group/period; functional currency per entity; presentation currency; ledger currency; foreign-operation ownership/NCI; trial balances by entity/currency; opening translated balances; transaction/average/closing rates and source; equity historical rates; acquisitions/disposals; intercompany monetary items and whether part of net investment; hyperinflation/exchangeability conditions; prior CTA/FCTR balances.

## PRINCIPLES
- **Remeasurement and translation are different layers.** First get each entity's books into its functional currency; then translate a foreign operation's functional-currency financial statements into group presentation currency.
- Monetary-item remeasurement differences and foreign-operation translation differences generally have different presentation outcomes. Never net them without a documented bridge.
- Functional currency is an economic conclusion, not a management preference.
- Average rates are practical approximations, not automatic entitlements; challenge them during significant volatility.
- Translation reserve must roll forward from identifiable drivers and ownership changes, not a balancing plug.

## STANDARDS routing
### IFRS
IAS 21 is the core standard. Current official material requires a non-hyperinflationary foreign operation translated to another presentation currency to use closing rates for assets/liabilities and transaction-date rates for income/expenses, with resulting translation differences in OCI; average rates may approximate transaction-date rates when appropriate but are unsuitable during significant fluctuation. Net-investment monetary items, disposals and hyperinflation invoke specific IAS 21/IAS 29 rules. IFRS 18 now affects profit-or-loss classification of certain FX differences; the April 2026 IFRIC agenda decision on intragroup monetary balances is a current implementation reference, not a reason to alter IAS 21 recognition mechanics.

### AASB
AASB 121 is IFRS-aligned core. Current AASB text explicitly distinguishes closing-rate monetary-item remeasurement, historical-rate non-monetary items, fair-value-date rates and foreign-operation translation into OCI. Use current compilation and AASB 129 for hyperinflation where relevant.

### US GAAP
Route to ASC 830. Establish functional currency and distinguish remeasurement from translation under US GAAP; determine transaction gains/losses, CTA, highly inflationary economy rules, intercompany items and disposal/reclassification using current Codification. Do not copy IAS 21 mechanics or terminology where US requirements differ. Paragraph-level status remains PARTIAL without authorised Codification access.

### UK GAAP
Route to current FRS 102 Section 30 Foreign Currency Translation, plus consolidation/presentation sections and period-effective amendments. Maintain the 1 Jan 2026 Periodic Review gate and later presentation amendments as relevant. Verify Section 30 directly rather than infer from IAS 21.

## CAO workflow
1. Confirm framework, group structure, reporting period and presentation currency.
2. Document functional-currency conclusion for every material entity/branch.
3. Reperform entity-level remeasurement into functional currency where ledger currency differs or transactions are foreign currency.
4. Identify foreign operations included in consolidated/group reporting.
5. Translate assets/liabilities, income/expenses and equity using framework-required rates.
6. Calculate translation difference independently and allocate NCI share where applicable.
7. Identify intercompany monetary balances; assess net-investment designation/substance and consolidation treatment.
8. Assess hyperinflation/exchangeability before ordinary translation if indicators exist.
9. Process acquisitions/disposals/ownership changes and reserve recycling/reclassification under applicable framework.
10. Reconcile opening CTA/FCTR + current translation + ownership/disposal/reclassification = closing reserve.
11. Tie translated entity TBs to consolidation system, GL/equity and disclosures.

## Calculation architecture
Maintain three bridges separately: (A) transaction/monetary-item remeasurement P&L; (B) foreign-operation translation OCI/reserve; (C) net-investment/hedge effects where applicable. For a standard non-hyperinflationary IFRS/AASB translation, assets/liabilities use closing rate and income/expenses use transaction-date rates or valid approximations; translation difference is derived from those rate bases and opening net assets. Preserve historical equity-rate layers.

## Controls / audit evidence
Annual/event-driven functional-currency assessment; approved rate source and quote convention; average-rate reasonableness; closing-rate validation; entity TB completeness; CTA rollforward; NCI allocation; intercompany/net-investment review; acquisition/disposal trigger; hyperinflation/exchangeability watch; consolidation-system configuration; disclosure tie-out.

## Systems / TrackedFR
Useful where entity TBs, rate tables, consolidation outputs and GL reserve accounts are repeatedly reconciled across systems. TrackedFR is appropriate for governed data joins, rate validation and exception-based CTA reconciliation; not for replacing a specialist consolidation engine or making unsupported functional-currency judgments.

## Scenario tests
1. EUR subsidiary functional EUR, group USD → translate foreign operation after local EUR books are correct.
2. Subsidiary ledger maintained in USD but functional EUR → remeasure to EUR first, then translate to group presentation currency if needed.
3. Monthly average used during extreme FX volatility → reject/adjust if it no longer approximates transaction-date rates.
4. Intercompany loan denominated in parent's currency → determine entity-level FX and whether it forms part of net investment; consolidation elimination does not automatically eliminate every FX effect.
5. 80%-owned foreign operation → allocate applicable cumulative translation amount to NCI under framework.
6. Disposal of foreign operation → route reserve reclassification/recycling requirements before posting.
7. Hyperinflationary functional currency → invoke hyperinflation topic/rules before ordinary translation.
8. Translation reserve is a plug to make consolidation balance → fail control; rebuild rate/entity/equity bridge.

Expected routing: **8/8 PASS**.

## Completion assessment
Principles PASS; IFRS/AASB current-source routing PASS; UK routing PASS; US topic routing PASS with paragraph-depth limitation; calculations/reconciliation PASS; controls/audit/systems PASS; capability integration PASS; scenarios 8/8 PASS. **REVIEWED / production-candidate.**

## Authoritative sources
IFRS Foundation IAS 21 and IFRIC implementation/agenda material; FASB ASC 830 via current Codification; FRC current FRS 102 Section 30; AASB current AASB 121. Rights: REFERENCE_ONLY.