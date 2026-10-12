# Group accounting: independent baseline architecture assessment

Date: 2026-10-05. Reviewer: independent QA agent, fresh context. Scope: live repository reconstruction before flagship implementation. This document records code inspection, not acceptance or standards verification. Only QA artifacts are authored by this reviewer.

## Authoritative executable path

`orchestration/registry.py` obtains identity and contracts from skill frontmatter and `skills/production.py`. Metadata production status and callable execution are distinct. `production.assess_case`/`execute` is the governed owner boundary. It validates period/applicability, current canonical knowledge documents and approved claim population; executes `workflow.py`; balances journals; binds completion to an independent reviewer and an exact case/implementation fingerprint; and tests public rendering. No orchestration adapter may manufacture owner approval.

The default `DeterministicPlanner` decomposes supplied families in `FACT_ADAPTERS`, not all registered skills. At this baseline it has no consolidation, acquisition, intercompany, impairment or tax fact families. They can be registered production skills without default end-to-end selection support. Group accounting is consequently an integration extension, not merely a fixture addition.

`CAO.run` creates scoped nodes, graph dependencies from imports and handoffs, re-executes owners through production, verifies imported fresh results, challenges results, synthesizes conclusions, observes context candidates and renders before closure. Incomplete material nodes/open questions prevent CLOSED. A partial outcome is a documented unresolved conclusion.

## Actual native owner support

| Owner | Native support observed | Boundary needing explicit integration |
| --- | --- | --- |
| consolidation | Framework-specific control models, exclusion, aligned balanced entity TBs, account-level translation, reciprocal balance/transaction eliminations with per-entity caps, investment/equity/PPA opening journals, inventory/depreciable-asset profit elimination, supplied tax journals, NCI rollforward, retained-control and loss-of-control schedules, statement mapping, equity/CTA/cash bridges | Specialist schedules remain reviewed inputs. No automatic PPA valuation, acquisition-date profit cutoff, goodwill functional-currency reconstruction, rights-specific NCI allocation or tax computation |
| business-combinations | Ordinary current-period business acquisition, supported consideration and framework NCI choices, acquisition expenses, goodwill/bargain boundaries, bounded measurement-period adjustments and subsequent schedules | Opening acquisition cannot be replayed. Step/common-control/reverse/VIE routes and unresolved tax/NCI effects block. A purchase journal must not also be treated as another group's local-book posting |
| foreign-currency | Transaction monetary remeasurement separated from foreign-operation translation; reviewed quote/currencies, TB/net-assets/profit/dated-flow bridge, closing rates for assets/liabilities, owners/NCI CTA and bounded full disposal | Net investments, hyperinflation, exchangeability, hedges and partial disposal specialist boundaries. Translation output must attach to its operation and goodwill currency, not one scalar group FX total |
| intercompany-accounting | Bilateral principal, recharge allocation including cent allocation, local rates/book/GL reconciliation, settlement and FX journals with `journal_entities` index | Local-book journals are entity owned. Native owner does not eliminate group balances or unrealized profits; eliminator consumes confirmed principal once |
| asset-impairment / income-taxes | Registered separate owner routes; tax workflow uses jurisdiction/rate, current/deferred, allocation, acquisition and recoverability reviews | Existence does not prove group routing or bridges. Amount, affected asset/CGU, profit/OCI/equity/acquisition allocation and tax currency must be bound to consolidation |
| financial-statements / disclosure-management / management-accounting-analytics | Existing independent production/reporting and diagnostic owners | Group figures must be fresh typed owner results; caller-supplied matching totals are insufficient. Hypotheses remain propositions to test |

`skills/consolidation/engine.py` is a legacy/simple aggregation engine with explicit NCI/PPA/FX/profit exclusions. Production uses `workflow.py`. Evaluating engine.py alone would materially understate existing support.

## Integration hazards and required adversarial proof

