# Stage 4 progress handoff — implementation milestone, NOT complete

Repository: DanTrackedFR/chief-accounting-officer. Branch: orchestration/multi-entity-multi-period-flagship. Existing Draft PR #37. Baseline main: 607146b622318ee18e33e1a7a74da490dfbb8a62. Do not create another branch/PR or merge. Obtain actual current remote head rather than relying on a self-referential committed SHA.

## Completed at this milestone

Live-main start gate and architecture reconstruction; one Draft PR; generic retained blocked-result propagation regression (S4-D01); qualified three-entity ordinary-loan accounting control with native US/UK FX, native IFRS loan reassessments, native Consolidation/Financial Statements and native Management Accounting analytics. Initial material reciprocal EUR10m/EUR11m difference blocks Group accounting/reporting. Separately reviewed NL correction to EUR10m creates a new version and selective six-consumer rework. The earlier prototype reached COMPLETE/CLOSED, but independent QA proved that conclusion premature because current timing/FX loan economics were omitted. A complete-population runtime guard now rejects that rework. The corrected clean control is NOT complete. Historical results remain immutable; unrelated US/timing/FX/temporal controls retain versions.

Authored milestone suite: 20 Stage 4 lifecycle methods plus seven generic conflict-governance methods and 84 existing Stage 2/3 authored methods passed (111 distinct methods). This is NOT full release regression or final QA. Later source-intake changes require fresh validation.

## Current implementation and exact next work

`tests/stage4_fixtures.py`: direct `initial()`, `correct()`, `reviewed_rework()`, `rework()` and new `intake_initial()`. The latter is being validated against the new generic `intake/governed.py` ReviewedInputPack bridge. It binds exact node/Scope/Period/calendar identity and original controlled source principals/rate inputs. Financial completeness of source populations is NOT yet a final acceptance claim. Preserve this work, diagnose its remaining failing gates, and extend actual source populations rather than weakening validation.

`stage3.py` now validates multiple qualified matched ordinary loans and multiple translated legal populations inside one native Consolidation. It retains exact counterparty/economic matching and native CTA bridge population checks. This is a generic minimum extension, not a replacement engine. Additional adversarial coverage and independent QA are still required.

`cases.py` corrects a second lifecycle defect: partial DOCUMENTED cases must reopen for material dependency rework even when their outcome was already partial. The generic proof currently reaches CLOSED after qualified correction. Add permanent standalone adversarial regression and independent review history for this defect.

Analytics control: financial-account movements and native diagnostic source-flux tie Group cash489 to490 (EUR millions), with supplied financing receipt1. Noncash payable correction income1 is distinct. Prior-year calendar comparator follows the existing owner contract. No analytics accounting treatment is inferred. The current supported scenario is a controlled finance-holding Group, not general commercial-company GAAP conversion.

## Outstanding mandatory gates

Complete source inventory, semantic-plan/intake integration and reviewed corrections; source/Fact lineage for all material populations; period/comparative/effective integration beyond metadata where required; exact-once legal/translation/Group ledger; generic public conflict/clean answers and privacy attacks; all required integrated adversarial categories; at least eight executable lineage chains; deterministic full artifact generator and hash-seed proof; genuine separate-context independent QA/remediation/rerun; every prior flagship migration; complete repository release regression and validators; final integration and durable-memory documentation handoffs; roadmap completion ONLY after substantive acceptance; immutable final SHA; required exact-head Actions; original PR ready/open/mergeable/reconciled/unmerged.

Do not claim Stage 4 complete, do not advance the roadmap, and do not start persistence/authentication. Government Grants PR #27/package, Borrowing Costs, Investment Property and accounting knowledge remain untouched. No independent final acceptance has occurred. No complete release regression or final Actions has occurred.

## Independent QA and latest continuation state

Separate-context reviewer authored 15 distinct intermediate attacks in `tests/test_stage4_independent.py` and reconstructed production contracts independently. The report is `STAGE4-INDEPENDENT-QA.md`. IQA01 (undeclared complete intake snapshot) and IQA02 (unsupported recharge/legal journals in ordinary Group framework reassessment) were reproduced, fixed generically and independently rerun. IQA03 remains OPEN: current timing/FX loan positions are absent from the Group TB and qualified relationship population. The new optional reviewed `ALL_CURRENT_LOAN_SIDES` contract in `stage3.py` rejects missing/duplicate current legal-result coverage before native Consolidation. The Stage 4 source opts into it. This restores safe failure; it does not finish positive accounting integration.

Latest authored 20-method lifecycle run: 14 PASS, six ERROR because corrected clean rework now refuses the incomplete Group population. Positive closure assertions remain intact. Earlier 46-method authored run passed before this stronger coverage guard; it is historical, not final acceptance. The complete orchestration discovery was interrupted after concurrent development made its results unsuitable for release certification. No full release result is claimed.

