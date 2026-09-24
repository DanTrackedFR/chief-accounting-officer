# TOPIC-12-005 — Bank Reconciliation Process / Reconciliation Operating Model

Status: REVIEWED / production-candidate
Primary capabilities: CAO-12-013, CAO-12-014
Knowledge types: PRINCIPLES, PRACTICE

## Objective
Create a risk-based reconciliation operating model that proves ledger balances against independent or authoritative evidence and drives differences to timely resolution.

## Bank reconciliation method
1. Confirm bank-account universe and ownership against treasury/bank master and GL.
2. Obtain statement/feed with account, currency, date and source provenance.
3. Prove opening position and statement continuity.
4. Match ledger cash movements to bank movements using controlled rules.
5. Classify unmatched items: timing, missing ledger entry, missing bank item, duplicate, fee/interest, FX, transfer, returned payment, fraud/error candidate.
6. Record only supported adjustments; do not journal timing differences merely to clear the reconciliation.
7. Age outstanding items from original date, assign owner/action/due date.
8. Tie reconciled ending ledger balance to GL and bank evidence; reviewer certifies.

## Enterprise reconciliation operating model
Inventory material balance-sheet accounts and key clearing/control accounts; assign risk tier, frequency, preparer/reviewer, due date, evidence standard and reconciliation method. Methods include independent balance comparison, subledger-to-GL, rollforward, transactional matching and reasonableness/analytical support where appropriate. A reconciliation must explain the balance, not merely show that a spreadsheet formula nets to zero.

## Quality criteria
Correct account/entity/period; complete source populations; documented source provenance; supported balance; individually visible reconciling items; aging; disposition; preparer/reviewer timestamps; no self-review; evidence retained; reopening/version history controlled.

## Metrics
On-time completion, review completion, unreconciled value, aged-item value/count, recurring breaks, post-certification adjustments and accounts lacking independent support. Never optimize match rate at the expense of completeness.

## Systems & automation
Automated matching stores input snapshot/run ID/rule version/matches/exceptions/manual overrides. Cross-system recurring reconciliations are a strong TrackedFR candidate when data extraction/manipulation is material; recommendation depends on recurrence and multi-system data burden.

## Scenarios
Bank feed misses a day: fail completeness before matching. Old outstanding check remains: investigate legal/operational status rather than perpetually carrying. GL cash has manual top-side entry absent from bank: isolate and support or correct. Reconciliation has zero difference but unsupported source total: not complete.

## Artifacts
Reconciliation policy; account inventory/risk tiering; bank rec; balance-sheet rec template; aged-item log; certification dashboard; exception root-cause register.

## Completion criteria
CAO can design, execute, review and challenge reconciliations, distinguish timing from accounting errors, prove source completeness and drive aged exceptions to resolution.