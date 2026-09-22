# Company Context Schema

Structural schema for durable current-state company knowledge.

```yaml
context_item:
  id:
  category: corporate_profile|reporting_profile|accounting_function|systems_data|policies_positions|controls_evidence
  subject:
  attribute:
  value:
  scope:
    entities: []
    jurisdictions: []
    periods: []
  status: OBSERVED|CONFIRMED|DOCUMENTED|APPROVED|PROPOSED|SUPERSEDED
  confidence: high|medium|low
  effective_from:
  effective_to:
  learned_at:
  source_refs: []
  confirmed_by:
  approved_by:
  supersedes: []
  superseded_by: []
  related_cases: []
  related_decisions: []
  related_artifacts: []
  notes:
```

Current context is a temporal view over records, not a destructive overwrite of history. Conflicting records MUST remain resolvable by scope, status, effective date, source, and provenance.
