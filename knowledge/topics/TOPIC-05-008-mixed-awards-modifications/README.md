# TOPIC-05-008 — Cash-and-Equity Mixed Awards / Modification, Cancellation & Settlement of Awards

Status: **REVIEWED / production-candidate**  
Primary capabilities: **CAO-05-015, CAO-05-016**  
Sensitivity: **M (framework-sensitive)**  
Last source check: **2026-09-23**

## Objective
Enable the CAO to determine the accounting for awards with cash/equity settlement alternatives and for modifications, cancellations, replacements and settlements of share-based awards. This topic extends TOPIC-05-007; it does not repeat basic scope, grant-date measurement, vesting-condition or valuation mechanics.

## Required inputs
1. Reporting framework, entity, reporting period and award population.
2. Executed plan and grant documents, including settlement-choice clauses.
3. Original grant date, vesting/service/performance conditions and classification.
4. Original valuation and cumulative expense/equity/liability recognized.
5. Amendment, cancellation, replacement or settlement documents and effective dates.
6. Who controls settlement choice: entity, counterparty or neither in substance.
7. Past settlement practice, stated policy and legal ability to issue equity.
8. Fair value immediately before/after modification where required; liability fair value at modification/settlement where applicable.
9. Employee/nonemployee status and group-plan relationships.
10. Tax-withholding/net-settlement terms where relevant.

## Principles
- Classification follows the substantive settlement obligation, not the label used in the plan.
- A modification analysis starts by preserving the original award history: original classification, measurement basis, vesting terms, cumulative recognized cost and unrecognized cost.
- Do not erase previously recognized service merely because terms change. Determine whether the framework requires minimum original-grant cost, incremental cost, liability remeasurement, acceleration, reversal, or a new/replacement award.
- Cancellation, settlement, forfeiture and modification are distinct events. The CAO must establish the event before calculating the accounting.
- Mixed awards require explicit identification of who has settlement choice and whether a present cash obligation exists.
- Any accounting conclusion must reconcile award-level calculations to payroll/equity administration, the GL and disclosures.

## Framework routing

### IFRS — IFRS 2
Authoritative route: IFRS 2 Share-based Payment.

Key CAO rules:
- Equity-settled modifications retain, at minimum, the grant-date fair-value service cost subject to the original vesting-condition model; beneficial modifications can create incremental value.
- Cancellation/settlement of an equity award during vesting is generally treated as accelerated vesting, with payments analyzed between repurchase of equity and any excess expense as applicable.
- Cash-settled awards are liability-accounted and remeasured through settlement.
- IFRS 2 contains specific guidance for a modification that changes a cash-settled award to equity-settled: measure the equity award at modification-date fair value, derecognize the cash liability, and recognize the difference immediately in profit or loss; apply the modified vesting period where relevant.
- Settlement-choice arrangements require the specific IFRS 2 cash/equity alternative guidance rather than a generic compound-instrument analogy.
- Net settlement for withholding tax has specific IFRS 2 classification requirements and must be tested against the standard rather than assumed to create liability classification.

Useful paragraph anchors for primary-source verification: IFRS 2.26–29, 30–33, 34–43, B42–B44C. Paragraph-level use remains reference-only in this public repository.

### AASB — AASB 2
AASB 2 is IFRS 2-aligned for this topic. AASB 2.26–29 addresses modifications/cancellations/settlements; Appendix B includes the cash-to-equity modification mechanics at B44A–B44C. The CAO must still verify the current Australian compilation and reporting period rather than infer compliance solely from IFRS.

### US GAAP — ASC 718
Authoritative route: ASC Topic 718, Compensation—Stock Compensation.

