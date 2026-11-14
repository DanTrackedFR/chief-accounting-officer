# Phase A independent accounting QA — plan and pre-implementation contract review

Reviewer: independent accounting QA agent (`accounting_qa`), separate from implementation.
Baseline inspected: `97d0621331c6ad2a66b12ed09c0ec40c05c626b9`.
Status: planning/contract review only; **no implementation acceptance is claimed**.

## Inspected contract and production path

`architecture/PRESUMED-SOURCES-DESIGN.md`, `interfaces/source-case.schema.json`,
`skills/source_execution.py`, `skills/source_screening.py`,
`skills/fixed-assets/workflow.py`, native journal creation and public serialization.
This is review of the existing bounded machinery method, not approval of new standards claims.
Formal/Profile 1.1 methods and the approved knowledge population must remain unchanged.

## Decisions required before changing amounts

1. **Life basis.** Existing straight-line calculation uses remaining depreciable carrying
   balance divided by remaining life at the reporting-period opening (or availability for
   use for a new asset), not original gross cost divided by original total lifetime.
   Preserve that basis; distinguish input remaining life from original total useful life.
   For sequential periods, opening accumulated depreciation and remaining life must advance
   together; replaying unchanged opening assumptions is not a roll-forward.
2. **Units.** Legacy `remaining_life` means years. New `remaining_life_months` means months.
   Equivalent months and years must produce the same cent-rounded result. Retain exact
   Decimal/rational arithmetic through the charge; avoid pre-rounding months/12, especially
   one-month final periods. Explicit disagreement blocks the affected row.
3. **Actual days.** Existing method includes both eligible start and end dates and splits
   calendar years with denominators 365 or 366. Preserve no-election behavior. Life is
   elapsed-year basis under this policy; it is not implicitly calendar-month life.
4. **Monthly periods.** Full eligible month = annual remaining-balance charge/12.
   Partial month must have an explicit, governed supported policy (e.g. eligible actual days
   in the calendar month) or an actionable unresolved requirement. Neither a half-month nor
   a full-month rule may be invented. Ready date and disposal date bound eligibility.
5. **Policy priority.** Applicable confirmed company policy wins; current explicit election
   cannot silently supersede it. Applicable established memory follows valid current
   election; fallback remains actual days. A supplied expected amount is comparison evidence,
   not policy confirmation. Unsupported/malformed/conflicting elections cannot leak charges.
6. **Exhausted life.** Zero life with remaining depreciable balance blocks charging until
   estimate/balance assessment. Negative life is inconsistent. Fully depreciated assets may
   remain in use without disposal; no amount or disposal journal may be fabricated. A zero
   life row must be explained specifically even if its charge is zero.
7. **Supplied balances.** Require explicit opening or closing comparison basis/date. Opening
   NBV = opening gross minus opening accumulated, before current additions. Closing NBV =
   supported closing gross minus closing accumulated; after disposal these are zero.
   A comparison difference never changes the accounting basis or creates a balancing entry.
8. **Journals and assumptions.** Public journals must match native workpaper lines exactly,
   with stable row/Case references and clear proposals-only status. Assumptions must describe
   actually used inputs and distinguish class/default/current policy provenance. Unresolved
   rows must not produce journal lines; valid unrelated rows may remain qualified proposals.

## Fresh independent numerical scenarios

Use independently authored amounts, not implementation expected fixtures. Round each native
journal amount half-up to cents once, after exact arithmetic.

| Scenario | Independent expected calculation |
|---|---|
| May monthly | Opening gross 79,200; accumulated 18,000; residual 3,600; 24 months (=2 years). Basis 57,600; annual 28,800; May charge 2,400; closing accumulated 20,400; closing NBV 58,800. |
| May actual days | Same asset: 28,800 ×31/365 = 2,446.03; closing NBV 58,753.97. |
| February monthly | Same basis: 2,400 in 2026. Leap-year monthly arithmetic also 2,400; a hosted 2028 Case must remain outside current 2026 scope. |
| February actual days | 2026: 28,800 ×28/365 = 2,209.32. Leap-year arithmetic probe: 28,800 ×29/366 = 2,281.97; do not remove runtime year support boundary. |
| Partial May | May 11–31 eligible, explicit actual-days-in-month policy: 2,400 ×21/31 = 1,625.81. Without supported partial policy: affected row unresolved, no journal. |
| Mid-month disposal | May 1–19 inclusive: 2,400 ×19/31 = 1,470.97 monthly-partial; supported disposal workpaper must derecognize updated carrying amount and distinguish cash from receivable. |
| Unit equivalence | Independent basis 45,360: 12/24/36/60 months =1/2/3/5 years. Full-month charges 3,780/1,890/1,260/756. Verify both consistently supplied and conflicting inputs. |
| Final cap | Basis 128.55, remaining months 0.5, full month: uncapped 257.10 capped at 128.55; residual retained. |
| Exhausted | Gross 20,000; accumulated 16,000; residual 1,000; zero life: 3,000 unresolved depreciable balance, no charge. Gross=accumulated 20,000, residual zero: asset may stay in use, no automatic disposal. |
| Comparison defect | May monthly asset supplied closing NBV 318,800 instead of 58,800: variance +260,000 (supplied minus calculated), unchanged 2,400 depreciation/journal. |
| Partial comparison | Supply only closing accumulated 20,400: match, no invented NBV input; supply both with NBV 58,801: inconsistency and +1 variance, no journal alteration. |
| Sequential months | May gross 79,200, acc 18,000, residual 3,600, life 24 months; June acc 20,400 and life 23 months: same 2,400 June charge, aggregate 4,800, closing NBV 56,400. |

## Integrated QA execution gate

After implementation SHA is supplied, independently execute actual authenticated hosted HTTP,
persisted Case/reopen and retry scenarios. Challenge all four supported framework selectors,
unsupported scope rejection, missing/blank/null/wrong-type Case fields, mixed invalid life and
valid rows, policy conflicts, optional malformed comparisons, balance dates, journal equality,
assumption provenance and no posting authority. Publish commands, tested SHA, expected/actual
amounts, findings and dispositions. A code inspection or this plan is not passing QA.
