# Skill Specification

A Skill is a bounded expert capability invoked by CAO orchestration. It is not a user-facing agent, accounting standard, domain, or static article.

## Required SKILL.md contract

Every production skill MUST declare:

```yaml
id:
name:
version:
status: draft|review|production|deprecated
primary_domain:
related_domains: []
description:
triggers: []
non_triggers: []
framework_sensitivity: NONE|LOW|MEDIUM|HIGH
applicable_frameworks: []
jurisdiction_sensitivity: NONE|LOW|MEDIUM|HIGH
industry_sensitivity: NONE|LOW|MEDIUM|HIGH
context_requirements:
  required: []
  retrieve_if_available: []
inputs: []
outputs: []
artifacts: []
dependencies: []
related_skills: []
knowledge_sources:
  principles: []
  standards: []
  practice: []
risk_level: LOW|MEDIUM|HIGH
review_required:
completion_criteria: []
```

## Execution contract

A skill MUST:
1. state its objective and boundary;
2. retrieve required context before concluding;
3. identify missing facts and distinguish assumptions from facts;
4. apply the relevant framework, jurisdiction, industry, and company overlays;
5. expose significant judgments and uncertainty;
6. return structured results to the CAO;
7. identify downstream accounting, control, reporting, audit, system, and documentation consequences;
8. satisfy explicit completion criteria.

A skill MUST NOT silently invent missing company facts, authoritative guidance, materiality, approvals, or evidence.

## Standard result envelope

```yaml
skill_result:
  skill_id:
  status: complete|partial|blocked|not_applicable
  conclusion:
  recommendation_class: REQUIRED|RECOMMENDED|WORLD_CLASS|SHORTCUT_RISK
  facts_used: []
  assumptions: []
  framework:
  jurisdiction:
  entities: []
  periods: []
  method:
  calculations: []
  evidence: []
  judgments: []
  uncertainties: []
  confidence: high|medium|low
  open_items: []
  journal_entry_implications: []
  controls_impacted: []
  reporting_impacted: []
  disclosures_impacted: []
  systems_impacted: []
  documentation_required: []
  audit_evidence_required: []
  related_artifacts: []
  memory_candidates: []
```

Not every field must contain a value, but the envelope MUST preserve the distinction between facts, assumptions, evidence, judgments, and conclusions.

## Skill package

A mature skill MAY contain:
- `SKILL.md` — contract and orchestration instructions;
- `methods/` — analytical procedures and workflows;
- `references/` — links into governed knowledge layers;
- `checklists/` — completeness/review checks;
- `templates/` — governed output structures;
- `examples/` — synthetic worked examples;
- `tests/` — routing, reasoning, completeness, and regression tests.

Framework-specific rules SHOULD live in standards knowledge rather than being duplicated across skills.

## Context requirements

`required` means the skill cannot responsibly complete without the fact or an explicit assumption. `retrieve_if_available` means orchestration SHOULD retrieve it because it may materially improve the work.

## Versioning and change

Material changes to a production skill MUST be versioned and tested. Deprecated skills MUST identify their replacement. Skill IDs SHOULD remain stable even when display names evolve.
