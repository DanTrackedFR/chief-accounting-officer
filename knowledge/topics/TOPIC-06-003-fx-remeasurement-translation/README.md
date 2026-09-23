# TOPIC-06-003 — Foreign Currency Remeasurement / Foreign Currency Translation

Status: **REVIEWED / production-candidate**  
Primary capabilities: **CAO-06-006, CAO-06-007**  
Sensitivity: **H**  
Source check: **2026-09-23**

## Objective
Enable the CAO to distinguish transaction remeasurement into functional currency from translation of a functional-currency set of financial statements into a presentation/reporting currency, calculate the resulting exchange effects, and reconcile them through entity and consolidation reporting.

## Required inputs
Framework, entity/group, reporting period; functional and presentation/reporting currencies; source-ledger currencies; opening monetary/non-monetary balances; transaction dates and historical rates; closing/average/actual rates; equity history; foreign-operation acquisition/disposal history; intercompany monetary items and net-investment designation; hyperinflation status; exchangeability restrictions; CTA/FCTR opening balance; consolidation mapping.

## Core distinction
**Remeasurement** gets the books to the entity's functional currency. Monetary foreign-currency items are generally updated using the required closing/current rate and exchange effects usually enter earnings unless a specific exception applies. Non-monetary items require their measurement-basis/historical-rate analysis.

**Translation** takes a functional-currency financial statement set into a different presentation/reporting currency for group/reporting purposes. The translation difference is not the same thing as transaction FX and commonly accumulates in OCI/equity under IFRS/AASB and US GAAP translation models.

Never combine transaction FX, remeasurement FX and translation adjustment into a single unexplained “FX” account.

## IFRS — IAS 21
- Determine functional currency before remeasurement/translation.
- Foreign-currency transactions are initially recorded using the spot rate at transaction date (permitted practical approximations only when appropriate).
- At reporting date, monetary items are translated using closing rate; historical-cost non-monetary items retain transaction-date rate; fair-value non-monetary items use the rate when fair value was measured.
- Exchange differences on monetary items generally enter P&L subject to IAS 21 exceptions, including qualifying net-investment monetary items in consolidated financial statements.
- For a non-hyperinflationary functional currency translated to another presentation currency, IAS 21.39 uses closing rate for assets/liabilities, transaction-date rates for income/expenses and OCI for resulting translation differences.
- Lack of Exchangeability amendments apply for annual periods beginning on/after **1 January 2025** and require a consistent exchangeability assessment, estimated spot rate when not exchangeable and disclosures.
- November 2025 IAS 21 amendments on translation to a hyperinflationary presentation currency are effective annual periods beginning on/after **1 January 2027** (early application permitted). Do not apply them prematurely without an effective-period check.
- March 2026 IFRIC material confirms that an intragroup loan that is a foreign-currency monetary item and is not part of net investment can create a P&L exchange difference that is not eliminated merely because the underlying intragroup balance is eliminated on consolidation.

## AASB — AASB 121
Core architecture is IFRS-aligned. AASB 2023-5 Lack of Exchangeability applies annual periods beginning on/after **1 January 2025**. AASB 2025-4 addresses translation to a hyperinflationary presentation currency and applies annual periods beginning on/after **1 January 2027**, with early application permitted. Verify the current Australian compilation and reporting tier/entity overlays rather than relying only on IFRS.

## UK GAAP — FRS 102 Section 30
Use the reporting-period-effective Section 30. Foreign-currency transaction, functional-currency and foreign-operation translation mechanics must be taken from current FRS 102, not copied from IAS 21. The Periodic Review 2024 version is generally effective for periods beginning on/after **1 January 2026**. FRC's current differences material notes that IFRS-for-SMEs exchangeability paragraphs were not incorporated into FRS 102 and that Section 30 has company-law-specific net-investment and hyperinflationary translation provisions. Effective-period routing is mandatory.

## US GAAP — ASC 830
ASC 830 is the authoritative route for functional currency, foreign-currency transactions, remeasurement and translation. Remeasurement of books into functional currency and translation into reporting currency are distinct steps. Highly inflationary accounting has a US-specific model; do not import IAS 29/IAS 21 mechanics. Public FASB material does not expose all current Codification paragraphs, so paragraph-level conclusions remain **PARTIAL** until verified against authorized current Codification access.

