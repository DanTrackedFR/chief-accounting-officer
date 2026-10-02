---
id: SKILL-REC-001
name: Balance Sheet Reconciliations
version: 1.0.0
status: production
primary_domain: "02"
related_domains: ["02", "03", "04", "05", "07", "08", "09", "12"]
description: Governed balance sheet reconciliations with independently substantiated accounting inputs.
triggers: [balance sheet reconciliations]
non_triggers: [ERP posting, legal conclusions, tax advice, unsupported valuations]
framework_sensitivity: HIGH
applicable_frameworks: [IFRS, US_GAAP, UK_GAAP, AASB]
jurisdiction_sensitivity: HIGH
industry_sensitivity: MEDIUM
context_requirements:
  required: [case_id, entity, entity_type, jurisdiction, framework, period_start, reporting_period, execution_date, policy_elections, applicability_review, evidence, judgment_memo, controls, knowledge_review]
  retrieve_if_available: [comparatives, materiality, GL_mapping, prior_exceptions, source_extracts]
inputs: [trial_balance, inventory, reconciliations]
outputs: [skill_result, calculations, journals, reconciliations, judgments, controls, disclosures, specialist_handoff]
artifacts: [source_population_proof, calculation_workpaper, journal_pack, reconciliation, exception_register, reviewer_certification]
dependencies: [approved_topic_retrieval, company_context, independent_reviewer, deterministic_calculator]
related_skills: [revenue-recognition, financial-instruments-ecl, lease-accounting, asset-impairment, consolidation, financial-statements, foreign-currency]
knowledge_sources:
  principles: [TOPIC-02-004, TOPIC-02-005, TOPIC-02-008]
  standards: [TOPIC-02-004, TOPIC-02-005, TOPIC-02-008]
  practice: [TOPIC-02-004, TOPIC-02-005, TOPIC-02-008]
risk_level: HIGH
review_required: true
completion_criteria: [approved_knowledge_review, entity_period_policy_resolved, complete_source_population, numerical_reperformance, balanced_journals, gross_GL_reconciliation, adverse_route_review, qualified_citations, public_output_allowlist, independent_exact_case_certification]
---

# Balance Sheet Reconciliations

Execute through `production.assess_case("balance-sheet-reconciliations", case)` or `skills/run_skill.py`. Read canonical topic documents and registers first. Claim approval and directly verified authority are separate. Retain each actual evidence rating and audit requirement; paragraph references with unverified confidence remain expressly unverified. Never substitute this contract for period-specific approved knowledge.

Balanced TB, complete balance-sheet inventory including active zero accounts, independent source rollforward, bidirectional ID matching, quantified gross timing differences and absolute/relative/age gates; posted supported correcting adjustments and final GL tie-out.

Inventory is the independently approved complete balance-sheet account population; TB also contains non-balance-sheet accounts. Debit-positive signed account balances are used consistently. gl_closing is the frozen pre-adjustment balance and adjustments are confirmed posted subsequent entries.

Framework/jurisdiction gate: resolve actual IFRS edition, US entity/ASC adoption, FRS102 edition and pre/post-2026 adoption and policy elections, AASB compilation/tier and for-profit scope. Unsupported FRS101/105, NFP/public sector overlays and applicability exceptions block. Operational mechanics do not themselves create framework-specific recognition rules. Record transaction standards, jurisdictional requirements and source limitations in the independent applicability/judgment memo. No missing company facts or rates may be inferred. Prior errors versus changed estimates use IAS8, ASC250, FRS102 Section10 or AASB108 as appropriate.

Synthetic worked example: Opening prepaid 100,000 + additions 40,000 - consumption 15,000 = 125,000. GL 130,000 requires supported -5,000 correction, debit expense / credit prepaid, rather than a plug. Offsetting +5,000/-5,000 timing items retain gross exposure 10,000.

Recognition and error-versus-estimate conclusions remain with the underlying topic owner. Aged or unidentified items cannot be certified by this clean-certification route; remediate or obtain a separate conditional close decision.

Required evidence: immutable entity/book/currency source extract and query/version, period-end as-of, independent source count and absolute amount, completeness/cutoff assessment, contracts/receipts/remittances as applicable, current policy and estimate decisions, source-to-posting lineage, source-to-GL proofs and exception disposition. Each row approval names different owner/reviewer and matches the exact current row version. The separate execution_date must be on/after reporting cutoff; post-period preparation and approval are permitted through that execution date without backdating. Effective journal dates and actual posting/approval dates remain distinct. These are reviewed external records, not authenticated human identities.

Reviewer must reperform all supported calculation routes, inspect adverse alternatives and gross omissions, review material judgments and disclosures, verify specialist evidence and approve this exact case fingerprint. Missing/stale signoff returns partial; unresolved evidence, numerical or specialist routes return blocked without usable journals. An open exception cannot receive clean certification. No live ERP or collection communication is performed.

Public output uses the existing adapter for all seven routes. Only generated conclusions, numeric schedules, journals, disclosure requirements and curated caveats cross the boundary. Raw source notes, original memos, reviewer metadata, internal claim objects and hashes remain internal. Contamination blocks output. Disclosure outputs are a review checklist/workpaper, not automatically filed notes; Financial Statements assesses actual materiality, presentation and current/comparative completeness.

Production promotion requires comprehensive four-framework normal and adverse cases, numerical/period/evidence boundaries, stale-approval and output controls, independent contract QA, and full repository/lease/standards suites. A correct calculator alone is insufficient.
