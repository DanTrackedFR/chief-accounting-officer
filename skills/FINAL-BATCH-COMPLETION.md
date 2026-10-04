# Phase 3 final bounded batch — #30 / #48 / #49 / #50

Baseline live main: `eb915dea82831d4ff385591ea4c4265633957132` (39 production skills). Branch: `phase-3/db-controls-systems-operating-model`. Existing batch PR: **#22**. No merge authorized or performed. Skill #30 was explicitly released by the owner from the reserved queue for this batch only.

## Immutable mapping and bounded outcomes

`FINAL-BATCH-KNOWLEDGE-MAP.json` was committed before implementation in `6e7f79fbb5ec693f8c34959ae2cc1ef29548c339`. Its original bytes remain unchanged. It freezes 22 actual APPROVED topics, 46 selected capability mappings, 32 full original claim objects and every selected knowledge-document hash. These are a subset of the unchanged canonical universe, not new canonical topics or a supplemental namespace.

| Roadmap skill | Selected topics and capabilities | Supported executable boundary |
|---|---|---|
| #30 Defined Benefit & Other Post-Employment Benefits | TOPIC-05-005; CAO-05-010 | Qualified single-employer DB/OPEB supplied-source obligation/assets/funded-status workpaper in IFRS, US GAAP, FRS 102 and AASB contexts. Only the event-free, annual-calendar IFRS deficit pension bridge produces P&L/OCI/funding journals. |
| #48 Accounting Controls & SOX / ICFR | TOPIC-09-001: CAO-09-001/002/003; 09-002: 004/005/006; 09-003: 007/008/009; 09-004: 010/011; 09-007: 017/018; 09-008: 019/020; 09-009: 021/022 | Risk/control design, actual precision/IPE/person-level ownership, full calendar monthly/quarterly/annual occurrence/evidence readiness, qualified deficiency and retested-remediation workpaper. Not operating-effectiveness or SOX certification. |
| #49 Accounting Systems & Data Integrity | TOPIC-11-002: CAO-11-004/005/006; 11-003: 007/008/009; 11-004: 010; 11-005: 013/014; 11-006: 015; 11-007: 017/018; 11-009: 021/022 | Actual entity/book/master-data/access registry, physical source-target item/count/signed/gross/GL ties, mapping/version/dimension and cutover/EUC/AI accounting acceptance controls. No writes or technical-completeness certification. |
| #50 Accounting Operating Model & Team Governance | TOPIC-01-001: CAO-01-002/003; 01-002: 004/005/006; 01-003: 008; 01-004: 009/010; 01-005: 011/012; 01-006: 013/014; 01-007: 015/016 | Actual accounting services/team/RACI, retained accountability, measured peak capacity, qualified REQUIRED/RECOMMENDED/WORLD_CLASS/SHORTCUT_RISK judgments, sourced cadence/SLA and transition/automation dependencies. Actual #47 KPI imports only; no recreated KPI engine. |

All abbreviated capability suffixes in the table retain the row's domain prefix. The map contains the exact full IDs, propositions, original approval tracks, evidence statuses, confidence, audit flags, effective periods, entity/jurisdiction limitations and document hashes.

### Exact claim IDs

#30: `TOPIC-05-005-IFRS-001`, `TOPIC-05-005-UK-001`, `TOPIC-05-005-US-001`, `TOPIC-05-005-AASB-001`, `TOPIC-05-005-IFRS-E001`, `TOPIC-05-005-US_GAAP-E002`, `TOPIC-05-005-UK_GAAP-E003`, `TOPIC-05-005-AASB-E004`, `TOPIC-05-005-IFRS-E005`, `TOPIC-05-005-US_GAAP-E006`, `TOPIC-05-005-UK_GAAP-E007`, `TOPIC-05-005-AASB-E008`.

#48: `TOPIC-09-001-SEC-E01`, `TOPIC-09-001-OTHER-E02`, `TOPIC-09-002-SEC-E01`, `TOPIC-09-002-OTHER-E02`, `TOPIC-09-003-SEC-E01`, `TOPIC-09-003-OTHER-E02`, `TOPIC-09-004-SEC-E01`, `TOPIC-09-004-OTHER-E02`, `TOPIC-09-004-OTHER-E05`, `TOPIC-09-007-SEC-E01`, `TOPIC-09-007-OTHER-E02`, `TOPIC-09-007-OTHER-E03`, `TOPIC-09-007-OTHER-E04`, `TOPIC-09-007-OTHER-E05`, `TOPIC-09-008-SEC-E01`, `TOPIC-09-008-OTHER-E02`, `TOPIC-09-008-OTHER-E03`, `TOPIC-09-009-SEC-E01`, `TOPIC-09-009-OTHER-E05`, `TOPIC-09-009-OTHER-E06`.

#49 and #50: actual practice-only topic registers contain **zero claims**; none were manufactured. #48 SEC claims are retained map context, not a rule that every IFRS/US/UK/AASB entity is subject to SOX. Operational/practice routes apply no fabricated normative claims or framework differences.

## Precise remaining knowledge/scope gaps

