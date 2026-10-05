# Treasury / Financing integration handoff

## Live baseline and delivery

Repository: DanTrackedFR/chief-accounting-officer. Branch: `orchestration/treasury-financing-flagship`. PR: #32. Baseline live main: `a8e11237fbbfa0daeff74f47c75eae52b430c855`. SaaS PR #31 was merged and its semantic adapters, reviewed owner-result bindings, exact-once journal ownership, reporting handoffs and scoped synthesis were verified before branch creation. See TREASURY-ARCHITECTURE-RECONSTRUCTION.md. The PR remains unmerged. Exact candidate SHA and CI run links are recorded in the PR metadata, avoiding a self-referential committed SHA.

## Architecture and authority

Existing intake, GovernedPlanner, registry, CAO runtime, challenge and public_record are reused. Generic additions comprise debt/cash fact-family preparation, exact native list-row owner references, whole-document source qualification, explicit Debt/Hedge/Cash reporting semantics, bounded debt-plus-FX composition, and bank-origin economic event identity tied to the actual cash population. No second planner, Treasury runtime or journal deduplication engine exists.

Analytics SKILL-ANALYTICS-001 moves from 1.2.0 to 1.2.1 for native list-row owner references; its existing source/owner flux and rate/quantity methods remain unchanged. Debt 1.0.0, FX 1.0.0, Hedge 1.0.0, Cash Flow 1.0.1 and Financial Statements 1.0.0 retain accounting methods and authority. Fingerprint-sensitive existing examples were regenerated after the shared reference helper changed; unrelated accounting conclusions were not expanded.

## Source and semantic flow

The user supplies a natural December month-end request covering annual YTD Treasury activity, with 18 raw-ish documents: lender/debt terms/schedule/payment support, FX report, derivative confirmation, external valuation, designation/effectiveness workpapers, bank activity/summary, TB, cash-flow support, reconciliation, policy, P&L, prior-period comparator and management commentary. Intake produces inventory, extraction/transformation ledgers, candidates, proposal, conflicts/material questions and owner-input candidates. Controlled synthetic independent reviewer scaffolding prepares ReviewedInputPack; runtime never certifies sources or manufactures approval. Sixty-four field bindings plus whole-document/metadata bindings and cash-population qualification connect source data to native owner inputs/results.

Primary mode: RECONCILIATION_INVESTIGATION. Secondary modes are DIAGNOSTIC_ANALYTICS and CLOSE_REVIEW; supporting modes are ACCOUNTING_DETERMINATION and REPORTING, derived from actual issues. Selected owners: Debt, FX, Derivatives/Hedge, Cash Flow, Reconciliations, Financial Statements and Analytics. Native Debt reruns supporting Analytics do not count as additional owners. ECL, Fair Value, Disclosure and Close are absent because facts do not require their executable scope. Inventory, Agriculture, Insurance, Revenue, AR, Payroll, Business Combinations, Consolidation, Grants, Borrowing Costs and Investment Property are excluded. Narrow controls select Debt only; FX only; Hedge plus its Debt source dependency; Cash plus Debt/FX. Genuine qualifying-asset interest identifies unavailable Borrowing Costs and fails closed.

## Governed quantitative results (EUR)

| Result | Amount / treatment |
|---|---|
| Debt opening | 1,000 (USD 1,000 at opening EUR/USD 1.00) |
| Debt interest / cash interest | 80 / 80 |
| Principal repayment | 200, financing cash |
| Debt base closing before FX | 800 |
| FX remeasurement | 80 loss; USD 800 at 1.10 becomes EUR 880 |
| Debt reported closing | 880, current 880 / noncurrent 0, evidenced reporting-date rights and actual maturity |
| Prior/current annual interest | 60 / 80; rate effect +20, volume effect 0, residual 0 |
| Externally valued derivative | Asset 40; designated benchmark-rate risk, not loan FX risk |
| Hedge allocation | Effective 36 OCI, ineffective 4 earnings gain, closing reserve 36 |
| Cash opening / closing | 2,000 / 1,720 |
| Operating / investing / financing / cash FX | -80 / 0 / -200 / 0 |
| Profit / OCI | -156 / +36 |

Debt bridge: 1,000 +80 accrual -80 cash interest -200 principal +80 FX =880; residual zero. Interest bridge: 60 +20 rate +0 volume =80, residual zero. Cash bridge: 2,000 -80 operating -200 financing =1,720, residual zero. Noncash FX loss80, derivative FV40 and OCI36 are not cash. Cash-flow movement differs from debt movement because recognition/remeasurement and cash settlement have distinct governed economics. No plug exists.

