---
id: SKILL-AGR-001
name: "Agriculture / Biological Assets"
roadmap_number: 38
version: 1.0.0
status: production
primary_domain: "14"
related_domains: ["04", "08", "09", "11", "15"]
description: Bounded agricultural biological-asset accounting using independently governed supplemental knowledge and qualified valuation evidence.
triggers: [agriculture accounting, biological assets, IAS 41, AASB 141, FRS 102 agriculture]
non_triggers: [farm management, agronomy, autonomous valuation, post-harvest inventory, government grants, ERP posting]
framework_sensitivity: HIGH
applicable_frameworks: [IFRS, US_GAAP, UK_GAAP, AASB]
jurisdiction_sensitivity: HIGH
industry_sensitivity: HIGH
context_requirements:
  required: [case_id, entity, framework, jurisdiction, period_start, reporting_period, execution_date, accounting_policy, applicability_review, knowledge_review, controls, assets, asset_source, movements, movement_source, opening_population, closing_population, documents, classification, disclosures, currency, gl]
  retrieve_if_available: [qualified_valuation_reports, actual_owner_results, legal_control_evidence]
inputs: [current_controlled_source_populations, quantity_and_GL_records, qualified_current_valuations, harvest_records, disclosure_requirements]
outputs: [skill_result, quantity_and_monetary_rollforward, measurement_gain_bridge, harvest_entry_schedule, balanced_journal_pack, downstream_handoff]
artifacts: [source_reconciliation, technical_workpaper, synthetic_examples, exact_case_certification]
dependencies: [SUPPLEMENTAL_AGRICULTURE, qualified_valuation, current_applicability, independent_review]
related_skills: [fixed-assets, fair-value-measurement, financial-statements, disclosure-management, foreign-currency, inventory-cost, government-grants]
knowledge_sources:
  principles: [SUPPLEMENTAL_AGRICULTURE]
  standards: [SUPPLEMENTAL_AGRICULTURE]
  practice: [methods.md, AGRICULTURE-KNOWLEDGE-MAP.json]
risk_level: HIGH
review_required: true
completion_criteria: [independent_claim_approval, current_source_reconciliation, exact_case_review, independent_implementation_QA, privacy, full_regression, exact_head_CI]
---

# Specialist accounting contract

Skill #38 owns the biological-asset accounting decision, through the supported harvest boundary. Invoke through `production.assess_case("agriculture-biological-assets", case)` and the existing public allowlist. Read the approved supplemental documents and methods.md first. APPROVED preserves the actual evidence ratings and future authoritative audit flags; source notes remain internal.

Supplemental knowledge and implementation have separate independent approvals. This 1.0.0 production candidate remains unmerged until the full regression, reproduced examples and exact-head CI gates pass and integration review accepts it. No repository or ERP merge/posting is authorized by this skill.
