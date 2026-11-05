# Profile 1.2 runner recovery — bounded correction

PR #49 remains Draft and unmerged. No full accounting regression, final release receipt, workflow dispatch, merge or deployment was performed. This is runner recovery, not release acceptance.

## Reproduced cause and correction

At published baseline `a000d52991142352d9cd94ad2f554ea84fa1d151`, the source-assurance workflow executed regression only when the historical acceptance pointer was absent. The pointer existed, its historical manifest digest was valid, but its source identity differed already at that baseline (for example `local_cao/adapter.py`). `reproduction.json` and the permanent dispatch test record the exact predicate and mismatch. This is local evaluation of the actual workflow condition, not a claimed GitHub Actions execution.

The underlying `run_release.py` did not skip. It already refuses an existing attempt directory and is unchanged. New `execute_release.py` provides the workflow boundary: default means a new regression, regardless of any historical pointer. A mandatory unique `CAO_SOURCES_ATTEMPT`, contained paths and exclusive outer-log creation protect prior evidence. Failures propagate. Successful generation writes an attempt-local `execution.json` with `release_accepted=false`; it never writes an acceptance pointer.

Reuse is permitted only when explicitly requested with `--reuse POINTER` (or the workflow dispatch `acceptance_pointer` input), and only after the full existing release verifier passes: version-2 inventory, artifact hashes, complete population, source and execution-input maps, current discovery and historical preservation. Invalid explicit evidence aborts without fallback. Metadata-only commits may reuse acceptance when all these identities remain equal; changed source or execution inputs require new regression. The verifier now accepts `--pointer POINTER`; its no-argument historical default remains fail-closed. Optimization refusal is unchanged.

The workflow uploads fresh evidence before intentionally failing its final acceptance step with an explicit pending-review message. This expected pending-acceptance failure is distinct from a regression failure; inspect `execution.json`, the manifest and outer log. A reviewed, valid explicitly selected acceptance can pass that step. No green final gate is conferred merely by generation.

## Bounded verification

Permanent tests include the original workflow-condition reproduction, current workflow routing assertions, actual CI command execution with unchanged runner implementations across run/retry/separate attempt, repeated-attempt refusal, and independent subprocess reuse/tamper tests. Existing historical/preservation/population tests remain enforced.

Independent positive reuse uses a temporary synthetic repository executing 17 trivial tests and 10 trivial validators through the actual runner. Its verifier algorithms are unchanged, but its historical digest/count constants describe a one-canary synthetic contract. This is expressly not the real accounting regression or a new CAO release receipt. Real 8,912-entry historical preservation is checked separately against this checkout. See independent-qa/REVIEW.md and focused-results.json for final results and source bindings.

All existing receipts, manifests, workflow archives, acceptance artifacts and 13 remediations remain unchanged. The old CI canary test was adapted to preserve an existing historical pointer and assert the new unaccepted execution record instead of expecting automatic pointer issuance. Its old source remains in Git; no archived evidence was edited.

## Exact resumption procedure — next release agent only

1. Check out the published recovery checkpoint SHA in the PR handoff comment, with full Git history. Confirm clean status and Draft PR. Freeze Python, execution-input and workflow identities; treat any later source change as requiring a fresh run. Rerun the bounded checks if the source changes:

   ```sh
   python -m unittest discover -s tests -p 'test_presumed_runner_*.py' -v
   python -m unittest discover -s tests -p test_presumed_ci_evidence.py -v
   python -m unittest discover -s tests -p test_presumed_release.py -v
   python -m unittest discover -s tests -p test_presumed_workflow_migration.py -v
   ```

2. Complete the release preflight under the separate full-acceptance assignment. On GitHub, dispatch `cao-presumed-sources.yml` on `feature/presumed-user-sources` with `acceptance_pointer` empty. The workflow names attempts `presumed-sources-attempt-ci-${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}`. Earlier QA/proof/persistence gates remain in place; any failure there is a separate blocker, not proof of runner execution. Do not bypass them. Alternatively, in the frozen full checkout, the actual regression execution command is:

   ```sh
   export CAO_SOURCES_ATTEMPT="presumed-sources-recovery-$(date -u +%Y%m%d%H%M%S)-$(python -c 'import uuid; print(uuid.uuid4().hex)')"
   python skills/presumed-sources/execute_release.py
   ```

   Do not redirect over a historical log. The wrapper creates the exclusive conventional outer log itself. A failed attempt is retained; retry with a new identity. This command is intentionally NOT executed in this recovery assignment.

3. Preserve/download the resulting artifact, record run/attempt/artifact IDs and independently verify its ZIP and every required member. Independently review the real manifest, 17 suites, 10 validators, distinct discoveries, command/shard logs, all start/test/current maps and historical preservation. Add a new attempt-local `receipt-review.md` only after the review. Do not reuse synthetic QA evidence or relabel an old receipt.

4. Issue the NEW version-2 inventory outside the immutable attempt directory using `receipt_integrity.seal_inventory`, purpose `release`, manifest `build4/release/<attempt>/release-regression.json`, outer log `skills/presumed-sources/release/full-regression-<attempt>.log`, review `build4/release/<attempt>/receipt-review.md`. Include every attempt file (including `execution.json`). Choose fresh inventory and pointer filenames, e.g. `build4/release/<attempt>-inventory-v2.json` and `build4/release/<attempt>-acceptance-v2.json`; create the pointer with exclusive `open('x')`. Never replace `presumed-sources-accepted-release.json` or any historical path. Inventory issuance is NOT performed by this recovery.

5. Verify the new pointer explicitly:

   ```sh
   python skills/presumed-sources/verify_release.py --pointer build4/release/<attempt>-acceptance-v2.json
   ```

   Publish reviewed evidence without changing execution inputs, and reverify map equivalence. Dispatch source assurance with `acceptance_pointer` set to that exact new path to verify/reuse it. Each dispatch still uses its own unique output directory. Invalid pointers fail closed; do not retry them as if accepted.

6. Complete independent final acceptance and all exact-head CI/readiness work under the next assignment. Other legacy consumers (notably `build4/verify_release.py`) still select the historical default pointer; this bounded correction does not rewrite them or promote a new global acceptance. Before final CI, the next release agent must explicitly wire those consumers to the reviewed versioned pointer under the release contract, preserving history. If that requires changing Python/workflow execution inputs, make that source change BEFORE freezing/executing the full regression, not afterward. No final cross-engine CI/readiness acceptance is claimed here.

Stop this recovery after publication. Do not merge, deploy, mark Ready, issue final acceptance or run full accounting regression.
