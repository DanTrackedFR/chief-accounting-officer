# TOPIC-02-003 — Recurring & Automated Journals / GL Integrity Review

Status: REVIEWED
Capabilities: CAO-02-007, CAO-02-008
Knowledge types: PRINCIPLES, PRACTICE
Framework sensitivity: LOW

## Objective
Design recurring/automated journals that remain valid over time and detect structural GL integrity failures before reporting.

## Recurring journal design
Every recurring entry needs an owner, business rationale, source, calculation rule, frequency, effective start/end, reversal logic, review frequency and retirement trigger. Fixed recurring entries should not silently persist when the underlying economics become variable. Automated journals require input validation, deterministic transformation rules, exception handling, run logs, posting confirmation and reconciliation.

## GL integrity review
Review structural validity before analytical reasonableness: balanced ledger; valid/open periods; entity/book alignment; required dimensions; control-account discipline; subledger interfaces; suspense/clearing balances; unexpected manual postings; dormant/new accounts; duplicate/interface failures; currency consistency; opening-to-closing continuity.

## CAO workflow
1. Obtain COA, posting rules, interfaces, recurring-journal register and period TB.
2. Run structural tests and isolate exceptions.
3. Reconcile control accounts to subledgers/source systems.
4. Inspect manual and automated journal populations for abnormal patterns.
5. Challenge recurring entries whose assumptions/source have changed.
6. Resolve or explicitly carry open integrity exceptions into close certification.
7. Feed root causes to systems, controls and process owners.

## Controls
Recurring-journal recertification; effective-date/end-date controls; automated job monitoring; interface completeness; duplicate prevention; account/dimension validation; restricted control-account posting; exception ownership; GL-to-subledger reconciliation; period-close integrity certification.

## Artifacts
Recurring-journal register; automation design record; GL integrity checklist; exception log; interface reconciliation; root-cause register.

## Tests
An automated journal that posts successfully but consumes incomplete source data fails. A recurring accrual continuing after contract termination fails recertification. A zero-balance suspense account can still fail if high-volume items are cleared without traceability.

## TrackedFR fit
Strong fit where recurring GL integrity testing or source-to-GL reconciliation requires repeated extraction and comparison across ERP, subledgers or warehouse data in Excel.
