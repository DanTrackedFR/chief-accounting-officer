# Stage 4 substrate defect register (implementation checkpoint)

## S4-D01 — material unresolved dependency cannot produce a retained blocked downstream version

Layer: VersionedExecution / VersionRegistry / CaseRegistry. Before remediation, an explicitly required unresolved bilateral match could not issue a safe current receipt; the runner either raised or, when only node status was inspected, a completed matching analysis could be mistaken for resolved accounting. The Group consumer had no retained blocked version with exact upstream bindings for subsequent correction invalidation.

Reproducer: `orchestration.tests.test_integrated_conflict_governance`. A generic Group observation receives both an actual Financial Statements result and an unresolved match. This is not a Stage 4 fixture/status override.

Minimum correction: derive blockers from actual required/material dependency bindings. Publish a schema-exact blocked governance record containing no accounting authority/journals, and preserve upstream version bindings. Reject fake complete publication and fabricated blocked records. Refuse current metric receipts from unresolved producers. Case refresh additionally recognizes unresolved producer payloads. Historical immutable versions and ordinary selective invalidation remain unchanged.

Authored validation: seven distinct regression methods PASS; existing Stage 3 + Stage 2 authored suites (84 methods) PASS. Independent QA and full release regression remain outstanding. This record does not claim final acceptance.

## S4-D02 — partial documented Case did not reopen for dependency rework

Layer: CaseRegistry.refresh. A partial DOCUMENTED/CONCLUDED Case could retain that status after material invalidation because reopening was nested under outcome changes, although the outcome was already partial. Reopening now depends directly on unresolved material currentness, while outcome and history remain governed independently. The authored lifecycle and generic conflict tests exercise this path; final standalone adversarial/independent closure acceptance remains outstanding with the positive full-population control.

## Independent findings — history and executable coverage

The authoritative independent history is `STAGE4-INDEPENDENT-QA.md`; permanent attacks are `tests/test_stage4_independent.py`.

- S4-IQA01: complete native intake snapshot omitted from declared population. Layer: governed intake qualification. Explicit source declaration/fingerprint checks added; independent rerun PASS.
- S4-IQA02: services/recharges entered bounded ordinary-loan framework reassessment and emitted legal journals from a Group node. Layer: Stage 3 native source validation and publication boundary. Reject recharge populations and legal journal output; independent rerun PASS.
- S4-IQA03: current timing/FX loans omitted from translated/Group populations while full objective closed. Layer: integration source coverage and native Consolidation receipt qualification. Actual current roster/match-side coverage guard now independently proves safe rejection. OPEN until genuine positive accounting/source integration and final independent rerun pass. Latest independent suite: 17 methods, 15 PASS, two hard FAIL for this finding. No balancing plug or fabricated accounting remedy was added.

A safe refusal is remediation of false completeness, not completion of the corrected clean control. No final release or zero-unresolved-findings claim is made.

- S4-IQA04: full-population source could erase/shrink its legal perimeter before constructing the required roster. Reproduced independently at the actual population guard (three initial failures; no successful native closure claim). Generic legal-scope/perimeter completeness checks now reject empty, Group-only, unknown and missing-one-real-entity populations. Four permanent attacks plus seven independent sealed replacement tests rerun PASS; complete history in `STAGE4-POPULATION-INDEPENDENT-QA.md`. This does not resolve IQA03 positive population integration.

Native temporal integration is now executable within bounded source contracts: ordinary current NL owner consumes prior closing as opening book, and an included-period native owner validates its exact effective interval at runtime. Five authored and five independently authored temporal regressions pass; details/history in the separate population QA report. These steps do not resolve IQA03 Group population completeness or establish final acceptance.

## TSIQA01 — native translation functional-currency substitution

Layer: governed native translation and bounded reassessment qualification. Separate-context review reproduced USD20 legal input certifying a native operation claiming GBP, preserving numeric values and receipts. Generic native runtime and exact matched-legal-source currency guards reject it. Permanent independent attack and thirteen-method rerun PASS: `tests/test_stage4_two_sides_independent.py`; full history `STAGE4-TWO-SIDES-INDEPENDENT-QA.md`. Resolved for the bounded two-translated-side extension. This neither resolves IQA03 nor establishes final Stage4 QA.

## PCIQA01 / PCIQA02 — inherited blocked public-output compatibility

Independent release probes reproduced blocked tax missing-fact output exposing the internal `case_id` key to the public boundary and ordinary `dependency:` prose being mistaken for a typed dependency identifier. Generic remediation translates only deterministic missing-fact field names into useful public requirements, preserving every requirement/caveat, and distinguishes actual no-space typed identifiers from ordinary colon-space prose. Arbitrary contaminated conclusions and real identifiers remain fail closed. Nine permanent independent methods and both original reproductions PASS. Initial failures, inherited-byte verification and expanded adversarial rerun are preserved in `STAGE4-PUBLIC-COMPATIBILITY-INDEPENDENT-QA.md`. Resolved within intermediate public compatibility review; not final QA.

