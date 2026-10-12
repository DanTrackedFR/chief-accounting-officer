# Focused IQA03 correction testing — Outcome B

Starting live PR #37 head: `231ec80799739d93b75b5832076476ed84ffbbc8`.
Same branch: `orchestration/multi-entity-multi-period-flagship`. PR remains Draft/open/unmerged. This is a focused durable milestone, not final Stage 4 release acceptance. All earlier QA history and the main complete-population guard are preserved.

## Evidence and native accounting

The separate deterministic synthetic source `UK-IC-OPEN-02` corrects a pre-remeasurement opening-book export transcription from GBP16 to GBP15. Its independently supplied opening operation ledger has cash100, receivable15 and capital115. The original ledger/export, native result and original FX_DIFFERENCE remain historical. The correction is synthetic reviewed fixture evidence, not authenticated real-company approval or an inferred prior-period restatement method.

USD20 principal, USD source currency, GBP functional currency, UK receivable legal side, US counterparty, agreement-fx, book-fx-ENTITY-UK, Scope, Case, Period, framework and the original 0.8 GBP/USD closing quote are unchanged. No desired EUR closing amount is supplied. A fresh sealed ReviewedInputPack includes a separate raw source inventory, exact source snapshot, Fact binding and receipt lineage. Source qualification executes no accounting and is not Group completeness.

Existing `intercompany-accounting/workflow.py` supports evidenced opening books and ordinary monetary remeasurement. It calculates GBP16 closing receivable and GBP1 FX gain, producing one UK-owned Dr intercompany receivable / Cr FX gain or loss journal. The actual native Foreign Currency owner then translates the separately reviewed bounded operation: EUR16 receivable, EUR1 profit and zero CTA. Native profit is explicitly consumed through an exact dependency and signed TB row; no translation legal journal duplicates it. The US legal USD20 payable and original EUR0.9/USD presentation quote remain current: EUR18 payable. The narrow existing IFRS ordinary-loan reassessment returns EUR16/EUR18 with no journals. Four current currency/framework transformation receipts independently revalidate.

The fixture's amounts are **millions**. Original and refreshed signed receivable-minus-payable residual: **EUR-2.00 million**, material and UNRESOLVED. Equal USD principals establish reciprocal identity, not resolution of unequal EUR carrying amounts. The correction changes native P&L, not closing carrying value. No plug, rate solve, asymmetric elimination, invented CTA or residual suppression was used.

## Immutable versions and selective refresh

Original UK legal version: `version:c98a94e6c56889dbf946b1cc7366d775a8a144be521b02349a895ee94f7b7fe8`.
New UK legal version: `version:74fef5a8839526cc6476b1a262b3597a43c8fab083c8889a94c2e0bfa0dbc1dc`.
Original is immutable/SUPERSEDED; new is CURRENT. The original matching conflict, native outputs and source identity are retained.

Stage 2 derives three direct consumers: `fx-translation-ENTITY-UK`, `match-fx-current`, `match-fx`. Five transitive consumers: `fx-reassessment`, `elimination`, `reporting`, `analytics`, `group`. All eight old consumer versions become STALE before rework. No affected set is hardcoded.

Deterministic actual execution order: UK FX translation → current FX principal match → retained FX-difference observation refresh → native FX reassessment → Group elimination → Group reporting → analytics → Group observation. Exact current receipts replace superseded receipts. Group accounting/reporting/analytics publish new blocked governance versions through their actual required dependencies; no accounting totals or journals are produced from those blocks. A current qualified IFRS/EUR Group dependency carries16.00, but it is not elimination authority or a complete Group result.

Twenty unrelated nodes preserve exact current versions: `uk-translation`, `fx-translation-ENTITY-US`, `translation`, `timing-current-ENTITY-NL`, `timing-effective-ENTITY-NL`, `clean-ENTITY-NL`, `mismatch-ENTITY-NL`, `timing-ENTITY-NL`, `timing-ENTITY-UK`, `mismatch-ENTITY-UK`, `clean-ENTITY-US`, `fx-ENTITY-US`, `conversion`, `uk-conversion`, `nl-comparative`, `match-timing-current`, `nl-opening`, `match-clean`, `match-timing`, `match-mismatch`.