Generator `tests/generate_stage4_examples.py` now captures the actual rework refusal and writes INCOMPLETE acceptance state, stale/unaffected ledgers, reviewed initial source population and correction history. Obsolete generated final-success files are removed by the generator. Never restore their false completeness. Next run the generator only without a concurrently running discovery suite, which also invokes generators.

**Exact next implementation action:** reconstruct all currently governed local legal loan positions (including UK current timing payable and UK/US FX relationship), include each in native entity closing populations, qualify necessary currency/framework paths using bounded production contracts, and supply reviewed native Group elimination/reporting inputs consuming the exact actual result versions. Preserve timing/FX classifications and historical evidence; do not force them to zero or bypass the population gate. Resolve the positive control using qualified evidence and accounting owner execution. Then integrate correction/rework intake evidence, run retained positive assertions, and independently rerun IQA03 and all attacks. Continue the SAME branch and Draft PR #37 from actual pushed head. Preserve previous findings and do not restart Stage 4.

## Latest verified checkpoint validation

- `python -m unittest orchestration.tests.test_stage2 orchestration.tests.test_stage3 orchestration.tests.test_integrated_conflict_governance`: 91 distinct methods PASS after the complete-population guard. This is targeted compatibility, not every prior flagship migration.
- Stage 4 generator invoked independently under `PYTHONHASHSEED=19` and `941`: 35 checkpoint JSON artifacts, identical file sets and SHA-256 hashes. These represent INCOMPLETE safe refusal, not a final complete control. No generated JSON was manually patched.
- Independent intermediate suite: 17 distinct methods, 15 PASS and two hard FAIL retaining IQA03 population coverage and positive complete-control requirements. Test-local bounded legacy attack control is explicitly separate from full flagship acceptance.
- `git diff --check` passed for the published implementation checkpoint. Current local and remote repository trees matched before advancing the local branch. No final candidate freeze or exact-head release CI acceptance occurred.

Fresh continuation must fetch live main and the SAME Stage 4 branch, check whether the remote advanced, and resume from the current pushed branch head (the handoff cannot embed its own commit SHA). Do not restart implementation or create a replacement PR. Read this handoff, the full Stage 3-to-4 specification, architecture reconstruction, defect register and independent QA report before edits. The prior correctable source and all immutable results are retained in the generator's initial/correction checkpoint artifacts.

The population guard is an explicit opt-in reviewed full-population contract. Legacy absent-declaration chains are still bounded proofs, never proof of a complete objective. Extending or pinning full-population requirements must respect the sealed reviewed source contract and preserve legacy bounded cases. Do not disable this opt-in guard in the real flagship to regain CLOSED. Do not copy the independent test-local bypass into production or authored fixture.

Additional temporal gaps remain: the partial/effective interval is validated metadata rather than executed accounting work; opening/comparative observations presently feed the Group observation but not current native loan recognition. Additional intake gap remains: corrected and downstream replacement packs do not yet have fresh sealed raw-source inventories. Public analytics initial state is blocked with the Group dependency; useful available local analysis needs explicit evidence-backed public coverage. A full adversarial inventory and final distinct-suite release record have not been authored.

Preserved exclusions: no Government Grants package, Borrowing Costs, Investment Property, canonical approval, supplemental knowledge or standards mapping was edited. No persistence or authenticated governance was implemented. Roadmap remains Stage 4 NEXT/in progress, with no completion advancement.

## Fresh continuation milestone — sealed correction intake and independent perimeter finding

Live branch/main reverified at continuation start: branch `b66f36f1f79524a6650899dcd138338599068e1a`; main `607146b622318ee18e33e1a7a74da490dfbb8a62`. Existing PR #37 remains the sole workstream. No replacement branch/PR or merge.

`intake/governed.py` now separates source qualification from execution. `qualify_replacement` qualifies a fresh sealed single-node ReviewedInputPack against the retained exact graph/Case/objective/registries/incoming dependencies, without running any accounting owner. It rejects faithfully sealed obsolete receipts. Native certification, immutable publication, supersession/invalidation and selective reexecution remain ordinary CAO responsibilities. The fixture's NL correction and prospective downstream replacement packs now use fresh deterministic source inventories and complete workpaper snapshots; original intake evidence is retained. Qualification is not proof of Group source completeness or positive accounting acceptance. Generator retains fresh replacement intake evidence even when the native population guard refuses accounting.

Separate-context independent reviewer found IQA04: the full-population guard derived its perimeter from the native source and accepted empty/Group-only/unknown populations. Remediation requires a distinct nonempty registered legal perimeter and completeness against governed CURRENT/effective legal descendants of the Group. Hierarchy supplies this coverage boundary only, never consolidation authority or dependency edges. Four permanent perimeter attacks and seven sealed replacement tests independently PASS (11 distinct tests). History and limitations: `STAGE4-POPULATION-INDEPENDENT-QA.md`; suite `tests/test_stage4_population_independent.py`. IQA01/IQA02/IQA03 history remains unchanged. IQA04 is resolved narrowly; IQA03 remains OPEN.

