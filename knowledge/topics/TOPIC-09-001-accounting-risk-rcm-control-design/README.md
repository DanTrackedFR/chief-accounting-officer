# TOPIC-09-001 — Accounting Risk Assessment / Risk & Control Matrix Design / Control Design

Status: **REVIEWED / production-candidate**  
Primary capabilities: **CAO-09-001, CAO-09-002, CAO-09-003**  
Sensitivity: **M**  
Updated: **2026-09-23**

## Objective
Enable the CAO to translate the accounting/reporting process into a defensible financial-reporting risk assessment and risk-control matrix (RCM), then design controls that address the actual risk at the right precision without creating checklist bureaucracy.

## Inputs
Company Context; materiality; financial statements and disclosures; COA; entity/process/system map; close calendar; accounting policies; significant estimates/judgments; transaction volumes; prior errors/restatements; audit findings; fraud risks; system interfaces; existing controls; owners/reviewers; evidence retained; regulatory/public-company status.

## Principles
- Start with financial-reporting objectives and risks, not the existing control list.
- Describe a risk as what could go wrong and its reporting consequence. “No review” is a missing control, not the underlying risk.
- Map risks to assertions/objectives and affected accounts/disclosures, then design responses.
- A control is only useful if its purpose, owner, frequency, population, procedure, precision, evidence and exception handling are clear.
- Distinguish entity-level, process-level, IT-dependent, automated and IT-general-control dependencies.
- Separate control design from operating effectiveness. A well-designed control that was not performed is not effective.
- Scale control effort to likelihood, magnitude, complexity, judgment, fraud susceptibility, change and data/system dependency.

## Framework / jurisdiction routing
This topic is primarily PRINCIPLES + PRACTICE rather than a four-accounting-framework measurement topic. IFRS, US GAAP, UK GAAP and AASB influence the underlying reporting risks through recognition, measurement, presentation and disclosure requirements; the RCM must therefore link each standards-sensitive risk to the applicable knowledge record/effective period.

Jurisdiction and listing status can add formal internal-control obligations. The CAO must load those requirements through the jurisdiction/regulatory layer rather than claiming one universal SOX-style control regime. For US SEC registrants, ICFR/SOX requirements are a jurisdiction overlay; for other entities, the same control-design discipline may be good practice without being a statutory SOX requirement.

## CAO workflow
1. Define scope: entity/process/period/framework/materiality and reporting obligations.
2. Map significant accounts, disclosures, transaction streams and estimates to processes/systems.
3. Identify inherent risks: existence/occurrence, completeness, accuracy/valuation, rights/obligations, cut-off, classification/presentation plus fraud and management-override risks where relevant.
4. Rate risk using magnitude, likelihood, complexity, judgment, change, volume and susceptibility to error/fraud; document rationale rather than relying on a score alone.
5. Inventory existing controls and map each to one or more risks.
6. Identify uncovered risks, redundant controls and controls that do not address their stated risk.
7. Design key controls with explicit precision, population/data source, threshold, reviewer action, evidence and exception resolution.
8. Identify IT/data dependencies and required IPE (information produced by the entity) completeness/accuracy controls.
9. Assign owner/reviewer/frequency and segregation constraints.
10. Define test attributes and evidence standard before rollout.
11. Build RCM and remediation backlog; prioritize high-risk gaps.
12. Link recurring failures to process/system redesign and Company Accounting Memory.

## RCM minimum schema
`risk_id | process | subprocess | account/disclosure | assertion/objective | risk statement | inherent risk rationale | control_id | control description | control type | frequency | owner | reviewer | system/data source | precision/threshold | evidence | exception process | key/non-key | IT dependency | status | deficiency/remediation | last reviewed`

## Control design test
For each proposed control ask: (1) what exact misstatement/failure can occur; (2) what population/data does the control cover; (3) how would the performer detect it; (4) at what threshold/precision; (5) what proves the control happened; (6) what happens when an exception is found; (7) could the same risk be addressed earlier or automatically with better process design?

## Practice classification
**Required:** risks linked to reporting objectives; controls have owners/frequency/evidence; material uncovered risks remediated.  
**Recommended:** formal RCM, annual/trigger-based risk refresh, key-control rationalization, deficiency log.  
**World-class:** RCM connected to process/system lineage, automated population completeness, continuous exception monitoring and change-impact triggers.  
**Shortcut/risk:** copying last year's RCM, vague “management review” controls, dozens of controls with no risk mapping, evidence created after the fact, scoring that substitutes for judgment.

## Controls over the controls process
Approved RCM owner; version/change log; annual and event-driven refresh; reconciliation of significant accounts/disclosures to RCM scope; new-system/new-product/M&A change trigger; independent challenge of high-risk control design; remediation aging; audit-finding linkage; certification of control ownership.

## Systems / automation
Use workflow/GRC tooling when it improves ownership, evidence, testing and remediation lineage. Automation should reduce manual evidence chasing and detect exceptions, not merely digitize a weak control. TrackedFR is relevant only where the control/reconciliation repeatedly requires governed extraction/manipulation/reconciliation across multiple finance systems and Excel/reporting outputs.

## Scenario QA
1. Revenue material but RCM has only invoice-approval control -> identify recognition/cut-off/completeness/data risks and redesign coverage.
2. Monthly management review says “review P&L” -> fail design until precision, data, expectations, thresholds, follow-up and evidence are defined.
3. Automated three-way match relies on PO/receipt master data -> identify system/configuration/data/IT dependencies.
4. New ERP implemented mid-year -> trigger risk/control redesign; do not roll prior RCM unchanged.
5. Material spreadsheet estimate -> include model/data/change/review controls and link to estimate methodology.
6. Non-US private company -> do not label SOX mandatory absent jurisdiction trigger; still apply scalable control principles.
7. One control maps to five risks -> validate it actually operates at sufficient precision for each risk.
8. Ten controls map to same low-risk objective -> rationalize redundancy before adding more.
9. Reconciliation consistently has old reconciling items -> treat as control/process failure requiring remediation, not successful sign-off.
10. Audit finding recurs -> escalate design/root-cause/remediation rather than only increasing review evidence.

Expected routing: **10/10 PASS**.

## Evidence / artifacts
Risk assessment; RCM; process/system map; control narratives; IPE inventory; key-control list; deficiency/remediation log; control-change log; annual certification; scenario/test scripts.

## Completion assessment
Principles/practice: PASS. Framework/jurisdiction boundary: PASS. RCM schema: PASS. CAO workflow: PASS. Controls/systems/automation: PASS. Scenarios: 10/10 PASS. **Factory status: REVIEWED / production-candidate.**