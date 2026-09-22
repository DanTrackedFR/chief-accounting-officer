# Framework Differences Record Schema

Differences are first-class knowledge objects.

```yaml
id: DIFF-<TOPIC>-<NNN>
topic_id:
issue:
status: draft|reviewed|approved|superseded
frameworks_compared: []
effective:
  from:
  to:
positions:
  IFRS:
    summary:
    source_ids: []
    paragraph_refs: []
  US_GAAP:
    summary:
    source_ids: []
    paragraph_refs: []
  UK_GAAP:
    summary:
    source_ids: []
    paragraph_refs: []
  AASB:
    summary:
    source_ids: []
    paragraph_refs: []
practical_consequence:
recognition_measurement_effect:
presentation_disclosure_effect:
process_system_effect:
documentation_effect:
decision_points: []
related_knowledge_records: []
related_skill_ids: []
source_checked_at:
review_status:
```

A differences record MUST explain a real divergence or explicitly document that a reviewed issue has no material divergence. It MUST NOT replace the underlying framework records.
