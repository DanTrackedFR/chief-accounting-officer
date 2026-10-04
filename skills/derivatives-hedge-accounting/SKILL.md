---
name: derivatives-hedge-accounting
skill_id: SKILL-HEDGE-001
version: 0.1.0
status: review
roadmap: 29
---

# Derivatives & Hedge Accounting

Own derivative scope, whole-instrument recognition and settlement, basic fair-value,
cash-flow and net-investment hedge accounting. Produce journals, reserve movements,
basis-adjustment receipts and disclosure support from actual independently reviewed
sources. Do not value instruments, select a strategy or execute/post trades.

Invoke through `production.assess_case` using `package: derivatives-hedge-accounting`.
Current supported period is 2026 and approved supplemental knowledge is mandatory.
Read methods.md. Current framework/policy applicability and reviewer certification
must pass the shared production boundary before a result is complete.

## Inputs

Actual contract completeness population; independently frozen contract and valuation
sources; current signed opening/change/settlement/closing values; dated designation;
actual quantities and documented effectiveness; independently measured designated
risk; opening reserves; actual forecast/outcome data; GL/statement reconciliation;
operative framework disclosure review; completed current accounting owner imports.

## Outputs

`calculations.derivatives`, `hedge_reserves`, `effectiveness`, `gl_movements`, and
`basis_adjustments` plus balanced journals. Each basis receipt has unique economic
identity, SKU/acquisition/quantity, date/entity/framework/currency and signed cost
adjustment. A positive effective gain reduces a purchased asset basis. Inventory
consumes the receipt once and performs its own costing.

## Dependencies

Qualified external derivative valuation is supported because current Fair Value
Measurement owner only supports listed equity valuations. No curves are invented.
Reexecute Debt, Foreign Currency and Consolidation owners for facts required by
respective relationships. Financial Instruments retains host classification/ECL.
Reporting owns final statement/disclosure production. No owner postings are copied
into hedge journals; hedge adjustments remain separately identifiable.
