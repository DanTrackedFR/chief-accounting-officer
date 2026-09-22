# Decision Register Schema

```yaml
decision:
  id:
  title:
  status: proposed|approved|implemented|reversed|superseded
  decision_date:
  effective_date:
  learned_at:
  previous_state:
  new_state:
  rationale_category: Accounting Standard|Accounting Policy|Accounting Judgment|Control|Process Design|Management Choice|Legacy / No Documented Rationale
  reason:
  drivers: []
  accounting_implications: []
  processes_impacted: []
  systems_impacted: []
  controls_impacted: []
  reporting_impacted: []
  entities: []
  framework:
  source_refs: []
  related_cases: []
  related_artifacts: []
  approved_by:
  confidence:
  supersedes: []
  superseded_by: []
```

A decision record explains **why**. A Company Context record states **what is true**. Material decisions normally update both without collapsing them into one record.
