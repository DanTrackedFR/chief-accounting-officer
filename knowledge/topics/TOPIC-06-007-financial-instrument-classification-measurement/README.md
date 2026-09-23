# TOPIC-06-007 — Financial Asset & Liability Classification and Measurement

Status: **REVIEWED / production-candidate**
Primary capabilities: CAO-06-014, CAO-06-015
Sensitivity: H
Updated: 2026-09-23

## Objective
Enable the CAO to identify the instrument, establish the governing framework and reporting period, classify the asset or liability, determine initial and subsequent measurement, produce the accounting conclusion and entries, and preserve the evidence supporting the conclusion.

## Mandatory intake
1. Entity, reporting framework, period and functional currency.
2. Executed instrument and all amendments/side letters.
3. Holder/issuer perspective and legal form.
4. Settlement terms, maturity, interest/coupon, prepayment/extension/conversion/contingent features.
5. For financial assets: how the portfolio is actually managed, performance evaluated and cash flows realised.
6. Initial fair value, transaction costs, fees and subsequent cash-flow history.
7. Related instruments, guarantees, derivatives, collateral and embedded features.
8. Elections already made and prior-period accounting.

## Principles
- Recognition starts when the entity becomes party to contractual provisions; legal labels do not replace analysis of contractual rights and obligations.
- Separate classification from measurement. First determine what the instrument is and the applicable model, then calculate carrying amount and P&L/OCI/equity effects.
- For IFRS 9/AASB 9 financial assets, business model and contractual cash-flow characteristics are core classification gates. Amortised cost requires hold-to-collect plus SPPI; debt FVOCI requires hold-to-collect-and-sell plus SPPI; residual assets are generally FVTPL, subject to applicable elections and scope rules.
- Financial liabilities require separate analysis; do not mirror asset classification mechanically. Identify FVTPL designation/trading, amortised-cost treatment, own-credit presentation where applicable, and compound/equity features under the relevant framework.
- Transaction costs follow the measurement category: they are not treated identically for instruments at FVTPL and instruments subsequently measured at amortised cost/FVOCI.
- Reclassification is framework-specific and constrained; a change in management intent for one asset is not automatically a business-model change.
- Classification does not complete the accounting. Route to impairment, fair value, derivatives/hedging, FX, derecognition, modification and disclosure topics where triggered.

## Framework routing
### IFRS
Primary authorities: IFRS 9 (classification, recognition, measurement, impairment, hedge accounting) plus IAS 32 for financial liability/equity presentation and IFRS 7 for disclosures. IFRS 9's official summary confirms business-model/SPPI classification and initial fair-value measurement with directly attributable transaction costs for instruments not at FVTPL. The 2024 classification-and-measurement amendments to IFRS 9/IFRS 7 are effective for annual periods beginning on or after 1 January 2026; the CAO must period-gate them rather than applying them to earlier periods without early adoption.

### AASB
Primary authorities: AASB 9, AASB 132 and AASB 7. The current AASB 9 compilation for periods beginning on or after 1 January 2026 incorporates the classification-and-measurement amendments. AASB 2024-2 is effective for annual periods beginning on or after 1 January 2026 and addresses, among other matters, electronic-payment settlement and contractual cash-flow features including ESG-linked features. Check the exact operative compilation for the reporting period and entity tier.

### UK GAAP
Route first by reporting period and instrument scope. FRS 102 Sections 11 and 12 remain the central financial-instrument architecture; use the applicable Periodic Review 2024 version for periods beginning on or after 1 January 2026 unless early adopted. Do not import IFRS 9 categories into FRS 102 by analogy. Determine whether the instrument falls within the basic-instrument model or other-financial-instrument model and apply the corresponding recognition/measurement rules and permitted accounting-policy choices in the effective version.

### US GAAP
US GAAP is not an IFRS 9 business-model/SPPI model. Route by instrument type and holder/issuer facts across the relevant Codification topics, including ASC 310/320/321/326 for receivables, debt/equity investments and credit losses; ASC 405/470/480 for liabilities and distinguishing liabilities from equity; ASC 815 for derivatives/embedded derivatives and hedging; and ASC 820 for fair value. Public FASB material does not expose every current Codification paragraph body; paragraph-level records remain PARTIAL unless directly verified from authoritative access.

