# Independent engineering QA — presumed user-provided sources

This review independently challenges Profile 1.2 transport, durable identity,
source provenance, output privacy and compatibility. The QA worker changed only
its new HTTP and release-verifier test suites, this report, the two existing
engineering test fixture-copy lists plus their composed compatibility helper
target, and the existing Investment Property QA exact-dispatch-chain adaptation. No accounting method,
production implementation, canonical knowledge or historical accounting artifact
was changed by this worker.

## Findings reproduced and repaired

**Private policy approver exposed in public guidance.** The initial source
renderer serialized the complete client `class_assumptions` object into public
accounting guidance. A synthetic `approved_by` field therefore exposed its private
policy-approver value through an actual HTTP job result. The implementation author
replaced that serialization with a curated set of accounting assumption fields.
`test_class_assumption_private_evidence_is_never_published` preserves the exact
trigger. It passes after remediation while retaining the supported depreciation.

**Partial compatibility normalization after a captured-digest mismatch.** The
new compatibility wrapper normalized the dispatcher hash before checking the
captured public-boundary digest. A subsequent failed comparison returned that
partially changed map. The existing independently authored captured-digest test,
now directed through the composed wrapper, reproduced the defect. The author
changed failure paths to return the original captured implementation unchanged.
The permanent adversarial assertion passes for both common boundaries. Historical
expected hashes and tamper assertions remain intact.

An exploratory harness assumed every accounting refusal would have partial status.
An invalid attestation correctly returned a durable blocked accounting result and
SUCCEEDED operational job. The harness was corrected to permit blocked refusals;
valid numerical scenarios still explicitly require partial status. This was a QA
harness correction, not a production finding.

## Executable acceptance

`hosted_cao/tests/test_presumed_engineering_qa.py` contains **32 distinct tests**.
The final combined run with the **26 original preparation engineering tests** passed
**58 distinct tests**, with no skips, errors or failures:

```sh
python -m unittest hosted_cao.tests.test_presumed_engineering_qa hosted_cao.tests.test_prepared_engineering_qa -v
```

The corrected intended-final source passed all 58 targeted tests in 32.291 seconds,
retained at `skills/presumed-sources/release/engineering-qa/final-corrected-rerun-58-tests.log`.
Earlier 58-test evidence remains in `final-targeted-58-tests.log`.
The earlier 53-test run took approximately 33 seconds. A later targeted run is retained
at `skills/presumed-sources/release/engineering-qa/targeted-current-53-tests.log`.
Earlier observed failure excerpts are explicitly labeled transcriptions in
`skills/presumed-sources/release/engineering-qa/prior-findings-observed-excerpts.md`;
the original temporary logs were unavailable after the agent resumed.
Reruns and subtest variations are
not counted as additional distinct tests. This targeted evidence does not replace
full repository regression or exact-final-head CI.

The new suite starts a real loopback HTTP server and exercises source submission,
`/v1/jobs`, numerical execution, structured anomaly retrieval, idempotent retry,
new Service instances and local resume. It also exercises default-off and exact
boolean flags, dependency on Profile 1.1, immutable assurance selection, row/wire
substitution, unsupported owners, nested review-record injection through direct
JSON and a staged file, imported workpapers and journal-authority rejection.

Acceptance binds changed source versions, user attestations, class assumptions
and immutable assurance descriptors before the worker can execute. A committed
checkpoint is recovered after service restart with `CAO.run` forbidden, proving
that job retrieval and resume do not rerun accounting. The original suite retains
pending historical ACCEPTED/EXECUTING job compatibility and company isolation.

Public delivery is checked through all seven registered routes. Private source
hashes, client attesting-user reference, optional row approval identity and native
review/knowledge records remain absent. The private native checkpoint retains
client-assertion origin, original source hash and proposed journal workpaper;
there is no fabricated execution review, formal result version or posting
implication. Source Case omission produces `invalid_request` with its specific
field requirement.

