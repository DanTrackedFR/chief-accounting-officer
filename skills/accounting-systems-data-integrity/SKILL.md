---
id: SKILL-SYS-001
name: "Accounting Systems & Data Integrity"
version: 0.9.0
status: review
primary_domain: "11"
related_domains: ["02", "08", "09", "10", "11", "15"]
description: Supplied accounting interface lineage, exact item/source-target/migration reconciliation and evidenced control requirements; no engineering writes.
triggers: ["Accounting Systems & Data Integrity", bounded accounting workpaper]
non_triggers: [autonomous valuation, external certification, ERP posting, system mutation, excluded specialists]
framework_sensitivity: NONE
applicable_frameworks: [IFRS, US_GAAP, UK_GAAP, AASB]
jurisdiction_sensitivity: HIGH
industry_sensitivity: HIGH
context_requirements:
  required: [case_id, entity, framework, jurisdiction, entity_type, period_start, reporting_period, execution_date, controls, evidence, judgment_memo, assumptions, applicability_review, knowledge_review]
  retrieve_if_available: [actual_owner_results, prior_workpapers, specialist_reports]
inputs: [independent_original_populations, actual_source_documents, current_qualified_method, accounting_owner_imports]
outputs: [skill_result, bounded_workpaper, journal_implications_where_supported, unresolved_handoff]
artifacts: [source_reconciliation, controlled_case, reviewer_certification, synthetic_examples]
dependencies: [approved_knowledge, actual_entity_context, current_evidence, independent_review]
related_skills: [employee-benefits-payroll, financial-statements, management-accounting-analytics, ipo-accounting-readiness, audit-support-pbc]
knowledge_sources:
  principles: [TOPIC-11-002, TOPIC-11-003, TOPIC-11-004, TOPIC-11-005, TOPIC-11-006, TOPIC-11-007, TOPIC-11-009]
  standards: [TOPIC-11-002, TOPIC-11-003, TOPIC-11-004, TOPIC-11-005, TOPIC-11-006, TOPIC-11-007, TOPIC-11-009]
  practice: [FINAL-BATCH-KNOWLEDGE-MAP.json, methods.md]
risk_level: HIGH
review_required: true
completion_criteria: [bounded_knowledge_sufficiency, actual_case_applicability, full_original_populations, current_owner_imports, exact_case_knowledge_implementation_fingerprints, independent_review, privacy, independent_QA, full_regression, exact_head_CI]
---

# Bounded execution contract

Supplied accounting interface lineage, exact item/source-target/migration reconciliation and evidenced control requirements; no engineering writes.

Read methods.md, ../REVIEWER-CONTROLS.md and the actual frozen canonical documents before invoking production.assess_case("accounting-systems-data-integrity", case). Use the existing runtime and public interface. APPROVED is not SOURCE_VERIFIED; retain every evidence rating, audit flag, approval track and effective-period limitation.

Require current original source populations, separate preparer/reviewer, source snapshots/content hashes, and exact release/case certification. Imports must be actual current complete unaltered same-entity/framework/jurisdiction/period results, evidence-only and exact-once. A missing signature is partial; contradictory or unsupported facts block. Workpaper completion is never external compliance or legal/actuarial/audit approval.

Public output allowlists generated schedules and material limitations only. Raw source notes, original memos, evidence internals, reviewers and fingerprints remain internal across all seven routes. Synthetic approvals are regression fixtures, not authenticated people. No external actions are authorized.
