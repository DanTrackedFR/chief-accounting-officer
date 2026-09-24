# TOPIC-12-002 — Order-to-Cash / Billing-to-GL / Cash Application

Status: REVIEWED / production-candidate
Primary capabilities: CAO-12-004, CAO-12-005, CAO-12-006
Knowledge types: PRINCIPLES, PRACTICE; revenue recognition and ECL route to Domain 03

## Objective
Operate the accounting chain from commercial order/contract through billing, receivable, cash receipt, application and GL while keeping billing mechanics distinct from revenue recognition.

## Operating model
1. Ingest approved customer/contract/order facts and stable identifiers.
2. Establish billing trigger, invoice schedule, entity, currency, tax inputs and customer master.
3. Separately determine accounting recognition through the relevant revenue topic.
4. Create invoice/credit with contract/order lineage; interface to AR/GL with batch completeness.
5. Reconcile billed amounts to billing source and GL; reconcile revenue/deferred/contract-asset consequences separately.
6. Receive bank/processor/remittance data; match cash to customer/open items using governed rules.
7. Route short-pay, overpay, deductions, chargebacks, unidentified cash and FX differences to explicit queues.
8. Close: AR subledger-to-GL, unapplied cash, billing completeness, credit-note lookback and revenue/billing bridge.

## Critical distinctions
Invoice != revenue. Cash != revenue. Customer credit balance != automatically revenue reduction. A contract asset is not simply unbilled AR. Operational billing changes must not silently change accounting policy.

## Controls
Customer-master governance; approved billing triggers; invoice-sequence/completeness checks where relevant; price/quantity validation; credit-note approval; source-to-interface-to-GL control totals; AR-to-GL reconciliation; bank/processor completeness; automated-match rule governance; unapplied-cash aging; manual application approval; period lock; post-close credit-note review.

## Systems/data
Required lineage: entity, customer, contract/order, performance/billing reference, invoice/credit, accounting document, AR item, receipt, bank/processor transaction, application event and period. Automated matching stores rule/version/confidence and manual overrides.

## Artifacts
O2C accounting narrative; billing/revenue bridge; AR reconciliation; unapplied-cash aging; cash-application exception log; billing completeness test; interface lineage map; close certification.

## TrackedFR applicability
Strong candidate when CRM/billing/processor/bank/ERP datasets recur and require cross-system reconciliation or manipulation. Not a generic billing-system recommendation.

## Scenarios
Annual SaaS invoice paid upfront: billing and cash occur while revenue follows the applicable recognition pattern. Processor deposits net of fees: reconcile gross customer receipts, fees, refunds and settlement to bank/GL. Unidentified receipt at close: retain as unapplied cash/liability route until evidence supports application.

## Completion criteria
CAO can explain and test the billing/revenue/cash distinctions, prove interface completeness, design cash-application controls, reconcile O2C populations and route technical revenue/ECL conclusions to their authoritative topics.