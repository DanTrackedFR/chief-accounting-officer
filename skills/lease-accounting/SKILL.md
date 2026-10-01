---
id: SKILL-LEASE-001
name: Lease accounting assessment and measurement
version: 0.1.0
status: review
primary_domain: "04"
related_domains: ["08", "12", "13"]
description: Assess lessee lease contracts and generate a documented measurement and journal pack.
triggers: [lease assessment, lease accounting, lease schedule, lease journal, lease modification, lease reassessment]
non_triggers: [lessor-only accounting, sale-and-leaseback without specialist handoff, legal contract drafting]
framework_sensitivity: HIGH
applicable_frameworks: [IFRS, US_GAAP, UK_GAAP, AASB]
jurisdiction_sensitivity: HIGH
industry_sensitivity: MEDIUM
context_requirements:
  required: [entity, framework, reporting_period, commencement_date, enforceable_contract, payment_schedule, lease_term_assessment, discount_rate_support]
  retrieve_if_available: [entity_policy_elections, comparative_periods, materiality, GL_mapping, lease_subledger]
inputs: [contract_facts, framework_and_period, payment_schedule, options_and_components, rate_and_elections]
outputs: [skill_result, assessment, calculation_schedule, journals, controls, citations]
artifacts: [lease_assessment, lease_term_memo, rate_memo, initial_measurement, liability_rollforward, journal_pack, disclosure_support]
dependencies: [approved_topic_retrieval, company_context, deterministic_calculator]
related_skills: [lease_modification, sale_and_leaseback, financial_statement_disclosure]
knowledge_sources:
  principles: [TOPIC-04-007, TOPIC-04-008, TOPIC-04-009, TOPIC-04-010]
  standards: [TOPIC-04-007, TOPIC-04-008, TOPIC-04-009, TOPIC-04-010, TOPIC-04-011]
  practice: [TOPIC-04-010, TOPIC-12-004]
risk_level: HIGH
review_required: true
completion_criteria: [framework_period_resolved, scope_and_term_documented, payments_and_rate_reconciled, schedule_balances, journals_balance, citations_verified_or_qualified, reviewer_signoff]
---

# Lease accounting skill — lessee vertical slice

Use this as the CAO orchestration contract. Never use the skill text as a substitute for the approved, period-specific topic knowledge. Retrieve the approved topics and their claim registers before deciding a framework-sensitive question.

## Execution
1. Resolve entity, jurisdiction, framework, annual-period start, adoption/early-adoption status and policy elections. For UK GAAP, distinguish pre-/post-2026 FRS 102 periods and FRS 105 or FRS 101 where relevant. For US GAAP, distinguish ASC 842 finance/operating and relevant entity alternatives. Do not assume identical IFRS/AASB treatment.
2. Inspect the enforceable contract and identify the asset, control of use, substitution rights, lease and non-lease components, exemptions and lessor/lessee roles. Record contract excerpts as internal evidence, not user-facing provenance.
3. Determine commencement, enforceable period, extension/termination and purchase options, reasonably-certain judgments and reassessment triggers. Do not silently equate contract signature with commencement.
4. Reconcile payment population, dates, currency, fixed/in-substance-fixed/index-linked/variable payments, residual guarantees, incentives, prepayments and direct costs. Exclude payments not included under the applicable framework.
5. Select and document the applicable discount rate, rate convention, periodicity and rate evidence. If essential inputs are missing, return partial or blocked rather than invent a rate.
6. Run the deterministic calculator for supported fixed-payment liability and IFRS/AASB-style ROU schedules. Apply framework-specific classification, amortization, presentation and impairment separately; never pass an IFRS straight-line ROU schedule off as ASC 842 operating accounting.
7. Produce initial and subsequent journals, reconcile to the lease subledger/GL, and identify disclosure, controls, audit and documentation implications.
8. On modification, reassessment, index reset, partial termination or sale-and-leaseback, retrieve TOPIC-04-009 or TOPIC-04-011 and run a separately reviewed event-specific calculation. Do not treat a generic liability refresh as the full modification method.
9. Cite the specific applicable standard and paragraph only when the reference is established in retrieved knowledge for the applicable period. A provisional paragraph is identified as unverified and must not be presented as a confirmed pinpoint citation.
10. Return the standard `skill_result` envelope from `architecture/skill-specification.md`, separating facts, assumptions, calculations, judgments, uncertainties and open items. Obtain reviewer sign-off before production use.

## Boundaries
The included calculator is an auditable numerical component, not an autonomous standards interpreter or a production retrieval/application integration. A successful numerical test does not approve a contract classification or a paragraph citation. Public output uses the established curated output contract.
