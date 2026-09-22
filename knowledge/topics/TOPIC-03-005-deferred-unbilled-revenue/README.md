# TOPIC-03-005 — Deferred Revenue and Unbilled Revenue Accounting

Status: REVIEWED / US SOURCE-DEPTH PARTIAL
Capabilities: CAO-03-010, CAO-03-011
Knowledge: PRINCIPLES + STANDARDS + PRACTICE
Source check: 2026-09-22

## Objective
Translate the revenue model into operational accounting for amounts billed/collected before performance and performance completed before unconditional billing rights, without allowing operational labels such as deferred or unbilled revenue to override framework presentation.

## Framework principle
Under IFRS 15/AASB 15, presentation depends on the relationship between performance and payment. An unconditional right is a receivable; a performance-created right still conditional on something other than time is a contract asset; consideration received or due before transfer creates a contract liability. Revised FRS 102 Section 23 adopts the new revenue model for periods principally beginning on/after 1 January 2026 with UK transition requirements. ASC Topic 606 contains corresponding contract-balance architecture; direct current Codification paragraph verification remains a recorded US source-depth limitation.

## CAO workflow — deferred revenue
1. Reconcile billing/cash population to customer contracts and performance obligations.
2. Identify consideration received or due before related performance.
3. Determine contract-liability amount under applicable revenue requirements rather than simply carrying invoice value.
4. Build release schedule from the actual satisfaction pattern of performance obligations.
5. Separate credits/refunds, financing components, taxes collected for third parties and non-revenue liabilities.
6. Reconcile opening + billings/receipts + acquisitions/FX/reclasses - recognized revenue/refunds = closing liability, with framework-appropriate presentation.

## CAO workflow — unbilled revenue
1. Identify performance recognized before invoice/unconditional receivable.
2. Determine whether remaining condition is only passage of time. If yes, route to receivable; if another performance/acceptance/contract condition remains, evaluate contract-asset presentation.
3. Trace amount to transaction-price allocation and recognized progress/delivery.
4. Establish expected billing trigger/date and aging.
5. Test recoverability/credit-loss interaction under applicable financial-instrument guidance.
6. Reconcile conversion from contract asset to receivable when the right becomes unconditional.

## Required inputs
Contract/order; performance-obligation allocation; revenue schedule; invoice schedule; cash receipts; acceptance/milestone data; credit notes; cancellations; modifications; FX; acquisition data; billing-system and GL extracts.

## Journal logic
Pre-performance billing/collection commonly increases cash/receivable and a contract liability. Performance reduces the liability and recognizes revenue. Performance before unconditional billing may increase a contract asset and revenue; when unconditional, reclassify to receivable. Exact entries depend on billing mechanics and framework facts.

## Controls
Billing-to-contract completeness; revenue schedule approval; contract-liability rollforward; unbilled aging and billing-trigger review; contract-asset-to-AR conversion; negative/abnormal balance review; credit-note/refund matching; FX consistency; subledger-to-GL reconciliation; disclosure rollforward tie-out.

## Audit
Evidence should allow reperformance from contract terms through allocation, performance, billing and GL. High-risk populations include old unbilled balances, manual deferred-revenue releases, negative contract liabilities, large post-close invoices, unusual acceptance terms and contract modifications.

## Systems/data
Maintain contract, performance obligation, invoice, revenue event and cash identifiers separately. Avoid a single net deferred-revenue field that destroys lineage. Required dates include performance, invoice, due, cash and unconditional-right dates.

## Scenarios
Annual SaaS invoice paid upfront: contract liability releases with service transfer. Milestone service recognized but billing awaits substantive customer acceptance: evaluate contract asset. Work completed and only invoice processing remains: assess whether right is already unconditional. Old unbilled item with no planned invoice date triggers accounting and collectability challenge rather than automatic rollover.

## TrackedFR fit
Strong when recurring contract/revenue schedules, billing, AR, cash and GL must be reconciled across systems in Excel.

## QA
PASS for production-candidate operational accounting. Cross-reference TOPIC-03-004 for formal contract-balance classification and revenue timing topics for recognition.