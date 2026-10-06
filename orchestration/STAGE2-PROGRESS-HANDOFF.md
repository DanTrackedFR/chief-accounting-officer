# Stage 2 durable intermediate checkpoint — continuation required

Repository: DanTrackedFR/chief-accounting-officer. Baseline main f2c47c03fd2faaafe99b73bf621cee473e53b675. Continue only branch `orchestration/case-period-invalidation`, Draft PR #35. No merge, no replacement PR, no Stage 3/4/persistence. The pushed checkpoint SHA belongs in PR metadata (not this self-referential file).

## Completed intermediate implementation

- Live architecture reconstruction committed before implementation.
- `periods.py`: deterministic calendar-qualified immutable Period records; explicit CURRENT/PRIOR/COMPARATIVE/OPENING/PARTIAL_INCLUDED_PERIOD relationships; interval/cycle validation; effective acquisition/disposal intervals; OPEN/CLOSED/REOPENED lifecycle; synthetic governed reopening; canonical serialization loader that replays and verifies lifecycle history.
- `cases.py`: registry composing existing runtime Case with Scope, Period, objective and cycle identity; ENTITY_CASE/SUBGROUP_CASE/GROUP_CASE support; explicit parent/child references; node binding; independent Case issue/evidence/status/result-version structures; dependency-aware rework state and retained governance history.
- Existing Node/Case dataclasses extended. Stage 1 execution identity tuple is unchanged for existing callers; an explicitly governed Period ID composes with it for temporal callers. Source Period/calendar qualification lives in scoped_context.
- `versions.py`: immutable result snapshots, predecessor/supersession lineage, separate CURRENT/STALE/SUPERSEDED states, exact-version dependency bindings and receipts, direct/transitive invalidation, bounded topological rework plan and selective rerun on existing Graph. Production execution goes through CAO/native assess_case; bounded orchestration consumers cannot claim accounting authority or postings. Late dependency insertion after consumer publication fails closed.
- `current_journals` selects only current exact-version owner implications through the existing scoped gross-line allocator. Scoped event qualification now includes governed Period/version where supplied. Opening/observation results create no postings; supersession creates no reversal.
- Existing Group activity cutoff now passes through generic Period/EffectiveInterval normalization before inherited population and specialist qualification checks; original accounting conclusions preserved.
- Controlled proof: GROUP-EUR, ENTITY-NL, ENTITY-US, ENTITY-UK; five governed Cases; calendar-year/US July fiscal calendars; September/October, explicit opening/comparative relationships and acquisition interval. Nine nodes include native Revenue at US September, US October and UK September. US September source progress correction changes actual production Revenue 800→900, supersedes original, stales precisely US reporting→US October opening observation→Group October local observation→Group analytics observation, then selectively reruns four nodes. UK and independent controls remain current. Group outputs remain local USD observations with unresolved conversion, never consolidated EUR accounting authority.
- 31 deterministic Stage 2 artifacts in `examples/case-period-invalidation/`; generator `python -m orchestration.tests.generate_stage2_examples`. Seven executable lineages preserve Scope/Period/version/dependency/currentness.
- 41 authored Stage 2 tests; 41 independent Stage 2 tests and eight remediated substantive finding classes. `STAGE2-INDEPENDENT-QA.md` records independent review, reproducers, dispositions and intermediate reruns.

## Validation evidence and limits

Authored Stage 2: 41 PASS. Independent reviewed intermediate implementation: 41 PASS; eight substantive finding classes remediated; independent reviewer reports zero unresolved findings in inspected intermediate scope. Independent Stage 1 authored+independent: 96 PASS. Independent generator checks: same 31 artifacts under PYTHONHASHSEED 19 and 941. All eight orchestration generators completed successfully, including Stage 2. No manual artifact edits.

A combined Stage2/Stage1/Group run executed 125 distinct methods: 124 passed and one Group artifact comparison failed because new dataclass fields required regeneration. The existing generators were rerun afterward. Record the focused post-regeneration rerun result in PR metadata. This is not a completed full migration/full repository regression. Repeated reruns must not inflate distinct totals.

