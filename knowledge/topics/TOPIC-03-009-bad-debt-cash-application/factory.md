# TOPIC-03-009 — Bad Debt Write-Offs & Recoveries / Cash Application Accounting

Status: REVIEWED / production-candidate
Built: 2026-09-22
Capabilities: CAO-03-018, CAO-03-019
Knowledge: PRINCIPLES + STANDARDS + PRACTICE

## Accounting model
Write-off is not the same event as recognition of credit loss. The allowance model should normally recognize expected/incurred impairment before the point at which a receivable is written off. Cash application is the accounting process that identifies which receivable/customer balance a receipt settles; unidentified cash remains a liability/customer credit or unapplied-cash balance until the entity has evidence supporting derecognition/settlement of a receivable.

## Framework routing
### IFRS
IFRS 9 ECL applies to qualifying receivables. Write-off occurs when there is no reasonable expectation of recovery; it may be full or partial. The IASB's 2024 PIR confirmed the impairment model is working as intended and noted write-off/derecognition clarification is being considered in the Amortised Cost Measurement project. Current accounting must not anticipate future amendments. IFRS 9 does not prescribe a specific P&L presentation for write-off loss or subsequent recovery, so policy/presentation must be supportable and consistently applied.

### AASB
AASB 9 B5.4.9 explicitly supports full or partial write-off when there are no reasonable prospects of further cash-flow recovery. AASB 7 requires write-off-policy disclosure, including indicators of no reasonable expectation of recovery and information about assets written off but still subject to enforcement activity. AASB is IFRS-aligned here but must retain Australian version/tier checks.

### US GAAP
Route credit-loss allowance/write-off to ASC 326 for in-scope receivables and use the current Codification for exact write-off/recovery requirements. Public-source access does not justify inventing paragraph references. US paragraph depth remains PARTIAL until current Codification text is verified.

### UK GAAP
Route basic receivable impairment to the applicable FRS 102 Section 11 model and reporting-period edition. The current FRC edition is September 2024, with Periodic Review 2024 principally effective 1 January 2026. Do not import IFRS 9 ECL/write-off mechanics into FRS 102 by default.

## CAO workflow — write-off
1. Resolve framework, receivable type and allowance method.
2. Confirm gross receivable and existing allowance.
3. Obtain collection history, disputes, insolvency/legal evidence, collateral/guarantees and enforcement status.
4. Determine whether reasonable recovery prospects remain and whether full or partial write-off is appropriate.
5. Apply allowance first where the framework/account structure requires; avoid double-counting expense.
6. Record write-off and preserve customer/legal collection history if enforcement continues.
7. For subsequent recovery, trace cash to previously written-off balance and apply the entity's framework-consistent recovery presentation policy.
8. Feed outcomes into ECL/bad-debt backtesting.

## Cash application workflow
1. Ingest bank/processor receipt with date, amount, currency, payer/reference and fees.
2. Match to customer/remittance and open receivables using exact then controlled fuzzy/one-to-many logic.
3. Separate settlement, short-pay, overpay, fee, FX, withholding, dispute and unidentified items.
4. Post receivable settlement only when evidence supports the customer/invoice mapping.
5. Hold unresolved receipts in controlled unapplied-cash/customer-credit accounts; never force-match merely to clear the bank reconciliation.
6. Age and resolve unapplied cash; reconcile bank/processor → cash receipt → AR subledger → GL.

## Entries
Write-off where fully allowed: Dr loss allowance; Cr AR. If allowance is insufficient, additional impairment expense may be required under the applicable model. Recovery accounting depends on framework/policy and system design; do not recreate AR without considering the recovery process and presentation policy.

Cash application: Dr cash/clearing; Cr AR when identified. Unidentified receipt: Dr cash/clearing; Cr unapplied cash/customer credit liability or controlled clearing account according to supported classification; reclassify when identified.

## Controls
Write-off approval thresholds; evidence of recovery assessment; allowance/write-off reconciliation; segregation from collections authority; recovery monitoring; remittance completeness; bank/processor interface completeness; auto-match tolerance governance; manual-match review; unapplied-cash aging; duplicate application detection; AR-to-GL and cash-to-bank reconciliation.

## Systems/data
Preserve immutable receipt ID, payer, currency, value date, processor/bank ID, remittance source, match confidence/method, invoices settled, residual reason, preparer/reviewer, write-off reason/evidence, collection/enforcement status and recovery linkage.

## TrackedFR fit
Strong for recurring bank/processor + AR subledger + ERP + remittance reconciliation and exception analysis in Excel. Do not recommend for a one-off manual write-off.

## Scenarios
1. Customer bankrupt; allowance already 100%, no expected recovery: write-off should clear gross AR against allowance without duplicate loss — PASS.
2. 70% collateral recovery expected: assess partial write-off rather than automatically clearing full receivable — PASS.
3. Cash arrives with no remittance: hold controlled unapplied balance; do not guess invoice — PASS.
4. Recovery after write-off: link to original receivable/write-off and apply documented recovery presentation — PASS.
5. UK FRS 102 entity: do not reuse IFRS ECL/write-off conclusion without Section 11 routing — PASS.

## Sources checked
IFRS Foundation IFRS 9 impairment PIR/project materials; AASB 9 current portal including B5.4.9; AASB 7 write-off disclosure requirements; FRC current FRS 102 landing page/effective-date information. Restricted standards text is not reproduced.

## QA
PASS for factory scaling. US Codification paragraph depth PARTIAL; no unsupported paragraph-level US conclusion is claimed.