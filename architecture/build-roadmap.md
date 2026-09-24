# Build Roadmap

## Phase 1 — Operating system
Status: **complete**.

## Phase 2A — Knowledge infrastructure
Status: **complete**. Active frameworks: IFRS, US GAAP, UK GAAP and AASB. NZ IFRS deferred.

## Phase 2B — Topic universe
Status: **complete**. 157 top-level topics; 347/347 primary capability coverage.

## Phase 2C — Leases vertical slice
Status: **complete as architecture checkpoint**. Full factory proven end-to-end.

## Phase 2D — Full knowledge population
Status: **IN PROGRESS**.

Build topic-by-topic across the remaining universe. Full factory means PRINCIPLES/STANDARDS/PRACTICE as applicable; authoritative sources for standards claims; differences; CAO execution logic; calculations/examples where relevant; documentation; controls/audit/disclosures/systems; capability integration; tests; QA; commit and tracking. Operational topics must not manufacture framework records.

### Completed domain families
- Domain 02 Close & General Ledger — TOPIC-02-001–010 — REVIEWED.
- Domain 03 Revenue & Receivables — TOPIC-03-001–012 — REVIEWED / production-candidate.
- Domain 04 Assets & Capitalization — TOPIC-04-001–006 worked through plus proven Leases vertical slice; remaining canonical Domain 04 denominator handled according to lease mapping/hygiene rules.
- Domain 05 Liabilities, Expenses & Compensation — TOPIC-05-001–010 — REVIEWED / production-candidate.
- Domain 06 Cash, FX & Financial Instruments — TOPIC-06-001–010 — REVIEWED / production-candidate.
- Domain 07 Group Accounting & Consolidation — TOPIC-07-001–009 — REVIEWED / production-candidate.
- Domain 08 Financial Reporting — TOPIC-08-001–010 — REVIEWED / production-candidate.
- Domain 09 Controls & Governance — TOPIC-09-001–009 — REVIEWED / production-candidate.
- Domain 10 Audit & Assurance Readiness — TOPIC-10-001–007 — REVIEWED / production-candidate.
- Domain 11 Accounting Systems & Data — TOPIC-11-001–010 — REVIEWED / production-candidate.
- Domain 12 Accounting Operations — TOPIC-12-001–009 — REVIEWED / production-candidate. Regression 013 PASS.

### Domain 12 architecture findings
Accounting operations consume technical conclusions rather than duplicating them. Population completeness precedes matching/accuracy metrics. Operational automation retains source/run/configuration identity, exception populations and overrides. Queue history can be accounting evidence where it affects close completeness. Service-level management pairs timeliness with quality. TrackedFR is assessed only for recurring, multi-system, data-intensive reconciliation/manipulation workflows.

### Source guardrails
Public FASB materials still do not expose all current Codification paragraph bodies; affected US GAAP records remain PARTIAL at paragraph-level authority rather than receiving unsupported APPROVED status. Rights/licensing guardrails remain in force. Operational topics are PRINCIPLES/PRACTICE-led unless the underlying accounting conclusion invokes a standards-sensitive topic.

### Progress
Cumulative canonical post-Leases Phase 2D topics worked through: **102 / 156**. Remaining: **54**. No fully blocked topics. Thirteen regression reviews completed.

Repository duplicate/retry folders remain a non-blocking hygiene item; canonical Phase 2B IDs and `knowledge/phase-2d-progress.md` are authoritative.

Next: Domain 13 Complex Transactions & Special Situations (TOPIC-13-001–012), with authoritative framework verification and regression after 5–10 topics.

## Phase 3 — Production skills
Build skills systematically across all 17 domains after knowledge population is sufficiently mature.