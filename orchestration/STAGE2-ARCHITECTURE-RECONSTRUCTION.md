# Stage 2 live architecture reconstruction

Verified GitHub main and local checkout: f2c47c03fd2faaafe99b73bf621cee473e53b675 (Stage 1 PR #34 merge). The roadmap records Stage 1 COMPLETE, Stage 2 NEXT, overall IN PROGRESS, persistence NOT YET NEXT.

## Existing authority and extension points

The runtime is CAO.run → Planner/Issue → Graph/Node → production.assess_case → challenge/synthesis → public_record. Registry reads actual live production metadata. No new accounting executor is appropriate. Case in runtime.py already retains independent issue/evidence/workplan/challenge/artifact/lifecycle records. Graph has deterministic node keys, dependencies, readiness, challenge invalidation and retained challenged results. Its current invalidation marks blocked and clears active results; general version currentness and selective multi-Case rework are absent.

ScopeRegistry validates arbitrary LEGAL_ENTITY/SUBGROUP/GROUP identities and organizational parents. execution_identity binds owner, Scope, framework/jurisdiction/currencies and date bounds. OwnerInputs and NodeTable fail ambiguous aliases. Stage 2 must preserve this tuple and compose calendar-qualified Period identity, without deriving Cases or dependencies from Scope parentage.

Current typed receipts bind actual owner result/full fingerprints, exact Scope source/target and native certification. Native owner imports and accounting-specific handoffs retain accounting authority. Their CURRENT flag is an initial-execution property, not a version registry. Stage 2 must add exact-version dependency binding and reject stale/superseded receipts independently of amount equality.

Scoped journal qualification wraps the inherited CAO._qualified_journals gross-line allocator. Its event identity includes posting Scope and bounded period; result supersession must select only current versions before allocation, never synthesize reversal entries. period_selection validates complete sourced acquisition activity windows and specialist-qualified effective dates. Governed Period/effective interval normalization must precede that existing accounting population validation.

## Migration controls

Stage 1 three-entity Revenue proof uses native production certification and local-result observations with unresolved conversion boundaries. Group uses specialist receipts, acquisition cutoff, account-by-account source replay and consolidation-only posting. SaaS, Treasury, Intake, Diagnostic and Manufacturing share CAO/Graph and the public adapter. Single-period callers need deterministic normalization rather than a parallel legacy engine. Existing exact dates and native certification must continue to be checked.

Read: architecture roadmap/system overview/CAO/orchestration/Case/memory/context/artifact specifications; Stage1→Stage2 and Stage1 integration handoffs; Group→Multi-Entity and Group integration handoffs; SaaS/Treasury/Intake/Diagnostic/foundation handoffs. Inspected runtime, planning, registry, scopes, execution, scoped receipts/journals, journal scopes, period selection, intake and interfaces contracts, Stage 1 fixture/proof and all three workflows.

## Planned contract

Governed calendar/Period registry; runtime Case registry composing explicit Scope/Period/objective identity; dependency contracts attached to the existing Graph; immutable result snapshots with separate currentness state; deterministic edge traversal and topological selective rework through existing production authority. Parent status follows declared required dependencies only. Reopening preserves Period identity and closed history using synthetic governed approval conventions. No persistence/authentication or Stage3 conversion/IC network.

## Release gates

Authored controls, genuinely independent attacks/remediation/rerun, all prior migration suites, deterministic artifacts, full repository authority regression and unchanged-head Actions. No roadmap completion before these pass. Government Grants/Borrowing Costs/Investment Property and all knowledge authority remain untouched.
