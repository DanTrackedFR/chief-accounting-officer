# Phase 2D — Knowledge Factory Progress

Updated: 2026-09-23
Denominator: 156 post-Leases top-level topics to work through.

## Status
- REVIEWED / worked through this phase: **58**
- BLOCKED: **0**
- Remaining not yet worked through: **98**
- Regression reviews: **7**

## Worked-through topics
| Topic range | Status | Notes |
|---|---|---|
| TOPIC-02-001–010 | REVIEWED | Close & GL factory built; duplicate retry folders noted below |
| TOPIC-03-001–012 | REVIEWED / production-candidate | Revenue & receivables family built |
| TOPIC-04-001–006 | REVIEWED / production-candidate | PPE through impairment/goodwill family built |
| TOPIC-05-001–010 | REVIEWED / production-candidate | AP, cut-off/accruals, provisions, onerous contracts, payroll/benefits, bonuses/commissions, SBC, mixed awards/modifications, termination/leave and compensation reconciliation. Domain 05 complete. |
| TOPIC-06-001–010 | REVIEWED / production-candidate | Cash/bank, FX, debt, instruments, fair value/derivatives, hedge/investment and impairment/disclosure factory. Domain 06 complete. |
| TOPIC-07-001–009 | REVIEWED / production-candidate | Domain 07 complete: perimeter/control/NCI, intercompany, eliminations, consolidation journals/system, foreign operations/group COA, group packages/equity method, joint arrangements/ownership changes, acquisitions/disposals and final consolidation review. Latest commits b2f9d15a, 33a0a693, 481355c9, 5278d36a, 6f9010c5. |
| TOPIC-08-005 | REVIEWED / production-candidate | Going concern/subsequent-events vertical topic already built |

## Blockers
No fully blocked topic. Non-blocking source-depth limitation: public FASB materials do not always expose complete current Codification paragraph bodies. US records affected by this remain PARTIAL at paragraph-level authority rather than receiving unsupported APPROVED status.

## Regression
- Regression 001: early Close & GL factory scaling.
- Regression 002: full Close/GL + Revenue/Receivables cross-topic review. PASS.
- Regression 003: TOPIC-05-001–006 liabilities/compensation review. PASS.
- Regression 004: Domain 05 completion + Domain 06 handoff. PASS.
- Regression 005: TOPIC-06-001–006 FX/debt review. PASS.
- Regression 006: full Domain 06 Cash, FX & Financial Instruments. PASS.
- Regression 007: full Domain 07 Group Accounting & Consolidation. PASS. Confirmed perimeter-before-mechanics, transformation lineage, ownership-boundary routing, equity-method/joint-arrangement separation, effective-date gates and certification bridges. Commit 8b2450a1.

## Repository hygiene
Duplicate folders exist for some stable topic IDs due build retries/concurrent factory writes; Phase 2C lease folder naming does not map one-to-one to the canonical Phase 2B denominator. Canonical topic universe and this ledger—not raw folder counts—are authoritative until a later normalization batch. Do not delete potentially useful duplicate material during active factory scaling.

## Current build sequence
Domain 07 is complete. Continue Domain 08 Financial Reporting: TOPIC-08-001–004, skip already-worked TOPIC-08-005, then TOPIC-08-006–010. Run Regression 008 after 5–9 new canonical topics. Standards-heavy topics require current official-source verification, explicit framework differences and period/effective-date routing.