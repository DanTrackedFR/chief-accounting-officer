# Provenance and History Schema

```yaml
history_event:
  id:
  event_type: learned|confirmed|approved|changed|implemented|superseded|corrected
  subject_ref:
  recorded_at:
  effective_at:
  effective_at_precision: exact|month|quarter|year|approximate|unknown
  previous_value:
  new_value:
  source_refs: []
  actor:
  reason:
  confidence:
  related_case:
  related_decision:
  related_artifacts: []
```

History is append-preserving. Corrections create new provenance; they do not erase the fact that an earlier state or understanding existed.