Authored fresh replacement suite has 16 distinct methods. Targeted validation with Stage2/Stage3/generic conflict suites: 107 distinct methods PASS (16 + 91). These are checkpoint checks, not full release acceptance. All original positive Stage4 tests remain enabled and require the incomplete current Group population to be implemented. No complete Group result is claimed; final independent QA, all temporal integration, final artifact/release/roadmap/CI gates remain outstanding.

Exact next action remains native timing/FX integration. Independently reconstructed constraint: current NL timing needs a new native October owner result qualified from September closing/current opening. Current UK timing GBP30 must enter native translation and bounded IFRS reassessment. UK FX GBP16 and US FX USD20 need actual native translation rows and both exact qualified counterpart paths. Existing bounded reassessment validates only one translation plus an EUR-qualified legal counterparty; the minimum generic two-translated-side extension must preserve original transaction USD20, native owners, Scope/Case/Period, exact versions, signed legal carrying rows and no generated accounting authority. Supply separately reviewed legitimate rate/book/economic evidence, retain original TIMING_DIFFERENCE/FX_DIFFERENCE results, and do not force equal translated carrying amounts or manufacture offsets. A native whole-operation TB must balance from supplied real source populations. The Group completeness guard remains enabled.

## Native temporal milestone and durable continuation boundary

The current NL October timing execution is now an actual `intercompany-accounting` production node, `timing-current-ENTITY-NL`. Its independently reviewed October source binds `pairs[0].opening_book_a` to the exact September native `a_functional` version through an OPENING dependency; transaction principal/rate remain separately supplied source facts. This creates current NL economics instead of assuming a September balance is current. It is not yet consumed by qualified Group matching/transformation/accounting and therefore does not resolve IQA03.

`timing-effective-ENTITY-NL` executes native loan reconciliation within the governed September 20–30 included Period, with an actual PARTIAL_INCLUDED_PERIOD dependency and exact Group-observation dependency. `temporal_inputs.validate_native_sources` validates the optional governed effective interval against the actual Scope/owner/included Period and registered partial relationship at ordinary execution/correction entry. The workpaper supplies book/principal amounts; dates infer no recognition, drawdown or accounting allocation. This owner emits no new posting. An equal-value prior result replacement invalidates five actual direct consumers (match-timing, nl-opening, nl-comparative, timing-current-ENTITY-NL, timing-effective-ENTITY-NL) and Group observation transitively; unrelated owners/relationships remain current. Original prior and interval evidence remain retained history.

Five authored native temporal tests PASS. Separate-context reviewer added five ordinary-runtime temporal attacks, bringing `test_stage4_population_independent` to 16 distinct PASS methods (four perimeter + seven sealed replacement + five temporal); no new substantive finding. This is bounded step review, not final Stage4 QA. The reviewed complete-population guard is still active. Original material conflict and blocked Group reporting remain; corrected full control still refuses omitted timing/FX populations.

Checkpoint artifacts regenerate through the existing generator: 36 JSON files reproduce byte-identically under independent hash seeds 19 and 941, including new native temporal source/Fact/version/dependency populations and fresh replacement inventories. They remain INCOMPLETE safe-refusal artifacts; no generated JSON was manually patched. Roadmap remains in progress; no final release handoff or final candidate is claimed.

This run stops new substantive implementation at a reliable context/runtime continuation boundary. All useful implementation, authored tests, independent review/history and generated artifacts are committed and published to the existing branch; PR #37 remains Draft/unmerged. A fresh continuation must verify the actual remote head and read the entire original specification and committed progress/QA history. This is not an external accounting blocker or completed workstream.

**Immediate next action:** connect the new current NL timing owner to a separately reviewed current bilateral match with the UK October timing owner; retain the original cross-period timing match/version. Integrate current UK timing and both UK/US FX legal balances into complete native foreign-operation TBs with independently supplied reviewed capital/book/rate/profit/CTA rollforwards. Implement only the minimum bounded two-qualified-translation ordinary-loan reassessment extension needed by the FX counterparties; each signed translated row must bind the correct legal side and original economic/currency/principal identity. Do not choose rates or capital balances merely to obtain agreement, suppress residuals, or reuse historical matches as current. Qualify all current positions into Group dependencies, native Consolidation, reporting and analytics. Preserve the original EUR1m conflict and immutable blocked outputs. Fresh replacement qualification is available for each corrected/rework input, but snapshot qualification is never Group completeness or accounting acceptance.

**Outstanding release gates:** IQA03 positive complete population and legitimate COMPLETE/CLOSED; actual qualified full Group source chain for every current timing/FX position (including current NL timing); temporal participation in final Group accounting/reporting and comparative financial lineage; complete required permanent attack inventory including individual omissions; eight accepted full lineages; final genuinely independent review/remediation/rerun with zero substantive findings; truthful final lifecycle artifacts and prior flagship regeneration/migrations; full repository distinct-suite release regression and both validators; final integration and Durable Memory documentation handoffs; gated roadmap completion; immutable final SHA; required exact-head workflows and readiness protocol. Do not start persistence/authentication, reset useful newer work, create another branch/PR, merge, disable guards or claim final completion.