Key CAO rules:
- First establish equity versus liability classification under Topic 718 and whether the changed terms require modification accounting.
- Topic 718 modification accounting generally treats a modified equity award as an exchange and can require incremental compensation cost based on the value immediately before and after modification, subject to the detailed classification/vesting rules.
- A cancellation followed by a replacement award may be economically and accounting-wise linked; do not book the events independently until the replacement analysis is complete.
- Settlement of an equity-classified award requires analysis of whether consideration exceeds the applicable fair value and whether additional compensation cost results.
- Changes that affect classification, vesting conditions or value require careful Topic 718 routing; administrative-only changes should not be elevated into economic modifications without support.
- Public FASB material does not expose the full current Codification body through the project’s public-source route. Therefore detailed ASC 718 paragraph-level conclusions remain **PARTIAL** until verified against authorized/current Codification access. Do not invent paragraph citations.

Current-source note: ASU 2024-01 added illustrative scope guidance for profits-interest awards; ASU 2025-04 addresses share-based consideration payable to a customer. Neither should be treated as a general rewrite of employee modification accounting. Current FASB projects/tentative decisions do not change GAAP until issued and effective.

### UK GAAP — FRS 102 Section 26
Authoritative route: FRS 102 Section 26, with reporting-period routing for the Periodic Review 2024 amendments (generally periods beginning on/after 1 January 2026 unless early adopted).

Key CAO rules:
- Cash-settled arrangements use liability measurement and remeasurement mechanics in Section 26.
- Under the revised Section 26, when the entity controls settlement choice, equity settlement is generally used unless the equity alternative lacks commercial substance or past practice/stated policy creates cash settlement; when the counterparty controls settlement choice, route through the specific Section 26 requirements rather than importing IFRS 2 mechanically.
- The Periodic Review 2024 changes added/clarified cash-settled measurement and cash-alternative mechanics, including paragraphs 26.14A–26.14C and revised 26.15-series requirements.
- UK GAAP is not assumed identical to IFRS 2. Effective-period gating is mandatory.

## Framework differences the CAO must surface
1. **Settlement choice:** IFRS 2, ASC 718 and FRS 102 have their own classification mechanics. Never infer one framework’s outcome from another.
2. **Modification mechanics:** incremental-value, classification-change and vesting-condition treatment can diverge. Calculate only after framework routing.
3. **Cancellation/replacement:** determine whether the replacement is linked to the cancelled award under the applicable framework.
4. **Liability awards:** remeasurement creates P&L volatility; equity awards generally preserve a fixed measurement basis after the relevant measurement date, subject to modification accounting.
5. **UK effective period:** pre-2026 and 2026+ FRS 102 must be routed separately where amendments affect the conclusion.
6. **US source depth:** retain PARTIAL paragraph-level status unless current Codification text has been independently verified.

## CAO execution workflow
1. Resolve framework/entity/period and employee/nonemployee/group-plan context.
2. Reconstruct original award: classification, grant date, units, vesting terms, measurement and recognized/unrecognized cost.
3. Read the actual amendment/cancellation/settlement and establish legal effective date.
4. Determine event type: modification, cancellation, forfeiture, settlement, replacement, or combination.
5. Determine settlement-choice holder and substantive cash obligation.
6. Reperform classification immediately before and after the event.
7. Determine required measurement dates and obtain valuations.
8. Calculate original minimum cost, incremental cost, liability remeasurement, acceleration/reversal and settlement allocation as applicable.
9. Build award-level rollforward: opening equity/liability + service cost + remeasurement + modification/cancellation/settlement + cash/equity issuance = closing balance.
10. Produce JE and map expense classification consistently with employee function unless another standard requires capitalization.
11. Reconcile to equity administration/payroll/HR data, GL, cash/share issuance and disclosures.
12. Document significant judgments: settlement substance, replacement linkage, valuation inputs, vesting impact, classification and framework differences.
13. Promote durable plan elections/policies and recurring accounting method to Company Accounting Memory.

## Calculation pattern
Do not use a single universal formula across frameworks. Maintain these separate calculation blocks:

**A — Original award baseline**
- original measurement basis;
- cumulative cost recognized before event;
- remaining service/unrecognized cost.

**B — Modification delta**
- fair value of modified award at required measurement point;
- fair value of original award at the corresponding measurement point;
- incremental value where the framework requires it;
- revised service/vesting allocation.

**C — Liability remeasurement**
- opening liability;
- current fair value × vested/service proportion as applicable;
- current-period remeasurement through P&L;
- derecognition on settlement or classification change.

