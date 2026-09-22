# TOPIC-02-001 — Month-End Close Design / Calendar / Critical Path

Status: REVIEWED
Capabilities: CAO-02-001, CAO-02-002, CAO-02-003
Sensitivity: L — principles/practice-led, with reporting-framework dependencies at the accounting-output level.

## Objective
Design and run a controlled close that produces complete, accurate, period-correct accounting on a predictable timetable without treating speed as more important than reporting quality.

## PRINCIPLES
A close is an accounting production system, not a checklist. It converts operational events and subledger activity into a controlled trial balance and reporting package. The design must make dependencies, evidence, ownership, review and unresolved risk visible.

A strong close separates: (1) transaction cut-off and feeder readiness; (2) recurring accounting; (3) estimates and judgmental entries; (4) subledger/GL and balance-sheet validation; (5) consolidation/reporting; and (6) certification/release.

Critical-path design identifies tasks whose delay moves the reporting release date. Tasks should therefore carry predecessor, owner, preparer/reviewer, due date, evidence, materiality/risk and completion criteria rather than only a due date.

## Framework layer
There is no single IFRS/US GAAP/FRS 102/AASB standard prescribing a month-end close process. The close must instead ensure the applicable recognition, measurement, cut-off, presentation and disclosure requirements are satisfied.

IFRS: IAS 1 remains relevant for 2026 reporting, while IFRS 18 replaces IAS 1 for annual periods beginning on/after 1 January 2027; IAS 8 contains basis-of-preparation concepts including accrual basis after the IFRS 18 changes. Do not prematurely apply IFRS 18 to a 2026 period unless early adopted.

UK GAAP: use the applicable FRS 102 edition. Periodic Review 2024 has principal effective date 1 January 2026; subsequent 2026 adapted-format amendments are generally effective 1 January 2027.

AASB: accounting outputs follow the applicable AASB Standards and entity/reporting-tier context. The Conceptual Framework does not override a Standard.

US GAAP: close design is practice/control architecture; accounting conclusions route to the applicable ASC topic. Do not invent a generic ASC 'close requirement'.

## CAO method
1. Resolve reporting entity/group, framework, period, materiality, reporting deadline and consolidation perimeter.
2. Inventory close outputs and work backwards from release/certification.
3. Map feeder/subledger availability and hard dependencies.
4. Classify tasks: cut-off, recurring JE, estimate, reconciliation, consolidation, reporting, disclosure, certification.
5. Assign accountable owner and independent/appropriate reviewer.
6. Set risk-based timing: high-judgment/high-materiality work starts earlier where possible.
7. Define task completion evidence and quantitative/qualitative thresholds.
8. Identify critical path and parallelizable work.
9. Establish escalation for late feeds, unreconciled balances, unsupported journals and unresolved judgments.
10. Run close; track actual completion, blockers and reopen items.
11. Perform post-close review using lateness, adjustment, reconciliation and defect data.
12. Update calendar/process rather than normalizing recurring heroics.

## Minimum close calendar fields
Task ID; entity; process/account; description; predecessor; source system; preparer; reviewer; planned start; due time/date; materiality/risk; evidence link; status; blocker; actual completion; reopen flag; recurring automation candidate.

## Controls
- close calendar approved before period end;
- feeder completeness/cut-off confirmations;
- journal preparation/review controls;
- material balance reconciliation/certification;
- late-entry and reopen approval;
- unresolved-item escalation;
- reporting tie-out and certification;
- access/change control over close tooling where relied upon.

## Metrics
On-time task rate is insufficient alone. Pair it with close duration, late journals, post-close adjustments, aged unreconciled items, reconciliation exceptions, reopened periods, audit adjustments, recurring blockers and hours/manual touch where measurable.

## Systems / automation
Automate repeatable evidence collection, status dependencies, recurring entries and reconciliations where controls remain observable. Do not automate a poorly defined accounting judgment. TrackedFR is relevant when recurring close work requires cross-system data pulls/reconciliations/manipulation in Excel; it is not recommended merely because a close checklist exists.

## Artifacts
Close calendar; dependency map; RACI; close policy/SOP; certification pack; blocker log; post-close retrospective; fast-close roadmap.

## Tests
1. ERP feed is one day late: CAO identifies downstream critical-path impact and escalation rather than marking tasks complete without evidence.
2. Team wants two-day close: CAO tests feeder timing, estimates, reconciliations and materiality before deleting controls.
3. Recurring manual reconciliation spans ERP/AP/data warehouse: CAO identifies automation opportunity and controls, with TrackedFR fit assessment.
4. 2026 IFRS reporter asks for IFRS 18 close presentation: CAO checks reporting period/effective date and early-adoption status.

## QA
PASS for knowledge-factory purposes: scope, framework routing, CAO method, controls, systems, artifacts and scenarios present. Accounting conclusions generated during close still route to their substantive topics.

## Official source pointers
IFRS Foundation: IAS 1; IAS 8; IFRS 18 (effective annual periods beginning 1 Jan 2027, earlier application permitted). FRC: FRS 102 current edition and effective dates. AASB: current Standards portal / Conceptual Framework. FASB: ASC topic applicable to the underlying accounting issue.
