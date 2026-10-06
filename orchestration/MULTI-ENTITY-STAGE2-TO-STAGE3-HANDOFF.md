# Stage 2 → Stage 3 architecture handoff

Stage 2 extends the Stage 1 Scope substrate with governed Case, Period, dependency and result-version semantics. Stage 3 must begin only after PR #35 is owner-reviewed and merged, from the resulting live main.

## Stable Stage 2 substrate

- `CaseRegistry` composes governed ENTITY_CASE / SUBGROUP_CASE / GROUP_CASE identity from Scope, Period, objective and cycle. Scope hierarchy, Case hierarchy and execution dependency graph remain separate.
- `PeriodRegistry` provides deterministic calendar-qualified Period identity, CURRENT/PRIOR/COMPARATIVE/OPENING/PARTIAL_INCLUDED_PERIOD relationships, effective intervals and governed close/reopen history. Dates establish no accounting authority.
- Ordinary runtime repeated-owner selection is Scope + governed Period aware. Stage 1 execution identity remains compatible; a supplied governed Period ID composes into the node identity.
- `Dependency` binds exact producer/consumer nodes, Cases, Scopes, Periods, dependency type, metric and governed evidence. Parent relationships never create dependency edges implicitly.
- `VersionRegistry` preserves immutable result versions and CURRENT / STALE / SUPERSEDED state. Publication binds exact current dependency versions; supersession never deletes history.
- Invalidation follows exact dependency bindings transitively. Selective re-execution is topological and rejects unrelated reruns. Scope/Case membership alone cannot stale work.
- Typed receipts bind exact result version/currentness plus Scope/Period dimensions. Stale, superseded, wrong-Scope and wrong-Period receipts fail closed even at equal values.
- Reopening is governance/versioning, not an accounting reversal. Closed history is retained.
- Period-aware scoped journals admit only current result versions through the inherited exact-once allocator. Superseded history is evidence, not additional current economics.
- The Group acquisition cutoff is normalized through generic Period/EffectiveInterval infrastructure while specialist owners retain accounting authority.

## Controlled proof

The bounded proof uses GROUP-EUR, ENTITY-NL, ENTITY-US and ENTITY-UK. A qualified US September Revenue result is corrected from 800 to 900. The original version is superseded; actual downstream US reporting → US October opening observation → Group October observation → Group analytics observation becomes stale and is selectively re-executed. UK and independent controls remain current. No framework conversion, generalized FX translation or consolidated-EUR accounting authority is manufactured.

## Stage 3 implementation scope

Stage 3 must build the generalized cross-scope interaction layer on top of these stable identities:

1. multi-counterparty intercompany graph with explicit legal entities/counterparties;
2. transaction-level bilateral matching and residual classification;
3. business-relationship cycles without execution-DAG cycles;
4. cross-period intercompany relationships using Stage 2 Period/version/currentness contracts;
5. multi-currency intercompany relationships without currency relabelling;
6. explicit Group elimination dependencies distinct from legal-book postings;
7. local-framework → Group-framework conversion receipts, with production accounting owners retaining treatment authority;
8. multiple functional currencies and Group presentation currency;
9. governed translation chains using qualified FX-owner outputs;
10. exact-once economics across legal-book, counterparty and Group layers;
11. invalidation/selective rework across those Stage 3 edges using the Stage 2 dependency/version substrate;
12. deterministic artifacts, independent adversarial QA and migration of all prior flagships.

## Stage 3 boundaries

Do not redesign Stage 1 Scope identity or Stage 2 Case/Period/version identity merely for convenience. If a genuine defect is demonstrated, reproduce it, make the smallest generic correction and preserve migration regressions.

Stage 3 must not become the Stage 4 full integration flagship. It must not build durable database persistence, authenticated governance or new accounting authority.

## Deliberate remaining limitations after Stage 2

Stage 2 does not provide generalized multi-counterparty intercompany matching, generalized framework conversion, generalized multi-step currency translation, durable persistence or authenticated approval. The controlled Group/reporting/analytics consumers used for dependency proof are non-authoritative observations where specialist accounting conversion is unavailable.

Government Grants PR #27/package, Borrowing Costs and Investment Property remain excluded. Preserve canonical approvals, supplemental knowledge, public-output boundaries and fail-closed unavailable owners.
