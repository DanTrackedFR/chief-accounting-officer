# CAO Orchestration Foundation

The user supplies an accounting objective, company context and source workpapers.
The runtime identifies issues, discovers governed owners, builds dependency waves,
executes native production gates, challenges the combined position and answers as
one CAO. The manufacturing scenario is a fixture, not a special engine branch.

## Supported runtime

`CAO.run(request)` returns the internal `Case`. `CAO.public(case, route)` creates
a separate curated record through `public_record`. The public CLI is:

```sh
python -m orchestration.run_case request.json
python -m unittest discover -s orchestration/tests -p 'test_*.py'
python -m orchestration.tests.generate_examples
```

The input object contains `objective`, `case_id`, execution `scope`, governed
`company_context` records, structured economic `facts`, qualified `handoffs`,
independent `challenge_assertions` and, for an integrated posting workpaper,
`journal_account_mapping` and an independently reviewed `journal_pack_review`.
The user does not name skills. Source ingestion/preparation currently supplies
reviewed native workpapers under economic fact families, e.g. employee_cost,
machinery, supplier_cost, inventory and customer_contract. See the synthetic
factory fixture for the complete executable input contract. It is not a natural
language extractor for arbitrary uploaded documents.

## Registry and issue identification

Registry introspects every actual SKILL.md and resolves identities against
production.PACKAGES. It exposes status, production and executor availability,
triggers/non-triggers, domains, context/dependency/related-owner and input/output
contracts, framework declarations, source paths and limitations. Sparse existing
metadata is visible, not supplemented with invented authority. Metadata production
status never bypasses the actual knowledge/certification executor. Leases remains
a production vertical slice with a missing shared-runtime adapter, so a requested
Lease node is explicitly blocked in this foundation.

Planner.identify is the bounded interface for future semantic interpretation. The
provided deterministic implementation decomposes supplied economic populations
first, then resolves owners and actual imported owner dependencies transitively.
Objective scope controls the bounded AP balance inquiry; no manufacturing keyword
runs a fixed package list. Missing/unrecognized/malformed supplied fact families
remain visible. Related skills are context, never automatically invoked wholesale.
Cross-cutting judgment, recurring process, material balance, new process and
manual cross-system rules add genuine relevant graph nodes/considerations.

## Graph, execution and Case lifecycle

Node IDs are independent of owner package IDs. Nodes retain issue, reason,
entity/framework/period, prerequisites, inputs, owner-result dependencies, status,
result/evidence/open items, downstream consumers, iteration and challenge/rework.
Graph validates duplicate IDs/dependencies, missing dependencies and cycles.
Independent ready nodes share an execution wave; local native calls execute
serially inside a wave for deterministic CI. This supports parallel eligible work
without claiming asynchronous external workers. Conditional nodes can become not
applicable. Invalidation propagates transitively and retains invalidated result
history. Reopen allows graph rework; CAO.rework uses a newly versioned request,
fresh native approvals and explicit case supersession without deleting history.

Case fields follow memory/accounting-case-schema.md, plus execution/handoff and
economic ledgers. Lifecycle is OPEN → SCOPED → IN_PROGRESS → CHALLENGE → CONCLUDED
→ DOCUMENTED → CLOSED. A partial/blocked conclusion remains DOCUMENTED; material
unresolved work cannot be hidden by a clean close. Complete work can include a
separately identified, explicitly immaterial independent secondary blocker.
Unknown materiality is never invented or treated as immaterial.

Required questions identify missing dimensions/workpapers or real contradictions.
Optional industry/policy/system history does not block an otherwise scoped case.
Company Context is read before questions; current scoped confirmed/documented/
approved records can resolve facts. Proposed/superseded/expired/wrong-scope records
do not become established truth. Conflicts remain disputed.

## Ownership, exact-once and challenge

All accounting invocation uses production.assess_case. No runtime signs cases or
calls private arithmetic functions. Native imports still reexecute and compare
actual full results; dimensions additionally include jurisdiction and currency.
Inventory binds original economic IDs and eligible cost evidence to actual
Payroll expense, Fixed Assets depreciation, AP invoices and FX historical basis.
Actual owner imports determine graph edges; caller omission cannot remove required
Inventory/Revenue → Reporting or Inventory → Reconciliation bridges.

Qualified handoffs check semantic owner/metric, amount, target, dimensions,
current result and original economic identity. Separate identity, metric and
consumer-target checks prevent aliases from consuming an amount twice. Reporting
references can appear in multiple consumers, but each consumer receives a metric
once; absorption economics remains globally once. Upstream journals remain owned
upstream; downstream results never repost them. Internal journal packs retain
owner identity and original source fingerprints.

An integrated mapped journal pack requires independent exact-payload review of
native owner journals plus mappings. CHALLENGE reconciles every mapped signed
movement to the current-minus-comparative native Financial Statements GL. The
review label/hash alone cannot authorize an economically wrong mapping. Omitting
the pack validation cannot certify a multi-owner reporting case.

