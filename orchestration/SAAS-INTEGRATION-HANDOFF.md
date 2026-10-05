# SaaS / month-end close integration handoff

Branch: `orchestration/saas-close-flagship`; PR #31, no merge.
Live baseline main: `2700b3dd7c8cb43c21ff874ef44bd0832e73b351` (reverified through GitHub).
The immutable candidate SHA and its Actions runs are recorded on the PR after
publication. PR readiness requires successful CI on that exact head; any later
repository edit invalidates that gate.

## Architecture and scope

This is the first Additional End-to-End Flagship, not a new accounting skill.
The live architecture reconstruction is in `SAAS-ARCHITECTURE-RECONSTRUCTION.md`.
The original five gap reproducers and final independent acceptance review are in
`SAAS-ARCHITECTURE-INDEPENDENT-QA.md` and `SAAS-ACCEPTANCE-INDEPENDENT-QA.md`.

The existing flow remains:

Natural request → controlled company exports → inventory/extraction → explicit
transformations → Fact Candidates/conflicts → validated semantic proposal →
material questions → separately reviewed owner input pack → GovernedPlanner →
existing CAO runtime → production owners → diagnostic accounting recheck →
challenge → one curated public conclusion.

No SaaS objective dispatcher, parallel engine, analytics package, persistence,
authentication, UI or deployment was created. A structured fixture proposer
simulates the existing SemanticPlanner interface; live model inference and
automatic qualification of company workpapers remain outside this foundation.
The user supplies a natural request and company-shaped sources, never internal
skill IDs, work modes, fact adapters, owner cases or accounting conclusions.

Generic integration changes:

- Receivable-population and credit-exposure semantic fact families.
- Controlled tabular source identity, ISO-date and explicit boolean facts;
  source fact establishment never certifies accounting reliability.
- Reviewed source population bindings compare invoice IDs, bank IDs and journal
  IDs against actual owner populations, detecting omission and duplication.
- Reviewed owner-result bindings validate an explicit semantic producer/path
  contract before comparing source claims with qualified owner calculations.
  An equal billing or receipt amount cannot substitute recognized revenue.
- Prior-actual balance diagnostic bindings retain actual/comparator dimensions.
- AR/ECL, AR/FS/REC, Revenue/FS/REC and FX/FS governed handoffs, including allowance
  contra-asset and contract-balance classification checks.
- Exact-case reviewed journal economic-event ownership: native implications are
  retained as primary/witness evidence, mapped gross Dr/Cr vectors must agree,
  and every native line is consumed exactly once. Split bank receipts preserve
  unapplied cash; public postings are balanced event journals. Unqualified
  duplicates still fail closed.
- Cross-owner ECL exposure/bucket reconciliation and current reviewed loss-rate
  evidence qualification. Strict ISO dates, period/as-of, version, reviewed rows
  and AR ageing must agree; runtime never supplies rates or reviewer approval.
- Close observations distinguish economic effective date, approval date and
  posting date, and retain authorized reopening/reclosure.
- One balance-review public narrative and scoped reporting, without raw sources,
  reviewers, hashes, evidence statuses or internal routing identifiers.

## Production changes

| Existing package | Final version | Precise change |
|---|---|---|
| Accounts Receivable | 1.1.0 | Optional independently reviewed FX monetary-item import, tied to original invoice currency, foreign amount, date and carried book amount; settlement and remaining position reconcile to FX owner results |
| Month-End Close | 1.0.1 | Reopened periods require nonblank authorization and reclose evidence |
| Management Accounting Analytics | 1.2.0 | Reviewed prior-calendar-month balance diagnostics over exact governed Revenue/AR/ECL/FX results, disjoint movement bridges, ageing, collection indicators and owner escalation |

Revenue, ECL, FX, Reconciliation, Financial Statements and Disclosure accounting
contracts are unchanged. No evidence gate or exact-case fingerprint was loosened.
Independent acceptance exercises the native changes as well as orchestration;
`skills/tests/test_saas_owner_integration.py` additionally covers foreign
settlement with remaining remeasurement and the Close defect.
Fingerprint-sensitive existing examples are regenerated through their existing
generators; this is not substantive expansion of unrelated accounting packages.

## Controlled company pack and semantic intake

