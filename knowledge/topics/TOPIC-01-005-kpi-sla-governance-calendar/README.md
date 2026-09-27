# TOPIC-01-005 — Accounting KPI & Service-Level Design / Accounting Governance Calendar
Capabilities: CAO-01-011, CAO-01-012
Status: REVIEWED / production-candidate

## Purpose
Provide CAO-level operating logic for accounting kpi & service-level design / accounting governance calendar. This topic is PRINCIPLES/PRACTICE-led; accounting-standard recognition and measurement questions route to the relevant technical topic.

## KPI design
Use a balanced set of timeliness, quality, control, exception, capacity and stakeholder measures. Every KPI needs definition, owner, source, frequency, target/tolerance, escalation and anti-gaming check. Pair speed with quality—for example close day with late journals/reopens; reconciliation timeliness with aged exceptions; automation rate with exception/rework rate.

## Governance calendar
Build one recurring calendar covering close, account certification, policy/estimate reviews, control certifications, access reviews, disclosure preparation, audit milestones, statutory reporting, system/change governance, vendor reviews and post-close retrospectives. Each event has owner, required evidence, dependency, escalation and completion record.

## CAO decision logic
1. Start from accounting outcomes and risks, not available dashboard fields.
2. Define numerator/denominator and clock boundaries so metrics are reproducible.
3. Establish baseline before setting targets.
4. Segment where averages hide material failures.
5. Link threshold breaches to named actions and governance forums.
6. Retire metrics that no longer drive decisions.
7. Reconcile governance events to reporting/audit obligations and company changes.

## Deliverables
KPI dictionary; SLA catalogue; dashboard specification; threshold/escalation matrix; annual/quarterly/monthly governance calendar; meeting charters; evidence register; action log.

## Controls / systems
Metric source data needs lineage and controlled definitions. Manual KPI adjustments are logged and reviewed. Calendar completion is evidenced; missed control-critical events escalate rather than merely roll forward.

## Failure modes
Vanity metrics; targets without baselines; averages masking aged exceptions; speed metrics encouraging premature close; conflicting SLA definitions; calendar events without evidence; duplicate governance forums with no decision rights.

## Scenario QA
PASS — close improves from day 7 to day 5 but reopenings double: dashboard flags deterioration rather than declaring success.
PASS — 98% reconciliations on time hides one material account: segmentation prevents false green status.
PASS — vendor SLA breach: threshold routes to named owner and governance action.
PASS — quarterly estimate review omitted: governance calendar records exception and escalation.
PASS — KPI source logic changes: definition/version control preserves comparability.

## Framework routing
IFRS, US GAAP, UK GAAP and AASB do not prescribe a universal operating model for this topic. Apply framework-specific requirements where the underlying accounting, reporting, disclosure or control obligation arises; do not invent differences.
