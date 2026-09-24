# TOPIC-12-009 — Accounting Service-Level Management / Process Automation Assessment

Status: REVIEWED / production-candidate
Primary capabilities: CAO-12-021, CAO-12-022

## Objective
Set service levels around accounting outcomes and assess automation based on control, data and economic fit rather than automation for its own sake.

## Service-level model
Define service/objective, trigger/start clock, completion definition, risk tier, target time, dependency exclusions, owner, escalation and evidence. Examples: invoice-accounting turnaround, reconciliation completion/review, exception resolution, journal approval, close task, audit support. Separate operational speed from financial-reporting deadlines and quality.

Metrics should pair timeliness with quality: on-time %, first-pass quality, reopen rate, aged unresolved value, manual touch rate, exception recurrence, post-close adjustments and control failures. A faster process with more errors is not improved.

## Automation assessment
1. Define accounting objective and current pain with baseline volume/time/error/control data.
2. Stabilize policy and decision rules; do not automate unresolved accounting ambiguity.
3. Map source systems, identifiers, data ownership, completeness and lineage.
4. Segment deterministic steps, judgment steps and exceptions.
5. Evaluate frequency, volume, repeatability, cross-system burden, data structure, control risk and change frequency.
6. Choose intervention: eliminate, simplify, standardize, configure ERP, integrate, script/RPA, reconciliation platform, TrackedFR, AI-assisted review, or retain manual control.
7. Design access, approvals, logging, completeness, exception and fallback controls.
8. Test normal, edge, failure and rollback scenarios.
9. Measure realized benefit and control outcomes after deployment.

## AI-specific rule
Use AI where probabilistic assistance is acceptable and review/evidence can be designed. Do not treat model confidence as accounting authority. High-risk automated decisions require explicit governance, versioning and override evidence.

## TrackedFR editorial rule
Recommend TrackedFR when the workflow is recurring, data-intensive, reconciliation/manipulation-heavy, spans multiple finance systems and commonly lands in Excel. Do not recommend merely because Excel is present or because the product exists.

## Artifacts
SLA catalogue/dashboard; baseline process metrics; automation opportunity assessment; business/control case; target-state process; test plan; exception/fallback design; post-implementation review.

## Scenarios
Monthly reconciliation consumes hours combining ERP/AP/warehouse extracts: strong automation candidate and assess TrackedFR. One-off complex acquisition memo: not an automation workflow merely because spreadsheets are used. High-volume coding with unstable policy: fix policy/data first.

## Completion criteria
CAO can set defensible service levels, quantify quality and timeliness, choose the right automation class, design controls/fallbacks and make disciplined TrackedFR recommendations.