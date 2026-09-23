# Phase 2D — Knowledge Factory Progress

Updated: 2026-09-23
Denominator: 156 post-Leases top-level topics to work through.

## Status
- REVIEWED / worked through this phase: **48**
- BLOCKED: **0**
- Remaining not yet worked through: **108**
- Regression reviews: **5**

## Worked-through topics
| Topic range | Status | Notes |
|---|---|---|
| TOPIC-02-001–010 | REVIEWED | Close & GL factory built; duplicate retry folders noted below |
| TOPIC-03-001–012 | REVIEWED / production-candidate | Revenue & receivables family built |
| TOPIC-04-001–006 | REVIEWED / production-candidate | PPE through impairment/goodwill family built |
| TOPIC-05-001–010 | REVIEWED / production-candidate | AP, cut-off/accruals, provisions, onerous contracts, payroll/benefits, bonuses/commissions, SBC, termination/leave and compensation reconciliation. Domain 05 complete. |
| TOPIC-06-001 | REVIEWED / production-candidate | Bank reconciliation, cash in transit and restricted cash |
| TOPIC-06-002 | REVIEWED / production-candidate | Cash classification/presentation and foreign-currency transaction accounting; current IAS 7/IAS 21, AASB 107/121, FRS 102 Sections 7/30 and ASC 230/830 routing |
| TOPIC-06-003 | REVIEWED / production-candidate | FX remeasurement/translation; includes exchangeability, hyperinflationary-presentation and intragroup FX routing |
| TOPIC-06-004 | REVIEWED / production-candidate | FX gain/loss analysis and functional currency; 10 scenarios |
| TOPIC-06-005 | REVIEWED / production-candidate | Debt and issuance costs; 10 scenarios |
| TOPIC-06-006 | REVIEWED / production-candidate | Debt modification/extinguishment and covenants; current-rule guardrails around active IASB/FASB projects; 10 scenarios |
| TOPIC-06-007 | REVIEWED / production-candidate | Financial asset/liability classification; IFRS/AASB business-model+SPPI, US instrument-specific ASC routing, FRS 102 Sections 11/12 and policy-election logic; 2026 effective-date gate; 10 scenarios |
| TOPIC-06-008 | REVIEWED / production-candidate | Fair value measurement and derivative accounting; IFRS 13/AASB 13, ASC 820/815 and FRS 102 Section 2A/11/12 routing; ASU 2025-07 adoption gate and 2026 FASB proposal separated from current GAAP; 10 scenarios |
| TOPIC-06-009 | REVIEWED / production-candidate | Hedge accounting and investment accounting; commit cbc2c986; IFRS 9/IFRIC 16, ASC 815/320/321, FRS 102 11/12 and AASB 9 routing; 2026 IFRS classification amendments and 2025 US derivative-scope adoption gates; 10 scenarios |
| TOPIC-08-005 | REVIEWED / production-candidate | Going concern/subsequent-events vertical topic already built |

## Blockers
No fully blocked topic. Non-blocking source-depth limitation: public FASB materials do not always expose complete current Codification paragraph bodies. US records affected by this remain PARTIAL at paragraph-level authority rather than receiving unsupported APPROVED status.

## Regression
- Regression 001: early Close & GL factory scaling.
- Regression 002: full Close/GL + Revenue/Receivables cross-topic review. PASS.
- Regression 003: TOPIC-05-001–006 liabilities/compensation review. PASS.
- Regression 004: Domain 05 completion + Domain 06 handoff. PASS.
- Regression 005: TOPIC-06-001–006 FX/debt review. PASS. Confirmed transaction-v-remeasurement-v-translation separation, functional-currency dependency, effective-date routing, debt legal-principal-v-carrying-amount separation, modification/EIR controls, covenant separation and future-project `not current GAAP` guardrail.

## Repository hygiene
Duplicate folders exist for some stable topic IDs due build retries; Phase 2C lease folder naming does not map one-to-one to the canonical Phase 2B denominator. Canonical topic universe and this ledger—not raw folder counts—are authoritative until a later normalization batch. Do not delete potentially useful duplicate material during active factory scaling.

## Current build sequence
Complete TOPIC-06-010 financial-instrument impairment/disclosures, then run Regression 006 and proceed to Domain 07 Group Accounting & Consolidation. Standards-heavy topics require current official-source verification and explicit framework differences.