# TOPIC-12-003 — Collections Interface / Payroll Accounting Process / Payroll-to-GL Reconciliation

Status: REVIEWED / production-candidate
Primary capabilities: CAO-12-007, CAO-12-008, CAO-12-009

## Objective
Define accounting interfaces around collections and payroll without absorbing collections strategy or HR/payroll operations.

## Collections-to-accounting
Collections activity provides evidence about disputes, recoverability, credits and customer status. Accounting consumes that evidence for AR application, write-off, ECL/doubtful-debt and revenue/contract assessments. Collection promises do not override impairment evidence. Maintain customer/item-level linkage between collector notes, disputes, credits, receipts and accounting conclusions.

Controls: restricted write-off authority; credit memo governance; dispute coding; collections-to-AR status reconciliation; aging integrity; subsequent-receipt evidence; escalation of deterioration to ECL; no deletion of aged items merely to clean operational queues.

## Payroll accounting process
1. Lock employee/entity/pay-period population and payroll-run ID.
2. Reconcile approved HR/payroll inputs to processed population.
3. Validate gross-to-net control totals and employer costs.
4. Map wages, bonuses, commissions, benefits, taxes/deductions and liabilities to approved GL/dimensions.
5. Separate cash payroll from equity compensation and other technical accounting routes.
6. Interface payroll journal with run-to-batch-to-GL lineage.
7. Record accruals for earned/unprocessed compensation where required by the applicable topic.
8. Reconcile payroll clearing, payable, tax/deduction liabilities and cash settlement.
9. Investigate off-cycle/manual runs, reversals and stale balances.

## Boundaries
HR owns employee records and compensation administration. Payroll operations owns calculation/execution. Treasury owns cash execution. CAO owns accounting classification, cut-off, reconciliation, evidence and financial-reporting consequences.

## Controls
Run authorization; population completeness; change reports; privileged-access review; gross-to-net control totals; GL mapping governance; interface completeness; manual journal restriction; clearing-account aging; payroll-bank reconciliation; terminated-employee anomalies; off-cycle review; period-end accrual completeness.

## Data lineage
Employee ID may be sensitive and should be access-controlled, but accounting requires durable run-level lineage: entity, pay period, earning/deduction code, cost center, payroll run, accounting batch, GL posting and settlement. Aggregation must remain drillable under authorized access.

## Artifacts
Payroll accounting matrix; payroll-to-GL reconciliation; clearing-account reconciliation; accrual support; exception log; collections/ECL handoff; control evidence.

## Scenarios
Bonus approved after payroll cutoff but earned pre-close: route to bonus/accrual topic, not simply next payroll. Collector marks invoice disputed: accounting evaluates credit/revenue/ECL consequences rather than auto-writing off. Payroll batch differs from bank settlement due to rejected payment: isolate clearing item and preserve liability until resolved.

## Completion criteria
CAO can run accounting interfaces and reconciliations while respecting operational boundaries, route technical compensation/ECL issues correctly, and preserve source-to-GL evidence.