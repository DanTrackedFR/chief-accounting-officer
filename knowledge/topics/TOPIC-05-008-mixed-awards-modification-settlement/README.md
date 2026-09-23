# TOPIC-05-008 — Cash-and-Equity Mixed Awards / Modification, Cancellation & Settlement of Awards

Status: **REVIEWED / production-candidate**  
Primary capabilities: CAO-05-015, CAO-05-016  
Sensitivity: M (standards-sensitive in classification, measurement and modification mechanics)

## CAO objective
Take an executed compensation arrangement and subsequent change event from facts to classification, measurement, expense/equity/liability accounting, journal entries, disclosures, controls and audit evidence. Never infer classification from the plan label alone.

## Required facts
Entity/framework/period; award holder and service relationship; grant/approval/communication dates; instrument and settlement alternatives; who controls settlement choice; number of awards; vesting/service/performance/market/non-vesting conditions; fair-value evidence; cash cap/floor; withholding feature; group-settlement facts; modification/cancellation/settlement dates and terms; original and modified fair values; vested/unvested status; forfeitures; payroll/tax settlement data.

## Decision logic
1. Establish scope and applicable reporting period.
2. Read legal plan, grant notice and amendments; identify substantive settlement obligation rather than relying on HR terminology.
3. Classify each component/arrangement as equity-settled, cash-settled/liability, or an arrangement with settlement alternatives under the applicable framework.
4. Separate genuinely distinct components only where the framework requires it; avoid economically double-counting one promise.
5. Establish original measurement basis and cumulative expense immediately before the change.
6. Identify event: modification, cancellation, forfeiture for failure of vesting condition, settlement, replacement, or classification change.
7. Determine whether modification accounting is triggered and whether employee-beneficial incremental value/minimum compensation floors apply.
8. Remeasure liability-classified awards through settlement as required; do not mechanically freeze grant-date fair value.
9. Account for cancellation/settlement and any replacement award; distinguish consideration for equity repurchase from compensation where required.
10. Reconcile award register → valuation → expense schedule → payroll/settlement → GL → equity/liability rollforward → disclosures.
11. Document conclusion, judgments, entries, evidence and durable policy/elections.

## Framework overlays
### IFRS
IFRS 2 covers equity-settled, cash-settled and arrangements with cash alternatives. Cash-settled awards are liability-measured and remeasured; equity-settled employee awards generally use grant-date measurement subject to IFRS 2 condition mechanics. IFRS 2 contains specific modification/cancellation rules and specific mechanics when a cash-settled transaction is modified to equity-settled. The 2016 amendments clarified cash-settled vesting/non-vesting effects, qualifying net settlement for withholding, and cash-to-equity classification changes. Primary pointers: IFRS 2 including paragraphs 27–29 and B42–B44C as applicable. Source body is REFERENCE_ONLY in this public repository.

### US GAAP
Route employee/nonemployee share-based compensation through ASC 718. Classification and modification conclusions are not assumed to equal IFRS 2. Topic 718 modification accounting generally treats a modification as exchange of the original award for a modified award and can create incremental compensation cost. ASU 2017-09 narrowed when a change requires modification accounting; use current Codification for final paragraph-level authority. Public FASB materials are sufficient for architecture but not every current paragraph body, so paragraph-level status remains PARTIAL until verified in authoritative Codification access.

### UK GAAP
FRS 102 Section 26 is the primary share-based-payment route. Confirm reporting period and current edition before applying. Do not import IFRS 2 mechanics where Section 26 differs or simplifies. The September 2024 FRS 102 edition plus subsequent amendments is the current source set; most Periodic Review 2024 changes have principal effective date 1 January 2026.

### AASB
AASB 2 incorporates IFRS 2 with Australian-specific material identified by Aus paragraphs. Use the period-applicable AASB compilation independently; the AASB portal identifies the current AASB 2 version for periods beginning on/after 1 January 2022 and before 1 January 2027, with future AASB 18 consequential amendments requiring effective-date routing.

