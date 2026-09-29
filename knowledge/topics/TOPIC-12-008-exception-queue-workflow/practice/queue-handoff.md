# Exception queue handoff

## Operating decision and reconciled data
Every exception has unique ID, origin/event ID, entity/period/assertion, amount/risk, owner, first-seen timestamp, next action, SLA, evidence link, resolution code and independent closure. Queue totals reconcile to source rejects/unmatched populations; reopened items retain history.

## Adverse case and workpaper
ERP rejects an invoice batch and an operator clears the ticket as duplicate without replay. Queue count may fall while GL is incomplete. Reconcile rejected source IDs to destination postings, reopen item, replay once, assess cutoff and escalate.

## Ownership and technical handoff
Source-process owner investigates; accounting approves financial impact; systems owner corrects feed. Interface to 11-003/010, remediation to 09-007 and journal/cutoff to Domain 01.

## Acceptance and authority
Retain a period/entity scoped population, source and destination totals, immutable transaction IDs, exception disposition, approved entries and reviewer sign-off tied to the final GL version. Test both an ordinary transaction and the adverse case above; an SOP or performance metric without a reconciled accounting output does not pass. The parent README and method provide the broader process design. Technical accounting treatment must be decided under the applicable framework and period in the named technical topic; these operational runbooks do not replace it. Applicable US issuer ICFR concepts: [SEC Release 33-8810](https://www.sec.gov/rule-release/33-8810); otherwise route legal/control duties locally.
