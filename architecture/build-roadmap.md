# Build Roadmap

## Phase 1 — Operating system
Status: complete.

## Phase 2A — Knowledge infrastructure
Status: complete. Active frameworks: IFRS, US GAAP, UK GAAP and AASB. NZ IFRS deferred.

## Phase 2B — Topic universe
Status: complete. 157 top-level topics; 347/347 primary capability coverage.

## Phase 2C — Leases vertical slice
Status: complete as architecture checkpoint. Full factory proven end-to-end.

## Phase 2D — Full knowledge population
Status: COMPLETE AT SUBSTANTIVE REVIEWED LEVEL.

Canonical status source: `knowledge/phase-2d-topic-manifest.json`. Current independently reconciled substantive status: **0 REVIEWED, 0 PARTIAL, 0 NOT_STARTED, 0 BLOCKED, 157 APPROVED** across 157 canonical topics, with **347/347** canonical capabilities covered. All three Phase 2D production workstreams are integrated; there is no remaining substantive worker closure queue.

REVIEWED and standards-evidence assurance are separate axes. A REVIEWED topic may still contain claims requiring direct authoritative-source verification. APPROVED uses the owner-authorised two-track gate. Individually signed-off topics passed scope, claims, adversarial and relevant numerical review; source-evidence labels remain independent.

### Execution rule
For each canonical topic, complete the appropriate full factory: principles/standards/practice, authoritative sources where applicable, framework differences, CAO execution logic, examples/calculations where relevant, documentation, controls/audit/disclosures/systems, capability integration, scenario tests and QA. Operational topics must not manufacture four-framework records. Promote to REVIEWED only when evidence is recorded in the manifest. APPROVED remains a separate higher bar.

### Tracking rule
Update the canonical manifest first. Derived progress reports and roadmap are regenerated only after the manifest update. Duplicate/retry folders never count as additional topics. Preserve useful duplicate material until canonicalization is safe.

### Next sequence
Phase 2D and the full Phase 2E two-track approval audit are closed. Preserve the individual evidence and run both standards-evidence and canonical approval validators after changes. Future direct-source assurance work remains a separate queue; access restrictions alone do not reverse owner-authorised training-data approvals.

## Phase 3 — Production skills
Status: substantially complete for current product development.

All 50 roadmap positions are accounted for. Current live-main position after the specialist build:
- **47 production skills**.
- **#34 Government Grants & Assistance** — incomplete/WIP; the existing main package remains NONPRODUCTION. Separate remediation work may exist on an unmerged branch and must not be treated as live production.
- **#35 Borrowing Costs** — deferred; existing package remains explicit NONPRODUCTION/fail-closed pending separately governed substantive knowledge.
- **#37 Investment Property** — deferred; existing package remains explicit NONPRODUCTION/fail-closed pending separately governed substantive knowledge.

The three residual packages do not block CAO runtime/orchestration development. Orchestration must detect unavailable owners and return precise partial/blocked dependencies rather than fabricate accounting.

### CAO Orchestration Foundation
Status: **complete and integrated**.

The governed runtime now supports objective-led issue decomposition, a dynamic dependency graph, production-skill execution through the existing accounting boundary, semantic/exact-once owner handoffs, Case lifecycle, active challenge/rework, curated synthesis, Context Observer memory candidates and runtime public-output filtering. The manufacturing flagship proves multi-skill orchestration from a broad user objective without requiring the user to name internal skills.

This foundation is intentionally bounded: it is not yet arbitrary natural-language/document understanding, every skill combination, multi-entity/multi-period execution, durable persistence, authenticated approvals or a complete product UI.

## CAO runtime & intelligence workstreams — unnumbered
Do not rename these workstreams as a new numbered project phase unless the owner explicitly authorises that roadmap change.

