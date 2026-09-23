# TOPIC-03-001 — Revenue Contract Assessment, Performance Obligations & Transaction Price

Status: REVIEWED
Capabilities: CAO-03-001, CAO-03-002, CAO-03-003
Knowledge types: PRINCIPLES + STANDARDS + PRACTICE + DIFFERENCES
Framework sensitivity: HIGH
Source check: 2026-09-23

## Objective
Determine whether an arrangement is in the revenue model, identify the accounting contract and promised goods/services, determine which promises are separate units of account, and establish the transaction-price population before allocation and recognition.

## Authoritative source map
IFRS: IFRS 15 Revenue from Contracts with Customers; official IFRS Foundation standard page and implementation-support/TRG materials. IFRS Foundation states IFRS 15 is effective from 1 January 2018 and applies a five-step model.
US GAAP: ASC Topic 606; official FASB Revenue Recognition project and 2024 PIR materials. FASB confirms the same core five-step model and that Topic 606 applies to contracts with customers unless another Topic scopes the contract out.
UK GAAP: FRS 102 Section 23 Revenue from Contracts with Customers, Periodic Review 2024. Most Periodic Review amendments are effective for periods beginning on/after 1 January 2026; reporting-period routing is mandatory. Revised Section 23 is aligned to the IFRS 15 principles with simplifications.
AASB: AASB 15. Core model aligns with IFRS 15, but the applicable compilation/amendments and Australian entity context must be resolved. The AASB portal shows an uncompiled amendment operative from 1 July 2026, so a 2026 case must be version-routed rather than blindly using the December 2022 compilation.

## Core five-step architecture
1. Identify contract(s) with a customer.
2. Identify performance obligations/promises.
3. Determine transaction price.
4. Allocate transaction price.
5. Recognize revenue when/as the promise is satisfied.

This topic owns steps 1–3 at the top level. Variable consideration and allocation deepen in TOPIC-03-002; timing/modifications in TOPIC-03-003.

## Contract assessment
CAO establishes: counterparty is a customer for the scoped activity; approval/commitment; enforceable rights; identifiable payment terms; commercial substance; collection threshold under the applicable framework; combination criteria; contract duration/termination rights; scope exclusions such as leases, insurance or financial instruments.

A signed document is evidence, not the accounting conclusion. Oral/customary arrangements can matter where enforceable. Conversely, a signed master agreement may not create an accounting contract if parties can terminate without substantive rights/obligations.

## Promises / performance obligations
Build a promise inventory from contract, order forms, SOWs, side letters, sales materials and customary business practices. Test whether promised goods/services are distinct under the framework: benefit on own/together with readily available resources, and separately identifiable in the contract context. Evaluate integration, significant modification/customization and interdependence. Identify series treatment where applicable.

Do not let billing line items define performance obligations automatically.

## Transaction price
Inventory fixed consideration; variable consideration; consideration payable to customer; significant financing effects where applicable; noncash consideration; taxes/amounts collected for third parties; price concessions; rebates/refunds/credits; penalties/bonuses; contractually linked arrangements. Establish which elements require deeper routing.

## CAO workflow
1. Resolve entity/framework/period/industry and contract population.
2. Obtain executed agreements, amendments, order forms, SOWs, side letters and relevant sales practice.
3. Confirm customer and scope.
4. Test contract criteria and combination.
5. Build promise inventory and map dependencies.
6. Determine performance obligations / separate promises under applicable framework.
7. Build transaction-price bridge from contractual billing to accounting consideration.
8. Route variable consideration to TOPIC-03-002 and financing/noncash/customer-payments as needed.
9. Record judgments and evidence.
10. Feed outputs to allocation and timing topics.

## Key differences / convergence
IFRS 15 and ASC 606 were jointly developed and share the core model, but they are not identical in every application detail. Do not infer US GAAP solely from IFRS or vice versa. Differences can arise in collectibility thresholds/wording, practical expedients, impairment interactions, shipping/handling policy choices, noncash consideration amendments, licensing and other implementation areas.

Revised FRS 102 Section 23 is based on IFRS 15 principles but intentionally simplified for UK GAAP entities. It must not be represented as verbatim IFRS 15.

AASB 15 largely carries the IFRS 15 model but requires Australian version/entity routing; public-sector/NFP amendments can affect applicability.

## Required evidence
Executed contract set; amendments; customer identity; rights/payment terms; credit/collectibility support; product/service catalogue; SOW/deliverables; standalone-sales information; side letters; customary promises; pricing approvals; rebates/credits; sales compensation terms where relevant; billing schedule; legal/enforceability input when contract rights are genuinely uncertain.

## Controls
Contract population completeness; nonstandard-term review; side-letter capture; approved revenue accounting matrix; new-product review; performance-obligation approval for material/nonstandard contracts; transaction-price bridge; contract master-data governance; framework/version control; periodic back-testing of assumptions.

## Systems/data
Contract ID, customer, entity, framework, start/end, enforceability/termination, promised item, performance-obligation ID, SSP reference, fixed/variable consideration, billing terms, currency, modification chain, accounting conclusion, evidence link and review status should be structured data rather than memo-only fields.

## Artifacts
Contract accounting assessment; promise/performance-obligation matrix; transaction-price bridge; judgment memo; accounting requirements for revenue subledger; control checklist; open-items register.

## World-class practice
Create reusable accounting patterns by contract archetype while preserving exception routing. Connect CRM/CPQ, contract repository, billing and ERP data so nonstandard terms are surfaced before close. Treat revenue accounting as contract data plus governed judgment, not spreadsheet archaeology at month end.

## TrackedFR fit
Relevant when recurring revenue accounting requires cross-system extraction/reconciliation across CRM/contract data, billing/subledger, ERP and warehouse/Excel. Not recommended merely because a revenue memo or calculation uses Excel.