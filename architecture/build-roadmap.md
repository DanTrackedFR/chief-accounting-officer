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

### Batches 001–002 — Close & GL — 22 September 2026
REVIEWED: TOPIC-02-001 through TOPIC-02-010. Domain 02 complete. Regression PASS.

### Batches 003–005 — Revenue & receivables — 22 September 2026
REVIEWED / production-candidate: TOPIC-03-001 through TOPIC-03-012 plus TOPIC-08-005 Going Concern/Subsequent Events dependency. Domain 03 complete. Regression PASS. ECL preserves IFRS 9/AASB 9, ASC 326 and FRS 102 divergence.

### Batches 006–010 — Assets & capitalization — 22–23 September 2026
REVIEWED / production-candidate: TOPIC-04-001 through TOPIC-04-006 plus the previously proven lease vertical slice mapped across canonical lease capabilities. PPE, depreciation/disposals, CIP/FA reconciliation, capitalized software/R&D/cloud implementation, intangibles/amortization and impairment/goodwill worked through.

### Batches 011–014 — Liabilities, expenses & compensation — 23 September 2026
REVIEWED / production-candidate: TOPIC-05-001 through TOPIC-05-010. Domain 05 complete. AP, expense cut-off/accruals, provisions, onerous contracts, payroll/benefits, bonuses/commissions, SBC/mixed awards, termination/leave and compensation reconciliations built. Regression 003 and 004 PASS.

### Batches 015–016 — Cash, FX & debt start — 23 September 2026
REVIEWED / production-candidate: TOPIC-06-001 through TOPIC-06-006. Bank/cash, foreign-currency transactions, remeasurement/translation, functional currency, debt/issuance costs, modifications/extinguishments and covenants built. Regression 005 PASS.

Current-source gates include IAS/AASB 21 Lack of Exchangeability effective 1 January 2025, IFRS/AASB hyperinflationary-presentation amendments effective 1 January 2027, UK FRS 102 Periodic Review effective-period routing, IFRS 9 2026 classification/measurement amendments, and explicit separation of active IASB/FASB projects from current GAAP.

Non-blocking source limitation: public FASB materials do not always expose complete current Codification paragraph bodies required for APPROVED paragraph-level status. Affected US records remain PARTIAL at paragraph level; work continues.

Cumulative canonical post-Leases Phase 2D topics worked through: **45 / 156**. Remaining: **111**. No fully blocked topics. Five regression reviews completed.

Repository hygiene remains non-blocking: duplicate/retry folders exist for some stable topic IDs. Canonical Phase 2B IDs and `knowledge/phase-2d-progress.md` remain authoritative until normalization.

Next: TOPIC-06-007 through TOPIC-06-010 financial instruments, then Domain 07 Group Accounting & Consolidation.

## Phase 3 — Production skills
Build skills systematically across all 17 domains after knowledge population is sufficiently mature.