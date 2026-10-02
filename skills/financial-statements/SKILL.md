---
id: SKILL-FS-001
name: Financial statements and disclosures
version: 0.9.0
status: review
primary_domain: "08"
related_domains: ["07", "08", "09", "14", "15"]
description: Governed financial statements and disclosures workpaper, accounting decisions, reconciliations, journals, disclosure review and specialist routing.
triggers: [financial statements and disclosures, accounting assessment, journal and disclosure review]
non_triggers: [legal opinion, autonomous valuation, unsupported tax conclusion, automatic posting]
framework_sensitivity: HIGH
applicable_frameworks: [IFRS, US_GAAP, UK_GAAP, AASB]
jurisdiction_sensitivity: HIGH
industry_sensitivity: HIGH
context_requirements:
  required: [entity, jurisdiction, framework, entity_type, period_start, reporting_period, effective_standards, policy_elections, evidence, judgment_memo, assumptions]
  retrieve_if_available: [materiality, prior_workpapers, source_ledgers, regulatory_scope, chart_of_accounts]
inputs: [presentation, current_tb, comparative_tb, comparative, cash_flow, equity_bridge, notes, checklist, coverage]
outputs: [skill_result, technical_memo, calculation_schedule, journal_pack, disclosure_review, specialist_handoff]
artifacts: [reviewed_case, numerical_workpaper, reconciliations, journals, public_output, certification]
dependencies: [approved_canonical_knowledge, company_context, accounting_judgments, specialist_inputs, independent_review]
related_skills: [consolidation, disclosure_review, technical_accounting_research]
knowledge_sources:
  principles: ["TOPIC-08-001","TOPIC-08-002","TOPIC-08-003","TOPIC-08-004","TOPIC-08-005","TOPIC-08-006","TOPIC-08-007","TOPIC-08-008","TOPIC-08-009"]
  standards: ["TOPIC-08-001","TOPIC-08-002","TOPIC-08-003","TOPIC-08-004","TOPIC-08-005","TOPIC-08-006","TOPIC-08-007","TOPIC-08-008"]
  practice: ["TOPIC-08-001","TOPIC-08-002","TOPIC-08-003","TOPIC-08-004","TOPIC-08-005","TOPIC-08-006","TOPIC-08-007","TOPIC-08-008","TOPIC-08-009"]
risk_level: HIGH
review_required: true
completion_criteria: [approved_scope_and_period, supported_facts_and_assumptions, applicable_claim_selection, balanced_journals, reconciled_bridges, disclosure_population_review, public_output_safe, independent_certification, independent_package_QA, full_regression]
---

# Financial statements and disclosures — governed execution contract

IAS 1 / IFRS 18 / IAS 7; applicable ASC and SEC; FRS 102 Sections 3–8; AASB 101 / 18 / 107 / 1060. Read methods.md and the complete canonical knowledge documents returned by canonical_knowledge before preparing a case. Approved topic status is not direct authoritative verification.

1. Resolve framework, jurisdiction, entity scope, reporting dates, actual edition/amendments and elections. Use the shared context gates; UK FRS 101/105 and Australian NFP/public-sector overlays require separate methods.
2. Inspect complete source populations. Separate company facts, supported judgments and explicit assumptions. Do not invent rates, forecasts, valuations, legal rights, approval, tax bases or materiality.
3. Retrieve approved claims and exact document hashes. Independently select applicable claim IDs and document period/entity scope. Preserve evidence ratings and unresolved authority audit requirements. Qualify provisional paragraph references as unverified; never add a guessed locator.
4. Execute `production.assess_case("financial-statements", case)` through `run_skill.py`. Apply `workflow.py` only within the bounded methods described in methods.md. Missing facts, unsupported model routes or unresolved specialist work return a blocked standard envelope and evidence-specific handoff, without journals.
5. Reperform deterministic schedules, source-population completeness, journal balances and statement/note tie-outs. Review alternative/adverse routes; matching arithmetic does not prove the accounting judgment.
6. Review disclosure applicability using the actual tier, filer, period and transaction population. Assign owner/evidence and resolve all material open items before certification.
7. Obtain an independent reviewer record, distinct from preparer, bound to the exact case, canonical knowledge and implementation fingerprint. Missing/stale signoff returns partial. Synthetic regression identities are examples, not authenticated authorization.
8. Render only through `production.to_public` for all registered routes. Keep source notes, evidence-tier objects, internal memos and reviewer metadata internal. Public safety failures block completion.
9. Hand off tax, valuation, legal, specialized transaction and filing questions to named subject specialists with required evidence and a rerun/certification gate. Do not book specialist-generated estimates until supported by reviewed workpapers.

Read `../REVIEWER-CONTROLS.md`. No ERP posting is performed. Reconcile illustrative account labels to the company-approved chart and close controls. Test success alone cannot promote this package. The completion report and independent QA determine package promotion; unresolved cases remain blocked even for a production package.

