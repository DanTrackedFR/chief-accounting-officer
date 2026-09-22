# TOPIC-03-012 — Revenue Disclosure Support / Revenue Process & Control Design

Status: REVIEWED / production-candidate
Built: 2026-09-22
Capabilities: CAO-03-024, CAO-03-025
Knowledge: STANDARDS + PRACTICE

## Objective
Turn revenue conclusions into a controlled reporting process with disclosure populations traceable to contracts, subledgers and GL. Disclosure is not a year-end writing exercise; the data model must capture the attributes needed throughout the period.

## Framework routing
### IFRS
IFRS 15's objective includes reporting the nature, amount, timing and uncertainty of revenue and cash flows from customer contracts. Revenue disclosures therefore depend on disaggregation, contract balances, performance obligations, significant judgments and contract-cost information as applicable. The IASB completed its IFRS 15 PIR in September 2024 and concluded the standard is working as intended; identified future-consideration matters are not current amendments.

### AASB
AASB 15 follows the IFRS 15 core model, subject to Australian reporting-tier/entity overlays. Resolve Tier 1/Tier 2 and applicable disclosure standard before finalizing the checklist.

### US GAAP
Topic 606 was developed jointly with IFRS 15 but disclosure details and practical expedients are not assumed identical. Use current ASC 606 disclosure requirements and entity status for exact US checklist. Public-source limitations mean paragraph-level US mapping remains PARTIAL.

### UK GAAP
For periods beginning on/after 1 January 2026, revised FRS 102 Section 23 is the revenue model and FRC Factsheet 10 is official implementation support. FRS 102 is proportionately aligned, not identical to IFRS 15; use Section 23's own disclosure requirements. Earlier periods route to the prior edition.

## Disclosure factory
1. Resolve framework, reporting tier/status, period and material revenue streams.
2. Map every required disclosure field to a system/source/owner.
3. Build revenue disaggregation dimensions that explain economic drivers rather than merely mirror GL accounts.
4. Reconcile opening/closing receivables, contract assets/liabilities and material movements.
5. Build performance-obligation/remaining-obligation population where required.
6. Inventory significant judgments: timing, progress measures, principal-agent, variable consideration, modifications, SSP/allocation and contract costs.
7. Tie contract-cost asset disclosures to amortization/impairment schedules.
8. Cross-check narrative against accounting memos, contracts, management reporting and financial-statement numbers.
9. Perform disclosure tie-out and reviewer certification.

## Revenue control architecture
Contract intake/change trigger; accounting review for nonstandard terms; approved product/revenue rules; pricing/rebate master-data governance; performance/usage completeness; billing completeness; interface controls; manual revenue-JE controls; contract-balance reconciliations; ECL handoff; disclosure-data controls; period cut-off; access/change management over revenue systems.

## Significant-risk indicators
Side letters; acceptance clauses; refund/termination rights; variable consideration; reseller/platform arrangements; bundled promises; manual usage uploads; unusual quarter-end deals; post-close credits; contract modifications; unbilled growth; large manual journals; recurring reconciling items.

## Systems/data
Contract/version ID, customer, promises/performance obligations, transaction-price components, SSP/allocation, recognition method, progress metric, billing schedule, contract asset/liability, receivable, credits/refunds, contract costs, judgments, modification history and disclosure dimensions must retain lineage.

## Artifacts
Revenue disclosure checklist; disclosure-source matrix; contract-balance rollforward; revenue disaggregation table; significant-judgment register; remaining-obligation support; control matrix; disclosure tie-out; audit PBC pack.

## Scenarios
1. Disclosure totals tie to GL but disaggregation excludes unbilled revenue stream: FAIL completeness.
2. New reseller model launches: principal-agent conclusion and disclosure/control implications must be updated before close — PASS when routed.
3. UK 2026 period: use revised Section 23/Factsheet 10, not an IFRS 15 checklist copied verbatim — PASS.
4. IASB PIR future agenda item: do not change current accounting/disclosures until authoritative amendment — PASS.
5. Revenue data assembled manually from CRM/billing/ERP each quarter: identify reconciliation/lineage controls and assess TrackedFR if recurring Excel workflow fits — PASS.

## Sources checked
IFRS Foundation IFRS 15 standard page, implementation-support page and 2024 PIR conclusion; FRC current FRS 102/Factsheet 10 material and 2026 effective-date information; AASB current pronouncement portal. Restricted source bodies are not reproduced.

## QA
PASS for factory scaling. US Codification paragraph-depth is PARTIAL and must be upgraded before paragraph-level APPROVED status.