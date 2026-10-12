# Exact local history and publication recovery

PR #43 uses the existing branch `phase-3/investment-property-accounting` only.
There is no new PR, merge, reset or force push.

The configured GitHub writer publishes verified Git blobs and a tree that must
equal the final local release tree exactly. Its publication commit retains the
original PR head `a66a43b54f1c72a9eea686589173d94c5138384d` and integrated main
`e75375b84813b9d584db12aa692b2f4d16baf052` as parents. API-generated commit
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
The publication lease must still match the original published head, with
`force=false`; a changed head requires deliberate reconciliation, not retrying
with a weaker lease.

All superseded full runs remain diagnostic. Reproduce only new Investment
Property examples; never regenerate historical artifacts to obtain matching hashes.
Exact published-head and unchanged-head readiness CI run references belong to the
PR #43 release completion comment, avoiding a self-referential commit hash in the
commit's own report.
