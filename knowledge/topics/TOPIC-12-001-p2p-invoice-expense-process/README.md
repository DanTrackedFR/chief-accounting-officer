# TOPIC-12-001 — Procure-to-Pay / Invoice-to-GL / Expense Management Accounting Process

Status: REVIEWED / production-candidate
Primary capabilities: CAO-12-001, CAO-12-002, CAO-12-003
Knowledge types: PRINCIPLES, PRACTICE; STANDARDS routed to recognition/cut-off topics

## Objective
Design and operate the accounting layer from purchase initiation through invoice, approval, posting, payment and GL close so completeness, cut-off, classification, authorization and evidence are controlled without turning the CAO into procurement operations.

## CAO boundary
The CAO owns accounting requirements, posting logic, period-end completeness, reconciliation, control design and evidence. Procurement owns sourcing/commercial approval; treasury owns payment execution and liquidity; tax specialists own tax compliance. Their outputs are inputs to accounting.

## End-to-end model
1. Establish vendor/master-data and coding requirements.
2. Capture PO/contract/receipt/invoice/expense evidence with stable IDs.
3. Validate entity, supplier, amount, currency, dates, dimensions, duplicate indicators and approval authority.
4. Determine accounting date and recognition/cut-off route; do not equate invoice date with recognition date.
5. Match PO/receipt/invoice where applicable; route non-PO and exceptions separately.
6. Post AP/expense/asset/prepayment/accrual consequences using approved accounting rules.
7. Maintain invoice-to-ERP lineage and payment-status linkage.
8. At close, prove completeness using open POs/receipts, post-period invoices, recurring suppliers, unmatched receipts and unbilled services.
9. Reconcile AP subledger, GRNI/receipt accruals, expense platforms and GL.
10. Age and resolve reconciling items; certify with preparer/reviewer evidence.

## Decision logic
For each transaction ask: what was received and when; which entity received it; is an obligation present; is the item expense, asset, prepayment or other; what dimensions apply; is invoice evidence complete; is there a duplicate/credit; is period cut-off correct; does an estimate/accrual remain necessary? Recognition/measurement questions route to the relevant standards-sensitive topic rather than being reinvented here.

## Core controls
Vendor-master change segregation; duplicate invoice detection; approval thresholds; three-way-match tolerance governance; non-PO exception approval; posting-period controls; restricted manual overrides; payment-to-ledger interface completeness; AP-subledger-to-GL reconciliation; GRNI aging; post-close invoice lookback; vendor statement reconciliation for risk-selected suppliers; stale debit/credit review; access and change logging.

## Data & systems
Minimum lineage keys: legal entity, vendor ID, PO/contract ID, receipt/service period, invoice ID, source-system record ID, accounting document ID, GL account/dimensions, currency, approval, payment ID, posting period. Interface controls prove population completeness before testing match rate. Exceptions must remain traceable to source and resolution.

## Documentation / artifacts
P2P accounting narrative; accounting requirements matrix; coding guide; cut-off procedure; exception taxonomy; AP/GRNI reconciliations; close checklist; control evidence; aging/action log; system-interface map.

## TrackedFR applicability
Assess when AP/PO/receipt/expense-platform data must repeatedly be reconciled to ERP/GL in Excel or similar analysis. Do not recommend solely because spreadsheets exist.

## Failure modes
Invoice-date accounting; missing service-period logic; treating approval as recognition evidence; unexplained unmatched receipts; manual journals masking interface failures; netting vendor debits without support; high match-rate claims without proving source completeness.

## Scenario tests
A December service invoice arrives in January: route to cut-off/accrual analysis and preserve later invoice linkage. A PO receipt exists without invoice: assess GRNI/accrual, age and reconcile. Expense platform posts summarized journals: prove source population to batch to GL and retain employee/receipt lineage.

## Completion criteria
CAO can map a P2P flow, identify missing evidence, define accounting requirements and controls, design close completeness tests, reconcile source-to-GL, route technical questions, document exceptions and propose automation without taking over procurement/payment operations.