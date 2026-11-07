# Operational readiness — assessment only

Reviewed against accepted main `97d0621331c6ad2a66b12ed09c0ec40c05c626b9` on 7 November 2026. No operational-limit implementation is included. These are separate from the six Phase A corrections. Scope estimates below are engineering estimates, not commitments.

## A. Company provisioning requires service restart

`hosted_cao/__main__.py:main` reads `CAO_SERVICE_CONFIG` once and passes configuration to `Service`. `hosted_cao/service.py:Service.__init__` copies and validates company roots, builds a fixed credential list and creates one company lock per company. There is no provisioning or reload operation in `OPERATIONS`, no configuration watcher and no administrative HTTP route. `authenticate` checks both the credential allowlist and company registry. Adding a directory or editing the JSON configuration while the process runs does not provision it into the live service.

Integration impact: TrackedFR cannot safely self-provision a new customer through the accounting API. A controlled restart with validated configuration is the current supported operational route. Existing workers and jobs must be drained or safely recovered; process shutdown is not a substitute for deleting or migrating durable workspaces.

Minimum safe correction: introduce an authenticated administrative provisioning boundary, validate a unique company identity and canonical private workspace root, initialize a complete context, then atomically publish its registry, credential scope and lock. Keep this authority separate from ordinary accounting-client credentials. Concurrent requests must see either the old or complete new configuration; updating the dictionaries manually is unsafe. Revoke/reload behavior, audit history, persistence of provisioning state and crash recovery need explicit decisions. An alternative first step is controlled immutable snapshot reload with atomic swaps and active-job compatibility checks.

Dependencies: deployment secrets/credential management, workspace ownership model, authorization model for the administrative actor, lifecycle/audit persistence, worker concurrency and operational runbook. Estimated scope: medium (roughly 3–5 engineering days plus independent security/isolation/concurrency QA once the model is agreed). Recommended priority: high before multitenant pilot onboarding; current restart procedure remains viable for a small controlled pilot. Follow-up issue should be separate from Issue #50.

## B. The 2026 restriction is a governed support boundary

Two independent Profile 1.2 paths enforce it: `skills/source_execution.py:requirements` reports unsupported scope for either reporting date outside 2026; `skills/prepared_execution.py:qualify` requires `2026-01-01 <= period_start <= reporting_period <= 2026-12-31`. The latter also governs Profile 1.1. `architecture/PRESUMED-SOURCES-DESIGN.md` and `architecture/PREPARED-EXECUTION-COMPLETION-REPORT.md` explicitly describe commercial for-profit 2026-only support. FRS 102 and AASB selectors are edition/compilation selectors, not simply reporting-year labels. `orchestration/periods.py` itself supports governed ISO reporting periods beyond 2026; this is not a generic date parser defect.

January 2027 impact: supported Profile 1.2 fixed-asset/AP execution will remain unresolved for a 2027 close even if request/company scope is valid. TrackedFR must not relabel 2027 activity as 2026 or fabricate a prior reporting date to bypass the boundary.

Minimum safe correction: create an explicit period/framework support matrix for the relevant fixed-assets and AP methods, assess 2027 effective-date and transition differences and the continued applicability of governed claims, then update bounded qualification, validation, schema/guidance and tests consistently. Preserve distinct reporting dates and standards edition selectors. Verify opening/closing continuity across December–January and do not reopen or rewrite historical accepted results. Preserve the current restrictions for unsupported entity types, regulatory overlays and methods.

Standards/evidence implications: applicable 2027 requirements and effective-date transitions must be reviewed for IFRS, private US GAAP, FRS 102 and AASB within the selected scope. Current receipt and source SHA do not evidence that assessment. Fresh source-bound regression and separate release/governance acceptance are required; original-upload retesting remains separately owned.

Recommended timeline: authorize investigation in November 2026, complete scoped implementation and independent accounting/engineering review during December, and accept/deploy through a separate release assignment before the first January 2027-close rehearsal. Priority: high, time-bound. Estimated scope: medium and evidence-dependent (approximately 3–7 engineering/review days after the standards applicability review; more if transitions affect methods). A separate follow-up issue should own this boundary.

## C. 200 rows is an aggregate per source Case cap

`skills/source_execution.py:requirements` sums list lengths across `assets`, `costs`, `cip`, `invoices`, `accruals`, `payments`, and `supplier_balances`; the combined maximum is 200. `interfaces/source-case.schema.json` also has per-array `maxItems: 200` and explicitly documents the stricter aggregate runtime rule. It is not 200 assets plus 200 costs. General inert intake limits (`orchestration/intake/sources.py`) independently bound payload bytes, nesting and array size; they do not enlarge the Profile 1.2 supported accounting population.

Observed authenticated HTTP experiment: 200 valid machinery asset rows plus one valid training-cost row were submitted and an execution job completed operationally, but the governed result was blocked, returned `bounds.population` at `source`, no calculated financial amounts and no journal workpaper. Explanation: “This profile supports at most 200 supplied rows per Case; partition the population and reconcile the partitions.” Operational job success means the task ran, not supported accounting acceptance. No truncation was observed. HTTP body limits can independently reject an oversized request earlier.

Why it exists: the published Profile 1.2 design deliberately bounds supplied-file execution. The code does not prove an exact performance-derived 200-row threshold; do not describe 200 as a measured system capacity. It limits runtime, screening and durable result populations. Existing matching/cost dependency scans include repeated row scans, and every result persists source facts, lineage, anomaly findings, workpapers and public output. Raising the cap increases CPU, SQLite/checkpoint bytes and response size; jobs are single-host and must retain timeout/crash/idempotency behavior.

Customer impact: a modest real-world register may exceed 200 rows, particularly when cost/CIP movements consume the same allowance. Current partition guidance must preserve complete-population reconciliation and asset/cost dependencies; arbitrary splitting can orphan additions, duplicate assets or omit supplier reconciliation. TrackedFR should preflight aggregate counts and explain unsupported capacity before accepting an upload as complete.

Safe options: (1) retain 200 and add an explicit adapter partition-and-reconcile contract with stable row identities and dependent rows kept together; (2) raise a bounded tested cap after load/durability tests, schema/runtime alignment, response-size checks and independent accounting completeness review; (3) introduce durable batch execution with explicit population controls and cross-partition reconciliation, a larger redesign. Never silently truncate or remove bounds. Recommended priority: high if the original pilot register exceeds capacity; otherwise medium before larger customers. Estimated scope: 2–4 days for a measured bounded-cap increase plus independent QA; 1–2 weeks or more for robust governed batch orchestration. Separate follow-up issue required; no capacity change in this PR.

## Separate follow-up tracking

- A — [Company provisioning without restart, Issue51](https://github.com/DanTrackedFR/chief-accounting-officer/issues/51).
- B — [Governed2027 support, Issue52](https://github.com/DanTrackedFR/chief-accounting-officer/issues/52).
- C — [Capacity beyond aggregate200 rows, Issue53](https://github.com/DanTrackedFR/chief-accounting-officer/issues/53).

These are assessment-only follow-ups; no provisioning, reporting-year or capacity change is implemented here.
