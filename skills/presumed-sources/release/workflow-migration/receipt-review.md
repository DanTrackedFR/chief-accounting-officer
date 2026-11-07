# Independent review of the Profile 1.2 workflow migration release receipt

**PASS, 4 November 2026.** The tested source was
`d856cb846c2e79fe4cba08d844db88d7f0837e4e`, tree
`10846bdd41ca12bdb9eb91059c191f1d09854b75`. GitHub reported success for
all 16 steps of run 41779799873, attempt 1, job 126408500978, including the
artifact round trip, full regression, evidence upload and release verification.
Probe artifact 13298631739 and release artifact 13301623417 both identify that
tested commit.

## Evidence inspected

The 636,062-byte release ZIP matched the independently retrieved GitHub SHA-256,
`701d611a896cdfa808a0dff95c413f040f6face7b0b178947250d1dfb9552694`.
ZIP CRC validation passed. All 180 file members had unique, safe paths and
matched the imported repository bytes. The active pointer selected
`build4/release/presumed-sources-attempt-ci-41779799873-1/release-regression.json`
with SHA-256 `b8d810dcc8a66d260c77e81d7d6bfadb7535a0a95bf6e6d67ba6ea3d62958c4b`.

A separate audit checked the parent output against the 17 suite and 10 validator
exits, all 28 command log digests, all 65 orchestration shard log digests, and
the actual unittest count and success footer of each non-sharded suite and
each individual shard. Shard identities and counts matched the parent
orchestration log. Fresh discovery verified 3,844 distinct IDs with zero
errors, failures or skips. The start and tested maps matched each other and
the current files for all 439 Python sources and 2,700 execution inputs.

The original 8,912-entry v1 manifest matched its prior Git bytes. All 8,911
unmigrated files matched their original digests at the original paths. The
archive matched the pre-migration Git workflow bytes, and the active successor
matched its authorized digest. Both the Profile 1.2 and Build 4 receipt
verifiers passed on the imported evidence. The review used discovery and
receipt validation only. The prior 3,835-test result belongs to its earlier
source. Final-head and readiness checks are recorded separately on PR 49.
