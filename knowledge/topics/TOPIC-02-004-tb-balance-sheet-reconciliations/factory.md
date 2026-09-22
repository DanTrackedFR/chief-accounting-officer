# TOPIC-02-004 — Trial Balance Review / Balance Sheet Reconciliations

Status: REVIEWED
Capabilities: CAO-02-009, CAO-02-010
Knowledge mix: PRINCIPLES + PRACTICE, with accounting treatment inherited from each balance's topic.

## Objective
Prove that recorded balances are supported by underlying rights/obligations, source records and appropriate accounting, and surface errors before reporting.

## Reconciliation types
Subledger-to-GL; bank-to-GL; rollforward; external statement; schedule-to-GL; intercompany reciprocal; source-system-to-GL; analytical/estimate reconciliation; zero-balance/clearing; proof-of-cash where appropriate.

A rollforward is not automatically a reconciliation. It must explain opening balance + valid movements = closing balance and independently support the movements/closing position where required.

## Minimum reconciliation standard
Account/entity/period; GL balance; source/support balance; difference; reconciling items individually listed; age; cause; owner; resolution action/date; preparer/reviewer; evidence; conclusion. Reconciliation must identify what assertion it proves.

## CAO workflow
1. Risk-tier accounts using size, volatility, judgment, fraud susceptibility, manual activity, complexity, prior errors and external-audit significance.
2. Select the strongest feasible reconciliation method; do not default to prior-month rollforward.
3. Obtain GL independently from supporting source where possible.
4. Validate completeness of support population.
5. Compare and isolate differences.
6. Classify differences: timing, known valid reconciling item, posting error, source error, mapping, FX, cut-off, unsupported/unexplained.
7. Correct errors; do not hide them as reconciling items.
8. Age legitimate reconciling items and escalate stale items.
9. Review underlying accounting reasonableness, not only arithmetic tie.
10. Conclude whether balance is fairly supported for close/reporting purposes.

## Trial-balance review
Review period and YTD movement; unexpected signs; new/dormant accounts; material manual entries; entity/dimension anomalies; accounts with no reconciliation; large round amounts; unusual offset accounts; unexplained prior-period movement; retained earnings/opening balance; intercompany mismatches; subledger control accounts; suspense/clearing.

## Review standard
Reviewer re-performs key tie-outs, inspects support, challenges old items, verifies corrections, assesses accounting treatment and signs only after exceptions are resolved or explicitly accepted/escalated.

## Materiality
Materiality informs depth/frequency but does not justify leaving known errors unassessed. Small recurring items can indicate systemic failure or fraud risk. Use both quantitative and qualitative factors.

## Controls
Complete account inventory; required frequency; preparer/reviewer ownership; due dates; certification; standardized evidence; aged-item escalation; no self-review for material/high-risk accounts; reconciliation completeness dashboard; change control over automated matching rules.

## Automation
Automate extraction, matching, rollforward and exception generation; retain judgment over validity and accounting disposition. Matching rule should carry rule ID, fields, tolerance, date window, priority, false-positive monitoring and version.

## TrackedFR fit
Prime use case when balances require recurring triangulation across ERP, bank, P2P, billing, warehouse or other source data and Excel remains the working layer.

## Artifacts
Account inventory; risk/frequency matrix; reconciliation template; aging dashboard; certification report; TB analytics; exception log; remediation plan.

## Scenarios
A. AP GL ties to AP aging but aging contains old debit vendors: arithmetic tie passes; accounting review still flags classification/recovery/credit-balance issues.
B. Bank rec has six-month outstanding checks: require stale-item assessment; do not accept merely because reconciling schedule foots.
C. Prepaid schedule equals GL but contains expired contracts: existence/measurement fails despite tie.

## QA
PASS: distinguishes tie-out from substantive reconciliation; covers assertions, risk tiering, stale items, review and automation.