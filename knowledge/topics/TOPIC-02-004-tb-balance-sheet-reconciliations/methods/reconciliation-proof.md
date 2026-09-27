# Trial balance and balance sheet — reconciliation proof

Extends existing README/factory/knowledge packs; preserve the alternate `trial-balance-reconciliations` folder. Capabilities CAO-02-009–010. PRINCIPLES/PRACTICE; 2026-09-27.

## Two distinct assertions

A TB review tests whether account movements and mapping are plausible and complete relative to independent information; it is not a balance-sheet reconciliation. A balance-sheet reconciliation proves a specific GL balance from underlying source detail or an independent rollforward, with reconciling items quantified, aged, owned and resolved. A TB that balances debits and credits can contain misstated assets, liabilities or omitted transactions. Risk-tier accounts by magnitude, volume, judgment, fraud and change; review evidence depth accordingly.

## Worked reconciliation

Prepaid GL opening debit 100,000 + approved additions 40,000 − consumption 15,000 = expected closing debit 125,000. GL closing is 130,000. The 5,000 difference is not “immaterial timing” by assertion alone: compare source schedule IDs and journals, identify whether a duplicate addition, missing amortization or mapping error caused it, and book a supported correcting entry under journal governance. If the 5,000 is a newly received valid prepayment omitted from the schedule, update the controlled schedule after source verification rather than plug the GL. Reconcile in both directions: schedule items absent from GL and GL items absent from schedule. Preserve absolute amounts so offsetting 5,000 errors do not disappear in a zero net difference.

Reviewer tests population completeness, cutoff, policy basis, calculations, aged items, threshold and prior-period movements. Workpaper includes source extract parameters, as-of timestamp, GL version, account/book/entity/currency, opening and closing balances, transaction detail, differences and actions, preparer/reviewer timestamps. Unreconciled items > risk-based threshold or without evidence cannot receive unqualified certification; escalate before close lock.

**Negative test:** GL and TB match 130,000, but source schedule supports 125,000. Expected FAIL; trace the 5,000 and restrict sign-off. This is an operational proof; recognition of prepayments depends on the relevant framework/transaction. Dependencies: 02-005, 02-007, 09-005, 10-002, 11-003.
