# Regression 001 — Close Core

Date: 2026-09-22
Scope: TOPIC-02-001 through TOPIC-02-010
Status: PASS WITH ARCHITECTURE ACTIONS

## Coverage
All ten Close & GL top-level topics now have substantive knowledge coverage. Topics 02-002, 02-003, 02-004, 02-005, 02-008 and 02-010 were already present and were re-read; 02-001, 02-006, 02-007 and 02-009 were built/filled in this pass.

## Cross-topic routing tests
1. Late vendor invoice for December service -> cut-off -> accrual -> journal -> reconciliation -> flux -> close certification: PASS.
2. Unsupported clearing difference -> suspense/clearing -> reconciliation governance -> journal only after destination treatment established: PASS.
3. Material error discovered after close -> post-close governance -> error-v-estimate classification -> applicable framework correction -> opening-balance continuity: PASS.
4. Fast-close proposal removing review -> close evidence/fast close rejects; transformation routes to dependency/automation redesign: PASS.
5. Automated recurring journal with incomplete source feed -> recurring-journal integrity and interface controls reject despite successful posting: PASS.

## Architecture findings
- Operational topics should reference framework-sensitive recognition topics rather than duplicate GAAP records. Confirmed.
- Effective-date routing is now important beyond leases: IFRS 18 replaces IAS 1 for periods beginning on/after 1 January 2027 and shifts some basis requirements to IAS 8; FRS 102 has further presentation amendments effective 1 January 2027. Company Context must carry reporting-period start and early-adoption status globally.
- Source hierarchy remains valid: FASB Codification is authoritative US GAAP; Concepts Statements are non-authoritative.
- A close case should maintain one issue graph across cut-off, accrual, journal, reconciliation, error assessment and reporting rather than opening disconnected cases.

## QA
No standards text intentionally reproduced. No fabricated paragraph references added. Standards-sensitive conclusions are deliberately routed where current primary-source verification is needed.

## Next family
Revenue & Receivables is the next high-value recurring-controller family after remaining asset/capitalization topics are reconciled with the existing lease vertical slice.
