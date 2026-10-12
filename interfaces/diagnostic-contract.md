# Structured intent and diagnostic adapter contract

This extends the existing Planner, Case and public boundary. It is not a second
orchestrator, replacement skill taxonomy, intake parser or persistence service.

`Planner.interpret(objective, facts, context, registry) -> Intent` proposes one
primary governed work mode, unique secondary modes and unique supporting
modes/reasons. The runtime validates the proposal. `Planner.identify` still returns
existing governed `Issue` objects and their actual owner dependencies. A future
semantic planner may implement this interface; CI uses deterministic structured
fixtures and no model/network inference.

Work modes: DIAGNOSTIC_ANALYTICS, ACCOUNTING_DETERMINATION, CLOSE_REVIEW,
RECONCILIATION_INVESTIGATION, REPORTING, PROCESS_CONTROL_REVIEW, AUDIT_SUPPORT,
DOCUMENTATION, TRANSACTION_ACCOUNTING. Modes and skills have a many-to-many
relationship; mode assignment never authorizes an owner or bypasses availability.

The Case adds `work_modes`, `diagnostics` and `accounting_questions`. A diagnostic
contains a `bridge`, `methods`, `hypotheses`, `observations`, `accounting_questions`,
`attribution_ledger` and `open_items`. Bridge output includes metric/unit,
starting/ending/change, signed driver contributions, explained amount/percentage,
explicit residual/tolerance/materiality/status, presentation basis and comparator
kind/version. Gross-profit bridges additionally retain a percentage-point bridge
with a separately identified denominator effect.

Each driver has ID/label/contribution/category/confidence/status/evidence class and
lineage: source owner/metric/document/period/entity/currency/unit/comparator/method,
disjoint original economic components and native component-allocation references
where a metric is partitioned. Those internal references support later governed
charting; the existing public boundary exposes a curated explanation, amounts and
limitations, never raw lineage/reviewer/hash/owner-routing data.

Each hypothesis retains observation, proposed explanation, actual test evidence,
evidence class, calculated disposition and confidence. Statistical association,
management explanation and model hypotheses cannot establish quantitative causal
drivers. An unusual journal or trend signal is an observation requiring evidence,
not a journal correction or accounting error conclusion.

An accounting question has target owner, issue, reason, amount, result path,
source evidence, supplied materiality and status. Follow-up execution resolves the
actual production owner, verifies the current result and preserves authority in
that owner. Only the existing reviewed owner workpaper is executable: questions
outside native supported scope remain unresolved pending revised workpapers.
The current follow-up path reuses/rechecks existing production owners; it does not
invent a missing new accounting method or source case.

Input adapters must feed native owner workpapers plus independently controlled
Analytics source documents, comparator edition/freeze information and diagnostic
methods. Native source/release/case certification remains mandatory. Matching
entity/framework/jurisdiction/period/currency is enforced; current execution stays
one scoped native period per Case, with supplied comparative analytical sources.