1. Global `dimensions()` and `_handoff` currently demand equal entity/framework/jurisdiction/period/functional currency. Group producers intentionally span entities/currencies. Use a group-specific reviewed scope/operation binding; weakening generic dimension checks contaminates established workflows.
2. Runtime owner inputs are keyed by package and imports reject conflicting cases for that package. Multiple subsidiary FX/impairment owners need a bounded population adapter or explicitly supported repeated owner identity. Quiet overwriting loses entities.
3. Consolidation source entity IDs are not by themselves proof of legal control date, legal hierarchy, acquisition cutoff or stable perimeter version. Balanced TBs and memos do not establish those cross-owner relationships.
4. Consolidation account-level translation computes a balancing CTA while foreign-currency owner computes an independent net-assets bridge. Both routes must reconcile, with no duplicate translation or goodwill FX adjustment.
5. Native intercompany journals preserve entity identity in calculations, while generic journal output is flat. A group journal ledger must bind each journal to entity or group layer, currency, period and source; account and amount equality alone cannot authorize cross-book deduplication.
6. Generic `_economics` scans only selected top-level populations and keys journals by node plus journal digest. It does not guarantee every acquisition/IC/ownership/translation/group event is counted once. `_qualified_journals` offers gross debit/credit witness coverage and exact reviewed payloads, but existing event source validation assumes one reporting entity/currency.
7. Investment coverage and per-account caps are useful native controls. Acquisition equity, NCI adjusted profit/OCI and opening goodwill nevertheless remain supplied schedules; acceptance needs independently recomputed cross-owner ties and pre/post acquisition evidence.
8. Reporting tieouts must distinguish group expense, NCI attribution, OCI, equity and eliminated transactions. A cash-flow bridge cannot be certified by net cash balance alone.
9. Fresh owner rerun/hash checking and fingerprint signoff must survive group adapter caching and imported results. Source identity, amount, perimeter or dates changing must invalidate downstream reporting, analytics and closure.
10. Public boundary allowlists fields and rejects internal provenance tokens across registered routes. Group nested artifacts require deliberate curation; evidence/reviewer/fingerprint objects may remain internal. Test actual runtime public output and exports, not merely a token utility.
11. Existing clean lifecycle is only as strong as selected critical nodes. Missing group owners and negative-selection errors can produce falsely complete cases unless required evidence-driven routes are inferred.

## Independent acceptance matrix for later executable QA

The permanent adversarial suite will cover the following 25 categories. Every case must exercise a public runtime/flagship entry point and assert blocked/partial versus complete, affected descendants, concrete amounts and journal/lineage behavior as applicable. No tests have been claimed passed in this architecture assessment.

| # | Category | Attack or required proof |
| --- | --- | --- |
| 1 | Control/perimeter | Contradict voting percentage and substantive rights; omit controlled subsidiary |
| 2 | Framework control | VIE versus IFRS/UK routes and exclusion evidence |
| 3 | Acquisition date | Change actual acquisition/cutover date without profit schedule change |
| 4 | PPA | Consideration/net assets/goodwill mismatch and stale PPA |
| 5 | NCI basis | Framework-ineligible election and wrong ownership |
| 6 | Pre/post acquisition | Include pre-acquisition result or omit post-acquisition movement |
| 7 | FX rates | Wrong quote, rate date/category and absent rate evidence |
| 8 | CTA | Incomplete net-assets rollforward or balancing-plug reserve |
| 9 | Goodwill currency | Translate acquisition goodwill in wrong functional currency |
| 10 | IC reconciliation | Timing/principal/FX mismatch concealed by matched flag |
| 11 | IC balance elimination | Duplicate pair, outside perimeter and per-entity over-elimination |
| 12 | IC transaction elimination | Wrong family, duplicate elimination and omitted transaction |
| 13 | Unrealized profit | Upstream/downstream inventory and asset depreciation/unwind |
| 14 | Impairment | Wrong CGU/group layer, stale carrying amount and omitted posting |
| 15 | Tax | PPA/profit-elimination effects, wrong rate/allocation or unsupported recovery |
| 16 | Exact once economics | Aliased event IDs and reused records across owners |
| 17 | Entity/group journals | Local FX/recharge/PPA journal erroneously netted with group elimination |
| 18 | Entity contamination | Same account/amount from another entity silently accepted |
| 19 | Period contamination | Owner/schedule/reporting period mismatch and stale cutover |
| 20 | Currency contamination | Local versus presentation journal/rate mismatch |
| 21 | Stale results | Change source amount, owner result, perimeter or implementation |
| 22 | Reporting/disclosures | Missing required group ties or totals with wrong classification |
| 23 | Analytics/hypothesis | False management explanation against group bridge and comparators |
| 24 | Negative selection/privacy | Unrelated owner omitted; unsupported route blocked; all public routes curated |
| 25 | Incorrect closure | Required unresolved specialist/journal/lineage work cannot reach CLOSED |

Decision: baseline provides substantial bounded accounting methods and governance primitives, but no demonstrated integrated Group Accounting flagship. Completion must be established through concrete cross-owner bridges and executable adversarial tests; this assessment does not certify implementation absent from the baseline.

