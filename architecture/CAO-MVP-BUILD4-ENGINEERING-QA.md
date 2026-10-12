# Build 4 independent adversarial engineering QA

The delegated engineering reviewer authored `build4/tests/test_engineering_qa.py` independently of the implementation author. No production implementation or historical reference artifacts were changed by this reviewer. The suite uses the real `ExecutionInterface.call`, the actual stdin/stdout CLI in fresh Python processes, and a real localhost hosted HTTP server. It does not claim authenticated TrackedFR application acceptance or live model acceptance.

## Executable challenges

Run `python -m unittest build4.tests.test_engineering_qa -v`.

The 21 independently chosen tests cover:

- Real operating-system SIGKILL immediately after native SQLite checkpoint commit, followed by fresh-process CLI restoration and three execution retries. Revision stays 1, checkpoint count stays 1, and curated accounting results are identical. The killed calculation runs the existing production Fixed Assets owner. Synthetic input qualification is explicitly test-only.
- Actual CLI duplicate JSON keys and private path error hygiene.
- Wrong legal entity and wrong Period documents fail before mutation.
- Changed bytes under the same document identity/version fail after adapter restart.
- Document-embedded policy promotion, approval and posting instructions remain unqualified observations and cannot complete accounting.
- A model-generated claim citing a fabricated source fails without echoing the fabricated reference.
- Known Case lookup under another company fails without leaking the objective.
- Unsupported approval, closure, posting and memory-promotion operations and wire authority overrides fail.
- Reused event ID with changed interpretation fails without creating another revision.
- Missing executed agreement remains BLOCKED across execution retries and genuine fresh-process restoration.
- Native stale writer fails with `RevisionConflict`, retaining the newer committed checkpoint.
- Five concurrent HTTP submissions with one idempotency key produce one job identity. A changed route under that key conflicts; another tenant cannot read the job.
- Invalid credentials and body/header company mismatch reject with curated errors.
- Hosted investigation output and local restoration agree exactly, while raw sources, reviewer signoff, internal standards notes, tracebacks and binary content remain absent.

## Initial results and findings

Initial boundary suite: **15 tests PASS**, 6.368 seconds. Expanded durability acceptance added four real CORRECT/REWORK process kills and one permanent release-workflow cache regression. This is a bounded review of the tested paths, not certification of every possible adversarial input.

The initial interruption test kills after successful SQLite commit to exercise a lost acknowledgment. Four additional tests use the unfamiliar Boreal revenue contract, materially correct its price from EUR 42,000 to EUR 45,500, then kill real processes after sealed `SQLiteStore.prepare` or `SQLiteStore.recover` calls during CORRECT and REWORK. Fresh-process CLI restoration and exact-event recovery/retries must preserve historical result versions, retain exactly two native operation records and one rework history entry, and return the same revised curated accounting outcome without duplicate checkpoints or journal economics. These test-only seams terminate with OS SIGKILL, not a simulated raised exception.

Source observation assertions are deliberately exercised without native approval. The production Fixed Assets input in the restart test uses existing synthetic reviewer fixtures solely to reach the qualified owner; it is not represented as an authenticated real-person approval. Hosted service bearer credentials identify a test caller only, not an accounting approver.

## Release rerun

The release coordinator must rerun this suite on the final corrected source tree and retain the command, result and source/artifact hashes in the full regression manifest. The initial PASS cannot substitute for final-tree validation.

## Release engineering finding EQA-01

The original orchestration workflow omitted Build 4 paths, execution and its readiness-cache requirement. That could allow release validation to omit the new integrated acceptance population. The implementation author added `build4/**`, the Build 4 suite and fresh-process deterministic proof comparisons, `build4.verify_release`, and the same step name to the cache's required successful step set. The independent permanent regression `test_readiness_cache_requires_build4_step_and_actual_execution` parses the embedded Python required set and verifies real execution commands plus exact-head/workflow qualification. Its targeted rerun PASS.

The reviewer also challenged stale top-level suite JSON reuse after subprocess failures and Python-only source consistency. The coordinator added a fresh-mtime guard and start/end source population equality, and was asked to include non-Python accounting knowledge, contracts and workflows in final immutability verification.

## Preserved failed attempts

The first expanded suite ran 19 tests in 75.614 seconds, with one failure before process interruption: correction setup returned a generic invalid request. A targeted rerun reproduced a scope mismatch during initial native revenue execution. Diagnostic traceback isolated `orchestration/intake/preparation.py:350`, `Reviewed scope mismatch`, called by `intelligence/engine.py`. The original log files are `/tmp/build4-engineering-expanded.log` and `/tmp/build4-engineering-rework-rerun.log`; they must remain preserved in release evidence. The exact cause was an unconditional empty `memory_context_dependencies` insertion into prepared scope, differing from the independently reviewed no-memory scope. The implementation now augments scope only when actual qualified memory references exist; no expected result or scope control was weakened. Complete post-remediation rerun is recorded below.

