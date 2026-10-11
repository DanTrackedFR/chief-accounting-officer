# PR 42 recovery checkpoint — INCOMPLETE

Original published head: `7be93b8dadf0b6a890d841c044c53bf9d364a085`.
Verified live main: `8e256701e555db3b7308694526242d7379e43e0f`.

Forensic inventory: accessible repository checkouts belong to MVP Builds 3 and 4. Their statuses are clean; branches, reflogs and stashes contain no unpublished Borrowing Costs recovery. Other accessible scratch directories contain no recovery checkout. The workspace root `.git` is an empty placeholder. No old Borrowing Costs workspace, recovery fixes, migrations or unpublished independent QA were recovered. PR 42 has no issue comments carrying recovery evidence.

Previous-agent claims remain unverified. This checkpoint preserves all original published tracked bytes in place with an SHA256 manifest. Git parent history preserves their original content. No accounting artifacts have been regenerated or migrated. No implementation changes or main reconciliation have occurred.

Narrow baseline validation: both original behavior tests run unchanged; 2 tests fail. Unknown materiality aborts before graph construction with `Owner outside registered Scopes`; unavailable borrowing evidence similarly has no blocked owner node. No full regression was run.

Remaining: reconstruct owner-scoped fingerprint repair; repair missing reviewed-source intake; investigate Stage 2 receipt/version provenance; compare Stage 4 history; independently review any migrations; integrate latest main; complete accounting, knowledge and full exact-head release gates. PR must remain Draft.

## Reconstructed intake repair

Missing company/Scope identity now retains the planned owner with missing reviewed-source evidence, rather than aborting graph construction. Explicit wrong or incomplete Scope identity still fails closed. Both original test bodies remain unchanged and pass. Three additional adversarial tests pass. Borrowing authored plus existing independently authored QA: 97 tests pass. Supplemental knowledge: 16 tests pass. Foundation and Treasury modules: 54 tests, one historical Treasury artifact reproduction failure; 53 behavior checks pass. No historical references were updated to silence this failure. Logs retain the actual failure.

This is not release acceptance or independent fresh-agent approval. Owner-scoped fingerprints, Stage 2/4 provenance, main integration and full regression remain open.
