# Stage 4 population review — separate-context interim QA

This independent reviewer reconstructed the actual Stage 3 runtime contracts and Stage 4 durable checkpoint without authoring runtime or flagship inputs. This is an interim review, not final acceptance. Prior IQA01/IQA02/IQA03 history in `STAGE4-INDEPENDENT-QA.md` remains authoritative and preserved.

## IQA03 current accounting chain

The current complete-population guard correctly rejects the flagship's missing current UK timing and UK/US FX sides. Safe refusal alone does not resolve IQA03. Current legal population comprises clean NL/US, mismatch NL/UK, timing UK October, and FX UK/US October. NL timing September is historical evidence, not automatically an October carrying amount.

The actual governed chain must include a separately reviewed current NL timing result qualified from the prior-closing/current-opening relationship. UK timing GBP30 must enter a native translation TB row and qualified bounded IFRS ordinary-loan reassessment. UK FX GBP16 and US FX USD20 must each enter native translation, retaining the original USD20 transaction identity and actual legal side. Translation rates are independently supplied reviewed source evidence; orchestration may not compute, infer, or relabel them. Native ordinary-loan reassessment and Consolidation retain accounting authority.

Existing `validate_native_bindings` allows only one translation and a directly qualified EUR counterparty legal result for bounded Group IC reassessment. The UK/US relationship has neither EUR-functional legal counterparty. A minimum generic extension to accept two exact native translation receipts is required for that relationship, binding the actual receiving/paying legal scope to gl_a/gl_b respectively and retaining exact principal, transaction, framework, currency and version checks. This is an integration-contract correction, not permission for generic GAAP conversion.

Original TIMING_DIFFERENCE/FX_DIFFERENCE matching results must remain immutable evidence. Fresh reviewed MATCHED decisions may qualify the current chain when exact original transaction principal, reciprocal identity and explicit temporal alignment satisfy the existing native matching contract; this must not erase the historical timing/currency distinction. Group reporting must consume every current qualified population through native owner dependencies.

## S4-IQA04 — self-declared perimeter erases complete population

**Reproduced; unresolved at initial reviewer run.** `validate_group_loan_population` constructs the expected current legal roster only from `source['entities']`. A full-close source with empty entities, empty roster and empty matching receipts passes. The same guard accepts GROUP-EUR or an unknown entity as the supposed legal perimeter, again producing an empty expected roster. These are direct actual-runtime guard reproducers on the real initial flagship session; no fixture, runtime, bounded bypass or successful-close control was modified.

Permanent executable file: `tests/test_stage4_population_independent.py`.

- `test_full_population_cannot_erase_legal_perimeter`
- `test_full_population_cannot_substitute_group_for_legal_perimeter`
- `test_full_population_cannot_substitute_unknown_scope`

Initial execution: `python -m unittest orchestration.tests.test_stage4_population_independent -v`: **3 distinct tests, 3 FAIL**, each `ValueError not raised`. This establishes a population-guard contract weakness, not demonstrated complete native Consolidation closure with an empty TB. Other native checks may independently reject those incomplete inputs.

Minimum remediation: require nonempty registered legal scopes in the declared complete population; bind that perimeter to the independently reviewed full objective/intake perimeter so native source mutation cannot silently shrink it. Scope hierarchy remains organizational identity rather than an execution dependency: exact explicit edges and receipts still supply consumption authority. Reviewer will independently rerun after generic correction; final acceptance still requires the real complete flagship chain and subsequent independent review.

## IQA04 independent remediation rerun

The implementation now requires a distinct nonempty registered LEGAL_ENTITY perimeter and compares it against CURRENT/effective legal descendants of the consuming Group Scope. This supplies a completeness boundary only: native consolidation eligibility/ownership and exact dependency consumption remain separately governed. Empty, Group-only, unknown and one-real-entity-omitted perimeter attacks now reject. The missing-UK attack preserves the genuine current NL/US roster, demonstrating that a shortened source cannot shrink the coverage promise merely by presenting internally consistent remaining versions.

Initial three reproducers independently rerun **3 PASS**. Expanded suite independently rerun **11 distinct tests, 11 PASS**, command unchanged. IQA04 is remediated for this opt-in declared full-population contract. It does not establish completeness for legacy bounded chains lacking that declaration, nor discover unseen/unregistered real companies; governed Scope inventory completeness remains an upstream reviewed-source obligation. A CURRENT Scope overlapping only part of a reporting period remains within the complete population, consistent with effective-interval inclusion rather than a fabricated whole-period accounting conclusion.

## Fresh correction intake independent review

`qualify_replacement` independently reuses sealed source qualification, then compares the exact node record, root Case/objective, Scope/Period registries, incoming dependency contracts and complete Case population against the retained ordinary graph. It executes no owner and publishes no replacement itself. Accounting-owner certification and version/invalidation remain ordinary CAO responsibilities. Observation replacements receive complete snapshot/manifest/dimensional checks despite having no accounting Fact binding; this closes a plausible non-native source loophole. Incoming receipts are rebuilt from current actual dependencies and compared, so a faithfully sealed obsolete receipt still rejects.

Seven additional independent tests verify fresh reviewed replacement preserves original current execution, rejects unsealed accounting mutation, wrong retained Case, changed execution identity, omitted complete snapshot, omitted incoming edge, and independently sealed obsolete matching receipt. All PASS. Source identity and provenance are fresh deterministic identities of separately supplied replacement inputs; the original fixture is copied and remains immutable. These tests use no bounded bypass and claim no complete Group closure.

Review limits: the source inventory and review approvals remain controlled synthetic evidence. A sealed snapshot is an exact supplied accounting workpaper, not independent proof that real-world evidence outside that inventory was exhaustively obtained or approval identities authenticated. Final IQA03 positive Group chain, temporal native execution, complete release regressions, final artifacts, final independent acceptance and exact-head CI remain outstanding. This interim reviewer modified only the two assigned independent-review files, with no runtime/fixture edits, commits or pushes.