## Scaffold adversarial execution, 2026-10-05

Permanent reproduction: `orchestration/tests/test_group_independent.py`. Command: `PYTHONPATH=chief-accounting-officer:chief-accounting-officer/skills python -m unittest orchestration.tests.test_group_independent -q` from workspace. Initial execution: 13 tests, 6 failures. These are direct production architecture validators with real completed synthetic native workpapers; full flagship integration is still pending. A failing rejection assertion is an observed missing control, not an expected-failure waiver.

Observed missing controls:

- All consolidation receipts may be omitted, or impairment receipt alone omitted, without receipt validation rejecting.
- Acquisition activity selection may be omitted without period validation rejecting.
- Foreign-operation `operation_id` may name another operation while the goodwill receipt still accepts.
- Source selected revenue/expense of 250/150 may be replaced in translated TB by 1250/1150. Profit remains 100; activity validator accepts gross P&L inflation.
- NCI actual adjusted OCI may be changed to zero while `specialist_receipts.nci_oci` remains -21. Receipt binds the spare scalar rather than the NCI schedule it purports to qualify.

Successful rejection tests include stale result, substituted dimensions, inconsistent reporting scope currency, pre-acquisition inclusion and contaminated translated populations. Some additional integration relationships are being remediated concurrently; final acceptance requires a fresh rerun and runtime-level omission attacks after complete wiring.

Corrected rerun: 13 tests, **7 failures**. Replacing the acquisition object (rather than mutating a shared fixture dictionary in place) exposes an additional missing control: changing actual acquisition date to 2026-06-01 leaves the July activity cutoff accepted. Fixture receipt `facts_used` may alias input dictionaries; independent attacks isolate those references so incidental stale-result rejection cannot masquerade as acquisition-date validation.

## Integrated independent adversarial run

The suite now exercises the actual GovernedPlanner used by intake, nine native owners and the FS diagnostic recheck. The clean positive control reaches complete/CLOSED and produces group profit 285 and closing NCI 176. Primary conflicting IC source preserves partial/DOCUMENTED. The prior scaffold rejection assertions now pass after remediation.

Expanded execution: 19 test methods with 25 named runtime attack categories, seven independently re-sealed journal attacks, all registered public output routes and five fresh-source contradiction attacks. The 25 mutated-native tests check exact-case/stale governance plus bounded-route rejection; they do **not** establish substantive native correctness under newly approved wrong assumptions. The seven journal attacks reseal the synthetic payload review, and thus test actual journal omission/duplication/scope semantics rather than stale hash alone.

Observed integration failures (five subcases in the executed expanded run): fresh company exports and narrative source documents can contradict native workpapers while the final Case still closes. Reproductions preserve intake source provenance, generate new source fingerprints and refresh synthetic independent native reviews through `group_review_pack`:

| Source | Mutation | Observed outcome |
| --- | --- | --- |
| Parent TB | Cash 1380 to 9999 | complete/CLOSED |
| Subsidiary TB | Revenue -450 to -9450 | complete/CLOSED |
| SPA completion | Signed 1 July to signed 1 June | complete/CLOSED |
| Appraisal | Incremental land fair value USD100 to USD999 | complete/CLOSED |
| Currency policy | Subsidiary functional USD to GBP | complete/CLOSED |

`DocumentBinding` verifies fingerprint/metadata, which proves the reviewed document identity but does not verify its content against accounting fields. A separately reviewed workpaper cannot close an evidenced contradiction simply by certifying the document hash. Structured extracted assertions/population ties or explicit visible unresolved specialist contradictions are required.

Additional independently reproduced scope attack: change reporting Group's execution scope `level` from `group` to `entity`, retaining all native reviews and the reviewed Group journal payload. The runtime still reaches complete/CLOSED and publishes group postings targeting that declared legal-entity scope. Added permanent rejection regression. No legal-entity posting occurs externally, but the reviewable journal contract accepts incompatible layer meaning.

Acceptance remains **failed** pending remediation and a fresh full rerun. There is no independent completion claim.

## Second remediation review and bypasses

The initial five source contradictions and reporting scope-level attack are now rejected. Keyed TB populations and complete value comparisons also reject renamed source account identities and balanced extra omitted rows. Whole-decimal text capture rejects USD100.99. Native translation-only FX now accepts an actual empty transaction list only when translation is explicitly enabled; independent tests confirm zero monetary result without a fabricated item and reject disabled translation or an empty nonlist.

