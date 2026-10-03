---
id: SKILL-HYPER-001
name: "Hyperinflation Accounting"
version: 1.0.0
status: production
primary_domain: "13"
related_domains: ["02", "04", "05", "06", "07", "08", "13", "15"]
description: Governed bounded special-reporting workflow with independently evidenced accounting and fail-closed boundaries.
triggers: ["Hyperinflation Accounting", reporting assessment, disclosure reconciliation]
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
related_skills: [foreign-currency, consolidation, income-taxes, financial-statements]
knowledge_sources:
  principles: [TOPIC-13-011]
  standards: [TOPIC-13-011]
  practice: [SPECIAL-REPORTING-KNOWLEDGE-MAP.json, methods.md]
risk_level: HIGH
review_required: true
completion_criteria: [approved_scope, operative_framework_period, current_evidence, independent_population, deterministic_reconciliation, balanced_entries_where_applicable, disclosures, independent_exact_fingerprint_review, public_privacy, independent_QA, full_regression]

---

# Bounded execution contract

IFRS/AASB economic-assessment and isolated index workpaper only. Complete purchasing-power accounting, US/UK measurement and all translation/consolidation remain separate blocked routes.

Read methods.md, the complete actual approved documents/claims in the immutable batch map and ../REVIEWER-CONTROLS.md. APPROVED never implies SOURCE_VERIFIED. Preserve all evidence ratings and limitations.

Resolve actual entity, framework, jurisdiction, period, edition/adoption, scope and economic/legal facts. Obtain independently reviewed current applicability evidence. Only call production.assess_case("hyperinflation-accounting",case) through the established CLI. The complete status applies solely to this declared workpaper scope.

Freeze independent populations, source identities and amounts, actual case versions and the disclosure checklist. Every source approval must be independent and current. Supplied accounting judgments are evidenced inputs, not model conclusions or authenticated human identity. Require exact case, knowledge and implementation fingerprints. Missing/stale sign-off is partial; contradictions and unsupported routes block.

Cross-skill imports must be current, complete, exact entity/framework/period and unaltered, used once as evidence only. No journals from an existing owner are reposted. External supplied workpapers cannot authorize an unsupported engine.

Return controlled derived schedules and material limitations through the seven-route public allowlist. Exclude raw evidence, sources, reviewers, hashes and claim internals. No posting, legal advice, regulatory certification, filing or external communication is authorized.
