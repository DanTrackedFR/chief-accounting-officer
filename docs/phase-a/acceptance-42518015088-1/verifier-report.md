# Independent production verifier checks before issuance

Frozen source `6b36ae0d9bb942ec4eacc199e59c099c4cc01133`. Used a distinct detached Git worktree with the original bytes from GitHub artifact 13633904464 for run 42518015088 attempt 1. Archive SHA-256 `2d377c812a6df2c9bfb37bcdf9f2599937a6950852bc1bf8c59af3a933f14a61`.

Checked every manifest command log and orchestration shard log against its embedded SHA-256. Compared all 23 suite sidecars to their manifest entries (removing only the runner-added exit_code). All matched. The original, separate historical pointer packaged in the ZIP selects run 41779799873 and does not select this candidate.

Executed production `validate_population` on the untouched hosted manifest. Passed. Recomputed `source_hashes()` and `release_input_hashes()` against the checked-out tree. Both dictionaries exactly match the manifest. Production `verify_source_binding` passed. Production `verify_historical` returned 8912. Fresh production discovery returned 4012 and exact per-suite identity list equality across all 23 suites. No suites were executed for rediscovery.

Ran the Profile 1.2 and Build 4 delegated production CLI entrypoints on missing and historical pointers. Each exited 1 for the missing pointer, and each rejected the historical pointer for lacking the required version-2 inventory. Both rejected optimized Python with -O and -OO at module entry, as their tested contract requires. Full command outcomes are in verifier-negative.json.

The production issuer is `skills/presumed-sources/receipt_integrity.py::seal_inventory`. Required review lives inside the immutable attempt directory as receipt-review.md. The inventory must live outside that directory. The two attested role paths, all attempt members, command and shard logs, all suite sidecars, both starting maps and the authoritative manifest must verify. Extra files can include the unmodified ZIP, original historical pointer and immutable provenance record. After independent review and issuance, use explicit --pointer with both entrypoints and explicit --reuse with a new local attempt identifier. The unmodified fresh execution.json remains acceptance-pending.

Positive final acceptance is a separate outcome that requires the reviewed receipt. The checks in this document authorize no receipt by themselves.
