# CAO Intent & Diagnostic Analytics Foundation — integration handoff

Branch: `orchestration/intent-diagnostic-analytics`. PR #29 targets main; do not merge.
Exact candidate SHA and CI evidence are recorded in the PR after final push. This
file avoids self-referential commit hashes.

## Architecture and governed execution

Built on live main `186b302877c1c63e4e5c224d846aefb032a378cf` after orchestration
PR #28. No second orchestrator or Analytics package was created. Read
`DIAGNOSTIC-ARCHITECTURE-RECONSTRUCTION.md` and `interfaces/diagnostic-contract.md`.

`Intent` preserves primary/secondary/supporting work modes and reasons, separate
from skill identity. Nine governed work modes are supported. Planner.interpret is
a clean semantic-planner extension interface; current interpretation is bounded
and deterministic. Registry/runtime retain production identity, availability,
actual owner dependencies, source approval, exact-once handoff, active challenge
and public-output authority. Narrow accounting, documentation and process work
avoid incidental diagnostic selection. Simple AP/inventory inquiries use the
bounded owner plus actual native imports, rather than a broad review graph.

Analytics remains **SKILL-ANALYTICS-001, version 1.1.0, production**. A materially
expanded optional diagnostic contract is in the existing workflow and release
review. Diagnostic implementation bytes join shared case fingerprints. Historical
flux, source reconciliation and reconciliation KPI behavior remain supported.
Regenerated examples are synthetic certificate updates, never real approvals.

Supported diagnostic methods: signed owner/source flux; rate/quantity with explicit
interaction convention; baseline-weighted PVM; current-versus-prior posted actual
and independently supplied budget/forecast/standard/target/approved baseline;
owner-bound material/labour/conversion/capacity component schedules; reconciled
GP/margin-point bridges; explicit residuals and supplied materiality/tolerance;
threshold observations and evidence-tested hypotheses. Comparative analytical
sources do not imply multi-period native graph execution. Journal/FX/write-down
movement may be analysed only when the supplied source and actual owner component
are present, disjoint and supported; missing adapters remain unresolved.

No autonomous budget/forecast generation, planning ownership, operating-plan
optimization, invented causes, generic BI, statistical causal inference, journal
posting or capitalization decision. Accounting authority remains in production
owners. No document/data intake, parser, email ingestion or persistence project.

## Method, hypothesis and accounting-question controls

Rate/quantity uses baseline-rate quantity effect, then current-quantity rate effect;
interaction belongs to rate. PVM uses baseline weighted-price total volume,
baseline-price mix and current-quantity price; all effects sum to the movement.
Margin points use GP contributions/current revenue and a separate denominator
effect, never a prior-revenue denominator silently applied to all drivers.

Every bridge retains starting/ending/change/driver/residual, dimension,
status/confidence and lineage. Original economic components are consumed once;
semantic owner metrics and multi-group native component allocations prevent
alias/relabel/omission attacks. Current accounting components tie to actual owner
results. Baseline discrepancies and omitted driver components remain explicit
residuals. Absolute tolerance is supplied in [0,.01]; unknown/material residuals
keep work partial. Immaterial residuals remain visible. Drivers never change to
plug a bridge; unsupported "timing" is not a method.

Hypothesis tests calculate SUPPORTED/PARTIALLY_SUPPORTED/REJECTED/UNRESOLVED.
Source evidence classifications must qualify the test: management explanations,
association and model hypotheses cannot become established operational causes.
Anomaly flags are observations/questions, not accounting errors.

Accounting questions bind issue/reason/owner/amount/result path/source evidence
and supplied materiality. Runtime expands the graph with bounded owner-recheck
nodes, reuses actual native owner work and invokes production.assess_case again.
A changed/unsupported owner remains open; no journals/economics are duplicated.
This path rechecks existing governed workpapers, rather than inventing a missing
new accounting treatment. Material unresolved diagnostic evidence keeps the
follow-up open. Valid partial bridges survive Case/public output; challenged
invalid diagnostic outputs cannot become explanations.

## Monthly manufacturing diagnostic flagship

