# Phase 2D — Knowledge Factory Progress

Updated: 2026-09-23
Denominator: 156 post-Leases top-level topics to work through.

## Status
- REVIEWED / worked through this phase: 41
- BLOCKED: 0
- Remaining not yet worked through: 115
- Regression reviews: 4

## Worked-through topics
| Topic range | Status | Notes |
|---|---|---|
| TOPIC-02-001–010 | REVIEWED | Close & GL factory built; duplicate retry folders noted below |
| TOPIC-03-001–012 | REVIEWED / production-candidate | Revenue & receivables family built |
| TOPIC-04-001–006 | REVIEWED / production-candidate | PPE through impairment/goodwill family built |
| TOPIC-05-001–006 | REVIEWED / production-candidate | AP, cut-off/accruals, provisions, onerous contracts, payroll/benefits, bonuses/commissions |
| TOPIC-05-007 | REVIEWED / production-candidate | Share-based compensation / employee share schemes; current IFRS 2, ASC 718, FRS 102 Section 26 and AASB 2 routing built; US/UK paragraph-depth guardrails retained |
| TOPIC-05-008 | REVIEWED / production-candidate | Mixed cash/equity awards; modifications, cancellations and settlements; commit 79ec3b71; 9 routing scenarios defined |
| TOPIC-05-009 | REVIEWED / production-candidate | Severance/termination benefits and vacation/leave liabilities; commit a3d09f34; 10 scenarios |
| TOPIC-05-010 | REVIEWED / production-candidate | Compensation reconciliations and expense classification; commit ee54ea1f; 10 scenarios. Domain 05 complete |
| TOPIC-06-001 | REVIEWED / production-candidate | Bank reconciliation, cash in transit and restricted cash; commit 0399b8a5; current IAS 7/IFRIC, AASB 107, FRS 102 and ASC 230 routing; 10 scenarios |
| TOPIC-06-002 | REVIEWED / production-candidate | Cash classification/presentation and foreign-currency transaction accounting; commits bccd5373, d9b7bbce, b0dfe1fb, a1d56765; current IAS 7/IAS 21, AASB 107/121, FRS 102 Sections 7/30 and ASC 230/830 routing; 10/10 scenarios PASS. Effective-period gates include IFRS/AASB presentation changes, UK 2026 Periodic Review and exchangeability considerations. |
| TOPIC-08-005 | REVIEWED / production-candidate | Going concern/subsequent-events vertical topic already built |

## Blockers
No fully blocked topic. Non-blocking source-depth limitation: public FASB materials do not always expose complete current Codification paragraph bodies. US records affected by this remain PARTIAL at paragraph-level authority rather than receiving unsupported APPROVED status.

## Regression
- Regression 001: early Close & GL factory scaling.
- Regression 002: full Close/GL + Revenue/Receivables cross-topic review. Passed with repository-hygiene and US source-depth actions.
- Regression 003: TOPIC-05-001–006 liabilities/compensation review. PASS. Confirmed accrual-v-provision boundary, contract-specific onerous routing, payroll accounting boundary, employee-benefit/SBC boundary, sales-commission contract-cost routing and continued US source-depth guardrail.
- Regression 004: Domain 05 completion + Domain 06 handoff. PASS. Confirmed service-v-termination routing, leave liability boundary, compensation-reconciliation inheritance of technical topics, restructuring double-count prevention, and bank/cash reconciliation separation from treasury operations. Reconfirmed that framework overlays are not manufactured for operational reconciliation mechanics.

## Repository hygiene
Duplicate folders exist for some TOPIC-02 IDs due build retries; Phase 2C lease folder naming does not map one-to-one to the canonical Phase 2B denominator. Canonical topic universe and this ledger—not raw folder counts—are authoritative until a later normalization batch. Do not delete potentially useful duplicate material during active factory scaling.

## Current build sequence
Continue TOPIC-06-003–010 FX remeasurement/translation, functional currency, debt and financial instruments. Standards-heavy topics require current official-source verification and explicit framework differences. Run Regression 005 after no more than another 4–7 canonical topics.