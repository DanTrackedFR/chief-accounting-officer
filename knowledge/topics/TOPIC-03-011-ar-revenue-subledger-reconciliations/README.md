# TOPIC-03-011 — AR and Revenue Subledger-to-GL Reconciliations

Status: REVIEWED
Capabilities: CAO-03-022, CAO-03-023
Knowledge: PRINCIPLES + PRACTICE
Framework sensitivity: Low, with accounting-topic routing for reconciling items

## Objective
Prove completeness and accuracy of AR and revenue accounting across operational source, subledger, GL and reporting layers; identify timing versus error; drive reconciling items to resolution.

## Reconciliation architecture
A strong reconciliation proves populations and movements, not only ending balances. For AR: opening AR + invoices/receivables created - cash applied - credits/write-offs +/- FX/reclasses = closing AR, reconciled by customer/entity/currency as appropriate. For revenue: source performance/delivery events and revenue-subledger movements reconcile to GL revenue, contract assets/liabilities and related adjustments.

## CAO method
1. Define systems of record and reconciliation boundary.
2. Freeze period/version and record extraction timestamps.
3. Reconcile record counts/control totals before balance comparison.
4. Map source/subledger accounts, entities, currencies and dimensions to GL.
5. Reconcile opening balance and period movement categories to closing balance.
6. Identify unmatched/mismatched items using stable transaction/contract/customer IDs.
7. Classify exceptions: timing; mapping; interface rejection; duplicate/missing record; manual JE; FX; master-data issue; accounting judgment; write-off/credit; cash-application issue.
8. Determine accounting impact and materiality; route technical items to the owning topic.
9. Correct source/process where possible rather than repeatedly patching GL.
10. Age and certify unresolved items; evidence reviewer challenge.

## Revenue-specific tests
Contract/subscription/order population to billing/revenue engine; revenue engine to GL; manual revenue journals; deferred revenue/contract liability rollforward; unbilled/contract asset rollforward; credits/refunds; modifications; cut-off; currency; acquired/migrated contracts; disclosure population.

## AR-specific tests
AR subledger control account; customer debit/credit balances; unapplied cash; credit notes; write-offs/recoveries; FX remeasurement; intercompany/customer master anomalies; aging-to-GL; ECL allowance presentation and separate reconciliation.

## Controls
Automated interface control totals; reconciliation completeness register; preparer/reviewer separation; materiality/aging policy; manual-JE overlay; stale-item escalation; source-correction tracking; post-close item monitoring; certification.

## Evidence
Extraction parameters; source reports; mapping table; movement bridge; exception population; supporting documents; correction JE/source fix; aging; reviewer sign-off; subsequent clearing evidence.

## Systems/automation
Use immutable IDs and reproducible queries. Avoid manual copy/paste as the reconciliation key. Automate deterministic matching but preserve explainable exception categories and evidence. Monitor interface completeness independently from balance equality.

## TrackedFR fit
Very high: recurring reconciliation across billing/revenue subledger, AR, ERP/GL, bank and warehouse data in Excel is directly within the product wedge.

## Scenarios
GL equals AR subledger but one invoice duplicated in both after a failed interface retry: balance equality alone does not prove source completeness. Revenue engine differs from GL solely by approved manual acquisition true-up: reconcile and separately govern the journal. Aging total differs from AR GL due to unapplied cash excluded from aging: establish population definitions rather than force-match reports.

## QA
PASS. Framework-neutral reconciliation practice appropriately routes accounting treatment of exceptions to revenue, ECL, FX, errors, cut-off and other technical topics.