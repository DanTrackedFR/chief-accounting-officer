# Build Roadmap

## Phase 1 — Operating system

Status: **complete**.

Deliverables: scope, domains, complete skill map, skill contract, CAO Agent, orchestration, cases, Company Accounting Memory, schemas, knowledge architecture, artifact architecture, evaluations, and build sequencing.

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

Completed to REVIEWED knowledge status:
- TOPIC-02-001 Month-End Close Design / Calendar / Critical Path — fec625ca
- TOPIC-02-002 Journal Entry Preparation / Review / Manual Governance — 00142dab
- TOPIC-02-003 Recurring & Automated Journals / GL Integrity — 0e1510a1
- TOPIC-02-004 Trial Balance Review / Balance Sheet Reconciliations — f7425aeb
- TOPIC-02-005 Reconciliation Governance / Account Certification — 9395eb20

Regression 001: PASS. Later regression enhancement added temporal routing and reusable evidence/risk primitives.

### Batch 002 — Close & GL completion — 22 September 2026

Completed to REVIEWED knowledge status:
- TOPIC-02-006 Suspense/Clearing & Cut-Off — d7ddc28b
- TOPIC-02-007 Accruals & Prepaids — 73dd2e7e
- TOPIC-02-008 Flux Review & Post-Close Governance — 1a455ecf
- TOPIC-02-009 Prior-Period Errors & Opening-Balance Integrity — 98ecfd8d
- TOPIC-02-010 Close Evidence / Sign-Off / Fast Close — 2298b7f7

Regression 002 (full Domain 02 family): PASS — 4ee9619f.

### Batch 003 — Revenue start + reporting dependency — 22 September 2026

Worked through to REVIEWED / production-candidate:
- TOPIC-03-001 Revenue Contract Accounting Assessment / Performance Obligation Identification. Full four-framework routing, revised FRS 102 Section 23 paragraph map, CAO workflow, differences, controls/systems and 10 scenario tests. US Codification paragraph depth explicitly PARTIAL pending direct current Codification verification.
- TOPIC-08-005 Going Concern / Subsequent Events. Four-framework routing, effective-date logic, CAO assessment workflow, differences, controls/audit/systems and 10 scenario tests. US ASC 205-40/855 paragraph depth explicitly PARTIAL pending direct current Codification verification.
- TOPIC-03-002 Variable Consideration / Transaction Price Allocation — 2974a279. IFRS/AASB official transaction-price/allocation architecture, FRC 2026 routing, FASB Topic 606 implementation guidance, CAO execution logic, example, controls/systems/artifacts and eight scenarios. US Codification paragraph depth remains PARTIAL under the same recorded source limitation.
- TOPIC-03-003 Revenue Recognition Timing / Contract Modifications — 1a3d2932. IFRS/AASB over-time/point-in-time routing, enforceable-right-to-payment logic, contract-modification decision model, FRS 102 effective-period routing, US Topic 606 architecture, controls/audit/systems and eight scenarios. US paragraph depth remains PARTIAL.

Non-blocking source limitation: public FASB materials confirm Topic 606 / ASC 205-40 / ASC 855 architecture but do not expose all current Codification paragraph bodies required for APPROVED paragraph-level status. Per build rule, the limitation is recorded and work continues rather than stopping the programme.

Cumulative Phase 2D topics worked through: **14** (10 Domain 02 + TOPIC-03-001/002/003 + TOPIC-08-005). No fully blocked topics.

Next: continue Revenue & Receivables TOPIC-03-004 onward; run next family regression after 5–10 additional topics.

## Phase 3 — Production skills

Build skills systematically across all 17 domains after knowledge population is sufficiently mature. Each production skill receives contract, methods, knowledge references, checklists, templates, examples and tests.
