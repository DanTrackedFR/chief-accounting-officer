# TOPIC-02-005 — Reconciliation Governance / Account Certification

Status: REVIEWED
Capabilities: CAO-02-011, CAO-02-012
Knowledge mix: PRINCIPLES + PRACTICE.

## Objective
Operate reconciliations as a controlled accounting system: complete population, risk-based frequency, accountable ownership, evidence, review, aging/escalation and explicit certification.

## Account inventory
Maintain every balance-sheet/control account with entity, account number/name, purpose, accounting owner, reconciliation method, risk tier, frequency, preparer, reviewer, source system, due date, materiality/tolerance, expected balance/sign, certification status and retirement date. New accounts enter governance automatically; closed accounts remain until zero/retirement is evidenced.

## Risk tiering
High: cash, revenue/AR control, payroll liabilities, intercompany, equity, estimates/reserves, acquisition balances, material manual accounts, historically problematic balances.
Medium: material routine accrual/prepaid/asset/liability balances with reliable support.
Low: immaterial/stable balances with low judgment and strong automated source controls.

Risk tier determines frequency, reviewer seniority, evidence depth and due date. It never removes the need to understand a non-zero balance.

## Certification
Certification is a positive assertion that the account has been reconciled under policy, material reconciling items are valid, errors are corrected or formally assessed, aged items are escalated, support is retained, and the recorded balance is reasonable under applicable accounting.

Possible states: not started; prepared; reviewer returned; reconciled with open items; certified; certified with approved exception; overdue; blocked. Avoid a binary green check that conceals unresolved items.

## Reconciling-item governance
Each item requires amount, origin date, reason, expected resolution, owner, age bucket, accounting impact and evidence. Define aging thresholds by item type rather than one universal threshold. Escalate recurring and stale items; determine whether write-off/reclassification/adjustment is required.

## Tolerances
Matching tolerances can improve efficiency but cannot silently write off differences. Separate automated matching tolerance from accounting adjustment/write-off authority. Qualitative risk overrides amount thresholds.

## Review and escalation
Reviewer challenges method suitability, source independence/completeness, old items, unexplained changes, recurring manual adjustments and conclusion. Escalation goes to accounting leadership when material items remain unresolved at reporting cutoff or repeated process failures persist.

## Governance metrics
Population completeness; on-time preparation/review/certification; overdue accounts by risk; unresolved item value/count/age; repeat items; adjustments arising from reconciliation; accounts certified with exception; auto-match rate plus false-match rate; reviewer return rate.

## Operating model
Central policy with local ownership is usually scalable: CAO/Controller sets methodology, risk tiers and evidence standards; process/account owners prepare; independent reviewers certify; close governance monitors exceptions. Shared service/offshore preparation does not transfer accounting accountability away from designated owner/reviewer.

## Systems and automation
Reconciliation platform should preserve source snapshots, matching rules, preparer/reviewer actions, item history and certification. Automated reconciliations require source completeness controls and exception review.

## Artifacts
Reconciliation policy; account inventory; risk matrix; certification wording; aging/escalation policy; dashboard; exception approval; automated-match governance; account opening/closing checklist.

## Scenarios
A. Low-risk account unreconciled for three months because balance is zero: validate zero from GL/source and account activity; policy may permit lower frequency but must be explicit.
B. High-risk cash account auto-matches 99.9%: remaining exceptions and source completeness still require review.
C. Reviewer certifies with $500k stale item: certification must expose exception and escalation, not mark clean.

## QA
PASS: creates population-level governance rather than isolated workpapers; separates certification, matching tolerance and accounting adjustment authority.