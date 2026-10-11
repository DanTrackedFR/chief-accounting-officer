# CAO MVP Build 1 completion report

Baseline: `ea19ee62c938dba06f3faf758a75e17a7da27e15`.
Branch: `mvp/local-cao-execution-contract`.
PR: https://github.com/DanTrackedFR/chief-accounting-officer/pull/44.
No merge occurred. Specialist PRs #27, #42 and #43 were not modified.

## Implemented

The version 1.0 `local_cao.ExecutionInterface.call(JSON)` contract and stdin/stdout
CLI compose the existing CAO runtime, production owners, public boundary and
SQLiteStore. No accounting methods, registry, planner, lifecycle, memory engine,
native source qualification or historical reference artifacts were changed.

Operations: initialize, diagnose, context, capabilities, start, status, questions,
submit, execute, result, resume and list. Request/response schemas and
interfaces/CAO-EXECUTION-CONTRACT.md define identity, state, errors, currentness,
immutable retries, evidence references and future authenticated transport boundaries.

Install/use: docs/LOCAL-CAO.md. Clone/checkout this branch, use Python 3.12+ on
Linux/macOS or WSL, create .cao-local, copy/edit company-context.example.md,
initialize/diagnose then launch your installed Claude Code. Accounting uses only
Python's standard library and needs no Anthropic credentials or hosted service.
CLAUDE.md requires native execution and curated results rather than unaudited
conversational calculations.

Markdown establishes explicit stable company/entity/calendar and bounded period
configuration. Duplicate or contradictory execution keys reject. Company narrative,
policies, user preferences and source links remain unreviewed assertions/metadata;
they cannot approve policy or promote Company Accounting Memory. Semantic conflicts
in arbitrary narrative still require human clarification. Private context, default
workspaces and SQLite files are Git-ignored; custom workspaces must be ignored too.

## Actual execution and acceptance

Fresh-process CLI proof invokes two native production owners with existing synthetic
reviewed workpapers: fixed-assets depreciation produces EUR90,000 of owned journals;
accounts-payable produces EUR9,600 accrual journals and a native EUR20 closing-AP
public calculation. Fixed-assets' curated calculation array is empty under native
public semantics; its real calculation is evidenced by the native journal result.
No demonstration substitutes a precomputed adapter answer for owner execution.

Both scenarios persist through native schema 3 SQLite checkpoints and restore in
fresh processes at revision 1. Result fingerprints and journals are unchanged on
retry; persisted operations do not reexecute owners. Input submissions are immutable
and atomic. Company isolation, source boundaries and native currentness are preserved.

Revenue without a contract and prepayment investigation without reconciliation each
return blocked results, no calculations/journals and actionable requirements.
Signed agreement/price/obligations/delivery support or reconciliation/comparative
trial balances/movements/thresholds must be supplied, not invented.

**3,050 distinct tests passed, exit 0, zero failures/errors/skips:** 2,995 existing
repository tests plus 25 authored and 30 genuinely independent tests. The existing
population includes 1,344 orchestration tests and 1,651 skills, Leases, public/canonical
and supplemental-knowledge tests. Seven supplement/claim/approval validators also
returned exit 0. Historical deterministic artifact reproduction passed unchanged.
Two full fresh-process CLI proofs under hash seeds 19 and 941 are byte-identical to
the committed proof. local_cao/release/release-regression.json contains every distinct
test ID, actual suite durations, bounded log hashes, proof hash and tested source
manifest. The frozen 320-file Python manifest was rechecked before publication.

Independent QA repaired three significant reproduced defects: empty execution
freezing a Case, identical retry rejection and unrelated evidence completing the
declared target. An authored staged-read execution defect was independently retested
after repair. Permanent regressions cover these and filesystem/atomicity attacks.
No significant reproduced defect remains unresolved in the reviewed bounded facade.
See architecture/CAO-MVP-BUILD1-INDEPENDENT-QA.md for executed coverage and limits.

The immutable final publication SHA and exact-head GitHub Actions results, including
ready_for_review-triggered runs, are recorded in PR 44's final release-evidence comment.
Those remote gates must pass before readiness; this source-controlled record reports
source-frozen local acceptance and cannot self-reference its containing commit SHA.

## Boundaries and next build

Claude Code itself was unavailable. The exact underlying CLI was independently tested;
the documented live-Claude smoke prompts still require owner validation. This is the
explicit permitted fallback, not a fabricated live conversational demonstration.

One selected legal entity/period, client-declared supported native fact family and
controlled qualified workpapers are supported. Partially committed Cases preserve
unresolved work but cannot accept replacement reviewed evidence through this facade.
Native sealed CORRECT/REWORK and memory promotion remain native operations awaiting
qualified integration. No binary extraction, general live model planner, autonomous
follow-up evidence gathering, Google Drive/ERP retrieval, posting, hosting or SaaS
authentication was added.

Build 2 can reuse the versioned envelopes, stable identities, context parser, dynamic
capability metadata, curated results, safe errors, immutable staging and native resume.
It must compose existing intake/rework authority rather than build another engine.
architecture/TRACKEDFR-CAO-FINANCE-CONTEXT-REQUIREMENTS.md is the actionable separate
Replit-agent specification, distinguishing verified CAO contracts, proposed context
extensions and unseen TrackedFR schema mappings needing inspection. The integration
handoff explains future Express-to-authenticated-Python transport and ownership.
