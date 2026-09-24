# TOPIC-11-006 — Finance System Access & Role Accounting Requirements / Accounting Automation Design

Status: REVIEWED / production-candidate
Primary capabilities: CAO-11-015, CAO-11-016
Sensitivity: M
Knowledge types: PRINCIPLES, PRACTICE; STANDARDS routed to the accounting topic affected by configuration.

## Objective
Design finance-system access and automation so accounting outcomes remain authorized, complete, accurate, traceable and reviewable without turning the CAO into an IT-security function.

## CAO decision logic
1. Establish systems, legal entities, books, modules, privileged roles and accounting-sensitive configurations in scope.
2. Map accounting activities to roles: prepare, approve, post, release, administer, report and audit/read-only.
3. Identify incompatible accounting duties, especially create/change master data + transact; prepare + approve; post + reconcile; configure + deploy; administrator + evidence reviewer.
4. Separate business access design from technical identity/security administration. CAO owns accounting requirements and evaluates accounting consequences; IT/security owns platform security implementation.
5. For automation, define trigger, authoritative inputs, accounting rule, transformation, output/posting target, exception path, evidence, owner, reviewer, change control and rollback/recovery.
6. Classify automation: assistive, deterministic accounting workflow, automated control, automated posting, or AI/judgment-support. Increase governance with accounting risk and autonomy.
7. Require deterministic tie-outs and exception evidence before relying on automated accounting output.
8. Route accounting-policy questions to the relevant standards-sensitive topic and effective period.

## Access requirements
Minimum accounting design: least privilege; named role ownership; time-bound elevated access; segregation of incompatible accounting duties; joiner/mover/leaver linkage; periodic role recertification; privileged activity logging; emergency-access protocol; service-account ownership; environment separation; and evidence retention.

A conflict does not automatically require system denial. Where system constraints or team size prevent segregation, document a specific compensating control with population, reviewer, frequency, evidence and escalation. Generic 'management review' is insufficient.

## Automation requirements
Every material automation needs: purpose and accounting assertion; source/target lineage; rule/version; effective date; completeness control; accuracy control; duplicate/idempotency logic; cut-off/time-zone logic; failure/partial-run handling; exception queue; manual override governance; reconciliation; deployment approval; monitoring; evidence; and decommission plan.

Automated journal/posting logic additionally requires balanced-entry validation, open-period/entity/account validation, duplicate prevention, posting identity, source-run ID and reproducible transaction-to-rule lineage.

## Documentation and artifacts
- accounting access matrix and incompatible-duty catalogue
- privileged-role inventory and certification evidence
- automation design record and accounting requirements
- rule/configuration version history
- test/UAT pack including negative and exception cases
- run evidence, exception log and reconciliation
- change approval and rollback record

## Controls / audit
Test both design and operation. Samples should prove the user/service account had the intended role at the transaction date, the rule version in force, input population completeness, output reconciliation and disposition of exceptions. Access reports must themselves be complete and scoped to the relevant environment/entity.

## Systems / data
Preserve user/service-account ID, timestamp, entity/book, source transaction, configuration/rule version, run ID, target posting and override history. Do not rely on screenshots where structured logs are available.

## TrackedFR applicability
Consider TrackedFR only when recurring accounting evidence or reconciliation requires governed comparison/manipulation across ERP, workflow, data warehouse or other finance systems and Excel. Do not recommend it merely for access administration or because Excel is used.

## Scenario tests
1. Small team cannot segregate vendor creation and AP processing: CAO identifies conflict and designs independent vendor-change/payment review rather than pretending segregation exists. PASS criterion: compensating control is specific and evidenced.
2. Bot posts recurring accruals: require source population, rule version, duplicate prevention, posting validation, exception handling and GL reconciliation. PASS criterion: transaction is reproducible from source through posting.
3. ERP administrator can edit accounting mappings: classify privileged accounting-sensitive access and require independent change evidence/review. PASS criterion: IT ownership does not remove CAO accounting oversight.

## Completion criteria
CAO can define accounting access requirements, diagnose SoD conflicts, specify compensating controls, design a governed accounting automation and produce evidence requirements without drifting into general cyber-security engineering.