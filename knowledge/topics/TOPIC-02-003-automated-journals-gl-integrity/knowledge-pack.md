# TOPIC-02-003 — Recurring & Automated Journals / GL Integrity Review

Status: REVIEWED
Capabilities: CAO-02-007, CAO-02-008
Knowledge types: PRINCIPLES, PRACTICE
Framework sensitivity: LOW; underlying recognition/measurement inherits the relevant accounting topic.

## Objective
Move stable recurring accounting into controlled automation while maintaining ledger integrity and rapid detection of incomplete, duplicated, misclassified or anomalous postings.

## Automation eligibility
A journal is a strong automation candidate when source population, calculation, mapping, timing and reversal logic are deterministic; exceptions can be explicitly detected; ownership is clear; and accounting policy is stable. Judgment-heavy estimates can automate data preparation but should preserve governed judgment and review.

## Automated journal design
Define trigger/frequency; authoritative source; completeness check; transformation/calculation; account/entity/dimension mapping; currency/FX source; posting period; reversal; tolerances; duplicate prevention/idempotency; exception queue; approval/release model; posting confirmation; audit log; reconciliation linkage; change control.

## GL integrity review
The CAO reviews ledger integrity through complementary tests:
- TB debits equal credits and books/entities are complete.
- expected subledger/control accounts reconcile;
- suspense/clearing balances are explained;
- unusual account combinations, users, periods, dimensions and amounts are investigated;
- automated feeds show expected run counts/totals;
- duplicate/missing batch detection;
- closed-period and late-posting review;
- opening + movement = closing rollforward where applicable;
- intercompany and FX mechanics are coherent;
- material accounts have appropriate reconciliation/certification.

## Exception classes
Source missing/incomplete; mapping missing; invalid dimension; duplicate batch; unexpected zero/volume; tolerance breach; posting failure; period closed; reversal failure; source-to-GL total mismatch; unauthorized configuration change.

## Controls
Approved automation specification; source completeness control; controlled mapping tables; test/UAT evidence; access/change management; run monitoring; exception resolution; posting-to-GL confirmation; periodic owner certification; reconciliation.

## Failure modes
Automating a copied spreadsheet without source controls; silent mapping defaults; posting despite incomplete source; no idempotency; automation user with unrestricted access; no alert when job fails; manual override not logged; integrity review limited to TB balancing.

## Artifacts
Automation design; mapping table; run-control report; exception log; GL integrity dashboard; anomaly report; control narrative; change log.

## Scenarios
1. Payroll accrual feed arrives twice: duplicate key prevents second posting and raises exception.
2. New department has no mapping: fail closed to exception queue, not default department.
3. TB balances but AP control differs from subledger: GL integrity fails despite debit-credit equality.

QA: PASS for principles/practice.