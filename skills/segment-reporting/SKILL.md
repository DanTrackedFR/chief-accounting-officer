---
id: SKILL-SEG-001
name: "Segment Reporting"
version: 0.9.0
status: review
primary_domain: "08"
related_domains: ["02", "04", "05", "06", "07", "08", "13", "15"]
description: Governed segment reporting workflow with independently evidenced accounting and fail-closed boundaries.
triggers: ["Segment Reporting", reporting assessment, disclosure reconciliation]
non_triggers: [ERP posting, legal advice, autonomous valuation, reserved specialist implementation]
framework_sensitivity: HIGH
applicable_frameworks: [IFRS, US_GAAP, UK_GAAP, AASB]
jurisdiction_sensitivity: HIGH
industry_sensitivity: HIGH
context_requirements:
  required: [case_id, entity, framework, jurisdiction, entity_type, period_start, reporting_period, execution_date, applicability_review, evidence, judgment_memo, assumptions, controls, disclosure_review, knowledge_review]
  retrieve_if_available: [prior_workpapers, legal_rights, consolidated_statements, specialist_workpapers]
inputs: [independent_source_inventory, current_approvals, qualified_framework_methods, reconciled_statement_population]
outputs: [skill_result, calculation_schedule, disclosure_workpaper, specialist_handoff]
artifacts: [case, source_reconciliation, worked_examples, partial_public_output, reviewer_certification]
dependencies: [approved_knowledge, company_context, accounting_owners, independent_review]
related_skills: [equity-capital, financial-statements, accounting-changes, going-concern, debt-financing, income-taxes]
knowledge_sources:
  principles: [TOPIC-08-006]
  standards: [TOPIC-08-006]
  practice: [PRESENTATION-KNOWLEDGE-MAP.json, methods.md]
risk_level: HIGH
review_required: true
completion_criteria: [approved_scope, operative_framework_period, current_evidence, independent_population, deterministic_reconciliation, balanced_entries_where_applicable, disclosures, independent_exact_fingerprint_review, public_privacy, independent_QA, full_regression]
---

# Governed execution contract

Actual CODM component identification, qualified aggregation/reportability parameters, coverage, corporate/intersegment bridges and complete geography/product/customer disclosure populations.

Actual period statement-line populations bind revenue/profit/assets/liabilities and included geographic noncurrent assets to GL and any completed Financial Statements import. Mixed-profit/loss aggregation is outside the supported threshold-denominator adapter.

No invented CODM practices, economic similarity or framework thresholds. UK obligation and US effective significant-expense/single-segment disclosures require qualified operative review.

1. Read methods.md, actual mapped knowledge documents/claims and ../REVIEWER-CONTROLS.md. Use the immutable batch map; APPROVED never implies SOURCE_VERIFIED. Preserve all reference-confidence qualifications.
2. Resolve framework/entity/jurisdiction, reporting start/end, actual operative edition/adoption and scope. Obtain qualified current methods where canonical knowledge does not prescribe detailed mechanics. Do not import IAS33/IFRS8 obligations into all FRS102 entities.
3. Freeze complete source IDs, amounts/counts, dated populations and independent source/statement bridges. Distinguish management assumptions from facts; obtain legal/management evidence.
4. Call production.assess_case("segment-reporting",case) through the established CLI. Guarded Decimal calculations and controlled schedules never manufacture facts, rights, probabilities, approvals or source evidence.
5. Keep underlying journal ownership with its existing skill. Require fresh completed, unaltered entity/framework/period results and exact-once reconciliation rather than silently reperforming specialist measurement.
6. Resolve disclosures, comparatives, significant judgments, alternatives and unsupported routes. Missing or inconsistent facts fail closed without journals; missing/stale independent certification remains partial.
7. Require independent reviewer/preparer separation and exact case, knowledge-document and implementation fingerprints. These validate supplied approval records, not human identity.
8. Render through the existing seven-route allowlist; exclude raw evidence, source notes, reviewer information and hashes. Retain material limitations in ordinary language.
9. Retain case/version, source lineage, reconciliations, unresolved dependencies and rerun history. Never post, file, submit returns or contact counterparties.

Production promotion requires independent accounting QA and the full repository gate, not calculator success.
