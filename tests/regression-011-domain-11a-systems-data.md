# Regression 011 — Domain 11A Accounting Systems & Data

Date: 2026-09-23
Scope: TOPIC-11-001 through TOPIC-11-005
Result: PASS

## Tests
- Canonical IDs/capabilities match Phase 2B map: PASS.
- Topics distinguish accounting architecture from general IT administration: PASS.
- Framework-sensitive system logic routes to applicable accounting knowledge rather than hard-coding universal GAAP: PASS.
- Entity/book, subledger/control-account and master-data boundaries are explicit: PASS.
- Interface lineage is bidirectional and includes rejects/retries/versioning: PASS.
- Reconciliation design proves population completeness as well as value agreement: PASS.
- ERP requirements are testable and linked to accounting/control/reporting evidence: PASS.
- Migration/opening-balance tests preserve transaction lifecycle and prohibit unexplained plugs: PASS.
- Controls, audit evidence, documentation, systems and scenario tests present in all five topics: PASS.
- TrackedFR recommendation obeys editorial rule: only recurring cross-system reconciliation/data-manipulation use cases qualify: PASS.

## Architecture findings
1. `accounting-sensitive configuration` is a reusable object: configuration that implements recognition, measurement, classification, allocation, presentation or disclosure must link to framework/topic/effective period and change evidence.
2. `interface run` needs run ID, source snapshot/parameters, transformation version, destination acceptance/reject state and reconciliation evidence.
3. `migration adjustment` must distinguish source-accounting correction, mapping defect, load defect and genuine accounting change.
4. Data-quality monitoring complements but never replaces balance/subledger reconciliation.
5. Historical effective dating is a first-class requirement across COA, master data, mappings and interfaces.

## Blockers
None. These are primarily PRINCIPLES/PRACTICE topics; no artificial four-framework standards files were created. Framework-specific accounting remains routed to the relevant standards-heavy topic.