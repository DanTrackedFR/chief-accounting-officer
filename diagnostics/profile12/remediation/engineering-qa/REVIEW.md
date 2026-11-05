# Independent engineering and governance remediation QA

**PASS for the bounded remediation review. No unresolved release-blocking engineering/governance remediation finding. This is not full Profile 1.2 release acceptance.**

Reviewed/tested candidate: `98c89f9ae3f76fae441a86edeeb6232dd5d790ef`.
Reviewer: independent engineering/governance agent, separate from production implementer and accounting reviewer. Source digests and exact counts are in `source-and-results.json`.

## Scope and evidence

`test_boundaries.py`: **12/12 methods pass**, zero failures/errors/skips, 7.705 seconds. Fresh inputs use a different source identity and asset amounts from the original defect fixtures. Actual authenticated loopback hosted API, local adapter, direct production owner, reopened durable native results, restart and idempotent job retry are exercised. Exact HTTP request/response traces are retained under `evidence/`; `boundaries.log` records all method outcomes.

The tests challenge invalid source Case identifiers through inline submission, staged file submission, changed staged evidence before job acceptance, and direct owner execution. Invalid variants include boolean, numeric, arrays, objects, whitespace and 257-character strings; a 256-character source identifier remains supported and is separate from the durable Case identity. Malformed operation variants cover null, booleans, numeric values, arrays and objects through both HTTP endpoints and the local adapter, with structured operation requirements and no job acceptance. Invalid disposal authorization representations cannot produce journal proposals at the direct owner boundary.

Fresh diagnostic tests verify an 8,192-character source identifier becomes a bounded display reference without losing material anomalies, while preserving the original source identity in native lineage. An 8,193-character source identifier is qualified without journals; an invalid oversized row identifier excludes only that row; 201-row input fails before partial accounting. Valid results and journal proposals survive reopening and retry unchanged.

`test_governance.py`: **10/10 methods pass**, zero failures/errors/skips, 25.917 seconds. It clones the committed candidate, issues a separate versioned focused receipt by executing the actual 19 diagnostic HTTP methods, and verifies that genuinely valid receipt **before** any tampering. No historical source receipt is repurposed. Exact verifier subprocesses, return codes, output and candidate SHA are retained under `governance-evidence/`; `governance.log` records method outcomes.

Fresh negative probes cover start-input snapshot, suite receipt, outer execution log and review content; changed inventory root; rehashed inventory omissions; deleted required sidecar; newly unlisted attempt evidence; an identical-byte symlink; rehashed review-role substitution; path escape; fabricated distinct test identities; and both `-O` and `-OO` through focused and direct historical entry points. All fail closed. The ordinary full-release entry point rejects the unchanged historical pointer as lacking a version-2 inventory, confirming the focused positive control is not release acceptance.

## Review feedback resolved during remediation

Initial inspection found the candidate focused verifier checked count/uniqueness but not actual discovered test identities. The implementation now compares against actual discovery; the invented-ID negative case passes.

An initial structural inventory probe could delete the review and redirect its role to an arbitrary file after rehashing the inventory/pointer. The implementation now requires the role paths prescribed by the receipt layout; the independent rehashed-role-substitution case passes. This is structural hardening, not a claim that an unsigned receipt can resist wholesale replacement of its trusted root, source and all evidence.

## Historical preservation

The real historical verifier confirms **8,912 original entries** with the authorized workflow migration. The original preservation manifest, old acceptance pointer and migration contract are byte-identical to diagnostic baseline `4cb7018d0ff2dbb5951954278dac4ff9927630e6`; exact hashes are in `historical-preservation.json`. No original workflow, archived workflow, frozen proof, historical receipt or original evidence artifact was rewritten by these tests. All destructive negative mutations occur only in disposable clones.

## Limits and next ownership

These are fresh synthetic, bounded tests, not a maximum-load endurance exercise or deployed TrackedFR verification. The source identifier and row budgets are behavioral bounds; this review does not claim a general fixed byte-size bound for every possible user-supplied workpaper. TrackedFR must retest its own uploads, session/source mapping, payload partitioning and client handling of qualification/client errors. Full regression, new source-bound release inventory/receipt issuance, independent release acceptance and final CI/readiness remain the subsequent release agent's work. This report neither merges nor deploys nor grants final readiness.
