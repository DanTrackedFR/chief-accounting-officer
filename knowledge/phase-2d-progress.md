# Phase 2D — Knowledge Factory Progress

Updated: 2026-09-22
Denominator: 156 post-Leases top-level topics to work through.

## Status
- REVIEWED / worked through this phase: 22
- BLOCKED: 0
- Remaining not yet worked through: 134
- Regression reviews: 2

## Worked-through topics
| Topic range | Status | Key commits |
|---|---|---|
| TOPIC-02-001–010 | REVIEWED | 86422401 through 8afbe6b9 |
| TOPIC-03-001–006 | REVIEWED / production-candidate | see build-roadmap Batch 003–004 |
| TOPIC-03-007 | REVIEWED | 860aaf6c |
| TOPIC-03-008 | REVIEWED | 37bd85d5 |
| TOPIC-03-009 | REVIEWED | 0197536f |
| TOPIC-03-010 | REVIEWED | 35ab988d |
| TOPIC-03-011 | REVIEWED | b8bb2e61 |
| TOPIC-03-012 | REVIEWED | c6083893 |

## Blockers
No fully blocked topic. Non-blocking source-depth limitation: public FASB materials do not always expose complete current Codification paragraph bodies. US records affected by this remain PARTIAL at paragraph-level authority rather than receiving unsupported APPROVED status.

## Regression
- Regression 001: early Close & GL factory scaling.
- Regression 002 (`53f16809`): full Close/GL + Revenue/Receivables cross-topic review. Passed with repository-hygiene and US source-depth actions. Confirmed reusable primitives for population completeness, classification, calculation, posting, reconciliation, disclosure and exception governance.

## Repository hygiene
Duplicate folders exist for some TOPIC-02 IDs due build retries; Phase 2C lease folder naming also does not map one-to-one to the canonical Phase 2B denominator. Canonical topic universe and this ledger—not raw folder counts—are authoritative until a later normalization batch.

## Next build sequence
Assets/capitalization and liabilities/expenses recurring-controller core, then bank/cash/FX, intercompany and primary financial reporting. Standards-heavy topics continue to require current official-source verification and framework differences; operational topics receive principles/practice/controls/systems depth without artificial four-framework records.