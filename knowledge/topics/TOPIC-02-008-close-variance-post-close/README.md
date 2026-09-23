# TOPIC-02-008 — Close Variance / Flux Review & Post-Close Governance

Status: REVIEWED
Capabilities: CAO-02-017, CAO-02-018
Knowledge types: PRINCIPLES, PRACTICE
Framework sensitivity: Low, with technical-accounting routing where an unexplained movement indicates an accounting issue.

## Objective
Use analytical review to detect incomplete, inaccurate or unusual period-end accounting, then govern any adjustment or ledger reopening after close.

## CAO method
1. Define review population: P&L, balance sheet, cash-flow-sensitive accounts, entities and material dimensions.
2. Compare current period to prior period, budget/expectation where useful, prior year and account-specific drivers.
3. Set thresholds using both amount and percentage, but override thresholds for inherently risky accounts.
4. Decompose movements into known business drivers, accounting entries, FX, acquisition/entity changes, reclasses and unexplained residual.
5. Trace explanations to evidence rather than accepting narrative alone.
6. Route unexplained items to journal, reconciliation, cut-off, estimate or technical-accounting work.
7. Classify proposed post-close adjustments by materiality, reporting impact, cause and whether books must reopen.
8. Require approval and an audit trail for reopen/reclose; rerun affected reconciliations, consolidation and reporting outputs.
9. Feed recurring late adjustments into root-cause remediation.

## Post-close decision model
A proposed entry after close should state: issue; amount/accounts/entities; discovery date; whether error/estimate/new information/reclassification; financial statement impact; materiality; external reporting status; affected controls/reconciliations; proposed period; approver; required re-performance.

Do not use a generic 'below threshold' rule to defer known errors automatically. Route materiality and error correction to the applicable framework and TOPIC-02-009 / policy-estimates-judgments knowledge.

## Controls
Document review population completeness; threshold rationale; evidence for material explanations; reviewer challenge; unresolved items; post-close journal approval; ledger reopen access; downstream rerun evidence; final re-certification.

## Systems
Automate variance population and driver decomposition where source lineage is reliable. Preserve the exact data snapshot used for review. Avoid AI-generated explanations without source evidence.

## Artifacts
Flux workbook/dashboard; explanation log; post-close adjustment form; reopen decision; root-cause log; re-certification evidence.

## Scenario tests
- Revenue up 18% but AR flat: require driver evidence and route possible deferred/unbilled/cash issue.
- Late $20k invoice after close: assess cut-off/materiality and policy; do not automatically reopen.
- Material consolidation elimination discovered after reporting draft: reopen governed steps and rerun affected outputs.

## QA
PASS: operational knowledge separated from technical error/materiality rules; evidence, downstream impact and governance are explicit.