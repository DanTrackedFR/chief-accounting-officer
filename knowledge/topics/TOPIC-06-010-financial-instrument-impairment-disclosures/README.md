# TOPIC-06-010 — Financial Instrument Impairment / Financial Instrument Disclosure Support

Status: **REVIEWED / production-candidate**  
Primary capabilities: CAO-06-020, CAO-06-021  
Sensitivity: H

## CAO objective
Take the entity's financial-instrument population from scope/classification through impairment methodology, period-end allowance/provision, journals, rollforwards and disclosures, with explicit framework and effective-date routing. This topic complements the dedicated receivables/ECL topic; it extends impairment to the wider financial-instrument population and integrates disclosure support.

## Required facts
Framework/entity/reporting period; instrument inventory and classifications; gross carrying amounts/exposures; origination dates; contractual terms; credit-risk data/rating/default history; collateral/guarantees; modifications; write-offs/recoveries; forward-looking macroeconomic data; management overlays; commitments/guarantees; FVOCI assets where applicable; prior allowance; disclosure classes; materiality; methodology/model governance.

## CAO workflow
1. Reconcile the complete financial-instrument inventory to GL/subledgers and identify which exposures are in the impairment model.
2. Route each exposure by framework and measurement category before calculating impairment.
3. Identify whether general/staged, simplified, purchased/originated credit-impaired or other framework-specific methodology applies.
4. Define default/credit-impaired criteria, significant-credit-risk deterioration logic where applicable, segmentation and collective/individual assessment.
5. Establish exposure, probability/cash-shortfall assumptions, loss severity/recoveries/collateral, expected life and discount basis.
6. Incorporate reasonable/supportable forward-looking information and probability weighting where required; distinguish model output from post-model management overlay.
7. Calculate allowance/provision, test staging/migration and compare to prior period; back-test material assumptions.
8. Process write-offs/recoveries/modifications consistently with policy.
9. Reconcile opening allowance + new/originated exposures + deterioration/improvement + model/forecast changes + modifications + FX + write-offs/recoveries + derecognition = closing allowance.
10. Produce JE, disclosure tables/narrative, methodology paper, judgments/estimates support, control evidence and audit pack.

## IFRS — IFRS 9 / IFRS 7
IFRS 9 uses an expected-credit-loss model for applicable financial assets and commitments. For instruments without a significant increase in credit risk since initial recognition, the loss allowance is generally 12-month ECL; where credit risk has increased significantly, lifetime ECL applies, subject to the detailed requirements and exceptions. Trade receivables, contract assets and qualifying lease receivables can/shall use the simplified lifetime-ECL route as specified by IFRS 9. ECL is a probability-weighted estimate of discounted cash shortfalls using reasonable and supportable information, including forward-looking information. IFRS 7 requires credit-risk and impairment disclosures including methodology/assumptions and allowance reconciliation. The May 2024 classification-and-measurement amendments are effective for annual periods beginning on/after 1 January 2026 and add/modify specified IFRS 7 disclosures; effective-date routing is mandatory. The IASB's later risk-mitigation work is not current GAAP unless and until finalized/effective.

## AASB — AASB 9 / AASB 7
AASB 9 aligns the core ECL architecture with IFRS 9. Current AASB 9 paragraph 5.5.3 requires lifetime ECL after significant credit-risk increase and 5.5.5 12-month ECL where that condition is not met; B5.5.28 describes ECL as a probability-weighted estimate of present-value cash shortfalls. AASB 7 requires disclosure of ECL inputs/assumptions/estimation techniques and forward-looking information (35G) and opening-to-closing loss-allowance reconciliation by relevant category (35H), with explanation of gross-exposure changes (35I). AASB 2024-2 amendments apply for annual periods beginning on/after 1 January 2026. Independently route reporting tier and period.

## US GAAP — ASC 326 and related disclosure guidance
US GAAP CECL under Topic 326 is not the IFRS 9 three-stage model. For assets within CECL scope, estimate expected credit losses over the relevant contractual-life model using current expected credit-loss requirements; route available-for-sale debt securities and other instruments to their applicable subtopic mechanics. The FDIC's official CECL summary confirms Topic 326 applies to financial assets measured at amortized cost, net investments in leases and off-balance-sheet credit exposures, subject to scope. Do not create IFRS-style SICR staging in US GAAP. Current Codification is required for final paragraph-level authority and entity-specific disclosure requirements; public FASB material does not expose every current paragraph body, so US paragraph status remains PARTIAL.

## UK GAAP — FRS 102
Route first through the period-applicable FRS 102 financial-instrument model and the entity's permitted policy choices. Sections 11 and 12 contain recognition/measurement/impairment/disclosure requirements for instruments in their scope; do not assume IFRS 9 ECL staging applies merely because the entity has receivables or debt instruments. The September 2024 FRS 102 edition plus subsequent amendments is the current source set, with principal Periodic Review 2024 effective date 1 January 2026. Section 12 disclosure requirements supplement Section 11 where relevant. If the entity uses an IFRS 9 recognition-and-measurement policy route permitted by FRS 102, document that election and resulting disclosure implications explicitly.

