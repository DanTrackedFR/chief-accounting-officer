# TOPIC-03-001 — Revenue Contract Assessment, Performance Obligations & Transaction Price

Status: REVIEWED
Capabilities: CAO-03-001, CAO-03-002, CAO-03-003
Knowledge: PRINCIPLES + STANDARDS + PRACTICE
Framework sensitivity: HIGH
Source check: 2026-09-22

## Authoritative source families
IFRS 15 Revenue from Contracts with Customers; FASB ASC Topic 606; FRS 102 Section 23 as revised by Periodic Review 2024; AASB 15 Revenue from Contracts with Customers. Repository stores original explanation and authority pointers, not standards text.

## Core principle
Revenue depicts transfer of promised goods/services to a customer in the amount of consideration to which the entity expects entitlement. IFRS 15 and Topic 606 were jointly developed and share the five-step architecture. Revised FRS 102 Section 23 introduces a proportionately aligned five-step model for periods beginning on/after 1 January 2026 (unless early adopted). AASB 15 follows the IFRS 15 core model with Australian applicability overlays.

## CAO workflow — Steps 1–3
1. Resolve framework, reporting period, entity, contract/customer and scope exclusions/interactions.
2. Establish enforceable contract: approval/commitment, identifiable rights/payment terms, commercial substance and collectibility threshold as required by framework.
3. Determine whether contracts must be combined and identify modification history.
4. Inventory all explicit and implied promises, including options, setup/implementation, warranties, licences, support, hosting, shipping and customer incentives where relevant.
5. Test whether promised goods/services are distinct: customer can benefit and promise is separately identifiable in context. Combine inseparable inputs into the appropriate performance obligation/promise.
6. Determine transaction price: fixed consideration plus framework-compliant variable consideration, financing, noncash consideration and consideration payable to customer effects. Do not confuse invoiced amount with transaction price.
7. Route variable consideration to TOPIC-03-002 and timing/modifications to TOPIC-03-003.

## Framework routing
### IFRS
IFRS 15 is effective for annual periods beginning on/after 1 January 2018. Five steps: contract, performance obligations, transaction price, allocation, recognition on/as satisfaction. The IASB's 2024 PIR concluded the standard is working as intended; principal-agent and consideration-payable-to-customer matters remain areas for possible future consideration, not current replacement requirements.

### US GAAP
ASC 606 uses the converged five-step model. Differences from IFRS exist in detailed application, practical expedients, collectibility, shipping/handling, noncash consideration and other areas; CAO must retrieve US-specific records rather than assume identity.

### UK GAAP
For periods beginning on/after 1 January 2026, revised FRS 102 Section 23 applies a single five-step model based on IFRS 15 but proportionately simplified. Earlier periods require version routing to legacy Section 23. FRC explicitly describes the new model as proportionate alignment, not wholesale IFRS 15 adoption.

### AASB
AASB 15 uses the IFRS 15 five-step model. Australian entity type and any sector-specific overlay must still be checked; never infer AASB compliance solely from an IFRS record.

## Required evidence
Executed contract and amendments; order forms/SOWs; price lists; side letters; customer identity; approval evidence; payment terms; termination/refund rights; product/service descriptions; implementation/support terms; historical concessions; collectibility evidence; sales compensation; billing configuration.

## Controls
Contract population completeness; non-standard-term review; legal-to-accounting handoff; promise inventory; approval of accounting assessment; contract-version control; master-data linkage to billing/revenue system; periodic review of side letters and concessions.

## Systems/data
Canonical contract ID, customer, entity, currency, dates, amendments, promise IDs, SSP source, consideration components, billing schedule, revenue rule and accounting conclusion. Preserve source-document lineage.

## Artifacts
Revenue contract assessment; performance-obligation matrix; transaction-price schedule; accounting memo; system requirements; control checklist.

## Scenario tests
- SaaS subscription plus mandatory implementation: assess whether implementation is distinct before treating as separate obligation.
- Master agreement plus same-day order forms negotiated as package: test combination.
- Customer with poor credit: apply framework collectibility requirements; cash receipt alone does not automatically establish ordinary revenue accounting.
- UK period starting Dec-2025 versus Jan-2026: route to correct Section 23 version.

## QA
PASS for topic build. Detailed variable consideration/allocation/timing/principal-agent differences remain in their mapped downstream topics rather than duplicated here.