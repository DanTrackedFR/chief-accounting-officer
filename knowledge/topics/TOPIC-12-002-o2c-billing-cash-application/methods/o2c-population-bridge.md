# O2C billing-to-GL and cash application — population bridge

Extends substantive README. Capabilities CAO-12-004–006. PRINCIPLES/PRACTICE; 2026-09-27.

Trace signed contract/performance events → approved price/customer master → invoice/credit → AR subledger → accounting rule and GL → bank receipt → application, unapplied cash, disputes and reconciliation. Billing is not synonymous with revenue; cash is not synonymous with billing or recognition. Retain contract, invoice, performance and receipt IDs and effective rule versions. Credits/refunds require original transaction link and authorization. Source-to-GL controls test complete and accurate population by legal entity, currency, period and status; AR aging and unapplied cash are separately reconciled.

Illustration: billing source 1,000 invoices/500,000; interface accepts 995/496,000 and rejects 5/4,000. GL receives 496,000 batch. Two customer payments of 2,000 each are unapplied; total cash 4,000 does **not** prove rejected invoices were recognized. Reconcile rejected invoice IDs and payments separately; assess revenue/contract balance with Domain 03, not by netting cash into revenue. If a credit reverses an invoice, preserve both IDs and period treatment.

**Negative test:** analyst books 4,000 revenue simply to match billed total while five rejected items lack performance evidence. Expected FAIL. Controls: price/contract master change, invoice sequencing, interface reject/retry idempotency, manual journal approval, cash-to-bank and AR-to-GL. Evidence: contract/performance, extract/filter, accepted/rejected ledger, journal, bank/remittance, aging and reviewer. Dependencies Domains 03, 09 and 11. Result PASS for operating route; technical revenue conclusion remains external to this process topic.