Expanded independent rerun: `python -m unittest build4.tests.test_engineering_qa -v` — **20 tests PASS**, 89.633 seconds, log `/tmp/build4-engineering-20-rerun.log`. All four genuine CORRECT/REWORK SIGKILL acceptance cases passed. EQA-01's permanent cache regression passed. No test requirement or historical expected accounting artifact was weakened. Final-tree full repository execution remains the coordinator's release gate.

## Independent review of bounded memory remediation

The engineering reviewer inspected the memory fix authored by another agent. Native USE retry comparison reads `audit['uses'][...]['value']`, matches root Case, Case and exact memory version, and prevents a second USE event. Before returning any loaded investigation, the guard retrieves the exact immutable reference again and requires current qualification; stale, superseded, retracted or unavailable references block delivery. `consume_context` retains native revision checks and qualification. Scope augmentation is conditional on actual references and validates supplied reviewed scope before adding derived dependency receipts.

New independent regression: `test_retracted_memory_after_real_execution_blocks_delivery_without_rewriting_results` executes the existing Revenue Recognition production owner using source-qualified Boreal evidence, then retracts the consumed company position through native memory governance. Fresh-process CLI resume/result/execute all return BLOCKED. Historical accounting versions and the one original USE receipt remain identical. Targeted independent rerun: **1 PASS**, 6.123 seconds, `/tmp/build4-engineering-memory-retraction-rerun.log`.

The first attempt of this additional test used the older Build 3 revenue qualification helper, whose fixed semantic assertion expected EUR text against a USD document. It failed safely before execution. The test was corrected to use Build 4's currency-qualified helper; the initial failed log `/tmp/build4-engineering-memory-retraction.log` remains preserved. This was a reviewer-fixture mismatch, not a relaxed production control.

Historical protection independently verified: `PYTHONHASHSEED=283 python -m intelligence.tests.prove_integrated` followed by `cmp intelligence/release/integrated-proof.json /tmp/build4-engineering-historical-build3.json` returned exit 0. The original Build 3 historical reference remains byte-identical after the bounded memory fix. The complete engineering population now contains 21 tests: the earlier 20-test full rerun and this independently added security regression; final release requires all 21 together in the complete final-tree regression.

## Release verifier finding EQA-02

During release preparation the coordinator reproduced a verifier defect: discovering differently located suites in one interpreter can alias repeated short module names such as `test_authored`. The initial release attempt was preserved and stopped; no partial run was represented as the complete final-tree regression. The verifier now discovers each population in a fresh subprocess, matching how the actual release suites execute. Complete final-tree regression restarted as `attempt-002` after the correction.

The independent engineering reviewer inspected the corrected read-only verifier and release runner without changing Python source. Independent fresh-process discovery succeeded for all 14 actual populations: 3,226 summed test identities, including 60 Build 4 tests and 21 independent engineering tests. The runner's population gate matches 14 suites, seven validators and one whitespace command, with 22 gate logs. It requires all suites to pass without skips, exact orchestration shard discovery coverage, fresh suite-record timestamps, and unchanged source and execution-input hashes. The verifier independently compares current discovery identities, Python and contract/knowledge/workflow hashes, original historical references, gate and shard log hashes, deterministic proof receipts and final artifact inventory. It never regenerates historical accounting evidence.

No unresolved engineering source finding remains following review of these corrections. Final release acceptance remains conditional on successful execution of `build4.verify_release` against the completed accepted `attempt-002` witness; this report does not claim that still-pending gate has passed.

## Primary shard 43 raw-log anomaly and bounded corroboration

Final attempt 002's `test_stage4_closing_independent.py` result witness records 32 tests, zero failures/errors/skips and PASS. Its original raw log contains 18 completed test lines and a partial nineteenth line. Read-only investigation found no test output redirection. The logfile birth timestamp follows its retained modification timestamp, suggesting replacement of the pathname while the original process was running; the actor and mechanism cannot be established. This is an incomplete raw log, not a complete transcript, and its original bytes and result JSON remain preserved unchanged.

The engineering reviewer independently reran only that same 32-test module through actual unittest discovery on frozen source. **32 PASS**, exit 0, 52.503 seconds wall time, with complete raw transcript `build4/release/secondary-shard43.log` and receipt `build4/release/secondary-shard43.json`. Log SHA256: `6ade95f55a12d5897cfbdd9f3b5d737d6bdcafac0b3a831e262f111dea433d8f`. Receipt verifies unchanged Python source, unchanged execution inputs, and unchanged primary log/result hashes. These are corroborating executions of the same test identities; the 32 tests are counted once in the full regression population. Raw logs are preserved byte-for-byte, including any trailing whitespace.

## Readiness fixture correction and preserved attempt 002

