# TOPIC-01-003 — Close Transformation / Shared Services Design
Capabilities: CAO-01-007, CAO-01-008
Status: REVIEWED / production-candidate

## Objective
Redesign close and shared-service delivery so speed improves without weakening accounting judgment, evidence, ownership or local statutory accountability. This topic is PRINCIPLES/PRACTICE-led.

## Required context
Capture close days and critical path, entity/jurisdiction map, material accounts and subledgers, process owners, journal and reconciliation volumes, late-adjustment history, audit findings, upstream cutoffs, systems/interfaces, local statutory requirements, service locations, exception volumes and growth forecast.

## Close-transformation decision logic
1. Baseline actual task start/finish times for at least three closes; distinguish elapsed time from active effort.
2. Identify hard dependencies: upstream data, billing/payroll/AP cutoffs, bank feeds, valuations, intercompany, consolidation and management judgments.
3. Classify work as pre-close, event-driven, day-specific or post-close. Move work earlier only where completeness and control evidence remain reliable.
4. Remove duplicate reconciliations/reports before automating them.
5. Standardize policy, journal templates, reconciliation evidence and sign-off criteria.
6. Automate deterministic work only after inputs, exception ownership and fallback controls are defined.
7. Set materiality/risk-based review depth; faster close must not mean blanket reduced review.
8. Pilot, measure late adjustments and control failures, then scale.
9. Define reopening governance and post-close learning.

## Shared-services decision logic
Assess standardizability, judgment intensity, local statutory knowledge, language/customer proximity, transaction scale, system commonality, control segregation and service-window needs. Transactional repeatable work can centralize; policy, significant estimates, technical conclusions and statutory accountability remain with appropriately qualified retained accounting owners.

A shared service is not an accountability transfer. Define retained owner, service owner, operator, reviewer, escalation route and local statutory owner for each service.

## Service design
The service catalogue records scope, inputs, output, cutoff, SLA, quality measure, evidence standard, exception route and exclusions. Use outcome SLAs such as on-time reconciled posting and exception ageing rather than ticket closure alone. Capacity includes close peaks, audit work, absences, transitions and expected exception load.

## Controls and systems
Preserve preparer/reviewer segregation, privileged-access governance, journal approval, reconciliation certification, interface monitoring, master-data controls and retained evidence. Standardize workflow before orchestration. System outages require documented fallback and subsequent completeness reconciliation.

## Artifacts
Close dependency graph; task inventory; critical-path analysis; pre-close opportunity register; late-adjustment root-cause log; target close calendar; shared-service suitability matrix; service catalogue; RACI; SLA/KPI set; transition plan; control-impact assessment; capacity model; exception matrix.

## Metrics
Close duration; critical-path duration; late tasks; post-close adjustments; reopened periods; reconciliation completion; aged exceptions; first-time-right; manual journals; interface failures; service SLA attainment; audit/control exceptions. Never optimize close days alone.

## Failure modes
Moving cutoffs earlier without completeness controls; lift-and-shift of broken processes; centralizing judgment because transactions are centralized; SLA gaming; eliminating local expertise; automation without exception ownership; assuming headcount reduction before stabilization; transformation without BAU capacity.

## Scenario QA
PASS — five-day close: recurring Day 3 reconciliations move to pre-close only after completeness and roll-forward controls are defined.
PASS — AP shared service: invoice processing centralizes while entity controllers retain cutoff/accrual judgment and close certification.
PASS — multi-country group: local statutory ownership remains explicit where GL processing is centralized.
PASS — automated journal feed: benefit is accepted only with interface completeness, exception queue, access and fallback controls.
PASS — SLA is green but late adjustments rise: accounting-quality metrics override ticket throughput.
PASS — acquisition on another ERP: migration waits for data mapping, controls and transition reconciliation acceptance.

## Framework routing
Recognition, measurement, presentation and disclosure conclusions route to the applicable IFRS, US GAAP, UK GAAP or AASB topic. Shared-service location does not change reporting framework or effective-period requirements.