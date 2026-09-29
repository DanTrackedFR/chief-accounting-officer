# Automated/recurring journals — posting contract

Extends existing factory and knowledge packs; preserve `TOPIC-02-003-recurring-journals-gl-integrity` as a useful duplicate/retry source. Capabilities CAO-02-007–008. PRINCIPLES/PRACTICE; 2026-09-27.

## Eligibility and configuration

Automate only stable, policy-approved logic with defined source fields, grain, entity/book/account mapping, period, currency, rounding, rule effective dates and exception disposition. Distinguish (a) deterministic periodic reversal/amortization, (b) data-driven entry from a controlled subledger, and (c) judgmental estimate. Category (c) may be system-assisted but requires explicit qualified approval of assumptions. Configuration is versioned and tested with positive, zero, duplicate, missing-data and prior-period cases. Separate config editor, executor and approver privileges.

## Reconciliation and worked run

Example monthly feed source has 1,000 transactions: 996 valid amounting to 99,600 and four rejects amounting to 400. Accepted-to-journal total must be 99,600 (subject to any documented accounting transformation); 400 stays in an owned exception queue, not silently in a 100,000 journal. Run ID `DEC-A`, source transaction keys and posted batch IDs establish exact-once processing. A timeout followed by retry `DEC-B` must first query destination IDs for `DEC-A`; it must not duplicate 99,600. After controlled resolution of four rejects, any additional posting has distinct IDs and a 400 support bridge. The final source-to-GL 100,000 claim is conditional on the accounting policy and the four dispositions.

Check counts **and** signed/absolute amounts by entity, currency and account; offsets can mask omissions. Review suspense, manual top-side overrides, dormant accounts, unexpected debit/credit signs and period locks in the GL integrity review. Preserve source snapshot/query, mapping hash/version, run logs, rejects, approver, posting and reversal IDs. Investigate unauthorized rule changes before accepting a matching total.

**Failure injection:** an operator reruns `DEC-A` after a timeout and destination contains 996 source keys already. Expected outcome is no second posting and documented idempotent skip. A second 99,600 batch is a control failure requiring reversal, completeness reassessment and access/change investigation. Result PASS for prescribed fail-stop logic; no production system was executed. Accounting treatment remains in the applicable underlying topic. Dependencies: 02-002, 09-003, 11-003/010, 12-008.
