# Phase 2D — Knowledge Factory Progress

Updated: 2026-09-24
Denominator: 156 post-Leases top-level topics to work through.

## Status
- REVIEWED / worked through this phase: **104**
- BLOCKED: **0**
- Remaining not yet worked through: **52**
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
| TOPIC-13-001 | REVIEWED / production-candidate | Business combinations / PPA coordination; current IFRS, FASB, FRC and AASB routing checked 2026-09-24 |
| TOPIC-13-002 | REVIEWED / production-candidate | Acquisition-date accounting / contingent consideration; 10 scenario checks PASS; IFRS/AASB measurement-period and contingent-consideration routing, US measurement-period architecture and UK divergence preserved |

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
- TOPIC-13-001: IASB business-combination disclosure/goodwill proposals remain under redeliberation in 2026 and are not current IFRS requirements; FASB ASU 2025-03 creates an effective-date gate for accounting-acquirer analysis in qualifying VIE equity-exchange combinations; FRS 102 Section 19 remains materially different from current IFRS 3; AASB periods beginning on/after 1 July 2026 require subsequent/uncompiled-amendment routing rather than sole reliance on the December 2022 compilation.
- TOPIC-13-002: IFRS 3/AASB 3 distinguish acquisition-date facts from post-acquisition events and cap the measurement period at one year. Contingent-consideration subsequent accounting depends on classification. US measurement-period presentation must reflect current ASC 805/ASU 2015-16 architecture. FRC confirms FRS 102 Section 19 remains based on IFRS 3 (2004), so modern IFRS contingent-consideration mechanics cannot be imported by analogy.

## Repository hygiene
Duplicate folders exist for some stable topic IDs due build retries/concurrent factory writes; Phase 2C lease folder naming does not map one-to-one to the canonical Phase 2B denominator. Canonical topic universe and this ledger—not raw folder counts—are authoritative until a later normalization batch.

## Current build sequence
Continue Domain 13 Complex Transactions & Special Situations with TOPIC-13-003 acquisition-related costs / measurement-period adjustments, then TOPIC-13-004 onward. Preserve business-combination versus asset-acquisition boundaries, transaction-date/effective-period routing, framework differences and specialist-input integration. Run regression after 5–10 canonical Domain 13 topics.
