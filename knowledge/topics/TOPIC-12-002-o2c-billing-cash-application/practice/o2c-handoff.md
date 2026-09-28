# O2C handoff

## Operating decision and reconciled data
Separate contract/order, billing event, cash application and revenue recognition. Reconcile order/invoice sequences, invoice/batch totals to AR and GL, bank receipts to unapplied cash, credits to original invoices, and recognized revenue/contract balances to the technical conclusion. Keep amendment and refund identifiers.

## Adverse case and workpaper
An invoice is raised before performance and cash arrives before period end. Billing and cash events cannot prove revenue; route to Domain 03 revenue decision. Hold unsupported recognition, preserve contract/performance evidence and bridge deferred balance to final GL.

## Ownership and technical handoff
Billing owner confirms invoice population; accounting owner signs recognition; treasury supports bank feed. Interface lineage to 11-003, cash reconciliation to 12-005 and deficiency to 09-007.

## Acceptance and authority
Retain a period/entity scoped population, source and destination totals, immutable transaction IDs, exception disposition, approved entries and reviewer sign-off tied to the final GL version. Test both an ordinary transaction and the adverse case above; an SOP or performance metric without a reconciled accounting output does not pass. The parent README and method provide the broader process design. Technical accounting treatment must be decided under the applicable framework and period in the named technical topic; these operational runbooks do not replace it. Applicable US issuer ICFR concepts: [SEC Release 33-8810](https://www.sec.gov/rule-release/33-8810); otherwise route legal/control duties locally.