No full orchestration/production/lease/canonical/supplemental regression or authority validators have been completed for this checkpoint. No immutable final candidate exists; no exact-head CI completion is claimed. Roadmap remains Stage2 NEXT (incomplete), Stage1 COMPLETE, Stage3/4 PENDING, overall IN PROGRESS, Durable Case/Memory NOT YET NEXT.

## Outstanding Stage 2 gates

1. Deliberately integrate generalized Case/Period/version governance into ordinary CAO.run and all prior single-period callers. Present native Stage2 execution uses existing CAO production boundary and Graph, but ordinary CAO.run still does initial execution through its established lifecycle without full version/Case registry normalization. Do not claim this compatibility work is complete or retain a hidden parallel temporal path.
2. Complete repeated-owner temporal issue selection in ordinary planner/intake (currently Issue scope selection cannot disambiguate multiple Periods for one Scope). Extend exact input/result/ReviewedInputPack/typed receipt handling generically; preserve Stage1 aliases and identity behavior.
3. Complete all required executable opening/comparative/restatement/current receipt contracts and adversarial tests, rather than relying only on represented Period relationships. Add Subgroup-specific lifecycle/status controls, explicit cross-entity nonconsuming Group control, unrelated Treasury/future-period controls, all requested period/journal attacks and canonical serialization/version-lineage validation coverage.
4. Confirm native accounting consumer exact-version input certification contracts. Current bounded entity/opening/Group/analytics consumers are deliberately nonauthoritative dependency observations, not actual FS/analytics accounting execution. Production owners remain authority. Do not fabricate conversions or journals to strengthen the proof.
5. Broaden independent QA to the completed architecture/all 32 requested attack categories after remaining integration. Eight reviewed findings are remediated, but intermediate acceptance is not final release acceptance.
6. Complete deterministic artifact requirements: adversarial executable result witness, architecture reconstruction witness, Stage3 handoff witness and final status/lineage/public controls; regenerate every prior flagship after final implementation; compare byte-for-byte under independent seeds.
7. Run all authored+independent temporal/Case/receipt/journal/privacy suites, Stage1, Group/Treasury/SaaS/Intake/Diagnostic/Manufacturing/ordinary single-entity migration and full repository regression. Report distinct tests accurately. Run all supplemental validators, canonical approvals, standards evidence and git diff --check.
8. Author actual final `MULTI-ENTITY-STAGE2-TO-STAGE3-HANDOFF.md`, final integration handoff/regression record and limitations. Existing checkpoint is not that final handoff.
9. Only after substantive gates pass, advance roadmap exactly one Stage; regenerate only authorized roadmap witness. Do not mark overall workstream complete or persistence NEXT.
10. Commit/publish immutable final candidate; enable/run all three required workflows on that exact head; resolve real defects; update this existing PR and mark ready only after exact-head green; allow any required readiness reruns. Do not merge.

## Next action for a fresh agent

Read this checkpoint, `STAGE2-ARCHITECTURE-RECONSTRUCTION.md`, the principal Stage1→Stage2 specification and independent QA record on the SAME PR head. First design/implement safe normalization of ordinary CAO.run into the governed Case/Period/version substrate, with temporal issue disambiguation, and add focused migration regressions. Preserve completed code/tests/artifacts; avoid gratuitous reruns of passed intermediate controls until changes justify them. Use GitHub connector commits/ref updates for durable milestones: ordinary HTTPS Git push has no credentials here, though public clone/fetch works. Keep local checkout aligned with connector commit tree; never discard useful changes.

## Preserved exclusions

No Government Grants PR #27/package, Borrowing Costs, Investment Property, canonical knowledge, approvals or supplemental accounting knowledge was substantively changed. No accounting authority, generalized intercompany network, framework conversion, generalized FX chain, durable storage, authenticated governance or Stage4 flagship was introduced.

This checkpoint is incomplete. Work stopped under the user's context/runtime reliability continuation rule, not an external accounting blocker or successful Stage2 completion.
