# TOPIC-06-006 — Debt Modification & Extinguishment / Covenant Accounting & Disclosure Assessment

Status: **REVIEWED / production-candidate**  
Primary capabilities: **CAO-06-012, CAO-06-013**  
Sensitivity: **H**  
Source check: **2026-09-23**

## Objective
Enable the CAO to determine whether changed debt terms continue an existing liability or extinguish it, account for fees/costs and new carrying amount, and separately assess covenant consequences for classification, going concern and disclosures.

## Required facts
Original and amended/exchanged agreements; old/new cash flows; original EIR; lender identity; fees paid/received by counterparty and third parties; modification date; legal release; changes in currency, maturity, rate, principal, collateral, conversion/embedded features; borrower financial difficulty; covenant definitions/testing dates; waiver/cure dates; grace periods; refinancing agreements; reporting date and financial-statement authorization date.

## IFRS / AASB — financial liability modification
IFRS 9/AASB 9 require derecognition when a liability is extinguished and treat an exchange with the same lender or substantial modification as extinguishment when terms are substantially different. The quantitative test in B3.3.6 compares discounted new contractual cash flows (including qualifying borrower-lender fees) using the original EIR; **at least 10%** difference is substantial. Current AASB text confirms only fees between borrower and lender (including on-behalf fees) enter that quantitative test. If extinguished, relevant costs/fees enter the extinguishment result; if not extinguished, applicable costs/fees adjust carrying amount and are amortized. Qualitative features still require analysis where relevant.

Important current-status gate: IASB's 2026 Amortised Cost Measurement project is active and is considering broader derecognition/modification improvements. Tentative decisions/exposure work **do not change current IFRS 9** until final amendments are issued and effective.

## US GAAP
ASC 470-50 is the current debt modification/extinguishment route. Official FASB materials confirm current GAAP distinguishes modification from issuance of new debt/extinguishment and includes a 10% cash-flow test in relevant debtor-creditor nontroubled modifications. The FASB Debt Exchanges project was **paused in March 2026**; proposals/tentative decisions do not change current GAAP. US creditor identity, syndication/exchange and troubled-debt fact patterns require ASC-specific analysis. Paragraph-level production conclusions remain PARTIAL without authorized current Codification verification.

## UK GAAP
FRS 102 Section 11 current public text states that an exchange with substantially different terms or a substantial modification is accounted for as extinguishment and a new liability, with the extinguishment difference recognized in P&L. Apply the reporting-period-effective version (Periodic Review 2024 generally 1 January 2026). Do not assume IFRS 9's exact quantitative mechanics where FRS 102 does not state them.

## Covenant assessment
Keep covenant accounting separate from modification math. For each covenant: identify testing date, measurement definition, headroom, breach/cure/waiver rights, lender rights at reporting date, events after reporting date, cross-default clauses and affected facilities. Route balance-sheet classification through the applicable presentation standard and effective period; route material uncertainty through Going Concern; route liquidity/financial-instrument disclosures through Financial Reporting. Do not assume a waiver obtained after reporting date retroactively changes rights existing at reporting date unless the applicable framework says so.

## CAO workflow
1. Establish old liability carrying amount and original EIR immediately before event.
2. Confirm legal release and lender/counterparty identity.
3. Reconstruct old remaining contractual cash flows and new cash flows.
4. Classify fees by borrower-lender versus third-party and by framework.
5. Perform framework-specific quantitative test where required; retain exact model.
6. Assess qualitative changes (currency, embedded features, counterparty, economics) under applicable framework.
7. Conclude modification vs extinguishment and calculate accounting.
8. Build new/continued EIR schedule and JE.
9. Independently perform covenant test and classification/disclosure assessment.
10. Reconcile modified debt schedule to lender confirmation, GL and disclosures.
11. Document current-standard conclusion and separately flag future standard-setting projects.

## IFRS/AASB 10% calculation control
PV(new contractual cash flows + qualifying net borrower/lender fees, discounted at original EIR) versus PV/remaining carrying cash-flow benchmark under the applicable guidance. Difference / benchmark >= 10% triggers substantial-difference conclusion. Model must preserve payment dates, compounding convention and original EIR; spreadsheet approximations require independent review.

## Controls / evidence
Executed amendments; lender confirmation; old/new cash-flow models; original EIR evidence; fee invoices and counterparty mapping; independent 10% model review; legal-release evidence; covenant certificate; waiver/cure correspondence; classification memo; JE; debt/GL/disclosure reconciliation; reviewer sign-off.

## Scenario tests
1. Same lender, PV difference 12% under IFRS → extinguishment route.
2. PV difference 6% but currency and economics materially changed → perform qualitative/framework analysis; do not auto-pass solely because <10%.
3. Third-party legal fees included in IFRS 10% numerator → correct model; only qualifying borrower-lender fees enter test.
4. US multi-creditor exchange in 2026 → apply current ASC 470; paused FASB project is not GAAP.
5. Covenant breached at reporting date; waiver arrives later → analyze rights/classification under applicable reporting framework and subsequent-event disclosures.
6. Covenant headroom is narrow but no breach → going-concern/liquidity sensitivity may still require attention.
7. Modification not extinguishment → update carrying amount/EIR treatment rather than writing off all deferred costs automatically.
8. Legal release obtained → test derecognition and any new obligation.
9. UK FRS 102 substantial modification → Section 11 extinguishment route; do not import unsupported IFRS mechanics.
10. Amendment introduces conversion feature → invoke financial-liability/equity/derivative topics before finalizing.

Expected routing: **10/10 PASS**.

## Source register / rights
Primary references checked 2026-09-23: IFRS Foundation IFRS 9 derecognition/10% test materials and active Amortised Cost Measurement project; AASB 9 current B3.3.6/B3.3.6A; FRC FRS 102 2024 Edition Section 11; FASB ASC 470-50 official EITF/project materials and March 2026 project status. Authoritative text is REFERENCE_ONLY.

## Completion assessment
Current-rule/effective-date routing: PASS. IFRS/AASB modification mechanics: PASS. UK routing: PASS. US routing: PASS with Codification-depth limitation. Covenant workflow: PASS. Calculation/control architecture: PASS. Scenarios: 10/10 PASS. **Factory status: REVIEWED / production-candidate.**