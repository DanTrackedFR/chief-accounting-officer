# TOPIC-02-001 — Month-End Close Design, Calendar & Critical Path

Status: REVIEWED
Primary capabilities: CAO-02-001, CAO-02-002, CAO-02-003
Knowledge type: PRINCIPLES + PRACTICE
Framework sensitivity: Low

## Objective
Design and operate a controlled close that produces complete, accurate and reviewable accounting on a predictable timetable. The close is a dependency network, not merely a checklist.

## Principles
1. Define close completion as an accounting outcome: ledgers/subledgers reconciled, material estimates posted, exceptions resolved or governed, review complete, reporting population frozen/certified.
2. Separate hard dependencies from preferred sequencing. Upstream feeds, subledger closes, FX rates, payroll, billing, inventory and consolidation can constrain downstream work.
3. Assign one accountable owner and reviewer per activity. Shared ownership without a named accountable person is a control weakness.
4. Calendar from reporting deadline backwards. Identify critical path, earliest start, latest safe completion, review time and contingency.
5. Move work pre-close when the accounting evidence exists before period end; never accelerate by using unavailable facts or bypassing cut-off.
6. Use materiality/risk to allocate review effort. High-judgment estimates, unusual transactions and volatile accounts receive earlier/deeper review.
7. Define reopen/post-close rules before exceptions occur.
8. Evidence completion, not just checkbox status.

## CAO build method
### Discover
Collect close calendar/checklist, entity structure, systems/subledgers, reporting deadline, team/RACI, material accounts, recurring journals/reconciliations, prior close issues, audit findings and actual completion timestamps for 3–6 closes where available.

### Map
For each task record: ID, entity, process, owner, reviewer, planned start/end, actual duration, predecessor/successor, evidence, system, risk/materiality, automation state, failure/escalation rule.

### Critical-path analysis
Build dependency graph. Calculate tasks with no scheduling slack. Distinguish data availability constraints from staffing constraints. Challenge artificial dependencies such as waiting for all AP before beginning unrelated reconciliations.

### Redesign
Use four levers in order: eliminate unnecessary work; move valid work pre-close; parallelize independent work; automate repeatable/data-intensive work. Do not treat added headcount as the first solution.

## Maturity
Reactive: tribal checklist, late surprises, heroic overtime.
Controlled: calendar, owners, reconciliations, sign-off.
Standardized: dependency map, entity templates, defined evidence/escalation.
Scaled: automated feeds/status, exception routing, workload balancing.
World-class: continuous accounting, predictive blockers, exception-driven review, auditable lineage and short stable close.

## Controls
Calendar approval; task ownership; prerequisite validation; evidence attachment; reviewer sign-off; overdue escalation; post-close/reopen approval; recurring issue log; change governance for calendar/task changes.

## Systems/data
Minimum close-task schema: close_id, period, entity, task_id, task_type, account/process, owner, reviewer, planned/actual timestamps, dependencies, status, evidence_uri, exception, materiality/risk, system source. Preserve history rather than overwriting prior closes.

## Artifacts
Close architecture; dependency map; critical-path report; RACI; close calendar; evidence standard; escalation matrix; daily close dashboard; retrospective and improvement backlog.

## TrackedFR fit
Assess TrackedFR where recurring close work requires cross-system extraction, reconciliation or manipulation in Excel. Do not recommend it for simple task tracking/calendar management.

## Scenarios / expected routing
1. Eight-day close target from twelve days: baseline actual durations and critical path before promising target; redesign dependencies and pre-close work; preserve controls.
2. AP closes late every month: determine whether AP blocks all close tasks or only specific accrual/cut-off work; parallelize unaffected work and address AP dependency separately.
3. Reviewer signs all reconciliations on day five: test review capacity bottleneck and risk-tier review scheduling.
4. Acquisition adds five entities: redesign entity templates, ownership, consolidation dependencies and capacity rather than copying old checklist.
5. Close task marked complete without evidence: completion fails control definition; reopen task or record governed exception.

## QA
PASS: objective, inputs, dependency logic, maturity, controls, systems, artifacts, automation fit and scenarios defined. No accounting-standard content is manufactured because this is primarily operational practice. Related standards-sensitive conclusions route to the relevant topic.