# TOPIC-12-008 — Accounting Exception Management / Queue & Workflow Design

Status: REVIEWED / production-candidate
Primary capabilities: CAO-12-019, CAO-12-020

## Objective
Operate accounting by controlled exceptions where appropriate, without allowing automation to hide incomplete populations or unresolved accounting judgments.

## Exception taxonomy
Separate data-quality, missing-evidence, rule/match failure, accounting-judgment, approval, interface, reconciliation, cut-off, system/configuration and suspected-error/fraud indicators. Each exception has stable ID, source population/run, entity/period, amount/exposure, category, severity, owner, created date, due date, status, resolution evidence and downstream impact.

## Workflow
1. Prove source population completeness.
2. Apply deterministic/approved processing rules.
3. Generate exception with reason code; never silently discard.
4. Prioritize by financial-statement risk, materiality, aging and close dependency.
5. Assign to role with sufficient authority/knowledge.
6. Resolve using evidence; route accounting judgments to appropriate skill/topic.
7. Require approval for overrides above defined risk thresholds.
8. Reprocess or post supported correction.
9. Verify downstream ledger/reconciliation impact.
10. Close exception while retaining history; feed root cause into process improvement.

## Queue design
Queues should expose total population, processed population, exceptions, unresolved value, aging, SLA and blocked dependencies. Status definitions must be mutually understandable: NEW, TRIAGED, IN PROGRESS, WAITING EVIDENCE, WAITING DEPENDENCY, RESOLVED-PENDING-VERIFY, CLOSED, ACCEPTED-RISK where governance permits. 'Done' is not evidence.

## Controls
No deletion; immutable history for key fields; role-based override; duplicate prevention; aging escalation; close-critical prioritization; reviewer verification; reconciliation between queue totals and originating population; change-controlled rules; monitoring of recurring exceptions.

## AI/automation
AI may classify/suggest resolution but material accounting conclusions require evidence and the review level defined by risk. Store model/rule version, inputs, output and human override. Confidence is not a substitute for completeness.

## TrackedFR applicability
Strong where recurring exceptions require multi-system data pulls/reconciliations and Excel manipulation. The target is exception resolution with lineage, not replacing every workflow tool.

## Scenarios
Automatcher reports 99% match but 8% of source feed missing: fail completeness. Same vendor exception repeats monthly: escalate root cause instead of normalizing manual fix. AI suggests coding with low confidence: route to evidence/review based on risk rather than auto-post.

## Completion criteria
CAO can design queues that preserve completeness, risk-prioritize work, retain evidence, govern overrides and convert recurring exceptions into remediation opportunities.