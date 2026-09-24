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

### Domain 13 — in progress
- TOPIC-13-001 Business Combination Accounting / PPA Coordination — REVIEWED / production-candidate. Current IFRS/FASB/FRC/AASB source routing checked 24 September 2026; 10 scenario tests PASS.
- Key gates: business-v-asset, accounting acquirer/date, framework/effective period, identifiable-net-assets completeness, specialist valuation challenge, PPA-to-reporting reconciliation and measurement-period ownership.
- Current-source findings: IASB's business-combination disclosure/goodwill project remains under redeliberation and is not effective IFRS; FASB ASU 2025-03 requires an effective-date gate for specified VIE accounting-acquirer analysis; FRS 102 Section 19 remains materially different from current IFRS 3; AASB 3 requires explicit subsequent/uncompiled-amendment routing for periods beginning on/after 1 July 2026.

### Source guardrails
Public FASB materials still do not expose all current Codification paragraph bodies; affected US GAAP records remain PARTIAL at paragraph-level authority rather than receiving unsupported APPROVED status. Rights/licensing guardrails remain in force.

### Progress
Cumulative canonical post-Leases Phase 2D topics worked through: **103 / 156**. Remaining: **53**. No fully blocked topics. Thirteen regression reviews completed.

Repository duplicate/retry folders remain a non-blocking hygiene item; canonical Phase 2B IDs and `knowledge/phase-2d-progress.md` are authoritative.

Next: TOPIC-13-002 acquisition-date accounting / contingent consideration, then continue Domain 13 and run regression after 5–10 canonical Domain 13 topics.

## Phase 3 — Production skills
Build skills systematically across all 17 domains after knowledge population is sufficiently mature.