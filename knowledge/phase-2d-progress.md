# Phase 2D — Knowledge Factory Progress

Updated: 2026-09-23
Denominator: 156 post-Leases top-level topics to work through.

## Status
- REVIEWED / worked through this phase: **53**
- BLOCKED: **0**
- Remaining not yet worked through: **103**
- Regression reviews: **6**

## Worked-through topics
| Topic range | Status | Notes |
|---|---|---|
| TOPIC-02-001–010 | REVIEWED | Close & GL factory built; duplicate retry folders noted below |
| TOPIC-03-001–012 | REVIEWED / production-candidate | Revenue & receivables family built |
| TOPIC-04-001–006 | REVIEWED / production-candidate | PPE through impairment/goodwill family built |
| TOPIC-05-001–010 | REVIEWED / production-candidate | AP, cut-off/accruals, provisions, onerous contracts, payroll/benefits, bonuses/commissions, SBC, mixed awards/modifications, termination/leave and compensation reconciliation. Domain 05 complete. |
| TOPIC-06-001–010 | REVIEWED / production-candidate | Cash/bank, FX, debt, instruments, fair value/derivatives, hedge/investment and impairment/disclosure factory. Domain 06 complete. |
| TOPIC-07-001–004 | REVIEWED / production-candidate | Consolidation scope/subsidiaries; control/NCI; intercompany accounting/reconciliation; eliminations/unrealized profit. TOPIC-07-002–004 commits 3dc59f5e, 01f7a552, ac255b0b. |
| TOPIC-08-005 | REVIEWED / production-candidate | Going concern/subsequent-events vertical topic already built |

## Blockers
No fully blocked topic. Non-blocking source-depth limitation: public FASB materials do not always expose complete current Codification paragraph bodies. US records affected by this remain PARTIAL at paragraph-level authority rather than receiving unsupported APPROVED status.

## Regression
- Regression 001: early Close & GL factory scaling.
- Regression 002: full Close/GL + Revenue/Receivables cross-topic review. PASS.
- Regression 003: TOPIC-05-001–006 liabilities/compensation review. PASS.
- Regression 004: Domain 05 completion + Domain 06 handoff. PASS.
- Regression 005: TOPIC-06-001–006 FX/debt review. PASS.
- Regression 006: full Domain 06 Cash, FX & Financial Instruments. PASS. Confirmed classification-before-measurement dependency; transaction/re-measurement/translation separation; IFRS/AASB ECL versus US CECL versus FRS 102 separation; effective-date gates; impairment-overlay anti-double-counting; disclosure tie-out dependency; and continued US source-depth guardrail.

## Repository hygiene
Duplicate folders exist for some stable topic IDs due build retries/concurrent factory writes; Phase 2C lease folder naming does not map one-to-one to the canonical Phase 2B denominator. Canonical topic universe and this ledger—not raw folder counts—are authoritative until a later normalization batch. Do not delete potentially useful duplicate material during active factory scaling.

## Current build sequence
Continue Domain 07 with TOPIC-07-005 consolidation journals/system design through TOPIC-07-009 acquisition/disposal/review. Run Regression 007 after another 2–5 canonical topics. Standards-heavy topics require current official-source verification and explicit framework differences.