# TOPIC-06-005 — Debt Accounting / Debt Issuance Cost Accounting

Status: **REVIEWED / production-candidate**  
Primary capabilities: **CAO-06-010, CAO-06-011**  
Sensitivity: **H**  
Source check: **2026-09-23**

## Objective
Enable the CAO to establish the complete debt population, determine initial/subsequent measurement, allocate fees and transaction costs correctly, build effective-interest schedules, reconcile debt to lenders/GL and route complex features to financial-instrument topics.

## Required facts
Executed facility/note and amendments; lender/borrower/entity; currency; principal/draws/repayments; issue price; stated/benchmark/margin rates; payment dates; fees by recipient and nature; legal/advisory/arranger costs; commitment/unused fees; warrants/conversion/embedded features; collateral; covenants; maturity/prepayment/call terms; refinancing events; accrued interest; current lender statements; framework/period.

## Principles
Debt accounting follows contractual economics and applicable financial-liability classification, not the cash proceeds alone. Separate lender fees, third-party transaction costs, ongoing service/commitment fees and equity/derivative components before calculating carrying amount. Maintain an instrument-level amortised-cost/effective-interest rollforward and reconcile it to legal principal and the GL.

## IFRS / AASB
Route financial-liability recognition/measurement through IFRS 9 / AASB 9, presentation through IAS/AASB 32 and disclosures through IFRS/AASB 7. Transaction costs directly attributable to a financial liability not measured at FVTPL affect initial carrying amount and effective-interest accounting; FVTPL transaction costs follow the applicable expense model. The 2024 IFRS 9/7 classification-and-measurement amendments are effective annual periods beginning on/after **1 January 2026**, including specified electronic-payment settlement and disclosure changes; test effective period before use. AASB current compilation must be independently checked.

## US GAAP
Route debt through current ASC 470 and related interest/imputation/presentation guidance. Debt issuance-cost presentation and amortization, revolving-line costs, discounts/premiums and instrument-specific features can differ from IFRS. Do not infer US treatment from IFRS 9. Public Codification depth is incomplete, so paragraph-level US conclusions remain **PARTIAL** unless verified through authorized current Codification access.

## UK GAAP
Use the reporting-period-effective FRS 102 Sections 11/12 (and other applicable sections) for financial liabilities, transaction costs and effective-interest mechanics. The Periodic Review 2024 version is generally effective periods beginning on/after **1 January 2026**. Do not assume IFRS 9 classification or derecognition mechanics apply unchanged.

## CAO workflow
1. Reconcile legal debt inventory to lender statements, bank cash flows, board/treasury records and GL.
2. Identify unit of account and complex features; route convertibles/warrants/derivatives separately before final measurement.
3. Determine classification/measurement category under framework.
4. Build gross proceeds bridge and classify every fee/cost by recipient, purpose and direct attribution.
5. Establish initial carrying amount and effective interest rate/yield.
6. Build contractual and accounting amortization schedule by payment date.
7. Accrue interest and amortize discount/premium/eligible costs; reconcile cash interest to effective interest.
8. Separate principal, accrued interest and presentation items consistently.
9. Assess current/non-current classification, covenant effects and refinancing under reporting framework/topic.
10. Reconcile lender/legal principal → accounting carrying amount → GL → financing-liability disclosures/cash-flow rollforward.
11. Document judgments and retain fee invoices/contracts/rate calculations.

## Calculation architecture
Opening carrying amount + new recognized debt +/- eligible initial measurement adjustments + effective interest expense - contractual cash interest/principal paid +/- FX/FV/other framework-supported movements = closing carrying amount. Maintain a separate legal-principal rollforward so unamortized costs/discounts do not obscure lender balance.

## Controls / audit / systems
Debt-register completeness; executed-agreement repository; draw/repayment-to-bank reconciliation; independent fee classification; EIR schedule validation; rate-reset control; covenant calendar; maturity/current-noncurrent review; modification trigger; debt-to-GL reconciliation; financing-liability disclosure rollforward; access/change control over debt schedules.

## Scenario tests
1. Term loan issued below par with lender fee and legal fee → classify costs before EIR schedule.
2. Revolver commitment fee with no draw → do not automatically net all fees against debt; analyze service/facility economics.
3. Convertible note → route conversion feature before final debt schedule.
4. USD debt in EUR-functional entity → debt accounting plus FX remeasurement topic.
5. Debt at FVTPL → do not mechanically capitalize transaction costs as amortized-cost debt.
6. New IFRS period beginning 2026 uses electronic settlement system → apply effective IFRS 9 amendment where criteria relevant.
7. US issuance costs → use ASC-specific presentation/amortization, not IFRS assumption.
8. Lender principal agrees but GL differs by unamortized fees → explain carrying-amount bridge.
9. Debt schedule uses nominal interest only despite material discount → rebuild effective-interest accounting.
10. Refinancing/amendment signed → trigger TOPIC-06-006 before continuing old schedule.

Expected routing: **10/10 PASS**.

## Sources / rights
Primary sources checked 2026-09-23: IFRS Foundation IFRS 9/IFRS 7 current pages and 2024 amendments; AASB 9 current online compilation; FRC FRS 102 current financial-instrument material; FASB ASC 470 official materials. Authoritative text is REFERENCE_ONLY; independently authored guidance only.

## Completion assessment
Principles: PASS. Framework routing: PASS subject to US paragraph-depth guardrail. Calculation architecture: PASS. Documentation/controls/audit/systems: PASS. Capability integration: PASS. Scenarios: 10/10 PASS. **Factory status: REVIEWED / production-candidate.**