## CRIQA01 — unchanged documented partial Case reopened on refresh

The inherited S4-D02 implementation reopened any documented unresolved Case even without changed evidence, versions or currentness. Independent reproduction loaded the exact checkpoint implementation against an ordinary native conflict Case and observed DOCUMENTED -> IN_PROGRESS/REWORK on an unchanged refresh. Generic refresh now distinguishes stable unresolved documentation from changed/stale result versions. Six permanent independent methods PASS, including real material dependency invalidation, equal-value current replacement, unrelated Case isolation and continued refusal of partial closure. Existing Group conflict test PASS. Full history: `STAGE4-CASE-REFRESH-INDEPENDENT-QA.md`. This repairs an overbroad S4-D02 correction while retaining its intended real-invalidation reopening behavior.

## CQA01 — focused correction translation ignored native profit / reviewed books

Independent correction-path review reproduced alternate opening14/nativegain2 translating as fixedprofit1/opening115. The source builder had selected accounting values from a correction-evidence boolean. Generic role-qualified preparation now reads and validates separately reviewed opening cash/position/capital, derives native actual gain/loss and binds the signed profit TB row through an exact dependency. Alternate corrected opening14 legitimately yieldsgain2/profit2/opening114 with unchangedclosing16. Permanent15-method independent suite plus17authored attacks independently PASS under19/941; unresolved correction-path findings0. See `STAGE4-CORRECTION-INDEPENDENT-QA.md`. This correction does not supply Group residual accounting authority. IQA03 remains OPEN; original/refreshedEUR16/EUR18 remains materialEUR-2million and theCase stayspartial. Full-population, lineage and release gates are unchanged.

## CLQA01 — reviewed presentation quote ignored during closing evidence preparation

Separate reviewer reproduced new closing sheet EUR/GBP1.20 being ignored while
retained native translation used1.00 and reported residual0. Generic
`closing_evidence.validate_quote_sheet` verifies finite positive supplied quotes,
triangle consistency and exact retained presentation inputs before new native
correction qualification. No rate/accounting output is calculated. Permanent
independent regression and32-method closing/population reruns under19/941 PASS.
Resolved within this milestone; prior histories preserved.

## IQA03 closing/current-population milestone and remaining reporting evidence

New same-date reviewed treasury/GL evidence through unchanged owners yields
GBP18/gain2, translatedEUR18/EUR18, residual0. Complete current population has
8legal sides,4matches and6native Group entries; Groupcash490/profit3/equity490.
Current population omission protection remains enabled. This establishes current
native Group accounting, not final end-to-end IQA03 closure.

Native Financial Statements refuses inherited comparativeequity489 versus actual
reviewed openingequity487. Separately reviewed full comparative/opening legal/TB,
net-assets/equity/cash history remains unavailable. No comparative overwrite,
invented residual liability/restatement or status override. Reporting/analytics/
Group observation remain STALE; Casepartial, globaljournalrelease refused.
IQA03 final acceptance stays OPEN, as do all final Stage4 release gates.
The native parent P&L exact binding and complete-operation cashbridge validation
were proactive risk fixes; not invented additional independently reproduced
findings. See `STAGE4-CLOSING-MILESTONE.md` and independent QA report.

## TQA01 — full Group reporting lacks exact comparative/opening qualification — OPEN

Separate-context temporal review reproduced native/arithmetic and ordinary reporting
acceptance with a fabricated recertified comparator and unsupported cash bridge.
The graph binds only current Consolidation; textual prior source labels do not
establish exact Group prior/opening result lineage. Permanent required-rejection
test remains hard FAIL (12 independent methods11PASS/1FAIL under19/941). No
expected-failure marker, acceptance rewrite or accounting source manufacture.
Details: `STAGE4-TEMPORAL-INDEPENDENT-QA.md`.

Actual unmodified source still correctly refuses: comparative equity/cash489 at
2025-10-31 versus October2026 opening equity487/cash490. Missing full intervening
Group TB/equity/cash history prevents supported OutcomeA/B/C. OutcomeD is retained;
no fabricated temporal source/version/restatement is supplied. Generic complete
native temporal mappings and evidence remain required; zero unresolved temporal
findings/final acceptance is not claimed. Current solved FX/Group accounting stays
unchanged. Full audit: `STAGE4-TEMPORAL-EVIDENCE-AUDIT.md` and governed temporal audit
artifact. Stop after durable same-branch publication; Stage4 remains incomplete.