Other tests verify optional P1.2 policy elections, ordinary AP execution without
PO/receipt-match inputs, NOT_PERFORMED matching checks, supplied matching errors,
selective row exclusion, aggregate missing-input requirements, absent-norm
NOT_PERFORMED results, and class-policy entity/framework/effective-period limits.

## Independently generated numerical scenario

The source rows are explicitly **synthetic deterministic test data**. They are
not the user's original uploaded workbook and do not claim to reproduce it. The
user clarified that exact original input access was not expected here; the
TrackedFR team will retest its original files.

- 27 ordinary machinery rows have opening gross costs €11,000 through €37,000,
  zero opening accumulation and explicit class assumptions of 10-year remaining
  life, zero residual and straight-line depreciation. Opening gross is €648,000;
  the full 2026 charge is **€64,800**.
- 10 ordinary service invoices have amounts €110 through €200. The supported
  invoice obligation is **€1,550**. No PO amount or receipt-match amount is supplied
  or invented. Recognition basis is an explicit company class assumption.
- Removing readiness from the first machinery row and opening accumulation from
  the second excludes those two rows and preserves **€62,500** depreciation on
  the valid rows, with two outstanding requirements.
- A conflicting supplied PO amount for the first €110 invoice excludes that row,
  preserving **€1,440** supported invoice obligations and an unresolved anomaly.

## Historical compatibility evidence

The new independent fingerprint tests reconstruct the unchanged Profile 1.1
algorithm using original main-7146 shared-boundary hashes and the original
preparation helper. Both supported packages match. The original formal fingerprint
algorithm test, captured-byte split-view tests, common-code tamper assertions and
historical formal identity assertions continue to pass.

Read-only `git show` comparisons against
`7146eaeca6a28d17d9183d0f9431fd9b9663f1fe` confirm byte-identical preservation of
`skills/prepared_execution.py`, `skills/prepared_fingerprint.py`, and both new
main-7146 dispatcher/public-boundary witnesses. No baseline output was regenerated.
New Profile 1.2 fingerprints bind source/attestation/class input changes, every new
source helper, the additive manifest and public-boundary bytes. Changing any new
compatibility witness/helper invalidates historical normalization.

## Final transport follow-up — remediated and passed

Five additional engineering methods challenge assurance-descriptor deletion,
malformed envelope aggregation, staged source Case omission, persisted safe job
error projection and unknown fact-family privacy. The first focused run passed
four methods and found one further raw-provenance disclosure. Its actual log is
retained at `skills/presumed-sources/release/engineering-qa/final-additions-first-run.log`.

The shared preliminary request validator interpolated unregistered fact-family
keys into `error.requirements.field_path` and `identifier` before the normal
family allowlist rejected them. A synthetic family key containing
`Source: ChatGPT training data private-QA-reference` was therefore echoed in an
actual HTTP 400 response. The permanent regression requires that this raw source
note and private reference never be emitted. The implementation author limited preflight interpolation to the registered
Profile 1.2 fact-family names, so unknown raw keys cannot enter requirements.
The final full 58-test targeted run passes the exact reproducer after this fix.

The descriptor-deletion regression verifies both removing only assurance and
removing assurance plus mode on an already committed Case. Both host-disabled
and host-enabled local status/questions/result/resume/execute refuse before any
owner call. Existing historical identity assertions remain unchanged.

Safe error tests deliberately inject a structured validation exception, a returned
local validation refusal and an unexpected exception after valid job acceptance.
Specific validation requirements survive job retrieval and a new Service instance;
unexpected private exception text stays unavailable. Real preacceptance tests
verify aggregate company/Case requirements and specific missing staged source
Case requirements without creating a job.

## Independent deterministic proof verification

The author-provided `hosted_cao.tests.prove_presumed_http` runner was executed
independently under `PYTHONHASHSEED=109` and `971`. Both complete JSON outputs are
byte-identical, retained in this evidence directory as `http-proof-seed109.json`
and `http-proof-seed971.json`. The comparison artifact
`independent-proof-comparison.json` confirms proof SHA-256
`48cac56e16ebe673db690cadcdb4a800018a8aedf50861740246e346dab58fd9`.
The reviewer separately checked €64,800 depreciation, €1,550 invoice obligations,
partial native status, restart equality and idempotent retry equality. These
repeat executions add **zero** distinct tests and do not certify an eventual
unchanged final release SHA; full release validation remains the owner's gate.

