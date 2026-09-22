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
- TOPIC-03-004 Principal-versus-Agent / Contract Asset & Liability Accounting — 310e8e1d. Includes IFRS/AASB principal-agent control logic, IFRIC software-reseller implementation evidence, contract-balance classification, revised FRS 102 period routing, Topic 606 routing, journals, controls/systems and five scenarios. US source depth PARTIAL.
- TOPIC-03-005 Deferred / Unbilled Revenue — 76dcec2d. Converts contract-balance standards into operational rollforwards, billing/performance classification, controls, systems and scenarios. US source depth PARTIAL.
- TOPIC-03-006 Contract Costs / Sales Commissions & Billing Completeness — 3073dd17. Includes IFRS/AASB contract-cost model, IFRIC fulfilment-cost guidance, official FASB IFRS15/Topic606 comparison mapping to ASC 340-40, UK effective-period routing, billing completeness workflow, controls/systems and scenarios.

Cumulative Phase 2D topics worked through: **17**. No fully blocked topics.

### Regression / hygiene finding
Regression file 3f0cc5ba records two repository-hygiene issues discovered during scaling: the Phase 2C lease folder naming spans canonical TOPIC-04-007 through 04-010 rather than matching the Phase 2B denominator one-to-one; and build retries created duplicate TOPIC-02-001 folders. These do not block substantive work, but completion-count automation must use the canonical topic universe rather than raw folder counts until normalization is completed.

Next: TOPIC-03-007 onward. Run the next revenue-family regression after another 2–5 topics.

## Phase 3 — Production skills
Build skills systematically across all 17 domains after knowledge population is sufficiently mature.