# TOPIC-02-001 — Month-End Close Design / Calendar / Critical Path

Status: REVIEWED
Capabilities: CAO-02-001, CAO-02-002, CAO-02-003
Knowledge mix: PRINCIPLES + PRACTICE; standards only where an underlying accounting topic drives a close requirement.

## Objective
Design a repeatable close that produces complete, accurate, timely and reviewable books without treating speed as the sole objective. The CAO should optimize for accounting quality, dependency management, evidence, review capacity and controlled acceleration.

## Required context
Reporting cadence and deadline; entity/group structure; ERP/subledgers; material accounts; close team and time zones; upstream data owners; consolidation/reporting dependencies; audit/control obligations; recurring estimates; system interfaces; current close calendar; known bottlenecks.

## CAO decision logic
1. Define the required reporting output and hard deadline.
2. Work backward from reporting/consolidation and identify every accounting output required.
3. Classify tasks as pre-close, day-specific, dependency-triggered, post-close or continuous.
4. Map predecessor/successor dependencies, data availability and reviewer capacity.
5. Identify critical path and near-critical tasks; do not assign arbitrary Day 1/2/3 dates before dependencies are known.
6. Separate accounting completion from review/sign-off. A prepared journal or reconciliation is not complete until required review/evidence exists.
7. Move work pre-close only when the accounting assertion remains valid at period end and a controlled true-up exists.
8. Automate stable, rules-based work before judgment-heavy work; preserve exception handling and evidence.
9. Set reopen/post-close rules and escalation thresholds.
10. Measure close quality as well as elapsed days.

## Close architecture
Minimum workstreams: upstream cut-off/data lock; subledger closes; recurring journals; estimates/accruals; cash; AP/AR/revenue; payroll/compensation; fixed assets/leases; intercompany; FX; tax-accounting inputs where relevant; reconciliations; consolidation; analytical review; reporting/disclosures; certification.

Each task record should carry: task ID, entity, account/process, owner, preparer, reviewer, planned date/time, dependency, source system, expected evidence, materiality/risk tier, status, blocker, completion timestamp and reopen history.

## Critical-path method
A task is critical when delay pushes the final close deadline. The CAO should model dependency chains rather than simply ranking tasks by importance. For each task capture earliest possible start, expected duration, required predecessor, reviewer availability and downstream consumer. Recalculate the critical path when actual completion times change.

## Fast-close rules
Recommended: pre-close recurring schedules; earlier intercompany confirmation; automated source-to-GL interfaces; standard estimate methodologies; materiality-based review; exception reporting; parallel work where dependencies permit.

Unsafe shortcut: posting unsupported estimates merely to hit Day N; skipping reconciliations; removing independent review; closing subledgers before completeness controls; rolling unresolved differences indefinitely. Label these as speed gained by accepting accounting/control risk.

## Controls and evidence
Calendar approved before period end; owner/reviewer segregation for high-risk tasks; dependency completion evidenced; material late journals flagged; unresolved reconciling items aged/escalated; close certification; controlled reopen; final TB/version retained; evidence repository linked to task IDs.

## KPIs
Elapsed close days; critical-path duration; on-time task rate; first-pass review rate; late/manual journal count and value; reconciliation aging; post-close adjustment count/value; reopened periods; recurring blocker count; hours/overtime; automated task share. Never optimize one KPI in isolation.

## Systems / automation
Close-management tooling should integrate task status with ERP/subledger evidence where possible. Automate status only from reliable system events. Cross-system recurring reconciliation/data manipulation is a TrackedFR candidate when it involves repeatable ERP/subledger/warehouse data and Excel-based investigation; do not recommend it for calendar management alone.

## Artifacts
Close calendar; dependency map; RACI; critical-path view; close policy; escalation matrix; evidence standard; KPI pack; post-close retrospective; 90-day close-improvement roadmap.

## Scenarios
A. Revenue feed arrives Day 3 but reporting due Day 4: identify feed as critical, test whether validated preliminary feed plus controlled true-up is supportable; do not simply move revenue close earlier.
B. Reviewers overloaded Day 2: move preparation does not solve bottleneck; redesign reviewer load/dependencies.
C. Close shortened from 8 to 5 days: baseline quality/error metrics, shift controllable tasks pre-close, automate stable feeds, preserve material reconciliations/reviews.

## QA
PASS: produces dependency-led calendar, distinguishes preparation/review, preserves evidence and explicitly treats fast-close shortcuts as risk decisions.