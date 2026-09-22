# TOPIC-02-004 — Trial Balance Review & Balance Sheet Reconciliations

Status: REVIEWED — Phase 2D
Primary capabilities: CAO-02-009, CAO-02-010

## Purpose
A trial-balance review detects ledger-level anomalies; a balance-sheet reconciliation proves a recorded balance to an independent or appropriately controlled source and explains reconciling items. Neither substitutes for the other.

## TB review
Compare current/previous periods, budget or operational expectations where useful; identify unexpected signs, dormant/new accounts, large/manual movements, unusual entity/dimension combinations, unexplained zeroes, stale balances, P&L-to-equity roll issues and out-of-balance consolidation/mapping effects. Investigation must resolve to transactions/accounting, not merely variance commentary.

## Reconciliation standard
Each reconciliation states: account/entity/period; GL balance; source/subledger balance; reconciling items; aging; owner; preparer/reviewer; source evidence; conclusion; open actions.

Formula: GL balance = independently supported balance + valid reconciling items, subject to account-specific presentation direction.

A reconciling item must have description, amount, origin date, expected resolution, accounting treatment, owner and evidence. A plug is not a reconciling item.

## Risk-tiering
Frequency/depth depends on balance magnitude, transaction volume, judgment, susceptibility to error/fraud, account volatility, prior issues, automation and source reliability. Low-risk accounts can use proportionate methods; material/high-risk accounts require stronger independent evidence and review.

## Controls
Complete account population; documented account ownership; timely preparation/review; source integrity; aged-item escalation; material unexplained differences prohibited; certification tied to evidence; dormant-account review; reconciliation policy exceptions approved.

## Systems/automation
Automate extraction/matching where rules are deterministic, but preserve unmatched-item queue and source lineage. Reconciliation tooling should distinguish timing, known valid differences, errors, duplicates and unsupported items.

## Scenarios
1. Bank GL agrees to bank feed but old outstanding checks remain: reconciliation not complete until aged items assessed.
2. Prepaid account agrees to internally generated schedule built from same GL: challenge independence/source completeness.
3. Zero-balance control account with gross offsetting items: TB balance alone does not prove integrity.
4. Cross-system revenue/AR rec in Excel every month: strong candidate for governed reconciliation automation/TrackedFR assessment.

## Completion
Balance is supported, differences explained and actionable, source lineage preserved, review evidenced, and material accounting consequences resolved.
