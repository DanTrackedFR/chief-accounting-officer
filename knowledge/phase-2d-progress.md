# Phase 2D — Knowledge Factory Progress

Updated: 2026-09-24
Denominator: 156 post-Leases top-level topics to work through.

## Status
- REVIEWED / worked through this phase: **110**
- BLOCKED: **0**
- Remaining not yet worked through: **46**
- Regression reviews: **13**

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
| TOPIC-11-001–010 | REVIEWED / production-candidate | Domain 11 complete; Regression 012 PASS |
| TOPIC-12-001–009 | REVIEWED / production-candidate | Domain 12 complete; Regression 013 PASS |
| TOPIC-13-001–008 | REVIEWED / production-candidate | Business combinations/PPA through complex contracts/related parties. TOPIC-13-006 debt restructuring/equity financing and TOPIC-13-007 convertibles/warrants preserve framework-specific classification/modification routing and current-v-pipeline separation. TOPIC-13-008 separates transaction-specific recognition/measurement from related-party disclosure and adds complete-contract/side-letter orchestration. |

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
11. Domain 11A Accounting Systems & Data — PASS.
12. Domain 11 complete — PASS.
13. Domain 12 Accounting Operations — PASS.

## Current source/effective-date findings
- IFRS 18 replaces IAS 1 and is mandatory for annual periods beginning on or after 1 January 2027, earlier application permitted; transition retrospective.
- AASB 18 timing is entity-type aware: generally 1 January 2027 for relevant for-profit entities and 1 January 2028 for NFP and specified superannuation entities, earlier application permitted.
- FRC February 2026 adapted-format amendments are effective for periods beginning on or after 1 January 2027 for entities choosing those formats; Periodic Review 2024 gating remains relevant from 1 January 2026.
- Domain 09 uses current official PCAOB/SEC jurisdiction anchors; SOX/ICFR is not generalized as an accounting-framework requirement.
- Domain 10 assurance effective dates are context gates rather than accounting-framework requirements.
- TOPIC-13-001–005 preserve transaction/effective-date gates across combinations, divestitures, asset acquisitions and restructuring.
- TOPIC-13-006 preserves current IFRS/AASB financial-liability derecognition/modification mechanics and marks the IASB 2026 amortised-cost modification proposals as PIPELINE, not current GAAP. US debt modification paragraph-level mapping remains PARTIAL where current Codification body is unavailable publicly.
- TOPIC-13-007 preserves IAS 32/AASB 132 compound-instrument and own-equity classification architecture, FRS 102 Section 22 routing, and independent US Codification routing. IFRIC's warrant reclassification agenda decision is treated as current interpretive context; FICE work remains pipeline.
- TOPIC-13-008 uses IAS 24 / ASC 850 / FRS 102 Section 33 / AASB 124 as related-party disclosure anchors while routing recognition and measurement to the transaction-specific literature. UK small-entity and Australian entity/tier overlays are explicit gates.

## Repository hygiene
Duplicate folders exist for some stable topic IDs due build retries/concurrent factory writes; Phase 2C lease folder naming does not map one-to-one to the canonical Phase 2B denominator. Canonical topic universe and this ledger—not raw folder counts—are authoritative until a later normalization batch.

## Current build sequence
Continue Domain 13 with TOPIC-13-009 Common-Control Transaction Accounting / Spin-Off / Demerger Accounting, then carve-outs/reorganization, hyperinflation and special-transaction workplans. Preserve transaction-date/effective-period routing, framework differences and specialist-input integration. Run Regression 014 after another 1–3 canonical Domain 13 topics.