## CAO workflow
1. Resolve entity, framework, reporting period and functional currency; stop if functional currency is unresolved and material.
2. Determine whether task is transaction remeasurement, foreign-operation translation, or both sequentially.
3. Classify balance-sheet items as monetary/non-monetary and identify measurement basis.
4. Build approved rate table with source, rate type, date and currency pair; test exchangeability where relevant.
5. Remeasure foreign-currency monetary and applicable non-monetary items into functional currency.
6. Separate realized/unrealized transaction FX as required by reporting design without changing GAAP/IFRS recognition.
7. Translate functional-currency FS to presentation/reporting currency using framework-specific rates.
8. Roll forward CTA/FCTR and identify OCI/P&L/equity destinations.
9. Analyze intercompany balances: elimination does not automatically eliminate FX consequences; assess net-investment treatment separately.
10. Address acquisitions/disposals/partial disposals and reclassification of accumulated translation amounts through the relevant group-accounting topic.
11. Reconcile local ledger → functional-currency TB → translated reporting package → consolidation → CTA/FCTR.
12. Document rate sources, exceptions, judgments and disclosure impacts; promote durable currency policies to Company Accounting Memory.

## Calculation architecture
Maintain three auditable layers: (A) source-currency ledger; (B) functional-currency remeasurement with rate and FX-difference columns; (C) presentation-currency translation with balance-sheet, P&L/equity historical-rate logic and CTA/FCTR bridge. CTA/FCTR rollforward should explain opening reserve + current translation movement + net-investment FX/hedge effects where applicable + acquisition/disposal/reclassification effects + other supported movements = closing reserve.

## Controls / audit / systems
Approved independent FX-rate source; rate-table access/change control; currency master-data governance; monetary/non-monetary mapping review; functional-currency approval; local-to-group TB reconciliation; CTA/FCTR rollforward; intercompany FX exception review; exchangeability/hyperinflation trigger; disposal/reclassification control; disclosure tie-out. Audit evidence includes source rates, ledger extracts, historical-rate support, translation calculation, reserve rollforward and significant judgment papers.

## TrackedFR applicability
A recurring multi-entity close that joins ERP local ledgers, rate tables, consolidation data and Excel translation/CTA schedules is a genuine TrackedFR candidate. A one-off manual currency conversion is not.

## Scenario tests
1. USD receivable in EUR-functional entity → monetary remeasurement to EUR with transaction FX.
2. Historical-cost PPE denominated in foreign currency → do not closing-rate remeasure historical cost merely because exchange rate moved.
3. EUR-functional subsidiary translated to USD group reporting → translation layer and CTA/OCI route.
4. Intragroup loan not part of net investment → eliminate balance on consolidation but do not automatically eliminate transaction FX consequence under IAS 21.
5. Currency lacks exchangeability in 2026 IFRS reporting → apply 2025-effective exchangeability model and evidence estimated spot rate.
6. UK entity period beginning 2026 → current FRS 102 Section 30 route, not IAS 21 copy.
7. US highly inflationary foreign entity → ASC 830-specific route, not IAS 29.
8. Presentation currency becomes hyperinflationary for IFRS period beginning 2027 → invoke 2025-issued IAS 21 amendment/effective-date gate.
9. Foreign operation disposed → route accumulated translation reserve treatment to group-accounting disposal topic.
10. Translation workbook does not reconcile to functional-currency TB → stop final conclusion and resolve data completeness.

Expected routing: **10/10 PASS**.

## Source register / rights
Primary references checked 2026-09-23: IFRS Foundation IAS 21 standard page, Lack of Exchangeability amendments and 2025 Translation to a Hyperinflationary Presentation Currency amendment; IFRIC March 2026 intragroup-loan discussion; AASB 121/AASB 2023-5/AASB 2025-4; FRC FRS 102 Section 30/current differences material; FASB ASC 830 and official amendment material. Authoritative text is REFERENCE_ONLY; this record is independently authored.

## Completion assessment
Principles: PASS. IFRS/AASB current effective-date routing: PASS. UK routing: PASS with primary-version verification required for paragraph-level APPROVED status. US routing: PASS with recorded Codification-depth limitation. Differences: PASS. CAO logic/calculation architecture: PASS. Controls/audit/systems: PASS. Capability integration: PASS. Scenarios: 10/10 PASS. **Factory status: REVIEWED / production-candidate.**