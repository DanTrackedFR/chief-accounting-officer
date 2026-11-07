# Independent QA — historical refusal compatibility and durable CI recovery

Reviewed the correction candidate based on durable commit
`88ca8040df361ba7d9846c2f80708b9df03853b8`. The reviewer authored only
`tests/test_presumed_historical_errors.py` and this release report. No production
implementation, historical artifact or existing test was modified by the reviewer.
No full regression was initiated, restarted or interrupted by this review.

## Confirmed historical proof defect

An isolated real local-API request reproduced the exact wrong-framework-calendar
case from `build4.prove_integrated` without running its full accounting journey.
Compared with the existing resolver-selected frozen record, the sole JSON change
was an added `$.error.requirements` array:

```json
[{"category":"invalid_shape","explanation":"Check the submitted fields and types against the execution contract.","field_path":"$","identifier":"request.shape"}]
```

The existing code, message, operation and public refusal were otherwise identical.
The new generic invalid-request fallback had applied to a historical default-host
context-resolution failure. The author gated the new preflight/fallback diagnostic
extension on the trusted `allow_presumed_user_sources` host switch in both local
and hosted adapters. With this feature off, formal and Profile 1.1 hosts retain
the original refusal envelopes. When enabled, structured source-profile binding
requirements remain available. Accounting source assurance still requires its
separate explicit request/Case selection; diagnostics do not select or approve an
accounting profile.

The historical reference remains unchanged at
`skills/government-grants/release-evidence/historical-qa/integration-fresh/build4.prove_integrated.json`,
SHA-256 `4d2f1acf2dd153b079fee4c1eb976a10e6cb9fe865e1aa90deff97a246ce348b`.
That file's hash was independently checked during this review. No golden output,
reference resolver or proof generator was altered to hide the difference.
The implementation owner's full seeded proof executions are separate evidence;
the reviewer did not count those reruns as independent tests.

## Permanent targeted acceptance

Actual command:

```sh
python -m unittest discover -s tests -p test_presumed_historical_errors.py -v
```

**10 distinct tests passed in 3.129 seconds, with no skips, failures or errors.**
The suite covers the exact complete frozen wrong-framework response for default
formal and Profile 1.1 hosts; unchanged malformed local refusal envelopes; exact
HTTP legacy refusals for default/Profile 1.1 hosts; and enabled source-host local
and HTTP structured missing-binding requirements and fallback diagnostics.
Missing hosted bindings reject before any job is accepted.

The new suite uses only the standard library and existing parser-independent
runtime modules. It does not introduce document-parser dependencies into the
repository test/standards workflows. Temporary workspaces are isolated; original
company data, historical references and source attestations are not manufactured.

## Durable CI workflow review

The proposed source-assurance workflow runs the unchanged complete release runner
only when an accepted-release pointer is absent. The runner must return success
and a receipt declaring complete, unchanged source before an ephemeral hash-bound
pointer is written. The unchanged verifier subsequently checks exact discovery,
logs, current source/input maps and historical preservation. A present stale or
invalid pointer fails verification rather than authorizing an accounting result.

The artifact step retains the actual attempt directory, main log and pointer,
including partial evidence after failure. Their common archive root preserves
`build4/...` and `skills/...` hierarchy. Artifacts are uploaded before the final
verifier so verification failure cannot erase the executed evidence. Candidate
receipts are not accepted merely because an artifact upload succeeded.

Before the expensive full run, a separate artifact round trip uploads the
committed persistence probe, downloads its artifact ZIP using the scoped GitHub
API, checks ZIP CRC integrity and compares the stored probe bytes exactly. Its
single-file archive member name is correct. The job supplies `actions: read`
permission and full Git history, Python 3.12 and the established parser install.
A failing durability round trip prevents the expensive run. This is a configured
remote probe, **not a claim that local file writes proved remote durability**;
its actual CI execution must succeed before that claim can be made.

Review identified one artifact-retention issue: immutable v4 artifact names could
conflict when a failed job is rerun within the same GitHub run. The author changed
both probe and release artifact names to include run ID **and run attempt**, while
retaining the release source SHA. This preserves prior attempt evidence instead
of overwriting it. The corrected names were inspected directly in the final YAML.

## Result and limits

The targeted compatibility fix and current durable-run workflow have no unresolved
material finding from this review. The legacy refusal reproduction is repaired
without changing its frozen reference, and source-host structured diagnostics are
retained. Full corrected-tree regression, actual remote durability round trip,
accepted receipt import and exact-head/readiness CI remain release requirements.
Unavailable attempt-005 outputs or past conversational progress are not completion
evidence. No missing receipt or command exit has been reconstructed.
