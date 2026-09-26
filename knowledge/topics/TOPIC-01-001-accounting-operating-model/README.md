# TOPIC-01-001 — Accounting Function Strategy / Operating Model / Organization Design
Capabilities: CAO-01-001, CAO-01-002, CAO-01-003
Status: REVIEWED / production-candidate

## Purpose
Design an accounting function that produces accurate, timely, controlled reporting as the company scales. This is PRINCIPLES/PRACTICE-led; do not manufacture IFRS/US GAAP/UK GAAP/AASB differences where none exist.

## CAO decision logic
1. Baseline company context: legal entities, jurisdictions, reporting frameworks, revenue/transaction volume, products, close target, audit/public-company obligations, systems and growth plan.
2. Map accounting outcomes: record-to-report, revenue/AR, AP/expenses, fixed assets, payroll accounting, cash, intercompany/consolidation, statutory/reporting, controls, technical accounting and audit.
3. Assign each outcome to global, regional/local, shared-service or specialist ownership. Separate policy/judgment ownership from transaction execution.
4. Identify control-critical segregation conflicts and key-person dependencies.
5. Choose centralization only where standardization, scale and control benefit exceed local-knowledge and responsiveness costs.
6. Define system-of-record, upstream/downstream interfaces and data ownership for every material accounting flow.
7. Size roles from workload drivers, complexity and control obligations rather than revenue alone.
8. Produce target organization, RACI, service boundaries, decision rights, transition roadmap and measurable outcomes.

## Design principles
- One accountable owner for each material accounting outcome.
- Central policy and technical judgment; execution may be distributed.
- Standard process before automation.
- Exceptions require named ownership and ageing.
- Local statutory obligations remain explicit even in centralized models.
- Capacity includes close peaks, audit, projects, leave and control review—not only BAU averages.
- Systems administration and accounting-data ownership need explicit governance.

## Deliverables
Current/target operating-model maps; organization chart; RACI; service catalogue; process-to-system map; capability/gap assessment; transition waves; dependency/risk register; capacity model; governance cadence.

## Controls / audit / systems
Evidence approval rights, journal/reconciliation ownership, privileged-access segregation, master-data ownership, close certification and change controls. Auditability requires traceable handoffs and retained evidence. System design should minimize manual bridges and uncontrolled spreadsheets.

## Failure modes
Designing from titles rather than outcomes; copying a benchmark organization; centralizing statutory knowledge away; assuming automation eliminates review; unclear finance-v-accounting boundaries; under-resourcing transformation while running BAU.

## Scenario QA
PASS — high-growth multi-entity SaaS: design separates global policy/technical accounting from regional statutory execution and scales transaction work through standardized processes.
PASS — acquisition doubles entity count: model triggers entity-complexity/capacity reassessment rather than headcount ratio alone.
PASS — small company: model permits combined roles but requires compensating review for incompatible duties.
PASS — automation proposal: capacity benefit is not booked until process/control redesign and exception workload are evidenced.
PASS — shared service: retained-accounting ownership remains accountable for policy, close certification and judgment.

## Framework routing
Accounting standards govern underlying recognition/measurement/reporting topics, not organization design itself. Route technical questions to the relevant knowledge topic and effective-period framework.