Latest combined checkpoint validation: `python -m unittest orchestration.tests.test_stage4_native_opening orchestration.tests.test_stage4_replacement_intake orchestration.tests.test_stage4_population_independent orchestration.tests.test_stage2 orchestration.tests.test_stage3 orchestration.tests.test_integrated_conflict_governance -q` — **128 distinct methods PASS** (5 native temporal + 16 fresh replacement + 16 separate-context independent + 91 retained Stage2/Stage3/conflict). Reruns are not added. Earlier complete Stage4/intermediate independent command reported 48 tests run with two failures/eight errors retaining incomplete positive-control/population gates; no successful full Stage4 run or release regression is asserted. `git diff --check` PASS. Actual main remains `607146b622318ee18e33e1a7a74da490dfbb8a62` at final checkpoint verification.

## Fresh continuation — bounded two-qualified-translated-side contract

Continuation verified live GitHub and cloned the existing branch at `e34121bdb68f23db815a580d666b52bc0ef02c98`; live main remained `607146b622318ee18e33e1a7a74da490dfbb8a62`. PR #37 remains the sole Draft/open/unmerged workstream. All previous implementation and QA history are preserved.

`stage3.validate_reassessment_sides` now permits the minimum bounded ordinary-loan route with two distinct qualified native translations, in addition to the retained translation/direct-EUR-counterparty route. Receivable binds positive asset input to `gl_a`; payable binds the signed liability row to positive `gl_b`. Each translated row must consume the exact current matched legal result and metric, with matching Scope, original economic identity, functional currency, presentation currency, source fingerprint, row category and sign. Equal-value different results and omitted mappings reject. This supplies no rates, remeasurement, balancing adjustment, Group residual disposition or generic conversion authority.

`cross_layer_receipts.py` requalifies both translation dependencies when producing a framework-to-Group receipt and preserves the payable's exact source metric/sign/native side in transformation records. Existing single-receivable receipts retain their original serialized fields. Permanent authored suite: `tests/test_stage4_two_translated_sides.py`, ten distinct methods. It executes GBP16 and USD20 through native translations and native IFRS reassessment and qualified Group dependency creation. It deliberately retains EUR16 versus EUR18, zero generated journals and historical FX_DIFFERENCE. A qualified Group dependency alone is explicitly **not executed Group accounting or clean closure**. The positive bounded control is not the actual full flagship; it has no completeness bypass.

Genuinely separate-context independent review: `STAGE4-TWO-SIDES-INDEPENDENT-QA.md`; permanent suite `tests/test_stage4_two_sides_independent.py`, thirteen distinct PASS methods. New substantive TSIQA01 reproduced a functional-currency substitution accepted by numeric-only native translation qualification. Generic runtime and exact matched-legal-source guards now reject it; independent rerun PASS. No unresolved findings remain **within this bounded extension review**. This is intermediate QA, never final Stage 4 acceptance.

**IQA03 remains OPEN.** The real flagship fixture has not yet integrated complete current timing/FX foreign-operation TBs, matching, conversion, Group source, reporting or public result. The real positive suite still fails: 48 distinct authored/intermediate-independent methods run, two failures/eight errors at retained incomplete population/closure requirements. No failure was skipped, weakened or converted into expected failure. The complete-population guard remains active. The original material conflict stays partial/blocked and corrected full closure remains refused.

**Exact next work:** integrate the current NL timing owner and separately reviewed UK October side using exact current matching while preserving original September/timing result history. Prepare independently supplied reviewed complete native US/UK operation TBs, book/capital/profit/closing/historical rate and CTA evidence for all current positions; preserve original GBP16/USD20 loan identity. Connect the new two-translated-side route to the actual full-operation populations with exact per-row legal lineage. The current bounded extension still requires a transaction-qualified translation operation; integrating a whole operation containing several transactions must preserve per-row economic identity rather than simply changing operation IDs. Do not choose convenient rates, leave an unexplained intra-Group carrying remainder, shrink populations or use the isolated bounded control as full-close acceptance. Native Consolidation has no generic asymmetric-loan residual accounting authority; unsupported treatment must remain blocked until independently reviewed native production-owner evidence/contracts support it.

**Remaining gates:** real complete timing/FX Group chain and IQA03 resolution; individual omission attacks; complete opening/comparative/effective participation and repeated-owner isolation; exact-once proof; required adversarial inventory; eight accepted end-to-end lineages; genuinely independent final QA/remediation/rerun with zero substantive unresolved findings; truthful final lifecycle artifacts; all prior flagship migrations and full repository release regression; final integration and Durable Case/Company Accounting Memory documentation handoffs; gated roadmap completion; immutable final SHA; required exact-head Actions and unchanged-head readiness. Do not implement persistence/authentication, create another branch/PR or merge.

