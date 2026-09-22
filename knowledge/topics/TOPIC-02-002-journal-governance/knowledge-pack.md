# TOPIC-02-002 — Journal Preparation, Review & Manual Journal Governance

Status: REVIEWED
Capabilities: CAO-02-004, CAO-02-005, CAO-02-006
Knowledge types: PRINCIPLES, PRACTICE
Framework sensitivity: LOW; underlying accounting conclusion remains framework-sensitive.

## Objective
Ensure every journal is valid, complete, accurate, authorized, traceable and posted in the correct entity, period, accounts and dimensions.

## Required journal package
Journal ID/type; entity/book; period; preparer; approver; purpose; accounting basis; source/evidence; calculation; debit/credit lines; currency/FX basis; dimensions; recurring/reversing status; reversal date; material judgment; related reconciliation; posting timestamp; ERP user; approval evidence.

## CAO preparation method
1. Establish business event and accounting objective.
2. Resolve framework/policy if accounting treatment is not routine.
3. Validate source population completeness and period/entity.
4. Reperform calculation and map accounts/dimensions.
5. Confirm debits=credits and signs/currency.
6. Determine reversal logic.
7. Attach evidence sufficient for an independent reviewer.
8. Route approval based on risk/materiality, not only amount.
9. Post and confirm ERP journal ID/status.
10. Link to reconciliation or rollforward affected.

## Review standard
Reviewer should understand purpose without oral explanation; challenge treatment, period, population, assumptions, calculation, mapping, unusual accounts, round-dollar entries, manual overrides and reversal. Evidence of clicking approve is not evidence of substantive review.

## Manual journal governance
Maintain journal types and approved sources. Restrict posting rights. Separate preparation/approval where practicable. Use thresholds plus qualitative risk triggers. Monitor late, top-side, unusual-user, unusual-account, weekend/out-of-hours, round-dollar, duplicate and post-close journals. Emergency access requires retrospective review.

## Required vs recommended
Accounting frameworks determine recognition/measurement, not a universal journal approval workflow. Approval matrices, SoD, anomaly monitoring and standardized templates are CAO control practice; jurisdictional ICFR/SOX obligations may elevate them into formal control requirements.

## Failure modes
Unsupported plug; spreadsheet total not tied to source; copied prior-month journal; wrong entity; stale FX rate; hidden hardcodes; preparer approves own material journal; recurring manual entry that should be automated; reversal omitted/doubled; post-close entry bypasses reopen governance.

## Controls / audit
Journal access control; approval; source-to-journal tie; automated validation; duplicate detection; completeness report; manual-journal analytics; post-close journal review; retained evidence. Audit package should allow sample reperformance from source to ledger.

## Systems
Prefer controlled recurring journals and source-system/subledger accounting where stable. Automation requires deterministic source, mapping, validation, exception handling and monitoring; do not automate a weak accounting conclusion.

## Artifacts
Journal template; review checklist; approval matrix; manual-journal policy; exception dashboard; sample audit support pack.

## Scenarios
1. $5m recurring accrual copied from prior month: fail until current source/estimate is supported.
2. $5k executive-related unusual journal below threshold: qualitative risk still triggers review.
3. Automated monthly allocation: require source completeness, mapping and exception controls, not manual approval theater.

QA: PASS for principles/practice.