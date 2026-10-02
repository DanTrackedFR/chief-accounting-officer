---
id: SKILL-DEBT-001
name: "Debt, Borrowings & Financing Accounting"
version: 0.9.0
status: review
primary_domain: "06"
related_domains: ["02", "04", "05", "06", "08", "13", "15"]
description: Governed evidence-dependent accounting workflow with bounded calculations and fail-closed specialist routing.
triggers: ["Debt, Borrowings & Financing Accounting", accounting assessment, journal and disclosure review]
non_triggers: [automatic posting, legal opinion, autonomous valuation, filing, payroll processing]
framework_sensitivity: HIGH
applicable_frameworks: [IFRS, US_GAAP, UK_GAAP, AASB]
jurisdiction_sensitivity: HIGH
industry_sensitivity: HIGH
context_requirements:
  required: [case_id, entity, jurisdiction, framework, entity_type, period_start, reporting_period, policy_elections, evidence, judgment_memo, assumptions, applicability_review, knowledge_review]
  retrieve_if_available: [materiality, source_ledgers, regulatory_scope, prior_workpapers]
inputs: [independently_complete_source_population, reviewed_method, source_evidence, opening_balances, source_GL_statement_bridges, disclosure_checklist]
outputs: [skill_result, technical_memo, calculation_schedule, journal_pack, specialist_handoff]
artifacts: [reviewed_case, reconciliation, journals, partial_public_output, complete_public_output, certification]
dependencies: [approved_knowledge, company_context, independent_judgments, qualified_specialists, independent_review]
related_skills: [financial-instruments-ecl, going-concern, cash-flow-reporting, equity-capital, foreign-currency, accounting-changes]
knowledge_sources:
  principles: [TOPIC-06-005, TOPIC-06-006, TOPIC-06-007, TOPIC-13-006]
  standards: [TOPIC-06-005, TOPIC-06-006, TOPIC-06-007, TOPIC-13-006]
  practice: [FINANCING-KNOWLEDGE-MAP.json, methods.md]
risk_level: HIGH
review_required: true
completion_criteria: [approved_scope_and_period, full_source_population, current_evidence_and_approvals, supported_judgments, balanced_journals, all_account_GL_tie, complete_disclosure_review, privacy, independent_exact_fingerprint_certification, independent_QA, full_regression]
---

# Governed contract

Plain term-debt cost/proceeds bridge, independently supported periodic EIR schedule, contractual interest/repayments, separate legal principal, maturity population and supplied reporting-date current/noncurrent rights; full liability/cash/expense/GL bridge.

No autonomous legal, covenant waiver, restructuring, convertible, derivative, revolver or FVTPL accounting. Modification/extinguishment cannot continue an old yield; instrument specialist required. No automatic nominal-interest substitution.

Production promotion requires independent accounting QA, not calculator success.

1. Read methods.md, the actual mapped knowledge and claim registers, and ../REVIEWER-CONTROLS.md. The immutable batch map records actual claims, capabilities and unchanged ratings; SUPPLEMENTAL_TAX is a supplemental namespace, not a fabricated canonical topic.
2. Resolve actual framework, jurisdiction, entity/tier, effective editions, adoption/elections and exact reporting period. Unsupported FRS101/105, AASB non-profit/public-sector and unresolved exceptions fail closed.
3. Independently freeze source IDs, opening stocks, current flows, gross count/amount and GL/statement population. Evidence records and approval assertions are supplied facts, not authenticated identities or authority.
4. Select reviewed applicable claims; retain full document hashes. APPROVED is not SOURCE_VERIFIED. Unverified paragraph references remain qualified; source notes and reviewer metadata stay internal.
5. Invoke production.assess_case("debt-financing", case) through run_skill.py. Deterministic guarded Decimal calculations never infer legal rights, rates, quantities, forecasts or intentions. Resolve malformed/missing facts and specialist boundaries before completion.
6. Reperform balanced entries and every offset-to-opening/closing GL bridge, source/GL/statement ties and disclosure completeness. Imported governed results must be completed, current, dimension-matched, unaltered and exact-once.
7. Obtain independent reviewer certification tied to case, reviewed knowledge documents and implementation fingerprints. Missing/stale/non-independent certification gives partial; unresolved route gives blocked without accounting journals.
8. Public output must pass the existing seven-route allowlist. Only generated controlled schedules/journals and accounting caveats leave the boundary, never source notes, internal reviewer records or hashes.
9. Retain workpapers, exceptions, judgments, alternatives and rerun lineage. No ERP postings, tax returns, legal filings or counterparty communications are performed.

Synthetic worked examples are regression evidence only; their reviewer identities are never represented as actual company authorization.
