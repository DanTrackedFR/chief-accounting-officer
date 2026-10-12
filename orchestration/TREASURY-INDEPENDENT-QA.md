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

## Executed first independent review

`tests/test_treasury_independent.py` adds 40 distinct acceptance tests (subtest
mutations are not counted as additional tests). Initial 38-test execution exposed
these substantive findings, with later tests extending the ownership reproduction:

### TQ-1 — disconnected source claims (material)

Clean-source mutations to lender principal/carrying/currency, remaining contractual
payments, debt draw/fee population, contract notional, designation quantity,
external valuation movement, effectiveness/reserve values and bank interest
classification all still completed. Selected source columns were bound, while
other material company facts were ignored and synthetic reviewed native cases
were regenerated from fixed unrelated values. Permanent reproductions are the
source mutation tests. Remediation must bind actual material claims/populations,
not remove contradictory sources or rely on regenerated synthetic approval.

### TQ-2 — contradictory inherited designation evidence (material)

Swap/variable-debt relationship retained commodity purchase eligibility, whole
commodity-risk and approved purchase-plan memos from the original template.
`test_no_template_commodity_designation_evidence` reproduces this contradiction.
The fixture needs actual benchmark-interest and debt-source evidence throughout;
changing numeric tags alone does not change documentary evidence.

### TQ-3 — journal source nature aliases defeat identity (material)

Two owners' identical principal payment journals both became primaries when the
source origin/record were the same bank payment but their free-text `nature`
labels differed. A doubled balanced Financial Statements TB plus renewed exact
payload review did not reject this. This is independently reproduced directly in
`test_bank_source_identity_cannot_change_with_nature_alias`. Bank-event identity
must not change when event/account/nature labels change. Multiple accounting
components legitimately associated with one valuation still need supported
component identity; blindly deleting all same-record implications is not a fix.

Native debt evidence/maturity/EIR/modification gates, native Hedge valuation and
risk gates, cash completeness/noncash/reconciliation, atom double-use, excluded
owners and narrow Debt/FX selection passed the first execution. Native FX alone
correctly accepts a separately certified different supported settlement rate;
the source/bank contradiction is the rejected condition, so the independent test
was corrected to mutate the actual company FX rate source. Final independent
rerun remains pending authored remediation.

## Independent remediation verification

Final independent rerun: **49 distinct unittest methods passed** in
`orchestration.tests.test_treasury_independent`. Subtests, reruns and the separate
bank-retag focused rerun are not additional distinct tests.

TQ-1 is remediated by expanded exact native/result bindings and independently
qualified DocumentBindings over the frozen original material source bytes and
metadata. The runtime compares those records; it does not manufacture source
approval. The original lender/payment/notional/designation/valuation/effectiveness/
bank/draw/fee/rate attacks now fail closed. New prose-only facility-right mutation
and wrong-entity valuation metadata attacks also fail closed.

TQ-2 is remediated by actual benchmark-interest variable-debt qualification memos
and separately reviewed interest timing/notional evidence, replacing the inherited
commodity purchase-plan assertions. Accounting remains an interest cash-flow hedge,
not an FX principal hedge. The independently supplied valuation still provides the
amount; no curve or market input was created by the runtime.

TQ-3 is remediated by bank identity based on original origin/record independently
of nature labels, and exact cash contribution ties to actual Cash Flow bank IDs,
amounts and complete population. Both duplicate nature aliases and fresh-reviewed
bank origin/record retagging now fail closed. Native journal atoms remain visible
and owned exactly once, including FX's repayment witness. Noncash valuation OCI
and earnings implications remain separate qualified components.

Additional independent checks pass: stale imported owner result; missing/late
accounting designation; native wrong-risk/notional/valuation/reserve gates;
analytics hidden residual, unsupported volume and wrong owner-result assertion;
required reporting handoff omission; reconciliation residual; seven actual public
routes; proposed context/memory; narrow Debt/FX and irrelevant-owner exclusions.

