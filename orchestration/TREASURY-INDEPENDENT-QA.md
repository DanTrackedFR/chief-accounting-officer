# Independent Treasury acceptance review

Reviewer context is separate from authored implementation. Baseline reconstructed:
`a8e11237fbbfa0daeff74f47c75eae52b430c855`. This document records acceptance
criteria before implementation; it is not a claim that pending checks passed.

## Independent architecture reconstruction

The current architecture retains one CAO runtime, reviewed semantic intake and
production owner execution. Fact-family selection is governed by the existing
registry. Intake candidates are never qualified accounting approvals. Existing
SaaS source bindings, reviewed result bindings and exact-case certification must
remain effective. Public output must use `public_record`.

Debt's supported method is plain amortized-cost debt with an independently
supplied actual/actual compound EIR, complete remaining payment PV backtest and
principal-pro-rata carrying allocation. Intra-interval draw/reset/fees, modification,
legal waiver and other methods cannot be invented. FX supports independently
reviewed opening monetary books, settlement rates and reporting rates. Debt's
current output has no autonomous foreign-currency schedule conversion method.
Hedge consumes qualified externally measured whole-instrument valuation, actual
contract/notional and separately evidenced designated risk; economic relationship
alone does not establish accounting designation. Its native reporting adapter is
narrower than its native calculations: first-year continuing cash-flow hedge,
zero opening reserve/derivative, no settlement/recycling/basis adjustment.
Cash Flow owns cash classification and independent direct/indirect/cash bridges,
not debt or derivative recognition. Fair Value quoted-equity output does not
qualify a derivative valuation. ECL has no automatic liability/derivative mandate.

## Integration risks identified before implementation

1. Existing runtime handoff allowlist does not bind Debt/Hedge/Cash metrics to
   reporting. Treasury reporting must require explicit semantic owner lineage.
2. Existing journal qualification validates mapped gross vectors and consumes all
   native atoms, but arbitrary distinct event labels alone cannot establish
   independent source economics. Relabelled source-equivalent postings need
   executable attacks, including account aliases and overlapping split atoms.
3. Reporting a foreign debt requires a governed cross-owner conversion bridge;
   adding Debt and FX outputs indiscriminately can duplicate settlement/interest.
4. Hedge native reporting boundaries must remain explicit if opening reserves or
   settlements are added to orchestration. Equal totals are insufficient evidence.

## Independent attack matrix

| Category | Independently derived acceptance attack |
|---|---|
| Debt versus cash | Equal cash/debt deltas do not erase EIR/FX noncash movements |
| Expense versus interest cash | Coupon substituted for independently supported EIR must fail |
| FX | Foreign amount/rate or liability sign mutation cannot close |
| Valuation | Missing/stale/wrong entity/date/currency qualified valuation cannot close |
| Qualification | Missing/late designation cannot obtain qualifying hedge OCI |
| Effectiveness | Unsupported method/notional/risk item and cumulative lower-of mismatch fail |
| OCI/P&L | FV change must equal governed OCI plus earnings, without duplicate reserve posting |
| Exact-once | Relabel repayment, settlement, interest and FX; account aliases cannot evade ownership |
| Cash classification | Wrong framework interest election and changed comparative policy fail |
| Noncash | FV/OCI/remeasurement inserted into bank cash cannot close |
| Classification | Remove rights evidence or alter maturity independently of payments: no clean split |
| Covenants | Source KPI arithmetic cannot certify legal waiver or reporting-date rights |
| Reporting | Remove selected owner's required handoff or substitute equal unrelated metric: fail |
| Reconciliation | Residual omission/plug cannot create COMPLETE |
| Analytics | Rate/volume inversion, duplicate FX and hidden residual fail |
| Hypotheses | Management assertion remains tested hypothesis, never unsupported causation |
| Dimensions | Same values with wrong entity/period/currency fail |
| Stale results | Mutated owner case/result must requalify exact source and fingerprint |
| Lineage | Four material conclusions trace to reviewed native input and raw source; one crosses owners |
| Modes | Narrow debt/FX/hedge/cash requests avoid broad close default |
| Owners | No unrelated Revenue/Inventory/Insurance/Consolidation/ECL/FV selection |
| Borrowing Costs | Ordinary interest never routes capitalization; qualifying asset exposes unavailable owner |
| Privacy | Raw sources/reviewer/hash/tiers/internal IDs absent in every public route |
| Outcome | Unresolved material conflict PARTIAL/BLOCKED; qualified clean control COMPLETE |

## Required execution record

Independent tests will import the completed flagship through intake, then mutate
native inputs with renewed synthetic certification where necessary. This isolates
accounting gates from stale-fingerprint rejection. Runtime/source attacks will
also test reviewed bindings and event identity directly. Each substantive defect
requires an executable reproducer, authored remediation and independent rerun.
Repeated executions are not distinct test counts. Pending implementation means
all matrix acceptance results are currently PENDING.
