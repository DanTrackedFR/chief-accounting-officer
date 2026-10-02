---
id: SKILL-GC-001
name: Going Concern & Liquidity Assessment
version: 0.9.0
status: review
primary_domain: "08"
related_domains: ["02", "05", "06", "08", "13", "15"]
description: Governed going concern & liquidity assessment using approved canonical knowledge and independently evidenced inputs.
triggers: [going concern & liquidity assessment]
non_triggers: [legal conclusions, unsupported valuation, fabricated evidence, autonomous filing]
framework_sensitivity: HIGH
applicable_frameworks: [IFRS, US_GAAP, UK_GAAP, AASB]
jurisdiction_sensitivity: HIGH
industry_sensitivity: HIGH
context_requirements:
  required: [case_id, entity, entity_type, jurisdiction, framework, period_start, reporting_period, execution_date, applicability_review, policy_elections, evidence, judgment_memo, controls, disclosure_review, knowledge_review]
  retrieve_if_available: [comparatives, materiality, source_extracts, GL_mapping, specialist_workpapers]
inputs: [assessment, scenarios, scenario_inventory, debt, debt_inventory, plans, sensitivities, management_review, handoffs]
outputs: [skill_result, calculations, journals, reconciliations, judgments, controls, disclosures, specialist_handoff]
artifacts: [source_population_proof, calculation_workpaper, journal_pack, reconciliation, exception_register, reviewer_certification]
dependencies: [approved_topic_retrieval, company_context, deterministic_calculator, independent_reviewer]
related_skills: [financial-statements, foreign-currency, consolidation, lease-accounting, provisions-contingencies, financial-instruments-ecl, share-based-compensation]
knowledge_sources:
  principles: [TOPIC-08-005, TOPIC-06-006]
  standards: [TOPIC-08-005, TOPIC-06-006]
  practice: [TOPIC-08-005, TOPIC-06-006]
risk_level: HIGH
review_required: true
completion_criteria: [approved_knowledge_review, entity_period_policy_resolved, complete_source_population, numerical_reperformance, balanced_journals, GL_reconciliation, adverse_route_review, qualified_citations, public_output_allowlist, independent_exact_case_certification]
---

# Going Concern & Liquidity Assessment

Run `production.assess_case("going-concern", case)` or `skills/run_skill.py`. The executable contract, supported branches, calculations, framework differences, evidence and examples are in [methods.md](methods.md). The actual canonical topics, capability IDs and immutable claim evidence ratings are recorded in [the mapping](../REPORTING-KNOWLEDGE-MAP.json). No canonical topic or claim is invented. Broader companion portions of shared topics are not automatically supported by this skill.

Retrieve the full approved topic method trees and original claim registers before classification. Knowledge review must match exact current document fingerprints and full framework claim population, selecting only applicable claims. APPROVED topic acceptance is separate from SOURCE_VERIFIED authority; preserve MODEL_DERIVED_AUDIT_REQUIRED, PRIMARY_CORROBORATED, SECONDARY_CORROBORATED and audit requirements. Provisional paragraph references stay explicitly unverified in curated public citations. SEC claims apply only to actual US registrants; unsupported reference or period never becomes verified by an approval memo.

Resolve actual IFRS edition, US entity adoption/filer scope, FRS102 edition and pre/post-2026 transitions, AASB for-profit compilation/tier, and actual jurisdiction. FRS101/105, NFP/public-sector or unsupported industry/tier overlays fail closed. Policy row must cover exact framework, entity and reporting period. No missing company fact, rate, management intent or legal conclusion is inferred. Nil populations require independent completeness evidence, not a missing key.

Source records require unique IDs, supported current-version approval, different owner/reviewer, approval not after execution date, complete independent source count/absolute amounts, inventories, economic cut-off and source/GL ties. Controls must retain original extract/query/version, contracts, source lineage, exceptions and disclosure checklist covering applicable comparative and narrative requirements. Raw records and hashes remain internal. Journals are review workpapers or validated imports; this skill cannot post to ERP, communicate externally, approve legal filings or manufacture specialist certification.

A qualified independent reviewer must reperform the route, calculations and journals, challenge population completeness, adverse cases, framework/period selection, citations, comparative/disclosure controls and specialist scope. Certification binds exact case, full approved knowledge and implementation fingerprints; absent/stale certification returns partial. Unresolved inputs, calculations or specialist evidence return blocked with no usable journal. The signature asserts supplied reviewed evidence; the repository does not authenticate a real human identity. Synthetic fixture signatures are for regression only.

All seven public-output routes use existing adapter allowlisting. Generated conclusions, numerical schedules, balanced journals, disclosure requirements and curated caveats are permitted. Internal source notes, confidence/evidence metadata, reviewer identities and fingerprints/hashes must not cross the boundary; contamination blocks rendering. The disclosure output is a controlled workpaper/checklist for Financial Statements review, not final filed notes. Public generated accounting judgments must not repeat raw memos.

Promotion requires full supported contract examples and adverse tests across four frameworks, independent accounting QA, complete shared/lease/repository/standards/approval validation and CI on frozen head SHA. Passing an initial calculator alone is insufficient.

