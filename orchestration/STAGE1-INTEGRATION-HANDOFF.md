# Stage 1 integration handoff

Repository: DanTrackedFR/chief-accounting-officer. Baseline live main: e0735d5a45971c9dac0334f68cacbcad42685035. Delivery: orchestration/scope-repeated-owner-foundation, PR #34. Unmerged. The PR records the immutable final candidate SHA and exact-head Actions results without introducing a self-referential committed hash.

## Architecture

ScopeRegistry is the single runtime Scope architecture for LEGAL_ENTITY, SUBGROUP and GROUP. IDs are explicitly governed stable keys, independent of display names, order, filenames and generated random IDs. Parent validation rejects duplicate/missing/self parents, cycles and illegal type transitions. Parent relationships establish metadata, never accounting control or execution dependency. Framework, jurisdiction, functional/presentation currency, calendar, current/effective metadata and provenance remain separate.

Canonical execution identity includes owner, Scope ID/type, framework, jurisdiction, currencies and existing bounded period. NodeTable and OwnerInputs retain convenient unique aliases; ambiguous repeated-owner package lookups fail rather than overwrite. Scope-aware reviewed packs qualify source inventories, material facts, complete native source manifests and native certification. Result envelopes retain producing node, exact-case fingerprint, dimensions and currentness. Typed receipts validate actual results and explicit source/target nodes/Scopes. Hierarchy alone authorizes no consumption.

The inherited gross-line economic allocator is extended with posting Scope and bounded period. Governed node/currency/period/layer validation precedes allocation. Account/event/nature aliases cannot bypass duplicates. Legitimate identical legal/entity/group economics remain distinct across posting Scopes. Existing Group replay and specialist authority are preserved. Manufacturing, Diagnostic, Intake, SaaS, Treasury and Group use the same primitives.

## Controlled proof and executable lineage

`python -m orchestration.tests.generate_scope_examples` executes production Revenue separately for ENTITY-NL (IFRS/EUR/NL), ENTITY-US (US_GAAP/USD/US) and ENTITY-UK (UK_GAAP/GBP/UK), under GROUP-EUR (IFRS/EUR presentation). Each has an independent source, reviewed pack, node, fingerprint, actual native result and journal population. Equal recognized revenue values are intentionally retained to prove numeric equality cannot establish identity.

The Group consumer is an explicit LOCAL_RESULT_OBSERVATION consumer. It displays qualified local results and unresolved US/UK framework/currency conversion boundaries. It creates no converted/consolidated IFRS/EUR revenue total and no accounting owner. Public output contains scoped useful observations without internal fingerprints, source routing or execution IDs.

Executable lineage: NL source → NL Fact → NL reviewed pack → NL Revenue → typed Group receipt; US and UK equivalents retain explicit unresolved conversion boundaries; Group profile source → governed GROUP-EUR → Group consumer → public CAO output. `examples/scope-repeated-owner/lineage.json` contains actual source, fact, node and receipt bindings.

## QA and release gates

Authored permanent Stage 1 controls: 52 tests. Independent reviewer: 44 coordinated tests, five substantive findings reproduced and remediated, permanent coverage, final independent rerun PASS and zero unresolved substantive findings. See STAGE1-INDEPENDENT-QA.md. Final regression totals, artifact reproduction and exact-head publication gates are recorded below and in PR metadata when complete. A successful local checkpoint alone does not establish readiness.

## Boundaries and continuation

Stage 2 handoff: STAGE1-TO-STAGE2-HANDOFF.md. Stage 1 provides Scope and execution identity, not general hierarchical Case lifecycle, opening/prior/comparative period chains, cross-period invalidation, reopening/supersession, acquisition/disposal histories, intercompany networks, framework conversion or new currency translation. No durable persistence or new accounting authority is introduced. Government Grants PR #27/package, Borrowing Costs and Investment Property are untouched. Canonical and supplemental accounting knowledge invariants remain protected.

Roadmap: Stage 1 implementation COMPLETE with publication gates still required; Stage 2 NEXT only after owner merge; Stages 3/4 PENDING; overall workstream IN PROGRESS; Durable Case/Memory NOT YET NEXT.
