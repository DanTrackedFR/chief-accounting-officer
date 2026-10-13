# Exact local history and publication recovery

PR #43 uses the existing branch `phase-3/investment-property-accounting` only.
There is no new PR, merge, reset or force push.

The configured GitHub writer publishes verified Git blobs and a tree that must
equal the final local release tree exactly. First publication `646493d9` retains
original PR head `a66a43b54f1c72a9eea686589173d94c5138384d` and integrated main
`e75375b84813b9d584db12aa692b2f4d16baf052` as parents. Corrected publication
fast-forwards from that first publication, retaining both ancestors. API-generated commit
metadata differs from the local implementation history; this is not represented
as identical commit SHA provenance.

The original `ip-local-checkpoints.bundle` preserves the earlier checkpoint chain.
The final `ip-final-local-checkpoints.bundle` preserves the later implementation,
independent QA and complete local acceptance checkpoints. Its exact archived head,
SHA256, prerequisites and verification command are recorded in the release
completion report. The subsequent archive-containing commit cannot contain
itself in its own archive; the tested source and release checkpoint are preserved.

Recover into a fresh repository or a distinct branch; never overwrite current work:

```sh
git fetch origin main phase-3/investment-property-accounting
git bundle verify build4/release/ip-final-local-checkpoints.bundle
git fetch build4/release/ip-final-local-checkpoints.bundle \
  refs/heads/phase-3/investment-property-accounting:refs/heads/recovery/ip-pr43-local
```

Use the exact archived head from the release completion report for inspection.
Compare the published and local release trees before any recovery operation.
The publication lease must match the actual expected-current published head, with
`force=false`; a changed head requires deliberate reconciliation, not retrying
with a weaker lease.

Interrupted attempts001–004 remain diagnostic. Attempt005 remains valid evidence
for its prior source freeze; corrected-source acceptance uses attempt006.
Reproduce only new Investment
Property examples; never regenerate historical artifacts to obtain matching hashes.
Exact published-head and unchanged-head readiness CI run references belong to the
PR #43 release completion comment, avoiding a self-referential commit hash in the
commit's own report.

## Incremental R7 / full006 archive

After loading the prior final archive, inspect its exact prerequisite head
`30bbc9e54e2ed76f5fe71b26efd08d434c4925af`, then load the incremental archive
into another distinct branch:

```sh
git bundle verify build4/release/ip-history-correction-local-checkpoints.bundle
git fetch build4/release/ip-history-correction-local-checkpoints.bundle \
  refs/heads/phase-3/investment-property-accounting:refs/heads/recovery/ip-pr43-r7
```

Exact archived head is `7cef2d7d9e15598c61eeafbc95bb76e12d6041da`;
archive SHA256 is `5ea87739fbb7ab46cfdb44e0f9c118a72e15944924ac077fe6904e72634a6e41`.
It preserves the original failure, independent correction, immutable pre-repair
receipt commit and qualified full006 acceptance. The archive-containing packaging
commit is subsequent and cannot archive itself. The diagnostics stdout limitation
and separate corroborating rerun remain explicit; never replace its original capture.
