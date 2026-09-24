# Phase 2D — Knowledge Factory Progress

Updated: 2026-09-23
Denominator: 156 post-Leases top-level topics to work through.

## Status
- REVIEWED / worked through this phase: **88**
- BLOCKED: **0**
- Remaining not yet worked through: **68**
- Regression reviews: **11**

## Worked-through topics
| Topic range | Status | Notes |
|---|---|---|
| TOPIC-02-001–010 | REVIEWED | Domain 02 Close & GL complete |
| TOPIC-03-001–012 | REVIEWED / production-candidate | Domain 03 Revenue & Receivables complete |
| TOPIC-04-001–006 | REVIEWED / production-candidate | PPE through impairment/goodwill family; lease vertical slice separately proven |
| TOPIC-05-001–010 | REVIEWED / production-candidate | Domain 05 complete |
| TOPIC-06-001–010 | REVIEWED / production-candidate | Domain 06 complete |
| TOPIC-07-001–009 | REVIEWED / production-candidate | Domain 07 complete |
| TOPIC-08-001–010 | REVIEWED / production-candidate | Domain 08 complete |
| TOPIC-09-001–009 | REVIEWED / production-candidate | Domain 09 complete; Regression 009 PASS |
| TOPIC-10-001–007 | REVIEWED / production-candidate | Domain 10 complete; Regression 010 PASS |
| TOPIC-11-001–005 | REVIEWED / production-candidate | ERP/COA/dimensions; books/subledgers/master data; interfaces/reconciliation/lineage; data quality/requirements/ERP design; migration/cutover/opening balances. Regression 011 PASS |

## Blockers
No fully blocked topic. Non-blocking source-depth limitation: public FASB materials do not always expose complete current Codification paragraph bodies. US records affected by this remain PARTIAL at paragraph-level authority rather than receiving unsupported APPROVED status.

## Regression
1. Early Close & GL factory scaling — PASS.
2. Full Close/GL + Revenue/Receivables — PASS.
3. TOPIC-05-001–006 liabilities/compensation — PASS.
4. Domain 05 completion + Domain 06 handoff — PASS.
5. TOPIC-06-001–006 FX/debt — PASS.
6. Domain 06 Cash, FX & Financial Instruments — PASS.
7. Domain 07 Group Accounting & Consolidation — PASS.
8. Domain 08 Financial Reporting — PASS.
9. Domain 09 Controls & Governance — PASS.
10. Domain 10 Audit & Assurance Readiness — PASS.
11. Domain 11A Accounting Systems & Data (TOPIC-11-001–005) — PASS. Added reusable accounting-sensitive-configuration, interface-run and migration-adjustment concepts; confirmed effective dating and transaction-level lineage as first-class requirements.

## Current source/effective-date findings
- IFRS 18 replaces IAS 1 and is mandatory for annual periods beginning on or after 1 January 2027, earlier application permitted; transition retrospective.
- AASB 18 timing is entity-type aware: generally 1 January 2027 for relevant for-profit entities and 1 January 2028 for NFP and specified superannuation entities, earlier application permitted.
- FRC February 2026 adapted-format amendments are effective for periods beginning on or after 1 January 2027 for entities choosing those formats; Periodic Review 2024 gating remains relevant from 1 January 2026.
- Domain 09 uses current official PCAOB/SEC jurisdiction anchors; SOX/ICFR is not generalized as an accounting-framework requirement.
- Domain 10 assurance effective dates are context gates rather than accounting-framework requirements.

## Repository hygiene
Duplicate folders exist for some stable topic IDs due build retries/concurrent factory writes; Phase 2C lease folder naming does not map one-to-one to the canonical Phase 2B denominator. Canonical topic universe and this ledger—not raw folder counts—are authoritative until a later normalization batch.

## Current build sequence
Complete Domain 11 with TOPIC-11-006–010 (access/roles, automation, spreadsheet/EUC governance, warehouse/reporting layer, AI/change impact, integration monitoring/reconciliation automation), then proceed to Domain 12 Accounting Operations. Operational systems topics receive PRINCIPLES/PRACTICE/controls/data-lineage depth; standards-sensitive configuration routes to the applicable framework/topic/effective period.