Challenge is a distinct executed phase: fresh owner reexecution, independent
numeric GL/system/quantity assertions, sales delivery versus Inventory relief,
policy/prior-position conflicts, alternatives, open owner dependencies and mapped
journal movement tests. Native skills independently gate source completeness,
framework/estimates, journals, reconciliation, documentation/control/disclosure
inputs. Failed challenge invalidates affected/downstream conclusions and changes
the case outcome; it does not pick a convenient source.

## Synthesis, privacy and Context Observer

Synthesis extracts accounting metrics only from their designated owner, combines
Revenue period revenue and Inventory COGS into margin, preserves reviewed stock/
production cost/absorption/under-recovery facts, journals and reporting/control
consequences, assumptions, limitations, approvals and unresolved areas. Completed
work remains available when another material owner is unavailable.

Every public route is curated separately and traverses public_record. Raw owner
results, source notes, approval tracks, evidence internals, reviewer identities,
fingerprints and claim registers are excluded; contaminated allowlisted text fails
closed. Accounting scope limitations, missing evidence, uncertainty and blocked
work remain visible. Internal evidence is retained intact. The CLI returns a safe
structured blocked answer if parsing/curation cannot succeed.

Context Observer emits PROPOSED durable-context candidates and OBSERVED supplied
observations, not automatic truth mutations or approval. Approved context and
history remain unmodified. Persistence and authenticated human identity remain
separate deferred architecture decisions, consistent with existing contracts.

## Manufacturing workpapers

The synthetic 2026 IFRS factory has RM/BOM/routing/order/WIP/FG, normal capacity,
owned machinery, employee expense, supplier cost, imported purchase, delivered
sales, GL/statements, physical count, source interfaces, control evidence and
close/disclosure/analytics workpapers. The planner selects 13 owners. Payroll,
Fixed Assets, AP and FX feed Inventory; Inventory/Revenue feed statements;
Inventory feeds reconciliations and native COGS analytics; statements feed native
disclosure work. Independent controls/systems/close work retains its bounded remit.

Derived closing stock: RM 510, WIP 11,304, FG 33,912; total 45,726. Eligible
production cost 56,520; fixed OH 90,000, absorbed 45,000 and under-recovery 45,000.
COGS 11,304; revenue 40,000; revenue less inventory relief 28,696. The supplied approved presentation policy
includes unallocated manufacturing expense in cost of sales: cost of sales 56,304
and gross margin −16,304 (−40.76%). Under-recovery remains separately visible and
is included once. Missing gross-margin policy creates a material question rather
than assuming its presentation. The figures derive from native results.
No biological assets, hedge, insurance, lease, grant or borrowing issue is forced
into the base graph. Removing imported purchases removes FX. Warranty facts add a
Provisions owner. A material grant produces a precise PARTIAL case while completed
manufacturing work is retained. An AP balance question invokes one owner.

The examples directory contains public answers and governed reference workpapers:
Case, graph, issue register, execution/handoff ledgers, reconciliation summary,
owned journal pack, challenge report and memory candidates. The compact internal
export references governed source/knowledge locations; the full Case representation
retains actual evidence in memory and is JSON serializable. Synthetic approvals
are fixture-only and must never be reused for a real company.

## Remaining scope

This is a deterministic orchestration foundation with a manufacturing flagship,
not the final CAO product. Arbitrary natural-language interpretation, document
extraction, broad input normalization, additional cross-skill semantic bindings,
multi-entity/multi-period graph execution, persistence, authentication, deployment
and UI remain later work. No claim is made that all 47 production combinations or
all framework/industry overlays are integration tested. Additional owners fail
closed when adapters/source contracts are missing. No accounting skill or
canonical/supplemental knowledge is authored here.

## Intent and diagnostic analytics foundation

The existing planner now has a governed `interpret` interface and `Intent` proposal:
primary mode, secondary modes, supporting modes/reasons and an optional bounded
owner inquiry. Runtime validates mode identities/duplicates; issue identification
and native production availability remain separate. Deterministic interpretation
is a bounded fixture adapter, not arbitrary semantic natural-language coverage.
Documentation/process/narrow accounting objectives avoid diagnostic expansion;
closing AP/inventory inquiries retain only the owner and genuine native imports.

Analytics 1.1.0 remains SKILL-ANALYTICS-001. Its optional reviewed diagnostic input
uses posted current owner metrics, frozen supplied comparators, deterministic
flux/rate/PVM bridges, native cost component allocation, explicit residuals,
evidence-tested hypotheses and observation-only anomalies. A comparator may be
budget/forecast/standard/target/approved baseline; generating those remains outside
scope. Accounting questions add bounded graph follow-ups and reexecute the actual
owner, retaining the accounting conclusion and its native treatment separately.
No follow-up duplicates owner journals or economics. Valid partial diagnostics
remain visible; challenged invalid analytics cannot supply a public explanation.

See `DIAGNOSTIC-INTEGRATION-HANDOFF.md`, `DIAGNOSTIC-INDEPENDENT-QA.md` and
`skills/management-accounting-analytics/methods.md`. The December/November factory
flagship and serializable bridge/lineage/hypothesis/Case/graph/public artifacts are
in `orchestration/examples/factory-diagnostic.*.json`. These are synthetic reviewed
source fixtures, not real-company approvals or an ingestion system.