Complete attempt 002 stopped at hosted suite 11: 44 tests ran, with one failure in `test_full_prior_exact_head_can_reuse`. The production workflow correctly refused cached reuse because the old test's successful-step fixture listed only eight required gates and omitted the newly required Build 4 gate. This was safe production behavior against an outdated positive test fixture, not a weakened release control.

The engineering reviewer made the single authorized correction to `hosted_cao/tests/test_readiness_gate.py`: add the exact Build 4 step name to `NAMES`. The existing exhaustive missing/failed/skipped-step test now also challenges the Build 4 gate. No runtime or workflow changes were made. Independent bounded validation: **8 readiness tests PASS** (0.074 seconds), then **all 44 hosted tests PASS** (21.718 seconds). Full logs are `build4/release/readiness-fixture-correction-8.log` and `build4/release/readiness-fixture-correction-hosted44.log`.

Attempt 002 and its failed manifest remain preserved; its partial successful suites are not claimed as complete final-tree regression. This known fixture change ends the prior source freeze, and complete final-tree regression must restart on the corrected tree as attempt 003. Python source is now frozen again following the bounded passes. Distinct repository test population remains 3,226, counted once.

## Final-tree regression review and explicit evidence recovery

The independent reviewer checked completed attempt 003: 3,226 distinct identities exactly once across 14 passing suites, zero failures/errors/skips, seven passing validators and whitespace, 22 successful gate receipts, unchanged Python and execution-input populations. All non-orchestration suite logs contain their exact expected test count and complete OK summary. Module 43 now has a complete primary 32-test PASS transcript. Failed attempts 001/002 and earlier anomaly evidence remain preserved.

Three final orchestration raw logs were incomplete: module 9 (22 tests), module 20 (62 tests), and module 50 (16 tests). Original module result JSONs and subprocess receipts record PASS. Modules 9/20's preserved raw bytes match their manifest hashes. Module 50's manifest expected `87fd872aa90c201fab8e86a4d3d3f5e73d99d852d28337dace75add23b8be7f5`, while its current preserved incomplete log hashes to `8adbc3bb4496291ecf449b3b0ece90fd37be1c86a4db1ffdce352ed06e227641`; the originally hashed complete bytes cannot be recovered. Neither original manifest nor original raw log was silently retargeted or overwritten. The exact replacement actor is unknown.

The reviewer reran only those three same modules on unchanged final source, captured full stdout/stderr in memory, and atomically published new logs after completion. All passed with exact complete Ran/OK summaries: module 9, 22 tests in 30.939 seconds; module 20, 62 tests in 65.260 seconds; module 50, 16 tests in 2.245 seconds. Each `secondary-final-{9,20,50}.json` binds its full transcript SHA256, actual exit 0, unchanged Python source and execution inputs, unchanged original raw/result hashes, and `distinct_tests_counted_again=false`.

Independent acceptance judgment: an explicitly derived recovery witness may reference the complete secondary module 50 log while retaining the original full-run test/result population and 3,226 count, provided it binds the unchanged parent manifest SHA and openly records the lost raw-log hash. Modules 9/20's complete secondary logs supply corroboration alongside their preserved incomplete originals. This is bounded evidence recovery of an actually executed complete final-tree population, not a targeted-test substitute for full regression. No source or accounting expected result changed, and no whole-suite rerun is required to recover this logging evidence. Local regression acceptance remains conditional on successful read-only verification of that explicit recovery witness and final inventory. No remote CI acceptance is asserted here.

## Final independent local engineering acceptance receipt

The reviewer independently compared `recovered-release-regression.json` with its preserved original parent `attempt-003/release-regression.json`. Only module 50's raw-log pathname/hash and explicit per-record recovery metadata changed, plus the top-level recovery explanation. All accounting results, test identities, suite counts, gate results, source/input hashes and other 60 module records remain identical. The accepted pointer's derived SHA and preserved parent SHA match actual files. All 22 gate log hashes and all 61 referenced module log hashes verify successfully. Exactly 3,226 identities remain counted once; the 100 secondary executions are not added.

Current source and execution inputs exactly match the accepted complete final-tree witness. The explicit evidence recovery is accepted for local regression. **Independent engineering local acceptance: PASS, zero unresolved substantive engineering findings.** Final inventory verification, exact-head GitHub Actions and readiness-triggered GitHub checks are separate release gates and are not claimed by this local receipt. No Python, workflow, contract or accounting source edits followed the final complete regression.


The reviewer's first whole `python -m build4.verify_release` invocation returned exit 1 at artifact inventory comparison because the preliminary inventory preceded this report's final acceptance paragraph. Source, input, fresh discovery, result, gate-log, historical and proof checks passed before that document hash mismatch. The precise failed invocation is preserved in `engineering-inventory-timing-failure.json`. The coordinator must regenerate the final inventory after this report is frozen, then execute the read-only verifier again without further document edits. This is a deliverable/inventory timing correction, with no production or accounting changes. Final successful verification can be recorded in the immutable PR receipt without creating another report-hash cycle.
