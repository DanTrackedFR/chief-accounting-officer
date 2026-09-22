# Canonical Knowledge Record Schema

Every substantive Phase 2 knowledge item MUST conform to this contract.

```yaml
id: KR-<TOPIC>-<FRAMEWORK>-<NNN>
title:
topic_id:
subtopic:
record_type: PRINCIPLES|STANDARDS|PRACTICE|DIFFERENCES
framework: IFRS|US_GAAP|UK_GAAP|AASB|FRAMEWORK_INDEPENDENT
status: draft|reviewed|approved|superseded
version: 1.0.0

authority:
  source_ids: []
  standard_or_guidance:
  paragraph_refs: []
  authority_level: PRIMARY|OFFICIAL_INTERPRETIVE|REGULATOR|PROFESSIONAL_INTERPRETIVE|CAO_PRACTICE

effective:
  effective_from:
  effective_to:
  early_adoption:
  reporting_period_notes:
  supersedes: []
  superseded_by: []

applicability:
  transaction_or_balance:
  entity_types: []
  conditions: []
  exclusions: []

content:
  issue:
  cao_explanation:
  requirements_summary: []
  decision_points: []
  inputs_required: []
  exceptions: []
  calculations_required: []
  accounting_consequences: []
  journal_entry_implications: []
  presentation_implications: []
  disclosure_implications: []

judgment:
  significant_judgment: false
  judgments: []
  estimates: []
  uncertainties: []
  alternatives: []

execution:
  documentation_expected: []
  controls_considerations: []
  audit_evidence_considerations: []
  systems_data_considerations: []
  common_failure_modes: []

relationships:
  related_records: []
  related_difference_records: []
  related_skill_ids: []
  related_domains: []
  jurisdiction_overlays: []
  industry_overlays: []

provenance:
  source_checked_at:
  prepared_at:
  prepared_by:
  reviewed_at:
  reviewed_by:
  review_notes:
  copyright_classification:
  license_notes:
```

## Rules

- STANDARDS records MUST cite authoritative source IDs and paragraph references where meaningful.
- CAO-authored explanation MUST be independently written and distinguish requirements from interpretation/practice.
- Empty fields MAY be omitted only when genuinely inapplicable; N/A SHOULD be explicit where omission could imply incomplete work.
- Framework-independent operational topics SHOULD not manufacture standards analysis.
- Significant judgments MUST identify required facts, alternatives and documentation expectations.
- Records MUST be immutable in historical meaning: substantive changes create a new version and supersession link.
