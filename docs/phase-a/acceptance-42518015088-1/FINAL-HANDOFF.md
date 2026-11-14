# Phase A engine release handoff

**CAO PHASE A CORRECTIONS — ENGINE RELEASE ACCEPTANCE: BLOCKED**

[PR #54](https://github.com/DanTrackedFR/chief-accounting-officer/pull/54) remains draft pending hosted receipt reuse and exact-head readiness. Checkpoints C, D and E passed. Checkpoint F is outstanding. The final PR conversation handoff records the immutable publication commit and the live checks at that commit.

| Evidence | Verified result |
| --- | --- |
| Frozen source and tree | `6b36ae0d9bb942ec4eacc199e59c099c4cc01133` / `608963d0d7bc1028f2eeecdd11f2264ad0efd095` |
| Independent reviewed source | `3c63a3a2b95df7907f547e8de64c7c68cf963910` |
| Base main | `97d0621331c6ad2a66b12ed09c0ec40c05c626b9` |
| [Hosted execution](https://github.com/DanTrackedFR/chief-accounting-officer/actions/runs/42518015088) | Attempt 1, job 128845178599, workflow 404963318, fresh execution. The original GitHub conclusion is failure at the acceptance-report step. |
| [Original artifact](https://github.com/DanTrackedFR/chief-accounting-officer/actions/runs/42518015088/artifacts/13633904464) | 13633904464, 2,135,324 bytes, 298 original members. SHA-256 `2d377c812a6df2c9bfb37bcdf9f2599937a6950852bc1bf8c59af3a933f14a61`. ZIP and member inventory are preserved in this directory. |
| Actual outcomes | All 4,012 distinct identities discovered, scheduled, executed and passed. Zero failed, errored, skipped or unexecuted. Zero suite setup/teardown failures. All 34 commands succeeded, and the source remained unchanged. |
| Mandatory coverage | 4,011 previous plus one new control, 63 historical remediation, 55 Phase A, 16 infrastructure and 33 previous affected, including 28 previously setup-blocked. Each has an actual success line. See mandatory.json. |
| Independent recommendation | Accept hosted accounting, engineering and governance evidence for issuance. Original independent review in the attempt directory, SHA-256 `c1ef0100663c9f5b62915df3e3313eeae124b8da237a3bcbba246729f4c33caf`. |
| Maps and proofs | 464 Python files and 2,745 execution inputs. Seed 109 and 971 HTTP output matched phase-a-v1, including numerical, restart and retry checks. See source-report.md. |
| Preservation | 8,910 unchanged active and two archived originals of 8,912. Separately 7,959 unchanged active and four archived originals of 7,963 accepted-main protected files. |
| Immutable receipt manifest | `build4/release/presumed-sources-attempt-ci-42518015088-1/release-regression.json`, SHA-256 `6e653312f199cbf49f506269636e68218dbbcfa6692c591b70ee629335e03651`. The governed receipt seals this original hosted manifest with the new inventory and pointer. |
| Version-2 inventory | `build4/release/presumed-sources-inventory-42518015088-1-v2.json`, SHA-256 `d429f7b19c8d1911b7f12d24614836f4fc6aa7af636aad6cdeacfea8511b42ec`. Covers the original ZIP, all member paths, hosted provenance and independent review. |
| New acceptance pointer | `build4/release/presumed-sources-accepted-42518015088-1-v2.json`, SHA-256 `416e0c2e081755029dc11a4a4a0abdb2fce91ecb67a514c314e5bf92e1fe4f38`. Historical and default pointers retain their original bytes. |
| Production verifiers | Profile 1.2 and Build 4 delegated verifiers both returned PASS, 4,012 tests and 8,912 historical files. Independent missing/corrupt evidence and changed-source checks failed closed. Both refused -O and -OO as required. See issued-independent-checks.json and verifier-negative.json. |
| Explicit local reuse | Production execute_release.py --reuse returned ACCEPTANCE_REUSED and release_accepted=true. Durable output in `build4/release/phase-a-reviewed-local-reuse-42518015088-1/execution.json`. |
| Hosted reuse and exact-head CI | Pending at publication. Checkpoint F requires successful exact-head hosted reuse, live checks, mergeability and safe readiness verification. |

## Suite reconciliation

The four counts in each row agree exactly by identity. Columns for all unsuccessful or absent outcomes are zero in every row and are retained in suite-reconciliation.json.

| Suite | Selection | Discovered / scheduled / executed / passed |
| --- | --- | ---: |
| orchestration/tests | `test_*.py` | 1377 / 1377 / 1377 / 1377 |
| skills/tests | `test_*.py` | 1616 / 1616 / 1616 / 1616 |
| skills/lease-accounting/tests | `test_*.py` | 17 / 17 / 17 / 17 |
| tests | `test_*.py` | 141 / 141 / 141 / 141 |
| knowledge/income-taxes | `test*.py` | 10 / 10 / 10 / 10 |
| knowledge/agriculture | `test*.py` | 83 / 83 / 83 / 83 |
| knowledge/insurance-contracts | `test*.py` | 35 / 35 / 35 / 35 |
| knowledge/derivatives-hedge | `test*.py` | 4 / 4 / 4 / 4 |
| knowledge/derivatives-hedge | `independent_review_tests.py` | 7 / 7 / 7 / 7 |
| knowledge/inventory-cost | `test*.py` | 262 / 262 / 262 / 262 |
| local_cao/tests | `test_*.py` | 55 / 55 / 55 / 55 |
| knowledge/borrowing-costs | `test*.py` | 16 / 16 / 16 / 16 |
| hosted_cao/tests | `test_*.py` | 127 / 127 / 127 / 127 |
| intelligence/tests | `test_*.py` | 72 / 72 / 72 / 72 |
| build4/tests | `test_*.py` | 60 / 60 / 60 / 60 |
| knowledge/government-grants | `test_*.py` | 39 / 39 / 39 / 39 |
| knowledge/investment-property | `test_*.py` | 12 / 12 / 12 / 12 |
| diagnostics/profile12 | `regressions.py` | 19 / 19 / 19 / 19 |
| diagnostics/profile12 | `governance.py` | 4 / 4 / 4 / 4 |
| diagnostics/profile12/remediation/accounting-qa | `test_accounting_qa.py` | 18 / 18 / 18 / 18 |
| diagnostics/profile12/remediation/engineering-qa | `test_boundaries.py` | 12 / 12 / 12 / 12 |
| diagnostics/profile12/remediation/engineering-qa | `test_governance.py` | 10 / 10 / 10 / 10 |
| tests/phase_a_release_infra | `test_*.py` | 16 / 16 / 16 / 16 |

## Exact next action

The authenticated GitHub connector has no workflow-dispatch action. The CLI and browser are signed out. Once the final PR comment confirms the published head, use GitHub Actions **CAO presumed user-provided source assurance**, select branch `feature/profile12-phase-a-integration-corrections`, and explicitly supply `build4/release/presumed-sources-accepted-42518015088-1-v2.json` as acceptance_pointer. An empty pointer launches the full regression. Do not rerun the original run. From an authenticated GitHub CLI the single equivalent command is

```bash
gh workflow run cao-presumed-sources.yml --repo DanTrackedFR/chief-accounting-officer --ref feature/profile12-phase-a-integration-corrections -f acceptance_pointer=build4/release/presumed-sources-accepted-42518015088-1-v2.json
```

Record new run ID, attempt and head, confirm the explicit pointer, inspect uploaded execution.json for ACCEPTANCE_REUSED and release_accepted=true, and verify job success. Recheck the live PR, mergeability and required checks. The workflow also listens to ready_for_review and its PR event has no dispatch input, so evaluate the no-rerun constraint before transitioning Ready. The protected default Build 4 pointer selects historical evidence. A bounded explicit verifier invocation selects this receipt. Avoid a default-pointer substitution, an empty-input run or a broad CI rerun.

## TrackedFR integration boundary

The original Pulse Restore fixed-assets register and other uploaded files still need end-to-end testing for monthly depreciation, remaining-life years/months, supplied NBV and accumulated depreciation, structured proposed journals, assumptions, Case-level scope and historical Case behavior. Issues #51, #52 and #53 remain outside this release. No further full accounting regression, merge or deployment occurred during this assignment.
