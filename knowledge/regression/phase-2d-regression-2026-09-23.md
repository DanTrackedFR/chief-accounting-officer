# Phase 2D Regression Review — 2026-09-23

Status: ACTION REQUIRED / programme continues

## Scope
Regression review after the first recurring-controller/revenue build batches.

## Findings
1. **Knowledge depth is scaling appropriately.** Operational topics are principles/practice-heavy; standards-sensitive topics use framework routing and authoritative source families.
2. **Source-depth limitation is being handled correctly.** Some US GAAP topics are REVIEWED / US SOURCE-DEPTH PARTIAL because public FASB materials do not expose every current Codification paragraph body. This is recorded rather than invented and is not a blocker to building other topics.
3. **Effective-date routing is essential.** FRS 102 Periodic Review 2024 creates a major 1 January 2026 routing boundary for revenue and leases. AASB current-version routing can also require uncompiled amendments during 2026.
4. **Canonical-path drift detected.** The repository contains multiple folders for some identical stable topic IDs (for example TOPIC-02-001 and other Domain 02 topics) created under different descriptive slugs during separate build batches. Stable topic ID, not slug, must be the uniqueness key.
5. **Do not count duplicate folders as completed topics.** Progress metrics count unique topic IDs only.

## Required architecture correction
Before final programme completion, run a canonicalization pass:
- choose one canonical folder per stable topic ID;
- merge the strongest content and provenance;
- preserve commit/history references;
- delete redundant duplicate folders only after content comparison;
- add an automated validation that fails when more than one topic folder begins with the same `TOPIC-DD-NNN-` prefix;
- use the topic-universe ID as the write-time lookup key before creating a folder.

This issue does not block knowledge population, so the programme continues under the user's blocker rule.

## Revenue-family regression
The five-step architecture remains coherent across TOPIC-03-001 onward. Cross-topic boundaries are preserved: contract/scope/promises/initial transaction price → variable consideration/allocation → timing/modification → principal-agent/contract balances → contract costs/billing → AR/ECL/cash/disputes → reconciliations → disclosure/controls.

## Quality guardrail
A topic may be REVIEWED with an explicit source-depth qualifier. It may not be APPROVED/COMPLETE if a material framework conclusion depends on unverified authoritative text. No topic is blocked merely because one framework has a source-depth limitation; record limitation and continue.