Latest executed complete suite: 25 test methods, two failing subcases (Parent and Subsidiary execution scopes relabelled `group`). All other included assertions passed, including 25 original runtime attack categories. The exact TextAssertion population is now manifest-bound, and simple omission is rejected.

One additional freshly approved bypass is independently reproduced and added permanently: modify SPA completion to June; omit its assertion; remove `business-combinations.source_semantic_controls`; refresh independent synthetic reviews, every downstream actual receipt/import and the scoped journal review payload. The integrated Case still reaches complete/CLOSED. Optional manifests permit a source-qualified integrated owner to downgrade to the legacy path. Requiring manifests for integrated owners whose source documents require semantic qualification can preserve legacy nonintegrated fixtures while preventing this downgrade.

Acceptance remains failed pending these two scope subcases and manifest downgrade remediation. Final rerun must include `test_fresh_review_cannot_downgrade_source_qualified_owner_to_no_manifest` (added after the 25-method run).

## Third remediation verification

Fresh full rerun passed 26 test methods in 57.836 seconds. Previously reproduced legal-source scope relabeling and freshly re-approved semantic-manifest downgrade are now rejected. Existing legacy owner workflows without qualified source documents retain their boundary. Native FX translation-only checks pass, and public output across every registered route remains curated.

A new independently reproduced net-equal component attack was appended after that run: change valuation CSV recoverable/goodwill/other assets from `900,180,700` to `900,0,880`. Fresh intake, native independent synthetic reviews, specialist receipts and journal review still reached complete/CLOSED at reproduction. Total unit carrying remains 880, so aggregate `unit_carrying` comparison misses the reclassification of translated goodwill 180 into other net assets. A component tie must preserve goodwill identity and its amount, not just the net unit total. This rejection subcase is now permanent within the fresh-document attacks.

A separate formatter regression verifies that an unrelated rejected management hypothesis cannot reject the acquisition contribution claim; its current execution passed against the completed live group graph. The public group summary uses current completed owner amounts and maintains acquisition functional currency versus group presentation currency distinction.

The passed 26-method run predates the newly appended impairment subcase and formatter test; it must not be reported as final independent acceptance for those additions.

Additional fresh legal-scope contradiction: replace SPA sentence `No earnout, prior interest or ownership change.` with `Contingent earnout USD500 is payable. Parent held a prior interest USD200.` Current source preparation and independently re-reviewed native pack still produce complete/CLOSED. Business-combinations appropriately blocks step acquisition when prior-interest inputs are populated, but the source SPA is only date-bound and its explicit unsupported scope facts never enter that method gate. Permanent source attack added. Acquisition legal-scope exclusions need source-level semantic qualification or a visible unresolved specialist scope; a signed document hash and correct completion date are insufficient.

Further complete rerun: **27 test methods passed**, 105.262 seconds. This includes component-level goodwill preservation and unrelated-hypothesis formatter behavior after remediation, all registered public routes, scoped journal coverage and legacy safeguards. The process started before the newly added earnout/prior-interest SPA source subcase, so the passing run does not resolve that last legal-scope finding. Independent acceptance remains conditional on rejection of that exact freshly qualified source contradiction and a final stable rerun containing it.

## Final independent acceptance — current implementation

**PASS within the explicit bounded flagship contract.** This final decision supersedes the historical failed/interim decisions above; historical reproductions remain permanent regressions.

Fresh execution against the completed implementation:

- Full independent module: `PYTHONPATH=chief-accounting-officer:chief-accounting-officer/skills python -m unittest orchestration.tests.test_group_independent -q` — **27 methods passed**, 112.869 seconds.
- Subsequently added material-receipt omission regression: `... python -m unittest orchestration.tests.test_group_independent.GroupIndependentContracts.test_material_component_and_attribution_receipts_cannot_be_omitted -q` — **1 method passed**, 4.309 seconds, exercising five separately omitted required receipts.
- Therefore **28 distinct independent test methods executed successfully** across these two commands. This is not a claim that the final 28-method file was rerun in one command, nor that root-authored tests are independent tests.

