# Stage 3 → Stage 4 handoff

Stage 3 is the bounded intercompany-network and governed transformation substrate, not the final integration flagship. Start Stage 4 from newly merged live main, independently reconstruct it, and retain the Stage 1 Scope and Stage 2 Case/Period/version architecture. Do not start Stage 4 before Stage 3 integration.

## Implemented contracts

`intercompany_network.py` carries governed legal counterparties, deterministic economic/agreement/book-entry identities, exact current native result versions and actual source-row evidence. Explicit reviewed bilateral decisions preserve both legal sides and classify MATCHED, TIMING_DIFFERENCE, FX_DIFFERENCE, CLASSIFICATION_DIFFERENCE, MISSING_COUNTERPARTY, MISSING_SOURCE_EVIDENCE or UNRESOLVED_MISMATCH. Business cycles are independent of the execution DAG. The current native transaction adapter supports ordinary intercompany loans; other transaction classes fail closed until their real production contracts are connected.

`cross_layer_receipts.py` binds exact producers/consumers, versions, Scopes, Cases, Periods, semantic/economic identities, layers, frameworks, currencies and current native fingerprints. Native Foreign Currency translation is revalidated against actual input/output rows. Supported framework qualification is narrowly the existing Intercompany owner's IFRS ordinary-loan reassessment of the native translated US-GAAP result, with zero framework adjustment; it is not a general GAAP converter. Unsupported general conversions remain unresolved. Consolidation and Financial Statements remain accounting authorities.

`stage3.py` integrates native bindings and the bounded matching observation with ordinary CAO execution and the existing VersionedExecution engine. No parallel invalidation engine exists. Matching carries no journals. Translation contributes native presentation values through witnessed Group population; monetary-FX journals cannot be hidden under a translation-only disposition. Legal adjustments and Group eliminations retain separate exact-once identities. Public output uses the existing curated boundary and exposes the unresolved residual without internal receipts or source-review metadata.

## Controlled proof and correction

`tests/stage3_fixtures.py` and `examples/intercompany-framework-currency/` prove GROUP-EUR, ENTITY-NL, ENTITY-US and ENTITY-UK; September/October and distinct calendars; four bilateral relationships and a business cycle; clean, timing, FX and unresolved differences; US-GAAP/USD → native EUR translation → qualified IFRS reassessment → native Consolidation → native Financial Statements. This order is supported only for the fixture's actual owner contracts.

An upstream US legal carrying result correction preserves its old version and invalidates exactly six consumers: clean match, translation, conversion, elimination, reporting and Group observation. Selective topological re-execution produces current replacement receipts and keeps unrelated bilateral relationships current. Group equity changes EUR390 to EUR381.82; profit is EUR8.18 and OCI EUR−16.36. The unresolved UK/NL residual remains EUR−1, and the aggregate Case remains partial. No invented correction or balancing offset closes it.

The fixture prepares separately reviewed prospective native input packs in an isolated rehearsal; orchestration does not certify accounting or fabricate transformation values. Scope/economic-qualified repeated owners use existing node/version identity extensions. Legacy absent qualifiers serialize exactly as before.

## Stage 4 responsibility

Build the realistic full integration flagship using this substrate and existing production owners. Include at least three legal entities, Group, multiple periods/currencies/frameworks, repeated owners, network relationships, Group reporting and analytics. Demonstrate both a material-conflict Case that safely remains blocked/partial and a corrected clean control that legitimately reaches COMPLETE/CLOSED. Expand owner adapters only where actual qualified contracts support them; never turn unsupported conversion into a generic relabeling engine.

Repeat authored tests, genuinely independent adversarial QA/remediation/rerun, all prior flagship migrations, deterministic artifact generation, complete repository regression and immutable-head required GitHub Actions. Only Stage 4 acceptance can mark the overall roadmap workstream COMPLETE and make durable Case/Company Accounting Memory persistence NEXT. Stage 3 adds neither persistence nor authenticated governance.
