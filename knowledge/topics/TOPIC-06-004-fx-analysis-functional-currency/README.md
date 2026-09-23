# TOPIC-06-004 — FX Gain/Loss Analysis / Functional Currency Assessment

Status: **REVIEWED / production-candidate**  
Primary capabilities: **CAO-06-008, CAO-06-009**  
Sensitivity: **H**  
Source check: **2026-09-23**

## Objective
Enable the CAO to determine and document functional currency, identify genuine changes in underlying economics, explain FX gains/losses by driver and distinguish transaction/remeasurement FX from translation reserves and hedging effects.

## Required facts
Entity and reporting framework/period; revenue pricing/settlement currencies; competitive/regulatory price environment; labour/material/other cost currencies; financing currencies; currencies in which operating receipts are retained; autonomy of foreign operation; intragroup activity and remittance patterns; debt-service currency; historical functional-currency conclusions; business-model changes; FX GL detail and exposures; intercompany/net-investment items; hedges; rate sources.

## Functional-currency principle
Functional currency is an **economic conclusion**, not a management election and not automatically local currency, parent currency, invoicing currency or presentation currency. Once determined, change it only when underlying transactions, events and conditions change. A desire to reduce FX volatility is not evidence for changing functional currency.

## IFRS — IAS 21
IAS 21 defines functional currency as the currency of the primary economic environment in which the entity operates. Primary indicators focus on currencies influencing sales prices and labour/material/other costs. Financing currency and the currency in which operating receipts are retained provide supporting evidence; foreign operations have additional autonomy, intragroup-activity, remittance and debt-service indicators. When indicators are mixed, judgment is required and primary indicators receive priority. A change is prospective from the date underlying economics change. Lack-of-exchangeability requirements are effective from 1 January 2025; hyperinflation overlays must be assessed separately.

## AASB — AASB 121
AASB 121 paras 9–14 provide the IFRS-aligned functional-currency architecture and expressly prioritize primary indicators when evidence is mixed. Current compilation includes the 1 January 2025 Lack of Exchangeability amendments. Australian entities must retain current-compilation and entity/tier checks.

## UK GAAP — FRS 102 Section 30
Determine functional currency under the reporting-period-effective Section 30. Current FRC text confirms changes are prospective and only when underlying transactions/events/conditions change. The Periodic Review 2024 version is generally effective for periods beginning on/after 1 January 2026. Do not assume all IAS 21 exchangeability requirements were copied into FRS 102; FRC differences material specifically notes omissions.

## US GAAP — ASC 830
Use ASC 830's functional-currency framework, including highly-inflationary-economy rules and remeasurement/translation consequences. Do not force IAS 21 indicator weighting into US conclusions without current ASC support. Public Codification depth remains limited, so detailed paragraph-level US conclusions are **PARTIAL** pending authorized current Codification verification.

## CAO functional-currency workflow
1. Define the entity/foreign operation being assessed; functional currency is entity-specific.
2. Build an evidence matrix for revenue pricing/settlement and cost drivers over a representative period.
3. Assess competitive/regulatory environment and whether pricing is genuinely linked to a currency rather than merely denominated in it.
4. Assess financing/retained-receipt evidence.
5. For a foreign operation, assess autonomy, intragroup transaction proportion, cash-flow remittance and independent debt-service ability.
6. Weight indicators under the applicable framework; document mixed evidence and counterarguments.
7. Compare with prior conclusion and identify whether economics changed or only rates/management preference changed.
8. If change is justified, establish exact change date and prospective accounting; update systems/master data and historical-rate controls.
9. Document conclusion, sensitivity and disclosure implications.

## FX gain/loss analysis
Build a driver bridge rather than reporting a single FX number. At minimum separate: trade receivables/payables; cash; debt; intercompany monetary balances; accruals/other monetary items; realized settlement FX; period-end remeasurement; net-investment items; hedge accounting effects; consolidation translation/CTA/FCTR; manual FX journals; rate-source/mapping differences. Analyze by currency pair, entity, account and exposure size.

Useful diagnostic: approximate exposure-driven FX = average/open foreign-currency monetary exposure × relevant rate movement, then reconcile to transaction timing, settlements, new activity, historical-rate/non-monetary items and system mechanics. This is an analytical control, not a substitute for transaction-level accounting.

## Controls / documentation
Annual and event-driven functional-currency reassessment; approval of significant judgments; source evidence for primary indicators; rate-source governance; FX-account mapping; monthly FX bridge; intercompany/net-investment designation control; manual-JE review; functional-currency master-data change control; disclosure tie-out. Keep a functional-currency memo with evidence, weighting, contrary indicators, conclusion, effective date and reviewer.

## TrackedFR applicability
A recurring FX bridge joining ERP balances, intercompany data, rate tables and consolidation outputs is a strong TrackedFR candidate when data is multi-system and Excel-heavy. A one-off functional-currency memo is not.

## Scenario tests
1. Australian subsidiary invoices USD but pricing and payroll/cost economics are AUD → do not select USD from invoicing alone.
2. SaaS entity prices globally in USD, costs mostly EUR, financing USD → mixed indicators require weighted documented judgment.
3. Parent wants subsidiary to adopt USD solely to remove P&L FX → reject as non-economic reason.
4. Business model shifts from local distributor to autonomous manufacturer with local pricing/costs → reassess and establish prospective change date if evidence supports.
5. FX P&L dominated by intragroup loan → isolate exposure and assess net-investment status separately.
6. CTA movement is booked in FX gain/loss account → identify classification/process error.
7. UK 2026 reporter → use current FRS 102 Section 30, not IAS 21 by analogy.
8. US foreign entity in highly inflationary economy → ASC 830-specific route.
9. Currency not exchangeable under IFRS/AASB in 2026 → invoke exchangeability model before rate analysis.
10. Monthly FX cannot be reconciled to exposure/rate movements → open data/system exception; do not accept unexplained residual.

Expected routing: **10/10 PASS**.

## Source register / rights
Primary references checked 2026-09-23: IFRS Foundation IAS 21; AASB 121 current compilation (paras 9–14 and exchangeability additions); FRC FRS 102 Section 30/current differences material; FASB ASC 830 official materials. Authoritative standard text is REFERENCE_ONLY; this file is independently authored.

## Completion assessment
Principles: PASS. IFRS/AASB functional-currency routing: PASS. UK routing/effective period: PASS. US topic routing: PASS with Codification-depth limitation. FX analytical method: PASS. Controls/documentation/systems: PASS. Capability integration: PASS. Scenarios: 10/10 PASS. **Factory status: REVIEWED / production-candidate.**