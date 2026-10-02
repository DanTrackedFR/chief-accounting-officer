# Balance Sheet Reconciliations — governed method

Balanced TB, complete balance-sheet inventory including active zero accounts, independent source rollforward, bidirectional ID matching, quantified gross timing differences and absolute/relative/age gates; posted supported correcting adjustments and final GL tie-out.

Inventory is the independently approved complete balance-sheet account population; TB also contains non-balance-sheet accounts. Debit-positive signed account balances are used consistently. gl_closing is the frozen pre-adjustment balance and adjustments are confirmed posted subsequent entries.

Opening prepaid 100,000 + additions 40,000 - consumption 15,000 = 125,000. GL 130,000 requires supported -5,000 correction, debit expense / credit prepaid, rather than a plug. Offsetting +5,000/-5,000 timing items retain gross exposure 10,000.

Recognition and error-versus-estimate conclusions remain with the underlying topic owner. Aged or unidentified items cannot be certified by this clean-certification route; remediate or obtain a separate conditional close decision.

Read the exact case schema in workflow.py and synthetic examples. Decimal strings only; positive rates/lives, nonnegative amounts and balanced cent-rounded journals. Source and GL gross populations must agree independently of net totals. Use case fingerprint certification only after source, period, framework and specialist review.

Every TB row has reviewed balance_sheet/profit_loss classification. The independent inventory must exactly cover all balance-sheet IDs, including equity and active zero balances. Corrections are aggregated across every mapped account before final reconciliation; an offset into another balance-sheet account must reconcile there too. Absolute and relative thresholds and item ageing are company-approved inputs, not universal standards.
