# Phase 2D — Knowledge Factory Progress

Updated: 2026-09-23
Denominator: 156 post-Leases top-level topics to work through.

## Status
- REVIEWED / worked through this phase: **83**
- BLOCKED: **0**
- Remaining not yet worked through: **73**
- Regression reviews: **10**

## Worked-through topics
| Topic range | Status | Notes |
|---|---|---|
| TOPIC-02-001–010 | REVIEWED | Domain 02 Close & GL complete |
| TOPIC-03-001–012 | REVIEWED / production-candidate | Domain 03 Revenue & Receivables complete |
| TOPIC-04-001–006 | REVIEWED / production-candidate | PPE through impairment/goodwill family; lease vertical slice separately proven |
| TOPIC-05-001–010 | REVIEWED / production-candidate | Domain 05 complete: AP, cut-off/accruals, provisions, payroll/benefits, compensation/SBC |
| TOPIC-06-001–010 | REVIEWED / production-candidate | Domain 06 complete: cash/bank, FX, debt, instruments, fair value/derivatives, hedge/investment and impairment/disclosure |
| TOPIC-07-001–009 | REVIEWED / production-candidate | Domain 07 Group Accounting & Consolidation complete |
| TOPIC-08-001–010 | REVIEWED / production-candidate | Domain 08 Financial Reporting complete |
| TOPIC-09-001–009 | REVIEWED / production-candidate | Domain 09 Controls & Governance complete; Regression 009 PASS |
| TOPIC-10-001–007 | REVIEWED / production-candidate | Domain 10 Audit & Assurance Readiness complete; Regression 010 PASS |

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
9. Domain 09 Controls & Governance — PASS. Added jurisdiction gating for SOX/ICFR, reusable IPE object and deficiency-case architecture.
10. Domain 10 Audit & Assurance Readiness — PASS. Added assurance-regime context distinct from accounting framework; evidence-lineage/submission-history requirements; explicit management-versus-auditor conclusion boundaries.

## Current source/effective-date findings
- IFRS 18 replaces IAS 1 and is mandatory for annual periods beginning on or after 1 January 2027, earlier application permitted; transition retrospective.
- AASB 18 timing is entity-type aware: generally 1 January 2027 for relevant for-profit entities and 1 January 2028 for NFP and specified superannuation entities, earlier application permitted.
- FRC February 2026 adapted-format amendments are effective for periods beginning on or after 1 January 2027 for entities choosing those formats; Periodic Review 2024 gating remains relevant from 1 January 2026.
- Domain 09 uses current official PCAOB/SEC jurisdiction anchors; SOX/ICFR is not generalized as an accounting-framework requirement.
- Domain 10 current PCAOB checks: AS 2310 confirmation standard applies for audits of fiscal years ending on/after 15 June 2025; technology-assisted AS 1105/2301 amendments apply for fiscal years beginning on/after 15 December 2025; the AS 1215 page identifies amendments effective 15 December 2026. Assurance effective dates are now treated as context gates.
- Audit evidence supplied by management requires population completeness, source/report parameters, transformation lineage, reconciliation and version history where relevant; auditor risk/independence/conclusions remain auditor responsibilities.

## Repository hygiene
Duplicate folders exist for some stable topic IDs due build retries/concurrent factory writes; Phase 2C lease folder naming does not map one-to-one to the canonical Phase 2B denominator. Canonical topic universe and this ledger—not raw folder counts—are authoritative until a later normalization batch. Do not delete potentially useful duplicate material during active factory scaling.

## Current build sequence
Proceed to Domain 11 Accounting Systems & Data (TOPIC-11-001–010), with regression after 5–10 topics. Operational systems topics receive principles/practice/controls/data-lineage depth; standards-sensitive architecture must still route accounting-framework/effective-period requirements rather than embedding one framework as universal.