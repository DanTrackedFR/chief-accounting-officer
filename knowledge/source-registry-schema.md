# Source Registry Schema

Every external source used in Phase 2 MUST be registered.

```yaml
source_id: SRC-<PUBLISHER>-<NNN>
publisher:
title:
source_type: STANDARD|INTERPRETATION|AGENDA_DECISION|REGULATOR|IMPLEMENTATION_GUIDANCE|PROFESSIONAL_GUIDANCE|OTHER
frameworks: []
jurisdictions: []
authority_level: PRIMARY|OFFICIAL_INTERPRETIVE|REGULATOR|PROFESSIONAL_INTERPRETIVE
official_url:
access_model: PUBLIC|REGISTRATION|SUBSCRIPTION|LICENSED
copyright_classification: REFERENCE_ONLY|PERMITTED_PUBLIC|LICENSED|UNKNOWN
allowed_repository_use:
  cite_title: true
  cite_paragraphs: true
  link: true
  reproduce_text: false
  ingest_source_text: false
effective_from:
effective_to:
last_verified:
supersedes: []
superseded_by: []
notes:
```

## Authority hierarchy

1. PRIMARY — authoritative standard-setter literature.
2. OFFICIAL_INTERPRETIVE — official interpretations, agenda decisions and implementation material.
3. REGULATOR — applicable regulator material.
4. PROFESSIONAL_INTERPRETIVE — reputable professional interpretation.
5. CAO_PRACTICE is internal knowledge and is not an external source class.

## Copyright rule

The registry controls what may be stored, quoted, linked or referenced. If rights are UNKNOWN, default to reference/link only and no reproduction or ingestion until resolved.