Checkpoint artifacts remain the truthful INCOMPLETE lifecycle: all 36 generated JSON files reproduced identically under `PYTHONHASHSEED=19` and `941`, with no manual patching. Both canonical/standards validators PASS (157 approved topics, 347 capabilities, 1598 claims, zero errors). Protected accounting packages, canonical approvals and supplemental knowledge are untouched. Broader release probes and any new public-compatibility findings are recorded below; they are not a successful final release claim.

### Broader compatibility remediation in this continuation

Independent release probes discovered inherited PCIQA01/PCIQA02 public rendering failures and CRIQA01 stable partial-documentation reopening. These were reproduced, documented, generically remediated and independently rerun. Reports and permanent suites: `STAGE4-PUBLIC-COMPATIBILITY-INDEPENDENT-QA.md` / `tests/test_stage4_public_compatibility_independent.py` (nine distinct PASS methods) and `STAGE4-CASE-REFRESH-INDEPENDENT-QA.md` / `tests/test_stage4_case_refresh_independent.py` (six distinct PASS methods). Prior failed independent reproduction history is preserved. Actual typed identifiers, hashes, source notes, signoff metadata and arbitrary contaminated conclusions still fail closed. Static documented partial Cases remain DOCUMENTED; real changed/stale versions reopen through the ordinary lifecycle. Partial closure remains prohibited.

Shared public execution bytes are part of synthetic native certification fingerprints. Regenerate affected nested synthetic example certifications and prior flagship artifacts through the existing generators after these changes; do not manually amend fingerprints. This is fixture requalification, not promotion of accounting knowledge or modification of actual company approvals. No protected accounting or knowledge path changed.

### Verified continuation checkpoint gates and stop boundary

- Retained Stage2/Stage3/conflict, native temporal/replacement/perimeter, Stage3 independent and new bounded/public compatibility suites: **184 distinct methods PASS**. Separate new Case refresh suite: **six distinct methods PASS**. Combined distinct targeted total **190**, never increased by reruns.
- New bounded two-side/public/Case independent and authored suites: **38 distinct methods PASS**, already included in 190.
- Complete production-skill discovery: **1180 distinct methods**. The post-remediation full run had 1179 PASS and one artifact reproduction failure from an omitted Hedge/Inventory integration fixture requalification. Its existing governed generator was then run, and the exact failing method reran standalone PASS. This is 1180 distinct passing methods after the isolated artifact repair, not 1181, and not a claim of an uninterrupted all-green full command. All synthetic generated source/owner fingerprints were regenerated, never manually patched.
- Lease vertical slice: **17 distinct PASS methods**. Repository/canonical public tests: **53 distinct PASS methods**. Supplemental/independent knowledge: **401 distinct PASS methods**, plus all five supplemental validators. Both standards-evidence and canonical approval validators report zero errors.
- Full Stage4 authored/intermediate independent positive run remains **48 tests run, two failures/eight errors** at the retained IQA03 completeness/closure gates. Original assertions remain intact. The corrected real Case is not COMPLETE/CLOSED.
- Earlier broad orchestration discovery was started before the compatibility remediations and interrupted after source changes invalidated its release-certification value. No complete full-orchestration regression or prior-flagship all-green release claim is made. All ten existing orchestration artifact generators (Manufacturing, Diagnostic, Intake, SaaS, Treasury, Group, Scope/Stage1, Stage2, Stage3, Stage4) subsequently completed against the corrected code; Stage4 still generated truthful INCOMPLETE refusal artifacts.
- Final checkpoint Stage4 artifacts: **36 JSON files**, identical under independent hash seeds 19 and 941 after public/Case fixes. This does not replace final accepted lifecycle artifacts or prove eight complete lineages.
- Established CAO, Phase3 and standards workflow push triggers now include the **same existing Stage4 branch**, preparing exact-head release CI without a replacement branch/PR. Any checks on this incomplete checkpoint are not final release acceptance; the orchestration gate must still reject outstanding IQA03 tests.

This continuation stops at a context/runtime reliability boundary and preserves all useful work on the same branch and PR. It is not a completed Stage4 workstream and not an external accounting blocker. IQA03 and every previously listed substantive final lifecycle/lineage/QA/release/roadmap/readiness gate remain outstanding. TSIQA01, PCIQA01, PCIQA02 and CRIQA01 are resolved within their intermediate independently rerun scopes. IQA01/IQA02/IQA04 history remains preserved. Do not treat these bounded suites as final independent acceptance. No persistence, authenticated governance, general GAAP/FX conversion or parallel consolidation was started. Roadmap remains in progress. Protected Government Grants, Borrowing Costs, Investment Property, canonical approvals and supplemental knowledge remain untouched.

