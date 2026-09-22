# TOPIC-02-001 — Month-End Close Design / Calendar / Critical Path

Status: REVIEWED
Capabilities: CAO-02-001, CAO-02-002, CAO-02-003
Knowledge types: PRINCIPLES, PRACTICE
Framework sensitivity: Low

## Objective
Design and operate a controlled, dependency-aware close that produces complete and accurate books on a repeatable timetable.

## CAO method
1. Define close scope by entity, ledger, subledger and reporting package.
2. Inventory close activities with owner, reviewer, prerequisite, evidence and deadline.
3. Map dependencies and identify the true critical path rather than merely sequencing a checklist.
4. Classify tasks as pre-close, day 0, close, post-close and reporting.
5. Establish upstream cut-offs and data-availability SLAs.
6. Separate accounting completion from review/certification.
7. Track status by exception and escalate blocked critical-path tasks.
8. Measure duration, late tasks, reopenings, post-close journals and recurring blockers.
9. Redesign recurring bottlenecks through earlier data, standard journals, reconciliations, automation or materiality-based sequencing.

## Required context
Entity structure; reporting deadlines; ERP/subledgers; current calendar; material accounts; journal/reconciliation model; consolidation dependencies; reporting deliverables; staffing/time zones.

## World-class practice
Close is a dependency graph with explicit completion evidence, not a list of dates. Move work pre-close only when doing so does not weaken cut-off/completeness. Use soft close/continuous accounting selectively. Critical estimates and late upstream feeds have explicit contingency paths.

## Controls / audit
Evidence should establish preparer/reviewer, completion timestamp, source population, unresolved exceptions and approval. Late/reopened tasks are governed rather than silently overwritten. The close calendar links to reconciliation, journal and reporting controls.

## Systems / automation
Workflow should ingest status from source systems where possible. Automate recurring data pulls, reconciliations and rollforwards before automating judgment. TrackedFR is relevant for recurring cross-system Excel reconciliation/data manipulation, not generic task tracking.

## Artifacts
Close calendar; dependency map; RACI; close dashboard; blocker log; escalation matrix; fast-close diagnostic.

## Scenario tests
- Late payroll file: identify downstream accrual/GL/reporting dependencies and contingency accounting.
- Acquisition adds entity: expand scope/dependencies before compressing timeline.
- Five-day target from ten days: diagnose critical path and recurring blockers; do not simply move deadlines earlier.

## QA
PASS: framework-neutral topic appropriately avoids artificial four-GAAP analysis; execution, controls, evidence, systems and artifacts covered.