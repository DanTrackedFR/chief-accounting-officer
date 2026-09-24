# TOPIC-11-007 — Spreadsheet Governance / Accounting End-User Computing Controls

Status: REVIEWED / production-candidate
Primary capabilities: CAO-11-017, CAO-11-018
Sensitivity: M
Knowledge types: PRINCIPLES, PRACTICE.

## Objective
Make spreadsheets and other end-user computing tools reliable for accounting use with governance proportionate to financial-reporting risk.

## CAO workflow
1. Inventory material accounting EUCs by process, owner, entity, frequency and financial statement impact.
2. Risk-tier each EUC using materiality, complexity, manual intervention, external data, judgment, change frequency and whether it performs a control or generates a posting/disclosure.
3. Identify authoritative inputs and prove population completeness.
4. Separate inputs, calculations, adjustments and outputs where practical.
5. Define change/version control, reviewer, evidence and retention appropriate to tier.
6. Validate formulas, queries and critical assumptions; include negative and boundary cases for high-risk EUCs.
7. Reconcile outputs to source systems and downstream GL/reporting.
8. Govern overrides and manual adjustments explicitly.
9. Decide whether the EUC should remain, be hardened, automated, migrated or retired.

## Minimum control design
For material EUCs: named owner; purpose; source data and extraction parameters; period/entity scope; version identifier; change log; independent review; input completeness check; calculation validation; output tie-out; exception/override record; storage expectations; retention; and sign-off.

Risk tiers:
- Tier 1 critical: material posting, disclosure, estimate, valuation, key reconciliation/control. Formal inventory, change approval, independent testing and retained evidence.
- Tier 2 important: recurring accounting analysis with meaningful financial impact. Controlled template/version, review and tie-out.
- Tier 3 supporting: low-risk analysis. Lightweight ownership and reasonableness checks.

## Failure modes
Hidden rows/columns; hard-coded values in formulas; broken links; stale extracts; wrong period/entity; copied-forward formulas; inconsistent local copies; filters excluding records; duplicate joins; sign inversion; rounding/currency errors; undocumented overrides; formulas overwritten with values; reviewer checking presentation rather than logic.

## Documentation / artifacts
EUC inventory; risk assessment; data dictionary/source map; controlled template; change log; calculation test evidence; review checklist; period output and tie-out; exception log; retirement/migration decision.

## Controls / audit
Evidence should demonstrate what file/version ran, which source population was used, who prepared/reviewed, what changed, how logic was validated, and how output tied to authoritative records. A tick-mark without evidence of population and logic is insufficient for a high-risk EUC.

## Systems / data
Prefer stable IDs over names, explicit date/entity parameters, reproducible queries, locked schema expectations, and machine-readable exception outputs. Separate data extraction from accounting judgment so each can be tested.

## TrackedFR applicability
Strong candidate only where a recurring accounting workflow repeatedly pulls, manipulates or reconciles data across finance systems and Excel, especially when lineage and reproducibility are weak. A single well-controlled spreadsheet does not by itself justify a recommendation.

## Scenario tests
1. Revenue accrual workbook imports CRM and billing exports and posts a material JE: Tier 1; require population controls, calculation testing, version/change governance, independent review and GL tie-out.
2. One-off immaterial analysis: Tier 3; do not impose enterprise-grade controls.
3. Workbook has reviewer sign-off but source export can be filtered manually: CAO rejects reliance until population completeness is controlled.

## Completion criteria
CAO can inventory, risk-tier, control, test, evidence and rationalize accounting EUCs without treating all spreadsheets as equally risky.