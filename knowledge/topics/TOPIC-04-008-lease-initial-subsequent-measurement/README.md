# TOPIC-04-008 — Lease Initial Measurement / Lease Subsequent Measurement

Capabilities: CAO-04-019, CAO-04-020
Status: REVIEWED

## Workflow
Confirm commencement, term, payment population and supported discount rate. Measure the liability from qualifying unpaid lease payments discounted at the applicable rate. Build the ROU asset from the initial liability adjusted for applicable prepayments, incentives, initial direct costs and restoration obligations. Tie inputs to executed contracts and payment data; lock the commencement schedule.

Payment population evaluates fixed/in-substance-fixed amounts, index/rate-based payments at commencement, residual guarantees, purchase options and termination penalties as applicable. Ordinary usage/performance variable payments are excluded when the framework requires expense as incurred.

## Frameworks
IFRS 16.22–46: initial ROU/liability recognition, subsequent interest/payment mechanics and specified remeasurement; ROU asset generally follows depreciation/impairment. ASC 842: finance leases generally show interest plus ROU amortization; operating leases use ROU mechanics designed for generally straight-line single lease cost. Revised FRS 102 Section 20 (2026+) uses its revised liability/ROU model and must not be applied automatically to pre-2026 periods. AASB 16 for-profit core generally follows IFRS 16 subject to Australian overlays.

## Worked example
Five annual fixed payments of 100 in arrears at a supported 5% annual rate, with no other adjustments: commencement PV ≈432.95. Year-one interest ≈21.65; after a 100 payment, closing liability ≈354.60. Production schedules require exact dates, frequency, rate convention and framework-specific inputs.

## Controls / evidence
Contract-to-schedule input reconciliation; rate support; payment completeness; commencement approval; versioned schedule; JE support; monthly rollforward; ROU/liability GL reconciliation; modification log; disclosure population; independent recalculation samples.

## Scenario QA
Missing rate → stop and route to rate methodology PASS. CPI-linked rent → commencement index/rate plus later remeasurement route PASS. ASC 842 operating lease → do not apply IFRS P&L pattern PASS. Worked PV/rollforward recalculation PASS. Lease-system/GL difference → block sign-off until reconciled PASS.

## Provenance
Derived from reviewed TOPIC-04-010 lease source pack checked 2026-09-22. IFRS references are references, not reproduced text. Public FASB paragraph-level access remains PARTIAL.
