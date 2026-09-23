# Phase 2D — Knowledge Factory Progress

Updated: 2026-09-23
Denominator: 156 post-Leases top-level topics to work through.

## Status
- REVIEWED / worked through this phase: **45**
- BLOCKED: **0**
- Remaining not yet worked through: **111**
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
| TOPIC-06-003 | REVIEWED / production-candidate | FX remeasurement/translation; commit f9bbd226; includes 2025 exchangeability gate, 2027 hyperinflationary-presentation gate and intragroup FX routing |
| TOPIC-06-004 | REVIEWED / production-candidate | FX gain/loss analysis and functional currency; commit 331fcde7; 10 scenarios |
| TOPIC-06-005 | REVIEWED / production-candidate | Debt and issuance costs; commit d2fe0893; 10 scenarios |
| TOPIC-06-006 | REVIEWED / production-candidate | Debt modification/extinguishment and covenants; commit 3b0eb4ca; current-rule guardrails around active IASB/FASB projects; 10 scenarios |
| TOPIC-08-005 | REVIEWED / production-candidate | Going concern/subsequent-events vertical topic already built |

## Blockers
No fully blocked topic. Non-blocking source-depth limitation: public FASB materials do not always expose complete current Codification paragraph bodies. US records affected by this remain PARTIAL at paragraph-level authority rather than receiving unsupported APPROVED status.

## Regression
- Regression 001: early Close & GL factory scaling.
- Regression 002: full Close/GL + Revenue/Receivables cross-topic review. PASS.
- Regression 003: TOPIC-05-001–006 liabilities/compensation review. PASS.
- Regression 004: Domain 05 completion + Domain 06 handoff. PASS.
- Regression 005: TOPIC-06-001–006 FX/debt review. **PASS**. Confirmed transaction-v-remeasurement-v-translation separation, functional-currency dependency, effective-date routing, debt legal-principal-v-carrying-amount separation, modification/EIR controls, covenant separation and future-project `not current GAAP` guardrail. Commit 69968c45.

## Repository hygiene
Duplicate folders exist for some TOPIC-02 IDs due build retries; Phase 2C lease folder naming does not map one-to-one to the canonical Phase 2B denominator. Canonical topic universe and this ledger—not raw folder counts—are authoritative until a later normalization batch. Do not delete potentially useful duplicate material during active factory scaling.

## Current build sequence
Continue TOPIC-06-007–010 financial asset/liability classification, fair value/derivatives, hedge/investment accounting and impairment/disclosures. Standards-heavy topics require current official-source verification and explicit framework differences. Then proceed to Domain 07 Group Accounting & Consolidation.