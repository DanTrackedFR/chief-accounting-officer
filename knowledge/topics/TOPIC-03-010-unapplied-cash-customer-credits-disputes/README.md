# TOPIC-03-010 — Unapplied Cash, Customer Credit Balances & Dispute Accounting

Status: REVIEWED
Capabilities: CAO-03-020, CAO-03-021
Knowledge: PRINCIPLES + STANDARDS + PRACTICE
Framework sensitivity: Medium

## Objective
Account correctly for customer cash and credit positions that cannot yet be matched to receivables, and separate commercial disputes from accounting errors, concessions, refunds, ECL events and contract modifications.

## Principles
Cash receipt does not itself prove revenue. An unmatched receipt is a liability/credit position or reduction of a valid receivable only when the entity has support for that treatment. Customer credits should not be netted against unrelated receivables merely to make aging cleaner. A dispute is a fact pattern requiring classification, not an accounting account.

## CAO workflow
1. Reconcile bank receipt to cash ledger and cash-application system.
2. Identify payer/customer/entity/currency and remittance evidence.
3. Search open invoices/contract balances using amount, reference and timing.
4. If unmatched, record/retain a separately identifiable customer credit/unapplied-cash position under the entity's accounting policy and applicable presentation requirements.
5. Age the item and establish refund, application or investigation path.
6. For disputes, determine cause: billing error; service/product claim; price concession; rebate/credit; contract modification; return/refund; collectibility/ECL; duplicate invoice; cash application; legal claim.
7. Route to revenue, ECL, provision/contingency, error or contract-modification topic as facts require.
8. Resolve source record and GL consistently; retain customer communication/evidence.

## Framework routing
Revenue-related concessions/refunds/modifications route to IFRS 15/ASC 606/revised FRS 102 Section 23/AASB 15 as applicable. Credit deterioration routes to IFRS 9/ASC 326 or applicable UK/Australian financial-instrument model. Legal claims can invoke provisions/contingencies. Presentation and offsetting require framework-specific support; operational convenience is not a basis for netting.

## Controls
Daily/periodic unapplied-cash aging; remittance capture; customer-master validation; refund approval; no unauthorized write-off/netting; dispute reason codes; SLA/escalation; credit-note linkage; AR/GL reconciliation; stale-credit review including unclaimed-property/escheat jurisdiction routing where applicable.

## Systems/data
Receipt ID, bank reference, payer, customer, invoice, currency, amount, receipt date, application date, dispute code, owner, evidence, refund/credit ID, GL account and resolution reason. Preserve one-to-many/many-to-one applications.

## Artifacts
Unapplied cash aging; customer credit rollforward; dispute register; accounting conclusion memo for material disputes; refund/credit pack; reconciliation.

## Scenarios
Customer prepays before performance: do not recognize revenue solely because cash arrived. Customer shorts invoice alleging SLA failure: determine contractual credit/variable-consideration treatment versus collectibility. Old credit cannot be tied to customer: do not sweep to revenue without legal/accounting analysis. Customer disputes duplicate invoice: correct billing/source and AR rather than create ECL on an invalid receivable.

## TrackedFR fit
High where bank, payment processor, AR/billing and ERP data require recurring matching and exception management in Excel.

## QA
PASS at REVIEWED level. Jurisdiction-specific unclaimed-property rules are outside the generic accounting record and must route to jurisdiction knowledge.