# TOPIC-09-004 — Control Ownership, Segregation of Duties & Journal Entry Controls

Status: **REVIEWED / production-candidate**  
Primary capabilities: CAO-09-010, CAO-09-011, CAO-09-012  
Knowledge type: PRINCIPLES + PRACTICE + JURISDICTION OVERLAY

## Purpose
Enable the CAO to design accountable control ownership, assess segregation-of-duties (SoD) conflicts from a financial-reporting perspective, and design journal-entry controls that address error and management-override risk without confusing accounting governance with general IT/security administration.

## Authoritative anchors
- PCAOB AS 2401.58–.62: auditors specifically address management override by examining journal entries and other adjustments; understanding the financial-reporting process and controls over journals is part of that work.
- PCAOB AS 2201: ICFR design is risk/assertion driven; controls may be preventive or detective and must operate at sufficient precision.
- SEC Release 33-8810: management's ICFR evaluation is top-down and risk-based; relevant ITGCs are those necessary for financial-reporting controls.

These are US issuer/audit anchors, not universal accounting-framework requirements. IFRS, UK GAAP and AASB do not themselves impose a universal SOX-style control model. Apply local corporate/regulatory requirements through jurisdiction overlays.

## CAO decision model
### 1. Establish the control objective
For each material process/account/disclosure identify: risk, assertion, control objective, control activity, performer, reviewer/approver, frequency, evidence, system dependency and escalation path. Ownership means accountable operation; review means an independent challenge with sufficient competence and authority.

### 2. Design ownership
A control owner must know what failure the control is intended to prevent/detect, what population is in scope, what evidence proves performance, what threshold requires investigation and who resolves exceptions. Avoid nominal ownership where the named owner cannot access evidence or challenge the preparer.

### 3. Assess SoD
Map incompatible financial-reporting capabilities rather than job titles. High-risk combinations include: create/modify master data + initiate transaction; initiate + approve; prepare + post sensitive manual journal; prepare + final-review same reconciliation; administer privileged finance access + perform accounting; create vendor + release payment where the accounting control relies on that separation.

Classify each conflict: prevented by system role; prevented procedurally; detected by independent monitoring; accepted with a documented compensating control; unresolved. Small teams may require compensating review rather than impossible headcount expansion. The compensating control must address the same risk at adequate precision.

### 4. Journal control architecture
Segment journals by risk: automated/interface, recurring standard, manual routine, non-routine, top-side/consolidation, post-close, privileged/admin, and management entries. Define minimum support, preparer/approver independence, approval thresholds, posting rights, period controls, restricted accounts, recurring-template governance, reversal logic and exception monitoring.

For manual/non-routine journals, evidence should normally establish business purpose, accounts/entities/period, amount/calculation, source evidence, accounting rationale, preparer, approver and posting reference. Higher-risk entries warrant stronger approval and/or retrospective analytics.

### 5. Management override
Do not assume approval eliminates override risk. Maintain a complete journal population and enable analytics over unusual users, times, accounts, round amounts, descriptions, period-end/post-close entries, dormant combinations and entries by privileged personnel. Investigation criteria must be documented; analytics are not a substitute for resolving exceptions.

## Required vs recommended vs world-class
**Required by applicable regime:** controls sufficient for the entity's financial-reporting obligations; US issuer ICFR requirements only where applicable.  
**Recommended:** named owner/reviewer, explicit SoD matrix, risk-tiered journal policy, evidence standard, access-to-journal-role mapping, exception log.  
**World-class:** role conflicts continuously monitored; journal risk scoring; workflow-enforced evidence/approval; complete-population analytics; privileged entries separately surfaced; changes to posting roles linked to control impact assessment.  
**Shortcut/risk:** blanket monetary approval thresholds, spreadsheet SoD matrices never reconciled to live roles, self-review, shared accounts, or assuming ERP workflow means the journal is substantively valid.

## Inputs
Entity/regulatory status; close and journal policy; ERP roles; user-role extract; journal population; account/entity hierarchy; approval matrix; privileged-user list; workflow configuration; prior deficiencies/audit findings.

## Outputs/artifacts
- control ownership matrix
- financial-reporting SoD conflict matrix and disposition log
- journal risk taxonomy and approval matrix
- journal evidence standard
- privileged/manual journal monitoring specification
- exception/remediation register
- RCM updates and audit-ready support package

## Controls and evidence
Evidence must show performance, not merely policy existence. For approval controls preserve the item reviewed, review date, reviewer, evidence of challenge/resolution and final disposition. For SoD monitoring preserve population completeness, conflict rules, exceptions, compensating-control evidence and remediation status.

## Systems/data
Reconcile ERP role extracts to HR/user populations and privileged accounts. Confirm journal population completeness to GL totals/counts before analytics. System-enforced workflow should prevent bypass or log overrides. Changes to journal roles/workflows require accounting-control impact review.

## CAO execution
1. Resolve entity/regime and material reporting risks.
2. Obtain process/control and access data.
3. Map control owners and reviewers.
4. Build incompatible-duty rules tied to accounting risks.
5. Test actual role combinations and exceptions.
6. Design journal taxonomy and risk tiers.
7. Set preparation/approval/evidence/posting rules.
8. Design population completeness and journal analytics.
9. Document compensating controls and unresolved gaps.
10. Produce remediation priorities and update Company Accounting Memory with approved governance choices.

## Scenario tests
1. Controller can prepare and approve a $4m acquisition journal: **FAIL** absent an effective independent compensating control; escalate risk and redesign.
2. Three-person finance team cannot fully segregate vendor setup and AP review: **ROUTE** to precise independent payment/vendor-change monitoring, document residual risk.
3. ERP requires approval but CFO has superuser bypass: **ROUTE** privileged-entry monitoring plus independent review; workflow alone is insufficient.
4. Auditor requests journal population: **PRODUCE** complete reconciled extract, control description, risk filters, selected-entry support and exception disposition.

## Completion criteria
PASS when the CAO can distinguish ownership from review, assess actual SoD conflicts, design compensating controls, build a risk-tiered journal control model, address management override, specify evidence and system data, and keep SOX/ICFR obligations jurisdiction-specific.