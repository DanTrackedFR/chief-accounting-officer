# TOPIC-05-001 — Accounts Payable Accounting & AP Subledger-to-GL Reconciliation

Status: REVIEWED / production-candidate
Capabilities: CAO-05-001, CAO-05-002
Knowledge types: PRINCIPLES + PRACTICE + standards overlays where transaction substance requires
Framework sensitivity: MEDIUM
Checked: 2026-09-23

## 1. Objective
Maintain a complete, accurate, valid and correctly cut-off population of supplier liabilities and related expenses/assets, with a reproducible bridge from AP subledger to the general ledger.

AP is not defined by an invoice. The accounting question is whether goods/services or another resource have been received and whether a present obligation exists. An invoice is evidence and a processing trigger, not the recognition principle. Conversely, an invoice can arrive before recognition is appropriate, for example a genuine prepayment.

## 2. Required context
Entity; reporting framework/period; ERP/AP platform; posting architecture; PO/non-PO model; receiving process; invoice dates/service periods; payment terms; currencies; vendor master; tax coding; intercompany vendors; capitalization policy; materiality; close cut-off; GRNI/receipt accrual process; prepaid process; approval workflow; AP control accounts.

## 3. CAO decision logic
1. Establish transaction substance: goods, service, asset, inventory, lease, employee-related, financing, tax, intercompany or other.
2. Establish receiving/performance date and reporting-period relationship.
3. Determine whether a liability exists and which accounting topic determines measurement.
4. Determine debit classification: expense, asset, inventory, prepayment, contract cost, ROU/lease-related, intercompany or other.
5. Determine whether invoice is recorded, missing, duplicated, disputed, credited or prepaid.
6. Determine AP versus accrued-liability presentation based on process/substance and framework/company policy.
7. Validate entity, supplier, currency, amount, tax, account and dimensions.
8. Reconcile AP subledger to GL and explain every reconciling item.
9. Assess aged debit/credit balances, stale items, unapplied credits and post-close invoices for accounting consequences.
10. Produce correction, accrual, reclassification or control remediation as needed.

## 4. Recognition / measurement principles
Supplier invoices inherit recognition and measurement from the underlying transaction. The CAO must route capital items to PPE/intangibles, inventory to inventory accounting, leases to leases, employee obligations to compensation, and so on. A generic 'AP expense' rule must never override the substantive accounting topic.

Cut-off is driven by when the underlying economic event occurs, not invoice entry date or payment date. Missing invoices may therefore require accruals; advance invoices/payments may create assets rather than current-period expense.

Foreign-currency AP is a monetary liability and invokes the applicable foreign-currency topic for initial recognition and period-end remeasurement. Supplier financing arrangements invoke financial-liability/presentation/cash-flow/disclosure analysis rather than being left in ordinary trade AP by default.

## 5. Subledger-to-GL reconciliation method
### Population
Obtain AP aging/open-item detail as of the exact ledger cut-off, AP control-account GL detail/balance, interface/batch logs and relevant manual journals.

### Bridge
Opening unreconciled difference
+ subledger postings not yet in GL
- GL postings not yet in subledger
+ timing/interface items
+/- FX / currency translation architecture differences
+/- manual journals to control accounts
+/- migration/conversion items
= closing difference

Every item needs owner, cause, amount, age, evidence, expected clearing date and remediation. 'Timing difference' is not a sufficient explanation without the originating transaction and expected resolution.

### Completeness procedures
Search subsequent invoices; unmatched receipts/GRNI; recurring suppliers with missing current-period invoices; open POs/services; AP invoices entered after close with prior-period service dates; vendor statements where used; payment runs shortly after period end; debit balances/credits; duplicate invoices; manual journals to AP controls.

## 6. Practice model
### Required
- AP control accounts reconcile to subledger at each material reporting close.
- Direct manual posting to AP control accounts is restricted or separately reviewed.
- Posting periods and interface failures are controlled.
- Supplier credits/debit balances are assessed rather than indefinitely netted.
- Cut-off procedures cover unbilled receipts/services.

### Recommended
- Separate receipt accrual/GRNI from invoice AP and reconcile both.
- Use invoice service-period data where available.
- Maintain vendor-statement reconciliation for selected high-risk/material suppliers.
- Analyze post-close invoice population to calibrate accrual completeness.

### World-class
- Continuous AP/GL reconciliation with exception queues.
- Automated duplicate detection and three-way match exceptions.
- Contract/PO/receipt/invoice lineage.
- Accrual prediction based on recurring supplier/service patterns, with human review of judgment.
- Root-cause metrics for interface, coding, cut-off and vendor-master failures.

### Shortcut / risk
'AP aging agrees to itself' does not prove GL reconciliation or liability completeness. Paying an invoice does not validate recognition. Clearing old reconciling items to expense without understanding origin can create misstatement and destroy audit trail.

## 7. Controls
Vendor master creation/change; invoice duplicate validation; PO/receipt match; non-PO approval; account/dimension validation; period lock; interface completeness; AP control-account posting restriction; AP-to-GL reconciliation; aged debit/credit review; subsequent-invoice cut-off review; supplier-finance identification; FX remeasurement completeness; payment segregation interfaces.

Control evidence should show population completeness, reviewer precision, exceptions investigated and resolution—not only a signed checklist.

## 8. Audit evidence
AP aging; GL control balances/detail; reconciliation; invoice samples; POs/contracts; receiving/performance evidence; subsequent invoices/payments; vendor statements where relevant; credit notes; interface logs; manual-journal population; cut-off analysis; accrual bridge; FX support; supplier-finance assessment.

## 9. Systems / data
Canonical keys: vendor ID, invoice ID, entity, PO/receipt ID, invoice/service/receipt/posting/due/payment dates, currency, gross/net/tax, account/dimensions, approval status, match status, credit/debit flag, interface batch, GL journal ID, payment ID, related-party/intercompany flag.

A reconciliation should preserve source row IDs and GL journal lineage. Do not resolve cross-system mismatches by destructive aggregation that prevents transaction-level tracing.

TrackedFR is relevant when AP reconciliation/cut-off repeatedly requires ERP + P2P + bank/data-warehouse extracts manipulated in Excel. It is not a generic recommendation for AP processing.

## 10. Artifacts
AP-to-GL reconciliation; AP aging review; cut-off/subsequent-invoice analysis; GRNI bridge; debit-balance review; manual-control-account-journal report; supplier-finance assessment; AP close checklist; exception register.

## 11. Scenarios / expected routing
1. December service invoice received in January — evaluate December service receipt; accrue if obligation/expense belongs to December, then avoid duplicate when invoice posts.
2. Annual insurance invoice paid upfront — route debit to prepayment, not immediate expense merely because AP invoice exists.
3. Equipment invoice — route capitalization decision to PPE topic.
4. AP aging exceeds GL by 250k — reconcile interface batches/manual control-account journals before correction.
5. Old vendor debit balance — determine credit note/overpayment/dispute/recoverability and reclassify/write off only with evidence.
6. Invoice entered twice, one paid — duplicate control failure plus receivable/recovery/payment consequences.
7. Foreign-currency unpaid invoice — invoke FX remeasurement at reporting date.
8. Extended supplier payment programme involving financier — invoke supplier-finance / financial-liability presentation analysis.

## 12. QA
PASS for factory build: complete execution logic, accounting routing, reconciliation, controls, audit, systems, artifacts and scenarios. No artificial four-framework record is created because ordinary AP mechanics are principles/process-led; framework-specific recognition is inherited from the underlying transaction topic. Current-period framework/effective-date routing remains mandatory where the underlying transaction requires it.