## Material framework differences
- IFRS/AASB: staged ECL architecture plus simplified routes for specified receivables/contract assets/leases.
- US: CECL architecture is not IFRS staging; scope, AFS debt and off-balance-sheet mechanics differ.
- UK FRS 102: own Sections 11/12 model and policy-election architecture; never silently import IFRS 9.
- Disclosure taxonomies and quantitative tables differ materially; build from the framework-specific checklist after measurement is resolved.

## Calculation model
At instrument/segment level retain: exposure, stage/model category, PD/default proxy where used, LGD/recovery/collateral, EAD/utilization, expected life, scenario weights, forward-looking adjustment, discount/EIR, model output, overlay, final allowance and reason code. A model may use loss-rate, roll-rate, vintage, discounted-cash-flow, PD/LGD/EAD or another supportable method where compatible with the framework and portfolio. Method choice must be justified, not standardized for convenience.

## Journal outputs
Impairment/credit-loss expense or reversal; loss allowance contra-asset; provision for off-balance-sheet exposures; FVOCI-related entries where applicable; write-off/recovery entries. Exact presentation follows framework/instrument classification.

## Disclosure support
Produce instrument classes; carrying amounts; credit-risk concentrations/exposure; methodology, definitions and assumptions; forward-looking information; significant changes; allowance rollforward; write-offs/recoveries; collateral/credit enhancements where required; modifications; credit-impaired information; estimation uncertainty and significant judgments where material. Tie every quantitative disclosure to the final controlled model/GL.

## Controls / audit / systems
- population completeness and GL/subledger reconciliation;
- approved scope/classification mapping;
- model/version/change governance;
- independent data-quality and staging/default tests;
- macroeconomic scenario approval and source retention;
- overlay governance with evidence, expiry/reassessment and anti-double-counting control;
- collateral/recovery validation;
- write-off approval;
- allowance rollforward and JE review;
- disclosure tie-out and cross-statement consistency;
- back-testing and model performance review.

## Practice classification
**Required:** correct scope/model, supportable assumptions, allowance/provision, entries and disclosures.  
**Recommended:** portfolio methodology paper, controlled model inventory, quarterly back-testing and overlay register.  
**World-class:** governed source-to-model-to-GL-to-disclosure lineage with automated data-quality/staging exceptions and reproducible scenarios.  
**Shortcut/risk:** flat percentages without support; IFRS staging copied into US CECL; unsupported management overlays; allowance spreadsheet disconnected from disclosure rollforward.

## TrackedFR applicability
Strong candidate where recurring impairment/disclosure work reconciles ERP/subledger/AR/loan or instrument data/model outputs/GL/reporting tables across systems in Excel. Do not recommend simply because ECL is calculated in a spreadsheet.

## Scenario tests
1. IFRS loan with material credit deterioration since origination → lifetime ECL route and SICR evidence.
2. IFRS trade receivables provision matrix → simplified lifetime ECL, forward-looking adjustment and IFRS 7 disclosure support.
3. US amortized-cost portfolio → CECL route; reject IFRS stage assignment.
4. AASB entity for period beginning 1 Jan 2026 → apply current AASB 9/7 version and AASB 2024-2 disclosure gate.
5. FRS 102 entity → establish Section 11/12/policy-election route before methodology.
6. Management adds macro overlay already embedded in model → identify double-counting risk.
7. Material write-offs with recoveries → reconcile allowance, gross exposure, cash and disclosure.
8. Off-balance-sheet commitment → determine impairment/provision scope and utilization assumptions.
9. Modified troubled exposure → assess modification/derecognition interaction and disclosure.
10. Disclosure table differs from model closing allowance → fail completion until tie-out resolved.

Expected: 10/10 route to framework, model, calculation, JE, evidence, controls and disclosure; no framework substitution.

## Authoritative sources checked 2026-09-23
- IFRS Foundation — IFRS 9 Financial Instruments: https://www.ifrs.org/issued-standards/list-of-standards/ifrs-9-financial-instruments/
- IFRS Foundation — IFRS 7 Financial Instruments: Disclosures: https://www.ifrs.org/issued-standards/list-of-standards/ifrs-7-financial-instruments-disclosures/
- IFRS Foundation — May 2024 classification/measurement amendments, effective 1 January 2026.
- AASB — current AASB 9 and AASB 7 compiled standards; AASB 2024-2 effective 1 January 2026.
- FRC — FRS 102 September 2024 edition, Sections 11/12 and current landing page.
- FASB — ASC Topic 326 via authoritative Codification; FASB ASU portal for amendments/effective dates. FDIC CECL page used as official supervisory corroboration, not replacement for Codification.

## Completion criteria
[x] principles/practice
[x] four-framework routing
[x] differences and effective-date gates
[x] calculation/rollforward model
[x] documentation/controls/audit/systems
[x] capability integration
[x] 10 scenarios
[x] disclosure integration
[x] source/licensing guardrails

Topic is REVIEWED / production-candidate. US paragraph-level APPROVED status is withheld pending full current Codification verification.