Named series include all 25 requested runtime challenge categories; seven freshly re-sealed journal omission/duplication/scope attacks; all seven registered public routes; ten fresh-source contradiction/bypass variants; two legal-source scope relabelings; and five newly omitted goodwill/NCI/analytics component receipts. Additional individual methods preserve acquisition cutoff, identity/currency/period, stale result, gross P&L, NCI schedule, pre-acquisition inclusion, manifest downgrade, unrelated-hypothesis and empty-FX-population checks. Several original category mutations intentionally test exact-case approval and stale governance; the freshly qualified source, manifest and journal variants separately challenge semantic controls beyond a stale-hash rejection.

The final fresh full run contains and rejects the earnout/prior-interest legal-scope attack. Actual source legal text must equal the separately reviewed normalized `qualified_legal_extract`; completion-date, fair-value, currency and NCI assertions retain specific primitive ties. This is reviewed extract coverage, not a general legal-language parser or autonomous business/control determination.

Latest architecture review confirms:

- Native owner approval and implementation/knowledge fingerprints remain authoritative; runtime does not create professional approval.
- Source semantic-control manifests prevent downgrade of source-qualified integrated owners; complete keyed TB populations preserve both account identity and values, including balanced omitted populations.
- Exactly one reporting group scope and separate legal-entity scopes govern source assembly. Evidence-only native implications cannot silently become another entity's postings. Consolidation-only events use complete gross line allocation and replay the qualified source TB into the current owner result.
- Actual translated goodwill and unit carrying amounts separately qualify impairment inputs. Aggregate-equal reclassification no longer hides an incorrect goodwill component.
- Consolidation NCI profit, OCI and closing amounts bind to Financial Statements. Actual translated post-acquisition contribution and actual statement profit bind to Analytics; an unrelated rejected hypothesis cannot certify rejection of the requested acquisition claim.
- The five scoped group note requirements consume completed Financial Statements assertions. Registered public routes pass the real renderer's allowlisting/provenance checks, and the group answer draws coherent figures from completed owners.
- The clean control reaches complete/CLOSED with group profit 285, OCI -105, closing equity 2360, NCI 176 and goodwill 180. The material conflicting IC source remains partial/DOCUMENTED. Native translation-only FX has an honest empty transaction population; disabled translation and an empty nonlist do not become completed monetary accounting.
- Narrow natural-source controls are separate reviewed single-owner workpapers. Their fixture semantic planner explicitly bounds scope and does not assert the full group reporting/posting bridge.

No unresolved reproduced defect remains in this tested bounded scenario. Acceptance does not expand it to multiple acquisitions/repeated owner populations, mixed frameworks, nested reporting groups, partial-goodwill CGU gross-up, step/common-control/reverse acquisitions, actual impairment-loss posting allocation, arbitrary legal source interpretation, external filing certification or tax-law/valuation generation. Those routes remain explicit specialist/unsupported boundaries. The integrated accounting example is the reviewed IFRS ordinary full-goodwill acquisition of one foreign subsidiary, with independently supplied tax/rates/valuation and controlled source populations; registered/native support is not evidence that every other framework has an equivalent completed flagship.

Ownership: reviewer authored only this QA assessment and `orchestration/tests/test_group_independent.py`; implementation, root-authored tests and generated artifacts remain separately authored.

## Final source-input refinement review

New supplied valuation cashflow, discount, terminal, unit/FV/undiscounted inputs and recoverable-as-actual-owner-result eliminate invisible fixture valuation assumptions. The governed entity contribution population computes Parent standalone profit from qualified entity balances; actual post-acquisition FX contribution and group profit remain separately bound. Three new fresh raw variants (recoverable 700 against actual 900, Parent 300 against actual 200, and net-equal Parent 115/Post 170 against actual 200/85) passed rejection checks, together with the newly required entity-contribution receipt omission.

One final independently reproduced lexical defect: appraisal `USD100,` replaced by `USD100,999,` still reached complete/CLOSED. The decimal capture rejected dot suffixes but accepted a prefix before a thousands comma. Permanent `test_formatted_appraisal_amount_cannot_be_prefix_truncated` added. Prior passing runs predate this new method; final acceptance must include its remediation. A formatted numeric token must be parsed completely or rejected, with ordinary punctuation still supported.

## Final stable full-module result — supersedes all interim decisions

**Independent acceptance: PASS for the bounded contract, with no unresolved reproduced defect.**

After the final implementation freeze and lexical remediation, the entire current independent module was executed in one command:

`PYTHONPATH=chief-accounting-officer:chief-accounting-officer/skills python -m unittest orchestration.tests.test_group_independent -q`

