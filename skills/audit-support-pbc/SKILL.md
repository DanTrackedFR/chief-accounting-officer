---
id: SKILL-PBC-001
name: "Audit Support & PBC Management"
version: 0.9.0
status: review
primary_domain: "10"
related_domains: ["02", "08", "14"]
description: Management PBC population reconciliation, auditor-selected sample support and factual query packages; no auditor conclusions.
triggers: [audit PBC management, audit support workpapers, audit query support]
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
related_skills: [financial-statements, month-end-close, accounting-changes, sec-filing-accounting]
knowledge_sources:
  principles: [TOPIC-10-001, TOPIC-10-002]
  standards: [TOPIC-10-001, TOPIC-10-002]
  practice: [GOVERNANCE-KNOWLEDGE-MAP.json, methods.md]
risk_level: HIGH
review_required: true
completion_criteria: [approved_scope, operative_framework_period, current_evidence, independent_population, deterministic_reconciliation, balanced_entries_where_applicable, disclosures, independent_exact_fingerprint_review, public_privacy, independent_QA, full_regression]

---

# Bounded execution contract

Management PBC population, source reconciliation, query and auditor-selected sample support only; no opinion, sufficiency/independence determination, confirmations, adjustments or accounting alteration.

Run production.assess_case("audit-support-pbc",case) through the existing CLI/public allowlist. Read methods.md, ../REVIEWER-CONTROLS.md and every frozen actual knowledge document before execution. APPROVED is separate from direct-source authority. Empty normative registers are approved practice, not invented claims.

Require exact entity/framework/jurisdiction/period, current qualified scope and actual controlled independent populations, source snapshots/versions/content hashes, source-to-output reconciliation and reviewer/preparer separation. Underlying recognition remains with actual completed accounting owners or reviewed specialist conclusions. Imports are complete, unaltered, current and evidence-only, never reposted. Missing/stale case approval is partial; contradictory/unsupported routes block. Full completion is only the declared workpaper, never accounting compliance or external readiness certification.

Public output is generated numeric/control workpaper and material limitations. Raw source contents, original memos, reviewer identities, evidence status/source notes and hashes remain internal across all seven routes. No communication, ERP posting, auditor procedure, legal/regulatory certification or filing occurs. Promotion requires individual knowledge sufficiency, comprehensive tests, genuine independent QA/remediation/rerun, examples, full regression and exact-head CI.
