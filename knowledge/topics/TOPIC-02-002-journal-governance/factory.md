# TOPIC-02-002 — Journal Entry Preparation / Review / Manual Journal Governance

Status: REVIEWED
Capabilities: CAO-02-004, CAO-02-005, CAO-02-006
Knowledge mix: PRINCIPLES + PRACTICE; underlying debit/credit conclusion inherits the relevant accounting topic/framework.

## Objective
Ensure every journal is valid, complete, correctly classified, period-appropriate, supported, authorized and traceable from business event to ledger and financial statement.

## Journal taxonomy
System-generated; recurring automated; recurring manual; standard manual; estimate/judgment; top-side/consolidation; reclassification; correction; post-close; prior-period; interface/error correction. Risk and review rules should differ by taxonomy.

## Required journal package
Entity/book; period; journal type; business purpose; accounts/dimensions; debit/credit lines; currency; preparer; source data; calculation; accounting basis/policy; material judgments; reversal treatment; attachments/evidence; related reconciliation; reviewer/approver; posting timestamp; system journal ID.

## CAO workflow
1. Establish the economic event and applicable accounting topic.
2. Determine recognition, measurement, classification and period before constructing the entry.
3. Validate entity, account, dimensions, currency and posting date.
4. Reperform calculation or trace to governed source.
5. Evaluate whether reversal is required and whether reversal creates next-period distortion.
6. Apply risk-tiered review based on amount, account, manual nature, user, timing, complexity and unusual combinations.
7. Post only after required approval unless documented emergency/post-close governance permits otherwise.
8. Link to reconciliation and close evidence.

## Manual-journal risk indicators
Late/post-close posting; round-dollar values; unusual account combinations; senior-user/self-posting; direct posting to revenue/cash/equity/reserves; entries just below review thresholds; recurring 'one-off' journals; vague descriptions; spreadsheet-only source; repeated reversals/reposts; unsupported top-side entries.

These indicators trigger review; they do not prove error or fraud.

## Review standard
Reviewer must understand the purpose, inspect evidence, challenge accounting treatment and assumptions, validate account/entity/period, check arithmetic and assess consistency with policy/prior periods. Clicking approve is not review evidence.

## Control design
Role-based posting access; preparer cannot approve own high-risk entry; approved templates for recurring entries; workflow thresholds; restricted sensitive accounts; duplicate detection; period locks; late-journal report; audit trail; recurring-journal recertification; monitoring of privileged users; controlled emergency posting.

## Automation
Automate deterministic recurring journals only after source lineage, calculation logic, posting rules, exception handling, ownership and change control are established. Automated does not mean uncontrolled: interface completeness, job monitoring, failed-posting queues and change governance remain required.

## Common failures
Journal explains mechanics but not business event; support does not tie to amount; entry posted to wrong entity/period; review occurs after posting without exception approval; recurring template becomes stale; reversal omitted; entry masks unreconciled balance; threshold splitting.

## Artifacts
Journal policy; taxonomy/risk matrix; preparation checklist; review checklist; manual-journal dashboard; recurring-journal register; late-journal report; sensitive-account matrix; exception log.

## Scenarios
A. $2m manual revenue top-side entry on final close day: high risk; require revenue accounting basis, contract/source support, calculation, independent senior review and disclosure/control implications.
B. Monthly rent accrual from approved schedule: recurring template can automate if schedule/change controls are governed.
C. CFO posts directly to equity: authority does not remove independent review or evidence requirement.

## QA
PASS: separates accounting conclusion from posting mechanics; risk-tiers journals; addresses access, evidence, review, late posting and automation.