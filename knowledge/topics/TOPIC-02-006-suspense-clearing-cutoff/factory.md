# TOPIC-02-006 — Suspense & Clearing Accounts / Cut-Off Accounting

Status: REVIEWED
Capabilities: CAO-02-013, CAO-02-014
Knowledge mix: PRINCIPLES + PRACTICE + underlying framework recognition rules.

## Objective
Prevent temporary holding accounts and period-boundary timing from obscuring the economic substance, completeness or classification of transactions.

## Suspense / clearing principles
Use a suspense or clearing account only for a defined temporary purpose with named owner, expected clearing mechanism and aging threshold. It is not a destination for unresolved accounting.

Required register fields: account, purpose, permitted source, normal sign, owner, clearing event, expected clearing time, prohibited uses, balance threshold, aging buckets, reviewer and escalation.

CAO workflow: obtain transaction-level population; classify by source and age; match offsetting legs; identify system/interface failures; determine correct accounting destination; post corrections; investigate recurring root cause; certify residual balance with item-level support.

Red flags: old items, round-dollar plugs, unsupported manual journals, recurring reclasses, mixed processes in one account, credit/debit items netted, large balance that clears immediately after reporting date, unknown owner.

## Cut-off principles
Cut-off follows the underlying recognition principle, not invoice/payment date by default. For each material flow identify the economic recognition event, source evidence, system timestamp and period-end treatment.

Typical evidence: goods receipt/service delivery; customer performance/acceptance; shipment/control transfer where relevant; payroll service period; contract milestones; bank settlement; asset availability for use; lease commencement; intercompany counterpart confirmation.

## CAO cut-off workflow
1. Identify material transaction streams and applicable accounting topic.
2. Define recognition event and evidence.
3. Map operational event to ERP/subledger posting logic.
4. Test transactions around period end in both directions: recorded before cutoff and recorded after cutoff.
5. Identify unrecorded liabilities/assets/revenue/expenses and premature recognition.
6. Assess returns, credits, reversals and subsequent invoices/cash as corroborating evidence.
7. Correct and document exceptions; remediate systemic timing gaps.

## Controls
Period-end receiving/service confirmation; unbilled/GRNI reports; shipping/acceptance reports; subledger close controls; interface timestamp monitoring; restricted backdating; post-close journal monitoring; suspense aging; clearing-account reconciliation.

## Systems / automation
Preserve business-event timestamp separately from accounting posting timestamp. Automated cutoff tests can compare source events, invoices and ledger dates and route exceptions. Recurring multi-system cutoff triangulation is a strong TrackedFR candidate.

## Artifacts
Suspense policy/register; aging report; cutoff matrix by process; period-end test pack; exception log; root-cause analysis; correcting-entry pack.

## Scenarios
Goods received 30 Dec, invoice 4 Jan: route to inventory/AP or expense/accrual recognition based on facts, not invoice date. Customer invoice 29 Dec for January service: billing date does not establish revenue. Clearing account carries unmatched cash for 90 days: investigate customer/source and classification rather than certify net balance.

## QA
PASS: ties cutoff to underlying accounting recognition; suspense balances require item-level resolution and root-cause governance.