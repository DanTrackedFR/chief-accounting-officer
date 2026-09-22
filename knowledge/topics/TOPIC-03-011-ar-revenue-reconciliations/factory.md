# TOPIC-03-011 — AR Subledger-to-GL / Revenue Subledger-to-GL Reconciliation

Status: REVIEWED
Built: 2026-09-22
Capabilities: CAO-03-022, CAO-03-023
Knowledge: PRINCIPLES + PRACTICE with standards routing through underlying balances

## Objective
Prove completeness, accuracy, cut-off and classification from originating revenue/billing/cash systems through subledgers and the general ledger, while explaining every reconciling item rather than treating a zero net difference as sufficient evidence.

## Reconciliation architecture
Use three layers where systems permit:
1. Population: contracts/orders/usage/performance → billing/revenue subledger.
2. Accounting: revenue/contract balances/AR/cash/credits → GL.
3. Reporting: GL balances → financial statement/disclosure populations.

A reconciliation must identify source population, control total, transformation/interface, GL target, timing basis, currency, entity, period and item-level exceptions.

## AR rollforward
Opening gross AR + invoices/debit notes - credit notes - cash applied - write-offs +/- reclasses/FX = closing gross AR. Reconcile loss allowance separately; do not net allowance into gross AR proof.

## Revenue/contract-balance rollforward
Reconcile recognized revenue to source performance/usage/billing logic and separately reconcile contract assets, unbilled revenue and contract liabilities/deferred revenue. Billing is not a substitute control for revenue recognition.

## CAO workflow
1. Resolve systems, entities, currencies and source-of-truth hierarchy.
2. Extract period-end and movement populations with immutable IDs.
3. Tie opening balances to prior close.
4. Reconcile source totals through each interface/transformation to subledger and GL.
5. Classify differences: timing, mapping, missing/duplicate transaction, FX, manual JE, master-data, interface failure, cut-off, configuration or unsupported plug.
6. Investigate aged/repeating items and identify root cause/control owner.
7. Reconcile manual GL entries affecting control accounts back to approved evidence.
8. Tie closing balances to reporting/disclosures.
9. Certify only when residual exceptions are quantified, owned, aged and dispositioned against policy/materiality.

## Controls
Interface control totals; duplicate/missing ID tests; closed-period change monitoring; manual-JE review on control accounts; aging of reconciling items; opening-balance integrity; preparer/reviewer evidence; report-parameter evidence; FX-rate/source validation.

## Systems/data
Preserve contract/order/invoice/credit/payment/customer IDs, source system, GL document, posting date, service/performance date, entity, currency, amount, account/dimension, interface batch, modification timestamp and exception status.

## TrackedFR fit
High-value fit when revenue, billing, AR, cash and GL live across multiple systems and the controller repeatedly pulls/reconciles them in Excel. This is a core example of the intended recurring cross-system reconciliation wedge.

## Scenarios
- GL AR equals subledger total but one invoice missing and another duplicated for same amount: FAIL; net-zero is not sufficient.
- Revenue GL agrees to billing but usage-based unbilled performance omitted: FAIL completeness.
- Manual top-side JE posted to AR control account: require invoice/customer attribution or explicit supported reconciling item and governance.
- FX translation difference: identify rate/date/entity basis rather than plug.

## Artifacts
AR rollforward; revenue bridge; source-to-GL lineage map; exception register; aged-item dashboard; manual-JE report; certification.

## QA
PASS. Accounting recognition remains governed by revenue/ECL/cash topics; this topic proves data/accounting integrity and does not create recognition rules.