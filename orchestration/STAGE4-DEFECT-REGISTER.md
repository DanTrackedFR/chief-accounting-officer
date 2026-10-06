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
