# Case Management

Substantive CAO work is managed as a Case. A Case is the durable work container for a task; it is not automatically Company Context.

## Case lifecycle

`OPEN → SCOPED → IN_PROGRESS → CHALLENGE → CONCLUDED → DOCUMENTED → CLOSED`

A case MAY be reopened. A later case MAY supersede a prior conclusion without deleting it.

## Minimum case record

```yaml
case_id:
title:
status:
objective:
requested_output:
opened_at:
closed_at:
entities: []
periods: []
frameworks: []
jurisdictions: []
industry_overlays: []
materiality:
facts:
  established: []
  assumed: []
  disputed: []
open_questions: []
issues: []
workplan_nodes: []
skills_invoked: []
knowledge_sources: []
evidence: []
judgments: []
alternatives_considered: []
conclusions: []
review_challenges: []
artifacts: []
decisions_created: []
memory_candidates: []
supersedes: []
superseded_by: []
```

## Workplan graph

Each node SHOULD identify capability, prerequisites, inputs, outputs, status, dependencies, evidence, and whether rework was triggered. Orchestration MAY add, remove, or revisit nodes as facts emerge.

## Challenge gate

Before a material case is concluded, the CAO MUST challenge:
- completeness of facts;
- applicability of framework/jurisdiction;
- plausible alternative accounting treatments;
- contradictory evidence;
- material judgments and estimates;
- consistency with approved policy and prior cases;
- downstream entries, controls, disclosures, systems, audit evidence, and documentation.

## Close gate

A case is CLOSED only when the requested output is delivered or explicitly blocked, material open items are visible, required artifacts are identified, and the Context Observer has run.
