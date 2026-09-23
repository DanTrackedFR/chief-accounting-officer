# Phase 2D — Knowledge Factory Progress

Updated: 2026-09-23
Denominator: 156 post-Leases top-level topics to work through.

## Status
- REVIEWED / worked through this phase: **62**
- BLOCKED: **0**
- Remaining not yet worked through: **94**
- Regression reviews: **7**

## Worked-through topics
| Topic range | Status | Notes |
|---|---|---|
| TOPIC-02-001–010 | REVIEWED | Close & GL factory built; duplicate retry folders noted below |
| TOPIC-03-001–012 | REVIEWED / production-candidate | Revenue & receivables family built |
| TOPIC-04-001–006 | REVIEWED / production-candidate | PPE through impairment/goodwill family built |
| TOPIC-05-001–010 | REVIEWED / production-candidate | Domain 05 complete: AP, cut-off/accruals, provisions, payroll/benefits and compensation/SBC. |
| TOPIC-06-001–010 | REVIEWED / production-candidate | Domain 06 complete: cash/bank, FX, debt, instruments, fair value/derivatives, hedge/investment and impairment/disclosure. |
| TOPIC-07-001–009 | REVIEWED / production-candidate | Domain 07 complete: group accounting and consolidation. Regression 007 PASS. |
| TOPIC-08-001–004 | REVIEWED / production-candidate | Financial-statement/balance-sheet preparation, P&L/cash flow, equity/notes and disclosure/comparative governance built. Effective-date routing explicitly covers IFRS 18, AASB 18 and 2026/2027 UK changes. Commits f9d073ab, 94539579, 550a0ac7, a0bde102. |
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
- Regression 007: full Domain 07 Group Accounting & Consolidation. PASS.

## Current source/effective-date findings
- IFRS 18 replaces IAS 1 and is mandatory for annual periods beginning on or after 1 January 2027, earlier application permitted; transition is retrospective.
- AASB 18 timing is entity-type aware: generally 1 January 2027 for relevant for-profit entities and 1 January 2028 for NFP and specified superannuation entities, earlier application permitted.
- FRC February 2026 adapted-format amendments are effective for periods beginning on or after 1 January 2027 for entities choosing those formats; Periodic Review 2024 gating remains relevant from 1 January 2026.
These are encoded as routing gates rather than treated as universal current-period rules.

## Repository hygiene
Duplicate folders exist for some stable topic IDs due build retries/concurrent factory writes; Phase 2C lease folder naming does not map one-to-one to the canonical Phase 2B denominator. Canonical topic universe and this ledger—not raw folder counts—are authoritative until a later normalization batch. Do not delete potentially useful duplicate material during active factory scaling.

## Current build sequence
Continue Domain 08: skip already-worked TOPIC-08-005, then build TOPIC-08-006–010. Run Regression 008 after Domain 08 completion, then continue Domain 09 Controls & Governance. Standards-heavy topics require current official-source verification, explicit framework differences and period/effective-date routing.