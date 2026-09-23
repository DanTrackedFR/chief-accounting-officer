# TOPIC-03-001 — Revenue Contract Assessment / Performance Obligations / Transaction Price

Status: REVIEWED
Capabilities: CAO-03-001, CAO-03-002, CAO-03-003
Sensitivity: HIGH
Source checked: 2026-09-22

## Authoritative source register
- IFRS: IFRS 15 Revenue from Contracts with Customers, official IFRS Foundation standard page. Effective annual periods beginning on/after 1 Jan 2018. Primary, REFERENCE_ONLY.
- US GAAP: ASC Topic 606, Revenue from Contracts with Customers. FASB's Revenue Recognition project confirms Topic 606 establishes the revenue principles; Codification is authoritative. Primary, REFERENCE_ONLY.
- UK GAAP: FRS 102 Section 23 Revenue from Contracts with Customers, September 2024 edition / Periodic Review 2024. Revised Section 23 is proportionately aligned to IFRS 15 and generally effective periods beginning on/after 1 Jan 2026; early application permitted. Primary, REFERENCE_ONLY.
- AASB: AASB 15 Revenue from Contracts with Customers. For-profit Tier 1 requirements incorporate IFRS 15; Australian-specific NFP guidance and Tier 2 disclosure requirements require separate routing. Primary.

No standards body text is reproduced here; explanations are independently authored with paragraph pointers.

## Core principle
Revenue depicts transfer of promised goods/services to customers in the consideration the entity expects to be entitled to. IFRS 15 and Topic 606 were developed jointly and share the five-step architecture. Revised FRS 102 Section 23 uses a proportionately aligned five-step model for 2026+ periods. AASB 15 closely follows IFRS 15 for for-profit Tier 1 entities but includes Australian overlays.

## Step 0 — Scope
Before applying the revenue model, establish whether the counterparty is a customer and whether the contract is within revenue scope. Lease, insurance, financial-instrument and specified non-monetary exchange arrangements can be outside the model. Mixed contracts require separation/routing to other applicable literature before the revenue portion is assessed.

## Step 1 — Contract existence
IFRS/AASB paragraph family 9–21; ASC 606-10-25 contract-recognition family.

CAO tests: approval/commitment; identifiable rights; identifiable payment terms; commercial substance; collectibility threshold under the applicable framework; combination of contracts; modification interaction. Obtain executed agreement, order forms/SOWs, amendments, side letters, pricing approvals and evidence of customary business practices. Do not infer enforceable rights solely from invoice issuance.

If recognition criteria are not met, do not force the arrangement through the remaining model. Route consideration received under the framework's requirements until a contract exists or other specified conditions are met.

## Step 2 — Promised goods/services and performance obligations
IFRS/AASB 22–30; corresponding ASC 606-10-25 promised-goods/performance-obligation guidance.

Build the complete promise population from explicit terms plus promises created by customary practice/published policy/specific statements where relevant. Then test whether each good/service is distinct: customer can benefit from it on its own or with readily available resources, and the promise is separately identifiable in the contract context. Evaluate integration, significant modification/customization and interdependence rather than relying on contract line items.

Consider series guidance for substantially similar distinct services transferred with the same pattern. Consider options/material rights, warranties, licences, setup/implementation activities and principal-agent questions through their dedicated subtopics where triggered.

## Step 3 — Transaction price
IFRS/AASB 46–72; corresponding ASC 606-10-32 measurement family.

Inventory fixed consideration, variable consideration, significant financing, non-cash consideration and consideration payable to customers. Variable amounts require an estimation method appropriate to the fact pattern plus the applicable constraint before inclusion. Refunds/rebates/credits/service levels/usage/bonuses/penalties/returns are not automatically 'future period' items; determine whether and how they affect transaction price.

Do not confuse invoice amount, contract value, cash collected or ARR with transaction price.

## Framework routing
### IFRS
Use IFRS 15 current requirements and official implementation/PIR material as interpretive support. IASB's 2024 PIR concluded the Standard is working as intended; possible future work on principal-agent/payments-to-customers/interactions does not change current requirements.

### US GAAP
Use current ASC 606 Codification. Shared core model does not justify assuming every IFRS conclusion is identical: route known wording/practical-expedient/application differences through differences records. Check current amendments for the reporting period, including share-based consideration payable to customers where relevant.

### UK GAAP
Mandatory effective-date gate. Periods beginning before 1 Jan 2026 may use the previous Section 23. For 2026+ use revised Section 23. Do not copy IFRS 15 mechanically: the FRC describes the model as proportionate alignment and has UK-specific simplifications/wording.

### AASB
Resolve reporting period, for-profit/NFP status and reporting tier. Current AASB portal shows the Dec-2022 compilation operative for periods beginning on/after 1 Jan 2023 but before 1 Jul 2026, with subsequent amendments applying after that date. For-profit Tier 1 compliance aligns with IFRS 15; NFP Australian implementation guidance and Tier 2 AASB 1060 disclosures require overlay.

## CAO execution workflow
1. Resolve entity/framework/period/tier and revenue stream.
2. Obtain full contract package and commercial context.
3. Determine scope/customer.
4. Test contract criteria and combination.
5. Build promise inventory.
6. Determine distinct goods/services and series/material-right/warranty/licence dependencies.
7. Document performance obligations.
8. Build consideration waterfall: fixed → variable → financing → noncash → payable-to-customer.
9. Identify estimates/constraints and evidence.
10. Hand off to allocation (TOPIC-03-002) and timing/modification (TOPIC-03-003).
11. Determine contract-balance, billing, disclosure, controls and system consequences.
12. Promote durable contract archetype/policy positions to Company Accounting Memory.

## Controls
Contract completeness between CRM/CPQ/legal/billing/ERP; approved contract templates; nonstandard-term flag; side-letter capture; accounting review triggers; promise inventory review; pricing/variable-consideration approval; contract-version control; master-data linkage from contract to performance obligation/billing/revenue schedule; periodic contract-population reconciliation.

## Systems/data model
contract_id, customer_id, legal_entity, framework, effective dates, amendment/version, currency, enforceability status, promise_id, performance_obligation_id, SKU/service, distinct conclusion, series flag, fixed consideration, variable type/estimate/constraint, financing flag, noncash/payable-to-customer, source_document_uri, reviewer, accounting_case_id.

## Artifacts
Revenue contract assessment; performance-obligation matrix; transaction-price calculation; significant-terms abstract; accounting memo for judgmental contracts; contract-to-billing/revenue lineage; controls evidence.

## Scenarios
1. SaaS subscription + implementation: determine whether implementation transfers a distinct service before treating it as separate PO.
2. Product + 'free' future service: free label does not remove promised service; identify and allocate if a performance obligation/material right.
3. Volume rebate: estimate variable consideration and apply constraint; do not wait automatically for credit note.
4. Customer with significant credit concern: test applicable collectibility/contract criteria before revenue model.
5. UK period starting Dec-2025: do not apply revised 2026 Section 23 automatically.
6. Australian NFP licence/service arrangement: retrieve Australian NFP overlay; do not inherit for-profit IFRS answer blindly.

## QA
PASS for factory build: four-framework routing, effective-period gates, principles, CAO workflow, controls, data, artifacts and scenarios established from official sources. Detailed allocation/timing/modification/principal-agent/contract-balance/disclosure mechanics intentionally route to TOPIC-03-002 onward rather than duplicating them here.