### 1. CAO Intent & Diagnostic Analytics Foundation — COMPLETE
Status: **complete**. Governed intent, bounded diagnostic methods and the manufacturing diagnostic flagship passed authored, independent adversarial and full repository regression, plus exact-head GitHub Actions on the integration candidate. See `orchestration/DIAGNOSTIC-INTEGRATION-HANDOFF.md`; final publication repeats CI after this documentation update. Semantic Planner + Document/Data Intake is described below.

The CAO must determine not only which accounting topics are implicated, but what the user is actually trying to accomplish. Intent/work-mode decomposition should distinguish and combine, as appropriate:
- diagnostic analytics;
- technical accounting / accounting determination;
- close review;
- reconciliation / investigation;
- reporting;
- process and controls review;
- audit support;
- documentation;
- transaction accounting.

These are orchestration work modes, not replacement skills.

Diagnostic analytics must become a first-class cross-skill capability. The CAO should be able to explain **what changed, why it changed, whether the accounting is reliable, and what action or further work is required**, while routing any accounting-treatment conclusion back through the relevant governed accounting owner.

Core analytical capabilities should include, where supported by supplied data:
- period-over-period and actual-versus-budget/forecast/standard bridges;
- price / volume / mix analysis;
- material price, usage and yield analysis;
- labour rate and efficiency analysis;
- overhead spending, capacity and absorption/recovery analysis;
- FX impact;
- product/customer/geography mix;
- gross-margin and cost-driver bridges;
- unusual journal / close-movement analysis;
- balance flux analysis;
- trends and controlled anomaly identification;
- reconciliation of analytical explanations back to accounting/GL movements.

Analytics may generate and test **hypotheses**, but must not turn a hypothesis into an accounting conclusion. For example, analytics may identify low factory utilisation as the driver of margin deterioration; the Inventory & Cost owner determines the accounting treatment of under-absorbed overhead.

Analytical bridges must preserve source/owner lineage, avoid double counting and expose unexplained residuals. A bridge should reconcile explained drivers plus residual to the actual movement rather than burying unresolved amounts in “other”.

The first diagnostic flagship should reuse the manufacturing environment with a user objective such as:

> “Our factory margins look terrible this month. Can you review the close and figure out what’s going on?”

The CAO should recognise this primarily as a diagnostic-analytics / close-integrity task, draw governed data and outputs from the relevant accounting owners, decompose the margin movement, distinguish genuine economic drivers from accounting errors/timing, and invoke technical accounting only where the findings create an accounting question.

Independent QA must challenge at least:
- correlation presented as causation;
- double-counted analytical drivers;
- overlapping price/mix/FX/usage effects;
- inconsistent denominators;
- stale standards/budgets/forecasts;
- unexplained residual hidden in “other”;
- analytics that do not reconcile to the P&L/GL movement;
- management forecast presented as fact;
- an accounting adjustment mislabelled as an economic driver;
- genuine economic deterioration mislabelled as an accounting error;
- accounting conclusions made directly by analytics instead of the governed owner.

### 2. Semantic Planner + Document/Data Intake — COMPLETE
Status: **complete** within the bounded foundation. Structured semantic proposals, deterministic validation, inert source adapters, provenance/transformations, fact/conflict/context resolution, owner-input candidates and integration with the existing runtime passed authored and independent adversarial QA plus full repository regression. See `orchestration/INTAKE-INTEGRATION-HANDOFF.md`; final publication requires exact-head GitHub Actions before PR readiness. Native binary extraction, live model inference, authenticated approvals and persistence remain outside scope. The three additional end-to-end flagships are now complete within their documented bounds; multi-entity and multi-period orchestration is next.

After the analytical-intent foundation is stable, allow the CAO to interpret genuinely free-form objectives and supplied company materials into governed facts, issues and workplan proposals.

Target inputs include trial balances, monthly P&Ls, ERP/subledger exports, inventory reports, payroll data, contracts, policies, reconciliations, management commentary and other company documents.

