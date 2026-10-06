# Stage 3 governed cross-scope reporting contracts

## Identity and matching

`Node.economic_id` optionally composes a commercial transaction qualifier into existing execution identity. Absent/None retains prior identity byte-for-byte. The same native owner/Scope/Period can execute separate transactions; Scope, Case, Period and version identity are not replaced. Display/account labels, ordering, amounts and filenames are excluded from transaction identity. Native source economic identity and scoped journals retain the qualifier.

`TransactionSide` binds network/agreement/economic/book-entry IDs, legal Scope/counterparty, originating and reciprocal Case/Period, exact native result version/metric, original transaction and functional amounts/currencies, and actual reviewed native source row. The current bounded adapter supports ordinary loan sides through Intercompany's actual principal/functional outputs. Other semantic adapters remain unavailable. Unknown/self/Group/Subgroup legal counterparties fail.

The business relationship registry never inserts execution dependencies. Explicit Stage 2 Dependency contracts establish all edges. Business triangles may cycle; Graph rejects execution cycles. `MatchingDecision` selects exact legal sides/versions. No fuzzy or amount-only match exists. Calendar alignment is reviewed; different dated Periods cannot become clean matches. Both legal sides survive. Residuals remain explicit, without generated corrections. A completed matching analysis is not resolved accounting: material unresolved dependencies keep Case outcome partial.

## Native transformations

Existing production owners remain the accounting boundary. Native input mappings bind actual owner TB/pair/elimination paths and all financially material exact-version receipts; shadow annotations cannot qualify input. Source packs must already possess independent native certification. Runtime never generates replacement approvals.

The bounded proof sequence is local US-GAAP result -> native US-GAAP EUR translation -> native IFRS ordinary reciprocal-balance reassessment -> Group elimination -> Financial Statements. This fixture-specific ordering is explicit, not a universal conversion policy. Foreign Currency determines all translated amounts and CTA from supplied reviewed rates and balanced functional TB.

The supported framework path is separately certified IFRS ordinary IC reassessment preserving original transaction principal, actual counterparties and qualified Group-currency carrying values. Supported adjustment is zero; equal numbers alone cannot supply qualification. No generic converter exists. Other/general recognition or measurement conversion remains unresolved. Source US_GAAP persists until an actual IFRS production result exists.

## Receipts, postings and lifecycle

CrossLayerReceipt retains exact producer/consumer nodes, Scopes, Cases, Periods, result/source fingerprints, version/currentness, accounting layer, semantic metric, economic identity and required framework/currency. Owner/layer/path semantics are governed. Translation cannot masquerade as legal currency; raw US-GAAP/USD cannot meet IFRS/EUR Group requirements. Native transformation receipts retain actual rate/evidence populations and currentness.

Consolidation binds translated TB to the producing legal Scope plus separate exact CTA reserve/movement dependencies. Unsupported balancing offsets cannot hide differences. Financial Statements binds every actual consolidated account. Native Consolidation retains accounting authority and distinct Group journals.

ReportingBasis.current_journals uses the inherited scoped gross-line allocator. Current local IC implications belong to the actual legal book; Consolidation implications belong to Group. Translation already embodied in the qualified Group TB is explicitly witnessed evidence, not another legal/Group posting. Dispositions bind entity population, exact versions and CTA. Superseded results cannot contribute current economics; supersession creates no reversal.

Ordinary CAO.run/correct/selective_reexecute uses the Stage 2 substrate. One transaction correction supersedes its version and selectively refreshes only declared consumers. Unrelated transactions sharing owner/Scope/Period stay current. In-memory governance and synthetic fixture reviewers remain existing limits; Stage 4, persistence and authenticated approvals are not implemented.
