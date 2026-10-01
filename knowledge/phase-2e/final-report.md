# Phase 2E — final 157-topic approval audit

Completed 2026-10-01 on `qa/phase-2e-157-topic-approval`. [Dedicated PR #10](https://github.com/DanTrackedFR/chief-accounting-officer/pull/10) remains open and unmerged. PR #9's revised two-track policy is integrated through base commit `69cd977371eeb514663feb40bd8a438cb0dc1cb6`. Phase 2D substantive work and 347/347 canonical capabilities are preserved.

## Final population

| Measure | Result |
|---|---:|
| Canonical topics individually processed | 157 |
| Topics moved from REVIEWED to APPROVED | 157 |
| Remaining REVIEWED / BLOCKED topics | 0 / 0 |
| Genuine unresolved accounting blockers | None |
| Canonical claim-register coverage | 157/157 |
| Registers containing material claims | 120 |
| Empty registers with documented non-normative scope review | 37 |
| Individually checked claims | 1,598 |
| Track A: direct-source checked | 90 |
| Track B: training-data checked | 1,508 |

Each topic has a signed, dated [individual review](reviews/) covering scope, independent accuracy challenges, period/entity gates, framework differences, relevant numerical examples, cross-topic consistency, per-claim disposition and blockers. The baseline status is REVIEWED. The canonical manifest links the individual review and exactly one register for every topic. Empty registers represent documented practice-only scope decisions, not missing normative research. Reviews identify their artifact inventory separately from their actual findings; they do not assert blanket operative-source verification of every historical link.

## Evidence assurance remains separate

| Underlying claim evidence status | Claims |
|---|---:|
| SOURCE_VERIFIED | 90 |
| MODEL_DERIVED_AUDIT_REQUIRED | 1,454 |
| PRIMARY_CORROBORATED | 51 |
| SECONDARY_CORROBORATED | 3 |
| CONFLICTED / NOT_RESEARCHED | 0 / 0 |

Only actually inspected operative provisions support SOURCE_VERIFIED. Track B records `Source: ChatGPT training data`, independent accuracy checks, reviewer/date, applicable period, scope and limitations. Existing corroboration labels remain intact. Training-data approval does not manufacture paragraph references, make training data authoritative text, or close the future direct-source assurance queue.

## Inventory reconciliation

The baseline contained 64 physical registers but only 63 manifest register references; just 59 of those references resolved to existing files. Four stale paths were corrected: TOPIC-03-009, TOPIC-13-010, TOPIC-13-011 and TOPIC-15-002. The existing TOPIC-16-006 register had no canonical manifest reference and was linked. This reconciled the baseline to 64 actual referenced registers; the audit then completed coverage to 157. See [the inventory evidence](inventory-reconciliation.json).

There are 195 physical topic directories, including preserved duplicate/retry folders. The structural validator reports 38 such directories without their own register. These are not 38 missing canonical topics: the canonical validator proves 157/157 unique canonical register paths. No competing substantive topic implementation was created.

## Corrections and challenges

Individual findings and batch commits contain the full evidence. Targeted corrections include the cash reconciliation bank/book direction, effective-interest schedule rounding, indirect cash-flow signs, recognition versus billing/control gates, UK 2026 lease/revenue transitions, materiality and policy/estimate distinctions, transaction allocation and restructuring boundaries, regulatory-capital aggregation, and sustainability units and jurisdictional timing. Relevant scenario amounts were recomputed; no live model or application execution is claimed where the repository only supplies an illustration.

The GHG unit example now correctly treats 0.4 t/MWh as equal to 0.4 kg/kWh; a one-sided conversion still fails. The September 30, 2026 FCA sustainability instrument was inspected and its 2027 commencement and comply-or-explain scope recorded. Future operative dates remain separate from current reporting requirements.

The final contract reconciliation linked 169 already-recorded period findings into claim rows that lacked effective_period and added 17 missing early-batch model-review dispositions from existing independent checks. It did not promote further topics or upgrade their authority evidence.

## Validation and regression

Validated code/evidence commit: [`7d5a49087661e7e94f56dcf2cabf7bed2b9b0b86`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/7d5a49087661e7e94f56dcf2cabf7bed2b9b0b86).
Successful exact-head CI: [run 36869350471](https://github.com/DanTrackedFR/chief-accounting-officer/actions/runs/36869350471).

- Standards-evidence schema/structural validator: 157 registers, 1,598 unique claims, **0 errors and 0 warnings**.
- Canonical approval validator: **157 APPROVED**, 347 capabilities, 157 register paths, 37 justified empty registers, **0 errors**.
- Accounting, schema, privacy and approval-contract regression suite: **53 tests passed**. The revenue tests also reperform the 46 linked scenarios.
- Negative approval tests reject unchecked propositions, unresolved conflicts, missing period/review evidence, unsupported source upgrades and unjustified empty registers.
- Nineteen completed audit batches contain 5–10 topics each. Validator and relevant regression checks were completed between batches. After the local execution environment became unavailable following batch 10, execution continued through GitHub Actions; final validation executes the PR head directly.

## Internal source-note privacy

No runnable production CAO application, response renderer or retrieval service is present. The applicable contracts are implemented in:

- [Executable public boundary](../../interfaces/public_output.py): explicit output-field and citation-field allowlists for answer context, answers, retrieval snippets, citations, tool output, user-visible logs and exports. Unknown metadata is excluded; contaminated allowlisted text fails closed.
- [Closed public JSON schema](../../interfaces/public-answer.schema.json) and [integration instructions](../../interfaces/README.md).
- [Automated privacy tests](../../tests/test_public_output.py), included in the passing 53-test run.

Tests cover both `Source: [source name]` and `Source: ChatGPT training data`, nested citation metadata and contaminated public text. They confirm that provenance is excluded while material accounting uncertainty, entity scope and effective-period limitations survive. A rejected contaminated record requires curation; the boundary does not silently delete substantive accounting caveats.

**Production integration and runtime verification remain pending** until a runnable application exists. Contract tests passed; no production runtime test is represented as executed. This dependency does not block the completed accounting audit. Internal evidence remains inspectable by repository readers; the privacy contract governs user-facing application output.

## Canonical tracking and files

The canonical manifest was updated before derived progress and roadmap in each batch and in final reconciliation. Final status is 157 APPROVED and no remaining accounting blockers. No Master Build Map was found.

Changed files include all 157 claim registers, all 157 individual QA records, targeted guidance/scenario corrections, 18 batch reports (batch 1 is recorded in its commit and individual reviews), the inventory reconciliation, two-track policy/schema, dependency-free validators, public boundary/schema, 14 regression test files, CI and canonical tracking. The exact file inventory is [files-changed.json](files-changed.json).

## Commits and handoff

| Batch | Topics approved | Commit |
|---|---:|---|
| 1 | 8 | [`83d2a346`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/83d2a346cc7b64fad13e4fa88a36c2f78f3bc23c) |
| 2 | 10 | [`c8309965`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/c8309965e603f9e6742b62d3b6eaa7c14b3008a3) |
| 3 | 9 | [`2fc14696`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/2fc14696e47b1997de37dbc4adf8e718b8d37fa4) |
| 4 | 10 | [`8d522998`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/8d5229982980decd61dff9e3a84a96eb930b0e99) |
| 5 | 10 | [`fda9d0e5`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/fda9d0e5206af986c8d37e5915a784c7faf83bc7) |
| 6 | 9 | [`602c12ad`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/602c12ad0d0cf83ede6bfc13644b8b450f262ee1) |
| 7 | 9 | [`9f1f4baa`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/9f1f4baad4844f3bfff1711d4b5832e42ccb3739) |
| 8 | 6 | [`0dd1e4cb`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/0dd1e4cb238e1d6606e9b43ae6914b472337f1e7) |
| 9 | 5 | [`406e786f`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/406e786f8ce6003a15ee4042a1a55e4e6db79f1b) |
| 10 | 10 | [`77e9e276`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/77e9e276d4376b9045de98b9266f55390ccee88c) |
| 11 | 10 | [`2e5d003a`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/2e5d003a32d5521b0b6f08139e33bb3adf2a3052) |
| 12 | 9 | [`62449865`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/62449865f5332c95c92c63d0728abbf5d1213716) |
| 13 | 10 | [`2d24557f`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/2d24557f1956bf0051290e07f1febe12a46c892f) |
| 14 | 6 | [`150b065a`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/150b065a6aa227e9bbf39703bbc4a5e28a33437e) |
| 15 | 6 | [`bcf328a8`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/bcf328a840daf80d8add88d927dc8727e5c4a084) |
| 16 | 8 | [`553aa97a`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/553aa97ac79a3642229d04aad67a7ca6aee2966c) |
| 17 | 8 | [`e0c7f461`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/e0c7f4610f554ce7a7cd04398d919ead3e3cc81a) |
| 18 | 7 | [`2a3907e5`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/2a3907e553b3c7905324c6145cd56f6f396d7f87) |
| 19 | 7 | [`29c9f626`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/29c9f6261887ed8e36fbdddc94c1642f867dee3d) |

Final contract enforcement: [`7d5a4908`](https://github.com/DanTrackedFR/chief-accounting-officer/commit/7d5a49087661e7e94f56dcf2cabf7bed2b9b0b86). This report and the final file inventory are added in the subsequent handoff commit. [All PR commits](https://github.com/DanTrackedFR/chief-accounting-officer/pull/10/commits) include the inherited PR #9 policy commits.

[Review PR #10](https://github.com/DanTrackedFR/chief-accounting-officer/pull/10). The PR has not been merged.
