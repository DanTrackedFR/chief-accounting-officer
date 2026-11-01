# Governed accounting execution — optional review mode

Repository baseline: `fbf8bb9a092955d2cd5fbf728c85e6dc62f4bd1c`.
Branch: `feature/prepared-accounting-execution`. PR: #48. Do not merge.

## Result and scope

`prepared_unreviewed` is explicit and host-disabled by default. It executes the
existing governed fixed-assets machinery and accounts-payable supplier-cost
owners through the same local/HTTP Case path. Synthetic governed production
proofs return EUR 90,000 depreciation and EUR 9,600 supplier accrual without
fabricated knowledge review, applicability review or execution reviewer sign-off.

The profile is deliberately bounded to ordinary commercial for-profit work in
calendar 2026, the existing cost-model/operational methods, private-company US
GAAP, FRS 102 2026 applicability, and AASB 2026 Tier 1/2. Unsupported owners,
periods, framework/entity overlays and policy elections block. This is not an
authorization to expand system preparation across the production skill catalog.
Actual source-population controls, source-row approvals, reconciliations and
specialist handoff evidence remain mandatory and are never manufactured.

## Authority, provenance and delivery

Accounting knowledge approval/source assurance, company evidence sufficiency and
workflow independent review are separate. Supported calculations have explicit
SUPPORTED/SUFFICIENT/SYSTEM_PREPARED indicators and retain native partial status.
The existing Case checkpoint stores partial work without publishing a complete
formal result version or upgrading Company Memory authority. Missing material
facts produce blocked UNRESOLVED/INSUFFICIENT results. Wider objective blockers
remain visible alongside supported owner numbers.

Public output explains treatment, calculations, material assumptions and proposed
journal implications. It contains no generic accountant-consultation or AI
uncertainty disclaimer. Canonical packages are honestly labeled background
guidance because automated claim-level application is not established here.
Private population manifests, hashes, source assurance labels and reviewer
identities stay private. Journals remain proposals; the native authorized journal
implication list is empty. TrackedFR may record its own informal user Finalised
attestation, but that cannot change native review authority.

## Integration and historical compatibility

Trusted host opt-in is the strict boolean `allow_prepared_unreviewed`; the local
CLI has a corresponding host flag. Mode is selected at start, enters immutable
request/Case cycle identity, binds owner fingerprints and canonical document
populations, and participates in hosted idempotency/input binding. Later explicit
mode values must match. Recursive accounting review injection, imported owners,
extra fact families and journal authority packs reject. Machine provenance is
categorically invalid as formal review evidence even if its reviewer is relabeled.

The dispatch and public enum additions use an exact byte-checked compatibility
witness to preserve historical formal fingerprints. Unenumerated common code,
helper or witness changes invalidate normalization. Historical accounting
artifacts, reference results and prior release pointers are preserved unchanged.
Two older dispatcher integration tests now check composition through the preserved
merged dispatcher and the additive bridge, retaining their original accounting
hash assertions. Existing byte-only tamper regressions caught an implementation
bug where the new bridge read a text view instead of authoritative bytes. It now
checks exact bytes and the captured implementation digests before normalization,
with additional independent split-view regressions.
Blocked native requests use a refusal-only renderer, avoiding any unsupported
package treatment or citation. Full-suite testing also exposed an existing HTTP
logging race: safe operational logs now precede response delivery, so client
receipt cannot outrun the required error-log event.
The versioned 1.0 wire envelope receives additive profile 1.1 fields, avoiding a
breaking change to historical clients. Shared local/HTTP schemas and the Build 2B
handoff describe all constraints and separate native review from UI finalization.

## Independent findings and remediation

Accounting QA identified missing public treatment/assumptions/proposal detail and
an owner-mismatch check bypass. Engineering QA identified hidden sibling diagnostic
blockers. All were reproduced, repaired generically and retained as permanent
regressions. Release integration identified the proof runner printing a summary
instead of its deterministic JSON; it now prints full output without rewriting
its frozen reference. Independent release review also found that the inherited
receipt verifier checked counts without pinning exact suite/validator populations;
the new verifier pins all 17 suites, 10 validators, command order, actual distinct
counts and orchestration shard unions. Twelve adversarial verifier tests pass. Accounting QA also corrected a supplier
profile provenance label to avoid implying IAS 37/AASB 137 governs every trade
payable; the neutral compatibility selector preserves the actual accounting
framework and canonical evidence without inventing standards applicability.

Independent native accounting QA: 29 tests. Independent HTTP/adversarial engineering
QA: 26 tests. The reports and raw logs are retained under knowledge/worker-reports,
architecture/PREPARED-EXECUTION-RELEASE-QA.md and skills/prepared-accounting/release.
Two independently seeded HTTP proofs match the unchanged reference byte for byte.

## Release evidence

The final acceptance manifest is selected by
`build4/release/prepared-execution-accepted-release.json`. Its verifier requires
unchanged tested Python/execution input hashes, exact full test discovery, passing
unskipped suites/validators, hash-bound logs, and the inherited historical artifact
inventory. Earlier exploratory/failed release attempts remain preserved and are
not accepted receipts. Narrow Git whitespace attributes retain interrupted raw
stdout fragments verbatim, following the existing release-evidence convention;
source whitespace checks remain active. No historical reference was regenerated
to pass a test.

The final release SHA and exact-head workflow results are frozen in PR #48 after
all required checks pass. Readiness-triggered workflows must use that same SHA.
Mergeability and main divergence are checked at handoff. Owner authorization is
required for integration; this implementation does not merge.

Superseded candidate local acceptance: **3,714 distinct tests**, all **17 suites** and
**10 validators** passed with no skipped tests, failures or errors. Beginning/end
Python and execution-input hashes are unchanged. The complete connected durable
proof passed with historical artifacts unchanged. That receipt remains retained for candidate b7232e36; current acceptance must select attempt 007.

The prior 3,714-test candidate was superseded after reproducing a cross-mode
Case-cycle alias. Prepared cycles now use a structured private identity outside
the legal formal request-ID alphabet, preserving historical formal cycles. A
permanent independent regression verifies both creation orders, actual evidence,
separate HTTP jobs and restart isolation. Renewed full frozen acceptance selects
attempt 007 only after that run passes.
