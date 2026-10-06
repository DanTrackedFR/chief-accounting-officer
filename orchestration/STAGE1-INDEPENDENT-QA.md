# Stage 1 independent executable QA

Reviewer: fresh independent agent, delegated only reviewer-owned test/report files. Runtime, fixtures and authored regressions were not edited by the reviewer. Baseline reviewed: pushed candidate `9272b4695d518eac01efeeab87adde97da6e0e14`; implementation remediation occurred concurrently and final rerun below must qualify the final state.

The suite `orchestration/tests/test_scope_independent.py` contains 44 distinct tests. It uses production certification on coordinated mutated inputs and refreshed exact-result receipts, rather than treating a stale fingerprint as evidence that Scope controls work. It exercises Intake, runtime and allocator public entry points. It includes existing Group execution and ordinary single-entity normalization, artifact regeneration and recursive public-output checks.

## Substantive findings and reproduction

| ID | Finding | Executable reproduction | Required remediation |
|---|---|---|---|
| QA-S1-01 | Wrong or mixed source population accepted after native recertification and receipt refresh | `test_coordinated_wrong_source_population`, `test_coordinated_mixed_source_population`: US native declares UK source, or adds NL; update child pack and refresh result receipts; Intake initially CLOSED/complete | Validate declared source populations against exact bound fact lineage and governed source metadata; retain exact per-execution packs |
| QA-S1-02 | Journal row/event agreement bypasses governed currency, period and node dimensions | `test_journal_currency_agreement_does_not_authorize_relabel`, `test_journal_period_must_be_bounded`, `test_journal_node_scope_must_match`, `test_journal_node_owner_must_match`: relabel both native/event currency EUR, stale period, UK node on US journal, or impairment owner on Revenue node | Validate row currency and period against registered Scope execution metadata; require deterministic exact node identity for supplied owner and Scope |
| QA-S1-03 | Qualified document exact-payload equality does not establish proper source Scope | `test_wrong_scope_qualified_document_matching_payload`: US native embeds actual UK document fingerprint/metadata with matching DocumentBinding, synchronized child pack and valid recertification | Validate source-document Scope/framework/jurisdiction/currency as well as bytes; explicit Group owner may qualify cross-scope sources under its governed contract |
| QA-S1-04 | Inactive Scope produces CURRENT result and receipts | `test_inactive_scope_cannot_produce_current_result`: set registered US Scope INACTIVE, run current Revenue objective | Refuse inactive/outside-effective Scope at execution selection without imposing a lifecycle or requiring unused registered Scopes to be executed |
| QA-S1-05 | Group context source id is decorative rather than executable lineage | `test_group_context_source_must_exist`, `test_group_context_source_scope_must_match_inventory`: replace Group context source id by nonexistent or US source id while claims retain Group dimensions; Intake initially completes | Bind Group context source to actual reviewed inventory and correct governed Scope metadata |

A suspected metadata contradiction bypass was retracted after correcting a positional test mutation. Targeting source-ENTITY-NL by ID with entity=ENTITY-UK already caused unresolved promotion rejection. The permanent rejection regression remains; this is not counted as a substantive finding.

## Challenge coverage

| Required challenge | Independent evidence |
|---|---|
| 1 Scope-ID collision | Distinct legal id with duplicate governed Scope id rejected |
| 2 Graph reorder | JSON roundtrip and reversed registry preserve every exact execution identity |
| 3 Unrelated insertion | Added independent Scope preserves US node identity |
| 4 Duplicate/missing/self parent | Independent collision test; independent missing/self-parent tests plus generic registry review |
| 5 Hierarchy cycle | Independent two-subgroup cycle rejected |
| 6 Hierarchy versus dependency | Real executed entity nodes have no hierarchy-derived dependencies |
| 7 Repeated-owner overwrite | Conflicting additional native case rejected and Group exact producer population checked |
| 8 Fingerprint/source reuse | Coordinated source populations with valid refreshed fingerprints, whole receipt swaps |
| 9 Mixed-entity population | Coordinated mixed native source population |
| 10 Wrong ReviewedInputPack | Exact child packs maintained during adversarial recertification; omitted/duplicate binding cases rejected |
| 11 Equal-value substitution | Entire equal-value receipt swap and substituted result fingerprints rejected |
| 12 Framework | US native recertified IFRS cannot become US GAAP producer |
| 13 Currency | Native functional-currency poison, receipt dimension poison, coordinated journal relabel |
| 14 Jurisdiction | UK native recertified NL jurisdiction rejected |
| 15 Source lineage | Wrong native source population and matching wrong-Scope qualified document |
| 16 Semantic entity creation | Unknown scoped issue does not mutate approved registry |
| 17 Ambiguous Scope | Source identity removed; filename never establishes qualification |
| 18 Group journal in legal books | Coordinated layer/posting/currency mutation rejected |
| 19 Legal journal in Group | Coordinated layer/posting/currency mutation rejected |
| 20 False cross-Scope dedup | Identical commercial event and amount in NL/US remain two postings |
| 21 Same-Scope alias duplicate | Separate alias journal index cannot reuse same economic identity |
| 22 Group migration bypass | Existing clean Group fixture executes generic registered scopes and exec node IDs |
| 23 Single entity | Ordinary Revenue automatic one-Scope normalization |
| 24 Public leakage | Recursive rendered public JSON excludes exact fingerprints, internal node IDs and source population identifiers |
| 25 Deterministic regeneration | Two complete independent artifact generations compare byte-for-byte canonical JSON |

## Validation status

Initial review demonstrated real acceptance failures for QA-S1-01 through QA-S1-05. These tests deliberately assert fail-closed expected behavior and remain permanent regression coverage. Final independent rerun pending remediation; do not claim final readiness from this intermediate report.
