# Phase 2B Mapping QA

Date: 2026-09-22

## Results

- Topic rows: 157
- Capability rows in machine matrix: 347
- Unique capability IDs: 347
- Duplicate primary capability mappings: 0
- Orphan Phase 1 capabilities: 0
- Top-level topics: 157

## Sensitivity distribution

- H — standards-heavy: 68
- M — partial framework dependency: 51
- L — principles/practice-led: 21
- J — jurisdiction/regulatory-led: 17

## QA conclusion

The map passes structural coverage QA: every Phase 1 capability has exactly one primary top-level topic mapping. This does not mean a capability consumes only one topic at runtime. Cross-topic dependencies remain an orchestration concern.

The sensitivity classification is a build-planning classification, not an accounting conclusion. It can be refined during topic sourcing without changing the topic ID.

## Phase 2B conclusion

Checkpoint 2 is complete as a build map:
- denominator established at 157 top-level topics;
- 347/347 primary capability coverage proven;
- machine-readable and reverse mappings created;
- build waves defined;
- framework sensitivity classified.

Next checkpoint is Phase 2C: Leases vertical slice. Substantive accounting content begins only after checkpoint review/approval.
