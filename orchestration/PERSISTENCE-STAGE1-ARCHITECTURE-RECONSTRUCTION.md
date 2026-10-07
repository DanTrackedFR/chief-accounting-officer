# Durable Case Stage 1 live architecture reconstruction

Live GitHub main and local clone verified at `a96dd66b55b2920443576d9910208423f3240582`,
Stage 4 merge PR37. Remote branch inventory and persistence PR search found no
existing Stage 1 persistence work. Dedicated branch: persistence/durable-case-foundation.
The attached March project setup pack is product context, not authority to redesign
this runtime or restrict this repository task to its earlier Excel wedge.

Read the roadmap, Durable Case/Memory compatibility handoff, Stage1/2/3 integration
handoffs and Stage4 integration, final independent QA, release manifest, temporal
model QA, progress history and additive defect register. Historical incomplete
checkpoints remain history; final Stage4 disposition resolves IQA03/TQA01 and
retains the original conflict. Stage4 merge is the authoritative current baseline.

Actual contracts inspected: runtime Case/CAO, Company Context record filtering,
ScopeRegistry/execution_identity, PeriodRegistry/calendar/relationships, CaseRegistry,
Graph/Node, VersionRegistry/VersionedExecution/Dependency/ResultVersion,
runtime_governance and governed_plan, sealed intake Inventory/RawSource/extraction,
ReviewedInputPack and native/replacement qualification, current journal allocator
and CAO.public/current synthesis provenance. No replacement accounting runtime.

Main contains all four accepted multi-entity stages and required governed hierarchy,
arbitrary Scopes, multi-period calendars, immutable result versions, exact typed
receipts, stale/supersession/invalidation/selective rework, distinct opening and
comparative roles, bounded intercompany/framework/currency chains, legal versus
Group exact-once accounting, native Consolidation/Financial Statements, original
material-conflict and corrected CLOSED controls, public privacy and release artifacts.
The roadmap's older introductory IN PROGRESS text is stale relative to its final
Stage4 COMPLETE subsection and merged acceptance; preserve historical stage plans.

The user's new sequential four-stage persistence plan is this implementation plan,
not a pre-existing historical specification. Stage1 covers durable checkpoints,
atomicity/revision checks, validation and independent restoration only. Stage2
restart-safe rework/release, Stage3 approved company memory and Stage4 durable full
integration remain future. SQLite is a standard-library local transactional adapter.
A compatibility gap is retaining full historical source payloads rather than only
fingerprints/latest inputs; publication copies them without changing results.
