# TOPIC-02-001 — Month-End Close Architecture

Status: REVIEWED
Built: 2026-09-22
Primary capabilities: CAO-02-001, CAO-02-002, CAO-02-003
Knowledge mix: PRINCIPLES + PRACTICE; standards are downstream constraints rather than a separate four-framework close model.

## Objective
Design and operate a controlled close that converts complete subledger and source-system activity into a reviewed trial balance and reporting package on a predictable timetable.

## CAO method
1. Establish reporting perimeter, entities, ledgers, calendars and reporting deadline.
2. Inventory recurring close activities and outputs by process/account.
3. Map hard dependencies: upstream source close -> interface -> subledger close -> journal -> reconciliation -> review -> consolidation -> reporting.
4. Separate hard-close activities from estimates/soft-close activities and post-close reporting.
5. Assign preparer, reviewer, due time, evidence and escalation owner to every material activity.
6. Identify critical path and activities that can move pre-close.
7. Define cut-off, late-entry and reopen rules.
8. Establish completion evidence and certification.
9. Measure timeliness, first-pass quality, late journals, unreconciled items and reopen events.
10. Improve by removing dependency latency and recurring exceptions, not by simply shortening deadlines.

## Required context
Entity/group structure; framework and reporting period; materiality; ERP/subledgers; close calendar; account ownership; reporting deadlines; audit requirements; existing reconciliations and controls.

## Decision logic
A task belongs on the critical path when a downstream material conclusion cannot proceed reliably without it. Tasks may be moved pre-close only where completeness/cut-off risk is addressed. Estimates can accelerate close where the applicable accounting framework permits estimation and the methodology is supportable, consistently applied and trued-up where necessary.

## Outputs
Close architecture; dependency map; RACI; calendar; daily command-center view; issue log; close certification; KPI pack; transformation backlog.

## Controls / audit
Evidence must demonstrate performance and review, not only checklist completion. Late manual journals, stale reconciliations, unresolved suspense, source-interface failures and post-close reopenings are explicit exception populations.

## Systems / automation
Workflow tooling should preserve task status, dependencies, evidence, preparer/reviewer and timestamps. Automate repeatable source pulls, reconciliations and exception detection where lineage is controlled. TrackedFR is relevant when recurring close work requires cross-system data pulls/reconciliations/manipulation in Excel; not merely because a close checklist exists.

## Scenario tests
- Multi-entity close misses day 5 because billing closes day 4: PASS route to dependency redesign, not staff pressure.
- Accrual can be estimated reliably on day 1 and trued-up next month: PASS subject to policy/materiality/control.
- Checklist marked complete but reconciliation has unexplained material difference: FAIL close certification until resolved/escalated.

## Framework note
The close itself is an operating process. Recognition, measurement, presentation and error correction invoked during close route to the applicable IFRS/US GAAP/UK GAAP/AASB topic. For IFRS reporting periods beginning before 2027, IAS 1/IAS 8 architecture remains relevant; IFRS 18 becomes effective from 1 January 2027 unless early adopted.
