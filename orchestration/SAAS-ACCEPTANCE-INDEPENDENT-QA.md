# Independent SaaS acceptance design

This is test design derived independently from repository contracts and knowledge.
It is not acceptance of implementation bytes that have not yet been reviewed.

Sources reconstructed: Revenue workflow cumulative-to-period contract bridge;
AR operational invoice/receipt/credit and dated customer liability workflow;
ECL classification, exposure, allowance and native journal mechanics; FX
monetary transaction schedules; runtime exact-input downstream challenge,
economic ledger and mapping; semantic fact validation and material questions;
AR independent population completeness knowledge (TOPIC-03-011); customer
credit origin/dispute knowledge (TOPIC-03-010); monetary FX/translation boundary
(TOPIC-06-003). Source knowledge explicitly warns that zero net GL difference
can hide missing and duplicate invoices of equal amounts.

## Specialist extension review requirements

### AR monetary-FX import

The extension must consume a freshly executed FX-owner monetary result, not
calculate rates or accept a caller-asserted gain. Link one exact FX item to one
invoice/customer. Preserve original currency, nominal amount, initial date,
original due date and rate lineage. The dated prefix logic for deposits remains
untouched. Functional opening/invoice values and closing remeasurement must be
separate; ageing uses outstanding closing exposure in functional currency while
delinquency still uses original due dates. Foreign receipts require distinct
settlement lineage if supported; otherwise explicitly remain unsupported.

Mutate each: foreign amount, currency, customer/invoice ID, opening book,
monetary classification, closing amount, gain, item fingerprint, period, entity,
functional currency, owner completion and original due date. Reject copied FX
result from another item; duplicate imports; a gain assigned to both billed
movement and FX movement; an import used for a contract liability; an unsupported
foreign receipt silently normalized; FX ignored in customer confirmation/GL.
Verify AR 1.0 cases unchanged and zero FX does not bypass review.

### Economic journal ownership allocation

Allocation must be exact-payload independently reviewed, complete over native
owner implications, and stable against stale-result reuse. It must retain the
native workpapers and distinguish same-event corroboration from unrelated equal
amounts. Journal identity must include source event and economic nature, not
only a numerical/account signature. A Revenue release and annual invoice are
not one event just because both equal 100. ECL additions/cash/FX journals also
overlap with AR/Revenue/FX; all implicated owners require coverage.

Attack: omit one native journal; allocate twice; suppress a genuine correction;
claim two different customers' equal invoices are duplicates; attribute a
receipt as billing; change allocation after approval; change result after
allocation; map revenue to deferred liability to force a GL tie; supply reviewed
allocation covering stale fingerprint; split journal lines across inconsistent
events; retain both FX and ECL gross FX for one remeasurement. Valid allocation
must produce one real GL effect and full native evidence lineage.

### ECL exposure and rate qualification

Current ECL loss-rate arithmetic does not independently reconcile summed term
exposures to gross carrying amount. Integration must enforce exposure population
and bucket lineage to actual AR result, including monetary FX, separately from
loss-rate review. A supported review memo does not cure a wrong exposure amount.

Attack: correct gross rollforward but half the scenario exposure; duplicate
customer/exposure; missing disputed customer; bucket shifted without dates;
stale reviewed rate table; invented rate; rate outside [0,1]; wrong framework;
IFRS general staging substituted for simplified model; UK own-model replaced
with IFRS portfolio; allowance counted as AR write-off; credit concession
classified as insolvency without Revenue disposition; FX allowance/gross events
duplicated between ECL and FX. Require allowance bridge reconciliation and
explicit unqualified assumption questions, not runtime-created approvals.

### Analytics expansion

Monthly actual/prior-actual comparators must remain distinct from budgets and
forecasts. Each bridge carries signed typed roles, source lineage, period,
entity, currency and explicit residual. Revenue/billings/cash are independent
quantities. Contract assets cannot be ordinary AR. Contract-net balances require
asset/liability sign handling and no cross-contract netting.

DSO must define numerator, denominator, days, period convention, and version.
Attack mixed current closing AR with prior revenue; zero denominator; negative
revenue; prior definition different from current; prior/current differing day
conventions; budget replacing actual; unverifiable management explanation;
FX residual embedded in collection driver; manual release double-counted;
statistical contribution described as causal proof. Rates and accounting
allowances remain ECL-owned; recognized revenue remains Revenue-owned.

