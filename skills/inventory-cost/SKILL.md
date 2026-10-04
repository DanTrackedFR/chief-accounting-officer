---
id: SKILL-INV-001
name: "Inventory & Cost Accounting"
version: 0.1.0
status: review
primary_domain: "04"
related_domains: ["02", "04", "05", "06", "08", "13", "15"]
description: Governed ordinary inventory and manufacturing costing integrator with controlled sources, standard/actual variance accounting and fail-closed specialist boundaries.
triggers: ["Inventory & Cost Accounting", accounting assessment, journal and disclosure review]
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
related_skills: [fixed-assets, employee-benefits-payroll, accounts-payable, foreign-currency, revenue-recognition, agriculture-biological-assets, financial-statements, disclosure-management, accounting-systems-data-integrity, accounting-controls-icfr]
knowledge_sources:
  principles: []
  standards: []
  practice: [INVENTORY-KNOWLEDGE-MAP.json, methods.md]
risk_level: HIGH
review_required: true
completion_criteria: [approved_scope_and_period, full_source_population, current_evidence_and_approvals, supported_judgments, balanced_journals, all_account_GL_tie, complete_disclosure_review, privacy, independent_exact_fingerprint_certification, independent_QA, full_regression]
---

# Governed manufacturing accounting contract

The historical lack of Inventory authority is resolved by the independently approved owner-authorized `SUPPLEMENTAL_INVENTORY_COST` namespace: 228 claims, separately governed and not canonical topics. The existing package ID remains SKILL-INV-001. Candidate metadata remains review until implementation QA, complete regression and exact-head CI pass.

Ordinary commercial inventory in annual periods beginning and ending in 2026 is supported: full IFRS, ordinary US GAAP, full FRS102 September2024 and AASB Tier1 for-profit. Current edition/entity applicability and no early adoption require supplied independent sources. Approval preserves actual evidence ratings and outstanding direct-source audits.

Manufacturing is core: controlled BOM/material issues and original-layer production returns; routing hours; eligible direct labour; variable OH; fixed OH normal capacity; low-output unallocated expense; high-output caps; actual and standard cost; eight underlying signed standard variance measurements with actual company component/group reporting and independent normal/idle disposition; negative standard over-recovery; homogeneous component-equivalent WIP; job/batch/production-order/process collection; RM/WIP/FG source bridges; completion and inventory relief. Standard-to-actual approximation adjustments follow explicit component journals and stay separate from abnormal/idle expense.

Purchased/landed cost, FIFO, perpetual moving weighted average, noninterchangeable specific identification and controlled US unit LIFO layers are supported. US LIFO uses bounded replacement-cost market ceiling/floor; US FIFO/average use LCNRV. IFRS-family supported write-down reversals are capped by independently sourced prior write-down/original cost. US reversals remain prohibited. Raw-material indicators require current actual linked finished-goods cost/recovery evidence, preserving the IFRS/AASB recoverable-FG exception and independently reviewed US/UK lower-cost routes. Future-production raw contexts without current FG costing remain gated. Current item ageing/expiry/demand reviews, count/location population, actual ownership/cutoff, all GL offsets and framework-specific disclosure support are mandatory.

Qualified original source reports and actual current completed accounting-owner outputs are accepted. Numerical imports bind the original economic identity, eligible cost qualification, current entity/framework/period/currency, actual supported metric and source target once. Agriculture initial harvest recognition stays with Agriculture; Inventory consumes that actual entry basis without remeasurement or repeated gain/entry. Upstream payroll/depreciation/AP/FX are not recalculated. Downstream Inventory workpaper assertions expose reconciled balances and owner boundaries for future orchestration.

Unsupported routes fail closed: joint/by/co-products, retail technique, complex dollar-value LIFO pools/indexes, separate yield/mix variance decomposition, manufacturing purchase-PPV/consumption-price allocation, customer/vendor return recovery-owner adapters, heterogeneous stage-equivalent process WIP, standalone zero-output factory costing, class transfers, forecast creation, borrowing-cost capitalization, specialist commodity/broker exceptions, industry overlays, AASB Tier2/NFP and FRS102 reduced-disclosure overlays. Return layers require original issue identity and remaining quantity. Count adjustments currently support measured shortages; unsupported positive adjustments need a controlled acquisition/return basis. No inventory reserve percentages or production standards are invented.

Execute through `production.assess_case("inventory-cost", case)` and the existing seven-route public allowlist. Source notes, original records, claims metadata, reviewer identities and fingerprints stay internal. Independent case certification must match exact case/knowledge/implementation bytes and differ from the preparer; unsupported facts block without journals, missing/stale certification gives partial. Never post to an ERP or issue an audit opinion.