`tests/saas_fixtures.py` supplies 21 CSV/JSON/Markdown company exports: current and
prior TB, P&L, balance sheet, billing, receipts, customer ledger/control totals,
ageing, revenue schedule, one customer contract excerpt, contract balances,
reviewed loss-rate table, allowance schedule, FX report, close checklist,
reconciliation pack, posted journals, prior management actuals, commentary and
monthly disclosure scope. Amounts are synthetic USD; one original EUR right is
preserved. The one hosted API service series has fixed consideration 12,000 for
12,000 processing units; October/November/December delivery is 600/400/500 units.
December cumulative progress is 1,500/12,000, not an invented time-elapsed ratio.

The execution yields 79 Fact Candidates, 71 exact source bindings, three source
population checks, nine owner-input candidates, two preserved conflicts and two
material questions. Contract wording remains source evidence requiring separate
reviewed qualification; the runtime does not certify prose automatically.

Primary mode is CLOSE_REVIEW. Secondary modes are DIAGNOSTIC_ANALYTICS and
RECONCILIATION_INVESTIGATION; ACCOUNTING_DETERMINATION and REPORTING support the
actual accounting and presentation questions. No gratuitous control/system owner
is selected for a source contradiction alone.

Selected owners: Revenue Recognition; AR & Collections; ECL; FX; Reconciliation;
Close; Financial Statements; Disclosure; Analytics. The diagnostic allowance
question reruns the existing ECL owner, not a new owner or autonomous estimate.

Inventory, Agriculture, Insurance, Derivatives/Hedge, Business Combinations,
Consolidation, Defined Benefit and the three unavailable owners are excluded:
the source pack contains no supporting inventory, biological, insurance, hedge,
acquisition, group, pension, grant, construction-financing or investment-property
facts. Narrow Revenue selects only Revenue; AR selects AR plus its actual FX
position; ECL selects ECL plus AR/FX exposure evidence, not the entire close.

## Governed results and CAO interpretation

| Measure | Result |
|---|---|
| Recognized December revenue | 500, compared with November 400 |
| Enforceable current billings | 800, compared with prior net billings 500 |
| Bank collections | 250, compared with prior 450; applied 200, unapplied 50 |
| Gross billed AR | 910 + 800 − 200 + 10 FX = 1,520; residual 0 |
| AR ageing | Current 800; 31–60 days 720; original due dates retained |
| Contract liability | 1,000 + 800 billings − 500 recognition = 1,300; residual 0 |
| Contract asset | 0; never included in ordinary billed AR |
| ECL allowance | 20 + 60 expense = 80; residual 0 |
| Reviewed lifetime rates | Current exposure 800 × 1%; aged exposure 720 × 10%; no invented inputs |
| Original foreign right | EUR 100; opening book 110, closing book 120, FX gain 10 |
| Late manual accrual | 25; effective December 31, approved/posted January 2; supported cutoff |
| Current reporting | Revenue 500, gross AR 1,520, contra-allowance 80, liability 1,300; profit 425; cash 5,250 |
| Cash flow | Operating increase 250; gross movements and noncash FX separated |

The actual reconciliation workpapers carry gross reviewed movements, including
AR additions 810 and reductions 200; liability additions 500 and reductions 800;
allowance reduction 60. They do not plug unexplained differences. Owner outputs
are tied to actual current GL/TB and statements. The scoped monthly credit-loss
note consumes completed ECL and Financial Statements results; it is not a universal
disclosure checklist or external compliance certification.

The supplied ageing summary says 1,515 while the GL/control and detailed buckets
say 1,520. The checklist says no open reconciliation difference while the supplied
reconciliation summary says 5. Both evidence pairs remain preserved. Questions
ask to resolve ageing completeness and the open reconciliation difference, not
to select a skill or repeat information already supplied.

The final Case is PARTIAL / DOCUMENTED, never CLOSED as clean. Governed accounting
workpapers reconcile; late accrual/reopening are explained exceptions; the
summary contradictions are open data/control issues requiring the complete
export and supported disposition. A clean-source control completes the same
flow without conflicts. No accounting adjustment is manufactured to absorb 5.

