# TOPIC-03-012 — Revenue Disclosure Support & Revenue Process/Control Design

Status: REVIEWED
Capabilities: CAO-03-024, CAO-03-025
Knowledge: STANDARDS + PRACTICE
Framework sensitivity: HIGH
Source check: 2026-09-23

## Objective
Produce complete, traceable revenue disclosures and a control environment that supports the full contract-to-revenue lifecycle rather than only validating the final journal.

## Source map
IFRS 15 contains a disclosure objective and requirements covering revenue disaggregation, contract balances, performance obligations, significant judgments and assets from contract costs. IFRS Foundation's official page and implementation-support materials are the primary source family.

ASC Topic 606 contains the US revenue disclosure model; FASB's official project and PIR materials confirm enhanced disclosures were a core objective of Topic 606. Current Codification must be used for paragraph-level US conclusions and private-company reliefs.

Revised FRS 102 Section 23 applies for most periods beginning on/after 1 January 2026 and contains proportionate UK disclosure requirements; do not import the full IFRS 15 disclosure checklist.

AASB 15 follows the IFRS 15 architecture but current Australian amendments, entity type and Tier 2/AASB 1060 disclosure regime must be resolved.

## Disclosure workflow
1. Resolve framework, entity type, reporting tier and period.
2. Determine revenue streams in/out of the revenue standard.
3. Reconcile reported revenue to GL and revenue subledger.
4. Build disaggregation dimensions that explain economic factors affecting nature, amount, timing and uncertainty rather than merely mirror internal product labels.
5. Reconcile opening/closing contract assets and liabilities and explain significant changes as required.
6. Compile performance-obligation information, including timing and significant payment terms as applicable.
7. Compile remaining-performance-obligation information/exemptions where applicable.
8. Capture significant judgments and changes in judgments affecting timing/amount.
9. Capture contract-cost asset information where required.
10. Tie every quantitative disclosure to governed source data and qualitative statement to approved accounting conclusions.

## Revenue control architecture
### Contract initiation
Contract population completeness; approved templates; nonstandard-term flag; side-letter capture; customer/master-data governance; accounting review trigger.

### Accounting setup
Performance-obligation approval; transaction-price/SSP review; revenue rule configuration; contract modification workflow; framework/effective-period control.

### Transaction processing
Billing completeness/accuracy; revenue-engine interface; manual override governance; credit/refund/rebate processing; cut-off; contract asset/liability logic.

### Close
Revenue subledger-to-GL reconciliation; contract balance reconciliation; deferred/unbilled rollforward; variable-consideration reassessment; modification queue; exception aging; flux analytics.

### Reporting
Disclosure population completeness; tie-out; significant-judgment refresh; disclosure checklist; reviewer certification; financial-statement consistency.

## Management review controls
A review control is not precise merely because a senior person signs it. Define data population, expectation, investigation threshold, evidence of investigation and resolution. Revenue analytics should isolate price, volume, mix, timing, FX, new/churned contracts and accounting changes where relevant.

## Systems/data
Contract repository/CRM/CPQ → billing/revenue subledger → ERP/GL → warehouse/reporting. Maintain contract ID and performance-obligation lineage across systems. Reconcile record counts and amounts at interfaces; monitor rejected/changed records; govern revenue rule changes and privileged access.

## Audit evidence
Disclosure checklist; GL/subledger ties; contract balance rollforwards; sampled contract assessments; SSP/variable consideration support; modification log; system-rule evidence; interface reconciliation; manual journal/override population; control review evidence; final disclosure tie-out.

## Artifacts
Revenue disclosure checklist; disclosure data pack; revenue process narrative; RCM; system/data-lineage map; revenue close checklist; exception dashboard; audit support pack.

## Scenarios
A disclosure agrees to GL but excludes acquired contracts from the subledger population: fail completeness despite arithmetic tie. A reviewer signs a 20% revenue variance without threshold/investigation evidence: control precision is insufficient. A UK 2026 reporter uses an IFRS 15 checklist wholesale: reject and route to revised Section 23. An Australian Tier 2 entity: resolve AASB 1060 interaction before applying full AASB 15 disclosure list.

## TrackedFR fit
High when disclosure/revenue close requires recurring reconciliation of contract, billing/subledger, ERP and warehouse data in Excel. This is a canonical cross-system accounting use case.

## QA
PASS at REVIEWED level. Exact disclosure requirements remain framework/version-specific and must be sourced at execution time; this topic provides CAO workflow, control architecture and routing rather than pretending one universal checklist exists.