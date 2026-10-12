# Government Grants #34 — release handoff for PR #27

The existing `phase-3/government-grants-assistance` branch retains original PR head `f64d641d3439fceef27be06bd5b8795be71279c0` and reconciles merged main `a2c1aa351a63f245bc6279602f1610266a4859da` by a normal merge. Government Grants executes through `production.assess_case("government-grants", case)` and the existing native CAO, durable Case, local and hosted boundaries. There is no new accounting engine or automatic posting. PR #27 is the only publication destination; integration and merge remain the owner's decision.

## Actual support

See `skills/government-grants/FRAMEWORK-SUPPORT.md` and `methods.md`. The bounded release supports reviewed 2026 for-profit reporting: IFRS IAS 20; Australian AASB 120 Tier 1; UK FRS 102 Section 24 with an explicit performance/accrual election; and US business entities with evidenced early adoption of ASU 2025-10 Topic 832. Future mandatory adoption is not presumed. Nonadopters without a qualified policy remain blocked. Unsupported entity, period, scope, policy, condition, valuation and owner routes fail safely.

Supported methods include income and asset grant recognition, matching, new cash advances, deferred-income schedules, IAS 20/AASB deduction and US monetary cost accumulation elections, past-cost compensation, qualified nonmonetary transfers and simple monetary clawbacks. US nonmonetary cost accumulation is withheld until an independently qualified cost-to-entity asset-owner adapter exists. Complex basis repayment, prior advance conversion, changed assets, other owners' measurements and unsupported nonadopter analogies remain blocked. This is a bounded specialist release, not coverage of every transaction permitted by a standard.

## Independent assurance

All 172 original supplemental claims and their histories remain unchanged: IFRS 47, AASB 48, UK 32, US 45; SOURCE_VERIFIED 47, PRIMARY_CORROBORATED 29, MODEL_DERIVED_AUDIT_REQUIRED 96. The original eleven knowledge artifacts are hash preserved. The continuation knowledge reviewer challenged all claims, operative periods and model distinctions; 39 knowledge tests pass. The implementation reviewer independently executed 57 adversarial tests, with seven initial material findings permanently reproduced, corrected and retested, plus the subsequent controls recorded in its report. AI reviewer identities are stated accurately; these reports do not authenticate a human or replace real company certification.

Authored tests include 40 grant methods/controls and five actual native, SQLite restart, local and HTTP parity tests. Twenty-eight reproducible examples include complete, blocked and incomplete-certification outcomes, source/calculation/journal/public artifacts and hashes. Independent accounting numbers differ from the authored round-number cases. Missing or stale certification produces no executable journals.

## Historical preservation

The historical reviewer preserved 4,631 original/main files and independently compared full original, preceding accepted and current authorities. Prior 48 production skills, Borrowing Costs fingerprint repairs, canonical 157 topics / 347 mappings / 1,598 claims, supplemental packages and old release receipts remain intact. Reviewed successor references live in their separate Grants namespace; original artifacts were not rewritten. Identity changes are explicitly bijective and hash bound. Only exact approved blocked diagnostics change, with no accounting amounts, journals, completed owner results or public financial outputs changed.

The Insurance protection manifest is unchanged. Its exact prior roadmap is archived and hash verified; the updated roadmap retains that entire prior text before the continuation. Four legacy Grant cases still block with no calculations or journals. Permanent tests assert the exact independently approved topic, missing-review reason and handoff wording transition, retaining the old outputs. See the architecture reconciliation report and `skills/government-grants/release-evidence/`.

## Release evidence

`CAO_GRANTS_ATTEMPT=grants-pr27-attempt-002 python skills/government-grants/run_release.py` exited 0: **3521 distinct tests, zero failures, zero errors, zero skips**, all nine validators and whitespace gate exited 0. Source and execution inputs remained unchanged.

| Suite | Actual tests | Exit |
|---|---:|---:|
| orchestration/tests (`test_*.py`) | 1361 | 0 |
| skills/tests (`test_*.py`) | 1400 | 0 |
| skills/lease-accounting/tests (`test_*.py`) | 17 | 0 |
| tests (`test_*.py`) | 56 | 0 |
| knowledge/income-taxes (`test*.py`) | 10 | 0 |
| knowledge/agriculture (`test*.py`) | 83 | 0 |
| knowledge/insurance-contracts (`test*.py`) | 35 | 0 |
| knowledge/derivatives-hedge (`test*.py`) | 4 | 0 |
| knowledge/derivatives-hedge (`independent_review_tests.py`) | 7 | 0 |
| knowledge/inventory-cost (`test*.py`) | 262 | 0 |
| local_cao/tests (`test_*.py`) | 55 | 0 |
| knowledge/borrowing-costs (`test*.py`) | 16 | 0 |
| hosted_cao/tests (`test_*.py`) | 44 | 0 |
| intelligence/tests (`test_*.py`) | 72 | 0 |
| build4/tests (`test_*.py`) | 60 | 0 |
| knowledge/government-grants (`test_*.py`) | 39 | 0 |

Accepted manifest SHA-256: `5e28e7746506fd46c6ef7a765f2d6240b4ad56b26d5a722c29bb2b9a6bd16c3b`. Full command/log/source/input receipts: `build4/release/grants-pr27-attempt-002/release-regression.json`. The focused independent metadata retest executed 71 tests separately; those cases are also included in the full discovered population and are not added twice to the distinct release total.

The unsuccessful immutable-source attempt is retained and explicitly failed; it is not counted as acceptance. Its failures were legacy expectations about Grant availability/public diagnostics and the authorized roadmap continuation. Corrections were independently reviewed and retested. The final attempt executes every discovered test in all sixteen suites and all nine validators, with no skipped tests. Each command, exit status, actual distinct test ID, log digest and source/input SHA is retained. Existing full fresh-process persistence, recovery, Company Memory, Build 4 and historical deterministic tests execute normally.

The separate `build4/release/grants-pr27-accepted-release.json` points to the accepted continuation. `python -m build4.verify_release` verifies the final discovery population, logs, frozen inputs and preserved histories without replacing the old Build 4 accepted receipt.

## Publication gates

The final exact-head Actions and subsequent unchanged-head readiness receipts are recorded on PR #27 after publication. This local handoff is committed before those runs and does not invent CI references. Readiness is authorized only after the final source commit is green; all readiness-triggered runs must be verified on that unchanged commit. The existing orchestration workflow may explicitly verify a prior successful full run on the identical SHA; reused/skipped steps are identified as reuse, not a new test execution.

Exact publication SHA, all Actions run links and readiness-triggered unchanged-head verification are recorded on PR #27. No source is amended after those exact-head gates. PR readiness is not authorization to merge. No merge, ERP posting or authenticated reviewer identity is claimed.

A retained repository-test log was found truncated after execution. Its exact original 7,796 bytes were independently recovered to the pre-existing recorded SHA-256, with original manifest and suite-result bytes unchanged. The damaged prefix remains retained; independent adjudication and a fresh actual 56-test, zero-skip rerun are recorded under attempt002. No expected digest, test outcome, source input or historical accounting artifact was changed. See suite-3-byte-exact-restoration.json and suite-3-independent-recovery-adjudication.json.

Final publication whitespace validation preserves verbatim stdout in the two Grants release-attempt log folders. Five unfinished captured progress lines contain trailing spaces; these exact log paths disable only blank-at-eol normalization. Source and all other artifact whitespace rules remain active. Captured bytes and recorded digests are unchanged.
