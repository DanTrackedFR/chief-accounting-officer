# Independent release evidence review — final local acceptance

Reviewer: independent_review (fresh delegated reviewer; did not implement or issue receipt).
Reviewed source: 126c2f85ea37dc216bb8a732ed4394e4bfbc7e17.
Actual artifact: 13545745955, run 42297337399 attempt 1.

Conclusion: PASS for genuine downloaded evidence, regression reconciliation, source identity, historical preservation and issued receipt integrity. GitHub reviewed reuse and exact-head CI remain separate release gates.

Independently calculated ZIP SHA-256: 4fc7d563b6e2d90d690afdfc68351cafc3da7d0c5c95c68f581ff521963e41b7. ZIP length 1,412,552 bytes; 296 members; CRC passes. Download was performed by the parent through authenticated GitHub artifact tool; reviewer independently read the unchanged bytes and does not claim a separate download.

All 3,940 unique identifiers reconcile among discovery, release manifest, sidecars and actual verbose unittest success records. Sixteen success descriptions span two lines, so a single-line-only parser undercounts; the multiline reconciliation passes exactly. All 22 mandatory suites passed without failure, error or skip. Five remediation suites executed 19, 4, 18, 12 and 10 methods respectively. No exclusions or duplicate identities. All 33 manifest command exit codes are zero; all log SHA-256 values agree. The 65 orchestration shard sidecars and logs reconcile exactly with their aggregate suite. Execution status REGRESSION_COMPLETE_ACCEPTANCE_PENDING is consistent with regression completion pending receipt review.

All 453 Python-file bytes and 2,722 execution-input bytes agree with the frozen checkout. Canonical sorted compact JSON plus trailing LF produces source-map SHA-256 80aebee2ba308dcacb47c2e447071d120198cde4958cb7c3e125a89608f74191 and execution-input map SHA-256 c5e66b68d83f178f2a2c44a244ca2730055f94a928304a47332ae0d73ecc791d. Workflow bytes match 06fd70ffb1802947a3a4ea240f2afa181e6ca5c77341c937553bb30adefaf558.

Actual verify_historical() passed all 8,912 entries including the pinned authorized workflow migration: 8,911 unchanged entries and archived original workflow plus validated successor. This does not mean active migrated workflow equals its historical original.

Executed independent_check.py against the actual downloaded data and frozen source. Positive production validate_population passed. Mutations removing a suite, adding a skipped test, duplicating an identity and making a command fail were rejected. Both actual verifiers rejected a deliberately missing pointer under normal Python; both refused optimized Python at import with the required integrity error. No full regression was run.

Build 4 selection inspection confirms explicit pointer/environment conflict rejection and default current-release selection, with no silent historical acceptance fallback when Profile 1.2 exists. Receipt_integrity requires version 2, full immutable attempt inventory, distinct fixed-path outer-log/review attestations, sidecar equality, map equality and file digests.

Evidence-only equivalence is bounded: source_hashes includes every Python file, including release directories; release_input_hashes excludes non-Python files under /release/ while retaining mandatory remediation contract and diagnostic fixtures. Adding non-Python evidence under release directories can preserve source equivalence; adding Python evidence cannot. Final published tree must regenerate both maps and compare exactly before reuse. This is not permission to alter executable source or historical evidence.

Original TrackedFR uploads remain untested by this review. Post-issuance results follow below.

## Post-issuance independent challenges

Actual receipt `build4/release/presumed-sources-accepted-42297337399-1-v2.json` was copied with the complete repository into a disposable checkout. Both actual production verifiers accepted it under normal Python, each returning PASS, 3,940 distinct tests and 8,912 historical entries. Both rejected optimized execution, stale historical v1 acceptance and missing pointers. Profile 1.2 rejected independently altered/missing suite-17 JSON, independently altered/missing suite-17 log, and executable source drift. Restoring all original bytes restored positive verification. No shared source or sealed evidence was mutated. No full regression was rerun.

Commands: `python independent_check.py`; `python independent_receipt_checks.py`; `python independent-repo/build4/verify_release.py`. Challenge result sidecar: `independent-receipt-results.json` beside this report. The disposable scripts independently check actual downloaded data and call production verifiers; they do not manufacture regression fixtures or issue receipts.

Final independent local receipt conclusion: PASS. GitHub accepted-pointer reuse, final published-head map equivalence and exact-head CI remain release-agent gates. This report does not certify those future actions or original-upload integration.

Reviewed build4/release/presumed-sources-accepted-42297337399-1-v2.json SHA-256: f467f10c6da646432600e31657c795733dacbdc1b7e4eb046a2773e3365add5f

Reviewed build4/release/presumed-sources-inventory-42297337399-1-v2.json SHA-256: 3aba57f04087743e019ffd682eb39ea8b843e41e389de9f3982e7636ff77beae

Reproduction scripts are preserved beside this report as `independent_check.py.txt` and `independent_receipt_checks.py.txt`. Copy them outside the repository as `.py`; use a frozen checkout named `repo`, the downloaded ZIP extracted as `evidence`, and a disposable complete copy named `independent-repo`. Retaining scripts as `.txt` under the release namespace avoids altering the tested Python source population.
