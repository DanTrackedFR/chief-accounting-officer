# CAO Orchestration Foundation — integration handoff

Branch: `orchestration/cao-foundation`. PR #28 targets main; do not merge.
Exact final candidate and Actions evidence are recorded in the PR after push;
this document does not embed a self-referential commit SHA.

## Delivered scope

* `registry.py`: source-derived registry for all 50 packages, 47 production
  metadata statuses, contracts/limitations and executor availability.
* `planning.py`: economic fact decomposition via Planner interface; deterministic
  fact adapters, cross-cutting architecture rules, transitive actual-owner imports,
  node-ID-independent graph, readiness waves, conditions, cycle guards and rework.
* `runtime.py`: native `production.assess_case` execution, dimension/current/full
  result controls, semantic handoffs and alias-proof economic/metric/target ledgers,
  required reporting bridges, distinct active challenge, governed Case lifecycle,
  combined accounting synthesis, approved margin basis and Context Observer.
* `run_case.py` and public interface: separate internal and curated public records,
  all seven governed routes, substantive limitations/open items retained,
  contamination fails closed. Internal evidence is retained unchanged.
* `tests/fixtures.py`: actual complete native synthetic owner workpapers. Only test
  fixtures regenerate synthetic approvals; no runtime approval manufacturing.
* `examples/`: Case reference export, graph, issue/execution/handoff ledgers,
  reconciliation summary, owned mapped journal pack, challenge, public conclusion,
  candidate memory, partial grant case, contradiction and one-owner AP control.
* `.github/workflows/cao-orchestration.yml`: immutable head checkout and complete
  orchestration/skill/lease/repository/knowledge/authority regression.

## Manufacturing result

Broad objective: prepare year-end manufacturing accounting review and assess
inventory/gross margin, without naming skills. Automatically selected owners:
Fixed Assets; AP; Employee Benefits/Payroll; FX; Inventory/Cost; Revenue;
Financial Statements; Balance Sheet Reconciliations; Month-End Close;
Systems/Data Integrity; Controls/ICFR; Disclosure Management; Accounting Analytics.

Base facts do not select Agriculture, Derivatives/Hedge, Insurance, Leases,
Government Grants, Borrowing Costs or Investment Property. FX disappears when the
imported exposure is removed; warranty facts identify a Provisions owner.

Actual cost handoffs: Payroll expense 10,800; AP eligible supplier cost 120;
machinery depreciation 90,000; historical imported-input cost 110. Inventory
absorbs eligible labour/variable OH and 45,000 fixed OH under normal capacity,
retaining 45,000 under-recovery separately. RM 510; WIP 11,304; FG 33,912; total
45,726. Eligible production cost 56,520; Inventory sale relief/COGS 11,304;
Revenue 40,000. Approved presentation policy includes unallocated manufacturing
expense in cost of sales: 56,304; gross margin −16,304 (−40.76%). Revenue less
Inventory relief remains separately labelled 28,696. Missing/unapproved margin
policy produces a material question, rather than inventing presentation.

Inventory and Revenue feed governed statement rows; Inventory feeds actual
reconciliation and native Analytics COGS bridge; Statements feeds native Disclosure.
Repeated evidence references do not repost owner journals. The independently
reviewed mapped pack ties every signed movement to native statement GL changes.

## Adversarial/partial behavior

Wrong Payroll import; duplicate direct AP cost; wrong-period depreciation; stock
versus GL; delivered sales units versus Inventory relief; FX amount mismatch;
system quantities; duplicate production order; stale full owner result; economic
aliases; omitted reporting bridges; arbitrary/stale/re-reviewed wrong journal
mapping and omitted pack validation all produce unresolved/challenged outcomes.
Transitive affected results are invalidated with retained prior evidence.

Material unavailable Government Grant: PARTIAL, manufacturing work retained,
precise unavailable-owner open item, no fabricated grant journals. Explicitly
immaterial independent secondary gap can coexist with complete scoped work;
unknown materiality cannot waive a blocker. A bounded AP-balance question runs
only AP and derives closing AP 20. Partial/material unresolved cases cannot close.

## Independent QA and remediation

See `INDEPENDENT-QA.md`: separate reviewer authored 30 tests and documented
IQA-01–09, plus the omission bypass under IQA-07. Findings covered custom node IDs,
malformed facts, boolean materiality, transitive imports, economic aliases,
mandatory reporting coverage, mapped journal integrity, approved margin basis
and deterministic artifact ordering. All substantive findings were fixed,
executable-regressed and independently rerun. Final independent suite: 30 PASS.
Artifact reproduction: 3 PASS separately under hash seeds 17 and 31.

## Local final regression

| Gate | Tests | Result |
|---|---:|---|
| Orchestration, authored + independent + adversarial + artifacts | 70 | PASS |
| Full shared production skills | 1,176 | PASS |
| Repository/privacy/canonical tests | 53 | PASS |
| Lease vertical slice | 17 | PASS |
| Tax supplement | 10 | PASS |
| Agriculture supplement | 12 | PASS |
| Independent Agriculture claims | 71 | PASS |
| Insurance supplement/independent claims | 35 | PASS |
| Derivatives supplement | 4 | PASS |
| Independent Derivatives review | 7 | PASS |
| Inventory supplement/independent claims | 262 | PASS |
| Total distinct final suites | 1,717 | PASS |

All five supplemental validators, canonical claims/approval validators and
`git diff --check` pass. Existing generated synthetic owner imports were regenerated
because changed public/governance implementation bytes invalidate fingerprints.
No real approval was rewritten. Historical architecture/orchestration.md remains
byte-identical because its Insurance release baseline protects it; new runtime
resolution is documented here and in README/reconstruction instead.

## Preserved boundaries and remaining work

Government Grants PR #27 and branch remain untouched. Borrowing Costs and
Investment Property substantive packages remain untouched. No knowledge file
changed: 157/157 approved canonical topics, 347 mappings, 1,598 claims; supplemental
Tax64, Agriculture66, Inventory228, Derivatives100, Insurance168 preserved. No
Government Grants supplemental material from its WIP branch was imported.

Remaining: general model-backed semantic planning/document extraction, more input
adapters/owner bindings/scenario combinations/framework overlays, multi-entity and
multi-period graph execution, authenticated governance, persistence and UI.
Leases needs a governed shared executor adapter. Independent graph waves execute
locally in deterministic order, not simultaneous external workers. This is the
orchestration foundation and manufacturing flagship, not a complete final CAO
product or a new numbered roadmap phase.
