# Stage 2 integration handoff — INCOMPLETE

Release correction: Stage 2 is incomplete. The earlier completion wording on head `29f9ae126ac1a577187d3d6c5a44bbdff315ed89` was disproved by fresh executable independent review. This document is provisional; final architecture, regression and exact-head acceptance must be rewritten after the remaining gates pass. PR #35 is Draft and unmerged. See `STAGE2-PROGRESS-HANDOFF.md` and `STAGE2-FINAL-INDEPENDENT-QA.md`. No Stage 3 work is authorized.


Stage 2 — Case Hierarchy + Multi-Period + Dependency Invalidation/Rework.

Baseline main: `f2c47c03fd2faaafe99b73bf621cee473e53b675` (Stage 1 merged). Delivery branch: `orchestration/case-period-invalidation`, PR #35. The immutable final SHA and exact-head workflow conclusions belong in PR metadata after finalization to avoid a self-referential committed hash.

## Delivered architecture

Stage 2 composes the Stage 1 Scope substrate with governed Case, Period, dependency and result-version identity. ENTITY_CASE, SUBGROUP_CASE and GROUP_CASE retain independent governance; Scope hierarchy, Case hierarchy and dependency graph are separate. Periods are deterministic and calendar-qualified, with explicit opening/prior/comparative/partial relationships, effective intervals and close/reopen history.

Ordinary runtime repeated-owner issue/input selection is Scope + governed Period aware. Governed `period_id` is propagated into ordinary workplan nodes when supplied, while simple legacy callers retain the Stage 1 compatibility path.

Dependencies bind exact producer/consumer nodes, Cases, Scopes and Periods. Immutable result versions preserve CURRENT / STALE / SUPERSEDED state and exact dependency bindings. Supersession preserves history. Stale/superseded/wrong-Scope/wrong-Period receipts cannot satisfy current dependencies.

Invalidation traverses actual dependency bindings only. Selective re-execution is topological and rejects unrelated reruns. Reopening is a governance/version event and does not create an accounting reversal. Period-aware journals admit only current exact-version economics through the inherited scoped exact-once allocator.

## Controlled proof

The bounded proof uses GROUP-EUR, ENTITY-NL, ENTITY-US and ENTITY-UK with calendar-year and US fiscal-calendar identities. It includes September/October, opening/comparative relationships and a bounded effective interval.

A qualified native US September Revenue result is corrected from 800 to 900. The old result is superseded. Actual downstream US reporting → US October opening observation → Group October observation → Group analytics observation becomes stale and is selectively re-executed. UK and independent controls remain current. The Group/analytics observations remain non-authoritative and do not manufacture framework conversion, FX translation or consolidated-EUR accounting.

## QA and deterministic evidence

Authored and independent Stage 2 suites cover Case/Period identity, hierarchy separation, exact-version receipts, stale/superseded rejection, invalidation, selective rework, reopening, journal currentness, privacy and deterministic graph behavior. The independent QA record preserves the substantive finding/remediation history rather than erasing it.

Deterministic Stage 2 artifacts under `orchestration/examples/case-period-invalidation/` provide before/after result versions, dependency/invalidation/rework ledgers, Case/Period registries, journals, receipts, lineages and public output. Final exact-head regression and workflow results are recorded in PR #35 metadata.

## Migration

Stage 1, Group Accounting, Treasury, SaaS, Semantic/Data Intake, Diagnostic Analytics, Manufacturing and ordinary single-entity execution remain migration gates. Existing Group acquisition cutoff logic is normalized through generic Period/EffectiveInterval infrastructure without changing specialist accounting authority.

## Boundaries

Stage 2 introduces no generalized intercompany network, general framework-conversion engine, generalized multi-step FX translation, durable persistence, authenticated governance or new accounting authority. Stage 3 and Stage 4 remain unimplemented.

Government Grants PR #27/package, Borrowing Costs and Investment Property remain untouched.

## Next

After owner review and merge, Stage 3 starts from the resulting live main and follows `orchestration/MULTI-ENTITY-STAGE2-TO-STAGE3-HANDOFF.md`.