User objective: “Our factory margins look terrible this month. Can you review the
close and figure out what’s going on?” No skill names supplied.

Current period: December 2026; comparative analytical actual: November 2026.
All current native workpapers have matching December dimensions and certification.
Machinery uses supplied units-of-production consumption, not annual depreciation
relabeled as monthly. Monthly control occurrence populations are reconciled.

Primary: DIAGNOSTIC_ANALYTICS. Supporting: RECONCILIATION_INVESTIGATION and
CLOSE_REVIEW. Automatically selected production owners: Fixed Assets; AP;
Employee Benefits/Payroll; FX; Inventory/Cost; Revenue; Financial Statements;
Balance Sheet Reconciliations; Month-End Close; Systems/Data Integrity;
Controls/ICFR; Disclosure Management; Management Reporting & Accounting Analytics.
Inventory's analytical question adds a follow-up recheck node, not a new skill.

Correctly excluded: Government Grants, Borrowing Costs, Investment Property,
Agriculture, Derivatives/Hedge, Insurance, Leases and unrelated specialist owners.
The imported FX purchase remains unsold stock, so it creates no extra margin FX
contribution. A real currency owner is selected for the input, without inventing a
cost-of-sales FX driver or double counting it in material price.

| Gross-profit bridge, USD | Signed contribution |
|---|---:|
| November gross profit | 15,000.00 |
| Sales volume | -16,666.67 |
| Product mix | -833.33 |
| Selling price | +7,500.00 |
| Material usage | -20.00 |
| Material price | 0.00 |
| Labour hours contribution | 0.00 |
| Labour rate | -160.00 |
| Identified remaining conversion-cost reduction | +3,876.00 |
| Fixed overhead capacity contribution | -20,000.00 |
| Fixed overhead spending contribution | -5,000.00 |
| Explicit residual | 0.00 |
| December gross profit | -16,304.00 |

Exact unrounded serialized contributions reconcile. Explained signed deterioration
is **31,304 USD, 100%**; explicit residual is zero. Revenue moves 50,000 → 40,000;
margin moves 30.00% → -40.76%, a **70.76 percentage-point deterioration**. The
percentage bridge separately retains its +7.50-point denominator contribution.

Economic bridge effects include volume/mix/price, material usage, labour rate and
identified allocated conversion-cost movement. Capacity/spending effects are mixed
economic/accounting attribution; they are not labelled accounting errors. There
is no supported write-down, cutoff correction, invented material inflation,
labour-efficiency cause or separate close adjustment in this dataset.

Current Inventory COGS 11,304 ties to source components: material120, labour2160,
variable overhead24 and absorbed fixed9000. Each diagnostic source component binds
the actual native production component and actual owner COGS/eligible-cost ratio.
Inventory independently supports **45,000 unallocated manufacturing expense**;
the 25,000 movement is analytically decomposed, while the accounting owner confirms
the current expense treatment and native entry. Analytics does not conclude that
any amount should be capitalized.

Actual native GL/statement journal mapping, stock reconciliation, interfaces,
control readiness and close workpapers pass. The clean synthetic scenario has no
unresolved data/close adjustment; observation flags still direct attention to
capacity evidence. Public answers preserve confidence and hypothesis limitations.
Real operational causation requires the relevant supplied direct evidence.

## Intent controls, QA and artifacts

Authored controls cover diagnostic, accounting determination, close, documentation,
process/control and simple inventory objectives over similar supplied facts.
A nonmanufacturing AP-supported expense bridge proves reusable methods without
factory-objective dispatch. Missing diagnostic data cannot yield a clean
"why" answer from technical accounting alone.

Independent context reviewed promoted 1.1.0 bytes and authored **32 adversarial
tests**. Seven substantive findings were remediated and executable-regressed:
economic aliases; hypothesis evidence relabel; sign/presentation integrity;
forced-zero residual; partial diagnostic suppression; impossible comparator dates
and uncaught date exceptions; native component-allocation omission. Independent
final rerun PASS. Full findings/hashes are in `DIAGNOSTIC-INDEPENDENT-QA.md`.

