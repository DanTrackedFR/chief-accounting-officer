# TOPIC-02-005 — Reconciliation Governance & Account Certification

Status: REVIEWED
Capabilities: CAO-02-011, CAO-02-012
Knowledge types: PRINCIPLES, PRACTICE
Framework sensitivity: LOW

## Objective
Create a governed reconciliation operating model so every in-scope account has the right owner, method, frequency, evidence, review and escalation, and certification represents an accounting assertion rather than administrative completion.

## Account inventory
Maintain account number/name; entity; balance type; owner; reviewer; risk rating; materiality; reconciliation method; frequency; source system; due date; key/non-key status; automation status; last completion; open items; policy references.

## Risk scoring
Consider balance/transaction volume, estimation/judgment, fraud susceptibility, manual activity, system interfaces, complexity, history of errors, aged items, volatility, related parties and regulatory/disclosure significance. Risk determines method, frequency and review depth.

## Certification assertion
Certification should mean, as applicable: account is reconciled to appropriate evidence; reconciling items are identified and valid; necessary adjustments are recorded/escalated; classification/cut-off are reasonable; support is retained; no known material issue is omitted. Define certification language explicitly.

## Governance method
1. Reconcile COA/account inventory completeness.
2. Risk-rate accounts and approve scope.
3. Assign owner/reviewer and prevent orphan accounts.
4. Define standard reconciliation method by account class.
5. Establish due dates aligned to close dependencies.
6. Set item-aging and escalation rules.
7. Monitor completion, quality and overdue items separately.
8. Perform quality reviews, not just timeliness checks.
9. Certify at account/entity/close level as designed.
10. Feed recurring exceptions into remediation/automation roadmap.

## Quality metrics
On-time completion; first-pass quality; aged reconciling items; unexplained items; recurring items; post-certification adjustments; reopen events; reviewer rejections; automated-match rate with exception quality; orphan accounts. Avoid a single health score that obscures risk.

## Controls
COA-to-reconciliation completeness; assignment approval; preparer/reviewer; evidence retention; overdue escalation; aged-item review; certification; post-certification adjustment monitoring; periodic risk-rating refresh.

## Failure modes
100% completion but weak support; certifying before source feed final; reviewer same as preparer without compensating review; low-risk label never revisited; zero-balance accounts omitted despite activity risk; netting unrelated reconciling items; auto-certification with unresolved exceptions.

## Systems / automation
Governed workflow should distinguish prepared, reviewed, rejected, certified and reopened states. Automated reconciliations require source lineage, rule versioning, exception retention and human review where judgment remains.

## Artifacts
Account inventory; risk matrix; governance policy; certification statement; dashboard; aging/escalation report; quarterly quality review; automation backlog.

## Scenarios
1. Zero-balance clearing account with high volume: keep in scope due activity/interface risk.
2. Automated bank reconciliation with 99.9% matches: certification still addresses exceptions and source completeness.
3. Account certified then material late journal posted: automatically reopen/re-certify affected account or document governed post-certification treatment.

QA: PASS.