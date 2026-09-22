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
Worked through to REVIEWED / production-candidate:
- TOPIC-03-001 Revenue Contract Accounting Assessment / Performance Obligation Identification.
- TOPIC-03-002 Variable Consideration / Transaction Price Allocation — 2974a279.
- TOPIC-03-003 Revenue Recognition Timing / Contract Modifications — 1a3d2932.
- TOPIC-08-005 Going Concern / Subsequent Events.

Non-blocking source limitation: public FASB materials confirm Topic 606 / ASC 205-40 / ASC 855 architecture but do not expose all current Codification paragraph bodies required for APPROVED paragraph-level status. The limitation is recorded and work continues.

### Batch 004 — Revenue continuation — 22 September 2026
Worked through to REVIEWED / production-candidate:
- TOPIC-03-004 Principal-versus-Agent / Contract Asset & Liability Accounting — 310e8e1d.
- TOPIC-03-005 Deferred / Unbilled Revenue — 76dcec2d.
- TOPIC-03-006 Contract Costs / Sales Commissions & Billing Completeness — 3073dd17.
- TOPIC-03-007 Credit Notes, Refunds, Rebates & Accounts Receivable Accounting — 860aaf6c.
- TOPIC-03-008 AR Aging / Expected Credit Loss / Doubtful Debt Allowance — 37bd85d5.

TOPIC-03-008 records a material framework divergence: IFRS 9/AASB 9 lifetime-ECL mechanics for qualifying trade receivables; ASC 326 CECL under US GAAP; FRS 102 Section 11 objective-evidence/incurred-loss model. The factory explicitly prevents reusing an IFRS provision matrix as UK GAAP by default.

Cumulative Phase 2D topics worked through: **19**. No fully blocked topics. US source-depth remains PARTIAL where full current Codification paragraph bodies are unavailable through the public source path; this is not programme-blocking and no paragraph-level APPROVED claim is made.

### Regression / hygiene finding
Regression file 3f0cc5ba records repository-hygiene issues: Phase 2C lease folder naming spans canonical TOPIC-04-007 through 04-010 rather than matching the Phase 2B denominator one-to-one; build retries created duplicate TOPIC-02-001 folders. Canonical-universe counts, not raw folder counts, remain authoritative until normalization.

Next: TOPIC-03-009 onward. Run revenue-family regression after another 1–4 topics.

## Phase 3 — Production skills
Build skills systematically across all 17 domains after knowledge population is sufficiently mature.