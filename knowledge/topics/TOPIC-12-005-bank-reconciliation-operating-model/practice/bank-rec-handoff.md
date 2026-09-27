# Bank reconciliation handoff

## Operating decision and reconciled data
Bank-account inventory is independent of ledger account listing; obtain statement/feed completeness by bank/account/day, bank and ledger opening/closing balances, transaction-level matched/unmatched totals, FX and timing-item aging. Evidence uses statement identifier, feed hash, GL extract timestamp and reviewer challenge.

## Adverse case and workpaper
Bank feed omits one day but matching engine shows no unmatched items. Block certification, recover missing bank period, rerun matching and inspect intervening cash transactions; assess close impact and interface deficiency.

## Ownership and technical handoff
Treasury confirms bank universe and authorized accounts; accounting owns GL adjustment/certification. Interface to 11-003/010, reconciliation design to 09-005, suspicious payment to 09-009 and cash presentation to Domain 02.

## Acceptance and authority
Retain a period/entity scoped population, source and destination totals, immutable transaction IDs, exception disposition, approved entries and reviewer sign-off tied to the final GL version. Test both an ordinary transaction and the adverse case above; an SOP or performance metric without a reconciled accounting output does not pass. The parent README and method provide the broader process design. Technical accounting treatment must be decided under the applicable framework and period in the named technical topic; these operational runbooks do not replace it. Applicable US issuer ICFR concepts: [SEC Release 33-8810](https://www.sec.gov/rule-release/33-8810); otherwise route legal/control duties locally.
