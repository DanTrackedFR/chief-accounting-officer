# TOPIC-03-009 — Bad Debt Write-Offs & Recoveries / Cash Application Accounting

Status: REVIEWED
Capabilities: CAO-03-018, CAO-03-019
Knowledge: PRINCIPLES + STANDARDS + PRACTICE
Framework sensitivity: HIGH for write-off/impairment interaction; LOW for cash-application mechanics
Source check: 2026-09-22

## Scope
Accounting for derecognition/write-off of receivables judged uncollectible, subsequent recoveries, and accurate application of customer cash to receivable balances. ECL/allowance measurement is owned by TOPIC-03-008.

## Framework architecture
IFRS 9 / AASB 9 write-off logic applies when there is no reasonable expectation of recovery; write-off reduces the gross carrying amount and interacts with the loss allowance. Recovery after write-off is accounted for consistently with the framework and entity policy. US GAAP routes trade-receivable credit losses through ASC 326 and related receivable guidance; full current Codification paragraph-body verification remains source-depth PARTIAL under the programme-wide public-source limitation. UK FRS 102 Section 11 uses its own impairment/derecognition architecture and must not be treated as IFRS 9 ECL.

## CAO write-off workflow
1. Resolve framework, receivable, customer/entity and existing allowance treatment.
2. Obtain collection history, disputes, insolvency/legal facts, collateral/guarantees and recovery actions.
3. Distinguish write-off from merely increasing an allowance. A write-off is not a device for cleaning aged AR while collection remains reasonably expected.
4. Determine full versus partial write-off and whether contractual/legal collection activity can continue after accounting write-off.
5. Post against allowance where applicable; identify any incremental P&L effect rather than double-counting loss already provided.
6. Preserve customer-level subledger history and approval evidence.
7. For later recovery, link cash to original written-off item and apply framework/entity-policy accounting consistently.
8. Feed write-off/recovery outcomes into ECL backtesting.

## Cash application workflow
1. Establish bank receipt population and completeness.
2. Identify payer/customer/entity/currency and remittance evidence.
3. Match to open invoices/credits using exact references first, then controlled rules.
4. Separate genuine customer credit, unapplied cash, short pay, deduction, dispute, FX difference, bank fee and unidentified receipt.
5. Do not force-match residuals merely to clear queues.
6. Post application with transaction lineage; route disputes/credits to appropriate accounting topic.
7. Reconcile bank receipts → cash receipts journal → AR subledger → GL.
8. Age unapplied/unidentified cash and escalate exceptions.

## Journal patterns
Write-off where allowance already exists: Dr loss allowance / Cr trade receivable, subject to framework and ledger design. Incremental loss beyond allowance routes through credit-loss expense. Cash application: Dr cash / Cr trade receivable when entitlement and matching are established; unidentified receipts may require a controlled clearing/customer-credit classification rather than arbitrary AR application.

## Controls / audit
Write-off approval thresholds; segregation from collections; evidence of recovery assessment; allowance/write-off reconciliation; recovery tracking; bank-feed completeness; cash-application rule governance; unmatched-cash aging; duplicate application detection; subledger-to-GL reconciliation; manual override review.

## Systems/data
Customer/invoice IDs, receipt ID, bank transaction, currency, remittance, applied amount, write-off reason, approval, allowance linkage, recovery ID and source evidence. Automated matching confidence must be auditable and exceptions retained.

## Artifacts
Write-off memo/register; approval; recovery log; cash-application reconciliation; unapplied-cash aging; ECL backtest feed; exception report.

## Scenarios
- Customer in liquidation with no realistic recovery: assess full/partial write-off using framework evidence.
- 180-day invoice still under active enforceable payment plan: aging alone does not mandate write-off.
- Recovery of previously written-off invoice: link to original item and avoid recreating gross AR without basis.
- One bank receipt covers five invoices plus disputed deduction: apply supported invoices and route residual, not force-match.
- Receipt payer name differs from customer because parent pays centrally: require relationship/remittance evidence.

## TrackedFR fit
Strong when recurring bank/AR/ERP datasets require multi-system matching, reconciliation and exception handling in Excel. Not a fit merely because a write-off approval is documented in a spreadsheet.

## QA
PASS for production-candidate topic. Cross-topic dependency to TOPIC-03-008 is explicit; UK impairment divergence preserved; US paragraph-depth limitation remains PARTIAL but non-blocking.