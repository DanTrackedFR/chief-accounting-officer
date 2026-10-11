# Build 4 full regression manifest

Accepted attempt: `attempt-003`. The fresh complete run passed **3,226 distinct tests**, with no failures, errors or skips. All 14 suite populations, seven validators and whitespace checks passed. Targeted reruns and prior attempts are not added to this count.

| Suite | Distinct tests | Seconds | Result |
|---|---:|---:|---|
| orchestration/tests / test_*.py | 1344 | 3141.222 | PASS |
| skills/tests / test_*.py | 1180 | 214.878 | PASS |
| skills/lease-accounting/tests / test_*.py | 17 | 0.001 | PASS |
| tests / test_*.py | 53 | 0.223 | PASS |
| knowledge/income-taxes / test*.py | 10 | 0.005 | PASS |
| knowledge/agriculture / test*.py | 83 | 0.024 | PASS |
| knowledge/insurance-contracts / test*.py | 35 | 2.329 | PASS |
| knowledge/derivatives-hedge / test*.py | 4 | 0.007 | PASS |
| knowledge/derivatives-hedge / independent_review_tests.py | 7 | 0.108 | PASS |
| knowledge/inventory-cost / test*.py | 262 | 0.637 | PASS |
| local_cao/tests / test_*.py | 55 | 5.39 | PASS |
| hosted_cao/tests / test_*.py | 44 | 21.643 | PASS |
| intelligence/tests / test_*.py | 72 | 59.238 | PASS |
| build4/tests / test_*.py | 60 | 209.974 | PASS |

The orchestration population ran as 61 isolated module subprocesses, seven workers, with exact equality to the complete discovery population. Every module exited successfully. Other suites each ran in a fresh process. The manifest retains every qualified test identity, suite/module result, exit code and log SHA-256.

All seven repository validators passed: income taxes, agriculture, insurance contracts, derivatives/hedge and inventory supplements; standards claims; standards approvals. Repository public-output, canonical authority and specialist regression tests are included in the populations above.

The start/end snapshots bind 351 Python files and 1820 execution inputs. Both populations and all bytes remained unchanged. `accepted-release.json` binds the complete raw manifest. `artifact-inventory.json` binds deliverables; `build4.verify_release` independently discovers each suite in a fresh process and verifies the evidence without regenerating references.

## Preserved unsuccessful attempts

- Attempt 001 was interrupted after independent review reproduced a verifier-only module-name collision across suite directories. Fresh-process discovery fixes it generically. Its interruption, partial logs and source snapshots remain preserved; it is not credited as a complete regression.
- Attempt 002 executed 3,094 distinct tests before one hosted readiness-fixture failure. The workflow correctly refused cache reuse because the old successful-run mock omitted the new required Build 4 step. The fixture now includes that step; omitted/failed/skipped-step regressions cover it. Bounded reruns passed all eight readiness tests and all 44 hosted tests, followed by the entire fresh attempt 003. The original failed manifest and logs remain unchanged.
- Attempt 002 module 43 has a preserved incomplete raw text log although its fresh result recorded 32 passing tests and exit zero. The file replacement/truncation actor could not be established. An independent 32-test secondary rerun passed with complete output and unchanged source/input/primary evidence hashes. It is corroboration, not an extra distinct count or a replacement primary log. Narrow binary attributes retain incident capture bytes exactly; source whitespace checks remain active. Attempt 003 supplies the new complete test-result population.
- Development findings and failed fixture/proof attempts remain under `build4/release`; nine interrupted logs with trailing whitespace are stored losslessly as base64, bound by `lossless-log-inventory.json`. Original failed accounting artifacts have not been rewritten.

## Reproduction

```sh
CAO_BUILD4_ATTEMPT=owner-reproduction-001 python -m build4.run_release
python -m build4.verify_release
```

Choose an unused attempt name; the runner refuses to overwrite earlier attempts. The verifier checks the committed accepted manifest, not the new reproduction pointer. Long existing durable artifact checks inspect multiple fresh processes and may take close to an hour locally; inspect phase progress before restarting. Local success is distinct from exact-head GitHub Actions and unchanged-head readiness checks, whose final receipts belong in the sole PR.

## Explicit final raw-log recovery

Final engineering review found incomplete original module9/20 raw logs (their hashes still match) and module50 raw bytes changed after its recorded hash. The pathname replacement/truncation actor remains unknown. Original full-run manifest, raw bytes and passing22/62/16-test result JSON remain unchanged. Independent atomic PIPE captures reran exactly those modules on unchanged351Python/1820executioninputs; all100tests passed with complete Ran/OK logs. These are corroboration, not100additional release tests.

`recovered-release-regression.json` binds the original manifest SHA and changes only the module50 raw-log receipt to its complete16-test secondary capture. Original counts, outcomes, all22gate receipts and all other module receipts remain intact. `accepted-release.json` points explicitly to that derived witness. The original expected module50 log hash87fd872a... and preserved damaged8adbc3bb... are recorded; no silent repair or historical accounting migration occurred. Engineering QA approved this recovery, with accounting concurrence; the release verifier and artifact inventory bind the resulting evidence chain. Narrow binary attributes preserve only the incident raw log paths.
