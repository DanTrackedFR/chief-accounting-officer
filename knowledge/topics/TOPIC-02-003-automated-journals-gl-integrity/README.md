# TOPIC-02-003 — Recurring/Automated Journals & GL Integrity

Status: REVIEWED — Phase 2D
Primary capabilities: CAO-02-007, CAO-02-008

## Recurring/automated journal design
A recurring journal is appropriate when accounting logic, source, frequency and dimensions are stable enough to encode. Automation does not remove ownership.

Design record: objective; accounting policy/topic; source dataset; transformation/calculation; posting cadence; entity/book; accounts/dimensions; rounding; FX; reversal; exception rules; owner; reviewer; change control; reconciliation/control dependency.

Automated output should fail closed or route exceptions when required source data is incomplete, duplicated, stale or outside tolerance. Material manual overrides are logged and reviewed.

## GL integrity model
CAO reviews whether the ledger is structurally capable of producing reliable accounting outputs:
- debits equal credits and posting batches complete;
- opening + movement = closing by account/entity/currency where relevant;
- subledger/control accounts reconcile;
- suspense/clearing aged and owned;
- invalid/retired accounts or dimensions blocked;
- intercompany pairs and eliminations identifiable;
- posting periods and books correctly controlled;
- unusual/late/manual activity surfaced;
- retained earnings/opening balances roll correctly;
- source-to-ledger interfaces complete and unique.

## Controls
Automated journal configuration approval; test evidence before release; version/change log; source completeness; batch control totals; duplicate prevention; posting error queue; post-run reconciliation; access segregation; periodic logic recertification.

## Systems/data
Preserve source record ID → transformation/run ID → journal batch → journal line → GL balance lineage. A journal that cannot be traced back to its source population is not world-class automation.

## Scenarios
1. Monthly amortization journal: automate only after schedule/source completeness and reversal/termination behavior are defined.
2. Interface posts twice: detect via source/batch uniqueness and control totals; reverse duplicate with evidence.
3. Account suddenly carries opposite-sign balance: investigate source/journal activity rather than mechanically reclassifying.
4. Automation saves time but produces unexplained plug: reject design; automation must preserve accounting lineage.

## TrackedFR fit
Strong fit when integrity/reconciliation requires recurring cross-system extraction and comparison in Excel; otherwise use native ERP controls where sufficient.
