# TOPIC-02-003 — Recurring/Automated Journals & General Ledger Integrity

Status: REVIEWED
Capabilities: CAO-02-007, CAO-02-008
Knowledge types: PRINCIPLES, PRACTICE
Framework sensitivity: LOW

## Objective
Move stable accounting flows from repeated manual posting to controlled recurrence/automation while continuously testing that the general ledger remains structurally and economically coherent.

## Recurring-journal eligibility
Use recurrence when accounting basis, source, mapping, frequency and reversal are stable. Parameterize period-sensitive values rather than copying entries. Automation requires defined source of truth, completeness check, transformation logic, account/dimension mapping, posting rules, approval/change governance, exception path and monitoring.

Do not automate unresolved estimates, unsupported plugs or a process with unstable source data merely to accelerate close.

## GL integrity tests
- ledger balances and journal batches are complete for expected books/entities/periods;
- control accounts agree to governed subledgers or explained reconciling items;
- suspense/clearing balances are aged and owned;
- unusual debit/credit signs and dormant/new accounts are investigated;
- opening + movements = closing rollforwards where applicable;
- intercompany pairs and elimination accounts behave as designed;
- foreign-currency balances use correct currency attributes;
- dimensions required by policy are populated and valid;
- retained earnings/opening-balance mechanics operate correctly;
- duplicate, out-of-period and unauthorized postings are identified;
- system interfaces reconcile record counts/amounts and failures.

## CAO method
Inventory recurring manual journals; score volume, hours, stability, judgment and error history; prioritize deterministic high-volume entries; design automated control; parallel-run; reconcile output; approve migration; monitor exceptions and changes.

For GL integrity, build a monthly rule suite plus risk-based analytical review. A clean trial balance is not proof of integrity: balanced debits/credits can still contain wrong entity, period, account, currency or dimensions.

## Controls
Recurring-journal master changes approved; effective dates; version history; source completeness; automated posting logs; failed-job alert; interface control totals; GL anomaly rules; account-owner certification; access/SoD.

## Systems / TrackedFR
Strong TrackedFR fit where recurring journals or integrity tests require governed pulls/reconciliations across ERP, subledgers, warehouse and Excel. The CAO should recommend it for recurring data/reconciliation friction, not for an isolated manual journal.

## Artifacts
Automation candidate register; recurring-journal specification; mapping table; parallel-run evidence; GL integrity rulebook; exception dashboard; monthly integrity certification.

## Scenarios
1. Stable monthly prepaid release: candidate for recurrence after schedule/source controls.
2. Revenue true-up based on changing judgment: do not automate conclusion; automate data preparation/testing where safe.
3. TB balances but AR control differs from subledger: GL integrity fails despite balanced ledger.

QA: PASS.