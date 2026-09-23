# TOPIC-02-006 — Suspense & Clearing Accounts / Cut-Off Accounting

Status: REVIEWED
Capabilities: CAO-02-013, CAO-02-014
Knowledge types: PRINCIPLES, PRACTICE; standards inherited from transaction-specific topics
Framework sensitivity: MEDIUM

## Objective
Prevent temporary holding accounts from becoming permanent unexplained balances and ensure transactions are recognized in the correct reporting period based on the underlying accounting event rather than invoice/payment timing alone.

## Suspense and clearing accounts
Every account needs a defined purpose, permitted transaction types, expected clearing mechanism/time, owner, reconciliation source and escalation threshold. Distinguish legitimate timing clearing from unknown/unclassified suspense.

### CAO method
1. Reconcile opening + inflows - clearings = closing.
2. Trace material/aged items to source transaction.
3. Classify reason: timing, mapping, missing master data, interface failure, unmatched cash, unidentified counterparty, posting error or true accounting judgment.
4. Determine correct destination/accounting and period.
5. Clear via supported entry; never write off solely because item is old.
6. Root-cause recurring items and fix upstream process/system.

## Cut-off accounting
Cut-off follows the recognition point for the underlying asset, liability, income or expense under the applicable framework/topic. Invoice date, PO date, cash date and system posting date are evidence but are not universally the recognition date.

### Cut-off evidence by flow
P2P: receipt/performance evidence, service period, GRNI/receipts, invoice, contract/PO. Revenue: performance/transfer evidence and contract terms. Payroll: service period and earned compensation. Assets: control/availability-for-use evidence. Cash: bank value/settlement and in-transit facts. Inventory: shipping terms/control and physical movement. Intercompany: both counterparties use consistent event facts.

## Close procedures
Define pre/post-period sample windows based on risk; inspect subsequent invoices/credits/cash where relevant; compare receiving and invoice dates; analyze late-posted journals; review unmatched receipts and goods/services received; investigate unusual reversals; quantify proposed cut-off adjustments.

## Required vs practice
Recognition rules come from the applicable accounting topic. Sample windows, exception thresholds, GRNI aging and suspense SLAs are process/control choices and must not be presented as accounting-standard prescriptions.

## Controls
Interface completeness; suspense aging; unmatched-item escalation; receiving completeness; invoice cut-off testing; late-journal review; period locks; documented estimates for unbilled/uninvoiced activity; post-close true-up analysis.

## Failure modes
Using invoice date as universal expense date; clearing suspense to miscellaneous expense without investigation; netting unrelated items; ignoring credits after period end; forcing operational cutoff earlier without accrual mechanism; recurring GRNI balances never validated to actual receipt obligations.

## Artifacts
Suspense policy; clearing-account inventory; aging dashboard; cut-off checklist; period-end evidence pack; subsequent-invoice analysis; adjustment log; root-cause backlog.

## Scenarios
1. December service invoiced January: determine December obligation from service facts; do not wait for invoice if recognition criteria met.
2. Cash received Dec 31 but unidentified until Jan 4: cash may exist at period end while customer allocation remains clearing/unapplied; investigate presentation.
3. Three-year-old suspense debit: age is a red flag, not evidence supporting write-off.

QA: PASS; transaction-specific recognition remains delegated to relevant standards topic.