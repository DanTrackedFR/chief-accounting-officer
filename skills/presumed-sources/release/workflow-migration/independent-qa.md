# Independent engineering verification of workflow preservation

Reviewed 4 November 2026 for PR 49. The historical reference commit was
`56c5f256390dd35446ed124bf75d4998fb526002`. The scope was workflow output
isolation and the authorized preservation migration.

## Independent byte comparison

Read the historical manifest directly from the Git object at the reference
commit and compared it byte-for-byte with the current manifest. Both hash to
`2c4fcdc1b938a1297acb31080e32c3c6ec388ad756395146028df45c98e70c49`.
All 8,912 entries are present. A separate loop hashed every historical path
other than the orchestration workflow directly from disk against its original
entry. All 8,911 files matched. The archived original workflow matches both the
original Git object and its v1 manifest digest,
`a4dbd9518ad72926bf3a46e0d4bc5a98d0bc286e23838aaaef29645c4aa671d7`.

The successor at the original path hashes to
`5699e0d078775e2b6a1132788505195af436bf35302ff023a65afe10414f6c31`.
Its single changed invocation uses the GitHub run ID and attempt number.
The reviewed verifier selects the sole historical workflow by its exact
original path, verifies the archived and active bytes separately, and checks
the hash-pinned v2 contract. Every other historical digest still applies at
its original path.

## Executable challenges

The seven initial methods in `tests/test_presumed_workflow_migration.py`
passed. Cases included rollback or alteration of the successor, a missing or
altered archive or contract, joint forgery of the successor and its digest
in the contract, alteration of a retained CI log, and alteration of v1.
The twenty existing historical/population tests passed unchanged.

The permanent canary `tests/test_presumed_ci_evidence.py` passed. It runs the
workflow shell commands using the actual intelligence, Build 4 and Profile 1.2
release runners in an isolated synthetic Git repository. Across (123, 1),
(123, 2) and (124, 1), every historical canary and every prior attempt's output
file stayed byte-for-byte identical. Each receipt named its own attempt and
matched its SHA-256. The earlier negative control used the original fixed
invocation and overwrote the synthetic historical canary.

The independent hash comparisons and execution tests support this specific
single-path migration. Corrected-source full regression, published receipt
verification and GitHub readiness require their own release evidence.
