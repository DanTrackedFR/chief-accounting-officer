# TrackedFR Phase A — final implementation handoff

**Implementation complete; release NOT accepted.** All six findings have independently verified dispositions. No merge, deployment, complete historical accounting regression or new release receipt is authorized or claimed.

PR: https://github.com/DanTrackedFR/chief-accounting-officer/pull/54

Branch: `feature/profile12-phase-a-integration-corrections`, from accepted main `97d0621331c6ad2a66b12ed09c0ec40c05c626b9`.

Final production implementation SHA: `f3f78debd750f1ca86c6e7edc7019a353c7c2b11`. Independently retested published implementation/test candidate: `02767e0563acd965b26d16e79565a89f80ea8bfd`, Git tree `58a11c98026a7dd2a1b452d9deeec4e54155903b`. Subsequent publication contains evidence/documentation only; the final PR head is shown in the PR. The publication-source-map and independent engineering publication verification prove all ten staged local/published Git trees and stage-parent order. Git-data API commit metadata changed commit SHAs, not file contents.

## Six-finding disposition

| Finding | Classification/severity | Implemented disposition | Independent QA |
|---|---|---|---|
| PA-01 | Confirmed diagnostic defect / Medium | Shared exact Case scope validation; HTTP422 aggregated field requirements; safely evaluable row defects included; invalid source not staged; identity preserved. | PASS, accounting/governance and authenticated HTTP/durable tests. Issue50 updated. |
| PA-06 | Confirmed potentially material contract defect / High | `remaining_life` YEARS unchanged; `remaining_life_months` exact MONTHS; dual fields must reconcile; specific invalid inputs block affected row. Synthetic mismatch quantified12× understatement. | PASS,12/24/36/60 equivalents, residual/caps/periods, durable retries and journals. |
| PA-03 | Confirmed diagnostic defect / Low | Exhausted/negative/missing/null/nonnumeric/unsupported-unit/conflict requirements identify exact row field. No automatic disposal or invalid-row proposals. | PASS, mixed valid/invalid and fully depreciated in-use assets. |
| PA-02 | Policy-contract gap/enhancement / Medium | Explicit monthly/actual_days, recommended monthly for new monthly-close configurations, confirmed-policy precedence, explicit partial treatment; legacy no-election actual days unchanged. | PASS, independent calculations, May/February, leap helper arithmetic, additions/disposals, rounding and multimonth continuity. |
| PA-04 | Comparison enhancement / Medium | Supplied opening/closing NBV/accumulated comparisons, equation/status/variance and actionable malformed/ambiguous requirements; never overrides accounting or proposes balancing entries. | PASS, synthetic260,000 mismatch; original Pulse Restore untested because unavailable. |
| PA-05 | Confirmed structured-API gap / Medium | First-class `proposed_journals`, `applied_assumptions`, `balance_comparisons`; exact native workpaper lines, curated lineage, actual provenance, proposals only. Historical workpapers reopen unchanged without invented lineage. | PASS, all public routes, AP/assets, identical cost entries, mixed-row/cross-Case isolation, persisted reopen/idempotency and actual accepted-main store migration path. |

[Diagnostic register](diagnostic-register.md) maps each baseline reproduction, root cause, production path, correction, executable permanent test and final independent disposition. Original integration bundle `docs/acceptance/phase-a-revision4-bundle.zip` and Pulse Restore register are absent; no access to original uploads is claimed.

## Accounting policy and schema decisions

Remaining balance basis is `max(cost + supported additions − opening accumulated − residual,0)` and remaining life at period start/availability, not original cost/lifetime. Monthly full-month charge = annual straight-line charge÷12 = remaining balance÷remaining months. Partial monthly reporting/readiness/disposal requires explicit `actual_days_in_month`; otherwise the affected row is unresolved. Actual days retains inclusive calendar-day/year365/366 proration. Use exact rational/decimal arithmetic, final HALF_UP cent rounding and remaining-balance cap. Callers roll opening balances and remaining life forward for each period.

Confirmed applicable client company `asset_policy` governs before compatible explicit Case elections. Conflicts/unqualified policies block. Native established memory remains `CONTEXT_ONLY`, requiring explicit confirmation/resubmission into that scoped policy contract; autonomous binding-memory reuse is not implemented or claimed. No convention election keeps legacy actual days and is labeled unconfirmed engine default. The monthly recommendation is operational, not a universal IFRS/private US GAAP/FRS102/AASB requirement. Units-of-production does not falsely claim calendar convention or year/month assumptions.

`interfaces/source-case.schema.json` explicitly defines the required scope fields, years/months, optional comparison fields and balance basis, bounded election and confirmed-policy inputs. `interfaces/public-answer.schema.json` and its production allowlist define the three new structured arrays. Amounts are exact numeric decimal strings, consistent with existing public calculations; use decimal arithmetic. Guidance remains human-readable. Native `journal_entry_implications` remains empty, not repurposed. No posting authority is introduced.

