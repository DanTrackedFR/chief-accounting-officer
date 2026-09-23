# Phase 2D Regression Review — 2026-09-23 A

Status: ACTION REQUIRED / build continues

## Scope
Repository architecture and recent knowledge-factory output reviewed while deepening policy/estimate/error topics.

## Finding 1 — duplicate topic directories
The repository contains multiple directories for the same stable topic IDs (examples observed for TOPIC-02-001, TOPIC-02-003, TOPIC-02-004 and TOPIC-02-006). This creates a source-of-truth risk: two knowledge files can claim the same stable topic ID with different names/content.

### Rule established
- Stable topic ID is the canonical key, not folder slug.
- Do not create another folder for an ID when one already exists; fetch/update the best existing canonical record.
- A future cleanup pass must inventory duplicate-ID paths, choose canonical paths, merge unique substantive content, then remove/supersede duplicates without losing provenance.
- Duplicate cleanup is an architecture hygiene task, not a blocker to continuing untouched topics.

## Finding 2 — shallow REVIEWED records
Some earlier Phase 2D records marked REVIEWED contain good operational logic but limited framework/source depth. Status alone cannot be used as evidence that a topic has passed the full factory.

### Rule established
Final programme summary must distinguish:
1. factory-complete/deep-reviewed;
2. reviewed but needing source-depth expansion;
3. partial/blocked.
No completion percentage may count a shallow record as full factory completion merely because its front matter says REVIEWED.

## Finding 3 — cross-topic reuse is essential
Policy/estimate/error knowledge demonstrates that duplicating IAS 8/ASC 250/Section 10/AASB 108 analysis across every dependent topic would create drift. Topic records should reference reusable classification engines while retaining topic-specific application.

## Regression outcome
Build continues. No accounting conclusion was changed by this review. Repository normalization is logged as required cleanup before final Phase 2D closure.