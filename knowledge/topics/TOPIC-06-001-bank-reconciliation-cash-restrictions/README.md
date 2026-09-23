# TOPIC-06-001 — Bank Reconciliation / Cash in Transit / Restricted Cash

Status: **REVIEWED / production-candidate**
Primary capabilities: CAO-06-001, CAO-06-002, CAO-06-003
Sensitivity: M
Frameworks: IFRS, US GAAP, UK GAAP, AASB
Source check: 2026-09-23

## Objective
Enable the CAO to prove recorded cash to external evidence, account for timing items, determine whether restrictions change classification/presentation, and produce close/audit evidence.

## Required facts
Entity/framework/period; complete bank-account inventory; bank statements/confirmations; GL cash accounts; bank feeds; payment and receipt files; merchant/processor balances; transfers around period end; legal/contractual restrictions; escrow/trust/collateral terms; overdrafts; cash-equivalent investments; consolidation restrictions; prior reconciliation and outstanding items.

## Core principles
- External bank evidence is reconciled to book cash account-by-account, then to the financial-statement cash population.
- Timing differences are not automatically errors. Outstanding checks/payments, deposits in transit, bank fees, interest, rejected items and book/bank errors require separate treatment and ageing.
- Inter-account transfers require paired testing around period end to detect kiting/double counting.
- Restriction on use does not automatically mean an amount ceases to be cash; assess the instrument's nature, access terms, restriction duration and presentation/disclosure rules under the applicable framework.
- Cash-in-transit classification depends on control, settlement mechanics and underlying receivable/payable facts; do not use a generic suspense balance indefinitely.

## Framework routing
### IFRS
IAS 7 defines cash as cash on hand and demand deposits and cash equivalents as short-term, highly liquid investments readily convertible to known cash amounts with insignificant value-change risk. IAS 7 requires disclosure of cash/cash-equivalent components and reconciliation to statement-of-financial-position amounts. IFRIC's demand-deposit agenda decision confirms that a third-party contractual use restriction does not by itself remove a demand deposit from cash if the restriction does not change the nature of the deposit; significant unavailable balances require disclosure. Current presentation must be routed through IFRS 18/IAS 7 for the applicable effective period. IASB's 2026 cash-equivalent project decisions are pipeline, not current accounting.

### AASB
AASB 107 is IFRS-aligned on cash equivalents: readily convertible to a known amount with insignificant value risk; short maturity is an indicator, commonly around three months from acquisition. Verify Australian version/effective period independently and route Tier/entity-specific presentation where applicable.

### UK GAAP
Use current FRS 102 Section 7 Statement of Cash Flows and applicable presentation requirements. Periodic Review 2024 amendments have principal effective date 1 January 2026; use the current FRC edition and do not assume IFRS paragraph equivalence. FRC Factsheet 3 may support implementation but does not replace the standard.

### US GAAP
Use ASC 230 and current Codification presentation/disclosure guidance. ASU 2016-18 amended Topic 230 so the statement-of-cash-flows reconciliation explains change in the total of cash, cash equivalents and amounts generally described as restricted cash/restricted cash equivalents. Current paragraph-level conclusions require authorised Codification verification where public FASB source body is incomplete.

## CAO bank-reconciliation workflow
1. Obtain bank-account master and prove completeness to treasury/bank portals, GL and prior period.
2. Lock bank and GL extracts for the same cut-off/timezone.
3. Reconcile statement ending balance to adjusted bank balance and GL ending balance.
4. Categorise every difference: outstanding payment, deposit/receipt in transit, bank-only item, book-only item, error, transfer, unidentified.
5. Test subsequent clearing and age outstanding items.
6. For transfers, trace both bank legs and both GL legs across cut-off.
7. Post supported bank-only/book corrections; do not journal legitimate timing differences merely to force agreement.
8. Review negative cash/overdrafts, processor/merchant balances and cash-equivalent investments separately.
9. For restrictions, read the governing contract/law and document access, permitted use, duration and release conditions.
10. Reconcile bank-account totals to financial-statement cash/restricted-cash presentation and disclosure.
11. Reviewer certifies unreconciled exposure and stale items.

## Calculation / reconciliation model
Adjusted bank = statement balance + deposits in transit - outstanding payments +/- verified bank errors. Adjusted book = GL balance + bank-only credits - bank-only debits +/- book corrections. A completed reconciliation has adjusted bank = adjusted book, with each reconciling item supported and aged. This equation is a control method, not a basis to create unsupported balancing entries.

## Controls
Bank-account opening/closing approval; bank master completeness; independent monthly reconciliation; preparer/reviewer segregation; direct bank-feed/interface monitoring; stale-item thresholds/escalation; transfer cut-off testing; bank-detail change controls; restricted-cash legal review; cash-FS tie-out; access review for banking and ERP posting.

## Audit evidence
Bank statements/confirmations; bank-account listing; GL detail; reconciliation; subsequent-clearance evidence; transfer testing; restriction agreements; bank/cash-equivalent terms; JE support; reviewer sign-off; FS tie-out. Expect audit challenge on stale checks, deposits in transit, transfer cut-off, undisclosed accounts, restricted balances and unsupported manual cash entries.

## Systems / automation
Recurring bank-to-ERP matching is a prime exception-driven automation area. TrackedFR is relevant where multiple banks/processors/ERP accounts feed Excel-based reconciliations and recurring matching/manipulation is material; it is not necessary for a simple low-volume native ERP bank reconciliation.

## Scenario tests
1. Old outstanding check clears after year-end: retain timing item with subsequent evidence.
2. Deposit recorded in GL on 31 Dec but bank credits 2 Jan: test control/settlement facts and support transit.
3. Transfer debit posted before year-end and receiving credit after: paired cut-off/kiting test.
4. Demand deposit contractually restricted to a specified purpose but accessible on demand under IFRS: assess nature, presentation and disclosure rather than automatically excluding cash.
5. Cash locked for >12 months: assess current/non-current and restriction presentation under applicable framework.
6. US restricted cash included in cash-flow reconciliation: route ASC 230/current Codification.
7. Money-market investment with variable redemption amount: do not call cash equivalent solely because liquid.
8. Merchant processor balance: determine whether cash, receivable or transit based on settlement/control terms.
9. Unknown bank account found after close: completeness deficiency and reconciliation remediation.
10. 40 bank accounts across ERP and spreadsheets: exception-driven automation/TrackedFR assessment.

Expected routing: **10/10 PASS**.

## Sources / rights posture
Primary pointers: IAS 7 and IFRIC demand-deposit agenda decision; AASB 107; FRC FRS 102 Section 7/current Factsheet 3; FASB ASC 230 and ASU 2016-18. Standards text remains REFERENCE_ONLY; this is independently authored operational/technical guidance.

## Completion assessment
Principles: PASS. Framework routing/differences: PASS subject to US paragraph-depth guardrail. Calculation/reconciliation: PASS. Documentation/controls/audit/systems: PASS. Capability integration: PASS. Scenarios: 10/10 PASS. Overall: **REVIEWED / production-candidate**.