Historical Cases lacking native row-lineage metadata retain original guidance, calculations and workpapers. Their new structured proposals array is empty with `integration.historical_journal_lineage` requirement and explicit limitation; it does not mean no historical proposal existed. Create a separately identified correction Case for new structured proposals. No historical read reexecutes accounting or silently rewrites a result.

## Focused validation

| Final selected suite | Methods | Result |
|---|---:|---|
| Fixed-assets/source/Profile1.1/public/fingerprint compatibility |176| PASS |
| Existing local/hosted authored and independent QA |91| PASS |
| Original13-finding diagnostic regressions/control scenarios |19| PASS |
| Historical remediation accounting compatibility |18| PASS |
| Historical remediation API boundaries |12| PASS |
| Phase A authored arithmetic/Case scope |16| PASS |
| Fresh independent accounting |16| PASS |
| Fresh independent engineering + retained fingerprints |32| PASS |

Total380 selected passing method executions,371 unique methods (nine fingerprint methods repeated in engineering review). Subtests exercise more combinations than method count. The new permanent Phase A population contains55 methods. Six independent Draft2020-12 source/public validations PASS. Additional standalone Phase A skill discovery30 PASS. Published-source rechecks: independent accounting16 PASS and engineering32 PASS at `02767e05`.

Final commands/logs are retained in this directory. Initial invocation/import errors and incomplete isolated compatibility-fixture closures are retained and explicitly resolved, not hidden. Existing assertions were retained/strengthened. Final legacy evidence-generating tests ran in a disposable detached worktree. These are focused/compatibility tests, not the complete release regression.

Independent accounting conclusion: **PASS**, fresh scenarios, HTTP/native equality, actual assumption provenance, backward-compatible year/day behavior and no unsupported conclusions. See [accounting-qa.md](accounting-qa.md) and published log.

Independent engineering/API/governance conclusion: **PASS**, actual original defect reproduction, HTTP semantics, schemas, lineage, privacy, native persistence, retries, isolation and historical reopening. See [engineering-qa.md](engineering-qa.md), actual historical red/green evidence and publication verification.

## Compatibility and preservation

Formal/Profile1.1 execution/source assurance and existing legacy calculation behavior pass selected compatibility. The new additive exact-byte bridge has separate accepted-main snapshots and tamper tests; historical witness/manifests/helpers are unchanged. New Profile1.2 results bind corrected implementation bytes; the old receipt is not reused for correction acceptance.

Historical preservation manifest: **7,963 protected existing files match accepted main exactly**, including historical releases, release evidence, examples, diagnostic evidence and source/prepared fingerprint witnesses. Legacy test-generated working fixture copies were restored from accepted Git objects; no historical change was committed/published. Real accepted-main persisted Case reopened over the final authenticated HTTP service:200, identical guidance/calculations and native-result digest, with owner execution explicitly forbidden. PR49 is unchanged.

## Assessment-only operational readiness

| Item | Finding and minimum safe next step | Tracking |
|---|---|---|
| Provisioning | Company/credential/lock registry is startup-only. Governed admin authorization and atomic audited registry publication/recovery needed; controlled restart remains supported. High before multitenant onboarding. | [Issue51](https://github.com/DanTrackedFR/chief-accounting-officer/issues/51) |
|2027|2026-only is an intentional profile support boundary, enforced in both source validation and shared qualification. Review2027 framework applicability/evidence/transitions, December–January continuity and separately release before first January close rehearsal. | [Issue52](https://github.com/DanTrackedFR/chief-accounting-officer/issues/52) |
| Capacity |200 rows aggregate across all source tables; over-limit result blocks without truncation. Measure bounded increase or design governed partitions/batches with dependencies, controls, persistence and performance QA. | [Issue53](https://github.com/DanTrackedFR/chief-accounting-officer/issues/53) |

No operational-limit redesign is included. [Operational assessment](operational-readiness.md) gives architecture, impacts, dependencies, scope estimates and priorities.

## TrackedFR handoff and remaining acceptance

Use the [precise integration contract](integration-contract.md), including input/validation/journal examples, actual policy hierarchy, useful-life migration and original-file retest matrix. TrackedFR must retest its original Phase A files including Pulse Restore and verify it can consume all accounting amounts from structured fields without guidance parsing. Inventory historical month-column mappings into `remaining_life`; independently assess impacted Cases/proposals, preserving originals and using explicit correction Cases. Successful old execution does not prove correct units, and proposed journals are not evidence of posting.

A separate release assignment must authorize the current complete source-bound accounting regression, fresh test inventory, versioned deterministic public proof selection, new receipt/artifacts, independent integrity/historical/governance verification and final exact-head GitHub checks. Existing workflows compare historical proof outputs and must use a separately governed versioned correction proof/acceptance path rather than overwriting old evidence. The original Profile1.2 receipt does not cover these changes.

Publication commit messages contain `[skip ci]` because existing automatic PR workflows would start the forbidden full regression. No workflow definition, check result or acceptance evidence was altered to manufacture green CI. Skipped/pending checks are not release acceptance. Mark Ready for Review after final evidence publication/verification; do not merge or deploy.

Work stops after publication. No further implementation or release work is in progress.