Model reasoning may propose facts/issues/workplans, but production status, owner boundaries, dependency controls, exact-once lineage, accounting authority and challenge gates remain governed by the deterministic runtime and production skill contracts.

### 3. Additional end-to-end flagship scenarios — COMPLETE
Build broader orchestration coverage after semantic/data intake:
1. **SaaS / month-end close — COMPLETE** — Revenue + AR + ECL + FX + Reconciliations + Close + Reporting + Disclosure + analytics.
2. **Treasury / financing — COMPLETE** — Debt + FX + Derivatives/Hedge + Financial Instruments + Cash Flow + Reporting + analytics.
3. **Group accounting — COMPLETE** — Business Combinations + Consolidation + NCI + FX + Impairment + Tax + Reporting.

SaaS uses the governed semantic/intake foundation, controlled sources, nine production owners, exact-once journal ownership, source conflicts, diagnostics and independent acceptance QA. See `orchestration/SAAS-INTEGRATION-HANDOFF.md`. Treasury now also proves governed Debt/FX/Hedge/Cash/reporting integration, raw-source qualification, exact-once ownership and independent adversarial acceptance. See `orchestration/TREASURY-INTEGRATION-HANDOFF.md`. Group now proves acquisition/Tax/FX/Intercompany/Impairment/Consolidation/NCI/reporting integration from company-shaped sources, with explicit entity/period dimensions, exact-once economics, a partial conflict Case and complete clean control. Authored and independent adversarial QA, deterministic artifacts and full regression passed. See `orchestration/GROUP-INTEGRATION-HANDOFF.md`. All three additional flagships are complete within their documented bounds; exact-head Actions remain the final publication gate.

Each flagship must test issue discovery, positive/negative skill selection, owner handoffs, exact-once economics, challenge/rework, analytics where appropriate and one coherent CAO result.

### 4. Multi-entity and multi-period orchestration — COMPLETE
Status: **COMPLETE and integrated on live main** through merged PR37.

The four stages below established the existing governed multi-entity and multi-period architecture. The original Group-to-multi-entity handoff remains historical; the current compatibility baseline is `orchestration/STAGE4-INTEGRATION-HANDOFF.md`.

This roadmap item is intentionally split into four sequential PRs. Each stage starts from the newly merged `main` produced by the previous stage. Do not run the four stages in parallel and do not mark the overall workstream COMPLETE until Stage 4 passes its final integration gates.

#### Stage 1 — Scope + Repeated-Owner Execution Foundation — COMPLETE
Stage 1 delivers the stable dimensional execution substrate. Integration publication remains gated by exact-head CI and owner review; Stage 2 cannot begin before merge. See `orchestration/STAGE1-TO-STAGE2-HANDOFF.md` and `orchestration/STAGE1-INTEGRATION-HANDOFF.md`.

Implemented:
- arbitrary LEGAL_ENTITY / GROUP / SUBGROUP scope registry without a hard three-scope cap;
- stable deterministic scope and multidimensional execution-node identity;
- repeated execution of the same production owner across different scopes without package-key collision;
- scope-aware facts, source lineage, owner inputs/results and semantic receipts;
- explicit functional/presentation currency, framework and jurisdiction dimensions;
- legal-entity versus subgroup/group journal/event scope;
- scoped exact-once economics;
- migration of the bounded Group flagship to the generic scope primitives;
- complete backwards compatibility with Manufacturing, Diagnostic, Intake, SaaS, Treasury and Group flagships.

Stage 1 success requires executable proof that one production owner can run independently for at least three legal-entity scopes with separate fingerprints, evidence, results, journals and consumers; wrong-scope/currency/framework substitution fails closed; and existing Group/single-entity execution remains green. Produce a committed Stage-2 handoff. Do not build general Case hierarchy lifecycle, multi-period invalidation, or the full intercompany network in Stage 1.

