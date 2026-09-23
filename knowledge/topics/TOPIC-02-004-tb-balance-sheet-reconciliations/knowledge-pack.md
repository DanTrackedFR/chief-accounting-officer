# TOPIC-02-004 — Trial Balance Review / Balance Sheet Reconciliations

Status: REVIEWED
Capabilities: CAO-02-009, CAO-02-010
Knowledge types: PRINCIPLES, PRACTICE
Framework sensitivity: LOW; balance-specific accounting inherits its standards topic.

## Objective
Prove material balance-sheet balances are complete, valid, accurately measured and understood, and identify ledger-level anomalies before reporting.

## Reconciliation standard
A reconciliation is an evidence-based comparison of a GL balance to an independent or sufficiently detailed substantiation source, with reconciling items individually explained, aged, owned and resolved. Merely reproducing the GL or rolling forward last month is not substantiation.

## CAO method
1. Confirm account/entity/period/currency and GL balance.
2. Identify appropriate substantiation source and its completeness.
3. Reconcile source total to GL.
4. Identify every reconciling item above defined risk/materiality criteria.
5. Classify timing, known adjustment, error, unsupported, stale or other.
6. Determine required journal/action and owner/date.
7. Test aging and stale-item policy.
8. Perform reasonableness/rollforward where useful.
9. Reviewer challenges source independence, unexplained items, stale items and unusual movements.
10. Certify only when completion criteria are met.

## TB review
Compare period/current/prior/budget where useful; scan unusual debit/credit signs, zero/unexpected balances, dormant accounts with activity, new accounts, suspense balances, intercompany mismatches, large manual journals, retained-earnings/opening-balance anomalies and classification issues. TB analytics supplement, not replace, account substantiation.

## Reconciliation tiers
High risk: cash, revenue/AR, payroll, tax-accounting balances, intercompany, equity, debt, estimates and material judgment accounts — stronger evidence/review/frequency. Low-risk immaterial stable accounts may use proportionate procedures.

## Reconciling-item governance
Fields: item ID, description, origin date, amount/currency, category, root cause, accounting consequence, owner, due date, proposed adjustment, evidence, status. Aging alone is insufficient; risk and nature matter.

## Controls
Population completeness; preparer/reviewer; timely completion; stale-item escalation; certification; unreconciled balance reporting; JE linkage; evidence retention; account ownership; account creation/closure governance.

## Automation / TrackedFR
Strong fit when recurring reconciliation joins ERP, subledger, bank/invoice/warehouse data and Excel with repeatable matching and exception investigation. Automation should preserve source lineage, match rule, exception reason and reviewer evidence.

## Artifacts
Reconciliation template; account inventory; risk tiering; certification dashboard; reconciling-item log; TB analytical review; remediation backlog.

## Scenarios
1. Prepayment rec equals GL copied into Excel: fail—no independent substantiation.
2. Bank rec has old $20k reconciling item below overall materiality: investigate nature/fraud/error risk; do not auto-clear.
3. AR subledger agrees GL but aging contains negative customer balances: reconciliation passes total but CAO flags classification/process issue.

QA: PASS.