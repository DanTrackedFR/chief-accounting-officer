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

Regression 001: PASS — 49f69710.

### Batch 002 — Close & GL completion — 22 September 2026

Completed to REVIEWED knowledge status:
- TOPIC-02-006 Suspense/Clearing & Cut-Off — d7ddc28b
- TOPIC-02-007 Accruals & Prepaids — 73dd2e7e
- TOPIC-02-008 Flux Review & Post-Close Governance — 1a455ecf
- TOPIC-02-009 Prior-Period Errors & Opening-Balance Integrity — 98ecfd8d
- TOPIC-02-010 Close Evidence / Sign-Off / Fast Close — 2298b7f7

Regression 002 (full Domain 02 family): PASS — 4ee9619f.

Cumulative Phase 2D coverage: **10 top-level topics / 22 mapped capabilities**. No blockers. Domain 02 is fully worked through to REVIEWED knowledge status. Standards anchors were checked against current official IFRS Foundation, FASB, FRC and AASB sources where standards-sensitive conclusions arise.

Architecture finding confirmed: close/GL execution knowledge should invoke underlying accounting topics for recognition conclusions rather than duplicate standards logic inside operational records. Reconciliation assertion logic and error-versus-estimate routing become reusable primitives for later domains.

Next: recurring-controller core, beginning Revenue & Receivables.

## Phase 3 — Production skills

Build skills systematically across all 17 domains after knowledge population is sufficiently mature. Each production skill receives contract, methods, knowledge references, checklists, templates, examples and tests.
