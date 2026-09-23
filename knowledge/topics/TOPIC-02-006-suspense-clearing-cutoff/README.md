# TOPIC-02-006 — Suspense, Clearing and Cut-Off

Status: REVIEWED
Built: 2026-09-22
Capabilities: CAO-02-013, CAO-02-014
Knowledge types: PRINCIPLES, STANDARDS, PRACTICE
Framework sensitivity: MEDIUM

## Objective
Resolve temporary transaction-routing differences and recognize transactions in the reporting period required by the applicable accounting model.

## Principles
Suspense and clearing accounts are temporary routing mechanisms. Governance considers gross activity, item age and transaction risk, not closing balance alone. Each item needs source, reason, owner, expected resolution and aging. Unrelated items should not be offset simply to produce a zero balance.

Cut-off follows the recognition event for the underlying accounting topic. Invoice and payment dates are evidence, not universal recognition rules.

## CAO workflow
1. Extract gross suspense/clearing population and opening items.
2. Match to source events and destination accounts.
3. Age unmatched items and distinguish timing, mapping/interface failure and accounting error.
4. Define the period-end recognition event by transaction class.
5. Test transactions around period end using relevant operational evidence.
6. Record accrual, deferral, reclassification or correction where required.
7. Clear items only when destination treatment is supported.
8. Root-cause recurring exceptions and repair upstream processes.

## Framework routing
IFRS basis-of-preparation requirements interact with topic-specific recognition rules. IFRS 18 replaces IAS 1 for periods beginning on or after 1 January 2027 and moves some basis concepts to IAS 8. US GAAP uses applicable Codification recognition guidance; FRS 102 and AASB use their applicable recognition models. Revenue, inventory, leases, payroll, provisions and financial instruments route to their specific topics.

## Controls and artifacts
Clearing aging; interface monitoring; period-end cut-off testing; late-invoice analytics; post-close subsequent-event review; cut-off matrix; exception register; correcting-entry pack; root-cause log.

## Tests
A zero closing clearing balance does not pass if old gross items were offset. A service invoiced after period end may require an accrual when service was received before period end. An invoice dated before period end does not alone establish recognition if the underlying recognition event occurs later.

## Systems
Strong fit for recurring matching of ERP, AP, procurement/receipts, billing and bank datasets where exceptions are worked in Excel.
