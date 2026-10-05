---
id: SKILL-ANALYTICS-001
name: "Management Reporting & Accounting Analytics"
version: 1.2.1
status: production
primary_domain: "08"
related_domains: ["01", "02", "11"]
description: Reconciled accounting reporting, factual flux, diagnostic driver bridges, supplied comparators, hypotheses and accounting-owner inquiries.
triggers: [management statutory bridge, accounting flux analysis, accounting KPI reporting, diagnostic analytics, accounting margin investigation]
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
  principles: [TOPIC-08-008, TOPIC-02-008, TOPIC-01-005, TOPIC-11-008]
  standards: [TOPIC-08-008, TOPIC-02-008, TOPIC-01-005, TOPIC-11-008]
  practice: [GOVERNANCE-KNOWLEDGE-MAP.json, methods.md]
risk_level: HIGH
review_required: true
completion_criteria: [approved_scope, operative_framework_period, current_evidence, independent_population, deterministic_reconciliation, balanced_entries_where_applicable, disclosures, independent_exact_fingerprint_review, public_privacy, independent_QA, full_regression]

---

# Bounded execution contract

Accounting-source lineage, management/statutory bridge, comparable factual flux, reconciliation timing metrics and bounded diagnostic analytics. Supplied approved budgets, forecasts, standards, targets and baselines may be analytical comparators; they never become accounting actual. No budget/forecast generation, planning ownership, optimization, generic BI, invented adjustments or undisclosed netting.

The optional `diagnostic` contract uses independently frozen source documents, complete disjoint driver populations, exact current accounting-owner components and reviewed comparator versions. Supported methods: signed source/owner flux; quantity/rate with interaction in current-quantity rate; explicit baseline-weighted price/volume/mix; reconciled gross-profit and margin-percentage-point bridges; threshold observations; evidence-tested hypotheses. Source dimensions, owner metrics and original economic component identities remain attached. Residuals are calculated and exposed without plugs; unknown or material residuals keep work partial. Accounting questions are structured inquiries bound to actual source metrics; the existing runtime rechecks the governed owner. Analytics creates no journals and does not decide recognition, capitalization or accounting adjustments.

Current diagnostic accounting metric bindings cover ordinary factory gross profit from actual Revenue and Inventory results, and signed owner-supported balance/expense/revenue components. Material/usage/labour/capacity explanations require controlled component schedules, never invented operational causes. FX, write-downs and close effects may appear only where their actual source movement is present, disjoint and reconciled. Missing or unsupported adapters remain open work. Arbitrary document ingestion, statistical causal inference, unsupplied comparators, operational optimization and full multi-entity graph execution remain outside scope. See methods.md for formulas and limitations.

Run production.assess_case("management-accounting-analytics",case) through the existing CLI/public allowlist. Read methods.md, ../REVIEWER-CONTROLS.md and every frozen actual knowledge document before execution. APPROVED is separate from direct-source authority. Empty normative registers are approved practice, not invented claims.

Require exact entity/framework/jurisdiction/period, current qualified scope and actual controlled independent populations, source snapshots/versions/content hashes, source-to-output reconciliation and reviewer/preparer separation. Underlying recognition remains with actual completed accounting owners or reviewed specialist conclusions. Imports are complete, unaltered, current and evidence-only, never reposted. Missing/stale case approval is partial; contradictory/unsupported routes block. Full completion is only the declared workpaper, never accounting compliance or external readiness certification.

Public output is generated numeric/control workpaper and material limitations. Raw source contents, original memos, reviewer identities, evidence status/source notes and hashes remain internal across all seven routes. No communication, ERP posting, auditor procedure, legal/regulatory certification or filing occurs. Promotion requires individual knowledge sufficiency, comprehensive tests, genuine independent QA/remediation/rerun, examples, full regression and exact-head CI.

## Governed balance and collections diagnostics (1.2.0)

Optional `balance_diagnostics: {doc: <reviewed document ID>}` consumes a complete
source-frozen preceding-month actual population and semantic current references
to Revenue, AR, ECL and FX owners. It calculates revenue/billings/bank collection
flux, full-bucket ageing movement, AR and signed contract-net bridges, allowance
movement, FX effect and unapplied cash. Every bridge exposes a residual. Current
allowance and recognised revenue are owner results, never Analytics estimates.
Current exposure is tied to AR and ECL. One separately reviewed contract net is
supported; unrelated contract balances cannot be offset or pooled by this method.

The bounded snapshot collection indicator is ending gross billed AR / period
net billings × actual calendar days, with the same numerator/denominator/day
convention in both periods. Complete calendar months and positive denominators
are required; invalid denominators remain unresolved. Prior net billings are
explicit supplied actuals. This is not rolling or revenue-based DSO and does not
become approved company policy. Annual billing mix and invoice timing limit it.
Monthly factual account comparison is additionally supported with a frozen
preceding-calendar-month source. No forecast or budget is generated.

The management explanation that collections only look worse because revenue
grew is tested against absolute governed bank collections and recognised revenue.
Falling cash with rising recognised revenue rejects that narrow hypothesis,
without inventing customer payment causes. Deteriorating ageing creates an ECL
inquiry; the runtime must recheck the governed ECL owner. Unresolved accounting
questions and material residuals prevent a clean close. No loss rates, FX rates,
accounting recognition, posting or external compliance certification are inferred.

## 1.2.1 integration correction
Qualified numeric owner references may address an exact array index or unique native row ID as well as dictionary fields. This permits existing owner_flux/rate_quantity methods to consume Debt and Hedge outputs. Bounds, row uniqueness, fresh actual owner execution and exact-case review remain required; no accounting or analytical method is added.
