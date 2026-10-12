---
id: SKILL-BORROW-001
name: "Borrowing Costs"
version: 1.0.0
status: production
primary_domain: "04"
related_domains: ["02", "04", "05", "06", "07", "08", "13", "15"]
description: Governed borrowing costs workflow with independently evidenced accounting and fail-closed boundaries.
triggers: ["Borrowing Costs", construction interest capitalization, qualifying asset financing cost]
non_triggers: [ERP posting, legal advice, autonomous valuation, debt recognition, investment property, government grants]
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
  principles: [SUPPLEMENTAL_BORROWING_COSTS]
  standards: [SUPPLEMENTAL_BORROWING_COSTS]
  practice: [SUPPLEMENTAL-KNOWLEDGE-MAP.json, methods.md]
risk_level: HIGH
review_required: true
completion_criteria: [approved_scope, operative_framework_period, current_evidence, independent_population, deterministic_reconciliation, balanced_entries_where_applicable, disclosures, independent_exact_fingerprint_review, public_privacy, independent_QA, full_regression]
---

# Governed execution contract

Read methods.md and the approved supplemental package. Version 1.0.0 supports the independently accepted bounded methods in methods.md; it does not assert universal domain support. The original 0.1.0 NONPRODUCTION CIP-only method and archived blocked examples remain historical baseline evidence.

1. Qualify the exact framework, entity and 2026 annual edition; unsupported overlays fail closed.
2. Independently review one tangible construction object, actual paid expenditure, full temporal population and original financing sources.
3. Reconcile specific/general sources, dated contractual accruals, draws, repayments, temporary investment income and weighted general rates with exact Decimal arithmetic.
4. Execute only through production.assess_case("borrowing-costs", case); retain original source capture and independent knowledge review.
5. Keep debt and asset recognition with their existing owners. Only expense-to-asset allocation belongs here.
6. Reconcile construction cost and finance expense to source, GL snapshot and financial statement support.
7. Require independent exact-fingerprint case certification before releasing journal implications. Missing certification is PARTIAL; unsupported accounting is BLOCKED.
8. Render through the established allowlist. Never export private source records, approval identities or hashes; never post to ERP.

Bounded supported scope, methods and exclusions are explicit in methods.md; broad Borrowing Costs coverage is not asserted.