#### Stage 2 — Case Hierarchy + Multi-Period + Dependency Invalidation/Rework — COMPLETE
Stage 2 substantive implementation, final independent QA/remediation, deterministic artifacts and full local release regression are complete. See `orchestration/STAGE2-INTEGRATION-HANDOFF.md`, `orchestration/STAGE2-FINAL-INDEPENDENT-QA.md` and `orchestration/STAGE2-RELEASE-REGRESSION.json`. Immutable-head required Actions and PR readiness are recorded in PR #35; Stage 3 starts only after owner integration.

The delivered architecture adds hierarchical Entity/Subgroup/Group Case governance, deterministic calendar-qualified Period identity, opening/prior/comparative/partial-period relationships, effective intervals, exact-version dependency contracts, CURRENT/STALE/SUPERSEDED result lineage, dependency-driven invalidation, selective topological re-execution and governed reopening without rewriting history.

The controlled proof corrects a qualified US September Revenue result and invalidates only its actual downstream US/Group/next-period consumers while unrelated UK and independent controls remain current. Ordinary runtime repeated-owner selection is Scope + governed Period aware; stale/superseded/wrong-Period receipts fail closed. See `orchestration/MULTI-ENTITY-STAGE2-TO-STAGE3-HANDOFF.md` and the Stage 2 integration handoff.

Stage 2 does not implement generalized intercompany networks, framework conversion, generalized currency-translation chains, durable persistence or authenticated governance.

#### Stage 3 — Intercompany Network + Framework/Currency Conversion — COMPLETE
Stage 3 delivers the bounded intercompany network and governed cross-layer execution described in `orchestration/STAGE3-INTEGRATION-HANDOFF.md`, `orchestration/STAGE3-INDEPENDENT-QA.md` and `orchestration/STAGE3-RELEASE-REGRESSION.json`. Exact-head Actions and readiness are recorded in PR #36. Implemented cross-scope interaction:
- multi-counterparty intercompany graph and transaction-level matching;
- business-relationship cycles without orchestration-DAG cycles;
- cross-period and multi-currency intercompany relationships;
- explicit residual classification and elimination dependencies;
- local-framework → group-framework conversion receipts;
- multiple functional currencies and group presentation currency;
- governed translation chains and exact-once economics across legal-book/counterparty/group layers.

Critical proof: a multi-entity intercompany network reconciles across periods/currencies, local-framework results cannot masquerade as group-framework results, and group eliminations remain distinct from legal-book entries. Produce a committed Stage-4 handoff.

#### Stage 4 — Full Multi-Entity / Multi-Period Integration Flagship — COMPLETE
After Stages 1–3 are merged, prove the architecture end-to-end with a controlled multi-entity Group objective using at least three legal entities plus Group scope, repeated owners, multiple periods, multiple functional currencies, local/group framework differences, multiple intercompany edges, group reporting and analytics.

The flagship must deliberately change one qualified upstream entity/period result and prove dependency-driven invalidation, selective rework and an updated Group result without rerunning unrelated work. It must include a material-conflict Case that fails safely and a corrected clean control that reaches COMPLETE/CLOSED.

Stage4 substantive architecture, controlled flagship, independent QA/remediation/rerun, prior migration, deterministic artifact and local release gates pass. The workstream is COMPLETE subject to owner integration. See `orchestration/STAGE4-INTEGRATION-HANDOFF.md`, `orchestration/STAGE4-FINAL-INDEPENDENT-QA.md` and `orchestration/STAGE4-RELEASE-REGRESSION.json`. Immutable-head required Actions and unchanged-head readiness are recorded on existing PR37 before owner review. Durable Case + Company Accounting Memory is NEXT; its handoff is documentation only, with no persistence implementation in Stage4.

### 5. Durable Case and Company Accounting Memory persistence — IN PROGRESS
This new workstream follows the merged four-stage multi-entity architecture. Its sequential four-stage plan is the current implementation assignment, not a retroactive historical specification. Accounting owners and native governance remain authoritative. See `orchestration/DURABLE-CASE-COMPANY-ACCOUNTING-MEMORY-HANDOFF.md`.

