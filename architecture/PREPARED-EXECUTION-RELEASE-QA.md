# Independent release engineering QA — prepared accounting execution

## Scope and finding

Independently reviewed `skills/prepared-accounting/run_release.py`, its verifier,
and the optional Prepared release dispatch in `build4/verify_release.py`.
The inherited historical exact-tree release cannot attest a subsequent enhancement;
a new source-frozen manifest is therefore appropriate. Existing acceptance pointers,
accounting reference outputs and preservation inventories remain unchanged.

The initial new verifier accepted a manifest's chosen suite directories/patterns
and checked only the totals of 17 suite records and 28 command logs. It did not
independently require the expected full suite and validator population. A narrower
specialist pattern or a substituted validator could therefore masquerade as full
regression if the corresponding manifest and pointer were regenerated. The actual
builder selected the full population; this was a verifier false-pass gap.

The implementation author repaired the verifier generically with an explicit
17-suite and 10-validator allowlist, exact ordered command shapes, per-suite
executed/distinct counts, global uniqueness, no failures/errors/skips, successful
exits, and orchestration shard union/count/exact-discovery requirements. Interpreter
location is normalized while its executable identity and remaining command are
checked. Source and execution-input hashes, fresh discovery, command/shard log
hashes, manifest hash and inherited historical preservation checks remain in force.

## Independent regression

`tests/test_prepared_release.py` provides 12 independent adversarial tests with
multiple mutation cases. The test independently pins every suite and validator;
it challenges narrower patterns, substituted/omitted/reordered suites or
validators, incorrect counts and duplicate identities, failed/skipped results,
changed commands or interpreter identity, missing whitespace checks, and missing,
duplicated, incomplete or failed orchestration shards. All 12 passed in an
independent run after the repair. The run output was retained at
`/tmp/prepared-release-independent-qa.log` during this review.

The prior independent execution review also provided 23 passing transport,
identity, persistence, fingerprint and public-boundary tests. Its separate report
is `knowledge/worker-reports/prepared-accounting-engineering-qa.md`. The HTTP proof
runner was corrected to print deterministic JSON without writing its frozen
reference. Seeds 41 and 1481 match the unchanged reference byte for byte.

## Remote fingerprint finding and independent follow-up

The initial remote Phase 3 workflow exposed a substantive split-view defect in
the compatibility helper: its text comparison could hide a byte-only mutation
already captured by the fingerprint caller. Local physical-file tamper tests had
missed this boundary. The repaired helper uses authoritative bytes throughout
and checks captured production/public digests before normalization. The
independent engineering suite now adds byte-only production/public mutation,
inconsistent text-view and mismatched captured-digest regressions, including
both authorized accounting packages. All 23 engineering tests and all 12 release
population tests pass after the repair.

Independent diff review of the two Investment Property integration adjustments
confirms composition of old and new additive dispatchers while retaining the
original historical hash and accounting assertions. The no-fabricated-review
proof concerns execution-review records; it retains accurately labeled synthetic
source-control reviewer evidence and does not imply actual human finalization.

## Hosted logging regression follow-up

The full hosted suite exposed a response/log ordering race in an existing
privacy assertion. The author moved emission of the unchanged safe operational
metadata before sending the HTTP response. Independent review confirms the
same bounded fields and no request, credential or private accounting content.
All 44 original hosted tests, 20 repeated executions of the original confidential
error log test and all 23 independent engineering tests pass after the repair.
Their logs are retained under `skills/prepared-accounting/release/`. Attempt 004's
failure evidence remains preserved and does not attest the repaired source tree.

## Historical pending-job compatibility follow-up

The final audit identified a pre-upgrade pending-job hash incompatibility in an
initial universal descriptor-binding change. Formal jobs must retain their old
`[configuration, evidence]` hash; only prepared jobs add the immutable request
descriptor. The author restored that distinction. Two independent regression
methods construct old-format ACCEPTED/EXECUTING rows for both packages, resume
them with preparation disabled and no reviewer-seal refresh, and separately
verify that prepared descriptor substitution prevents owner execution. The full
engineering suite now contains 25 passing tests. Read-only review found no
additional changes to pending DB/request/Case identity or investigation resume
contracts. Attempt 005 remains superseded evidence; final attempt 006 must
freeze and verify the repaired source tree.

## Preservation and release status

A read-only diff against main `fbf8bb9a092955d2cd5fbf728c85e6dc62f4bd1c` across the
historical release/reference/recovery/knowledge namespaces showed additions for
this enhancement and its QA only; no existing historical accounting artifact was
modified. The former release attempt is retained. Because release code and tests
changed during that attempt, it cannot be used as evidence for the final tree.
The final replacement `prepared-execution-attempt-006` must run the complete
population with fresh beginning/end source and execution-input snapshots; prior
attempts remain retained and cannot certify subsequent source changes.

This report does not declare the replacement full regression, exact-head remote
workflows or PR readiness successful before their results exist. Those release
receipts remain required. No unresolved substantive finding remains in the
reviewed release builder/verifier after the independent adversarial checks.
