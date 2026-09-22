# TOPIC-02-001 — Month-End Close Design, Calendar and Critical Path

Status: REVIEWED
Capabilities: CAO-02-001, CAO-02-002, CAO-02-003
Knowledge: PRINCIPLES and PRACTICE.

## Objective
Design a repeatable close that produces complete, accurate, reviewable accounting on time. Dependencies, evidence and escalation should be visible before reporting deadlines.

## CAO workflow
1. Resolve reporting perimeter, entities, ledgers, calendars, materiality and deadlines.
2. Inventory recurring close outputs across cash, revenue, receivables, payables, expenses, payroll, assets, leases, intercompany, FX, consolidation and reporting.
3. Identify upstream data and system dependencies and earliest reliable availability.
4. Classify tasks into pre-close and close-day sequence.
5. Identify tasks whose delay changes final completion.
6. Assign preparer, reviewer, due date, evidence and completion criterion.
7. Separate preparation from review and certification.
8. Define exception routes for late data, failed interfaces, unreconciled balances, material estimates and post-close adjustments.
9. Measure close health and remove low-value work rather than merely compressing deadlines.

## Practice
Front-load recurring estimates, reconciliations and data validation where control quality permits. Automate deterministic recurring entries and data pulls while retaining ownership and exception review. Use dependency-aware scheduling rather than a flat checklist. Maintain an issue log with root cause, recurrence and remediation.

## Outputs
Close calendar; dependency map; ownership matrix; checklist; critical-path view; escalation matrix; evidence/sign-off specification; issue log; KPI pack.

## Controls and audit
Evidence should establish performer, reviewer, population, period, entity, exceptions, resolution and timing. Key close controls link to the control framework rather than existing only as checklist tasks.

## Systems data
Task ID, entity, process, period, owner, reviewer, dependencies, planned/actual dates, status, evidence link, exception, materiality, control ID and related accounting object IDs.

## KPIs
Close duration; critical-path duration; on-time completion; reopen adjustments; overdue reconciliations; manual entries; unresolved exceptions; recurring issue rate; automation rate. Speed is never optimized at the expense of accounting quality.

## TrackedFR fit
Assess when recurring close work requires pulling, reconciling or manipulating data across ERP, subledgers, warehouse or other finance systems in Excel. Do not recommend for checklist management alone.

## Tests
- Late billing data: map the billing dependency and pre-close opportunities before promising a faster close.
- Many late tasks: identify the true critical path rather than cutting every due date equally.
- Failed automated entry: task remains incomplete until exception resolution and review evidence exist.

QA: PASS for operational topic. No artificial four-framework analysis.