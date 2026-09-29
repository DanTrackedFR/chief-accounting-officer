# AR/revenue reconciliation — two-sided proof

Capabilities CAO-03-022/023. This is a practice record. The accounting treatment of an exception belongs to the linked technical topic. Do not manufacture framework standards for matching mechanics.

## AR movement and independent population test

Opening AR 500; approved new invoices 900; applied receipts 600; credit notes 50; write-offs 20; FX remeasurement increases AR 10. Expected closing control balance = 500+900−600−50−20+10 = 740. AR subledger shows 740 and GL shows 740. Nevertheless the independent delivery log contains one billable 40 event missing from both, while a duplicate 40 invoice appears in both following a retry. Equality of balances does not prove completeness or accuracy. Inspect delivery and billing linkage; reverse the duplicate and assess the missing item against contract terms and revenue timing, rather than posting an unreviewed net-zero pair.

**Executed:** movement bridge 740, subledger-to-GL difference zero, source population exceptions two transactions of 40 with opposite signs. PASS exception detection; final accounting unresolved until performance and billing facts verified.

## Revenue bridge

Revenue engine records 1,000 for the period; authorized manual acquisition true-up is +25; GL revenue is 1,030. An unexplained +5 remains. Tie true-up to memo/journal approval and trace 5 by journal ID. Do not classify it as a timing difference without an expected clearing event. **Executed:** 1,030−1,000−25=5. FAIL reconciliation until cleared and accounting impact assessed.

## Control execution

Freeze source queries at a documented UTC timestamp, save filters/entity/currency/period and counts; reconcile opening balances and each movement by stable transaction ID. Sample interface rejection and retry logs, zero-value/credit transactions, late-posted adjustments and manually created entries. Reperform mapping of entity, revenue stream and account; maintain an aged exception ledger with owner, root cause, evidence, proposed posting and reviewer approval. For revenue/contract assets and liabilities, reconcile performance events to accounting schedules separately from invoice events. Reviewer signs a challenge log, not merely a total.

Source interface: contract-balance and receivable classification is governed by [IFRS 15](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-15-revenue-from-contracts-with-customers/), FASB ASC 606, FRS 102 Section 23 or AASB 15 as applicable; the mechanics above are framework-neutral. Cross-topic TOPIC-03-005/007/008/009/010/012 and TOPIC-06-003 (FX). Proposed REVIEWED candidate for operational method after independent QA of example; technical accounting conclusions stay with owning topics.
