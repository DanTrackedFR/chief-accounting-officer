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

## QA
PASS — five-year property routes term/payments/rate before ROU/liability and schedule.
PASS — IFRS-versus-ASC-842 scenario preserves different subsequent expense/ROU mechanics.
PASS — CPI-linked rent applies initial index/rate logic and routes later changes to remeasurement.
PASS — cross-system close requires rollforward and lease-system/GL/AP reconciliation.

Executed evidence: `../TOPIC-04-010-leases/tests/executed-scenarios.md` S2–S4 and S11. REVIEWED retains the shared vertical slice's paragraph-level source-QA limitations and is not final APPROVED.
