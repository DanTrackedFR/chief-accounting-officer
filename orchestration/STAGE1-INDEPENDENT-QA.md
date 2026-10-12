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

Initial review demonstrated real acceptance failures for QA-S1-01 through QA-S1-05. These tests deliberately assert fail-closed expected behavior and remain permanent regression coverage.

Final independent rerun against pushed remediation milestone `ee7ee0b357e071108eca9f39948f3218a245a2df` (tree `eda4ab16962b5c65d02de1f34da02af73993edc1`):

`python -m unittest orchestration.tests.test_scope_independent -v`

**44 distinct independent tests passed, 18.273 seconds, zero failures/errors.** No implementation or fixture was changed by the reviewer. The only post-rerun reviewer change is this report.

Verified remediation:

- QA-S1-01: separate exact scoped child ReviewedInputPacks, exact declared source population versus actual fact lineage, and reviewed inventory fingerprint/metadata manifests; direct repeated-owner runtime independently checks source dimensions.
- QA-S1-02: deterministic producing node must match supplied owner plus governed posting Scope dimensions; native/event currency and bounded period must match governed Scope; allocation uses the existing gross-line exact-once allocator.
- QA-S1-03: qualified documents, population bindings and text assertions require registered origin Scope; supplied metadata agrees with origin framework/currency/jurisdiction. Shared Group policy is explicitly qualified through `applies_to_scope_ids`, retaining its Group origin; hierarchy does not authorize it automatically.
- QA-S1-04: selected execution and journal source/posting qualification reject inactive or outside-effective Scopes. This is bounded currentness validation, not a Case lifecycle engine.
- QA-S1-05: Group context id, exact source fingerprint and Scope/framework/currency must match actual Intake inventory; no fictional fourth lineage is accepted.

The supplemental same-Scope document metadata attack and effective interval/posting-currentness attacks passed on the stable rerun. Rejected inputs cannot yield a complete result; legitimate equal-value cross-Scope postings remain distinct. Existing clean Group execution used generic Scope registry and deterministic node identities. Ordinary single-entity Revenue executed complete through automatic one-Scope normalization.

Public artifact review: `examples/scope-repeated-owner/public-answer.json` reports NL EUR/IFRS, US USD/US GAAP, and UK GBP/UK GAAP separately. It explicitly states that no consolidated IFRS/EUR total is established, exposes unresolved US/UK conversion requirements, emits no posting journals, and leaks no internal execution IDs, source population identifiers or exact fingerprints. Its complete status means the bounded local-result observation objective is complete; conversion authority remains unresolved and outside Stage 1. Two independent complete artifact generations matched canonical JSON exactly.

**Unresolved substantive Stage 1 independent architecture findings: 0.** This reviewer acceptance does not assert repository-wide regression or exact-head CI completion; those remain parent-owned final gates.

## Final migration/prepublication independent acceptance

Independent rerun after migration and prepublication fixes at local commit `30f0a85255306f2e10c3903fb66d0280385b853f`, tree `87b1bc7a98fbe3f437e802c57598a6e0dd08e2bf` (same PR #34): **44 distinct tests passed in 17.578 seconds, zero failures/errors.** The earlier 44-test rerun is repeated validation of the same distinct suite and does not increase the test total.

The reviewer examined the intervening runtime Treasury handoff-owner resolution, explicit unresolved Scope Candidate validation/questions, initialization of current scoped question context, and generator document/reviewed-pack/adversarial witnesses. These changes preserve exact producing node identity, avoid semantic entity creation, and do not weaken scoped execution or public curation. No additional substantive finding arose.

Additional read-only independent reproducibility check: invoked `adversarial_results()` twice, confirmed identical sorted results for **52 distinct authored tests**, and compared the result with committed `adversarial-results.json`. Generated all **22** ordinary Stage 1 artifact payloads in memory and verified equality with their committed regenerated JSON files, including architecture/handoff document SHA256 witnesses and exact scoped reviewed-pack records. No generated artifact was manually edited by the reviewer. These authored-witness reruns do not increase independent or authored distinct test totals.

The final public artifact still reports three local revenue observations with original frameworks and currencies, explicit unresolved US/UK conversion requirements, no consolidated IFRS/EUR revenue total, and no posting journals/internal receipt fingerprints. **Final unresolved substantive independent Stage 1 findings = 0.** Repository-wide regression, immutable final candidate freeze and required exact-head CI remain separate parent-owned gates. Only this reviewer report was changed after the final independent rerun.
