---
id: SKILL-CONS-001
name: Consolidation and group reporting
version: 0.1.0
status: review
primary_domain: "07"
related_domains: ["08", "09", "14", "15"]
description: Governed consolidation and group reporting assessment, calculation and review pack.
triggers: [consolidation, accounting assessment, journal and disclosure review]
non_triggers: [legal advice, tax advice, unaudited assumption as fact]
framework_sensitivity: HIGH
applicable_frameworks: [IFRS, US_GAAP, UK_GAAP, AASB]
jurisdiction_sensitivity: HIGH
industry_sensitivity: HIGH
context_requirements:
  required: [group_structure, ownership_and_rights, control_assessment, entity_trial_balances, reporting_period, framework, intercompany_balances]
  retrieve_if_available: [entity_policy_elections, materiality, prior_period_workpapers, chart_of_accounts, disclosure_checklist]
inputs: [case_facts, evidence, framework_and_period, policy_elections, reviewed_assumptions]
outputs: [skill_result, accounting_memo, calculation_workpaper, journals, citations, review_items]
artifacts: [technical_memo, measurement_schedule, journal_pack, reconciliation, disclosure_support]
dependencies: [approved_topic_retrieval, company_context, deterministic_calculator, reviewer_signoff]
related_skills: [technical_accounting_research, disclosure_review, close_reconciliation]
knowledge_sources:
  principles: [TOPIC-07-001, TOPIC-07-002, TOPIC-07-003, TOPIC-07-004, TOPIC-07-005, TOPIC-07-006, TOPIC-07-007, TOPIC-07-008, TOPIC-07-009]
  standards: [TOPIC-07-001, TOPIC-07-002, TOPIC-07-003, TOPIC-07-004, TOPIC-07-005, TOPIC-07-006, TOPIC-07-007, TOPIC-07-008, TOPIC-07-009]
  practice: [TOPIC-07-001, TOPIC-07-002, TOPIC-07-003, TOPIC-07-004, TOPIC-07-005, TOPIC-07-006, TOPIC-07-007, TOPIC-07-008, TOPIC-07-009]
risk_level: HIGH
review_required: true
completion_criteria: [framework_and_period_resolved, all_required_facts_present, approved_claims_retrieved, method_and_judgments_documented, arithmetic_reconciled, journals_balance, citations_checked, reviewer_signoff]
---

# Consolidation and group reporting — governed execution contract

Determine consolidation perimeter under IFRS 10/AASB 10, ASC 810 and applicable FRS 102, including substantive rights, variable returns or VIE assessments, NCI and changes in ownership. Align reporting dates and accounting policies, translate foreign operations, eliminate investments/equity, intercompany balances, transactions and unrealized profits, roll forward NCI and reconcile consolidated financial statements.

## Workflow
1. Establish the entity, applicable framework, jurisdiction, reporting period, adoption status and entity-specific policy elections.
2. Collect all required contract, transaction and accounting evidence. Distinguish facts from assumptions; block rather than invent essential inputs.
3. Retrieve the approved canonical topic knowledge and claim registers above. Select only claims applicable to the framework, period and entity scope. Preserve the claim evidence tier and any unverified pinpoint references.
4. Complete the relevant recognition, classification and measurement decision tree; explicitly document competing routes and judgments.
5. Run the deterministic numerical workpaper only after the accounting route and input assumptions are approved. Reconcile opening-to-closing balances, journals and supporting source data.
6. Generate an accounting memo, alternative/adverse-case analysis, entries, disclosure checklist, control owner and audit-evidence requirements.
7. Cite the specific standard and paragraph where the governed claim establishes a reliable locator; label provisional references for independent verification rather than inventing certainty.
8. Return the standard result envelope in architecture/skill-specification.md. Apply the existing public-output adapter and obtain reviewer sign-off before posting entries.

## Specialist boundaries
Do not infer control solely from ownership percentage; do not treat ASC 810 VIE analysis as IFRS 10; do not manufacture acquisition-date fair values, goodwill, FX rates or non-controlling-interest elections.

The skill is not production-complete until executable decision routes, period/framework tests, numerical regression, output boundary, and integration tests pass. A contract alone does not satisfy that gate.
