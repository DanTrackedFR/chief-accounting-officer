---
id: SKILL-INS-001
name: insurance-contracts-accounting
skill_id: SKILL-INS-001
version: 0.9.0
status: review
roadmap: 39
primary_domain: insurance_accounting
related_domains: [financial_instruments, reporting, actuarial_sources]
description: Governed insurance contract classification and accounting of independently qualified actuarial inputs.
triggers: [insurance_contracts, insurance_service_revenue, insurance_liabilities, reinsurance_held]
non_triggers: [actuarial_projection, investment_portfolio, derivative_valuation, claims_management, ERP_posting]
framework_sensitivity: HIGH
applicable_frameworks: [IFRS, AASB, US_GAAP]
jurisdiction_sensitivity: HIGH
industry_sensitivity: HIGH
context_requirements:
  required: [framework, entity, period_start, reporting_period, entity_type, currency, operative_standard, actuarial_report, complete_source_populations]
  retrieve_if_available: [qualified_owner_outputs, policy_history]
inputs: [contract_terms, complete_policy_groups, controlled_claims_cash_costs, current_actuarial_reports, qualified_assumptions_and_model_versions, GL, statement_review, disclosure_review]
outputs: [classification, group_rollforwards, CSM_RA_loss_bridges, gross_reporting_support, balanced_journals, qualified_input_boundary, explicit_handoffs]
artifacts: [accounting_workpaper, source_lineage, statement_support, disclosure_support]
dependencies: [approved_insurance_supplement, qualified_actuarial_review, current_case_certification]
related_skills: [financial-instruments-ecl, fair-value-measurement, derivatives-hedge-accounting, foreign-currency, revenue-recognition, provisions-contingencies, business-combinations, financial-statements, disclosure-management, accounting-systems-data-integrity, accounting-controls-icfr, accounting-changes]
knowledge_sources:
  principles: [knowledge/insurance-contracts/FRAMEWORK-METHOD.md]
  standards: [knowledge/insurance-contracts/standards-claims.json]
  practice: [knowledge/insurance-contracts/RESEARCH.md]
risk_level: HIGH
review_required: true
completion_criteria: [approved_current_knowledge, exact_controlled_populations, supported_contract_model, qualified_actuarial_sources, balanced_journals, GL_and_reporting_ties, framework_disclosure_support, independent_exact_case_signoff]
---

# Insurance Contracts / Insurance Accounting

Invoke `production.assess_case('insurance-contracts-accounting', case)`.
The supplemental namespace is `SUPPLEMENTAL_INSURANCE_CONTRACTS`; it never changes
historical canonical topic IDs or denominators. Read methods.md before execution.

Own insurance scope, group/contract recognition and supported insurance accounting.
Consume qualified actuarial output; never prepare or certify actuarial projections,
IBNR, mortality, lapses, assumptions, discount curves, risk adjustment or coverage
forecasts. Source hashes preserve reviewed bytes; they do not authenticate a human
identity or prove source truth. Actual qualification evidence and independent review
remain required. Synthetic examples contain synthetic signoffs only.

Supported accounting uses new groups recognized in 2026, one functional currency,
for-profit full IFRS or AASB Tier1 and native US GAAP short-duration issued contracts.
IFRS/AASB issued routes support nonparticipating GMM and eligible PAA. Reinsurance
held supports prospective proportionate PAA with separately qualified linked gross
underlying business and nonperformance assessment. UK FRS103 measurement remains
blocked pending actual existing policy and legal-format evidence.

`calculations.groups` exposes remaining coverage, incurred claims/recoveries, CSM,
RA, loss component, service and finance amounts. `statement_support` contains exact
signed debit balances and semantic account categories. `disclosure_support` exposes
source populations and framework review requirements; `amounts_by_group` provides
numeric scalar paths for native Disclosure Management. Final statements and final
applicability checklists remain with their owners. No source journals are reposted.
