---
id: SKILL-REV-001
name: Revenue recognition
version: 0.1.0
status: review
primary_domain: "03"
related_domains: ["08", "09", "14", "15"]
description: Governed revenue recognition assessment, calculation and review pack.
triggers: [revenue recognition, accounting assessment, journal and disclosure review]
non_triggers: [legal advice, tax advice, unaudited assumption as fact]
framework_sensitivity: HIGH
applicable_frameworks: [IFRS, US_GAAP, UK_GAAP, AASB]
jurisdiction_sensitivity: HIGH
industry_sensitivity: HIGH
context_requirements:
  required: [customer_contract, enforceable_rights, performance_obligations, transaction_price, variable_consideration, recognition_pattern, reporting_period]
  retrieve_if_available: [entity_policy_elections, materiality, prior_period_workpapers, chart_of_accounts, disclosure_checklist]
inputs: [case_facts, evidence, framework_and_period, policy_elections, reviewed_assumptions]
outputs: [skill_result, accounting_memo, calculation_workpaper, journals, citations, review_items]
artifacts: [technical_memo, measurement_schedule, journal_pack, reconciliation, disclosure_support]
dependencies: [approved_topic_retrieval, company_context, deterministic_calculator, reviewer_signoff]
related_skills: [technical_accounting_research, disclosure_review, close_reconciliation]
knowledge_sources:
  principles: [TOPIC-03-001, TOPIC-03-002, TOPIC-03-003, TOPIC-03-004, TOPIC-03-005, TOPIC-03-006, TOPIC-03-012]
  standards: [TOPIC-03-001, TOPIC-03-002, TOPIC-03-003, TOPIC-03-004, TOPIC-03-005, TOPIC-03-006, TOPIC-03-012]
  practice: [TOPIC-03-001, TOPIC-03-002, TOPIC-03-003, TOPIC-03-004, TOPIC-03-005, TOPIC-03-006, TOPIC-03-012]
risk_level: HIGH
review_required: true
completion_criteria: [framework_and_period_resolved, all_required_facts_present, approved_claims_retrieved, method_and_judgments_documented, arithmetic_reconciled, journals_balance, citations_checked, reviewer_signoff]
---

# Revenue recognition — governed execution contract

IFRS 15 / ASC 606 / applicable FRS 102 / AASB 15. Apply the five-step model, separate non-revenue components, assess collectibility, distinct promises, series, variable consideration constraints, significant financing, stand-alone selling prices, allocation, point-in-time/over-time evidence, modifications, principal/agent, contract costs and balances. Never infer a contract judgment from numerical allocation alone.

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
Do not allocate unresolved variable consideration or book revenue without supported satisfaction evidence. FRS 102 must be period-gated; do not silently treat it as IFRS 15.

The skill is not production-complete until executable decision routes, period/framework tests, numerical regression, output boundary, and integration tests pass. A contract alone does not satisfy that gate.
