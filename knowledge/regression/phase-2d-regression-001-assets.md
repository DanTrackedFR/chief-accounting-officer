# Phase 2D Regression Review 001 — Assets Family

Date: 2026-09-23
Scope: TOPIC-04-001 through TOPIC-04-006 plus existing Lease vertical slice TOPIC-04-007 through TOPIC-04-011 architecture.

## Findings
1. **Temporal routing must be first-class, not metadata-only.** AASB compilation periods, FRS 102 Periodic Review 2024, and US ASU 2025-06 software changes can change the applicable model. Every standards-heavy topic must resolve reporting period before retrieving records.
2. **Framework inheritance is dangerous even where standards are closely aligned.** AASB generally mirrors IFRS in these asset topics but Australian compilation dates, NFP material and disclosure tiers require independent verification.
3. **Topic boundaries work when dependencies are explicit.** PPE recognition routes software to TOPIC-04-004 and impairment to TOPIC-04-006 rather than duplicating rules. CIP owns the operating/reconciliation process while software owns recognition eligibility.
4. **US GAAP needs model-routing before rules.** PPE, software and impairment are distributed across ASC topics/subtopics and accounting alternatives; the CAO must classify the asset/arrangement before applying mechanics.
5. **Policy thresholds are not GAAP recognition criteria.** Capitalization thresholds belong in PRACTICE/Company Context with materiality governance.
6. **Operational data contracts should be standardized.** Asset topics repeatedly require entity, asset/project ID, source document, date, cost, class, status, GL mapping, evidence link and reviewer status. This should become a reusable asset data contract in Phase 3.

## Quality review
- No direct standards text intentionally stored.
- Official primary source families used for IFRS/AASB/FRC and FASB where accessible.
- Secondary interpretation is not treated as primary authority.
- Framework differences are expressed as accounting consequences.
- Controls, evidence, systems and scenarios included.
- Blockers/partial depth are stated rather than hidden.

## Architecture change recommendation
Add mandatory `effective_period_resolution` and `adoption_status` fields to standards-sensitive skill retrieval. For US GAAP future-effective ASUs and UK/Australian compilation changes, retrieval should fail closed if period/adoption cannot be resolved and the difference could alter accounting.

## Progress
New production-candidate topics in this batch: TOPIC-04-001, 04-002, 04-003, 04-005, 04-006. TOPIC-04-004 already existed and was reviewed; its US paragraph depth remains explicitly PARTIAL. Lease topics remain governed by Phase 2C status.