The ordinary current-journal allocator selects the UK native FX adjustment once and excludes the superseded legal result. Translation carries the same profit in presentation only; reassessment has no journal; Group elimination is NOT_PRODUCED. No old+new legal accounting or duplicate elimination enters current economics.

Case: **IN_PROGRESS / partial**, never COMPLETE/CLOSED. Public answer refreshes to partial without unsupported Group totals or private source/review metadata. A separate trial corrects the earlier NL mismatch and reruns its genuine prerequisites; the unchanged complete-population guard still refuses incomplete Group accounting. This trial proves the original mismatch is not concealing an accepted full Group close. The main Stage 4 positive assertions remain hard failures.

## Independent review and focused validation

One substantive finding, **CQA01**, reproduced native profit loss under alternate opening14 evidence: owner gain2 was incorrectly translated with fixed profit1/opening115. Generic source preparation now reads/validates reviewed opening books, derives actual native gain/loss and consumes a second exact native profit receipt. Alternate opening14 yields profit2/opening114 with unchanged closing16. Permanent regression and five additional contradictory-ledger/profit-lineage attacks independently PASS. Full history: `STAGE4-CORRECTION-INDEPENDENT-QA.md`. Unresolved substantive correction-path findings: **0**. The material accounting residual is an unresolved accounting state, not a hidden QA defect.

Focused suites: **230 distinct methods PASS**, including retained Stage2/Stage3/conflict/independent, Stage4 opening/replacement/population/two-side/public/Case/current-timing suites,17 authored correction methods and15 independent correction methods. Native owner checks: five Foreign Currency tests plus five selected Intercompany/Consolidation/presentation tests PASS. Public-output privacy: three tests PASS. Total passing distinct focused methods: **243**; reruns are not additions. Initial local missing-file reconstruction and an authored attack setup error were corrected before these final passing runs; they did not justify test weakening or repository authority edits.

Retained full Stage4 lifecycle/independent acceptance: **48 methods, two failures/eight errors**, at existing IQA03 positive population/closure gates. Not skipped, weakened or expected-failed. No all-green Stage4 release claim.

Governed generators reproduce **40 artifacts** byte-identically under independent hash seeds19 and941:37 original INCOMPLETE checkpoint files are also byte-identical to the starting remote blobs; three new correction-path/attack/acceptance files live in `examples/multi-entity-multi-period-correction/`. The correction generator runs all32 correction attacks before writing acceptance data. No JSON was manually patched. The artifact retains original conflict, fresh ReviewedInputPacks, native results, versions/supersession, stale/unaffected states, rework, exact receipts, transformations, material residual, exact-once selection, Group refusal and partial public answer.

## Exact remaining accounting/evidence requirement and Stage 4 gates

Opening-book correction alone cannot resolve unchanged closing EUR16/EUR18. Reviewed closing-date legal/rate/settlement evidence capable of changing actual native closing accounting has not been supplied; alternatively, a genuinely supported production-owner residual disposition would need its own substantive accounting contract and evidence. Existing ordinary-loan owners do not authorize an asymmetric residual elimination. Do not select replacement values/rates to solve equality.

The focused FX operation TBs are explicitly bounded and must not substitute for complete US/UK operations. Complete timing/clean/mismatch/FX source populations, whole-operation per-row legal lineage, qualified transformations and every required Group dependency remain necessary. No complete-population declaration was removed or shortened. Required omissions, stale/superseded, wrong dimensions and equal-value wrong-lineage attacks remain permanent.

Outstanding overall Stage4 gates: genuine IQA03 positive complete population and COMPLETE/CLOSED; all final temporal/opening/comparative/effective financial lineage and repeated-owner isolation; full Group exact-once economics and required adversarial inventory; eight accepted complete lineages; genuinely independent final Stage4 QA/remediation/rerun; final lifecycle/prior-flagship migrations and regeneration; complete repository release regression and validators; final integration/Durable Case/Memory documentation handoffs; gated roadmap completion; immutable final release SHA and required exact-head CI/readiness protocol. No roadmap completion, PR readiness, Durable Case/Memory implementation or merge is authorized by this milestone.
