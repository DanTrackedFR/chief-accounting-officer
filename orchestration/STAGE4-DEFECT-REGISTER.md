# Stage 4 substrate defect register (implementation checkpoint)

## S4-D01 — material unresolved dependency cannot produce a retained blocked downstream version

Layer: VersionedExecution / VersionRegistry / CaseRegistry. Before remediation, an explicitly required unresolved bilateral match could not issue a safe current receipt; the runner either raised or, when only node status was inspected, a completed matching analysis could be mistaken for resolved accounting. The Group consumer had no retained blocked version with exact upstream bindings for subsequent correction invalidation.

Reproducer: `orchestration.tests.test_integrated_conflict_governance`. A generic Group observation receives both an actual Financial Statements result and an unresolved match. This is not a Stage 4 fixture/status override.

Minimum correction: derive blockers from actual required/material dependency bindings. Publish a schema-exact blocked governance record containing no accounting authority/journals, and preserve upstream version bindings. Reject fake complete publication and fabricated blocked records. Refuse current metric receipts from unresolved producers. Case refresh additionally recognizes unresolved producer payloads. Historical immutable versions and ordinary selective invalidation remain unchanged.

Authored validation: seven distinct regression methods PASS; existing Stage 3 + Stage 2 authored suites (84 methods) PASS. Independent QA and full release regression remain outstanding. This record does not claim final acceptance.