#30 is not an actuarial valuation engine: no mortality selection, yield curve, discount-rate derivation, census present-value valuation, plan-asset valuation or actuarial certification. US ASC 715 expected-return/amortization/presentation, FRS 102 and AASB detailed journal mechanics, OPEB detailed presentation, surplus/asset ceiling/minimum funding, amendments, settlements, curtailments, FX, multi-employer and other-long-term routes require separately governed methods and fail closed. No IAS 19 mechanics are transplanted to other frameworks. The ordinary payroll/defined-contribution owner is unchanged.

#48 does not determine legal applicability, invent deficiency severity, execute controls or issue an ICFR/audit opinion. Non-calendar or other occurrence-frequency methods are outside this executable calendar. #49 is accounting governance, not ERP engineering, migration execution, cybersecurity or automatic accounting correction. #50 invents no staffing ratio, maturity score, headcount, benchmark, employment action, ROI or IPO conclusion. Existing #43/#44/#47 ownership is preserved.

## Implementation and independent QA

All four packages use the existing Phase 3 production envelope, canonical retrieval, exact case/knowledge/implementation digests, preparer/reviewer separation, complete independently frozen populations, supplied-source document digests, release-payload approval and seven-route public allowlist. Every supplied owner result must be complete/current/unaltered/dimension-matched, imported evidence-only and reconciled exactly once to an actually used numeric source assertion. Unsupported governance facts cannot authorize substantive monetary accounting.

Fresh independent reviewer authored `tests/test_independent_final_batch.py` and `FINAL-BATCH-INDEPENDENT-QA.md`, inspected actual knowledge and designed fresh counterexamples. Five initial false-COMPLETE defects (risk document binding, monthly occurrence coverage, empty systems/process scopes, retained accountability) were corrected and independently rerun. Later two false-COMPLETE variants of one KPI-ownership defect were corrected with typed/named actual #47 linkage; valid owner handoff still completes. Root review additionally strengthened actuarial feature flags, annual expense/OCI GL openings, parsed expectation chronology, full source/target access population and existing employee-benefit retrieval preservation. Independent rerun passed at report-anchored bytes. No unresolved production blocker remains within the stated bounded scope; external source authenticity and human qualifications still require actual qualified case review.

## Synthetic examples and fingerprint regeneration

Normal generator: `PYTHONPATH=skills:skills/tests python skills/tests/generate_final_batch_examples.py`.

Eight supported example routes: four distinct #30 supplied-report workpapers, one IFRS journal bridge, and one operational/practice route each for #48/#49/#50. **40 new JSON files**: 8 unsigned cases, 8 blocked cases and 24 public outputs (complete/partial/blocked). Complete remains complete; unsigned remains partial; forbidden actions block. Public artifacts contain no raw source notes, evidence internals, reviewer identities or hashes. IFRS example separately reconciles opening deficit 200, closing deficit 210, expense 68, OCI loss 12 and funding 70 with three balanced journals.

The existing shared implementation architecture also invalidates nested synthetic certificates in prior policy/disclosure and adjusting-event examples. Their normal existing generator refreshes only those dependency/case certificates and associated synthetic memo hashes. Prior accounting amounts and public outputs remain unchanged. No real approval is refreshed automatically; stale certification tests continue to reject changed bytes.

## Regression and integration gates

Stable candidate regression: authored final-batch tests **66 PASS**, independent final-batch tests **51 PASS**, full shared suite **633 PASS** (includes authored/independent/cross-skill/privacy/stale/malformed suites), lease **17 PASS**, repository **53 PASS**, supplemental tax **10 PASS**: **713 tests total without double-counting**. Standards-evidence, canonical approval and supplemental validators PASS; git diff --check PASS. Exact-head candidate CI is a prerequisite for promotion; final production metadata then requires fresh generated fingerprints, another complete regression and a separate exact-head green run. The final committed-head SHA and run IDs are recorded in PR #22 metadata/checks, not inferred from this self-containing report.

An early shared-suite run overlapped implementation edits and observed one stale intercompany certification; isolated unchanged-contract rerun passed. It is not counted as the final stable regression gate and no old contract was weakened to bypass it.

Canonical approval validator confirms **157/157 APPROVED**, **347 capabilities**, **1,598 claims**, 90 DIRECT_SOURCE_CHECKED and 1,508 TRAINING_DATA_CHECKED approvals; evidence remains 90 SOURCE_VERIFIED, 1,454 MODEL_DERIVED_AUDIT_REQUIRED, 51 PRIMARY_CORROBORATED and 3 SECONDARY_CORROBORATED. Supplemental validator confirms **64 APPROVED Income Tax claims**. Actual evidence fields and audit flags remain unchanged; APPROVED is not SOURCE_VERIFIED.

No knowledge/, architecture/ or public renderer files were changed. Government Grants, Borrowing Costs and Investment Property remain unchanged NONPRODUCTION/fail-closed. Reserved #24/#29/#38/#39 artifacts/queue are unchanged. This batch does not reopen any of them.

Promotion disposition remains gated until exact-head CI: four bounded candidates at 0.9.0/review; 39 current production skills, **43 projected if all four are gated, promoted and later merged by the owner**. Keep PR Draft until all final gates pass. Do not merge or begin another batch.
