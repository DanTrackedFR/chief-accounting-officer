# TOPIC-11-005 — ERP Migration & Cutover / Opening Balance Validation

Status: REVIEWED / production-candidate
Primary capabilities: CAO-11-013, CAO-11-014
Sensitivity: M

## Objective
Move accounting records to a new system without losing balance integrity, transaction lifecycle, historical lineage, accounting basis, reconciliation status or evidence.

## Core rule
A migration is an accounting event only if the underlying economics/accounting change. A system move should ordinarily preserve accounting. Any migration adjustment must therefore be separately identified, explained, approved and supported; “migration difference” is not an acceptable accounting rationale.

## Migration populations
Classify what moves: GL opening balances; comparative/history; open AP/AR; cash items; fixed assets and accumulated depreciation; leases; inventory; payroll balances; revenue/contract assets/liabilities; debt/instruments; intercompany; tax/accounting balances where in CAO remit; master data; recurring journals; allocations; reconciliations; and supporting attachments/evidence.

For each population define source-of-truth, extraction date, cutoff, grain, transformation, target object, key crosswalk, expected totals, currency, retained history, owner and acceptance test.

## CAO cutover workplan
1. Freeze target design and mappings before final migration.
2. Approve source populations and cutoff timetable.
3. Extract with reproducible parameters and control totals.
4. Validate mapping/transformation outside target load.
5. Load using unique run/batch IDs.
6. Reconcile source → transformation → load → target ledger/subledger.
7. Reconcile subledgers to GL and GL to signed/approved closing trial balance.
8. Validate retained earnings/current-year result, CTA/FX reserves, equity, intercompany and control accounts explicitly.
9. Sample transaction-level lineage and open-item lifecycle.
10. Validate period locks, recurring entries, interfaces and reports.
11. Obtain accounting acceptance before production close.
12. Track hypercare exceptions without obscuring opening-balance baseline.

## Opening-balance validation
Minimum evidence: signed source TB; target opening TB; account/entity/currency crosswalk; unmapped/multi-mapped account report; zero-balance and inactive-account treatment; retained-earnings bridge; subledger/control-account reconciliations; intercompany reciprocal match; balance-sheet rollforward continuity; historical FX/reserve treatment; migration journals; and proof that debits equal credits by relevant book/entity/currency basis.

Balance equality alone is insufficient. Validate accounting classification, entity, currency, dimensions, open-item status, due dates, asset lives, lease terms, contract positions and other attributes needed for future accounting.

## Migration adjustments
Maintain a separate adjustment register with amount, accounts, entity, cause, whether correction of source accounting vs mapping/load issue, framework analysis if accounting changes, approver, journal ID and evidence. Never net unrelated migration differences into retained earnings or suspense merely to make the load balance.

## Cutover controls
Restricted configuration changes; source/target freeze windows; controlled late transactions; numbered extraction/load runs; hash/control totals; independent review; failed-record queue; duplicate detection; rollback plan; reconciliation sign-off; post-go-live interface monitoring; and first-close enhanced review.

## Failure modes
Loading only net balances when open items are needed; changing COA and accounting policy simultaneously without bridge; losing historical asset cost/depreciation; AR/AP balances that agree in total but lose invoice identity; unexplained retained-earnings plugs; historical currency conversion using current rates; duplicate cutover transactions; source remains active after target starts; no proof of which extraction was loaded.

## Artifacts
Migration accounting plan; population inventory; mapping/crosswalk; extraction manifest; transformation specification; load manifest; opening-balance workbook; subledger reconciliations; adjustment register; cutover checklist; acceptance memo; hypercare issue log.

## TrackedFR applicability
Strong where migration validation requires repeated cross-system extracts, mapping, reconciliation and exception analysis in Excel across legacy and target finance systems. Use it for governed reconciliation/manipulation, not as the migration engine itself.

## Scenario tests
- Legacy AR total equals target but 14 invoices are duplicated and 14 omitted: record-level completeness test catches failure.
- Old and new COA differ: crosswalk supports one-to-many only with deterministic rule and aggregate proof.
- Historical fixed assets loaded at NBV only: challenge if future depreciation, disposal, disclosure or audit requires original cost/accumulated depreciation history.
- Go-live mid-month: explicitly define ownership of transactions around cutoff and reconcile sequence numbers/timestamps across both systems.

## Completion criteria
CAO can define migration populations, control every transformation, prove opening balances at aggregate and relevant transaction level, isolate true accounting adjustments, approve/reject cutover, and preserve a reproducible evidence chain into the first production close.