## End-to-end acceptance attacks

1. Equal missing and duplicate invoice net-zero population: source count/event
   matching must detect gross exceptions despite GL tie.
2. Original due date changed to promise-to-pay date: ageing must fail.
3. Duplicate bank ID and duplicate differently named receipt: economic ID and
   bank completeness must both prevent double application.
4. Unapplied cash excluded from cash receipts or transferred to revenue: reject.
5. Credit counted in original billing and again as negative bridge component:
   reject or expose residual.
6. Deferred release counted in both recognition and manual accounting journal:
   single governed recognition; duplicate adjustment rejected.
7. Open reconciliation plus completed checklist: retain both sources; do not
   certify complete close. Net-zero exceptions remain visible.
8. Late journal approval versus effective date and period reopen: both dates and
   lock history independently matter; late status cannot silently disappear.
9. Stale/wrong-period Revenue, AR, ECL, FX, FS or Disclosure result: downstream
   invalidation and public partial/blocked outcome.
10. Disclosure selected without scoped material need, or excluded despite
    material supported reporting requirement: independently justify selection.
11. Narrow AR balance/revenue schedule/ECL allowance requests: avoid full-close
    invocation while retaining genuinely required evidence dependencies.
12. Public output contains reviewer, raw text, fingerprint, hashes, skill IDs or
    internal source status: reject; useful limitations/conflicts remain.
13. Management 'collections worsened only because revenue grew': tested against
    billed rights, receipts, ageing and FX; conclusion not accepted by wording.
14. Economic deterioration labelled accounting error, or unsupported accounting
    release labelled growth: final synthesis preserves both classes.
15. Three final quantitative conclusions traced to source rows, one crossing
    multiple owners, with no orphan binding or stale fingerprint.
16. Durable DSO/materiality/policy context is candidate only; no promotion.
17. Unavailable skills fail closed; no Government Grants/Borrowing Costs/
    Investment Property execution or unrelated flagship work.
18. Every bridge failure exposes an explicit residual; no balancing plug or
    unexplained 'other' amount used to certify cleanliness.
19. Final mix of clean, explained, accounting, data/control and open items cannot
    collapse into 'clean' when a material unresolved item survives.

## Independent execution protocol

After author fixtures exist, derive executable mutations against those actual
interfaces. Findings require reproducer, remediation and independent rerun.
Version/fingerprint artifacts must be regenerated after changed production
bytes. Baseline diagnostic tests remain reproduction-only until superseded by
positive acceptance regressions. Final acceptance must be against immutable
candidate head, with earlier flagship and full repository regression evidence.

## Executable implementation review (independent)

Authored `tests/test_saas_acceptance_independent.py` against actual source,
intake, owner workpapers, runtime allocation and Analytics interfaces. Tests
requalify mutated owner workpapers externally where appropriate so failures
exercise real semantic/contract boundaries rather than merely stale hashes.

Findings and reproducers:

- **QA-S01, rate freshness:** the fixture originally carried a
  `loss_rate_review` object unused by implementation. Re-certified ECL with a
  2020 review still completed. Runtime now qualifies current as-of, effective
  period, independently supplied review rows/version and bucket exposure to AR.
  `test_stale_loss_rate_table_is_rejected` and
  `test_unreviewed_loss_rate_table_is_rejected` independently pass after repair.
- **QA-S02, malformed dates:** the first qualification used lexical comparisons;
  `effective_from=0000-not-a-date` and `reviewed_on=2026-12-99` both survived.
  `test_malformed_loss_rate_dates_are_rejected` reproduced both failures. Strict
  ISO parsing remediation independently reran green.
- **QA-S03, original invoice due-date lineage:** changing raw billing
  old-domestic due date from 2026-11-01 to 2026-12-30 still produced a completed
  AR owner with unchanged 31–60 exposure of 720 because dates were hardcoded in
  qualification and only amounts were mapped. Reproducer
  `test_changed_original_due_date_cannot_reuse_hardcoded_owner` initially failed.
  This requires explicit extracted-date to reviewed-owner bindings; merely
  hardcoding the same date in another fixture field does not remediate it.

Independent run before adding QA-S03: 31 acceptance methods plus 5 updated
architecture boundary/regression methods passed (36 distinct tests). QA-S03 adds
one acceptance method and remains pending remediation at this checkpoint.

