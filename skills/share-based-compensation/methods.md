# Award classification, attribution and events

Read canonical05-007/008 knowledge and registers. Confirm grant date (approvals/understanding of terms), employee service, legal settlement obligation, grant terms, vesting/nonvesting conditions and external valuation before computing. Ordinary employee awards only; profits interests (including US ASU2024-01 period scope), nonemployee, group, withholding, settlement choice and classification-changing awards are specialist methods.

| Framework/route | Measurement | Conditions and policy |
| --- | --- | --- |
| IFRS2/AASB2 equity | Supported grant-date FV | Re-estimate service/nonmarket vesting quantities; market conditions in FV, not automatic cost reversal |
| ASC718 equity | Reviewed grant-date FV and attribution | Actual forfeiture election or estimate; independently review US classification/modification scope |
| FRS102 Section26 equity | Independently reviewed effective-edition model | Do not silently inherit US actual-forfeiture election or option simplifications |
| Cash/liability | Current/settlement-date supported FV | Remeasure liability through expense until settlement |

Use unique tranches with grant quantity/FV, validated ISO vest date and service attribution memo. Supply opening_cumulative and an opening_balance_memo tying prior service cost to the ledger. Each dated schedule row is within the current reporting period and covers every tranche, with a reconciled opening booked cumulative amount, expected vesting, actual forfeitures, service progress, current value and explicit condition assessments. Historical rows do not become current-period journals. The workflow calculates each tranche separately, avoiding unreviewed blended graded-vesting shortcuts. Progress is an approved service measure, not an inferred employee fact. At vest date it must be complete and quantities must agree to actual nonforfeited grants. Expected vesting cannot exceed nonforfeited grants. Actual forfeiture policy count = grants - actual forfeitures; estimate policy uses reviewed expected vesting. Service/nonmarket failure can remove eligibility; market failure alone does not.

Valuation input register requires model/share price/exercise price/volatility/risk-free/expected term/dividend yield/market condition treatment and reviewed evidence. The workflow consumes certified fair values; it does not manufacture an option valuation from missing market data. Validate inputs against independent specialist models.

Continuing award schedules must reach reporting date; stale interim service/FV cannot certify year-end balances. Modification recognition reaches that same reporting date. Settlement/cancellation uses a same-date service/census schedule, with full-vesting/event evidence; a closing event before year-end can close the award without inventing later activity.

## Events and journal/reconciliation

Cumulative cost = qualifying quantity × applicable fair value × approved service progress. Period expense = current cumulative - previous booked. Equity Dr expense/Cr award equity; cash Dr expense/Cr liability. Negative catch-up reverses the same credit, not a new income concept.

Beneficial ordinary equity modification with unchanged conditions and original probable vesting preserves original cost and adds max(modified FV - original FV at modification,0) × eligible count × remaining-service progress. Keep modification_date separate from the reporting recognition/event date and support remaining-service attribution in a memo. The supported actual_days basis computes elapsed/remaining service from validated dates; optional submitted progress must match it, rather than overriding chronology. Other service conventions need specialist schedules. An unvested modification cannot recognize full remaining cost immediately; progress at its modification date is zero, and at vesting is one. Different tranche remaining service periods need a specialist event schedule. US failed/probability-changing threshold cases route to ASC718 specialists. More than one modification requires a chronological separate event schedule. Cancellation, not vesting forfeiture, accelerates reconciled remaining original cost; repurchase up to event FV reduces equity and excess is expense. Cash vested settlement cannot precede the validated vest date; it remeasures to event-date FV, reconciles payment and clears liability. Replacement/conversion events are blocked, not forced into a beneficial-modification calculation.

## Worked and adverse examples

100employees ×100options, grantFV12, vest3years: expected90 year1 =>36000; expected80 year2 => cumulative64000/expense28000; actual82 year3 =>98400/expense34400. Equity reporting-date price must not replace grantFV12.
Cash rights10000, year1 FV8 and half service =>40000; vestFV12 =>120000, next expense80000, settlement120000 clears liability.
1000options grantFV10, year1 cost5000; modification-date oldFV8/newFV11 adds3000 over remaining service, total13000/year2expense8000. Do not replace original grantFV10 with11 or reverse cost because a market condition failed.

Reconcile grant/forfeiture/vesting/exercise/settlement counts, cap table/payroll, expense and equity/liability bridges. Inspect original/modified agreements, valuation versions, leaver/performance census and event chronology. Disclose terms, populations, valuation inputs, expense, unrecognized cost and event effects under actual framework/tier. Provisional IFRS2 paragraph ranges remain explicitly unverified.
