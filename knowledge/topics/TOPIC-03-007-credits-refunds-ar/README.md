# TOPIC-03-007 — Credit Notes, Refunds, Rebates & Accounts Receivable Accounting

Status: REVIEWED / US SOURCE-DEPTH PARTIAL
Capabilities: CAO-03-014, CAO-03-015
Knowledge types: PRINCIPLES, STANDARDS, PRACTICE, DIFFERENCES
Source checked: 2026-09-22

## Authoritative source map
- IFRS: IFRS 15 paragraphs 55, 105–108 and B20–B27; IFRS 9 recognition/measurement/derecognition and impairment architecture.
- US GAAP: ASC 606 revenue/refund architecture and financial-receivable guidance; public FASB material verifies architecture but full current Codification paragraph-body verification remains PARTIAL.
- UK GAAP: revised FRS 102 Section 23 for 2026-onward revenue/refunds plus Section 11 basic financial instruments; Periodic Review 2024 generally effective periods beginning on/after 1 Jan 2026.
- AASB: AASB 15 paragraphs 55, 105–108 and B20–B27; AASB 9 financial asset requirements.

## CAO decision logic
1. Establish why the credit/refund/rebate arises: price concession, variable consideration, product return, billing error, service failure, cancellation, dispute, overpayment or post-contract event.
2. Determine whether it changes transaction price/revenue, creates/remeasures a refund liability, corrects an AR/billing error, settles a customer credit balance, or represents another expense/obligation.
3. Determine whether the right to consideration is unconditional. If only passage of time remains before payment, route to receivable; otherwise evaluate contract-asset treatment under the revenue framework.
4. For rights of return, estimate consideration expected to be retained, recognize/update refund obligation and separately evaluate recovery asset/inventory consequences.
5. Once a receivable exists, apply the applicable financial-instrument framework for measurement, impairment and derecognition. ECL/doubtful-debt methodology is owned by TOPIC-03-008.
6. Link issued credit notes to original invoice/contract/performance obligation and prevent duplicate revenue reduction or cash refund.

## Framework consequences
IFRS/AASB revenue architecture is closely aligned: refund liabilities are updated for changed expectations; unconditional customer rights are presented as receivables and then accounted for under IFRS 9/AASB 9. UK GAAP 2026+ uses revised Section 23 and Section 11 and requires effective-period routing. US GAAP uses Topic 606 plus applicable receivable/credit-loss guidance; do not claim paragraph-level APPROVED status until current Codification is directly verified.

## Journal patterns
Illustrative only:
- Expected refund/price concession: Dr revenue (or adjust transaction price) / Cr refund liability.
- Credit correcting an overstated receivable and revenue: Dr revenue / Cr AR, subject to facts and period/error analysis.
- Cash refund settlement: Dr refund/customer-credit liability / Cr cash.
- AR impairment is separate from commercial credit/refund accounting and routes to TOPIC-03-008.

## Controls
Credit-note approval and reason codes; original-invoice linkage; refund authorization; duplicate refund/credit prevention; contract/price approval; returns completeness; AR subledger-to-GL; customer-credit aging; period cut-off; revenue-impact review; post-close credit analytics.

## Audit evidence
Contract/order; invoice; credit note/refund request; approval; return evidence; pricing/rebate terms; transaction-price estimate; customer correspondence; cash settlement; AR ledger; GL linkage; subsequent settlement; ECL linkage.

## Systems/data
Preserve contract/order/invoice/credit/refund IDs, reason code, original transaction, entity, customer, dates, tax treatment interface, revenue account, AR balance, cash settlement and approval trail. Do not net unrelated customer balances without policy/legal basis.

## Artifacts
Credit/refund accounting memo for unusual items; refund-liability rollforward; AR accounting policy; customer-credit aging; credit-note analytics; revenue-to-AR bridge.

## Scenario tests
1. Retail return right: refund liability + recovery-asset route; PASS.
2. SaaS service credit under SLA: determine transaction-price/revenue effect before treating as bad debt; PASS.
3. Duplicate invoice reversed by credit note: correct AR/revenue and preserve invoice linkage; PASS.
4. Customer cannot pay: route impairment/ECL, not commercial refund; PASS.
5. Unconditional billed receivable subject to possible future refund: receivable and refund obligation can coexist; PASS.
6. UK 2025 period: do not automatically apply revised 2026 Section 23; PASS.
7. Customer overpayment: liability/customer credit, not negative AR revenue by default; PASS.
8. Material credit issued after reporting date: route subsequent-event/error/cut-off analysis as applicable; PASS.

## QA
PASS for production-candidate architecture. US paragraph depth remains PARTIAL pending direct current Codification verification. No restricted standards text is reproduced.