Coverage includes source conflicts, invoice/billing/cash distinction, duplicate
bank receipts, unapplied cash, original foreign amount/currency, FX item/source
result freshness, customer totals, framework ECL routing, rate freshness and
bucket evidence, exact-payload journal review, atom omission/duplicate/split
mismatch, entity/period/currency, source input binding, late journal and reopen,
close tasks, public privacy, excluded owners, narrow revenue, DSO definition,
actual versus budget, accounting authority metric attribution, bridge residuals,
management hypothesis, stale reporting and executable multi-owner lineage.

### Remediation rerun checkpoint

QA-S03 is remediated: extracted original invoice dates, currencies, customer,
opening status and foreign amount bind to reviewed owner fields. A changed source
due date can no longer reuse the old qualified AR result. Generic independently
supplied `PopulationBinding` proves exact original invoice-ID and bank-ID
populations. New attacks cover extra source invoice, duplicate invoice ID,
omitted owner invoice and duplicate bank source row; all reject before execution.

Fixture-realism concern is also resolved: the contract is an API-processing
service series with output progress. October 600 + November 400 + December 500
units = 1500/12000 = 0.125. At USD1 per contracted processing unit, opening
cumulative USD1000 plus December USD500 reconciles to cumulative USD1500.
No ordinary stand-ready time-elapsed annual contract is implied.

Independent final checkpoint command:

```
python -m unittest orchestration.tests.test_saas_acceptance_independent orchestration.tests.test_saas_architecture_independent -q
```

Result: **41 distinct methods passed** (36 acceptance +5 architecture boundary
methods), 15.241 seconds. AR-only selects AR+necessary foreign-receivable FX;
ECL-only selects ECL+AR+necessary FX. Neither routes the full close.
QA-S01, QA-S02 and QA-S03 now have executable regression coverage and independent
successful reruns. This checkpoint is local reviewer evidence, not exact-head CI
certification; final immutable-head regression and CI remain author/integration
gates. Review does not claim generic unreviewed user contracts or automatic
qualification outside the supported controlled-fixture boundary.

### Owner-result binding follow-up

Authored five additional acceptance methods for the generic `owner_result`
binding: source billing/cash substituted for recognised revenue; incorrect
producer metric path; prior actual used as current result; stale owner
qualification; and a colluding wrong numeric source plus wrong metric path.

**QA-S04, semantic result-path authority:** the first four controls reject, but
changing source period revenue from 500 to 800 and binding its
`recognised_revenue` fact to Revenue `contract_bridge.billings` accepts billing
as recognition. Numeric equality plus correct owner identity is insufficient;
the semantic fact role must govern the permitted producer calculation path.
Executable reproducer:
`test_owner_result_billing_metric_cannot_masquerade_as_revenue`.
This finding was sent to the implementation author and requires remediation and
independent rerun. Result comparison must continue executing the actual qualified
owner rather than trusting caller-provided output or permitting source overwrite.

### Final independent local acceptance rerun

QA-S04 is remediated by an explicit family/attribute → governed producer and
calculation-path contract. `customer_contract.recognised_revenue` binds only
Revenue `period_revenue`; a reviewed billing result or numerical equality cannot
substitute. Independent wrong-source/wrong-path reproducer now rejects.

Reran both independent modules after this repair: **46 distinct methods passed**
(41 acceptance +5 architecture), **18.951 seconds**. All four substantive
findings QA-S01–QA-S04 have documented reproducers, remediation and successful
independent reruns. No production accounting package or evidence gate was
modified by the independent reviewer. This is final local acceptance evidence;
repository-wide exact final-head regression and CI remain integration gates.

### Final fixture/artifact integration rerun

After journal-date/ID and task-status source bindings, journal population proof,
and gross reconciliation movements were added, independently reran the same
**46 distinct methods: all passed in 21.742 seconds**. Inspected regenerated
38-file `examples/saas-close` pack: three material lineage records connect
Revenue500, closing AR1520 and contract-net liability−1300 through actual owner
results to FS/reconciliation consumers and extracted source facts. The final
Case and public artifact both remain partial for unresolved source conflicts.
The nine actual owners exclude irrelevant specialist packages; close-review is
primary with diagnostic analytics and reconciliation investigation secondary.
All seven public economic-event journals balance. Public artifact scan found no
case/payload fingerprints, reviewer identities, SKILL IDs or FX import routing
IDs. Scoped monthly reporting/disclosure states no external certification.
No further substantive findings in this final fixture/artifact check.
