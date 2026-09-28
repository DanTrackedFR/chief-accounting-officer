# Accounting change and automation — investment and control case

Knowledge type: PRINCIPLES / PRACTICE. Capabilities: CAO-01-013, CAO-01-014. Extends the existing README/completion note; prepared 2026-09-27.

## Select and design

First prove the current workflow's source population, accounting decision, exception patterns, effort and control outcome. Classify each step as eliminate, standardize, automate deterministically or reserve for human judgment. Assess volume, rule stability, data quality, explainability, reversibility, security and periodic changes. A high-volume process with unstable accounting rules may be a poor unattended automation candidate.

Document as-is and to-be flow, requirement-to-policy mapping, interface data contract, approval hierarchy, access/segregation, versioning, failure alerts, reprocessing and rollback. A bot can propose a journal, but policy selection, unusual transactions and material judgment need a named qualified decision maker. Define acceptance tests against an independently constructed expected result, not only agreement with the legacy process, which may itself be wrong.

## Business case and example

Illustrative monthly reconciliation requires 80 staff hours. Automation reduces mechanical work to 20 hours but adds 12 hours of exception review, 5 hours of control monitoring and 3 hours of change maintenance. Net time saved is 40 hours/month, **not** 60. At an illustrative fully loaded 75 per hour, gross annual capacity benefit is 36,000. Subtract 12,000 annual platform cost and 8,000 implementation amortization for an illustrative 16,000 annual net capacity value. Do not present the 40 hours as cash savings unless staffing or spend actually changes. Add risk/quality benefits separately with evidence, and sensitivity-test exception volume and provider downtime.

## Release gate and tests

Before launch, retain approved accounting requirements, representative and negative test cases, parallel-run reconciliations by entity/account/period, source completeness proofs, access evidence, incident simulation and rollback rehearsal. During hypercare compare output against independent source totals and sampled underlying records; keep both versions. Terminate or revert when material unexplained differences persist.

**Failure injection:** rule update changes 10% of prepaid postings to expense before service period. A matching total debit/credit does not pass; expected outcome is failed entity/account/period test, no deployment and documented change correction. If a production release nevertheless posts, assess financial impact and correction through TOPIC-02-008/009 as applicable.

## Source boundary and handoffs

This is operational practice; accounting standards determine the underlying entries, not the automation tool. US issuer ICFR controls may be assessed using [SEC Release 33-8810](https://www.sec.gov/rule-release/33-8810), checked 2026-09-27; applicability is jurisdiction/entity specific. Handoffs: TOPIC-09-003 automated controls, TOPIC-11-003 interface lineage, TOPIC-11-006 access and automation and TOPIC-12-008 exceptions.
