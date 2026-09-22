# Knowledge-to-Skill Linking Contract

Skills consume knowledge; standards are not skills.

## Skill declaration
A standards-sensitive skill declares:
- topic IDs required;
- framework sensitivity;
- applicable frameworks;
- required Company Context;
- optional jurisdiction and industry overlays.

## Runtime retrieval
1. Determine objective and reporting period.
2. Resolve framework, entity and jurisdiction from Company Context/case.
3. Retrieve relevant topic records effective for the period.
4. Retrieve applicable DIFFERENCES records only when comparison or multi-framework work requires them.
5. Retrieve PRACTICE records separately from STANDARDS records.
6. Preserve source IDs and paragraph references in the case evidence trail.
7. Return structured skill result to CAO.

## Guardrails
- A skill MUST NOT infer a standards requirement solely from a PRACTICE record.
- Conflicting current records block a definitive conclusion until challenged/resolved.
- Superseded records may be used for historical periods but not silently for current periods.
- Missing required framework knowledge is surfaced as a knowledge gap, not filled by fabrication.
