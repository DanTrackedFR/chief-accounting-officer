# TOPIC-02-010 — Close Evidence, Sign-Off & Fast-Close Design

Status: REVIEWED
Capabilities: CAO-02-021, CAO-02-022
Knowledge: PRINCIPLES + PRACTICE
Framework sensitivity: LOW

## Objective
Make close completion provable and accelerate close by removing waste and latency without weakening accounting evidence or review.

## Evidence standard
A completed task shows what was performed, population/period/entity, source data, method, result, exceptions, preparer, reviewer, timestamps and evidence location. Sign-off is an assertion that required work is complete and exceptions are resolved or explicitly accepted within authority. A checkbox without evidence is not certification.

## Fast-close diagnostic
Measure elapsed and touch time separately. For each critical-path task identify waiting for data, manual extraction, transformation, matching/reconciliation, judgment, review queue, correction/rework and system latency. Attack structural delay in that order rather than simply moving due dates earlier.

## CAO design
1. Establish current close duration and quality baseline.
2. Map critical path and evidence requirements.
3. Move stable work pre-close: recurring journals, standing-data validation, reconciliations where continuous data exists, estimate inputs.
4. Automate repeatable extraction/matching after controls and ownership are defined.
5. Use risk/materiality tiers for review depth.
6. Replace sequential handoffs with safe parallel work.
7. Set exception tolerances and escalation.
8. Lock/certify subledgers, GL, consolidation and reporting in dependency order.
9. Track post-close entries and rework as counter-metrics to speed.
10. Reassess after each close.

## World-class indicators
Close is exception-driven; reconciliations are substantially current before period end; late manual journals are rare; evidence is captured automatically; reviewer queues are visible; data lineage is known; closing faster does not increase reopenings or audit adjustments.

## Controls
Evidence retention; preparer/reviewer segregation; certification hierarchy; unresolved-exception register; close/reopen authority; KPI integrity; automation change control; final reporting certification.

## Artifacts
Evidence standard; certification matrix; fast-close diagnostic; critical-path redesign; automation backlog; KPI dashboard; close certification pack.

## Tests
A proposed two-day close that increases estimated postings and removes review fails. A three-day close with continuous reconciliations and automated evidence can pass. A task completed on time without source evidence remains incomplete.

## TrackedFR fit
Prioritize recurring cross-system reconciliation/data-manipulation bottlenecks. Calendar workflow alone is not a TrackedFR use case.