## Complete-release acceptance review — remediated and passed

A read-only review of the new release runner/verifier and GitHub Actions found
that the main-7146 historical-preservation JSON was not bound by execution input
hashes (release JSON is intentionally excluded) and its enumeration lacked a
pinned digest/count. An empty mapping could therefore bypass all new historical
checks while retaining the baseline string. The author accepted the finding and
added `verify_historical()` with exact manifest SHA-256, exact population count
and repository namespace checks. The final manifest is pinned to SHA-256
`2c4fcdc1b938a1297acb31080e32c3c6ec388ad756395146028df45c98e70c49`
and exactly 8,912 preserved files. All 20 independent release-verifier methods
pass, retained in `skills/presumed-sources/release/engineering-qa/final-corrected-20-release-tests.log`.

`tests/test_presumed_release.py` adds 20 independent adversarial methods: the
12 established 17-suite/10-validator population assertions are inherited unchanged
and directed through the new verifier; eight isolated history checks qualify a
valid fixture first and then challenge manifest bytes, empty/reduced enumeration
even with a matching digest, deleted/changed original content, namespace escape
and the actual pinned manifest/count. No real artifact is mutated.

The initial complete release also exposed old QA assumptions that live dispatch
was exactly Profile 1.1. The existing Investment Property test now proves the
entire additive chain from the unchanged e753 original, through the preserved
main-fbf8 and main-7146 dispatch witnesses, to the live enumerated Profile 1.2
transform. All historical expected accounting hashes, original witness checks
and numerical outcomes remain unchanged. Its text/byte split-view test uses the
composed compatibility wrapper while retaining the original normalized baseline
SHA. All 15 targeted methods pass with full repository history available; the log
is `skills/presumed-sources/release/engineering-qa/ip-main-reconciliation-targeted.log`.

## Corrected intended-final source verification

After the author's further accounting corrections, the reviewer independently
reran the 32 new and 26 original engineering methods: **58 distinct tests pass**.
The 20 additive release-verifier methods also pass. The separately retained
15-method IP reconciliation run preserves every original accounting fingerprint
and result digest. These sets are not reruns counted as additional distinct tests.

The first 58-test run on the corrected candidate exposed a stale QA expectation
that an entirely excluded population should publish zero depreciation. The
author's substantive correction properly omitted unsupported aggregates. The
reviewer strengthened that test to require no financial calculation, all 27 rows
excluded, no journal implication prose and UNRESOLVED accounting. The initial
error log remains `final-corrected-58-tests.log`; the passing complete rerun is
`final-corrected-rerun-58-tests.log`. No production behavior was changed for this
QA expectation correction.

New proof captures on corrected intended-final production are retained as
`final-http-proof-seed109.json` and `final-http-proof-seed971.json`. They match
byte for byte, with SHA-256
`be06ab1a1ee247bc24159f7ad605eb30c1dc70fccb13c864b50a9da25e88bcb7`.
`final-independent-proof-comparison.json` records independently checked €64,800
depreciation, €1,550 invoice obligations, partial status, restart recovery and
idempotent retry. Earlier proof captures remain preserved; repeat executions
add zero distinct tests. Full corrected regression and exact-final-head CI remain
the release owner's responsibility.

## Result and limits

No unresolved substantive engineering finding remains from this targeted review.
All four independently identified execution/release defects have permanent
passing regression coverage.
The implementation remains subject to separate accounting QA, complete repository
regression, historical population preservation and exact-final-head release gates.
The HTTP tests use synthetic sources and one host; they do not verify actual
TrackedFR authentication, external user identity, source-file authenticity,
production deployment, ERP posting or distributed exactly-once behavior.
