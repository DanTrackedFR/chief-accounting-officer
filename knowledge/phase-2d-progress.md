# Phase 2D — Knowledge Factory Progress

Updated: 2026-09-23
Denominator: 156 post-Leases top-level topics to work through.

## Status
- REVIEWED / worked through this phase: 37
- BLOCKED: 0
- Remaining not yet worked through: 119
- Regression reviews: 3

## Worked-through topics
| Topic range | Status | Notes |
|---|---|---|
| TOPIC-02-001–010 | REVIEWED | Close & GL factory built; duplicate retry folders noted below |
| TOPIC-03-001–012 | REVIEWED / production-candidate | Revenue & receivables family built |
| TOPIC-04-001–006 | REVIEWED / production-candidate | PPE through impairment/goodwill family built |
| TOPIC-05-001 | REVIEWED / production-candidate | AP accounting + AP-to-GL reconciliation; commits bd9332b9, 21a40827 |
| TOPIC-05-002 | REVIEWED / production-candidate | Expense cut-off + accrual methodology; commits 0a375062, 1c7a4a72 |
| TOPIC-05-003 | REVIEWED / production-candidate | Vendor debit/credits; provisions & contingencies; commit 37d7f131 |
| TOPIC-05-004 | REVIEWED / production-candidate | Onerous contracts; payroll-to-GL; commit 230cd0cc |
| TOPIC-05-005 | REVIEWED / production-candidate | Payroll accruals; employee benefits; commit b83477cd |
| TOPIC-05-006 | REVIEWED / production-candidate | Bonuses; sales incentives/commission compensation; commit 880fdf53 |
| TOPIC-05-007 | REVIEWED / production-candidate | Share-based compensation / employee share schemes; current IFRS 2, ASC 718, FRS 102 Section 26 and AASB 2 routing built; US/UK paragraph-depth guardrails retained |
| TOPIC-05-008 | REVIEWED / production-candidate | Mixed cash/equity awards; modifications, cancellations and settlements; commit 79ec3b71; 9 routing scenarios defined |
| TOPIC-08-005 | REVIEWED / production-candidate | Going concern/subsequent-events vertical topic already built |

## Blockers
No fully blocked topic. Non-blocking source-depth limitation: public FASB materials do not always expose complete current Codification paragraph bodies. US records affected by this remain PARTIAL at paragraph-level authority rather than receiving unsupported APPROVED status.

## Regression
- Regression 001: early Close & GL factory scaling.
- Regression 002: full Close/GL + Revenue/Receivables cross-topic review. Passed with repository-hygiene and US source-depth actions.
- Regression 003: TOPIC-05-001–006 liabilities/compensation review. PASS. Confirmed accrual-v-provision boundary, contract-specific onerous routing, payroll accounting boundary, employee-benefit/SBC boundary, sales-commission contract-cost routing and continued US source-depth guardrail.

## Repository hygiene
Duplicate folders exist for some TOPIC-02 IDs due build retries; Phase 2C lease folder naming does not map one-to-one to the canonical Phase 2B denominator. Canonical topic universe and this ledger—not raw folder counts—are authoritative until a later normalization batch. Do not delete potentially useful duplicate material during active factory scaling.

## Current build sequence
Continue TOPIC-05-009–010 termination/leave accounting and compensation reconciliations, then Domain 06 bank/cash/FX/financial instruments. Run Regression 004 no later than completion of the next five canonical topics. Standards-heavy topics require current official-source verification and framework differences; operational topics receive principles/practice/controls/systems depth without artificial four-framework records.