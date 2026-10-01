# Authority QA execution — checkpoint 2026-10-01

This ledger is an audit work queue, not a claim of completed verification.

## Current state
- Canonical manifest: 157 REVIEWED, 0 APPROVED.
- Historical baseline (2026-09-30): 64 registers / 93 missing.
- Manifest-referenced register paths at this checkpoint: 63 / 94 missing references. TOPIC-16-006 is included in the historical baseline but not in the manifest path references. Its exact topic directory and file existence require confirmation; do not silently assume either count is an independently verified filesystem inventory.
- Promotion threshold: `knowledge/standards-evidence/approved-gate.md`.

## Execution batches
1. Reconcile the register inventory and TOPIC-16-006 discrepancy. Validate existing JSON, global claim IDs and evidence invariants.
2. Scope-review each missing-register topic; extract material standards claims or document a reasoned non-normative finding. Empty registers are not a shortcut.
3. Recheck every existing SOURCE_VERIFIED claim against applicable current operative text, effective period and entity scope. Downgrade labels if inspection evidence is inadequate.
4. Research remaining claims against current authorized IFRS, FASB, FRC, AASB, SEC and applicable legislation. Use official amendments and reputable literature to corroborate inaccessible text, never to simulate direct inspection.
5. Independently QA batches of 5–10 topics, including cross-framework, adversarial, numerical and rights regression. Controller alone promotes individually passing topics in the manifest and then reconciles derived reporting.

## Initial candidate queue
- TOPIC-02-009: sampled register has 19 claims, 11 labelled SOURCE_VERIFIED and 8 corroborated. Revalidate all 19 before considering approval.
- TOPIC-04-001: sampled register has seven claims, none labelled SOURCE_VERIFIED.
- TOPIC-03-001: sampled register has 165 claims, including 150 MODEL_DERIVED_AUDIT_REQUIRED. Audit duplicate legacy/granular records and all material claims.

## Access and licensing
Try FASB official Codification Basic View and IFRS registered Standards Navigator first. Authorized human inspection may supply documented verification where automated retrieval fails. Official ASUs, amendments, regulator summaries and professional literature support corroboration only unless the applicable operative text is directly inspected. Record precise locators and versions without committing restricted paragraph text, licensed PDFs, credentials or unlicensed reproductions.

## Checkpoint disposition
No topic promoted by this checkpoint. Continue the claim-level audit; do not infer APPROVED from substantive REVIEWED.
