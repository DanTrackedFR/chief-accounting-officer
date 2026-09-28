# TOPIC-04-008 — Lease Initial / Subsequent Measurement
Capabilities: CAO-04-019, CAO-04-020
Status: REVIEWED / production-candidate

## Canonical scope
Measure lease liabilities/right-of-use assets at commencement and subsequently under the applicable framework. Reuse the Phase 2C lease vertical slice as the shared technical authority.

## Decision path
Resolve framework/period and commencement date; establish in-scope payment population; determine rate using TOPIC-04-009; calculate initial liability and ROU asset; build framework-appropriate subsequent schedule and expense/journal logic; assess impairment interaction; reconcile schedule/system to GL and disclosures.

## Shared factory artifacts
Use `../TOPIC-04-010-leases/methods/calculation-model.md`, `examples/illustrative-calculation.md`, framework records under `standards/`, `differences/framework-differences.md`, and `practice/controls-audit-systems.md`. Do not duplicate the calculation engine or framework source maps here.

## Controls and evidence
Retain executed contract/payment population, commencement evidence, rate support, schedule version, preparer/reviewer, change log, GL reconciliation and disclosure rollforward. Unsupported assumptions are surfaced rather than invented.

## Payment detail and worked case retained from main
Evaluate fixed and in-substance-fixed consideration, index/rate-based amounts at commencement, residual guarantees, purchase options and termination penalties where the framework/option assessment requires them. Assess prepayments, incentives, initial direct costs and restoration obligations in the ROU opening bridge; ordinary usage-based payments follow the framework-specific variable-payment model. IFRS 16 and AASB 16 interest/payment and ROU depreciation/impairment are distinct from ASC 842 operating lease's generally single lease cost; UK revised FRS 102 Section 20 applies from the operative 2026 period, not automatically in 2025. Five end-of-year payments of 100 discounted at 5%, without other adjustments, give PV approximately 432.95; first-year interest 21.65 and liability after 100 payment approximately 354.60. The 04-010 schedule owns precise date/rate convention and control logic. A missing supported rate blocks approval, and a schedule-to-GL difference fails reconciliation. Source edition/US current paragraph limitations remain recorded in 04-010.

## QA
PASS — five-year property routes term/payments/rate before ROU/liability and schedule.
PASS — IFRS-versus-ASC-842 scenario preserves different subsequent expense/ROU mechanics.
PASS — CPI-linked rent applies initial index/rate logic and routes later changes to remeasurement.
PASS — cross-system close requires rollforward and lease-system/GL/AP reconciliation.

Executed evidence: `../TOPIC-04-010-leases/tests/executed-scenarios.md` S2–S4 and S11. REVIEWED retains the shared vertical slice's paragraph-level source-QA limitations and is not final APPROVED.