The floating loan uses supplied independently reviewed reset/EIR cashflows, not nominal-rate substitution or an internally forecast floating-rate yield. Subsequent resets need a fresh reviewed owner schedule. No draws or fees occur in the main case; permanent native boundary controls cover funded draw/fee ownership and standalone derivative settlement. No modification/extinguishment, waiver or refinancing right is inferred. Approved pre-2027 IAS7 interest policy classifies paid interest operating.

Hedge consumes qualified external valuation and designated-risk effectiveness evidence; it does not build curves or value instruments. Fair Value and Financial Instruments/ECL are not invoked. The generic Hedge-to-FS adapter is explicitly limited to first-year continuing cash-flow hedges with zero opening derivative/reserve and no settlement, recycling or basis adjustment, preserving the native adapter boundary. Native specialist settlement capabilities do not imply unsupported integrated reporting support.

## Exceptions, challenge and final answer

Primary sources preserve cash-flow support financing0 versus bank financing-200. Material question: resolve the omitted repayment and approve corrected support. Reconciliations/owner calculations are qualified, but this source conflict keeps the primary Case PARTIAL / DOCUMENTED. Clean-source control corrects the support to -200 and reaches COMPLETE / CLOSED. Missing rights, stale results, incorrect dimensions, mismatched source evidence, material residuals and unsupported accounting dependencies remain blocking/partial as appropriate.

Management's rate explanation for interest is supported by the owner-bound quantitative bridge. Its claim that the hedge offsets almost all FX loss is REJECTED: the instrument designates benchmark-interest risk and its earnings gain4 does not explain FX loss80. Synthesis distinguishes economic rate/volume drivers, accounting FX/FV/OCI, actual cash flows and close-process exceptions. Accounting escalation retains unresolved evidence instead of changing owner conclusions. Company currency/policy/KPI context remains PROPOSED memory, never promoted automatically.

The public answer is a single CAO synthesis. All seven public routes use public_record and are tested against raw documents, reviewer identities, source notes, tiers, hashes, fingerprints, routing IDs and confidence internals. Material limitations, reconciliation exceptions and meaningful source descriptions survive.

## Exact-once and executable lineage

Six controlled events: interest accrual, principal repayment, interest payment, FX remeasurement, hedge earnings and hedge OCI. Debt's principal repayment posts once; FX's matching settlement remains a visible evidence witness. Bank-origin identity is independent of event/owner/account/nature aliases and must tie the actual Cash Flow source population. Native journal atoms, payload review and ownership are retained. Aliased repayments/settlements/interest, disguised FX, duplicate FV/reserve postings and account renaming fail closed.

Four executable material lineages are saved: lender/debt source -> Debt -> composed FX handoff -> FS closing debt; currency/rates -> FX -> FS/diagnostics; external valuation/designation/effectiveness -> Hedge -> FS; bank -> Cash Flow -> financing cash reporting. Equal totals alone cannot authorize a semantic handoff.

## Independent QA and regression

TREASURY-INDEPENDENT-QA.md documents independently reconstructed attacks and permanent executable reproductions. Remediated findings cover unbound critical source fields, inherited commodity/forward prose, bank event aliases under separately reviewed balanced payloads, and the explicit first-year reporting boundary. Independent reruns include native draw and derivative settlement controls. Authored, independent, intake/semantic/runtime, exact-once, public privacy and deterministic hash-seed tests are included in orchestration discovery. Final distinct repository total: 2,011 tests (360 orchestration including 28 authored Treasury and 52 independent Treasury; 1,180 shared production; 471 repository/lease/supplemental/independent knowledge). Repeated runs and eight exploratory scratch checks are not added. Seven validators and git diff --check pass. The PR records exact-head CI status.

Existing SaaS, manufacturing, diagnostics, intake and base orchestration regressions are retained. Shared production, lease, repository/canonical/privacy, all supplemental and independent knowledge suites and seven validators run. Canonical topics/mappings/claims and supplemental authority remain invariant. The insurance protected-roadmap baseline hash changes only for the explicitly requested roadmap update; other protected-document hashes remain intact.

## Artifacts and preservation

`examples/treasury-financing/` contains deterministic sources, inventory, extraction, transformations, semantic proposal/modes, candidates, conflicts/questions, source/owner/document/population bindings, issues/workplan/execution, handoffs, exact-once ledger, debt/interest/FX/derivative/effectiveness/reserve/cash/financing/noncash/classification bridges, reconciliations, reporting, hypothesis, diagnostics, escalation/challenge, internal/public Cases, clean control, memory and executable lineage. Reproduce with `python -m orchestration.tests.generate_treasury_examples`.

Roadmap marks SaaS and Treasury COMPLETE and Group NEXT; the additional flagship section remains open. Government Grants PR #27 and its package are untouched. Borrowing Costs and Investment Property remain untouched/nonproduction. No Group Accounting work or separate multi-entity/multi-period project was started. No PR is merged.
