# Phase 2 Knowledge Infrastructure Tests

## Schema fixture tests
- [x] Standards fixture can represent source, framework, effective period, applicability, judgments, execution and provenance.
- [x] Practice fixture can exist without masquerading as authoritative literature.
- [x] Difference schema can point to multiple framework records.
- [x] Source registry can express restrictive rights.
- [x] Supersession can preserve historical applicability.
- [x] Knowledge-to-skill contract prevents PRACTICE from becoming GAAP authority.

## Pre-production automated checks to implement with populated records
- unique IDs;
- valid enum values;
- source ID resolution;
- skill ID resolution;
- required source for STANDARDS;
- paragraph-reference verification state;
- effective-period handling;
- copyright classification;
- active-framework completion/N/A;
- difference coverage;
- no COMPLETE topic with draft required records;
- no prohibited source-body files.

## Human accounting QA
Machine validation does not establish technical accounting correctness. Production topic completion requires source-led accounting review and scenario testing.
