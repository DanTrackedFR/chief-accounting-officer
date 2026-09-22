# TOPIC-02-002 — Journal Entry Preparation / Review / Manual Journal Governance

Status: REVIEWED
Capabilities: CAO-02-004, CAO-02-005, CAO-02-006
Sensitivity: L

## Objective
Ensure journals are valid, complete, period-correct, supported, approved and traceable, with stronger governance for manual/non-standard entries.

## PRINCIPLES
A journal is the controlled mechanism for recording an accounting conclusion in the ledger. The accounting basis comes from the relevant substantive topic; journal governance ensures that conclusion is faithfully translated into accounts, entities, dimensions, currency and period.

Manual journals carry elevated error/fraud/override risk because they can bypass normal subledger controls. Governance should be risk-based rather than treating every entry identically.

## CAO method
1. Identify business/accounting event and authoritative accounting conclusion.
2. Resolve entity, book, period, currency, accounts and dimensions.
3. Build debit/credit logic and confirm balance.
4. Attach calculation and source evidence sufficient for a reviewer to reperform/understand the entry.
5. Distinguish recurring, standard, automated, manual-standard and manual-nonstandard entries.
6. Apply approval thresholds and segregation appropriate to risk/materiality.
7. Validate posting period, duplicate risk, restricted accounts and unusual users/times.
8. Post through controlled workflow; preserve immutable ID/evidence/audit trail.
9. Confirm expected ledger effect and downstream reconciliation.
10. Reverse where appropriate using controlled reversal date/logic.

## Required journal record
Journal ID; entity/book; period; currency; account/dimension lines; debit/credit; description/business purpose; accounting basis/topic; preparer; reviewer/approver; source/calculation; posting timestamp/user; recurring/reversal status; related case/control; exceptions.

## Review standard
Reviewer should challenge accounting basis, arithmetic, completeness, account/entity/dimension coding, period, evidence, consistency and unusual characteristics. Approval is not a click-only control.

## Manual journal risk analytics
Prioritize entries posted by privileged users; late/post-close entries; unusual accounts; round amounts; dormant/new accounts; unusual combinations; entries just below approval thresholds; entries posted/reversed quickly; entries without expected source; weekend/out-of-hours activity where relevant; self-prepared/approved entries; recurring 'one-offs'. Analytics are risk indicators, not proof of error/fraud.

## Controls
Role-based posting rights; preparer/approver segregation; threshold-based approval; restricted account rules; closed-period controls; required support; recurring template governance; automated-interface monitoring; duplicate detection; post-close journal report; periodic privileged-access review; journal population completeness for audit.

## Framework
No four-framework journal mechanics should be fabricated. Recognition/measurement comes from the underlying IFRS/ASC/FRS 102/AASB topic. The journal layer preserves the framework conclusion and evidence.

## Systems
Prefer workflow-generated IDs, enforced required fields, approval logs and source links. Spreadsheet upload templates need version/access/completeness controls. Automated journals require interface/configuration/change monitoring and reconciliation.

## Artifacts
JE template; journal policy; approval matrix; manual-JE risk report; recurring-JE register; post-close journal review; audit population.

## Tests
- Unsupported accrual: reject/return for methodology/evidence rather than approve because it balances.
- CFO posts late material manual JE: route through override/independent review and preserve evidence; title alone does not waive control.
- Automated recurring entry changes after system configuration: require change evidence and validate resulting posting.
- Wrong dimension but correct total: fail because faithful ledger classification matters.

## QA
PASS for factory purposes. Underlying accounting remains delegated to substantive knowledge topics.