#### Stage 1 — Durable Case State & Persistence Foundation — COMPLETE (MERGED)
Implemented and independently validated in PR #38; final immutable head `b90bf8269a9f96b9f0b572256b52774fba7055f8` was merged into `main` as `2f79018b7f9a0a8ff39fb7ebfebf9dfdbafaafd3` on 2026-10-08. All required exact-head GitHub Actions passed, including readiness-triggered CAO integration; 2,772 distinct repository tests passed, six substantive independent QA findings were reproduced and generically remediated, and zero substantive findings remain open. The versioned SQLite adapter provides atomic immutable checkpoints, optimistic revision concurrency, exact native restoration, sealed evidence/history validation, schema compatibility and bounded recovery. See `orchestration/PERSISTENCE-STAGE1-INTEGRATION-HANDOFF.md`, `orchestration/PERSISTENCE-STAGE1-INDEPENDENT-QA.md`, `orchestration/PERSISTENCE-STAGE1-RELEASE-REGRESSION.json` and `orchestration/PERSISTENCE-STAGE1-TO-STAGE2-HANDOFF.md`. Restoration runs no accounting owner or journal release. Company memory approval/reuse is not delivered.

#### Stage 2 — Durable Dependency, Rework & Recovery Lifecycle — IN PROGRESS
Active on `persistence/durable-rework-recovery`, draft PR #39, from live main `d202e910e17de559d908df478939ce10042e41db`. Native correction/rework recovery, atomic operation outcomes, retained exact dependencies, closed-period governance and internal journal-selection idempotency are implemented. Independent QA accepts the remediated production tree with 21 permanent methods and zero unresolved substantive findings; final artifact publication, two-seed comparison and release regression remain pending. See `orchestration/PERSISTENCE-STAGE2-ARCHITECTURE-RECONSTRUCTION.md`, `orchestration/PERSISTENCE-STAGE2-INDEPENDENT-QA.md` and `orchestration/persistence/CONTRACT.md`. Stage 3 has not started; no approved company-memory reuse or external posting guarantee is delivered.

#### Stage 3 — Company Accounting Memory & Controlled Promotion — FUTURE
Evidence-backed company-specific candidates, proposal/approval/supersession, provenance, qualified retrieval and safe reuse. Persistence must never promote candidates into approved company truth.

#### Stage 4 — Full Durable CAO Integration Flagship — FUTURE
Prove the complete durable lifecycle and controlled company-memory promotion/reuse against the existing multi-entity/multi-period flagship, including restart, recovery, selective rework, preserved conflicts and independent release acceptance. Stages2–4 are not implemented in Stage1.

### 6. Authenticated governance and approvals
Add real user identity, roles, preparer/reviewer separation, approval events and audit trail. Synthetic reviewer identities/fingerprints remain regression evidence only.

### 7. Product/API/UI layer
Expose the governed CAO runtime through an application experience for conversational objectives, document/data intake, material questions, Case/workplan review, artifacts, judgments and approvals. Every user-visible route must continue to pass through the public-output boundary.

### Parallel residual accounting backlog
When capacity permits, independently complete:
1. #34 Government Grants & Assistance;
2. #35 Borrowing Costs;
3. #37 Investment Property.

These should use the same standalone knowledge-extension / independent-QA / promotion pattern used by the completed specialists. They are parallel backlog items rather than blockers for the CAO intelligence/runtime sequence.

## Phase 2E — approval audit
Complete: 157/157 individually processed and approved; no remaining canonical accounting blockers. See `knowledge/phase-2e/reviews/`. Per-claim source assurance remains separate. No Master Build Map found.

Runtime public-output integration and verification are now implemented in the CAO orchestration foundation. Future application adapters must continue to enforce the same public boundary. Exact-commit GitHub Actions remain the integration standard.
