---
id: SKILL-IP-001
name: "Investment Property"
version: 1.0.0
status: production
primary_domain: "04"
related_domains: ["02", "04", "05", "06", "07", "08", "13", "15"]
description: Governed bounded special-reporting workflow with independently evidenced accounting and fail-closed boundaries.
triggers: ["Investment Property", reporting assessment, disclosure reconciliation]
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
related_skills: [fixed-assets, fair-value-measurement, asset-impairment, financial-statements]
knowledge_sources:
  principles: [TOPIC-04-001]
  standards: [SUPPLEMENTAL_INVESTMENT_PROPERTY]
  practice: [SUPPLEMENTAL-KNOWLEDGE-MAP.json, methods.md]
risk_level: HIGH
review_required: true
completion_criteria: [approved_scope, operative_framework_period, current_evidence, independent_population, deterministic_reconciliation, balanced_entries_where_applicable, disclosures, independent_exact_fingerprint_review, public_privacy, independent_QA, full_regression]

---

# Bounded execution contract

Bounded production candidate: full-framework for-profit calendar2026 owned ordinary single-property, single-functional-currency accounting. Only period-end events are supported: cash purchase, holding measurement, qualified IFRS/AASB cost transfers, fair-value transfer out and cash disposal. Independent release QA and exact-head Actions remain required before owner integration.

Read methods.md, the actual independently approved 96-claim supplemental package and ../REVIEWER-CONTROLS.md. APPROVED never implies SOURCE_VERIFIED: all96 claims retain independently checked model-derived assurance and an open direct-authority audit. The canonical PPE pointer remains classification background only.

Resolve actual entity, framework, jurisdiction, period, edition/adoption, scope and economic/legal facts. Obtain independently reviewed current applicability evidence. Only call production.assess_case("investment-property",case) through the established CLI. The complete status applies solely to this declared workpaper scope.

Freeze independent populations, source identities and amounts, actual case versions and the disclosure checklist. Every source approval must be independent and current. Supplied accounting judgments are evidenced inputs, not model conclusions or authenticated human identity. Require exact case, knowledge and implementation fingerprints. Missing/stale sign-off is partial; contradictions and unsupported routes block.

IFRS/AASB permit documented cost or fair value. Full FRS102 calendar2026 requires ordinary-property fair value; group-lessor cost follows the specific group election and PPE presentation, never the deleted undue-cost-or-effort exception. Ordinary US property is historical-cost PPE, not an IAS40 fair-value category. Cost depreciation/impairment are independently qualified existing-owner effects, rechecked and retained once; no duplicate owner journal is emitted.

Cost transfer-in requires a current PPE owner carrying-value bridge, including pre-transfer depreciation/impairment, rather than reuse of prior-year carrying value. Those charges remain outside the IP class rollforward and are not posted twice. Every closing IFRS/AASB cost-model property, including cutoff acquisition and transfer-in, requires a qualified reporting-date fair-value disclosure amount without fair-value recognition. All US transfer routes remain blocked with the PPE owner.

Initial recognition is limited to explicitly qualified cash purchases of nongifted property with independently evidenced strictly positive property-price consideration, distinct from paid transaction fees. Missing acquisition-nature/gift qualifications, gifts, nonexchange acquisitions and fee-only or zero-price acquisitions are blocked for separately governed original-owner treatment; this adapter establishes no gift measurement method.

Legacy0.1.0 cases remain NONPRODUCTION. ROU/finance-lessor, construction, combinations, intra-year activity, into-FV PPE revaluation, inventories/held-for-sale, industry models, policy/estimate changes, prior cost impairment, foreign operations, other periods and Tier2/NFP/small-entity overlays fail closed. Neither a valuation certificate nor a reviewer assertion expands accounting authority. Native owner-result imports remain blocked pending an asset-bound adapter; source-qualified documentary workpapers are supported.

Return controlled derived schedules and material limitations through the seven-route public allowlist. Exclude raw evidence, sources, reviewers, hashes and claim internals. No posting, legal advice, regulatory certification, filing or external communication is authorized.
