# Stage 1 live architecture reconstruction

Baseline live main: `e0735d5a45971c9dac0334f68cacbcad42685035`, verified by fresh public clone and connected GitHub repository/branch reads. Group merge `94664b574e17df40d754126ed15abd556a07b1d6` is an ancestor. All six prior integrations and four-stage roadmap exist.

The authoritative inputs are build-roadmap.md, GROUP-TO-MULTI-ENTITY-HANDOFF.md and GROUP-INTEGRATION-HANDOFF.md. Treasury, SaaS, Intake, Diagnostic and Manufacturing handoffs describe the migration regressions. architecture/ retains the CAO → orchestration → domains → production-owner model, Case challenge/close gates, separate memory promotion, and artifact provenance. No new accounting authority is needed.

## Current execution substrate

`planning.py` provides Issue, Node and Graph, validates a dependency DAG and handles bounded challenge/rework. `runtime.py` builds a Case, merges governed context without promoting proposals, resolves owners from `registry.py`, checks dimensions, invokes `production.assess_case`, validates current results, challenges, synthesizes and publishes through `interfaces/public_output.py`. Native exact-case certification belongs to production owners, not intake/runtime.

`scopes.py` currently accepts at most three entity/group contexts and one common framework. `runtime.py` keys workpapers and bridge discovery by package; repeated owners collide. Node IDs currently originate in planner issue IDs. `result_bindings.py` contains typed actual-result semantic contracts for the Group handoffs. `journal_scopes.py` validates the Consolidation source assembly against independently reviewed source populations and native journals. `_qualified_journals` is the gross-line exact-once event allocator: every implication must be assigned exactly once; aliases cannot create fresh lines. These accounting gates must survive migration.

Intake source adapters are inert bounded CSV/TSV/JSON/normalized document/workbook extractors. Source IDs and byte/extraction fingerprints, cell/block locations, dimensions and transformation records survive. `ProposalValidator` validates untrusted semantic proposals; `Intake.prepare` resolves facts/conflicts and creates input candidates. `ReviewedInputPack` independently supplies fact, complete keyed population, whole-document and single-capture text bindings. `Intake.execute` checks the sealed proposal and qualified bindings before invoking the same CAO runtime. Existing source populations and native certificates must never be synthesized by runtime.

## Stage 1 design

One immutable governed Scope registry accepts legal entities, subgroups and groups; explicit registered IDs are stable natural keys. Compatibility inputs (single entity and existing execution_scopes) normalize immediately into the same registry without a cap or scenario switch. Structural hierarchy is metadata, not accounting control or a dependency. Missing/duplicate/cyclic/illegal relationships fail closed.

Every execution gets a deterministic key from owner, Scope, framework, jurisdiction, functional/presentation currency and bounded start/end dates. Package/issue aliases may resolve only when unique, preserving ordinary callers while forbidding repeated-owner ambiguity. Workpapers/results are node-addressed; native results retain their existing contract, with a separate dimensional execution envelope. Explicit typed receipts bind exact source/target nodes and Scopes. No numeric equality authorizes conversion or cross-Scope consumption.

Stage 1 adds scoped accounting-layer identity to the inherited event allocator and migrates Group to those generic primitives. The controlled proof independently certifies Revenue in NL/US/UK and uses an orchestration-only Group observation consumer. Incompatible frameworks/currencies remain visible unresolved conversion boundaries; no consolidated IFRS/EUR total is generated. Hierarchical Cases, general periods/invalidation, intercompany networks, conversion and persistence remain future work.

## Validation and delivery

Authored adversarial tests, a fresh independent reviewer, remediation/rerun, deterministic generators, all prior flagships and both repository workflows are required. Durable milestone pushes precede long QA/regression. Government Grants PR #27, Borrowing Costs and Investment Property are excluded. Stage 1 remains incomplete until exact-head CI and readiness gates pass.
