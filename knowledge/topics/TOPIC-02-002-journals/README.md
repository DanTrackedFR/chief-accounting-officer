# TOPIC-02-002 — Journal Entry Preparation, Review & Manual Journal Governance

Status: REVIEWED — Phase 2D
Primary capabilities: CAO-02-004, CAO-02-005, CAO-02-006

## Principle
A journal is an execution mechanism for an accounting conclusion, not evidence of the conclusion itself. Every material/manual journal must be traceable to the underlying transaction, calculation, accounting basis, period, entity and approval.

## CAO workflow
1. Establish business event and accounting objective.
2. Resolve entity, period, currency and ledger/book.
3. Retrieve the governing accounting topic/policy.
4. Build calculation/support and source population.
5. Construct balanced debit/credit lines with valid dimensions.
6. Validate cut-off, classification, intercompany/tax-sensitive fields and reversal behavior.
7. Determine materiality/risk and required reviewer.
8. Post through approved mechanism; prohibit uncontrolled direct production changes.
9. Retain evidence and posting identifier.
10. Reconcile/verify downstream result; monitor reversal/recurrence.

## Manual-journal risk taxonomy
Higher-risk indicators include unusual account combinations; senior-management posting; late/post-close entry; round-dollar/manual estimate; unsupported top-side entry; dormant/new account; entry just below approval threshold; revenue/reserve/equity impact; nonstandard user; weekend/out-of-hours posting; manual override of automated flow.

Indicators trigger scrutiny; they are not proof of error or fraud.

## Minimum support
Purpose; accounting basis/policy; source; calculation; preparer; reviewer; entity/period; journal lines; dimensions; reversal instruction; material judgment; related-party/intercompany flag where relevant; evidence link; posting ID.

## Controls
Maker-checker independence appropriate to risk; approval matrix; restricted posting access; duplicate detection; period lock; high-risk journal analytics; completeness of recurring reversals; post-posting verification; audit trail; emergency-entry governance.

## Systems
Prefer standardized journal templates/imports with validation, controlled recurring journals, workflow approvals and immutable posting logs. Automated journals require change/configuration controls and interface monitoring rather than weaker review merely because they are automated.

## Tests
- Unsupported revenue top-side entry: block and request accounting/source support.
- Valid recurring accrual: verify basis, amount, dimensions, reversal and owner before posting.
- CFO-created late journal: apply same or heightened governance; title does not bypass control.
- Automated journal changes after ERP release: require change evidence and output validation.

## Completion
Journal governance is complete when accounting basis, calculation, authorization, posting and downstream verification are all traceable.
