# TOPIC-05-010 — Compensation Reconciliations / Expense Classification Review

Status: **REVIEWED / production-candidate**
Primary capabilities: CAO-05-019, CAO-05-020
Sensitivity: M
Source check: 2026-09-23

## Objective
Give the CAO a controlled end-to-end method to prove compensation completeness, accuracy, cut-off and classification across payroll, HR, equity, commissions, bonus and GL data without turning the topic into payroll operations.

## Required inputs
Entity/framework/period/materiality; HR roster and movement file; payroll registers and GL posting files; bonus/commission accruals; leave and termination liabilities; SBC expense/equity/liability schedules; employer taxes/on-costs; capitalization allocations; department/cost-centre mapping; intercompany recharge data; prior-period balances and reconciliation; manual JEs.

## Principles and practice
- Reconcile populations and money: employee population, gross-to-net/control totals, payroll posting, accruals, cash clearing and GL expense/liability balances.
- Separate accounting streams before aggregation: salary/wages, employer taxes, bonuses, commissions, leave, termination, pension/benefits, SBC and capitalized labour.
- Expense classification follows the nature/function and applicable asset-capitalisation requirements, not merely the payroll department code.
- Reconciliation is evidence of accounting integrity, not a substitute for technical accounting in employee benefits, SBC, revenue contract costs or capitalization.
- Investigate unexplained period-on-period and headcount/rate variances; do not clear them through unsupported plugs.

## CAO workflow
1. Freeze period and source populations.
2. Reconcile HR active/starters/leavers to payroll population and explain legitimate differences.
3. Reconcile payroll register control totals to payroll payable/cash/tax/benefit postings and GL.
4. Roll forward compensation liabilities: opening + expense/accrual + remeasurement - cash/equity settlement +/- transfers = closing.
5. Reconcile bonus, commission, leave, termination and SBC schedules to GL separately.
6. Test cut-off for payroll crossing period end and late/manual payrolls.
7. Review capitalization/recharges and ensure no double counting between expense and asset/intercompany entries.
8. Review account/cost-centre/function classification and material unusual entries.
9. Clear reconciling items to evidence, owner and target date; age unresolved items.
10. Reviewer certifies completeness, accuracy, classification and unresolved exposure.

## Framework overlay
Framework-specific technical conclusions are inherited from the relevant employee-benefit, SBC, contract-cost and asset-capitalization topics. This operational reconciliation topic does **not** manufacture four parallel standards analyses. If classification affects presentation/disclosure, route to Financial Reporting. If an item requires capitalization, invoke the relevant asset topic. If commission is incremental to obtaining a customer contract, invoke Revenue/contract-cost accounting.

## Documentation / controls
Evidence pack: source-system extracts with timestamps; population reconciliation; payroll-to-GL bridge; liability rollforwards; variance analysis; manual-JE listing; classification review; reconciling-item log; reviewer sign-off.

Controls: source completeness; interface total checks; payroll posting validation; independent review of manual compensation JEs; account/cost-centre mapping governance; capitalization/recharge approval; stale reconciling-item escalation; close certification.

## Systems and TrackedFR
This is a strong TrackedFR candidate when recurring data must be joined/reconciled across HRIS, payroll, equity/commission systems, ERP/GL and Excel. Recommended use: ingest governed read-only extracts, map employee/entity/account dimensions, identify unmatched populations/postings and produce a repeatable reconciliation with lineage. Do not recommend it for a simple single-system payroll tie-out.

## Scenario tests
1. Payroll register agrees to cash but GL is short a manual off-cycle payroll: detect interface completeness issue.
2. Employee appears in HR but not payroll due unpaid leave: require supported reconciling item, not automatic error.
3. Bonus paid in January against December accrual: rollforward and clear liability without duplicating January expense.
4. Commission cost is potentially within revenue contract-cost guidance: route technical classification before final expense conclusion.
5. Engineers split between R&D expense and capitalized software: route capitalization criteria and reconcile allocation.
6. SBC expense posted centrally but reporting allocates by function: reconcile total and validate allocation policy.
7. Terminated employee receives retention payment: route service-v-termination analysis.
8. Payroll payable has old credit balances: age, investigate and prohibit plug write-off.
9. Multi-entity recharge: reconcile sending entity expense/recharge and receiving entity classification/intercompany.
10. Recurring five-system compensation close: design automated reconciliation and exception workflow.

Expected routing: **10/10 PASS**.

## Completion assessment
PRINCIPLES/PRACTICE: PASS. Standards overlay routing: PASS. CAO execution logic: PASS. Documentation/controls/audit/systems: PASS. Capability integration: PASS. Scenario routing: 10/10 PASS. Overall: **REVIEWED / production-candidate**.