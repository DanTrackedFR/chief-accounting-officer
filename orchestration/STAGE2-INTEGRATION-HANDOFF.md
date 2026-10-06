# Stage 2 integration handoff

Delivery: existing `orchestration/case-period-invalidation`, PR #35. Baseline live main `f2c47c03fd2faaafe99b73bf621cee473e53b675`; final immutable SHA and exact-head workflow conclusions are recorded in PR metadata, avoiding a self-referential committed hash. No merge.

## Delivered architecture

The existing CAO.run, Graph and production boundary compose with ScopeRegistry, PeriodRegistry, CaseRegistry and VersionedExecution. ENTITY_CASE, SUBGROUP_CASE and GROUP_CASE retain objective/cycle identity, lifecycle and result references. Scope parentage, Case parentage and execution dependencies remain separate; membership never infers consumption or invalidation. Simple legacy callers normalize through compatibility Periods with unknown fiscal starts explicitly retained, while supplied Period registries require exact calendar identity.

Issue.period_id is a real serialized field. Planner source/import traversal, semantic proposals, OwnerInputs, ReviewedInputPacks and all bindings retain exact owner + Scope + Period. Temporal facts and native/auxiliary source manifests bind actual Period/calendar/relationship role and exact source inventory. Ambiguous material Periods produce blocking questions; same-Scope questions retain their separate Periods. September evidence cannot certify October or be relabelled as opening/current/comparative. Scope activity is authorized using the actual execution interval; valid historical journals use their own interval.

Dependency contracts bind producer/consumer nodes, Cases, Scopes, Periods, semantic metric and declared relationship. Receipts bind exact immutable producer result version, currentness, fingerprint, metric and both framework/currency contexts. STALE/SUPERSEDED, wrong-period, wrong-dimension and equal-value substituted receipts fail. Native dependent corrections require separately reviewed exact-version receipts and native certification; orchestration never manufactures accounting approvals.

CAO.correct publishes a reviewed new native or bounded version on the existing graph. CAO.selective_reexecute validates the exact topological plan, reruns only actual consumers, checks currentness and refreshes ordinary delivery. Consecutive corrections retain pending consumers bound to any replaced predecessor. Ordinary synthesis captures its exact version/currentness view; changed views cannot republish historical conclusions. Correctly qualified partial diagnostic bridges preserve their residuals and limitations.

Closed Periods require explicit synthetic governed reopening with qualified Case/node authorization. History is retained and can reclose. CAO.restate adds governed original-to-new-version lineage without granting accounting restatement authority. Supersession/reopening creates no reversal. Only exact current versions contribute through the inherited scoped gross-line journal allocator; aliases and historical versions cannot double count economics.

## Executable proofs

Central ordinary proof: native Revenue / ENTITY-US / September 800 -> US September reporting -> US October opening/downstream -> Group October local reporting -> Group October local analytics. The independently reviewed correction changes Revenue to 900; v1 remains immutable SUPERSEDED and v2 is CURRENT. Exactly US-REPORT, US-OPEN, GROUP and ANALYTICS stale and rerun in topological order. Public Group observations update to900 USD.

Eight unaffected controls keep their exact CURRENT versions: US-OCT native Revenue, UK-SEP Revenue, UK-CONTROL, NL-CONTROL, TREASURY, FUTURE (November), GROUP-CONTROL (nonconsuming) and UK-COMPARATIVE. Treasury is an unrelated observation control, not a new Treasury accounting treatment. Opening lineage carries exact prior-closing producer version into the actual next-period consumer.

A separate UK restatement proof preserves original September and comparative payloads, supersedes their delivery versions and reruns only the actual October comparative consumer. Structural SUBGROUP proof uses the same ordinary governed-plan execution, Case/Period identity and current receipts; US correction propagates only through its declared subgroup/Group edges. Bounded observations produce no journals or converted accounting totals. Three native Revenue executions contribute18 current journal implications; corrected history adds no extra current implications.

## Independent QA and release validation

All earlier eight intermediate finding classes and final F1-F14 history are preserved in the two QA documents. Final separate-context reviewer reran 118 distinct Stage2 methods plus the existing diagnostic residual migration regression; zero unresolved substantive findings. Permanent tests cover auxiliary/native temporal evidence, material questions, consecutive correction, Scope activity, prior-period journal qualification and public synthesis currentness, alongside original receipt/period/journal attacks.

Final local release: 2301 distinct tests PASS:650 orchestration,1180 production skills,17 leases,53 repository/canonical and401 supplemental/independent knowledge. Stage2 has133 distinct methods; the118 independent-review run is a subset and reruns are never added to totals. All Stage1, Group, Treasury, SaaS, Intake, Diagnostic, Manufacturing and ordinary compatibility suites pass. Both canonical approval and standards-evidence validators, all supplemental validators and diff check pass. Details: STAGE2-RELEASE-REGRESSION.json.

All eight governed generators regenerated their artifacts; all reproduce under independent PYTHONHASHSEED 19/941. Stage2 has 37 artifacts covering versions before/after, receipts, invalidation, unaffected nodes, topological rerun, journals, close/reopen, opening/comparative/restatement, SUBGROUP, intake, adversarial controls and public output. Existing reference exports retain version hashes/bindings without duplicating native imported workpapers; full immutable runtime snapshots and Stage2 version witnesses remain preserved.

## Limits and next work

In-memory serializable governance only; approvals are synthetic regression conventions. No authenticated governance, persistence, generalized intercompany network, framework conversion or translation chains. Local reporting/opening/comparative/subgroup/analytics observations prove orchestration lineage, not new accounting treatment, formal restatement approval or consolidated-EUR totals. Production owners remain authority. Missing native mappings/certifications and unsupported temporal input assemblies fail closed; no model inference or automatic recertification fills them.

Stage 1 COMPLETE; Stage 2 COMPLETE; Stage 3 NEXT (only after owner review/merge); Stage 4 PENDING; overall Multi-Entity/Multi-Period IN PROGRESS; Durable Case/Company Accounting Memory NOT YET NEXT. Stage 3/4/persistence were not started. Government Grants PR27/package, Borrowing Costs, Investment Property and canonical/supplemental knowledge are unchanged. Only the authorized generated roadmap protection witness is regenerated.

After immutable-head required CI succeeds, PR35 is ready for owner integration review and remains unmerged. Follow MULTI-ENTITY-STAGE2-TO-STAGE3-HANDOFF.md only after owner integration.