Result: **29 distinct independently authored unittest methods passed in 143.076 seconds.** This run includes every current test and subcase; it is not the earlier combined full/targeted count. Root-authored acceptance tests and repository-wide regression are separate evidence, not included in this independent count.

The current suite includes the 25-category runtime series, seven freshly resealed journal attacks, all seven public routes, thirteen fresh raw-source contradiction variants, six required component/attribution receipt omissions, legal-scope and manifest downgrade checks, and the dedicated formatted-appraisal token regression. Clean and primary partial controls, native FX guards and unrelated-hypothesis formatting also pass.

Final refinement review:

- Supplied valuation cashflow 990, discount 10%, terminal zero, FV/undiscounted values and unit entity are actual source candidates. Recoverable amount is compared against the completed native owner calculation. Supplied recoverable 700 cannot falsely overwrite actual 900.
- Consolidation's actual source population qualifies entity analytical contribution. Parent standalone profit is recomputed from the reviewed entity balances and statement classifications; Parent 300 or net-equal Parent 115/Post 170 cannot replace actual 200/85.
- Whole normalized SPA extract coverage and explicit price, NCI value, ownership and acquirer assertions preserve legal source scope and primitive ties. This remains a bounded separately reviewed extract, not an autonomous legal parser.
- The appraisal rule accepts the complete reviewed decimal token and required sentence suffix. Thousands/scientific/magnitude suffixes fail extraction rather than silently using an integer prefix. Numeric text assertions additionally preserve actual owner currency.
- Group scope identity remains the declared primary reporting group regardless of row ordering; legal/group layers retain the previously tested separation.

All previously reproduced failures are remediated and retained as permanent tests. The bounded IFRS ordinary full-goodwill foreign-subsidiary scenario, independently supplied professional valuation/tax/rates and explicit unsupported specialist routes remain the limits stated in the earlier final architecture review. No standards-evidence status, real reviewer approval or general filing/legal/valuation capability is promoted by this QA pass.

## Final source-dimensional hardening — stable acceptance

Following the last source-dimensional revision, the whole current independent module was freshly rerun with the same command above: **29 test methods passed in 142.876 seconds**, in one full-module execution. This supersedes the preceding historical timing/result for final acceptance. No unresolved reproduced defect remains in the bounded contract.

Two permanent fresh-source variants were added without changing the method count: IC principal denomination USD changed to EUR while the Parent remains functionally EUR; and the tax source's `LAND-1` identity changed to `UNRELATED-ASSET-1` with unchanged basis/amount. Both are rejected under freshly prepared and synthetically re-reviewed owner workpapers. The fresh raw-source series now has **15 variants**, plus the separate formatted-appraisal regression.

Reviewed final controls preserve the distinction between nominal USD125 and Parent functional EUR100: amount denomination is source-evidenced separately from legal-entity functional context and must equal the actual native pair contract. The typed IC receipt also compares actual A-functional balance to the Parent TB, actual B-functional balance to the subsidiary's USD FX-source TB, and requires unity rates on same-currency legs. This verifies reciprocal legal books before group elimination rather than trusting equal totals or a matched flag.

Acquisition tax qualification now compares common asset identity, carrying/FV adjustment and acquisition allocation against the actual identified PPA asset. Equal scalar DTL on an unrelated asset is insufficient. Acquisition date and legal-entity checks continue to apply.

These are orchestration/source contract controls; no new native accounting capability or source-evidence promotion is inferred. Group totals and the earlier bounded acceptance limits remain unchanged. Reviewer ownership remains QA assessment/tests only.

## Final source-evidence completion — current acceptance

After the final source-only additions, the entire current independent module was rerun again under the frozen implementation: **29 methods passed in 148.034 seconds**, in one execution of the full command above. This is the latest current acceptance result; previous timings are historical.

The matching raw and separately reviewed normalized SPA now expressly describes the operating team, service-delivery systems, substantive processes and recurring outputs supporting the supplied ordinary-business scope. Direct acquisition costs zero is a bound source fact. The appraisal's `LAND-1` identity and independently valued minority-interest FV USD200 each have exact native semantic assertions, alongside the existing monetary-token, currency and manifest protections. The additions supply source evidence without changing native accounting methods or group totals. Existing adversarial mutation markers remain active and all prior regressions pass.

**Final independent decision remains PASS within the explicit bounded contract. No unresolved reproduced defect remains.** This QA does not supply professional valuation/tax/legal approval or upgrade standards-evidence status; it verifies the governed application boundaries, concrete synthetic accounting calculations and adversarial behaviors stated above.