Economic observations are lower absolute collections, older unpaid invoices,
increased billed rights and foreign exposure. Customer payment causes remain
unresolved. Accounting effects are recognition, liability release, allowance
expense and remeasurement. Close/process effects are the late approved accrual,
authorized reopen and contradictory summary controls. Management's hypothesis
that collection performance only appears worse because revenue grew is REJECTED:
cash receipts actually declined. This does not establish an invented customer
causal explanation. The allowance question is resolved by the fresh governed
ECL workpaper; Analytics never determines the allowance.

Collection ratio is bank receipts/net billings = 250/800 = 31.25%.
Bounded snapshot collection days are:

`ending gross billed AR / period net billings × actual calendar days`

Current: 1,520/800×31 = 58.90; prior: 910/500×30 = 54.60.
The numerator, denominator, day convention, actual source lineage and definition
are explicit and stable. This is not rolling or revenue-based DSO, and annual
billing timing affects comparability. It is not automatically company policy.
Company currency/context observations and other durable candidates remain
proposals only; no memory promotion occurs.

## Lineage, artifacts and unsupported scope

38 deterministic JSON artifacts live in `examples/saas-close/`. Reproduce with
`python -m orchestration.tests.generate_saas_examples`; the authored artifact
test checks the entire saved population. Artifacts include raw sources,
inventory/extraction/transforms, proposal/modes/facts/conflicts/questions,
owner-input candidates/bindings/populations, issues/graph/execution/handoffs,
journal ownership, all quantitative bridges, close cleanliness/exceptions,
reconciliation/reporting/disclosure, diagnostics/escalation/challenge, internal
Case/public answer, hypotheses, memory candidates and executable lineage.

Three material lineage checks traverse:

- Revenue output progress source row → reviewed Revenue input → recognized
  revenue → Financial Statements handoff → final revenue conclusion.
- Bank application row → AR allocation/right population → closing AR →
  Financial Statements handoff and Analytics AR bridge → public AR conclusion.
- Contract billing row → reviewed Revenue input → signed contract closing
  balance → Reconciliation handoff and diagnostic bridge → final liability.

Supported analytical scope is actual prior-month revenue/net-billings/cash,
gross AR/ageing, signed single-contract asset/liability, allowance rollforward,
reviewed receivable FX, unapplied cash, explicit residuals and bounded snapshot
collection days. This is not generic BI, forecasting, budgets or universal KPIs.
No unsupported commercial causal driver is invented. Multi-contract offsets,
multi-entity/multi-period owner execution, general FX attribution, foreign
invoice credits/deposit applications, unreviewed credit scenarios/rates,
arbitrary DSO definitions, restatement, external filing certification, native
binary-document parsing and autonomous workpaper approval remain unsupported.
These mechanisms require actual qualified contracts; unavailable owners fail
closed. Treasury and Group Accounting scenarios are not implemented.

## Acceptance and preservation

Independent review used a separate agent/context that reconstructed contracts and
derived adversarial tests. Four substantive findings each have executable
reproducers, remediation and independent reruns: stale/unreviewed loss-rate
evidence; malformed dates; omitted original due-date lineage; billing metric
substitution through owner-result bindings. See the independent QA document for
the exact tests. Authored tests additionally exercise clean/partial controls,
narrow routing, source mutations, owner gates, journals, close/reconciliation,
DSO, memory and public boundaries. No finding is left intentionally unremediated.

Full repository regression includes prior manufacturing, factory diagnostic and
semantic/intake artifacts, all production/lease suites, public/canonical tests,
every supplemental suite, canonical approval and standards-evidence validators,
and `git diff --check`. Final local regression: 1,931 distinct tests: orchestration 280; production skills
1,180; repository 53; lease 17; income-tax supplement 10; agriculture 12 plus
71 independent; insurance 35; hedge 4 plus 7 independent; inventory 262. All
passed. The seven validators and whitespace check passed. Prior flagships and
artifact reproduction passed. Exact-head workflow links are recorded on the PR;
repeated local/CI runs are not extra tests.

The roadmap marks only SaaS / month-end close COMPLETE. The Additional Flagships
workstream remains open and Treasury / Financing remains next. Insurance's
protected baseline refresh changes only the intentional roadmap hash; all other
protected entries and metadata are preserved. Canonical/supplemental knowledge
and approval invariants are unchanged. Government Grants PR #27, Borrowing Costs
and Investment Property are untouched. Do not merge this PR.