The additional broad Group/Group-independent/conflict regression command was interrupted at this reliability boundary rather than certified from a partial run. Its 61 Group methods are not claimed green or added to distinct passing totals. The native Group artifact generator and separate-context material-conflict acceptance reproducer passed after the Case refresh remediation. Complete Group migration regression remains an explicit continuation release gate, alongside all other prior flagships and full orchestration discovery.

## Recovered-head continuation — current October timing match

Live PR #37 was verified Draft/open/unmerged at recovered remote head
`38ca7739f3434af6bd04da78b227229f0a7468d7`. The supplied setup pack, all ten
requested committed handoffs/reviews and live owner contracts were inspected.
No remote reset, new branch/PR or merge was performed.

The real fixture now executes `match-timing-current` through the existing
`STAGE3_MATCH` contract. Its distinct observation purpose
`orchestration-current-match` separates the current October review from the
retained cross-period observation, without changing either transaction's
`timing` economic identity. Exact dependencies consume October
`timing-current-ENTITY-NL` and `timing-ENTITY-UK`; current matching uses their
native source-row fingerprints, signed roles, agreement, counterparties,
Cases, Periods and result versions. The original `match-timing` still records
the September/October TIMING_DIFFERENCE. No matching accounting authority or
journal was created. Current matching is not yet qualified Group elimination.

Prior-closing replacement now additionally invalidates this current matching
node transitively through the actual NL opening owner. The five direct temporal
consumers remain unchanged; transitive consumers are Group observation and
current timing match. Unrelated work remains current. Existing executable
temporal expectations were expanded, rather than weakened.

Separate-context intermediate review authored eight permanent attacks/controls
in `tests/test_stage4_current_timing_independent.py`; all PASS. Full review:
`STAGE4-CURRENT-TIMING-INDEPENDENT-QA.md`. Historical substitution, omitted side,
wrong economic/counterparty/Scope lineage and stale/superseded current versions
reject. No new substantive finding was identified in this bounded review; it
does not constitute final independent Stage 4 acceptance.

The reviewer also independently confirmed that unchanged EUR16/EUR18 cannot be
fully eliminated by existing ordinary-loan owner contracts. Source-supported
native legal remeasurement and a complete reviewed operation TB containing its
FX profit are a possible supported correction route. Fresh independently
supplied closing-rate/book evidence is necessary; rates must not be selected
solely to solve equality. No residual adjustment or CTA plug was invented.

Checkpoint validation: 112 distinct retained Stage2/Stage3/conflict/native
opening/replacement methods PASS; 54 distinct population/two-side/public/Case
methods PASS. New current timing methods and Stage3 independent coverage are
recorded in the PR publication result. Full Stage4 authored/intermediate
acceptance still runs 48 methods with two FAIL and eight ERROR at IQA03's
unchanged positive population requirements. These failures were not skipped,
weakened or reclassified. No release regression or final CI claim is made.

The governed generator now produces 37 truthful INCOMPLETE checkpoint JSON
artifacts, including `current-timing-match.json`. File sets and SHA-256 hashes
reproduce identically under independent hash seeds 19 and 941. No manual JSON
patching occurred. The full-population guard remains enabled.

**IQA03 remains OPEN and Stage4 remains INCOMPLETE.** Next integrate all current
timing/FX rows into complete reviewed native foreign-operation TBs, preserving
per-row transaction and signed legal lineage when an operation has multiple
transactions. Qualify current timing matching and both FX sides into Group
dependencies. If correction evidence legitimately supports native legal
remeasurement, retain original GBP16/USD20 and EUR16/EUR18 results, seal fresh
correction intake, supersede/rework exact dependencies and carry FX P&L once.
Unsupported asymmetric treatment must fail closed. Do not weaken the guard or
use isolated bounded controls as full-population acceptance.

Every outstanding final population/temporal/exact-once/lineage/adversarial/QA,
migration/release, final handoff, roadmap and immutable-head CI/readiness gate
listed above remains outstanding. PR stays Draft. Protected accounting packages
and knowledge remain untouched. Persistence and authenticated governance were
not started. Useful work is published on the same branch as an intermediate
checkpoint, never represented as the immutable final candidate.

## Focused reviewed correction milestone — Outcome B

Starting verified live head231ec80799739d93b75b5832076476ed84ffbbc8; same existing branch and Draft PR #37. New focused control `tests/stage4_correction_fixtures.py` uses the actual Stage4 Scope/Case/Period graph and unchanged native owners, extending it with exact FX translation/reassessment/Group dependencies before execution. The original full fixture and37 checkpoint artifacts remain unchanged. No legacy population bypass is used.

Separately reviewed synthetic opening ledger UK-IC-OPEN-02 changes pre-remeasurement GBP16 toGBP15, preserving USD20 principal, GBP functional currency, exact UK receivable/US counterparty identity and original closing quotes. Native Intercompany calculates GBP16 closing andGBP1 FX gain; native Foreign Currency carries the exact gain once in presentation with zeroCTA. Fresh sealed replacement evidence creates new CURRENT UK legal version74fef5a8839526cc6476b1a262b3597a43c8fab083c8889a94c2e0bfa0dbc1dc; original versionc98a94e6c56889dbf946b1cc7366d775a8a144be521b02349a895ee94f7b7fe8 is immutable/SUPERSEDED. Stage2 invalidates3 direct/5 transitive consumers, preserves20 unrelated versions and orders selective rework. Four exact current transformation receipts qualify. Group dependency16 is current, but Group accounting/reporting/analytics refresh to blocked versions. Case remains IN_PROGRESS/partial; COMPLETE/CLOSED is not earned.