Generated artifacts include separate public answer, internal Case, graph, intent,
bridge with lineage/margin points, attribution ledger, hypotheses, accounting
questions, challenge and proposed memory candidates. Existing manufacturing
foundation artifacts and fingerprint-sensitive skill examples are regenerated.
No memory candidate is promoted to Company Context.

## Final gates

Local regression passed. Exact-head GitHub Actions on candidate
`143eb75aacf83d5e6357177a56ab07c7c70ac244` passed the assembled 120-test orchestration
suite and all remaining gates: integration run37243420989 and structural audit
run37243420987. Final publication repeats CI after the narrow roadmap completion
and protected roadmap-hash update. Final-head evidence is recorded in PR #29.

| Gate | Distinct tests | Result |
|---|---:|---|
| Existing orchestration foundation | 70 | PASS |
| New authored diagnostic/intent/generality | 17 | PASS |
| Independent diagnostic + protected-baseline maintenance | 32 | PASS |
| New diagnostic artifact reproduction | 1 | PASS |
| Full shared skills | 1176 | PASS |
| Repository/public/canonical | 53 | PASS |
| Lease vertical slice | 17 | PASS |
| Tax supplement | 10 | PASS |
| Agriculture supplement | 12 | PASS |
| Independent Agriculture claims | 71 | PASS |
| Insurance supplement/claims | 35 | PASS |
| Derivatives supplement | 4 | PASS |
| Independent Derivatives review | 7 | PASS |
| Inventory supplement/independent claims | 262 | PASS |
| Total distinct regression tests | 1767 | PASS |

Artifact reproduction also passes in fresh interpreters under hash seeds17 and31:
four tests per rerun including original and diagnostic artifacts. These repeated
runs are not added to distinct totals. All five supplemental validators, canonical
claims/approval validators and git diff --check pass. Exact-head CI evidence is
recorded in PR #29 after publication; the PR becomes ready only after final-head CI succeeds.

Roadmap: CAO Intent & Diagnostic Analytics Foundation is complete after all
candidate gates passed. Semantic Planner + Document/Data Intake remains future
work. Final docs do not change reviewed Analytics implementation bytes or artifacts.

One pre-existing live-main gate was reconciled: Insurance LIVE-BASELINE.json still
protected the roadmap hash from before the owner updated live main186b3028.
Only its protected roadmap hash is refreshed. The unchanged release test continues
to enforce exact bytes; independent regression additionally freezes all1100 other
protected entries and metadata. This does not change Insurance accounting or
knowledge authority.

## Preserved invariants and limitations

PR #27 and its Government Grants branch/package remain untouched. No substantive
Government Grants, Borrowing Costs or Investment Property changes. Canonical and
supplemental knowledge files remain byte-identical: 157 approved topics,
347 mappings,1598 canonical claims; Tax64, Agriculture66, Inventory228,
Derivatives100 and Insurance168 supplemental claims. All knowledge/approval/source
validators remain required. Historical protected architecture/orchestration.md is
unchanged; the executable extension is documented here.

Remaining: arbitrary semantic natural-language interpretation, ingestion,
additional supported owner combinations/metric bindings, multi-entity/multi-period
native execution, authenticated approvals, persistent memory and UI. Source and
comparator certification are supplied reviewed evidence, not independent
verification of a real company's data. No full FP&A or final-product claim.


## Existing practice knowledge audit

The existing frozen Analytics map covers TOPIC-08-008/CAO-08-016 statutory bridges,
TOPIC-02-008/CAO-02-017 flux/post-close, TOPIC-01-005/CAO-01-011 accounting metric
definitions and TOPIC-11-008/CAO-11-019–020 reporting-layer lineage. Their live mapped
practice documents already support source-frozen prior-period/forecast/budget
reasonableness, price/volume/FX/mix bridges, quantified residuals and accounting-owner
escalation. The earlier skill contract was narrower than the mapped practice.
The extension formalizes deterministic methods in the existing package, rather
than adding normative accounting claims or changing canonical approvals.
