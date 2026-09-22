# TOPIC-03-010 — Unapplied Cash, Customer Credit Balances & Customer Dispute Accounting

Status: REVIEWED / production-candidate
Built: 2026-09-22
Capabilities: CAO-03-020, CAO-03-021
Knowledge: PRINCIPLES + STANDARDS + PRACTICE

## Principle
A credit on a customer account is not automatically negative revenue and an unresolved customer dispute is not automatically bad debt. Classify the underlying economic event before posting: advance/overpayment, unidentified receipt, refund obligation, credit note/price concession, disputed receivable, contractual offset, withholding, processor timing item, or genuine credit loss.

## CAO workflow
1. Obtain AR aging at invoice/customer level plus cash receipts, credits, remittances and dispute log.
2. For every credit/unapplied item determine source transaction, legal/customer entitlement and expected resolution.
3. Separate cash received before performance/billing from overpayments and unidentified receipts; route revenue-related advances to the applicable contract-liability model where appropriate.
4. For disputes, identify cause: performance/acceptance, pricing, quantity, tax, duplicate billing, service credit/SLA, rebate, return/refund, insolvency or administrative issue.
5. Route revenue concessions/refunds to revenue guidance; route collectability deterioration to impairment guidance; route billing errors to correction/credit-note accounting.
6. Assess offset only where applicable presentation/netting requirements are met; customer-level debit and credit balances should not be netted merely for convenience.
7. Age unresolved credits/disputes and define escalation/refund/write-off/escheatment or jurisdictional routing where relevant.

## Framework dependencies
IFRS/AASB: IFRS 15/AASB 15 contract liabilities, consideration payable/refunds/variable consideration as applicable; IFRS 9/AASB 9 for receivable credit impairment. US: Topic 606 plus ASC 326 as applicable; exact Codification paragraph depth remains source-gated. UK: revised FRS 102 Section 23 for revenue for periods beginning on/after 1 January 2026 and Section 11 for basic financial instruments; earlier periods require the applicable prior edition. Jurisdiction-specific unclaimed-property rules are a separate legal/regulatory overlay.

## Accounting consequences
- Advance for future goods/services: generally revenue-contract analysis, not AR offset.
- Customer overpayment/refundable credit: liability/credit balance until applied/refunded/otherwise legally resolved.
- Valid credit note for price/service adjustment: adjust revenue/receivable under underlying revenue model.
- Disputed invoice with unchanged enforceable consideration but elevated default risk: impairment assessment rather than automatic revenue reversal.
- Billing error: correct receivable/revenue as required by underlying facts; do not bury in bad debt.

## Controls
Daily/periodic unapplied-cash queue; remittance chase; customer-credit aging; refund authorization; dispute reason taxonomy; credit-note approval linked to original invoice/contract; revenue-versus-credit-loss review; debit/credit balance presentation review; stale-credit escalation; subledger/GL reconciliation.

## Systems/data
Customer/invoice/contract IDs; receipt/credit-note IDs; amount/currency; source/reason; dispute owner/status; expected resolution; revenue/ECL routing; refund right; aging; match confidence; approvals; legal/jurisdiction flag.

## Artifacts
Unapplied-cash aging; customer-credit rollforward; dispute register; accounting-routing memo for material disputes; stale-credit action log; reconciliation.

## Scenarios
1. Customer pays twice: record refundable/customer credit; do not reduce revenue — PASS.
2. Customer refuses invoice due to service failure and entity agrees 10% concession: route concession through revenue accounting, not ECL — PASS.
3. Customer simply lacks liquidity: retain revenue conclusion unless facts change; route credit risk to impairment — PASS.
4. Unknown bank receipt: controlled unapplied cash, not arbitrary AR match — PASS.
5. Old customer credit potentially subject to unclaimed-property law: flag jurisdiction/legal overlay; CAO does not invent legal extinguishment — PASS.

## QA
PASS. Topic distinguishes revenue adjustment, liability, AR settlement and impairment; jurisdictional legal disposition is explicitly outside accounting knowledge until applicable rules are resolved.