Debt economics independently agree: base debt1000 + EIR80 - cash coupon80 -
principal200 =800, then remaining USD800 at1.10 gives reporting liability880 and
FX loss80. Cash2000 - coupon80 - principal200 =1720. External derivative40 divides
into OCI36 and earnings4 under separately measured designated-risk evidence.
Profit-156 = -interest80 -FX80 +hedge earnings4; indirect operating cash-80 =
profit-156 +FX80 -hedge earnings4. Equity1000 -156 +36 =880. No cash/FX/FV plug is
required. The interest bridge60→80 is an explicit reviewed rate attribution on
unchanged opening exposure1000; year-end principal repayment does not imply a
full-year volume effect. Benchmark-interest hedge does not offset FX principal
remeasurement; management's broad FX-offset claim must remain rejected.

Boundaries remain: independently supplied reset/payment/EIR inputs are not a
forecast engine; no modification/extinguishment, inferred waiver/refinancing,
qualifying-asset capitalization, autonomous derivative valuation, legal covenant
certification, or multi-entity execution. Cash-flow primary-source conflict keeps
the primary Case partial; qualified clean source control completes. This review
is not exact-head CI or final repository-wide regression; those are recorded by
the integration owner after the immutable final candidate is published.

## Final independently executed broader regression

After latest target/class handoff gates, wildcard native population bindings,
monetary public narrative and Cash Flow's explicit current Debt/FX imports:

| Independently run suite | Distinct tests | Result |
|---|---:|---|
| Treasury independent | 49 | PASS |
| Repository/public/canonical | 53 | PASS |
| Lease | 17 | PASS |
| Income tax supplement | 10 | PASS |
| Agriculture supplement | 12 | PASS |
| Agriculture independent | 71 | PASS |
| Insurance supplemental/independent claims | 35 | PASS |
| Hedge supplement | 4 | PASS |
| Hedge independent | 7 | PASS |
| Inventory supplemental/independent claims | 262 | PASS |

Other suites total471; including Treasury independent totals520. Treasury49 is
already included in the full orchestration test discovery and must not be counted
twice in final repository totals. All seven supplemental/canonical validators and
`git diff --check` passed. Exact commands, exit codes and original output are in
`/tmp/treasury-other-regression.log`; this log is local verification evidence,
not an exact-head Actions claim.

Additional independently executed native category checks use existing supported
fixtures: funded debt draw1000 less directly attributable fee20 gives net cash980;
standalone swap opening liability80, FV loss30 and cash settlement40 gives closing
liability70. Each source journal was qualified as a primary with a corroborating
cash witness exactly once. Duplicate event aliases, amount mutations and renamed
accounts attempting native atom reuse fail closed (eight scratch executions,
not additional repository unittest methods). These checks do not establish
foreign debt draw integration or nonzero-opening/settled cash-flow hedge reporting.
The native Hedge reporting adapter explicitly excludes those routes. The flagship
control proves the first-year pending benchmark-interest hedge with no settlement;
more advanced combined reporting requires its separately governed scope and tests.

## Permanent category coverage and reporting scope guard

Final independent suite expanded to **52 distinct methods, all PASS**. The three
additional methods permanently preserve previously separate scratch checks:

- `test_native_funded_draw_ownership_and_alias_attacks` executes the actual
  supported native funding/eligible-fee case and tests exact-once witnesses,
  relabelled event duplication, amount changes and account aliases.
- `test_native_standalone_derivative_settlement_ownership_attacks` executes the
  actual native standalone swap settlement and applies the same ownership attacks.
- `test_reporting_excludes_advanced_hedge_movement_scope` exercises the newly
  explicit first-year continuing Hedge→Financial Statements scope gate against
  standalone route, nonzero derivative opening/settlement, reserve opening,
  reclassification and basis-adjustment mutations. None can obtain the flagship's
  reporting handoff by matching amounts alone.

### TQ-4 — explicit reporting scope preservation

Independent contract reconstruction identified that the new generic Hedge metric
bindings lacked the native reporting adapter's explicit movement-scope boundary.
The integration owner added that boundary rather than implying support for
untested second-year/settled/standalone reporting. The permanent independent
scope test now passes. Native supported standalone valuation/settlement remains
available in its own workpaper; the Treasury flagship reporting extension is
first-year continuing cash-flow hedge only. This does not claim a complete
standalone settlement reporting scenario.

The latest independent 52-method execution passed in32.685 seconds. Earlier49
remains historical execution evidence, not extra distinct tests. Other independently
run suites remain471 distinct methods; combined independent execution coverage
is523, with Treasury52 also included in orchestration discovery. Complete authored
orchestration/production totals and final exact-head CI are reported separately by
the integration owner.