## Framework-difference guardrails
- Never assume IFRS 2 and ASC 718 modification/cancellation outcomes are identical.
- Reconfirm liability/equity classification after any settlement-choice change.
- Separate a forfeiture caused by failure to satisfy a vesting condition from an entity/employee cancellation.
- Net settlement for employee tax withholding is framework-specific; do not generalize an exception.
- Group awards require identification of which entity receives services and which entity settles.

## Calculation model
Maintain award-level fields for quantity, original FV, modified FV, vested fraction, cumulative cost before event, incremental value, liability remeasurement, cash paid, equity issued and remaining service period. Recompute cumulative recognized cost after each event and derive current-period catch-up/remaining expense. Preserve valuation model/version and input lineage.

## Journal-entry outputs
Possible outputs include compensation expense or capitalized employee cost; AP/payroll withholding payable; share-based-payment liability; equity reserve/APIC; cash; share capital; and settlement/reclassification entries. Exact accounts depend on entity COA and framework conclusion.

## Controls / audit / systems
- approved plan and grant master tied to cap table/HRIS;
- maker-reviewer over valuation inputs and modification classification;
- legal/board/HR change feed to accounting;
- completeness reconciliation of grants, exercises, cancellations and settlements;
- payroll withholding reconciliation;
- valuation version lock and evidence retention;
- quarterly award-register-to-GL rollforward;
- disclosure tie-out.

Evidence pack: executed plan/grants/amendments, approvals, valuation reports/models, employee population, vesting evidence, payroll settlement, cap table, award rollforward, JE support and memo.

## Practice classification
**Required:** correct scope/classification/measurement/event accounting and disclosures.  
**Recommended:** award-level subledger, quarterly legal/HR completeness certification, independent valuation review for material complex awards.  
**World-class:** event-driven accounting feed from equity platform + HRIS + payroll with exception-based review and automated GL/disclosure reconciliation.  
**Shortcut/risk:** treating all equity-plan awards as equity-settled or treating every cancellation as forfeiture.

## TrackedFR applicability
Relevant only where recurring award/payroll/cap-table/ERP data must be reconciled or manipulated across systems. Not recommended merely because a valuation schedule is in Excel.

## Scenario tests
1. Cash-settled award changed to equity settlement mid-vesting → route classification-change mechanics, derecognition/recognition and catch-up.
2. Equity award repriced while unvested → assess modification and incremental cost; preserve original minimum where applicable.
3. Award cancelled by employer with cash payment → distinguish cancellation/settlement from vesting-condition forfeiture.
4. Net share settlement for payroll withholding → framework-specific exception test, payroll liability and equity-platform reconciliation.
5. Parent settles subsidiary employee award → group/entity-level accounting route.

Expected: all scenarios produce facts request, framework route, calculation, JE, evidence, controls and documentation; no unsupported cross-framework equivalence.

## Authoritative source register (checked 2026-09-23)
- IFRS Foundation — IFRS 2 Share-based Payment overview/current project history: https://www.ifrs.org/issued-standards/list-of-standards/ifrs-2-share-based-payment/
- IFRS Foundation — 2016 Classification and Measurement amendments.
- FASB — Accounting Standards Codification is sole authoritative nongovernmental US GAAP; ASU 2017-09 communicates Topic 718 modification changes.
- FRC — FRS 102 September 2024 edition, Section 26; principal Periodic Review 2024 effective date 1 January 2026.
- AASB — AASB 2 current-version portal and current accounting-standards register.

## Completion criteria
[x] principles/practice
[x] four-framework routing as applicable
[x] differences/decision logic
[x] calculation and JE model
[x] documentation/controls/audit/systems
[x] capability integration
[x] scenarios
[x] source/effective-period guardrails

APPROVED paragraph-level status is intentionally withheld where current authoritative paragraph bodies have not been independently verified.