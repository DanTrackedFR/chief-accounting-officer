# Build Roadmap

## Phase 1 — Operating system
Status: **complete**.

## Phase 2A — Knowledge infrastructure
Status: **complete**. Active frameworks: IFRS, US GAAP, UK GAAP and AASB. NZ IFRS deferred.

## Phase 2B — Topic universe
Status: **complete**. 157 top-level topics; 347/347 primary capability coverage.

## Phase 2C — Leases vertical slice
Status: **complete as architecture checkpoint**. Framework routing, effective-period routing, source mapping, differences, calculations, CAO logic, practice/control/audit/systems, artifacts and 11 scenario tests demonstrated.

## Phase 2D — Full knowledge population
Status: **IN PROGRESS**.

Build topic-by-topic across the remaining universe. Full factory means PRINCIPLES/STANDARDS/PRACTICE as applicable; authoritative sources for standards claims; differences; CAO execution logic; calculations/examples where relevant; documentation; controls/audit/disclosures/systems; capability integration; tests; QA; commit and tracking. Operational topics must not manufacture framework records.

### Batch 001 — Close core — 22 September 2026
REVIEWED: TOPIC-02-001 through TOPIC-02-005. Regression PASS.

### Batch 002 — Close & GL completion — 22 September 2026
REVIEWED: TOPIC-02-006 through TOPIC-02-010. Domain 02 fully worked through. Regression PASS.

### Batch 003 — Revenue start + reporting dependency — 22 September 2026
REVIEWED / production-candidate: TOPIC-03-001 through TOPIC-03-003 and TOPIC-08-005 Going Concern / Subsequent Events.

Non-blocking source limitation: public FASB materials confirm relevant architecture but do not expose all current Codification paragraph bodies required for APPROVED paragraph-level status. The limitation is recorded and work continues.

### Batch 004 — Revenue continuation — 22 September 2026
REVIEWED / production-candidate: TOPIC-03-004 through TOPIC-03-008. TOPIC-03-008 preserves material IFRS 9/AASB 9, ASC 326 and FRS 102 Section 11 impairment divergence.

### Batch 005 — Revenue & receivables completion — 22 September 2026
REVIEWED: TOPIC-03-009 through TOPIC-03-012. Regression PASS. Domain 03 fully worked through.

### Batch 006 — PPE recognition/capitalization + reporting depth — 22 September 2026
REVIEWED / production-candidate:
- TOPIC-04-001 Fixed Asset Recognition / Capitalization / Additions.
- TOPIC-08-005 Subsequent Events deepened with structured event-log method and authoritative framework map.

### Batch 007 — Depreciation / useful lives / disposals — 22 September 2026
REVIEWED / production-candidate:
- TOPIC-04-002 Depreciation / Useful Life & Residual Value / Asset Transfer, Disposal & Retirement — 15c6a77e.
- Official IAS 16, AASB 116 and FRS 102 Section 17 architecture checked. Component depreciation, available-for-use start, estimate-change routing, disposal logic, controls/data/artifacts and five scenarios built.
- Material US difference retained: component depreciation is not generally mandatory under US GAAP; full current ASC 360 paragraph-body depth remains PARTIAL under the existing non-blocking public-source limitation.

Cumulative canonical Phase 2D topics worked through: **24**. No fully blocked topics. Remaining: **132**.

Repository hygiene remains an open non-blocking action: duplicate/retry folders exist for some earlier topic IDs. Canonical Phase 2B topic IDs, not raw folder counts, control progress.

Next: TOPIC-04-003 Construction in Progress / FA reconciliation / Capitalized Software, then remaining Assets & Capitalization family. Regression after the next 4–6 canonical topics.

## Phase 3 — Production skills
Build skills systematically across all 17 domains after knowledge population is sufficiently mature.