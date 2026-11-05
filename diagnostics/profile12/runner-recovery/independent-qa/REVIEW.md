# Independent engineering/governance review — bounded runner recovery

**PASS for bounded runner correction. Full CAO release acceptance remains pending.**

Reviewer: independent delegated engineering/governance agent `/root/runner_qa`.
Baseline: `a000d52991142352d9cd94ad2f554ea84fa1d151`. Reviewed file digests are in
`source-and-preservation.json`; these bind the reviewed uncommitted candidate
without claiming that its later publication SHA was available during testing.

## Findings and correction assessment

The baseline workflow conditions new regression on absence of the historical
pointer. The Python regression runner itself does not read that pointer and
already rejects an existing attempt directory. The correction removes the
existence-only workflow shortcut, keeps the original runner, and adds an explicit
execution/reuse controller. No accounting code or 13-defect remediation was
changed by this correction.

Default execution ignores historical acceptance, invokes the actual runner, and
records `REGRESSION_COMPLETE_ACCEPTANCE_PENDING` without issuing an acceptance
pointer. Explicit reuse invokes the complete existing release verifier with an
explicit pointer; there is no stale-receipt fallback, reduced-verification path,
or success mock. Reuse requires matching Python/execution-input identities,
version-2 inventory, complete test/command population, discovered test identities,
evidence integrity and historical preservation. Metadata-only Git SHA differences
are permitted by this source/input-equivalence contract, not by pointer existence.

The workflow reads optional pointer input through a quoted environment variable,
uses run ID plus attempt for outputs, and uploads evidence before its final scope
gate. That gate intentionally fails when regression has completed but independent
acceptance has not occurred; a green workflow is not granted merely because fresh
regression succeeded. Explicit verified reuse passes that gate. Future release
operators must distinguish this expected pending-acceptance failure from an actual
regression failure.

Suggested fail-closed final workflow gate was incorporated and tested. No remaining
blocking issue was found in the bounded correction.

## Executed verification

Command from repository root:

```sh
python -m unittest discover -s tests -p test_presumed_runner_recovery.py -v
```

Final result: **16 methods passed, no failures/errors/skips, 6.227 seconds**.
Exact output: `final-gate.log`. Earlier 14- and 15-method executions remain in
`initial.log` and `final.log`; they are not additional distinct final methods.

Coverage includes:

- Actual controller and runner execute a new regression despite historical and
  valid matching acceptance pointers being present.
- Explicit valid acceptance passes the full verifier and does not rerun regression.
- Explicit historical, malformed, missing, path-escaping and symlink pointers fail.
- Changed Python and execution-input identities fail separately.
- Inventory artifact corruption fails.
- Optimized Python refuses before verification can bypass mandatory assertions.
- Existing attempt/outer-log collisions and redirected output paths preserve bytes.
- Invalid attempt labels fail before output creation.
- An actual failed synthetic test causes incomplete regression and no execution
  success/acceptance record.
- The exact workflow final-step shell rejects fresh/pending state and accepts
  the actual verified-reuse state.

## Synthetic-fixture boundary

The positive reuse test uses a disposable synthetic repository, actual subprocess
execution of **17 trivial tests in the 17 supported suite slots**, the 10 supported
validator command slots, and all 28 command records. The real runner, verifier,
inventory functions, discovery and source/input hashing run unmocked. The fixture
creates and seals a temporary synthetic receipt solely to exercise the reuse
contract; it is deleted with the fixture and is never published as CAO acceptance.

Only the fixture verifier's historical population constant and preservation digest
are replaced to bind its one immutable synthetic canary. This is necessary because
the actual 8,912 pinned historical files include the real accounting tests; replacing
those with cheap synthetic tests cannot satisfy their original hashes. Fixture
investment-property preservation and grants migration records likewise describe
only the synthetic fixture. No production verifier constants were changed. This
test is not a new accounting regression or proof of production receipt acceptance.

Separately, the **unmodified actual historical verifier returned 8,912** on the real
checkout. The actual historical acceptance pointer matches baseline Git bytes.
The tracked diff contains no historical release/evidence changes. These results
and reviewed file hashes are in `source-and-preservation.json`.

## Remaining ownership

No full accounting regression, final release receipt, workflow dispatch, readiness
transition, commit, merge or deployment was performed by this reviewer. The next
release agent owns actual corrected-source regression, artifact retrieval and
independent receipt review, new version-2 inventory/pointer issuance at new paths,
explicit acceptance verification and final readiness checks. This report approves
only the bounded runner recovery behavior.

`build4/verify_release.py` remains an unchanged legacy consumer: it detects the
historical pointer and calls the no-argument source verifier. That path remains
fail-closed and is not wired to a future versioned acceptance pointer. The bounded
controller/new explicit verifier entry point can execute and verify new evidence,
but this review does **not** assert all downstream release gates are ready. The
next release agent must settle cross-engine acceptance-pointer selection before
freezing the full-regression candidate if doing so changes Python/workflow inputs;
changing those inputs after regression would invalidate that regression's identity.
