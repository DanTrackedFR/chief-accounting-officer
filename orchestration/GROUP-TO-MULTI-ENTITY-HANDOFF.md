# Group to multi-entity / multi-period handoff

This flagship is a bounded precursor, **not general multi-entity or multi-period orchestration**. It uses the existing CAO Case, planner, graph, native production executors, challenge, event allocator and public adapter. It does not introduce a second engine.

## Implemented boundary

One reporting Group, two separately identified legal entities, one framework and one reporting Case. Explicit scopes carry entity, entity/group level, framework, jurisdiction, currency and source/reporting period. Every owner remains one independently reviewed native workpaper per package. Group journals cannot target either legal scope, and legal scopes cannot silently become nested groups. Source candidates retain legal identity before native Consolidation aggregates the qualified populations.

Complete supplied dated activity windows preserve full-year source data and select only post-acquisition results. The effective date must match the actual Business Combination acquisition date. No prorating or inferred split is permitted. The full-year TB, acquisition retained profit, gross included revenue/expense and closing balance population reconcile before FX execution. This is one acquisition cutoff inside one reporting Case, not comparative execution.

Typed current-result receipts bind Tax → BC, BC → FX/Consolidation, FX → Impairment/Consolidation/Analytics, IC → Consolidation, Impairment → Consolidation, Consolidation → FS/Analytics and FS → Analytics. The IFRS controlled route uses full-goodwill fair-value NCI, one ordinary acquisition, unchanged ownership, one foreign operation, one matched bilateral loan, supplied valuation and **nil impairment**. Positive impairment/allocation, partial-goodwill gross-up, earnouts, step acquisitions and disposals are explicitly unsupported in this integrated route and must fail closed. Native specialist support does not imply integrated support.

PPA, acquisition DTL and CTA implications embedded in the qualified source snapshot remain evidence-only. The existing gross-line event allocator selects Consolidation's actual investment/equity, IC and NCI journals once, and replays source plus postings to every final account. This is a reviewable consolidation journal pack, not a legal-book posting API. Separate narrow specialist controls use previously qualified evidence and do not claim a full Group bridge.

Document identity alone is insufficient. Reviewed text assertions and complete keyed TB populations are manifest-bound inside native owner certification. The entire separately reviewed normalized SPA extract is retained internally so unknown scope clauses cannot be discarded by refreshing its hash. This is explicit reviewed extraction, not unrestricted legal NLP or autonomous accounting certification.

## Requirements deliberately left for the next workstream

| Area | Required general capability |
| --- | --- |
| Entity graphs | Arbitrary ownership/control graphs, nested groups, missing entities, associates/JVs, acquisitions/disposals, multiple consolidation methods and ownership histories; rights-based determination remains Consolidation authority. |
| Case hierarchy | Durable Parent/Sub/legal-entity Cases linked to a Group Case; separate issue registers, reviews, closure gates and local versus group workplans. |
| Node identity | Stable `(owner, legal/group entity, framework, currency, source period, included period)` keys; repeated owners at several entities rather than one package-keyed input. |
| Intercompany graph | Multiple bilateral counterparties, transaction-level matching across legal books, currency/timing/source-correction edges, cycles, source-currentness, residual materiality and elimination dependencies. |
| Currency | Multiple functional currencies, historical capital layers, presentation currencies and permitted translation chains; no currency relabelling; reviewed rate populations and specialist mechanics. |
| Framework | Local/group framework differences and independently qualified conversion adjustments before translation/consolidation. |
| Periods | Multiple reporting periods and comparatives, opening balances, acquisition/disposal effective dates, rolling source populations, partial periods, fiscal/calendar misalignment and ownership changes. |
| Journals | Persist legal-entity postings separately from consolidation-only journals; immutable source economic identities, evidence-only downstream uses, reversal/reopening and exact-once consumption across Cases/periods. |
| Dependencies | Cross-entity/cross-period invalidation and rework; fresh owner-result bindings, scoped disclosure/reporting adapters and entity-contribution analytics after shared-account aggregation. |
| Persistence | Durable scope/graph versions, source exports, approval events, selected intervals, result fingerprints, economic consumption ledger, source-to-public lineage and supersession history. No implicit memory promotion. |
| Approval | Real authenticated preparer/reviewer separation and scope-specific approval events, rather than synthetic test certificates. |

The dedicated next workstream must independently specify these contracts and migration behavior. Do not generalize by increasing the three-scope cap or weakening receipt/source/journal gates. Existing Manufacturing, Diagnostic, Intake, SaaS and Treasury regressions remain mandatory migration controls.