Original and refreshed EUR16/EUR18 leave material EUR-2.00 **million**. Opening evidence changes native P&L but not closing carrying value. No supported asymmetric ordinary-loan elimination or reviewed closing-date evidence changing closing accounting is available. Complete whole-operation timing/FX populations and per-row legal lineage remain required. A separate trial corrects the other NL mismatch and still triggers the full-population guard, independently of that original conflict. Do not confuse this useful OutcomeB proof with IQA03 resolution.

Independent CQA01 exposed hardcoded translationprofit/openingbook under alternate opening14/nativegain2 evidence. Generic reviewed-ledger validation and an exact native-profit dependency remediate it;15 independent and17 authored correction methods PASS under19/941. Unresolved substantive correction-path QA findings0; material accounting residual remains unresolved. Focused retained/new suites230distinct PASS;10 selected native-owner and3 privacy tests PASS (243distinct total). Full Stage4 acceptance remains48methods/twoFAIL/eightERROR at IQA03, with no weakened assertion.40governed artifacts reproduce under19/941 (37 unchanged remote checkpoint +3 new correction files); no manualJSON editing.

Detailed evidence, version IDs, all affected/unaffected nodes, accounting/evidence limitation and exact remaining release gates: `STAGE4-CORRECTION-MILESTONE.md`. Independent history: `STAGE4-CORRECTION-INDEPENDENT-QA.md`. Existing QA history/guards are preserved. Stable focused work is to be published durably to the SAME branch/PR, then STOP; PR stays Draft, roadmap incomplete, no final release lifecycle or merge. Obtain actual ending head from live PR rather than embedding a self-referential commit SHA.

## Reviewed closing-date milestone — current accounting resolved, historical reporting evidence refused

Starting actual live head `99d15a5c711cd7bd3e0f0f7099ad0f002a856901`.
Fresh synthetic closing treasury/GL evidence now drives existing native legal
remeasurement: unchanged USD20/openingGBP16 → closingGBP18/FXgain2 → EUR18;
US EUR18 remains current. Original EUR16/EUR18 conflict is immutable. A fresh
same-date coherent quote sheet is validated against retained presentation quotes;
no rate solve, Group plug or rewritten original evidence. The earlier opening
correction fixture and all40 prior artifacts remain unchanged.

A new complete-operation control represents all8 current legal sides and4
relationships. Whole-operation signed carrying/native-profit rows and the parent
native correction profit have exact version dependencies. Native Consolidation
executes6 entries and genuinely produces cash490/profit3/closingequity490, with
all loan/investment accounts zero. The nine-consumer closing rework order and23
unrelated exact versions are derived from actual edges. Native current accounting
is proved; this is not merely a qualified receipt.

Financial Statements now legitimately refuses the inherited comparative489
against reviewed openingequity487. Separately reviewed complete comparative/
opening Group TB, legal carrying and cash/net-assets history are still required.
Do not rewrite the comparative, invent a residual liability3 or restatement,
or force completion. Ordinary CAO selective reexecution preserves current native
Group accounting while reporting/analytics/Group remain STALE and publicpartial.
Global journal release also correctly refuses stale downstream versions; native
journal inventory8 is not falsely called a released full exact-once ledger.

Pre-implementation inspected contract: `STAGE4-CLOSING-CONTRACT.md`.
Full durable evidence/results/version/order/blocker/remaining gates:
`STAGE4-CLOSING-MILESTONE.md`. Separate-context QA:
`STAGE4-CLOSING-INDEPENDENT-QA.md`. CLQA01 ignored presentation quote was
reproduced, generically remediated and independently rerun. New15 authored and32
independent tests pass; independent32 pass19/941. Unresolved substantive findings
within this reviewed milestone0; final IQA03 end-to-end acceptance remains OPEN.

277 focused orchestration +18 selected native/privacy methods pass (295 distinct).
Original48-method positive acceptance remains2 FAIL/8 ERROR, with unchanged
assertions.44 governed artifacts reproduce under19/941, original40 unchanged.
Both standards/canonical validators report zero errors. No final regression,
lineage, roadmap completion, handoff acceptance or exact-head green CI/readiness
claim. Publish all useful work to the SAME branch/PR and stop for owner review of
the exact documented comparative/opening accounting evidence requirement.

## Comparative/opening reconstruction — Outcome D, evidence still unsupported

