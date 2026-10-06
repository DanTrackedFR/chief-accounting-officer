# Group Accounting integration handoff

Base reconstructed from live main after Treasury PR #32: `92a784881cf77d0fd889ee8fa064ccccfd62cf9f`. One branch `orchestration/group-accounting-flagship`, one PR #33. Integration review and merge belong to the owner; this work does not merge.

## Governed execution

Natural year-end group request + company-shaped CSV/Markdown source pack → existing inert inventory/extraction → transformations and entity-aware Fact Candidates → source conflicts/material questions → validated semantic proposal/work modes → separate ReviewedInputPack → existing governed planner/CAO graph → current native production owners → scoped assembly/challenge → Analytics accounting recheck and FS/Disclosure → one `public_record` answer.

The source conflict Case is **partial / DOCUMENTED**: Parent IC ledger claims EUR105 versus reviewed reciprocal EUR100. Both sources remain preserved; residual EUR5 is visible; no plug, silent preference or clean-close claim is made. The independently qualified EUR100 population supports provisional workpapers only. The corrected source version reaches **complete / CLOSED** through the same architecture.

Nine actual production owners run, plus the existing bounded FS diagnostic recheck. Business Combinations owns PPA and initial NCI. Tax determines acquisition DTL from supplied bases/rates. FX owns foreign-operation translation. Intercompany reconciles both legal books. Impairment consumes supplied valuation and actual translated goodwill. Consolidation consumes their current completed results, controls the perimeter, eliminates investment/equity and bilateral balances, attributes NCI and assembles the Group. FS consumes the actual consolidated population, NCI profit/OCI/closing balances; Disclosure prepares five scoped current statement notes. Analytics explains actual contribution and rejects management's full-year claim, escalating the accounting check to FS.

## Quantitative acceptance (source units)

Acquisition USD: consideration800 + full-goodwill NCI200 − identifiable assets1000 + liabilities225 = goodwill225. Liabilities include acquisition DTL25, determined once from land FV100, tax base0 and supplied rate25%. Ordinary rights/control evidence is supplied separately from 80% ownership. Only July–December revenue250 less expense150 = post-acquisition profit100 is included; the complete full-year source profit250 remains preserved.

EUR: translated post-acquisition profit85; opening foreign-operation net assets900 + profit85 − CTA105 = closing880. Acquisition goodwill202.5 − currency movement22.5 − supported nil impairment = goodwill180. NCI180 + post-profit17 − OCI21 = closing176. Parent standalone profit200 + qualified Subsidiary85 = Group285; the IC loan balance elimination does not affect performance. Equity2000 + profit285 − OCI105 + acquisition NCI180 =2360. Assets2540 − liabilities180 =2360. Closing deferred tax20 reflects translation of the actual acquisition DTL. No acquisition amortization, inventory profit elimination or elimination tax effect is fabricated for this loan/land fixture.

The independently supplied valuation workpaper includes FV less disposal costs900, one supplied valuation cash flow990, discount rate10%, terminal0, carrying goodwill180/other net assets700 and unit identity. Native Impairment computes recoverable900, headroom20, loss0. The CAO does not generate valuation inputs or forecasts. Management's claimed full-year contribution EUR212.5 is rejected against actual supported post-acquisition EUR85.

## Ownership, source qualification and limits

Explicit source/entity/group/currency/period dimensions survive intake and receipts. Source TB account identities and complete values are bound; pre/post windows reconcile to full-year source balances. Reviewed documentary assertions bind signed completion, consideration/NCI/ownership, valuation, election and functional currency. Complete reviewed SPA coverage blocks unknown earnout/prior-interest clauses. Synthetic fixture reviewers are not authenticated approvals.

PPA/Tax/CTA journals already embedded in qualified source populations remain witnessed evidence. Consolidation's native Group adjustments are the only posting pack and replay to every consolidated account. Gross-line event allocation is the inherited exact-once architecture; aliases cannot evade it. Native IC local-book mechanics never post the Group elimination. No general legal-book posting, arbitrary entity graph, multi-period runtime, local/group framework conversion, positive impairment integrated posting or partial-goodwill integrated route is claimed. See `GROUP-TO-MULTI-ENTITY-HANDOFF.md` and `interfaces/scoped-owner-receipts.md`.

Only one specialist modification was needed: Foreign Currency **SKILL-FX-001 1.0.1** permits an empty monetary-item list when foreign-operation translation is explicitly enabled. The prior nonempty gate forced a fabricated zero transaction in a genuine translation-only case. No rate, translation, framework, evidence or certification gate was loosened. Independent native tests cover enabled/disabled translation and incorrect empty-list shape. All global fingerprint-sensitive embedded fixture certificates are regenerated through existing governed generators.

Four separately reviewed natural-source controls invoke only the relevant specialist (acquisition, bilateral IC, foreign-operation translation, impairment), using already qualified specialist source evidence. They do not claim the whole Group close or silently waive required dependencies inside the flagship.

## Reproduction and gates

- `python -m orchestration.tests.generate_group_examples` writes the controlled source pack, intake ledgers, proposal, candidates, conflicts/questions, reviewed bindings, specialist results/handoffs, acquisition/NCI/CTA/IC/goodwill/tax/equity/profit/assembly bridges, execution/event ledgers, five executable lineages, challenge, internal Case and curated conflict/clean answers in `orchestration/examples/group-accounting/`.
- `python -m unittest orchestration.tests.test_group` runs authored acceptance and determinism controls.
- `python -m unittest orchestration.tests.test_group_independent` runs fresh independent adversarial regressions. `GROUP-ARCHITECTURE-INDEPENDENT-QA.md` records discoveries, executable reproductions, remediations and independent reruns across all 25 challenge categories. Historical failed runs remain an audit trail, superseded only by explicit final acceptance.
- Full orchestration, shared production skills, leases, public/canonical tests, every supplemental knowledge suite, standards-evidence/approval validators and whitespace gates passed locally. `GROUP-REGRESSION-RESULTS.md` records 2,072 distinct tests. Exact-head Actions are reported in the PR, not cumulative rerun counts. `python -m orchestration.tests.update_roadmap_baseline` regenerates only the authorized roadmap documentation witness while rejecting any unrelated protected-document drift; no accounting baseline is reset.

Government Grants PR #27/package, Borrowing Costs and Investment Property remain untouched. Source/code absence of those owner dependencies remains fail-closed. Memory observations remain candidates and are never automatically promoted.

Roadmap completion is gated on all substantive acceptance and regression checks. Multi-entity / multi-period orchestration remains the next workstream; this controlled proof does not complete it. Exact-head GitHub Actions must pass after the final repository change before PR #33 becomes ready. If any file changes afterward, that CI evidence is stale and must be rerun.