**D — Settlement/cancellation**
- accelerated unrecognized service cost where required;
- consideration paid;
- equity repurchase component versus excess compensation expense where required;
- replacement-award accounting if linked.

## Documentation package
Minimum production file:
- event chronology and executed documents;
- original award accounting summary;
- framework/effective-period conclusion;
- before/after classification assessment;
- valuation evidence and calculation workbook;
- modification/cancellation/settlement memo;
- JE and rollforward;
- equity/liability/expense reconciliation;
- disclosure impact assessment;
- reviewer evidence and open items.

## Controls, audit and systems
- Change feed from legal/equity-administration/HR to accounting for every plan amendment, cancellation, settlement and replacement.
- Independent accounting review before modified terms are booked.
- Completeness reconciliation of board-approved compensation actions to equity-admin records.
- Valuation control over before/after fair values and liability remeasurement.
- Award-level rollforward to GL and statement-of-equity/disclosure tie-out.
- Effective-date control over FRS 102 amendments and other framework changes.
- Evidence retention for legal settlement rights and past-practice conclusions.
- System configuration should preserve original award terms and modification history; never overwrite source history with only the latest terms.

## TrackedFR applicability
Recommend TrackedFR only when the recurring close requires cross-system manipulation/reconciliation across equity administration, payroll/HR, ERP/GL and reporting workbooks. It is not recommended merely because a valuation or award schedule happens to be in Excel.

## Scenario tests
1. Equity award repriced upward in employee’s favor: route to beneficial-modification/incremental-value analysis; preserve original baseline.
2. Equity award cancelled during vesting for cash: distinguish forfeiture from cancellation; test acceleration and settlement allocation.
3. Cash-settled IFRS/AASB award modified to equity-settled: route to B44A–B44C mechanics, derecognize liability and recognize modification-date equity/difference.
4. Entity has contractual cash/equity choice but established cash-settlement practice: do not assume equity classification; evaluate framework-specific substance.
5. Counterparty controls settlement choice: invoke framework-specific mixed/compound mechanics rather than entity-choice rules.
6. US award terms changed but value, vesting conditions and classification are unchanged: verify whether Topic 718 modification accounting is required before calculating incremental cost.
7. UK entity period beginning 1 January 2026: route to revised FRS 102 Section 26; do not reuse a pre-2026 conclusion blindly.
8. Replacement grant issued contemporaneously with cancellation: test linkage before treating it as an unrelated new grant.
9. Modification spreadsheet does not reconcile to equity-admin population: stop accounting conclusion, resolve completeness/data lineage and retain open item.

Expected result: **9/9 routing tests pass** when the CAO follows this workflow.

## Completion assessment
- Principles: PASS
- IFRS source routing: PASS
- AASB source routing: PASS
- UK GAAP source routing/effective-period gate: PASS
- US GAAP topic routing: PASS; paragraph-level authority depth PARTIAL
- Differences: PASS
- CAO workflow: PASS
- Calculation architecture: PASS
- Documentation/controls/audit/systems: PASS
- Capability integration: PASS
- Scenario design: PASS

**Factory status: REVIEWED / production-candidate.** Promotion to APPROVED requires the normal record-level source verification, including authorized/current ASC 718 paragraph verification where a conclusion depends on paragraph detail.

## Authoritative source register
- IFRS Foundation — IFRS 2 Share-based Payment standard page and official issued-standard material; current source check 2026-09-23.
- IFRS Foundation — Classification and Measurement of Share-based Payment Transactions amendments; effective for annual periods beginning on/after 1 January 2018.
- FASB — Topic 718 official ASUs/current project materials; Codification remains authoritative.
- FRC — FRS 102 Periodic Review 2024 amendments, Section 26; most amendments effective periods beginning on/after 1 January 2026.
- AASB — AASB 2 current online standard, paragraphs 26–29 and Appendix B B44A–B44C.

Public repository rule: source names, paragraph pointers and independently authored explanations are stored; copyrighted standards body text is not republished.