Starting actual PR37/remote head2b8f827077fc3018868b7e3f64809eaa7ed11ce8.
See `STAGE4-TEMPORAL-EVIDENCE-AUDIT.md` and separate-context
`STAGE4-TEMPORAL-INDEPENDENT-QA.md`. Inherited comparative489 is dated2025-10-31;
current opening487/cash490 is October2026. No complete intervening Group history,
September2026 Group closing TB, issued comparative population or error/policy
chronology establishes the equity-2/cash+1 differences. Neither number is presumed
wrong. Current NLgain1/UKFXgain2 is noncash current profit, not a retrospective
bridge. Existing owner authority cannot infer missing historical accounting.

Native Financial Statements correctly refuses actual evidence. Reporting/analytics/
Group stay STALE, Casepartial/IN_PROGRESS, publicpartial. New governed audit artifact
retains source/registry/contracts/hashes/original/current versions; no new temporal
accounting version/restatement/supersession/invalidation is invented. Original44
artifacts and all solved current Group accounting are unchanged.

Independent TQA01 is OPEN: recertified fabricated numerical comparative/cash inputs
can pass the current-only reporting qualification because complete Group
comparative/opening version dependencies are missing. Permanent rejection regression
is retained as a hard FAIL, not weakened to acceptance.12 temporal methods11PASS/
1FAIL independently19/941; this is not all22 positive temporal attacks or zero
findings.572 distinct retained focused compatibility methodsPASS; original48
acceptance38PASS/2FAIL/8ERROR. Both validators zero errors; new audit byte-identical
19/941; diff checkPASS. No full release/finalQA/roadmap/CI/readiness claim.

Next requires separately reviewed full comparative and adjacent prior/opening
Group TB/equity/cash populations, intervening owner-supported movements and exact
Stage2 native temporal receipts consumed by reporting. If evidence establishes an
error/transition, execute Accounting Changes and preserve original/corrected lineage;
otherwise do not invent restatement. Read detailed contract/evidence audit before
implementation. Same branch/PR remains draft/open/unmerged. Protected work unchanged;
persistence/authenticated governance not started. Publish this useful audit durably
and stop under OutcomeD; no further unsupported accounting loop.

## Temporal model and generic TQA01 continuation checkpoint

Starting verified live head `1c480514e4ce36df8f1c85ee68f9b5821cf6905e`.
Same branch and draft/open/unmerged PR37. New controlled fixture
`tests/stage4_temporal_fixtures.py` preserves all earlier bounded controls and
historical evidence. Adjacent September2026 closing -> governed October1 opening
-> October2026 reporting have distinct native immutable versions. Prior-year
October2025 comparative489 remains separate presentation history.

Adjacent authorized gross TB retains cash490, receivables10/16, payables11/18,
and equity487. These are the original nonreciprocal loans, not a balancing
liability, fabricated year bridge or retrospective current profit. Current native
corrections legitimately produce profit3/equity490/cash490 as before. The controlled
stock evidence is synthetic supplied review; external company history and
approval authentication are not claimed. No twelve months are generated.

`reporting_temporal.py` generically qualifies exact producer/consumer identities,
versions/currentness, source fingerprints, Scope/Case/Period/calendar/framework/
currency, distinct relationship types and whole authorized TB populations.
Financial Statements now accepts a separately reviewed adjacent opening TB,
using it for equity/cash ties; comparative presentation is independent. An
empty classified cash population requires evidenced actual zero movements.
The full controlled new path executes native Financial Statements, reporting,
analytics, Group observation and normal CLOSED/complete. This is a positive
checkpoint, not final Stage4 acceptance.

Public synthesis now selects exact current Group Scope/Period reporting, keeping
historical native statements from multiplying the current result count.
Analytics describes the observed prior-year cash stock difference only; no
unsupported financing receipt or intervening-year movement is inferred.
Replacement fixture review preserves the sealed workpaper knowledge selection
rather than rewriting it after sealing. All original positive full-release gates
remain enabled; their inherited incomplete fixture must still be integrated
without weakening requirements.

Original TQA0112-method suite and112 combined Stage2/Stage3/replacement/temporal
methods PASS. New authored11-method positive/temporal/exact-once/rework suite and
initial20 independent methods passed before the explicit opening-version
extension; expanded independent rerun follows. Two independently reproduced new
findings were fixed and permanently tested. Exact current acceptance counts
must be reverified after final changes; seed reruns are never double counted.
New governed generator: `tests/generate_stage4_temporal_model_examples.py`.
New artifacts: `examples/multi-entity-multi-period-temporal-model/`.

Remaining: expanded independent temporal-chain rerun and required individual
rejections; full eight-lineage/source-intake proof; every retained Stage4 positive
acceptance gate; fresh complete final independent QA; deterministic accepted
artifacts; every prior migration; full release/validators; final integration and
Durable Memory documentation handoffs; gated roadmap; immutable SHA; exact-head
required CI; unchanged-head ready protocol. No persistence/authenticated
governance, protected knowledge/accounting edits, new branch/PR or merge.