## CAO decision workflow
1. Resolve framework, period, entity/tier and perspective.
2. Inventory contractual rights/obligations and identify unit of account.
3. Run scope exclusions and special-model routing.
4. Identify derivative, conversion, contingent-settlement, guarantee and embedded features.
5. Classify the instrument under the applicable framework — never by cross-framework analogy.
6. Establish initial fair value and transaction-cost treatment.
7. Determine subsequent measurement basis and effective-interest mechanics where applicable.
8. Route impairment/ECL, FX, fair value and derivative effects.
9. Evaluate modifications, derecognition and reclassification triggers.
10. Prepare entries and carrying-value rollforward.
11. Determine presentation and disclosure dependencies.
12. Reconcile instrument register/subledger to GL and financial statements.
13. Document judgments, elections, evidence and review.
14. Promote durable elections/classification policies to Company Accounting Memory.

## Required output
- Instrument/fact summary and scope conclusion.
- Classification conclusion with framework-specific rationale.
- Initial measurement and transaction-cost calculation.
- Subsequent measurement schedule/rollforward.
- Entries and P&L/OCI/equity mapping.
- Impairment/fair-value/derivative/FX dependencies.
- Presentation/disclosure requirements to be completed by linked topics.
- Evidence gaps, judgments, uncertainties and review requirements.
- Reconciliation/control evidence and memory candidates.

## Controls and audit evidence
Maintain a complete instrument register tied to executed agreements and GL; independent review of new/modified complex instruments; documented business-model/SPPI analysis where applicable; approval of elections/designations; fair-value and EIR model controls; completeness controls over treasury/legal/AP/AR sources; modification/derecognition triggers; impairment linkage; period-end subledger-to-GL reconciliation; disclosure tie-out; and evidence of management review.

## Common failure modes
- Calling an instrument 'debt' or 'investment' and skipping contractual analysis.
- Applying IFRS 9 SPPI logic to US GAAP or FRS 102.
- Ignoring embedded/contingent/conversion features.
- Treating transaction costs identically across measurement categories.
- Missing the 1 January 2026 IFRS/AASB classification-amendment effective-date gate.
- Treating an individual sale or management-intent change as an automatic IFRS business-model reclassification.
- Completing classification without routing impairment, fair value, FX, derivatives or disclosures.

## Scenario QA
1. IFRS loan held to collect with basic lending cash flows -> assess amortised cost and ECL dependency.
2. IFRS debt portfolio managed both to collect and sell with SPPI cash flows -> assess debt FVOCI.
3. IFRS equity investment not held for trading -> assess applicable irrevocable OCI election facts; do not treat as debt FVOCI.
4. ESG-linked loan for 2026 period -> apply effective-period amended cash-flow-characteristic guidance.
5. US debt security -> route to US instrument-specific model, not SPPI.
6. UK basic debt instrument -> route through effective FRS 102 Sections 11/12, not IFRS 9 categories.
7. Convertible note issued -> route liability/equity/derivative features before measurement.
8. Liability designated FVTPL -> separately analyze own-credit/presentation requirements under applicable framework.
9. Modified instrument -> route modification/derecognition topic before assuming original classification continues unchanged.
10. Register-to-GL difference -> stop financial-statement completion until population/reconciliation exception is resolved.

Expected result: **10/10 route correctly**.

## Source register
- IFRS Foundation, IFRS 9 Financial Instruments official standard page and current amendments material; checked 2026-09-23.
- IFRS Foundation, 2024 Amendments to Classification and Measurement of Financial Instruments (IFRS 9/IFRS 7); checked 2026-09-23.
- AASB, AASB 9 current standards portal/2025 compilation and AASB 2024-2; checked 2026-09-23.
- FRC, FRS 102 current standards page and Periodic Review 2024/Factsheet 4 routing; checked 2026-09-23.
- FASB Accounting Standards Codification topic architecture and public standards materials; checked 2026-09-23. Public paragraph-body limitation recorded above.

Copyright posture: references and independently authored explanation only; no standards body text reproduced as a substitute for the authoritative literature.
