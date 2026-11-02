# Prior observed engineering failures — retained excerpts

These are concise transcriptions of earlier tool-observed failures, **not recovered
original log files**. The original `/tmp` logs were unavailable when the QA agent
resumed. No passing result is reconstructed or inferred from these excerpts.
Permanent executable tests preserve both triggers; current runs are stored directly
in this repository directory.

## Private policy approver disclosure

Command executed before remediation:

```sh
python -m unittest hosted_cao.tests.test_presumed_engineering_qa.IndependentPresumedEngineeringQA.test_class_assumption_private_evidence_is_never_published -v
```

Observed result:

```text
test_class_assumption_private_evidence_is_never_published ... FAIL
AssertionError: 'private-class-policy-approver-QA' unexpectedly found in ... public_result ...
Ran 1 test in 0.921s
FAILED (failures=1)
```

The synthetic input added `approved_by: private-class-policy-approver-QA` to the
machinery class assumptions. The actual HTTP result's `guidance` included that
value inside the complete serialized `Applied assumptions` policy object. The
same output contained supported €64,800 depreciation. This reproduced the private
policy identity leak without real personal data. The author replaced wholesale
serialization with curated accounting assumption fields.

## Partial compatibility normalization

Command executed before remediation:

```sh
python -m unittest hosted_cao.tests.test_prepared_engineering_qa.IndependentFingerprintEngineeringQA -v
```

Observed result:

```text
test_authoritative_bytes_do_not_depend_on_inconsistent_read_text ... ok
test_byte_only_shared_boundary_changes_cannot_hide_behind_original_text ... ok
test_common_helper_and_witness_tampering_invalidates_formal_seals ... ok
test_formal_fingerprint_matches_original_main_algorithm ... ok
test_mismatched_captured_common_digest_never_normalizes (boundary='interfaces/public_output.py') ... FAIL
test_prepared_fingerprint_binds_new_implementation ... ok
AssertionError: ... Digest captured by caller must match the authoritative bytes before normalization
Ran 6 tests in 0.557s
FAILED (failures=1)
```

The independently authored regression supplied an incorrect captured
`interfaces/public_output.py` digest. `bind_source_mode` returned a map whose
`skills/production.py` digest had already been normalized to the historical
main-7146 dispatcher hash. The author changed every failed qualification path to
return the original implementation map, preserving the exact assertion that
no partial normalization may occur.

## Exploratory harness correction

The first new-suite run observed 23 tests with one failure because the helper
incorrectly required partial native status even for an invalid source attestation.
The actual result was a durable blocked accounting result with unresolved source
assertion requirements. The helper was corrected to accept partial or blocked
accounting; valid numerical scenarios retain their explicit partial assertion.
This was a test harness correction, not an accounting implementation failure.
